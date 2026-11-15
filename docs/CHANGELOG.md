# CHANGELOG.md

# AMGCR Earthquake Research - Changelog

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog** and follows semantic versioning where practical.

---

## [Unreleased] - Swiss Set C Vertical-Only Independent Evaluation (2026-11-12, STEP ML-4)

### Added

- `src/models/vertical_models.py`: `SwissVerticalRandomForestModel` and `SwissVerticalXGBoostModel` with 18-feature vertical-only schema, LOGO CV runner, and serialization.
- `src/models/__init__.py`: Updated with vertical model exports.
- `scripts/ml/train_vertical_models_set_a.py`: LOGO CV training on Set A with 18-feature vertical schema; freezes both vertical models.
- `scripts/analysis/run_swiss_set_c_feature_engineering.py`: Instrument-response-corrected (m/s) causal vertical 18-feature extraction from Set C HHZ waveforms; includes `st.merge(method=1)` fix for fragmented traces.
- `scripts/ml/evaluate_vertical_models_set_c.py`: Out-of-sample evaluation of frozen vertical models on Set C; generates four figures.
- `reports/ml/vertical_rf_model_set_a.joblib`: Serialized vertical Random Forest model (frozen after training on Set A only).
- `reports/ml/vertical_xgb_model_set_a.joblib`: Serialized vertical XGBoost model (frozen after training on Set A only).
- `reports/ml/vertical_feature_schema.json`: Formal 18-feature vertical schema definition.
- `reports/ml/vertical_set_a_evaluation_summary.json`: Set A LOGO CV results for both vertical models.
- `reports/ml/vertical_set_a_per_event_cv.csv`: Per-event held-out scores (20 events) for Set A training.
- `reports/ml/vertical_set_c_evaluation_summary.json`: Set C independent evaluation metrics for RF, XGBoost, and STA/LTA.
- `reports/ml/vertical_set_c_per_event_results.csv`: Per-event evaluation results on Set C (15 events).
- `reports/features/swiss_set_c_feature_matrix.csv`: 1,100-sample × 35-column ML-ready feature matrix for Set C.
- `reports/features/swiss_set_c_feature_summary.json`: Dataset summary with feature statistics and class distributions.
- Figures in `reports/ml/figures/`:
  - `fig05_vertical_set_c_roc_curves.png`: ROC curves for RF, XGBoost, and STA/LTA on Set C.
  - `fig06_vertical_feature_importance.png`: Top 10 feature importances (Gini vs Gain) for vertical models.
  - `fig07_vertical_set_c_confusion_matrices.png`: Confusion matrices for all three models on Set C.
  - `fig08_vertical_set_c_per_event_f1.png`: Per-event F1 score breakdown across 15 Set C events.
- `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md`: Canonical full evaluation report with Set A vs Set C side-by-side comparison, feature importance analysis, and defense points.
- `reports/ml/SET_C_VERTICAL_ML_EVALUATION_REPORT.md`: Brief summary version.
- `reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md`: Comprehensive cross-dataset benchmark consolidating STEP ML-3 (24-feature Set A CV) and STEP ML-4 (18-feature Set A CV + Set C independent) results.
- `tests/test_vertical_models.py`: Automated pytest suite (4 tests): 18-feature schema integrity, Set C matrix column check, frozen model inference, and Set C evaluation metrics thresholds.

### Key Findings

- **Vertical RF** achieved Set A LOGO CV: Accuracy=97.92%, F1=0.9789, ROC-AUC=0.9994.
- **Vertical XGBoost** achieved Set A LOGO CV: Accuracy=98.33%, F1=0.9832, ROC-AUC=0.9984.
- **On independent Set C (N=1,100, 15 events never seen during training; 79 stations, of which 54 — all Set A stations — also appear in Set A):**
  - XGBoost: Accuracy=92.27%, Precision=0.9915, Recall=0.8527, F1=0.9169, AUC=0.9780 (FP=4, FN=81)
  - Random Forest: Accuracy=91.91%, Precision=0.9936, Recall=0.8436, F1=0.9125, AUC=0.9767 (FP=3, FN=86)
  - STA/LTA (threshold 8.0): Accuracy=66.73%, F1=0.5014, AUC=0.8448 (FP=0, FN=366)
- ML models reduced missed P-wave windows vs the ML-4 window-level STA/LTA baseline (366 FN) by **77.9% (XGBoost, 81 FN)** and **76.5% (Random Forest, 86 FN)**; this baseline is distinct from the STEP 2K record-level detector (72.9% detected).
- Documentation corrections 2026-11-12: `sta_lta_max/mean` use STA 0.5 s (Set A) vs 1.0 s (Set C), impact NOT VERIFIED; threshold 8.0 derives from the Swiss Set A grid (California baseline 2.5), pre-declaration documented but not git-verifiable; v1.8.0 is an internal documentation milestone, v1.0.0 the frozen submission release.
- Dominant features: `z_spectral_entropy` (#1 in both models; RF Gini=0.1937, XGB Gain=0.3791), `z_spectral_centroid_hz` (#2). Together >34% RF importance and >57% XGB gain.
- Failure modes on Set C concentrated on small events (M≤2.66) at large distances (>70 km): `2020flmsvb` (recall 0.46), `2022gzvhhy` (recall 0.63), `2024ujblmf` (recall 0.69).
- 89/89 project unit tests passing after STEP ML-4 additions.
- Original 24-feature models (`swiss_rf_model.joblib`, `swiss_xgb_model.joblib`) and STEP 2K STA/LTA results remain untouched.

---

## [Unreleased] - Swiss Set A Supervised ML Training & Benchmarking (2026-11-12, STEP ML-3)

### Added

- `src/models/random_forest.py`: Reusable `SwissRandomForestModel` with `fit`, `predict`, `predict_proba`, `get_feature_importances`, serialization (`save`/`load`), and Leave-One-Group-Out (LOGO) cross-validation runner.
- `src/models/xgboost_model.py`: Reusable `SwissXGBoostModel` with L1/L2 regularization and identical API.
- `src/models/__init__.py`: Exported model classes and evaluation utilities.
- `scripts/ml/train_random_forest.py`: Standalone script for Random Forest cross-validation and production model fitting.
- `scripts/ml/train_xgboost.py`: Standalone script for XGBoost cross-validation and production model fitting.
- `scripts/ml/evaluate_models.py`: Comprehensive benchmarking script evaluating Random Forest, XGBoost, and the traditional STA/LTA (threshold 8.0) baseline on the same window dataset.
- `reports/ml/swiss_rf_model.joblib`: Serialized production Random Forest model.
- `reports/ml/swiss_xgb_model.joblib`: Serialized production XGBoost model.
- `reports/ml/rf_cross_validation_results.json`: Detailed 20-fold RF LOGO and 5-fold GroupKFold metrics.
- `reports/ml/xgb_cross_validation_results.json`: Detailed 20-fold XGBoost LOGO and 5-fold GroupKFold metrics.
- `reports/ml/swiss_ml_evaluation_summary.json`: Unified comparative benchmark summary.
- `reports/ml/per_event_cross_validation_results.csv`: Per-event held-out test scores across all 20 earthquakes.
- Figures in `reports/ml/figures/`:
  - `fig01_roc_curves.png`: High-resolution ROC curves comparing RF (AUC=0.9990), XGBoost (AUC=0.9990), and STA/LTA (AUC=0.9710).
  - `fig02_feature_importance.png`: Top 10 feature importances (Gini Impurity vs Gain).
  - `fig03_confusion_matrices.png`: Side-by-side confusion matrices.
  - `fig04_per_event_f1.png`: Per-event F1 score distribution across 20 events.
- `docs/ML_RESULTS_REPORT.md` (and `reports/ml/ML_RESULTS_REPORT.md`): Comprehensive formal academic benchmark report.
- `tests/test_ml_models.py`: Automated pytest test suite verifying model fitting, predictions, probability sums, feature importances, artifact deserialization, anti-leakage grouping integrity, and metrics.

### Key Findings

- Random Forest achieved 99.17% accuracy, 100.0% precision (0 false alarms), 98.33% recall (only 2 missed), and 0.9916 F1-score on 20-fold event-grouped cross-validation.
- XGBoost achieved 98.33% accuracy, 99.15% precision, 97.50% recall, and 0.9832 F1-score.
- Random Forest reduced missed detections by 84.6% relative to STA/LTA threshold-8.0 (2 vs 13 false negatives) while eliminating false alarms.
- 18 of 20 independent earthquakes achieved 100% test accuracy under Leave-One-Group-Out CV in Random Forest.

---

## [Unreleased] - Swiss Set A Causal 3C Feature Extraction (2026-11-12, STEP ML-2)

### Added

- `scripts/analysis/run_swiss_set_a_feature_engineering.py`: Instrument-response-corrected (m/s) causal 3C waveform feature extraction script.
- `reports/features/swiss_set_a_feature_matrix.csv`: Complete ML-ready tabular dataset with 240 causal window samples (120 P-wave + 120 ambient noise) and 24 time-domain, frequency-domain, and 3C seismic features.
- `reports/features/swiss_set_a_per_record_features.csv`: Record-level view across all 120 Set A records with SNR and travel-time metrics.
- `reports/features/swiss_set_a_feature_summary.json`: Detailed dataset summary with class distributions, feature definitions, and class means.
- Quality control plots in `reports/features/swiss_figures/`:
  - `fig01_noise_vs_pwave_velocity.png`: Ambient noise vs. early P-wave peak velocity and SNR distributions.
  - `fig02_p_latency_vs_distance.png`: Travel-time curves with theoretical crustal P velocities (6.0–8.0 km/s).
  - `fig03_sta_lta_vs_vh_ratio.png`: Feature space discrimination in STA/LTA vs. V/H ratio.
  - `fig04_energy_vs_frequency.png`: Energy vs. dominant frequency feature discrimination.
- `tests/test_swiss_set_a_features.py`: Automated pytest test suite verifying schema, class balance, causal timestamp bounds, physical units, and verified label matching (all passing).

---

## [Unreleased] - Swiss Set A SED Analyst Pick Acquisition (2026-11-12, STEP ML-1A)

### Added

- `data/manifests/sed_switzerland_set_a_picks.csv`: Canonical manifest of 120 verified same-station manual first-P arrival picks for the 20 Set A events.
- `scripts/download/download_sed_switzerland_set_a_picks.py`: FDSN QuakeML acquisition and verification script.
- `reports/switzerland_set_a_picks/picks_acquisition_summary.json`: Acquisition summary with latency statistics and verification logs.
- `data/metadata/switzerland/{short_id}/quakeml.xml`: Preserved raw QuakeML provenance files for all 20 events.
- `tests/test_switzerland_set_a_picks.py`: Automated pytest test suite verifying schema, 120/120 matches, and timestamp validity.

### Fixed / Resolved

- Resolved the primary ML blocker: supervised machine learning was previously blocked due to lack of independent Set A ground-truth labels. 100% manual analyst coverage achieved without circular detector dependencies.

---

## [Unreleased] - Certificate wrap and AI/ML close-out (2026-11-11)

### Added

- Final AI/ML position for the certificate (no training): `docs/AI_ML_CERTIFICATE_WRAP.md`
- Presentation pack for 13 November 2026:
  - `reports/Certificate_Wrap_Presentation.pptx`
  - `reports/Presentation_Certificate_Wrap_Outline.md`
  - `scripts/presentation/build_certificate_wrap_pptx.py`

### Notes

- Supervised ML remains **NO-GO**. Set C, threshold 8.0, and STEP 2K numbers were not changed.

---

## [Unreleased] - Scientific freeze and ML feasibility audit (2026-09-11)

### Added

- STEP 3A: ML feasibility inspection of existing Set A tables. Decision **NO-GO** (no independent labels, no Swiss feature matrix, no model trained).
  - `docs/SWISS_ML_FEASIBILITY_AUDIT.md`

### Notes

- Consistency audit confirmed STEP 2K headline metrics across CSVs, JSON, and the results markdown.
- Threshold 8.0, Set C, Set A, and California v1.0.0 were not modified.

---

## [Unreleased] - Swiss independent frozen STA/LTA validation (2026-09-11)

### Added

- STEP 2K: evaluated the pre-declared STA/LTA configuration (causal 0.1–15 Hz HHZ, 0.5/10 s, trigger_on **8.0**) on locked Set C.
  - 15/15 events, 550/550 usable records; 401 detections, 149 NO DETECTION
  - `scripts/analysis/run_swiss_independent_validation.py`
  - `src/analysis/switzerland_validation.py`
  - `configs/sed_switzerland_validation.yaml`
  - `docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md`
  - `reports/switzerland_validation/`
  - `tests/test_switzerland_validation.py`

### Notes

- Threshold 8.0 was not retuned and is not claimed to be optimal.
- SED/manual first-P picks are independent references, not ground truth.
- California v1.0.0, Set A, and Set C membership were not modified.
- No ML training and no operational EEW claim.

---

## [Unreleased] - Swiss independent validation acquisition (2026-09-11)

### Added

- STEP 2J: acquired locked Set C MiniSEED and StationXML using origin − 60 s → origin + 90 s.
  - 15/15 events, 550 CH HHZ records, 550 StationXML responses verified per station/channel/interval
  - `scripts/download/download_sed_switzerland_validation.py`
  - `docs/SWISS_VALIDATION_ACQUISITION_REPORT.md`
  - `data/manifests/sed_switzerland_validation_waveforms.csv`
  - `data/manifests/sed_switzerland_validation_picks.csv`

### Notes

- No STA/LTA, no validation metrics, no retuning of threshold 8.0, no Set C reselection.
- California v1.0.0 and the 20-event Swiss development set were not modified.

---

## [Unreleased] - Swiss independent validation design correction (2026-09-11)

### Changed

- STEP 2I.1: distinguished **acquisition** (origin−60 s → origin+90 s), **detection** (origin → origin+90 s), and **pre-event noise/QC** (origin−60 s → origin−10 s) windows.
- Renamed the locked 15-event subset to **Independent Swiss/Adjacent-Border Validation Set** (9/15 immediate-border). Set C IDs were not replaced.
- HH 3C availability is now a **unique CH station-code** count covering the acquisition window.
- StationXML status set to **not yet verified per station** (BALST spot-check is not full coverage).
- Same-station SED first-P ∩ HHZ availability recorded; event-level picks are not treated as a station reference.

### Notes

- No validation MiniSEED download, no STA/LTA on Set C, no metric computation, no retuning of threshold 8.0.
- California v1.0.0 and the 20-event Swiss development set were not modified.

---

## [Unreleased] - Swiss independent validation design (2026-09-11)

### Added

- Independent Swiss validation-set **design/audit** (no MiniSEED download, no STA/LTA on the new events, no retuning of threshold 8.0):
  - `docs/SWISS_INDEPENDENT_VALIDATION_PLAN.md`
  - `data/manifests/sed_switzerland_validation_candidates.csv` (227 independent earthquakes; 15 proposed)
  - `configs/sed_switzerland_validation_audit.yaml`
  - `src/acquisition/switzerland_validation_audit.py`
  - `scripts/audit/audit_swiss_validation_candidates.py`
  - `tests/test_switzerland_validation_audit.py`
  - `reports/switzerland_validation_audit/audit_summary.json`

### Notes

- The 20-event Swiss development set and the frozen California v1.0.0 pipeline were **not** modified.
- Threshold 8.0 remains the pre-declared/proposed value from the development set, reserved for independent validation. It is not claimed to be optimal or already validated.

---

## [Unreleased] - Swiss SED methods-transfer acquisition (2026-09-06)

### Added

- Swiss seismic-data acquisition pipeline (separate from frozen California v1.0.0):
  - `configs/sed_switzerland_pilot.yaml`
  - `src/acquisition/switzerland_pilot.py`
  - `scripts/download/download_sed_switzerland_pilot.py`
  - `data/manifests/sed_switzerland_pilot_events.csv` (20 events, 120 event–station rows)
  - `docs/SED_SWITZERLAND_DATASET_REPORT.md`
  - `tests/test_switzerland_pilot.py`
  - `reports/switzerland_pilot/` acquisition and response-test JSON
- Raw MiniSEED under `data/raw/switzerland/`; StationXML under `data/metadata/switzerland/` (local / gitignored XML).

### Notes

- California IRIS pilot, analysis scripts, reports, figures, and `FINAL_SUBMISSION/` were **not** modified.
- No Swiss STA/LTA, feature engineering, or ML. Not an operational EEW system.

---

## [1.4.0] - Pre-release audit (2026-08-02)

### Added

- **`CITATION.cff`** — repository citation metadata (software v1.0.0).
- **`CODE_OF_CONDUCT.md`** — Contributor Covenant v2.1.

### Fixed

- **LICENSE** — MIT license added (was empty).
- **requirements.txt** — added `PyYAML` and `pytest` for reproducible installs.
- **pyproject.toml** — version aligned to **1.0.0**.
- Removed dev scratch file `tmp_probe.py`; ignore `tmp_*.py`.

### Documentation

- Aligned EarthESND status across README, charter, status, PAPER_REPRODUCTION, REPRODUCIBILITY, and final report: **literature/optional v3.0 track**; **not in v1.0.0 code tree**; **9 acquisition tests**.
- Fixed broken links in `RELEASE_SUMMARY_v1.0.md`.
- Updated `FINAL_DELIVERABLE_AUDIT.md` post-submission sign-off.

---

## [2.0.0] - Version 2.0 interactive platform (documentation sync)

### Added

- **`website/`** — public interactive research platform (Next.js 16, TypeScript, Tailwind v4) at platform version **2.0.0**.
- Nineteen routes: dashboard, workflow, results, dataset, waveforms, map, docs portal, global search, about, contact, and more.
- Release documentation: `docs/V2_RELEASE_NOTES.md`, `V2_DEPLOYMENT_GUIDE.md`, `V2_TEST_REPORT.md`, `V2_KNOWN_LIMITATIONS.md`, `V2_PUBLIC_LAUNCH_CHECKLIST.md`.
- `website/CHANGELOG.md` — platform changelog.

### Documentation

- Synchronized README, AGENTS, PROJECT_STATUS, ROADMAP, PROJECT_CHARTER, PROJECT_GUIDE, AI_AGENT for **v2.0 platform complete**.
- Future work reframed as **Version 2.1** (platform) and **Version 3.0** (science/infrastructure).
- **No changes** to v1.0 analysis scripts, scientific results, or FINAL_SUBMISSION.

### Notes

- Science release remains **`v1.0.0`** (29 July 2026).
- Suggested platform tag: **`v2.0.0-website-release`** or team convention.

---

## [1.3.0] - v1.0.0 Submission Release

### Added

- **FINAL_SUBMISSION/** — PDF/DOCX/PPTX bundle (D-F4), checklists, validation summary (**PASS**).
- **reports/Research_Report_Final.md** (D-F1), presentation outline/script (D-F2/D-F3).
- **docs/REPRODUCIBILITY_STATEMENT.md**, **docs/DATA_AVAILABILITY_STATEMENT.md** (D-S1/S2).
- **RELEASE_SUMMARY_v1.0.md** — submission overview and Version 2.0 roadmap pointer.
- **docs/FINAL_DELIVERABLE_AUDIT.md** — artefact audit (completed).

### Documentation

- Synchronized README, PROJECT_CHARTER, PROJECT_STATUS, ROADMAP, IMPLEMENTATION_PLAN, AI_AGENT, ARCHITECTURE, PROJECT_GUIDE, AGENTS, RESEARCH_DIRECTION, DATASET, FINAL_DELIVERABLE_PLAN, CHANGELOG.
- **Current stage:** v1.0 submission **complete**; **Version 2.0** future work (website, dashboard, Europe, ML, streaming, deployment).
- Documentation-only release relative to v1.0 science freeze; **no changes** to analysis source code or scientific results.

### Notes

- Suggested Git tag: **`v1.0.0`**.

---

## [1.2.0] - Final documentation synchronization

### Documentation

- Synchronized README, PROJECT_STATUS, ROADMAP, PROJECT_CHARTER, RESEARCH_DIRECTION, AI_AGENT, PROJECT_GUIDE, and ARCHITECTURE to **current repository status**.
- Canonical completion: EarthESND reference, California IRIS pilot, EDA, signal analysis, preprocessing, feature engineering, results & discussion, **Research Proposal & Technical Report** (Deliverable 1).
- **Current stage (historical):** Research Proposal v1 complete at 1.2.0; superseded by **v1.0.0 Submission Release** in 1.3.0.

### Notes

- Documentation-only release; no changes to source code, tests, scripts, or YAML.

---

## [1.1.0] - Phase A California pilot analysis

### Added

- **Phase A.1** — `scripts/analysis/run_california_pilot_eda.py`: MiniSEED inspection, dataset summary, EDA figures and tables under `reports/`.
- **Phase A.2** — `scripts/analysis/run_california_signal_analysis.py`: amplitude metrics, noise/SNR, ObsPy STA/LTA P picks, per-event signal figures.

### Documentation

- Added **docs/EDA_REPORT.md** and **docs/SIGNAL_ANALYSIS_REPORT.md**.
- Updated PROJECT_STATUS, ROADMAP, IMPLEMENTATION_PLAN, PROJECT_CHARTER, ARCHITECTURE, README, AI_AGENT, PROJECT_GUIDE, and DATASET for Phase A completion and Phase B / proposal next steps.

---

## [1.0.0] - Research charter and documentation refactor

### Documentation

- Established **docs/PROJECT_CHARTER.md** as the authoritative project definition (Swiss certificate EEW research; Europe focus, USA experimental data).
- Added **docs/RESEARCH_DIRECTION.md** explaining the pivot from EarthESND paper reproduction to Western-region active research.
- Synchronised README, PROJECT_STATUS, ROADMAP, ARCHITECTURE, PAPER_REPRODUCTION, IMPLEMENTATION_PLAN, AI_AGENT, and PROJECT_GUIDE with Phases A–D roadmap and professor requirements.
- Clarified EarthESND **literature track documented** vs **executable pipeline not in v1.0.0**; USA IRIS/California pilot documented as active workflow.

### Notes

- No Python source, tests, or YAML configuration values were changed in this release.

---

## [0.3.0] - Phase 2B Catalogue Retrieval

### Added

- Implemented configuration-driven event catalogue retrieval with ObsPy.
- Added provider-aware query shaping so the retrieval workflow works with the USGS event service.
- Verified a sample catalogue retrieval and saved a QuakeML file to data/raw/catalogs/catalog.xml.
- Added regression tests for provider resolution and query construction.

### Documentation

- Updated the project status, implementation plan, dataset notes, experiment log, roadmap, and README to reflect the completed acquisition milestone.

---

## [0.2.0] - Phase 2A Acquisition Framework Preparation

### Added

- Created a modular acquisition package under src/acquisition.
- Added catalog, waveform, station, and download manager modules with documentation and placeholder logic.
- Implemented a YAML-based configuration loader for future acquisition workflows.
- Added default acquisition configuration in configs/acquisition_config.yaml.
- Added validators and custom exceptions for configuration-driven acquisition.
- Added unit tests covering configuration loading and validation.

### Documentation

- Updated project status and implementation notes for the acquisition preparation phase.

---

## [0.1.0] - Phase 1 Initialization

### Added

- Repository structure reorganised to support research and development work.
- Virtual environment created and validated.
- Core dependencies installed and verified for ObsPy, NumPy, Pandas, Matplotlib, SciPy, and PyYAML.
- Initial package scaffold created inside src/.
- Logging configuration and project settings added.
- Initial import verification test added.

### Documentation

- Updated project status and implementation notes.
- Added project decision log entries for the initialization phase.

---

## Changelog Guidelines

Record only meaningful project changes.

Include:

- New features
- Bug fixes
- Documentation updates
- Refactoring
- Research milestones

Avoid logging trivial edits such as spelling corrections unless they materially improve documentation.

---

Current Version: **1.4.0** (science **v1.0.0** · platform **v2.0.0**)
