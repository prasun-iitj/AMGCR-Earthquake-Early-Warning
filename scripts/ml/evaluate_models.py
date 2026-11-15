"""Comprehensive Evaluation and Comparison script for Swiss Set A ML Models vs STA/LTA.

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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import auc, roc_curve

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
OUTPUT_DIR = Path("reports/ml")
FIGURES_DIR = OUTPUT_DIR / "figures"
SUMMARY_JSON_PATH = OUTPUT_DIR / "swiss_ml_evaluation_summary.json"
PER_EVENT_CSV_PATH = OUTPUT_DIR / "per_event_cross_validation_results.csv"


def evaluate_sta_lta_baseline(
    df: pd.DataFrame,
    threshold: float = 8.0,
    target_col: str = "is_earthquake",
) -> dict:
    """Evaluate traditional STA/LTA threshold detector on the windowed dataset."""
    y_true = df[target_col].values
    sta_lta_vals = df["sta_lta_max"].values
    y_pred = (sta_lta_vals >= threshold).astype(int)

    # For continuous ROC curve, normalize or use raw sta_lta_max as score
    metrics = compute_binary_metrics(y_true, y_pred, y_proba=sta_lta_vals)
    metrics["threshold"] = threshold
    metrics["y_true"] = [int(v) for v in y_true]
    metrics["y_pred"] = [int(v) for v in y_pred]
    metrics["y_proba"] = [float(v) for v in sta_lta_vals]
    return metrics


def plot_roc_curves(
    rf_res: dict,
    xgb_res: dict,
    sta_lta_res: dict,
    output_path: Path,
) -> None:
    """Generate ROC curves comparing RF, XGBoost, and STA/LTA."""
    plt.figure(figsize=(8, 6), dpi=300)

    # RF ROC
    fpr_rf, tpr_rf, _ = roc_curve(rf_res["y_true"], rf_res["y_proba"])
    roc_auc_rf = auc(fpr_rf, tpr_rf)
    plt.plot(fpr_rf, tpr_rf, color="#1f77b4", lw=2.2, label=f"Random Forest (AUC = {roc_auc_rf:.4f})")

    # XGBoost ROC
    fpr_xgb, tpr_xgb, _ = roc_curve(xgb_res["y_true"], xgb_res["y_proba"])
    roc_auc_xgb = auc(fpr_xgb, tpr_xgb)
    plt.plot(fpr_xgb, tpr_xgb, color="#2ca02c", lw=2.2, linestyle="--", label=f"XGBoost (AUC = {roc_auc_xgb:.4f})")

    # STA/LTA continuous ROC
    fpr_sta, tpr_sta, _ = roc_curve(sta_lta_res["y_true"], sta_lta_res["y_proba"])
    roc_auc_sta = auc(fpr_sta, tpr_sta)
    plt.plot(fpr_sta, tpr_sta, color="#ff7f0e", lw=1.8, linestyle=":", label=f"STA/LTA (Continuous, AUC = {roc_auc_sta:.4f})")

    # STA/LTA fixed threshold 8.0 operating point
    sta_fpr_pt = sta_lta_res["fp"] / (sta_lta_res["fp"] + sta_lta_res["tn"])
    sta_tpr_pt = sta_lta_res["tp"] / (sta_lta_res["tp"] + sta_lta_res["fn"])
    plt.scatter([sta_fpr_pt], [sta_tpr_pt], color="#d62728", s=100, zorder=5,
                label=f"STA/LTA Threshold=8.0 (TPR={sta_tpr_pt:.3f}, FPR={sta_fpr_pt:.3f})")

    # Random baseline
    plt.plot([0, 1], [0, 1], color="#7f7f7f", linestyle="--", lw=1.2, label="Random Chance (AUC = 0.50)")

    plt.xlim([-0.02, 1.02])
    plt.ylim([-0.02, 1.02])
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=11, fontweight="bold")
    plt.ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=11, fontweight="bold")
    plt.title("Receiver Operating Characteristic (ROC) Comparison\nSwiss Set A Event-Grouped Cross-Validation (N=240)", fontsize=12, fontweight="bold")
    plt.legend(loc="lower right", framealpha=0.95, fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_feature_importance(
    rf_importances: pd.Series,
    xgb_importances: pd.Series,
    output_path: Path,
    top_n: int = 10,
) -> None:
    """Generate side-by-side feature importance plot."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    top_rf = rf_importances.head(top_n).iloc[::-1]
    ax1.barh(range(len(top_rf)), top_rf.values, color="#1f77b4", edgecolor="black", alpha=0.85)
    ax1.set_yticks(range(len(top_rf)))
    ax1.set_yticklabels(top_rf.index, fontsize=9)
    ax1.set_xlabel("Mean Gini Impurity Reduction", fontsize=10, fontweight="bold")
    ax1.set_title(f"Top {top_n} Features - Random Forest", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.4, axis="x")

    top_xgb = xgb_importances.head(top_n).iloc[::-1]
    ax2.barh(range(len(top_xgb)), top_xgb.values, color="#2ca02c", edgecolor="black", alpha=0.85)
    ax2.set_yticks(range(len(top_xgb)))
    ax2.set_yticklabels(top_xgb.index, fontsize=9)
    ax2.set_xlabel("Relative Gain Importance", fontsize=10, fontweight="bold")
    ax2.set_title(f"Top {top_n} Features - XGBoost", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.4, axis="x")

    plt.suptitle("Supervised Seismic Feature Importance Analysis (Swiss Set A)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_confusion_matrices(
    rf_cm: list,
    xgb_cm: list,
    sta_cm: list,
    output_path: Path,
) -> None:
    """Plot confusion matrices for RF, XGBoost, and STA/LTA."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=300)
    models = [
        ("Random Forest (LOGO CV)", rf_cm, "#1f77b4"),
        ("XGBoost (LOGO CV)", xgb_cm, "#2ca02c"),
        ("STA/LTA (Threshold=8.0)", sta_cm, "#ff7f0e"),
    ]

    for ax, (title, cm, color) in zip(axes, models):
        cm_arr = np.array(cm)
        im = ax.imshow(cm_arr, interpolation="nearest", cmap="Blues")
        ax.set_title(title, fontsize=11, fontweight="bold")

        tick_marks = np.arange(2)
        ax.set_xticks(tick_marks)
        ax.set_yticks(tick_marks)
        ax.set_xticklabels(["Noise (0)", "P-Arrival (1)"], fontsize=10)
        ax.set_yticklabels(["Noise (0)", "P-Arrival (1)"], fontsize=10)

        thresh = cm_arr.max() / 2.0
        for i in range(2):
            for j in range(2):
                val = cm_arr[i, j]
                text_color = "white" if val > thresh else "black"
                ax.text(j, i, f"{val}\n({val/120.0*100:.1f}%)",
                        ha="center", va="center", color=text_color, fontsize=11, fontweight="bold")

        ax.set_ylabel("True Ground Truth", fontsize=10, fontweight="bold")
        ax.set_xlabel("Predicted Class", fontsize=10, fontweight="bold")

    plt.suptitle("Confusion Matrix Benchmark on Swiss Set A (N=240 Windows)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_per_event_f1(
    per_event_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Plot per-event F1-score comparisons across the 20 events."""
    plt.figure(figsize=(14, 5.5), dpi=300)
    x = np.arange(len(per_event_df))
    width = 0.35

    plt.bar(x - width / 2, per_event_df["rf_f1"], width, label="Random Forest", color="#1f77b4", alpha=0.85, edgecolor="black")
    plt.bar(x + width / 2, per_event_df["xgb_f1"], width, label="XGBoost", color="#2ca02c", alpha=0.85, edgecolor="black")

    plt.xticks(x, per_event_df["event_id"], rotation=45, ha="right", fontsize=9)
    plt.ylim([0.0, 1.05])
    plt.ylabel("F1-Score", fontsize=11, fontweight="bold")
    plt.xlabel("Earthquake Event ID (Held-out Fold)", fontsize=11, fontweight="bold")
    plt.title("Per-Event Generalization Performance (Leave-One-Group-Out CV)", fontsize=12, fontweight="bold")
    plt.axhline(1.0, color="#7f7f7f", linestyle="--", alpha=0.7)
    plt.legend(loc="lower right", framealpha=0.95)
    plt.grid(True, linestyle="--", alpha=0.4, axis="y")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    print("=" * 75)
    print("STEP ML-3: COMPREHENSIVE BENCHMARK & COMPARATIVE EVALUATION")
    print("=" * 75)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(FEATURE_MATRIX_PATH)
    print(f"Loaded dataset: {df.shape[0]} rows, 20 events, 24 numeric features.")

    # 1. Random Forest LOGO CV
    print("\n[1/4] Running Random Forest LOGO Cross-Validation...")
    rf_logo = evaluate_logo_cross_validation(
        df,
        model_factory=lambda: SwissRandomForestModel(
            n_estimators=200,
            max_depth=6,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
        ),
        feature_cols=FEATURE_COLUMNS,
    )
    final_rf = SwissRandomForestModel(
        n_estimators=200,
        max_depth=6,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
    )
    final_rf.fit(df[FEATURE_COLUMNS], df["is_earthquake"])
    rf_importances = final_rf.get_feature_importances()

    # 2. XGBoost LOGO CV
    print("[2/4] Running XGBoost LOGO Cross-Validation...")
    xgb_logo = evaluate_xgboost_logo_cross_validation(
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
    )
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
    xgb_importances = final_xgb.get_feature_importances()

    # 3. Traditional STA/LTA Baseline
    print("[3/4] Evaluating Traditional STA/LTA Baseline (Threshold=8.0)...")
    sta_lta_res = evaluate_sta_lta_baseline(df, threshold=8.0)

    # 4. Comparative Metrics Summary
    print("\n" + "=" * 75)
    print("BENCHMARK COMPARISON TABLE (LEAVE-ONE-GROUP-OUT CROSS-VALIDATION, N=240)")
    print("=" * 75)
    print(f"{'Model':<25} | {'Accuracy':<8} | {'Precision':<9} | {'Recall':<8} | {'F1-Score':<8} | {'ROC-AUC':<8}")
    print("-" * 75)
    print(f"{'Random Forest':<25} | {rf_logo['accuracy']:<8.4f} | {rf_logo['precision']:<9.4f} | {rf_logo['recall']:<8.4f} | {rf_logo['f1_score']:<8.4f} | {rf_logo['roc_auc']:<8.4f}")
    print(f"{'XGBoost':<25} | {xgb_logo['accuracy']:<8.4f} | {xgb_logo['precision']:<9.4f} | {xgb_logo['recall']:<8.4f} | {xgb_logo['f1_score']:<8.4f} | {xgb_logo['roc_auc']:<8.4f}")
    print(f"{'STA/LTA (Threshold=8.0)':<25} | {sta_lta_res['accuracy']:<8.4f} | {sta_lta_res['precision']:<9.4f} | {sta_lta_res['recall']:<8.4f} | {sta_lta_res['f1_score']:<8.4f} | {sta_lta_res['roc_auc']:<8.4f}")
    print("=" * 75)

    # Per-event dataframe
    event_rows = []
    rf_events = {e["event_id"]: e for e in rf_logo["per_event"]}
    xgb_events = {e["event_id"]: e for e in xgb_logo["per_event"]}

    for eid in sorted(rf_events.keys()):
        rf_e = rf_events[eid]
        xgb_e = xgb_events[eid]
        event_rows.append({
            "event_id": eid,
            "rf_accuracy": rf_e["accuracy"],
            "rf_precision": rf_e["precision"],
            "rf_recall": rf_e["recall"],
            "rf_f1": rf_e["f1_score"],
            "rf_roc_auc": rf_e["roc_auc"],
            "xgb_accuracy": xgb_e["accuracy"],
            "xgb_precision": xgb_e["precision"],
            "xgb_recall": xgb_e["recall"],
            "xgb_f1": xgb_e["f1_score"],
            "xgb_roc_auc": xgb_e["roc_auc"],
        })
    per_event_df = pd.DataFrame(event_rows)
    per_event_df.to_csv(PER_EVENT_CSV_PATH, index=False)
    print(f"\nSaved per-event cross-validation results to: {PER_EVENT_CSV_PATH}")

    # 5. Generate Figures
    print("\n[4/4] Generating Publication Figures in reports/ml/figures/...")
    fig01_path = FIGURES_DIR / "fig01_roc_curves.png"
    fig02_path = FIGURES_DIR / "fig02_feature_importance.png"
    fig03_path = FIGURES_DIR / "fig03_confusion_matrices.png"
    fig04_path = FIGURES_DIR / "fig04_per_event_f1.png"

    plot_roc_curves(rf_logo, xgb_logo, sta_lta_res, fig01_path)
    plot_feature_importance(rf_importances, xgb_importances, fig02_path)
    plot_confusion_matrices(rf_logo["confusion_matrix"], xgb_logo["confusion_matrix"], sta_lta_res["confusion_matrix"], fig03_path)
    plot_per_event_f1(per_event_df, fig04_path)

    print(f"Generated: {fig01_path}")
    print(f"Generated: {fig02_path}")
    print(f"Generated: {fig03_path}")
    print(f"Generated: {fig04_path}")

    # 6. Save Overall Summary JSON
    summary_payload = {
        "task": "STEP ML-3: Supervised Machine Learning Benchmark",
        "dataset": "Swiss Set A (N=240 windows, 120 early-P arrivals, 120 ambient noise)",
        "cross_validation_strategy": "Leave-One-Group-Out (LOGO) grouped by earthquake event (short_id, 20 folds)",
        "anti_leakage_guarantee": "Zero cross-station or cross-window earthquake event leakage",
        "models": {
            "random_forest": {
                "accuracy": rf_logo["accuracy"],
                "precision": rf_logo["precision"],
                "recall": rf_logo["recall"],
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
            "xgboost": {
                "accuracy": xgb_logo["accuracy"],
                "precision": xgb_logo["precision"],
                "recall": xgb_logo["recall"],
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
            "sta_lta_threshold_8_0": {
                "threshold": 8.0,
                "accuracy": sta_lta_res["accuracy"],
                "precision": sta_lta_res["precision"],
                "recall": sta_lta_res["recall"],
                "f1_score": sta_lta_res["f1_score"],
                "roc_auc": sta_lta_res["roc_auc"],
                "confusion_matrix": sta_lta_res["confusion_matrix"],
                "tp": sta_lta_res["tp"],
                "fp": sta_lta_res["fp"],
                "tn": sta_lta_res["tn"],
                "fn": sta_lta_res["fn"],
            },
        },
        "top_features_rf": rf_importances.head(10).to_dict(),
        "top_features_xgb": xgb_importances.head(10).to_dict(),
    }

    with open(SUMMARY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)
    print(f"\nSaved benchmark evaluation summary to: {SUMMARY_JSON_PATH}")


if __name__ == "__main__":
    main()
