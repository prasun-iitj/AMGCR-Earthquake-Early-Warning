"""Tests for Swiss STA/LTA transfer-investigation helpers only."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from obspy import UTCDateTime

from src.analysis.switzerland_sta_lta_transfer import (
    apply_proposal_rule,
    cft_window_stats,
    count_in_window,
    first_in_window,
    load_transfer_config,
    onset_times_from_samples,
    trigger_window_counts,
    unmasked_onset_is_in_mute_region,
    window_pair,
)

CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "swiss_sta_lta_transfer.yaml"


def test_transfer_config_loads_and_avoids_california_paths():
    config = load_transfer_config(CONFIG_PATH)
    assert config["baseline"]["threshold"] == 2.5
    assert config["baseline"]["sta_window_s"] == 0.5
    assert 2.5 in config["thresholds"]
    assert 10.0 in config["thresholds"]
    assert "switzerland" in config["output"]["reports_dir"] or "swiss" in config["output"]["reports_dir"]
    assert "iris" not in config["output"]["reports_dir"]


def test_window_counts_split_pre_and_post_origin():
    origin = UTCDateTime("2020-01-25T19:13:28")
    windows = {
        "noise_start_offset_s": -60.0,
        "noise_end_offset_s": -10.0,
        "pre_origin_start_offset_s": -5.0,
        "pre_origin_end_offset_s": 0.0,
        "post_origin_start_offset_s": 0.0,
        "post_origin_end_offset_s": 90.0,
    }
    times = [origin - 40.0, origin - 2.0, origin + 6.0, origin + 12.0]
    counts = trigger_window_counts(times, origin, windows)
    assert counts["n_onsets_noise"] == 1
    assert counts["n_onsets_pre_origin"] == 1
    assert counts["n_onsets_post_origin"] == 2
    assert counts["has_noise_onset"] is True
    assert counts["search_is_pre_origin"] is True
    assert counts["first_post_origin_latency_s"] == 6.0
    noise = window_pair(origin, -60.0, -10.0)
    assert count_in_window(times, *noise) == 1
    assert first_in_window(times, origin, origin + 90.0) == origin + 6.0


def test_cft_window_stats_and_edge_mute_flag():
    rate = 100.0
    cft = np.ones(1000) * 1.0
    cft[200:300] = 4.0  # 2–3 s after start
    start = UTCDateTime(2020, 1, 1)
    stats = cft_window_stats(cft, start, rate, (start + 2.0, start + 3.0), 2.5)
    assert stats["max_cft"] == 4.0
    assert stats["fraction_above"] == 1.0
    quiet = cft_window_stats(cft, start, rate, (start + 5.0, start + 8.0), 2.5)
    assert quiet["n_above"] == 0
    assert unmasked_onset_is_in_mute_region(100, rate, 15.0) is True  # 1 s < 15 s
    assert unmasked_onset_is_in_mute_region(2000, rate, 15.0) is False
    times = onset_times_from_samples(start, rate, [100, 200])
    assert times[0] == start + 1.0


def test_proposal_rule_picks_lowest_threshold_meeting_cuts_not_the_highest():
    rule = {
        "sta_window_s": 0.5,
        "lta_window_s": 10.0,
        "processing": "causal_bandpass",
        "channel": "HHZ",
        "max_noise_record_fraction": 0.25,
        "min_post_origin_coverage": 0.75,
        "fallback_min_post_origin_coverage": 0.70,
    }
    rows = [
        {"threshold": 2.5, "sta_window_s": 0.5, "lta_window_s": 10.0, "processing": "causal_bandpass", "channel": "HHZ", "noise_record_fraction": 0.99, "post_origin_coverage": 1.0, "median_post_origin_latency_s": 2.0},
        {"threshold": 6.0, "sta_window_s": 0.5, "lta_window_s": 10.0, "processing": "causal_bandpass", "channel": "HHZ", "noise_record_fraction": 0.20, "post_origin_coverage": 0.80, "median_post_origin_latency_s": 4.0},
        {"threshold": 8.0, "sta_window_s": 0.5, "lta_window_s": 10.0, "processing": "causal_bandpass", "channel": "HHZ", "noise_record_fraction": 0.05, "post_origin_coverage": 0.78, "median_post_origin_latency_s": 5.0},
    ]
    chosen = apply_proposal_rule(rows, rule)
    assert chosen["proposed"] is True
    assert chosen["threshold"] == 6.0
    assert chosen["mode"] == "primary"
    assert "not validated" in chosen["label"]
    assert chosen["threshold"] != 8.0
