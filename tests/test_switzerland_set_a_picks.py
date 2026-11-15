"""Independent validation test for Swiss Set A SED manual analyst picks."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
from obspy import UTCDateTime

REPO_ROOT = Path(__file__).resolve().parents[1]
SET_A_MANIFEST = REPO_ROOT / "data" / "manifests" / "sed_switzerland_pilot_events.csv"
SET_A_PICKS = REPO_ROOT / "data" / "manifests" / "sed_switzerland_set_a_picks.csv"
METADATA_DIR = REPO_ROOT / "data" / "metadata" / "switzerland"

EXPECTED_FIELDS = (
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


def test_set_a_picks_manifest_exists_and_schema():
    assert SET_A_PICKS.exists(), "sed_switzerland_set_a_picks.csv must exist"
    with SET_A_PICKS.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert tuple(reader.fieldnames) == EXPECTED_FIELDS
        rows = list(reader)

    assert len(rows) == 120, "Must contain exactly 120 pick rows"


def test_set_a_picks_match_waveform_records():
    with SET_A_MANIFEST.open("r", encoding="utf-8") as f:
        wf_rows = list(csv.DictReader(f))
    with SET_A_PICKS.open("r", encoding="utf-8") as f:
        pick_rows = list(csv.DictReader(f))

    assert len(wf_rows) == 120
    assert len(pick_rows) == 120

    # Index by (short_id, station)
    pick_map = {(r["short_id"], r["station"].upper()): r for r in pick_rows}
    assert len(pick_map) == 120, "All 120 (short_id, station) keys must be unique"

    for wf in wf_rows:
        short_id = wf["event_id"].split("/")[-1]
        station = wf["station"].upper()
        key = (short_id, station)

        assert key in pick_map, f"Missing pick for event {short_id} station {station}"
        pick = pick_map[key]

        # Verify evaluation mode and network
        assert pick["network"] == "CH"
        assert pick["pick_evaluation_mode"] == "manual"
        assert pick["pick_phase"] in {"Pg", "Pn", "P", "P1", "Pb", "Pdiff"}
        assert pick["same_station_pick_status"] == "manual_ch_first_p"

        # Timestamp consistency
        origin = UTCDateTime(wf["origin_time_utc"])
        pick_time = UTCDateTime(pick["pick_time_utc"])
        wf_start = UTCDateTime(wf["waveform_start_utc"])
        wf_end = UTCDateTime(wf["waveform_end_utc"])

        # Pick must be after origin and within plausible EEW range
        latency = pick_time - origin
        assert 0.0 <= latency <= 60.0, f"Latency {latency}s outside valid physical bounds for {key}"

        # Pick must be inside the waveform window
        assert wf_start <= pick_time <= wf_end, f"Pick {pick_time} outside waveform window [{wf_start}, {wf_end}]"


def test_raw_quakeml_provenance_exists():
    with SET_A_PICKS.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    unique_events = sorted({r["short_id"] for r in rows})
    assert len(unique_events) == 20

    for sid in unique_events:
        quakeml_path = METADATA_DIR / sid / "quakeml.xml"
        assert quakeml_path.exists(), f"Raw QuakeML must exist for {sid}"
        assert quakeml_path.stat().st_size > 10000, f"Raw QuakeML for {sid} is too small"
