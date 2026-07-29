# PAPER_REPRODUCTION.md

# AMGCR Earthquake Research - Paper Reproduction Plan

## Purpose

This document defines the strategy for reproducing the **EarthESND** methodology. Implementation authority:

- `docs/EARTHESND_REVERSE_ENGINEERING.md`
- `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md`

---

## Primary reference paper

**Title:** *Scalable multiscale echo state reservoirs with dendritic readouts for intelligent earthquake early warning systems* (EarthESND), Joshi, Singh, and Raman, *Computers and Electrical Engineering* 135 (2026) 111161.

**Software:** EarthESND implementation **complete** (phases 1–6, **88** passing tests).  
**Scientific reproduction:** **Pending** — **exact** numerical reproduction **not claimed** while supplementary details and YAML null fields remain unresolved.

---

## Reproduction objectives

- Use paper-traced software with fail-closed gaps (no silent defaults).
- Record every project assumption used in place of “not specified in the paper.”
- Compare results to published tables only after training runs and a deviation log exist.

---

## Checklist

### Software (complete)

- [x] Study paper / RE spec  
- [x] Data contracts & configs  
- [x] Preprocessing pipeline  
- [x] Feature schema (numerics blocked by design)  
- [x] ESN + DENN + EarthESNDModel forward path  
- [x] CTGAN / ensemble contracts  
- [x] Evaluation metrics, scoped benchmarks, timing helpers  
- [x] Experiment metadata and exact-reproduction guard  

### Scientific reproduction (remaining)

- [ ] Acquire datasets (K-NET Japan, PESMOS India, Noto holdout workflow)  
- [ ] Resolve undocumented paper parameters or declare assumptions in deviation log  
- [ ] Train models (DENN, synthetic/ensemble blocks when settings declared)  
- [ ] Generate tables/figures aligned with paper layout  
- [ ] Compare with published results (Tables 3–6; separate `M_JMA` / `M_w` scopes)  
- [ ] Final reproducibility report  

**Tests:** **88 passing** (`python -m pytest`)

---

## Implementation status (aligned with README)

| Step | Status |
|------|--------|
| Study paper / RE spec | ✅ |
| Data contracts & configs | ✅ |
| Preprocessing | ✅ |
| Feature schema | ✅ (numerics blocked) |
| ESN + DENN + EarthESNDModel | ✅ (`predict`; training pending reproduction) |
| CTGAN / ensemble contracts | ✅ (training blocked until YAML resolved) |
| Evaluation framework | ✅ |
| K-NET-scale waveforms & manifest | ⬜ Reproduction |
| Training & full pipeline runs | ⬜ Reproduction |
| Evaluation vs Tables 3–6 | ⬜ Reproduction |

---

## Experiment log

| Experiment | Status | Notes |
|------------|--------|-------|
| Literature / RE spec | ✅ | Main PDF only; supplement missing |
| Software implementation | ✅ | Fail-closed; 88 tests |
| Data preparation | ⬜ | Manifest contract ready |
| Preprocessing on study data | ⬜ | Unit tested on synthetic/fixtures |
| Model training / synthesis | ⬜ | Blocked fields in YAML until declared |
| Paper benchmark comparison | ⬜ | Evaluation module ready |

---

## Reproducibility notes

- Unsupported paper details remain **blocked** or **null** in config—not undocumented code defaults.
- Do not mix `M_JMA` and `M_w` without explicit documentation.
- Log substitutions in a deviation register before claiming reproduction quality.
- `assert_no_unresolved_settings` blocks **exact** reproduction claims while any config field remains `null`.

---

Version: **1.0.0**
