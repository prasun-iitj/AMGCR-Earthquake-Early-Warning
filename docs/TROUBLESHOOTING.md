# TROUBLESHOOTING.md

# AMGCR Earthquake Research - Troubleshooting Guide

## Purpose

This document records common issues, their probable causes, and recommended
solutions encountered during the development of the AMGCR Earthquake Research
project.

---

# Python Issues

## Python Not Found

### Symptoms
- `'python' is not recognized`
- Incorrect Python version displayed

### Solution
- Verify Python installation.
- Ensure Python is added to the system PATH.
- Confirm with:

```bash
python --version
```

---

# Virtual Environment Issues

## Virtual Environment Not Activated

### Symptoms
Packages cannot be imported.

### Solution

Windows PowerShell:

```powershell
.venv\Scripts\Activate
```

Verify that the prompt begins with:

```text
(.venv)
```

---

# Package Installation Issues

## ModuleNotFoundError

### Cause

Required package has not been installed inside the active virtual environment.

### Solution

```bash
pip install -r requirements.txt
```

---

# ObsPy Issues

## Import Error

```python
import obspy
```

fails.

### Solution

- Verify the virtual environment is active.
- Reinstall ObsPy if required.
- Confirm installation using:

```bash
python -c "import obspy; print(obspy.__version__)"
```

---

# Network Issues

## Unable to Connect to FDSN Service

Possible causes:

- No internet connection
- Temporary server outage
- Firewall or proxy restrictions

Recommended action:

- Test internet connectivity.
- Retry after a few minutes.
- Try another FDSN provider if necessary.

---

# Git Issues

## Repository Not Initialised

Run:

```bash
git init
```

Verify:

```bash
git status
```

---

# General Best Practices

- Activate the virtual environment before working.
- Keep `requirements.txt` updated.
- Commit changes frequently using Git.
- Record significant issues and their resolutions.

---

Version: **1.0.0**
