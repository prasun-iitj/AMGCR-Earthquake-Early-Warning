# IMPLEMENTATION_PLAN.md

Tracks **what was built** in the repository and **what to implement next**, aligned with [PROJECT_CHARTER.md](PROJECT_CHARTER.md).

---

## Part 1 — Foundation (completed)

### Phase 1 — Repository initialization ✅

### Phase 2A — Acquisition framework ✅

### Phase 2B — Event catalogue retrieval ✅

(See prior sections in git history / v0.3.0 changelog.)

---

## Part 2 — EarthESND reference implementation (completed)

| Deliverable | Status |
|-------------|--------|
| Config, preprocessing, models, evaluation | ✅ |
| 88 tests (full reference checkout) | ✅ |
| Scientific paper reproduction | ⬜ Not started |

See [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md).

---

## Part 3 — USA dataset workflow (completed)

| Step | Artifact |
|------|----------|
| ObsPy FDSN integration | `scripts/download/download_iris_california_pilot.py` |
| 8-event California pilot | `data/raw/iris/`, manifest CSV |
| Acquisition report | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |

---

## Part 4 — Phase A — USA waveform analysis

### Phase A.1 — EDA ✅

- [x] `scripts/analysis/run_california_pilot_eda.py`
- [x] Dataset summary, MiniSEED inspection CSV
- [x] Figures: example waveform, magnitude histogram, events over time, station usage
- [x] Tables: `event_summary.csv`, `station_summary.csv`
- [x] [EDA_REPORT.md](EDA_REPORT.md)

### Phase A.2 — Signal analysis ✅

- [x] `scripts/analysis/run_california_signal_analysis.py`
- [x] Per-event metrics (peak, RMS, noise, SNR, duration, STA/LTA P pick)
- [x] Eight four-panel figures in `reports/figures/signal_analysis_*.png`
- [x] `reports/tables/signal_analysis_per_event.csv`
- [x] [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md)

### Phase A.3 — Proposal & literature 🔄

- [ ] Introduction, Dataset, Methodology, Expected outcomes
- [ ] Literature review document or section

---

## Part 5 — Next implementation

### Phase B — Signal processing ⬜

- [ ] Filter/detrend/QC pipeline on pilot data
- [ ] Pre-origin FDSN windows for noise estimation
- [ ] Features under `data/processed/`

### Phase C — European extension ⬜

### Phase D — AI methods ⬜

---

## Part 6 — Optional (EarthESND scientific reproduction)

Execute [DATASET_ACQUISITION_PLAN.md](DATASET_ACQUISITION_PLAN.md) only if explicitly prioritised.

---

Version: **1.1.0**
