"""Tests for Swiss signal-analysis helpers only (no California test changes)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import yaml
from obspy import Stream, Trace, UTCDateTime
from obspy.core.trace import Stats

from src.acquisition.exceptions import AcquisitionConfigurationError
from src.analysis.switzerland_signal import (
    REQUIRED_HH_3C,
    amplitude_term,
    analysis_windows,
    bandpass_freqmax_used,
    classify_trigger,
    common_overlap,
    cumulative_squared,
    epicentral_distance_km,
    first_sta_lta_trigger,
    has_complete_hh_3c,
    horizontal_amplitude,
    hypocentral_distance_km,
    identify_hh_components,
    load_swiss_analysis_config,
    peak_abs,
    pre_filt_for_sampling,
    rms,
    sampling_rates_consistent,
    select_trigger_from_onsets,
    slice_array_window,
    snr_ratio,
    stationxml_path_for_row,
    units_label,
    validate_swiss_analysis_config,
    vector_amplitude,
    window_covered,
)

CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "swiss_signal_analysis.yaml"


def _trace(channel: str, data: np.ndarray, start: UTCDateTime, rate: float = 100.0, station: str = "TEST") -> Trace:
    stats = Stats()
    stats.network = "CH"
    stats.station = station
    stats.location = ""
    stats.channel = channel
    stats.sampling_rate = rate
    stats.starttime = start
    stats.npts = len(data)
    return Trace(data=np.asarray(data, dtype=np.float64), header=stats)


def test_analysis_config_loading_and_california_path_guard():
    config = load_swiss_analysis_config(CONFIG_PATH)
    assert config["windows"]["noise_start_offset_s"] == -60.0
    assert config["windows"]["noise_end_offset_s"] == -10.0
    assert config["sta_lta"]["sta_window_s"] == 0.5
    assert config["sta_lta"]["lta_window_s"] == 10.0
    assert config["sta_lta"]["threshold"] == 2.5
    assert config["bandpass"]["freqmin_hz"] == 0.1
    assert config["bandpass"]["freqmax_hz"] == 15.0
    assert "swiss" in config["output"]["reports_dir"]
    payload = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    payload["output"]["reports_dir"] = "reports/signal_analysis"
    # California path substring is 'california' or 'iris'; signal_analysis is allowed.
    validate_swiss_analysis_config(payload)
    payload["inputs"]["raw_dir"] = "data/raw/iris"
    with pytest.raises(AcquisitionConfigurationError, match="California/IRIS"):
        validate_swiss_analysis_config(payload)


def test_window_calculation_uses_pre_event_not_origin_aligned():
    origin = UTCDateTime("2020-01-25T19:13:28.756778")
    config = load_swiss_analysis_config(CONFIG_PATH)
    windows = analysis_windows(origin, config["windows"])
    noise_s, noise_e = windows["noise"]
    event_s, event_e = windows["event"]
    assert abs(float(origin - noise_s) - 60.0) < 1e-6
    assert abs(float(origin - noise_e) - 10.0) < 1e-6
    assert abs(float(event_s - origin)) < 1e-9
    assert abs(float(event_e - origin) - 180.0) < 1e-6
    assert noise_e <= origin <= event_s
    assert not window_covered(origin, origin + 300.0, windows["noise"])
    assert window_covered(origin - 90.0, origin + 210.0, windows["noise"])
    assert window_covered(origin - 90.0, origin + 210.0, windows["event"])


def test_3c_detection_and_inconsistent_sampling():
    t0 = UTCDateTime(2020, 1, 1)
    z = _trace("HHZ", np.zeros(100), t0, rate=200.0)
    n = _trace("HHN", np.zeros(100), t0, rate=200.0)
    e = _trace("HHE", np.zeros(100), t0, rate=200.0)
    complete = Stream([z, n, e])
    assert has_complete_hh_3c(complete)
    assert set(identify_hh_components(complete)) == set(REQUIRED_HH_3C)
    assert sampling_rates_consistent(complete)
    missing = Stream([z, n])
    assert not has_complete_hh_3c(missing)
    mixed = Stream([z, n, _trace("HHE", np.zeros(100), t0, rate=120.0)])
    assert has_complete_hh_3c(mixed)
    assert not sampling_rates_consistent(mixed)


def test_common_overlap_and_slice_window():
    t0 = UTCDateTime(2020, 1, 1, 0, 0, 0)
    origin = t0 + 90.0
    rate = 100.0
    data = np.arange(30000, dtype=float)
    st = Stream(
        [
            _trace("HHZ", data, t0, rate=rate),
            _trace("HHN", data, t0 + 1.0, rate=rate),
            _trace("HHE", data[:-500], t0, rate=rate),
        ]
    )
    overlap = common_overlap(st)
    assert overlap is not None
    assert overlap[0] == t0 + 1.0
    window = (origin - 60.0, origin - 10.0)
    z = st[0]
    sliced = slice_array_window(z.data, z.stats.starttime, rate, window)
    assert sliced.size == pytest.approx(50.0 * rate, abs=1)


def test_response_correction_unit_labels_and_failure_path():
    assert units_label("VEL", "applied") == "m/s"
    assert units_label("ACC", "applied") == "m/s^2"
    assert units_label("VEL", "failed") == "counts"
    assert amplitude_term("m/s", "peak") == "band_limited_pgv_m_s"
    assert amplitude_term("m/s^2", "peak") == "band_limited_pga_m_s2"
    assert amplitude_term("counts", "peak") == "peak_response_corrected_amplitude"


def test_snr_calculation_formula():
    noise = np.ones(1000) * 2.0
    signal = np.ones(1000) * 10.0
    noise_rms = rms(noise)
    assert noise_rms == pytest.approx(2.0)
    assert snr_ratio(peak_abs(signal), noise_rms) == pytest.approx(5.0)
    assert snr_ratio(rms(signal), noise_rms) == pytest.approx(5.0)
    assert not np.isfinite(snr_ratio(float("nan"), 1.0))


def test_sta_lta_does_not_invent_pick_and_classifies_windows():
    rate = 100.0
    n = int(100 * rate)
    data = np.random.RandomState(0).normal(0, 0.1, n)
    # No event → no_crossing, sample is None (not LTA-end fallback).
    quiet = first_sta_lta_trigger(data, rate, 0.5, 10.0, 8.0, 0.5)
    assert quiet["method"] in {"no_crossing", "trace_shorter_than_lta"}
    assert quiet["sample"] is None

    data[int(70 * rate) : int(72 * rate)] += 20.0
    picked = first_sta_lta_trigger(data, rate, 0.5, 10.0, 2.5, 0.5)
    assert picked["method"] in {"trigger_onset_first", "first_threshold_crossing"}
    assert picked["sample"] is not None
    data_edge = np.random.RandomState(0).normal(0, 0.1, n)
    data_edge[int(5 * rate) : int(6 * rate)] += 25.0
    data_edge[int(70 * rate) : int(72 * rate)] += 20.0
    skipped_edge = first_sta_lta_trigger(data_edge, rate, 0.5, 10.0, 2.5, 0.5, mute_start_s=15.0, mute_end_s=15.0)
    assert skipped_edge["sample_unmasked"] is not None
    assert skipped_edge["sample"] is not None
    assert skipped_edge["sample"] > int(15 * rate)

    origin = UTCDateTime(2020, 1, 1, 0, 1, 30)
    windows = {
        "noise": (origin - 60.0, origin - 10.0),
        "event": (origin, origin + 180.0),
        "expected_trigger": (origin, origin + 90.0),
    }
    false_t = origin - 40.0
    cls = classify_trigger(false_t, origin, windows)
    assert cls["false_trigger_candidate"] is True
    assert cls["in_noise_window"] is True
    ok = classify_trigger(origin + 5.0, origin, windows)
    assert ok["trigger_class"] == "expected_event_window"
    assert ok["trigger_latency_s"] == pytest.approx(5.0)
    none = classify_trigger(None, origin, windows)
    assert none["trigger_class"] == "no_trigger"
    late = classify_trigger(origin + 120.0, origin, windows)
    assert late["trigger_class"] == "late_or_outside_expected_window"
    selected = select_trigger_from_onsets(
        [origin - 40.0, origin + 6.0],
        origin,
        windows,
        -5.0,
        90.0,
    )
    assert selected["trigger_latency_s"] == pytest.approx(6.0)
    assert selected["false_trigger_candidate"] is True
    assert selected["n_onsets_in_noise_window"] == 1
    assert selected["trigger_class"] == "expected_event_window"


def test_amplitude_and_3c_vector_quantities():
    n = np.array([3.0, 0.0])
    e = np.array([4.0, 0.0])
    z = np.array([0.0, 12.0])
    h = horizontal_amplitude(n, e)
    assert h[0] == pytest.approx(5.0)
    v = vector_amplitude(z, n, e)
    assert v[0] == pytest.approx(5.0)
    assert v[1] == pytest.approx(12.0)
    with pytest.raises(ValueError):
        horizontal_amplitude(n, e[:1])
    dt = 0.01
    energy = cumulative_squared(np.array([1.0, 1.0]), dt)
    assert energy == pytest.approx(0.02)


def test_distance_calculation():
    # Same point
    assert epicentral_distance_km(46.2, 7.7, 46.2, 7.7) == pytest.approx(0.0, abs=1e-6)
    # ~111.2 km per degree latitude
    d = epicentral_distance_km(46.0, 8.0, 47.0, 8.0)
    assert d == pytest.approx(111.2, rel=0.01)
    hypo = hypocentral_distance_km(30.0, 40.0)
    assert hypo == pytest.approx(50.0)


def test_pre_filt_scales_with_nyquist_not_california_40hz():
    config = load_swiss_analysis_config(CONFIG_PATH)
    pf_200 = pre_filt_for_sampling(200.0, config["instrument_response"], config["bandpass"])
    pf_120 = pre_filt_for_sampling(120.0, config["instrument_response"], config["bandpass"])
    # California frozen pre_filt used 20 and 25 Hz; Swiss 200 Hz must be higher.
    assert pf_200[2] > 25.0
    assert pf_200[3] > pf_200[2]
    assert pf_120[3] < 60.0
    assert pf_200[0] < config["bandpass"]["freqmin_hz"]
    fmax_200 = bandpass_freqmax_used(200.0, config["bandpass"])
    fmax_40 = bandpass_freqmax_used(40.0, config["bandpass"])
    assert fmax_200 == 15.0
    assert fmax_40 == pytest.approx(15.0)  # 0.9 * 20 = 18, so 15 still used


def test_stationxml_path_uses_swiss_metadata_dir():
    repo = Path("C:/repo")
    path = stationxml_path_for_row(repo, "data/metadata/switzerland", "smi:ch.ethz.sed/sc3a/2020btnrcj", "EMBD", "--")
    assert path.as_posix().endswith("data/metadata/switzerland/2020btnrcj/CH.EMBD.--.HH.xml")
    assert "iris" not in path.as_posix()
