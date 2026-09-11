"""Tests for independent Swiss validation-set audit helpers (no network, no STA/LTA)."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from obspy import UTCDateTime

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.switzerland_validation_audit import (
    apply_window_offsets,
    classify_location,
    count_ch_p_picks,
    development_short_ids,
    exclusion_reason,
    first_p_station_codes,
    load_validation_audit_config,
    locked_proposed_short_ids,
    next_replacement,
    overlaps_development,
    parse_quakeml_picks,
    propose_validation_subset,
    same_station_reference_counts,
    short_ids_from_manifest_csv,
    unique_ch_stations_covering,
    validate_validation_audit_config,
    window_offsets,
)

CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "sed_switzerland_validation_audit.yaml"
PILOT_MANIFEST = Path(__file__).resolve().parents[1] / "data" / "manifests" / "sed_switzerland_pilot_events.csv"
PILOT_CONFIG = Path(__file__).resolve().parents[1] / "configs" / "sed_switzerland_pilot.yaml"


def test_frozen_configuration_is_not_retunable_in_audit_config():
    config = load_validation_audit_config(CONFIG_PATH)
    frozen = config["frozen_configuration"]
    assert frozen["trigger_on"] == 8.0
    assert frozen["sta_window_s"] == 0.5
    assert frozen["lta_window_s"] == 10.0
    assert frozen["component"] == "HHZ"
    assert frozen["search_start_offset_s"] == 0.0
    assert frozen["search_end_offset_s"] == 90.0
    offsets = window_offsets(config)
    assert offsets["acquisition"] == (-60.0, 90.0)
    assert offsets["detection"] == (0.0, 90.0)
    assert offsets["pre_event_noise"] == (-60.0, -10.0)
    locked = locked_proposed_short_ids(config)
    ids = development_short_ids(config)
    assert len(ids) == 20
    assert "2020btnrcj" in ids
    assert len(locked) == 15
    assert not (set(locked) & ids)


def test_audit_config_rejects_retuned_threshold():
    payload = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    payload["frozen_configuration"]["trigger_on"] = 7.5
    with pytest.raises(AcquisitionConfigurationError, match="8.0"):
        validate_validation_audit_config(payload)


def test_audit_config_rejects_detection_before_origin():
    payload = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    payload["windows"]["detection"]["start_offset_s"] = -5.0
    with pytest.raises(AcquisitionConfigurationError, match="origin"):
        validate_validation_audit_config(payload)


def test_development_ids_match_pilot_config_and_manifest():
    audit = load_validation_audit_config(CONFIG_PATH)
    audit_ids = development_short_ids(audit)
    pilot = yaml.safe_load(PILOT_CONFIG.read_text(encoding="utf-8"))
    assert set(pilot["event_ids"]) == audit_ids
    manifest_ids = short_ids_from_manifest_csv(PILOT_MANIFEST)
    assert manifest_ids == audit_ids
    assert len(manifest_ids) == 20


def test_overlap_and_exclusion_reasons():
    development = {"2020btnrcj", "2022rvutkg"}
    allowed = ["earthquake", "induced earthquake"]
    assert overlaps_development("smi:ch.ethz.sed/sc3a/2020btnrcj", development)
    assert not overlaps_development("2024abcdef", development)
    excluded = exclusion_reason(
        {
            "short_id": "2020btnrcj",
            "event_type": "earthquake",
            "magnitude": 3.2,
            "origin_time_utc": "2020-01-01T00:00:00",
            "latitude": 46.2,
            "longitude": 7.7,
        },
        development_ids=development,
        allowed_types=allowed,
        min_magnitude=2.5,
    )
    assert excluded == "in_development_20_event_set"
    not_eq = exclusion_reason(
        {
            "short_id": "2024abcdef",
            "event_type": "quarry blast",
            "magnitude": 3.2,
            "origin_time_utc": "2024-01-01T00:00:00",
            "latitude": 46.2,
            "longitude": 7.7,
        },
        development_ids=development,
        allowed_types=allowed,
        min_magnitude=2.5,
    )
    assert not_eq.startswith("event_type")
    keep = exclusion_reason(
        {
            "short_id": "2024abcdef",
            "event_type": "earthquake",
            "magnitude": 2.7,
            "origin_time_utc": "2024-06-01T00:00:00",
            "latitude": 46.2,
            "longitude": 7.7,
        },
        development_ids=development,
        allowed_types=allowed,
        min_magnitude=2.5,
    )
    assert keep == ""


def test_location_class_uses_region_suffix_and_box():
    box = {"minlatitude": 45.82, "maxlatitude": 47.81, "minlongitude": 5.96, "maxlongitude": 10.49}
    assert classify_location(47.75, 7.34, "Mulhouse F", box) == "immediate_border"
    assert classify_location(46.23, 7.71, "Graechen VS", box) == "swiss_territory"
    assert classify_location(45.50, 6.10, "Annecy F", box) == "immediate_border"
    assert classify_location(45.50, 10.80, "unnamed", box) == "immediate_border"
    assert classify_location(47.11, 9.57, "Vaduz FL", box) == "immediate_border"


def test_p_pick_counting_ignores_non_ch_and_s_phases():
    summary = count_ch_p_picks(
        [
            {"network": "CH", "station": "BALST", "channel": "HHZ", "phase": "P", "evaluation_mode": "manual"},
            {"network": "CH", "station": "BALST", "channel": "HHN", "phase": "Pg", "evaluation_mode": "manual"},
            {"network": "CH", "station": "DAVAX", "channel": "HHZ", "phase": "S", "evaluation_mode": "manual"},
            {"network": "FR", "station": "OGGY", "channel": "HHZ", "phase": "P", "evaluation_mode": "manual"},
            {"network": "CH", "station": "FUSIO", "channel": "HHZ", "phase": "Pn", "evaluation_mode": "automatic"},
        ]
    )
    assert summary["n_ch_p_picks"] == 3
    assert summary["n_ch_hhz_p_picks"] == 2
    assert summary["n_ch_manual_p_picks"] == 2
    assert summary["sed_p_pick_available"] == "yes"
    assert "manual" in summary["sed_p_pick_modes"]


def test_parse_quakeml_picks_from_minimal_event():
    xml = """<?xml version="1.0"?>
<q:quakeml xmlns:q="http://quakeml.org/xmlns/quakeml/1.2"
           xmlns="http://quakeml.org/xmlns/bed/1.2">
  <eventParameters publicID="smi:ch.ethz.sed/test">
    <event publicID="smi:ch.ethz.sed/sc3a/2024abcdef">
      <pick publicID="smi:ch.ethz.sed/pick/1">
        <time><value>2024-03-01T12:00:01.000000Z</value></time>
        <waveformID networkCode="CH" stationCode="BALST" channelCode="HHZ"/>
        <phaseHint>P</phaseHint>
        <evaluationMode>manual</evaluationMode>
      </pick>
    </event>
  </eventParameters>
</q:quakeml>
"""
    parsed = parse_quakeml_picks(xml)
    assert "2024abcdef" in parsed
    assert parsed["2024abcdef"][0]["station"] == "BALST"
    assert parsed["2024abcdef"][0]["phase"] == "P"


def test_propose_subset_excludes_development_and_spreads_strata():
    diversity = {
        "year_bins": [[2020, 2021], [2022, 2023], [2024, 2024], [2025, 2026]],
        "year_quotas": [4, 4, 4, 3],
        "min_swiss_territory": 6,
        "magnitude_bins": [[2.5, 3.0], [3.0, 3.5], [3.5, 4.0], [4.0, 10.0]],
        "lat_split": 46.85,
        "lon_split": 8.35,
    }
    pool = [
        {
            "short_id": "2020btnrcj",
            "in_development_set": True,
            "origin_time_utc": "2020-01-25T19:13:28",
            "magnitude": 3.0,
            "latitude": 46.2,
            "longitude": 7.7,
            "location_class": "swiss_territory",
            "n_ch_p_picks": 40,
            "n_hh_3c_stations_available": 20,
        }
    ]
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    mags = [2.6, 3.1, 3.6, 4.1]
    lats = [46.2, 47.2]
    lons = [7.2, 9.2]
    n = 0
    for year in years:
        for mag in mags:
            for lat in lats:
                for lon in lons:
                    n += 1
                    pool.append(
                        {
                            "short_id": f"evt{n:04d}",
                            "in_development_set": False,
                            "origin_time_utc": f"{year}-06-01T00:00:00",
                            "magnitude": mag,
                            "latitude": lat + 0.2 * (year - 2020),
                            "longitude": lon + 0.15 * (mag - 2.6),
                            "location_class": "swiss_territory" if lat < 47 else "immediate_border",
                            "n_ch_p_picks": 5 + n,
                            "n_hh_3c_stations_available": 3,
                        }
                    )
    selected = propose_validation_subset(pool, 15, diversity, min_separation_km=15.0)
    assert len(selected) == 15
    assert "2020btnrcj" not in selected
    assert len(set(selected)) == 15
    by_id = {e["short_id"]: e for e in pool}
    years = {int(str(by_id[sid]["origin_time_utc"])[:4]) for sid in selected}
    assert years & {2020, 2021}
    assert years & {2022, 2023}
    assert 2024 in years
    assert years & {2025, 2026}
    mags = [float(by_id[sid]["magnitude"]) for sid in selected]
    assert min(mags) < 3.0
    assert max(mags) >= 4.0
    n_swiss = sum(1 for sid in selected if by_id[sid].get("location_class") == "swiss_territory")
    assert n_swiss >= 6


def test_next_replacement_stays_in_year_and_skips_failed_availability():
    diversity = {
        "year_bins": [[2020, 2021], [2022, 2023], [2024, 2024], [2025, 2026]],
        "magnitude_bins": [[2.5, 3.0], [3.0, 3.5], [3.5, 4.0], [4.0, 10.0]],
        "lat_split": 46.85,
        "lon_split": 8.35,
    }
    selected = [
        {
            "short_id": "keep1",
            "origin_time_utc": "2024-01-01T00:00:00",
            "magnitude": 2.6,
            "latitude": 46.2,
            "longitude": 7.2,
        }
    ]
    failed = {
        "short_id": "fail1",
        "origin_time_utc": "2024-06-01T00:00:00",
        "magnitude": 2.7,
        "latitude": 47.8,
        "longitude": 7.4,
    }
    pool = selected + [
        failed,
        {
            "short_id": "same_year",
            "in_development_set": False,
            "origin_time_utc": "2024-08-01T00:00:00",
            "magnitude": 2.8,
            "latitude": 46.9,
            "longitude": 9.1,
            "n_ch_p_picks": 20,
            "hh_3c_availability_verified": "not_checked",
        },
        {
            "short_id": "other_year",
            "in_development_set": False,
            "origin_time_utc": "2022-08-01T00:00:00",
            "magnitude": 2.8,
            "latitude": 46.5,
            "longitude": 8.1,
            "n_ch_p_picks": 80,
            "hh_3c_availability_verified": "not_checked",
        },
        {
            "short_id": "no_hh",
            "in_development_set": False,
            "origin_time_utc": "2024-09-01T00:00:00",
            "magnitude": 2.8,
            "latitude": 47.1,
            "longitude": 8.5,
            "n_ch_p_picks": 90,
            "hh_3c_availability_verified": "no",
        },
    ]
    choice = next_replacement(pool, selected, failed, diversity, 15.0, same_year_only=True)
    assert choice is not None
    assert choice["short_id"] == "same_year"


def test_three_windows_are_distinct_and_detection_does_not_start_before_origin():
    config = load_validation_audit_config(CONFIG_PATH)
    origin = UTCDateTime("2024-01-26T23:06:45")
    offsets = window_offsets(config)
    acq_start, acq_end = apply_window_offsets(origin, *offsets["acquisition"])
    det_start, det_end = apply_window_offsets(origin, *offsets["detection"])
    noise_start, noise_end = apply_window_offsets(origin, *offsets["pre_event_noise"])
    assert abs(float(origin - acq_start) - 60.0) < 1e-9
    assert abs(float(acq_end - origin) - 90.0) < 1e-9
    assert abs(float(det_start - origin) - 0.0) < 1e-9
    assert abs(float(det_end - origin) - 90.0) < 1e-9
    assert abs(float(origin - noise_start) - 60.0) < 1e-9
    assert abs(float(origin - noise_end) - 10.0) < 1e-9
    assert det_start >= origin
    assert det_start > acq_start
    assert noise_end < origin
    assert noise_start == acq_start
    assert det_end == acq_end


def test_same_station_pick_matching_ignores_event_level_and_other_stations():
    picks = [
        {"network": "CH", "station": "", "channel": "HHZ", "phase": "P", "evaluation_mode": "manual"},
        {"network": "CH", "station": "BALST", "channel": "HHZ", "phase": "P", "evaluation_mode": "manual"},
        {"network": "CH", "station": "DAVAX", "channel": "HHN", "phase": "Pg", "evaluation_mode": "manual"},
        {"network": "FR", "station": "OGGY", "channel": "HHZ", "phase": "P", "evaluation_mode": "manual"},
    ]
    counts = same_station_reference_counts(picks, {"BALST", "FUSIO"})
    assert counts["has_event_level_picks"] is True
    assert counts["n_unique_ch_stations_with_first_p"] == 2
    assert counts["n_same_station_first_p_and_hhz"] == 1
    assert counts["n_same_station_hhz_first_p_and_hhz"] == 1
    assert first_p_station_codes(picks, channel="HHZ") == {"BALST"}


def test_unique_station_hh_3c_count_is_station_codes_not_channels():
    origin = UTCDateTime("2024-01-01T00:00:00")
    start = origin - 60.0
    end = origin + 90.0
    rows = [
        {"network": "CH", "station": "BALST", "channel": "HHZ", "earliest": start, "latest": end},
        {"network": "CH", "station": "BALST", "channel": "HHN", "earliest": start, "latest": end},
        {"network": "CH", "station": "BALST", "channel": "HHE", "earliest": start, "latest": end},
        {"network": "CH", "station": "DAVAX", "channel": "HHZ", "earliest": start, "latest": end},
        {"network": "CH", "station": "SHORT", "channel": "HHZ", "earliest": start + 10.0, "latest": end},
        {"network": "CH", "station": "SHORT", "channel": "HHN", "earliest": start + 10.0, "latest": end},
        {"network": "CH", "station": "SHORT", "channel": "HHE", "earliest": start + 10.0, "latest": end},
        {"network": "CH", "station": "EDGE", "channel": "HHZ", "earliest": start + 0.4, "latest": end - 0.4},
        {"network": "CH", "station": "EDGE", "channel": "HHN", "earliest": start + 0.4, "latest": end - 0.4},
        {"network": "CH", "station": "EDGE", "channel": "HHE", "earliest": start + 0.4, "latest": end - 0.4},
    ]
    hh3c = unique_ch_stations_covering(rows, start, end, ("HHZ", "HHN", "HHE"))
    hhz = unique_ch_stations_covering(rows, start, end, ("HHZ",))
    assert hh3c == {"BALST", "EDGE"}
    assert hhz == {"BALST", "DAVAX", "EDGE"}
    assert "SHORT" not in hh3c


def test_locked_set_c_matches_proposed_csv_rows():
    config = load_validation_audit_config(CONFIG_PATH)
    locked = set(locked_proposed_short_ids(config))
    csv_path = Path(__file__).resolve().parents[1] / "data" / "manifests" / "sed_switzerland_validation_candidates.csv"
    proposed = set()
    with csv_path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("proposed_validation") == "yes":
                proposed.add(row["short_id"])
    assert proposed == locked
    assert len(proposed) == 15
