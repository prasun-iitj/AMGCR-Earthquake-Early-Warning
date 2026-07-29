# IMPLEMENTATION_PLAN.md

# AMGCR Earthquake Research - Implementation Plan

## Purpose

This document tracks implementation milestones. For **EarthESND** requirements and progress detail, see `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md` (Implementation progress) and `docs/EARTHESND_REVERSE_ENGINEERING.md` (§17).

**Automated tests:** **65 passing**  
**Documentation version:** **0.5.0**

---

## EarthESND reproduction (primary track)

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Repository foundation, manifest, splits, acquisition framework | ✅ Complete |
| 2 | Preprocessing (paper gates, filter, windows; fail-closed nulls) | ✅ Complete |
| 3 | Feature engineering schema (seven names; numerics blocked) | ✅ Complete |
| 4 | Echo State Network | ✅ Complete |
| 5 | DENN, fusion, EarthESNDModel; CTGAN & ensemble contracts | ✅ Complete |
| 6 | Evaluation, trainer, full pipeline, K-NET data | ⬜ Pending |

---

## Phase 1 — Repository initialization

### Status

✅ Completed

---

## Phase 2A — Acquisition framework preparation

### Status

✅ Completed

---

## Phase 2B — Event catalogue retrieval

### Status

✅ Completed

---

## Next planned work

1. Evaluation metrics and benchmarks (`src/evaluation/` per spec).  
2. `EarthESNDTrainer` and differentiable DENN training once Adam fields are declared.  
3. K-NET / PESMOS adapters and populated manifest.  
4. `EarthESNDPipeline` and declared final aggregation weights.  

---

Version: **0.5.0**
