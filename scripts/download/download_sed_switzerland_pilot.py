#!/usr/bin/env python3
"""Swiss methods-transfer pilot: SED/ETH FDSN acquisition.

Downloads MiniSEED and StationXML for the configured Swiss candidate events.
Does not modify the frozen California v1.0.0 pipeline or write into IRIS paths.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable, TypeVar

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from obspy import UTCDateTime, read, read_inventory
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException

from src.acquisition.exceptions import AcquisitionRuntimeError
from src.acquisition.switzerland_pilot import (
    MANIFEST_FIELDS,
    attach_coordinates,
    acquisition_window,
    empty_manifest_row,
    event_short_id,
    group_availability_by_station,
    load_switzerland_config,
    location_label,
    parse_availability_text,
    sampling_rate_label,
    select_stations,
    utc_now_iso,
    validate_stream,
)

DEFAULT_CONFIG = REPO_ROOT / "configs" / "sed_switzerland_pilot.yaml"
T = TypeVar("T")
LOGGER = logging.getLogger("switzerland_pilot")

STOP_HTTP = {429, 503}


class SedServiceStop(RuntimeError):
    """Raised when SED/ETH FDSN must not be retried with a substitute provider."""


def _configure_swiss_logging(logs_dir: Path) -> Path:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "sed_switzerland_pilot.log"
    LOGGER.handlers.clear()
    LOGGER.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)
    LOGGER.propagate = False
    return log_path


def _http_get(url: str, timeout: int, user_agent: str = "AMGCR-SwitzerlandPilot/1.0") -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        if exc.code in STOP_HTTP:
            raise SedServiceStop(f"SED HTTP {exc.code} for {url}: {body[:300]}") from exc
        return exc.code, body
    except Exception as exc:  # noqa: BLE001
        raise SedServiceStop(f"SED request failed for {url}: {type(exc).__name__}: {exc}") from exc


def _retry(func: Callable[[], T], attempts: int, delay_seconds: float, label: str) -> T:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            return func()
        except SedServiceStop:
            raise
        except FDSNNoDataException:
            raise
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            LOGGER.warning("%s failed (attempt %s/%s): %s", label, attempt + 1, attempts, exc)
            if attempt + 1 < attempts:
                time.sleep(delay_seconds * (attempt + 1))
    assert last_error is not None
    raise last_error


def _join_url(base: str, path: str) -> str:
    return base.rstrip("/") + "/" + path.lstrip("/")


def fetch_sed_catalog_text(config: dict[str, Any], timeout: int) -> str:
    """Retrieve the SED event catalogue as FDSN text. Does not use USGS/IRIS."""
    catalog = config["catalog"]
    query = (
        f"starttime={catalog['starttime']}&endtime={catalog['endtime']}"
        f"&minmagnitude={catalog['minmagnitude']}"
        f"&minlatitude={catalog['minlatitude']}&maxlatitude={catalog['maxlatitude']}"
        f"&minlongitude={catalog['minlongitude']}&maxlongitude={catalog['maxlongitude']}"
        f"&format={catalog.get('format', 'text')}&nodata=404"
    )
    url = _join_url(config["endpoints"]["event"], "query") + "?" + query
    LOGGER.info("catalog_query %s", url)
    code, body = _http_get(url, timeout=timeout)
    if code != 200:
        raise SedServiceStop(f"SED event catalogue HTTP {code}: {body[:300]}")
    return body


def parse_sed_catalog_text(text: str) -> dict[str, dict[str, Any]]:
    """Index catalogue rows by short event ID."""
    by_id: dict[str, dict[str, Any]] = {}
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) < 14:
            continue
        resource_id = parts[0].strip()
        short_id = event_short_id(resource_id)
        by_id[short_id] = {
            "event_id": resource_id,
            "short_id": short_id,
            "origin_time_utc": parts[1].strip(),
            "latitude": float(parts[2]),
            "longitude": float(parts[3]),
            "depth_km": float(parts[4]) if parts[4] else "",
            "magnitude_type": parts[9].strip(),
            "magnitude": float(parts[10]) if parts[10] else "",
            "region": parts[12].strip(),
            "event_type": parts[13].strip(),
            "contributor": parts[7].strip(),
        }
    return by_id


def fetch_ch_station_coords(config: dict[str, Any], timeout: int) -> dict[str, dict[str, Any]]:
    """CH broadband (HH/BH) station coordinates from fdsnws-station."""
    url = (
        _join_url(config["endpoints"]["station"], "query")
        + "?network=CH&channel=HH?,BH?&format=text&level=station&nodata=404"
    )
    LOGGER.info("station_inventory_query %s", url)
    code, body = _http_get(url, timeout=timeout)
    if code != 200:
        raise SedServiceStop(f"SED station inventory HTTP {code}: {body[:300]}")
    coords: dict[str, dict[str, Any]] = {}
    for line in body.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) < 8:
            continue
        coords[parts[1]] = {
            "network": parts[0],
            "station": parts[1],
            "latitude": float(parts[2]),
            "longitude": float(parts[3]),
            "site": parts[5],
            "start": parts[6],
            "end": parts[7],
        }
    LOGGER.info("ch_broadband_stations_in_inventory %s", len(coords))
    return coords


def _availability_query(
    config: dict[str, Any],
    stations: list[str],
    start: UTCDateTime,
    end: UTCDateTime,
    timeout: int,
) -> tuple[int, str]:
    selection = config["station_selection"]
    sta_csv = ",".join(stations)
    url = (
        _join_url(config["endpoints"]["availability"], "query")
        + f"?network={selection['network']}&station={sta_csv}"
        + f"&channel={selection['availability_channels']}"
        + f"&starttime={start.strftime('%Y-%m-%dT%H:%M:%S')}"
        + f"&endtime={end.strftime('%Y-%m-%dT%H:%M:%S')}"
        + "&format=text&nodata=404"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "AMGCR-SwitzerlandPilot/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        if exc.code in STOP_HTTP:
            raise SedServiceStop(f"SED availability HTTP {exc.code}: {body[:300]}") from exc
        return exc.code, body
    except urllib.error.URLError as exc:
        return 0, f"URLError: {exc}"
    except TimeoutError as exc:
        return 0, f"TimeoutError: {exc}"


def query_availability_for_event(
    config: dict[str, Any],
    station_names: list[str],
    start: UTCDateTime,
    end: UTCDateTime,
    timeout: int,
    sleep_s: float,
) -> list[dict[str, Any]]:
    """Batch availability queries. 404/204 means no data for that batch, not a stop."""
    batch_size = int(config["station_selection"].get("availability_station_batch_size", 8))
    rows: list[dict[str, Any]] = []
    for offset in range(0, len(station_names), batch_size):
        batch = station_names[offset : offset + batch_size]
        code, body = _availability_query(config, batch, start, end, timeout)
        time.sleep(sleep_s)
        if code in {204, 404}:
            LOGGER.info("availability_batch empty HTTP %s stations=%s", code, batch)
            continue
        if code != 200:
            LOGGER.warning("availability_batch HTTP %s stations=%s body=%s", code, batch, body[:180])
            continue
        parsed = parse_availability_text(body)
        rows.extend(parsed)
    return rows


def download_station_waveforms(
    client: Client,
    candidate: Any,
    start: UTCDateTime,
    end: UTCDateTime,
    event_dir: Path,
    origin: UTCDateTime,
    attempts: int,
    delay: float,
) -> tuple[Path | None, Stream | None, str]:
    """Download one MiniSEED file per event-station (all selected components)."""
    loc = candidate.location
    loc_label = location_label(loc)
    band = candidate.preferred_band or "HH"
    channel_wildcard = f"{band}?"
    filename = (
        f"{candidate.network}.{candidate.station}.{loc_label}.{band}."
        f"{origin.strftime('%Y%m%dT%H%M%S')}.mseed"
    )
    path = event_dir / filename

    def _fetch() -> Stream:
        return client.get_waveforms(
            network=candidate.network,
            station=candidate.station,
            location=loc if loc else "",
            channel=channel_wildcard,
            starttime=start,
            endtime=end,
        )

    try:
        stream = _retry(_fetch, attempts=attempts, delay_seconds=delay, label=f"dataselect {candidate.station}")
    except FDSNNoDataException:
        return None, None, "NO_DATA"
    except SedServiceStop:
        raise
    except Exception as exc:  # noqa: BLE001
        LOGGER.error("waveform_download_failed station=%s error=%s", candidate.station, exc)
        return None, None, f"FAILED:{type(exc).__name__}"

    if stream is None or len(stream) == 0:
        return None, None, "NO_DATA"
    event_dir.mkdir(parents=True, exist_ok=True)
    stream.merge(method=1, fill_value="interpolate")
    stream.write(str(path), format="MSEED")
    if path.stat().st_size <= 0:
        return None, None, "FAILED:empty_file"
    return path, stream, "OK"


def download_stationxml(
    client: Client,
    candidate: Any,
    start: UTCDateTime,
    end: UTCDateTime,
    metadata_event_dir: Path,
    attempts: int,
    delay: float,
) -> tuple[Path | None, str]:
    """Save StationXML (level=response) beside the event; do not alter MiniSEED."""
    loc = candidate.location
    loc_label = location_label(loc)
    band = candidate.preferred_band or "HH"
    filename = f"{candidate.network}.{candidate.station}.{loc_label}.{band}.xml"
    path = metadata_event_dir / filename

    def _fetch():
        return client.get_stations(
            network=candidate.network,
            station=candidate.station,
            location=loc if loc else "",
            channel=f"{band}?",
            starttime=start,
            endtime=end,
            level="response",
        )

    try:
        inventory = _retry(_fetch, attempts=attempts, delay_seconds=delay, label=f"stationxml {candidate.station}")
    except FDSNNoDataException:
        return None, "NO"
    except SedServiceStop:
        raise
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("stationxml_failed station=%s error=%s", candidate.station, exc)
        return None, "NO"

    if inventory is None or len(inventory) == 0:
        return None, "NO"
    metadata_event_dir.mkdir(parents=True, exist_ok=True)
    inventory.write(str(path), format="STATIONXML")
    return path, "YES"


def write_manifest(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(MANIFEST_FIELDS), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in MANIFEST_FIELDS})


def run_response_tests(
    config: dict[str, Any],
    rows: list[dict[str, Any]],
    reports_dir: Path,
) -> list[dict[str, Any]]:
    """Technical remove_response() check on a small subset. Does not overwrite raw files."""
    test_cfg = config.get("response_test") or {}
    if not test_cfg.get("enabled", False):
        return []
    wanted_events = set(test_cfg.get("event_ids") or [])
    max_stations = int(test_cfg.get("max_stations_per_event", 3))
    output = str(test_cfg.get("output", "VEL"))
    water_level = float(test_cfg.get("water_level", 60.0))
    pre_filt = test_cfg.get("pre_filt")

    eligible = [
        row
        for row in rows
        if event_short_id(str(row.get("event_id", ""))) in wanted_events
        and row.get("download_status") == "OK"
        and row.get("stationxml_available") == "YES"
        and row.get("waveform_file")
    ]
    by_event: dict[str, list[dict[str, Any]]] = {}
    for row in eligible:
        by_event.setdefault(event_short_id(str(row["event_id"])), []).append(row)

    results: list[dict[str, Any]] = []
    for event_id, event_rows in by_event.items():
        for row in event_rows[:max_stations]:
            waveform_path = REPO_ROOT / str(row["waveform_file"])
            xml_name = Path(str(row["waveform_file"]).replace("data/raw/switzerland", "data/metadata/switzerland"))
            xml_path = REPO_ROOT / xml_name.with_suffix(".xml")
            # Reconstruct StationXML path from waveform stem with band suffix already in name
            meta_dir = REPO_ROOT / config["output"]["metadata_dir"] / event_id
            station = row["station"]
            loc = location_label(str(row.get("location") or ""))
            xml_candidates = list(meta_dir.glob(f"CH.{station}.{loc}.*.xml"))
            record: dict[str, Any] = {
                "event_id": event_id,
                "station": station,
                "channel": row.get("channels", ""),
                "units_before": "counts",
                "units_after": "",
                "response_test_status": "FAIL",
                "exception_if_failed": "",
                "waveform_file": str(row["waveform_file"]),
            }
            try:
                if not xml_candidates:
                    raise FileNotFoundError(f"StationXML not found in {meta_dir} for {station}")
                xml_path = xml_candidates[0]
                stream = read(str(waveform_path))
                inventory = read_inventory(str(xml_path))
                kwargs: dict[str, Any] = {
                    "inventory": inventory,
                    "output": output,
                    "water_level": water_level,
                }
                if pre_filt:
                    kwargs["pre_filt"] = tuple(pre_filt)
                stream.remove_response(**kwargs)
                record["units_after"] = "m/s" if output == "VEL" else output
                record["response_test_status"] = "PASS"
                record["stationxml_file"] = str(xml_path.relative_to(REPO_ROOT)).replace("\\", "/")
                LOGGER.info("response_test PASS event=%s station=%s", event_id, station)
            except Exception as exc:  # noqa: BLE001
                record["exception_if_failed"] = f"{type(exc).__name__}: {exc}"
                LOGGER.warning("response_test FAIL event=%s station=%s error=%s", event_id, station, exc)
            results.append(record)

    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path = reports_dir / "response_test.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    LOGGER.info("response_test_written %s n=%s", out_path, len(results))
    return results


def summarize(rows: list[dict[str, Any]], catalog_missing: list[str], response_tests: list[dict[str, Any]]) -> dict[str, Any]:
    acquired_events = sorted({event_short_id(str(r["event_id"])) for r in rows if r.get("download_status") == "OK"})
    ok_rows = [r for r in rows if r.get("download_status") == "OK"]
    return {
        "generated_utc": utc_now_iso(),
        "candidate_event_count": 20,
        "catalog_missing_event_ids": catalog_missing,
        "successfully_acquired_events": len(acquired_events),
        "acquired_event_ids": acquired_events,
        "event_station_waveform_records": len(ok_rows),
        "complete_3c_records": sum(1 for r in ok_rows if r.get("validation_status") in {"PASS", "PARTIAL"} and "incomplete three-component" not in str(r.get("validation_status", ""))),
        "records": len(rows),
        "download_ok": len(ok_rows),
        "validation_pass": sum(1 for r in rows if r.get("validation_status") == "PASS"),
        "validation_partial": sum(1 for r in rows if r.get("validation_status") == "PARTIAL"),
        "validation_fail": sum(1 for r in rows if r.get("validation_status") == "FAIL"),
        "stationxml_yes": sum(1 for r in ok_rows if r.get("stationxml_available") == "YES"),
        "pre_event_ge_60": sum(
            1
            for r in ok_rows
            if r.get("pre_event_seconds") not in {"", None} and float(r["pre_event_seconds"]) >= 60.0
        ),
        "failed_records": [
            {
                "event_id": r.get("event_id"),
                "station": r.get("station"),
                "download_status": r.get("download_status"),
                "validation_status": r.get("validation_status"),
            }
            for r in rows
            if r.get("download_status") != "OK" or r.get("validation_status") == "FAIL"
        ],
        "response_tests": response_tests,
    }


def run(config_path: Path) -> int:
    config = load_switzerland_config(config_path)
    output = config["output"]
    logs_dir = REPO_ROOT / output["logs_dir"]
    log_path = _configure_swiss_logging(logs_dir)
    LOGGER.info("switzerland_pilot_start config=%s log=%s", config_path, log_path)
    LOGGER.info("endpoints %s", json.dumps(config["endpoints"]))

    retry = config.get("retry") or {}
    timeout = int(retry.get("timeout_seconds", 60))
    attempts = int(retry.get("attempts", 3))
    delay = float(retry.get("delay_seconds", 1.0))
    sleep_s = float(retry.get("sleep_between_requests_seconds", 0.35))
    window = config["window"]
    selection = config["station_selection"]

    catalog_text = fetch_sed_catalog_text(config, timeout=max(timeout, 90))
    catalog = parse_sed_catalog_text(catalog_text)
    wanted = [event_short_id(item) for item in config["event_ids"]]
    missing = [eid for eid in wanted if eid not in catalog]
    if missing:
        LOGGER.error("catalog_missing_ids %s — stopping rather than inventing hypocentres", missing)
        raise SedServiceStop(f"SED catalogue did not return required event IDs: {missing}")

    station_coords = fetch_ch_station_coords(config, timeout=max(timeout, 90))
    if not station_coords:
        raise SedServiceStop("SED station inventory returned no CH stations.")
    station_names = sorted(station_coords.keys())

    client = Client(config["endpoints"].get("obspy_client_base") or "https://eida.ethz.ch", timeout=timeout)
    raw_root = REPO_ROOT / output["raw_dir"]
    meta_root = REPO_ROOT / output["metadata_dir"]
    reports_dir = REPO_ROOT / output.get("reports_dir", "reports/switzerland_pilot")
    rows: list[dict[str, Any]] = []

    for short_id in wanted:
        event = catalog[short_id]
        origin = UTCDateTime(event["origin_time_utc"])
        start, end = acquisition_window(origin, window["pre_event_seconds"], window["post_event_seconds"])
        LOGGER.info(
            "event %s origin=%s window=%s..%s mag=%s region=%s",
            short_id,
            event["origin_time_utc"],
            start,
            end,
            event["magnitude"],
            event["region"],
        )
        avail_rows = query_availability_for_event(config, station_names, start, end, timeout, sleep_s)
        candidates = group_availability_by_station(
            avail_rows,
            origin,
            float(window["pre_event_seconds"]),
            float(window["post_event_seconds"]),
            network=selection["network"],
        )
        attach_coordinates(candidates, station_coords, float(event["latitude"]), float(event["longitude"]))
        chosen = select_stations(
            candidates,
            max_stations=int(selection.get("max_stations_per_event", 6)),
            bin_edges_km=[float(x) for x in selection.get("distance_bins_km", [0, 50, 100, 150, 250, 400])],
            max_per_bin=int(selection.get("max_stations_per_bin", 2)),
            prefer_three_component=bool(selection.get("prefer_three_component", True)),
            allow_incomplete=bool(selection.get("allow_incomplete_three_component", False)),
        )
        LOGGER.info("event %s availability_rows=%s candidates=%s selected=%s", short_id, len(avail_rows), len(candidates), [c.station for c in chosen])

        if not chosen:
            rows.append(
                empty_manifest_row(
                    event,
                    network=selection["network"],
                    download_status="NO_SUITABLE_STATION",
                    validation_status="NOT_RUN",
                )
            )
            continue

        event_dir = raw_root / short_id
        meta_dir = meta_root / short_id
        for candidate in chosen:
            time.sleep(sleep_s)
            wave_path, stream, dl_status = download_station_waveforms(
                client, candidate, start, end, event_dir, origin, attempts, delay
            )
            time.sleep(sleep_s)
            xml_path, xml_flag = download_stationxml(client, candidate, start, end, meta_dir, attempts, delay)

            validation_status = "NOT_RUN"
            pre_s: Any = ""
            post_s: Any = ""
            channels = ";".join(candidate.download_channels)
            rates = sampling_rate_label(candidate.sample_rates_hz, candidate.preferred_band)
            w_start = ""
            w_end = ""
            rel_wave = ""

            if stream is not None and wave_path is not None:
                validation = validate_stream(
                    stream,
                    origin,
                    float(window["min_pre_event_seconds"]),
                    float(window["min_post_event_seconds"]),
                )
                validation_status = validation.status
                pre_s = validation.pre_event_seconds if validation.pre_event_seconds is not None else ""
                post_s = validation.post_event_seconds if validation.post_event_seconds is not None else ""
                channels = ";".join(validation.channels) if validation.channels else channels
                rates = validation.sampling_rate_hz or rates
                w_start = validation.starttime
                w_end = validation.endtime
                rel_wave = str(wave_path.relative_to(REPO_ROOT)).replace("\\", "/")
                if validation.notes:
                    LOGGER.info("validation %s %s %s notes=%s", short_id, candidate.station, validation.status, validation.notes)
            else:
                validation_status = "FAIL"

            rows.append(
                empty_manifest_row(
                    event,
                    network=candidate.network,
                    station=candidate.station,
                    location=location_label(candidate.location),
                    channels=channels,
                    sampling_rate_hz=rates,
                    waveform_start_utc=w_start,
                    waveform_end_utc=w_end,
                    pre_event_seconds=pre_s,
                    post_event_seconds=post_s,
                    stationxml_available=xml_flag,
                    waveform_file=rel_wave,
                    download_status=dl_status,
                    validation_status=validation_status,
                )
            )

    manifest_path = REPO_ROOT / output["manifest_csv"]
    write_manifest(manifest_path, rows)
    LOGGER.info("manifest_written %s rows=%s", manifest_path, len(rows))

    response_tests = run_response_tests(config, rows, reports_dir)
    summary = summarize(rows, missing, response_tests)
    # Count complete 3C from validation notes / channel lists more accurately
    ok_rows = [r for r in rows if r.get("download_status") == "OK"]
    complete_3c = 0
    for row in ok_rows:
        chans = set(str(row.get("channels") or "").replace(",", ";").split(";"))
        chans.discard("")
        bands = {ch[:2] for ch in chans if len(ch) >= 3}
        if any({f"{band}Z", f"{band}N", f"{band}E"}.issubset(chans) for band in bands):
            complete_3c += 1
    summary["complete_3c_records"] = complete_3c
    reports_dir.mkdir(parents=True, exist_ok=True)
    summary_path = reports_dir / "acquisition_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    LOGGER.info("summary_written %s", summary_path)
    LOGGER.info(
        "switzerland_pilot_complete acquired_events=%s records_ok=%s 3c=%s stationxml=%s",
        summary["successfully_acquired_events"],
        summary["download_ok"],
        complete_3c,
        summary["stationxml_yes"],
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download the Swiss SED methods-transfer pilot dataset.")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="Path to configs/sed_switzerland_pilot.yaml",
    )
    args = parser.parse_args(argv)
    try:
        return run(Path(args.config))
    except SedServiceStop as exc:
        LOGGER.error("STOP: %s", exc)
        print(f"STOP: {exc}", file=sys.stderr)
        return 2
    except AcquisitionRuntimeError as exc:
        LOGGER.error("acquisition_runtime %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
