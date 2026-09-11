"""Tests for STEP 2J validation acquisition helpers (no network, no STA/LTA)."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pytest
import yaml
from obspy import Stream, Trace, UTCDateTime
from obspy.core.inventory import Channel, Inventory, Network, Response, Station
from obspy.core.inventory.response import InstrumentSensitivity
from obspy.core.inventory.util import Site

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.switzerland_validation_acquisition import (
    WAVEFORM_MANIFEST_FIELDS,
    acquisition_interval,
    cohort_short_ids_from_rows,
    detection_interval,
    empty_waveform_row,
    inspect_miniseed_stream,
    load_validation_acquisition_config,
    locked_set_c_ids,
    noise_interval,
    preferred_same_station_first_p,
    present_ids_match,
    proposed_events_from_candidate_csv,
    quakeml_eventid_candidates,
    select_same_station_hhz_targets,
    stationxml_hhz_status,
    summarize_acquisition,
    validate_validation_acquisition_config,
    waveform_filename,
)
from src.acquisition.switzerland_validation_audit import locked_proposed_short_ids, window_offsets

REPO = Path(__file__).resolve().parents[1]
ACQ_CONFIG = REPO / "configs" / "sed_switzerland_validation_acquisition.yaml"
AUDIT_CONFIG = REPO / "configs" / "sed_switzerland_validation_audit.yaml"
CANDIDATE_CSV = REPO / "data" / "manifests" / "sed_switzerland_validation_candidates.csv"
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


def test_windows_match_audit_and_do_not_start_detection_before_origin():
    config = load_validation_acquisition_config(ACQ_CONFIG)
    origin = UTCDateTime("2024-01-26T23:06:45")
    acq_start, acq_end = acquisition_interval(origin, config)
    det_start, det_end = detection_interval(origin, config)
    noise_start, noise_end = noise_interval(origin, config)
    assert abs(float(origin - acq_start) - 60.0) < 1e-9
    assert abs(float(acq_end - origin) - 90.0) < 1e-9
    assert abs(float(det_start - origin) - 0.0) < 1e-9
    assert abs(float(det_end - origin) - 90.0) < 1e-9
    assert abs(float(origin - noise_start) - 60.0) < 1e-9
    assert abs(float(origin - noise_end) - 10.0) < 1e-9
    assert det_start >= origin
    assert window_offsets(config) == window_offsets(config["_audit"])


def test_frozen_threshold_and_scientific_boundary_remain_off():
    config = load_validation_acquisition_config(ACQ_CONFIG)
    assert config["frozen_configuration"]["trigger_on"] == 8.0
    assert config["_audit"]["frozen_configuration"]["trigger_on"] == 8.0
    boundary = config["scientific_boundary"]
    assert boundary["run_sta_lta"] is False
    assert boundary["compute_validation_metrics"] is False
    assert boundary["retune_threshold"] is False
    assert boundary["reselection_set_c"] is False
    assert config["output"]["raw_dir"] == "data/raw/switzerland_validation"
    assert config["output"]["raw_dir"] != "data/raw/switzerland"


def test_set_c_locked_ids_match_candidate_csv():
    config = load_validation_acquisition_config(ACQ_CONFIG)
    locked = locked_set_c_ids(config)
    assert locked == LOCKED
    assert locked == locked_proposed_short_ids(config["_audit"])
    events = proposed_events_from_candidate_csv(CANDIDATE_CSV, locked)
    assert [row["short_id"] for row in events] == LOCKED
    assert len(events) == 15


def test_full_sed_resource_ids_are_preferred():
    resource = "smi:ch.ethz.sed/sc20a/Event/2024bvrces"
    candidates = quakeml_eventid_candidates("2024bvrces", resource)
    assert candidates[0] == resource
    assert "2024bvrces" in candidates


def test_same_station_matching_ignores_event_level_and_other_stations():
    origin = UTCDateTime("2024-01-01T00:00:00")
    start, end = origin - 60.0, origin + 90.0
    picks = [
        {"network": "CH", "station": "", "channel": "HHZ", "phase": "P", "time_utc": "2024-01-01T00:00:05", "evaluation_mode": "manual"},
        {"network": "CH", "station": "BALST", "channel": "HHZ", "phase": "P", "time_utc": "2024-01-01T00:00:08", "evaluation_mode": "manual", "location": ""},
        {"network": "CH", "station": "DAVAX", "channel": "HHN", "phase": "Pg", "time_utc": "2024-01-01T00:00:09", "evaluation_mode": "manual", "location": ""},
        {"network": "FR", "station": "OGGY", "channel": "HHZ", "phase": "P", "time_utc": "2024-01-01T00:00:07", "evaluation_mode": "manual"},
        {"network": "CH", "station": "BALST", "channel": "HHZ", "phase": "S", "time_utc": "2024-01-01T00:00:20", "evaluation_mode": "manual"},
    ]
    availability = [
        {"network": "CH", "station": "BALST", "location": "", "channel": "HHZ", "earliest": start, "latest": end},
        {"network": "CH", "station": "FUSIO", "location": "", "channel": "HHZ", "earliest": start, "latest": end},
        {"network": "CH", "station": "DAVAX", "location": "", "channel": "HHZ", "earliest": start, "latest": end},
    ]
    targets = select_same_station_hhz_targets(picks, availability, start, end)
    stations = [item["station"] for item in targets]
    assert stations == ["BALST", "DAVAX"]
    assert "FUSIO" not in stations
    pick = preferred_same_station_first_p(picks, "BALST")
    assert pick is not None
    assert pick["phase"] == "P"
    assert pick["time_utc"] == "2024-01-01T00:00:08"


def test_miniseed_inspection_is_structural_only():
    origin = UTCDateTime("2024-01-01T00:00:00")
    start, end = origin - 60.0, origin + 90.0
    npts = int(150.0 * 100.0)
    data = np.arange(npts, dtype=np.float64)
    trace = Trace(
        data=data,
        header={
            "network": "CH",
            "station": "BALST",
            "location": "",
            "channel": "HHZ",
            "sampling_rate": 100.0,
            "starttime": start,
        },
    )
    inspection = inspect_miniseed_stream(
        Stream([trace]),
        requested_start=start,
        requested_end=end,
        expected_station="BALST",
    )
    assert inspection.readable is True
    assert inspection.verification_status == "PASS"
    assert inspection.coverage_status == "full"
    assert inspection.channel == "HHZ"
    assert inspection.sample_count == npts
    assert inspection.gaps == 0

    short = Trace(
        data=np.arange(1000, dtype=np.float64),
        header={
            "network": "CH",
            "station": "BALST",
            "channel": "HHZ",
            "sampling_rate": 100.0,
            "starttime": origin,
        },
    )
    partial = inspect_miniseed_stream(
        Stream([short]),
        requested_start=start,
        requested_end=end,
        expected_station="BALST",
    )
    assert partial.coverage_status == "partial"
    assert partial.verification_status == "PARTIAL"


def test_stationxml_status_is_not_falsely_verified():
    origin = UTCDateTime("2024-01-01T00:00:00")
    start, end = origin - 60.0, origin + 90.0
    empty = Inventory(networks=[], source="test")
    status, reason = stationxml_hhz_status(
        empty, network="CH", station="BALST", location="", channel="HHZ", start=start, end=end
    )
    assert status == "unavailable"
    assert status != "verified"

    channel = Channel(
        code="HHZ",
        location_code="",
        latitude=47.0,
        longitude=8.0,
        elevation=0.0,
        depth=0.0,
        start_date=start - 86400,
        end_date=end + 86400,
        sample_rate=100.0,
        response=Response(
            instrument_sensitivity=InstrumentSensitivity(
                value=1.0, frequency=1.0, input_units="M/S", output_units="COUNTS"
            )
        ),
    )
    station = Station(
        code="BALST",
        latitude=47.0,
        longitude=8.0,
        elevation=0.0,
        channels=[channel],
        site=Site(name="test"),
    )
    inventory = Inventory(networks=[Network(code="CH", stations=[station])], source="test")
    ok, ok_reason = stationxml_hhz_status(
        inventory, network="CH", station="BALST", location="", channel="HHZ", start=start, end=end
    )
    assert ok == "verified"
    assert "response" in ok_reason

    other = stationxml_hhz_status(
        inventory, network="CH", station="DAVAX", location="", channel="HHZ", start=start, end=end
    )
    assert other[0] != "verified"


def test_failed_downloads_do_not_remove_set_c_events():
    locked = list(LOCKED)
    rows = [
        empty_waveform_row({"short_id": sid, "event_id": f"smi:ch.ethz.sed/{sid}"}, download_status="failed", download_reason="NO_DATA")
        for sid in locked
    ]
    rows[0]["download_status"] = "ok"
    rows[0]["station"] = "BALST"
    rows[0]["verification_status"] = "PASS"
    rows[0]["same_station_pick_status"] = "manual_ch_first_p"
    assert present_ids_match(rows, locked)
    kept = cohort_short_ids_from_rows(rows, locked)
    assert kept == locked
    summary = summarize_acquisition(rows, locked)
    assert summary["n_set_c_events"] == 15
    assert summary["set_c_unchanged"] is True
    assert summary["events_with_downloaded_hhz"] == 1
    assert summary["n_download_failed"] == 14
    assert summary["sta_lta_run"] is False
    assert summary["validation_metrics_calculated"] is False
    assert list(empty_waveform_row({"short_id": "2024bvrces"}).keys()) == list(WAVEFORM_MANIFEST_FIELDS)


def test_acquisition_config_rejects_set_a_output_and_retuned_threshold():
    payload = yaml.safe_load(ACQ_CONFIG.read_text(encoding="utf-8"))
    audit = yaml.safe_load(AUDIT_CONFIG.read_text(encoding="utf-8"))
    payload["output"]["raw_dir"] = "data/raw/switzerland"
    with pytest.raises(AcquisitionConfigurationError, match="Set A"):
        validate_validation_acquisition_config(payload, audit)
    payload = yaml.safe_load(ACQ_CONFIG.read_text(encoding="utf-8"))
    payload["frozen_configuration"]["trigger_on"] = 7.5
    with pytest.raises(AcquisitionConfigurationError, match="8.0"):
        validate_validation_acquisition_config(payload, audit)
    payload = yaml.safe_load(ACQ_CONFIG.read_text(encoding="utf-8"))
    payload["station_selection"]["copy_set_a_distance_bins"] = True
    with pytest.raises(AcquisitionConfigurationError, match="distance-bin"):
        validate_validation_acquisition_config(payload, audit)


def test_deterministic_filename():
    origin = UTCDateTime("2024-01-26T23:06:45")
    name = waveform_filename("CH", "BALST", "", "HHZ", origin)
    assert name == "CH.BALST.--.HHZ.20240126T230645.mseed"


def test_candidate_csv_proposed_column_still_has_exactly_15():
    proposed = []
    with CANDIDATE_CSV.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("proposed_validation") == "yes":
                proposed.append(row["short_id"])
    assert proposed == LOCKED


def test_tracked_waveform_manifest_keeps_locked_set_c_and_does_not_reselect():
    path = REPO / "data" / "manifests" / "sed_switzerland_validation_waveforms.csv"
    assert path.exists()
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    ids = []
    for row in rows:
        sid = row["short_id"]
        if sid not in ids:
            ids.append(sid)
        assert row["channel"] == "HHZ"
        assert row["network"] == "CH"
    assert ids == LOCKED
    assert set(ids) == set(LOCKED)
    assert len(ids) == 15
    assert all(row["MiniSEED_path"].startswith("data/raw/switzerland_validation/") for row in rows)

