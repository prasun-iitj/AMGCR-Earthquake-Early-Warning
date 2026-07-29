# ROADMAP.md

Development and **research roadmap** for AMGCR Earthquake Research.

**Release:** **v1.0.0 — Submission Release** (29 July 2026)  
**Authoritative priorities:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md) · **Context:** [RESEARCH_DIRECTION.md](RESEARCH_DIRECTION.md)

---

## Archived — v1.0 submission (complete)

All items below were **completed** by 2026-07-29 and are **frozen** for the certificate submission.

| Milestone | Status | Primary doc / output |
|-----------|--------|----------------------|
| Phase 1 — Environment & repo | ✅ | [CHANGELOG.md](CHANGELOG.md) |
| Phase 2A/2B — Acquisition framework | ✅ | `src/acquisition/` |
| **EarthESND reference implementation** | ✅ | `src/`, 88 tests |
| **USA California IRIS/EarthScope pilot** | ✅ | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |
| **EDA** | ✅ | [EDA_REPORT.md](EDA_REPORT.md) |
| **Signal analysis** | ✅ | [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) |
| **Preprocessing** | ✅ | [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) |
| **Feature engineering** | ✅ | [FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md) |
| **Results & discussion** | ✅ | [RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md) |
| **D-S1 / D-S2** | ✅ | [REPRODUCIBILITY_STATEMENT.md](REPRODUCIBILITY_STATEMENT.md), [DATA_AVAILABILITY_STATEMENT.md](DATA_AVAILABILITY_STATEMENT.md) |
| **D-F1 Final report** | ✅ | [Research_Report_Final.md](../reports/Research_Report_Final.md) |
| **D-F2 / D-F3 Presentation** | ✅ | [Presentation_Outline_D-F2.md](../reports/Presentation_Outline_D-F2.md), [Presentation_Script_D-F3.md](../reports/Presentation_Script_D-F3.md) |
| **D-F4 FINAL_SUBMISSION** | ✅ | [FINAL_SUBMISSION/](../FINAL_SUBMISSION/) — validation **PASS** |

Optional reference track: K-NET paper tables — ⬜ not started ([PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md)).

---

## Version 2.0 / future roadmap (planned)

**Not part of v1.0 submission.** Prioritisation subject to programme and infrastructure decisions.

### 1. Communication and visualisation

- **Interactive project website** (programme-facing narrative, artefact index)  
- **Public dashboard** (pilot metrics, manifest status, reproducibility health)  
- **Interactive visualisations** (waveforms, features, cross-event exploration)

### 2. European and extended datasets

- **Europe dataset expansion** — ORFEUS/EIDA and national FDSN endpoints  
- **Additional datasets** — scaled California/Western USA catalogues; optional K-NET track  
- Cross-region feature comparison (USA vs Europe)

### 3. Machine learning and evaluation

- **EarthESND model training and evaluation** on Western data (deviation log vs Japan paper)  
- Tabular and waveform baselines on `feature_matrix.csv` and NPZ stages  
- Comparative evaluation vs literature with documented metrics

### 4. Real-time and operations

- **Real-time streaming support** (e.g. SeedLink simulation, continuous STA/LTA)  
- Latency budgets and onsite feature push prototypes  
- **Production deployment** path (operational EEW integration, governance, uncertainty communication)

### 5. Data quality and science hardening

- Instrument response caching and physical-unit amplitudes  
- Pre-origin download windows for unbiased noise/SNR  
- Three-component data where available  
- Stratified sampling by magnitude, distance, and azimuth  

---

## Milestone summary

| Track | v1.0 | v2.0 |
|-------|------|------|
| Reference (EarthESND code) | ✅ Complete | Optional K-NET reproduction |
| California pilot science | ✅ Complete | Scale / extend |
| Submission deliverables | ✅ Complete | — |
| Web / dashboard / viz | — | ⬜ Planned |
| Europe / ML / streaming / deploy | — | ⬜ Planned |

---

Version: **1.3.0** (v1.0.0 submission release)
