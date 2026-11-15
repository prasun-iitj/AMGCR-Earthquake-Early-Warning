# STEP ML-4: Independent Cross-Dataset Evaluation Report (Swiss Set A to Set C)

See complete canonical report at `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md`.

## Independent Benchmark Summary (Swiss Set C, N=1,100 Samples)

| Model | Accuracy | Precision | Recall | Specificity | F1-Score | ROC-AUC | TP | TN | FP | FN |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Vertical)** | **0.9227** | **0.9915** | **0.8527** | **0.9927** | **0.9169** | **0.9780** | 469 | 546 | 4 | 81 |
| **Random Forest (Vertical)** | **0.9191** | **0.9936** | **0.8436** | **0.9945** | **0.9125** | **0.9767** | 464 | 547 | 3 | 86 |
| **STA/LTA (Threshold = 8.0)** | **0.6673** | **1.0000** | **0.3345** | **1.0000** | **0.5014** | **0.8448** | 184 | 550 | 0 | 366 |

Artifacts in this directory:
- `vertical_rf_model_set_a.joblib`: Frozen Vertical Random Forest model
- `vertical_xgb_model_set_a.joblib`: Frozen Vertical XGBoost model
- `vertical_feature_schema.json`: Formal 18-feature vertical schema
- `vertical_set_a_evaluation_summary.json`: Set A LOGO CV summary
- `vertical_set_a_per_event_cv.csv`: Set A per-event CV table
- `vertical_set_c_evaluation_summary.json`: Set C independent evaluation summary
- `vertical_set_c_per_event_results.csv`: Set C per-event results across 15 events
- `figures/fig05_vertical_set_c_roc_curves.png`: Set C ROC curves
- `figures/fig06_vertical_feature_importance.png`: Feature importance bar charts
- `figures/fig07_vertical_set_c_confusion_matrices.png`: Confusion matrices side-by-side
- `figures/fig08_vertical_set_c_per_event_f1.png`: Per-event F1 scores
