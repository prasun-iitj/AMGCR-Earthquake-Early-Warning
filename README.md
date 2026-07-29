# AMGCR Earthquake Research

> A research-oriented, test-backed reproduction of the **EarthESND** earthquake early warning methodology (Joshi, Singh, and Raman, *Computers and Electrical Engineering* 135, 2026), using Python, ObsPy, and NumPy/SciPy.

## Project overview

This repository implements the **EarthESND** pipeline described in the project’s reverse-engineering and implementation specifications—not a generic magnitude-prediction prototype. Behaviour is driven by `docs/EARTHESND_REVERSE_ENGINEERING.md` and `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md`.

### Scientific reproducibility philosophy

- **Paper-derived** requirements are traced to the reverse-engineering document (RE).
- Details **not specified in the main paper** stay `null` in YAML, raise `NotImplementedError`, or require an explicit **project assumption**—**no undocumented assumptions implemented as silent defaults**.
- The project uses a **fail-closed** posture: unresolved fields block exact-reproduction claims and blocked APIs until settings are declared.
- **Software implementation is complete**; **scientific reproduction is pending** (data, training runs, table comparison). The project does **not** claim exact replication while required fields remain unresolved or while unavailable supplementary material is missing.
- Automated tests (**88 passing**) guard contracts (shapes, fail-closed config, equation order, metrics, train-only synthetic/ensemble rules).

## Current project status

| Status | Meaning |
|--------|---------|
| **Implementation complete** | Spec build-order gates 1–6 delivered in `src/` with tests |
| **Scientific reproduction pending** | Datasets, parameter resolution, training experiments, and paper benchmarks not yet executed |

### Implementation phases (EarthESND spec)

| Phase | Scope | Status |
|-------|--------|--------|
| 1 | Repository foundation, acquisition framework, data manifest & splits | ✅ Complete |
| 2 | Paper preprocessing pipeline (STA/LTA, gates, filter, integration, windows) | ✅ Complete |
| 3 | Feature engineering schema (seven named vertical features; numeric extraction blocked) | ✅ Complete |
| 4 | Echo State Network (ESN), Eq. 1-style update, spectral-radius scaling | ✅ Complete |
| 5 | DENN readout, fusion, `EarthESNDModel`, CTGAN & ensemble **contracts** | ✅ Complete |
| 6 | Evaluation metrics, benchmarks, timing, experiment metadata | ✅ Complete |

### Blocked by paper (fail-closed in code / YAML)

- Numeric vertical P-wave feature formulas (supplement not in repo).
- STA/LTA window lengths, filter phase, integration policy, station scaling (YAML `null`).
- Serial multiscale **deep** ESN topology (`esn.layer_count`, widths, radii, washout, seed).
- DENN mask construction, local branch nonlinearity, learnable masks (YAML `null`).
- Adam β, ε, weight decay; full `EarthESNDModel.fit` and `EarthESNDTrainer` training loop.
- CTGAN generator/discriminator/training hyperparameters; live tree-model training with default YAML.
- Final seven-way `aggregation_weights` (explicit weights required at runtime).

### Pending reproduction experiments

- Acquire K-NET / PESMOS datasets and populate the manifest.
- Resolve or declare project assumptions for blocked YAML fields.
- Train models (DENN, optional serial ESN stack, CTGAN, ensemble) under deviation log.
- Run Japan test, Noto holdout, and India cross-region evaluation vs published tables.
- Generate tables/figures and final reproducibility report.

**Automated tests:** **88 passing** (`python -m pytest`).

**Documentation version:** **1.0.0** (see `CHANGELOG.md`).

## Architecture overview

```text
Manifest / splits (Japan, Noto, India scopes; M_JMA vs M_w)
      │
      ▼
Preprocessing → (T, 9) waveform tensors + tabular feature schema
      │
      ├──► ESN terminal state ──┐
      │                         ├──► Fusion ──► DENN ──► y_esn
      └──► Tabular features ────┘
      │
      ├──► DENN-CTGAN (train-only contract) ──► augmented tabular
      └──► Tabular ensemble (6 predictors) ──► explicit-weight aggregation
      │
      ▼
Evaluation (MAE, RMSE, % MAE improvement, timing) + run metadata / deviation log
```

Generic FDSN catalogue acquisition exists in parallel; it is **not** the paper’s K-NET study path.

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
| Evaluation | `src/evaluation/` | MAE, RMSE, % improvement, scoped benchmarks, timing |
| Reproducibility | `src/experiments/run_metadata.py` | Metadata, deviation log, exact-run guard |
| EarthESND configs | `configs/earthesnd/*.yaml` | Paper values + intentional `null`s |

## Remaining work (scientific reproduction)

- **Dataset acquisition:** K-NET / PESMOS adapters, full manifest, real waveforms.
- **Parameter resolution:** Declare assumptions for YAML nulls; record in deviation log.
- **Training experiments:** `EarthESNDTrainer`, differentiable DENN + Adam; optional serial multiscale ESN.
- **Orchestration:** `EarthESNDPipeline`, seven-way aggregation with declared weights.
- **Paper reproduction:** Tables 3–6, ablations, baselines (Phase E, RE §15).
- **Features:** Numeric `tau_c`, `ID2`, … only after approved deviation.

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
│   ├── models/
│   ├── evaluation/
│   └── experiments/
├── tests/                  # 88 automated tests
├── pyproject.toml
└── README.md
```

## Technology stack

- Python 3.11+
- ObsPy, NumPy, Pandas, SciPy, Matplotlib, PyYAML
- pytest (dev)

Install: `pip install -e ".[dev]"`

## Development roadmap

1. ✅ Foundation, preprocessing, features (schema), ESN, DENN, fusion, model wrapper, synthetic/ensemble contracts, evaluation & reproducibility  
2. ⬜ Declare project assumptions for blocked YAML fields where reproduction runs are needed  
3. ⬜ K-NET-scale data path and feature numerics (with deviation log)  
4. ⬜ DENN training + optional serial multiscale ESN + full pipeline  
5. ⬜ Train models, compare to published tables, final reproducibility report  

See `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md` (build order) and `docs/EARTHESND_REVERSE_ENGINEERING.md` §17–§18.

## Verification

Run the full suite from the repository root:

```bash
python -m pytest
```

Expected: **88 passed**.

## Key documents

- `docs/EARTHESND_REVERSE_ENGINEERING.md` — evidence-bound paper specification  
- `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md` — implementation authority and progress  
- `CHANGELOG.md` — milestone history  
- `docs/PAPER_REPRODUCTION.md` — reproduction strategy  
- `docs/PROJECT_STATUS.md` — implementation vs reproduction status  
