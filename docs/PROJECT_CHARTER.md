# PROJECT_CHARTER.md

**Authoritative project definition for AMGCR Earthquake Research.**

Future contributors and AI agents should treat this document as the single source of truth for vision, scope, status, and priorities. When other docs disagree, **this charter wins**.

---

## 1. Project identity

| Field | Value |
|-------|--------|
| **Name** | AMGCR Earthquake Research |
| **Context** | Swiss certificate programme research project |
| **Domain** | Earthquake Early Warning (EEW) research with AI-assisted, reproducible workflows |
| **Stack** | Python, ObsPy, NumPy/SciPy/Pandas, Matplotlib, YAML-configured modules |

---

## 2. Primary research goal

Develop a **reproducible, AI-assisted Earthquake Early Warning (EEW) research workflow** focused on **Western seismic regions**:

| Priority | Region | Role |
|----------|--------|------|
| **1 — Primary research focus** | **Europe** | Long-term target for theory, datasets, analysis, and programme proposal |
| **2 — Primary experimental dataset** | **United States / California** | Implementation, experimentation, ObsPy/FDSN practice, figures and tables |

The **EarthESND** paper implementation remains in the repository as a **reference** (literature, architecture, AI methodology, reproducible benchmark). It is **not** the final project objective.

---

## 3. Background and evolution

The repository **began as an EarthESND paper reproduction** effort. That **software reference implementation is complete** (see §6). Scientific reproduction of the paper’s published tables on K-NET-scale data is **not started** and is **out of scope** for the active certificate research unless explicitly revived.

**Active direction** follows professor guidance (§4): a logical European-oriented EEW research project with real data, theory, waveform analysis, visualisation, and written proposal sections.

---

## 4. Professor’s requirements (binding)

Contributors and agents **must** align work with:

- Download earthquake waveform data using **Python ObsPy**.
- Use **IRIS / EarthScope** for **USA** earthquake events.
- Build a **logical research project** including:
  - **Theory**
  - **Real datasets**
  - **Waveform analysis**
  - **Graphs and tables**
  - **Literature review**
- Write proposal-style sections:
  - **Introduction**
  - **Dataset**
  - **Methodology**
  - **Expected outcomes**
- Target a **European / Swiss research programme** narrative: **Europe** as ultimate focus; **USA (California)** for implementation and experimentation.

---

## 5. Research scope (what we build)

### In scope (active)

- FDSN-based acquisition (events + waveforms), starting with **California / IRIS–EarthScope**.
- Exploratory waveform analysis, statistics, station and event studies.
- Signal processing suitable for EEW research (filtering, STA/LTA, features) on Western datasets.
- European dataset identification and integration (future).
- Evaluation of **EarthESND-inspired** and other modern AI/ML approaches on **Western** datasets—not only Japan K-NET replication.
- Documentation, notebooks, figures, tables, and reproducible scripts under `scripts/`, `notebooks/`, `outputs/`.

### Reference only (maintain, do not prioritise for certificate deliverables)

- Full **EarthESND** pipeline in `src/` (ESN, DENN, contracts, 88 tests).
- **K-NET / PESMOS / Noto** acquisition plans (`docs/DATASET_ACQUISITION_PLAN.md`, etc.) for optional literature reproduction.
- Paper table reproduction (Tables 3–6) without a explicit programme decision.

### Out of scope unless requested

- Modifying EarthESND YAML nulls to fake paper completeness.
- Claiming exact EarthESND numerical reproduction without datasets and deviation log.

---

## 6. Implementation status

### 6.1 EarthESND reference implementation

| Item | Status |
|------|--------|
| Software (phases 1–6 in repo spec) | **Complete** |
| Automated tests | **88 passing** (`python -m pytest`) |
| Scientific reproduction (K-NET-scale training + paper tables) | **Not started** |
| Role going forward | Literature, architecture, and AI methodology **reference** |

Key docs: `docs/EARTHESND_REVERSE_ENGINEERING.md`, `docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md`, `docs/PAPER_REPRODUCTION.md`.

### 6.2 USA dataset workflow

| Item | Status |
|------|--------|
| ObsPy FDSN workflow | **Done** |
| IRIS / EarthScope integration | **Done** |
| California pilot (MiniSEED) | **Done** (8 events in manifest) |
| Metadata CSV + acquisition report | **Done** |
| Download script | `scripts/download/download_iris_california_pilot.py` |
| Raw data | `data/raw/iris/` |
| Manifest | `data/manifests/iris_california_pilot_events.csv` |
| Report | `docs/IRIS_DATASET_REPORT.md` |

### 6.3 California pilot — analysis & reporting

| Item | Status |
|------|--------|
| EDA | **Complete** — `docs/EDA_REPORT.md`, `reports/eda/` |
| Signal analysis | **Complete** — `docs/SIGNAL_ANALYSIS_REPORT.md`, `reports/signal_analysis/` |
| Preprocessing | **Complete** — `docs/PREPROCESSING_REPORT.md`, `reports/preprocessing/` |
| Feature engineering | **Complete** — `docs/FEATURE_ENGINEERING_REPORT.md`, `reports/features/` |
| Results & discussion | **Complete** — `docs/RESULTS_AND_DISCUSSION.md` |
| Research Proposal & Technical Report (Deliverable 1) | **Complete** — `reports/Research_Proposal_v1.md` |

**Current active stage:** Research Proposal & Technical Report (Deliverable 1 delivered). **Future work:** European dataset integration, AI modelling, real-time EEW, comparative evaluation.

### 6.4 Generic acquisition foundation

| Item | Status |
|------|--------|
| Modular `src/acquisition/` + sample QuakeML | **Done** (early milestone) |

---

## 7. Datasets (current and planned)

| Dataset | Region | Status | Location / doc |
|---------|--------|--------|----------------|
| California pilot waveforms | USA | **Complete** (acquired & analysed) | `data/raw/iris/`, `docs/IRIS_DATASET_REPORT.md` |
| Sample FDSN catalogue | Generic | Sample only | `data/raw/catalogs/` |
| EarthESND Japan (K-NET) | Japan | Planned for optional reproduction | `docs/DATASET_ACQUISITION_PLAN.md` |
| European networks (e.g. ORFEUS, EIDA) | Europe | **Planned** | Phase C roadmap |

Storage conventions: `docs/DATASET.md`, `data/raw/`, `data/manifests/`, `data/processed/` (when used).

---

## 8. Research roadmap (prioritised)

### Completed (California pilot)

| Stage | Status |
|-------|--------|
| EDA | **Complete** |
| Signal analysis | **Complete** |
| Preprocessing | **Complete** |
| Feature engineering | **Complete** |
| Results & discussion | **Complete** |
| Research Proposal & Technical Report | **Complete** |

### Future work

- **European dataset integration** (ORFEUS/EIDA pattern)  
- **AI modelling** on Western data  
- **Real-time EEW** prototypes  
- **Comparative evaluation** (incl. EarthESND-**inspired** baselines, not Japan reproduction mandate)  

Legacy EarthESND/K-NET reproduction: optional — [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md).

---

## 9. Documentation map (read order)

| Audience | Start here |
|----------|------------|
| **Everyone** | `docs/PROJECT_CHARTER.md` (this file) |
| **Why we pivoted** | `docs/RESEARCH_DIRECTION.md` |
| **Day-to-day status** | `docs/PROJECT_STATUS.md` |
| **Plans and phases** | `docs/ROADMAP.md` |
| **System layout** | `docs/ARCHITECTURE.md` |
| **EarthESND reference track** | `docs/PAPER_REPRODUCTION.md` |
| **USA data** | `docs/IRIS_DATASET_REPORT.md` |
| **USA EDA (A.1)** | `docs/EDA_REPORT.md` |
| **USA preprocessing (B.1)** | `docs/PREPROCESSING_REPORT.md` |
| **USA features (B.2)** | `docs/FEATURE_ENGINEERING_REPORT.md` |
| **Interpretation** | `docs/RESULTS_AND_DISCUSSION.md` |
| **Deliverable 1** | `reports/Research_Proposal_v1.md` |
| **AI assistants** | `docs/AI_AGENT.md` → then this charter |

---

## 10. Repository rules (summary)

- Prefer **ObsPy** and **FDSN** for seismological data.
- Keep **raw data immutable**; document sources in manifests and reports.
- **Do not** treat EarthESND Japan reproduction as the main milestone unless the charter is formally revised.
- **Do** produce analysis artefacts (scripts under `scripts/analysis/`, `reports/`, proposal text) suitable for a Swiss certificate proposal.
- Sync **PROJECT_STATUS**, **ROADMAP**, and **CHANGELOG** when milestones change.

---

## 11. Version

| Version | Date | Summary |
|---------|------|---------|
| **1.2.0** | 2026-07-29 | Final doc sync: full pilot pipeline + Deliverable 1 complete; future work defined |
| **1.1.0** | 2026-07-29 | Phase A.1 EDA and A.2 signal analysis on California pilot |
| **1.0.0** | 2026-07-29 | Charter established; pivot to Europe-focused EEW research with USA experimental data |
