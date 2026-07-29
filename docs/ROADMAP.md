# ROADMAP.md

# AMGCR Earthquake Research - Development Roadmap

## Purpose

This document defines the development plan for the AMGCR Earthquake Research project.

**EarthESND software (spec phases 1–6):** ✅ **Implementation complete**  
**Scientific reproduction:** ⬜ **Pending**  
**Automated tests:** **88 passing**

---

# EarthESND track (primary)

| Phase | Scope | Status |
|-------|--------|--------|
| 1 | Repository foundation, manifest, splits | ✅ Complete |
| 2 | Preprocessing | ✅ Complete |
| 3 | Feature engineering (schema) | ✅ Complete |
| 4 | Echo State Network | ✅ Complete |
| 5 | DENN, EarthESNDModel, CTGAN & ensemble contracts | ✅ Complete |
| 6 | Evaluation & reproducibility | ✅ Complete |
| — | Dataset acquisition, training, paper benchmarks | ⬜ Scientific reproduction |

---

# Phase 1 — Environment Setup

## Status

✅ Completed

## Objectives

- Create project structure
- Create Python virtual environment
- Install required libraries
- Verify ObsPy installation
- Configure Git repository

### Deliverables

- Working development environment
- `pyproject.toml` / editable install
- Initial documentation

---

# Phase 2 — Earthquake Event Retrieval

## Status

✅ Completed

## Objectives

- Connect to FDSN services
- Build an acquisition framework for future downloads
- Retrieve earthquake catalogues
- Save QuakeML files

### Deliverables

- Acquisition framework
- Sample event catalogue dataset

### Submilestones

- Phase 2A — Acquisition framework preparation: ✅ Completed
- Phase 2B — Sample catalogue retrieval: ✅ Completed

---

# Phase 3 — Waveform Acquisition

## Status

⬜ Pending (scientific reproduction — K-NET / PESMOS)

## Objectives

- Download study strong-motion records (three components)
- Station metadata and scaling provenance
- Organise data by event and station

### Deliverables

- Source-specific adapters and populated manifest

---

# Phase 4 — Signal Preprocessing

## Status

✅ Completed (EarthESND pipeline in `src/preprocessing/`)

## Objectives

- Paper STA/LTA, gates, baseline, bandpass, integration hooks, P-wave windows
- Fail-closed on unresolved operational YAML fields

### Deliverables

- `(T, 9)` window tensors (unit tested)

---

# Phase 5 — Visualisation

## Status

⬜ Planned

## Objectives

- Plot waveforms and diagnostics
- Publication-ready figures for reproduction report

### Deliverables

- Figures aligned with paper where applicable

---

# Phase 6 — Feature Extraction

## Status

✅ Schema complete; numeric extraction blocked until approved deviation

## Objectives

- Seven named vertical P-wave features
- ML-ready tabular matrices when formulas are declared

### Deliverables

- Feature matrices with deviation log

---

# Phase 7 — Research Reproduction

## Status

⬜ Pending (software ready; experiments not run)

## Objectives

- Train EarthESND and ensemble path under declared assumptions
- Compare results to EarthESND paper (Tables 3–6)
- Document findings and gaps

### Deliverables

- Reproducibility report and deviation log

---

# Phase 8 — AI / ML Extension

## Status

⬜ Planned

## Objectives

- Additional baselines or extensions beyond paper scope
- Document improvements

### Deliverables

- Experimental models (optional)

---

# Milestone Summary

| Milestone | Status |
|-----------|--------|
| Environment | ✅ |
| Event Retrieval | ✅ |
| EarthESND preprocessing & models | ✅ |
| EarthESND evaluation & metadata | ✅ |
| Waveforms (study scale) | ⬜ Reproduction |
| Visualisation | ⬜ |
| Feature numerics | ⬜ Blocked / deviation |
| Research Reproduction (paper tables) | ⬜ |
| AI/ML Extension | ⬜ |

---

Version: **1.0.0**
