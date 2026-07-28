# ROADMAP.md

# AMGCR Earthquake Research - Development Roadmap

## Purpose

This document defines the complete development plan for the AMGCR Earthquake Research project.

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
- requirements.txt
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

⬜ Planned

## Objectives
- Download MiniSEED waveform files
- Download StationXML metadata
- Organise data by event and station

### Deliverables
- Waveform downloader
- Station metadata

---

# Phase 4 — Signal Preprocessing

## Status

⬜ Planned

## Objectives
- Detrend signals
- Remove noise
- Apply filters
- Trim waveform windows
- Normalise data

### Deliverables
- Clean waveform dataset

---

# Phase 5 — Visualisation

## Status

⬜ Planned

## Objectives
- Plot waveforms
- Plot earthquake locations
- Generate summary statistics

### Deliverables
- Publication-ready figures

---

# Phase 6 — Feature Extraction

## Status

⬜ Planned

## Objectives
- Extract waveform features
- Prepare ML-ready datasets

### Deliverables
- Feature matrices

---

# Phase 7 — Research Reproduction

## Status

⬜ Planned

## Objectives
- Reproduce the methodology from the selected reference paper
- Compare results
- Document findings

### Deliverables
- Reproducible experiments

---

# Phase 8 — AI / ML Extension

## Status

⬜ Planned

## Objectives
- Develop baseline ML models
- Evaluate performance
- Document improvements

### Deliverables
- Experimental models
- Final report

---

# Milestone Summary

| Milestone | Status |
|-----------|--------|
| Environment | ✅ |
| Event Retrieval | ✅ |
| Waveforms | ⬜ |
| Preprocessing | ⬜ |
| Visualisation | ⬜ |
| Feature Extraction | ⬜ |
| Research Reproduction | ⬜ |
| AI/ML Extension | ⬜ |

---

Version: **0.3.0**
