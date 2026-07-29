# PROJECT_STATUS.md

# AMGCR Earthquake Research - Project Status

## Purpose

This document tracks progress for the **EarthESND** paper reproduction effort. Authority for requirements remains `docs/EARTHESND_REVERSE_ENGINEERING.md` and `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md`.

---

## Project information

**Project name:** AMGCR_Earthquake_Research  

**Software implementation:** **COMPLETE** (EarthESND spec phases 1–6)  

**Current stage:** **Scientific reproduction** (datasets, training, benchmarks—not yet executed)  

**Reproduction claim:** **Pending** — no exact paper match while YAML null fields and missing supplement details remain  

**Automated tests:** **88 passing** (`python -m pytest`)  

**Documentation version:** **1.0.0**

---

## Implementation phases (spec)

| Phase | Scope | Status |
|-------|--------|--------|
| 1 | Repository foundation, manifest, splits, acquisition framework | ✅ Complete |
| 2 | Preprocessing | ✅ Complete |
| 3 | Feature engineering (schema; numerics blocked) | ✅ Complete |
| 4 | Echo State Network (ESN) | ✅ Complete |
| 5 | DENN, EarthESNDModel, CTGAN & ensemble contracts | ✅ Complete |
| 6 | Evaluation & reproducibility | ✅ Complete |

---

## Overall progress

| Area | Status |
|------|--------|
| Repository foundation & generic acquisition | ✅ Completed |
| EarthESND data manifest & splits | ✅ Completed |
| EarthESND preprocessing | ✅ Completed |
| Feature schema (seven names; numerics blocked) | ✅ Completed |
| Echo State Network (ESN) | ✅ Completed |
| DENN readout & fusion | ✅ Completed |
| EarthESNDModel (`predict`; `fit` blocked) | ✅ Completed |
| CTGAN & tabular ensemble contracts | ✅ Completed |
| Evaluation metrics, benchmarks, timing & run metadata | ✅ Completed |
| End-to-end paper reproduction (tables, timing parity) | ⬜ Scientific reproduction pending |
| K-NET / PESMOS waveform acquisition | ⬜ Pending (reproduction) |
| DENN training / EarthESNDTrainer | ⬜ Pending (reproduction) |
| Serial multiscale deep ESN | ⬜ Pending (reproduction / optional stack) |
| Full pipeline orchestration | ⬜ Pending (reproduction) |
| Visualisation & notebooks | ⬜ Planned |

---

## Completed milestones (software)

- [x] Repository structure, `pyproject.toml`, pytest suite (**88** tests)  
- [x] Acquisition framework and sample FDSN catalogue retrieval  
- [x] `configs/earthesnd/*` with paper values and intentional nulls  
- [x] Preprocessing pipeline with fail-closed unresolved settings  
- [x] ESN, DENN, fusion, `EarthESNDModel`  
- [x] CTGAN, ensemble, and aggregation contracts  
- [x] Evaluation (`src/evaluation/*`) and experiment metadata (`src/experiments/run_metadata.py`)  

---

## Scientific reproduction (remaining)

- [ ] Acquire datasets (K-NET, PESMOS) and populate manifest  
- [ ] Resolve undocumented paper parameters or record project assumptions  
- [ ] Train models (DENN, CTGAN, ensemble) under deviation log  
- [ ] Generate tables/figures aligned with paper  
- [ ] Compare metrics with published results (Japan, Noto, India scopes)  
- [ ] Final reproducibility report  

---

## Fail-closed philosophy (unchanged)

- No undocumented assumptions implemented as code or YAML defaults for paper-unspecified fields.  
- Blocked APIs and `null` config fields remain until explicitly declared for reproduction runs.  

---

## Current goal

Execute **scientific reproduction** on top of the completed implementation: data, assumptions register, training experiments, and benchmark comparison—without claiming exact replication while unresolved nulls remain.

---

Version: **1.0.0**
