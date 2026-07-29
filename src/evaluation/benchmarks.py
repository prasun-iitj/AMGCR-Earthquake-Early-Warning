"""Scope-separated benchmark evaluation for Japan, Noto, and India.

Each entry point enforces the paper's target scale for that evaluation scope
and validates manifest provenance when records are supplied.

Trace: RE §10–§12; Spec R-EVAL.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from src.data.manifest import ManifestRecord
from src.evaluation.metrics import mean_absolute_error, root_mean_squared_error

JAPAN_TEST_MAGNITUDE_SCALE = "M_JMA"
NOTO_HOLDOUT_MAGNITUDE_SCALE = "M_JMA"
INDIA_CROSS_REGION_MAGNITUDE_SCALE = "M_w"

SCOPE_JAPAN_TEST = "japan_test"
SCOPE_NOTO_HOLDOUT = "noto_holdout"
SCOPE_INDIA_CROSS_REGION = "india_cross_region"


@dataclass(frozen=True, slots=True)
class BenchmarkMetrics:
    """MAE and RMSE for one declared evaluation scope and magnitude scale."""

    scope: str
    magnitude_scale: str
    mae: float
    rmse: float
    record_count: int


def evaluate_japan_test(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    magnitude_scale: str,
    records: Sequence[ManifestRecord] | None = None,
) -> BenchmarkMetrics:
    """Evaluate the stratified Japan test split in ``M_JMA`` (RE §10–§11)."""
    return _evaluate_scope(
        scope=SCOPE_JAPAN_TEST,
        required_scale=JAPAN_TEST_MAGNITUDE_SCALE,
        magnitude_scale=magnitude_scale,
        y_true=y_true,
        y_pred=y_pred,
        records=records,
        record_predicate=_is_japan_test_record,
    )


def evaluate_noto_holdout(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    magnitude_scale: str,
    records: Sequence[ManifestRecord] | None = None,
) -> BenchmarkMetrics:
    """Evaluate the 2024 Noto held-out event in ``M_JMA`` (RE §12)."""
    return _evaluate_scope(
        scope=SCOPE_NOTO_HOLDOUT,
        required_scale=NOTO_HOLDOUT_MAGNITUDE_SCALE,
        magnitude_scale=magnitude_scale,
        y_true=y_true,
        y_pred=y_pred,
        records=records,
        record_predicate=_is_noto_holdout_record,
    )


def evaluate_india_cross_region(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    magnitude_scale: str,
    records: Sequence[ManifestRecord] | None = None,
) -> BenchmarkMetrics:
    """Evaluate the 157-record India cross-region set in ``M_w`` (RE §12)."""
    return _evaluate_scope(
        scope=SCOPE_INDIA_CROSS_REGION,
        required_scale=INDIA_CROSS_REGION_MAGNITUDE_SCALE,
        magnitude_scale=magnitude_scale,
        y_true=y_true,
        y_pred=y_pred,
        records=records,
        record_predicate=_is_india_cross_region_record,
    )


def _evaluate_scope(
    *,
    scope: str,
    required_scale: str,
    magnitude_scale: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    records: Sequence[ManifestRecord] | None,
    record_predicate,
) -> BenchmarkMetrics:
    if magnitude_scale != required_scale:
        raise ValueError(
            f"{scope} requires magnitude_scale {required_scale!r}; got {magnitude_scale!r}."
        )
    y_true_arr = np.asarray(y_true, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    if records is not None:
        if len(records) != y_true_arr.shape[0]:
            raise ValueError("records length must match y_true length.")
        for index, record in enumerate(records):
            if not record_predicate(record):
                raise ValueError(
                    f"Record at index {index} is outside the {scope!r} evaluation scope."
                )
            if record.magnitude_scale != required_scale:
                raise ValueError(
                    f"Record at index {index} has magnitude_scale {record.magnitude_scale!r}; "
                    f"{scope!r} requires {required_scale!r}."
                )
    mae = mean_absolute_error(y_true_arr, y_pred_arr, magnitude_scale=magnitude_scale)
    rmse = root_mean_squared_error(y_true_arr, y_pred_arr, magnitude_scale=magnitude_scale)
    return BenchmarkMetrics(
        scope=scope,
        magnitude_scale=magnitude_scale,
        mae=mae,
        rmse=rmse,
        record_count=int(y_true_arr.shape[0]),
    )


def _is_japan_test_record(record: ManifestRecord) -> bool:
    return (
        record.source_region.lower() == "japan"
        and record.split == "test"
        and not record.is_noto_holdout
    )


def _is_noto_holdout_record(record: ManifestRecord) -> bool:
    return record.is_noto_holdout


def _is_india_cross_region_record(record: ManifestRecord) -> bool:
    return record.source_region.lower() == "india"
