# PAPER_REPRODUCTION.md

**EarthESND paper reproduction** — optional **reference track**, not the active certificate research path.

**Programme direction:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md) · [RESEARCH_DIRECTION.md](RESEARCH_DIRECTION.md)

---

## Primary reference paper

**EarthESND:** Lightweight Multiscale Echo State Network with Dendritic Neural Network Readout for Earthquake Early Warning  
(Joshi, Singh, Raman — *Computers and Electrical Engineering*, 2026)

| Aspect | Status |
|--------|--------|
| Paper selected as **literature & architecture reference** | ✅ |
| **Software** reproduction in this repository | ✅ **Complete** |
| **Scientific** reproduction (K-NET training, paper tables) | ⬜ **Not started** |
| Role in certificate project | Benchmark only; **Western EEW research** is primary |

---

## What “complete” means (software)

- Primary paper: [REFERENCES.md](../references/REFERENCES.md) · local copy `references/papers/ScienceDirect_EarthESND_2026.pdf`
- Pipeline modules under `src/` with **88 passing tests** on a full reference checkout
- Config contracts under `configs/earthesnd/`

This does **not** imply published Table 3–6 numbers have been replicated.

---

## What “not started” means (scientific)

Scientific reproduction requires at minimum:

- Japan K-NET (and related) waveform acquisition at paper scale — **not started**; scope when revived under [ROADMAP.md](ROADMAP.md) Version 2.0 and this document
- Training and evaluation runs with documented hyperparameters
- Comparison to paper metrics with a **deviation log**

None of that is on the **critical path** for Phases A–D unless the charter is revised.

---

## Reproduction objectives (when explicitly scoped)

- Reproduce data preparation as described in the paper
- Run the implemented ESN/DENN stack on acquired K-NET-class data
- Compare to Tables 3–6 and figures where feasible
- Document all differences (sampling, magnitude definition, station set, etc.)

---

## Prerequisites checklist

| Prerequisite | Reference track | Active USA track |
|--------------|-----------------|------------------|
| Environment & ObsPy | ✅ | ✅ |
| Implementation in `src/` | ✅ | N/A (reuse optional) |
| K-NET-scale waveforms | ⬜ | N/A |
| California pilot waveforms | N/A | ✅ — [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |
| Pilot EDA & signal analysis | N/A | ✅ — [EDA_REPORT.md](EDA_REPORT.md), [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) |
| Preprocessing on target geography | ⬜ (Japan) | ✅ — [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) |
| Paper table reproduction | ⬜ | Out of scope unless requested |

---

## Experiment log (EarthESND scientific track)

| Experiment | Status | Notes |
|------------|--------|-------|
| Literature review | ✅ | Cited in [Research_Report_Final.md](../reports/Research_Report_Final.md) |
| K-NET / PESMOS data acquisition | ⬜ | Version 2.0 / optional — [ROADMAP.md](ROADMAP.md) |
| Data preparation (Japan) | ⬜ | |
| Training & evaluation | ⬜ | |
| Table / figure comparison | ⬜ | |

---

## Reproducibility notes

- Record ObsPy, Python, and dependency versions
- Store dataset sources in manifests (`data/manifests/`)
- Never claim paper parity without datasets and a deviation log
- For new work, prefer **USA pilot → Europe** workflow documented in the charter

---

Version: **1.3.0** (v1.0.0 submission release)
