# RESEARCH_DIRECTION.md

## Purpose

Explain **why** the AMGCR Earthquake Research repository changed direction, and how **reference implementation** work relates to **active certificate research**.

**Authoritative scope:** `docs/PROJECT_CHARTER.md`.

---

## 1. Why the focus shifted

The project **started** as a structured reproduction of the **EarthESND** paper (Joshi, Singh, Raman, *Computers and Electrical Engineering*, 2026). The **EarthESND reference implementation is complete** (88 passing tests on a full checkout). Scientific reproduction on K-NET-scale data is **not started** and is **not** the certificate programme objective.

**Professor guidance** reframed the work toward a **European-oriented EEW research project** with real waveforms, analysis, figures, tables, and a formal **Research Proposal & Technical Report**. **California FDSN data** served as the **completed pilot** for method development.

---

## 2. Reference implementation vs active research

| Aspect | EarthESND reference | Active certificate research |
|--------|---------------------|----------------------------|
| **Goal** | Literature/architecture benchmark | EEW workflow for **Europe (focus)** + **USA pilot (done)** |
| **Geography** | Japan (K-NET) in paper | California **complete**; **Europe next** |
| **Status** | Software **complete** | Acquisition → features → interpretation → **Proposal v1 complete** |
| **Deliverables** | Optional paper tables | `reports/`, phase docs, **Research_Proposal_v1.md** |

---

## 3. Completed pilot outcomes (USA)

The following are **complete** (see `docs/PROJECT_STATUS.md`):

- USA / California IRIS–EarthScope pilot  
- EDA, signal analysis, preprocessing, feature engineering  
- Results & discussion  
- Deliverable 1 — Research Proposal & Technical Report  

EarthESND remains **reference methodology only**, not the primary objective.

---

## 4. Future direction

1. **European dataset integration**  
2. **AI modelling** on Western data  
3. **Real-time EEW** prototyping  
4. **Comparative evaluation** (including EarthESND-**inspired** baselines)

---

## 5. Implications for contributors and AI agents

1. Read **`docs/PROJECT_CHARTER.md`** first.  
2. Do **not** restart completed pilot analyses unless fixing documented bugs.  
3. Do **not** treat K-NET reproduction as the default milestone.  
4. Extend toward **Europe** and **future work** above.  
5. Cite **`reports/Research_Proposal_v1.md`** as the consolidated programme narrative.

---

## 6. Related documents

- `docs/PROJECT_CHARTER.md`, `docs/PROJECT_STATUS.md`, `docs/ROADMAP.md`  
- `docs/EDA_REPORT.md` through `docs/RESULTS_AND_DISCUSSION.md`  
- `reports/Research_Proposal_v1.md`  
- `docs/PAPER_REPRODUCTION.md` — optional EarthESND scientific track  

---

Version: **1.2.0** (2026-07-29)
