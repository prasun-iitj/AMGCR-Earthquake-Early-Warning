# PAPER_REPRODUCTION.md

# AMGCR Earthquake Research - Paper Reproduction Plan

## Purpose

This document defines the strategy for reproducing the **EarthESND** methodology. Implementation authority:

- `docs/EARTHESND_REVERSE_ENGINEERING.md`
- `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md`

---

## Primary reference paper

**Title:** *Scalable multiscale echo state reservoirs with dendritic readouts for intelligent earthquake early warning systems* (EarthESND), Joshi, Singh, and Raman, *Computers and Electrical Engineering* 135 (2026) 111161.

**Status:** Core software architecture and contracts **implemented**; **exact** numerical reproduction **not claimed** while supplementary details and YAML null fields remain unresolved.

---

## Reproduction objectives

- Implement paper-traced behaviour with fail-closed gaps (no silent defaults).
- Record every project assumption used in place of “not specified in the paper.”
- Compare results to published tables only after evaluation phase and deviation log exist.

---

## Implementation status (aligned with README)

| Step | Status |
|------|--------|
| Study paper / RE spec | ✅ |
| Data contracts & configs | ✅ |
| Preprocessing | ✅ |
| Feature schema | ✅ (numerics blocked) |
| ESN + DENN + EarthESNDModel | ✅ (`predict`; training pending) |
| CTGAN / ensemble contracts | ✅ (training blocked) |
| K-NET-scale waveforms & manifest | ⬜ |
| Evaluation vs Tables 3–6 | ⬜ |

**Tests:** **65 passing**

---

## Prerequisites checklist

- [x] Environment setup and ObsPy  
- [x] EarthESND YAML configs  
- [x] Preprocessing pipeline  
- [x] Model core (ESN, DENN, fusion)  
- [ ] Paper-scale Japan dataset / K-NET path  
- [ ] Numeric tabular features (approved deviation)  
- [ ] Training and evaluation modules  
- [ ] Declared aggregation weights for full system  

---

## Experiment log

| Experiment | Status | Notes |
|------------|--------|-------|
| Literature / RE spec | ✅ | Main PDF only; supplement missing |
| Data preparation | ⬜ | Manifest contract ready |
| Preprocessing | ✅ | Unit tested |
| Model implementation | ✅ | Contracts + forward path |
| Training / synthesis | ⬜ | Blocked fields in YAML |
| Evaluation | ⬜ | Not started |

---

## Reproducibility notes

- Unsupported paper details remain **blocked** or **null** in config—not undocumented code defaults.
- Do not mix `M_JMA` and `M_w` without explicit documentation.
- Log substitutions in a deviation register before claiming reproduction quality.

---

Version: **0.5.0**
