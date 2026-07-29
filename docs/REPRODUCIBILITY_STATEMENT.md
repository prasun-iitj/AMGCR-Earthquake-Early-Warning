# REPRODUCIBILITY_STATEMENT.md

**Deliverable D-S1 — Reproducibility statement**  
**Project:** AMGCR Earthquake Research  
**Scope:** California IRIS / EarthScope FDSN pilot (acquisition → feature matrix)  
**Date:** 29 July 2026  

This document describes how to reproduce the **completed certificate-track California pilot workflow** documented in the repository. It does **not** cover EarthESND K-NET scientific reproduction or future European pilots.

**Related:** [DATA_AVAILABILITY_STATEMENT.md](DATA_AVAILABILITY_STATEMENT.md) · [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) · [FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md)

---

## 1. What this workflow reproduces

The pilot chain implemented in `scripts/download/` and `scripts/analysis/` produces:

1. Event manifest and raw MiniSEED under `data/` (when download is run)  
2. Phase A.1 EDA — summaries, inspection CSV, four EDA figures  
3. Phase A.2 Signal analysis — per-event metrics JSON, eight four-panel figures, summary table  
4. Phase B.1 Preprocessing — frozen config, per-event stage NPZ, eight comparison figures, QC table  
5. Phase B.2 Feature engineering — **8×18** feature matrix, correlation table, four feature figures  

Narrative interpretation lives in `docs/EDA_REPORT.md` through `docs/RESULTS_AND_DISCUSSION.md` and in `reports/Research_Proposal_v1.md`. Those reports **describe** outputs; they do not re-run computations.

The **EarthESND reference implementation** in `src/` is separate (88 tests when the full reference tree is installed). **California pilot results were not produced with EarthESND modules** (`docs/RESULTS_AND_DISCUSSION.md`).

---

## 2. Software environment

| Requirement | Source |
|-------------|--------|
| **Python** | ≥ 3.11 (`pyproject.toml`) |
| **Core packages** | ObsPy ≥ 1.5, NumPy, Pandas, Matplotlib, SciPy, PyYAML (`pyproject.toml`) |
| **Optional (reference track only)** | pytest ≥ 9.1 (`pyproject.toml` `[project.optional-dependencies] dev`) |

**Suggested setup** (from repository root):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

There is **no** separate `requirements.txt`; dependencies are declared in `pyproject.toml`.

**Network:** FDSN download and optional instrument-response steps require internet access to USGS and EarthScope services.

---

## 3. Execution order

Run all commands from the **repository root**. Stages depend on prior outputs as shown.

```text
Step 0  Acquisition     → data/raw/iris/, data/manifests/iris_california_pilot_events.csv, logs/iris_california_pilot_summary.json
Step 1  EDA (A.1)       → reports/eda/, reports/tables/event_summary.csv, station_summary.csv, reports/figures/ (4 EDA PNGs)
Step 2  Signal (A.2)    → reports/signal_analysis/, reports/tables/signal_analysis_per_event.csv, reports/figures/ (8 signal PNGs)
Step 3  Preprocess (B.1)→ reports/preprocessing/, reports/tables/preprocessing_quality_metrics.csv, reports/figures/ (8 preprocessing PNGs)
Step 4  Features (B.2)  → reports/features/, reports/tables/feature_matrix.csv, feature_correlation_matrix.csv, reports/figures/ (4 feature PNGs)
```

### Step 0 — Download (optional if raw data already present)

Documented in [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) §4:

```powershell
python scripts/download/download_iris_california_pilot.py --event-count 8 --min-events 5
```

Optional CLI paths: `--raw-dir`, `--manifest-csv` (defaults: `data/raw/iris/`, `data/manifests/iris_california_pilot_events.csv`). The script writes a JSON summary to **`logs/iris_california_pilot_summary.json`** by default (see `scripts/download/download_iris_california_pilot.py`).

**Public FDSN pilot — no credentials** ([IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) §4).

### Steps 1–4 — Analysis (manifest-linked traces only)

Commands match phase reports:

```powershell
python scripts/analysis/run_california_pilot_eda.py
python scripts/analysis/run_california_signal_analysis.py
python scripts/analysis/run_california_preprocessing.py
python scripts/analysis/run_california_feature_engineering.py
```

| Step | Script | Primary doc |
|------|--------|-------------|
| 1 | `scripts/analysis/run_california_pilot_eda.py` | [EDA_REPORT.md](EDA_REPORT.md) |
| 2 | `scripts/analysis/run_california_signal_analysis.py` | [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) |
| 3 | `scripts/analysis/run_california_preprocessing.py` | [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) |
| 4 | `scripts/analysis/run_california_feature_engineering.py` | [FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md) |

Preprocessing parameters for the completed run are recorded in `reports/preprocessing/preprocessing_config.json`. Feature engineering reads **`filtered`** arrays from `reports/preprocessing/<short_id>_stages.npz` and P picks from `reports/signal_analysis/<short_id>_metrics.json` ([FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md)).

---

## 4. Artefacts: included in the repository vs excluded

### 4.1 Typically **included** (version-controlled in this project)

These paths are part of the documented pilot and are intended to be shared via Git (see repository commits; audit date 2026-07-29):

| Category | Paths |
|----------|--------|
| **Scripts** | `scripts/download/download_iris_california_pilot.py`, `scripts/analysis/run_california_*.py` |
| **Manifest** | `data/manifests/iris_california_pilot_events.csv` |
| **Phase documentation** | `docs/IRIS_DATASET_REPORT.md`, `docs/EDA_REPORT.md`, `docs/SIGNAL_ANALYSIS_REPORT.md`, `docs/PREPROCESSING_REPORT.md`, `docs/FEATURE_ENGINEERING_REPORT.md`, `docs/RESULTS_AND_DISCUSSION.md` |
| **Tables & summaries** | `reports/tables/*.csv`, `reports/eda/*.json`, `reports/eda/mseed_file_inspection.csv`, `reports/signal_analysis/*.json`, `reports/preprocessing/*.json`, `reports/features/*.json`, `reports/features/feature_matrix.csv` |
| **Intermediate arrays** | `reports/preprocessing/*_stages.npz`, per-event metrics JSON under `reports/signal_analysis/` and `reports/preprocessing/` |
| **Consolidated narrative** | `reports/Research_Proposal_v1.md` |

Exact Git tracking may vary by commit; the **manifest and analysis outputs under `reports/` (except figures)** were part of the completed pilot deliverable set per [FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md).

### 4.2 **Intentionally excluded** from Git (`.gitignore`)

| Path / pattern | Reason | How to obtain |
|----------------|--------|----------------|
| **`data/raw/`** (including `data/raw/iris/*.mseed`) | Raw waveforms are large and immutable inputs; re-fetched from FDSN | Step 0 download script |
| **`logs/`** (including `logs/iris_california_pilot_summary.json`) | Local run logs | Created when Step 0 runs |
| **`figures/`** (matches **`reports/figures/`**) | Generated PNG outputs; reproducible from analysis scripts | Steps 1–4 |
| **`data/interim/`**, **`data/processed/`**, **`data/output/`** | Reserved for other pipelines | Not used for this pilot’s published matrix |
| **`.venv/`**, **`.env`** | Local environment and secrets | User-created |

Audit finding ([FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md) §1, §5): on a **fresh clone**, **24 PNGs** under `reports/figures/` and **raw MiniSEED** are **not** present unless regenerated or supplied in a separate archive.

### 4.3 Local-only nuance (documented, not a separate Git policy)

[EDA_REPORT.md](EDA_REPORT.md) and `reports/eda/mseed_file_inspection.csv` record **twelve** MiniSEED files on disk at EDA time (**eight** manifest-linked + **four legacy** from an earlier download). **All completed analyses use the eight manifest-linked records only.**

---

## 5. Regenerating excluded artefacts

| Excluded artefact | Regeneration |
|-------------------|--------------|
| Raw MiniSEED | `python scripts/download/download_iris_california_pilot.py --event-count 8 --min-events 5` |
| Acquisition JSON log | Same download run → `logs/iris_california_pilot_summary.json` |
| EDA figures (4) | `python scripts/analysis/run_california_pilot_eda.py` |
| Signal figures (8) | `python scripts/analysis/run_california_signal_analysis.py` |
| Preprocessing figures (8) | `python scripts/analysis/run_california_preprocessing.py` (requires prior signal metrics for consistency with documented chain) |
| Feature figures (4) | `python scripts/analysis/run_california_feature_engineering.py` (requires preprocessing NPZ + signal metrics) |

Full figure index: `reports/Research_Proposal_v1.md` Appendix A; filenames listed in phase reports.

---

## 6. Reproducibility limitations

These limits are **documented project findings**, not new science:

1. **FDSN variability** — Re-running Step 0 may yield different events or stations if catalog or dataselect availability changes; the **published manifest** (8 events, CI.ADO / CI.USC) reflects the **2026-07-29** run ([IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) §3).  
2. **Station selection** — Fixed distance-ranked candidate list; not uniform network sampling ([IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) §2.2, §5).  
3. **Origin-aligned windows** — 300 s from catalog origin; no pre-event quiet time for noise ([SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) §1.2).  
4. **Instrument response** — Preprocessing run: response removal **0/8 applied**; filtered traces remain in **counts** ([PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) §4).  
5. **Small sample** — **N = 8** events, single **BHZ** component; statistics are illustrative ([RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md)).  
6. **EarthESND** — Reference code in `src/` is **not** on the California reproduction path.  
7. **Bit-identical PNGs** — Matplotlib/ObsPy versions may produce minor visual differences; tabular/json outputs should match for the same inputs and manifest.

---

## 7. Verification pointers

After regeneration, compare against frozen summaries (completed pilot):

- `reports/eda/dataset_summary.json`  
- `reports/signal_analysis/signal_analysis_summary.json`  
- `reports/preprocessing/preprocessing_summary.json`  
- `reports/features/feature_summary.json`  

Phase reports and [FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md) list expected file counts (e.g. **24** PNGs, **8** manifest events).

---

## 8. References (software and methods cited in repository)

Krischer, L., Megies, T., Barsch, R., Beyreuther, M., Lecocq, T., Caudron, C., and Wassermann, J. (2015). ObsPy: A bridge for earthquake science. *Seismological Research Letters*, 86(3), 765–771.

International Federation of Digital Seismograph Networks (FDSN). FDSN web services specification. https://www.fdsn.org/webservices/

**Project documentation:** [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md), phase analysis reports under `docs/`, [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md) §12.

---

**Document control:** D-S1 reproducibility statement v1.0 — 29 July 2026. No source code modified to produce this file.
