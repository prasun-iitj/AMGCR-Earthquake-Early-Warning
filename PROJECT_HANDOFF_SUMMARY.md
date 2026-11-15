# AMGCR Earthquake Research — Full Project Handoff Summary

> **STATUS UPDATE (2026-11-12):** This summary was generated 2026-11-06 and is **historical** in parts. The ML "NO-GO" decision and the hard rule "Do NOT train any ML model on Swiss Set A" below were **superseded**: STEP ML-1A (120/120 SED analyst picks) removed the labelling blocker, and STEP ML-2 to ML-4 trained Random Forest/XGBoost on Set A and evaluated them on Set C (offline windowed benchmark, not an operational EEW system). Current authority: `docs/PROJECT_STATUS.md`. Still frozen: California v1.0.0, Set C membership, STEP 2K threshold 8.0 (derived from the Swiss Set A grid; California baseline was 2.5). Versions: **v1.0.0** = frozen submission release; **v1.8.0** = internal documentation milestone (STEP ML-4).
> **Purpose:** This document is a complete, structured summary of everything done in this project so far. It is intended to onboard a new AI agent (ChatGPT, Claude, Gemini, etc.) or collaborator so they are fully in sync with the current state.

---

## 1. What This Project Is

**Project Name:** AMGCR Earthquake Research  
**Type:** Swiss Certificate Programme research project  
**Domain:** Earthquake Early Warning (EEW) — using AI and signal processing to detect earthquakes as early as possible  
**Primary Tech Stack:** Python, ObsPy, NumPy, SciPy, Pandas, Matplotlib, Next.js (website)  
**Repository location (local):** `c:\Users\prasun.tripathi\Desktop\MY\AMGCR_Earthquake_Research`

### Core Research Goal
Develop a **reproducible, AI-assisted Earthquake Early Warning (EEW) research workflow** focused on **Western seismic regions**:
- **Europe** = long-term primary research focus
- **USA / California** = completed experimental pilot (proof-of-concept)

### Reference Paper
The project references **EarthESND** (a published Japanese EEW deep-learning paper). This paper is treated as a **literature and architecture reference only** — it is NOT the final project goal and its executable pipeline is NOT in the codebase. Scientific reproduction of EarthESND on Japanese K-NET data is an optional future track (Version 3.0), not started.

---

## 2. Project Version History

| Version | Date | What happened |
|---------|------|---------------|
| **v1.0.0** | 2026-07-29 | Full California pilot science completed and submitted |
| **v2.0.0** | 2026-08-02 | Interactive research website launched |
| **v2.1 (partial)** | 2026-10-16 | Website updated with Swiss research content + UI bug fixes |
| **v3.0** | Future | Europe expansion, ML training, real-time streaming |

---

## 3. What Has Been Scientifically Completed

### Phase 1 — California Pilot (v1.0 — FROZEN, do not re-run)

All steps below are **complete and frozen**. Do NOT modify, re-run, or alter any California analysis scripts or outputs.

| Step | What was done | Output location |
|------|--------------|----------------|
| **Data Acquisition** | Downloaded 8 real California earthquake waveform records (MiniSEED format) using Python ObsPy from IRIS/EarthScope FDSN | `data/raw/iris/`, `data/manifests/iris_california_pilot_events.csv` |
| **EDA (Exploratory Data Analysis)** | Analysed event properties: magnitude, depth, distance, station coverage | `docs/EDA_REPORT.md`, `reports/eda/` |
| **Signal Analysis** | Studied P-wave and S-wave characteristics, spectrogram analysis, SNR | `docs/SIGNAL_ANALYSIS_REPORT.md`, `reports/signal_analysis/` |
| **Preprocessing** | Filtered and cleaned seismic signals (bandpass filtering, instrument response removal) | `docs/PREPROCESSING_REPORT.md`, `reports/preprocessing/` |
| **Feature Engineering** | Extracted EEW-relevant features: STA/LTA ratio, peak amplitude, dominant frequency, etc. | `docs/FEATURE_ENGINEERING_REPORT.md`, `reports/features/`, `reports/features/feature_matrix.csv` |
| **Results & Discussion** | Interpreted results, assessed EEW feasibility for California data | `docs/RESULTS_AND_DISCUSSION.md` |
| **Reproducibility Statement (D-S1)** | Formal statement on reproducibility | `docs/REPRODUCIBILITY_STATEMENT.md` |
| **Data Availability Statement (D-S2)** | Formal data availability statement | `docs/DATA_AVAILABILITY_STATEMENT.md` |
| **Final Research Report (D-F1)** | Full academic report | `reports/Research_Report_Final.md` |
| **Presentation (D-F2/D-F3)** | Presentation outline and script | `reports/Presentation_Outline_D-F2.md`, `reports/Presentation_Script_D-F3.md` |
| **FINAL_SUBMISSION (D-F4)** | Complete submission package | `FINAL_SUBMISSION/` — **validation PASS** |

---

### Phase 2 — Swiss SED Pilot (Part of v3.0 work — FROZEN, do not re-run)

After the California submission, the same methods were transferred to Switzerland to test on European seismic data.

#### Swiss Set A — Methods Transfer (20 events)

| Step | What was done | Output |
|------|--------------|--------|
| **Acquisition** | Downloaded 20 Swiss earthquake events, 120 CH HH 3-component MiniSEED waveforms + StationXML from Swiss Seismological Service (SED) | `data/raw/switzerland/`, `docs/SED_SWITZERLAND_DATASET_REPORT.md` |
| **Signal Analysis** | Applied the California signal analysis pipeline to Swiss waveforms; generated 11 new signal figures | `reports/switzerland_transfer/` |
| **STA/LTA Transfer** | Applied the STA/LTA detection algorithm (threshold = 8.0, pre-declared) to Swiss Set A | Results in `reports/switzerland_transfer/` |

#### Swiss Set C — Independent Validation (15 events, 550 waveforms — FROZEN)

This is a completely separate, independent validation dataset — **not** the same events as Set A.

| Step | What was done | Output |
|------|--------------|--------|
| **Validation Set Design (STEP 2I.1)** | Designed independent validation set with 15 events (Swiss + adjacent border) separate from Set A | `docs/SWISS_INDEPENDENT_VALIDATION_PLAN.md` |
| **Acquisition (STEP 2J)** | Downloaded 15 events, 550 CH HHZ MiniSEED + StationXML (window: origin−60s → origin+90s) | `data/raw/switzerland_validation/` |
| **Frozen STA/LTA Validation (STEP 2K)** | Applied pre-declared threshold **8.0** to 550 records WITHOUT any retuning or modification | `docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md`, `reports/switzerland_validation/validation_summary.json` |
| **Validation Results** | **72.9% detection rate**, **1.24 second median timing error** across 550 records | `reports/switzerland_validation/` |
| **Scientific Consistency Audit** | Verified all headline metrics agree across CSVs, JSON, and markdown results | ✅ Passed |

#### Swiss ML Feasibility Audit (STEP 3A) — NO-GO Decision

| Item | Decision | Reason |
|------|----------|--------|
| Supervised ML on Swiss Set A | ❌ **NO-GO** | No independent P-wave arrival picks (labels) exist for Set A events. Training ML using STA/LTA detections as labels would be circular (the model would just learn to replicate STA/LTA, not real physics). |
| ML on California `feature_matrix.csv` (N=8) | ❌ Not scientifically sufficient | Only 8 events — too small for meaningful ML. |
| **What needs to happen to unblock ML** | Acquire **official first-P wave arrival picks** from the SED catalog for the 20 Set A training events | This is the **single blocker** |

---

## 4. What Was Built — The Website (v2.0 / v2.1)

An interactive research website built with **Next.js 16 / TypeScript / Tailwind CSS v4** was developed in `website/`. It is a standalone app that reads all research data at build time from the parent repository.

### Website Pages (27 static pages)
- `/` — Hero page with project highlights and timeline
- `/dashboard` — Research dashboard with live Swiss validation metrics
- `/workflow` — Step-by-step research workflow explorer
- `/results` — Results explorer: 38 figures + 11 CSV tables, 6 research phases
- `/dataset` — Dataset explorer
- `/waveforms` — Waveform viewer for 8 California events
- `/map` — Earthquake map
- `/docs` — Documentation portal (all research documents)
- `/research/report` — Full final research report viewer
- `/resources`, `/github`, `/about`, `/contact`

### Website Updates Done (v2.1, October 2026)
1. **Added 7 new documents** to the docs portal: Swiss SED Dataset Report, Swiss Independent Validation Results, Swiss ML Feasibility Audit, Research Direction, Roadmap, and others
2. **Dashboard updated** with Swiss validation metrics (72.9% detection, 1.24s timing error) and ML NO-GO status
3. **Results Explorer expanded** from California-only → 6 phases including Swiss Transfer and Swiss Validation
4. **Search index re-indexed** to 122 records covering all Swiss documents
5. **UI bug fixed**: Research Report page had duplicate overlapping headings — fixed by stripping HTML cover block from document content before rendering
6. **Build verified**: All 27 pages compile with zero TypeScript errors

---

## 5. Key Repository Structure

```
AMGCR_Earthquake_Research/
├── data/
│   ├── raw/iris/                        # California MiniSEED waveforms
│   ├── raw/switzerland/                 # Swiss Set A waveforms (20 events, 120 records)
│   ├── raw/switzerland_validation/      # Swiss Set C waveforms (15 events, 550 records)
│   └── manifests/                       # Event CSVs
├── docs/                                # All research documents (Markdown)
│   ├── PROJECT_CHARTER.md               # ⭐ Single source of truth for scope
│   ├── AI_AGENT.md                      # ⭐ Rules for AI agents
│   ├── PROJECT_STATUS.md                # Current status of all components
│   ├── ROADMAP.md                       # Future work plan
│   ├── EDA_REPORT.md                    # California EDA
│   ├── SIGNAL_ANALYSIS_REPORT.md        # California signal analysis
│   ├── PREPROCESSING_REPORT.md          # California preprocessing
│   ├── FEATURE_ENGINEERING_REPORT.md    # California features
│   ├── RESULTS_AND_DISCUSSION.md        # California results
│   ├── SED_SWITZERLAND_DATASET_REPORT.md   # Swiss Set A dataset
│   ├── SWISS_INDEPENDENT_VALIDATION_RESULTS.md  # Swiss Set C results
│   └── SWISS_ML_FEASIBILITY_AUDIT.md    # ML NO-GO decision
├── reports/
│   ├── eda/                             # California EDA figures
│   ├── signal_analysis/                 # California signal figures
│   ├── preprocessing/                   # California preprocessing figures
│   ├── features/                        # California feature tables
│   │   └── feature_matrix.csv           # N=8, California features
│   ├── switzerland_transfer/            # Swiss Set A figures (fig01–fig11)
│   ├── switzerland_validation/          # Swiss Set C figures + validation_summary.json
│   │   └── validation_summary.json      # detection_percent: 72.9, median_abs_timing_error_s: 1.238
│   └── Research_Report_Final.md         # Complete final academic report
├── scripts/
│   ├── download/                        # Data acquisition scripts
│   └── analysis/                        # Analysis scripts (FROZEN — do not re-run)
├── FINAL_SUBMISSION/                    # v1.0 submission package (FROZEN)
├── AGENTS.md                            # Root rules for all AI agents
└── website/                             # Next.js interactive research platform
    ├── lib/content/documents.ts         # All registered documents
    ├── lib/results/config.ts            # Figure phases and table definitions
    ├── lib/dashboard/config.ts          # Dashboard pipeline + timeline
    ├── public/figures/                  # All research figures (38 total)
    └── public/tables/                   # All CSV tables (11 total)
```

---

## 6. Hard Rules — What Must NOT Be Done

> Any AI agent working on this project MUST follow these rules strictly:

1. ❌ **Do NOT re-run California analysis scripts** — v1.0 results are frozen
2. ❌ **Do NOT retune the Swiss STA/LTA threshold (8.0)** — STEP 2K is frozen
3. ❌ **Do NOT train any ML model on Swiss Set A data** — STEP 3A is NO-GO; no independent labels exist
4. ❌ **Do NOT modify FINAL_SUBMISSION/ contents**
5. ❌ **Do NOT modify or add events to Swiss Set C** — it is a locked validation set
6. ❌ **Do NOT treat EarthESND as the main goal** — it is reference only
7. ✅ **DO update PROJECT_STATUS, ROADMAP, and CHANGELOG** when any new milestone is completed

---

## 7. What's Next (Planned)

### Immediate Blocker
- Acquire **official first-P wave arrival picks (analyst picks)** from the Swiss SED catalog for the 20 Set A training events
- **This is the ONLY thing blocking ML training**

### Version 2.1 (Website Maintenance)
- Deploy website to Vercel or GitHub Pages
- Add contact form backend
- Embed presentation PDF viewer
- Automated end-to-end test suite

### Version 3.0 (Future Science)
- Train supervised ML models on Swiss Set A (once SED analyst picks are available)
- Expand to broader European datasets via ORFEUS/EIDA networks
- Real-time streaming simulation (SeedLink-based continuous STA/LTA)
- Cross-region (USA vs Europe) detection performance comparison
- Optional: EarthESND model training on Western data

---

## 8. Key Numbers to Know

| Metric | Value |
|--------|-------|
| California pilot events | 8 |
| Swiss Set A events | 20 |
| Swiss Set A waveforms | 120 (CH HH 3-component) |
| Swiss Set C (validation) events | 15 |
| Swiss Set C waveforms | 550 (CH HHZ) |
| STA/LTA threshold (pre-declared, frozen) | **8.0** |
| Swiss detection rate (Set C) | **72.9%** |
| Swiss median timing error (Set C) | **1.24 seconds** |
| Website pages | 27 |
| Research figures on website | 38 |
| Data tables on website | 11 |
| Search index records | 122 |

---

## 9. Document Reading Order (for any new agent)

1. `AGENTS.md` — root rules (brief)
2. `docs/PROJECT_CHARTER.md` — full scope and priorities
3. `docs/AI_AGENT.md` — what to do and what NOT to do
4. `docs/PROJECT_STATUS.md` — current status of everything
5. `docs/ROADMAP.md` — planned future work
6. `reports/Research_Report_Final.md` — full academic report
7. `docs/SWISS_ML_FEASIBILITY_AUDIT.md` — why ML is blocked
8. `docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md` — Swiss validation numbers

---

*Generated: 2026-11-06. Project science frozen at v1.0.0 (California) and STEP 2K (Swiss). Website at v2.1.*
