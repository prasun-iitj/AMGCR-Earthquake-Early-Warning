# ML Reproduction Guide (STEP ML-1A to ML-4)

What a reviewer can run, what it needs, and what it writes. All commands run from the repository root.

> **Warning.** The training, extraction and evaluation scripts **overwrite** the committed artifacts in `reports/ml/` and `reports/features/`. To inspect results without changing anything, read the saved JSON/CSV files instead (section 3). To re-run, work in a copy or a separate branch.

## 1. Environment

- Python 3.11 or newer (results were produced with Python 3.13).
- Install:

```powershell
python -m venv .venv
.venv\Scripts\activate          # Windows; use `source .venv/bin/activate` on Linux/macOS
pip install -r requirements.txt -r requirements-ml.txt
```

`requirements.txt` is the v1.0.0 freeze and does not contain the ML packages; `requirements-ml.txt` adds `scikit-learn==1.9.1`, `xgboost==3.4.1`, `joblib==1.6.0`. Other versions used: numpy 2.5.1, pandas 3.0.5, scipy 1.18.0, obspy 1.5.0, matplotlib 3.11.1, pytest 9.1.1. Alternative: `pip install -e ".[dev,ml]"`.

Website (optional): Node.js 20 or newer; `cd website && npm ci && npm run build`.

## 2. Data

Raw MiniSEED and StationXML are **not** in the repository (`data/raw/` and `data/metadata/**/*.xml` are git-ignored). Manifests in `data/manifests/` are tracked.

| Need | Command | Source |
|---|---|---|
| Set A waveforms (20 events, 120 records) | `python scripts/download/download_sed_switzerland_pilot.py` | SED/ETH FDSN (`eida.ethz.ch`) |
| Set A analyst picks | `python scripts/download/download_sed_switzerland_set_a_picks.py` | SED QuakeML |
| Set C waveforms (15 events, 550 records) | `python scripts/download/download_sed_switzerland_validation.py` | SED/ETH FDSN |

Needs network access. Downloads are public; no credentials are required. Re-downloading may return slightly different data if the SED catalogue is revised. Do not change Set C membership.

## 3. Verify without re-running (fast, read-only)

```powershell
python -m pytest tests/test_vertical_models.py tests/test_ml_models.py tests/test_swiss_set_a_features.py tests/test_switzerland_set_a_picks.py -q
```

Run for this package on 2026-11-15 (system clock): **20 passed** (4 + 6 + 7 + 3 tests). These tests read the saved artifacts and feature matrices. The full suite (documented as 89/89 in earlier reports) was **not** re-run for this package. Also read:

- `reports/ml/vertical_set_c_evaluation_summary.json` (Set C metrics, confusion counts, importances)
- `reports/ml/vertical_set_a_evaluation_summary.json`, `reports/ml/swiss_ml_evaluation_summary.json`
- `reports/ml/vertical_feature_schema.json`

## 4. Re-run the pipeline (overwrites artifacts)

| Step | Command | Reads | Writes |
|---|---|---|---|
| ML-2 Set A features | `python scripts/analysis/run_swiss_set_a_feature_engineering.py` | Set A manifest, picks, `data/raw/switzerland/`, StationXML | `reports/features/swiss_set_a_feature_matrix.csv` (240 x 45), per-record CSV, summary JSON, 4 figures |
| ML-3 RF / XGB (24 features) | `python scripts/ml/train_random_forest.py`, `python scripts/ml/train_xgboost.py`, `python scripts/ml/evaluate_models.py` | Set A feature matrix | `reports/ml/swiss_rf_model.joblib`, `swiss_xgb_model.joblib`, CV JSON, figures. **Frozen; do not overwrite.** |
| ML-4 Set A vertical models | `python scripts/ml/train_vertical_models_set_a.py` | Set A feature matrix | `vertical_rf_model_set_a.joblib`, `vertical_xgb_model_set_a.joblib`, Set A summary JSON, per-event CV CSV |
| ML-4 Set C features | `python scripts/analysis/run_swiss_set_c_feature_engineering.py` | Set C manifest, `data/raw/switzerland_validation/` | `reports/features/swiss_set_c_feature_matrix.csv` (1,100 x 35) |
| ML-4 Set C evaluation | `python scripts/ml/evaluate_vertical_models_set_c.py` | Set C matrix, frozen vertical models | `vertical_set_c_evaluation_summary.json`, per-event CSV, `fig05` to `fig08` |
| Final figures | `python scripts/reporting/make_final_figures.py` | Saved JSON and feature matrices, one Set A MiniSEED file (Fig. 3) | `reports/figures/final/fig01` to `fig12` |

Training uses fixed seeds (42). Exact bit-for-bit reproduction of the saved models depends on library versions (section 1).

## 5. Known caveats for reproducers

1. `sta_lta_max/mean` use STA 0.5 s in the Set A script and 1.0 s in the Set C script. Re-running reproduces the saved results; it does not remove the mismatch. Its effect is unverified.
2. Feature scripts apply a zero-phase bandpass to the full trace before windowing.
3. The ML-4 STA/LTA baseline is window-level and differs from the STEP 2K record-level detector (`scripts/analysis/run_swiss_independent_validation.py`).
4. Joblib files are pickles. Load only files from this repository, and only with the pinned library versions.

## 6. Website

```powershell
cd website
npm ci
npm run build     # syncs figures/results, rebuilds the search index, then next build
```

The `/ml-evaluation` page reads the saved JSON/CSV at build time. No model is run in the browser.
