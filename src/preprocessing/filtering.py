"""Butterworth band-pass filtering with explicit project-assumption controls."""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt, sosfiltfilt


VALID_PHASE_MODES = frozenset({"causal_sosfilt", "zero_phase_sosfiltfilt"})
VALID_TRANSIENT_HANDLING = frozenset({"scipy_default"})


def bandpass_butterworth(
    trace: np.ndarray,
    sampling_rate_hz: float,
    low_hz: float,
    high_hz: float,
    poles: int,
    phase_mode: str | None,
    transient_handling: str | None,
) -> np.ndarray:
    """Apply a Butterworth band-pass filter.

    The paper specifies four poles and 0.0075–45 Hz, but not phase or
    transient behavior. The accepted values are project assumptions, and both
    are required parameters so they cannot be silently selected.
    """
    values = _validate_trace(trace)
    _validate_filter_parameters(sampling_rate_hz, low_hz, high_hz, poles)
    if phase_mode not in VALID_PHASE_MODES:
        raise ValueError(f"phase_mode must be one of {sorted(VALID_PHASE_MODES)}; it is not specified in the paper.")
    if transient_handling not in VALID_TRANSIENT_HANDLING:
        raise ValueError(
            "transient_handling must explicitly select 'scipy_default'; the paper does not specify handling."
        )

    sos = butter(poles, [low_hz, high_hz], btype="bandpass", fs=sampling_rate_hz, output="sos")
    if phase_mode == "causal_sosfilt":
        return sosfilt(sos, values)
    return sosfiltfilt(sos, values)


def _validate_trace(trace: np.ndarray) -> np.ndarray:
    values = np.asarray(trace, dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("trace must be a non-empty one-dimensional array.")
    if not np.isfinite(values).all():
        raise ValueError("trace must contain only finite values.")
    return values


def _validate_filter_parameters(sampling_rate_hz: float, low_hz: float, high_hz: float, poles: int) -> None:
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in (sampling_rate_hz, low_hz, high_hz)):
        raise TypeError("sampling rate and cutoff frequencies must be numeric.")
    if isinstance(poles, bool) or not isinstance(poles, int):
        raise TypeError("poles must be an integer.")
    if sampling_rate_hz <= 0 or low_hz <= 0 or high_hz <= low_hz:
        raise ValueError("Filter frequencies must satisfy 0 < low_hz < high_hz.")
    if high_hz >= sampling_rate_hz / 2:
        raise ValueError("high_hz must be below the Nyquist frequency.")
    if poles <= 0:
        raise ValueError("poles must be positive.")
