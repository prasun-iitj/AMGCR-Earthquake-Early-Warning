# PROJECT_STATUS.md

# AMGCR Earthquake Research - Project Status

## Purpose

This document tracks progress for the **EarthESND** paper reproduction effort. Authority for requirements remains `docs/EARTHESND_REVERSE_ENGINEERING.md` and `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md`.

---

## Project information

**Project name:** AMGCR_Earthquake_Research  

**Current focus:** Evaluation, training orchestration, and dataset acquisition (post–core architecture)  

**Automated tests:** **65 passing** (`python -m pytest`)  

**Documentation version:** **0.5.0**

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
| K-NET / PESMOS waveform acquisition | ⬜ Pending |
| DENN training / EarthESNDTrainer | ⬜ Pending |
| Serial multiscale deep ESN | ⬜ Pending |
| Evaluation & paper table comparison | ⬜ Pending |
| Visualisation & notebooks | ⬜ Planned |

---

## Completed milestones

- [x] Repository structure, `pyproject.toml`, pytest suite  
- [x] Acquisition framework and sample FDSN catalogue retrieval  
- [x] `configs/earthesnd/*` with paper values and intentional nulls  
- [x] Preprocessing pipeline with fail-closed unresolved settings  
- [x] ESN, DENN, fusion, `EarthESNDModel`  
- [x] CTGAN, ensemble, and aggregation contracts  

---

## Pending / blocked

- [ ] Declare project assumptions for blocked YAML fields before reproduction runs  
- [ ] Implement evaluation module and experiment metadata  
- [ ] Implement full Adam DENN training and optional serial ESN stack  
- [ ] K-NET-compatible data path and numeric feature formulas (with deviation log)  
- [ ] Full pipeline orchestration and seven-way aggregation with declared weights  

---

## Current goal

Complete **spec build-order gate 6 (evaluation)** and dataset acquisition without inventing undocumented paper details.

---

Version: **0.5.0**
