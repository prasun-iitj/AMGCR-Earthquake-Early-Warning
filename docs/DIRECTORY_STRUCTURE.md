# DIRECTORY_STRUCTURE.md

Purpose of major directories and files in **AMGCR Earthquake Research** ( **v1.0.0 Submission Release** ).

Authoritative scope: [PROJECT_CHARTER.md](PROJECT_CHARTER.md) · Index: [PROJECT_GUIDE.md](PROJECT_GUIDE.md)

---

## Root structure

```text
AMGCR_Earthquake_Research/
├── FINAL_SUBMISSION/          # Official v1.0 PDF/DOCX/PPTX + validation
├── configs/                   # EarthESND reference YAML + acquisition config
├── data/
│   ├── manifests/             # Tracked pilot event CSV
│   └── raw/                   # MiniSEED, sample catalogues (often gitignored)
├── docs/                      # Charter, phase reports, submission statements
├── references/                # Literature (EarthESND paper notes, REFERENCES)
├── reports/                   # Final report, figures, tables, JSON/NPZ artefacts
├── scripts/
│   ├── download/              # FDSN California pilot download (executed)
│   └── analysis/              # EDA → features pipeline (executed; frozen)
├── src/
│   ├── acquisition/           # Generic FDSN acquisition modules
│   └── models/                  # EarthESND reference implementation
├── tests/                     # pytest (88 tests on full reference checkout)
├── notebooks/                 # Optional exploration (not on v1.0 critical path)
├── RELEASE_SUMMARY_v1.0.md    # v1.0 release overview
├── README.md
├── AGENTS.md
├── CHANGELOG.md               # Pointer to docs/CHANGELOG.md
└── requirements.txt
```

Legacy or optional paths (`outputs/`, `literature/`) may appear in older notes; **v1.0 artefacts live under `reports/`**.

---

## FINAL_SUBMISSION/

Submission-ready exports (D-F4): final report, presentation, script, D-S1/S2 PDFs, checklists, validation summary. See [FINAL_SUBMISSION/FINAL_SUBMISSION_README.md](../FINAL_SUBMISSION/FINAL_SUBMISSION_README.md).

---

## data/

| Path | Role |
|------|------|
| `manifests/iris_california_pilot_events.csv` | **8** California pilot events (tracked) |
| `raw/iris/` | Pilot MiniSEED by event id (local; often gitignored — [DATA_AVAILABILITY_STATEMENT.md](DATA_AVAILABILITY_STATEMENT.md)) |
| `raw/catalogs/` | Sample QuakeML for generic FDSN tests |
| `processed/` | Reserved; v1.0 features in `reports/features/` |

Details: [DATASET.md](DATASET.md).

---

## docs/

Project governance, phase reports, and submission statements. Start with [PROJECT_CHARTER.md](PROJECT_CHARTER.md), [PROJECT_STATUS.md](PROJECT_STATUS.md), [ROADMAP.md](ROADMAP.md).

---

## reports/

| Area | Examples |
|------|----------|
| Final deliverables | `Research_Report_Final.md`, presentation outline/script |
| Phase artefacts | `eda/`, `signal_analysis/`, `preprocessing/`, `features/` |
| Tables & figures | `tables/`, `figures/` (figures often gitignored; regenerate per D-S1) |
| Proposal v1 | `Research_Proposal_v1.md` (superseded for submission) |

---

## scripts/

- `download/download_iris_california_pilot.py` — USGS + EarthScope pilot acquisition  
- `analysis/run_california_*.py` — frozen v1.0 analysis chain  

Do **not** change analysis scripts for documentation-only releases unless explicitly approved.

---

## src/

- **`acquisition/`** — reusable FDSN catalogue/waveform helpers  
- **`models/`** (EarthESND reference) — preprocessing, ESN/DENN, evaluation; **reference only** for certificate science  

Configs: `configs/earthesnd/`.

---

## tests/

Unit and integration tests for acquisition and EarthESND reference modules. Full tree: **88 passing** tests (`python -m pytest`).

---

## Naming conventions

- Python modules: `snake_case`
- Reports and docs: `UPPER_SNAKE` or descriptive `Title_Case` filenames as established
- One responsibility per script; manifests document every acquisition

---

Version: **1.3.0** (v1.0.0 submission release)
