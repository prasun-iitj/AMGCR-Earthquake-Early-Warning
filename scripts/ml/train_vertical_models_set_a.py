"""Training and Cross-Validation script for Vertical-Only ML Models on Swiss Set A.

AMGCR Earthquake Research - Supervised ML Track (STEP ML-4)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

from src.models.vertical_models import (
    VERTICAL_FEATURE_COLUMNS,
    SwissVerticalRandomForestModel,
    SwissVerticalXGBoostModel,
    evaluate_vertical_logo_cross_validation,
)

SET_A_FEATURE_MATRIX = PROJECT_ROOT / "reports/features/swiss_set_a_feature_matrix.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports/ml"
RF_MODEL_PATH = OUTPUT_DIR / "vertical_rf_model_set_a.joblib"
XGB_MODEL_PATH = OUTPUT_DIR / "vertical_xgb_model_set_a.joblib"
SUMMARY_JSON_PATH = OUTPUT_DIR / "vertical_set_a_evaluation_summary.json"
PER_EVENT_CSV_PATH = OUTPUT_DIR / "vertical_set_a_per_event_cv.csv"
SCHEMA_JSON_PATH = OUTPUT_DIR / "vertical_feature_schema.json"


def main() -> None:
    print("=" * 75)
    print("STEP ML-4: VERTICAL-ONLY ML TRAINING & LOGO CROSS-VALIDATION (SET A)")
    print("=" * 75)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df_a = pd.read_csv(SET_A_FEATURE_MATRIX)
    print(f"Loaded Set A dataset: {df_a.shape[0]} samples, {len(VERTICAL_FEATURE_COLUMNS)} vertical features.")
    print(f"Events: {df_a['short_id'].nunique()}, Stations: {df_a['station'].nunique()}")

    # 1. Save Schema
    schema_payload = {
        "n_features": len(VERTICAL_FEATURE_COLUMNS),
        "features": VERTICAL_FEATURE_COLUMNS,
        "input_component": "Vertical (HHZ)",
        "source_dataset": "Swiss Set A",
        "validation_target": "Swiss Set C",
    }
    with open(SCHEMA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(schema_payload, f, indent=2)
    print(f"Saved feature schema to: {SCHEMA_JSON_PATH}")

    # 2. Random Forest LOGO CV
    print("\n[1/3] Running Vertical Random Forest LOGO Cross-Validation (20 folds)...")
    rf_logo = evaluate_vertical_logo_cross_validation(
        df_a,
        model_factory=lambda: SwissVerticalRandomForestModel(
            n_estimators=200,
            max_depth=6,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
        ),
        feature_cols=VERTICAL_FEATURE_COLUMNS,
    )
    print(f"  RF Accuracy:    {rf_logo['accuracy']:.4f}")
    print(f"  RF Precision:   {rf_logo['precision']:.4f}")
    print(f"  RF Recall:      {rf_logo['recall']:.4f}")
    print(f"  RF Specificity: {rf_logo['specificity']:.4f}")
    print(f"  RF F1-Score:    {rf_logo['f1_score']:.4f}")
    print(f"  RF ROC-AUC:     {rf_logo['roc_auc']:.4f}")
    print(f"  RF Confusion Matrix: {rf_logo['confusion_matrix']}")

    # 3. XGBoost LOGO CV
    print("\n[2/3] Running Vertical XGBoost LOGO Cross-Validation (20 folds)...")
    xgb_logo = evaluate_vertical_logo_cross_validation(
        df_a,
        model_factory=lambda: SwissVerticalXGBoostModel(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
        ),
        feature_cols=VERTICAL_FEATURE_COLUMNS,
    )
    print(f"  XGB Accuracy:    {xgb_logo['accuracy']:.4f}")
    print(f"  XGB Precision:   {xgb_logo['precision']:.4f}")
    print(f"  XGB Recall:      {xgb_logo['recall']:.4f}")
    print(f"  XGB Specificity: {xgb_logo['specificity']:.4f}")
    print(f"  XGB F1-Score:    {xgb_logo['f1_score']:.4f}")
    print(f"  XGB ROC-AUC:     {xgb_logo['roc_auc']:.4f}")
    print(f"  XGB Confusion Matrix: {xgb_logo['confusion_matrix']}")

    # 4. Fit Final Frozen Models on all 240 samples
    print("\n[3/3] Fitting & Freezing Final Vertical Models on full Set A...")
    final_rf = SwissVerticalRandomForestModel(
        n_estimators=200,
        max_depth=6,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
    )
    final_rf.fit(df_a[VERTICAL_FEATURE_COLUMNS], df_a["is_earthquake"])
    final_rf.save(str(RF_MODEL_PATH))
    print(f"  Frozen Random Forest model saved: {RF_MODEL_PATH}")

    final_xgb = SwissVerticalXGBoostModel(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
    )
    final_xgb.fit(df_a[VERTICAL_FEATURE_COLUMNS], df_a["is_earthquake"])
    final_xgb.save(str(XGB_MODEL_PATH))
    print(f"  Frozen XGBoost model saved: {XGB_MODEL_PATH}")

    rf_imp = final_rf.get_feature_importances()
    xgb_imp = final_xgb.get_feature_importances()

    print("\nTop 5 Vertical Features (RF Gini):")
    for feat, val in rf_imp.head(5).items():
        print(f"  {feat:<26}: {val:.4f}")

    print("\nTop 5 Vertical Features (XGB Gain):")
    for feat, val in xgb_imp.head(5).items():
        print(f"  {feat:<26}: {val:.4f}")

    # Per-event breakdown
    rf_events = {e["event_id"]: e for e in rf_logo["per_event"]}
    xgb_events = {e["event_id"]: e for e in xgb_logo["per_event"]}
    event_rows = []
    for eid in sorted(rf_events.keys()):
        re = rf_events[eid]
        xe = xgb_events[eid]
        event_rows.append({
            "event_id": eid,
            "rf_accuracy": re["accuracy"],
            "rf_precision": re["precision"],
            "rf_recall": re["recall"],
            "rf_f1": re["f1_score"],
            "rf_roc_auc": re["roc_auc"],
            "xgb_accuracy": xe["accuracy"],
            "xgb_precision": xe["precision"],
            "xgb_recall": xe["recall"],
            "xgb_f1": xe["f1_score"],
            "xgb_roc_auc": xe["roc_auc"],
        })
    per_event_df = pd.DataFrame(event_rows)
    per_event_df.to_csv(PER_EVENT_CSV_PATH, index=False)
    print(f"\nSaved per-event cross-validation metrics to: {PER_EVENT_CSV_PATH}")

    summary_payload = {
        "experiment": "STEP ML-4: Vertical-Only Supervised ML on Swiss Set A",
        "dataset": "Swiss Set A (N=240 windows, 20 events)",
        "features": VERTICAL_FEATURE_COLUMNS,
        "n_features": len(VERTICAL_FEATURE_COLUMNS),
        "models": {
            "random_forest_vertical": {
                "accuracy": rf_logo["accuracy"],
                "precision": rf_logo["precision"],
                "recall": rf_logo["recall"],
                "specificity": rf_logo["specificity"],
                "f1_score": rf_logo["f1_score"],
                "roc_auc": rf_logo["roc_auc"],
                "confusion_matrix": rf_logo["confusion_matrix"],
                "tp": rf_logo["tp"],
                "fp": rf_logo["fp"],
                "tn": rf_logo["tn"],
                "fn": rf_logo["fn"],
                "mean_fold_time_s": rf_logo["mean_fold_time_s"],
                "total_time_s": rf_logo["total_time_s"],
            },
            "xgboost_vertical": {
                "accuracy": xgb_logo["accuracy"],
                "precision": xgb_logo["precision"],
                "recall": xgb_logo["recall"],
                "specificity": xgb_logo["specificity"],
                "f1_score": xgb_logo["f1_score"],
                "roc_auc": xgb_logo["roc_auc"],
                "confusion_matrix": xgb_logo["confusion_matrix"],
                "tp": xgb_logo["tp"],
                "fp": xgb_logo["fp"],
                "tn": xgb_logo["tn"],
                "fn": xgb_logo["fn"],
                "mean_fold_time_s": xgb_logo["mean_fold_time_s"],
                "total_time_s": xgb_logo["total_time_s"],
            },
        },
        "feature_importances_rf": rf_imp.to_dict(),
        "feature_importances_xgb": xgb_imp.to_dict(),
    }
    with open(SUMMARY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)
    print(f"Saved evaluation summary to: {SUMMARY_JSON_PATH}")


if __name__ == "__main__":
    main()
