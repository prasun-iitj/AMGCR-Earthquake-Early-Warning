# DATASET.md

How earthquake datasets are acquired, organised, stored, and documented.

**Authoritative scope:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md)

---

## Data sources

| Source | Role |
|--------|------|
| **USGS** FDSN Event | Event catalog (California pilot) |
| **EarthScope** (formerly IRIS DMC) | Waveforms (MiniSEED) |
| Other FDSN services | Future (Europe, optional Japan reproduction) |

---

## Directory layout

```text
data/
├── raw/
│   ├── catalogs/          # Sample QuakeML (generic FDSN test)
│   └── iris/              # California pilot MiniSEED (by event id)
├── manifests/
│   └── iris_california_pilot_events.csv
└── processed/             # Reserved (v1.0 features in reports/features/)
```

Analysis outputs (not raw data) live under **`reports/`** — see [EDA_REPORT.md](EDA_REPORT.md) and [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md).

---

## Active dataset — California pilot

| Field | Value |
|-------|--------|
| Region | California (bounding box in download script) |
| Events in manifest | **8** |
| Format | MiniSEED, **BHZ**, **40 Hz**, **300 s** from origin |
| Stations (pilot) | **CI.ADO**, **CI.USC** |
| Acquisition doc | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |
| Download script | `scripts/download/download_iris_california_pilot.py` |

**Rules:** Do not edit raw MiniSEED; re-download or version new pulls if parameters change.

---

## Other datasets

| Dataset | Status | Doc |
|---------|--------|-----|
| Sample FDSN catalogue | Sample | `data/raw/catalogs/catalog.xml` |
| EarthESND Japan (K-NET) | Planned (optional, Version 2.0) | [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md) |
| Europe | Planned (Version 2.0) | [ROADMAP.md](ROADMAP.md) |

---

## Metadata checklist

For each acquisition, document: source, query parameters, download date, manifest path, and a report in `docs/`.

---

Version: **1.3.0** (v1.0.0 submission release)
