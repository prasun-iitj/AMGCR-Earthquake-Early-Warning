# AMGCR Earthquake Research

Reproducible **AI-assisted Earthquake Early Warning (EEW)** research for **Western seismic regions**, developed in the context of a **Swiss certificate programme**.

**Release:** **v1.0.0 — Submission Release** (29 July 2026) · [RELEASE_SUMMARY_v1.0.md](RELEASE_SUMMARY_v1.0.md)

## Start here

| Document | Role |
|----------|------|
| **[docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md)** | **Authoritative** vision, scope, status, roadmap |
| [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | Milestones · v2.0 platform status |
| [docs/V2_RELEASE_NOTES.md](docs/V2_RELEASE_NOTES.md) | **Version 2.0** interactive platform release |
| [website/README.md](website/README.md) | Website development and deployment |
| [RELEASE_SUMMARY_v1.0.md](RELEASE_SUMMARY_v1.0.md) | **v1.0 submission** overview and deliverables |
| [FINAL_SUBMISSION/FINAL_SUBMISSION_README.md](FINAL_SUBMISSION/FINAL_SUBMISSION_README.md) | PDF/DOCX/PPTX submission package |
| [docs/RESEARCH_DIRECTION.md](docs/RESEARCH_DIRECTION.md) | Reference vs active research; Europe vs California |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Archived v1.0 milestones · v2.0 platform complete · v2.1/v3.0 future work |
| [docs/SED_SWITZERLAND_DATASET_REPORT.md](docs/SED_SWITZERLAND_DATASET_REPORT.md) | Swiss SED methods-transfer acquisition (v3.0 start) |
| [docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md](docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md) | Frozen Set C STA/LTA validation (STEP 2K) |

**AI assistants:** read [docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md) and [docs/AI_AGENT.md](docs/AI_AGENT.md).

## Primary research goal

1. **Europe** — primary long-term research focus (proposal, theory, datasets).
2. **United States / California** — **completed pilot** for method development (ObsPy, IRIS/EarthScope).

**EarthESND** is a **literature and architecture reference only** (optional Version 3.0 track — see [docs/PAPER_REPRODUCTION.md](docs/PAPER_REPRODUCTION.md)); **not included as executable code in v1.0.0**. K-NET scientific paper reproduction: **not started**.

## v1.0 submission status (complete)

| Component | Status |
|-----------|--------|
| EarthESND literature / optional track | ✅ **Documented** ([PAPER_REPRODUCTION.md](docs/PAPER_REPRODUCTION.md); not in v1.0.0 code tree) |
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

**Version 2.0 platform (complete — 2 August 2026):** Interactive research website in [`website/`](website/) — dashboard, workflow, results, dataset, waveforms, map, documentation portal, global search. Platform version **2.0.0** · Science baseline **v1.0.0** (frozen). See [docs/V2_RELEASE_NOTES.md](docs/V2_RELEASE_NOTES.md).

**Version 2.1 / 3.0:** platform maintenance; Swiss SED acquisition **complete** (waveforms only); Europe analysis, ML, streaming, operational deployment remain future work — [docs/ROADMAP.md](docs/ROADMAP.md). The **v1.0 California analysis chain is frozen** at 2026-07-29 artefacts.

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
├── configs/                # Acquisition and project YAML
├── data/manifests/         # California + Swiss event CSVs (tracked)
├── data/raw/iris/          # California MiniSEED (local; gitignored — see D-S2)
├── data/raw/switzerland/   # Swiss SED MiniSEED (local; gitignored)
├── data/metadata/switzerland/  # Swiss StationXML (XML gitignored)
├── docs/                   # Charter, phase reports, submission statements
├── reports/                # Final report, figures, tables, presentation assets
├── scripts/download/       # California (frozen) + Swiss SED download
├── scripts/analysis/       # EDA → features (executed; frozen)
├── src/                    # Acquisition framework (+ reserved package stubs)
├── tests/
└── website/                # Version 2.0 interactive platform (Next.js)
```

## Technology stack

Python 3.11+, ObsPy, NumPy, Pandas, Matplotlib, SciPy, PyYAML, Git.

## Verification

- Acquisition framework + Swiss helpers: `python -m pytest` (existing California tests unchanged; Swiss tests in `tests/test_switzerland_pilot.py`).
- California pilot: **8×18** feature matrix, **24** figures — see [FINAL_SUBMISSION/VALIDATION_SUMMARY.md](FINAL_SUBMISSION/VALIDATION_SUMMARY.md).
- Swiss SED methods-transfer: **20** events, **120** CH HH 3C records — [docs/SED_SWITZERLAND_DATASET_REPORT.md](docs/SED_SWITZERLAND_DATASET_REPORT.md).

## License, citation, and community

| Resource | Link |
|----------|------|
| **License** | [LICENSE](LICENSE) (MIT) |
| **Citation** | [CITATION.cff](CITATION.cff) |
| **Code of conduct** | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| **Contributing** | [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) |
| **Security** | [docs/SECURITY.md](docs/SECURITY.md) |

## Version

**Science:** v1.0.0 — Submission Release (documentation **1.4.0**)  
**Platform:** v2.0.0 — Interactive website ([website/](website/))

See [docs/CHANGELOG.md](docs/CHANGELOG.md) · [website/CHANGELOG.md](website/CHANGELOG.md)
