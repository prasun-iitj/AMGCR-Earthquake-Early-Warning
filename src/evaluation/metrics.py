"""Paper-named evaluation metrics with explicit magnitude-scale guards.

Standard MAE and RMSE use record-level mean aggregation. That choice is a
project assumption because the paper does not specify denominators or
aggregation level (RE §9).

Trace: RE §9; Spec R-EVAL, test_metric_equations_and_scale_guard.
"""

from __future__ import annotations

import numpy as np

VALID_MAGNITUDE_SCALES = frozenset({"M_JMA", "M_w"})


class MagnitudeScaleMismatchError(ValueError):
    """Raised when ``M_JMA`` and ``M_w`` labels would be mixed or conflated."""


def require_matching_magnitude_scales(
    left_scale: str,
    right_scale: str,
    *,
    context: str = "comparison",
) -> None:
    """Reject direct comparison or pairing across different magnitude scales."""
    _validate_scale_label(left_scale, "left_scale")
    _validate_scale_label(right_scale, "right_scale")
    if left_scale != right_scale:
        raise MagnitudeScaleMismatchError(
            f"Cannot {context} across magnitude scales {left_scale!r} and "
            f"{right_scale!r}; keep M_JMA and M_w separate (RE §12, §16)."
        )


def mean_absolute_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    magnitude_scale: str,
    target_magnitude_scale: str | None = None,
) -> float:
    """Compute mean absolute error for targets on a single declared scale."""
    y_true_arr, y_pred_arr = _paired_arrays(y_true, y_pred)
    _validate_scale_label(magnitude_scale, "magnitude_scale")
    if target_magnitude_scale is not None:
        _validate_scale_label(target_magnitude_scale, "target_magnitude_scale")
        require_matching_magnitude_scales(
            magnitude_scale,
            target_magnitude_scale,
            context="evaluate targets",
        )
    return float(np.mean(np.abs(y_true_arr - y_pred_arr)))


def root_mean_squared_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    magnitude_scale: str,
    target_magnitude_scale: str | None = None,
) -> float:
    """Compute root mean squared error for targets on a single declared scale."""
    y_true_arr, y_pred_arr = _paired_arrays(y_true, y_pred)
    _validate_scale_label(magnitude_scale, "magnitude_scale")
    if target_magnitude_scale is not None:
        _validate_scale_label(target_magnitude_scale, "target_magnitude_scale")
        require_matching_magnitude_scales(
            magnitude_scale,
            target_magnitude_scale,
            context="evaluate targets",
        )
    return float(np.sqrt(np.mean((y_true_arr - y_pred_arr) ** 2)))


def percent_mae_improvement(
    mae_other: float,
    mae_ours: float,
    *,
    magnitude_scale: str,
    other_magnitude_scale: str | None = None,
) -> float:
    """Apply the paper's percentage MAE improvement formula (RE §9).

    ``Percent improvement = ((MAE_other - MAE_ours) / MAE_other) * 100%``.
    """
    _validate_scale_label(magnitude_scale, "magnitude_scale")
    if other_magnitude_scale is not None:
        _validate_scale_label(other_magnitude_scale, "other_magnitude_scale")
        require_matching_magnitude_scales(
            magnitude_scale,
            other_magnitude_scale,
            context="compare MAE values",
        )
    if not np.isfinite(mae_other) or not np.isfinite(mae_ours):
        raise ValueError("MAE inputs must be finite numbers.")
    if mae_other == 0.0:
        raise ValueError("mae_other must be non-zero to compute percent improvement.")
    return float(((mae_other - mae_ours) / mae_other) * 100.0)


def _paired_arrays(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    y_true_arr = np.asarray(y_true, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    if y_true_arr.ndim != 1 or y_pred_arr.ndim != 1:
        raise ValueError("y_true and y_pred must be one-dimensional arrays.")
    if y_true_arr.shape != y_pred_arr.shape:
        raise ValueError("y_true and y_pred must have the same length.")
    if y_true_arr.size == 0:
        raise ValueError("y_true and y_pred must be non-empty.")
    if not np.isfinite(y_true_arr).all() or not np.isfinite(y_pred_arr).all():
        raise ValueError("y_true and y_pred must contain only finite values.")
    return y_true_arr, y_pred_arr


def _validate_scale_label(scale: str, field_name: str) -> None:
    if scale not in VALID_MAGNITUDE_SCALES:
        raise ValueError(
            f"{field_name} must be one of {sorted(VALID_MAGNITUDE_SCALES)}; got {scale!r}."
        )
