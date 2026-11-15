# Data Acquisition and Reproduction Guide

How to obtain the original data and rebuild the datasets from it. Companion to [ML_REPRODUCTION_GUIDE.md](ML_REPRODUCTION_GUIDE.md) (models and ML outputs) and [DATA_COLLECTION_AND_ANALYSIS_REPORT.md](DATA_COLLECTION_AND_ANALYSIS_REPORT.md) (the narrative).

Command arguments below were checked against the scripts' argument parsers and path constants. Only the commands marked **(run)** were executed for this document. Downloads and feature extraction were **not** re-run, to avoid overwriting frozen artefacts and re-downloading about 41 MB of data.

## 0. Two pathways

| | Pathway A: verify published results | Pathway B: reconstruct from raw data |
|---|---|---|
| Uses | committed manifests, feature matrices, saved models, JSON/CSV, published California intermediates | data downloaded again from USGS, EarthScope and SED/ETH |
| Network / raw waveforms | not needed | needed (raw data are not on GitHub) |
| Writes to the repository | no | yes, overwrites committed files |
| Result | recomputes published numbers from published files | a new dataset that may differ from the original (section 7) |

> **Pathway B must run in a separate clone or branch.** Download and extraction scripts overwrite committed manifests, feature matrices, models and frozen California outputs. Use
> `git clone https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning.git amgcr-repro`, then `cd amgcr-repro` and `git switch -c repro-check`. Do not commit or push the outputs, and delete the clone afterwards. Never change the 15 locked Set C event IDs.

Safety tags used below: **RO** = writes no tracked file (it may create git-ignored `__pycache__`); **OVERWRITES** = writes to a committed path; **NET** = needs network. All commands run from the **repository root**; arguments such as `--config` are resolved against the current directory.

## 1. Software and operating systems

- Python 3.11 or newer; results were produced with 3.13. `pip install -r requirements.txt -r requirements-ml.txt` (`requirements.txt` has no ML packages). Key versions: obspy 1.5.0, numpy 2.5.1, pandas 3.0.5, scipy 1.18.0, matplotlib 3.11.1, PyYAML 6.0.3, scikit-learn 1.9.1, xgboost 3.4.1, joblib 1.6.0.
- Everything in this repository's documentation was executed on **Windows with PowerShell** only. On Linux and macOS use `python3 -m venv .venv`, `source .venv/bin/activate` and `python3`; this is standard practice but was **not tested**. XGBoost on macOS may need the OpenMP runtime (`libomp`). Scripts use `pathlib`, and the manifests store forward-slash paths, so path separators should not matter, but this was only exercised on Windows.
- Network access to `earthquake.usgs.gov`, `service.earthscope.org` and `eida.ethz.ch`. The scripts use no credentials or API keys and contain none. Services may rate-limit (HTTP 429/503); the Swiss scripts stop on those codes instead of retrying forever.
- Disk: about 41 MB of MiniSEED and about 32 MB of StationXML/QuakeML.

## 2. Sources and licences

| Source | URL | Used for |
|---|---|---|
| USGS FDSN event | https://earthquake.usgs.gov/fdsnws/event/1/ | California events |
| EarthScope (IRIS) dataselect | https://service.earthscope.org | California waveforms |
| SED/ETH EIDA event | https://eida.ethz.ch/fdsnws/event/1/ | Swiss catalogue, QuakeML picks |
| SED/ETH EIDA dataselect | https://eida.ethz.ch/fdsnws/dataselect/1/ | Swiss MiniSEED |
| SED/ETH EIDA station | https://eida.ethz.ch/fdsnws/station/1/ | StationXML, coordinates |
| SED/ETH EIDA availability | https://eida.ethz.ch/fdsnws/availability/1/ | station selection |

**Licence, attribution and redistribution terms of these providers have not been reviewed** in this repository, and nothing here says that redistribution is permitted. Check them before sharing raw data. This is why raw data are not on GitHub. The endpoint URLs were read from the scripts and configs; the links were not re-fetched for this document.

## 3. California pilot: reproducing frozen results vs re-running acquisition

These are different activities.

### 3.1 Reproducing the frozen results (no raw data, no network)

California v1.0.0 is frozen. Its published outputs are committed: `data/manifests/iris_california_pilot_events.csv` (8 rows), `reports/eda/`, `reports/signal_analysis/` (8 per-event metric JSONs, STA/LTA picks), `reports/preprocessing/` (18 files, including per-event `*_stages.npz`), `reports/tables/*.csv`, `reports/features/feature_matrix.csv` (8 x 25), and the `FINAL_SUBMISSION/` package.

- **Read-only check (RO).** Print the manifest and feature-matrix shapes, e.g. the manifest snippet in section 6, and open `reports/features/feature_matrix.csv`. The manifest has 8 events and 8 waveform files (stations CI.ADO and CI.USC, BHZ, 40 Hz).
- **Re-derive the features from published intermediates (OVERWRITES, separate clone only, no network).** `python scripts/analysis/run_california_feature_engineering.py` reads `reports/preprocessing/*_stages.npz` and `reports/signal_analysis/*_metrics.json` plus the manifest. It does not read raw MiniSEED. It rewrites the California files in `reports/features/` (`feature_matrix.csv`, `feature_summary.json`, and the other California files there), `reports/figures/` and `reports/tables/`. Values are in digital counts (no response correction).

### 3.2 Re-running the acquisition (NET; new data, not the frozen data)

`python scripts/download/download_iris_california_pilot.py` (options: `--event-count`, `--min-events`, `--raw-dir`, `--manifest-csv`; there is no option to request specific event IDs).

- It queries USGS for 2024-01-01 to 2024-12-31, California box 32.5 to 42.0 N, -124.5 to -114.0 E, magnitude 4.0 to 7.5, then scans the returned list **in time order** until `--event-count` (default 8) events return a non-empty BHZ waveform from a distance-ranked list of predefined sites (up to 5 attempts, 1 station per event).
- The frozen pilot is therefore "the first 8 events that returned data on 2026-07-29" (41 catalogue matches then). A new run depends on the current USGS catalogue and on EarthScope availability. If either has changed, a different set of events or stations may result. The script cannot be pinned to the frozen 8 events by an option.
- It overwrites `data/manifests/iris_california_pilot_events.csv` and `logs/iris_california_pilot_summary.json`, so run it with `--raw-dir` and `--manifest-csv` pointing outside the committed paths, or in a separate clone. Compare the new manifest's `event_id` values with the committed manifest to see whether the same events were obtained.
- `data/raw/iris/` in the original working copy contains 12 MiniSEED files; 4 are not in the manifest (`CI.ADO.--.BHZ.20240823T153158`, `CI.ADO.--.BHZ.20241114T024035`, `CI.ADO.--.BHZ.20241209T230831`, `CI.USC.--.BHZ.20240912T142821`). The repository does not explain them. The EDA script lists files as in or out of the manifest.

### 3.3 Re-running the California analysis chain on re-downloaded data

| Script | Needs | Tag |
|---|---|---|
| `run_california_pilot_eda.py` | raw MiniSEED (`data/raw/iris`, all `*.mseed` including extras) + manifest | OVERWRITES `reports/eda`, `reports/figures`, `reports/tables` |
| `run_california_signal_analysis.py` | raw MiniSEED + manifest | OVERWRITES `reports/signal_analysis`, figures, tables |
| `run_california_preprocessing.py` | raw MiniSEED + manifest + **network**: it requests StationXML from EarthScope for response removal | OVERWRITES `reports/preprocessing`, figures, tables |
| `run_california_feature_engineering.py` | published `reports/preprocessing` and `reports/signal_analysis` outputs | OVERWRITES `reports/features`, figures, tables |

The scripts take no arguments. **Important:** in the frozen run the response request failed for all 8 records (response applied 0/8, amplitudes in counts; `docs/PREPROCESSING_REPORT.md`). A re-run with working network access may succeed and produce velocity instead of counts, which would not match the frozen results. California outputs must not be mixed with Swiss results.

## 4. Swiss acquisition (Pathway B, step 1; NET; OVERWRITES manifests)

| Step | Command | Arguments (verified) | Reads | Writes |
|---|---|---|---|---|
| Set A waveforms + StationXML | `python scripts/download/download_sed_switzerland_pilot.py --config configs/sed_switzerland_pilot.yaml` | `--config` (default: that file) | config (20 event IDs, endpoints, windows) | `data/raw/switzerland/<short_id>/`, `data/metadata/switzerland/<short_id>/`, `data/manifests/sed_switzerland_pilot_events.csv`, `reports/switzerland_pilot/*.json` |
| Set A picks | `python scripts/download/download_sed_switzerland_set_a_picks.py` | none | Set A manifest | `data/metadata/switzerland/<short_id>/quakeml.xml`, `data/manifests/sed_switzerland_set_a_picks.csv`, `reports/switzerland_set_a_picks/` |
| Set C waveforms + StationXML + picks | `python scripts/download/download_sed_switzerland_validation.py --config configs/sed_switzerland_validation_acquisition.yaml` | `--config` | candidate CSV, audit config (locked IDs) | `data/raw/switzerland_validation/<short_id>/`, `data/metadata/switzerland_validation/<short_id>/`, `data/manifests/sed_switzerland_validation_waveforms.csv`, `sed_switzerland_validation_picks.csv`, `reports/switzerland_validation_acquisition/` |
| Set C candidate pool (design step, not needed to reproduce) | `python scripts/audit/audit_swiss_validation_candidates.py` | `--config` (default `configs/sed_switzerland_validation_audit.yaml`), `--refresh-set-c PATH` ("refresh availability and same-station picks for the locked 15 events; does not reselect") | SED catalogue and QuakeML (NET) | the candidate CSV and audit reports. The committed CSV and the locked IDs in the config are authoritative |

Expected result as originally acquired: Set A 20 events, 120 records, 120 StationXML, validation PASS 120/120, 120/120 manual picks (Pg 114, P1 3, Pn 3). Set C 15 events, 550 HHZ records, 550 StationXML, 550 manual picks (Pg 390, P1 87, Pn 73).

Behaviour on re-run (read from the code):

- The Set A pilot script re-requests data and rewrites its manifest; it has no "skip existing files" logic.
- The Set C script **reuses existing non-empty MiniSEED and StationXML files** it finds in `data/raw/switzerland_validation/` and `data/metadata/switzerland_validation/`. To test a genuine re-download, use a clone without those folders.
- The Set A picks script exits with an error if any of the 120 stations has no pick.

## 5. Expected directory structure and counts after acquisition

```
data/raw/iris/<quakeml_..._eventid_ID_format_quakeml>/CI.<STA>.--.BHZ.<origin>.mseed
data/raw/switzerland/<short_id>/CH.<STA>.--.HH.<origin>.mseed            (3 components per file)
data/raw/switzerland_validation/<short_id>/CH.<STA>.--.HHZ.<origin>.mseed
data/metadata/switzerland/<short_id>/CH.<STA>.--.HH.xml  and  quakeml.xml
data/metadata/switzerland_validation/<short_id>/CH.<STA>.--.HHZ.xml
```

Originally: 120 Set A and 550 Set C `.mseed` files, 140 Set A XML (120 StationXML + 20 QuakeML) and 550 Set C StationXML. A new run may yield different numbers (section 7).

## 6. Pathway A checks for the data (read-only)

**6.1 Manifest counts (RO).** Paste into Python started in the repository root:

```python
import pandas as pd
m = "data/manifests/"
ca = pd.read_csv(m + "iris_california_pilot_events.csv")
a = pd.read_csv(m + "sed_switzerland_pilot_events.csv")
ap = pd.read_csv(m + "sed_switzerland_set_a_picks.csv")
c = pd.read_csv(m + "sed_switzerland_validation_waveforms.csv")
cp = pd.read_csv(m + "sed_switzerland_validation_picks.csv")
print("California: events", ca["event_id"].nunique(), "| files", ca["waveform_file_count"].sum())
print("Set A: events", a["event_id"].nunique(), "| records", len(a), "| stations", a["station"].nunique(), "| picks", len(ap), ap["pick_phase"].value_counts().to_dict())
print("Set C: events", c["short_id"].nunique(), "| records", len(c), "| stations", c["station"].nunique(), "| picks", len(cp), cp["pick_phase"].value_counts().to_dict())
print("Set A / Set C event overlap:", len(set(a["event_id"].str.split("/").str[-1]) & set(c["short_id"])))
print("Station overlap (shared / Set A / Set C):", len(set(a["station"]) & set(c["station"])), a["station"].nunique(), c["station"].nunique())
```

Output when run on 2026-11-15 **(run)**: California events 8, files 8; Set A events 20, records 120, stations 54, picks 120 `{'Pg': 114, 'P1': 3, 'Pn': 3}`; Set C events 15, records 550, stations 79, picks 550 `{'Pg': 390, 'P1': 87, 'Pn': 73}`; event overlap 0; station overlap 54 / 54 / 79.

**6.2 Matrix columns and model results.** [ML_REPRODUCTION_GUIDE.md](ML_REPRODUCTION_GUIDE.md) sections 3 and 6 (column split 45 = 20 + 1 + 24 and 35 = 16 + 1 + 18; recomputed Set C confusion counts).

**6.3 Tests (RO).** `python -m pytest tests/test_switzerland_set_a_picks.py tests/test_swiss_set_a_features.py tests/test_vertical_models.py tests/test_ml_models.py tests/test_switzerland_validation_acquisition.py tests/test_switzerland_pilot.py tests/test_switzerland_validation_audit.py -q -p no:cacheprovider` **(run 2026-11-15: 58 passed)**. The full suite (`python -m pytest -q -p no:cacheprovider`) was run separately on 2026-11-15: 89 passed.

**6.4 Lineage audit (OVERWRITES one file).** `python scripts/reporting/audit_data_lineage.py` recomputes the counts from the manifests, matrices, schemas and saved models and, if present, the local raw folders, then rewrites `reports/data_lineage/data_lineage_summary.json` (the timestamp changes). It reads no waveform samples. Run it in a separate clone, or restore the file afterwards.

## 7. Where new downloads may differ from the original acquisition

No identical-result guarantee is made. Differences can come from:

- **Catalogue revisions.** SED and USGS may revise origins, magnitudes, event types or event IDs. The Swiss scripts resolve the fixed IDs against the live catalogue; hypocentres and magnitudes are not hard-coded.
- **Pick revisions.** Manual picks are read from the live QuakeML. Analysts or SED may have added, changed or removed picks. The Set A picks script stops if a station loses its pick. If several manual picks exist it takes the earliest.
- **Station availability.** Set A used distance-bin selection from availability queries, and some availability batches timed out in the original run (`docs/SED_SWITZERLAND_DATASET_REPORT.md`). A re-run may select different stations. Set C uses "all same-station pick and HHZ pairs", so changed picks or availability change its record count.
- **California.** The frozen events are "the first 8 that returned data"; new results depend on current USGS and EarthScope holdings (section 3.2).
- **Metadata.** StationXML responses can be updated by the provider, which changes response-corrected amplitudes.
- **Software.** ObsPy, NumPy, SciPy, scikit-learn and XGBoost versions, and thread counts, can change numeric results in the last digits. Bit-for-bit identity of features or models was not tested.
- **Resume behaviour.** The Set C script reuses files already present (section 4).

Any new dataset should be treated as a new acquisition and compared with the committed manifests before it is used with the saved models.

## 8. Preprocessing and feature extraction (Pathway B, step 2; OVERWRITES)

| Step | Command | Reads | Writes |
|---|---|---|---|
| Set A features (240 x 45) | `python scripts/analysis/run_swiss_set_a_feature_engineering.py` | Set A manifest, picks, raw data, StationXML | `reports/features/swiss_set_a_feature_matrix.csv`, `swiss_set_a_per_record_features.csv`, `swiss_set_a_feature_summary.json`, `reports/features/swiss_figures/` |
| Set C features (1,100 x 35) | `python scripts/analysis/run_swiss_set_c_feature_engineering.py` | Set C manifest (`MiniSEED_path`, `StationXML_path`, picks), raw data | `reports/features/swiss_set_c_feature_matrix.csv`, `swiss_set_c_feature_summary.json` |
| Swiss signal analysis, STA/LTA transfer, STEP 2K | `python scripts/analysis/run_swiss_signal_analysis.py`, `run_swiss_sta_lta_transfer.py`, `run_swiss_independent_validation.py` | Swiss raw data, configs | `reports/swiss_signal_analysis/`, `reports/switzerland_validation/` |

None of these scripts takes command-line arguments. Expected outcome: the same shapes and columns; values may differ as in section 7. A re-run does **not** remove the documented differences between the Set A and Set C scripts (STA window 0.5 s vs 1.0 s; response pre-filter corners; zero-phase filtering of full traces). Models and ML outputs: [ML_REPRODUCTION_GUIDE.md](ML_REPRODUCTION_GUIDE.md) section 4.

## 9. What can be checked without raw files

Everything in `reports/features/`, `data/manifests/`, `reports/ml/`, `reports/data_lineage/` and the published California intermediates is committed. With these a reviewer can verify the counts and the Set C confusion matrices (Pathway A) but not waveform-level content or the feature derivation.

## 10. Limitations of reproduction

- Raw waveforms are not on GitHub; re-acquisition depends on provider availability.
- Catalogue and pick revisions after the original download may change results.
- Station availability timeouts affected the Set A station selection.
- Four extra California MiniSEED files exist in the original working copy that the manifest does not list.
- Provider licensing was not reviewed.
- Windows was the only operating system used to run these commands.
