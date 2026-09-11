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

The repository **began as an EarthESND paper reproduction** effort. The **EarthESND literature track is documented** as an optional Version 3.0 path (see §6.1); executable modules are **not included in v1.0.0**. Scientific reproduction of the paper’s published tables on K-NET-scale data is **not started** and is **out of scope** for the active certificate research unless explicitly revived.

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
- Evaluation of **EarthESND-inspired** and other modern AI/ML approaches on **Western** datasets—not only Japan K-NET replication (optional **Version 3.0** track).
- Documentation, notebooks, figures, tables, and reproducible scripts under `scripts/`, `notebooks/`, `outputs/`.

### Reference only (maintain, do not prioritise for certificate deliverables)

- **EarthESND** executable pipeline — optional **Version 3.0** track; literature reference documented in [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md) (not included in v1.0.0 code tree).
- **K-NET / PESMOS / Noto** optional Japan reproduction — see [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md).
- Paper table reproduction (Tables 3–6) without a explicit programme decision.

### Out of scope unless requested

- Modifying EarthESND YAML nulls to fake paper completeness.
- Claiming exact EarthESND numerical reproduction without datasets and deviation log.

---

## 6. Implementation status

### 6.1 EarthESND reference track

| Item | Status |
|------|--------|
| Literature and architecture reference (paper, optional track doc) | **Documented** |
| Executable EarthESND pipeline in v1.0.0 release | **Not included** — optional Version 3.0 |
| Acquisition framework automated tests | **9 passing** (`python -m pytest`) |
| Scientific reproduction (K-NET-scale training + paper tables) | **Not started** |
| Role going forward | Literature, architecture, and AI methodology **reference** |

Key docs: [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md), [REFERENCES.md](../references/REFERENCES.md).

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
| Reproducibility Statement (D-S1) | **Complete** — `docs/REPRODUCIBILITY_STATEMENT.md` |
| Data Availability Statement (D-S2) | **Complete** — `docs/DATA_AVAILABILITY_STATEMENT.md` |
| Final Research Report (D-F1) | **Complete** — `reports/Research_Report_Final.md` |
| Presentation & submission package (D-F2–F4) | **Complete** — `FINAL_SUBMISSION/` (validation **PASS**) |
| Research Proposal v1 (superseded) | **Complete** — `reports/Research_Proposal_v1.md` |

**Current stage:** **v1.0.0 Submission Release** (29 July 2026) · **Version 2.0 platform live** (2 August 2026) · **Swiss frozen STA/LTA validation complete** (STEP 2K) · **ML feasibility NO-GO** (STEP 3A). California pilot analysis **frozen**. Roadmap: [ROADMAP.md](ROADMAP.md).

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
| EarthESND Japan (K-NET) | Japan | Planned (optional, Version 3.0) | [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md) |
| European networks (e.g. ORFEUS, EIDA) | Europe | **Planned (Version 3.0)** | [ROADMAP.md](ROADMAP.md) |
| Swiss SED methods-transfer pilot | Switzerland / CH network | **Acquisition complete**; Set A analysis + Set C frozen STA/LTA validation (STEP 2K). Not operational EEW | `data/raw/switzerland/`, [SED_SWITZERLAND_DATASET_REPORT.md](SED_SWITZERLAND_DATASET_REPORT.md), [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md) |

Storage conventions: `docs/DATASET.md`, `data/raw/`, `data/manifests/`, `data/processed/` (when used).

---

## 8. Research roadmap (prioritised)

### Completed (v1.0 submission)

| Stage | Status |
|-------|--------|
| EDA | **Complete** |
| Signal analysis | **Complete** |
| Preprocessing | **Complete** |
| Feature engineering | **Complete** |
| Results & discussion | **Complete** |
| D-S1 / D-S2 statements | **Complete** |
| D-F1–F4 submission deliverables | **Complete** |

### Version 2.0 platform (complete)

Interactive website, dashboard, and explorers — **complete** (August 2026). See [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md) and [../website/README.md](../website/README.md).

### Version 2.1 / Version 3.0 (future work)

See [ROADMAP.md](ROADMAP.md): **Version 2.1** platform maintenance; **Version 3.0** Europe dataset expansion, EarthESND training/evaluation, real-time streaming, operational deployment, and related science hardening.

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
| **Submission (v1.0)** | [RELEASE_SUMMARY_v1.0.md](../RELEASE_SUMMARY_v1.0.md), `FINAL_SUBMISSION/` |
| **Final report** | `reports/Research_Report_Final.md` |
| **Proposal v1** | `reports/Research_Proposal_v1.md` |
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
| **1.4.0** | 2026-08-02 | Pre-release audit sync: v2.0 platform complete; EarthESND status aligned to v1.0.0 tree; LICENSE; reproducibility deps |
| **1.3.0** | 2026-07-29 | **v1.0.0 Submission Release** — FINAL_SUBMISSION, D-F1–F4, D-S1/S2, validation PASS; Version 2.0 roadmap |
| **1.2.0** | 2026-07-29 | Final doc sync: full pilot pipeline + Deliverable 1 complete; future work defined |
| **1.1.0** | 2026-07-29 | Phase A.1 EDA and A.2 signal analysis on California pilot |
| **1.0.0** | 2026-07-29 | Charter established; pivot to Europe-focused EEW research with USA experimental data |
