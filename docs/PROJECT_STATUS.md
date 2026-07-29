# PROJECT_STATUS.md

Current progress for **AMGCR Earthquake Research**. Authoritative scope: [PROJECT_CHARTER.md](PROJECT_CHARTER.md).

---

## Project information

| Field | Value |
|-------|--------|
| **Programme** | Swiss certificate EEW research |
| **Primary focus** | Europe (long-term) |
| **Pilot implementation** | USA / California (IRIS–EarthScope) — **complete** |
| **Reference track** | EarthESND software **complete**; paper scientific reproduction **not started** |
| **Current active stage** | **Research Proposal & Technical Report** ([Research_Proposal_v1.md](../reports/Research_Proposal_v1.md) — **complete**) |

---

## Status summary (canonical)

| Component | Status |
|-----------|--------|
| EarthESND reference implementation | ✅ **Complete** |
| USA / California IRIS pilot | ✅ **Complete** |
| EDA | ✅ **Complete** |
| Signal analysis | ✅ **Complete** |
| Preprocessing | ✅ **Complete** |
| Feature engineering | ✅ **Complete** |
| Results & discussion | ✅ **Complete** |
| Research Proposal & Technical Report (Deliverable 1) | ✅ **Complete** |

---

## Overall progress

| Area | Status |
|------|--------|
| Environment & repo foundation | ✅ Completed |
| Generic acquisition framework (Phase 2A/2B) | ✅ Completed |
| EarthESND reference implementation | ✅ **Complete** |
| USA IRIS–EarthScope pilot acquisition | ✅ **Complete** |
| Phase A.1 — EDA | ✅ **Complete** |
| Phase A.2 — Signal analysis | ✅ **Complete** |
| Phase B.1 — Preprocessing | ✅ **Complete** |
| Phase B.2 — Feature engineering | ✅ **Complete** |
| Phase C — Results & discussion | ✅ **Complete** |
| Deliverable 1 — Research Proposal v1 | ✅ **Complete** |
| EarthESND scientific reproduction (K-NET tables) | ⬜ Not started (optional) |

---

## Completed deliverables (links)

| Phase | Documentation | Outputs |
|-------|---------------|---------|
| Acquisition | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) | `data/raw/iris/`, manifest CSV |
| EDA | [EDA_REPORT.md](EDA_REPORT.md) | `reports/eda/`, EDA figures/tables |
| Signal analysis | [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) | `reports/signal_analysis/` |
| Preprocessing | [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) | `reports/preprocessing/` |
| Features | [FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md) | `reports/features/feature_matrix.csv` |
| Interpretation | [RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md) | — |
| Proposal | [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md) | Deliverable 1 |

---

## Future work (planned)

1. **European dataset integration** — EIDA/ORFEUS-style pilots; manifests and reports mirroring California workflow.  
2. **AI modelling** — tabular and waveform models on Western data; optional EarthESND-**inspired** architectures (reference code only).  
3. **Real-time EEW** — streaming/SeedLink prototypes; latency budgets.  
4. **Comparative evaluation** — cross-station, cross-region, and benchmark vs literature with deviation logs.

Supporting improvements (as needed): instrument response caching, pre-origin noise windows, larger catalogues.

---

## Current goal

Maintain documentation alignment with completed pilot science and pursue **future work** above without conflating EarthESND Japan reproduction with the European programme narrative.

---

## Blockers

None for documentation or planning. European FDSN access may require network-specific credentials (future).

---

Version: **1.2.0**
