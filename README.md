# AMGCR Earthquake Research

Reproducible **AI-assisted Earthquake Early Warning (EEW)** research for **Western seismic regions**, developed in the context of a **Swiss certificate programme**.

**Release:** **v1.0.0 — Submission Release** (29 July 2026) · [RELEASE_SUMMARY_v1.0.md](RELEASE_SUMMARY_v1.0.md)

## Start here

| Document | Role |
|----------|------|
| **[docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md)** | **Authoritative** vision, scope, status, roadmap |
| [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | Milestones and Version 2.0 roadmap |
| [RELEASE_SUMMARY_v1.0.md](RELEASE_SUMMARY_v1.0.md) | **v1.0 submission** overview and deliverables |
| [FINAL_SUBMISSION/FINAL_SUBMISSION_README.md](FINAL_SUBMISSION/FINAL_SUBMISSION_README.md) | PDF/DOCX/PPTX submission package |
| [docs/RESEARCH_DIRECTION.md](docs/RESEARCH_DIRECTION.md) | Reference vs active research; Europe vs California |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Archived v1.0 milestones · Version 2.0 future work |

**AI assistants:** read [docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md) and [docs/AI_AGENT.md](docs/AI_AGENT.md).

## Primary research goal

1. **Europe** — primary long-term research focus (proposal, theory, datasets).
2. **United States / California** — **completed pilot** for method development (ObsPy, IRIS/EarthScope).

**EarthESND** is a **reference implementation only** (literature, architecture, AI methodology)—**not** the programme objective. Reference software: **complete**; K-NET scientific paper reproduction: **not started**.

## v1.0 submission status (complete)

| Component | Status |
|-----------|--------|
| EarthESND reference implementation | ✅ **Complete** |
| USA / California IRIS–EarthScope pilot | ✅ **Complete** |
| EDA | ✅ **Complete** |
| Signal analysis | ✅ **Complete** |
| Preprocessing | ✅ **Complete** |
| Feature engineering | ✅ **Complete** |
| Results & discussion | ✅ **Complete** |
| Reproducibility Statement (D-S1) | ✅ **Complete** |
| Data Availability Statement (D-S2) | ✅ **Complete** |
| Final Research Report (D-F1) | ✅ **Complete** |
| Presentation outline & script (D-F2/D-F3) | ✅ **Complete** |
| FINAL_SUBMISSION package (D-F4) | ✅ **Complete** |
| Submission validation | ✅ **PASS** ([VALIDATION_SUMMARY.md](FINAL_SUBMISSION/VALIDATION_SUMMARY.md)) |

**Version 2.0 / future work** is documented in [docs/ROADMAP.md](docs/ROADMAP.md) (website, dashboard, Europe expansion, ML, streaming, deployment). The **v1.0 analysis chain is frozen** at 2026-07-29 artefacts.

## Key reports and deliverables

| Report | Path |
|--------|------|
| **Final report (primary)** | [reports/Research_Report_Final.md](reports/Research_Report_Final.md) |
| Proposal (v1, superseded for submission) | [reports/Research_Proposal_v1.md](reports/Research_Proposal_v1.md) |
| Acquisition | [docs/IRIS_DATASET_REPORT.md](docs/IRIS_DATASET_REPORT.md) |
| EDA | [docs/EDA_REPORT.md](docs/EDA_REPORT.md) |
| Signal analysis | [docs/SIGNAL_ANALYSIS_REPORT.md](docs/SIGNAL_ANALYSIS_REPORT.md) |
| Preprocessing | [docs/PREPROCESSING_REPORT.md](docs/PREPROCESSING_REPORT.md) |
| Features | [docs/FEATURE_ENGINEERING_REPORT.md](docs/FEATURE_ENGINEERING_REPORT.md) |
| Interpretation | [docs/RESULTS_AND_DISCUSSION.md](docs/RESULTS_AND_DISCUSSION.md) |
| Reproducibility | [docs/REPRODUCIBILITY_STATEMENT.md](docs/REPRODUCIBILITY_STATEMENT.md) |
| Data availability | [docs/DATA_AVAILABILITY_STATEMENT.md](docs/DATA_AVAILABILITY_STATEMENT.md) |
| Presentation | [reports/Presentation_Outline_D-F2.md](reports/Presentation_Outline_D-F2.md) · [reports/Presentation_Script_D-F3.md](reports/Presentation_Script_D-F3.md) |

Analysis artefacts: `reports/eda/`, `reports/signal_analysis/`, `reports/preprocessing/`, `reports/features/`, `reports/figures/`, `reports/tables/`.

## Repository structure

```text
AMGCR_Earthquake_Research/
├── FINAL_SUBMISSION/       # v1.0 PDF/DOCX/PPTX + checklists (official submission)
├── configs/                # EarthESND reference + acquisition YAML
├── data/manifests/         # California pilot event CSV (tracked)
├── data/raw/iris/          # Pilot MiniSEED (local; gitignored — see D-S2)
├── docs/                   # Charter, phase reports, submission statements
├── reports/                # Final report, figures, tables, presentation assets
├── scripts/download/       # FDSN pilot download (executed)
├── scripts/analysis/       # EDA → features (executed; frozen)
├── src/                    # acquisition + EarthESND reference
└── tests/
```

## Technology stack

Python 3.11+, ObsPy, NumPy, Pandas, Matplotlib, SciPy, PyYAML, Git.

## Verification

- EarthESND reference: **88 passing tests** when the full reference tree imports (`python -m pytest`).
- California pilot: **8×18** feature matrix, **24** figures — see [FINAL_SUBMISSION/VALIDATION_SUMMARY.md](FINAL_SUBMISSION/VALIDATION_SUMMARY.md).

## Version

**v1.0.0 — Submission Release** (documentation **1.3.0**). See [docs/CHANGELOG.md](docs/CHANGELOG.md).
