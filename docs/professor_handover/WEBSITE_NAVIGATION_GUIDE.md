# Website Navigation Guide for Academic Reviewers

**Project:** AMGCR Earthquake Research  
**Research focus:** Offline P-wave candidate-window classification using Swiss SED data  
**Website:** https://amgcr-research.vercel.app/  
**Repository:** https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning

## Recommended route through the website

| Step | Website page | What to inspect |
|---|---|---|
| 1 | [Home](https://amgcr-research.vercel.app/) | Project introduction, key highlights, workflow and featured resources |
| 2 | [Research](https://amgcr-research.vercel.app/research) | Research background, objective and scope |
| 3 | [Workflow](https://amgcr-research.vercel.app/workflow) | End-to-end sequence from data acquisition to evaluation |
| 4 | [Data Collection & Analysis](https://amgcr-research.vercel.app/data-analysis) | Data providers, acquisition, raw data structure, preprocessing, Swiss Set A and Set C, features and integrity checks |
| 5 | [Dataset](https://amgcr-research.vercel.app/dataset) and [Waveforms](https://amgcr-research.vercel.app/waveforms) | Dataset information and waveform examples |
| 6 | [ML Evaluation](https://amgcr-research.vercel.app/ml-evaluation) | Set A validation, Set C results, model comparison, confusion matrices, feature importance and per-event results |
| 7 | [Results](https://amgcr-research.vercel.app/results) | High-level project outcomes |
| 8 | [Resources](https://amgcr-research.vercel.app/resources) | Supporting documents and downloadable artefacts |

The website header also contains the **Reviewer Guide** entry, which opens the same guided sequence and provides direct links to the main evidence.

## Important results to locate

On the ML Evaluation page, inspect the independent Swiss Set C comparison:

- XGBoost: F1-score **0.9169**, recall **0.8527**.
- Random Forest: F1-score **0.9125**, recall **0.8436**.
- Window-level STA/LTA baseline: F1-score **0.5014**, recall **0.3345**.

The charts and confusion matrices are accompanied by the saved result artefacts in the repository. The ML-4 STA/LTA baseline is a window-level rule and must not be confused with the separate STEP 2K record-level detector.

## Where the supporting evidence is stored

The GitHub repository contains:

- `data/manifests/`: event, record and pick manifests.
- `reports/features/`: California, Set A and Set C feature matrices.
- `reports/ml/`: saved models, evaluation JSON files, per-event CSV files and ML figures.
- `reports/figures/final/` and `reports/figures/data/`: report figures and data-lineage visuals.
- `scripts/download/`, `scripts/analysis/`, `scripts/ml/`, `scripts/reporting/`: acquisition, feature extraction, training/evaluation and figure-generation code.
- `docs/` and `docs/professor_handover/`: methodology, data dictionary, reproduction instructions, limitations and reviewer notes.

**Raw-data note:** Raw MiniSEED, StationXML and QuakeML files are not published in GitHub. They are stored locally and can be re-downloaded using the documented scripts. Provider redistribution terms have not been reviewed. Published manifests, feature matrices, models, result files, scripts and figures allow substantial inspection of the workflow without committing the raw waveform archive.

## Interpretation and limitations

This is an offline, pre-cut candidate-window classification benchmark. Positive windows are aligned to analyst-provided P picks. It is not continuous real-time P-wave arrival detection, earthquake prediction, or a deployed operational EEW system.

Set A and Set C contain different earthquake events, but all 54 Set A stations also occur in Set C. The evaluation is event-independent, not station-independent. The report and integrity documentation describe additional preprocessing differences and other limitations; these should be read alongside the performance charts.

## Recommended documents for a deeper review

- [Professor Handover Guide](https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning/blob/main/docs/professor_handover/PROFESSOR_HANDOVER_GUIDE.md)
- [Set C Vertical ML Evaluation Report](https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning/blob/main/docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md)
- [Data and Model Inventory](https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning/blob/main/docs/DATA_AND_MODEL_INVENTORY.md)
- [ML Reproduction Guide](https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning/blob/main/docs/ML_REPRODUCTION_GUIDE.md)
- [Final Integrity Check](https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning/blob/main/FINAL_INTEGRITY_CHECK.md)

*The live website should be opened before the review meeting to confirm that the latest deployment is available. The source changes for the Reviewer Guide have been committed to the repository; deployment is subject to the configured Vercel build.*
