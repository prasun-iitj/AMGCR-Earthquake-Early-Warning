# IMPLEMENTATION_PLAN.md

Tracks **what was built** in the repository and **Version 2.0** implementation targets, aligned with [PROJECT_CHARTER.md](PROJECT_CHARTER.md).

**v1.0 submission:** complete — no open certificate implementation tasks.

---

## Part 1 — Foundation (archived ✅)

### Phase 1 — Repository initialization ✅

### Phase 2A — Acquisition framework ✅

### Phase 2B — Event catalogue retrieval ✅

(See [CHANGELOG.md](CHANGELOG.md) v0.1–v0.3.)

---

## Part 2 — EarthESND reference implementation (archived ✅)

| Deliverable | Status |
|-------------|--------|
| Config, preprocessing, models, evaluation | ✅ |
| 88 tests (full reference checkout) | ✅ |
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

## Part 5 — Version 2.0 / future implementation (planned)

Not started unless explicitly prioritised. See [ROADMAP.md](ROADMAP.md).

| Theme | Examples |
|-------|----------|
| Web & UX | Interactive project website, public dashboard, interactive visualisations |
| Data | Europe dataset expansion, additional Western catalogues |
| ML | EarthESND-inspired training/evaluation on Western tensors; tabular baselines |
| Operations | Real-time streaming (SeedLink), latency budgets, production deployment |
| Quality | Instrument response caching, pre-origin noise windows, larger **N** |

---

## Part 6 — Optional (EarthESND scientific reproduction)

Execute [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md) only if explicitly prioritised (Version 2.0 / optional reference track).

---

Version: **1.3.0** (v1.0.0 submission release)
