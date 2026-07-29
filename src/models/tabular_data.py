"""Tabular dataset helpers for synthetic augmentation and split guards.

Trace: RE §7.1 (augmented tabular union); Spec gate — train-only synthetic fit.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from src.data.manifest import VALID_SPLITS


TRAINING_SPLIT = "train"


def assert_training_split_only(split: str) -> None:
    """Ensure a declared split label is the training partition."""
    if split not in VALID_SPLITS:
        raise ValueError(f"split must be one of {sorted(VALID_SPLITS)}, got {split!r}.")
    if split != TRAINING_SPLIT:
        raise ValueError(
            "Tabular synthetic generation and ensemble fitting must use training "
            f"data only; received split {split!r}."
        )


def assert_all_training_splits(splits: Sequence[str]) -> None:
    """Ensure every record split label is ``train``."""
    for split in splits:
        assert_training_split_only(split)


def build_augmented_tabular(
    tab_syn: np.ndarray,
    y_syn: np.ndarray,
    tab_act: np.ndarray,
    y_act: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Form ``{Tab_aug | y_aug} = {Tab_syn | y_syn} || {Tab_act | y_act}``.

    Trace: RE §7.1.

    Args:
        tab_syn: Synthetic feature matrix ``Tab_syn``.
        y_syn: Synthetic targets ``y_syn``.
        tab_act: Real training features ``Tab_act``.
        y_act: Real training targets ``y_act``.

    Returns:
        Concatenated feature matrix and target vector for augmented training.
    """
    tab_syn = np.asarray(tab_syn, dtype=float)
    y_syn = np.asarray(y_syn, dtype=float)
    tab_act = np.asarray(tab_act, dtype=float)
    y_act = np.asarray(y_act, dtype=float)

    if tab_syn.ndim != 2 or tab_act.ndim != 2:
        raise ValueError("Feature matrices must be two-dimensional.")
    if tab_syn.shape[1] != tab_act.shape[1]:
        raise ValueError("Synthetic and real feature matrices must share column count.")
    if y_syn.ndim != 1 or y_act.ndim != 1:
        raise ValueError("Target vectors must be one-dimensional.")
    if tab_syn.shape[0] != y_syn.shape[0]:
        raise ValueError("Synthetic features and targets row counts must match.")
    if tab_act.shape[0] != y_act.shape[0]:
        raise ValueError("Real features and targets row counts must match.")

    features = np.vstack([tab_syn, tab_act])
    targets = np.concatenate([y_syn, y_act])
    return features, targets
