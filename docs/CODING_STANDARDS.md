# CODING_STANDARDS.md

# AMGCR Earthquake Research - Coding Standards

## Purpose

This document defines the coding conventions to be followed throughout the
AMGCR Earthquake Research project to ensure readability, consistency, and
maintainability.

---

## General Principles

- Write clear, readable code.
- Prefer simplicity over cleverness.
- Keep functions small and focused.
- Document non-obvious logic.

---

## Python Style

- Follow PEP 8.
- Use meaningful variable and function names.
- Add type hints where practical.
- Keep line length reasonable.

Example:

```python
def download_events(start_time, end_time):
    """Download earthquake events for the specified time range."""
    pass
```

---

## Project Structure

- Place reusable code inside the `src/` directory.
- Keep notebooks for experimentation only.
- Store raw data in `data/raw/`.
- Store processed data in `data/processed/`.

---

## Documentation

- Every module should include a module docstring.
- Public functions should include docstrings.
- Update documentation whenever behaviour changes.

---

## Version Control

- Make small, descriptive commits.
- Use feature branches for major work.
- Review changes before merging.

---

## Testing

- Test new functionality before committing.
- Record experiment results in `EXPERIMENT_LOG.md`.

---

Version: **1.0.0**
