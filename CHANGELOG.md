# Changelog

All notable changes to this project are documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/).  
**Current version:** **1.0.0** (EarthESND software implementation complete; **88** automated tests passing; scientific reproduction pending).

---

## [1.0.0] - EarthESND implementation complete

### Added

- **Phase 6 — Evaluation & reproducibility:** MAE, RMSE, percentage MAE improvement, scoped benchmarks (Japan test, Noto holdout, India cross-region), training seconds/epoch timing helper (`src/evaluation/`).
- **Experiment metadata:** `ExperimentMetadata`, deviation log persistence, exact-reproduction guard for unresolved YAML nulls (`src/experiments/run_metadata.py`).
- Unit tests: `tests/test_earthesnd_evaluation.py`.

### Summary (full EarthESND software stack)

- Complete EarthESND implementation through spec build-order gate 6.
- Echo State Network (ESN) with spectral-radius scaling and terminal-state readout.
- Dendritic Neural Network (DENN) readout and ESN–tabular fusion.
- `EarthESNDModel` forward path (`predict()`; training blocked until declared Adam settings).
- DENN-CTGAN and tabular ensemble **contracts** (train-only guards, six predictors, explicit aggregation weights).
- Evaluation framework and reproducibility framework (fail-closed; no cross-scale metric mixing).
- **88** automated tests passing (`python -m pytest`).

### Documentation

- README, implementation spec, reverse engineering §17–§18, PROJECT_STATUS, PAPER_REPRODUCTION, IMPLEMENTATION_PLAN, ARCHITECTURE, ROADMAP aligned with **implementation complete / reproduction pending**.

### Reproducibility note

Scientific reproduction (datasets, training runs, paper table comparison) remains **pending**. No exact paper claim while spec-mandated YAML fields remain `null` or supplementary details are missing.

---

## [0.5.0] - EarthESND core architecture and contracts

### Added

- **Dendritic Neural Network (DENN):** masked branch readout, GELU/linear two-layer structure (`src/models/dendritic.py`).
- **ESN → DENN fusion:** `concatenate_terminal_state_and_features` (`src/processing/fusion.py`).
- **EarthESNDModel:** ESN terminal state + tabular fusion + DENN `predict()`; config loader (`src/models/earthesnd.py`, `earthesnd_config.py`).
- **CTGAN contract:** train-only DENN-CTGAN wrapper, 10 000 synthetic row enforcement (`src/models/denn_ctgan.py`).
- **Synthetic / ensemble contracts:** augmented tabular union, six tabular predictors, explicit-weight aggregation (`src/models/tabular_ensemble.py`, `tabular_data.py`, `aggregation.py`).
- Unit tests: `tests/models/test_dendritic.py`, `test_earthesnd.py`, `test_synthetic_ensemble.py`.

### Verification

- **65** automated tests passing (`python -m pytest`).

---

## [0.4.0] - EarthESND preprocessing, features, and ESN

### Added

- EarthESND preprocessing pipeline (STA/LTA, quality gate, baseline, Butterworth bandpass, integration hooks, P-wave windows).
- Seven-name vertical feature schema with blocked numeric extraction.
- Echo State Network with spectral-radius scaling and terminal-state readout.
- Data manifest and magnitude-stratified splits; `configs/earthesnd/*.yaml`.

---

## [0.3.0] - Phase 2B catalogue retrieval

### Added

- Configuration-driven event catalogue retrieval with ObsPy.
- Provider-aware FDSN query shaping; sample QuakeML under `data/raw/catalogs/`.

---

## [0.2.0] - Phase 2A acquisition framework

### Added

- Modular `src/acquisition` package, YAML config loader, validators, tests.

---

## [0.1.0] - Phase 1 initialization

### Added

- Repository structure, `pyproject.toml` dependencies, logging, initial tests.

---

## Guidelines

Record meaningful milestones: features, tests, documentation, and reproducibility status. Do not claim exact paper reproduction while spec-mandated fields remain unresolved.
