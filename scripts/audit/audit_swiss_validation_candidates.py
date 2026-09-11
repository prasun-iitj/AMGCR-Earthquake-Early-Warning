#!/usr/bin/env python3
"""Independent Swiss validation-set audit against SED/ETH FDSN.

Queries the official SED catalogue and (where possible) QuakeML arrivals.
Does not download MiniSEED. Does not run STA/LTA. Does not retune threshold 8.0.
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
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from obspy import UTCDateTime

from src.acquisition.switzerland_pilot import (
    event_short_id,
    parse_availability_text,
)
from src.acquisition.switzerland_validation_audit import (
    CANDIDATE_FIELDS,
    apply_window_offsets,
    classify_location,
    count_ch_p_picks,
    development_short_ids,
    empty_candidate_row,
    exclusion_reason,
    load_validation_audit_config,
    locked_proposed_short_ids,
    parse_quakeml_picks,
    same_station_reference_counts,
    short_ids_from_manifest_csv,
    unique_ch_stations_covering,
    window_offsets,
)

DEFAULT_CONFIG = REPO_ROOT / "configs" / "sed_switzerland_validation_audit.yaml"
LOGGER = logging.getLogger("switzerland_validation_audit")
STOP_HTTP = {429, 503}


class SedServiceStop(RuntimeError):
    """Raised when SED/ETH FDSN must not be retried with a substitute provider."""


def _configure_logging(logs_dir: Path) -> Path:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "sed_switzerland_validation_audit.log"
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


def _http_get(url: str, timeout: int, user_agent: str = "AMGCR-SwitzerlandValidationAudit/1.0") -> tuple[int, str]:
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


def fetch_sed_catalog_text(config: dict[str, Any], timeout: int) -> tuple[str, str]:
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
    return url, body


def parse_sed_catalog_text(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) < 14:
            continue
        resource_id = parts[0].strip()
        rows.append(
            {
                "event_id": resource_id,
                "short_id": event_short_id(resource_id),
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
        )
    return rows


def fetch_quakeml_arrivals(
    config: dict[str, Any],
    starttime: str,
    endtime: str,
    timeout: int,
) -> tuple[str, str]:
    catalog = config["catalog"]
    query = (
        f"starttime={starttime}&endtime={endtime}"
        f"&minmagnitude={catalog['minmagnitude']}"
        f"&minlatitude={catalog['minlatitude']}&maxlatitude={catalog['maxlatitude']}"
        f"&minlongitude={catalog['minlongitude']}&maxlongitude={catalog['maxlongitude']}"
        f"&format=xml&includearrivals=true&nodata=404"
    )
    url = _join_url(config["endpoints"]["event"], "query") + "?" + query
    LOGGER.info("quakeml_arrivals_query %s", url)
    code, body = _http_get(url, timeout=timeout)
    if code in {204, 404}:
        return url, ""
    if code != 200:
        raise SedServiceStop(f"SED QuakeML HTTP {code}: {body[:300]}")
    return url, body


def fetch_event_quakeml(config: dict[str, Any], event_id: str, timeout: int) -> tuple[int, str]:
    url = (
        _join_url(config["endpoints"]["event"], "query")
        + f"?eventid={event_id}&format=xml&includearrivals=true&nodata=404"
    )
    LOGGER.info("quakeml_event_query %s", url)
    return _http_get(url, timeout=timeout)


def fetch_ch_station_names(config: dict[str, Any], timeout: int) -> list[str]:
    url = (
        _join_url(config["endpoints"]["station"], "query")
        + "?network=CH&channel=HH?&format=text&level=station&nodata=404"
    )
    LOGGER.info("station_inventory_query %s", url)
    code, body = _http_get(url, timeout=timeout)
    if code != 200:
        raise SedServiceStop(f"SED station inventory HTTP {code}: {body[:300]}")
    names: list[str] = []
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
        + f"&starttime={start.strftime('%Y-%m-%dT%H:%M:%S.%f')}"
        + f"&endtime={end.strftime('%Y-%m-%dT%H:%M:%S.%f')}"
        + "&format=text&nodata=404"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "AMGCR-SwitzerlandValidationAudit/1.0"})
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
    config: dict[str, Any],
    station_names: list[str],
    start: UTCDateTime,
    end: UTCDateTime,
    timeout: int,
    sleep_s: float,
) -> tuple[list[dict[str, Any]], bool]:
    """FDSN availability rows for the acquisition window. No MiniSEED."""
    batch_size = int(config["station_selection"].get("availability_station_batch_size", 10))
    rows: list[dict[str, Any]] = []
    timed_out = False
    for offset in range(0, len(station_names), batch_size):
        batch = station_names[offset : offset + batch_size]
        code, body = _availability_query(config, batch, start, end, timeout)
        time.sleep(sleep_s)
        if code in {204, 404}:
            continue
        if code != 200:
            LOGGER.warning("availability_batch HTTP %s stations=%s body=%s", code, batch, body[:180])
            if code == 0:
                timed_out = True
            continue
        rows.extend(parse_availability_text(body))
    return rows, timed_out


def summarize_acquisition_availability(
    rows: list[dict[str, Any]],
    start: UTCDateTime,
    end: UTCDateTime,
    timed_out: bool,
) -> dict[str, Any]:
    hh3c = unique_ch_stations_covering(rows, start, end, ("HHZ", "HHN", "HHE"))
    hhz = unique_ch_stations_covering(rows, start, end, ("HHZ",))
    obtainable = "yes" if hhz else ("timeout_or_empty" if timed_out else "no")
    return {
        "n_unique_ch_stations_with_hh_3c": len(hh3c),
        "n_unique_ch_stations_with_hhz": len(hhz),
        "acquisition_window_obtainable": obtainable,
        "hhz_stations": hhz,
        "hh3c_stations": hh3c,
    }


def year_windows(start: str, end: str) -> list[tuple[str, str]]:
    start_year = int(start[:4])
    end_year = int(end[:4])
    windows: list[tuple[str, str]] = []
    for year in range(start_year, end_year + 1):
        lo = f"{year}-01-01T00:00:00"
        hi = f"{year + 1}-01-01T00:00:00"
        if year == start_year:
            lo = start
        if year == end_year:
            hi = end
        windows.append((lo, hi))
    return windows


def candidate_row_from_event(event: dict[str, Any], **extra: Any) -> dict[str, Any]:
    row = empty_candidate_row()
    row.update(
        {
            "short_id": event["short_id"],
            "event_id": event["event_id"],
            "origin_time_utc": event["origin_time_utc"],
            "latitude": event["latitude"],
            "longitude": event["longitude"],
            "depth_km": event.get("depth_km", ""),
            "magnitude": event["magnitude"],
            "magnitude_type": event.get("magnitude_type", ""),
            "region": event.get("region", ""),
            "event_type": event.get("event_type", ""),
            "location_class": event.get("location_class", ""),
            "in_development_set": "yes" if event.get("in_development_set") else "no",
        }
    )
    row.update({key: extra[key] for key in extra if key in row})
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CANDIDATE_FIELDS), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in CANDIDATE_FIELDS})


def pool_from_candidate_csv(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for raw in csv.DictReader(handle):
            event = dict(raw)
            event["in_development_set"] = str(raw.get("in_development_set") or "").lower() == "yes"
            event["latitude"] = float(raw["latitude"])
            event["longitude"] = float(raw["longitude"])
            event["magnitude"] = float(raw["magnitude"])
            event["n_ch_p_picks"] = int(raw["n_ch_p_picks"] or 0)
            event["n_ch_manual_p_picks"] = int(raw.get("n_ch_manual_p_picks") or 0)
            event["n_ch_hhz_p_picks"] = int(raw.get("n_ch_hhz_p_picks") or 0)
            event["n_unique_ch_stations_with_first_p"] = int(raw.get("n_unique_ch_stations_with_first_p") or 0)
            event["n_unique_ch_stations_with_hh_3c"] = raw.get("n_unique_ch_stations_with_hh_3c") or ""
            event["n_unique_ch_stations_with_hhz"] = raw.get("n_unique_ch_stations_with_hhz") or ""
            event["acquisition_window_obtainable"] = raw.get("acquisition_window_obtainable") or "not_checked"
            event["n_same_station_first_p_and_hhz"] = raw.get("n_same_station_first_p_and_hhz") or ""
            event["n_same_station_hhz_first_p_and_hhz"] = raw.get("n_same_station_hhz_first_p_and_hhz") or ""
            event["stationxml_status"] = "not_yet_verified_per_station"
            event["exclusion_concern"] = raw.get("exclusion_concern") or ""
            rows.append(event)
    return rows


def refresh_set_c_availability_and_picks(
    config: dict[str, Any],
    pool: list[dict[str, Any]],
    proposed_ids: list[str],
    timeout: int,
) -> None:
    """Update Set C only. Does not replace event IDs and does not download MiniSEED."""
    station_names = fetch_ch_station_names(config, timeout=timeout)
    offsets = window_offsets(config)
    by_id = {event["short_id"]: event for event in pool}
    for short_id in proposed_ids:
        event = by_id[short_id]
        origin = UTCDateTime(event["origin_time_utc"])
        acq_start, acq_end = apply_window_offsets(origin, *offsets["acquisition"])
        rows, timed_out = query_availability_rows(
            config, station_names, acq_start, acq_end, timeout=45, sleep_s=0.35
        )
        availability = summarize_acquisition_availability(rows, acq_start, acq_end, timed_out)
        event["n_unique_ch_stations_with_hh_3c"] = availability["n_unique_ch_stations_with_hh_3c"]
        event["n_unique_ch_stations_with_hhz"] = availability["n_unique_ch_stations_with_hhz"]
        event["acquisition_window_obtainable"] = availability["acquisition_window_obtainable"]
        event["stationxml_status"] = "not_yet_verified_per_station"

        code, body = fetch_event_quakeml(config, short_id, timeout=60)
        time.sleep(0.35)
        if code != 200 or not body:
            resource = str(event.get("event_id") or "")
            if resource and resource != short_id:
                LOGGER.info("quakeml_retry_resource_id %s", resource)
                code, body = fetch_event_quakeml(config, resource, timeout=60)
                time.sleep(0.35)
        picks: list[dict[str, Any]] = []
        if code == 200 and body:
            parsed = parse_quakeml_picks(body)
            picks = parsed.get(short_id, [])
            if not picks and parsed:
                picks = next(iter(parsed.values()))
        LOGGER.info("set_c_picks %s n=%s sample_stations=%s", short_id, len(picks), sorted({p.get("station") for p in picks if p.get("station")})[:8])
        pick_summary = count_ch_p_picks(picks)
        event.update(pick_summary)
        match = same_station_reference_counts(picks, availability["hhz_stations"])
        event["n_unique_ch_stations_with_first_p"] = match["n_unique_ch_stations_with_first_p"]
        event["n_same_station_first_p_and_hhz"] = match["n_same_station_first_p_and_hhz"]
        event["n_same_station_hhz_first_p_and_hhz"] = match["n_same_station_hhz_first_p_and_hhz"]
        concerns = [c for c in str(event.get("exclusion_concern") or "").split(";") if c]
        for stale in (
            "fewer_than_two_hh_3c_stations_in_availability",
            "acquisition_window_not_obtainable",
            "no_same_station_first_p_and_hhz",
            "few_ch_first_p_picks",
        ):
            concerns = [c for c in concerns if c != stale]
        if availability["n_unique_ch_stations_with_hhz"] < 1:
            concerns.append("acquisition_window_not_obtainable")
        if match["n_same_station_first_p_and_hhz"] < 1:
            concerns.append("no_same_station_first_p_and_hhz")
        if int(event.get("n_ch_p_picks") or 0) < 10 and "few_ch_first_p_picks" not in concerns:
            concerns.append("few_ch_first_p_picks")
        event["exclusion_concern"] = ";".join(concerns)
        LOGGER.info(
            "set_c %s acq_hhz=%s acq_hh3c=%s obtainable=%s same_station_p=%s",
            short_id,
            availability["n_unique_ch_stations_with_hhz"],
            availability["n_unique_ch_stations_with_hh_3c"],
            availability["acquisition_window_obtainable"],
            match["n_same_station_first_p_and_hhz"],
        )


def apply_availability_and_stationxml(
    config: dict[str, Any],
    pool: list[dict[str, Any]],
    proposed_ids: list[str],
    timeout: int,
) -> tuple[list[str], bool]:
    """Locked Set C refresh. Does not replace events and does not download MiniSEED."""
    refresh_set_c_availability_and_picks(config, pool, proposed_ids, timeout)
    return proposed_ids, True


def write_outputs(
    config: dict[str, Any],
    pool: list[dict[str, Any]],
    proposed_ids: list[str],
    summary: dict[str, Any],
) -> dict[str, Any]:
    proposed_set = set(proposed_ids)
    csv_rows: list[dict[str, Any]] = []
    for event in sorted(pool, key=lambda item: str(item["origin_time_utc"])):
        is_proposed = event["short_id"] in proposed_set
        role = "proposed_validation_subset" if is_proposed else "independent_candidate_pool"
        csv_rows.append(
            candidate_row_from_event(
                event,
                pool_role=role,
                proposed_validation="yes" if is_proposed else "no",
                n_ch_p_picks=event.get("n_ch_p_picks", ""),
                n_ch_manual_p_picks=event.get("n_ch_manual_p_picks", ""),
                n_ch_hhz_p_picks=event.get("n_ch_hhz_p_picks", ""),
                n_unique_ch_stations_with_first_p=event.get("n_unique_ch_stations_with_first_p", ""),
                sed_p_pick_available=event.get("sed_p_pick_available", "no"),
                sed_p_pick_modes=event.get("sed_p_pick_modes", ""),
                n_unique_ch_stations_with_hh_3c=event.get("n_unique_ch_stations_with_hh_3c", ""),
                n_unique_ch_stations_with_hhz=event.get("n_unique_ch_stations_with_hhz", ""),
                acquisition_window_obtainable=(
                    event.get("acquisition_window_obtainable", "not_checked")
                    if is_proposed
                    else event.get("acquisition_window_obtainable") or "not_checked"
                ),
                n_same_station_first_p_and_hhz=event.get("n_same_station_first_p_and_hhz", ""),
                n_same_station_hhz_first_p_and_hhz=event.get("n_same_station_hhz_first_p_and_hhz", ""),
                stationxml_status=(
                    "not_yet_verified_per_station" if is_proposed else "not_checked"
                ),
                exclusion_concern=event.get("exclusion_concern", ""),
            )
        )
    csv_path = REPO_ROOT / config["output"]["candidate_csv"]
    write_csv(csv_path, csv_rows)
    reports_dir = REPO_ROOT / config["output"]["reports_dir"]
    reports_dir.mkdir(parents=True, exist_ok=True)
    development_ids = development_short_ids(config)
    proposed_rows = [row for row in csv_rows if row["proposed_validation"] == "yes"]
    summary["proposed_short_ids"] = proposed_ids
    summary["n_proposed"] = len(proposed_ids)
    summary["proposed_overlap_with_development"] = [
        row["short_id"] for row in proposed_rows if row["short_id"] in development_ids
    ]
    summary["candidate_csv"] = str(csv_path.relative_to(REPO_ROOT)).replace("\\", "/")
    summary_path = reports_dir / "audit_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    LOGGER.info("wrote %s", csv_path)
    LOGGER.info("wrote %s", summary_path)
    return summary


def run_refresh_set_c(config_path: Path, candidates_csv: Path) -> dict[str, Any]:
    """Refresh availability/picks for the locked 15 events. Does not change Set C membership."""
    config = load_validation_audit_config(config_path)
    logs_dir = REPO_ROOT / config["output"]["logs_dir"]
    log_path = _configure_logging(logs_dir)
    summary_path = REPO_ROOT / config["output"]["reports_dir"] / "audit_summary.json"
    prior = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    pool = pool_from_candidate_csv(candidates_csv)
    proposed_ids = locked_proposed_short_ids(config)
    missing = [sid for sid in proposed_ids if sid not in {e["short_id"] for e in pool}]
    if missing:
        raise SedServiceStop(f"locked Set C IDs missing from candidate CSV: {missing}")
    LOGGER.info("locked_set_c %s", proposed_ids)
    refresh_set_c_availability_and_picks(config, pool, proposed_ids, timeout=90)
    offsets = window_offsets(config)
    prior.update(
        {
            "role": "independent_swiss_adjacent_border_validation_design",
            "dataset_display_name": config["validation_dataset"]["display_name"],
            "set_c_unchanged": True,
            "selection_rule": "locked_proposed_event_ids",
            "windows": {
                "acquisition": list(offsets["acquisition"]),
                "detection": list(offsets["detection"]),
                "pre_event_noise": list(offsets["pre_event_noise"]),
            },
            "hh_3c_availability_meaning": (
                "unique CH station codes with HHZ+HHN+HHE FDSN availability "
                "fully covering origin-60 s to origin+90 s (not a channel/trace count)"
            ),
            "stationxml_status": "not_yet_verified_per_station",
            "data_leakage_statement": str(config["data_leakage"]["statement"]).strip(),
            "reselected_from_existing_candidate_csv": False,
            "availability_checked_for_proposed": True,
            "log_path": str(log_path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "not_performed": [
                "waveform_download",
                "sta_lta_on_validation_events",
                "threshold_retuning",
                "ml_training",
                "validation_metric_computation",
            ],
        }
    )
    return write_outputs(config, pool, proposed_ids, prior)


def run_audit(config_path: Path) -> dict[str, Any]:
    config = load_validation_audit_config(config_path)
    logs_dir = REPO_ROOT / config["output"]["logs_dir"]
    log_path = _configure_logging(logs_dir)
    reports_dir = REPO_ROOT / config["output"]["reports_dir"]
    reports_dir.mkdir(parents=True, exist_ok=True)

    development_ids = development_short_ids(config)
    manifest_path = REPO_ROOT / config["development_dataset"]["manifest_csv"]
    manifest_ids = short_ids_from_manifest_csv(manifest_path)
    if manifest_ids != development_ids:
        raise SedServiceStop(
            "development event IDs in audit config do not match the 20-event Swiss pilot manifest."
        )

    timeout = 90
    catalog_url, catalog_text = fetch_sed_catalog_text(config, timeout=timeout)
    catalog_rows = parse_sed_catalog_text(catalog_text)
    allowed_types = list(config["catalog"]["allowed_event_types"])
    min_mag = float(config["catalog"]["minmagnitude"])
    swiss_box = config["swiss_interior_box"]

    exclusion_counts: dict[str, int] = {}
    independent: list[dict[str, Any]] = []
    development_seen: list[str] = []
    for event in catalog_rows:
        reason = exclusion_reason(
            event,
            development_ids=development_ids,
            allowed_types=allowed_types,
            min_magnitude=min_mag,
        )
        event["in_development_set"] = event["short_id"] in development_ids
        event["location_class"] = classify_location(
            float(event["latitude"]),
            float(event["longitude"]),
            str(event.get("region") or ""),
            swiss_box,
        )
        if event["in_development_set"]:
            development_seen.append(event["short_id"])
        if reason:
            exclusion_counts[reason] = exclusion_counts.get(reason, 0) + 1
            continue
        independent.append(event)

    missing_development = sorted(development_ids - set(development_seen))
    LOGGER.info(
        "catalog_events=%s independent_earthquakes=%s development_found=%s missing_development=%s",
        len(catalog_rows),
        len(independent),
        len(set(development_seen)),
        missing_development,
    )

    picks_by_event: dict[str, list[dict[str, Any]]] = {}
    quakeml_urls: list[str] = []
    quakeml_ok = True
    try:
        for start, end in year_windows(config["catalog"]["starttime"], config["catalog"]["endtime"]):
            url, xml_text = fetch_quakeml_arrivals(config, start, end, timeout=180)
            quakeml_urls.append(url)
            time.sleep(0.5)
            if not xml_text:
                continue
            parsed = parse_quakeml_picks(xml_text)
            for short_id, picks in parsed.items():
                picks_by_event.setdefault(short_id, []).extend(picks)
            LOGGER.info("quakeml_year %s-%s events_with_picks_in_file=%s", start[:4], end[:4], len(parsed))
    except SedServiceStop as exc:
        LOGGER.warning("yearly_quakeml_failed %s; falling back to per-event probes", exc)
        quakeml_ok = False

    if not picks_by_event:
        LOGGER.info("probing_single_events_for_picks n=%s", min(25, len(independent)))
        for event in independent[:25]:
            code, body = fetch_event_quakeml(config, event["short_id"], timeout=60)
            time.sleep(0.35)
            if code != 200 or not body:
                continue
            parsed = parse_quakeml_picks(body)
            for short_id, picks in parsed.items():
                picks_by_event.setdefault(short_id, []).extend(picks)
        quakeml_ok = bool(picks_by_event)

    pick_probe_event = independent[0]["short_id"] if independent else ""
    pick_probe_n = len(picks_by_event.get(pick_probe_event, [])) if pick_probe_event else 0

    pool: list[dict[str, Any]] = []
    for event in independent:
        summary = count_ch_p_picks(picks_by_event.get(event["short_id"], []))
        event.update(summary)
        event["n_unique_ch_stations_with_hh_3c"] = ""
        event["n_unique_ch_stations_with_hhz"] = ""
        event["acquisition_window_obtainable"] = "not_checked"
        event["stationxml_status"] = "not_checked"
        event["n_same_station_first_p_and_hhz"] = ""
        event["n_same_station_hhz_first_p_and_hhz"] = ""
        if summary["n_ch_p_picks"] <= 0:
            event["exclusion_concern"] = "no_ch_p_picks_in_queried_quakeml"
        else:
            event["exclusion_concern"] = ""
        pool.append(event)

    proposed_ids = locked_proposed_short_ids(config)
    LOGGER.info("locked_set_c %s", proposed_ids)
    proposed_ids, availability_checked = apply_availability_and_stationxml(
        config, pool, proposed_ids, timeout=timeout
    )
    LOGGER.info("proposed_validation_events_after_availability %s", proposed_ids)
    summary = {
        "role": "independent_validation_design_audit",
        "not_performed": [
            "waveform_download",
            "sta_lta_on_validation_events",
            "threshold_retuning",
            "ml_training",
            "validation_metric_computation",
        ],
        "selection_rule": "year_quotas_then_mag_geo_border",
        "frozen_configuration": config["frozen_configuration"],
        "catalog_query_url": catalog_url,
        "quakeml_query_urls": quakeml_urls,
        "catalog_endtime": config["catalog"]["endtime"],
        "n_catalog_rows": len(catalog_rows),
        "n_excluded": sum(exclusion_counts.values()),
        "exclusion_counts": exclusion_counts,
        "n_independent_earthquakes": len(independent),
        "n_candidate_pool_rows": len(pool),
        "n_with_ch_p_picks": sum(1 for event in pool if int(event.get("n_ch_p_picks") or 0) > 0),
        "development_ids_in_catalog": sorted(set(development_seen)),
        "development_ids_missing_from_catalog": missing_development,
        "quakeml_arrivals_parsed": bool(picks_by_event),
        "n_events_with_parsed_picks": len(picks_by_event),
        "pick_probe_event": pick_probe_event,
        "pick_probe_n_picks": pick_probe_n,
        "availability_checked_for_proposed": availability_checked,
        "log_path": str(log_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "quakeml_yearly_ok": quakeml_ok,
    }
    return write_outputs(config, pool, proposed_ids, summary)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an independent Swiss SED validation candidate set.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--refresh-set-c",
        type=Path,
        default=None,
        help="Refresh acquisition-window availability and same-station picks for the locked 15 events. Does not reselect.",
    )
    args = parser.parse_args()
    try:
        if args.refresh_set_c:
            summary = run_refresh_set_c(args.config, args.refresh_set_c)
        else:
            summary = run_audit(args.config)
    except SedServiceStop as exc:
        LOGGER.error("%s", exc)
        return 2
    overlap = summary["proposed_overlap_with_development"]
    if overlap:
        LOGGER.error("proposed set overlaps development IDs: %s", overlap)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
