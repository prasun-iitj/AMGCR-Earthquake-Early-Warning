# AMGCR Earthquake Research

> A research-oriented implementation of an Earthquake Early Warning System (EEWS) using Python, ObsPy, and Machine Learning.

## Project Overview

AMGCR (Assessment and Management of Geological and Climate Related Risk) is a research project focused on understanding earthquakes through seismic waveform analysis and building a reproducible Earthquake Early Warning workflow.

## Objectives

- Learn earthquake science from the fundamentals.
- Download real earthquake data from FDSN services.
- Process seismic waveforms using ObsPy.
- Visualize and analyse earthquake signals.
- Extract meaningful features.
- Reproduce research methodologies.
- Build an AI-ready and reproducible research pipeline.

## Repository Structure

```text
AMGCR_Earthquake_Research/
├── data/
├── docs/
├── literature/
├── notebooks/
├── outputs/
├── src/
├── tests/
├── README.md
├── requirements.txt
└── .gitignore
```

## Technology Stack

- Python 3.11+
- ObsPy
- NumPy
- Pandas
- Matplotlib
- SciPy
- PyYAML
- Git & GitHub

## Current Status

**Phase 2B – Earthquake catalogue retrieval completed**

### Implemented so far

- Repository initialization and environment setup
- Modular acquisition framework with YAML-based configuration
- ObsPy-based event catalogue retrieval and validation
- Sample QuakeML output saved to data/raw/catalogs/catalog.xml
- Automated tests covering the acquisition workflow

### Next focus

- Waveform acquisition and station metadata retrieval
- Preprocessing and first exploratory visualisations

## Verification

The acquisition workflow is currently verified by the automated test suite and a successful sample retrieval run.

## Version

**v0.3.0**
