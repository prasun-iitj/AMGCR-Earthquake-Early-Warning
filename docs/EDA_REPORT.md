# EDA_REPORT.md

**Phase A.1 — Exploratory Data Analysis**  
California IRIS / EarthScope pilot (raw MiniSEED)

| Field | Value |
|-------|--------|
| Report date (UTC) | 2026-07-29 |
| EDA script | `scripts/analysis/run_california_pilot_eda.py` |
| Event manifest | `data/manifests/iris_california_pilot_events.csv` |
| Waveform root | `data/raw/iris/` |
| Acquisition context | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |

Re-run EDA:

```powershell
python scripts/analysis/run_california_pilot_eda.py
```

---

## 1. Scope

This analysis uses **only** the California pilot data under `data/raw/iris/` and metadata from the pilot manifest. No filtering, instrument correction, or EarthESND preprocessing was applied. Summary statistics and figures for **events, magnitudes, and station usage** refer to the **current manifest** (8 events). **All** MiniSEED files on disk were inspected, including four files from earlier pilot runs that are no longer listed in the manifest (see §3).

---

## 2. Dataset summary

| Metric | Value |
|--------|--------|
| **Events (manifest)** | **8** |
| **MiniSEED files (manifest-linked)** | **8** |
| **MiniSEED files (total on disk)** | **12** |
| **Unique stations (manifest)** | **2** — `CI.ADO`, `CI.USC` |
| **Channels** | **BHZ** only (vertical broadband) |
| **Sampling rate** | **40 Hz** (all manifest traces) |
| **Record duration** | **300 s** each (12 000 samples); matches download window from origin |
| **Magnitude range** | **4.05 – 4.87** |
| **Mean magnitude** | **4.40** |
| **Median magnitude** | **4.39** |
| **Magnitude std. dev.** | **0.28** |
| **Origin time coverage** | **2024-05-01T20:49:00Z** → **2024-10-25T15:04:23Z** |

Magnitude types in the manifest: `mw`, `ml` (as reported by USGS).

Machine-readable summary: `reports/eda/dataset_summary.json`.

---

## 3. MiniSEED file inspection

Every `.mseed` file under `data/raw/iris/` was read with ObsPy. Per-file fields include network, station, channel, sampling rate, sample count, UTC start/end, and raw count statistics (min, max, mean, std).

| Output | Description |
|--------|-------------|
| `reports/eda/mseed_file_inspection.csv` | One row per file (12 rows) |
| `reports/eda/eda_run_metadata.json` | Run timestamp, summary snapshot, figure/table index |

**Manifest vs disk:** Four files have `in_manifest=False` (leftover from a previous download when the manifest listed different events). They are documented in the inspection CSV but **excluded** from event/station summary tables and from magnitude/time/station figures, which use the manifest only.

All inspected traces are **40 Hz**, **300 s**, **BHZ**, with trace start times aligned to within milliseconds of event origin (FDSN window from origin).

---

## 4. Figures

Figures are 300 DPI PNGs under `reports/figures/`.

### 4.1 `example_waveform_raw.png`

**Purpose:** Show an **unprocessed** vertical-component record as stored in MiniSEED (instrument counts vs time).

**Selection:** Event with **largest magnitude** in the manifest — **M 4.87** (`mw`), 2024-07-29, station **CI.ADO.--.BHZ**, file  
`…/ci40675215…/CI.ADO.--.BHZ.20240729T200052.mseed`.

**How to read:** The x-axis is seconds from the trace start (FDSN download window, not re-zeroed at P arrival). Amplitude is in **digital counts**; no response removal or filtering. Large excursions indicate the earthquake signal plus background noise; this pilot uses a single component only.

### 4.2 `magnitude_histogram.png`

**Purpose:** Distribution of **catalog magnitudes** for the eight manifest events.

**How to read:** Each event contributes one bar; bins span the observed magnitude range. The pilot is intentionally narrow (M ≥ 4 in the download query), so the histogram reflects **small-sample** California activity in 2024, not regional completeness.

### 4.3 `events_over_time.png`

**Purpose:** **Temporal coverage** of the pilot catalog.

**How to read:** Each point is one event (UTC origin time vs magnitude), labelled with magnitude. Clusters appear in **May**, **July–August**, and **late October 2024**; gaps reflect the script’s selection of the first eight catalog entries that returned waveforms, not uniform sampling in time.

### 4.4 `station_usage_frequency.png`

**Purpose:** **How often each station** supplied the single waveform chosen per event.

**How to read:** Horizontal bars show event counts: **CI.ADO** (6 events), **CI.USC** (2 events). This reflects the pilot’s distance-ranked candidate list, not network-wide station availability.

---

## 5. Tables

### 5.1 `reports/tables/event_summary.csv`

One row per **manifest** event.

| Column | Meaning |
|--------|---------|
| `event_id` | USGS QuakeML-style folder id |
| `origin_time_utc` | Hypocenter origin (UTC) |
| `latitude`, `longitude`, `depth_km` | Hypocenter from catalog |
| `magnitude`, `magnitude_type` | USGS magnitude and type |
| `station_id`, `channel` | Station that provided the waveform |
| `sampling_rate_hz`, `duration_s` | From MiniSEED |
| `waveform_file` | Path relative to `data/raw/iris/` |

Use this table for proposal **Dataset** sections (event list + recording metadata).

### 5.2 `reports/tables/station_summary.csv`

One row per **station** appearing in manifest waveforms.

| Column | Meaning |
|--------|---------|
| `station_id` | Network.station.location.channel |
| `event_count` | Number of manifest events at this station |
| `mean_sampling_rate_hz` | Mean over events (40 Hz here) |
| `mean_duration_s`, `min_duration_s`, `max_duration_s` | Length of downloaded windows |

---

## 6. Observations for Phase A.2+

- **Single component (BHZ)** — 3-component analysis would require additional downloads.
- **Fixed 300 s windows** — suitable for early visual QC; P/S picking and shorter EEW windows may be needed later.
- **Amplitude in counts** — Phase B should address filtering, detrending, and optionally instrument response before feature extraction.
- **Station bias** — Most events use **ADO**; USC appears for closer southern California events.

---

## 7. Output index

| Path | Type |
|------|------|
| `reports/eda/dataset_summary.json` | Summary statistics |
| `reports/eda/mseed_file_inspection.csv` | Per-file inspection |
| `reports/eda/eda_run_metadata.json` | Run metadata |
| `reports/figures/example_waveform_raw.png` | Figure |
| `reports/figures/magnitude_histogram.png` | Figure |
| `reports/figures/events_over_time.png` | Figure |
| `reports/figures/station_usage_frequency.png` | Figure |
| `reports/tables/event_summary.csv` | Table |
| `reports/tables/station_summary.csv` | Table |

---

Version: **1.0.0** (Phase A.1)
