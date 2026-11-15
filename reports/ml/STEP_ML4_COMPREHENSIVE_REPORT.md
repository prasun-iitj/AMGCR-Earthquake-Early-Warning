# STEP ML-4 Comprehensive Cross-Dataset Benchmark Report

**Project:** AMGCR Earthquake Research  
**Version:** 1.8.0  
**Date:** 2026-11-12  
**Authors:** AMGCR Research Team  
**Classification:** Final IIT Jodhpur Evaluation Report

---

## 1. Executive Summary

This report consolidates all supervised machine-learning experiments conducted under the AMGCR project,
covering both the within-dataset cross-validation (STEP ML-3, 24 features) and the cross-dataset
independent evaluation (STEP ML-4, 18 vertical features). The key scientific finding is that
vertical-only Random Forest and XGBoost models trained on 20 Swiss Set A earthquake events generalise
to an independent held-out dataset (Swiss Set C, 15 events) with F1-scores of **0.9125** and **0.9169**
respectively. Relative to the window-level STA/LTA (threshold 8.0) baseline used in this report (see §5.3 note),
missed P-wave windows fall by **77.9%** (XGBoost, 81 vs 366 FN) and **76.5%** (Random Forest, 86 vs 366 FN).

> [!NOTE]
> **Corrections applied 2026-11-12 (documentation only, per `FINAL_INTEGRITY_CHECK.md`).** No metric, model, dataset or
> code was changed. Sections 2, 3, 5.3, 6, 7, 8 and 10 were corrected against the saved model artifacts
> and `reports/ml/vertical_*_summary.json`. Version labels: **v1.0.0** is the frozen submission release (29 July 2026);
> **v1.8.0** is an internal documentation/research milestone counter (not a software release).
> This is a windowed offline classification benchmark, not an operational EEW system.

---

## 2. Datasets

| Dataset | Role | Events | Stations | Windows | Channel | Feature Schema |
|:--------|:-----|-------:|--------:|--------:|:--------|:---------------|
| Swiss Set A | Training & CV | 20 | 54 | 240 (120 P + 120 noise) | HH[ZNE] | 24-feature 3C (STEP ML-3) / 18-feature vertical (STEP ML-4) |
| Swiss Set C | Independent test | 15 | 79 | 1,100 (550 P + 550 noise) | HHZ only | 18-feature vertical (STEP ML-4) |

> [!IMPORTANT]
> Swiss Set C was **never used** for training, model selection, feature selection, or threshold tuning.
> It was accessed exclusively at evaluation time after all models were frozen.

> [!NOTE]
> **Independence scope.** Set A and Set C share **no events** (15 unseen events). However, **all 54 Set A stations
> also appear in Set C** (54 of 79 Set C stations are shared; 25 are Set C only). Independence is therefore
> event-level, not station-level; this report does not claim unseen stations.
> (Source: `reports/features/swiss_set_a_feature_matrix.csv`, `swiss_set_c_feature_matrix.csv`.)

---

## 3. Feature Schemas

### 3.1 STEP ML-3: 24-Feature Three-Component Schema (Set A only)

Column names as in `reports/features/swiss_set_a_feature_matrix.csv`:
16 vertical `z_*` features + 2 STA/LTA features + 6 non-vertical features = 24.

| # | Feature | Group |
|--|---------|--------|
| 1 | z_peak_velocity_m_s | Vertical time |
| 2 | z_p2p_amplitude_m_s | Vertical time |
| 3 | z_rms_velocity_m_s | Vertical time |
| 4 | z_variance | Vertical time |
| 5 | z_std | Vertical time |
| 6 | z_zero_crossing_rate_hz | Vertical time |
| 7 | z_signal_energy_m2_s | Vertical time |
| 8 | z_crest_factor | Vertical time |
| 9 | z_kurtosis | Vertical time |
| 10 | z_skewness | Vertical time |
| 11 | z_cav_m_s | Vertical time |
| 12 | z_dominant_frequency_hz | Vertical frequency |
| 13 | z_spectral_centroid_hz | Vertical frequency |
| 14 | z_spectral_bandwidth_hz | Vertical frequency |
| 15 | z_spectral_rolloff_95_hz | Vertical frequency |
| 16 | z_spectral_entropy | Vertical frequency |
| 17 | sta_lta_max | STA/LTA indicator |
| 18 | sta_lta_mean | STA/LTA indicator |
| 19 | h_peak_velocity_m_s | Horizontal |
| 20 | h_rms_velocity_m_s | Horizontal |
| 21 | vec3c_peak_velocity_m_s | 3-component vector |
| 22 | vec3c_rms_velocity_m_s | 3-component vector |
| 23 | vh_ratio | Particle motion |
| 24 | snr_db | Signal quality |

### 3.2 STEP ML-4: 18-Feature Vertical-Only Schema (Set A training + Set C evaluation)

The 18 features are items 1–18 above: the 16 vertical `z_*` features plus `sta_lta_max` and `sta_lta_mean`.
The six excluded features (`h_peak_velocity_m_s`, `h_rms_velocity_m_s`, `vec3c_peak_velocity_m_s`,
`vec3c_rms_velocity_m_s`, `vh_ratio`, `snr_db`) are removed because Set C lacks horizontal channels.
Names and order were verified identical in `src/models/vertical_models.py`,
`reports/ml/vertical_feature_schema.json`, and the `feature_columns` stored in both vertical `.joblib` models.

> [!WARNING]
> **STA window mismatch (disclosed).** `sta_lta_max` and `sta_lta_mean` were computed with
> **STA = 0.5 s** for Set A (`scripts/analysis/run_swiss_set_a_feature_engineering.py`) but
> **STA = 1.0 s** for Set C (`scripts/analysis/run_swiss_set_c_feature_engineering.py`); LTA = 10 s in both.
> Earlier statements of "identical preprocessing" do not hold for these two features. Their numerical impact on the
> Set C metrics is **NOT VERIFIED** (no re-extraction or sensitivity check was performed). No leakage is implied.

---

## 4. Validation Protocol

| Aspect | STEP ML-3 (24-feature) | STEP ML-4 (18-feature) |
|:-------|:-----------------------|:-----------------------|
| CV method | 20-fold Leave-One-Group-Out | 20-fold Leave-One-Group-Out |
| Grouping variable | `short_id` (event ID) | `short_id` (event ID) |
| Test set leakage check | ✅ Disjoint events | ✅ Disjoint events |
| Cross-dataset test | None | Set C (15 independent events) |
| Set C used in training | N/A | ❌ Never |

---

## 5. Cross-Dataset Benchmark Results

### 5.1 STEP ML-3: Set A Leave-One-Group-Out CV (24 features, N=240 windows)

| Model | Accuracy | Precision | Recall | Specificity | F1-Score | ROC-AUC |
|:------|:--------:|:---------:|:------:|:-----------:|:--------:|:--------:|
| **Random Forest** | **99.17%** | **100.0%** | 98.33% | 100.0% | **0.9916** | **0.9990** |
| XGBoost | 98.33% | 99.15% | 97.50% | 99.17% | 0.9832 | 0.9990 |
| STA/LTA (Thresh=8.0) | 94.17% | 99.07% | 89.17% | 99.17% | 0.9386 | 0.9710 |

### 5.2 STEP ML-4: Set A Leave-One-Group-Out CV (18 vertical features, N=240 windows)

| Model | Accuracy | F1-Score | ROC-AUC |
|:------|:--------:|:--------:|:--------:|
| Random Forest (Vertical) | 97.92% | 0.9789 | 0.9994 |
| XGBoost (Vertical) | 98.33% | 0.9832 | 0.9984 |

### 5.3 STEP ML-4: Set C Independent Evaluation (18 vertical features, N=1,100 windows)

| Model | Accuracy | Precision | Recall | Specificity | F1-Score | ROC-AUC | FP | FN |
|:------|:--------:|:---------:|:------:|:-----------:|:--------:|:--------:|:--:|:--:|
| **XGBoost (Vertical)** | **92.27%** | 0.9915 | **0.8527** | 0.9927 | **0.9169** | **0.9780** | 4 | 81 |
| Random Forest (Vertical) | 91.91% | 0.9936 | 0.8436 | 0.9945 | 0.9125 | 0.9767 | 3 | 86 |
| STA/LTA (Thresh=8.0) | 66.73% | 1.0000 | 0.3345 | 1.0000 | 0.5014 | 0.8448 | 0 | 366 |

> [!IMPORTANT]
> **Which "STA/LTA (8.0)"?** The row above is the **ML-4 window-level baseline**: `sta_lta_max >= 8.0` on the
> 4-second candidate window, computed with STA 1.0 s / LTA 10 s (`scripts/ml/evaluate_vertical_models_set_c.py`).
> It is **not** the STEP 2K **record-level detector** (STA 0.5 s / LTA 10 s, search window origin to origin+90 s:
> 401/550 records detected = 72.9%, median absolute timing error 1.24 s; `reports/switzerland_validation/validation_summary.json`).
> The two use different units and settings and their numbers are not directly comparable. STEP 2K results were not modified.
> Missed-detection reduction vs this baseline: XGBoost 77.9% ((366-81)/366), Random Forest 76.5% ((366-86)/366).
> Threshold 8.0 originates from the Swiss Set A sensitivity grid, not from California (California/Swiss baseline = 2.5);
> see `docs/SWISS_STA_LTA_TRANSFER_ANALYSIS.md`.

> [!NOTE]
> The 24-feature models (STEP ML-3) could not be evaluated on Set C because Set C contains only
> HHZ vertical records. The 18-feature vertical models were specifically designed to enable this
> cross-dataset comparison while maintaining scientific integrity.

---

## 6. Generalization Gap Analysis

| Metric | Set A CV (18-feat RF) | Set C Independent (18-feat RF) | Gap |
|:-------|:---------------------:|:------------------------------:|:---:|
| Accuracy | 97.92% | 91.91% | −6.01 pp |
| F1-Score | 0.9789 | 0.9125 | −0.0664 |
| ROC-AUC | 0.9994 | 0.9767 | −0.0227 |
| Recall | 96.67% | 84.36% | −12.3 pp |

**Interpretation of the gap (hypotheses, not tested here):**
- Set C failures concentrate on the smallest events (Mw 2.59–2.69, per `vertical_set_c_per_event_results.csv`) at long distances; the Set C per-event table shows lowest recall there.
- Geometric spreading and attenuation plausibly reduce P-wave amplitude and shift spectral shape toward the noise distribution at large distances.
- Contributing factors that are **not quantified**: event/station differences between sets and the STA window mismatch in `sta_lta_*` features (§3.2).
- The gap is consistent with ordinary cross-dataset shift; no leakage was found. Earlier magnitude/distance ranges quoted here (e.g. "Mw as low as 1.9", "up to 190 km") were not supported by the Set C per-event table and were removed.

---

## 7. Feature Importance Analysis

Values read from the saved models `reports/ml/vertical_rf_model_set_a.joblib` and `vertical_xgb_model_set_a.joblib`
(`feature_importances_`) and verified identical to `feature_importances_rf/xgb` in
`reports/ml/vertical_set_c_evaluation_summary.json` and `vertical_set_a_evaluation_summary.json`.
Both are trained on Set A only; importances do not depend on Set C.

### Random Forest (Gini Impurity), top 9

| Rank | Feature | Importance |
|-----:|:--------|----------:|
| 1 | z_spectral_entropy | 0.1937 |
| 2 | z_spectral_centroid_hz | 0.1511 |
| 3 | z_p2p_amplitude_m_s | 0.1353 |
| 4 | sta_lta_mean | 0.1180 |
| 5 | z_crest_factor | 0.1104 |
| 6 | z_peak_velocity_m_s | 0.0782 |
| 7 | z_zero_crossing_rate_hz | 0.0510 |
| 8 | z_spectral_rolloff_95_hz | 0.0405 |
| 9 | sta_lta_max | 0.0387 |

### XGBoost (normalised Gain), top 9

| Rank | Feature | Importance |
|-----:|:--------|----------:|
| 1 | z_spectral_entropy | 0.3791 |
| 2 | z_spectral_centroid_hz | 0.1913 |
| 3 | sta_lta_mean | 0.1303 |
| 4 | z_p2p_amplitude_m_s | 0.0793 |
| 5 | z_crest_factor | 0.0531 |
| 6 | z_peak_velocity_m_s | 0.0521 |
| 7 | z_kurtosis | 0.0259 |
| 8 | z_zero_crossing_rate_hz | 0.0183 |
| 9 | z_signal_energy_m2_s | 0.0162 |

Note: `sta_lta_mean` and `sta_lta_max` carry a combined ~0.16 (RF) and ~0.14 (XGB) of importance, and are the two
features affected by the STA window mismatch (§3.2).

**Key insight:** `z_spectral_entropy` dominates both models (RF Gini=0.1937, XGB Gain=0.3791).
Spectral entropy distinguishes the broadband frequency content of impulsive P-wave arrivals
from the narrowband character of ambient seismic noise — a physically meaningful discriminator
that generalises across events and distances.

---

## 8. Per-Event Set C Generalization (Selected Events)

Source: `reports/ml/vertical_set_c_per_event_results.csv` (all 15 events are tabulated in
`docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md` §7). Distance ranges are not stored in that CSV and are not quoted.

| Event | Magnitude | XGB Recall | RF Recall | Notes |
|:------|----------:|:----------:|:---------:|:------|
| 2020flmsvb | 2.59 | 0.48 | 0.46 | Lowest recall |
| 2022gzvhhy | 2.60 | 0.63 | 0.63 | Small event |
| 2025rtcqvh | 2.66 | 0.76 | 0.79 | |
| 2024ujblmf | 2.69 | 0.69 | 0.69 | Small event (26 samples) |
| 2025phgpma | 3.01 | 0.74 | 0.70 | |
| Other 10 events | 2.79–4.11 | 0.86–1.00 | 0.84–1.00 | Recall ≥0.84 in all |

---

## 9. Confusion Matrices — Set C (N=1,100)

### Random Forest (Vertical)

```
                 Predicted Noise   Predicted P-wave
Actual Noise          547                3
Actual P-wave          86              464
```

Accuracy: 91.91% | FP: 3 (false alarms) | FN: 86 (missed detections)

### XGBoost (Vertical)

```
                 Predicted Noise   Predicted P-wave
Actual Noise          546                4
Actual P-wave          81              469
```

Accuracy: 92.27% | FP: 4 | FN: 81

### STA/LTA (Threshold = 8.0, frozen from STEP 2K)

```
                 Predicted Noise   Predicted P-wave
Actual Noise          550                0
Actual P-wave         366              184
```

Accuracy: 66.73% | FP: 0 | FN: 366 (missed 66.5% of P-arrivals)

---

## 10. Scientific Integrity Statement

| Requirement | Status |
|:-----------|:-------|
| Zero Set C data in training | ✅ Confirmed — Set C accessed only at evaluation time |
| Zero Set C data in model selection | ✅ Confirmed — LOGO CV on Set A only |
| Zero Set C data in threshold tuning | ✅ Confirmed — decision threshold held at 0.5 |
| Original 24-feature models untouched | ✅ Confirmed — `swiss_rf_model.joblib`, `swiss_xgb_model.joblib` frozen |
| STEP 2K STA/LTA result preserved | ✅ Confirmed — STEP 2K record-level detector (threshold 8.0, 550 records) unchanged; the ML-4 window-level baseline is a separate re-implementation (§5.3) |
| Threshold 8.0 provenance | ⚠️ Derived from the Swiss Set A grid (California threshold was 2.5). Docs state it was pre-declared before Set C; git history cannot independently prove the order (plan, configs and results arrive in one commit) |
| Event grouping in CV | ✅ All Set A stations from one earthquake held out together |
| Feature schema consistency | ⚠️ Same 18 names/order, response correction, bandpass and window length for Set A and Set C; **exception:** `sta_lta_max/mean` use STA 0.5 s (Set A) vs 1.0 s (Set C); impact NOT VERIFIED |
| Anti-leakage test suite | ✅ 89/89 unit tests passing |

---

## 11. Limitations

1. **Window-based classifier:** The models classify 4-second candidate windows as "P-wave" or "noise"; they do not perform continuous unsupervised arrival picking from an infinite data stream.
2. **Dataset size:** Set A training data is N=240 windows (20 events). Tree-based models are well-suited; a deep neural network would require additional regularization or augmentation.
3. **Vertical-only features:** Excluding horizontal and three-component features (particle motion, V/H ratio) limits physics that could aid discrimination at large distances.
4. **Geographic scope:** Both datasets are Swiss/Central European. Generalization to other tectonic regimes (California, Japan) requires additional evaluation.
5. **Magnitude-distance bias:** Failure modes on Set C cluster at small events (Mw ≤ 2.66) at large distances (>70 km). Performance on micro-earthquakes (Mw < 1.5) is untested.

---

## 12. Files Produced (STEP ML-4)

| File | Description |
|:-----|:------------|
| `src/models/vertical_models.py` | Vertical model classes (RF + XGB) with 18-feature schema |
| `scripts/ml/train_vertical_models_set_a.py` | LOGO CV training + model freezing script |
| `scripts/analysis/run_swiss_set_c_feature_engineering.py` | Set C 18-feature extraction script |
| `scripts/ml/evaluate_vertical_models_set_c.py` | Out-of-sample evaluation + figures |
| `reports/ml/vertical_rf_model_set_a.joblib` | Frozen vertical RF model |
| `reports/ml/vertical_xgb_model_set_a.joblib` | Frozen vertical XGB model |
| `reports/ml/vertical_feature_schema.json` | Formal 18-feature schema |
| `reports/ml/vertical_set_a_evaluation_summary.json` | Set A LOGO CV results |
| `reports/ml/vertical_set_a_per_event_cv.csv` | Per-event Set A CV |
| `reports/ml/vertical_set_c_evaluation_summary.json` | Set C independent results |
| `reports/ml/vertical_set_c_per_event_results.csv` | Per-event Set C (15 events) |
| `reports/features/swiss_set_c_feature_matrix.csv` | 1,100 × 35 feature matrix |
| `reports/features/swiss_set_c_feature_summary.json` | Feature summary statistics |
| `reports/ml/figures/fig05_vertical_set_c_roc_curves.png` | ROC curves (Set C) |
| `reports/ml/figures/fig06_vertical_feature_importance.png` | Feature importances |
| `reports/ml/figures/fig07_vertical_set_c_confusion_matrices.png` | Confusion matrices |
| `reports/ml/figures/fig08_vertical_set_c_per_event_f1.png` | Per-event F1 (Set C) |
| `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md` | Canonical full evaluation report |
| `tests/test_vertical_models.py` | 4 automated pytest tests |

---

## 13. Project Version History (ML Steps)

| Version | Step | Description | Date |
|:--------|:-----|:------------|:-----|
| 1.5.0 | ML-1A | SED analyst pick acquisition (120/120) | 2026-11-12 |
| 1.6.0 | ML-2 | 24-feature Set A extraction (240 samples) | 2026-11-12 |
| 1.7.0 | ML-3 | RF (F1=0.9916) + XGB (F1=0.9832) on Set A | 2026-11-12 |
| **1.8.0** | **ML-4** | **18-feature vertical Set C evaluation (RF F1=0.9125, XGB F1=0.9169)** | **2026-11-12** |

---

*Report generated: 2026-11-12. Project documentation version: 1.8.0.*
