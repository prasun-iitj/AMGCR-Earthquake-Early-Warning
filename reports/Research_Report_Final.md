---
title: "Reproducible AI-Assisted Earthquake Early Warning Research for Western Seismic Regions"
subtitle: "Method Development on a California FDSN Pilot with Transfer Path to European Networks"
document: "Final Research Proposal and Technical Report (D-F1)"
version: "1.0"
date: "29 July 2026"
programme: "Assessment and Management of Geological and Climate Related Risk (AMGCR) — Swiss certificate research"
project: "AMGCR Earthquake Research"
status: "Consolidates completed pilot science; no new computations in this document"
---

<div align="center">

# Reproducible AI-Assisted Earthquake Early Warning Research for Western Seismic Regions

## Method Development on a California FDSN Pilot with Transfer Path to European Networks

**Final Research Proposal and Technical Report (Deliverable D-F1)**

**AMGCR Earthquake Research**

**29 July 2026**

</div>

---

## Certificate and programme statement

This report is submitted in partial fulfilment of research requirements for the **Swiss certificate programme** in **Assessment and Management of Geological and Climate Related Risk (AMGCR)**, as defined in `docs/PROJECT_CHARTER.md` and `docs/RESEARCH_DIRECTION.md`.

The **primary long-term research focus** of the programme is **Earthquake Early Warning (EEW) methodology for European seismic networks**. The **United States (California) FDSN pilot** documented herein is a **completed methods laboratory**, not the intended final deployment geography.

All quantitative results in this document are drawn from **existing repository artefacts** and phase reports dated **2026-07-29**. This final report **does not re-run** analysis scripts or introduce new scientific computations.

> **Evidence note:** The repository does not record a student author name or CERG edition number. Programme affiliation text above is taken from `reports/Research_Proposal_v1.md` and `docs/PROJECT_CHARTER.md` only.

---

## Executive summary

The **AMGCR Earthquake Research** project delivers a **documented, script-driven workflow** from FDSN earthquake catalogues and waveforms to **machine-learning-ready features**, aligned with European expectations for transparent natural-hazard research. Using **ObsPy** and public **USGS** (events) and **EarthScope** (waveforms) services, the pilot acquired **eight** vertical broadband (**BHZ**) MiniSEED recordings (magnitudes **4.05–4.87**, **2024**), performed exploratory data analysis, **STA/LTA**-based onsite metrics, band-limited preprocessing, and extraction of an **8×18** feature matrix.

**Main findings (completed pilot):**

1. A **reproducible end-to-end chain** exists from manifest CSV through tables, JSON summaries, and figures under `reports/`.
2. **Raw amplitudes** in digital counts vary by **orders of magnitude** across events and stations (**CI.ADO** vs **CI.USC**), reflecting path, site, and gain—not a homogeneous magnitude–amplitude relation at **N=8**.
3. **P-wave trigger times** from STA/LTA range **10.15–55.15 s** after trace start; late picks on several records indicate **trigger limitations** without pre-event windows or analyst validation.
4. **Preprocessing** improves visual clarity and band-limited SNR proxies (mean peak-SNR **137** raw → **1684** filtered), but **instrument response removal was not applied (0/8)**; amplitudes remain in **counts**, not physical ground-motion units.
5. **Feature statistics and correlations** are **illustrative only** at eight events; amplitude-derived features are highly collinear, while **crest factor**, **entropies**, and **zero-crossing rate** offer complementary shape information.

**EarthESND** (Joshi, Singh, and Raman, 2026) is retained as a **complete reference implementation** (**88 passing tests** on a full checkout) for **future comparative** ML studies—not as the geographic or scientific endpoint of this certificate work.

**European context:** The same manifest-and-report pattern is **proposed** for **ORFEUS/EIDA**-class archives. **No European waveform dataset** is included in the completed pilot.

**Submission artefacts:** Raw MiniSEED, local acquisition logs, and generated PNG figures may be **absent from Git clones** (`.gitignore`); see **Appendix C** and `docs/FINAL_DELIVERABLE_AUDIT.md`.

---

## Abstract

Earthquake Early Warning (EEW) delivers rapid estimates of ground shaking ahead of destructive S-wave arrival, combining seismological data acquisition, onsite triggering, signal processing, and increasingly machine-learning-based magnitude and intensity prediction. European programmes require transparent, reproducible workflows that can be audited, extended across national networks, and aligned with open data policies, yet many published pipelines remain tied to region-specific archives or proprietary tooling.

This report presents the **AMGCR Earthquake Research** project: a **European-focused** certificate programme whose **primary long-term target** is EEW-oriented analysis on **European seismic networks**, while **California** serves as the **completed pilot implementation** for method validation. Using ObsPy and FDSN services (USGS event metadata; EarthScope waveforms), we acquired eight MiniSEED recordings (magnitude 4.05–4.87, 2024), executed exploratory data analysis, STA/LTA-based signal characterisation, documented preprocessing, and extraction of an **8×18** feature matrix. Results confirm a reproducible path from raw waveforms to machine-learning-ready descriptors, while exposing limitations—origin-aligned download windows, absent instrument response correction in the pilot run, small sample size, and station-selection bias—that must be addressed before operational European deployment.

The repository retains a **complete EarthESND reference implementation** (echo state network with dendritic readout) **only as a literature and architecture benchmark**, not as the programme’s scientific endpoint. **Proposed future work** includes scaling datasets, integrating ORFEUS/EIDA-class European archives, response-corrected amplitudes, and comparative evaluation of modern onsite AI models including EarthESND-inspired designs on Western data.

**Keywords:** earthquake early warning; ObsPy; FDSN; reproducible research; feature engineering; Europe; California pilot; machine learning; STA/LTA; EarthScope; USGS

---

## Table of contents

1. [Introduction](#1-introduction)  
2. [Literature review](#2-literature-review)  
3. [Research gap](#3-research-gap)  
4. [Objectives](#4-objectives)  
5. [Dataset](#5-dataset)  
6. [Methodology](#6-methodology)  
7. [California pilot workflow and execution](#7-california-pilot-workflow-and-execution)  
8. [Results](#8-results)  
9. [Discussion](#9-discussion)  
10. [Limitations and threats to validity](#10-limitations-and-threats-to-validity)  
11. [European context and transfer](#11-european-context-and-transfer)  
12. [Future work and expected outcomes](#12-future-work-and-expected-outcomes)  
13. [Conclusion](#13-conclusion)  
14. [References](#14-references)  
15. [Statement of evidence support](#15-statement-of-evidence-support)  
- [Appendix A — Pilot event and station tables](#appendix-a--pilot-event-and-station-tables)  
- [Appendix B — Reproducibility statement (D-S1)](#appendix-b--reproducibility-statement-d-s1)  
- [Appendix C — Data availability and ethics statement (D-S2)](#appendix-c--data-availability-and-ethics-statement-d-s2)  
- [Appendix D — Supplementary per-event figures](#appendix-d--supplementary-per-event-figures)  
- [Appendix E — Machine-readable summary index](#appendix-e--machine-readable-summary-index)  

---

## List of figures

| Figure | File | Section |
|--------|------|---------|
| Figure 1 | `figures/example_waveform_raw.png` | §8.1 |
| Figure 2 | `figures/magnitude_histogram.png` | §8.1 |
| Figure 3 | `figures/events_over_time.png` | §8.1 |
| Figure 4 | `figures/station_usage_frequency.png` | §8.1 |
| Figure 5 | `figures/signal_analysis_ci40675215.png` | §8.2 |
| Figure 6 | `figures/signal_analysis_ci40699207.png` | §8.2 |
| Figure 7 | `figures/preprocessing_ci40675215.png` | §8.3 |
| Figure 8 | `figures/preprocessing_ci40699207.png` | §8.3 |
| Figure 9 | `figures/feature_engineering_fft_spectra.png` | §8.4 |
| Figure 10 | `figures/feature_correlation_heatmap.png` | §8.4 |
| Figure 11 | `figures/feature_distributions.png` | §8.4 |
| Figure 12 | `figures/feature_boxplots_by_station.png` | §8.4 |
| Figure D1–D6 | `figures/signal_analysis_ci40593503.png` … (see Appendix D) | Appendix D |
| Figure D7–D12 | `figures/preprocessing_ci40593503.png` … (see Appendix D) | Appendix D |

*All paths relative to this file’s directory (`reports/`). Full set: **24** PNGs per `docs/FINAL_DELIVERABLE_AUDIT.md`.*

---

## List of tables

| Table | Source | Section |
|-------|--------|---------|
| Table 1 | Pilot dataset attributes | §5.1 |
| Table 2 | FDSN query parameters (summary) | §5.2 |
| Table 3 | Objectives and status | §4 |
| Table 4 | Preprocessing parameters | §6.4 |
| Table 5 | Aggregate signal metrics | §8.2 |
| Table 6 | Station-level signal contrasts | §8.2 |
| Table 7 | Preprocessing SNR aggregates | §8.3 |
| Table 8 | Feature domains (18 features) | §6.5 |
| Table 9 | Threats to validity | §10.2 |
| Table A1 | Event summary | Appendix A |
| Table A2 | Station summary | Appendix A |

*Full CSV exports: `reports/tables/` and `reports/features/feature_matrix.csv`.*

---

## 1. Introduction

### 1.1 Motivation

Damaging earthquakes remain a major risk in Europe and adjacent regions, from the Mediterranean belt to the Alps and anthropogenic seismicity associated with industrial activity. EEW systems mitigate harm by issuing alerts seconds to tens of seconds before strong shaking arrives at a site, based on **P-wave detection**, **rapid magnitude estimation**, and **ground-motion prediction**. Public acceptance, regulatory frameworks, and civil-protection integration—in Switzerland and across the EU—increasingly expect **documented, open methodologies** rather than black-box prototypes.

### 1.2 Programme positioning

The project was initiated within a **Swiss certificate programme** in geophysical risk assessment, aligned with **European expectations** for traceable analysis (open data, documented processing, explicit limitations). Initial effort targeted reproduction of the **EarthESND** architecture (Joshi, Singh, and Raman, 2026), producing a **test-backed reference codebase** preserved for **methodological comparison only**. Programme guidance subsequently reframed the work toward a **logical European EEW research project** with real waveforms, theory, visualisation, tables, and formal reporting—using **California FDSN data** as a **completed pilot laboratory** (`docs/PROJECT_CHARTER.md`, `docs/RESEARCH_DIRECTION.md`).

### 1.3 Scope of this document

This **final report (D-F1)** supersedes `reports/Research_Proposal_v1.md` as the submission-oriented consolidation. It synthesises **completed pilot work** (acquisition through interpretation) and **proposed extensions** (European data, scale, AI evaluation, real-time paths). Sources: phase reports under `docs/`, artefacts under `reports/`, `docs/REPRODUCIBILITY_STATEMENT.md`, `docs/DATA_AVAILABILITY_STATEMENT.md`, and `docs/FINAL_DELIVERABLE_AUDIT.md`.

### 1.4 Document control

| Field | Value |
|-------|--------|
| Deliverable | D-F1 Final Research Proposal / Technical Report |
| Version | 1.0 |
| Date | 29 July 2026 |
| Prior version | Research Proposal v1.0 (`reports/Research_Proposal_v1.md`) |
| Pilot freeze date | 2026-07-29 (phase reports) |

---

## 2. Literature review

### 2.1 Earthquake Early Warning fundamentals

Classical EEW relies on **onsite algorithms** that detect P-wave onset via STA/LTA ratio tests or similar triggers, then estimate magnitude and alert levels from early windows of acceleration or velocity (Allen and Kanamori, 2003; Hoshiba et al., 2008). Key trade-offs include **detection latency**, **false alarm rate**, and **magnitude saturation** for large events. European deployments emphasise **standardised metadata**, **latency budgets**, and **uncertainty communication** to end users.

### 2.2 Open seismological software and data

**ObsPy** (Krischer et al., 2015) provides a standard interface for MiniSEED, FDSN web services, detrending, filtering, and instrument correction. **FDSN** federates event and waveform services; in this project, **USGS** supplies catalogues and **EarthScope** supplies waveforms (`docs/IRIS_DATASET_REPORT.md`). The same abstraction is intended for **European** endpoints (ORFEUS, EIDA, national nodes).

### 2.3 Machine learning in onsite EEW

Deep learning and reservoir computing approaches learn magnitude or intensity from early waveform segments but require **large, diverse training sets** and careful handling of **site effects** and **instrument response**. **EarthESND** proposes a multiscale **ESN** with **DENN** readout for onsite magnitude estimation in a **Japan K-NET** context. In AMGCR, EarthESND is implemented as **reference pipeline** code (`src/`, automated tests) for **architecture comparison**, **not** as the primary certificate geographic focus.

### 2.4 Reproducibility in computational seismology

Reproducible EEW research demands versioned **download parameters**, **manifests**, **processing configs**, and **analysis scripts**. This project institutionalises that pattern through CSV manifests, JSON summaries, and phase reports.

### 2.5 European and Swiss context

ORFEUS, **EIDA**, and member-state networks provide the **intended long-term data plane**. The California pilot functions as a **methods prototype** while the **scientific narrative** remains **Europe-forward** (`docs/PROJECT_CHARTER.md`).

---

## 3. Research gap

1. **European programme need vs. Japan-centric ML papers:** Transferable, documented workflows for **European FDSN data** are less commonly packaged for certificate-level research.  
2. **End-to-end openness:** Many studies lack full artifact trails from **raw MiniSEED** to **feature matrices**.  
3. **Separation of benchmark code and active science:** This project **decouples** EarthESND software completion from Western pilot analysis (`docs/RESEARCH_DIRECTION.md`).  
4. **Pilot-scale validity:** Small-**N** pilots illustrate methodology but **cannot** support operational EEW claims—the gap to validated European input remains **explicit**.

---

## 4. Objectives

### 4.1 Primary objective (programme)

Develop a **reproducible, AI-ready EEW research workflow** aimed ultimately at **European seismic networks**, documented for a Swiss/European research audience.

### 4.2 Secondary objective (pilot — completed)

Implement and validate the workflow on a **California IRIS/EarthScope pilot**: acquisition, EDA, signal analysis, preprocessing, feature engineering, and interpretation.

### 4.3 Specific objectives

**Table 3 — Objectives and status**

| ID | Objective | Status |
|----|-----------|--------|
| O1 | FDSN-based download of real earthquake waveforms with ObsPy | **Completed** |
| O2 | Exploratory dataset characterisation | **Completed** |
| O3 | Onsite-style signal metrics and STA/LTA P-wave analysis | **Completed** |
| O4 | Documented preprocessing chain toward ML inputs | **Completed** (response step **0/8**; documented) |
| O5 | Multi-domain feature matrix for EEW/ML experiments | **Completed** (**8×18**) |
| O6 | Scientific interpretation and European transfer narrative | **Completed** |
| O7 | European FDSN pilot and scaled catalogues | **Proposed** |
| O8 | AI model training on Western data | **Proposed** |
| O9 | Real-time / latency-oriented prototype | **Proposed** |
| O10 | Research Proposal & Technical Report | **Completed** (v1); **superseded by this D-F1 report** |

---

## 5. Dataset

### 5.1 Completed California pilot

**Table 1 — Pilot dataset attributes** (sources: `docs/IRIS_DATASET_REPORT.md`, `docs/EDA_REPORT.md`, `reports/eda/dataset_summary.json`)

| Attribute | Value |
|-----------|--------|
| Region | California bounding box, **2024** |
| Event provider | USGS FDSN Event |
| Waveform provider | EarthScope (`Client("EARTHSCOPE")`) |
| Events in manifest | **8** |
| Magnitude range | **4.05 – 4.87** (`mw`, `ml`) |
| Origin times (UTC) | **2024-05-01** – **2024-10-25** |
| Channel | **BHZ** |
| Sampling rate | **40 Hz** |
| Window | **300 s** from **catalog origin time** |
| Stations (manifest) | **CI.ADO** (6 events), **CI.USC** (2 events) |
| Manifest path | `data/manifests/iris_california_pilot_events.csv` |
| Raw waveforms (local) | `data/raw/iris/` |

**Legacy files:** EDA recorded **twelve** MiniSEED files on disk at run time; **four** lie outside the current manifest (`reports/eda/mseed_file_inspection.csv`). **All completed analyses use eight manifest-linked records only.**

### 5.2 FDSN acquisition parameters (summary)

**Table 2 — FDSN query parameters** (from `docs/IRIS_DATASET_REPORT.md`)

| Parameter | Event search (USGS) | Waveform download (EarthScope) |
|-----------|---------------------|--------------------------------|
| Time window | 2024-01-01 – 2024-12-31 | 300 s from origin |
| Latitude | 32.5° – 42.0° N | — |
| Longitude | −124.5° – −114.0° E | — |
| Magnitude | 4.0 – 7.5 | — |
| Networks (candidates) | — | CI, NC, BK |
| Channel | — | BHZ (may try HHZ/EHZ) |
| Stations per event | — | 1 (first successful candidate) |
| Catalog matches (query) | **41** | — |
| Events retained | **8** | **8** waveforms |

Station selection uses a **fixed distance-ranked candidate list**; this is **not** uniform network sampling.

### 5.3 European dataset (proposed)

No European waveforms are included. Future work is expected to mirror manifest and report patterns for **EIDA/ORFEUS** (`docs/PROJECT_CHARTER.md`, `docs/ROADMAP.md`).

### 5.4 Published tables and matrices

- `reports/tables/event_summary.csv`, `station_summary.csv`  
- `reports/tables/signal_analysis_per_event.csv`  
- `reports/tables/preprocessing_quality_metrics.csv`  
- `reports/features/feature_matrix.csv`, `reports/tables/feature_correlation_matrix.csv`  

---

## 6. Methodology

### 6.1 Acquisition (completed)

Script: `scripts/download/download_iris_california_pilot.py`. Events from USGS; waveforms from EarthScope dataselect. Parameters and results: `docs/IRIS_DATASET_REPORT.md`, `logs/iris_california_pilot_summary.json` (local, gitignored).

### 6.2 Exploratory data analysis (Phase A.1)

Script: `scripts/analysis/run_california_pilot_eda.py`. ObsPy inspection of all `.mseed` under `data/raw/iris/`; cohort summaries for **manifest** events only (`docs/EDA_REPORT.md`).

### 6.3 Signal analysis (Phase A.2)

Script: `scripts/analysis/run_california_signal_analysis.py`. Per trace: peak/RMS amplitudes, noise RMS from **0–5 s** proxy, peak SNR, STA/LTA P pick (**STA 0.5 s**, **LTA 10 s**, threshold **2.5**, ObsPy `classic_sta_lta`), signal duration (`docs/SIGNAL_ANALYSIS_REPORT.md`).

### 6.4 Preprocessing (Phase B.1)

Script: `scripts/analysis/run_california_preprocessing.py`. Frozen config: `reports/preprocessing/preprocessing_config.json`.

**Table 4 — Preprocessing parameters**

| Step | Setting |
|------|---------|
| Demean | Mean removal |
| Detrend | Linear |
| Taper | Hann, **5%** |
| Band-pass | **0.1–15 Hz**, four corners, zero-phase |
| Instrument response | EarthScope `level=response` → velocity (**attempted**) |
| Normalisation | Peak absolute amplitude |

**Outcome:** Response removal **0/8 applied** (skipped); filtered traces remain in **counts** (`docs/PREPROCESSING_REPORT.md` §4). Stages: `reports/preprocessing/<short_id>_stages.npz`.

### 6.5 Feature engineering (Phase B.2)

Script: `scripts/analysis/run_california_feature_engineering.py`. **18 features** from **filtered** traces; P times from Phase A.2 metrics JSON (`docs/FEATURE_ENGINEERING_REPORT.md`).

**Table 8 — Feature domains (18 features)**

| Domain | Count | Examples (repository names) |
|--------|-------|-----------------------------|
| Time-domain | 9 | `peak_amplitude`, `rms`, `crest_factor`, `zero_crossing_rate_hz`, `signal_entropy`, … |
| Frequency-domain | 5 | `dominant_frequency_hz`, `spectral_centroid_hz`, `spectral_bandwidth_hz`, `spectral_rolloff_95_hz`, `spectral_entropy` |
| Earthquake-related | 4 | `p_arrival_time_s`, `signal_duration_s`, `pgm_proxy_counts`, `arias_intensity_counts2_s_proxy` |

FFT spectra are **figure-only** (not matrix columns). **PGM** and **Arias** entries are **counts-based proxies**, not physical PGA or standard Arias intensity.

### 6.6 EarthESND reference (not primary experiment)

Full EarthESND-aligned implementation in `src/` with **88 passing tests** on a complete checkout. **K-NET scientific reproduction is not started.** California pilot results **did not** use EarthESND modules (`docs/RESULTS_AND_DISCUSSION.md` §1).

---

## 7. California pilot workflow and execution

```text
[Completed] USGS + EarthScope download → MiniSEED + CSV manifest
[Completed] Phase A.1 EDA → reports/eda/, four summary figures
[Completed] Phase A.2 Signal analysis → STA/LTA, SNR, eight four-panel figures
[Completed] Phase B.1 Preprocessing → stage NPZ, eight comparison figures
[Completed] Phase B.2 Features → 8×18 matrix, four feature figures
[Completed] Phase C Interpretation → docs/RESULTS_AND_DISCUSSION.md
[Completed] Deliverable 1 → Research_Proposal_v1.md
[Completed] D-S1/D-S2 → Reproducibility & data availability statements
[Completed] D-F1 → this document
[Proposed] European acquisition, response cache, larger N, ML, real-time
```

Reproduction commands: **Appendix B**. The EarthESND reference track remains optional (`docs/PAPER_REPRODUCTION.md`).

---

## 8. Results

*Primary synthesis: `docs/RESULTS_AND_DISCUSSION.md`. No new numbers below.*

### 8.1 Exploratory data analysis

Eight events occupy a narrow **M 4–5** band; **CI.ADO** supplies six of eight traces. Figures 1–4 summarise raw example, magnitude distribution, temporal coverage, and station usage.

![Figure 1: Raw BHZ record (highest pilot magnitude M 4.87, CI.ADO); amplitudes in digital counts, 300 s window from trace start.](figures/example_waveform_raw.png)

![Figure 2: Magnitude distribution for eight manifest events.](figures/magnitude_histogram.png)

![Figure 3: Origin time versus magnitude for manifest events.](figures/events_over_time.png)

![Figure 4: Station usage frequency (CI.ADO vs CI.USC).](figures/station_usage_frequency.png)

**Interpretation (`docs/RESULTS_AND_DISCUSSION.md` §2.3):** The histogram reflects **query cutoffs**, not regional completeness. Temporal gaps reflect **download success**. ADO dominance is **structural bias** from the acquisition script.

### 8.2 Signal analysis and waveform behaviour

Peak raw amplitudes span approximately **1.7×10⁴ to 3.5×10⁶ counts** (`reports/signal_analysis/signal_analysis_summary.json`).

**Table 5 — Aggregate signal metrics (8 events)**

| Quantity | Value |
|----------|--------|
| P pick (s from trace start) | **10.15 – 55.15** (mean **31.3**) |
| SNR (peak), raw | **6.3 – 778** (median **49.9**) |
| Signal duration (post-P proxy) | **0 – 289.5 s** (mean **183.2**) |

**Table 6 — Station contrasts** (`signal_analysis_summary.json`)

| Station | n | Mean SNR (peak) | Mean P pick (s) | Mean peak (counts) |
|---------|---|-----------------|-----------------|---------------------|
| CI.ADO | 6 | **169** | **30.5** | **2.98×10⁵** |
| CI.USC | 2 | **42** | **33.6** | **1.83×10⁶** |

Figure 5 shows **ci40675215** (M **4.87**, high SNR, early pick ~**10.2 s**). Figure 6 shows **ci40699207** at **CI.USC** (SNR **~6**, duration **0 s**), illustrating **noise-window contamination** when downloads start at origin time.

![Figure 5: Signal analysis panels for ci40675215 (raw, normalized, STA/LTA, P marker).](figures/signal_analysis_ci40675215.png)

![Figure 6: Signal analysis panels for ci40699207 (low peak-SNR case at USC).](figures/signal_analysis_ci40699207.png)

### 8.3 Preprocessing

**Table 7 — Aggregate peak-SNR proxy**

| Stage | Mean SNR (peak) |
|-------|-----------------|
| Raw | **137** |
| Filtered (pre-normalization) | **1684** |

Filtered/raw SNR ratio range **2.5–27.6** (mean **17.1**). Figures 7–8 show four-panel progressions (raw → detrended → filtered → normalized) for the same events as Figures 5–6.

![Figure 7: Preprocessing stages for ci40675215.](figures/preprocessing_ci40675215.png)

![Figure 8: Preprocessing stages for ci40699207.](figures/preprocessing_ci40699207.png)

**Interpretation:** Visual stabilisation supports ML-oriented comparison; **without response correction**, filtered **counts** are **not** physical velocity/acceleration for magnitude estimation.

### 8.4 Feature engineering

The **8×18** matrix is stored in `reports/features/feature_matrix.csv`. **Crest factor** cohort mean ≈ **11.4**; **dominant frequency** and **spectral centroid** cluster near **~2.3–2.6 Hz** (`reports/features/feature_summary.json`), consistent with the **0.1–15 Hz** band-pass.

Strong collinearity links amplitude-derived features; **crest factor**, **signal entropy**, **spectral entropy**, and **zero_crossing_rate_hz** provide partially independent shape information at **N=8** only.

![Figure 9: Per-event FFT power spectra (filtered traces).](figures/feature_engineering_fft_spectra.png)

![Figure 10: Pearson correlation heatmap (18 features, 8 samples).](figures/feature_correlation_heatmap.png)

![Figure 11: Per-feature distributions.](figures/feature_distributions.png)

![Figure 12: Selected features by station (ADO vs USC).](figures/feature_boxplots_by_station.png)

---

## 9. Discussion

### 9.1 Integration of phases

The pilot demonstrates a **script-driven, documented path** from FDSN services to **tabular ML inputs** and **normalized NPZ stages**, satisfying certificate requirements for ObsPy, real data, graphs, and tables (`docs/RESULTS_AND_DISCUSSION.md` §8).

### 9.2 Onsite triggering and warning-time budgets

STA/LTA panels connect classroom EEW theory to **P-time features**, but **late picks** and **origin-aligned noise** show that **trigger parameters cannot be tuned** on this dataset alone without pre-event windows and validation.

### 9.3 ML readiness versus generalisation

The feature matrix is **suitable for pilot baselines** (e.g., linear models, random forests) only in an **exploratory** sense. **No ML training or hold-out evaluation** was performed in the completed pilot—**no predictive performance metrics** are reported in repository artefacts.

> **Evidence note:** Any statement implying model accuracy or operational detection probability would be **unsupported**; this report claims **feature extraction only**.

### 9.4 Relation to EarthESND

Reference code enables **future** architecture comparison on **Western** tensors with an explicit **deviation log** from Japan-centric paper tables. It **does not** validate EarthESND on California data in the completed work.

---

## 10. Limitations and threats to validity

### 10.1 Pilot limitations (California)

1. **N = 8** — no reliable generalisation or correlation inference.  
2. **Single component (BHZ).**  
3. **Origin-aligned windows** — biased noise and SNR.  
4. **No response removal (0/8).**  
5. **Station selection bias** (ADO-heavy; USC **n=2**).  
6. **Mixed magnitude types (`mw`, `ml`).**  
7. **Four legacy MiniSEED files** on disk outside manifest.  
8. **Unvalidated P picks.**  
9. **Not comparable to EarthESND K-NET metrics.**

(Source: `docs/RESULTS_AND_DISCUSSION.md` §6.)

### 10.2 Threats to validity

**Table 9 — Threats and mitigations** (from `docs/RESULTS_AND_DISCUSSION.md` §7)

| Threat | Description | Mitigation (proposed) |
|--------|-------------|------------------------|
| Construct validity | Counts used where physical motion required | StationXML cache; response removal |
| Internal validity | SNR inflated after filtering with fixed noise window | Pre-origin download windows |
| External validity | California CI ≠ European networks | EIDA/ORFEUS pilot with same scripts |
| Statistical conclusion validity | N=8 | Larger catalogues; bootstrap CIs |
| Selection bias | First-eight successful downloads | Stratified sampling |
| Confirmation bias | Fixed STA/LTA threshold | Threshold sweeps; ML picks |

---

## 11. European context and transfer

Europe is the **primary programme focus**; California validates **methods**, not deployment geography (`docs/PROJECT_CHARTER.md`).

**Why the pilot supports European goals (`docs/RESULTS_AND_DISCUSSION.md` §9):**

- Demonstrates **ObsPy/FDSN reproducibility**.  
- Surfaces pitfalls (origin-aligned windows, response metadata, station bias) relevant to **ORFEUS/EIDA** integration.  
- Delivers **figures and tables** for methodology chapters while European catalogues are scoped.

**Transfer plan (proposed):** Reuse manifest CSV structure, phase report templates, and `scripts/` layout with European endpoint configuration; document licensing, magnitude conventions, and channel choices per network.

**Expected challenges (proposed):** Fragmented access policies, lower event rates in some regions, heterogeneous station density, accelerometer vs broadband mix, regulatory metadata (`docs/RESULTS_AND_DISCUSSION.md` §9.3).

**Expected benefits (proposed):** Cross-region feature comparison, open artifact trails, alignment with Swiss/European EEW research narratives.

---

## 12. Future work and expected outcomes

### 12.1 Already achieved

- Documented California FDSN acquisition and **full analysis chain**.  
- Phase reports, `reports/` artefacts, Research Proposal v1, D-S1/D-S2, and this D-F1 report.  
- EarthESND reference codebase for **comparative** studies (not primary objective).

### 12.2 Proposed extensions

| Direction | Objective |
|-----------|-----------|
| Larger catalogues | 50–200+ events; stratified splits |
| European FDSN pilot | EIDA/ORFEUS manifests and reports |
| Instrumentation | Response correction; 3-component data; pre-event noise |
| AI models | Tabular and waveform baselines; EarthESND-inspired comparisons with deviation log |
| Real-time EEW | SeedLink simulation; latency budgets |
| Formal publication | European transfer with uncertainty quantification |

(Source: `docs/RESULTS_AND_DISCUSSION.md` §10, `reports/Research_Proposal_v1.md` §11.)

---

## 13. Conclusion

1. A **reproducible chain** from FDSN acquisition to an **8×18 feature matrix** is **established** for the California pilot.  
2. **Raw waveforms** exhibit strong **station/path effects** and **heterogeneous STA/LTA pick times**; **ADO** dominates sampling.  
3. **Preprocessing** improves interpretability and band-limited SNR proxies, but **response removal failed for all eight traces**—**physical amplitude EEW is not yet supported**.  
4. **Features** combine time, frequency, and pick-based descriptors; **correlations** show redundancy among amplitude metrics and value in **shape statistics** at pilot scale.  
5. **Validity threats** must be addressed before **operational** or **publication-grade** EEW claims.  
6. California proves the **method**; **Europe** is the **intended context** for scaled deployment with network-specific metadata discipline.

---

## 14. References

Allen, R. M., and Kanamori, H. (2003). The potential for earthquake early warning in southern California. *Science*, 300(5620), 786–788.

Hoshiba, M., Iwakiri, K., Hayashimoto, N., Shimoyama, T., Hirano, K., Yamada, Y., Ishigaki, Y., and Kikuta, H. (2008). Outline of the 2007–2008 earthquake early warning experiments in Japan. *Earth Planets Space*, 60, 123–129.

Joshi, A., Singh, A. P., and Raman, B. (2026). EarthESND: Lightweight multiscale echo state network with dendritic neural network readout for earthquake early warning. *Computers and Electrical Engineering* (reference implementation: `docs/EARTHESND_REVERSE_ENGINEERING.md`; not primary geographic objective).

Krischer, L., Megies, T., Barsch, R., Beyreuther, M., Lecocq, T., Caudron, C., and Wassermann, J. (2015). ObsPy: A bridge for earthquake science. *Seismological Research Letters*, 86(3), 765–771.

International Federation of Digital Seismograph Networks (FDSN). FDSN web services specification. https://www.fdsn.org/webservices/

EarthScope Consortium. Data services. https://www.earthscope.org/

U.S. Geological Survey. Earthquake Hazards Program — FDSN event web service. https://earthquake.usgs.gov

ORFEUS Data Center / EIDA. European integrated waveform archives. https://www.orfeus-eu.org/

**Project documentation:** `docs/PROJECT_CHARTER.md`; `docs/RESEARCH_DIRECTION.md`; `docs/IRIS_DATASET_REPORT.md`; `docs/EDA_REPORT.md`; `docs/SIGNAL_ANALYSIS_REPORT.md`; `docs/PREPROCESSING_REPORT.md`; `docs/FEATURE_ENGINEERING_REPORT.md`; `docs/RESULTS_AND_DISCUSSION.md`; `docs/REPRODUCIBILITY_STATEMENT.md`; `docs/DATA_AVAILABILITY_STATEMENT.md`; `docs/FINAL_DELIVERABLE_AUDIT.md`.

---

## 15. Statement of evidence support

| Statement class | Support |
|-----------------|--------|
| Numeric results (SNR, picks, magnitudes, feature means) | **Supported** — JSON/CSV cited in phase reports and summarised in §8 |
| Figure content | **Supported** — PNG paths verified in `docs/FINAL_DELIVERABLE_AUDIT.md` (24/24 local) |
| ML model performance | **Not claimed** — no training artefacts in repository |
| Operational EEW deployment | **Not claimed** — explicitly out of scope |
| European dataset results | **Not claimed** — proposed only |
| Author name / CERG edition | **Not in repository** — placeholder avoided; programme name from charter only |
| EarthESND 88 tests | **Supported** — `docs/PROJECT_CHARTER.md`, `README.md` |
| Git clone contains all PNG/MiniSEED | **Qualified** — audit WARNING; see Appendix C |

---

## Appendix A — Pilot event and station tables

**Table A1 — Event summary** (full CSV: `reports/tables/event_summary.csv`)

| short_id | Magnitude | Type | Station | Origin (UTC) |
|----------|-----------|------|---------|----------------|
| ci40964384 | 4.54 | ml | CI.ADO | 2024-10-25 15:04:23 |
| ci40964128 | 4.72 | mw | CI.ADO | 2024-10-25 08:05:08 |
| ci40964048 | 4.16 | mw | CI.ADO | 2024-10-25 06:52:08 |
| nn00882322 | 4.39 | ml | CI.ADO | 2024-08-14 03:06:35 |
| ci40699207 | 4.39 | mw | CI.USC | 2024-08-12 19:20:24 |
| ci40675215 | 4.87 | mw | CI.ADO | 2024-07-29 20:00:52 |
| ci40593503 | 4.05 | mw | CI.ADO | 2024-05-20 12:17:36 |
| ci40735352 | 4.11 | mw | CI.USC | 2024-05-01 20:49:00 |

**Table A2 — Station summary** (`reports/tables/station_summary.csv`)

| Station | Events | Mean fs (Hz) | Duration (s) |
|---------|--------|--------------|--------------|
| CI.ADO.--.BHZ | 6 | 40.0 | 300.0 |
| CI.USC.--.BHZ | 2 | 40.0 | 300.0 |

---

## Appendix B — Reproducibility statement (D-S1)

*The following text is the repository reproducibility statement (`docs/REPRODUCIBILITY_STATEMENT.md`), included for submission. Figure paths in that file use repository-root notation; PNG outputs appear under `reports/figures/` relative to this report.*

### B.1 What this workflow reproduces

The pilot chain in `scripts/download/` and `scripts/analysis/` produces: manifest and MiniSEED (when downloaded); EDA summaries and four figures; signal metrics, eight figures, and CSV; preprocessing NPZ, eight figures, QC table; **8×18** feature matrix and four feature figures. Interpretation is in phase docs and prior proposals. **California results did not use EarthESND `src/` modules.**

### B.2 Software environment

Python **≥ 3.11**; ObsPy, NumPy, Pandas, Matplotlib, SciPy, PyYAML per `pyproject.toml`. Suggested install: `pip install -e ".[dev]"` from repository root. No separate `requirements.txt`.

### B.3 Execution order

```powershell
python scripts/download/download_iris_california_pilot.py --event-count 8 --min-events 5
python scripts/analysis/run_california_pilot_eda.py
python scripts/analysis/run_california_signal_analysis.py
python scripts/analysis/run_california_preprocessing.py
python scripts/analysis/run_california_feature_engineering.py
```

Defaults: `data/raw/iris/`, `data/manifests/iris_california_pilot_events.csv`, `logs/iris_california_pilot_summary.json`. Preprocessing config: `reports/preprocessing/preprocessing_config.json`.

### B.4 Included vs excluded artefacts

**Typically in Git:** scripts, manifest, phase docs, `reports/tables/`, JSON summaries, NPZ, feature matrix (see audit).

**Gitignored:** `data/raw/`, `logs/`, `figures/` (includes `reports/figures/`). Fresh clones must **regenerate** or use a separate archive (`docs/FINAL_DELIVERABLE_AUDIT.md`).

### B.5 Reproducibility limitations

FDSN rerun variability; fixed station list; origin-aligned windows; **0/8** response removal; **N=8**; EarthESND not on pilot path; PNGs may differ slightly by library version.

### B.6 Verification

Compare to `reports/eda/dataset_summary.json`, `reports/signal_analysis/signal_analysis_summary.json`, `reports/preprocessing/preprocessing_summary.json`, `reports/features/feature_summary.json`.

---

## Appendix C — Data availability and ethics statement (D-S2)

*Condensed from `docs/DATA_AVAILABILITY_STATEMENT.md` for this submission package.*

### C.1 Data sources

| Role | Provider | Access |
|------|----------|--------|
| Catalog | USGS FDSN Event | Public — https://earthquake.usgs.gov |
| Waveforms | EarthScope | Public FDSN — https://service.earthscope.org |

Query details: `docs/IRIS_DATASET_REPORT.md`. **Eight** events, magnitudes **4.05–4.87**, **CI.ADO** (6) / **CI.USC** (2). **No credentials** required.

### C.2 Repository availability

**In Git (typical):** manifest, derived `reports/` products, scripts, documentation.

**Not in Git:** raw MiniSEED (`data/raw/`), logs (`logs/`), figures (`reports/figures/` per `.gitignore` rule `figures/`).

**Regeneration:** download script + analysis pipeline (Appendix B).

### C.3 Ethics

Public seismic data only; no human subjects; cite USGS, EarthScope, and FDSN terms. GDPR note applies to **future** European integrations, not the completed California pilot.

### C.4 Data-use limitations

BHZ only; N=8; ADO bias; legacy files outside manifest; counts not physical motion; not EarthESND geography.

Full citations: see `docs/DATA_AVAILABILITY_STATEMENT.md` §7 and §14 of this report.

---

## Appendix D — Supplementary per-event figures

Remaining **signal analysis** panels (four-panel: raw, normalized, STA/LTA, P marker):

| Fig. | File |
|------|------|
| D1 | `figures/signal_analysis_ci40593503.png` |
| D2 | `figures/signal_analysis_ci40735352.png` |
| D3 | `figures/signal_analysis_ci40964048.png` |
| D4 | `figures/signal_analysis_ci40964128.png` |
| D5 | `figures/signal_analysis_ci40964384.png` |
| D6 | `figures/signal_analysis_nn00882322.png` |

Remaining **preprocessing** panels (raw → detrended → filtered → normalized):

| Fig. | File |
|------|------|
| D7 | `figures/preprocessing_ci40593503.png` |
| D8 | `figures/preprocessing_ci40735352.png` |
| D9 | `figures/preprocessing_ci40964048.png` |
| D10 | `figures/preprocessing_ci40964128.png` |
| D11 | `figures/preprocessing_ci40964384.png` |
| D12 | `figures/preprocessing_nn00882322.png` |

![Figure D1: Signal analysis — ci40593503.](figures/signal_analysis_ci40593503.png)

![Figure D2: Signal analysis — ci40735352.](figures/signal_analysis_ci40735352.png)

![Figure D3: Signal analysis — ci40964048.](figures/signal_analysis_ci40964048.png)

![Figure D4: Signal analysis — ci40964128.](figures/signal_analysis_ci40964128.png)

![Figure D5: Signal analysis — ci40964384.](figures/signal_analysis_ci40964384.png)

![Figure D6: Signal analysis — nn00882322.](figures/signal_analysis_nn00882322.png)

![Figure D7: Preprocessing — ci40593503.](figures/preprocessing_ci40593503.png)

![Figure D8: Preprocessing — ci40735352.](figures/preprocessing_ci40735352.png)

![Figure D9: Preprocessing — ci40964048.](figures/preprocessing_ci40964048.png)

![Figure D10: Preprocessing — ci40964128.](figures/preprocessing_ci40964128.png)

![Figure D11: Preprocessing — ci40964384.](figures/preprocessing_ci40964384.png)

![Figure D12: Preprocessing — nn00882322.](figures/preprocessing_nn00882322.png)

---

## Appendix E — Machine-readable summary index

| File | Content |
|------|---------|
| `reports/eda/dataset_summary.json` | EDA cohort statistics |
| `reports/signal_analysis/signal_analysis_summary.json` | Signal aggregates |
| `reports/preprocessing/preprocessing_summary.json` | Preprocessing aggregates |
| `reports/features/feature_summary.json` | Feature cohort statistics |
| `reports/preprocessing/preprocessing_config.json` | Frozen B.1 parameters |

---

**Document control:** Final Research Proposal and Technical Report (D-F1) v1.0 — AMGCR Earthquake Research, 29 July 2026. Supersedes Deliverable 1 (`reports/Research_Proposal_v1.md`) for submission packaging. No source code modified to produce this document.
