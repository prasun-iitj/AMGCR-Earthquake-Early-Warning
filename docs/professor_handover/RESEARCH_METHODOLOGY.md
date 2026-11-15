# Research Methodology

Stand-alone description of how the research was carried out. Every parameter is taken from the named script or configuration; where the repository does not say, the text says so. Field-level detail: [DATA_COLLECTION_AND_ANALYSIS_REPORT.md](../DATA_COLLECTION_AND_ANALYSIS_REPORT.md).

## 1. Original data acquisition

| Stage | Script and configuration | Procedure |
|---|---|---|
| California (2026-07-29 run) | `scripts/download/download_iris_california_pilot.py` | USGS FDSN events, 2024, California box 32.5 to 42.0 N and -124.5 to -114.0 E, magnitude 4.0 to 7.5 (41 matches); scan in time order until 8 events return a BHZ waveform from a distance-ranked list of predefined sites (1 station per event, 300 s from origin) via EarthScope |
| Swiss Set A (2026-09-06) | `scripts/download/download_sed_switzerland_pilot.py`, `configs/sed_switzerland_pilot.yaml` | 20 fixed SED event IDs re-resolved in the live catalogue; availability query; prefer complete HH three-component stations; up to 6 per event from distance bins (0 to 400 km); MiniSEED origin -90 s to +210 s; StationXML at response level |
| Set A picks (STEP ML-1A) | `scripts/download/download_sed_switzerland_set_a_picks.py` | SED QuakeML with arrivals; keep network CH P-type phases (P, Pg, Pn, Pb, P1, Pdiff); match by station; prefer manual picks, earliest if several; stop if any station lacks a pick |
| Swiss Set C (2026-09-11) | `scripts/audit/audit_swiss_validation_candidates.py`, `scripts/download/download_sed_switzerland_validation.py`, `configs/sed_switzerland_validation_audit.yaml`, `..._acquisition.yaml` | Catalogue pool of 227 independent earthquakes; 15 locked by diversity rules (year quotas 4/4/4/3, 15 km separation, magnitude bins, at least 6 in Swiss territory) without using detector performance; every station with a same-station first-P pick and an HHZ record; MiniSEED origin -60 s to +90 s |

Reason the original 20 Set A events were chosen, and the step-by-step ranking that produced the final 15 Set C IDs, are not documented beyond these configurations.

## 2. Data validation

- Set A: checked at download for at least 60 s before and after origin and complete HH three-component data; 120 of 120 passed; StationXML for 120 of 120.
- Set C: download, verification and time coverage 550 of 550; gaps 0; overlaps 0; StationXML verified 550 of 550.
- Picks: 120 and 550, all `manual` evaluation mode.
- Feature scripts skip and log a record if a file or pick is missing; both feature summaries report 0 failures. No NaN values in the feature columns.
- Not checked in the code: contamination of the noise windows by other seismic energy.

## 3. Waveform preprocessing

Applied identically in structure by `scripts/analysis/run_swiss_set_a_feature_engineering.py` and `run_swiss_set_c_feature_engineering.py`:

1. demean and linear detrend; 5% Hann taper;
2. `remove_response(output="VEL", water_level=60, zero_mean=True)` with a cosine pre-filter;
3. 0.1 to 15 Hz bandpass, 4 corners, **zero-phase**, on the **full trace**.

Differences between the two scripts: response pre-filter corners (Set A: `pre_filt_for_sampling`, 0.05 and 0.08 Hz with 0.75 and 0.85 of Nyquist; Set C: 0.05 and 0.08 Hz with min(18 Hz, 0.75 Nyquist) and min(22.5 Hz, 0.85 Nyquist)); STA window of the STA/LTA features (0.5 s versus 1.0 s). Effects are unquantified. California was not response-corrected (the StationXML request failed in the frozen run).

## 4. Manual P-wave labelling

The label source is the SED analyst first-P pick for each station, delivered in QuakeML. Phases: Set A Pg 114, P1 3, Pn 3; Set C Pg 390, P1 87, Pn 73. A pick is a reference annotation with analyst uncertainty, not ground truth.

## 5. Candidate window construction

One positive and one negative 4.0 s window per record: positive from the pick to pick + 4 s (`is_earthquake = 1`), negative from origin - 35 s to origin - 31 s (`0`). Set A: 240 windows; Set C: 1,100. Positive windows start at the analyst pick, so the benchmark measures discrimination of pick-aligned windows, not arrival detection.

## 6. Feature engineering

24 features for Set A (16 vertical `z_*`, 4 horizontal and vector, `vh_ratio`, 2 STA/LTA, `snr_db`); 18 vertical features for Set C (16 `z_*` plus `sta_lta_max`, `sta_lta_mean`). Definitions and units: [DATA_DICTIONARY.md](../DATA_DICTIONARY.md). Exact order: `reports/ml/vertical_feature_schema.json`. `z_cav_m_s` = sum(|v|) x dt on velocity (dimension of length); name retained.

## 7. Training and cross-validation

`src/models/random_forest.py`, `xgboost_model.py`, `vertical_models.py`; `scripts/ml/`.

- Random Forest: 200 trees, max depth 6, min split 4, min leaf 2, `max_features=sqrt`, `class_weight=balanced`, seed 42.
- XGBoost: 100 trees, max depth 4, learning rate 0.05, subsample 0.8, colsample 0.8, L1 0.1, L2 1.0, seed 42.
- Leave-One-Group-Out, 20 folds, group = earthquake (`short_id`): every window of one earthquake is held out together.
- Decision threshold 0.5 (not tuned).
- Two feature sets: 24 (STEP ML-3) and 18 vertical (STEP ML-4).

The repository does not record a comparative model-selection study; Random Forest and XGBoost were chosen as tree ensembles for small tabular data (see [PROJECT_STATUS.md](../PROJECT_STATUS.md), STEP ML-2 limitations).

## 8. Independent Set C evaluation

The frozen 18-feature models trained on Set A were applied once to the Set C matrix (`scripts/ml/evaluate_vertical_models_set_c.py`). No Set C data entered training, selection or thresholding. Independence is by event; all 54 Set A stations also occur in Set C. The 24-feature models cannot be applied to Set C because it lacks horizontal channels.

## 9. Baseline comparison

- **ML-4 baseline (window-level):** `sta_lta_max >= 8.0` on each Set C window, STA 1.0 s / LTA 10 s.
- **STEP 2K (record-level):** frozen detector, STA 0.5 s / LTA 10 s, response-corrected HHZ, 0.1 to 15 Hz, trigger on 8.0 and off 0.5, first trigger in origin to origin + 90 s; 401 of 550 records detected; `scripts/analysis/run_swiss_independent_validation.py`.
- Threshold 8.0 was chosen from the Swiss Set A grid with a rule written beforehand (`configs/swiss_sta_lta_transfer.yaml`); the California threshold was 2.5.

The two baselines use different units, STA windows and scoring and must not be compared as one number.

## 10. Performance evaluation

Positive class = P-wave window. Accuracy, precision, recall, specificity, F1, ROC-AUC, and confusion counts (TP, FP, TN, FN) from `reports/ml/*.json`; per-event recall from the per-event CSVs. Feature importance from the saved models (Random Forest Gini, XGBoost normalised gain): these describe model use, not physical causation. Results and interpretation: [RESEARCH_EXECUTIVE_SUMMARY.md](RESEARCH_EXECUTIVE_SUMMARY.md).
