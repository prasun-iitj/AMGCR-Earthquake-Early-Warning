"""Comprehensive Phase 2 tests traced to the implementation specification."""

from __future__ import annotations

import numpy as np
import pytest

from src.preprocessing.baseline import subtract_first_n_mean
from src.preprocessing.filtering import bandpass_butterworth
from src.preprocessing.integration import integrate_acceleration, integrate_velocity
from src.preprocessing.picking import pick_p_wave_sta_lta
from src.preprocessing.pipeline import PreprocessingConfig, PreprocessingPipeline, RejectedTraceError
from src.preprocessing.quality import mean_first_n_samples, passes_mean_amplitude_gate
from src.preprocessing.windows import extract_p_window


def test_sta_lta_picks_first_threshold_crossing() -> None:
    trace = np.concatenate([np.full(40, 0.001), np.full(30, 1.0), np.full(30, 0.001)])

    pick = pick_p_wave_sta_lta(trace, threshold=2.5, short_window=5, long_window=20)

    assert pick is not None
    assert 40 <= pick < 45


def test_sta_lta_requires_explicit_window_lengths() -> None:
    with pytest.raises(ValueError, match="must be configured"):
        pick_p_wave_sta_lta(np.ones(100), threshold=2.5, short_window=None, long_window=None)


def test_quality_gate_uses_strict_first_twenty_mean_threshold() -> None:
    at_threshold = np.full(20, 0.01)
    above_threshold = np.full(20, 0.0101)

    assert mean_first_n_samples(at_threshold, n=20) == pytest.approx(0.01)
    assert not passes_mean_amplitude_gate(at_threshold, threshold_gal=0.01, n=20)
    assert passes_mean_amplitude_gate(above_threshold, threshold_gal=0.01, n=20)


def test_baseline_correction_subtracts_first_twenty_mean() -> None:
    trace = np.concatenate([np.full(20, 3.0), np.array([5.0, 7.0])])

    corrected = subtract_first_n_mean(trace, n=20)

    assert corrected[:20].mean() == pytest.approx(0.0)
    assert corrected[-2:].tolist() == [2.0, 4.0]


def test_butterworth_filter_requires_explicit_phase_and_transient_policy() -> None:
    trace = np.sin(np.linspace(0, 10, 500))

    with pytest.raises(ValueError, match="phase_mode"):
        bandpass_butterworth(trace, 100.0, 0.5, 40.0, 4, None, "scipy_default")
    with pytest.raises(ValueError, match="transient_handling"):
        bandpass_butterworth(trace, 100.0, 0.5, 40.0, 4, "causal_sosfilt", None)


def test_butterworth_filter_returns_same_shape_with_explicit_policy() -> None:
    sample_rate = 100.0
    time = np.arange(1000) / sample_rate
    trace = np.sin(2 * np.pi * 5 * time) + np.sin(2 * np.pi * 48 * time)

    filtered = bandpass_butterworth(trace, sample_rate, 1.0, 20.0, 4, "zero_phase_sosfiltfilt", "scipy_default")

    assert filtered.shape == trace.shape
    assert np.isfinite(filtered).all()
    assert np.std(filtered) < np.std(trace)


def test_trapezoidal_integrations_require_explicit_method_and_initial_condition() -> None:
    values = np.array([0.0, 1.0, 2.0])

    with pytest.raises(ValueError, match="method"):
        integrate_acceleration(values, 1.0, None, 0.0)
    with pytest.raises(ValueError, match="initial_condition"):
        integrate_acceleration(values, 1.0, "trapezoidal", None)

    velocity = integrate_acceleration(values, 1.0, "trapezoidal", 0.0)
    displacement = integrate_velocity(velocity, 1.0, "trapezoidal", 0.0)

    assert velocity == pytest.approx([0.0, 0.5, 2.0])
    assert displacement == pytest.approx([0.0, 0.25, 1.5])


def test_p_wave_windows_cover_two_to_six_seconds_without_padding() -> None:
    trace = np.arange(700, dtype=float)

    assert extract_p_window(trace, 10, 2, 100.0).shape == (200,)
    assert extract_p_window(trace, 10, 6, 100.0).shape == (600,)
    with pytest.raises(ValueError, match="complete"):
        extract_p_window(trace, 200, 6, 100.0)
    with pytest.raises(ValueError, match="2, 3, 4, 5, or 6"):
        extract_p_window(trace, 0, 1, 100.0)


def make_pipeline() -> PreprocessingPipeline:
    return PreprocessingPipeline(
        PreprocessingConfig(
            sampling_rate_hz=100.0,
            sta_lta_threshold=2.5,
            sta_lta_short_window=5,
            sta_lta_long_window=20,
            pick_component="UD",  # Project assumption; paper does not name the pick component.
            station_scaling_factors={"NS": 1.0, "EW": 1.0, "UD": 1.0},
            quality_samples=20,
            quality_threshold_gal=0.01,
            baseline_samples=20,
            low_hz=0.0075,
            high_hz=45.0,
            filter_poles=4,
            phase_mode="causal_sosfilt",  # Explicit project assumption.
            transient_handling="scipy_default",  # Explicit project assumption.
            integration_method="trapezoidal",  # Explicit project assumption.
            integration_initial_condition=0.0,  # Explicit project assumption.
        )
    )


def test_pipeline_constructs_all_five_t_by_nine_tensors() -> None:
    baseline = np.full(100, 0.001)
    event = np.full(800, 1.0)
    trace = np.concatenate([baseline, event])
    pipeline = make_pipeline()

    processed = pipeline.process({"NS": trace, "EW": trace * 1.1, "UD": trace * 0.9})

    assert processed.p_pick_index >= 100
    assert {duration: tensor.shape for duration, tensor in processed.tensors.items()} == {
        2: (200, 9),
        3: (300, 9),
        4: (400, 9),
        5: (500, 9),
        6: (600, 9),
    }
    assert all(np.isfinite(tensor).all() for tensor in processed.tensors.values())


def test_pipeline_rejects_missing_unresolved_project_assumptions() -> None:
    config = PreprocessingConfig(
        sampling_rate_hz=100.0,
        sta_lta_threshold=2.5,
        sta_lta_short_window=5,
        sta_lta_long_window=20,
        pick_component=None,
        station_scaling_factors=None,
        quality_samples=20,
        quality_threshold_gal=0.01,
        baseline_samples=20,
        low_hz=0.5,
        high_hz=40.0,
        filter_poles=4,
        phase_mode=None,
        transient_handling=None,
        integration_method=None,
        integration_initial_condition=None,
    )

    with pytest.raises(ValueError, match="pick_component"):
        PreprocessingPipeline(config)


def test_pipeline_rejects_weak_signal_after_pick() -> None:
    pipeline = make_pipeline()
    trace = np.full(1000, 0.001)

    with pytest.raises(RejectedTraceError, match="STA/LTA"):
        pipeline.process({"NS": trace, "EW": trace, "UD": trace})
