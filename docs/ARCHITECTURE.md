# ARCHITECTURE.md

# AMGCR Earthquake Research - Project Architecture

## Purpose

This document describes the high-level architecture of the AMGCR Earthquake
Research project and how data flows through the system.

---

# Architecture Overview

```
FDSN Services
      │
      ▼
Event Retrieval (ObsPy)
      │
      ▼
Waveform Download
      │
      ▼
Station Metadata
      │
      ▼
Raw Data Storage
      │
      ▼
Preprocessing
      │
      ▼
Feature Extraction
      │
      ▼
Visualisation
      │
      ▼
Machine Learning / Analysis
      │
      ▼
Results & Reports
```

---

# Core Components

## 1. Data Acquisition
- Retrieve earthquake event catalogues.
- Download waveform data.
- Collect station metadata.

## 2. Data Storage
- `data/raw/` for original files.
- `data/processed/` for cleaned datasets.
- `data/output/` for final results.

## 3. Processing Pipeline
- Detrending
- Filtering
- Quality checks
- Feature extraction

## 4. Analysis
- Statistical analysis
- Visualisation
- Research paper reproduction
- Machine learning experiments

## 5. Documentation
- Record experiments.
- Update decision log.
- Maintain changelog.

---

# Design Principles

- Modular
- Reproducible
- Well-documented
- Extensible
- Research-focused

---

Version: **1.0.0**
