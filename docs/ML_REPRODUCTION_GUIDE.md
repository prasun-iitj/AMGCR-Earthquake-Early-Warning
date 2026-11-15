# ML Reproduction Guide (STEP ML-1A to ML-4)

Two different things can be reproduced. Keep them apart.

| | Pathway A: verify published results | Pathway B: rebuild from raw data |
|---|---|---|
| Starts from | committed feature matrices, saved models, JSON/CSV outputs | original waveforms, StationXML and SED manual picks, downloaded again |
| Needs network | no | yes |
| Needs raw waveforms | no | yes (not on GitHub) |
| Writes to the repository | nothing (read-only) | yes, it overwrites committed files |
| Guarantee | recomputes the published numbers from published artefacts | no guarantee of identical results (section 5) |
| Where | this guide, section 3 | this guide, section 4 and [DATA_ACQUISITION_AND_REPRODUCTION.md](DATA_ACQUISITION_AND_REPRODUCTION.md) |

> **Use a separate clone or branch for Pathway B.** The commands in section 4 overwrite committed artefacts (models, JSON, CSV, figures, feature matrices, manifests). Do not run them in the working copy you want to keep. Work in a throw-away clone (recommended) or at least on a new branch, and never commit or push their output:
>
> ```
> git clone https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning.git amgcr-repro
> cd amgcr-repro
> git switch -c repro-check
> ```
>
> Delete the clone when you are done. Pathway A needs none of this.

All commands assume the **current directory is the repository root**. Three scripts use paths relative to the current directory (`train_random_forest.py`, `train_xgboost.py`, `evaluate_models.py`); the others find the root from their own location. Arguments such as `--config` are resolved against the current directory.

## 1. Environment

- Python 3.11 or newer (`pyproject.toml`). The saved results were produced with Python 3.13 on Windows.
- Only Windows (PowerShell) was used to run the commands in this repository's documentation. The Linux and macOS lines below follow standard Python practice and were **not tested** here.

| Step | Windows (PowerShell) | Linux / macOS (untested) |
|---|---|---|
| Create environment | `python -m venv .venv` | `python3 -m venv .venv` |
| Activate | `.venv\Scripts\Activate.ps1` (may need `Set-ExecutionPolicy -Scope Process RemoteSigned`) | `source .venv/bin/activate` |
| Install | `pip install -r requirements.txt -r requirements-ml.txt` | same |
| Run a script | `python scripts/ml/...` (forward slashes work) | `python scripts/ml/...` |

- `requirements.txt` is the v1.0.0 freeze and does not contain the ML packages. `requirements-ml.txt` adds `scikit-learn==1.9.1`, `xgboost==3.4.1`, `joblib==1.6.0`. Other versions used: numpy 2.5.1, pandas 3.0.5, scipy 1.18.0, obspy 1.5.0, matplotlib 3.11.1, pytest 9.1.1.
- `pip install -e ".[dev,ml]"` is declared in `pyproject.toml` but was **not tested**; use the `requirements` files.
- On macOS, XGBoost wheels may need the OpenMP runtime (`libomp`); see the XGBoost installation notes. Not tested here.
- Website (optional): Node.js 20 or newer; `cd website && npm ci && npm run build`.

## 2. Command safety legend

| Tag | Meaning |
|---|---|
| **RO** | read-only: writes no tracked file. It may create git-ignored `__pycache__` folders |
| **OVERWRITES** | writes to a committed path; run only in a separate clone or branch |
| **NET** | needs network access |

## 3. Pathway A: verify published results (read-only)

No raw waveforms, no network, no retraining. Run from the repository root. Optional first step: `git status --short` (expect no output on a clean clone) and the same command afterwards to confirm nothing changed.

**3.1 Tests (RO).**

```
python -m pytest tests/test_vertical_models.py tests/test_ml_models.py tests/test_swiss_set_a_features.py tests/test_switzerland_set_a_picks.py -q -p no:cacheprovider
```

Run on 2026-11-15: 20 passed (4 + 6 + 7 + 3). A text search found no file-writing calls in these four test files. The full suite (documented as 89/89 in older reports) was not re-run.

**3.2 Recompute the Set C confusion counts from the saved models (RO).** This loads the two frozen vertical models (joblib pickles: load only files from this repository) and applies them to the published Set C feature matrix. Nothing is written. Save as a `.py` file outside the repository, or paste into a Python session started in the repository root:

```python
import json, sys
sys.path.insert(0, ".")
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score
from src.models.vertical_models import (
    SwissVerticalRandomForestModel, SwissVerticalXGBoostModel, VERTICAL_FEATURE_COLUMNS)

df = pd.read_csv("reports/features/swiss_set_c_feature_matrix.csv")
saved = json.load(open("reports/ml/vertical_set_c_evaluation_summary.json"))["models"]
for name, cls, path, key in [
    ("RF", SwissVerticalRandomForestModel, "reports/ml/vertical_rf_model_set_a.joblib", "random_forest_vertical"),
    ("XGB", SwissVerticalXGBoostModel, "reports/ml/vertical_xgb_model_set_a.joblib", "xgboost_vertical")]:
    pred = cls.load(path).predict(df[VERTICAL_FEATURE_COLUMNS])
    tn, fp, fn, tp = confusion_matrix(df["is_earthquake"], pred).ravel()
    s = saved[key]
    print(name, "recomputed TN/FP/FN/TP =", (tn, fp, fn, tp), "| saved =", (s["tn"], s["fp"], s["fn"], s["tp"]),
          "| F1 %.4f vs saved %.4f" % (f1_score(df["is_earthquake"], pred), s["f1_score"]))
```

Result when run on 2026-11-15 with the pinned versions (NumPy 2 prints the recomputed integers as `np.int64(547)` and so on): RF recomputed (547, 3, 86, 464), saved (547, 3, 86, 464), F1 0.9125; XGB recomputed (546, 4, 81, 469), saved (546, 4, 81, 469), F1 0.9169. Working tree unchanged afterwards. Newer scikit-learn or XGBoost versions may fail to load the pickles or predict differently; that is a version issue, not evidence about the science.

**3.3 Read the published outputs (RO).** `reports/ml/vertical_set_c_evaluation_summary.json` (Set C metrics, confusion counts, importances), `vertical_set_a_evaluation_summary.json`, `swiss_ml_evaluation_summary.json`, `vertical_feature_schema.json`, `vertical_set_c_per_event_results.csv`, `reports/data_lineage/data_lineage_summary.json`.

**3.4 What Pathway A does not show.** It does not show that the feature matrices were correctly derived from waveforms. That requires Pathway B.

## 4. Pathway B: rebuild from raw data (OVERWRITES; use a separate clone or branch)

First obtain the raw data, following [DATA_ACQUISITION_AND_REPRODUCTION.md](DATA_ACQUISITION_AND_REPRODUCTION.md) (NET). Then, in the separate clone:

| Step | Command (repository root) | Reads | Writes (all committed paths) | Tag |
|---|---|---|---|---|
| ML-2 Set A features | `python scripts/analysis/run_swiss_set_a_feature_engineering.py` | Set A manifest, Set A picks, `data/raw/switzerland/`, `data/metadata/switzerland/` | `reports/features/swiss_set_a_feature_matrix.csv`, `swiss_set_a_per_record_features.csv`, `swiss_set_a_feature_summary.json`, `reports/features/swiss_figures/fig01` to `fig04` | OVERWRITES |
| ML-3 Random Forest (24 features) | `python scripts/ml/train_random_forest.py` | Set A matrix (path relative to current directory) | `reports/ml/swiss_rf_model.joblib`, `rf_cross_validation_results.json` | OVERWRITES. The saved 24-feature models are frozen |
| ML-3 XGBoost (24 features) | `python scripts/ml/train_xgboost.py` | Set A matrix | `reports/ml/swiss_xgb_model.joblib`, `xgb_cross_validation_results.json` | OVERWRITES. Frozen |
| ML-3 comparison | `python scripts/ml/evaluate_models.py` | Set A matrix; recomputes the 20-fold LOGO CV in memory | `reports/ml/swiss_ml_evaluation_summary.json`, `per_event_cross_validation_results.csv`, `reports/ml/figures/fig01` to `fig04` | OVERWRITES |
| ML-4 vertical training | `python scripts/ml/train_vertical_models_set_a.py` | Set A matrix | `vertical_rf_model_set_a.joblib`, `vertical_xgb_model_set_a.joblib`, `vertical_set_a_evaluation_summary.json`, `vertical_set_a_per_event_cv.csv`, and **also rewrites `vertical_feature_schema.json`** | OVERWRITES |
| ML-4 Set C features | `python scripts/analysis/run_swiss_set_c_feature_engineering.py` | Set C waveform manifest (`MiniSEED_path`, `StationXML_path`, picks), `data/raw/switzerland_validation/`, `data/metadata/switzerland_validation/` | `reports/features/swiss_set_c_feature_matrix.csv`, `swiss_set_c_feature_summary.json` | OVERWRITES |
| ML-4 Set C evaluation | `python scripts/ml/evaluate_vertical_models_set_c.py` | Set C matrix and the two frozen vertical models (no retraining) | `vertical_set_c_evaluation_summary.json`, `vertical_set_c_per_event_results.csv`, `reports/ml/figures/fig05` to `fig08` | OVERWRITES |
| Final figures | `python scripts/reporting/make_final_figures.py` | saved JSON, matrices, one Set A MiniSEED file (Fig. 3 is skipped if absent) | `reports/figures/final/fig01` to `fig12` | OVERWRITES |

These scripts have no command-line options. Order matters: ML-2 before ML-3/ML-4 training, ML-4 Set C features and vertical training before the Set C evaluation. Training uses fixed seeds (42).

## 5. Where Pathway B results may differ

No identical-result guarantee is made.

- New downloads may differ from the original acquisition (catalogue, pick and metadata revisions, service changes, station availability). Details: [DATA_ACQUISITION_AND_REPRODUCTION.md](DATA_ACQUISITION_AND_REPRODUCTION.md) section 7.
- Library versions (scikit-learn, XGBoost, NumPy, ObsPy, SciPy), operating system and CPU thread count can change last digits of features and model internals. Bit-for-bit identity of the saved models was not tested.
- A re-run reproduces the published procedure, including its differences between the Set A and Set C scripts (below). It does not harmonise them.

## 6. What the 45 and 35 matrix columns are

Derived from the CSV headers and `reports/ml/vertical_feature_schema.json`; the snippet in section 6.3 recomputes the split.

| | Set A matrix | Set C matrix |
|---|---|---|
| File | `reports/features/swiss_set_a_feature_matrix.csv` | `reports/features/swiss_set_c_feature_matrix.csv` |
| Rows | 240 windows (120 P-wave + 120 noise) | 1,100 windows (550 + 550) |
| Total columns | **45** | **35** |
| Metadata columns (not model inputs) | **20** | **16** |
| Target label | **1** (`is_earthquake`) | **1** (`is_earthquake`) |
| Engineered features (model inputs) | **24** (the last 24 columns) | **18** (the last 18 columns, in schema order) |

### 6.1 Metadata columns (not features)

- **Set A (20):** `event_id`, `short_id`, `station`, `channel_group`, `sampling_rate_hz`, `magnitude`, `magnitude_type`, `region`, `epicentral_distance_km`, `hypocentral_distance_km`, `origin_time_utc`, `p_pick_time_utc`, `p_latency_s`, `p_phase`, `p_evaluation_mode`, `sample_id`, `window_type`, `window_start_utc`, `window_end_utc`, `window_duration_s`.
- **Set C (16):** `event_id`, `short_id`, `station`, `magnitude`, `magnitude_type`, `region`, `sampling_rate_hz`, `origin_time_utc`, `p_pick_time_utc`, `p_phase`, `p_evaluation_mode`, `sample_id`, `window_type`, `window_start_utc`, `window_end_utc`, `window_duration_s`.
- Set A has four columns Set C lacks: `channel_group`, `epicentral_distance_km`, `hypocentral_distance_km`, `p_latency_s`.
- Roles: identifiers (`event_id`, `short_id`, `station`, `sample_id`; `short_id` is the Leave-One-Group-Out grouping key); event description (`magnitude`, `magnitude_type`, `region`, distances, `origin_time_utc`); pick description (`p_pick_time_utc`, `p_phase`, `p_evaluation_mode`, `p_latency_s`); window description (`window_type`, `window_start_utc`, `window_end_utc`, `window_duration_s`); recording (`sampling_rate_hz`, `channel_group`).
- Several metadata columns encode the label or the pick (`window_type` is equivalent to `is_earthquake`; pick time and `p_latency_s` come from the analyst pick). They must not be used as model inputs. The saved models select their inputs by feature name (`feature_columns` stored inside each `.joblib`), so these columns are excluded.

### 6.2 Target and features

- **Target label:** `is_earthquake`; 1 = early P-wave window (pick to pick + 4 s), 0 = ambient-noise window (origin -35 s to -31 s).
- **Engineered features, Set A (24):** `z_peak_velocity_m_s`, `z_p2p_amplitude_m_s`, `z_rms_velocity_m_s`, `z_variance`, `z_std`, `z_zero_crossing_rate_hz`, `z_signal_energy_m2_s`, `z_crest_factor`, `z_kurtosis`, `z_skewness`, `z_cav_m_s`, `z_dominant_frequency_hz`, `z_spectral_centroid_hz`, `z_spectral_bandwidth_hz`, `z_spectral_rolloff_95_hz`, `z_spectral_entropy`, `h_peak_velocity_m_s`, `h_rms_velocity_m_s`, `vec3c_peak_velocity_m_s`, `vec3c_rms_velocity_m_s`, `vh_ratio`, `sta_lta_max`, `sta_lta_mean`, `snr_db`.
- **Engineered features, Set C (18):** the first 16 above plus `sta_lta_max` and `sta_lta_mean`, in the order of `vertical_feature_schema.json`.
- The 24-feature column order equals the saved 24-feature models' order; the 18-feature order is identical in the schema JSON, `VERTICAL_FEATURE_COLUMNS`, both saved vertical models and Set C inference (verified, see `reports/data_lineage/data_lineage_summary.json`). Definitions and units: [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

### 6.3 Recompute the split (RO)

```python
import json
import pandas as pd
schema = json.load(open("reports/ml/vertical_feature_schema.json"))["features"]
a = pd.read_csv("reports/features/swiss_set_a_feature_matrix.csv", nrows=0).columns.tolist()
c = pd.read_csv("reports/features/swiss_set_c_feature_matrix.csv", nrows=0).columns.tolist()
f24 = a[a.index("z_peak_velocity_m_s"):]
for name, cols, feats in [("Set A", a, f24), ("Set C", c, schema)]:
    meta = [x for x in cols if x not in feats and x != "is_earthquake"]
    print(name, "total", len(cols), "= metadata", len(meta), "+ label 1 + features", len(feats))
print("Set A features are the last 24 columns:", a[-24:] == f24, "| Set C features are the last 18 columns:", c[-18:] == schema)
print("Set C features in schema order:", [x for x in c if x in schema] == schema)
```

Output on 2026-11-15: `Set A total 45 = metadata 20 + label 1 + features 24`, `Set C total 35 = metadata 16 + label 1 + features 18`, and `True` for all three checks.

## 7. Known caveats for reproducers

1. `sta_lta_max/mean` use STA 0.5 s in the Set A script and 1.0 s in the Set C script. The response pre-filter corners also differ between the two scripts. Re-running reproduces the saved results; it does not remove these differences. Their effect is unverified.
2. Both feature scripts apply a zero-phase bandpass to the full trace before windowing. "Causal windows" refers to window placement only.
3. The ML-4 STA/LTA baseline is window-level and differs from the STEP 2K record-level detector (`scripts/analysis/run_swiss_independent_validation.py`).
4. Set C is event-level independent only: all 54 Set A stations also occur in Set C.
5. Joblib files are pickles. Load only files from this repository, and only with the pinned library versions.
6. This is an offline window-classification benchmark, not an operational early-warning system.

## 8. Website

```
cd website
npm ci
npm run build     # copies figures/results into website/public, rebuilds the search index, then runs next build
```

The `/ml-evaluation` page reads the saved JSON/CSV at build time. No model is run in the browser. The build only reads the repository; it writes git-ignored folders under `website/`.
