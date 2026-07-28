"""Explicit numerical integration for acceleration, velocity, and displacement."""

from __future__ import annotations

import numpy as np


VALID_METHODS = frozenset({"trapezoidal"})


def integrate_acceleration(
    acceleration: np.ndarray,
    sampling_rate_hz: float,
    method: str | None,
    initial_condition: float | None,
) -> np.ndarray:
    """Integrate acceleration into velocity with an explicit numerical policy."""
    return _integrate(acceleration, sampling_rate_hz, method, initial_condition)


def integrate_velocity(
    velocity: np.ndarray,
    sampling_rate_hz: float,
    method: str | None,
    initial_condition: float | None,
) -> np.ndarray:
    """Integrate velocity into displacement with an explicit numerical policy."""
    return _integrate(velocity, sampling_rate_hz, method, initial_condition)


def _integrate(
    trace: np.ndarray,
    sampling_rate_hz: float,
    method: str | None,
    initial_condition: float | None,
) -> np.ndarray:
    """Perform cumulative trapezoidal integration.

    The trapezoidal rule and numeric initial condition are project assumptions.
    They are required because the paper gives neither a method nor initial state.
    """
    values = np.asarray(trace, dtype=float)
    if values.ndim != 1 or values.size == 0 or not np.isfinite(values).all():
        raise ValueError("trace must be a non-empty one-dimensional finite array.")
    if method not in VALID_METHODS:
        raise ValueError(f"method must be one of {sorted(VALID_METHODS)}; it is not specified in the paper.")
    if initial_condition is None:
        raise ValueError("initial_condition is not specified in the paper and must be configured.")
    if isinstance(initial_condition, bool) or not isinstance(initial_condition, (int, float)):
        raise TypeError("initial_condition must be numeric.")
    if not isinstance(sampling_rate_hz, (int, float)) or isinstance(sampling_rate_hz, bool) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be positive.")

    result = np.empty_like(values, dtype=float)
    result[0] = initial_condition
    if values.size > 1:
        delta_t = 1.0 / sampling_rate_hz
        result[1:] = initial_condition + np.cumsum((values[:-1] + values[1:]) * 0.5 * delta_t)
    return result
