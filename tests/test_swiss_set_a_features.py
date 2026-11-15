"""Automated verification tests for Swiss Set A feature extraction."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from obspy import UTCDateTime

REPO_ROOT = Path(__file__).resolve().parents[1]
FEATURE_MATRIX_CSV = REPO_ROOT / "reports" / "features" / "swiss_set_a_feature_matrix.csv"
PER_RECORD_CSV = REPO_ROOT / "reports" / "features" / "swiss_set_a_per_record_features.csv"
SUMMARY_JSON = REPO_ROOT / "reports" / "features" / "swiss_set_a_feature_summary.json"
SET_A_PICKS = REPO_ROOT / "data" / "manifests" / "sed_switzerland_set_a_picks.csv"

EXPECTED_FEATURE_COLUMNS = [
    "z_peak_velocity_m_s",
    "z_p2p_amplitude_m_s",
    "z_rms_velocity_m_s",
    "z_variance",
    "z_std",
    "z_zero_crossing_rate_hz",
    "z_signal_energy_m2_s",
    "z_crest_factor",
    "z_kurtosis",
    "z_skewness",
    "z_cav_m_s",
    "z_dominant_frequency_hz",
    "z_spectral_centroid_hz",
    "z_spectral_bandwidth_hz",
    "z_spectral_rolloff_95_hz",
    "z_spectral_entropy",
    "h_peak_velocity_m_s",
    "h_rms_velocity_m_s",
    "vec3c_peak_velocity_m_s",
    "vec3c_rms_velocity_m_s",
    "vh_ratio",
    "sta_lta_max",
    "sta_lta_mean",
    "snr_db",
]


def test_feature_matrix_exists_and_row_counts():
    assert FEATURE_MATRIX_CSV.exists()
    assert PER_RECORD_CSV.exists()
    assert SUMMARY_JSON.exists()

    df = pd.read_csv(FEATURE_MATRIX_CSV)
    df_rec = pd.read_csv(PER_RECORD_CSV)

    assert len(df) == 240, "Feature matrix must have exactly 240 window samples"
    assert len(df_rec) == 120, "Per-record table must have exactly 120 records"


def test_balanced_binary_target():
    df = pd.read_csv(FEATURE_MATRIX_CSV)
    assert "is_earthquake" in df.columns

    n_pos = (df["is_earthquake"] == 1).sum()
    n_neg = (df["is_earthquake"] == 0).sum()

    assert n_pos == 120, "Must have exactly 120 positive P-arrival windows"
    assert n_neg == 120, "Must have exactly 120 negative noise windows"


def test_event_grouping_and_stations():
    df = pd.read_csv(FEATURE_MATRIX_CSV)
    assert df["short_id"].nunique() == 20, "Must contain exactly 20 unique earthquake events"
    assert df["station"].nunique() == 54, "Must contain 54 unique CH stations"

    # Exactly 12 rows (6 pairs) per event
    counts_per_event = df["short_id"].value_counts()
    for sid, count in counts_per_event.items():
        assert count == 12, f"Event {sid} must have exactly 12 window samples"


def test_feature_columns_and_finite_values():
    df = pd.read_csv(FEATURE_MATRIX_CSV)

    for col in EXPECTED_FEATURE_COLUMNS:
        assert col in df.columns, f"Missing feature column: {col}"
        vals = df[col].to_numpy()
        assert np.all(np.isfinite(vals)), f"Feature {col} contains NaNs or Infs"


def test_physical_units_and_velocity_ranges():
    df = pd.read_csv(FEATURE_MATRIX_CSV)

    # Velocities must be non-negative
    for col in ["z_peak_velocity_m_s", "h_peak_velocity_m_s", "vec3c_peak_velocity_m_s"]:
        assert np.all(df[col] >= 0.0), f"{col} has negative values"
        # For M2.9 - M4.7 local earthquakes in Switzerland, peak velocity should be < 0.1 m/s (100 mm/s)
        assert np.all(df[col] < 0.1), f"{col} has implausibly large velocity for local Swiss events"

    # Noise velocity should be distinctly lower than P-wave velocity on average
    mean_noise_vel = df[df["is_earthquake"] == 0]["vec3c_peak_velocity_m_s"].mean()
    mean_p_vel = df[df["is_earthquake"] == 1]["vec3c_peak_velocity_m_s"].mean()
    assert mean_p_vel > 10.0 * mean_noise_vel, "P-wave velocity must exceed noise by at least 10x"


def test_causal_window_timestamps():
    df = pd.read_csv(FEATURE_MATRIX_CSV)

    for _, row in df.iterrows():
        t_start = UTCDateTime(row["window_start_utc"])
        t_end = UTCDateTime(row["window_end_utc"])
        origin = UTCDateTime(row["origin_time_utc"])
        p_pick = UTCDateTime(row["p_pick_time_utc"])

        # Exactly 4 seconds
        assert abs((t_end - t_start) - 4.0) < 1e-4

        if row["is_earthquake"] == 0:
            # Noise window must end before origin time
            assert t_end <= origin, "Noise window must end at/before origin time"
        else:
            # P-wave window starts at P-pick
            assert abs(t_start - p_pick) < 1e-4, "Positive window must start at P-wave arrival"
            assert t_start >= origin, "P-wave arrival must occur after earthquake origin"


def test_label_matching_with_verified_sed_picks():
    df = pd.read_csv(FEATURE_MATRIX_CSV)
    df_picks = pd.read_csv(SET_A_PICKS)

    pick_lookup = {(r["short_id"], r["station"].upper()): r for _, r in df_picks.iterrows()}

    for _, row in df.iterrows():
        key = (row["short_id"], row["station"].upper())
        assert key in pick_lookup
        pick = pick_lookup[key]

        assert row["p_phase"] == pick["pick_phase"]
        assert row["p_evaluation_mode"] == "manual"
        assert abs(UTCDateTime(row["p_pick_time_utc"]) - UTCDateTime(pick["pick_time_utc"])) < 1e-4
