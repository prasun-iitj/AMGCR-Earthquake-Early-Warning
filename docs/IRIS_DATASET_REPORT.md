# IRIS_DATASET_REPORT.md

USA (California) pilot dataset acquired through ObsPy FDSN clients for scientific reproduction and regional experimentation. **This workflow is separate from the EarthESND Japan/K-NET pipeline** — no EarthESND modules or configs were changed.

| Field | Value |
|-------|--------|
| Report date (UTC) | 2026-07-29 |
| Acquisition script | `scripts/download/download_iris_california_pilot.py` |
| Run log (JSON) | `logs/iris_california_pilot_summary.json` |
| Event manifest (CSV) | `data/manifests/iris_california_pilot_events.csv` |
| Raw waveforms | `data/raw/iris/<event_id>/*.mseed` |

---

## 1. FDSN services used

| Role | Provider | ObsPy client | Base URL |
|------|----------|--------------|----------|
| **Event catalog** | USGS FDSN Event | `Client("https://earthquake.usgs.gov")` | https://earthquake.usgs.gov |
| **Waveforms & metadata** | EarthScope (formerly IRIS DMC) | `Client("EARTHSCOPE")` | https://service.earthscope.org |

EarthScope’s dataselect/station services expose **no event endpoint** (ObsPy lists only `dataselect` and `station`). Event search therefore uses **USGS**, which is standard for FDSN event queries in ObsPy. Waveforms are retrieved from **EarthScope**, the successor to the IRIS Data Management Center.

---

## 2. Query parameters

### 2.1 Event search (USGS)

| Parameter | Value |
|-----------|--------|
| `starttime` | `2024-01-01T00:00:00` |
| `endtime` | `2024-12-31T23:59:59` |
| `minlatitude` | 32.5 |
| `maxlatitude` | 42.0 |
| `minlongitude` | -124.5 |
| `maxlongitude` | -114.0 |
| `minmagnitude` | 4.0 |
| `maxmagnitude` | 7.5 |
| `orderby` | `time` (newest first in catalog iteration) |

Geographic box: approximate **California** bounding rectangle (WGS84).

Catalog matches in window: **41** events (before waveform filtering).

### 2.2 Waveform download (EarthScope)

| Parameter | Value |
|-----------|--------|
| Target networks (candidates) | `CI`, `NC`, `BK` |
| Channel | `BHZ` (primary; script may try `HHZ`/`EHZ` in candidate list) |
| Window length | **300 s** from origin time |
| Format | MiniSEED (`.mseed`) |
| Stations per event | **1** successful trace (first successful candidate) |
| Station selection | Distance-ranked list of predefined California broadband sites (no live FDSN station query in the pilot path) |

Pilot script scans the event catalog until **8** events have at least one non-empty waveform file (minimum **5** required).

---

## 3. Pilot results (2026-07-29 run)

| Metric | Value |
|--------|--------|
| **Events with waveforms** | **8** |
| **Catalog matches (query)** | 41 |
| **Magnitude range (selected events)** | **4.05 – 4.87** |
| **Origin time range (selected events)** | **2024-05-01T20:49:00Z – 2024-10-25T15:04:23Z** |

### 3.1 Stations providing data (this run)

| Station | Network | Events served |
|---------|---------|----------------|
| CI.ADO | California Integrated Seismic Network | 6 |
| CI.USC | California Integrated Seismic Network | 2 |

**Unique stations in manifest:** 2 (`CI.ADO`, `CI.USC`).

Candidate pool in script (for future runs / other events):  
`CI.PAS`, `CI.USC`, `CI.WNG`, `CI.SYP`, `CI.VLY`, `CI.CPO`, `CI.RVR`, `CI.LUC2`, `CI.SMP`, `CI.ADO`, `NC.CMB`, `NC.BKS`, `NC.SAO`, `BK.CMB`, `BK.KCC`, `BK.JRC2`.

### 3.2 Storage layout

```text
data/raw/iris/
└── quakeml_earthquake.usgs.gov_fdsnws_event_1_query_eventid_<id>_format_quakeml/
    └── <NET>.<STA>.--.BHZ.<ORIGIN_TIME>.mseed

data/manifests/
└── iris_california_pilot_events.csv
```

CSV columns: `event_id`, `origin_time_utc`, `latitude`, `longitude`, `depth_km`, `magnitude`, `magnitude_type`, `waveform_file_count`, `waveform_files`, `fdsn_event_provider`, `fdsn_waveform_provider`.

---

## 4. How to reproduce

```powershell
cd C:\Users\prasun.tripathi\Desktop\MY\AMGCR_Earthquake_Research
python scripts/download/download_iris_california_pilot.py --event-count 8 --min-events 5
```

Optional: `--raw-dir`, `--manifest-dir`, `--log-path`.

**No credentials** are required for this public FDSN pilot.

---

## 5. Scope and limitations

- **Acquisition** — raw MiniSEED only; no EarthESND tensor construction at download time.
- **Downstream analysis** — Phase A.1/A.2 in `scripts/analysis/` ([EDA_REPORT.md](EDA_REPORT.md), [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md)); exploratory STA/LTA, not paper-comparable metrics.
- **Not comparable to EarthESND paper metrics** — different region, magnitude band, and channel count vs. K-NET 3-component study data.
- **Station picking** — pilot uses a fixed candidate list ranked by epicentral distance; full FDSN `get_stations` radius search was avoided for reliability and runtime.
- **Skipped catalog entries** — many events in the 41-event catalog did not yield data from the candidate list (see `errors` in `logs/iris_california_pilot_summary.json`).

---

## 6. Version

| Version | Date | Notes |
|---------|------|--------|
| 1.0.0 | 2026-07-29 | Initial California IRIS/EarthScope pilot (8 events, 8 MiniSEED files) |
| 1.1.0 | 2026-07-29 | Cross-linked Phase A.1/A.2 analysis reports |
