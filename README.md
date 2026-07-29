# AMGCR Earthquake Research

Reproducible **AI-assisted Earthquake Early Warning (EEW)** research for **Western seismic regions**, developed in the context of a **Swiss certificate programme**.

## Start here

| Document | Role |
|----------|------|
| **[docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md)** | **Authoritative** vision, scope, status, roadmap |
| [docs/RESEARCH_DIRECTION.md](docs/RESEARCH_DIRECTION.md) | Reference vs active research; Europe vs California |
| [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | Milestones and future work |
| [reports/Research_Proposal_v1.md](reports/Research_Proposal_v1.md) | **Deliverable 1** — Research Proposal & Technical Report |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Completed phases and planned extensions |

**AI assistants:** read [docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md) and [docs/AI_AGENT.md](docs/AI_AGENT.md).

## Primary research goal

1. **Europe** — primary long-term research focus (proposal, theory, datasets).
2. **United States / California** — **completed pilot** for method development (ObsPy, IRIS/EarthScope).

**EarthESND** is a **reference implementation only** (literature, architecture, AI methodology)—**not** the programme objective. Reference software: **complete**; K-NET scientific paper reproduction: **not started**.

## Repository status (synchronized)

| Component | Status |
|-----------|--------|
| EarthESND reference implementation | ✅ **Complete** |
| USA / California IRIS–EarthScope pilot | ✅ **Complete** |
| EDA | ✅ **Complete** |
| Signal analysis | ✅ **Complete** |
| Preprocessing | ✅ **Complete** |
| Feature engineering | ✅ **Complete** |
| Results & discussion | ✅ **Complete** |
| **Research Proposal & Technical Report (Deliverable 1)** | ✅ **Complete** |

**Current programme focus:** documented pilot outcomes and **future work** — European dataset integration, AI modelling, real-time EEW, comparative evaluation (including EarthESND-**inspired** baselines).

## Key reports

| Report | Path |
|--------|------|
| Acquisition | [docs/IRIS_DATASET_REPORT.md](docs/IRIS_DATASET_REPORT.md) |
| EDA | [docs/EDA_REPORT.md](docs/EDA_REPORT.md) |
| Signal analysis | [docs/SIGNAL_ANALYSIS_REPORT.md](docs/SIGNAL_ANALYSIS_REPORT.md) |
| Preprocessing | [docs/PREPROCESSING_REPORT.md](docs/PREPROCESSING_REPORT.md) |
| Features | [docs/FEATURE_ENGINEERING_REPORT.md](docs/FEATURE_ENGINEERING_REPORT.md) |
| Interpretation | [docs/RESULTS_AND_DISCUSSION.md](docs/RESULTS_AND_DISCUSSION.md) |
| Proposal (v1) | [reports/Research_Proposal_v1.md](reports/Research_Proposal_v1.md) |

Analysis artefacts: `reports/eda/`, `reports/signal_analysis/`, `reports/preprocessing/`, `reports/features/`, `reports/figures/`, `reports/tables/`.

## Repository structure

```text
AMGCR_Earthquake_Research/
├── configs/              # EarthESND reference + acquisition YAML
├── data/raw/iris/        # California pilot MiniSEED
├── data/manifests/       # Event CSV
├── docs/                 # Charter, phase reports, interpretation
├── reports/              # Figures, tables, Research_Proposal_v1.md
├── scripts/download/     # FDSN pilot download
├── scripts/analysis/     # EDA → features (executed; outputs in reports/)
├── src/                  # acquisition + EarthESND reference
└── tests/
```

## Technology stack

Python 3.11+, ObsPy, NumPy, Pandas, Matplotlib, SciPy, PyYAML, Git.

## Verification

- EarthESND reference: **88 passing tests** when the full reference tree imports (`python -m pytest`).
- California pilot and analysis: see reports and docs listed above.

## Version

**1.2.0** — Final documentation sync (pilot pipeline + Deliverable 1 complete). See [docs/CHANGELOG.md](docs/CHANGELOG.md).
