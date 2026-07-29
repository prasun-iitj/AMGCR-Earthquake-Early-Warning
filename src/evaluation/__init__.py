"""EarthESND evaluation metrics, benchmarks, and timing helpers.

Trace: Spec Phase 6; RE §9–§12.
"""

from src.evaluation.benchmarks import (
    BenchmarkMetrics,
    evaluate_india_cross_region,
    evaluate_japan_test,
    evaluate_noto_holdout,
)
from src.evaluation.metrics import (
    MagnitudeScaleMismatchError,
    mean_absolute_error,
    percent_mae_improvement,
    require_matching_magnitude_scales,
    root_mean_squared_error,
)
from src.evaluation.timing import TrainingTimingResult, measure_training_seconds_per_epoch

__all__ = [
    "BenchmarkMetrics",
    "MagnitudeScaleMismatchError",
    "TrainingTimingResult",
    "evaluate_india_cross_region",
    "evaluate_japan_test",
    "evaluate_noto_holdout",
    "mean_absolute_error",
    "measure_training_seconds_per_epoch",
    "percent_mae_improvement",
    "require_matching_magnitude_scales",
    "root_mean_squared_error",
]
