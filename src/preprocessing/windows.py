"""P-wave window extraction for the five EarthESND input durations."""

from __future__ import annotations

import numpy as np


VALID_DURATIONS_SECONDS = frozenset({2, 3, 4, 5, 6})


def extract_p_window(
    trace: np.ndarray,
    p_pick_index: int,
    duration_seconds: int,
    sampling_rate_hz: float,
) -> np.ndarray:
    """Extract a complete P-wave window without padding.

    Rejecting incomplete windows is a project assumption: the paper does not
    state padding behavior, so no synthetic samples are introduced.
    """
    values = np.asarray(trace, dtype=float)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError("trace must be a one-dimensional finite array.")
    if isinstance(p_pick_index, bool) or not isinstance(p_pick_index, int) or p_pick_index < 0:
        raise ValueError("p_pick_index must be a non-negative integer.")
    if duration_seconds not in VALID_DURATIONS_SECONDS:
        raise ValueError("duration_seconds must be one of 2, 3, 4, 5, or 6.")
    if not isinstance(sampling_rate_hz, (int, float)) or isinstance(sampling_rate_hz, bool) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be positive.")

    sample_count = int(duration_seconds * sampling_rate_hz)
    if sample_count != duration_seconds * sampling_rate_hz:
        raise ValueError("duration_seconds * sampling_rate_hz must be an integer sample count.")
    end_index = p_pick_index + sample_count
    if end_index > values.size:
        raise ValueError("trace does not contain a complete requested P-wave window.")
    return values[p_pick_index:end_index].copy()
