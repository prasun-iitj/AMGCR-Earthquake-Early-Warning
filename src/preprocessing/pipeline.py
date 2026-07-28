"""Config-driven EarthESND preprocessing pipeline.

The project chooses a component for STA/LTA and represents station scaling as
per-component multiplication factors. Both choices are project assumptions,
because the paper does not provide the picking component or scaling formula.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping

import numpy as np

from src.preprocessing.baseline import subtract_first_n_mean
from src.preprocessing.filtering import bandpass_butterworth
from src.preprocessing.integration import integrate_acceleration, integrate_velocity
from src.preprocessing.picking import pick_p_wave_sta_lta
from src.preprocessing.quality import passes_mean_amplitude_gate
from src.preprocessing.windows import VALID_DURATIONS_SECONDS, extract_p_window


COMPONENT_ORDER = ("NS", "EW", "UD")


class RejectedTraceError(ValueError):
    """Project-assumption exception for records rejected by the paper's gate."""


@dataclass(frozen=True, slots=True)
class PreprocessingConfig:
    """All preprocessing controls, including paper-absent required choices."""

    sampling_rate_hz: float
    sta_lta_threshold: float
    sta_lta_short_window: int | None
    sta_lta_long_window: int | None
    pick_component: str | None
    station_scaling_factors: Mapping[str, float] | None
    quality_samples: int
    quality_threshold_gal: float
    baseline_samples: int
    low_hz: float
    high_hz: float
    filter_poles: int
    phase_mode: str | None
    transient_handling: str | None
    integration_method: str | None
    integration_initial_condition: float | None


@dataclass(frozen=True, slots=True)
class ProcessedWaveforms:
    """Paper-derived five tensor durations plus the selected P-wave pick."""

    p_pick_index: int
    tensors: Mapping[int, np.ndarray]


class PreprocessingPipeline:
    """Apply the paper-specified preprocessing sequence to three components."""

    def __init__(self, config: PreprocessingConfig) -> None:
        self.config = config
        self._validate_config()

    def process(self, components: Mapping[str, np.ndarray]) -> ProcessedWaveforms:
        """Pick, gate, correct, filter, integrate, window, and stack components."""
        if set(components) != set(COMPONENT_ORDER):
            raise ValueError("components must contain exactly NS, EW, and UD traces.")
        raw = {name: np.asarray(components[name], dtype=float) for name in COMPONENT_ORDER}
        if any(values.ndim != 1 or values.size == 0 or not np.isfinite(values).all() for values in raw.values()):
            raise ValueError("All component traces must be non-empty one-dimensional finite arrays.")

        p_pick_index = pick_p_wave_sta_lta(
            raw[self.config.pick_component],
            self.config.sta_lta_threshold,
            self.config.sta_lta_short_window,
            self.config.sta_lta_long_window,
        )
        if p_pick_index is None:
            raise RejectedTraceError("STA/LTA did not detect a P-wave onset.")

        scaled = {name: raw[name] * self.config.station_scaling_factors[name] for name in COMPONENT_ORDER}
        candidate = scaled[self.config.pick_component][p_pick_index:]
        if not passes_mean_amplitude_gate(candidate, self.config.quality_threshold_gal, self.config.quality_samples):
            raise RejectedTraceError("Trace failed the first-20-sample mean acceleration gate.")

        acceleration: dict[str, np.ndarray] = {}
        velocity: dict[str, np.ndarray] = {}
        displacement: dict[str, np.ndarray] = {}
        for name in COMPONENT_ORDER:
            post_pick = scaled[name][p_pick_index:]
            corrected = subtract_first_n_mean(post_pick, self.config.baseline_samples)
            acceleration[name] = bandpass_butterworth(
                corrected,
                self.config.sampling_rate_hz,
                self.config.low_hz,
                self.config.high_hz,
                self.config.filter_poles,
                self.config.phase_mode,
                self.config.transient_handling,
            )
            velocity[name] = integrate_acceleration(
                acceleration[name],
                self.config.sampling_rate_hz,
                self.config.integration_method,
                self.config.integration_initial_condition,
            )
            displacement[name] = integrate_velocity(
                velocity[name],
                self.config.sampling_rate_hz,
                self.config.integration_method,
                self.config.integration_initial_condition,
            )

        tensors: dict[int, np.ndarray] = {}
        for duration_seconds in sorted(VALID_DURATIONS_SECONDS):
            channels = [
                *(extract_p_window(acceleration[name], 0, duration_seconds, self.config.sampling_rate_hz) for name in COMPONENT_ORDER),
                *(extract_p_window(velocity[name], 0, duration_seconds, self.config.sampling_rate_hz) for name in COMPONENT_ORDER),
                *(extract_p_window(displacement[name], 0, duration_seconds, self.config.sampling_rate_hz) for name in COMPONENT_ORDER),
            ]
            tensors[duration_seconds] = np.column_stack(channels)
        return ProcessedWaveforms(p_pick_index=p_pick_index, tensors=tensors)

    def _validate_config(self) -> None:
        if self.config.pick_component not in COMPONENT_ORDER:
            raise ValueError("pick_component is a required project assumption and must be NS, EW, or UD.")
        factors = self.config.station_scaling_factors
        if factors is None or set(factors) != set(COMPONENT_ORDER):
            raise ValueError("station_scaling_factors must explicitly define NS, EW, and UD factors.")
        if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in factors.values()):
            raise TypeError("station_scaling_factors must be numeric.")
