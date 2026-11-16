# Professor Navigation Guide

**AMGCR Earthquake Research — M.Tech.-AI Research Submission**  
Student: Prasun Kumar Tripathi | Roll No.: M25AI2151 | IIT Jodhpur

## 1. Start here

| Resource | Link | Purpose |
|---|---|---|
| Research website | https://amgcr-research.vercel.app/ | Interactive overview of the research, datasets, workflow, analysis and ML evaluation. |
| Website Reviewer Guide | https://amgcr-research.vercel.app/review-guide | Guided route for reviewing the deployed research website. |
| GitHub repository | https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning | Source code, documentation, manifests, feature matrices, models, evaluation outputs and figures. |
| Professor Handover Guide | [Open guide](PROFESSOR_HANDOVER_GUIDE.md) | Detailed scope, dataset stages, caveats, repository map and reproduction routes. |

## 2. Research scope

The current ML study is an **offline classification of P-wave candidate windows versus ambient-noise windows** using Swiss SED data. Random Forest and XGBoost are trained on Set A and evaluated on separate events in Set C. This is not an operational real-time earthquake early-warning system and does not predict earthquakes.

## 3. Where research files are stored

| Repository path | Contents |
|---|---|
| `data/manifests/` | Event, waveform-record and SED analyst-pick manifests for California, Swiss Set A and Swiss Set C. |
| `reports/features/` | Published CSV feature matrices and summaries. |
| `reports/ml/` | Saved models, evaluation JSON/CSV files, feature schema and per-event results. |
| `reports/figures/` | Final research diagrams and data-journey figures. |
| `scripts/download/` | Scripts to reacquire waveform data and metadata. |
| `scripts/analysis/` | Waveform processing, window construction and feature extraction scripts. |
| `scripts/ml/` and `src/models/` | Model training/evaluation entry points and implementations. |
| `docs/` | Data collection report, data dictionary, acquisition/reproduction guides, ML reproduction guide and inventory. |
| `FINAL_INTEGRITY_CHECK.md` and `reports/data_lineage/` | Integrity checks and data-lineage summaries. |

## 4. Dataset overview

| Dataset | Summary |
|---|---|
| California pilot | 8 events; 8 waveform records listed in the manifest; 2 stations; BHZ; frozen pilot, separate from Swiss ML metrics. |
| Swiss Set A | 20 events; 120 three-component HH records; 54 stations; 120 manual first-P picks; 240 candidate windows; 24 engineered features. |
| Swiss Set C | 15 different events; 550 HHZ records; 79 stations; 550 manual first-P picks; 1,100 candidate windows; 18 vertical-only features. Event-level independent from Set A, but stations overlap. |

## 5. Data availability

**Published in GitHub:** manifests, feature matrices, trained models, result files, scripts, configurations, figures and documentation.

**Not published:** raw MiniSEED waveforms, StationXML and QuakeML are excluded from GitHub (identified as local-only / git-ignored in the repository inventory). They can be reacquired using scripts in `scripts/download/`.

The committed manifests and derived outputs support review of the reported analysis. Re-running waveform-level processing requires downloading the raw records and metadata again; a fresh download may not be byte-identical to the original local files.

## 6. Reproduction and review route

1. Start with the repository [README](../../README.md) and the [Professor Handover Guide](PROFESSOR_HANDOVER_GUIDE.md).
2. Inspect `data/manifests/`, `reports/features/`, `reports/ml/` and `reports/data_lineage/` for committed evidence.
3. Use [Data Acquisition and Reproduction](../DATA_ACQUISITION_AND_REPRODUCTION.md) to reacquire data and reproduce features.
4. Use [ML Reproduction Guide](../ML_REPRODUCTION_GUIDE.md) to verify model training and evaluation.
5. Use [Data and Model Inventory](../DATA_AND_MODEL_INVENTORY.md) for the file-level inventory and [Set C Vertical ML Evaluation Report](../SET_C_VERTICAL_ML_EVALUATION_REPORT.md) for detailed Set C results.

## 7. Important interpretation and limitations

- The reported ML metrics are candidate-window classification metrics, not event-detection rates, operational false-alert rates or warning-time measurements.
- The ML-4 window-level STA/LTA baseline is distinct from the STEP 2K record-level STA/LTA detector (401/550 records detected; 72.9%).
- Set A and Set C have no event overlap, but all 54 Set A stations also occur in Set C. The evaluation is event-independent, not station-independent.
- Set A and Set C feature scripts differ in STA window and response pre-filter settings; both apply zero-phase filtering to full traces before window cutting. The numerical impact has not been quantified.

---
Prepared as a navigation aid for the submitted research report and presentation.