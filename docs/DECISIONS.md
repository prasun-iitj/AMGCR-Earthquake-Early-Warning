# DECISIONS.md

# AMGCR Earthquake Research - Decision Log

## Purpose

This document records important technical and research decisions made during the project, along with the reasoning behind them.

---

## Decision Log

### DEC-001
**Decision:** Use Python as the primary programming language.

**Reason:** Strong ecosystem for scientific computing and excellent support through ObsPy.

---

### DEC-002
**Decision:** Use ObsPy for earthquake data acquisition and processing.

**Reason:** It is the standard open-source library for seismology research.

---

### DEC-003
**Decision:** Use a project-specific virtual environment (`.venv`).

**Reason:** Ensures reproducibility and isolates project dependencies.

---

### DEC-004
**Decision:** Maintain all documentation in Markdown.

**Reason:** Compatible with GitHub, Cursor, Kiro and other AI coding assistants.

---

### DEC-005
**Decision:** Use a structured src/ package layout with separate modules for acquisition, preprocessing, processing, analysis, visualization, models, and utilities.

**Reason:** Keeps the research workflow modular and easier to extend as the project evolves.

---

### DEC-006
**Decision:** Centralise logging and project settings through dedicated configuration modules.

**Reason:** Improves maintainability and makes the repository easier to run and debug.

---

### DEC-007
**Decision:** Build the acquisition workflow as a configuration-driven framework before any network access is implemented.

**Reason:** Keeps the repository modular, testable, and safe while preparing for future actual downloads.

---

### DEC-008
**Decision:** Use a provider-aware retrieval strategy for event catalogues.

**Reason:** Observed service differences across FDSN endpoints, including the USGS event service rejecting network-based filters; the workflow now adapts the request to the active provider.

---

## Future Decisions

Record all major architectural, dataset, preprocessing and modelling decisions here.

---

Version: **0.3.0**
