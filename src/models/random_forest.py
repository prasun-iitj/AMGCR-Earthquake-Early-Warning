"""Random Forest Classifier module for Swiss Set A earthquake window classification.

AMGCR Earthquake Research - Supervised ML Track (STEP ML-3)
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple
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

# Canonical list of 24 physical and spectral features extracted in STEP ML-2
FEATURE_COLUMNS: List[str] = [
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
    "h_peak_velocity_m_s",
    "h_rms_velocity_m_s",
    "vec3c_peak_velocity_m_s",
    "vec3c_rms_velocity_m_s",
    "vh_ratio",
    "sta_lta_max",
    "sta_lta_mean",
    "snr_db",
]


class SwissRandomForestModel:
    """Supervised Random Forest Classifier for windowed seismic detection."""

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
        self.feature_columns = feature_columns or list(FEATURE_COLUMNS)

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

    def fit(self, X: pd.DataFrame | np.ndarray, y: pd.Series | np.ndarray) -> SwissRandomForestModel:
        """Fit the Random Forest classifier on training data."""
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

    def get_feature_importances(self) -> pd.Series:
        """Return Gini impurity-based feature importances."""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before retrieving feature importances.")
        return pd.Series(
            self.classifier.feature_importances_,
            index=self.feature_columns,
            name="importance",
        ).sort_values(ascending=False)

    def save(self, filepath: str) -> None:
        """Serialize fitted model to disk via joblib."""
        payload = {
            "model_type": "RandomForestClassifier",
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
    def load(cls, filepath: str) -> SwissRandomForestModel:
        """Deserialize fitted model from disk."""
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


def compute_binary_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """Compute standard binary classification metrics."""
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    cm = confusion_matrix(y_true, y_pred).tolist()

    roc_auc = None
    if y_proba is not None:
        try:
            roc_auc = float(roc_auc_score(y_true, y_proba))
        except ValueError:
            roc_auc = None

    tn, fp, fn, tp = (
        cm[0][0] if len(cm) > 1 else 0,
        cm[0][1] if len(cm) > 1 else 0,
        cm[1][0] if len(cm) > 1 else 0,
        cm[1][1] if len(cm) > 1 else 0,
    )

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "confusion_matrix": cm,
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
    }


def evaluate_logo_cross_validation(
    df: pd.DataFrame,
    model_factory=lambda: SwissRandomForestModel(),
    feature_cols: Optional[List[str]] = None,
    group_col: str = "short_id",
    target_col: str = "is_earthquake",
) -> Dict[str, Any]:
    """Run Leave-One-Group-Out (LOGO) cross-validation grouped by earthquake event."""
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


def evaluate_group_kfold_cross_validation(
    df: pd.DataFrame,
    n_splits: int = 5,
    model_factory=lambda: SwissRandomForestModel(),
    feature_cols: Optional[List[str]] = None,
    group_col: str = "short_id",
    target_col: str = "is_earthquake",
    random_state: int = 42,
) -> Dict[str, Any]:
    """Run GroupKFold cross-validation grouped by earthquake event."""
    feature_cols = feature_cols or FEATURE_COLUMNS
    groups = df[group_col].values
    y = df[target_col].values

    gkf = GroupKFold(n_splits=n_splits)

    y_true_all = []
    y_pred_all = []
    y_proba_all = []
    fold_metrics_list = []
    fold_times = []

    for fold_idx, (train_idx, test_idx) in enumerate(gkf.split(df, y, groups)):
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
        m = compute_binary_metrics(y_true_fold, preds, probas)
        m["fold"] = fold_idx + 1
        m["n_test_samples"] = len(test_df)
        m["events_in_test"] = list(set(groups[test_idx]))
        m["fit_time_s"] = fit_time
        fold_metrics_list.append(m)

        y_true_all.extend(y_true_fold)
        y_pred_all.extend(preds)
        y_proba_all.extend(probas)

    overall = compute_binary_metrics(
        np.array(y_true_all),
        np.array(y_pred_all),
        np.array(y_proba_all),
    )
    overall["n_splits"] = n_splits
    overall["folds"] = fold_metrics_list
    overall["mean_fold_time_s"] = float(np.mean(fold_times))
    overall["total_time_s"] = float(np.sum(fold_times))
    return overall
