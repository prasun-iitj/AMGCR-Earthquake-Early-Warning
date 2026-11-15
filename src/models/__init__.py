"""Model-related modules for AMGCR Earthquake Research.

Includes Swiss Set A supervised machine-learning models (Random Forest, XGBoost)
and event-grouped cross-validation utilities for seismic window classification.
"""

from src.models.random_forest import (
    FEATURE_COLUMNS,
    SwissRandomForestModel,
    compute_binary_metrics,
    evaluate_group_kfold_cross_validation,
    evaluate_logo_cross_validation,
)
from src.models.xgboost_model import (
    SwissXGBoostModel,
    evaluate_xgboost_logo_cross_validation,
)

from src.models.vertical_models import (
    VERTICAL_FEATURE_COLUMNS,
    SwissVerticalRandomForestModel,
    SwissVerticalXGBoostModel,
    compute_binary_metrics_vertical,
    evaluate_vertical_logo_cross_validation,
)

__all__ = [
    "FEATURE_COLUMNS",
    "VERTICAL_FEATURE_COLUMNS",
    "SwissRandomForestModel",
    "SwissXGBoostModel",
    "SwissVerticalRandomForestModel",
    "SwissVerticalXGBoostModel",
    "compute_binary_metrics",
    "compute_binary_metrics_vertical",
    "evaluate_logo_cross_validation",
    "evaluate_group_kfold_cross_validation",
    "evaluate_xgboost_logo_cross_validation",
    "evaluate_vertical_logo_cross_validation",
]
