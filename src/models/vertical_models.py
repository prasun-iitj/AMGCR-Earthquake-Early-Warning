"""Vertical-Only Supervised ML Models for Swiss Earthquake Window Classification.

AMGCR Earthquake Research - Supervised ML Track (STEP ML-4)
Designed for cross-dataset evaluation from Swiss Set A to Swiss Set C (HHZ records).
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
import xgboost as xgb

# Exactly 18 vertical-component features compatible with single-component (HHZ) records
VERTICAL_FEATURE_COLUMNS: List[str] = [
    "z_peak_velocity_m_s",
    "z_p2p_amplitude_m_s",
    "z_rms_velocity_m_s",
    "z_variance",
    "z_std",
    "z_zero_crossing_rate_hz",
    "z_signal_energy_m2_s",
    "z_crest_factor",
    "z_kurtosis",
    "z_skewness",
    "z_cav_m_s",
    "z_dominant_frequency_hz",
    "z_spectral_centroid_hz",
    "z_spectral_bandwidth_hz",
    "z_spectral_rolloff_95_hz",
    "z_spectral_entropy",
    "sta_lta_max",
    "sta_lta_mean",
]


def compute_binary_metrics_vertical(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """Compute standard binary classification metrics including specificity."""
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    cm = confusion_matrix(y_true, y_pred).tolist()

    tn, fp, fn, tp = (
        cm[0][0] if len(cm) > 1 else 0,
        cm[0][1] if len(cm) > 1 else 0,
        cm[1][0] if len(cm) > 1 else 0,
        cm[1][1] if len(cm) > 1 else 0,
    )
    spec = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0

    roc_auc = None
    if y_proba is not None:
        try:
            roc_auc = float(roc_auc_score(y_true, y_proba))
        except ValueError:
            roc_auc = None

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "specificity": spec,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "confusion_matrix": cm,
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
    }


class SwissVerticalRandomForestModel:
    """Vertical-only Random Forest Classifier (18 features)."""

    def __init__(
        self,
        n_estimators: int = 200,
        max_depth: Optional[int] = 6,
        min_samples_split: int = 4,
        min_samples_leaf: int = 2,
        max_features: str | float | int = "sqrt",
        random_state: int = 42,
        class_weight: Optional[str] = "balanced",
        feature_columns: Optional[List[str]] = None,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.class_weight = class_weight
        self.feature_columns = feature_columns or list(VERTICAL_FEATURE_COLUMNS)

        self.classifier = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            max_features=self.max_features,
            random_state=self.random_state,
            class_weight=self.class_weight,
            n_jobs=-1,
        )
        self.is_fitted: bool = False
        self.training_time_s: float = 0.0

    def fit(self, X: pd.DataFrame | np.ndarray, y: pd.Series | np.ndarray) -> SwissVerticalRandomForestModel:
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
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict.")
        if isinstance(X, pd.DataFrame):
            X_mat = X[self.feature_columns].values
        else:
            X_mat = np.asarray(X)
        return self.classifier.predict(X_mat)

    def predict_proba(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict_proba.")
        if isinstance(X, pd.DataFrame):
            X_mat = X[self.feature_columns].values
        else:
            X_mat = np.asarray(X)
        return self.classifier.predict_proba(X_mat)

    def get_feature_importances(self) -> pd.Series:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before retrieving feature importances.")
        return pd.Series(
            self.classifier.feature_importances_,
            index=self.feature_columns,
            name="importance",
        ).sort_values(ascending=False)

    def save(self, filepath: str) -> None:
        payload = {
            "model_type": "SwissVerticalRandomForestModel",
            "classifier": self.classifier,
            "feature_columns": self.feature_columns,
            "params": {
                "n_estimators": self.n_estimators,
                "max_depth": self.max_depth,
                "min_samples_split": self.min_samples_split,
                "min_samples_leaf": self.min_samples_leaf,
                "max_features": self.max_features,
                "random_state": self.random_state,
                "class_weight": self.class_weight,
            },
            "training_time_s": self.training_time_s,
            "is_fitted": self.is_fitted,
        }
        joblib.dump(payload, filepath)

    @classmethod
    def load(cls, filepath: str) -> SwissVerticalRandomForestModel:
        payload = joblib.load(filepath)
        params = payload["params"]
        model = cls(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            min_samples_split=params["min_samples_split"],
            min_samples_leaf=params["min_samples_leaf"],
            max_features=params["max_features"],
            random_state=params["random_state"],
            class_weight=params["class_weight"],
            feature_columns=payload["feature_columns"],
        )
        model.classifier = payload["classifier"]
        model.is_fitted = payload["is_fitted"]
        model.training_time_s = payload.get("training_time_s", 0.0)
        return model


class SwissVerticalXGBoostModel:
    """Vertical-only XGBoost Classifier (18 features)."""

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
        self.feature_columns = feature_columns or list(VERTICAL_FEATURE_COLUMNS)

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

    def fit(self, X: pd.DataFrame | np.ndarray, y: pd.Series | np.ndarray) -> SwissVerticalXGBoostModel:
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
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict.")
        if isinstance(X, pd.DataFrame):
            X_mat = X[self.feature_columns].values
        else:
            X_mat = np.asarray(X)
        return self.classifier.predict(X_mat)

    def predict_proba(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict_proba.")
        if isinstance(X, pd.DataFrame):
            X_mat = X[self.feature_columns].values
        else:
            X_mat = np.asarray(X)
        return self.classifier.predict_proba(X_mat)

    def get_feature_importances(self) -> pd.Series:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before retrieving feature importances.")
        return pd.Series(
            self.classifier.feature_importances_,
            index=self.feature_columns,
            name="importance",
        ).sort_values(ascending=False)

    def save(self, filepath: str) -> None:
        payload = {
            "model_type": "SwissVerticalXGBoostModel",
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
    def load(cls, filepath: str) -> SwissVerticalXGBoostModel:
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


def evaluate_vertical_logo_cross_validation(
    df: pd.DataFrame,
    model_factory,
    feature_cols: Optional[List[str]] = None,
    group_col: str = "short_id",
    target_col: str = "is_earthquake",
) -> Dict[str, Any]:
    """Run Leave-One-Group-Out cross-validation for vertical models."""
    feature_cols = feature_cols or VERTICAL_FEATURE_COLUMNS
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
        m = compute_binary_metrics_vertical(y_true_fold, preds, probas)
        m["event_id"] = test_group
        m["n_test_samples"] = len(test_df)
        m["fit_time_s"] = fit_time
        event_results.append(m)

        y_true_all.extend(y_true_fold)
        y_pred_all.extend(preds)
        y_proba_all.extend(probas)

    overall = compute_binary_metrics_vertical(
        np.array(y_true_all),
        np.array(y_pred_all),
        np.array(y_proba_all),
    )
    overall["mean_fold_time_s"] = float(np.mean(fold_times))
    overall["total_time_s"] = float(np.sum(fold_times))
    overall["n_folds"] = n_splits
    overall["per_event"] = event_results
    overall["y_true"] = [int(v) for v in y_true_all]
    overall["y_pred"] = [int(v) for v in y_pred_all]
    overall["y_proba"] = [float(v) for v in y_proba_all]
    return overall
