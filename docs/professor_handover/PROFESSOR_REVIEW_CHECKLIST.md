# Professor Review Checklist

Tick items as you verify them. Paths are relative to the repository root. "Read-only" items change nothing; commands run from the repository root. Reproduction details: [DATA_ACQUISITION_AND_REPRODUCTION.md](../DATA_ACQUISITION_AND_REPRODUCTION.md), [ML_REPRODUCTION_GUIDE.md](../ML_REPRODUCTION_GUIDE.md).

## 1. Data provenance
- [ ] Sources and endpoints are stated: [report section 2](../DATA_COLLECTION_AND_ANALYSIS_REPORT.md); `configs/sed_switzerland_pilot.yaml`, `scripts/download/download_iris_california_pilot.py`.
- [ ] California events come from USGS and waveforms from EarthScope; no analyst picks, no StationXML saved.
- [ ] Swiss events, waveforms, StationXML and picks all come from SED/ETH via EIDA.
- [ ] Provider licence terms: **not reviewed**; decide before sharing raw data ([limitations C](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md)).
- [ ] The 4 California files outside the manifest are acknowledged ([limitations B1](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md)).

## 2. Dataset construction
- [ ] Counts agree with the manifests: run the snippet in [DATA_ACQUISITION_AND_REPRODUCTION.md](../DATA_ACQUISITION_AND_REPRODUCTION.md) section 6.1 (read-only). Expect California 8 events; Set A 20 / 120 / 54 / 120 picks; Set C 15 / 550 / 79 / 550 picks; event overlap 0; station overlap 54.
- [ ] Set A station rule (distance bins, up to 6 per event) and Set C rule (all same-station pick and HHZ pairs): `configs/`.
- [ ] Set C selection rules and the undocumented ranking: `configs/sed_switzerland_validation_audit.yaml`, `data/manifests/sed_switzerland_validation_candidates.csv`.
- [ ] Event independence versus station overlap: [Fig. 11](../../reports/figures/final/fig11_dataset_independence.png).

## 3. Preprocessing
- [ ] Steps and parameters: [report section 6](../DATA_COLLECTION_AND_ANALYSIS_REPORT.md); `scripts/analysis/run_swiss_set_a_feature_engineering.py`, `run_swiss_set_c_feature_engineering.py`.
- [ ] Differences between sets: STA window (0.5 s versus 1.0 s), pre-filter corners.
- [ ] Zero-phase filter on the full trace before windowing; "causal" means window placement.
- [ ] Before/after example: [Data Fig. 5](../../reports/figures/data/dfig05_filtering_before_after.png).

## 4. Feature engineering
- [ ] Column split: Set A 45 = 20 + 1 + 24, Set C 35 = 16 + 1 + 18 (snippet in [ML guide](../ML_REPRODUCTION_GUIDE.md) section 6.3, read-only).
- [ ] Feature definitions and units: [DATA_DICTIONARY.md](../DATA_DICTIONARY.md); `z_cav_m_s` unit caveat.
- [ ] Metadata and pick-derived columns are not model inputs (models select columns by name: `feature_columns` in each `.joblib`; `reports/ml/vertical_feature_schema.json`).

## 5. Model methodology
- [ ] Hyper-parameters: [Fig. 5](../../reports/figures/final/fig05_classifier_methodology.png), `src/models/*.py`.
- [ ] Event-grouped Leave-One-Group-Out, 20 folds: [Fig. 6](../../reports/figures/final/fig06_logo_cross_validation.png), `src/models/vertical_models.py`.
- [ ] No Set C data in training or selection: `scripts/ml/train_vertical_models_set_a.py`, `evaluate_vertical_models_set_c.py`.
- [ ] No model-selection study between classifiers is recorded.

## 6. Validation and evaluation
- [ ] Saved results: `reports/ml/vertical_set_c_evaluation_summary.json`, `vertical_set_a_evaluation_summary.json`, `swiss_ml_evaluation_summary.json`.
- [ ] Recompute Set C confusion counts from the saved models (read-only): [ML guide](../ML_REPRODUCTION_GUIDE.md) section 3.2. Expect RF (547, 3, 86, 464), XGB (546, 4, 81, 469).
- [ ] Per-event recall: `reports/ml/vertical_set_c_per_event_results.csv`.
- [ ] Window-level baseline versus STEP 2K detector are not mixed ([report section 11](../DATA_COLLECTION_AND_ANALYSIS_REPORT.md); `reports/switzerland_validation/validation_summary.json`).
- [ ] Tests: `python -m pytest -q -p no:cacheprovider` (89 passed on 2026-11-15). Tests check code and artefact consistency, not scientific validity.

## 7. Scientific interpretation
- [ ] Results are described as an offline window-classification benchmark.
- [ ] The Set A to Set C score drop is not explained.
- [ ] Feature importance describes the models, not physical causation.
- [ ] No claim of operational early warning or prediction ([FINAL_INTEGRITY_CHECK.md](../../FINAL_INTEGRITY_CHECK.md)).

## 8. Reproducibility
- [ ] Pathway A (read-only) runs without raw data.
- [ ] Pathway B overwrites artefacts; use a separate clone or branch.
- [ ] `requirements-ml.txt` is needed for ML packages.
- [ ] New downloads may differ from the originals ([data guide section 7](../DATA_ACQUISITION_AND_REPRODUCTION.md)).

## 9. Limitations
- [ ] Read [RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md), sections A to D, and decide which items need action before the work is cited.
