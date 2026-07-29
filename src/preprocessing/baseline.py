"""Baseline correction required by the EarthESND paper."""

from __future__ import annotations

import numpy as np

from src.preprocessing.quality import mean_first_n_samples


def subtract_first_n_mean(trace: np.ndarray, n: int = 20) -> np.ndarray:
    """Return a copy with its first-``n`` mean subtracted from every sample."""
    values = np.asarray(trace, dtype=float)
    baseline = mean_first_n_samples(values, n)
    return values - baseline
