# CHANGELOG.md

# AMGCR Earthquake Research - Changelog

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog** and follows semantic versioning where practical.

---

## [Unreleased] - Swiss independent frozen STA/LTA validation (2026-09-11)

### Added

- STEP 2K: evaluated the pre-declared STA/LTA configuration (causal 0.1–15 Hz HHZ, 0.5/10 s, trigger_on **8.0**) on locked Set C.
  - 15/15 events, 550/550 usable records; 401 detections, 149 NO DETECTION
  - `scripts/analysis/run_swiss_independent_validation.py`
  - `src/analysis/switzerland_validation.py`
  - `configs/sed_switzerland_validation.yaml`
  - `docs/SWISS_INDEPENDENT_VALIDATION_RESULTS.md`
  - `reports/switzerland_validation/`
  - `tests/test_switzerland_validation.py`

### Notes

- Threshold 8.0 was not retuned and is not claimed to be optimal.
- SED/manual first-P picks are independent references, not ground truth.
- California v1.0.0, Set A, and Set C membership were not modified.
- No ML training and no operational EEW claim.

---

## [Unreleased] - Swiss independent validation acquisition (2026-09-11)

### Added

- STEP 2J: acquired locked Set C MiniSEED and StationXML using origin − 60 s → origin + 90 s.
  - 15/15 events, 550 CH HHZ records, 550 StationXML responses verified per station/channel/interval
  - `scripts/download/download_sed_switzerland_validation.py`
  - `docs/SWISS_VALIDATION_ACQUISITION_REPORT.md`
  - `data/manifests/sed_switzerland_validation_waveforms.csv`
  - `data/manifests/sed_switzerland_validation_picks.csv`

### Notes

- No STA/LTA, no validation metrics, no retuning of threshold 8.0, no Set C reselection.
- California v1.0.0 and the 20-event Swiss development set were not modified.

---

## [Unreleased] - Swiss independent validation design correction (2026-09-11)

### Changed

- STEP 2I.1: distinguished **acquisition** (origin−60 s → origin+90 s), **detection** (origin → origin+90 s), and **pre-event noise/QC** (origin−60 s → origin−10 s) windows.
- Renamed the locked 15-event subset to **Independent Swiss/Adjacent-Border Validation Set** (9/15 immediate-border). Set C IDs were not replaced.
- HH 3C availability is now a **unique CH station-code** count covering the acquisition window.
- StationXML status set to **not yet verified per station** (BALST spot-check is not full coverage).
- Same-station SED first-P ∩ HHZ availability recorded; event-level picks are not treated as a station reference.

### Notes

- No validation MiniSEED download, no STA/LTA on Set C, no metric computation, no retuning of threshold 8.0.
- California v1.0.0 and the 20-event Swiss development set were not modified.

---

## [Unreleased] - Swiss independent validation design (2026-09-11)

### Added

- Independent Swiss validation-set **design/audit** (no MiniSEED download, no STA/LTA on the new events, no retuning of threshold 8.0):
  - `docs/SWISS_INDEPENDENT_VALIDATION_PLAN.md`
  - `data/manifests/sed_switzerland_validation_candidates.csv` (227 independent earthquakes; 15 proposed)
  - `configs/sed_switzerland_validation_audit.yaml`
  - `src/acquisition/switzerland_validation_audit.py`
  - `scripts/audit/audit_swiss_validation_candidates.py`
  - `tests/test_switzerland_validation_audit.py`
  - `reports/switzerland_validation_audit/audit_summary.json`

### Notes

- The 20-event Swiss development set and the frozen California v1.0.0 pipeline were **not** modified.
- Threshold 8.0 remains the pre-declared/proposed value from the development set, reserved for independent validation. It is not claimed to be optimal or already validated.

---

## [Unreleased] - Swiss SED methods-transfer acquisition (2026-09-06)

### Added

- Swiss seismic-data acquisition pipeline (separate from frozen California v1.0.0):
  - `configs/sed_switzerland_pilot.yaml`
  - `src/acquisition/switzerland_pilot.py`
  - `scripts/download/download_sed_switzerland_pilot.py`
  - `data/manifests/sed_switzerland_pilot_events.csv` (20 events, 120 event–station rows)
  - `docs/SED_SWITZERLAND_DATASET_REPORT.md`
  - `tests/test_switzerland_pilot.py`
  - `reports/switzerland_pilot/` acquisition and response-test JSON
- Raw MiniSEED under `data/raw/switzerland/`; StationXML under `data/metadata/switzerland/` (local / gitignored XML).

### Notes

- California IRIS pilot, analysis scripts, reports, figures, and `FINAL_SUBMISSION/` were **not** modified.
- No Swiss STA/LTA, feature engineering, or ML. Not an operational EEW system.

---

## [1.4.0] - Pre-release audit (2026-08-02)

### Added

- **`CITATION.cff`** — repository citation metadata (software v1.0.0).
- **`CODE_OF_CONDUCT.md`** — Contributor Covenant v2.1.

### Fixed

- **LICENSE** — MIT license added (was empty).
- **requirements.txt** — added `PyYAML` and `pytest` for reproducible installs.
- **pyproject.toml** — version aligned to **1.0.0**.
- Removed dev scratch file `tmp_probe.py`; ignore `tmp_*.py`.

### Documentation

- Aligned EarthESND status across README, charter, status, PAPER_REPRODUCTION, REPRODUCIBILITY, and final report: **literature/optional v3.0 track**; **not in v1.0.0 code tree**; **9 acquisition tests**.
- Fixed broken links in `RELEASE_SUMMARY_v1.0.md`.
- Updated `FINAL_DELIVERABLE_AUDIT.md` post-submission sign-off.

---

## [2.0.0] - Version 2.0 interactive platform (documentation sync)

### Added

- **`website/`** — public interactive research platform (Next.js 16, TypeScript, Tailwind v4) at platform version **2.0.0**.
- Nineteen routes: dashboard, workflow, results, dataset, waveforms, map, docs portal, global search, about, contact, and more.
- Release documentation: `docs/V2_RELEASE_NOTES.md`, `V2_DEPLOYMENT_GUIDE.md`, `V2_TEST_REPORT.md`, `V2_KNOWN_LIMITATIONS.md`, `V2_PUBLIC_LAUNCH_CHECKLIST.md`.
- `website/CHANGELOG.md` — platform changelog.

### Documentation

- Synchronized README, AGENTS, PROJECT_STATUS, ROADMAP, PROJECT_CHARTER, PROJECT_GUIDE, AI_AGENT for **v2.0 platform complete**.
- Future work reframed as **Version 2.1** (platform) and **Version 3.0** (science/infrastructure).
- **No changes** to v1.0 analysis scripts, scientific results, or FINAL_SUBMISSION.

### Notes

- Science release remains **`v1.0.0`** (29 July 2026).
- Suggested platform tag: **`v2.0.0-website-release`** or team convention.

---

## [1.3.0] - v1.0.0 Submission Release

### Added

- **FINAL_SUBMISSION/** — PDF/DOCX/PPTX bundle (D-F4), checklists, validation summary (**PASS**).
- **reports/Research_Report_Final.md** (D-F1), presentation outline/script (D-F2/D-F3).
- **docs/REPRODUCIBILITY_STATEMENT.md**, **docs/DATA_AVAILABILITY_STATEMENT.md** (D-S1/S2).
- **RELEASE_SUMMARY_v1.0.md** — submission overview and Version 2.0 roadmap pointer.
- **docs/FINAL_DELIVERABLE_AUDIT.md** — artefact audit (completed).

### Documentation

- Synchronized README, PROJECT_CHARTER, PROJECT_STATUS, ROADMAP, IMPLEMENTATION_PLAN, AI_AGENT, ARCHITECTURE, PROJECT_GUIDE, AGENTS, RESEARCH_DIRECTION, DATASET, FINAL_DELIVERABLE_PLAN, CHANGELOG.
- **Current stage:** v1.0 submission **complete**; **Version 2.0** future work (website, dashboard, Europe, ML, streaming, deployment).
- Documentation-only release relative to v1.0 science freeze; **no changes** to analysis source code or scientific results.

### Notes

- Suggested Git tag: **`v1.0.0`**.

---

## [1.2.0] - Final documentation synchronization

### Documentation

- Synchronized README, PROJECT_STATUS, ROADMAP, PROJECT_CHARTER, RESEARCH_DIRECTION, AI_AGENT, PROJECT_GUIDE, and ARCHITECTURE to **current repository status**.
- Canonical completion: EarthESND reference, California IRIS pilot, EDA, signal analysis, preprocessing, feature engineering, results & discussion, **Research Proposal & Technical Report** (Deliverable 1).
- **Current stage (historical):** Research Proposal v1 complete at 1.2.0; superseded by **v1.0.0 Submission Release** in 1.3.0.

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
- Clarified EarthESND **literature track documented** vs **executable pipeline not in v1.0.0**; USA IRIS/California pilot documented as active workflow.

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

Current Version: **1.4.0** (science **v1.0.0** · platform **v2.0.0**)
