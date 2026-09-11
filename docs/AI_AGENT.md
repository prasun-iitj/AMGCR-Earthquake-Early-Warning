# AI_AGENT.md

Instructions for AI coding assistants working on **AMGCR_Earthquake_Research**.

**Release:** **v1.0.0 — Submission Release** (29 July 2026)

---

## Primary objective

Support **European-focused EEW research** using a **completed California FDSN pilot** and **frozen v1.0 submission** as the method reference. **EarthESND** is **reference code only**—not the default task.

---

## Repository status (do not contradict)

| Component | Status |
|-----------|--------|
| EarthESND literature / optional track | ✅ Documented (not in v1.0.0 code tree) |
| USA / California IRIS pilot | ✅ Complete |
| EDA | ✅ Complete |
| Signal analysis | ✅ Complete |
| Preprocessing | ✅ Complete |
| Feature engineering | ✅ Complete |
| Results & discussion | ✅ Complete |
| Reproducibility & data availability (D-S1/S2) | ✅ Complete |
| Final report & FINAL_SUBMISSION (D-F1–F4) | ✅ Complete |
| Submission validation | ✅ PASS |
| Swiss SED methods-transfer (Set A) | ✅ Acquisition + signal analysis + STA/LTA transfer complete |
| Swiss independent validation-set design | ✅ Design/audit corrected (2026-09-11, STEP 2I.1) |
| Swiss independent validation acquisition | ✅ Complete (2026-09-11, STEP 2J); MiniSEED/StationXML |
| Swiss independent frozen STA/LTA validation | ✅ Complete (2026-09-11, STEP 2K); threshold 8.0 evaluated as pre-declared; no retuning |
| Swiss ML feasibility audit | ✅ Complete (2026-09-11, STEP 3A); **NO-GO** — no model trained |

**Current stage:** **scientific submission freeze**. California v1.0.0 frozen. Swiss Set C and threshold **8.0** frozen. STEP 2K results frozen. **Do not** re-run the California pilot, retune 8.0, train ML, modify Set C, or add datasets unless explicitly requested.

---

## Required reading (in order)

1. [PROJECT_CHARTER.md](PROJECT_CHARTER.md)  
2. [RESEARCH_DIRECTION.md](RESEARCH_DIRECTION.md)  
3. [PROJECT_STATUS.md](PROJECT_STATUS.md)  
4. [Research_Report_Final.md](../reports/Research_Report_Final.md)  
5. Phase reports as needed (`EDA_*` through `RESULTS_AND_DISCUSSION.md`)

For EarthESND optional track only: [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md), [REFERENCES.md](../references/REFERENCES.md).

---

## What to build next (default — Version 2.1 / 3.0)

Unless the user explicitly asks otherwise:

1. **Version 2.1** — platform maintenance, deployment, content sync, optional UX (`website/` only)  
2. **Do not** start Swiss ML: STEP 3A is **NO-GO** until independent Set A labels exist ([SWISS_ML_FEASIBILITY_AUDIT.md](SWISS_ML_FEASIBILITY_AUDIT.md))  
3. **Version 3.0 — further Europe data** — only if explicitly requested (Set C remains locked)  
4. **Version 3.0 — EarthESND training & evaluation** — Western data; deviation logs; only if explicitly requested  
5. **Version 3.0 — Real-time streaming** and operational deployment planning  

**Do not** modify completed v1.0 analysis scripts, re-run analyses, or alter frozen submission PDFs unless asked. **Do not** modify EarthESND reference without explicit request. **Do not** retune threshold 8.0 or rewrite STEP 2K outputs.

---

## Documentation rules

After Version 2.1 / 3.0 milestones: update **PROJECT_STATUS**, **ROADMAP**, **CHANGELOG**, and charter if scope changes.

---

Version: **1.4.0** (v2.0.0 platform release · science v1.0.0 frozen)
