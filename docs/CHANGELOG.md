# CHANGELOG.md

# AMGCR Earthquake Research - Changelog

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog** and follows semantic versioning where practical.

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

Current Version: **0.3.0**
