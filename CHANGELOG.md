# Changelog

Project history is maintained in **[docs/CHANGELOG.md](docs/CHANGELOG.md)**.

## Latest

**[Unreleased]** — Research review package (2026-11-15; documentation, figures and website only; no model, dataset or metric changed): `docs/RESEARCH_PACKAGE.md`, `docs/ML_REPRODUCTION_GUIDE.md`, `docs/DATA_AND_MODEL_INVENTORY.md`; 12 final figures in `reports/figures/final/` (`scripts/reporting/make_final_figures.py`); website `/ml-evaluation` page and refreshed dashboard wording (STEP 3A NO-GO shown as historical); `requirements-ml.txt` and `ml` extra for scikit-learn/xgboost/joblib (missing from `requirements.txt`). New disclosure: feature scripts apply a zero-phase bandpass to full traces before windowing. 20 ML-related tests run and passed; full suite not re-run.

**[Unreleased]** — Swiss Set C Vertical-Only Independent Evaluation (2026-11-12, STEP ML-4): 18-feature vertical Random Forest (Set C F1=0.9125, AUC=0.9767) and XGBoost (Set C F1=0.9169, AUC=0.9780) evaluated on N=1,100 independent windows across 15 unseen events, 79 stations (all 54 Set A stations also appear in Set C); missed P-wave windows reduced by 77.9% (XGBoost) / 76.5% (Random Forest) vs the ML-4 window-level STA/LTA baseline (F1=0.5014; distinct from the STEP 2K detector). `sta_lta_*` STA window differs between Set A (0.5 s) and Set C (1.0 s); impact NOT VERIFIED. v1.8.0 is an internal documentation milestone; v1.0.0 remains the frozen submission release. Zero Set C data used in training or tuning. 89/89 tests passing.

**[Unreleased]** — Swiss Set A Supervised ML Training & Benchmarking (2026-11-12, STEP ML-3): Random Forest (F1=0.9916, 100% precision) and XGBoost (F1=0.9832) trained on 240 causal windows with 20-fold Leave-One-Group-Out CV; benchmarked against STA/LTA (F1=0.9386). Zero cross-station event leakage.

**[Unreleased]** — Swiss Set A Causal 3C Feature Extraction (2026-11-12, STEP ML-2): 240 causal window samples (120 P-wave + 120 noise) across 24 response-corrected physical features; QC plots and test suite complete.

**[Unreleased]** — Swiss Set A SED Analyst Pick Acquisition (2026-11-12, STEP ML-1A): 120/120 (100%) manual first-P picks verified and persisted; raw QuakeML provenance saved; supervised ML unblocked.

**[Unreleased]** — Certificate wrap (2026-11-11): AI/ML close-out + 16-slide deck. Still no model trained. Swiss validation and threshold 8.0 frozen.

**[1.4.0]** — Pre-release audit: LICENSE, dependency sync, EarthESND alignment, `CITATION.cff`, `CODE_OF_CONDUCT.md` (2026-08-02).

**[2.0.0]** — Version 2.0 interactive platform (`website/`) complete; documentation sync (2026-08-02).

**[1.3.0]** — **v1.0.0 Submission Release**: FINAL_SUBMISSION package, D-F1–F4, D-S1/S2, validation PASS (2026-07-29).

Git tags: **`v1.0.0`** (science) · **`v2.0.0-website-release`** (platform, suggested). Documentation version: **1.4.0**.

Full history: **[docs/CHANGELOG.md](docs/CHANGELOG.md)**.
