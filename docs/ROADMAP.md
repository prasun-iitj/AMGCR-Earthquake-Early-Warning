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
| **EarthESND literature track** | ✅ | [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md) |
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

## Version 2.0 platform (complete — 2 August 2026)

All items below were **completed** for the public interactive research platform in `website/` (platform version **2.0.0**). Science baseline remains **v1.0.0** (frozen).

| Milestone | Status | Route / output |
|-----------|--------|----------------|
| Interactive project website | ✅ | `/` — hero slideshow, highlights, timeline |
| Public dashboard | ✅ | `/dashboard` |
| Workflow explorer | ✅ | `/workflow` |
| Results explorer (figures & tables) | ✅ | `/results` — 24 figures, 6 tables |
| Dataset explorer | ✅ | `/dataset` |
| Waveform explorer | ✅ | `/waveforms` — 8 pilot events |
| Earthquake map | ✅ | `/map` |
| Documentation portal | ✅ | `/docs`, `/research/report` |
| Global search | ✅ | `Ctrl+K` — 114 indexed records |
| Resources & GitHub pages | ✅ | `/resources`, `/github` |
| About & contact | ✅ | `/about`, `/contact` |
| SEO, error pages, accessibility | ✅ | sitemap, robots, OG image, 404/error |
| Release & deployment docs | ✅ | `docs/V2_*.md`, `website/CHANGELOG.md` |

See [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md) · [website/README.md](../website/README.md)

---

## Version 2.1 (planned)

Platform maintenance and polish — **not** new science.

- Production deployment on Vercel (or GitHub Pages fallback)
- Content sync when repository docs change
- Optional contact-form backend
- Embedded presentation PDF viewer
- Automated E2E test suite
- Performance monitoring post-launch

---

## Version 3.0 (planned)

Science and infrastructure expansion — **not** part of v1.0 or v2.0 scope.

### 1. European and extended datasets

- **Europe dataset expansion** — ORFEUS/EIDA and national FDSN endpoints  
- **Additional datasets** — scaled California/Western USA catalogues; optional K-NET track  
- Cross-region feature comparison (USA vs Europe)

### 2. Machine learning and evaluation

- **EarthESND model training and evaluation** on Western data (deviation log vs Japan paper)  
- Tabular and waveform baselines on `feature_matrix.csv` and NPZ stages  
- Comparative evaluation vs literature with documented metrics

### 3. Real-time and operations

- **Real-time streaming support** (e.g. SeedLink simulation, continuous STA/LTA)  
- Latency budgets and onsite feature push prototypes  
- **Production EEW deployment** path (operational integration, governance, uncertainty communication)

### 4. Data quality and science hardening

- Instrument response caching and physical-unit amplitudes  
- Pre-origin download windows for unbiased noise/SNR  
- Three-component data where available  
- Stratified sampling by magnitude, distance, and azimuth  

Optional reference track: K-NET paper tables — ⬜ not started ([PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md)).

---

## Milestone summary

| Track | v1.0 | v2.0 | v2.1 / v3.0 |
|-------|------|------|-------------|
| Reference (EarthESND literature) | ✅ Documented | — | Optional executable track (v3.0) |
| California pilot science | ✅ Complete | — | Scale / extend (v3.0) |
| Submission deliverables | ✅ Complete | — | — |
| Web / dashboard / explorers | — | ✅ Complete | Maintenance (v2.1) |
| Europe / ML / streaming / deploy | — | — | ⬜ Planned (v3.0) |

---

Version: **1.4.0** (v2.0.0 platform release · science v1.0.0 frozen)
