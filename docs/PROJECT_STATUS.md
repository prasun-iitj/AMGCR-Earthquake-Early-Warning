# PROJECT_STATUS.md

# AMGCR Earthquake Research - Project Status

## Purpose

This document tracks the current progress, completed milestones, pending tasks, blockers, and upcoming work for the project.

---

# Project Information

**Project Name:** AMGCR_Earthquake_Research

**Current Phase:** Phase 2B – Earthquake Event Catalogue Retrieval (Completed)

**Current Status:** Repository foundation and acquisition workflow are implemented and validated.

---

# Overall Progress

| Area | Status |
|------|--------|
| Environment Setup | ✅ Completed |
| Acquisition Framework (Phase 2A) | ✅ Completed |
| Event Catalogue Retrieval (Phase 2B) | ✅ Completed |
| Waveform Acquisition | ⬜ Planned |
| Signal Preprocessing | ⬜ Planned |
| Visualisation | ⬜ Planned |
| Feature Extraction | ⬜ Planned |
| Research Reproduction | ⬜ Planned |
| AI / ML Extension | ⬜ Planned |

---

# Completed

- [x] Repository structure created and organised
- [x] Virtual environment created and validated
- [x] Core scientific dependencies verified
- [x] ObsPy installation verified
- [x] Initial package structure created inside src/
- [x] Logging configuration added
- [x] Acquisition configuration loader implemented
- [x] Validators and custom exceptions added
- [x] Acquisition tests added and passing
- [x] Configuration-driven catalogue retrieval implemented
- [x] Sample catalogue retrieval completed using an ObsPy/FDSN client
- [x] Sample QuakeML output written to data/raw/catalogs/catalog.xml

---

# Pending Tasks

- [ ] Download station metadata and waveform data
- [ ] Build a waveform acquisition workflow
- [ ] Plot the first waveform
- [ ] Start preprocessing and feature extraction
- [ ] Reproduce a reference methodology

---

# Current Goal

Maintain a documented, test-backed foundation for the next phase of waveform-based analysis.

---

Version: **0.3.0**
