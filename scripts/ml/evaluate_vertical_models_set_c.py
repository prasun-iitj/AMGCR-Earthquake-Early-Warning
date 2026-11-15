"""Independent Cross-Dataset Evaluation of Vertical ML Models on Swiss Set C.

AMGCR Earthquake Research - Supervised ML Track (STEP ML-4)
Evaluates frozen Set A models strictly out-of-sample on Swiss Set C (1,100 samples, 15 events).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import auc, roc_curve

from src.models.vertical_models import (
    VERTICAL_FEATURE_COLUMNS,
    SwissVerticalRandomForestModel,
    SwissVerticalXGBoostModel,
    compute_binary_metrics_vertical,
)

SET_C_FEATURE_MATRIX = PROJECT_ROOT / "reports/features/swiss_set_c_feature_matrix.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports/ml"
FIGURES_DIR = OUTPUT_DIR / "figures"
RF_MODEL_PATH = OUTPUT_DIR / "vertical_rf_model_set_a.joblib"
XGB_MODEL_PATH = OUTPUT_DIR / "vertical_xgb_model_set_a.joblib"
SUMMARY_JSON_PATH = OUTPUT_DIR / "vertical_set_c_evaluation_summary.json"
PER_EVENT_CSV_PATH = OUTPUT_DIR / "vertical_set_c_per_event_results.csv"


def plot_set_c_roc_curves(
    rf_res: dict,
    xgb_res: dict,
    sta_lta_res: dict,
    output_path: Path,
) -> None:
    plt.figure(figsize=(8, 6), dpi=300)

    fpr_rf, tpr_rf, _ = roc_curve(rf_res["y_true"], rf_res["y_proba"])
    roc_auc_rf = auc(fpr_rf, tpr_rf)
    plt.plot(fpr_rf, tpr_rf, color="#1f77b4", lw=2.2, label=f"Random Forest (Set A Model, AUC = {roc_auc_rf:.4f})")

    fpr_xgb, tpr_xgb, _ = roc_curve(xgb_res["y_true"], xgb_res["y_proba"])
    roc_auc_xgb = auc(fpr_xgb, tpr_xgb)
    plt.plot(fpr_xgb, tpr_xgb, color="#2ca02c", lw=2.2, linestyle="--", label=f"XGBoost (Set A Model, AUC = {roc_auc_xgb:.4f})")

    fpr_sta, tpr_sta, _ = roc_curve(sta_lta_res["y_true"], sta_lta_res["y_proba"])
    roc_auc_sta = auc(fpr_sta, tpr_sta)
    plt.plot(fpr_sta, tpr_sta, color="#ff7f0e", lw=1.8, linestyle=":", label=f"STA/LTA (Continuous, AUC = {roc_auc_sta:.4f})")

    sta_fpr_pt = sta_lta_res["fp"] / (sta_lta_res["fp"] + sta_lta_res["tn"])
    sta_tpr_pt = sta_lta_res["tp"] / (sta_lta_res["tp"] + sta_lta_res["fn"])
    plt.scatter([sta_fpr_pt], [sta_tpr_pt], color="#d62728", s=100, zorder=5,
                label=f"STA/LTA Threshold=8.0 (TPR={sta_tpr_pt:.3f}, FPR={sta_fpr_pt:.3f})")

    plt.plot([0, 1], [0, 1], color="#7f7f7f", linestyle="--", lw=1.2, label="Random Chance (AUC = 0.50)")

    plt.xlim([-0.02, 1.02])
    plt.ylim([-0.02, 1.02])
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=11, fontweight="bold")
    plt.ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=11, fontweight="bold")
    plt.title("ROC Curves: Independent Evaluation on Swiss Set C\n(N=1,100 Samples, 15 Independent Events)", fontsize=12, fontweight="bold")
    plt.legend(loc="lower right", framealpha=0.95, fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_set_c_confusion_matrices(
    rf_cm: list,
    xgb_cm: list,
    sta_cm: list,
    output_path: Path,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=300)
    models = [
        ("Random Forest (Set C)", rf_cm, "#1f77b4"),
        ("XGBoost (Set C)", xgb_cm, "#2ca02c"),
        ("STA/LTA Threshold=8.0 (Set C)", sta_cm, "#ff7f0e"),
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
                ax.text(j, i, f"{val}\n({val/550.0*100:.1f}%)",
                        ha="center", va="center", color=text_color, fontsize=11, fontweight="bold")

        ax.set_ylabel("True Ground Truth", fontsize=10, fontweight="bold")
        ax.set_xlabel("Predicted Class", fontsize=10, fontweight="bold")

    plt.suptitle("Confusion Matrix Benchmark on Swiss Set C (N=1,100 Windows)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_set_c_feature_importance(
    rf_imp: pd.Series,
    xgb_imp: pd.Series,
    output_path: Path,
    top_n: int = 10,
) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    top_rf = rf_imp.head(top_n).iloc[::-1]
    ax1.barh(range(len(top_rf)), top_rf.values, color="#1f77b4", edgecolor="black", alpha=0.85)
    ax1.set_yticks(range(len(top_rf)))
    ax1.set_yticklabels(top_rf.index, fontsize=9)
    ax1.set_xlabel("Mean Gini Impurity Reduction", fontsize=10, fontweight="bold")
    ax1.set_title(f"Top {top_n} Vertical Features - Random Forest", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.4, axis="x")

    top_xgb = xgb_imp.head(top_n).iloc[::-1]
    ax2.barh(range(len(top_xgb)), top_xgb.values, color="#2ca02c", edgecolor="black", alpha=0.85)
    ax2.set_yticks(range(len(top_xgb)))
    ax2.set_yticklabels(top_xgb.index, fontsize=9)
    ax2.set_xlabel("Relative Gain Importance", fontsize=10, fontweight="bold")
    ax2.set_title(f"Top {top_n} Vertical Features - XGBoost", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle="--", alpha=0.4, axis="x")

    plt.suptitle("Vertical-Only Seismic Feature Importance (Trained on Set A)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_set_c_per_event_f1(
    per_event_df: pd.DataFrame,
    output_path: Path,
) -> None:
    plt.figure(figsize=(14, 5.5), dpi=300)
    x = np.arange(len(per_event_df))
    width = 0.28

    plt.bar(x - width, per_event_df["rf_f1"], width, label="Random Forest", color="#1f77b4", alpha=0.85, edgecolor="black")
    plt.bar(x, per_event_df["xgb_f1"], width, label="XGBoost", color="#2ca02c", alpha=0.85, edgecolor="black")
    plt.bar(x + width, per_event_df["sta_f1"], width, label="STA/LTA (8.0)", color="#ff7f0e", alpha=0.85, edgecolor="black")

    plt.xticks(x, per_event_df["short_id"], rotation=45, ha="right", fontsize=9)
    plt.ylim([0.0, 1.05])
    plt.ylabel("F1-Score", fontsize=11, fontweight="bold")
    plt.xlabel("Independent Swiss Earthquake Event ID", fontsize=11, fontweight="bold")
    plt.title("Per-Event Generalization Benchmark on Independent Swiss Set C (15 Events)", fontsize=12, fontweight="bold")
    plt.axhline(1.0, color="#7f7f7f", linestyle="--", alpha=0.7)
    plt.legend(loc="lower right", framealpha=0.95)
    plt.grid(True, linestyle="--", alpha=0.4, axis="y")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    print("=" * 80)
    print("STEP ML-4: INDEPENDENT CROSS-DATASET EVALUATION ON SWISS SET C")
    print("=" * 80)

    if not SET_C_FEATURE_MATRIX.exists():
        raise FileNotFoundError(f"Set C feature matrix not found at {SET_C_FEATURE_MATRIX}")

    df_c = pd.read_csv(SET_C_FEATURE_MATRIX)
    print(f"Loaded Set C dataset: {df_c.shape[0]} samples, {df_c['short_id'].nunique()} events, {df_c['station'].nunique()} stations.")

    # 1. Load Frozen Models
    print("\nLoading frozen Set A vertical models...")
    rf_model = SwissVerticalRandomForestModel.load(str(RF_MODEL_PATH))
    xgb_model = SwissVerticalXGBoostModel.load(str(XGB_MODEL_PATH))
    print(f"  Loaded Random Forest from: {RF_MODEL_PATH}")
    print(f"  Loaded XGBoost from:       {XGB_MODEL_PATH}")

    X_c = df_c[VERTICAL_FEATURE_COLUMNS]
    y_c = df_c["is_earthquake"].values

    # 2. Evaluate Random Forest on Set C
    print("\n[1/3] Evaluating Random Forest on Set C (1,100 samples)...")
    rf_preds = rf_model.predict(X_c)
    rf_probas = rf_model.predict_proba(X_c)[:, 1]
    rf_metrics = compute_binary_metrics_vertical(y_c, rf_preds, rf_probas)
    rf_metrics["y_true"] = [int(v) for v in y_c]
    rf_metrics["y_pred"] = [int(v) for v in rf_preds]
    rf_metrics["y_proba"] = [float(v) for v in rf_probas]

    print(f"  RF Set C Accuracy:    {rf_metrics['accuracy']:.4f}")
    print(f"  RF Set C Precision:   {rf_metrics['precision']:.4f}")
    print(f"  RF Set C Recall:      {rf_metrics['recall']:.4f}")
    print(f"  RF Set C Specificity: {rf_metrics['specificity']:.4f}")
    print(f"  RF Set C F1-Score:    {rf_metrics['f1_score']:.4f}")
    print(f"  RF Set C ROC-AUC:     {rf_metrics['roc_auc']:.4f}")
    print(f"  RF Set C Confusion Matrix: {rf_metrics['confusion_matrix']}")

    # 3. Evaluate XGBoost on Set C
    print("\n[2/3] Evaluating XGBoost on Set C (1,100 samples)...")
    xgb_preds = xgb_model.predict(X_c)
    xgb_probas = xgb_model.predict_proba(X_c)[:, 1]
    xgb_metrics = compute_binary_metrics_vertical(y_c, xgb_preds, xgb_probas)
    xgb_metrics["y_true"] = [int(v) for v in y_c]
    xgb_metrics["y_pred"] = [int(v) for v in xgb_preds]
    xgb_metrics["y_proba"] = [float(v) for v in xgb_probas]

    print(f"  XGB Set C Accuracy:    {xgb_metrics['accuracy']:.4f}")
    print(f"  XGB Set C Precision:   {xgb_metrics['precision']:.4f}")
    print(f"  XGB Set C Recall:      {xgb_metrics['recall']:.4f}")
    print(f"  XGB Set C Specificity: {xgb_metrics['specificity']:.4f}")
    print(f"  XGB Set C F1-Score:    {xgb_metrics['f1_score']:.4f}")
    print(f"  XGB Set C ROC-AUC:     {xgb_metrics['roc_auc']:.4f}")
    print(f"  XGB Set C Confusion Matrix: {xgb_metrics['confusion_matrix']}")

    # 4. Evaluate STA/LTA Baseline on Set C
    print("\n[3/3] Evaluating STA/LTA (Threshold=8.0) Baseline on Set C...")
    sta_lta_vals = df_c["sta_lta_max"].values
    sta_preds = (sta_lta_vals >= 8.0).astype(int)
    sta_metrics = compute_binary_metrics_vertical(y_c, sta_preds, sta_lta_vals)
    sta_metrics["y_true"] = [int(v) for v in y_c]
    sta_metrics["y_pred"] = [int(v) for v in sta_preds]
    sta_metrics["y_proba"] = [float(v) for v in sta_lta_vals]

    print(f"  STA/LTA Set C Accuracy:    {sta_metrics['accuracy']:.4f}")
    print(f"  STA/LTA Set C Precision:   {sta_metrics['precision']:.4f}")
    print(f"  STA/LTA Set C Recall:      {sta_metrics['recall']:.4f}")
    print(f"  STA/LTA Set C Specificity: {sta_metrics['specificity']:.4f}")
    print(f"  STA/LTA Set C F1-Score:    {sta_metrics['f1_score']:.4f}")
    print(f"  STA/LTA Set C ROC-AUC:     {sta_metrics['roc_auc']:.4f}")
    print(f"  STA/LTA Set C Confusion Matrix: {sta_metrics['confusion_matrix']}")

    # 5. Print Comparison Benchmark Table
    print("\n" + "=" * 80)
    print("INDEPENDENT SWISS SET C CROSS-DATASET BENCHMARK (N=1,100 SAMPLES, 15 EVENTS)")
    print("=" * 80)
    print(f"{'Model':<25} | {'Accuracy':<8} | {'Precision':<9} | {'Recall':<8} | {'Specificity':<11} | {'F1-Score':<8} | {'ROC-AUC':<8}")
    print("-" * 80)
    print(f"{'Random Forest (Vertical)':<25} | {rf_metrics['accuracy']:<8.4f} | {rf_metrics['precision']:<9.4f} | {rf_metrics['recall']:<8.4f} | {rf_metrics['specificity']:<11.4f} | {rf_metrics['f1_score']:<8.4f} | {rf_metrics['roc_auc']:<8.4f}")
    print(f"{'XGBoost (Vertical)':<25} | {xgb_metrics['accuracy']:<8.4f} | {xgb_metrics['precision']:<9.4f} | {xgb_metrics['recall']:<8.4f} | {xgb_metrics['specificity']:<11.4f} | {xgb_metrics['f1_score']:<8.4f} | {xgb_metrics['roc_auc']:<8.4f}")
    print(f"{'STA/LTA (Threshold=8.0)':<25} | {sta_metrics['accuracy']:<8.4f} | {sta_metrics['precision']:<9.4f} | {sta_metrics['recall']:<8.4f} | {sta_metrics['specificity']:<11.4f} | {sta_metrics['f1_score']:<8.4f} | {sta_metrics['roc_auc']:<8.4f}")
    print("=" * 80)

    # 6. Per-Event Analysis
    df_c["rf_pred"] = rf_preds
    df_c["xgb_pred"] = xgb_preds
    df_c["sta_pred"] = sta_preds

    event_rows = []
    for sid, group in df_c.groupby("short_id"):
        y_g = group["is_earthquake"].values
        rf_g = compute_binary_metrics_vertical(y_g, group["rf_pred"].values)
        xgb_g = compute_binary_metrics_vertical(y_g, group["xgb_pred"].values)
        sta_g = compute_binary_metrics_vertical(y_g, group["sta_pred"].values)
        mag = float(group["magnitude"].iloc[0])

        event_rows.append({
            "short_id": sid,
            "magnitude": mag,
            "n_samples": len(group),
            "rf_accuracy": rf_g["accuracy"],
            "rf_precision": rf_g["precision"],
            "rf_recall": rf_g["recall"],
            "rf_f1": rf_g["f1_score"],
            "xgb_accuracy": xgb_g["accuracy"],
            "xgb_precision": xgb_g["precision"],
            "xgb_recall": xgb_g["recall"],
            "xgb_f1": xgb_g["f1_score"],
            "sta_accuracy": sta_g["accuracy"],
            "sta_precision": sta_g["precision"],
            "sta_recall": sta_g["recall"],
            "sta_f1": sta_g["f1_score"],
        })

    per_event_df = pd.DataFrame(event_rows).sort_values("magnitude")
    per_event_df.to_csv(PER_EVENT_CSV_PATH, index=False)
    print(f"\nSaved per-event results across 15 events to: {PER_EVENT_CSV_PATH}")

    # 7. Generate Publication Figures
    print("\nGenerating Publication Figures in reports/ml/figures/...")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig05_path = FIGURES_DIR / "fig05_vertical_set_c_roc_curves.png"
    fig06_path = FIGURES_DIR / "fig06_vertical_feature_importance.png"
    fig07_path = FIGURES_DIR / "fig07_vertical_set_c_confusion_matrices.png"
    fig08_path = FIGURES_DIR / "fig08_vertical_set_c_per_event_f1.png"

    rf_imp = rf_model.get_feature_importances()
    xgb_imp = xgb_model.get_feature_importances()

    plot_set_c_roc_curves(rf_metrics, xgb_metrics, sta_metrics, fig05_path)
    plot_set_c_feature_importance(rf_imp, xgb_imp, fig06_path)
    plot_set_c_confusion_matrices(rf_metrics["confusion_matrix"], xgb_metrics["confusion_matrix"], sta_metrics["confusion_matrix"], fig07_path)
    plot_set_c_per_event_f1(per_event_df, fig08_path)

    print(f"  Generated: {fig05_path}")
    print(f"  Generated: {fig06_path}")
    print(f"  Generated: {fig07_path}")
    print(f"  Generated: {fig08_path}")

    # 8. Save Comprehensive Summary JSON
    summary_payload = {
        "evaluation": "STEP ML-4: Independent Swiss Set C Cross-Dataset Evaluation",
        "dataset_name": "Swiss Set C Independent Validation Set",
        "n_samples": len(df_c),
        "n_events": df_c["short_id"].nunique(),
        "n_stations": df_c["station"].nunique(),
        "class_balance": {
            "negative_noise_windows": int((y_c == 0).sum()),
            "positive_p_wave_windows": int((y_c == 1).sum()),
        },
        "features": VERTICAL_FEATURE_COLUMNS,
        "n_features": len(VERTICAL_FEATURE_COLUMNS),
        "training_origin": "Swiss Set A (Fitted and Frozen, Zero Set C Tuning)",
        "models": {
            "random_forest_vertical": {
                "accuracy": rf_metrics["accuracy"],
                "precision": rf_metrics["precision"],
                "recall": rf_metrics["recall"],
                "specificity": rf_metrics["specificity"],
                "f1_score": rf_metrics["f1_score"],
                "roc_auc": rf_metrics["roc_auc"],
                "confusion_matrix": rf_metrics["confusion_matrix"],
                "tp": rf_metrics["tp"],
                "fp": rf_metrics["fp"],
                "tn": rf_metrics["tn"],
                "fn": rf_metrics["fn"],
            },
            "xgboost_vertical": {
                "accuracy": xgb_metrics["accuracy"],
                "precision": xgb_metrics["precision"],
                "recall": xgb_metrics["recall"],
                "specificity": xgb_metrics["specificity"],
                "f1_score": xgb_metrics["f1_score"],
                "roc_auc": xgb_metrics["roc_auc"],
                "confusion_matrix": xgb_metrics["confusion_matrix"],
                "tp": xgb_metrics["tp"],
                "fp": xgb_metrics["fp"],
                "tn": xgb_metrics["tn"],
                "fn": xgb_metrics["fn"],
            },
            "sta_lta_threshold_8_0": {
                "threshold": 8.0,
                "accuracy": sta_metrics["accuracy"],
                "precision": sta_metrics["precision"],
                "recall": sta_metrics["recall"],
                "specificity": sta_metrics["specificity"],
                "f1_score": sta_metrics["f1_score"],
                "roc_auc": sta_metrics["roc_auc"],
                "confusion_matrix": sta_metrics["confusion_matrix"],
                "tp": sta_metrics["tp"],
                "fp": sta_metrics["fp"],
                "tn": sta_metrics["tn"],
                "fn": sta_metrics["fn"],
            },
        },
        "feature_importances_rf": rf_imp.to_dict(),
        "feature_importances_xgb": xgb_imp.to_dict(),
    }
    with open(SUMMARY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)
    print(f"\nSaved Set C evaluation summary to: {SUMMARY_JSON_PATH}")


if __name__ == "__main__":
    main()
