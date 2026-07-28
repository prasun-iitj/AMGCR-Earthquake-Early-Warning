# DIRECTORY_STRUCTURE.md

# AMGCR Earthquake Research - Directory Structure

## Purpose

This document explains the purpose of every directory and major file in the repository.

---

## Root Structure

```text
AMGCR_Earthquake_Research/
├── data/
├── docs/
├── literature/
├── notebooks/
├── outputs/
├── src/
├── tests/
├── README.md
├── PROJECT_GUIDE.md
├── requirements.txt
└── .gitignore
```

---

## data/

Stores all project datasets.

Subfolders:
- events/       : Earthquake catalogues
- waveforms/    : MiniSEED waveform files
- stations/     : Station metadata
- processed/    : Cleaned and processed datasets

---

## docs/

Contains all project documentation.

Examples:
- PROJECT_GUIDE.md
- ROADMAP.md
- PROJECT_STATUS.md
- AI_AGENT.md

---

## literature/

Research papers, notes and references used during the project.

---

## notebooks/

Jupyter notebooks for experiments, exploration and visualisation.

---

## outputs/

Stores generated outputs.

Subfolders:
- figures/
- reports/
- logs/

---

## src/

Main source code.

Typical modules:
- download_events.py
- download_waveforms.py
- preprocess.py
- plotting.py
- feature_extraction.py
- utils.py

---

## tests/

Unit tests and validation scripts.

---

## Root Files

README.md
: Project overview.

PROJECT_GUIDE.md
: Master operating guide.

requirements.txt
: Python dependencies.

.gitignore
: Files ignored by Git.

---

## Naming Conventions

- Use lowercase file names.
- Prefer snake_case for Python modules.
- Keep one responsibility per module.
- Organise datasets by type.

---

## Version

v1.0.0
