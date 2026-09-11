"""Tests for frozen independent Swiss validation helpers (no network, no retuning)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from obspy import UTCDateTime

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.switzerland_validation_audit import locked_proposed_short_ids, window_offsets
from src.analysis.switzerland_validation import (
    EVENT_SUMMARY_FIELDS,
    TRACE_METRIC_FIELDS,
    apply_timing_fields,
    count_noise_onsets,
    detection_status,
    event_summary_rows,
    first_detection_onset,
    load_validation_run_config,
    same_station_pick_for_record,
    summarize_trace_rows,
    timing_error_s,
    validate_validation_run_config,
    yes_no,
)

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / "configs" / "sed_switzerland_validation.yaml"
AUDIT = REPO / "configs" / "sed_switzerland_validation_audit.yaml"
LOCKED = [
    "2020flmsvb",
    "2020vcnoon",
    "2021ffattd",
    "2021toxjpc",
    "2022gzvhhy",
    "2022isnvgj",
    "2022ugepue",
    "2023ksedgz",
    "2024bvrces",
    "2024cxfhdh",
    "2024ftcvhn",
    "2024ujblmf",
    "2025phgpma",
    "2025rtcqvh",
    "2026bklhob",
]


def test_frozen_threshold_and_detection_window_start_at_origin():
    config = load_validation_run_config(CONFIG)
    frozen = config["frozen_configuration"]
    assert frozen["trigger_on"] == 8.0
    assert frozen["trigger_off"] == 0.5
    assert frozen["sta_window_s"] == 0.5
    assert frozen["lta_window_s"] == 10.0
    assert frozen["component"] == "HHZ"
    assert frozen["search_start_offset_s"] == 0.0
    assert frozen["search_end_offset_s"] == 90.0
    offsets = window_offsets(config)
    assert offsets["detection"] == (0.0, 90.0)
    assert offsets["detection"][0] >= 0.0
    assert offsets["acquisition"] == (-60.0, 90.0)
    assert offsets["pre_event_noise"] == (-60.0, -10.0)
    assert locked_proposed_short_ids(config["_audit"]) == LOCKED
    assert config["scientific_boundary"]["retune_threshold"] is False
    assert config["scientific_boundary"]["sweep_thresholds"] is False


def test_config_rejects_retuned_threshold_and_pre_origin_detection():
    payload = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    audit = yaml.safe_load(AUDIT.read_text(encoding="utf-8"))
    signal = yaml.safe_load((REPO / "configs" / "swiss_signal_analysis.yaml").read_text(encoding="utf-8"))
    payload["frozen_configuration"]["trigger_on"] = 6.0
    with pytest.raises(AcquisitionConfigurationError, match="8.0"):
        validate_validation_run_config(payload, audit, signal)
    payload = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    payload["frozen_configuration"]["search_start_offset_s"] = -5.0
    with pytest.raises(AcquisitionConfigurationError, match="origin"):
        validate_validation_run_config(payload, audit, signal)


def test_same_station_reference_matching_ignores_event_level():
    picks = [
        {"short_id": "2024bvrces", "network": "CH", "station": "", "pick_time_utc": "2024-01-26T23:06:50Z"},
        {"short_id": "2024bvrces", "network": "CH", "station": "DAVOX", "pick_time_utc": "2024-01-26T23:07:01Z", "pick_phase": "Pg"},
        {"short_id": "2024bvrces", "network": "CH", "station": "FUORN", "pick_time_utc": "2024-01-26T23:07:10Z"},
        {"short_id": "2020flmsvb", "network": "CH", "station": "DAVOX", "pick_time_utc": "2020-03-18T01:55:00Z"},
    ]
    davox = same_station_pick_for_record(picks, "2024bvrces", "DAVOX")
    assert davox is not None
    assert davox["pick_time_utc"].startswith("2024-01-26T23:07:01")
    assert same_station_pick_for_record(picks, "2024bvrces", "BALST") is None
    assert same_station_pick_for_record(picks, "2024bvrces", "") is None


def test_no_detection_and_timing_error():
    origin = UTCDateTime("2024-01-26T23:06:45")
    p_time = origin + 12.0
    first_valid = origin + 14.0
    later = origin + 20.0
    early = origin - 4.0
    noise = origin - 40.0
    times = [noise, early, first_valid, later]
    trigger = first_detection_onset(times, origin, 0.0, 90.0)
    assert trigger == first_valid
    assert trigger != later
    assert detection_status(trigger) == "DETECTED"
    assert abs(timing_error_s(trigger, p_time) - 2.0) < 1e-9
    assert first_detection_onset([noise, early], origin, 0.0, 90.0) is None
    assert detection_status(None) == "NO_DETECTION"
    assert timing_error_s(None, p_time) != timing_error_s(None, p_time)
    row = apply_timing_fields({}, origin, trigger, p_time)
    assert row["trigger_at_or_after_p"] == "yes"
    assert row["abs_trigger_minus_p_s"] == 2.0
    early_row = apply_timing_fields({}, origin, origin + 5.0, p_time)
    assert early_row["trigger_at_or_after_p"] == "no"
    none_row = apply_timing_fields({}, origin, None, p_time)
    assert none_row["detection_status"] == "NO_DETECTION"
    assert none_row["trigger_at_or_after_p"] == ""
    with pytest.raises(AcquisitionConfigurationError, match="before origin"):
        first_detection_onset(times, origin, -5.0, 90.0)
    assert yes_no(True) == "yes"


def test_pre_event_noise_trigger_count_excludes_detection_window():
    origin = UTCDateTime("2024-01-26T23:06:45")
    times = [origin - 70.0, origin - 40.0, origin - 10.0, origin - 9.0, origin + 5.0]
    assert count_noise_onsets(times, origin, -60.0, -10.0) == 1


def test_schema_and_no_detection_preserved_in_summary():
    locked = list(LOCKED)
    rows = []
    for i, sid in enumerate(locked):
        detected = i != 0
        paired = detected and i != 1
        rows.append(
            {
                "short_id": sid,
                "magnitude": 3.0,
                "region": "test",
                "location_class": "swiss_territory",
                "processing_status": "ok",
                "detection_status": "DETECTED" if detected else "NO_DETECTION",
                "has_usable_same_station_p": "yes",
                "trigger_minus_p_s": 1.5 if paired else float("nan"),
                "abs_trigger_minus_p_s": 1.5 if paired else float("nan"),
                "trigger_at_or_after_p": "yes" if paired else "no",
                "has_noise_onset": "yes" if i == 2 else "no",
            }
        )
    summary = summarize_trace_rows(rows, locked)
    assert summary["n_records_processed"] == 15
    assert summary["n_no_detection"] == 1
    assert summary["n_detected"] == 14
    assert summary["set_c_unchanged"] is True
    assert summary["frozen_trigger_on"] == 8.0
    events = event_summary_rows(rows, locked)
    assert [row["short_id"] for row in events] == locked
    assert events[0]["n_no_detection"] == 1
    assert list(TRACE_METRIC_FIELDS)[:3] == ["short_id", "station", "location"]
    assert "median_abs_timing_error_s" in EVENT_SUMMARY_FIELDS


def test_written_outputs_match_frozen_schema_when_present():
    reports = REPO / "reports" / "switzerland_validation"
    summary_path = reports / "validation_summary.json"
    traces_path = reports / "validation_trace_metrics.csv"
    events_path = reports / "validation_event_summary.csv"
    proc_path = reports / "processing_config.json"
    fail_path = reports / "failures.json"
    if not summary_path.exists():
        pytest.skip("validation outputs not generated yet")
    import csv
    import json

    traces = list(csv.DictReader(traces_path.open(encoding="utf-8")))
    events = list(csv.DictReader(events_path.open(encoding="utf-8")))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    proc = json.loads(proc_path.read_text(encoding="utf-8"))
    failures = json.loads(fail_path.read_text(encoding="utf-8"))
    assert [row["short_id"] for row in events] == LOCKED
    assert len(traces) == 550
    assert list(traces[0].keys()) == list(TRACE_METRIC_FIELDS)
    assert list(events[0].keys()) == list(EVENT_SUMMARY_FIELDS)
    assert any(row["detection_status"] == "NO_DETECTION" for row in traces)
    assert summary["frozen_trigger_on"] == 8.0
    assert summary["sta_lta_retuned"] is False
    assert proc["frozen_configuration"]["trigger_on"] == 8.0
    assert proc["frozen_configuration"]["search_start_offset_s"] == 0.0
    assert proc["threshold_retuned"] is False
    assert proc["threshold_is_optimal"] is False
    assert "processing_failures" in failures
