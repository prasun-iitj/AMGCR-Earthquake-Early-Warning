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
│   ├── manifests/             # Tracked California + Swiss event CSVs
│   ├── metadata/              # Swiss StationXML (XML often gitignored)
│   └── raw/                   # MiniSEED, sample catalogues (often gitignored)
├── docs/                      # Charter, phase reports, submission statements
├── references/                # Literature (EarthESND paper notes, REFERENCES)
├── reports/                   # Final report, figures, tables, JSON/NPZ artefacts
├── scripts/
│   ├── download/              # FDSN California pilot download (executed)
│   └── analysis/              # EDA → features pipeline (executed; frozen)
├── src/
│   ├── acquisition/           # Generic FDSN acquisition modules
│   └── models/                  # Reserved stub (EarthESND optional v3.0 track)
├── tests/                     # pytest (9 acquisition tests in v1.0.0)
├── website/                   # Version 2.0 interactive platform (Next.js 16)
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
| `manifests/sed_switzerland_pilot_events.csv` | **20** Swiss SED development events / **120** event–station rows (tracked) |
| `manifests/sed_switzerland_validation_candidates.csv` | Independent Swiss/Adjacent-Border validation **candidate pool** (tracked) |
| `manifests/sed_switzerland_validation_waveforms.csv` | STEP 2J event–station HHZ acquisition manifest (tracked; MiniSEED gitignored) |
| `manifests/sed_switzerland_validation_picks.csv` | Same-station SED first-P provenance for acquired records |
| `raw/iris/` | California MiniSEED by event id (local; often gitignored — [DATA_AVAILABILITY_STATEMENT.md](DATA_AVAILABILITY_STATEMENT.md)) |
| `raw/switzerland/` | Swiss MiniSEED by event id (local; gitignored) |
| `raw/switzerland_validation/` | Set C validation MiniSEED by event id (local; gitignored) |
| `metadata/switzerland/` | Swiss StationXML (XML gitignored; regenerable) |
| `metadata/switzerland_validation/` | Set C StationXML (XML gitignored; regenerable) |
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
| Swiss independent validation | `switzerland_validation/` (STEP 2K metrics/JSON); `switzerland_validation_acquisition/`; `switzerland_validation_audit/` |
| Tables & figures | `tables/`, `figures/` (figures often gitignored; regenerate per D-S1) |
| Proposal v1 | `Research_Proposal_v1.md` (superseded for submission) |

---

## scripts/

- `download/download_iris_california_pilot.py` — USGS + EarthScope California acquisition (**frozen**)  
- `download/download_sed_switzerland_pilot.py` — SED/ETH Swiss methods-transfer acquisition  
- `download/download_sed_switzerland_validation.py` — locked Set C validation MiniSEED/StationXML (STEP 2J)  
- `audit/audit_swiss_validation_candidates.py` — independent Swiss validation-set catalogue/availability audit (no MiniSEED)  
- `analysis/run_swiss_independent_validation.py` — frozen STA/LTA evaluation on Set C (STEP 2K; threshold 8.0 not retuned)  
- `analysis/run_california_*.py` — frozen v1.0 analysis chain  

Do **not** change California analysis scripts for documentation-only releases unless explicitly approved.

---

## src/

- **`acquisition/`** — reusable FDSN catalogue/waveform helpers  
- **`analysis/`** — Swiss signal/STA-LTA helpers (Set A and frozen Set C validation); California analysis remains in `scripts/analysis/`  
- **`models/`** (EarthESND reference) — preprocessing, ESN/DENN, evaluation; **reference only** for certificate science  

Configs: `configs/earthesnd/`.

---

## tests/

Unit and integration tests for the acquisition framework. **9 passing** tests in v1.0.0 (`python -m pytest`).

---

## website/

**Version 2.0 interactive platform** (Next.js 16, TypeScript, Tailwind v4). Separate from v1.0 science — does not modify analysis scripts or reports.

| Path | Role |
|------|------|
| `website/app/` | App Router pages (19 public routes) |
| `website/components/` | UI, explorers, layout |
| `website/lib/` | Build-time loaders, SEO, navigation |
| `website/public/` | Hero images, OG image; figures/tables/waveforms synced at build |
| `website/scripts/` | Asset sync + search index builders |

See [website/README.md](../website/README.md) and [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md).

---

## Naming conventions

- Python modules: `snake_case`
- Reports and docs: `UPPER_SNAKE` or descriptive `Title_Case` filenames as established
- One responsibility per script; manifests document every acquisition

---

Version: **1.4.0** (v2.0.0 platform release · science v1.0.0 frozen)
