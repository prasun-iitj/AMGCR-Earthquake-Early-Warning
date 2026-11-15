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

## Version 3.0 (in progress)

Science and infrastructure expansion — **not** part of v1.0 or v2.0 scope. California v1.0.0 remains frozen.

### 1. European and extended datasets

- **Swiss SED methods-transfer acquisition** — ✅ **Complete** (2026-09-06): 20 events, 120 CH HH 3C records, StationXML, pre-event window. See [SED_SWITZERLAND_DATASET_REPORT.md](SED_SWITZERLAND_DATASET_REPORT.md).
- **Swiss independent validation-set design** — ✅ **Corrected** (2026-09-11, STEP 2I.1): Independent Swiss/Adjacent-Border Validation Set; acquisition/detection/noise windows distinguished. See [SWISS_INDEPENDENT_VALIDATION_PLAN.md](SWISS_INDEPENDENT_VALIDATION_PLAN.md).
- **Swiss independent validation acquisition** — ✅ **Complete** (2026-09-11, STEP 2J): origin−60 s → origin+90 s; 15/15 events, 550 CH HHZ records. See [SWISS_VALIDATION_ACQUISITION_REPORT.md](SWISS_VALIDATION_ACQUISITION_REPORT.md).
- **Swiss independent frozen STA/LTA validation** — ✅ **Complete** (2026-09-11, STEP 2K): pre-declared threshold **8.0** evaluated on locked Set C; 550/550 records; **no** retuning. See [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md).
- **Swiss ML feasibility audit** — ✅ **Complete** (2026-09-11, STEP 3A): **NO-GO** (no independent Set A labels; no Swiss feature matrix; no model trained). See [SWISS_ML_FEASIBILITY_AUDIT.md](SWISS_ML_FEASIBILITY_AUDIT.md).
- **AI/ML certificate wrap** — ✅ **Complete** (2026-11-11): position paper and 16-slide deck; still no training. See [AI_ML_CERTIFICATE_WRAP.md](AI_ML_CERTIFICATE_WRAP.md).
- **Europe dataset expansion** — further ORFEUS/EIDA / national FDSN endpoints  
- **Additional datasets** — scaled California/Western USA catalogues; optional K-NET track  
- Cross-region feature comparison (USA vs Europe) — **not started**

### 2. Machine learning and evaluation

- **Swiss Set A SED analyst pick acquisition** — ✅ **Complete** (2026-11-12, STEP ML-1A): 120/120 (100%) manual first-P picks verified and persisted into `data/manifests/sed_switzerland_set_a_picks.csv`. Unblocks supervised ML.
- **Swiss Set A 3C feature extraction** — ✅ **Complete** (2026-11-12, STEP ML-2): 240 causal window samples (120 P-wave + 120 noise) across 24 physical velocity & 3C features in `reports/features/swiss_set_a_feature_matrix.csv`.
- **Swiss supervised ML models (RF, XGBoost)** — ✅ **Complete** (2026-11-12, STEP ML-3): Random Forest (Accuracy 99.17%, F1 0.9916), XGBoost (Accuracy 98.33%, F1 0.9832) trained on Swiss Set A with 20-fold Leave-One-Group-Out CV; benchmarked against STA/LTA (F1 0.9386). Zero cross-station event leakage. See [ML_RESULTS_REPORT.md](ML_RESULTS_REPORT.md).
- **Swiss Set C vertical-only independent evaluation** — ✅ **Complete** (2026-11-12, STEP ML-4): 18-feature vertical-only models trained on Set A (RF LOGO F1=0.9789, XGB LOGO F1=0.9832) and independently evaluated on locked Set C (N=1,100, 15 events, 79 stations). RF Set C F1=0.9125 (AUC=0.9767), XGB Set C F1=0.9169 (AUC=0.9780), STA/LTA F1=0.5014. ML models reduced missed detections by 77.9% vs STA/LTA. Zero Set C data used in training or tuning. See [SET_C_VERTICAL_ML_EVALUATION_REPORT.md](SET_C_VERTICAL_ML_EVALUATION_REPORT.md).
- **Independent Set C held-out evaluation** — ✅ **Complete** via STEP ML-4 vertical experiment.
- **EarthESND model training and evaluation** on Western data (deviation log vs Japan paper) — not started  
- Tabular and waveform baselines on California `feature_matrix.csv` (N=8) — not scientifically sufficient as a Swiss ML path  
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
| Europe / ML / streaming / deploy | — | — | Swiss Set A analysis ✅; Set C frozen validation ✅; STEP ML-1A labels ✅; STEP ML-2 features ✅; STEP ML-3 ML models ✅; STEP ML-4 Set C eval ✅ |

---

Version: **1.8.0** (v2.0.0 platform release · science v1.0.0 frozen · STEP ML-4 vertical Set C eval complete)
