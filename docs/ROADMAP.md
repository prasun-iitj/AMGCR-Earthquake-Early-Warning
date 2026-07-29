# ROADMAP.md

Development and **research roadmap** for AMGCR Earthquake Research.

**Authoritative priorities:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md) · **Context:** [RESEARCH_DIRECTION.md](RESEARCH_DIRECTION.md)

---

## Completed foundation

| Milestone | Status |
|-----------|--------|
| Phase 1 — Environment & repo | ✅ |
| Phase 2A/2B — Acquisition framework & sample catalogue | ✅ |
| **EarthESND reference implementation** | ✅ **Complete** |
| **USA California IRIS/EarthScope pilot** | ✅ **Complete** |

---

## Completed certificate research pipeline (California pilot)

| Phase | Status | Primary doc |
|-------|--------|-------------|
| **EDA** | ✅ Complete | [EDA_REPORT.md](EDA_REPORT.md) |
| **Signal analysis** | ✅ Complete | [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) |
| **Preprocessing** | ✅ Complete | [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) |
| **Feature engineering** | ✅ Complete | [FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md) |
| **Results & discussion** | ✅ Complete | [RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md) |
| **Research Proposal & Technical Report** | ✅ Complete | [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md) |

**Current active stage (programme):** **Research Proposal & Technical Report** — Deliverable 1 **published**; analysis chain **frozen** at documented artefacts in `reports/`.

---

## Future work (prioritised)

### 1. European dataset integration

- ORFEUS/EIDA and national FDSN endpoints  
- Pilot manifests and acquisition reports parallel to [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md)  
- Comparison of USA vs Europe feature distributions  

### 2. AI modelling

- Magnitude/intensity baselines on `feature_matrix.csv` and normalized waveform NPZ  
- Waveform deep learning on P-aligned windows  
- **EarthESND-inspired** models as **comparative** baselines only (reference `src/`, Western geography)

### 3. Real-time EEW

- Continuous acquisition simulation (SeedLink)  
- Onsite STA/LTA + feature latency profiling  

### 4. Comparative evaluation

- Cross-station and cross-region metrics  
- Deviation logs vs published ML EEW papers (including EarthESND **reference**, not reproduction mandate)  
- Response-corrected amplitudes before operational claims  

---

## Optional reference track — EarthESND paper reproduction

| Item | Status |
|------|--------|
| Reference software | ✅ Complete |
| K-NET scientific reproduction (Tables 3–6) | ⬜ Not started |

Details: [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md)

---

## Milestone summary

| Track | Item | Status |
|-------|------|--------|
| Reference | EarthESND implementation | ✅ |
| Pilot | California FDSN workflow | ✅ |
| Analysis | EDA → features → interpretation | ✅ |
| Deliverable | Research Proposal v1 | ✅ |
| Future | Europe / AI / real-time / evaluation | ⬜ Planned |

---

Version: **1.2.0**
