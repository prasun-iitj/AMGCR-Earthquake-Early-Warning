# RESULTS_AND_DISCUSSION.md

**Phase C — Scientific interpretation and research reporting**  
California IRIS / EarthScope pilot (certificate-track EEW research)

| Field | Value |
|-------|--------|
| Document date (UTC) | 2026-07-29 |
| Scope | Interpretation only — **no new computations**; draws on existing reports and `reports/` artefacts |
| Programme context | [PROJECT_CHARTER.md](PROJECT_CHARTER.md), [RESEARCH_DIRECTION.md](RESEARCH_DIRECTION.md) |

**Source reports:** [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) · [EDA_REPORT.md](EDA_REPORT.md) · [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) · [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) · [FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md)

---

## Abstract

Eight California earthquake waveforms (M 4.05–4.87, 2024) were acquired via USGS and EarthScope FDSN services, inspected, analysed with STA/LTA-based onsite metrics, preprocessed with a documented band-limited pipeline, and reduced to an **8×18** feature matrix. Results show **large station- and path-dependent amplitudes** in raw counts, **heterogeneous P-trigger times** (10–55 s after trace start), and **clear visual improvement** after detrending and filtering, but **no instrument response correction** in the current run. Feature statistics and correlations are **illustrative at N=8** yet demonstrate a **reproducible path** from open waveform data to EEW-oriented machine-learning inputs. The same workflow is positioned for transfer to **European FDSN archives** once inventory and scale requirements are met.

---

## 1. End-to-end workflow summary

The certificate research chain, as implemented and documented in this repository, proceeds as follows.

```text
Acquisition (USGS events + EarthScope MiniSEED)
    → data/raw/iris/ + data/manifests/iris_california_pilot_events.csv
    → docs/IRIS_DATASET_REPORT.md

Phase A.1 EDA
    → reports/eda/ (inspection CSV, dataset_summary.json)
    → reports/tables/event_summary.csv, station_summary.csv
    → reports/figures/ (example raw trace, magnitude histogram, events vs time, station usage)

Phase A.2 Signal analysis
    → reports/signal_analysis/ (per-event metrics JSON)
    → reports/tables/signal_analysis_per_event.csv
    → reports/figures/signal_analysis_*.png (raw, normalized, STA/LTA, P marker)

Phase B.1 Preprocessing
    → reports/preprocessing/ (config, stages NPZ, per-event metrics)
    → reports/tables/preprocessing_quality_metrics.csv
    → reports/figures/preprocessing_*.png (raw → detrended → filtered → normalized)

Phase B.2 Feature engineering
    → reports/features/feature_matrix.csv, feature_summary.json
    → reports/tables/feature_correlation_matrix.csv
    → reports/figures/feature_engineering_*.png (FFT grid, correlation heatmap, distributions, boxplots)
```

Each stage is **script-driven and reproducible**; the EarthESND reference implementation in `src/` was **not** used for these USA pilot results, preserving a clean separation between **literature benchmark code** and **active Western-region research**.

---

## 2. Dataset characteristics

### 2.1 Acquisition

- **Region:** California bounding box (2024 catalogue, M ≥ 4 in query).  
- **Events retained:** **8** with one **BHZ** waveform each.  
- **Providers:** USGS (hypocenters), EarthScope (waveforms).  
- **Sampling:** **40 Hz**, **300 s** windows starting at **catalog origin time**.  
- **Magnitudes:** **4.05–4.87** (mix of `mw` and `ml`); temporal spread **May–October 2024**.  
- **Stations:** **CI.ADO** (6 events), **CI.USC** (2 events)—a **distance-ranked download policy**, not uniform network sampling.

### 2.2 Tables interpreted

| Table | Main finding |
|-------|----------------|
| `event_summary.csv` | Each event tied to one station file; hypocenter metadata supports future distance–amplitude studies. |
| `station_summary.csv` | Confirms **40 Hz / 300 s** consistency; **ADO-dominated** sample. |
| `mseed_file_inspection.csv` | Twelve files on disk at EDA time; **four legacy** files excluded from manifest summaries—artefacts must be ignored or re-harmonised in future runs. |

### 2.3 EDA figures interpreted

| Figure | Interpretation |
|--------|----------------|
| **`example_waveform_raw.png`** | Strong motion on **M 4.87** at ADO in **raw counts**; energy visible without processing but baseline and coda dominate a 300 s window. |
| **`magnitude_histogram.png`** | Narrow M 4–5 band; **not** representative of full regional seismicity—consistent with pilot query cutoffs. |
| **`events_over_time.png`** | Clustering in **May**, **July–August**, and **late October**; gaps reflect **download success**, not uniform sampling. |
| **`station_usage_frequency.png`** | **ADO** supplies most traces because the acquisition script’s candidate list favoured it for epicentral distance—**structural bias** for any station-level inference. |

---

## 3. Waveform behaviour and signal quality

### 3.1 Raw dynamics

Signal analysis reports **peak counts** from **~1.7×10⁴ to ~3.5×10⁶**, with **full-trace RMS** dominated by energetic segments. Vertical-component records show **order-of-magnitude scatter** at similar catalog magnitudes, implying **path, site, and instrument gain** control raw scaling more than M alone in this sample.

### 3.2 STA/LTA P-wave observations

| Metric | Range / mean (8 events) |
|--------|-------------------------|
| P pick (s from trace start) | **10.15 – 55.15** (mean **31.3**) |
| SNR (peak), raw | **6.3 – 778** (median **49.9**) |
| Signal duration (post-P proxy) | **0 – 289.5 s** (mean **183.2**) |

**`signal_analysis_*.png` panels:** Raw traces show variable onset clarity; STA/LTA curves cross threshold **2.5** on all events, but **late picks** (35–55 s) on several ADO records suggest triggers on **stronger later arrivals or coda** rather than first motion. **Early picks** (~10–13 s) on high-SNR events (e.g. **ci40675215**, **ci40735352**) are more consistent with **near-source or energetic P coda**.

### 3.3 Signal quality and SNR limitations

Noise was estimated from the **first 5 s** of each **origin-aligned** trace. Because downloads **do not include pre-event quiet time**, the “noise” window can contain **early seismic energy** (notably at **USC**, **ci40699207**: SNR **~6**, duration **0 s**). Thus **SNR is a QC indicator**, not a calibrated EEW detection probability.

**Station contrast (signal_analysis_summary.json):**

| Station | n | Mean SNR (peak) | Mean P pick (s) | Mean peak (counts) |
|---------|---|-----------------|-----------------|---------------------|
| CI.ADO | 6 | **169** | **30.5** | **2.98×10⁵** |
| CI.USC | 2 | **42** | **33.6** | **1.83×10⁶** |

USC exhibits **higher peaks** but **lower mean SNR**—consistent with **contaminated noise windows** and **site amplification in counts**, not necessarily “worse” seismological quality.

---

## 4. Effect of preprocessing

### 4.1 Pipeline outcomes

Preprocessing applied **demean**, **linear detrend**, **5% Hann taper**, **0.1–15 Hz band-pass**, and **peak normalization**, with **instrument response removal attempted 0/8 times** (skipped; traces remain in **counts** after filtering).

### 4.2 Quality metrics (aggregate)

| Stage | SNR (peak), mean |
|-------|------------------|
| Raw | **137** |
| Filtered (pre-normalization) | **1684** |

Reported **SNR ratios** (filtered/raw) range **2.5–27.6** (mean **17.1**). This rise largely reflects **lower noise RMS in the band-limited first 5 s**, not guaranteed improvement in **operational pick latency**.

### 4.3 Preprocessing figures interpreted

**`preprocessing_*.png` (four panels each):**

1. **Raw** — DC offsets and long-period drift visible on 300 s windows.  
2. **Detrended** — Baseline flattened; earthquake-related oscillations stand out.  
3. **Filtered** — Motion concentrated in **EEW-relevant band**; high-frequency clutter reduced.  
4. **Normalized** — Peaks aligned to unity for **ML input scaling**; shape preserved.

**Discussion:** Visually, preprocessing **stabilises** traces for comparison and neural input. **Scientifically**, without **response correction**, filtered **counts** cannot be interpreted as velocity or acceleration for **magnitude estimation** or **cross-network** comparison.

---

## 5. Feature engineering: distributions and correlations

### 5.1 Feature matrix

- **Shape:** **8 events × 18 features** (`reports/features/feature_matrix.csv`).  
- **Domain mix:** Time (9), frequency (5), earthquake-related (4).  
- **P picks:** All features used **Phase A.2** STA/LTA times (`p_pick_source: phase_a2_metrics`).

### 5.2 Distributions (`feature_distributions.png`)

With **N=8**, histograms act as **pilot dashboards**, not density estimates. Notable aggregate behaviour from `feature_summary.json`:

- **Dominant frequency / spectral centroid** cluster near **~2.3–2.6 Hz**, shaped by **0.1–15 Hz band-pass** and window length.  
- **Crest factor** (mean **~11.4**, σ **~3.2**) indicates **impulsive** character on several records—relevant for **trigger tuning**.  
- **Large std on amplitude-derived features** (peak, RMS, variance, energy) reflects **USC vs ADO scaling** in counts.

### 5.3 Correlations (`feature_correlation_heatmap.png`, `feature_correlation_matrix.csv`)

Expected **strong collinearity**:

- **peak_amplitude**, **pgm_proxy_counts** (identical by definition).  
- **signal_energy**, **arias_intensity_counts2_s_proxy** (identical proxy).  
- **rms**, **std**, **variance** (algebraically related).

For ML, **dimensionality reduction** or **explicit feature selection** will be required. **Crest factor**, **zero-crossing rate**, **signal entropy**, and **spectral entropy** provide **partially independent** shape information useful for **small-N exploration**.

### 5.4 FFT spectra (`feature_engineering_fft_spectra.png`)

Power concentrates below **~15 Hz** by construction; inter-event differences in **spectral roll-off** and **dominant peaks** hint at **source and path variability** but cannot be generalised statistically at **N=8**.

### 5.5 Station boxplots (`feature_boxplots_by_station.png`)

**ADO (n=6) vs USC (n=2):** USC drives **upper tails** on **peak/RMS/PGM proxies**; ADO contributes **more stable** spectral means. **Boxplots are indicative only** given **unbalanced counts**.

---

## 6. Limitations of the California pilot

1. **Sample size:** **8** events — no reliable ML generalisation or correlation inference.  
2. **Single component (BHZ):** No horizontal energy, rotation, or MMI linkage.  
3. **Origin-aligned windows:** No true pre-event noise; **SNR and STA/LTA** metrics are **methodologically biased**.  
4. **No response removal:** Amplitude and intensity proxies are **not physical**.  
5. **Station selection bias:** Download logic favours **ADO**; USC **n=2**.  
6. **Magnitude types mixed (`mw`, `ml`):** Labels are **not** a homogeneous regression target.  
7. **Legacy MiniSEED on disk:** Four non-manifest files must not enter scientific summaries without reconciliation.  
8. **P picks unvalidated:** No analyst picks or travel-time modelling.  
9. **Decoupled from EarthESND paper geography:** Results **do not** reproduce K-NET-based literature metrics.

---

## 7. Threats to validity

| Threat | Description | Mitigation in future work |
|--------|-------------|---------------------------|
| **Construct validity** | Counts used where physical ground motion is required | Cache StationXML; remove response; report in m/s or m/s² |
| **Internal validity** | SNR inflated after filtering with fixed noise window | Pre-origin download (−30 s); independent noise segment |
| **External validity** | California CI network ≠ European networks | Re-run identical scripts on EIDA/ORFEUS pilots |
| **Statistical conclusion validity** | N=8, multiple testing on correlations | Hold-out regions; bootstrap CIs; larger catalogues |
| **Selection bias** | First-eight successful downloads | Stratify by magnitude, distance, azimuth |
| **Confirmation bias** | STA/LTA threshold chosen a priori | Sweep thresholds; compare ML picks |

---

## 8. Support for future Earthquake Early Warning research

Despite pilot limits, the workflow supports EEW research in four concrete ways:

1. **Reproducible FDSN-to-features path** — Documents every step from open data to **ML-ready tensors** (normalized NPZ) and **tabular features**, matching professor requirements (ObsPy, real data, graphs, tables).  
2. **Onsite trigger literacy** — STA/LTA panels and **P-time features** connect classroom theory to **warning-time budgets**.  
3. **Processing-aware QC** — Before/after preprocessing tables show why **band-limiting** and **detrending** precede magnitude proxies in operational systems.  
4. **Benchmark hook** — The same feature schema can be compared against **EarthESND-inspired** architectures (reference code) on **Western** data in Phase D, with an explicit **deviation log** from Japan-centric paper numbers.

---

## 9. Relevance to Europe

### 9.1 Why California is a suitable pilot

- **Mature FDSN infrastructure** (USGS + EarthScope) enables **ObsPy-first** teaching and research without proprietary APIs.  
- **High seismicity and dense networks (CI, NC, BK)** provide rich **waveform diversity** in a single language/locale of metadata.  
- **Manageable event counts** for a **certificate timeline** while still exposing **real noise, picks, and preprocessing pitfalls** that also appear in European operations.

California is **not** the programme’s end geography ([PROJECT_CHARTER.md](PROJECT_CHARTER.md)); it is the **experimental laboratory** for methods that will be **re-targeted to Europe**.

### 9.2 Transferring the workflow to European seismic networks

The same staged layout applies:

| Step | USA (done) | Europe (planned) |
|------|------------|------------------|
| Catalog + waveforms | USGS + EarthScope | ORFEUS/EIDA, national FDSN nodes (e.g. OE, CH, FR) |
| Manifest CSV | `iris_california_pilot_events.csv` | `europe_pilot_events.csv` (template) |
| Reports | `docs/IRIS_*`, `reports/*` | Parallel `docs/EU_*` reports |
| Scripts | `scripts/download/`, `scripts/analysis/` | Same code, new YAML/query params |

**ObsPy** abstracts most differences; **documentation** (query bounds, magnitude conventions, channel naming) becomes the main migration cost.

### 9.3 Expected challenges in Europe

- **Fragmented data policies** — mix of open and restricted networks; **authentication** on some endpoints.  
- **Lower event rates** in parts of Central/Northern Europe — longer calendar windows needed for **N** comparable to California pilots.  
- **Station density variability** — Alps vs platform regions; **uneven station usage** may worsen without explicit sampling design.  
- **Strong-motion vs broadband** mix — EEW often uses **accelerometers**; channel selection must be **documented per network**.  
- **Regulatory framing** — Swiss/EU programmes may require **GDPR**, **citation**, and **DOI** metadata in proposals.

### 9.4 Expected benefits

- **Proposal credibility** — Demonstrates a **complete pipeline** on real data before claiming European operational relevance.  
- **Cross-region science** — Compare **Alpine**, **Mediterranean**, and **Atlantic** path effects using **identical features**.  
- **Operational alignment** — European EEW initiatives (national early-warning test beds) value **open, scriptable** preprocessing and feature logs like those in `reports/preprocessing/preprocessing_config.json`.

---

## 10. Future research

| Direction | Objective |
|-----------|-----------|
| **Larger datasets** | Expand California (or western USA) to **50–200+** events; stratify by distance and magnitude; enable train/validation splits. |
| **European datasets** | Pilot download via EIDA; mirror manifests and Phase A–B reports; compare **feature distributions** USA vs EU. |
| **AI models** | Tabular baselines (magnitude regression); CNN/Transformer on **normalized windows** around P; optional **EarthESND-inspired** ESN/DENN on Western tensors with deviation log. |
| **Real-time EEW** | Stream simulation (SeedLink); latency budgets; replace batch FDSN with **continuous STA/LTA + feature push**. |
| **EarthESND-inspired approaches** | Use reference implementation for **architecture ablation**, not geography; train on **Western** data; document gaps vs Joshi et al. (2026) tables. |
| **Instrumentation** | Fix response removal; add **H/N components**; **pre-event noise** windows; analyst-validated picks. |
| **Proposal deliverables** | Consolidate this document into **Introduction, Dataset, Methodology, Expected outcomes** chapters for the Swiss certificate. |

---

## 11. Key conclusions

1. A **full reproducible chain** from FDSN acquisition to an **8×18 feature matrix** is established for the California pilot.  
2. **Raw waveforms** show **strong station/path effects** and **heterogeneous onsite pick times**; **ADO** dominates sampling.  
3. **Preprocessing** improves **visual interpretability** and **band-limited SNR proxies**, but **response removal failed** for all eight traces—**physical amplitude EEW is not yet supported**.  
4. **Features** combine time, frequency, and pick-based descriptors; **correlations** highlight redundancy among amplitude metrics and the value of **shape entropies and crest factor** for pilot ML.  
5. **Validity threats** (N, noise window, counts, selection bias) must be addressed before **operational** or **publication-grade** EEW claims.  
6. California proves the **method**; **Europe** is the **intended deployment context** for the same ObsPy-centric workflow at larger scale and with network-specific metadata discipline.

---

## 12. Artefact index (interpreted in this document)

**Reports:** `docs/IRIS_DATASET_REPORT.md`, `EDA_REPORT.md`, `SIGNAL_ANALYSIS_REPORT.md`, `PREPROCESSING_REPORT.md`, `FEATURE_ENGINEERING_REPORT.md`

**Summaries:** `reports/eda/dataset_summary.json`, `reports/signal_analysis/signal_analysis_summary.json`, `reports/preprocessing/preprocessing_summary.json`, `reports/features/feature_summary.json`

**Tables:** `reports/tables/event_summary.csv`, `station_summary.csv`, `signal_analysis_per_event.csv`, `preprocessing_quality_metrics.csv`, `feature_matrix.csv`, `feature_correlation_matrix.csv`

**Figures:** EDA and signal/preprocessing/feature PNGs under `reports/figures/` (see source reports for filenames).

---

Version: **1.0.0** (Phase C)
