# SECURITY.md

# AMGCR Earthquake Research - Security & Reproducibility Guidelines

## Purpose

This document describes the security, data integrity, and reproducibility
practices to be followed throughout the AMGCR Earthquake Research project.

---

# Security Guidelines

- Never commit API keys, passwords, or tokens.
- Store secrets in environment variables or a local `.env` file.
- Add sensitive files to `.gitignore`.
- Verify downloaded datasets originate from trusted sources.

---

# Data Integrity

- Preserve original downloads in `data/raw/`.
- Never overwrite raw data.
- Record preprocessing steps in `EXPERIMENT_LOG.md`.
- Track dataset versions in `DATASET.md`.

---

# Reproducibility

To reproduce an experiment:

1. Create a fresh virtual environment.
2. Install dependencies from `requirements.txt`.
3. Use the documented dataset version.
4. Follow the preprocessing pipeline.
5. Execute the analysis scripts in order.
6. Compare results with the documented experiment log.

---

# Backup Strategy

- Commit code regularly.
- Push changes to the remote repository.
- Keep backups of datasets and documentation.

---

# Reporting Issues

Document:
- Bug description
- Steps to reproduce
- Expected behaviour
- Actual behaviour
- Environment details (OS, Python, ObsPy versions)

---

Version: **1.0.0**
