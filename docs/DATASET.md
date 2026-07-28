# DATASET.md

# AMGCR Earthquake Research - Dataset Management

## Purpose

This document defines how earthquake datasets are acquired, organised, stored, documented, and versioned throughout the project.

---

# Data Sources

Primary sources used or planned for this project:

- EarthScope / IRIS FDSN
- USGS event service via ObsPy
- ISC and other FDSN-compatible services (when required)

---

# Dataset Categories

The project stores data in the following structure:

```text
data/
├── raw/
│   └── catalogs/
├── waveforms/
├── stations/
└── processed/
```

### raw/catalogs/
Raw earthquake catalogue downloads in QuakeML or CSV format.

### waveforms/
Raw MiniSEED waveform files downloaded from FDSN services.

### stations/
Station metadata (StationXML).

### processed/
Preprocessed datasets ready for analysis and modelling.

---

# Current Dataset Status

A sample catalogue retrieval has been completed and stored at data/raw/catalogs/catalog.xml. The retrieval used an ObsPy/FDSN client for a short time window and saved the result as QuakeML.

---

# Naming Convention

Use descriptive, consistent filenames.

Examples:

- catalog_2024_01_01.xml
- event_catalog_2024.csv
- waveform_<eventid>.mseed
- station_<network>_<station>.xml

---

# Dataset Rules

- Never modify raw data.
- Store processed data separately.
- Keep original downloads unchanged.
- Record the source of every dataset.
- Maintain reproducibility.

---

# Metadata

For each dataset, document:

- Source
- Download date
- Time range
- Magnitude filter
- Geographic region
- Processing steps

---

# Versioning

Do not overwrite datasets.

Instead, create new processed versions and document the changes.

---

# Future Expansion

This document will be updated as additional datasets and preprocessing pipelines are introduced.

---

Version: **0.3.0**
