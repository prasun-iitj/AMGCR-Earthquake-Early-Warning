# DATASET.md

How earthquake datasets are acquired, organised, stored, and documented.

**Authoritative scope:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md)

---

## Data sources

| Source | Role |
|--------|------|
| **USGS** FDSN Event | Event catalog (California pilot) |
| **EarthScope** (formerly IRIS DMC) | Waveforms (MiniSEED) — California |
| **SED / ETH EIDA** FDSN | Event catalogue, CH waveforms, StationXML — Swiss methods-transfer pilot |
| Other FDSN services | Future (broader Europe, optional Japan reproduction) |

---

## Directory layout

```text
data/
├── raw/
│   ├── catalogs/          # Sample QuakeML (generic FDSN test)
│   ├── iris/              # California pilot MiniSEED (by event id)
│   ├── switzerland/       # Swiss SED methods-transfer MiniSEED (by event id)
│   └── switzerland_validation/  # Set C validation MiniSEED (by event id)
├── metadata/
│   ├── switzerland/                 # Set A StationXML (regenerable)
│   └── switzerland_validation/      # Set C StationXML (regenerable)
├── manifests/
│   ├── iris_california_pilot_events.csv
│   ├── sed_switzerland_pilot_events.csv
│   ├── sed_switzerland_validation_candidates.csv
│   ├── sed_switzerland_validation_waveforms.csv
│   └── sed_switzerland_validation_picks.csv
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

## Active dataset — Swiss SED methods-transfer (acquisition)

| Field | Value |
|-------|--------|
| Region | Switzerland and immediate border (SED ECOS-09 box) |
| Events in manifest | **20** |
| Event–station records | **120** |
| Format | MiniSEED, **HH 3C**, **120 or 200 Hz**, **origin − 90 s to origin + 210 s** |
| Network | **CH** |
| Acquisition doc | [SED_SWITZERLAND_DATASET_REPORT.md](SED_SWITZERLAND_DATASET_REPORT.md) |
| Download script | `scripts/download/download_sed_switzerland_pilot.py` |

No Swiss analysis, ML, or operational EEW claims. California v1.0.0 is separate and frozen.

---

## Other datasets

| Dataset | Status | Doc |
|---------|--------|-----|
| Sample FDSN catalogue | Sample | `data/raw/catalogs/catalog.xml` |
| Swiss SED methods-transfer pilot | **Acquisition complete** (20 events, 120 CH 3C records) | [SED_SWITZERLAND_DATASET_REPORT.md](SED_SWITZERLAND_DATASET_REPORT.md) |
| Swiss independent validation candidates | **Design complete** — Independent Swiss/Adjacent-Border Validation Set (15 locked events) | [SWISS_INDEPENDENT_VALIDATION_PLAN.md](SWISS_INDEPENDENT_VALIDATION_PLAN.md) |
| Swiss independent validation waveforms | **Acquisition complete** (STEP 2J) — 15 events, 550 CH HHZ records; MiniSEED gitignored | [SWISS_VALIDATION_ACQUISITION_REPORT.md](SWISS_VALIDATION_ACQUISITION_REPORT.md) |
| Swiss independent frozen STA/LTA validation | **Complete** (STEP 2K) — threshold 8.0 evaluated as pre-declared; 550/550 records | [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md) |
| Swiss ML feasibility | **NO-GO** (STEP 3A) — inspection only; no model trained | [SWISS_ML_FEASIBILITY_AUDIT.md](SWISS_ML_FEASIBILITY_AUDIT.md) |
| EarthESND Japan (K-NET) | Planned (optional, Version 3.0) | [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md) |
| Broader Europe (ORFEUS/EIDA) | Planned (Version 3.0) | [ROADMAP.md](ROADMAP.md) |

---

## Metadata checklist

For each acquisition, document: source, query parameters, download date, manifest path, and a report in `docs/`.

---

Version: **1.4.0** (v1.0.0 science frozen · v2.0.0 platform · Swiss SED acquisition 2026-09-06)
