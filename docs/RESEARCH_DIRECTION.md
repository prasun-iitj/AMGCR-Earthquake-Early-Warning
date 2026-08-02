# RESEARCH_DIRECTION.md

## Purpose

Explain **why** the AMGCR Earthquake Research repository changed direction, and how **reference implementation** work relates to **active certificate research**.

**Authoritative scope:** `docs/PROJECT_CHARTER.md`.  
**Release:** **v1.0.0 — Submission Release** (29 July 2026)

---

## 1. Why the focus shifted

The project **started** as a structured reproduction of the **EarthESND** paper (Joshi, Singh, Raman, *Computers and Electrical Engineering*, 2026). The **EarthESND literature track is documented** as an optional Version 3.0 path ([PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md)); executable EarthESND code is **not included in v1.0.0**. Scientific reproduction on K-NET-scale data is **not started** and is **not** the certificate programme objective.

**Professor guidance** reframed the work toward a **European-oriented EEW research project** with real waveforms, analysis, figures, tables, and formal reporting. **California FDSN data** served as the **completed pilot** for method development.

---

## 2. Reference implementation vs active research

| Aspect | EarthESND reference | Active certificate research (v1.0) |
|--------|---------------------|-------------------------------------|
| **Goal** | Literature/architecture benchmark | EEW workflow for **Europe (focus)** + **USA pilot (done)** |
| **Geography** | Japan (K-NET) in paper | California **complete**; **Europe planned (Version 3.0)** |
| **Status** | Literature track **documented** | Pilot + **submission package complete** |
| **Deliverables** | Optional paper tables | Phase docs, **Research_Report_Final.md**, **FINAL_SUBMISSION/** |

---

## 3. Completed outcomes (v1.0)

The following are **complete** (see `docs/PROJECT_STATUS.md`):

- USA / California IRIS–EarthScope pilot  
- EDA, signal analysis, preprocessing, feature engineering  
- Results & discussion  
- Reproducibility and data availability statements  
- Final research report, presentation assets, **FINAL_SUBMISSION** (validation **PASS**)  

EarthESND remains **reference methodology only**, not the primary objective.

---

## 4. Version 2.0 platform and future direction

See [ROADMAP.md](ROADMAP.md). **Version 2.0** interactive platform (`website/`) is **complete** (August 2026). **Version 3.0** themes include European datasets, EarthESND training/evaluation, real-time streaming, and operational deployment.

---

## 5. Implications for contributors and AI agents

1. Read **`docs/PROJECT_CHARTER.md`** first.  
2. Do **not** restart completed v1.0 pilot analyses unless fixing documented bugs.  
3. Do **not** treat K-NET reproduction as the default milestone.  
4. Default new work: **Version 2.1 / 3.0** roadmap unless the user requests otherwise.  
5. Cite **`reports/Research_Report_Final.md`** as the consolidated submission narrative.

---

## 6. Related documents

- `docs/PROJECT_CHARTER.md`, `docs/PROJECT_STATUS.md`, `docs/ROADMAP.md`  
- `docs/EDA_REPORT.md` through `docs/RESULTS_AND_DISCUSSION.md`  
- `reports/Research_Report_Final.md`, [RELEASE_SUMMARY_v1.0.md](../RELEASE_SUMMARY_v1.0.md)  
- `docs/PAPER_REPRODUCTION.md` — optional EarthESND scientific track  

---

Version: **1.3.0** (v1.0.0 submission release)

