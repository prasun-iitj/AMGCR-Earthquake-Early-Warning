# Professor Handover Guide

Start here. This guide lets a reviewer find what was done, why, where the evidence is, and what is still open. It links to existing documents instead of repeating them.

**Scope.** The ML work is an **offline P-wave versus ambient-noise window-classification research benchmark**. It is not an operational real-time early-warning system and not earthquake prediction.

**State reviewed.** Repository `main` after commit `6d5b505`, plus the handover commit. Verified counts: [reports/data_lineage/data_lineage_summary.json](../../reports/data_lineage/data_lineage_summary.json). Results: saved JSON in [reports/ml/](../../reports/ml/).

## 1. Project in one page

| Item | Content |
|---|---|
| Title | AMGCR Earthquake Research: reproducible, AI-assisted earthquake early-warning (EEW) research for Western seismic regions |
| Context | Swiss certificate programme research project ([PROJECT_CHARTER.md](../PROJECT_CHARTER.md)) |
| Objective | Build a reproducible workflow from raw waveforms to labelled windows and features, then test whether supervised classifiers trained on Swiss events can recognise P-wave windows in other Swiss events, compared with an STA/LTA threshold rule |
| Motivation | Europe is the long-term focus; the professor's requirements asked for ObsPy, IRIS/EarthScope for USA events, real datasets, waveform analysis, tables and figures ([charter section 4](../PROJECT_CHARTER.md)) |
| Methodology | Acquire public FDSN data, correct instrument response, cut 4 s windows around SED analyst P picks and pre-origin noise, compute features, train Random Forest and XGBoost with event-grouped cross-validation, evaluate frozen models on a separate event set |
| Main result | On 15 unseen events (1,100 windows): XGBoost F1 0.9169, Random Forest F1 0.9125, window-level STA/LTA baseline F1 0.5014 ([results](../SET_C_VERTICAL_ML_EVALUATION_REPORT.md)) |
| Main caveats | Small development set; events independent but stations shared; preprocessing differences between Set A and Set C; zero-phase filtering before windowing; offline windows only ([limitations](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md)) |

## 2. Three research stages (never merged)

| Stage | Provider | Events | Records | Stations | Channels | P labels | Windows | Features |
|---|---|---|---|---|---|---|---|---|
| California pilot (v1.0.0, frozen) | USGS (events), EarthScope/IRIS (waveforms) | 8 | 8 listed in the manifest | 2 (ADO, USC) | CI BHZ, 40 Hz | automatic STA/LTA picks | none | 18 (counts) |
| Swiss Set A | SED/ETH via EIDA | 20 | 120 (three-component HH) | 54 | HHZ, HHN, HHE | 120 manual SED first-P | 240 (120 + 120) | 24 |
| Swiss Set C | SED/ETH via EIDA | 15 | 550 (HHZ only) | 79 | HHZ | 550 manual SED first-P | 1,100 (550 + 550) | 18 |

- **California local files.** 12 California MiniSEED files exist locally, but only 8 are listed in the manifest. The other 4 are `CI.ADO.--.BHZ.20240823T153158`, `CI.ADO.--.BHZ.20241114T024035`, `CI.ADO.--.BHZ.20241209T230831` and `CI.USC.--.BHZ.20240912T142821`. Their origin is not established in the current repository evidence.
- **Independence.** Set A and Set C share 0 events. All 54 Set A stations also occur in Set C; 25 stations are Set C only. Set C is **event-level** independent, not an unseen-station test.
- **Feature matrices.** Set A: 45 columns = 20 metadata + 1 label (`is_earthquake`) + 24 features. Set C: 35 columns = 16 metadata + 1 label + 18 features. Metadata and pick-derived columns are not model inputs ([details](../ML_REPRODUCTION_GUIDE.md), section 6).

## 3. Disclosures to read first

1. `sta_lta_max/mean`: STA window 0.5 s in the Set A script, 1.0 s in the Set C script.
2. The response pre-filter corners differ between the two feature scripts.
3. Both scripts apply a zero-phase bandpass to the full trace before cutting windows; "causal windows" refers to window placement only.
4. The numerical effect of items 1 to 3 has not been quantified.
5. `z_cav_m_s` is computed as sum(|v|) x dt on velocity and so has dimension of length despite its name. It was not renamed or recalculated.
6. The ML-4 STA/LTA baseline is **window-level** (STA 1.0 s, `sta_lta_max >= 8.0`). The STEP 2K detector is **record-level** (STA 0.5 s; 401 of 550 records detected, 72.9%). They are different procedures.
7. Threshold 8.0 came from the Swiss Set A threshold grid (California baseline: 2.5). Documents state it was pre-declared before Set C; Git history cannot prove the order.

Sources: [DATA_COLLECTION_AND_ANALYSIS_REPORT.md](../DATA_COLLECTION_AND_ANALYSIS_REPORT.md) section 6.1, [FINAL_INTEGRITY_CHECK.md](../../FINAL_INTEGRITY_CHECK.md).

## 4. Where to read what

| Question | Read |
|---|---|
| What was done, in two pages? | [RESEARCH_EXECUTIVE_SUMMARY.md](RESEARCH_EXECUTIVE_SUMMARY.md) |
| How exactly was it done? | [RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md) |
| Where did the data come from? | [DATA_COLLECTION_AND_ANALYSIS_REPORT.md](../DATA_COLLECTION_AND_ANALYSIS_REPORT.md) |
| What does each column or feature mean? | [DATA_DICTIONARY.md](../DATA_DICTIONARY.md) |
| What files, models and paths exist? | [DATA_AND_MODEL_INVENTORY.md](../DATA_AND_MODEL_INVENTORY.md) |
| What are the results? | [SET_C_VERTICAL_ML_EVALUATION_REPORT.md](../SET_C_VERTICAL_ML_EVALUATION_REPORT.md), [STEP_ML4_COMPREHENSIVE_REPORT.md](../../reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md), [RESEARCH_PACKAGE.md](../RESEARCH_PACKAGE.md) |
| What is weak or unresolved? | [RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md), [FINAL_INTEGRITY_CHECK.md](../../FINAL_INTEGRITY_CHECK.md) |
| How do I check it? | [PROFESSOR_REVIEW_CHECKLIST.md](PROFESSOR_REVIEW_CHECKLIST.md) |
| Likely questions and grounded answers | [PROFESSOR_DISCUSSION_NOTES.md](PROFESSOR_DISCUSSION_NOTES.md) |
| How do I reproduce it? | [DATA_ACQUISITION_AND_REPRODUCTION.md](../DATA_ACQUISITION_AND_REPRODUCTION.md), [ML_REPRODUCTION_GUIDE.md](../ML_REPRODUCTION_GUIDE.md) |
| California v1.0.0 submission | [Research_Report_Final.md](../../reports/Research_Report_Final.md), [FINAL_SUBMISSION/](../../FINAL_SUBMISSION/) |
| Current status and history | [PROJECT_STATUS.md](../PROJECT_STATUS.md), [CHANGELOG.md](../../CHANGELOG.md), [PROJECT_HANDOFF_SUMMARY.md](../../PROJECT_HANDOFF_SUMMARY.md) (historical, dated 2026-11-06; it sits in the repository root, not in `docs/`) |

## 5. Navigating the repository

```text
README.md                      entry point
docs/professor_handover/       this package
docs/                          reports, dictionary, guides, status
data/manifests/                published CSV manifests (events, records, picks)
data/raw/, data/metadata/      local raw waveforms and XML (git-ignored, not published)
reports/features/              feature matrices (California, Set A, Set C)
reports/ml/                    saved models, result JSON/CSV, ML reports
reports/data_lineage/          verified counts and checks
reports/figures/final|data/    research and data-journey figures
scripts/download|analysis|ml|reporting|audit/   code that produced the above
configs/                       acquisition and analysis configuration
tests/                         pytest suite (89 tests)
website/                       Next.js research website
FINAL_SUBMISSION/              frozen v1.0.0 submission package
```

## 6. Navigating the website

The website source is in `website/`. Live address given by the authors: https://amgcr-research.vercel.app/. Whether the live deployment contains the latest commit was **not verified** for this handover; build the site from the repository to be sure (`cd website && npm ci && npm run build`).

| Route | Content |
|---|---|
| `/data-analysis` | Data Collection & Analysis: sources, acquisition, raw data, preprocessing, Set A, Set C, California, features, analysis, integrity, reproduction, downloads |
| `/ml-evaluation` | Results: Set A and Set C comparisons, confusion matrices, importances, per-event recall, disclosures |
| `/docs` | Documentation portal (includes this handover package) |
| `/dashboard`, `/results`, `/dataset`, `/waveforms`, `/map`, `/workflow`, `/research`, `/research/report` | Earlier v2.0 pages (California pilot and Swiss content) |

## 7. Reproducing the analysis

Two pathways, kept separate in the guides:

- **Pathway A (read-only):** verify published numbers from committed manifests, feature matrices, saved models and JSON. No raw data or network needed. Example: the saved models reproduce the Set C confusion counts (RF 547/3/86/464, XGB 546/4/81/469) ([ML_REPRODUCTION_GUIDE.md](../ML_REPRODUCTION_GUIDE.md), section 3).
- **Pathway B (rebuild):** re-download raw data and re-run extraction and training. It overwrites committed files, so use a separate clone or branch, and results may differ from the originals ([DATA_ACQUISITION_AND_REPRODUCTION.md](../DATA_ACQUISITION_AND_REPRODUCTION.md)).

Checks run for this handover: the full test suite (89 passed) on 2026-11-15; the Pathway A snippets; link and number checks listed in [PROFESSOR_REVIEW_CHECKLIST.md](PROFESSOR_REVIEW_CHECKLIST.md).

## 8. Data availability statement

| Class | Content | Where |
|---|---|---|
| Published in GitHub | Manifests, feature matrices, saved models, result JSON/CSV, lineage summary, scripts, configs, figures, documents, California frozen outputs | the paths above |
| Available locally, not published | Raw MiniSEED (California 12, Set A 120, Set C 550), StationXML, QuakeML | `data/raw/`, `data/metadata/` in the authors' working copy |
| Obtainable from external providers | The same raw data | USGS, EarthScope, SED/ETH EIDA, via `scripts/download/` |
| Requires new acquisition | Any dataset beyond Set A, Set C and the California pilot (for example horizontal components for Set C) | not available in the repository |
| Restricted by unreviewed terms | Redistribution of raw waveforms and metadata | provider licence, attribution and citation terms have **not** been reviewed; no raw data are uploaded |

A reviewer can inspect manifests, matrices, models and results without any waveform. Waveform-level checks (windows, filtering, feature derivation, picks against traces) need the raw data from a fresh download.

## Appendix A. Inventory of review-relevant items

Status "published" = committed on `main`. "Required" = needed for an academic review of the research.

| Item | Purpose | Status | Published | Required |
|---|---|---|---|---|
| `README.md` | repository entry point | current | yes | yes |
| `docs/professor_handover/` | this package | new | yes | yes |
| `docs/RESEARCH_PACKAGE.md` | consolidated research summary | current | yes | yes |
| `docs/PROJECT_STATUS.md` | milestone log (historical in places) | current, corrected 2026-11-15 | yes | yes |
| `PROJECT_HANDOFF_SUMMARY.md` (repository root) | onboarding summary from 2026-11-06; **no copy in `docs/`** | historical | yes | no |
| `docs/DATA_COLLECTION_AND_ANALYSIS_REPORT.md` | data journey | current | yes | yes |
| `docs/DATA_DICTIONARY.md` | columns and features | current | yes | yes |
| `docs/DATA_ACQUISITION_AND_REPRODUCTION.md` | acquisition and reproduction | current | yes | yes |
| `docs/ML_REPRODUCTION_GUIDE.md` | ML reproduction | current | yes | yes |
| `docs/DATA_AND_MODEL_INVENTORY.md` | data and model paths | current | yes | yes |
| `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md` | ML-4 results | current | yes | yes |
| `reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md` | ML-3 and ML-4 results | current | yes | yes |
| `docs/ML_RESULTS_REPORT.md` | ML-3 results | corrected 2026-11-15 (see [limitations B4](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md)) | yes | yes |
| `FINAL_INTEGRITY_CHECK.md` | read-only integrity audit with addendum | current | yes | yes |
| `data/manifests/*.csv` (6 files) | events, records, picks, candidate pool | current | yes | yes |
| `reports/features/*_feature_matrix.csv` | model inputs and labels | current | yes | yes |
| `reports/ml/vertical_feature_schema.json` | 18-feature schema | frozen | yes | yes |
| `reports/ml/*.joblib` (4 models) | saved models | frozen | yes | yes |
| `reports/ml/*summary*.json`, per-event CSVs | results | frozen | yes | yes |
| `reports/data_lineage/data_lineage_summary.json` | verified counts | current | yes | yes |
| California outputs (`reports/eda`, `signal_analysis`, `preprocessing`, `tables`, `features/feature_matrix.csv`, `FINAL_SUBMISSION/`) | v1.0.0 | frozen | yes | yes |
| `reports/switzerland_validation/` and `docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md` | STEP 2K record-level validation | frozen | yes | yes |
| `reports/figures/final/` (12), `reports/figures/data/` (9) | figures | current | yes | yes |
| `data/raw/`, `data/metadata/**/*.xml` | raw waveforms and metadata | local only | no | for waveform-level checks |
| `website/` pages `/data-analysis`, `/ml-evaluation` | web presentation | current | yes (source) | no |
| Older v1.0/v2.0 docs and website pages | history and platform | frozen/historical | yes | no |

## Appendix B. Figure index

Generated by `scripts/reporting/make_final_figures.py`, `scripts/reporting/make_data_figures.py` (inputs: saved JSON, matrices, lineage JSON, and local raw records for waveform figures). All figures were inspected on 2026-11-15; values were compared with the saved JSON for the result figures. No figure was changed.

| Figure | File | Shows | Source data | Review note |
|---|---|---|---|---|
| Fig. 1 | `final/fig01_research_workflow.png` | workflow diagram | documented structure | ok |
| Fig. 2 | `final/fig02_dataset_evolution.png` | three stages and counts | lineage JSON | ok |
| Fig. 3 | `final/fig03_waveform_windows.png` | real Set A trace, windows, pick | raw MiniSEED (local), matrix | ok; amplitude in counts, display only |
| Fig. 4 | `final/fig04_feature_engineering.png` | window to features | feature scripts | ok |
| Fig. 5 | `final/fig05_classifier_methodology.png` | model settings | saved models | ok |
| Fig. 6 | `final/fig06_logo_cross_validation.png` | LOGO schematic (8 of 20 folds drawn) | schematic | caption text sits close to the last row |
| Fig. 7 | `final/fig07_set_a_model_comparison.png` | Set A CV metrics | JSON | y-axis starts at 0.80, which exaggerates differences; legend overlaps bar bases |
| Fig. 8 | `final/fig08_set_c_model_comparison.png` | Set C metrics | JSON | legend overlaps bar bases |
| Fig. 9 | `final/fig09_set_c_confusion_matrices.png` | Set C confusion counts | JSON | matches saved counts |
| Fig. 10 | `final/fig10_feature_importance.png` | importances | saved models | note that scales differ between models |
| Fig. 11 | `final/fig11_dataset_independence.png` | event and station overlap | matrices | ok |
| Fig. 12 | `final/fig12_limitations_roadmap.png` | limitations and roadmap | documents | ok |
| Data Fig. 1 | `data/dfig01_source_to_dataset_lineage.png` | lineage | documented structure | ok |
| Data Fig. 2 | `data/dfig02_iris_vs_sed_sources.png` | sources | scripts, configs | ok |
| Data Fig. 3 | `data/dfig03_raw_data_structure.png` | local folder structure | filesystem | ok |
| Data Fig. 4 | `data/dfig04_preprocessing_pipeline.png` | preprocessing steps | feature scripts | ok |
| Data Fig. 5 | `data/dfig05_filtering_before_after.png` | real record, three stages | raw MiniSEED, StationXML (local) | ok |
| Data Fig. 6 | `data/dfig06_three_component_vs_vertical.png` | Set A 3C vs Set C Z | raw records (local) | ok |
| Data Fig. 7 | `data/dfig07_set_a_vs_set_c_comparison.png` | counts, log scale | lineage JSON | the "n/a" label for California windows is displaced from its bar (cosmetic) |
| Data Fig. 8 | `data/dfig08_feature_matrix_structure.png` | column groups | matrix headers | ok |
| Data Fig. 9 | `data/dfig09_quality_control_summary.png` | QC table | manifests | ok |

Proposed cosmetic fixes (not applied; none affects a number): start Fig. 7 at 0, or state the truncated axis in its caption; move legends outside the plot area in Figs. 7 and 8; place the "n/a" label under the California bar in Data Fig. 7.
