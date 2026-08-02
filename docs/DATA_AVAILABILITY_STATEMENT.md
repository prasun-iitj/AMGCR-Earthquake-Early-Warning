# DATA_AVAILABILITY_STATEMENT.md

**Deliverable D-S2 — Data availability and ethics statement**  
**Project:** AMGCR Earthquake Research  
**Scope:** California FDSN pilot (USGS events + EarthScope waveforms)  
**Date:** 29 July 2026  

This statement describes **where data come from**, **what is stored in the repository**, **what is excluded from version control**, and **ethical considerations**. It is based on [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md), [DATASET.md](DATASET.md), [FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md), and [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md).

**Related:** [REPRODUCIBILITY_STATEMENT.md](REPRODUCIBILITY_STATEMENT.md)

---

## 1. Data used in the California pilot

| Role | Provider | Access | ObsPy client (as documented) |
|------|----------|--------|--------------------------------|
| **Earthquake catalog / hypocenters** | U.S. Geological Survey (USGS) FDSN Event service | Public web service | `Client("https://earthquake.usgs.gov")` |
| **Waveforms & station metadata** | EarthScope Consortium (successor to IRIS Data Management Center) | Public FDSN dataselect/station | `Client("EARTHSCOPE")` |

**Service URLs (repository documentation):**

- USGS FDSN Event: https://earthquake.usgs.gov  
- EarthScope data services: https://www.earthscope.org/  
- EarthScope FDSN base (ObsPy): https://service.earthscope.org  
- FDSN specification: https://www.fdsn.org/webservices/

**Pilot query summary** ([IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md)): California bounding box (32.5°–42.0° N, 124.5°–114.0° W), 2024-01-01 to 2024-12-31, magnitude **4.0–7.5**; **one BHZ** MiniSEED trace per retained event, **300 s** from origin, **40 Hz** sampling for manifest-linked files.

**Completed run (2026-07-29):** **8** events in `data/manifests/iris_california_pilot_events.csv`; magnitudes **4.05–4.87**; stations **CI.ADO** (6 events) and **CI.USC** (2 events).

**No credentials** were required for this public pilot ([IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) §4).

---

## 2. Data formats and locations

| Data type | Format | Location when present |
|-----------|--------|------------------------|
| Event manifest | CSV | `data/manifests/iris_california_pilot_events.csv` |
| Raw waveforms | MiniSEED (`.mseed`) | `data/raw/iris/<event_id>/` |
| Acquisition run summary | JSON | `logs/iris_california_pilot_summary.json` (after download) |
| Derived tables, metrics, NPZ, feature matrix | CSV, JSON, NPZ | `reports/tables/`, `reports/eda/`, `reports/signal_analysis/`, `reports/preprocessing/`, `reports/features/` |
| Figures | PNG (300 DPI) | `reports/figures/` |

**Rules:** Raw MiniSEED should remain **immutable**; new pulls or parameter changes should use new downloads or documented manifests ([DATASET.md](DATASET.md)).

---

## 3. Availability in the Git repository

### 3.1 Available without re-download (typical clone)

- **Event manifest** — `data/manifests/iris_california_pilot_events.csv` (authoritative list of the eight analysed events).  
- **Derived analysis products** under `reports/` (tables, JSON summaries, preprocessing stage NPZ, feature matrix) as committed in the project history.  
- **Documentation** of query parameters and methods — `docs/IRIS_DATASET_REPORT.md` and phase reports.  
- **Scripts** to re-fetch and recompute — `scripts/download/`, `scripts/analysis/`.

### 3.2 Not available in Git (intentionally excluded)

Per `.gitignore`:

| Excluded | Pattern / path |
|----------|----------------|
| Raw waveforms | `data/raw/` |
| Local logs | `logs/` |
| Generated figures | `figures/` (includes `reports/figures/`) |

[FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md): a fresh clone does **not** contain MiniSEED files, acquisition JSON in `logs/`, or the **24** pilot PNGs unless they are regenerated or supplied in a **separate submission archive**.

### 3.3 Regaining excluded data

| Need | Action |
|------|--------|
| Raw MiniSEED + updated manifest (if re-run) | `python scripts/download/download_iris_california_pilot.py --event-count 8 --min-events 5` |
| Acquisition log | Produced by the same download script → `logs/iris_california_pilot_summary.json` |
| Figures | Re-run analysis scripts in order ([REPRODUCIBILITY_STATEMENT.md](REPRODUCIBILITY_STATEMENT.md) §3–5) |

Users may also obtain equivalent event and waveform data directly from **USGS** and **EarthScope** FDSN services using the parameters in [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md).

---

## 4. European and other data (context only)

The **programme’s long-term focus** is European seismic networks ([PROJECT_CHARTER.md](PROJECT_CHARTER.md)). **No European waveform dataset is included** in this repository yet. Future work is expected to follow the same manifest-and-report pattern; **ORFEUS / EIDA** is cited as the intended archive class:

- ORFEUS Data Center / EIDA: https://www.orfeus-eu.org/

(European integration is **planned**, not part of the completed California pilot deliverable.)

**Other documented sources (not used for California pilot results):**

- Sample generic catalogue: `data/raw/catalogs/` (sample QuakeML).  
- EarthESND Japan (K-NET) — optional reproduction track only ([DATASET.md](DATASET.md), [PAPER_REPRODUCTION.md](PAPER_REPRODUCTION.md)).

---

## 5. Ethics and privacy

- **Human subjects:** The pilot uses **public seismological network data** only. No personal identifiers, survey responses, or human-subject research data are collected or processed.  
- **Sensitive locations:** Event locations and station codes are **public catalog metadata** from USGS and EarthScope.  
- **Licensing and attribution:** Data providers require **appropriate citation and use of FDSN services**; this project documents providers in reports and references (below). Users reusing data must comply with **USGS**, **EarthScope**, and **FDSN** terms applicable at the time of access.  
- **GDPR:** The completed pilot does not process EU personal data; future European integrations may require network-specific policies ([RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md) §9.3).

---

## 6. Limitations relevant to data use

Documented in project reports (not new claims):

- **Single component (BHZ)**, **N = 8**, mixed magnitude types (`mw`, `ml`).  
- **Selection bias** toward station **CI.ADO** due to download policy ([IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md), [EDA_REPORT.md](EDA_REPORT.md)).  
- **Legacy MiniSEED** files may exist locally outside the current manifest (four files noted in EDA); **published analyses use eight manifest-linked files only**.  
- **Instrument response correction** was not applied in the completed preprocessing run (**0/8**); amplitudes in counts are **not** physical PGA/PGV without further processing ([PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md)).  
- California pilot data **do not** reproduce EarthESND paper geography or metrics ([IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) §5).

---

## 7. Citations and references (data and software)

### Data services and archives

U.S. Geological Survey. Earthquake Hazards Program — FDSN event web service. https://earthquake.usgs.gov  

EarthScope Consortium. Data services. https://www.earthscope.org/  

International Federation of Digital Seismograph Networks (FDSN). FDSN web services specification. https://www.fdsn.org/webservices/  

ORFEUS Data Center / EIDA. European integrated waveform archives. https://www.orfeus-eu.org/  

### Software

Krischer, L., Megies, T., Barsch, R., Beyreuther, M., Lecocq, T., Caudron, C., and Wassermann, J. (2015). ObsPy: A bridge for earthquake science. *Seismological Research Letters*, 86(3), 765–771.

### EEW context (literature cited in repository proposal)

Allen, R. M., and Kanamori, H. (2003). The potential for earthquake early warning in southern California. *Science*, 300(5620), 786–788.

Hoshiba, M., Iwakiri, K., Hayashimoto, N., Shimoyama, T., Hirano, K., Yamada, Y., Ishigaki, Y., and Kikuta, H. (2008). Outline of the 2007–2008 earthquake early warning experiments in Japan. *Earth Planets Space*, 60, 123–129.

Joshi, A., Singh, A. P., and Raman, B. (2026). EarthESND: Lightweight multiscale echo state network with dendritic neural network readout for earthquake early warning. *Computers and Electrical Engineering* (optional literature track for this programme; see `docs/PAPER_REPRODUCTION.md`).

### Project documentation index

`docs/PROJECT_CHARTER.md`; `docs/RESEARCH_DIRECTION.md`; `docs/IRIS_DATASET_REPORT.md`; `docs/EDA_REPORT.md`; `docs/SIGNAL_ANALYSIS_REPORT.md`; `docs/PREPROCESSING_REPORT.md`; `docs/FEATURE_ENGINEERING_REPORT.md`; `docs/RESULTS_AND_DISCUSSION.md`; `reports/Research_Proposal_v1.md` §12.

---

**Document control:** D-S2 data availability statement v1.0 — 29 July 2026. No source code modified to produce this file.
