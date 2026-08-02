# Reproducible AI-Assisted Earthquake Early Warning Research for Western Regions: A European-Oriented Programme with a California FDSN Pilot

**AMGCR Earthquake Research — Deliverable 1 (Research Proposal & Technical Report, v1.0)**  
**Date:** 29 July 2026  
**Programme context:** Swiss certificate research in Assessment and Management of Geological and Climate Related Risk (AMGCR)  
**Status:** This document **consolidates completed pilot science** (acquisition through interpretation) and **states proposed European and operational extensions**. It does not alter code or recompute analyses.

### Completion status (pilot programme)

| Component | Status |
|-----------|--------|
| EarthESND literature / optional track | **Documented** (benchmark only) |
| USA / California IRIS–EarthScope pilot | **Complete** |
| EDA · Signal analysis · Preprocessing · Feature engineering | **Complete** |
| Results & discussion | **Complete** |
| This Research Proposal & Technical Report | **Complete** (Deliverable 1) |

---

## Table of contents

1. [Title](#title)  
2. [Abstract](#abstract)  
3. [Introduction](#1-introduction)  
4. [Literature Review](#2-literature-review)  
5. [Research Gap](#3-research-gap)  
6. [Objectives](#4-objectives)  
7. [Dataset](#5-dataset)  
8. [Methodology](#6-methodology)  
9. [Experimental Workflow](#7-experimental-workflow)  
10. [Results & Discussion](#8-results--discussion)  
11. [Relevance to Europe](#9-relevance-to-europe)  
12. [Expected Outcomes](#10-expected-outcomes)  
13. [Future Work](#11-future-work)  
14. [References](#12-references)  

**Appendix A:** Index of generated figures and tables  

---

## Title

**Reproducible AI-Assisted Earthquake Early Warning Research for Western Seismic Regions: Method Development on a California FDSN Pilot with Transfer Path to European Networks**

---

## Abstract

Earthquake Early Warning (EEW) delivers rapid estimates of ground shaking ahead of destructive S-wave arrival, combining seismological data acquisition, onsite triggering, signal processing, and increasingly machine-learning-based magnitude and intensity prediction. European programmes require transparent, reproducible workflows that can be audited, extended across national networks, and aligned with open data policies, yet many published pipelines remain tied to region-specific archives or proprietary tooling.

This report presents the **AMGCR Earthquake Research** project: a **European-focused** certificate programme whose **primary long-term target** is EEW-oriented analysis on **European seismic networks**, while **California** serves as the **completed pilot implementation** for method validation. Using ObsPy and FDSN services (USGS event metadata; EarthScope waveforms), we acquired eight MiniSEED recordings (magnitude 4.05–4.87, 2024), executed exploratory data analysis, STA/LTA-based signal characterisation, documented preprocessing, and extraction of an **8×18** feature matrix. Results confirm a reproducible path from raw waveforms to machine-learning-ready descriptors, while exposing limitations—origin-aligned download windows, absent instrument response correction in the pilot run, small sample size, and station-selection bias—that must be addressed before operational European deployment.

The repository retains **EarthESND as a documented literature and architecture benchmark** (echo state network with dendritic readout) **only as a methodological reference**, not as the programme’s scientific endpoint. **Proposed future work** includes scaling datasets, integrating ORFEUS/EIDA-class European archives, response-corrected amplitudes, and comparative evaluation of modern onsite AI models including EarthESND-inspired designs on Western data.

**Keywords:** earthquake early warning; ObsPy; FDSN; reproducible research; feature engineering; Europe; California pilot; machine learning

---

## 1. Introduction

### 1.1 Motivation

Damaging earthquakes remain a major risk in Europe and adjacent regions, from the Mediterranean belt to the Alps and anthropogenic seismicity associated with industrial activity. EEW systems mitigate harm by issuing alerts seconds to tens of seconds before strong shaking arrives at a site, based on **P-wave detection**, **rapid magnitude estimation**, and **ground-motion prediction**. Public acceptance, regulatory frameworks, and civil-protection integration—in Switzerland and across the EU—increasingly expect **documented, open methodologies** rather than black-box prototypes.

### 1.2 Programme positioning

The present project was initiated within a **Swiss certificate programme** in geophysical risk assessment, aligned with **European expectations** for traceable analysis in natural-hazard research (open data, documented processing, explicit limitations). Initial effort targeted documentation of a recent **EarthESND** machine-learning architecture (Joshi, Singh, and Raman, 2026) as an optional literature track preserved for methodological comparison only. **Programme guidance** subsequently reframed the work toward a **logical European EEW research project** with real waveforms, theory, visualisation, tables, and this **Research Proposal & Technical Report**—using **United States (California) FDSN data** as a **completed pilot laboratory** where open APIs and pedagogical resources are mature (`docs/PROJECT_CHARTER.md`, `docs/RESEARCH_DIRECTION.md`).

### 1.3 Scope of this document

This deliverable synthesises **completed pilot work** (acquisition through feature engineering and scientific interpretation) and **proposed extensions** (European data, scale, AI evaluation, real-time paths). It does **not** introduce new computations; all quantitative results cite existing reports under `docs/` and artefacts under `reports/`.

---

## 2. Literature Review

### 2.1 Earthquake Early Warning fundamentals

Classical EEW relies on **onsite algorithms** that detect P-wave onset via short-term average / long-term average (STA/LTA) ratio tests or similar triggers, then estimate magnitude and alert levels from early windows of acceleration or velocity (Allen and Kanamori, 2003; Hoshiba et al., 2008). Key trade-offs include **detection latency**, **false alarm rate**, and **magnitude saturation** for large events. European deployments (e.g., national networks, cross-border cooperation) emphasise **standardised metadata**, **latency budgets**, and **uncertainty communication** to end users.

### 2.2 Open seismological software and data

**ObsPy** (Krischer et al., 2015) provides a de facto standard for reading MiniSEED, invoking FDSN web services, and applying detrending, filtering, and instrument correction. **FDSN** federates event and waveform services; in this project, **USGS** supplies earthquake catalogues and **EarthScope** (successor to IRIS DMC) supplies waveforms (`docs/IRIS_DATASET_REPORT.md`). The same abstraction layer is intended for **European** endpoints (ORFEUS, EIDA, national FDSN nodes).

### 2.3 Machine learning in onsite EEW

Deep learning and reservoir computing approaches learn magnitude or intensity from early waveform segments, often outperforming empirical scaling in controlled experiments but requiring **large, diverse training sets** and careful handling of **site effects** and **instrument response**. **EarthESND** (Joshi, Singh, and Raman, 2026) proposes a lightweight **multiscale echo state network (ESN)** with **dendritic neural network (DENN)** readout for onsite magnitude estimation, trained in a Japan K-NET context. In AMGCR, this design is implemented as a **reference pipeline** (`src/`, configuration contracts, automated tests) for **architecture comparison**, **not** as the primary geographic or deliverable focus of the certificate programme.

### 2.4 Reproducibility in computational seismology

Reproducible EEW research demands versioned **download parameters**, **manifests**, **processing configs**, and **analysis scripts**. This project institutionalises that pattern through CSV manifests, JSON summaries, and phase reports (EDA through feature engineering).

### 2.5 European and Swiss context

National and cross-border seismological infrastructures in Europe—including ORFEUS, the European Integrated Data Archive (EIDA), and member-state networks—provide the **intended long-term data plane** for this research. Switzerland participates in broader European seismological cooperation and civil-protection planning, where **evidence-based EEW methodology** must be explainable to regulators and the public. The California pilot therefore functions as a **methods prototype**: it satisfies certificate requirements for hands-on ObsPy practice and published artefacts while the **scientific narrative** remains **Europe-forward**.

## 3. Research Gap

Several gaps motivate the AMGCR workflow:

1. **European programme need vs. Japan-centric ML papers:** State-of-the-art ML EEW models are often demonstrated on Asian strong-motion archives; **transferable, documented workflows for European FDSN data** are less commonly packaged for certificate-level research.

2. **End-to-end openness:** Many studies publish metrics without full artifact trails from **raw MiniSEED** to **feature matrices** suitable for ML.

3. **Separation of benchmark code and active science:** Teams may conflate **implementing a paper’s codebase** with **completing region-relevant science**; this project explicitly **decouples** EarthESND software completion from Western pilot analysis.

4. **Pilot-scale validity:** Small-N pilots can illustrate methodology but **cannot** support operational claims; the gap between **proof-of-concept** and **validated European EEW input** remains open—this report states that gap explicitly.

---

## 4. Objectives

### 4.1 Primary objective (programme)

Develop a **reproducible, AI-ready EEW research workflow** aimed ultimately at **European seismic networks**, documented for a Swiss/European research audience.

### 4.2 Secondary objective (pilot — **completed**)

Implement and validate the workflow on a **California IRIS/EarthScope pilot**: acquisition, EDA, signal analysis, preprocessing, feature engineering, and interpretation.

### 4.3 Specific objectives

| ID | Objective | Status |
|----|-----------|--------|
| O1 | FDSN-based download of real earthquake waveforms with ObsPy | **Completed** |
| O2 | Exploratory dataset characterisation (events, stations, channels) | **Completed** |
| O3 | Onsite-style signal metrics and STA/LTA P-wave analysis | **Completed** |
| O4 | Documented preprocessing chain toward ML inputs | **Completed** (response step failed in run; documented) |
| O5 | Multi-domain feature matrix for EEW/ML experiments | **Completed** (8×18) |
| O6 | Scientific interpretation and European transfer narrative | **Completed** (`docs/RESULTS_AND_DISCUSSION.md`) |
| O10 | Research Proposal & Technical Report (Deliverable 1) | **Completed** (`reports/Research_Proposal_v1.md`) |
| O7 | European FDSN pilot and scaled catalogues | **Proposed** |
| O8 | AI model training on Western data (incl. EarthESND-inspired baselines) | **Proposed** |
| O9 | Real-time / latency-oriented prototype | **Proposed** |

---

## 5. Dataset

### 5.1 Pilot dataset (**completed**)

**Source documentation:** `docs/IRIS_DATASET_REPORT.md`, `docs/EDA_REPORT.md`

| Attribute | Value |
|-----------|--------|
| Region | California (approximate bounding box, 2024) |
| Event provider | USGS FDSN Event |
| Waveform provider | EarthScope (ObsPy client `EARTHSCOPE`) |
| Events in manifest | **8** |
| Magnitude range | **4.05 – 4.87** (`mw`, `ml`) |
| Origin times | 2024-05-01 to 2024-10-25 (UTC) |
| Channel | **BHZ** (vertical broadband) |
| Sampling rate | **40 Hz** |
| Window length | **300 s** from **catalog origin time** |
| Stations (manifest) | **CI.ADO** (6 events), **CI.USC** (2 events) |
| Raw storage | `data/raw/iris/` |
| Manifest | `data/manifests/iris_california_pilot_events.csv` |

**Note:** Exploratory inspection identified **twelve** MiniSEED files on disk at one stage, including **four legacy files** outside the current manifest (`reports/eda/mseed_file_inspection.csv`); all **completed analyses** use the **eight manifest-linked** records only.

### 5.2 Tables (**completed**)

- **Event metadata:** `reports/tables/event_summary.csv`  
- **Station usage:** `reports/tables/station_summary.csv`  
- **Signal metrics:** `reports/tables/signal_analysis_per_event.csv`  
- **Preprocessing QC:** `reports/tables/preprocessing_quality_metrics.csv`  
- **Features:** `reports/features/feature_matrix.csv`, `reports/tables/feature_correlation_matrix.csv`  

### 5.3 European dataset (**proposed**)

Future work will mirror the manifest/report pattern for **EIDA/ORFEUS** or national FDSN services, documenting authentication, channel conventions, and licensing (`docs/PROJECT_CHARTER.md`, Phase C roadmap).

---

## 6. Methodology

### 6.1 Acquisition methodology (**completed**)

Events were queried from USGS with geographic and magnitude filters; waveforms retrieved via EarthScope dataselect for a **distance-ranked candidate station list** (networks CI, NC, BK). One successful BHZ trace per retained event was stored as MiniSEED. Parameters are recorded in `docs/IRIS_DATASET_REPORT.md` and `logs/iris_california_pilot_summary.json`.

### 6.2 Exploratory data analysis (**completed**)

**Reference:** `docs/EDA_REPORT.md`  
Per-file ObsPy inspection (sample rate, duration, amplitude statistics) and cohort summaries for manifest events.

### 6.3 Signal analysis (**completed**)

**Reference:** `docs/SIGNAL_ANALYSIS_REPORT.md`  
For each trace: peak and RMS amplitudes, noise RMS from a **0–5 s proxy window**, peak SNR, STA/LTA P pick (0.5 s / 10 s windows, threshold **2.5**, ObsPy `classic_sta_lta`), and post-pick signal duration. **Limitation:** downloads start at origin time; pre-event noise is unavailable.

### 6.4 Preprocessing (**completed**)

**Reference:** `docs/PREPROCESSING_REPORT.md`, `reports/preprocessing/preprocessing_config.json`  

| Step | Parameter |
|------|-----------|
| Demean | Mean removal |
| Detrend | Linear |
| Taper | Hann, 5% |
| Band-pass | **0.1–15 Hz**, 4 corners, zero-phase |
| Instrument response | EarthScope `level=response` → velocity (**attempted**) |
| Normalisation | Peak absolute amplitude |

**Outcome:** Response removal **0/8 applied** (skipped); filtered traces remain in **counts**. Stage arrays stored in `reports/preprocessing/*_stages.npz`.

### 6.5 Feature engineering (**completed**)

**Reference:** `docs/FEATURE_ENGINEERING_REPORT.md`  
**18 features** per event from **filtered** traces: nine time-domain (including crest factor, zero-crossing rate, signal entropy), five spectral (dominant frequency, centroid, bandwidth, 95% roll-off, spectral entropy), four earthquake-related (P arrival from Phase A.2, duration, PGM proxy, Arias **counts²·s** proxy). FFT spectra visualised but not stored as matrix columns.

### 6.6 EarthESND reference methodology (**completed software; not primary experiment**)

The repository documents an **EarthESND-aligned optional track** ([PAPER_REPRODUCTION.md](docs/PAPER_REPRODUCTION.md); preprocessing contracts, ESN/DENN concepts). Executable modules are **not included in v1.0.0**. **Scientific reproduction** of published K-NET tables is **not started**. Phase D **proposed** work may **compare** Western pilot features against EarthESND-inspired architectures without conflating geographic objectives.

---

## 7. Experimental Workflow

The following pipeline is **implemented and executed** on the California pilot (see `docs/RESULTS_AND_DISCUSSION.md`):

```text
[Completed] USGS + EarthScope download → MiniSEED + CSV manifest
[Completed] Phase A.1 EDA → reports/eda/, summary figures
[Completed] Phase A.2 Signal analysis → STA/LTA, SNR, per-event figures
[Completed] Phase B.1 Preprocessing → stage NPZ, comparison figures
[Completed] Phase B.2 Features → 8×18 matrix, correlation/distribution figures
[Completed] Phase C Interpretation → docs/RESULTS_AND_DISCUSSION.md
[Completed] Deliverable 1 → reports/Research_Proposal_v1.md (this document)
[Proposed] European acquisition + response cache + larger N
[Proposed] ML training / EarthESND-inspired Western benchmarks
[Proposed] Real-time streaming prototype
```

Scripts reside under `scripts/download/` and `scripts/analysis/`; this deliverable **does not modify** them or re-run analyses.

---

## 8. Results & Discussion

**Primary synthesis:** `docs/RESULTS_AND_DISCUSSION.md`. Summary below.

### 8.1 Dataset and EDA

Eight events span a narrow magnitude band with **ADO-dominated** station counts (`reports/figures/station_usage_frequency.png`, `reports/figures/magnitude_histogram.png`, `reports/figures/events_over_time.png`). The **example raw waveform** for M 4.87 (`reports/figures/example_waveform_raw.png`) illustrates strong motion in digital counts without instrument correction.

### 8.2 Waveform behaviour and stations

Peak raw amplitudes span roughly **1.7×10⁴ to 3.5×10⁶ counts** (`reports/signal_analysis/signal_analysis_summary.json`). **P picks** range **10.15–55.15 s** after trace start (mean **31.3 s**). **CI.ADO** shows higher mean peak-SNR than **CI.USC** but lower mean raw peaks—a pattern consistent with **noise-window contamination** and **site gain**, not necessarily inferior data quality (`reports/figures/signal_analysis_*.png`).

### 8.3 Preprocessing effects

Four-panel figures (`reports/figures/preprocessing_*.png`) show reduced baseline drift and band-limited motion. Aggregate peak-SNR (proxy) rises from mean **137** (raw) to **1684** (filtered) (`reports/preprocessing/preprocessing_summary.json`); interpret as **processing sensitivity**, not guaranteed operational gain, given origin-aligned noise windows.

### 8.4 Features

The **8×18** matrix (`reports/features/feature_matrix.csv`) exhibits strong collinearity among amplitude-derived variables; **crest factor** (cohort mean ≈ **11.4**), **signal entropy**, **spectral entropy**, and **zero-crossing rate** offer complementary shape information (`reports/features/feature_summary.json`). Dominant frequency and spectral centroid cluster near **~2.3–2.6 Hz**, consistent with the **0.1–15 Hz** band-pass. **`feature_correlation_heatmap.png`**, **`feature_distributions.png`**, **`feature_boxplots_by_station.png`**, and **`feature_engineering_fft_spectra.png`** support visual assessment at **N=8** only.

### 8.5 Limitations and validity

Small sample size, single component, mixed magnitude types, selection bias toward ADO, failed response removal, and unvalidated P picks constrain generalisation (`docs/RESULTS_AND_DISCUSSION.md`, §6–7). These threats must be mitigated before European operational claims.

---

## 9. Relevance to Europe

Europe is the **primary research focus** of the programme; California validates **methods**, not **final deployment geography**.

### 9.1 Why the California pilot supports European goals

- Demonstrates **ObsPy/FDSN reproducibility** expected in European graduate and continuing-education research.  
- Surfaces **methodological pitfalls** (origin-aligned windows, response metadata, station bias) that also arise when integrating **ORFEUS/EIDA** data.  
- Produces **proposal-ready figures and tables** for Methodology and Dataset chapters while European catalogs are scoped.

### 9.2 Transfer plan (**proposed**)

Reuse manifest CSV structure, phase reports (`EDA`, signal, preprocessing, features), and analysis script layout with **European endpoint configuration**. Document licensing, magnitude conventions, and accelerometer vs broadband choices per network.

### 9.3 Expected European challenges (**proposed**)

Fragmented access policies, lower event rates in some regions, heterogeneous station density, and regulatory metadata requirements (see `docs/RESULTS_AND_DISCUSSION.md`, §9.3).

### 9.4 Expected benefits (**proposed**)

Cross-region comparison of onsite features, open artifact trails for auditors, and alignment with Swiss/European EEW research narratives.

---

## 10. Expected Outcomes

### 10.1 Already achieved (**completed**)

- Documented **FDSN acquisition** for California.  
- **EDA, signal analysis, preprocessing, feature engineering**, and **results & discussion** with artefacts in `reports/`.  
- **This Research Proposal & Technical Report** (Deliverable 1), integrating European programme framing.  
- **Reference EarthESND codebase** for future **comparative** ML studies (not primary objective).

### 10.2 Expected upon programme completion (**proposed**)

| Outcome | Description |
|---------|-------------|
| European pilot dataset | Manifest + acquisition report analogous to IRIS report |
| Response-corrected amplitudes | Physical units for magnitude proxies |
| Scaled feature catalogues | Sufficient **N** for train/validation experiments |
| ML baselines | Tabular and waveform models on Western data |
| EarthESND-inspired comparison | Documented deviation from Japan-centric paper metrics |
| Real-time feasibility note | Latency and streaming constraints for EEW |

---

## 11. Future Work

1. **Expand California or western USA catalogues** (stratified by distance and magnitude).  
2. **European FDSN pilot** via EIDA/ORFEUS; harmonise manifests.  
3. **Instrument response** caching and reprocessing of pilot NPZ inputs.  
4. **Pre-origin download windows** for unbiased noise and SNR.  
5. **Three-component data** where available.  
6. **AI models:** regression on features; deep learning on normalized windows; optional EarthESND-inspired ESN/DENN on Western tensors.  
7. **Real-time EEW prototype** (SeedLink, continuous STA/LTA).  
8. **Formal publication** of European transfer results with uncertainty quantification.

---

## 12. References

Allen, R. M., and Kanamori, H. (2003). The potential for earthquake early warning in southern California. *Science*, 300(5620), 786–788.

Hoshiba, M., Iwakiri, K., Hayashimoto, N., Shimoyama, T., Hirano, K., Yamada, Y., Ishigaki, Y., and Kikuta, H. (2008). Outline of the 2007–2008 earthquake early warning experiments in Japan. *Earth Planets Space*, 60, 123–129.

Joshi, A., Singh, A. P., and Raman, B. (2026). EarthESND: Lightweight multiscale echo state network with dendritic neural network readout for earthquake early warning. *Computers and Electrical Engineering* (optional literature track discussed in `docs/PAPER_REPRODUCTION.md`; **not primary geographic objective of this programme**).

Krischer, L., Megies, T., Barsch, R., Beyreuther, M., Lecocq, T., Caudron, C., and Wassermann, J. (2015). ObsPy: A bridge for earthquake science. *Seismological Research Letters*, 86(3), 765–771.

International Federation of Digital Seismograph Networks (FDSN). FDSN web services specification. https://www.fdsn.org/webservices/

EarthScope Consortium. Data services. https://www.earthscope.org/

U.S. Geological Survey. Earthquake Hazards Program — FDSN event web service.

ORFEUS Data Center / EIDA. European integrated waveform archives. https://www.orfeus-eu.org/

**Project documentation (this repository):**  
`docs/PROJECT_CHARTER.md`; `docs/RESEARCH_DIRECTION.md`; `docs/IRIS_DATASET_REPORT.md`; `docs/EDA_REPORT.md`; `docs/SIGNAL_ANALYSIS_REPORT.md`; `docs/PREPROCESSING_REPORT.md`; `docs/FEATURE_ENGINEERING_REPORT.md`; `docs/RESULTS_AND_DISCUSSION.md`.

---

## Appendix A — Index of generated figures and tables

### Figures (`reports/figures/`)

| Figure | Phase | Description |
|--------|-------|-------------|
| `example_waveform_raw.png` | A.1 EDA | Raw BHZ, highest pilot magnitude |
| `magnitude_histogram.png` | A.1 | Magnitude distribution (N=8) |
| `events_over_time.png` | A.1 | Origin time vs magnitude |
| `station_usage_frequency.png` | A.1 | ADO vs USC event counts |
| `signal_analysis_<event>.png` (×8) | A.2 | Raw, normalized, STA/LTA, P marker |
| `preprocessing_<event>.png` (×8) | B.1 | Raw → detrended → filtered → normalized |
| `feature_engineering_fft_spectra.png` | B.2 | Per-event FFT power |
| `feature_correlation_heatmap.png` | B.2 | 18×18 Pearson matrix |
| `feature_distributions.png` | B.2 | Per-feature histograms |
| `feature_boxplots_by_station.png` | B.2 | ADO vs USC for selected features |

### Tables (`reports/tables/` and `reports/features/`)

| Table | Phase |
|-------|-------|
| `event_summary.csv` | A.1 |
| `station_summary.csv` | A.1 |
| `signal_analysis_per_event.csv` | A.2 |
| `preprocessing_quality_metrics.csv` | B.1 |
| `feature_matrix.csv` | B.2 |
| `feature_correlation_matrix.csv` | B.2 |

### Machine-readable summaries

`reports/eda/dataset_summary.json`; `reports/signal_analysis/signal_analysis_summary.json`; `reports/preprocessing/preprocessing_summary.json`; `reports/features/feature_summary.json`.

---

**Document control:** Research Proposal & Technical Report v1.0 — Deliverable 1, AMGCR Earthquake Research, 29 July 2026.
