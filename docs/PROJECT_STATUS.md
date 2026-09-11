# PROJECT_STATUS.md

Current progress for **AMGCR Earthquake Research**. Authoritative scope: [PROJECT_CHARTER.md](PROJECT_CHARTER.md).

**Release:** **v1.0.0 — Submission Release** (29 July 2026)

---

## Project information

| Field | Value |
|-------|--------|
| **Programme** | Swiss certificate EEW research (AMGCR) |
| **Primary focus** | Europe (long-term) |
| **Pilot implementation** | USA / California (IRIS–EarthScope) — **complete** |
| **Reference track** | EarthESND literature track **documented**; executable pipeline optional (v3.0); K-NET reproduction **not started** |
| **Current stage** | **v1.0 submission complete** · **Version 2.0 platform live** (2026-08-02) · **Swiss SED acquisition complete** (2026-09-06) · **Swiss independent frozen STA/LTA validation complete** (2026-09-11, STEP 2K) |

---

## Status summary (canonical)

| Component | Status |
|-----------|--------|
| EarthESND literature / optional track | ✅ **Documented** (not in v1.0.0 code tree) |
| USA / California IRIS pilot | ✅ **Complete** |
| EDA | ✅ **Complete** |
| Signal analysis | ✅ **Complete** |
| Preprocessing | ✅ **Complete** |
| Feature engineering | ✅ **Complete** |
| Results & discussion | ✅ **Complete** |
| Reproducibility Statement (D-S1) | ✅ **Complete** |
| Data Availability Statement (D-S2) | ✅ **Complete** |
| Final Research Report (D-F1) | ✅ **Complete** |
| Presentation outline & script (D-F2/D-F3) | ✅ **Complete** |
| FINAL_SUBMISSION package (D-F4) | ✅ **Complete** |
| Submission validation | ✅ **PASS** |
| **Version 2.0 interactive platform** (`website/`) | ✅ **Complete** (2 August 2026) |
| **Swiss SED methods-transfer acquisition** | ✅ **Complete** (2026-09-06) — 20 events, 120 CH 3C MiniSEED records |
| **Swiss independent validation-set design** | ✅ **Design/audit corrected** (2026-09-11, STEP 2I.1) — Independent Swiss/Adjacent-Border Validation Set (15 locked events) |
| **Swiss independent validation acquisition** | ✅ **Complete** (2026-09-11, STEP 2J) — 15/15 events, 550 CH HHZ MiniSEED + StationXML |
| **Swiss independent frozen STA/LTA validation** | ✅ **Complete** (2026-09-11, STEP 2K) — threshold **8.0** evaluated as pre-declared; 550/550 records; **no** retuning |

---

## Version 2.0 platform (complete — 2026-08-02)

| Component | Status |
|-----------|--------|
| Interactive website (19 routes) | ✅ **Complete** |
| Research dashboard | ✅ **Complete** |
| Workflow, results, dataset, waveform, map explorers | ✅ **Complete** |
| Documentation portal & global search | ✅ **Complete** |
| SEO, error pages, accessibility polish | ✅ **Complete** |
| Production deployment documentation | ✅ **Complete** |

Release notes: [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md) · Website guide: [website/README.md](../website/README.md)

---

## Archived — v1.0 milestones (2026-07-29)

| Milestone | Documentation / output |
|-----------|-------------------------|
| Acquisition | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |
| EDA | [EDA_REPORT.md](EDA_REPORT.md) |
| Signal analysis | [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) |
| Preprocessing | [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) |
| Feature engineering | [FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md) |
| Interpretation | [RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md) |
| Proposal v1 | [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md) |
| Final report | [Research_Report_Final.md](../reports/Research_Report_Final.md) |
| Submission package | [FINAL_SUBMISSION/](../FINAL_SUBMISSION/) |
| Deliverable audit | [FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md) |

EarthESND scientific reproduction (K-NET tables): ⬜ **Not started** — optional **Version 3.0** track ([PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md)).

---

## Version 2.1 / Version 3.0 roadmap

See [ROADMAP.md](ROADMAP.md). Summary:

- **Version 2.1** — platform maintenance, content sync, deployment hardening, optional UX improvements  
- **Version 3.0** — Europe dataset expansion (ORFEUS/EIDA), EarthESND training/evaluation, real-time streaming, operational deployment  

---

## Current goal

Preserve **v1.0 submission integrity** (frozen pilot artefacts). Maintain **Version 2.0 platform** (`website/`). Plan **Version 2.1** and **Version 3.0** without re-running or rewriting v1.0 science unless explicitly approved.

---

## Blockers

None for v1.0 submission. European FDSN access and web hosting may require credentials or infrastructure (Version 2.0).

---

Version: **1.4.0** (v2.0.0 platform release · science v1.0.0 frozen)
