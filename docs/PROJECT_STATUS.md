# PROJECT_STATUS.md

Current progress for **AMGCR Earthquake Research**. Authoritative scope: [PROJECT_CHARTER.md](PROJECT_CHARTER.md).

**Release:** **v1.0.0 — Submission Release** (29 July 2026), frozen. The "Version 1.8.0" label in the footer is an **internal documentation/research milestone counter** (STEP ML-4, 2026-11-12), not a software release; `pyproject.toml` and `CITATION.cff` remain 1.0.0.

**Documentation corrections (2026-11-12):** (a) `sta_lta_max/mean` features use STA 0.5 s for Set A and 1.0 s for Set C; numerical impact NOT VERIFIED. (b) All 54 Set A stations also appear in Set C; independence is event-level only. (c) Threshold 8.0 came from the Swiss Set A grid (California baseline was 2.5); docs state it was pre-declared, but git cannot prove the order. (d) Offline windowed benchmark, not an operational EEW system. See `FINAL_INTEGRITY_CHECK.md`.

---

## Project information

| Field | Value |
|-------|--------|
| **Programme** | Swiss certificate EEW research (AMGCR) |
| **Primary focus** | Europe (long-term) |
| **Pilot implementation** | USA / California (IRIS–EarthScope) — **complete** |
| **Reference track** | EarthESND literature track **documented**; executable pipeline optional (v3.0); K-NET reproduction **not started** |
| **Current stage** | **Set C Independent ML Evaluation** (2026-11-12) — Swiss Set A vertical models evaluated out-of-sample on Swiss Set C (1,100 samples) |

---

## Status summary (canonical)

| Component | Status |
|-----------|--------|
| EarthESND literature / optional track | ✅ **Documented** (not in v1.0.0 code tree) |
| USA / California IRIS pilot | ✅ **Complete** |
| EDA | ✅ **Complete** |
| Signal analysis | ✅ **Complete** |
| Preprocessing | ✅ **Complete** |
| Feature engineering | ✅ **Complete** |
| Results & discussion | ✅ **Complete** |
| Reproducibility Statement (D-S1) | ✅ **Complete** |
| Data Availability Statement (D-S2) | ✅ **Complete** |
| Final Research Report (D-F1) | ✅ **Complete** |
| Presentation outline & script (D-F2/D-F3) | ✅ **Complete** |
| FINAL_SUBMISSION package (D-F4) | ✅ **Complete** |
| Submission validation | ✅ **PASS** |
| **Version 2.0 interactive platform** (`website/`) | ✅ **Complete** (2 August 2026) |
| **Swiss SED methods-transfer acquisition** | ✅ **Complete** (2026-09-06) — 20 events, 120 CH 3C MiniSEED records |
| **Swiss independent validation-set design** | ✅ **Design/audit corrected** (2026-09-11, STEP 2I.1) — Independent Swiss/Adjacent-Border Validation Set (15 locked events) |
| **Swiss independent validation acquisition** | ✅ **Complete** (2026-09-11, STEP 2J) — 15/15 events, 550 CH HHZ MiniSEED + StationXML |
| **Swiss independent frozen STA/LTA validation** | ✅ **Complete** (2026-09-11, STEP 2K) — threshold **8.0** evaluated as pre-declared; 550/550 records; **no** retuning |
| **Swiss scientific consistency audit** | ✅ **Complete** (2026-09-11) — headline metrics agree across CSVs/JSON/results markdown |
| **Swiss ML feasibility audit** | ✅ **Complete** (2026-09-11, STEP 3A) — **NO-GO** on unlabelled tables; **unblocked via STEP ML-1A** |
| **Swiss Set A SED analyst pick acquisition** | ✅ **Complete** (2026-11-12, STEP ML-1A) — 120/120 (100%) manual first-P picks verified & persisted; raw QuakeML provenance saved |
| **Swiss Set A 3C feature extraction** | ✅ **Complete** (2026-11-12, STEP ML-2) — 240 window samples (120 P-wave + 120 noise), 24 causal features, response-corrected VEL (m/s) |
| **Swiss Set A Supervised ML Training** | ✅ **Complete** (2026-11-12, STEP ML-3) — Random Forest (F1=0.9916), XGBoost (F1=0.9832), STA/LTA (F1=0.9386); 20-fold LOGO CV |
| **Swiss Set C Vertical-Only ML Evaluation** | ✅ **Complete** (2026-11-12, STEP ML-4) — 18-feature vertical models trained on Set A (RF F1=0.9789, XGB F1=0.9832); independently evaluated on Set C (1,100 samples, 15 events): RF F1=0.9125, XGB F1=0.9169, STA/LTA F1=0.5014 |
| **AI/ML certificate wrap** | ✅ **Complete** (2026-11-11) — position paper + 16-slide deck; first models trained in STEP ML-3 |

---

## Version 2.0 platform (complete — 2026-08-02)

| Component | Status |
|-----------|--------|
| Interactive website (19 routes) | ✅ **Complete** |
| Research dashboard | ✅ **Complete** |
| Workflow, results, dataset, waveform, map explorers | ✅ **Complete** |
| Documentation portal & global search | ✅ **Complete** |
| SEO, error pages, accessibility polish | ✅ **Complete** |
| Production deployment documentation | ✅ **Complete** |

Release notes: [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md) · Website guide: [website/README.md](../website/README.md)

---

## Archived — v1.0 milestones (2026-07-29)

| Milestone | Documentation / output |
|-----------|-------------------------|
| Acquisition | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |
| EDA | [EDA_REPORT.md](EDA_REPORT.md) |
| Signal analysis | [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) |
| Preprocessing | [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) |
| Feature engineering | [FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md) |
| Interpretation | [RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md) |
| Proposal v1 | [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md) |
| Final report | [Research_Report_Final.md](../reports/Research_Report_Final.md) |
| Submission package | [FINAL_SUBMISSION/](../FINAL_SUBMISSION/) |
| Deliverable audit | [FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md) |

EarthESND scientific reproduction (K-NET tables): ⬜ **Not started** — optional **Version 3.0** track ([PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md)).

---

## Version 2.1 / Version 3.0 roadmap

See [ROADMAP.md](ROADMAP.md). Summary:

- **Version 2.1** — platform maintenance, content sync, deployment hardening, optional UX improvements  
- **Version 3.0** — Europe dataset expansion (ORFEUS/EIDA), EarthESND training/evaluation, real-time streaming, operational deployment  

---

## Current goal

Deliver the **13 November 2026** IIT Jodhpur final evaluation with STEP ML-4 complete. All scientific results locked. California v1.0, Set C STA/LTA (threshold 8.0, STEP 2K), and 24-feature models frozen. Vertical-only models trained on Set A and independently evaluated on Set C (N=1,100). 89/89 tests passing.

---

## Blockers

- **Previous Blocker (Lack of Set A independent labels):** **RESOLVED** via STEP ML-1A (100% manual analyst coverage achieved; 120/120 records).
- **Previous Blocker (Lack of Swiss feature matrix):** **RESOLVED** via STEP ML-2 (`reports/features/swiss_set_a_feature_matrix.csv`, 240 samples × 24 features).
- **Previous Blocker (3C features incompatible with Set C HHZ-only):** **RESOLVED** via STEP ML-4 vertical-only 18-feature schema; Set C independently evaluated with 1,100 samples.
- **No remaining blockers for IIT Jodhpur evaluation.** All results are complete and documented.

---

## STEP ML-1A: Swiss Set A SED Analyst Pick Acquisition (Complete — 2026-11-12)

| Field | Detail |
|---|---|
| **Task** | STEP ML-1A: SED Manual Analyst Pick Acquisition & Independent Verification |
| **Status** | ✅ **Complete & Verified (100.0%)** |
| **Events Audited** | 20 / 20 events (Graechen, Elm, Arolla, Mulhouse, Porrentruy, etc.) |
| **Waveform Records Matched** | **120 / 120 (100.0%)** same-station first-P picks matched |
| **Evaluation Mode** | **120 manual analyst picks** (100% manual; 0 automatic, 0 missing) |
| **Phase Breakdown** | Pg: 114, P1: 3, Pn: 3 |
| **Latency Statistics** | Min: 1.83 s, Median: 10.06 s, Max: 27.27 s (all within [0, 90 s] and within waveform boundaries) |
| **Circularity Status** | **Eliminated.** Labels are external ground-truth picks from SED certified analysts (`tdiehl@sc3ag`, etc.), entirely independent of STA/LTA detector |
| **Files Created** | - `data/manifests/sed_switzerland_set_a_picks.csv` (120 rows, standard schema)<br>- `scripts/download/download_sed_switzerland_set_a_picks.py`<br>- `reports/switzerland_set_a_picks/picks_acquisition_summary.json`<br>- `data/metadata/switzerland/{event_id}/quakeml.xml` (20 raw QuakeML provenance files)<br>- `tests/test_switzerland_set_a_picks.py` (3 automated tests, passing) |
| **Verification** | Verified event IDs, station codes, phase hints, UTC timestamps, waveform interval coverage, and independent test suite (72/72 tests pass) |
| **Limitations** | Set A contains confirmed earthquakes only (N=120 records across 20 events). Ambient noise windows from pre-origin intervals must be sampled for binary classification |
| **Next Step** | **STEP ML-2: Feature Extraction.** Complete (240 samples × 24 features). Next: STEP ML-3 Supervised Models. |

---

## STEP ML-2: Swiss Set A Feature Extraction (Complete — 2026-11-12)

| Field | Detail |
|---|---|
| **Task** | STEP ML-2: Causal 3C Waveform Feature Engineering with Verified Ground Truth |
| **Status** | ✅ **Complete & Tested (120 / 120 records, zero failures)** |
| **Dataset Size** | **240 window samples** across 20 events / 54 stations (balanced: 120 positive P-wave + 120 negative noise) |
| **Window Construction** | Causal 4.0-second windows: Class 0 from quiet pre-origin buffer `[origin - 35s, origin - 31s]`; Class 1 from verified P-onset `[P_pick, P_pick + 4.0s]`. Zero future sample leakage. |
| **Instrument Response** | Deconvolved using official StationXML metadata to physical **velocity (m/s)** with Nyquist-aware pre-filtering (`output='VEL'`, water-level 60.0, bandpass 0.1–15.0 Hz). |
| **Feature Set (24 features)** | Time-domain (peak velocity, p2p, RMS, variance, zero-crossing rate, energy, crest factor, kurtosis, skewness, CAV); Frequency-domain (dominant frequency, spectral centroid, bandwidth, rolloff, entropy); 3-Component vector metrics (horizontal velocity, 3C vector velocity, V/H ratio); Seismic indicators (continuous STA/LTA max/mean, SNR in dB). |
| **Target Variables** | Binary classification (`is_earthquake`: 0=noise, 1=P-arrival) + Continuous regression targets (`p_latency_s`, `epicentral_distance_km`, `hypocentral_distance_km`). |
| **Anti-Leakage Grouping** | `short_id` and `event_id` preserved on all rows to enforce `GroupKFold` or `LeaveOneGroupOut` (no cross-station event leakage). |
| **Files Created** | - `scripts/analysis/run_swiss_set_a_feature_engineering.py`<br>- `reports/features/swiss_set_a_feature_matrix.csv` (240 rows × 45 columns)<br>- `reports/features/swiss_set_a_per_record_features.csv` (120 rows × 21 columns)<br>- `reports/features/swiss_set_a_feature_summary.json`<br>- `reports/features/swiss_figures/fig01_noise_vs_pwave_velocity.png`<br>- `reports/features/swiss_figures/fig02_p_latency_vs_distance.png`<br>- `reports/features/swiss_figures/fig03_sta_lta_vs_vh_ratio.png`<br>- `reports/features/swiss_figures/fig04_energy_vs_frequency.png`<br>- `tests/test_swiss_set_a_features.py` (7 automated tests, passing) |
| **Verification** | 79 / 79 repository unit tests passing. Physical unit checks, finite value checks, and strict causal timestamp bounds validated. |
| **Limitations** | Dataset size N=240 windows (120 earthquake + 120 noise) across 20 events. Tree-based models (Random Forest, XGBoost) with GroupKFold cross-validation are best suited; deep CNN requires careful regularization or waveform sliding. |
| **Next Step** | **STEP ML-3: Supervised Model Implementation.** Implement Random Forest, XGBoost, and 1D CNN classifiers on Set A with LeaveOneEventOut cross-validation; evaluate comparatively on locked Set C. |

---

## STEP ML-3: Supervised ML Model Implementation & Benchmarking (Complete — 2026-11-12)

| Field | Detail |
|---|---|
| **Task** | STEP ML-3: Supervised ML Model Training (Random Forest & XGBoost) vs STA/LTA Baseline |
| **Status** | ✅ **Complete, Cross-Validated, and Formally Documented** |
| **Dataset** | Swiss Set A (`reports/features/swiss_set_a_feature_matrix.csv`, N=240 windows: 120 early-P + 120 noise) |
| **Validation Protocol** | **20-Fold Leave-One-Group-Out (LOGO)** cross-validation grouped by earthquake event ID (`short_id`). All stations for a given event strictly held out together in each fold. |
| **Anti-Leakage Guarantee** | **Zero cross-station or cross-window event leakage.** All fold splits are disjoint in events. Set C completely isolated and untouched. |
| **Random Forest Results** | **Accuracy: 99.17%**, **Precision: 100.0%** (0 false alarms), **Recall: 98.33%** (2 missed), **F1: 0.9916**, **ROC-AUC: 0.9990** |
| **XGBoost Results** | **Accuracy: 98.33%**, **Precision: 99.15%** (1 false alarm), **Recall: 97.50%** (3 missed), **F1: 0.9832**, **ROC-AUC: 0.9990** |
| **STA/LTA Baseline (Thresh=8.0)** | **Accuracy: 94.17%**, **Precision: 99.07%** (1 false alarm), **Recall: 89.17%** (13 missed), **F1: 0.9386**, **ROC-AUC: 0.9710** |
| **Scientific Findings** | RF reduced missed P-wave detections by **84.6%** compared to STA/LTA (2 vs 13 false negatives) while eliminating all false alarms on ambient noise (0 vs 1). Dominant physical features: `z_spectral_entropy` (Gini=0.176, Gain=0.380), `snr_db`, `z_spectral_centroid_hz`, and `vec3c_peak_velocity_m_s`. |
| **Per-Event Generalization** | **18 / 20 events achieved 100% test accuracy in Random Forest**; 17 / 20 in XGBoost. |
| **Files Created** | - `src/models/random_forest.py`<br>- `src/models/xgboost_model.py`<br>- `scripts/ml/train_random_forest.py`<br>- `scripts/ml/train_xgboost.py`<br>- `scripts/ml/evaluate_models.py`<br>- `reports/ml/swiss_rf_model.joblib`<br>- `reports/ml/swiss_xgb_model.joblib`<br>- `reports/ml/rf_cross_validation_results.json`<br>- `reports/ml/xgb_cross_validation_results.json`<br>- `reports/ml/swiss_ml_evaluation_summary.json`<br>- `reports/ml/per_event_cross_validation_results.csv`<br>- `reports/ml/figures/fig01_roc_curves.png`<br>- `reports/ml/figures/fig02_feature_importance.png`<br>- `reports/ml/figures/fig03_confusion_matrices.png`<br>- `reports/ml/figures/fig04_per_event_f1.png`<br>- `docs/ML_RESULTS_REPORT.md` (and `reports/ml/ML_RESULTS_REPORT.md`)<br>- `tests/test_ml_models.py` (6 automated tests, passing) |
| **Verification** | **85 / 85 project unit tests passing.** Deterministic reproducibility, probability consistency, and anti-leakage group integrity confirmed. |
| **Scientific Limitations** | Evaluates a 4.0-second candidate window (early P-wave onset vs ambient noise); does not constitute an unconstrained streaming continuous picker. Swiss Set C remains locked. |
| **Next Step** | Await user approval. Next recommended action: STEP ML-4 (1D CNN waveform prototype or continuous streaming stress test) prior to any Set C evaluation. |

---

## STEP ML-4: Swiss Set C Vertical-Only Independent Evaluation (Complete — 2026-11-12)

| Field | Detail |
|---|---|
| **Task** | STEP ML-4: Vertical-Only ML Experiment — Train on Set A, Evaluate Independently on Set C |
| **Status** | ✅ **Complete, Independently Evaluated, and Formally Documented** |
| **Motivation** | Swiss Set C contains only HHZ vertical records; the 24-feature Set A models require three-component data (H channels). A separate 18-feature vertical-only experiment was required for a valid cross-dataset generalization test. |
| **Training Dataset** | Swiss Set A (`reports/features/swiss_set_a_feature_matrix.csv`, N=240 windows: 120 P-wave + 120 noise) — same 20 events |
| **Evaluation Dataset** | Swiss Set C (`reports/features/swiss_set_c_feature_matrix.csv`, N=1,100 windows: 550 P-wave + 550 noise) — **15 independent events never seen during training; 79 stations, of which 54 (all Set A stations) also appear in Set A and 25 are Set C only** |
| **Feature Schema** | **18 vertical-only features** (excludes `h_*`, `vec3c_*`, `vh_ratio`, `snr_db`). Formal schema: `reports/ml/vertical_feature_schema.json`. Identical preprocessing, response correction, bandpass (0.1–15 Hz), and 4-second causal windows as Set A. |
| **Validation Protocol** | **20-Fold Leave-One-Group-Out (LOGO)** on Set A for model selection; **zero Set C data used in training or tuning**. |
| **Set A CV — RF (Vertical)** | **Accuracy: 97.92%**, **F1: 0.9789**, **ROC-AUC: 0.9994** |
| **Set A CV — XGB (Vertical)** | **Accuracy: 98.33%**, **F1: 0.9832**, **ROC-AUC: 0.9984** |
| **Set C Independent — RF** | **Accuracy: 91.91%**, **F1: 0.9125**, **ROC-AUC: 0.9767**, FP=3, FN=86 |
| **Set C Independent — XGB** | **Accuracy: 92.27%**, **F1: 0.9169**, **ROC-AUC: 0.9780**, FP=4, FN=81 |
| **Set C Independent — STA/LTA (Thresh=8.0)** | **Accuracy: 66.73%**, **F1: 0.5014**, **ROC-AUC: 0.8448**, FP=0, FN=366 |
| **Scientific Findings** | ML models reduced missed P-wave windows vs the ML-4 window-level STA/LTA baseline (`sta_lta_max >= 8.0`, 366 FN) by **77.9% (XGBoost, 81 FN)** and **76.5% (Random Forest, 86 FN)**. This baseline is distinct from the STEP 2K record-level detector (72.9% detected). XGBoost outperformed RF on Set C (F1 +0.0044). Dominant features: `z_spectral_entropy` (#1 in both models; RF Gini=0.1937, XGB Gain=0.3791), `z_spectral_centroid_hz` (#2). Failure modes concentrated on small events (M≤2.66) at large epicentral distances (>70 km): `2020flmsvb` (recall 0.46), `2022gzvhhy` (recall 0.63), `2024ujblmf` (recall 0.69). |
| **Scientific Integrity** | Zero Set C data used in training, model selection, or threshold tuning. 24-feature models (`swiss_rf_model.joblib`, `swiss_xgb_model.joblib`) remain untouched. STEP 2K STA/LTA (threshold 8.0) result preserved frozen. |
| **Files Created** | - `src/models/vertical_models.py`<br>- `scripts/ml/train_vertical_models_set_a.py`<br>- `scripts/analysis/run_swiss_set_c_feature_engineering.py`<br>- `scripts/ml/evaluate_vertical_models_set_c.py`<br>- `reports/ml/vertical_rf_model_set_a.joblib` (frozen)<br>- `reports/ml/vertical_xgb_model_set_a.joblib` (frozen)<br>- `reports/ml/vertical_feature_schema.json`<br>- `reports/ml/vertical_set_a_evaluation_summary.json`<br>- `reports/ml/vertical_set_a_per_event_cv.csv`<br>- `reports/ml/vertical_set_c_evaluation_summary.json`<br>- `reports/ml/vertical_set_c_per_event_results.csv`<br>- `reports/features/swiss_set_c_feature_matrix.csv` (1,100 × 35 columns)<br>- `reports/features/swiss_set_c_feature_summary.json`<br>- Figures: `fig05_vertical_set_c_roc_curves.png`, `fig06_vertical_feature_importance.png`, `fig07_vertical_set_c_confusion_matrices.png`, `fig08_vertical_set_c_per_event_f1.png`<br>- `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md`<br>- `reports/ml/SET_C_VERTICAL_ML_EVALUATION_REPORT.md`<br>- `reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md`<br>- `tests/test_vertical_models.py` (4 tests) |
| **Verification** | **89 / 89 project unit tests passing.** Per-event generalization, model inference, feature schema, and Set C matrix integrity confirmed. |
| **Limitations** | Windowed classifier (4-second windows) not a continuous real-time picker. Set A: N=240 (20 events); Set C: N=1,100 (15 events). Vertical-only features cannot capture particle motion or polarization. |
| **Next Step** | IIT Jodhpur final presentation (13 November 2026). No further model changes required. |

---

Documentation milestone: **1.8.0** (internal; science release remains v1.0.0) (STEP ML-4 Vertical Set C Independent Evaluation complete · 89/89 tests pass · science v1.0.0 & Set C frozen)
