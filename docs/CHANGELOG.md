# CHANGELOG.md

# AMGCR Earthquake Research - Changelog

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog** and follows semantic versioning where practical.

---

## [1.2.0] - Final documentation synchronization

### Documentation

- Synchronized README, PROJECT_STATUS, ROADMAP, PROJECT_CHARTER, RESEARCH_DIRECTION, AI_AGENT, PROJECT_GUIDE, and ARCHITECTURE to **current repository status**.
- Canonical completion: EarthESND reference, California IRIS pilot, EDA, signal analysis, preprocessing, feature engineering, results & discussion, **Research Proposal & Technical Report** (Deliverable 1).
- **Current active stage:** Research Proposal & Technical Report (complete). **Future work:** European dataset integration, AI modelling, real-time EEW, comparative evaluation.

### Notes

- Documentation-only release; no changes to source code, tests, scripts, or YAML.

---

## [1.1.0] - Phase A California pilot analysis

### Added

- **Phase A.1** — `scripts/analysis/run_california_pilot_eda.py`: MiniSEED inspection, dataset summary, EDA figures and tables under `reports/`.
- **Phase A.2** — `scripts/analysis/run_california_signal_analysis.py`: amplitude metrics, noise/SNR, ObsPy STA/LTA P picks, per-event signal figures.

### Documentation

- Added **docs/EDA_REPORT.md** and **docs/SIGNAL_ANALYSIS_REPORT.md**.
- Updated PROJECT_STATUS, ROADMAP, IMPLEMENTATION_PLAN, PROJECT_CHARTER, ARCHITECTURE, README, AI_AGENT, PROJECT_GUIDE, and DATASET for Phase A completion and Phase B / proposal next steps.

---

## [1.0.0] - Research charter and documentation refactor

### Documentation

- Established **docs/PROJECT_CHARTER.md** as the authoritative project definition (Swiss certificate EEW research; Europe focus, USA experimental data).
- Added **docs/RESEARCH_DIRECTION.md** explaining the pivot from EarthESND paper reproduction to Western-region active research.
- Synchronised README, PROJECT_STATUS, ROADMAP, ARCHITECTURE, PAPER_REPRODUCTION, IMPLEMENTATION_PLAN, AI_AGENT, and PROJECT_GUIDE with Phases A–D roadmap and professor requirements.
- Clarified EarthESND **reference implementation complete** vs **scientific paper reproduction not started**; USA IRIS/California pilot documented as active workflow.

### Notes

- No Python source, tests, or YAML configuration values were changed in this release.

---

## [0.3.0] - Phase 2B Catalogue Retrieval

### Added

- Implemented configuration-driven event catalogue retrieval with ObsPy.
- Added provider-aware query shaping so the retrieval workflow works with the USGS event service.
- Verified a sample catalogue retrieval and saved a QuakeML file to data/raw/catalogs/catalog.xml.
- Added regression tests for provider resolution and query construction.

### Documentation

- Updated the project status, implementation plan, dataset notes, experiment log, roadmap, and README to reflect the completed acquisition milestone.

---

## [0.2.0] - Phase 2A Acquisition Framework Preparation

### Added

- Created a modular acquisition package under src/acquisition.
- Added catalog, waveform, station, and download manager modules with documentation and placeholder logic.
- Implemented a YAML-based configuration loader for future acquisition workflows.
- Added default acquisition configuration in configs/acquisition_config.yaml.
- Added validators and custom exceptions for configuration-driven acquisition.
- Added unit tests covering configuration loading and validation.

### Documentation

- Updated project status and implementation notes for the acquisition preparation phase.

---

## [0.1.0] - Phase 1 Initialization

### Added

- Repository structure reorganised to support research and development work.
- Virtual environment created and validated.
- Core dependencies installed and verified for ObsPy, NumPy, Pandas, Matplotlib, SciPy, and PyYAML.
- Initial package scaffold created inside src/.
- Logging configuration and project settings added.
- Initial import verification test added.

### Documentation

- Updated project status and implementation notes.
- Added project decision log entries for the initialization phase.

---

## Changelog Guidelines

Record only meaningful project changes.

Include:

- New features
- Bug fixes
- Documentation updates
- Refactoring
- Research milestones

Avoid logging trivial edits such as spelling corrections unless they materially improve documentation.

---

Current Version: **1.2.0**
