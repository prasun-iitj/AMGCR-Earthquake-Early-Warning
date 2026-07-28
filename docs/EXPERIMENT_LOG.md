# EXPERIMENT_LOG.md

# AMGCR Earthquake Research - Experiment Log

## Purpose

This document records every experiment performed during the project to ensure that results are reproducible and easy to review.

---

# Experiment Record

## Experiment ID

EXP-001

### Title

Sample earthquake catalogue retrieval with ObsPy

### Date

2026-07-29

### Objective

Verify that the acquisition framework can retrieve an earthquake catalogue from a real FDSN-compatible service and save it to the project data directory.

### Dataset

- Source: USGS event service via ObsPy FDSN client
- Time range: 2024-01-01 to 2024-01-02
- Number of events: 10
- Number of stations: not applicable for this catalogue-only run

### Software Environment

- Python: 3.11+
- ObsPy: installed in the project virtual environment
- Operating System: Windows
- Git Commit: not yet recorded

### Method

Configured the acquisition client from the YAML settings, ran the retrieval workflow, and saved the QuakeML output to the raw catalog directory.

### Parameters

- Provider: https://earthquake.usgs.gov
- Minimum magnitude: 4.0
- Maximum magnitude: 8.0
- Limit: 10

### Results

The retrieval completed successfully and wrote a QuakeML file to data/raw/catalogs/catalog.xml.

### Conclusion

The objective was achieved and the workflow is now validated for a live catalogue retrieval path.

### Next Steps

Proceed to waveform and station metadata acquisition.

---

# Experiment Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| EXP-001 | Sample earthquake catalogue retrieval with ObsPy | Completed | 2026-07-29 |

---

# Best Practices

- Record experiments immediately after completion.
- Do not overwrite previous results.
- Reference generated figures and reports.
- Link related code modules where applicable.

---

Version: **0.3.0**
