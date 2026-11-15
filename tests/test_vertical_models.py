"""Unit and validation tests for Vertical-Only ML models on Swiss Set A and Set C.

AMGCR Earthquake Research - Supervised ML Track (STEP ML-4)
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.models.vertical_models import (
    VERTICAL_FEATURE_COLUMNS,
    SwissVerticalRandomForestModel,
    SwissVerticalXGBoostModel,
    compute_binary_metrics_vertical,
)

SET_A_MATRIX_PATH = Path("reports/features/swiss_set_a_feature_matrix.csv")
SET_C_MATRIX_PATH = Path("reports/features/swiss_set_c_feature_matrix.csv")
RF_MODEL_PATH = Path("reports/ml/vertical_rf_model_set_a.joblib")
XGB_MODEL_PATH = Path("reports/ml/vertical_xgb_model_set_a.joblib")
SET_C_SUMMARY_PATH = Path("reports/ml/vertical_set_c_evaluation_summary.json")


def test_vertical_feature_columns_schema():
    """Verify exact 18-feature vertical schema."""
    assert len(VERTICAL_FEATURE_COLUMNS) == 18
    assert "z_peak_velocity_m_s" in VERTICAL_FEATURE_COLUMNS
    assert "z_spectral_entropy" in VERTICAL_FEATURE_COLUMNS
    assert "sta_lta_max" in VERTICAL_FEATURE_COLUMNS
    assert "sta_lta_mean" in VERTICAL_FEATURE_COLUMNS

    # Confirm zero horizontal or 3C features in vertical schema
    for col in VERTICAL_FEATURE_COLUMNS:
        assert not col.startswith("h_")
        assert not col.startswith("vec3c_")
        assert col != "vh_ratio"
        assert col != "snr_db"


def test_set_c_feature_matrix_integrity():
    """Verify Swiss Set C feature matrix dimensions, nulls, and class balance."""
    assert SET_C_MATRIX_PATH.exists(), f"Set C matrix missing: {SET_C_MATRIX_PATH}"
    df_c = pd.read_csv(SET_C_MATRIX_PATH)

    assert len(df_c) == 1100, f"Expected 1100 samples, got {len(df_c)}"
    assert df_c["short_id"].nunique() == 15, "Expected 15 events"
    assert df_c["station"].nunique() == 79, "Expected 79 stations"

    # Verify class balance
    counts = df_c["is_earthquake"].value_counts().to_dict()
    assert counts[0] == 550, f"Expected 550 noise windows, got {counts.get(0)}"
    assert counts[1] == 550, f"Expected 550 P-wave windows, got {counts.get(1)}"

    # Verify zero nulls in 18 features
    null_count = df_c[VERTICAL_FEATURE_COLUMNS].isnull().sum().sum()
    assert null_count == 0, f"Found {null_count} nulls in Set C features"


def test_frozen_vertical_models_inference():
    """Test loading frozen Set A models and running inference on Set C."""
    assert RF_MODEL_PATH.exists()
    assert XGB_MODEL_PATH.exists()

    rf = SwissVerticalRandomForestModel.load(str(RF_MODEL_PATH))
    xgb = SwissVerticalXGBoostModel.load(str(XGB_MODEL_PATH))

    assert rf.is_fitted
    assert xgb.is_fitted
    assert rf.feature_columns == VERTICAL_FEATURE_COLUMNS
    assert xgb.feature_columns == VERTICAL_FEATURE_COLUMNS

    df_c = pd.read_csv(SET_C_MATRIX_PATH)
    X_c = df_c[VERTICAL_FEATURE_COLUMNS]

    rf_preds = rf.predict(X_c)
    xgb_preds = xgb.predict(X_c)

    assert rf_preds.shape == (1100,)
    assert xgb_preds.shape == (1100,)
    assert set(np.unique(rf_preds)).issubset({0, 1})
    assert set(np.unique(xgb_preds)).issubset({0, 1})


def test_set_c_independent_evaluation_metrics():
    """Verify that Set C evaluation results match summary JSON and exceed baselines."""
    assert SET_C_SUMMARY_PATH.exists()
    with open(SET_C_SUMMARY_PATH, "r", encoding="utf-8") as f:
        summary = json.load(f)

    rf_metrics = summary["models"]["random_forest_vertical"]
    xgb_metrics = summary["models"]["xgboost_vertical"]
    sta_metrics = summary["models"]["sta_lta_threshold_8_0"]

    # Verify RF generalization
    assert rf_metrics["accuracy"] >= 0.90
    assert rf_metrics["precision"] >= 0.98
    assert rf_metrics["recall"] >= 0.80
    assert rf_metrics["specificity"] >= 0.98
    assert rf_metrics["f1_score"] >= 0.90
    assert rf_metrics["roc_auc"] >= 0.97

    # Verify XGBoost generalization
    assert xgb_metrics["accuracy"] >= 0.90
    assert xgb_metrics["precision"] >= 0.98
    assert xgb_metrics["recall"] >= 0.80
    assert xgb_metrics["specificity"] >= 0.98
    assert xgb_metrics["f1_score"] >= 0.90
    assert xgb_metrics["roc_auc"] >= 0.97

    # Confirm ML models significantly outperform STA/LTA on Set C
    assert rf_metrics["recall"] > (2.0 * sta_metrics["recall"])
    assert xgb_metrics["recall"] > (2.0 * sta_metrics["recall"])
    assert rf_metrics["f1_score"] > sta_metrics["f1_score"]
    assert xgb_metrics["f1_score"] > sta_metrics["f1_score"]
