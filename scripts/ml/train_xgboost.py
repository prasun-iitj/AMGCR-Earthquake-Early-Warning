"""Training and evaluation script for Swiss Set A XGBoost Classifier.

AMGCR Earthquake Research - Supervised ML Track (STEP ML-3)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

from src.models.random_forest import (
    FEATURE_COLUMNS,
    evaluate_group_kfold_cross_validation,
)
from src.models.xgboost_model import (
    SwissXGBoostModel,
    evaluate_xgboost_logo_cross_validation,
)

FEATURE_MATRIX_PATH = Path("reports/features/swiss_set_a_feature_matrix.csv")
OUTPUT_DIR = Path("reports/ml")
MODEL_OUTPUT_PATH = OUTPUT_DIR / "swiss_xgb_model.joblib"
METRICS_OUTPUT_PATH = OUTPUT_DIR / "xgb_cross_validation_results.json"


def main() -> None:
    print("=" * 70)
    print("STEP ML-3: XGBOOST CLASSIFIER TRAINING & CROSS-VALIDATION")
    print("=" * 70)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not FEATURE_MATRIX_PATH.exists():
        raise FileNotFoundError(f"Feature matrix not found at {FEATURE_MATRIX_PATH}")

    df = pd.read_csv(FEATURE_MATRIX_PATH)
    print(f"Loaded dataset: {df.shape[0]} samples, {df.shape[1]} columns")
    print(f"Events: {df['short_id'].nunique()}, Stations: {df['station'].nunique()}")

    # 1. Leave-One-Group-Out Cross-Validation (20 folds, 1 event held out per fold)
    print("\n--- Running Leave-One-Group-Out (LOGO) Cross-Validation (20 folds) ---")
    logo_results = evaluate_xgboost_logo_cross_validation(
        df,
        model_factory=lambda: SwissXGBoostModel(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
        ),
        feature_cols=FEATURE_COLUMNS,
        group_col="short_id",
        target_col="is_earthquake",
    )

    print(f"LOGO Accuracy:  {logo_results['accuracy']:.4f}")
    print(f"LOGO Precision: {logo_results['precision']:.4f}")
    print(f"LOGO Recall:    {logo_results['recall']:.4f}")
    print(f"LOGO F1-score:  {logo_results['f1_score']:.4f}")
    print(f"LOGO ROC-AUC:   {logo_results['roc_auc']:.4f}")
    print(f"LOGO Confusion Matrix (TN, FP, FN, TP): {logo_results['confusion_matrix']}")
    print(f"Mean Fold Time: {logo_results['mean_fold_time_s']:.3f} s")

    # 2. 5-Fold GroupKFold Cross-Validation (4 events held out per fold)
    print("\n--- Running 5-Fold GroupKFold Cross-Validation ---")
    gkf_results = evaluate_group_kfold_cross_validation(
        df,
        n_splits=5,
        model_factory=lambda: SwissXGBoostModel(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
        ),
        feature_cols=FEATURE_COLUMNS,
        group_col="short_id",
        target_col="is_earthquake",
    )
    print(f"GroupKFold Accuracy:  {gkf_results['accuracy']:.4f}")
    print(f"GroupKFold Precision: {gkf_results['precision']:.4f}")
    print(f"GroupKFold Recall:    {gkf_results['recall']:.4f}")
    print(f"GroupKFold F1-score:  {gkf_results['f1_score']:.4f}")
    print(f"GroupKFold ROC-AUC:   {gkf_results['roc_auc']:.4f}")

    # 3. Fit Final Production Model on all 240 samples
    print("\n--- Fitting Full Set A Reference Model & Computing Feature Importances ---")
    final_xgb = SwissXGBoostModel(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
    )
    final_xgb.fit(df[FEATURE_COLUMNS], df["is_earthquake"])
    importances = final_xgb.get_feature_importances()

    print("\nTop 10 Feature Importances (Gain):")
    for feat, imp in importances.head(10).items():
        print(f"  {feat:<28}: {imp:.4f}")

    # 4. Save Model & Evaluation Results
    final_xgb.save(str(MODEL_OUTPUT_PATH))
    print(f"\nSaved model artifact to: {MODEL_OUTPUT_PATH}")

    payload = {
        "model_type": "XGBClassifier",
        "n_samples": len(df),
        "n_features": len(FEATURE_COLUMNS),
        "feature_columns": FEATURE_COLUMNS,
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 4,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "reg_alpha": 0.1,
            "reg_lambda": 1.0,
            "random_state": 42,
        },
        "logo_cv": {
            "accuracy": logo_results["accuracy"],
            "precision": logo_results["precision"],
            "recall": logo_results["recall"],
            "f1_score": logo_results["f1_score"],
            "roc_auc": logo_results["roc_auc"],
            "confusion_matrix": logo_results["confusion_matrix"],
            "tp": logo_results["tp"],
            "fp": logo_results["fp"],
            "tn": logo_results["tn"],
            "fn": logo_results["fn"],
            "mean_fold_time_s": logo_results["mean_fold_time_s"],
            "total_time_s": logo_results["total_time_s"],
            "per_event": logo_results["per_event"],
        },
        "group_kfold_cv": {
            "n_splits": gkf_results["n_splits"],
            "accuracy": gkf_results["accuracy"],
            "precision": gkf_results["precision"],
            "recall": gkf_results["recall"],
            "f1_score": gkf_results["f1_score"],
            "roc_auc": gkf_results["roc_auc"],
            "confusion_matrix": gkf_results["confusion_matrix"],
        },
        "feature_importances": importances.to_dict(),
    }

    with open(METRICS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Saved evaluation metrics to: {METRICS_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
