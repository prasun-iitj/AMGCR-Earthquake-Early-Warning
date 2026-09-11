#!/usr/bin/env python3
"""STEP 2J: acquire locked Set C validation MiniSEED and StationXML.

Does not run STA/LTA, compute validation metrics, retune 8.0, or reselection Set C.
Does not modify California v1.0.0 or the 20-event Swiss development set.
"""

from __future__ import annotations

import argparse
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
from src.acquisition.switzerland_pilot import event_short_id, parse_availability_text
from src.acquisition.switzerland_validation_acquisition import (
    PICK_MANIFEST_FIELDS,
    WAVEFORM_MANIFEST_FIELDS,
    acquisition_interval,
    empty_pick_row,
    empty_waveform_row,
    inspect_miniseed_stream,
    load_validation_acquisition_config,
    locked_set_c_ids,
    proposed_events_from_candidate_csv,
    quakeml_eventid_candidates,
    select_same_station_hhz_targets,
    stationxml_filename,
    stationxml_hhz_status,
    summarize_acquisition,
    utc_now_iso,
    waveform_filename,
    write_csv,
)
from src.acquisition.switzerland_validation_audit import parse_quakeml_picks

DEFAULT_CONFIG = REPO_ROOT / "configs" / "sed_switzerland_validation_acquisition.yaml"
T = TypeVar("T")
LOGGER = logging.getLogger("switzerland_validation_acquisition")
STOP_HTTP = {429, 503}


class SedServiceStop(RuntimeError):
    """Raised when SED/ETH FDSN must not be retried with a substitute provider."""


def _configure_logging(logs_dir: Path, log_name: str) -> Path:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / log_name
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


def _join_url(base: str, path: str) -> str:
    return base.rstrip("/") + "/" + path.lstrip("/")


def _http_get(url: str, timeout: int) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "AMGCR-SwitzerlandValidationAcquisition/1.0"})
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


def fetch_ch_station_names(audit: dict[str, Any], timeout: int) -> list[str]:
    url = (
        _join_url(audit["endpoints"]["station"], "query")
        + "?network=CH&channel=HH?&format=text&level=station&nodata=404"
    )
    LOGGER.info("station_inventory_query %s", url)
    code, body = _http_get(url, timeout=timeout)
    if code != 200:
        raise SedServiceStop(f"SED station inventory HTTP {code}: {body[:300]}")
    names = []
    for line in body.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) >= 2:
            names.append(parts[1])
    unique = sorted(set(names))
    LOGGER.info("ch_hh_stations_in_inventory %s", len(unique))
    return unique


def _availability_query(
    audit: dict[str, Any],
    stations: list[str],
    start: UTCDateTime,
    end: UTCDateTime,
    timeout: int,
) -> tuple[int, str]:
    selection = audit["station_selection"]
    url = (
        _join_url(audit["endpoints"]["availability"], "query")
        + f"?network={selection['network']}&station={','.join(stations)}"
        + f"&channel={selection['availability_channels']}"
        + f"&starttime={start.strftime('%Y-%m-%dT%H:%M:%S.%f')}"
        + f"&endtime={end.strftime('%Y-%m-%dT%H:%M:%S.%f')}"
        + "&format=text&nodata=404"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "AMGCR-SwitzerlandValidationAcquisition/1.0"})
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


def query_availability_rows(
    audit: dict[str, Any],
    station_names: list[str],
    start: UTCDateTime,
    end: UTCDateTime,
    timeout: int,
    sleep_s: float,
) -> list[dict[str, Any]]:
    batch_size = int(audit["station_selection"].get("availability_station_batch_size", 10))
    rows: list[dict[str, Any]] = []
    for offset in range(0, len(station_names), batch_size):
        batch = station_names[offset : offset + batch_size]
        code, body = _availability_query(audit, batch, start, end, timeout)
        time.sleep(sleep_s)
        if code in {204, 404}:
            continue
        if code != 200:
            LOGGER.warning("availability_batch HTTP %s stations=%s body=%s", code, batch, body[:180])
            continue
        rows.extend(parse_availability_text(body))
    return rows


def fetch_event_quakeml(audit: dict[str, Any], event_id: str, timeout: int) -> tuple[int, str, str]:
    url = (
        _join_url(audit["endpoints"]["event"], "query")
        + f"?eventid={event_id}&format=xml&includearrivals=true&nodata=404"
    )
    LOGGER.info("quakeml_event_query %s", url)
    code, body = _http_get(url, timeout=timeout)
    return code, body, url


def load_picks_for_event(audit: dict[str, Any], event: dict[str, Any], timeout: int, sleep_s: float) -> list[dict[str, Any]]:
    short_id = event["short_id"]
    resource = str(event.get("event_id") or "")
    last_code = 0
    for candidate in quakeml_eventid_candidates(short_id, resource):
        code, body, url = fetch_event_quakeml(audit, candidate, timeout)
        last_code = code
        time.sleep(sleep_s)
        if code == 200 and body:
            parsed = parse_quakeml_picks(body)
            picks = parsed.get(short_id) or []
            if not picks and parsed:
                picks = next(iter(parsed.values()))
            LOGGER.info("quakeml_ok event=%s query=%s n_picks=%s", short_id, candidate, len(picks))
            return picks
        LOGGER.info("quakeml_miss event=%s query=%s http=%s", short_id, candidate, code)
    LOGGER.warning("quakeml_unavailable event=%s last_http=%s", short_id, last_code)
    return []


def _relative(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def _request_params(network: str, station: str, location: str, channel: str, start: UTCDateTime, end: UTCDateTime) -> str:
    loc = location if location else ""
    return (
        f"network={network}&station={station}&location={loc or '--'}&channel={channel}"
        f"&starttime={start}&endtime={end}&provider=https://eida.ethz.ch/fdsnws/dataselect/1/"
    )


def download_hhz_miniseed(
    client: Client,
    *,
    network: str,
    station: str,
    location: str,
    start: UTCDateTime,
    end: UTCDateTime,
    path: Path,
    attempts: int,
    delay: float,
) -> tuple[Path | None, Any, str]:
    if path.exists() and path.stat().st_size > 0:
        try:
            stream = read(str(path))
            return path, stream, "ok_existing"
        except Exception as exc:  # noqa: BLE001
            return None, None, f"existing_unreadable:{type(exc).__name__}"

    loc = location if location else ""

    def _fetch():
        return client.get_waveforms(
            network=network,
            station=station,
            location=loc,
            channel="HHZ",
            starttime=start,
            endtime=end,
        )

    try:
        stream = _retry(_fetch, attempts=attempts, delay_seconds=delay, label=f"dataselect {station}")
    except FDSNNoDataException:
        return None, None, "NO_DATA"
    except SedServiceStop:
        raise
    except Exception as exc:  # noqa: BLE001
        return None, None, f"{type(exc).__name__}:{exc}"

    if stream is None or len(stream) == 0:
        return None, None, "NO_DATA"
    path.parent.mkdir(parents=True, exist_ok=True)
    # Preserve original MiniSEED; do not merge, interpolate, filter, or response-correct.
    stream.write(str(path), format="MSEED")
    if path.stat().st_size <= 0:
        return None, None, "empty_file"
    return path, stream, "ok"


def download_hhz_stationxml(
    client: Client,
    *,
    network: str,
    station: str,
    location: str,
    start: UTCDateTime,
    end: UTCDateTime,
    path: Path,
    attempts: int,
    delay: float,
) -> tuple[Path | None, Any, str, str]:
    if path.exists() and path.stat().st_size > 0:
        try:
            inventory = read_inventory(str(path))
            status, reason = stationxml_hhz_status(
                inventory,
                network=network,
                station=station,
                location=location,
                channel="HHZ",
                start=start,
                end=end,
            )
            return path, inventory, status, f"existing:{reason}"
        except Exception as exc:  # noqa: BLE001
            return None, None, "unavailable", f"existing_unreadable:{type(exc).__name__}"

    loc = location if location else ""

    def _fetch():
        return client.get_stations(
            network=network,
            station=station,
            location=loc,
            channel="HHZ",
            starttime=start,
            endtime=end,
            level="response",
        )

    try:
        inventory = _retry(_fetch, attempts=attempts, delay_seconds=delay, label=f"stationxml {station}")
    except FDSNNoDataException:
        return None, None, "unavailable", "NO_DATA"
    except SedServiceStop:
        raise
    except Exception as exc:  # noqa: BLE001
        return None, None, "unavailable", f"{type(exc).__name__}:{exc}"

    if inventory is None or len(inventory) == 0:
        return None, None, "unavailable", "empty_inventory"
    path.parent.mkdir(parents=True, exist_ok=True)
    inventory.write(str(path), format="STATIONXML")
    status, reason = stationxml_hhz_status(
        inventory,
        network=network,
        station=station,
        location=location,
        channel="HHZ",
        start=start,
        end=end,
    )
    return path, inventory, status, reason


def _pick_row(event: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    pick = target.get("pick") or {}
    return empty_pick_row(
        event,
        network="CH",
        station=target["station"],
        location=target.get("location") or pick.get("location") or "",
        channel=pick.get("channel") or "",
        pick_phase=pick.get("phase") or "",
        pick_time_utc=pick.get("time_utc") or "",
        pick_evaluation_mode=pick.get("evaluation_mode") or "",
        pick_evaluation_status=pick.get("evaluation_status") or "",
        same_station_pick_status=target.get("same_station_pick_status") or "missing",
    )


def run(config_path: Path) -> int:
    config = load_validation_acquisition_config(config_path, repo_root=REPO_ROOT)
    audit = config["_audit"]
    output = config["output"]
    log_path = _configure_logging(REPO_ROOT / output["logs_dir"], output.get("log_name", "sed_switzerland_validation_acquisition.log"))
    LOGGER.info("switzerland_validation_acquisition_start config=%s log=%s", config_path, log_path)
    LOGGER.info("scientific_boundary %s", json.dumps(config["scientific_boundary"]))
    LOGGER.info("frozen_trigger_on %s (not used in this step)", config["frozen_configuration"]["trigger_on"])

    retry = config.get("retry") or {}
    timeout = int(retry.get("timeout_seconds", 60))
    attempts = int(retry.get("attempts", 3))
    delay = float(retry.get("delay_seconds", 1.0))
    sleep_s = float(retry.get("sleep_between_requests_seconds", 0.35))

    locked = locked_set_c_ids(config)
    events = proposed_events_from_candidate_csv(REPO_ROOT / config["candidate_csv"], locked)
    LOGGER.info("locked_set_c n=%s ids=%s", len(events), locked)

    station_names = fetch_ch_station_names(audit, timeout=max(timeout, 90))
    if not station_names:
        raise SedServiceStop("SED station inventory returned no CH HH stations.")
    client = Client(audit["endpoints"].get("obspy_client_base") or "https://eida.ethz.ch", timeout=timeout)

    raw_root = REPO_ROOT / output["raw_dir"]
    meta_root = REPO_ROOT / output["metadata_dir"]
    reports_dir = REPO_ROOT / output["reports_dir"]
    raw_root.mkdir(parents=True, exist_ok=True)
    meta_root.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    waveform_rows: list[dict[str, Any]] = []
    pick_rows: list[dict[str, Any]] = []
    event_notes: dict[str, Any] = {}

    for event in events:
        short_id = event["short_id"]
        origin = UTCDateTime(event["origin_time_utc"])
        start, end = acquisition_interval(origin, config)
        LOGGER.info(
            "event %s origin=%s acquisition=%s..%s mag=%s region=%s class=%s",
            short_id,
            event["origin_time_utc"],
            start,
            end,
            event.get("magnitude"),
            event.get("region"),
            event.get("location_class"),
        )
        avail_rows = query_availability_rows(audit, station_names, start, end, timeout=45, sleep_s=sleep_s)
        picks = load_picks_for_event(audit, event, timeout=60, sleep_s=sleep_s)
        targets = select_same_station_hhz_targets(picks, avail_rows, start, end)
        LOGGER.info("event %s availability_rows=%s targets=%s", short_id, len(avail_rows), [t["station"] for t in targets])
        event_notes[short_id] = {
            "n_availability_rows": len(avail_rows),
            "n_quakeml_picks": len(picks),
            "n_same_station_hhz_targets": len(targets),
            "target_stations": [item["station"] for item in targets],
        }

        if not targets:
            waveform_rows.append(
                empty_waveform_row(
                    event,
                    requested_start=str(start),
                    requested_end=str(end),
                    download_status="failed",
                    download_reason="no_same_station_hhz_target",
                    verification_status="NOT_RUN",
                    request_parameters=_request_params("CH", "*", "", "HHZ", start, end),
                )
            )
            _write_partial(config, waveform_rows, pick_rows)
            continue

        event_dir = raw_root / short_id
        meta_dir = meta_root / short_id
        for target in targets:
            pick_rows.append(_pick_row(event, target))
            time.sleep(sleep_s)
            wave_name = waveform_filename("CH", target["station"], target["location"], "HHZ", origin)
            xml_name = stationxml_filename("CH", target["station"], target["location"], "HHZ")
            wave_path = event_dir / wave_name
            xml_path = meta_dir / xml_name
            path, stream, dl_status = download_hhz_miniseed(
                client,
                network="CH",
                station=target["station"],
                location=target["location"],
                start=start,
                end=end,
                path=wave_path,
                attempts=attempts,
                delay=delay,
            )
            time.sleep(sleep_s)
            xml_out, _inventory, xml_status, xml_reason = download_hhz_stationxml(
                client,
                network="CH",
                station=target["station"],
                location=target["location"],
                start=start,
                end=end,
                path=xml_path,
                attempts=attempts,
                delay=delay,
            )

            pick = target.get("pick") or {}
            row = empty_waveform_row(
                event,
                network="CH",
                station=target["station"],
                location=target["location"] or "--",
                channel="HHZ",
                requested_start=str(start),
                requested_end=str(end),
                same_station_pick_status=target.get("same_station_pick_status") or "missing",
                pick_phase=pick.get("phase") or "",
                pick_time_utc=pick.get("time_utc") or "",
                pick_evaluation_mode=pick.get("evaluation_mode") or "",
                pick_channel=pick.get("channel") or "",
                StationXML_status=xml_status,
                StationXML_reason=xml_reason,
                StationXML_path=_relative(xml_out) if xml_out is not None else "",
                request_parameters=_request_params("CH", target["station"], target["location"], "HHZ", start, end),
            )
            if path is None or stream is None or not str(dl_status).startswith("ok"):
                row["download_status"] = "failed"
                row["download_reason"] = dl_status
                row["verification_status"] = "FAIL"
                LOGGER.warning("download_failed event=%s station=%s reason=%s", short_id, target["station"], dl_status)
                waveform_rows.append(row)
                continue

            inspection = inspect_miniseed_stream(
                stream,
                requested_start=start,
                requested_end=end,
                expected_station=target["station"],
            )
            row.update(
                {
                    "download_status": "ok",
                    "download_reason": dl_status,
                    "MiniSEED_path": _relative(path),
                    "file_size_bytes": path.stat().st_size,
                    "actual_start": inspection.actual_start,
                    "actual_end": inspection.actual_end,
                    "sampling_rate": inspection.sampling_rate,
                    "sample_count": inspection.sample_count,
                    "n_traces": inspection.n_traces,
                    "gaps": inspection.gaps,
                    "overlaps": inspection.overlaps,
                    "masked_or_empty": "yes" if inspection.masked_or_empty else "no",
                    "coverage_status": inspection.coverage_status,
                    "verification_status": inspection.verification_status,
                    "network": inspection.network or "CH",
                    "station": inspection.station or target["station"],
                    "location": inspection.location if inspection.location != "" else (target["location"] or "--"),
                    "channel": inspection.channel or "HHZ",
                }
            )
            if inspection.notes:
                LOGGER.info("verify event=%s station=%s status=%s notes=%s", short_id, target["station"], inspection.verification_status, inspection.notes)
            waveform_rows.append(row)
        _write_partial(config, waveform_rows, pick_rows)

    summary = _final_summary(config, locked, waveform_rows, pick_rows, event_notes, log_path)
    LOGGER.info(
        "switzerland_validation_acquisition_complete events=%s downloaded=%s verified=%s stationxml=%s failed=%s",
        summary["n_set_c_events"],
        summary["events_with_downloaded_hhz"],
        summary["events_with_verified_miniseed"],
        summary["events_with_stationxml_verified"],
        summary["n_download_failed"],
    )
    return 0


def _write_partial(config: dict[str, Any], waveform_rows: list[dict[str, Any]], pick_rows: list[dict[str, Any]]) -> None:
    output = config["output"]
    write_csv(REPO_ROOT / output["manifest_csv"], waveform_rows, WAVEFORM_MANIFEST_FIELDS)
    write_csv(REPO_ROOT / output["picks_csv"], pick_rows, PICK_MANIFEST_FIELDS)


def _final_summary(
    config: dict[str, Any],
    locked: list[str],
    waveform_rows: list[dict[str, Any]],
    pick_rows: list[dict[str, Any]],
    event_notes: dict[str, Any],
    log_path: Path,
) -> dict[str, Any]:
    output = config["output"]
    _write_partial(config, waveform_rows, pick_rows)
    summary = summarize_acquisition(waveform_rows, locked)
    sparse = {}
    for sid in ("2024bvrces", "2024ftcvhn"):
        sparse[sid] = {
            "n_targets": event_notes.get(sid, {}).get("n_same_station_hhz_targets", 0),
            "n_download_ok": sum(1 for row in waveform_rows if row.get("short_id") == sid and row.get("download_status") == "ok"),
            "stations": [row.get("station") for row in waveform_rows if row.get("short_id") == sid],
        }
    payload = {
        "generated_utc": utc_now_iso(),
        "role": "independent_swiss_adjacent_border_validation_acquisition",
        "dataset_display_name": config["validation_dataset"]["display_name"],
        "step": "2J",
        "acquisition_window": {"start_offset_s": -60.0, "end_offset_s": 90.0},
        "detection_window": {"start_offset_s": 0.0, "end_offset_s": 90.0},
        "pre_event_noise_window": {"start_offset_s": -60.0, "end_offset_s": -10.0},
        "station_selection_rule": config["station_selection"]["rule"],
        "frozen_trigger_on": 8.0,
        "sta_lta_run": False,
        "validation_metrics_calculated": False,
        "set_c_reselected": False,
        "set_a_modified": False,
        "california_modified": False,
        "source_provider": "SED/ETH EIDA https://eida.ethz.ch",
        "n_pick_rows": len(pick_rows),
        "sparse_pick_events": sparse,
        "event_notes": event_notes,
        "log_path": _relative(log_path),
        "manifest_csv": output["manifest_csv"],
        "picks_csv": output["picks_csv"],
        **summary,
    }
    reports_dir = REPO_ROOT / output["reports_dir"]
    reports_dir.mkdir(parents=True, exist_ok=True)
    summary_path = reports_dir / "acquisition_summary.json"
    summary_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    LOGGER.info("summary_written %s", summary_path)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download the locked Set C Swiss validation waveforms.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to validation acquisition YAML")
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
