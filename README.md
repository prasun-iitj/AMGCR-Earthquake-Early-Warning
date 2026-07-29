# AMGCR Earthquake Research

> A research-oriented, test-backed reproduction of the **EarthESND** earthquake early warning methodology (Joshi, Singh, and Raman, *Computers and Electrical Engineering* 135, 2026), using Python, ObsPy, and NumPy/SciPy.

## Project overview

This repository implements the **EarthESND** pipeline described in the project’s reverse-engineering and implementation specifications—not a generic magnitude-prediction prototype. Behaviour is driven by `docs/EARTHESND_REVERSE_ENGINEERING.md` and `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md`.

### Scientific reproducibility philosophy

- **Paper-derived** requirements are traced to the reverse-engineering document (RE).
- Details **not specified in the main paper** stay `null` in YAML, raise `NotImplementedError`, or require an explicit **project assumption**—never silent defaults presented as reproduction.
- The project does **not** claim exact replication while required fields remain unresolved or while the unavailable supplementary material is missing.
- Automated tests guard contracts (shapes, fail-closed config, equation order, train-only synthetic/ensemble rules).

## Current project status

**EarthESND core architecture and contracts are implemented; end-to-end training, K-NET-scale data, and evaluation are not.**

| Phase | Scope | Status |
|-------|--------|--------|
| 1 | Repository foundation, acquisition framework, data manifest & splits | ✅ Complete |
| 2 | Paper preprocessing pipeline (STA/LTA, gates, filter, integration, windows) | ✅ Complete |
| 3 | Feature engineering schema (seven named vertical features; numeric extraction blocked) | ✅ Complete |
| 4 | Echo State Network (ESN), Eq. 1-style update, spectral-radius scaling | ✅ Complete |
| 5 | DENN readout, ESN→DENN fusion, `EarthESNDModel`, CTGAN & ensemble **contracts** | ✅ Complete |
| 6 | Evaluation metrics, benchmarks, timing, experiment metadata | ⬜ Pending |
| — | Full Adam DENN training, serial multiscale deep ESN, K-NET/PESMOS acquisition | ⬜ Pending / blocked |

**Automated tests:** **65 passing** (`python -m pytest`).

**Documentation version:** **0.5.0** (see `docs/CHANGELOG.md`).

## Implemented modules

| Area | Location | Notes |
|------|-----------|--------|
| Acquisition (generic FDSN) | `src/acquisition/` | Catalogue client; waveform/station placeholders |
| Data contracts | `src/data/manifest.py`, `splits.py` | Manifest, stratified 70:15:15 splits |
| Preprocessing | `src/preprocessing/` | Fail-closed on null STA/LTA windows, filter phase, integration policy |
| Features | `src/processing/features.py` | Seven-feature schema; formulas blocked |
| Fusion | `src/processing/fusion.py` | `C = [h_T \| Tab_mag]` |
| ESN | `src/models/esn.py` | Single-reservoir forward; terminal state |
| DENN | `src/models/dendritic.py` | Masked branches; 64/GELU → 1/linear |
| EarthESND predictor | `src/models/earthesnd.py`, `earthesnd_config.py` | `predict()`; `fit()` blocked until Adam details declared |
| CTGAN contract | `src/models/denn_ctgan.py` | Train-only; 10 000 rows; architecture blocked |
| Tabular ensemble | `src/models/tabular_ensemble.py`, `tabular_data.py` | Six predictors; hyperparameters blocked |
| Aggregation | `src/models/aggregation.py` | Explicit weights only (no implicit 1/7) |
| EarthESND configs | `configs/earthesnd/*.yaml` | Paper values + intentional `null`s |

## Remaining work

- **Evaluation:** MAE, RMSE, percent MAE improvement, timing (`src/evaluation/` per spec).
- **Training:** Differentiable DENN + Adam loop; `EarthESNDTrainer` (MSE / 50 epochs / batch 512).
- **Architecture:** Serial multiscale deep ESN while `esn.layer_count` and related fields are null.
- **Features:** Numeric `tau_c`, `ID2`, … only after approved deviation (supplement not in repo).
- **Data:** K-NET / PESMOS adapters, full manifest population, Noto/India holdouts on real waveforms.
- **Orchestration:** `EarthESNDPipeline`, full seven-way aggregation with declared weights.
- **Baselines & paper tables:** Phase E in RE §15 (Tables 3–6).

## Repository structure

```text
AMGCR_Earthquake_Research/
├── configs/
│   ├── acquisition_config.yaml
│   ├── settings.yaml
│   └── earthesnd/          # data, preprocessing, model, synthetic_ensemble, evaluation
├── data/                   # raw / processed stores (local data not in git)
├── docs/                   # specifications, status, changelog
├── references/papers/      # EarthESND PDF and notes
├── src/
│   ├── acquisition/
│   ├── data/
│   ├── preprocessing/
│   ├── processing/
│   └── models/
├── tests/                  # 65 automated tests
├── pyproject.toml
└── README.md
```

## Technology stack

- Python 3.11+
- ObsPy, NumPy, Pandas, SciPy, Matplotlib, PyYAML
- pytest (dev)

Install: `pip install -e ".[dev]"`

## Development roadmap

1. ✅ Foundation, preprocessing, features (schema), ESN, DENN, fusion, model wrapper, synthetic/ensemble contracts  
2. ⬜ Declare project assumptions for blocked YAML fields where reproduction runs are needed  
3. ⬜ DENN training + optional serial multiscale ESN  
4. ⬜ K-NET-scale data path and feature numerics (with deviation log)  
5. ⬜ Evaluation, full pipeline, comparison to published tables  

See `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md` (build order) and `docs/EARTHESND_REVERSE_ENGINEERING.md` §15–§17.

## Verification

Run the full suite from the repository root:

```bash
python -m pytest
```

Expected: **65 passed**.

## Key documents

- `docs/EARTHESND_REVERSE_ENGINEERING.md` — evidence-bound paper specification  
- `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md` — implementation authority and progress  
- `docs/CHANGELOG.md` — milestone history  
- `docs/PAPER_REPRODUCTION.md` — reproduction strategy  
