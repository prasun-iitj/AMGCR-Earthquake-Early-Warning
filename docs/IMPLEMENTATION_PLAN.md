# IMPLEMENTATION_PLAN.md

Tracks **what was built** in the repository. **Version 2.0 platform** is **complete** (August 2026). Future targets: [ROADMAP.md](ROADMAP.md) (v2.1 / v3.0).

**v1.0 submission:** complete — science frozen. **v2.0 platform:** complete — see [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md).

---

## Part 1 — Foundation (archived ✅)

### Phase 1 — Repository initialization ✅

### Phase 2A — Acquisition framework ✅

### Phase 2B — Event catalogue retrieval ✅

(See [CHANGELOG.md](CHANGELOG.md) v0.1–v0.3.)

---

## Part 2 — EarthESND literature track (archived ✅)

| Deliverable | Status |
|-------------|--------|
| Paper reproduction plan and references | ✅ Documented |
| Executable EarthESND pipeline in v1.0.0 | ⬜ Not included (optional v3.0) |
| Scientific paper reproduction | ⬜ Not started (optional) |

See [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md).

---

## Part 3 — USA dataset workflow (archived ✅)

| Step | Artifact |
|------|----------|
| ObsPy FDSN integration | `scripts/download/download_iris_california_pilot.py` |
| 8-event California pilot | `data/raw/iris/`, manifest CSV |
| Acquisition report | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |

---

## Part 4 — California pilot analysis & reporting (archived ✅)

### Phase A.1 — EDA ✅

- [x] `scripts/analysis/run_california_pilot_eda.py`
- [x] `docs/EDA_REPORT.md`, `reports/eda/`

### Phase A.2 — Signal analysis ✅

- [x] `scripts/analysis/run_california_signal_analysis.py`
- [x] `docs/SIGNAL_ANALYSIS_REPORT.md`, `reports/signal_analysis/`

### Phase B.1 — Preprocessing ✅

- [x] `scripts/analysis/run_california_preprocessing.py`
- [x] `docs/PREPROCESSING_REPORT.md`, `reports/preprocessing/`

### Phase B.2 — Feature engineering ✅

- [x] `scripts/analysis/run_california_feature_engineering.py`
- [x] `docs/FEATURE_ENGINEERING_REPORT.md`, `reports/features/`

### Phase C — Results & discussion ✅

- [x] [RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md)

### Phase D — Submission deliverables ✅

- [x] [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md)
- [x] [Research_Report_Final.md](../reports/Research_Report_Final.md)
- [x] [REPRODUCIBILITY_STATEMENT.md](REPRODUCIBILITY_STATEMENT.md), [DATA_AVAILABILITY_STATEMENT.md](DATA_AVAILABILITY_STATEMENT.md)
- [x] Presentation outline, script, [FINAL_SUBMISSION/](../FINAL_SUBMISSION/) — validation **PASS**

---

## Part 5 — Version 2.0 platform (complete ✅ — August 2026)

Implemented in `website/` — platform version **2.0.0**. See [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md).

| Theme | Status |
|-------|--------|
| Interactive website & dashboard | ✅ Complete |
| Workflow, results, dataset, waveform, map explorers | ✅ Complete |
| Documentation portal & global search | ✅ Complete |
| SEO, error pages, accessibility polish | ✅ Complete |

---

## Part 6 — Version 2.1 / 3.0 (planned)

See [ROADMAP.md](ROADMAP.md).

| Theme | Version | Examples |
|-------|---------|----------|
| Platform maintenance | 2.1 | Deployment, E2E tests, contact backend, embedded PDF |
| Data | 3.0 | Europe dataset expansion, additional Western catalogues |
| ML | 3.0 | EarthESND training/evaluation; tabular baselines |
| Operations | 3.0 | Real-time streaming (SeedLink), operational deployment |
| Quality | 3.0 | Instrument response caching, pre-origin noise windows, larger **N** |

---

## Part 7 — Optional (EarthESND scientific reproduction)

Execute [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md) only if explicitly prioritised (Version 3.0 / optional reference track).

---

Version: **1.4.0** (v2.0.0 platform release · science v1.0.0 frozen)
