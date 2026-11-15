"""Unit and integration tests for Swiss Set A ML models (Random Forest, XGBoost).

AMGCR Earthquake Research - Supervised ML Track (STEP ML-3)
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import LeaveOneGroupOut

from src.models.random_forest import (
    FEATURE_COLUMNS,
    SwissRandomForestModel,
    compute_binary_metrics,
    evaluate_logo_cross_validation,
)
from src.models.xgboost_model import (
    SwissXGBoostModel,
    evaluate_xgboost_logo_cross_validation,
)

FEATURE_MATRIX_PATH = Path("reports/features/swiss_set_a_feature_matrix.csv")
RF_MODEL_PATH = Path("reports/ml/swiss_rf_model.joblib")
XGB_MODEL_PATH = Path("reports/ml/swiss_xgb_model.joblib")
EVAL_SUMMARY_PATH = Path("reports/ml/swiss_ml_evaluation_summary.json")


@pytest.fixture(scope="module")
def feature_df() -> pd.DataFrame:
    """Load the verified Swiss Set A feature matrix."""
    assert FEATURE_MATRIX_PATH.exists(), f"Feature matrix missing at {FEATURE_MATRIX_PATH}"
    df = pd.read_csv(FEATURE_MATRIX_PATH)
    assert len(df) == 240
    return df


def test_feature_columns_definition():
    """Verify canonical feature column definitions."""
    assert len(FEATURE_COLUMNS) == 24
    assert "z_peak_velocity_m_s" in FEATURE_COLUMNS
    assert "sta_lta_max" in FEATURE_COLUMNS
    assert "snr_db" in FEATURE_COLUMNS
    assert "vec3c_peak_velocity_m_s" in FEATURE_COLUMNS
    assert "z_spectral_entropy" in FEATURE_COLUMNS


def test_random_forest_fit_predict(feature_df: pd.DataFrame, tmp_path: Path):
    """Test SwissRandomForestModel fitting, prediction, importances, and serialization."""
    rf = SwissRandomForestModel(n_estimators=10, max_depth=3, random_state=42)
    assert not rf.is_fitted

    X = feature_df[FEATURE_COLUMNS]
    y = feature_df["is_earthquake"]

    rf.fit(X, y)
    assert rf.is_fitted
    assert rf.training_time_s > 0

    preds = rf.predict(X)
    assert preds.shape == (240,)
    assert set(np.unique(preds)).issubset({0, 1})

    probas = rf.predict_proba(X)
    assert probas.shape == (240, 2)
    assert np.allclose(probas.sum(axis=1), 1.0)

    importances = rf.get_feature_importances()
    assert len(importances) == 24
    assert np.isclose(importances.sum(), 1.0)
    assert importances.iloc[0] >= importances.iloc[-1]

    # Serialization test
    save_file = tmp_path / "test_rf.joblib"
    rf.save(str(save_file))
    assert save_file.exists()

    loaded_rf = SwissRandomForestModel.load(str(save_file))
    assert loaded_rf.is_fitted
    loaded_preds = loaded_rf.predict(X)
    np.testing.assert_array_equal(preds, loaded_preds)


def test_xgboost_fit_predict(feature_df: pd.DataFrame, tmp_path: Path):
    """Test SwissXGBoostModel fitting, prediction, importances, and serialization."""
    xgb = SwissXGBoostModel(n_estimators=10, max_depth=3, random_state=42)
    assert not xgb.is_fitted

    X = feature_df[FEATURE_COLUMNS]
    y = feature_df["is_earthquake"]

    xgb.fit(X, y)
    assert xgb.is_fitted
    assert xgb.training_time_s > 0

    preds = xgb.predict(X)
    assert preds.shape == (240,)
    assert set(np.unique(preds)).issubset({0, 1})

    probas = xgb.predict_proba(X)
    assert probas.shape == (240, 2)
    assert np.allclose(probas.sum(axis=1), 1.0)

    importances = xgb.get_feature_importances()
    assert len(importances) == 24
    assert importances.iloc[0] >= importances.iloc[-1]

    # Serialization test
    save_file = tmp_path / "test_xgb.joblib"
    xgb.save(str(save_file))
    assert save_file.exists()

    loaded_xgb = SwissXGBoostModel.load(str(save_file))
    assert loaded_xgb.is_fitted
    loaded_preds = loaded_xgb.predict(X)
    np.testing.assert_array_equal(preds, loaded_preds)


def test_anti_leakage_grouping(feature_df: pd.DataFrame):
    """Verify that LeaveOneGroupOut strictly segregates earthquake events."""
    groups = feature_df["short_id"].values
    logo = LeaveOneGroupOut()
    n_splits = logo.get_n_splits(groups=groups)
    assert n_splits == 20

    for train_idx, test_idx in logo.split(feature_df, feature_df["is_earthquake"], groups):
        train_events = set(groups[train_idx])
        test_events = set(groups[test_idx])
        # Disjoint set intersection check
        assert len(train_events.intersection(test_events)) == 0
        assert len(test_events) == 1
        assert len(train_events) == 19


def test_compute_binary_metrics():
    """Verify metric computation utility."""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 0, 1])
    y_proba = np.array([0.1, 0.7, 0.4, 0.9])

    m = compute_binary_metrics(y_true, y_pred, y_proba)
    assert m["accuracy"] == 0.5
    assert m["tp"] == 1
    assert m["fp"] == 1
    assert m["tn"] == 1
    assert m["fn"] == 1
    assert m["roc_auc"] is not None
    assert 0.0 <= m["roc_auc"] <= 1.0


def test_saved_model_artifacts_exist():
    """Verify production model artifacts and metrics json exist on disk."""
    assert RF_MODEL_PATH.exists(), f"RF artifact missing: {RF_MODEL_PATH}"
    assert XGB_MODEL_PATH.exists(), f"XGB artifact missing: {XGB_MODEL_PATH}"
    assert EVAL_SUMMARY_PATH.exists(), f"Evaluation summary missing: {EVAL_SUMMARY_PATH}"

    with open(EVAL_SUMMARY_PATH, "r", encoding="utf-8") as f:
        summary = json.load(f)

    assert "models" in summary
    assert "random_forest" in summary["models"]
    assert "xgboost" in summary["models"]
    assert "sta_lta_threshold_8_0" in summary["models"]

    rf_f1 = summary["models"]["random_forest"]["f1_score"]
    xgb_f1 = summary["models"]["xgboost"]["f1_score"]
    sta_f1 = summary["models"]["sta_lta_threshold_8_0"]["f1_score"]

    assert rf_f1 >= 0.95
    assert xgb_f1 >= 0.95
    assert sta_f1 >= 0.85
