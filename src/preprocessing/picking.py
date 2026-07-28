"""STA/LTA P-wave picking for the EarthESND preprocessing phase.

Window units, the moving-average form, and trigger tie behavior are project
assumptions because the paper specifies only the STA/LTA threshold (2.5).
Window sizes are required arguments and never defaulted.
"""

from __future__ import annotations

import numpy as np


def pick_p_wave_sta_lta(
    trace: np.ndarray,
    threshold: float,
    short_window: int | None,
    long_window: int | None,
) -> int | None:
    """Return the first sample whose absolute-amplitude STA/LTA reaches threshold.

    ``short_window`` and ``long_window`` are sample counts (a project
    assumption). A zero long-term average does not trigger; the paper does not
    state an epsilon policy, so one is not silently introduced.
    """
    values = _as_one_dimensional_trace(trace)
    _validate_window_lengths(short_window, long_window, values.size)
    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or threshold <= 0:
        raise ValueError("threshold must be a positive number.")

    absolute = np.abs(values)
    for index in range(long_window - 1, values.size):
        sta = absolute[index - short_window + 1 : index + 1].mean()
        lta = absolute[index - long_window + 1 : index + 1].mean()
        if lta > 0 and sta / lta >= threshold:
            return index
    return None


def _as_one_dimensional_trace(trace: np.ndarray) -> np.ndarray:
    values = np.asarray(trace, dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("trace must be a non-empty one-dimensional array.")
    if not np.isfinite(values).all():
        raise ValueError("trace must contain only finite values.")
    return values


def _validate_window_lengths(short_window: int | None, long_window: int | None, trace_length: int) -> None:
    if short_window is None or long_window is None:
        raise ValueError("STA/LTA window lengths are not specified in the paper and must be configured.")
    if isinstance(short_window, bool) or isinstance(long_window, bool):
        raise TypeError("STA/LTA window lengths must be integers.")
    if not isinstance(short_window, int) or not isinstance(long_window, int):
        raise TypeError("STA/LTA window lengths must be integers.")
    if short_window <= 0 or long_window <= 0 or short_window > long_window:
        raise ValueError("STA/LTA windows must satisfy 0 < short_window <= long_window.")
    if long_window > trace_length:
        raise ValueError("long_window cannot exceed trace length.")
