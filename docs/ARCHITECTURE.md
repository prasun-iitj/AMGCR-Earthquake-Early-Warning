# ARCHITECTURE.md

# AMGCR Earthquake Research - Project Architecture

## Purpose

This document describes the high-level architecture of the AMGCR Earthquake
Research project and how data flows through the system.

**Status:** EarthESND **software implementation complete**; end-to-end scientific reproduction on real study data is **pending**.

---

# Architecture Overview

## Generic acquisition path (supporting infrastructure)

```
FDSN Services
      │
      ▼
Event Retrieval (ObsPy)
      │
      ▼
Waveform Download (placeholder / future K-NET–PESMOS adapters)
      │
      ▼
Station Metadata
      │
      ▼
Raw Data Storage (data/raw/)
```

## EarthESND pipeline (implemented)

```
Dataset manifest + stratified splits (M_JMA / M_w, Noto flag)
      │
      ▼
Preprocessing (STA/LTA, gates, filter, integration, 2–6 s windows)
      │
      ▼
(T, 9) waveform tensors + tabular feature schema (numerics blocked)
      │
      ├──► ESN ── terminal state h_T ──┐
      │                                 ├──► Fusion C ──► DENN ──► y_esn
      └──► Vertical tabular features ───┘
      │
      ├──► DENN-CTGAN (train-only contract) ──► synthetic / augmented tabular
      └──► Tabular ensemble (XGB/LGBM/CatB × real/aug) ──► six scalars
      │
      ▼
Explicit-weight aggregation (seven inputs when weights declared)
      │
      ▼
Evaluation (MAE, RMSE, % MAE improvement; Japan / Noto / India scopes)
      │
      ▼
Experiment metadata + deviation log (exact-run guard)
```

---

# Core Components

## 1. Data Acquisition

- Generic FDSN event catalogue retrieval (`src/acquisition/`).
- EarthESND manifest and splits (`src/data/`).
- K-NET / PESMOS-specific adapters: **pending reproduction** (inventory in spec).

## 2. Data Storage

- `data/raw/` for original files.
- `data/processed/` for cleaned datasets.
- `data/output/` for final results.

## 3. Processing Pipeline

- EarthESND preprocessing (`src/preprocessing/`) — fail-closed on unresolved YAML nulls.
- Feature schema (`src/processing/features.py`) — seven names; extraction blocked.
- Fusion (`src/processing/fusion.py`).

## 4. Models & ensemble

- ESN, DENN, `EarthESNDModel` (`src/models/`).
- CTGAN and tabular ensemble **contracts**; aggregation with explicit weights only.

## 5. Evaluation & reproducibility

- Metrics, benchmarks, timing (`src/evaluation/`).
- Run metadata and deviation logs (`src/experiments/run_metadata.py`).

## 6. Analysis & documentation

- Record experiments in `docs/EXPERIMENT_LOG.md`.
- Maintain changelog and reproduction checklist.

---

# Design Principles

- Modular and test-backed (**88** automated tests).
- Reproducible with fail-closed gaps for paper-unspecified details.
- No undocumented assumptions presented as paper facts.
- Research-focused; scientific table reproduction **pending** after data and training.

---

Version: **1.0.0**
