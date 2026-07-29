"""Paper-specified weak-signal quality gate."""

from __future__ import annotations

import numpy as np


def mean_first_n_samples(trace: np.ndarray, n: int = 20) -> float:
    """Return the mean of the first ``n`` samples.

    The paper supplies ``n=20``; keeping it an argument makes the project
    contract explicit rather than embedding it invisibly.
    """
    values = _trace_with_at_least_n_samples(trace, n)
    return float(values[:n].mean())


def passes_mean_amplitude_gate(trace: np.ndarray, threshold_gal: float = 0.01, n: int = 20) -> bool:
    """Return whether first-``n`` mean acceleration is strictly above threshold."""
    if not isinstance(threshold_gal, (int, float)) or isinstance(threshold_gal, bool):
        raise TypeError("threshold_gal must be numeric.")
    mean_acceleration = mean_first_n_samples(trace, n)
    # Project assumption: numerical ties within machine precision are treated
    # as equal, preserving the paper's strict "exceeding 0.01 gal" wording.
    tolerance = np.finfo(float).eps * max(1.0, abs(threshold_gal))
    return mean_acceleration > threshold_gal and not np.isclose(
        mean_acceleration, threshold_gal, rtol=0.0, atol=tolerance
    )


def _trace_with_at_least_n_samples(trace: np.ndarray, n: int) -> np.ndarray:
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer.")
    values = np.asarray(trace, dtype=float)
    if values.ndim != 1 or values.size < n:
        raise ValueError("trace must be one-dimensional and contain at least n samples.")
    if not np.isfinite(values).all():
        raise ValueError("trace must contain only finite values.")
    return values
