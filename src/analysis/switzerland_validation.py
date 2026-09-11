"""Frozen independent Swiss/Adjacent-Border validation helpers (STEP 2K).

Reuses the established Swiss causal-velocity STA/LTA implementation.
Does not retune threshold 8.0 and does not invent a new detector.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import yaml
from obspy import UTCDateTime
from pathlib import Path

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.switzerland_pilot import event_short_id
from src.acquisition.switzerland_validation_audit import (
    load_validation_audit_config,
    locked_proposed_short_ids,
    window_offsets,
)
from src.analysis.switzerland_signal import load_swiss_analysis_config
from src.analysis.switzerland_sta_lta_transfer import first_in_window, window_pair

TRACE_METRIC_FIELDS: tuple[str, ...] = (
    "short_id",
    "station",
    "location",
    "channel",
    "magnitude",
    "region",
    "location_class",
    "origin_time_utc",
    "processing_status",
    "failure_reason",
    "has_usable_same_station_p",
    "reference_p_time_utc",
    "reference_p_latency_s",
    "reference_p_phase",
    "reference_p_mode",
    "detection_status",
    "trigger_time_utc",
    "trigger_latency_s",
    "trigger_minus_p_s",
    "abs_trigger_minus_p_s",
    "trigger_at_or_after_p",
    "n_onsets_noise_window",
    "has_noise_onset",
    "n_onsets_detection_window",
    "sampling_rate_hz",
    "mute_s",
    "units",
)

EVENT_SUMMARY_FIELDS: tuple[str, ...] = (
    "short_id",
    "magnitude",
    "region",
    "location_class",
    "n_records",
    "n_usable",
    "n_detected",
    "n_no_detection",
    "detection_percent",
    "n_usable_same_station_p",
    "n_paired_timing",
    "median_timing_error_s",
    "median_abs_timing_error_s",
    "percent_detected_at_or_after_p",
    "n_noise_onset_records",
    "noise_trigger_record_percent",
)


def load_validation_run_config(path: str | Path, *, repo_root: Path | None = None) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise AcquisitionConfigurationError(f"validation run config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    if not isinstance(config, dict):
        raise AcquisitionConfigurationError("validation run config must be a YAML mapping.")
    root = repo_root or config_path.resolve().parents[1]
    audit = load_validation_audit_config(root / config["audit_config"])
    signal = load_swiss_analysis_config(root / config["signal_processing_config"])
    validate_validation_run_config(config, audit, signal)
    config["_audit"] = audit
    config["_signal"] = signal
    return config


def validate_validation_run_config(config: dict[str, Any], audit: dict[str, Any], signal: dict[str, Any]) -> None:
    frozen = config.get("frozen_configuration") or {}
    audit_frozen = audit["frozen_configuration"]
    if float(frozen.get("trigger_on", 0)) != 8.0 or float(audit_frozen["trigger_on"]) != 8.0:
        raise AcquisitionConfigurationError("frozen trigger_on must remain 8.0.")
    if float(frozen.get("trigger_off", 0)) != 0.5:
        raise AcquisitionConfigurationError("frozen trigger_off must remain 0.5.")
    if float(frozen.get("sta_window_s", 0)) != 0.5 or float(frozen.get("lta_window_s", 0)) != 10.0:
        raise AcquisitionConfigurationError("frozen STA/LTA windows must remain 0.5 / 10 s.")
    if frozen.get("component") != "HHZ":
        raise AcquisitionConfigurationError("frozen component must remain HHZ.")
    if list(frozen.get("bandpass_hz")) != [0.1, 15.0]:
        raise AcquisitionConfigurationError("frozen band-pass must remain 0.1–15 Hz.")
    if float(frozen.get("search_start_offset_s", -1)) != 0.0:
        raise AcquisitionConfigurationError("detection must start at origin.")
    if float(frozen.get("search_end_offset_s", 0)) != 90.0:
        raise AcquisitionConfigurationError("detection must end at origin + 90 s.")
    if window_offsets(config) != window_offsets(audit):
        raise AcquisitionConfigurationError("validation windows must match the audit windows.")
    if window_offsets(config)["detection"][0] < 0.0:
        raise AcquisitionConfigurationError("detection must not begin before origin.")
    boundary = config.get("scientific_boundary") or {}
    for key in ("retune_threshold", "sweep_thresholds", "reselection_set_c", "modify_set_a", "modify_california", "train_ml"):
        if boundary.get(key) is not False:
            raise AcquisitionConfigurationError(f"scientific_boundary.{key} must be false.")
    if float(signal["bandpass"]["freqmin_hz"]) != 0.1 or float(signal["bandpass"]["freqmax_hz"]) != 15.0:
        raise AcquisitionConfigurationError("signal-processing band-pass must remain 0.1–15 Hz.")
    if str(signal["instrument_response"]["output"]).upper() != "VEL":
        raise AcquisitionConfigurationError("instrument_response.output must remain VEL.")
    locked = locked_proposed_short_ids(audit)
    if len(locked) != 15:
        raise AcquisitionConfigurationError("Set C must remain 15 locked event IDs.")


def locked_set_c_ids(config: dict[str, Any]) -> list[str]:
    return locked_proposed_short_ids(config["_audit"])


def same_station_pick_for_record(picks: list[dict[str, Any]], short_id: str, station: str) -> dict[str, Any] | None:
    """Return the stored same-station SED first-P. Event-level (blank station) is ignored."""
    wanted_event = event_short_id(short_id)
    wanted_station = str(station or "").strip().upper()
    if not wanted_station:
        return None
    matches = []
    for pick in picks:
        if event_short_id(str(pick.get("short_id") or pick.get("event_id") or "")) != wanted_event:
            continue
        if str(pick.get("network") or "CH").upper() != "CH":
            continue
        if str(pick.get("station") or "").strip().upper() != wanted_station:
            continue
        if not str(pick.get("pick_time_utc") or "").strip():
            continue
        matches.append(pick)
    if not matches:
        return None
    matches.sort(key=lambda item: str(item.get("pick_time_utc") or ""))
    return dict(matches[0])


def detection_status(trigger_time: UTCDateTime | None) -> str:
    return "DETECTED" if trigger_time is not None else "NO_DETECTION"


def timing_error_s(trigger_time: UTCDateTime | None, reference_p: UTCDateTime | None) -> float:
    if trigger_time is None or reference_p is None:
        return float("nan")
    return float(trigger_time - reference_p)


def first_detection_onset(
    onset_times: list[UTCDateTime],
    origin: UTCDateTime,
    search_start_offset_s: float,
    search_end_offset_s: float,
) -> UTCDateTime | None:
    if search_start_offset_s < 0.0:
        raise AcquisitionConfigurationError("detection must not begin before origin.")
    start, end = window_pair(origin, search_start_offset_s, search_end_offset_s)
    return first_in_window(onset_times, start, end)


def count_noise_onsets(
    onset_times: list[UTCDateTime],
    origin: UTCDateTime,
    noise_start_offset_s: float,
    noise_end_offset_s: float,
) -> int:
    start, end = window_pair(origin, noise_start_offset_s, noise_end_offset_s)
    return sum(1 for t in onset_times if start <= t < end)


def yes_no(flag: bool) -> str:
    return "yes" if bool(flag) else "no"


def apply_timing_fields(
    row: dict[str, Any],
    origin: UTCDateTime,
    trigger: UTCDateTime | None,
    reference_p: UTCDateTime | None,
) -> dict[str, Any]:
    """Fill trigger/reference timing columns. Missing pairs stay NaN, not dropped."""
    row["detection_status"] = detection_status(trigger)
    row["trigger_time_utc"] = str(trigger) if trigger is not None else ""
    row["trigger_latency_s"] = float(trigger - origin) if trigger is not None else float("nan")
    row["reference_p_time_utc"] = str(reference_p) if reference_p is not None else ""
    row["reference_p_latency_s"] = float(reference_p - origin) if reference_p is not None else float("nan")
    err = timing_error_s(trigger, reference_p)
    row["trigger_minus_p_s"] = err
    row["abs_trigger_minus_p_s"] = abs(err) if err == err else float("nan")
    if trigger is not None and reference_p is not None:
        row["trigger_at_or_after_p"] = yes_no(float(trigger - reference_p) >= 0.0)
    else:
        row["trigger_at_or_after_p"] = ""
    return row


def finite_median(values: list[float] | np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    return float(np.median(arr))


def summarize_trace_rows(rows: list[dict[str, Any]], locked_ids: list[str]) -> dict[str, Any]:
    usable = [row for row in rows if row.get("processing_status") == "ok"]
    detected = [row for row in usable if row.get("detection_status") == "DETECTED"]
    no_det = [row for row in usable if row.get("detection_status") == "NO_DETECTION"]
    with_p = [row for row in usable if str(row.get("has_usable_same_station_p") or "") in {"yes", "True", "true"}]
    paired = [row for row in detected if str(row.get("has_usable_same_station_p") or "") in {"yes", "True", "true"}]
    abs_err = [float(row["abs_trigger_minus_p_s"]) for row in paired]
    after = [row for row in paired if str(row.get("trigger_at_or_after_p") or "") in {"yes", "True", "true"}]
    noise = [row for row in usable if str(row.get("has_noise_onset") or "") in {"yes", "True", "true"}]
    n_usable = len(usable)
    n_detected = len(detected)
    n_paired = len(paired)
    present = {event_short_id(str(row.get("short_id") or "")) for row in rows}
    return {
        "n_records_processed": len(rows),
        "n_usable_station_event_records": n_usable,
        "n_processing_failures": len(rows) - n_usable,
        "n_detected": n_detected,
        "n_no_detection": len(no_det),
        "detection_percent": 100.0 * n_detected / n_usable if n_usable else float("nan"),
        "no_detection_percent": 100.0 * len(no_det) / n_usable if n_usable else float("nan"),
        "n_usable_same_station_independent_p": len(with_p),
        "n_paired_trigger_and_p": n_paired,
        "median_abs_timing_error_s": finite_median(abs_err),
        "median_timing_error_s": finite_median([float(row["trigger_minus_p_s"]) for row in paired]),
        "percent_detected_at_or_after_p": 100.0 * len(after) / n_paired if n_paired else float("nan"),
        "n_records_with_noise_onset": len(noise),
        "pre_event_noise_trigger_rate": (len(noise) / n_usable) if n_usable else float("nan"),
        "set_c_ids_present": sorted(sid for sid in locked_ids if sid in present),
        "set_c_unchanged": set(locked_ids) <= present and len(locked_ids) == 15,
        "frozen_trigger_on": 8.0,
        "sta_lta_retuned": False,
    }


def event_summary_rows(rows: list[dict[str, Any]], locked_ids: list[str]) -> list[dict[str, Any]]:
    by_event: dict[str, list[dict[str, Any]]] = {sid: [] for sid in locked_ids}
    for row in rows:
        sid = event_short_id(str(row.get("short_id") or ""))
        if sid in by_event:
            by_event[sid].append(row)
    out: list[dict[str, Any]] = []
    for sid in locked_ids:
        group = by_event[sid]
        usable = [row for row in group if row.get("processing_status") == "ok"]
        detected = [row for row in usable if row.get("detection_status") == "DETECTED"]
        paired = [
            row
            for row in detected
            if str(row.get("has_usable_same_station_p") or "") in {"yes", "True", "true"}
        ]
        after = [row for row in paired if str(row.get("trigger_at_or_after_p") or "") in {"yes", "True", "true"}]
        noise = [row for row in usable if str(row.get("has_noise_onset") or "") in {"yes", "True", "true"}]
        proto = group[0] if group else {}
        n_usable = len(usable)
        n_paired = len(paired)
        out.append(
            {
                "short_id": sid,
                "magnitude": proto.get("magnitude", ""),
                "region": proto.get("region", ""),
                "location_class": proto.get("location_class", ""),
                "n_records": len(group),
                "n_usable": n_usable,
                "n_detected": len(detected),
                "n_no_detection": sum(1 for row in usable if row.get("detection_status") == "NO_DETECTION"),
                "detection_percent": 100.0 * len(detected) / n_usable if n_usable else float("nan"),
                "n_usable_same_station_p": sum(
                    1 for row in usable if str(row.get("has_usable_same_station_p") or "") in {"yes", "True", "true"}
                ),
                "n_paired_timing": n_paired,
                "median_timing_error_s": finite_median([float(row["trigger_minus_p_s"]) for row in paired]),
                "median_abs_timing_error_s": finite_median([float(row["abs_trigger_minus_p_s"]) for row in paired]),
                "percent_detected_at_or_after_p": 100.0 * len(after) / n_paired if n_paired else float("nan"),
                "n_noise_onset_records": len(noise),
                "noise_trigger_record_percent": 100.0 * len(noise) / n_usable if n_usable else float("nan"),
            }
        )
    return out
