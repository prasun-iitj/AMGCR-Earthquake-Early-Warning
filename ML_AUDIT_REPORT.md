# AMGCR Earthquake Research — ML Feasibility Audit Report
**Date:** 2026-11-12  
**Type:** Read-only repository audit  
**Purpose:** Assess feasibility of implementing Random Forest, XGBoost, and 1D CNN for earthquake detection, with comparative evaluation against the existing STA/LTA baseline.

> [!IMPORTANT]
> This is a **read-only audit**. No files were modified, no code was written, no packages were installed, no experiments were run, and no datasets were downloaded during this audit.

---

## A. Existing Project Architecture

### Repository Layout
```
AMGCR_Earthquake_Research/
├── configs/           # 8 YAML config files (acquisition, signal analysis, STA/LTA, validation)
├── data/
│   ├── manifests/     # 5 CSV files — event catalogs, picks, waveform manifests
│   ├── raw/iris/      # 74 California MiniSEED files (8 events × ~9 stations)
│   ├── raw/switzerland/           # 120 Swiss Set A MiniSEED (20 events, HH 3C)
│   ├── raw/switzerland_validation/# 550 Swiss Set C MiniSEED (15 events, HHZ)
│   └── metadata/      # StationXML for Set A (121 files) and Set C (551 files)
├── docs/              # 46 Markdown documents (reports, status, roadmap, audit)
├── reports/
│   ├── features/      # California feature_matrix.csv (8 × 18), feature_summary.json
│   ├── swiss_signal_analysis/     # Swiss Set A STA/LTA sensitivity, trace metrics
│   │   └── sta_lta_transfer/      # threshold_sensitivity.csv, record_trigger_grid.csv
│   ├── switzerland_validation/    # Set C frozen STA/LTA results
│   └── tables/        # 6 CSV tables (preprocessing, signal analysis, event/station summaries)
├── scripts/
│   ├── analysis/      # 7 Python scripts (California + Swiss analysis pipelines)
│   ├── audit/         # 1 script (Swiss validation candidate audit)
│   └── download/      # 3 scripts (IRIS + SED acquisition)
├── src/
│   ├── acquisition/   # 11 Python modules (FDSN download, SED client, validation)
│   ├── analysis/      # 3 Python modules (Swiss signal, STA/LTA transfer, validation)
│   ├── models/        # __init__.py ONLY — empty stub, no model code
│   ├── preprocessing/ # __init__.py only — empty stub
│   └── utils/         # logging_utils.py
├── tests/             # 10 test files (all acquisition/analysis, no ML tests)
├── notebooks/         # EMPTY — zero notebooks
├── FINAL_SUBMISSION/  # Frozen v1.0 submission package (14 files)
└── website/           # Next.js interactive research platform (27 pages)
```

### Scientific Pipeline (Completed)
```
California Pilot (v1.0 — FROZEN)
  ↓ ObsPy FDSN download (8 events, 74 MiniSEED)
  ↓ EDA → Signal Analysis → Preprocessing → Feature Engineering
  ↓ feature_matrix.csv (8 × 18 features, counts-based)
  ↓ Results & Discussion → Final Report → Submission (PASS)

Swiss Methods Transfer (v3.0 partial — FROZEN)
  ↓ SED FDSN download: Set A (20 events, 120 MiniSEED HH 3C)
  ↓ Swiss Signal Analysis → STA/LTA Transfer (threshold sweep 2.5–10.0)
  ↓ Threshold 8.0 proposed (92.5% detection, 10% noise rate on Set A)

Swiss Independent Validation (STEP 2K — FROZEN)
  ↓ SED FDSN download: Set C (15 events, 550 MiniSEED HHZ)
  ↓ Frozen STA/LTA evaluation: threshold 8.0, pre-declared, NOT retuned
  ↓ Results: 72.9% detection rate, 1.24 s median timing error
```

### Tech Stack
- **Language:** Python 3.11+ (virtual environment `.venv/`)
- **Seismology:** ObsPy 1.5.0, SciPy 1.18.0, NumPy 2.5.1
- **Data:** Pandas 3.0.5, PyYAML 6.0
- **Visualization:** Matplotlib 3.11.1
- **ML libraries installed:** ❌ **None** — no scikit-learn, XGBoost, TensorFlow, PyTorch, or Keras in `requirements.txt` or `pyproject.toml`
- **Git branch:** `main` (20 unstaged modified files, mostly website/docs)
- **Notable branches:** `feature/phase6-training-evaluation` (exists but not inspected; may contain prior ML planning)

---

## B. Available Datasets and Their Composition

### Dataset 1 — California Pilot (Set USA)
| Property | Value |
|---|---|
| Events | 8 earthquakes (California, Oct 2024 – Aug 2024) |
| MiniSEED files | 74 (across 2 stations: CI.ADO, CI.USC) |
| Channels | BHZ (40 Hz sampling rate) |
| Networks | CI (Southern CA), NC (Northern CA), NN (Nevada) |
| Magnitude range | M 4.05 – M 4.87 (all Mw or ML) |
| Depth range | 3.98 – 13.16 km |
| Acquisition window | ~300 s per record |
| Feature matrix | 8 rows × 18 features (counts-based, no response correction) |
| P-pick source | `phase_a2_metrics` — STA/LTA derived (NOT independent analyst picks) |
| Status | ✅ **FROZEN** — do not re-run |

### Dataset 2 — Swiss Set A (Methods Transfer / Development Set)
| Property | Value |
|---|---|
| Events | 20 Swiss earthquakes |
| MiniSEED files | 120 (3-component HH per station) |
| Channels | HHZ + HHN + HHE (complete 3C) |
| Sampling rates | 200 Hz (108 records), 120 Hz (12 records) |
| Acquisition window | origin−90 s → origin+210 s (300 s total) |
| Unique stations | 54 CH network stations |
| Magnitude types | MLh / MLhc (SED) |
| Feature matrix | ❌ **None** — no Swiss feature matrix exists |
| Independent P picks | ❌ **None for Set A** |
| STA/LTA results | Threshold sensitivity sweep (2.5–10.0); threshold 8.0 proposed |
| Status | ✅ Acquisition & signal analysis frozen; **no ML use** |

### Dataset 3 — Swiss Set C (Independent Validation Set — LOCKED)
| Property | Value |
|---|---|
| Events | 15 locked events (9 adjacent-border, 6 Swiss territory) |
| MiniSEED files | 550 (HHZ only) |
| Sampling rates | HHZ |
| Acquisition window | origin−60 s → origin+90 s (150 s total) |
| Independent P picks | ✅ **YES** — SED manual analyst picks for all records with match |
| Pick file | `data/manifests/sed_switzerland_validation_picks.csv` (96 KB) |
| Pick phases | P1, Pg, Pn (manual evaluation, SED QuakeML) |
| Frozen STA/LTA results | 72.9% detection, 1.24 s timing error (threshold 8.0, pre-declared) |
| Status | ✅ **LOCKED** — must NOT be used for model training or tuning |

### Dataset Composition Summary
| Dataset | Events | Records | Features | Independent Labels | ML Use |
|---|---|---|---|---|---|
| California (Set USA) | 8 | 74 | 18 (counts) | ❌ STA/LTA-derived | ❌ Too small; circular picks |
| Swiss Set A | 20 | 120 | ❌ None | ❌ None | ❌ No labels |
| Swiss Set C | 15 | 550 | ❌ None | ✅ Manual SED picks | ❌ LOCKED (validation only) |

---

## C. Availability and Quality of Training Labels

> [!CAUTION]
> **No scientifically valid training labels currently exist for any ML experiment in this project.**

### Label Inventory

| Label Source | Dataset | Available? | Valid for ML Training? | Reason |
|---|---|---|---|---|
| STA/LTA trigger detections (California) | Set USA | ✅ Yes | ❌ **NO** | Circular — P picks were derived from STA/LTA at threshold 2.5; labels would encode the detector, not physics |
| STA/LTA trigger outcomes (Swiss Set A) | Set A | ✅ Yes | ❌ **NO** | Circular — training labels cannot come from the same STA/LTA being replaced; also zero noise-class events |
| SED manual first-P picks (Swiss Set C) | Set C | ✅ Yes | ❌ **LOCKED** | Set C is the independent validation set; using it for training invalidates the validation |
| Independent SED picks for Swiss Set A | Set A | ❌ **Missing** | — | This is the **only blocker** for ML training |

### What Exists in `sed_switzerland_validation_picks.csv`
- 550 records with columns: `short_id, origin_time, network, station, channel, pick_phase, pick_time_utc, pick_evaluation_mode (manual), pick_source (SED QuakeML), same_station_pick_status (manual_ch_first_p)`
- These are reference picks for **Set C only** — used as comparison targets in validation, NOT as training labels
- The `validation_trace_metrics.csv` has computed columns: `has_usable_same_station_p`, `reference_p_time_utc`, `trigger_minus_p_s`, `trigger_at_or_after_p` — these are evaluation metrics, not training labels

### Critical: What "Circular" Means Here
California P picks (`p_pick_source: phase_a2_metrics`) were derived by running STA/LTA at threshold 2.5 and taking the first trigger. Training a Random Forest or CNN to predict those picks would just teach the model to replicate a simple threshold detector. This is scientifically invalid as a "machine learning improvement."

---

## D. Existing ML-Ready Features

### California `feature_matrix.csv` (8 × 18)
```
Columns:
  peak_amplitude, peak_to_peak_amplitude, rms, variance, std,
  zero_crossing_rate_hz, signal_energy, signal_entropy, crest_factor,
  dominant_frequency_hz, spectral_centroid_hz, spectral_bandwidth_hz,
  spectral_rolloff_95_hz, spectral_entropy,
  p_arrival_time_s, signal_duration_s, pgm_proxy_counts, arias_intensity_counts2_s_proxy

Units: Raw counts (no instrument response removal)
Sampling rate: 40.0 Hz (all 8 records)
Stations: CI.ADO.--.BHZ (6), CI.USC.--.BHZ (2)
```

**Assessment for ML:**
- **N=8 is far too small** for any supervised ML — this is exploratory research data only
- **Features are in counts**, not physical units (m/s or m/s²) — cross-station/event comparisons are limited
- **No noise class** — all 8 records are confirmed earthquakes; no non-event examples for binary classification
- **P-picks are STA/LTA-derived** — cannot be used as training labels for event detection

### Swiss Feature Matrix
- ❌ **Does not exist** — Set A has only STA/LTA sensitivity tables and signal analysis metrics
- The `swiss_trace_metrics.csv` in `reports/swiss_signal_analysis/` contains waveform diagnostic columns, not ML-ready earthquake detection features
- No feature extraction script has been run on Swiss waveforms

### Conclusion
**No ML-ready feature dataset currently exists** that is both (a) large enough and (b) paired with valid independent labels.

---

## E. Feasibility of Random Forest, XGBoost, and 1D CNN

### E.1 Random Forest
| Criterion | Status | Notes |
|---|---|---|
| Tabular features available | ⚠️ Partial | California: 8 × 18 (too small); Swiss: none |
| Valid training labels | ❌ Missing | Set C locked; Set A has no picks |
| Minimum viable N | ~500–1000 samples | Currently: 8 (CA) or 0 (Swiss) |
| **Feasibility now** | ❌ **NOT FEASIBLE** | Missing labels + insufficient N |
| **Feasibility with SED Set A picks** | ✅ **Conditionally feasible** | Need to extract features from 120 Set A records + obtain SED picks; N=120 is marginal but defensible for a research prototype |

### E.2 XGBoost
| Criterion | Status | Notes |
|---|---|---|
| Tabular features available | ⚠️ Same as RF | Same constraints |
| Valid training labels | ❌ Missing | Same constraints |
| Gradient boosting benefit | ✅ Yes (once data exists) | Better than RF on small-N tabular with cross-validation |
| **Feasibility now** | ❌ **NOT FEASIBLE** | Same as RF |
| **Feasibility with SED Set A picks** | ✅ **Conditionally feasible** | Preferred over RF for N=120 (regularization, feature importance) |

### E.3 1D CNN (Waveform-based)
| Criterion | Status | Notes |
|---|---|---|
| Raw waveforms available | ✅ Yes | 120 Set A MiniSEED (HH 3C) + 550 Set C (HHZ) |
| Valid training labels | ❌ Missing | Set A has no picks; Set C is locked |
| Minimum viable N | ~1000–10,000 samples | Currently: 120 Set A (not labeled) |
| Architecture complexity | High | Requires windowed samples, normalization, response correction |
| **Feasibility now** | ❌ **NOT FEASIBLE** | Missing labels; Set C cannot be used for training |
| **Feasibility with SED Set A picks** | ⚠️ **Marginal** | 120 labeled records is below standard CNN training threshold; would need aggressive augmentation; scientifically cautious interpretation required |

### E.4 Comparative Evaluation vs STA/LTA Baseline
| Scenario | Feasibility |
|---|---|
| Compare RF/XGBoost vs STA/LTA on a held-out test set | ✅ Feasible once training labels for Set A exist; use Set C as the final test benchmark |
| Compare 1D CNN vs STA/LTA | ⚠️ Marginal — only if Set A N=120 is augmented significantly |
| Claim improvement over STA/LTA baseline | Only valid if models are trained on Set A (with independent labels) and evaluated on locked Set C |

---

## F. Required Additional Data or Annotations

### F.1 Minimum Required to Unblock ML (Critical Path)
| Item | Description | Priority |
|---|---|---|
| **SED analyst P picks for Set A** | Official first-P wave arrival times from SED QuakeML catalog for 20 Set A events, same format as `sed_switzerland_validation_picks.csv` | 🔴 **Critical — only blocker** |

### F.2 Required to Build ML Features
| Item | Description |
|---|---|
| Feature extraction script for Swiss Set A | Apply the existing California feature engineering pipeline (`run_california_feature_engineering.py`) adapted for HH 3C Swiss waveforms |
| Response-corrected amplitudes | The California features are in counts. For Swiss ML, instrument response correction (via StationXML) should be applied to get physical units (m/s or m/s²) for cross-station comparability |
| Noise class samples | The California and Set A data contain only confirmed earthquakes. For binary event/no-event classification, noise windows (ambient noise or non-seismic recordings) are needed |

### F.3 Optional Improvements (for stronger science)
| Item | Benefit |
|---|---|
| Additional Swiss events (Set B pool: 227 candidates) | Increases training N significantly; would require the same SED analyst picks |
| 3C features (HHN, HHE in addition to HHZ) | More informative for CNN; available for Set A but not Set C |
| Augmented waveform windows | Slide/rotate windows for CNN training data augmentation |
| Cross-validation strategy | Mandatory for N~120 (leave-one-event-out or stratified k-fold by magnitude) |

---

## G. Recommended Scientific ML Implementation Strategy

> [!NOTE]
> This strategy is designed to be scientifically rigorous, reproducible, and consistent with the project's academic context. It follows the same evidence-based approach established in the California v1.0 work.

### Guiding Principles
1. **Never retrain on Set C** — it remains the independent final evaluation benchmark
2. **Never use STA/LTA detections as ground truth labels** — labels must be independent analyst picks
3. **Document everything** — every design decision, N count, limitation, and metric
4. **Distinguish training from claiming** — a model trained on N=120 is a research prototype, not a production EEW system
5. **STA/LTA remains the baseline** — all ML results are reported relative to threshold 8.0 on Set C

### Recommended Pipeline

```
STEP ML-1: Acquire SED analyst picks for Set A (20 events)
  → Download QuakeML with includearrivals from SED FDSN for Set A event IDs
  → Extract first-P picks, same format as sed_switzerland_validation_picks.csv
  → Save to data/manifests/sed_switzerland_set_a_picks.csv
  → Audit: how many of 120 records have same-station first-P picks?

STEP ML-2: Extract Swiss Set A features
  → Adapt California feature engineering pipeline for HH 3C, 200 Hz
  → Apply instrument response correction (StationXML available for all 120 records)
  → Use pre-origin window for noise features; post-origin for signal features
  → Label each record: pick_time_utc (from Step ML-1) OR NO_PICK
  → Save to reports/features/swiss_set_a_feature_matrix.csv

STEP ML-3: Define ML problem
  → Binary classification: Event detected before 10 s after P (yes/no)
    OR regression: predict latency (trigger_time − reference_P_time_s)
  → Split: Train on Set A (labeled records) / Evaluate on locked Set C
  → Cross-validation within Set A: leave-one-event-out (guards against event leakage)

STEP ML-4: Implement Random Forest baseline
  → scikit-learn RandomForestClassifier, n_estimators=200
  → Feature importance report
  → Cross-validated AUC on Set A

STEP ML-5: Implement XGBoost
  → xgboost XGBClassifier, early stopping on validation fold
  → SHAP feature importance
  → Cross-validated AUC on Set A

STEP ML-6: Implement 1D CNN (optional / conditional)
  → Only if N≥100 labeled records available after Step ML-1 audit
  → Input: 5-second HHZ window centered on STA/LTA trigger
  → Architecture: 3–4 Conv1D blocks → GlobalAvgPool → Dense(1)
  → Training: Set A (augmented); evaluation: Set C

STEP ML-7: Final comparative evaluation on locked Set C
  → Apply trained models to Set C (inference only, no retraining)
  → Compare vs STA/LTA baseline (threshold 8.0, STEP 2K)
  → Metrics: detection rate, false trigger rate, median timing error
  → Document: N_train, N_test, model architecture, all metrics

STEP ML-8: Documentation and report
  → Update PROJECT_STATUS.md, ROADMAP.md, CHANGELOG.md
  → Write ML_RESULTS_REPORT.md
  → Update website dashboard and results explorer
```

### Data Leakage Risks Identified
| Risk | Mitigation |
|---|---|
| Using STA/LTA detections as labels (circular) | Use only independent SED analyst picks |
| Training on Set C records | Set C is used ONLY for final evaluation |
| Event-level leakage in cross-validation | Use leave-one-event-out (not random k-fold on records) |
| Threshold tuning after seeing Set C results | All Set C evaluation is one-shot with pre-declared model |
| Feature computed on full waveform (including post-trigger) | Use only pre-trigger + early post-origin window (causal features) |

---

## H. Estimated Implementation Steps

### Prerequisites (must be completed before coding)
| # | Task | Effort |
|---|---|---|
| H-0 | Install ML libraries: `pip install scikit-learn xgboost shap` | 10 min |
| H-1 | Acquire SED analyst picks for Set A 20 events (STEP ML-1) | 1–2 days |
| H-2 | Audit: count records with valid same-station first-P picks in Set A | 2 hours |

### Implementation Steps (contingent on H-1 success)

| Step | Task | Estimated Effort | Output |
|---|---|---|---|
| **1** | Write Swiss Set A feature extraction script (adapted from California pipeline) | 1–2 days | `scripts/analysis/run_swiss_set_a_feature_engineering.py` |
| **2** | Generate `swiss_set_a_feature_matrix.csv` with valid labels | 2–4 hours | `reports/features/swiss_set_a_feature_matrix.csv` |
| **3** | Implement Random Forest model training + cross-validation | 1 day | `src/models/random_forest.py`, `scripts/ml/train_random_forest.py` |
| **4** | Implement XGBoost model training + SHAP analysis | 1 day | `src/models/xgboost_model.py`, `scripts/ml/train_xgboost.py` |
| **5** | Final evaluation of RF + XGBoost on locked Set C | 2–4 hours | `reports/ml/comparative_evaluation.csv` |
| **6** | Write ML Results Report | 1 day | `docs/ML_RESULTS_REPORT.md` |
| **7** | (Optional) 1D CNN if N≥100 — only after tabular models are done | 2–3 days | `src/models/cnn_1d.py`, `scripts/ml/train_cnn.py` |
| **8** | Update PROJECT_STATUS, ROADMAP, CHANGELOG, website | 2–4 hours | Docs + website sync |

**Total estimated effort (RF + XGBoost only, without CNN):** ~5–7 days of active development  
**Prerequisite (SED picks for Set A):** Outside direct control — requires SED/FDSN query to return analyst picks for 20 events

### Decision Tree
```
Can we query SED FDSN for Set A analyst picks?
  ├─ YES → How many of 120 records have same-station first-P picks?
  │         ├─ ≥60 records → Proceed with RF + XGBoost (tabular ML)
  │         ├─ ≥100 records → Also attempt 1D CNN
  │         └─ <60 records → Document as insufficient; prototype only with caveats
  └─ NO  → ML remains BLOCKED; document and update PROJECT_STATUS
                Options: request picks manually from SED, or use public SeisComP catalogs
```

---

## Audit Conclusions

| Question | Finding |
|---|---|
| Has any ML model been trained? | ❌ No — `src/models/` is an empty stub |
| Are ML libraries installed? | ❌ No — scikit-learn, XGBoost, PyTorch absent from requirements |
| Are valid training labels available? | ❌ No — Set C is locked; Set A has no independent picks |
| Is ML feasible right now? | ❌ Blocked — single blocker is SED analyst picks for Set A |
| Is ML feasible after acquiring picks? | ✅ Yes — RF and XGBoost are conditionally feasible at N~120 |
| Is 1D CNN feasible? | ⚠️ Marginal — N~120 is very small; feasible only with strong caveats |
| What is the STA/LTA baseline? | threshold 8.0, Set C: 72.9% detection, 1.24 s timing, 12.5% noise rate |
| Are there data leakage risks? | Yes — circular labels (STA/LTA as targets) and Set C contamination; both mitigated by strategy above |
| Are frozen results safe? | ✅ Yes — no frozen artefacts were modified in this audit |

---

*Audit prepared by: Antigravity AI Agent (read-only inspection)*  
*Repository: `c:\Users\prasun.tripathi\Desktop\MY\AMGCR_Earthquake_Research`*  
*Git branch: `main` | Last commit: `6480fa6` (docs: record scientific freeze and ML feasibility NO-GO)*
