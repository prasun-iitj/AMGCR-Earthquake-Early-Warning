# Data and Model Inventory

> **Data lineage and availability (added 2026-11-15).** Counts below are verified by `scripts/reporting/audit_data_lineage.py` (`reports/data_lineage/data_lineage_summary.json`). Narrative: [DATA_COLLECTION_AND_ANALYSIS_REPORT.md](DATA_COLLECTION_AND_ANALYSIS_REPORT.md). Columns and features: [DATA_DICTIONARY.md](DATA_DICTIONARY.md). Commands: [DATA_ACQUISITION_AND_REPRODUCTION.md](DATA_ACQUISITION_AND_REPRODUCTION.md).
>
> | Dataset | Provider | Events | Records | Stations | Channels | Picks | Raw files local | Raw files on GitHub | How to obtain |
> |---|---|---|---|---|---|---|---|---|---|
> | California pilot | USGS + EarthScope | 8 | 8 listed (12 files locally) | 2 | CI BHZ | none (STA/LTA triggers) | yes, `data/raw/iris/` | no | `download_iris_california_pilot.py` |
> | Swiss Set A | SED/ETH | 20 | 120 | 54 | CH HHZ/HHN/HHE | 120 manual | yes, 120 `.mseed` + 140 XML | no | `download_sed_switzerland_pilot.py`, `..._set_a_picks.py` |
> | Swiss Set C | SED/ETH | 15 | 550 | 79 | CH HHZ | 550 manual | yes, 550 `.mseed` + 550 XML | no | `download_sed_switzerland_validation.py` |
>
> Classes: **A** raw data present locally: all of the above. **B** local but excluded from GitHub: all raw MiniSEED, StationXML, QuakeML (`.gitignore`). **C** published: manifests, feature matrices, models, results, scripts, figures, documents. **D** external only: the provider archives. **E** reconstructable by script: all raw data via the download scripts (licence terms not reviewed). Event overlap Set A / Set C: 0. Station overlap: all 54 Set A stations also occur in Set C (25 Set C only).
>
> Lineage: provider endpoint -> download script -> raw file + manifest row -> feature script -> feature-matrix row -> saved models -> `reports/ml/*.json`. Derived files that exist only locally: none in `data/interim` or `data/processed` (both empty); processed signals are computed in memory by the feature scripts.

Paths are relative to the repository root. "Published" means committed to the GitHub repository. Sizes are from the working copy on 12 Nov 2026.

## 1. Waveform data (not published)

| Path | Content | Files / size | Published | Obtain with |
|---|---|---|---|---|
| `data/raw/iris/` | California pilot MiniSEED (IRIS/EarthScope) | 12 files | No (`data/raw/` git-ignored) | `scripts/download/download_iris_california_pilot.py` |
| `data/raw/switzerland/` | Swiss Set A MiniSEED, 20 events | 120 `.mseed` | No | `scripts/download/download_sed_switzerland_pilot.py` |
| `data/raw/switzerland_validation/` | Swiss Set C MiniSEED, 15 events | 550 `.mseed` | No | `scripts/download/download_sed_switzerland_validation.py` |
| `data/metadata/**` | StationXML and QuakeML per event | about 32 MB | StationXML/QuakeML `.xml` git-ignored | same download scripts |

All sources are public FDSN services (IRIS/EarthScope; SED/ETH via `eida.ethz.ch`). No credentials are needed. Redistribution terms of the data providers were not reviewed for this package, so raw waveforms are deliberately not committed. See [DATA_AVAILABILITY_STATEMENT.md](DATA_AVAILABILITY_STATEMENT.md).

## 2. Manifests (published)

| Path | Rows | Content |
|---|---|---|
| `data/manifests/iris_california_pilot_events.csv` | California events | v1.0.0 pilot manifest |
| `data/manifests/sed_switzerland_pilot_events.csv` | 120 | Set A records |
| `data/manifests/sed_switzerland_set_a_picks.csv` | 120 | SED manual first-P picks, Set A |
| `data/manifests/sed_switzerland_validation_candidates.csv` | 227 | Set C candidate pool and selection |
| `data/manifests/sed_switzerland_validation_waveforms.csv` | 550 | Set C records |
| `data/manifests/sed_switzerland_validation_picks.csv` | 550 | Same-station SED first-P picks, Set C |

## 3. Feature matrices (published, small)

| Path | Shape | Used for |
|---|---|---|
| `reports/features/feature_matrix.csv` | 8 x 18 | California v1.0.0 (frozen) |
| `reports/features/swiss_set_a_feature_matrix.csv` | 240 x 45 | Set A training and CV (24 features plus metadata) |
| `reports/features/swiss_set_a_per_record_features.csv` | 120 x 21 | Per-record Set A descriptors |
| `reports/features/swiss_set_c_feature_matrix.csv` | 1,100 x 35 | Set C evaluation (18 features plus metadata) |
| `reports/features/swiss_set_{a,c}_feature_summary.json` | | Extraction summaries |

## 4. Models (published, under 230 KB each, no Git LFS needed)

| Path | Features | Trained on | Status |
|---|---|---|---|
| `reports/ml/swiss_rf_model.joblib` | 24 (3C) | Set A | Frozen (STEP ML-3) |
| `reports/ml/swiss_xgb_model.joblib` | 24 (3C) | Set A | Frozen (STEP ML-3) |
| `reports/ml/vertical_rf_model_set_a.joblib` | 18 (vertical) | Set A | Frozen (STEP ML-4) |
| `reports/ml/vertical_xgb_model_set_a.joblib` | 18 (vertical) | Set A | Frozen (STEP ML-4) |

Joblib files are Python pickles; load only trusted files with the library versions in `requirements-ml.txt`. The 24-feature models cannot be applied to Set C (HHZ only).

## 5. Results and reports

| Path | Content |
|---|---|
| `reports/ml/vertical_set_c_evaluation_summary.json` | Set C metrics, confusion counts, feature importances |
| `reports/ml/vertical_set_a_evaluation_summary.json` | Set A LOGO CV (18 features) |
| `reports/ml/swiss_ml_evaluation_summary.json` | Set A LOGO CV (24 features, STEP ML-3) |
| `reports/ml/vertical_feature_schema.json` | Exact 18-feature names and order |
| `reports/ml/vertical_set_c_per_event_results.csv` | 15 events: accuracy, precision, recall, F1 for RF, XGB, STA/LTA |
| `reports/ml/vertical_set_a_per_event_cv.csv` | 20 held-out events |
| `reports/ml/figures/fig01` to `fig08` | Original ML figures |
| `reports/figures/final/fig01` to `fig12` | Final research figures (about 1.3 MB) |
| `reports/switzerland_validation/validation_summary.json` | STEP 2K record-level validation (401/550) |
| `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md`, `reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md` | STEP ML-4 reports |
| `docs/RESEARCH_PACKAGE.md`, `docs/ML_REPRODUCTION_GUIDE.md`, this file, `FINAL_INTEGRITY_CHECK.md` | Review package |

## 6. Code

| Path | Role |
|---|---|
| `scripts/download/` | Data acquisition (IRIS, SED waveforms, SED picks) |
| `scripts/analysis/run_swiss_set_{a,c}_feature_engineering.py` | Window cutting, response removal, feature extraction |
| `src/models/{random_forest,xgboost_model,vertical_models}.py` | Model classes and LOGO evaluation |
| `scripts/ml/` | Training and evaluation entry points |
| `scripts/reporting/make_final_figures.py` | Final figures from saved results |
| `tests/` | pytest suite; ML-related files: `test_ml_models.py`, `test_vertical_models.py`, `test_swiss_set_a_features.py`, `test_switzerland_set_a_picks.py` |
| `website/` | Next.js research website (reads the files above at build time) |

## 7. Publication exclusions

- `data/raw/`, `data/interim/`, `data/processed/`, `data/output/`, StationXML/QuakeML: size and data-provider terms.
- `logs/`, `.venv/`, `website/node_modules/`, `website/.next/`, `.pytest_cache/`: local or generated.
- `website/public/{figures,tables,datasets,waveforms,final-figures,ml-downloads}`: regenerated by `npm run build`.
- `.env*`: none are committed; the repository contains no credentials (the FDSN endpoints used are public).
