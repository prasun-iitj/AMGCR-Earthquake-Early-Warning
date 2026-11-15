"""XGBoost Classifier module for Swiss Set A earthquake window classification.

AMGCR Earthquake Research - Supervised ML Track (STEP ML-3)
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional, Tuple
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut

from src.models.random_forest import (
    FEATURE_COLUMNS,
    compute_binary_metrics,
)


class SwissXGBoostModel:
    """Supervised XGBoost Classifier for windowed seismic detection."""

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 4,
        learning_rate: float = 0.05,
        subsample: float = 0.8,
        colsample_bytree: float = 0.8,
        reg_alpha: float = 0.1,
        reg_lambda: float = 1.0,
        random_state: int = 42,
        scale_pos_weight: float = 1.0,
        feature_columns: Optional[List[str]] = None,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.random_state = random_state
        self.scale_pos_weight = scale_pos_weight
        self.feature_columns = feature_columns or list(FEATURE_COLUMNS)

        self.classifier = xgb.XGBClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate,
            subsample=self.subsample,
            colsample_bytree=self.colsample_bytree,
            reg_alpha=self.reg_alpha,
            reg_lambda=self.reg_lambda,
            random_state=self.random_state,
            scale_pos_weight=self.scale_pos_weight,
            eval_metric="logloss",
            n_jobs=-1,
        )
        self.is_fitted: bool = False
        self.training_time_s: float = 0.0

    def fit(self, X: pd.DataFrame | np.ndarray, y: pd.Series | np.ndarray) -> SwissXGBoostModel:
        """Fit the XGBoost classifier on training data."""
        if isinstance(X, pd.DataFrame):
            X_mat = X[self.feature_columns].values
        else:
            X_mat = np.asarray(X)

        y_vec = np.asarray(y)

        t0 = time.perf_counter()
        self.classifier.fit(X_mat, y_vec)
        self.training_time_s = time.perf_counter() - t0
        self.is_fitted = True
        return self

    def predict(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Predict binary class labels (0 = noise, 1 = earthquake)."""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict.")
        if isinstance(X, pd.DataFrame):
            X_mat = X[self.feature_columns].values
        else:
            X_mat = np.asarray(X)
        return self.classifier.predict(X_mat)

    def predict_proba(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        """Predict class probabilities [P(0), P(1)]."""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict_proba.")
        if isinstance(X, pd.DataFrame):
            X_mat = X[self.feature_columns].values
        else:
            X_mat = np.asarray(X)
        return self.classifier.predict_proba(X_mat)

    def get_feature_importances(self, importance_type: str = "gain") -> pd.Series:
        """Return feature importances (gain or weight)."""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before retrieving feature importances.")
        importances = self.classifier.feature_importances_
        return pd.Series(
            importances,
            index=self.feature_columns,
            name=f"importance_{importance_type}",
        ).sort_values(ascending=False)

    def save(self, filepath: str) -> None:
        """Serialize fitted model to disk via joblib."""
        payload = {
            "model_type": "XGBClassifier",
            "classifier": self.classifier,
            "feature_columns": self.feature_columns,
            "params": {
                "n_estimators": self.n_estimators,
                "max_depth": self.max_depth,
                "learning_rate": self.learning_rate,
                "subsample": self.subsample,
                "colsample_bytree": self.colsample_bytree,
                "reg_alpha": self.reg_alpha,
                "reg_lambda": self.reg_lambda,
                "random_state": self.random_state,
                "scale_pos_weight": self.scale_pos_weight,
            },
            "training_time_s": self.training_time_s,
            "is_fitted": self.is_fitted,
        }
        joblib.dump(payload, filepath)

    @classmethod
    def load(cls, filepath: str) -> SwissXGBoostModel:
        """Deserialize fitted model from disk."""
        payload = joblib.load(filepath)
        params = payload["params"]
        model = cls(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            learning_rate=params["learning_rate"],
            subsample=params["subsample"],
            colsample_bytree=params["colsample_bytree"],
            reg_alpha=params["reg_alpha"],
            reg_lambda=params["reg_lambda"],
            random_state=params["random_state"],
            scale_pos_weight=params["scale_pos_weight"],
            feature_columns=payload["feature_columns"],
        )
        model.classifier = payload["classifier"]
        model.is_fitted = payload["is_fitted"]
        model.training_time_s = payload.get("training_time_s", 0.0)
        return model


def evaluate_xgboost_logo_cross_validation(
    df: pd.DataFrame,
    model_factory=lambda: SwissXGBoostModel(),
    feature_cols: Optional[List[str]] = None,
    group_col: str = "short_id",
    target_col: str = "is_earthquake",
) -> Dict[str, Any]:
    """Run Leave-One-Group-Out cross-validation for XGBoost."""
    feature_cols = feature_cols or FEATURE_COLUMNS
    groups = df[group_col].values
    y = df[target_col].values

    logo = LeaveOneGroupOut()
    n_splits = logo.get_n_splits(groups=groups)

    y_true_all = []
    y_pred_all = []
    y_proba_all = []
    event_results = []
    fold_times = []

    for fold_idx, (train_idx, test_idx) in enumerate(logo.split(df, y, groups)):
        test_group = groups[test_idx][0]
        train_df = df.iloc[train_idx]
        test_df = df.iloc[test_idx]

        model = model_factory()
        t0 = time.perf_counter()
        model.fit(train_df[feature_cols], train_df[target_col])
        fit_time = time.perf_counter() - t0
        fold_times.append(fit_time)

        preds = model.predict(test_df[feature_cols])
        probas = model.predict_proba(test_df[feature_cols])[:, 1]

        y_true_fold = test_df[target_col].values
        fold_metrics = compute_binary_metrics(y_true_fold, preds, probas)
        fold_metrics["event_id"] = test_group
        fold_metrics["n_test_samples"] = len(test_df)
        fold_metrics["fit_time_s"] = fit_time
        event_results.append(fold_metrics)

        y_true_all.extend(y_true_fold)
        y_pred_all.extend(preds)
        y_proba_all.extend(probas)

    overall_metrics = compute_binary_metrics(
        np.array(y_true_all),
        np.array(y_pred_all),
        np.array(y_proba_all),
    )
    overall_metrics["mean_fold_time_s"] = float(np.mean(fold_times))
    overall_metrics["total_time_s"] = float(np.sum(fold_times))
    overall_metrics["n_folds"] = n_splits
    overall_metrics["per_event"] = event_results
    overall_metrics["y_true"] = [int(v) for v in y_true_all]
    overall_metrics["y_pred"] = [int(v) for v in y_pred_all]
    overall_metrics["y_proba"] = [float(v) for v in y_proba_all]

    return overall_metrics
