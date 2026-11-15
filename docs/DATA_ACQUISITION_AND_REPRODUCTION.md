# Data Acquisition and Reproduction Guide

How to obtain the original data and rebuild the datasets from it. Commands were read from the scripts' argument parsers and constants; only the lightweight, read-only items marked **(run)** were executed for this document. Downloads and extraction were **not** re-run, to avoid overwriting frozen artifacts and to avoid re-downloading about 41 MB of data.

> **Overwrite warning.** The scripts below write to committed paths (`data/manifests/*.csv`, `reports/features/*.csv`, `reports/ml/*`). Work in a separate clone or branch. Re-downloading may yield different data if a provider revises its catalogue or picks, and manifests would then differ from the published ones. Never change the 15 locked Set C IDs.

## 1. Software

- Python 3.11 or newer (results were produced with 3.13). `pip install -r requirements.txt -r requirements-ml.txt` (`requirements.txt` has no ML packages; see [ML_REPRODUCTION_GUIDE.md](ML_REPRODUCTION_GUIDE.md)). Key versions: obspy 1.5.0, numpy 2.5.1, pandas 3.0.5, scipy 1.18.0, matplotlib 3.11.1, PyYAML 6.0.3, scikit-learn 1.9.1, xgboost 3.4.1, joblib 1.6.0.
- Network access to `earthquake.usgs.gov`, `service.earthscope.org`, `eida.ethz.ch`. No credentials are needed; the services are public. Services may rate-limit (HTTP 429/503); the scripts back off and stop on those codes.
- Disk: about 41 MB of MiniSEED and about 32 MB of StationXML/QuakeML.

## 2. Sources

| Source | URL | Used for |
|---|---|---|
| USGS FDSN event | https://earthquake.usgs.gov/fdsnws/event/1/ | California events |
| EarthScope (IRIS) dataselect | https://service.earthscope.org | California waveforms |
| SED/ETH EIDA event | https://eida.ethz.ch/fdsnws/event/1/ | Swiss catalogue, QuakeML picks |
| SED/ETH EIDA dataselect | https://eida.ethz.ch/fdsnws/dataselect/1/ | Swiss MiniSEED |
| SED/ETH EIDA station | https://eida.ethz.ch/fdsnws/station/1/ | StationXML, coordinates |
| SED/ETH EIDA availability | https://eida.ethz.ch/fdsnws/availability/1/ | station selection |

Licence, attribution and redistribution terms of these providers were not reviewed in the repository. Check them before sharing raw data. This is why raw data are not on GitHub.

## 3. Acquisition (run from the repository root)

| Step | Command | Needs | Writes | Expected result |
|---|---|---|---|---|
| California | `python scripts/download/download_iris_california_pilot.py` (options `--event-count 8 --min-events 5 --raw-dir PATH --manifest-csv PATH`) | network | `data/raw/iris/`, `data/manifests/iris_california_pilot_events.csv`, `logs/iris_california_pilot_summary.json` | up to 8 events, 1 BHZ file each. Catalogue changes can change which events qualify; the frozen pilot used the 2026-07-29 run |
| Set A waveforms + StationXML | `python scripts/download/download_sed_switzerland_pilot.py --config configs/sed_switzerland_pilot.yaml` | network | `data/raw/switzerland/<short_id>/`, `data/metadata/switzerland/<short_id>/`, `data/manifests/sed_switzerland_pilot_events.csv`, `reports/switzerland_pilot/*.json` | 20 events, 120 records, 120 StationXML, validation PASS 120/120 (run on 2026-09-06; station availability timeouts can change the station choice on a re-run) |
| Set A picks | `python scripts/download/download_sed_switzerland_set_a_picks.py` | Set A manifest, network | `data/metadata/switzerland/<short_id>/quakeml.xml`, `data/manifests/sed_switzerland_set_a_picks.csv`, `reports/switzerland_set_a_picks/` | 120/120 manual picks (Pg 114, P1 3, Pn 3); exits with an error if any station has no pick |
| Set C candidate pool (design step; already committed) | `python scripts/audit/audit_swiss_validation_candidates.py` (config `configs/sed_switzerland_validation_audit.yaml`) | network | `data/manifests/sed_switzerland_validation_candidates.csv`, `reports/switzerland_validation_audit/` | 227 events, 15 locked. Not needed to reproduce the data; the committed CSV and the locked IDs are authoritative |
| Set C waveforms + picks | `python scripts/download/download_sed_switzerland_validation.py --config configs/sed_switzerland_validation_acquisition.yaml` | candidate CSV, network | `data/raw/switzerland_validation/<short_id>/`, `data/metadata/switzerland_validation/<short_id>/`, `data/manifests/sed_switzerland_validation_waveforms.csv`, `..._picks.csv`, `reports/switzerland_validation_acquisition/` | 15 events, 550 HHZ records, 550 StationXML, 550 picks |

Script options for the Swiss downloads are only `--config`. The picks script has no arguments.

## 4. Expected directory structure after acquisition

```
data/raw/iris/<quakeml_..._eventid_ID_format_quakeml>/CI.<STA>.--.BHZ.<origin>.mseed
data/raw/switzerland/<short_id>/CH.<STA>.--.HH.<origin>.mseed            (3 components per file)
data/raw/switzerland_validation/<short_id>/CH.<STA>.--.HHZ.<origin>.mseed
data/metadata/switzerland/<short_id>/CH.<STA>.--.HH.xml  and  quakeml.xml
data/metadata/switzerland_validation/<short_id>/CH.<STA>.--.HHZ.xml
```

## 5. Validation of the acquired data

1. Counts: 120 and 550 `.mseed` files (`python scripts/reporting/audit_data_lineage.py` **(run)** prints/saves them; it also compares manifests with the local folders and writes `reports/data_lineage/data_lineage_summary.json`).
2. Manifest status columns: Set A `download_status` = OK and `validation_status` = PASS for all rows; Set C `download_status` = ok, `verification_status` = PASS, `coverage_status` = full, `gaps` and `overlaps` = 0.
3. Picks: Set A 120 rows and Set C 550 rows, all `manual`.
4. Tests (offline): `python -m pytest tests/test_switzerland_set_a_picks.py tests/test_swiss_set_a_features.py tests/test_vertical_models.py tests/test_ml_models.py tests/test_switzerland_validation_acquisition.py tests/test_switzerland_pilot.py tests/test_switzerland_validation_audit.py -q` **(run 2026-11-15: 58 passed)**. The full test suite was not run.

## 6. Preprocessing and feature extraction

| Step | Command | Reads | Writes |
|---|---|---|---|
| Set A features (240 x 45) | `python scripts/analysis/run_swiss_set_a_feature_engineering.py` | Set A manifest, picks, raw data, StationXML | `reports/features/swiss_set_a_feature_matrix.csv`, `swiss_set_a_per_record_features.csv`, `swiss_set_a_feature_summary.json`, `reports/features/swiss_figures/` |
| Set C features (1,100 x 35) | `python scripts/analysis/run_swiss_set_c_feature_engineering.py` | Set C manifest (`MiniSEED_path`, `StationXML_path`, picks), raw data | `reports/features/swiss_set_c_feature_matrix.csv`, `swiss_set_c_feature_summary.json` |
| California chain (frozen) | `python scripts/analysis/run_california_pilot_eda.py`, `..._signal_analysis.py`, `..._preprocessing.py`, `..._feature_engineering.py` | California raw + manifest | `reports/eda`, `reports/signal_analysis`, `reports/preprocessing`, `reports/features/feature_matrix.csv` |
| Swiss signal analysis / STA/LTA transfer / STEP 2K | `python scripts/analysis/run_swiss_signal_analysis.py`, `run_swiss_sta_lta_transfer.py`, `run_swiss_independent_validation.py` | Swiss raw data, configs | `reports/swiss_signal_analysis/`, `reports/switzerland_validation/` |

Expected outcome: the same shapes and columns; floating-point values may differ in the last digits across library versions. A re-run does **not** remove the documented differences between the Set A and Set C scripts (STA window 0.5 s vs 1.0 s; response pre-filter corners; zero-phase filtering of full traces). Model training and evaluation: [ML_REPRODUCTION_GUIDE.md](ML_REPRODUCTION_GUIDE.md).

## 7. Data without raw files: what a reviewer can still check

Everything in `reports/features/`, `data/manifests/`, `reports/ml/` and `reports/data_lineage/` is published. With these a reviewer can recompute the evaluation counts and metrics from the saved models and Set C matrix (see the ML guide) and verify every number in [DATA_COLLECTION_AND_ANALYSIS_REPORT.md](DATA_COLLECTION_AND_ANALYSIS_REPORT.md) except waveform-level content.

## 8. Limitations of reproduction

- Raw waveforms are not on GitHub; re-acquisition depends on provider availability.
- Catalogue and pick revisions at SED or USGS after the original download may change results.
- Station availability timeouts affected the Set A station selection; a re-run may select different stations.
- Four extra California MiniSEED files exist locally that the manifest does not list.
- Provider licensing was not reviewed.
- The two Swiss feature scripts differ in the ways listed above; results from a re-run reproduce the published matrices, not a harmonised pipeline.
