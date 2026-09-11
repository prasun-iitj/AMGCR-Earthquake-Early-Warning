"""Tests for the Swiss SED methods-transfer acquisition helpers only."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import yaml
from obspy import Stream, Trace, UTCDateTime

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.acquisition.switzerland_pilot import (
    MANIFEST_FIELDS,
    StationCandidate,
    acquisition_window,
    empty_manifest_row,
    event_short_id,
    group_availability_by_station,
    has_three_component,
    load_switzerland_config,
    parse_availability_text,
    select_stations,
    validate_switzerland_config,
    validate_stream,
)

CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "sed_switzerland_pilot.yaml"


def test_config_loading_and_california_path_guard():
    config = load_switzerland_config(CONFIG_PATH)
    assert config["endpoints"]["event"].startswith("https://eida.ethz.ch/fdsnws/event/1")
    assert config["endpoints"]["dataselect"].startswith("https://eida.ethz.ch/fdsnws/dataselect/1")
    assert len(config["event_ids"]) == 20
    assert config["window"]["pre_event_seconds"] == 90.0
    assert config["window"]["post_event_seconds"] == 210.0
    assert "iris" not in config["output"]["raw_dir"]
    assert config["output"]["raw_dir"] == "data/raw/switzerland"


def test_config_rejects_california_output_path(tmp_path: Path):
    payload = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    payload["output"]["raw_dir"] = "data/raw/iris"
    with pytest.raises(AcquisitionConfigurationError, match="California/IRIS"):
        validate_switzerland_config(payload)


def test_manifest_schema_keys():
    row = empty_manifest_row(
        {
            "event_id": "smi:ch.ethz.sed/sc3a/2020btnrcj",
            "origin_time_utc": "2020-01-25T19:13:28",
            "latitude": 46.2,
            "longitude": 7.7,
            "depth_km": 3.7,
            "magnitude": 3.0,
            "magnitude_type": "MLh",
            "region": "Graechen VS",
        },
        station="DIX",
        download_status="OK",
    )
    assert list(row.keys()) == list(MANIFEST_FIELDS)
    assert row["event_id"].endswith("2020btnrcj")
    assert row["station"] == "DIX"
    assert row["validation_status"] == "NOT_RUN"


def test_event_short_id_handling():
    assert event_short_id("smi:ch.ethz.sed/sc3a/2020btnrcj") == "2020btnrcj"
    assert event_short_id("smi:ch.ethz.sed/sc20a/Event/2021mvcsag") == "2021mvcsag"
    assert event_short_id("2022rvutkg") == "2022rvutkg"
    assert event_short_id("  2024kyoses/ ") == "2024kyoses"


def test_window_is_not_origin_aligned():
    origin = UTCDateTime("2020-01-25T19:13:28.756778")
    start, end = acquisition_window(origin, 90.0, 210.0)
    assert abs(float(origin - start) - 90.0) < 1e-6
    assert abs(float(end - origin) - 210.0) < 1e-6
    assert float(end - start) == pytest.approx(300.0)
    with pytest.raises(ValueError):
        acquisition_window(origin, 0.0, 210.0)


def test_availability_parser_skips_inverted_spans():
    text = """
#Network Station Location Channel Quality SampleRate Earliest Latest
CH       DIX     --       HHZ     D       200.0      2020-01-25T19:11:58.000000Z 2020-01-25T19:16:58.000000Z
CH       DIX     --       HHN     D       200.0      2020-01-25T19:11:58.000000Z 2020-01-25T19:16:58.000000Z
CH       DIX     --       HHE     D       200.0      2020-01-25T19:11:58.000000Z 2020-01-25T19:16:58.000000Z
CH       BAD     --       HHZ     D       200.0      2020-01-25T19:16:00.000000Z 2020-01-25T19:11:00.000000Z
"""
    rows = parse_availability_text(text)
    assert len(rows) == 3
    assert {row["channel"] for row in rows} == {"HHZ", "HHN", "HHE"}
    assert rows[0]["location"] == ""


def test_station_selection_prefers_3c_and_distance_bins():
    origin = UTCDateTime("2020-01-25T19:13:28")
    text = """
CH DIX -- HHZ D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH DIX -- HHN D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH DIX -- HHE D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH EMBD -- HHZ D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH EMBD -- HHN D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH EMBD -- HHE D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH ZUR -- HHZ D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH ZUR -- HHN D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH ZUR -- HHE D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH BALST -- HHZ D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH BALST -- HHN D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH BALST -- HHE D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
CH ONLYZ -- HHZ D 200.0 2020-01-25T19:11:58Z 2020-01-25T19:16:58Z
"""
    rows = parse_availability_text(text)
    candidates = group_availability_by_station(rows, origin, 90.0, 210.0)
    coords = {
        "DIX": {"latitude": 46.08, "longitude": 7.41, "site": "Dix"},
        "EMBD": {"latitude": 46.18, "longitude": 7.80, "site": "Embd"},
        "ZUR": {"latitude": 47.37, "longitude": 8.58, "site": "Zurich"},
        "BALST": {"latitude": 47.33, "longitude": 7.69, "site": "Balsthal"},
        "ONLYZ": {"latitude": 46.20, "longitude": 7.50, "site": "Incomplete"},
    }
    from src.acquisition.switzerland_pilot import attach_coordinates

    attach_coordinates(candidates, coords, 46.235, 7.715)
    selected = select_stations(
        candidates,
        max_stations=4,
        bin_edges_km=[0, 50, 100, 150, 250, 400],
        max_per_bin=2,
        prefer_three_component=True,
        allow_incomplete=False,
    )
    names = [item.station for item in selected]
    assert "ONLYZ" not in names
    assert "DIX" in names or "EMBD" in names
    assert "ZUR" in names or "BALST" in names
    assert len(selected) <= 4
    assert all(item.has_hh_3c or item.has_bh_3c for item in selected)


def test_select_stations_does_not_force_quota():
    candidate = StationCandidate(
        network="CH",
        station="DIX",
        location="",
        channels={"HHZ", "HHN", "HHE"},
        sample_rates_hz={200.0},
        earliest=UTCDateTime("2020-01-25T19:11:58"),
        latest=UTCDateTime("2020-01-25T19:16:58"),
        latitude=46.08,
        longitude=7.41,
        distance_km=20.0,
    )
    selected = select_stations(
        [candidate],
        max_stations=6,
        bin_edges_km=[0, 50, 100, 150, 250, 400],
        max_per_bin=2,
    )
    assert [item.station for item in selected] == ["DIX"]


def test_has_three_component():
    assert has_three_component({"HHZ", "HHN", "HHE"}, "HH")
    assert not has_three_component({"HHZ", "HHN"}, "HH")
    assert has_three_component({"BHZ", "BHN", "BHE", "HHZ"}, "BH")


def _trace(channel: str, origin: UTCDateTime, pre: float, post: float, rate: float = 100.0) -> Trace:
    npts = int((pre + post) * rate)
    trace = Trace(data=np.ones(npts, dtype=np.float32))
    trace.stats.network = "CH"
    trace.stats.station = "DIX"
    trace.stats.channel = channel
    trace.stats.sampling_rate = rate
    trace.stats.starttime = origin - pre
    return trace


def test_validation_pass_for_3c_with_pre_event():
    origin = UTCDateTime("2020-01-25T19:13:28")
    stream = Stream([_trace(ch, origin, 90.0, 210.0) for ch in ("HHZ", "HHN", "HHE")])
    result = validate_stream(stream, origin, 60.0, 60.0)
    assert result.readable is True
    assert result.origin_inside is True
    assert result.complete_3c is True
    assert result.pre_event_seconds == pytest.approx(90.0, abs=0.02)
    assert result.post_event_seconds == pytest.approx(210.0, abs=0.02)
    assert result.status == "PASS"


def test_validation_fail_when_origin_not_inside():
    origin = UTCDateTime("2020-01-25T19:13:28")
    trace = Trace(data=np.ones(5000, dtype=np.float32))
    trace.stats.channel = "HHZ"
    trace.stats.sampling_rate = 100.0
    trace.stats.starttime = origin + 10.0
    result = validate_stream(Stream([trace]), origin, 60.0, 60.0)
    assert result.origin_inside is False
    assert result.status == "FAIL"


def test_validation_partial_when_pre_event_short():
    origin = UTCDateTime("2020-01-25T19:13:28")
    stream = Stream([_trace(ch, origin, 20.0, 210.0) for ch in ("HHZ", "HHN", "HHE")])
    result = validate_stream(stream, origin, 60.0, 60.0)
    assert result.origin_inside is True
    assert result.status == "PARTIAL"
    assert any("pre-event" in note for note in result.notes)
