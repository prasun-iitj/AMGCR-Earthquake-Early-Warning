"""Independent Swiss/Adjacent-Border validation acquisition helpers.

Downloads are executed by the STEP 2J script. This module does not run STA/LTA,
compute detection metrics, or retune threshold 8.0.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from obspy import Stream, UTCDateTime

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.switzerland_pilot import event_short_id, location_label
from src.acquisition.switzerland_validation_audit import (
    apply_window_offsets,
    first_p_station_codes,
    load_validation_audit_config,
    locked_proposed_short_ids,
    span_covers_interval,
    unique_ch_stations_covering,
    window_offsets,
)

SET_A_RAW_DIR = "data/raw/switzerland"
SET_A_METADATA_DIR = "data/metadata/switzerland"
CALIFORNIA_MARKERS = ("iris", "california")

WAVEFORM_MANIFEST_FIELDS: tuple[str, ...] = (
    "event_id",
    "short_id",
    "sed_event_resource_id",
    "origin_time",
    "magnitude",
    "magnitude_type",
    "region",
    "location_class",
    "network",
    "station",
    "location",
    "channel",
    "requested_start",
    "requested_end",
    "actual_start",
    "actual_end",
    "sampling_rate",
    "sample_count",
    "n_traces",
    "file_size_bytes",
    "gaps",
    "overlaps",
    "masked_or_empty",
    "coverage_status",
    "MiniSEED_path",
    "StationXML_path",
    "StationXML_status",
    "StationXML_reason",
    "same_station_pick_status",
    "pick_phase",
    "pick_time_utc",
    "pick_evaluation_mode",
    "pick_channel",
    "download_status",
    "download_reason",
    "verification_status",
    "source_provider",
    "request_parameters",
)

PICK_MANIFEST_FIELDS: tuple[str, ...] = (
    "short_id",
    "sed_event_resource_id",
    "origin_time",
    "network",
    "station",
    "location",
    "channel",
    "pick_phase",
    "pick_time_utc",
    "pick_evaluation_mode",
    "pick_evaluation_status",
    "pick_source",
    "same_station_pick_status",
)


def load_validation_acquisition_config(path: str | Path, *, repo_root: Path | None = None) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise AcquisitionConfigurationError(f"validation acquisition config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    if not isinstance(config, dict):
        raise AcquisitionConfigurationError("validation acquisition config must be a YAML mapping.")
    root = repo_root or config_path.resolve().parents[1]
    audit_rel = config.get("audit_config")
    if not isinstance(audit_rel, str) or not audit_rel.strip():
        raise AcquisitionConfigurationError("audit_config must be a path to the validation audit YAML.")
    audit = load_validation_audit_config(root / audit_rel)
    validate_validation_acquisition_config(config, audit)
    config["_audit"] = audit
    return config


def validate_validation_acquisition_config(config: dict[str, Any], audit: dict[str, Any]) -> None:
    if float(config.get("frozen_configuration", {}).get("trigger_on", 0)) != 8.0:
        raise AcquisitionConfigurationError("acquisition config must keep frozen trigger_on at 8.0.")
    if float(audit["frozen_configuration"]["trigger_on"]) != 8.0:
        raise AcquisitionConfigurationError("audit frozen trigger_on must remain 8.0.")

    acq_windows = window_offsets(config)
    audit_windows = window_offsets(audit)
    if acq_windows != audit_windows:
        raise AcquisitionConfigurationError("acquisition windows must match the audit windows.")
    if acq_windows["acquisition"] != (-60.0, 90.0):
        raise AcquisitionConfigurationError("acquisition window must be origin-60 s to origin+90 s.")
    if acq_windows["detection"] != (0.0, 90.0):
        raise AcquisitionConfigurationError("detection window must remain origin to origin+90 s.")
    if acq_windows["detection"][0] < 0.0:
        raise AcquisitionConfigurationError("detection must not begin before origin.")
    if acq_windows["pre_event_noise"] != (-60.0, -10.0):
        raise AcquisitionConfigurationError("pre-event noise window must be origin-60 s to origin-10 s.")

    selection = config.get("station_selection")
    if not isinstance(selection, dict):
        raise AcquisitionConfigurationError("station_selection must be a mapping.")
    if selection.get("rule") != "all_audit_same_station_first_p_and_hhz":
        raise AcquisitionConfigurationError(
            "station_selection.rule must be all_audit_same_station_first_p_and_hhz "
            "(do not invent a preferred-station ranking)."
        )
    if selection.get("network") != "CH" or selection.get("channel") != "HHZ":
        raise AcquisitionConfigurationError("validation acquisition is CH HHZ only.")
    if selection.get("copy_set_a_distance_bins") is not False:
        raise AcquisitionConfigurationError("do not copy Set A distance-bin station selection.")
    if selection.get("require_same_station_sed_first_p") is not True:
        raise AcquisitionConfigurationError("same-station SED first-P is required.")

    boundary = config.get("scientific_boundary") or {}
    for key in (
        "run_sta_lta",
        "compute_validation_metrics",
        "retune_threshold",
        "reselection_set_c",
        "modify_set_a",
        "modify_california",
    ):
        if boundary.get(key) is not False:
            raise AcquisitionConfigurationError(f"scientific_boundary.{key} must be false.")

    output = config.get("output")
    if not isinstance(output, dict):
        raise AcquisitionConfigurationError("output must be a mapping.")
    raw_dir = _posix(output.get("raw_dir"))
    meta_dir = _posix(output.get("metadata_dir"))
    if raw_dir == SET_A_RAW_DIR or meta_dir == SET_A_METADATA_DIR:
        raise AcquisitionConfigurationError("validation output must not write into Set A paths.")
    for value in (raw_dir, meta_dir, _posix(output.get("manifest_csv"))):
        lowered = value.lower()
        if any(marker in lowered for marker in CALIFORNIA_MARKERS):
            raise AcquisitionConfigurationError(f"validation output must not point at California paths: {value}")

    locked = locked_proposed_short_ids(audit)
    if len(locked) != 15:
        raise AcquisitionConfigurationError("Set C must contain exactly 15 locked event IDs.")


def locked_set_c_ids(config: dict[str, Any]) -> list[str]:
    return locked_proposed_short_ids(config["_audit"])


def acquisition_interval(origin: Any, config: dict[str, Any]) -> tuple[Any, Any]:
    start_off, end_off = window_offsets(config)["acquisition"]
    return apply_window_offsets(origin, start_off, end_off)


def detection_interval(origin: Any, config: dict[str, Any]) -> tuple[Any, Any]:
    start_off, end_off = window_offsets(config)["detection"]
    return apply_window_offsets(origin, start_off, end_off)


def noise_interval(origin: Any, config: dict[str, Any]) -> tuple[Any, Any]:
    start_off, end_off = window_offsets(config)["pre_event_noise"]
    return apply_window_offsets(origin, start_off, end_off)


def quakeml_eventid_candidates(short_id: str, resource_id: str) -> list[str]:
    """SED often 404s short eventid= tokens; try the full resource ID first."""
    short = event_short_id(short_id or resource_id)
    resource = str(resource_id or "").strip()
    ordered: list[str] = []
    if resource:
        ordered.append(resource)
    if short and short not in ordered:
        ordered.append(short)
    return ordered


def preferred_same_station_first_p(picks: list[dict[str, Any]], station: str) -> dict[str, Any] | None:
    """Earliest CH first-P at this station. Prefers manual. Ignores event-level picks."""
    wanted = str(station or "").strip().upper()
    if not wanted:
        return None
    matches: list[dict[str, Any]] = []
    for pick in picks:
        if str(pick.get("network") or "").upper() != "CH":
            continue
        if str(pick.get("station") or "").strip().upper() != wanted:
            continue
        phase = str(pick.get("phase") or "").strip().upper()
        if phase not in {"P", "PG", "PN", "PB", "P1", "PDIFF"}:
            continue
        if not str(pick.get("time_utc") or "").strip():
            continue
        matches.append(pick)
    if not matches:
        return None
    manual = [pick for pick in matches if str(pick.get("evaluation_mode") or "").strip().lower() == "manual"]
    pool = manual or matches
    pool.sort(key=lambda item: str(item.get("time_utc") or ""))
    return dict(pool[0])


def pick_status_label(pick: dict[str, Any] | None) -> str:
    if pick is None:
        return "missing"
    mode = str(pick.get("evaluation_mode") or "").strip().lower()
    if mode == "manual":
        return "manual_ch_first_p"
    if mode:
        return f"{mode}_ch_first_p"
    return "ch_first_p_mode_unspecified"


def _covering_hhz_rows(
    availability_rows: list[dict[str, Any]],
    start: Any,
    end: Any,
    slack_s: float = 1.5,
) -> dict[str, list[dict[str, Any]]]:
    by_station: dict[str, list[dict[str, Any]]] = {}
    for row in availability_rows:
        if str(row.get("network") or "").upper() != "CH":
            continue
        if str(row.get("channel") or "").upper() != "HHZ":
            continue
        station = str(row.get("station") or "").strip().upper()
        if not station:
            continue
        if not span_covers_interval(row["earliest"], row["latest"], start, end, slack_s):
            continue
        by_station.setdefault(station, []).append(row)
    return by_station


def _choose_location(hhz_rows: list[dict[str, Any]], pick: dict[str, Any] | None) -> str:
    locations = []
    seen: set[str] = set()
    for row in hhz_rows:
        loc = str(row.get("location") or "")
        if loc in {"--"}:
            loc = ""
        if loc not in seen:
            seen.add(loc)
            locations.append(loc)
    pick_loc = str((pick or {}).get("location") or "")
    if pick_loc in {"--"}:
        pick_loc = ""
    if pick_loc in seen:
        return pick_loc
    if "" in seen:
        return ""
    return sorted(locations)[0] if locations else ""


def select_same_station_hhz_targets(
    picks: list[dict[str, Any]],
    availability_rows: list[dict[str, Any]],
    start: Any,
    end: Any,
    slack_s: float = 1.5,
) -> list[dict[str, Any]]:
    """All CH stations with HHZ covering the acquisition window and a station-level first-P.

    Event-level picks (blank station) are not targets. Set A distance bins are not used.
    """
    covering = _covering_hhz_rows(availability_rows, start, end, slack_s)
    p_stations = first_p_station_codes(picks)
    targets: list[dict[str, Any]] = []
    for station in sorted(covering.keys() & p_stations):
        pick = preferred_same_station_first_p(picks, station)
        location = _choose_location(covering[station], pick)
        targets.append(
            {
                "network": "CH",
                "station": station,
                "location": location,
                "channel": "HHZ",
                "pick": pick,
                "same_station_pick_status": pick_status_label(pick),
            }
        )
    return targets


def waveform_filename(network: str, station: str, location: str, channel: str, origin: UTCDateTime) -> str:
    return f"{network}.{station}.{location_label(location)}.{channel}.{origin.strftime('%Y%m%dT%H%M%S')}.mseed"


def stationxml_filename(network: str, station: str, location: str, channel: str) -> str:
    return f"{network}.{station}.{location_label(location)}.{channel}.xml"


@dataclass
class MiniSeedInspection:
    readable: bool
    network: str
    station: str
    location: str
    channel: str
    actual_start: str
    actual_end: str
    sampling_rate: str
    sample_count: int
    n_traces: int
    gaps: int
    overlaps: int
    masked_or_empty: bool
    coverage_status: str
    verification_status: str
    notes: list[str] = field(default_factory=list)


def inspect_miniseed_stream(
    stream: Stream | None,
    *,
    requested_start: UTCDateTime,
    requested_end: UTCDateTime,
    expected_network: str = "CH",
    expected_station: str = "",
    expected_channel: str = "HHZ",
    coverage_slack_s: float = 1.5,
) -> MiniSeedInspection:
    """Structural/data-integrity check only. No STA/LTA, SNR, amplitude, or P picking."""
    if stream is None or len(stream) == 0:
        return MiniSeedInspection(
            readable=False,
            network="",
            station="",
            location="",
            channel="",
            actual_start="",
            actual_end="",
            sampling_rate="",
            sample_count=0,
            n_traces=0,
            gaps=0,
            overlaps=0,
            masked_or_empty=True,
            coverage_status="none",
            verification_status="FAIL",
            notes=["empty or unreadable stream"],
        )

    notes: list[str] = []
    networks = sorted({str(tr.stats.network) for tr in stream})
    stations = sorted({str(tr.stats.station) for tr in stream})
    locations = sorted({str(tr.stats.location or "") for tr in stream})
    channels = sorted({str(tr.stats.channel) for tr in stream})
    rates = sorted({float(tr.stats.sampling_rate) for tr in stream})
    start = min(tr.stats.starttime for tr in stream)
    end = max(tr.stats.endtime for tr in stream)
    sample_count = int(sum(int(tr.stats.npts) for tr in stream))

    gap_rows = stream.get_gaps()
    gaps = 0
    overlaps = 0
    for row in gap_rows:
        duration = float(row[6]) if len(row) > 6 else 0.0
        if duration < 0:
            overlaps += 1
        elif duration > 0:
            gaps += 1

    masked_or_empty = False
    if sample_count <= 0:
        masked_or_empty = True
        notes.append("zero samples")
    for tr in stream:
        data = tr.data
        if data is None or len(data) == 0:
            masked_or_empty = True
            notes.append("empty trace")
            continue
        if np.ma.isMaskedArray(data) and bool(np.ma.getmaskarray(data).any()):
            masked_or_empty = True
            notes.append("masked samples")
        if not np.isfinite(np.asarray(data, dtype=float)).any():
            masked_or_empty = True
            notes.append("non-finite samples")

    covers = start <= requested_start + coverage_slack_s and end >= requested_end - coverage_slack_s
    if covers:
        coverage_status = "full"
    elif end <= requested_start or start >= requested_end:
        coverage_status = "none"
    else:
        coverage_status = "partial"
        notes.append("incomplete coverage of requested acquisition window")

    if expected_network and expected_network not in networks:
        notes.append(f"network {networks} != {expected_network}")
    if expected_station and expected_station not in stations:
        notes.append(f"station {stations} != {expected_station}")
    if expected_channel and expected_channel not in channels:
        notes.append(f"channel {channels} != {expected_channel}")
    if gaps:
        notes.append(f"gaps={gaps}")
    if overlaps:
        notes.append(f"overlaps={overlaps}")

    if not covers or masked_or_empty or expected_channel not in channels:
        verification_status = "FAIL" if (not covers and coverage_status == "none") or masked_or_empty else "PARTIAL"
        if expected_channel not in channels:
            verification_status = "FAIL"
    else:
        verification_status = "PASS"
        if gaps or overlaps:
            verification_status = "PARTIAL"

    return MiniSeedInspection(
        readable=True,
        network=";".join(networks),
        station=";".join(stations),
        location=";".join(locations),
        channel=";".join(channels),
        actual_start=str(start),
        actual_end=str(end),
        sampling_rate=";".join(str(rate) for rate in rates),
        sample_count=sample_count,
        n_traces=len(stream),
        gaps=gaps,
        overlaps=overlaps,
        masked_or_empty=masked_or_empty,
        coverage_status=coverage_status,
        verification_status=verification_status,
        notes=notes,
    )


def stationxml_hhz_status(
    inventory: Any,
    *,
    network: str,
    station: str,
    location: str,
    channel: str,
    start: UTCDateTime,
    end: UTCDateTime,
) -> tuple[str, str]:
    """Per-station/channel response check. BALST spot-checks are not used."""
    if inventory is None or len(inventory) == 0:
        return "unavailable", "empty_inventory"
    loc = location if location not in {"", "--"} else "*"
    try:
        selected = inventory.select(
            network=network,
            station=station,
            location=loc,
            channel=channel,
            starttime=start,
            endtime=end,
        )
    except Exception as exc:  # noqa: BLE001
        return "unavailable", f"select_failed:{type(exc).__name__}"
    channels = [ch for net in selected for sta in net.stations for ch in sta.channels]
    if not channels:
        return "retrieved_but_incomplete", "no_matching_HHZ_channel_epoch"
    with_response = [ch for ch in channels if getattr(ch, "response", None) is not None]
    if not with_response:
        return "retrieved_but_incomplete", "HHZ_channel_present_but_no_response"
    stages_ok = False
    for ch in with_response:
        response = ch.response
        if getattr(response, "instrument_sensitivity", None) is not None:
            stages_ok = True
            break
        if getattr(response, "response_stages", None):
            stages_ok = True
            break
    if not stages_ok:
        return "retrieved_but_incomplete", "response_object_empty"
    return "verified", "station_channel_response_present"


def empty_waveform_row(event: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    row = {key: "" for key in WAVEFORM_MANIFEST_FIELDS}
    short_id = event_short_id(str(event.get("short_id") or event.get("event_id") or ""))
    resource = str(event.get("event_id") or event.get("sed_event_resource_id") or "")
    row.update(
        {
            "event_id": short_id,
            "short_id": short_id,
            "sed_event_resource_id": resource,
            "origin_time": event.get("origin_time_utc") or event.get("origin_time") or "",
            "magnitude": event.get("magnitude", ""),
            "magnitude_type": event.get("magnitude_type", ""),
            "region": event.get("region", ""),
            "location_class": event.get("location_class", ""),
            "network": "CH",
            "channel": "HHZ",
            "source_provider": "SED/ETH EIDA https://eida.ethz.ch",
            "download_status": "failed",
            "verification_status": "NOT_RUN",
            "StationXML_status": "unavailable",
            "same_station_pick_status": "missing",
        }
    )
    row.update(overrides)
    return row


def empty_pick_row(event: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    row = {key: "" for key in PICK_MANIFEST_FIELDS}
    row.update(
        {
            "short_id": event_short_id(str(event.get("short_id") or event.get("event_id") or "")),
            "sed_event_resource_id": str(event.get("event_id") or event.get("sed_event_resource_id") or ""),
            "origin_time": event.get("origin_time_utc") or event.get("origin_time") or "",
            "network": "CH",
            "pick_source": "SED QuakeML includearrivals",
            "same_station_pick_status": "missing",
        }
    )
    row.update(overrides)
    return row


def cohort_short_ids_from_rows(rows: list[dict[str, Any]], locked_ids: list[str]) -> list[str]:
    """Failed downloads must not drop locked Set C events."""
    present = {event_short_id(str(row.get("short_id") or row.get("event_id") or "")) for row in rows}
    missing = [item for item in locked_ids if item not in present]
    return list(locked_ids) if not missing else list(locked_ids)


def summarize_acquisition(rows: list[dict[str, Any]], locked_ids: list[str]) -> dict[str, Any]:
    by_event: dict[str, list[dict[str, Any]]] = {sid: [] for sid in locked_ids}
    for row in rows:
        sid = event_short_id(str(row.get("short_id") or row.get("event_id") or ""))
        if sid in by_event:
            by_event[sid].append(row)

    def _any(sid: str, pred) -> bool:
        return any(pred(row) for row in by_event[sid])

    downloaded = [sid for sid in locked_ids if _any(sid, lambda r: r.get("download_status") == "ok")]
    verified = [
        sid
        for sid in locked_ids
        if _any(sid, lambda r: r.get("download_status") == "ok" and r.get("verification_status") in {"PASS", "PARTIAL"})
    ]
    stationxml_ok = [
        sid for sid in locked_ids if _any(sid, lambda r: r.get("StationXML_status") == "verified")
    ]
    stationxml_missing = [sid for sid in locked_ids if sid not in stationxml_ok]
    with_picks = [
        sid
        for sid in locked_ids
        if _any(sid, lambda r: str(r.get("same_station_pick_status") or "").startswith(("manual", "automatic", "ch_first")))
    ]
    failed_rows = [row for row in rows if row.get("download_status") != "ok"]
    incomplete = [
        row
        for row in rows
        if row.get("download_status") == "ok" and row.get("coverage_status") != "full"
    ]
    gapped = [
        row
        for row in rows
        if row.get("download_status") == "ok"
        and (int(row.get("gaps") or 0) > 0 or int(row.get("overlaps") or 0) > 0)
    ]
    return {
        "n_set_c_events": len(locked_ids),
        "set_c_ids": list(locked_ids),
        "set_c_unchanged": present_ids_match(rows, locked_ids),
        "events_with_downloaded_hhz": len(downloaded),
        "events_with_verified_miniseed": len(verified),
        "events_with_stationxml_verified": len(stationxml_ok),
        "events_without_stationxml_verified": len(stationxml_missing),
        "events_with_same_station_sed_first_p": len(with_picks),
        "downloaded_event_ids": downloaded,
        "verified_event_ids": verified,
        "stationxml_verified_event_ids": stationxml_ok,
        "stationxml_not_verified_event_ids": stationxml_missing,
        "same_station_pick_event_ids": with_picks,
        "n_waveform_rows": len(rows),
        "n_download_ok": sum(1 for row in rows if row.get("download_status") == "ok"),
        "n_download_failed": len(failed_rows),
        "n_incomplete_coverage": len(incomplete),
        "n_gap_or_overlap": len(gapped),
        "failed_downloads": [
            {
                "short_id": row.get("short_id"),
                "station": row.get("station"),
                "download_status": row.get("download_status"),
                "reason": row.get("download_reason"),
            }
            for row in failed_rows
        ],
        "incomplete_waveform_records": [
            {
                "short_id": row.get("short_id"),
                "station": row.get("station"),
                "coverage_status": row.get("coverage_status"),
                "verification_status": row.get("verification_status"),
            }
            for row in incomplete
        ],
        "gap_overlap_records": [
            {
                "short_id": row.get("short_id"),
                "station": row.get("station"),
                "gaps": row.get("gaps"),
                "overlaps": row.get("overlaps"),
            }
            for row in gapped
        ],
        "sta_lta_run": False,
        "validation_metrics_calculated": False,
        "threshold_8_unchanged": True,
    }


def present_ids_match(rows: list[dict[str, Any]], locked_ids: list[str]) -> bool:
    present = {event_short_id(str(row.get("short_id") or row.get("event_id") or "")) for row in rows}
    present.discard("")
    return set(locked_ids) <= present and len(locked_ids) == 15


def write_csv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})


def proposed_events_from_candidate_csv(path: str | Path, locked_ids: list[str]) -> list[dict[str, Any]]:
    """Return locked Set C rows in locked order. Does not reselection."""
    by_id: dict[str, dict[str, Any]] = {}
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if str(row.get("proposed_validation") or "").lower() != "yes":
                continue
            by_id[row["short_id"]] = dict(row)
    missing = [sid for sid in locked_ids if sid not in by_id]
    if missing:
        raise AcquisitionConfigurationError(f"locked Set C IDs missing from candidate CSV: {missing}")
    extra = sorted(set(by_id) - set(locked_ids))
    if extra:
        raise AcquisitionConfigurationError(f"candidate CSV proposed IDs are not the locked Set C: {extra}")
    return [by_id[sid] for sid in locked_ids]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _posix(value: Any) -> str:
    return Path(str(value or "")).as_posix()
