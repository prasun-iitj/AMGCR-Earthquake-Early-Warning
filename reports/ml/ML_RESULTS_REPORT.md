# STEP ML-3: Supervised Machine Learning Benchmark Report

See complete canonical document at `docs/ML_RESULTS_REPORT.md`.

## Summary Table

| Detector / Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | TP | TN | FP | FN |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (LOGO CV)** | **0.9917** | **1.0000** | **0.9833** | **0.9916** | **0.9990** | 118 | 120 | 0 | 2 |
| **XGBoost (LOGO CV)** | **0.9833** | **0.9915** | **0.9750** | **0.9832** | **0.9990** | 117 | 119 | 1 | 3 |
| **STA/LTA (Threshold = 8.0)** | **0.9417** | **0.9907** | **0.8917** | **0.9386** | **0.9710** | 107 | 119 | 1 | 13 |

Artifacts in this directory:
- `swiss_rf_model.joblib`: Fitted Random Forest model artifact
- `swiss_xgb_model.joblib`: Fitted XGBoost model artifact
- `rf_cross_validation_results.json`: Random Forest CV metrics
- `xgb_cross_validation_results.json`: XGBoost CV metrics
- `swiss_ml_evaluation_summary.json`: Comprehensive comparative summary
- `per_event_cross_validation_results.csv`: Per-event held-out metrics
- `figures/fig01_roc_curves.png`: ROC comparison plot
- `figures/fig02_feature_importance.png`: Top feature importances
- `figures/fig03_confusion_matrices.png`: Confusion matrices side-by-side
- `figures/fig04_per_event_f1.png`: Per-event F1 scores
