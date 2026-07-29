"""Fusion of ESN terminal state with vertical tabular features.

Trace: RE §4–§6; Spec fusion_vector ``[terminal_state | tabular_features]``.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from src.processing.features import VerticalPWaveFeatures

TABULAR_FEATURE_ORDER: tuple[str, ...] = (
    "tau_c",
    "ID2",
    "IV2",
    "PI",
    "RSSCV",
    "Tva",
    "CAV",
)


def tabular_features_to_vector(
    features: VerticalPWaveFeatures | Sequence[float] | np.ndarray,
) -> np.ndarray:
    """Convert tabular features to a fixed-order 1D vector."""
    if isinstance(features, VerticalPWaveFeatures):
        return np.array(
            [getattr(features, name) for name in TABULAR_FEATURE_ORDER],
            dtype=float,
        )
    array = np.asarray(features, dtype=float).reshape(-1)
    if array.shape[0] != len(TABULAR_FEATURE_ORDER):
        raise ValueError(
            f"tabular features must have length {len(TABULAR_FEATURE_ORDER)}; "
            f"got shape {array.shape}."
        )
    return array


def concatenate_terminal_state_and_features(
    terminal_state: np.ndarray,
    tabular_features: VerticalPWaveFeatures | Sequence[float] | np.ndarray,
) -> np.ndarray:
    """Form ``C = [H^(L) | Tab_mag]`` as a single fusion vector.

    Args:
        terminal_state: Final reservoir state ``h_T`` (terminal state only).
        tabular_features: Seven vertical-component features in schema order.

    Returns:
        One-dimensional concatenated fusion vector.
    """
    state = np.asarray(terminal_state, dtype=float).reshape(-1)
    tabular = tabular_features_to_vector(tabular_features)
    return np.concatenate([state, tabular])
