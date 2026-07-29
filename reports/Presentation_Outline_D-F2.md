# D-F2 — Presentation outline (Markdown / PPT)

**Source of truth:** `reports/Research_Report_Final.md` (D-F1 v1.0, 29 July 2026)  
**Deliverable:** Oral presentation outline — **24 slides** (~10–15 minutes at ~40–45 s/slide)  
**Figure root:** `reports/figures/` (paths below are relative to `reports/`)

**Format:** Each slide = **Title** · **Bullets** (≤6) · **Figure placement** · **Speaker notes**

---

## Slide 1 — Title

**Title:** Reproducible AI-Assisted Earthquake Early Warning Research for Western Seismic Regions  

**Subtitle:** Method Development on a California FDSN Pilot with Transfer Path to European Networks  

**Bullets:**
- AMGCR Earthquake Research
- Final Research Proposal and Technical Report (D-F1)
- Swiss certificate programme — AMGCR
- 29 July 2026

**Figure:** None  

**Speaker notes:** This presentation summarises the completed California FDSN pilot and the European-oriented framing of the AMGCR certificate project. All results are drawn from the final technical report and frozen repository artefacts dated 2026-07-29. No new analyses are presented today.

---

## Slide 2 — Introduction: motivation

**Title:** Why Earthquake Early Warning and open methods matter  

**Bullets:**
- EEW: alerts seconds to tens of seconds before strong shaking
- Based on P-wave detection, magnitude estimation, ground-motion prediction
- Risk in Europe: Mediterranean belt, Alps, anthropogenic seismicity
- Switzerland and EU expect documented, open methodologies
- Not black-box prototypes for civil protection

**Figure:** None  

**Speaker notes:** The report opens with European relevance even though the pilot uses California data. Public and regulatory acceptance of EEW depends on traceable processing and explicit limitations. This project aligns with that expectation for certificate-level research.

---

## Slide 3 — Programme positioning

**Title:** Europe-focused programme; California as methods laboratory  

**Bullets:**
- Primary long-term target: European seismic networks
- California IRIS/EarthScope pilot: **completed** validation lab
- Initial EarthESND codebase: reference only (**88 tests** on full checkout)
- Active work: real waveforms, theory, figures, tables, formal reporting
- Pilot freeze: 2026-07-29; report consolidates completed science

**Figure:** None  

**Speaker notes:** The charter reframed the project from paper reproduction toward a logical European EEW workflow. EarthESND remains an architecture benchmark, not the geographic endpoint. California was chosen for mature FDSN APIs and ObsPy practice.

---

## Slide 4 — Research gap

**Title:** Gaps this workflow addresses  

**Bullets:**
- Few packaged, documented EEW workflows for **European FDSN** data
- Many studies lack trails from raw MiniSEED to ML-ready features
- Benchmark code (EarthESND) decoupled from Western pilot science
- Small-N pilots cannot support operational EEW claims
- Gap to validated European input stated explicitly

**Figure:** None  

**Speaker notes:** The report lists four gap themes: European programme need, end-to-end openness, separation of reference code from active science, and pilot-scale validity. The presentation does not claim to close the operational gap—only to document a reproducible methods path.

---

## Slide 5 — Objectives

**Title:** Objectives and completion status  

**Bullets:**
- **Primary:** Reproducible, AI-ready EEW workflow for European networks
- **Secondary (done):** California pilot end-to-end
- **O1–O6:** Download, EDA, signal, preprocessing, **8×18** features, interpretation — **completed**
- **O4 note:** Instrument response **0/8** applied; documented
- **O7–O9:** Europe scale, AI training, real-time — **proposed**
- **O10:** Proposal/report — **completed** (D-F1 supersedes v1)

**Figure:** None (optional: show **Table 3** from report as handout)  

**Speaker notes:** Objectives map directly to repository phases and scripts. Completed objectives O1–O6 match the certificate pipeline through feature engineering. Proposed objectives are roadmap items, not results of this pilot.

---

## Slide 6 — Literature: EEW fundamentals

**Title:** Literature — onsite EEW  

**Bullets:**
- STA/LTA and similar triggers for P-wave onset
- Early-window amplitude/velocity for magnitude and alerts
- Trade-offs: latency, false alarms, magnitude saturation
- Allen and Kanamori (2003); Hoshiba et al. (2008)
- European focus: metadata, latency budgets, uncertainty communication

**Figure:** None  

**Speaker notes:** Classical EEW literature motivates the signal-analysis phase. The pilot uses ObsPy classic STA/LTA with documented window lengths and threshold, not operational network tuning. European deployments emphasise standardised metadata and user-facing uncertainty.

---

## Slide 7 — Literature: data, software, and ML context

**Title:** Literature — ObsPy, FDSN, ML, reproducibility  

**Bullets:**
- **ObsPy** (Krischer et al., 2015): MiniSEED, FDSN, processing
- **USGS** events + **EarthScope** waveforms in this pilot
- ML/reservoir methods need large datasets and response handling
- **EarthESND:** ESN/DENN; Japan K-NET context; **reference code only** here
- Reproducibility: manifests, JSON configs, phase reports

**Figure:** None  

**Speaker notes:** The same FDSN abstraction is intended for ORFEUS/EIDA later. EarthESND is cited as literature and implemented in src for future comparison, not trained on California in the completed work. Reproducibility is a first-class deliverable alongside science.

---

## Slide 8 — California pilot dataset

**Title:** Dataset — completed California pilot  

**Bullets:**
- **8** events; M **4.05–4.87** (`mw`, `ml`); May–Oct **2024**
- **BHZ**, **40 Hz**, **300 s** from catalog origin time
- **CI.ADO:** 6 events; **CI.USC:** 2 events
- Manifest: `data/manifests/iris_california_pilot_events.csv`
- **12** MiniSEED on disk at EDA; **4** legacy — analyses use **8** manifest only
- No European waveforms in completed pilot

**Figure:** None (optional: **Table 1** / **Table A1** from report)  

**Speaker notes:** Table 1 in the report consolidates these attributes. Legacy files are documented but excluded from cohort summaries. The pilot is intentionally small for certificate timeline while exposing real processing pitfalls.

---

## Slide 9 — FDSN acquisition parameters

**Title:** How data were acquired  

**Bullets:**
- USGS event search: California box, 2024, M **4.0–7.5** → **41** catalog matches
- EarthScope: **CI, NC, BK** candidates; **BHZ**; one trace per event
- **8** events retained with waveforms
- Fixed distance-ranked station list — not uniform sampling
- Public FDSN; no credentials
- Script: `scripts/download/download_iris_california_pilot.py`

**Figure:** None (optional: **Table 2** from report)  

**Speaker notes:** Acquisition parameters are frozen in the IRIS dataset report cited by D-F1. Station policy explains ADO dominance in later results. Re-running download may yield different events; published science uses the committed manifest.

---

## Slide 10 — End-to-end workflow

**Title:** California pilot workflow (completed vs proposed)  

**Bullets:**
- **Done:** Download → EDA → signal → preprocessing → features → interpretation
- **Done:** D-S1/D-S2 statements; D-F1 final report
- **Outputs:** `reports/eda/`, `signal_analysis/`, `preprocessing/`, `features/`, `figures/`
- **Not used for pilot:** EarthESND `src/` modules
- **Proposed:** European FDSN, larger N, ML, real-time SeedLink
- Reproduction: Appendix B commands

**Figure:** None (use workflow as **text diagram** from report §7 on slide; no separate PNG in repository)  

**Speaker notes:** Walk the audience through the linear pipeline in section 7 of the report. Each stage has a dedicated script and phase report. Proposed items are clearly labelled and must not be presented as completed outcomes.

---

## Slide 11 — Methodology: EDA and signal analysis

**Title:** Methods — Phase A.1 EDA & Phase A.2 signal  

**Bullets:**
- **EDA:** ObsPy inspection; manifest-only summaries; four cohort figures
- **Signal:** Peak/RMS, noise **0–5 s** proxy, peak SNR
- **STA/LTA:** 0.5 s / 10 s, threshold **2.5**; P pick + duration
- Limitation: windows start at **origin** — no pre-event quiet time
- Scripts: `run_california_pilot_eda.py`, `run_california_signal_analysis.py`

**Figure:** None  

**Speaker notes:** Methods match SIGNAL_ANALYSIS_REPORT and EDA_REPORT as summarised in D-F1 section 6. The noise window limitation drives SNR caveats in results. P picks are exploratory onsite triggers, not analyst-validated phase picks.

---

## Slide 12 — Methodology: preprocessing and features

**Title:** Methods — Phase B.1 preprocessing & Phase B.2 features  

**Bullets:**
- Demean, linear detrend, **5%** Hann taper
- Band-pass **0.1–15 Hz**, zero-phase
- Response removal attempted → **0/8 applied** (counts remain)
- Peak normalisation; stages in `*_stages.npz`
- **18 features** from **filtered** traces; P times from Phase A.2
- Domains: 9 time, 5 frequency, 4 earthquake-related (counts proxies)

**Figure:** None (optional: **Table 4**, **Table 8** from report)  

**Speaker notes:** Preprocessing config is frozen in preprocessing_config.json. PGM and Arias entries are counts-based proxies, not physical intensity. Feature matrix shape is 8×18 plus metadata columns in CSV.

---

## Slide 13 — Results: EDA (example waveform)

**Title:** Results — exploratory data analysis (1/2)  

**Bullets:**
- Narrow **M 4–5** band; not regional completeness
- Example: largest pilot M **4.87** at **CI.ADO**
- Raw amplitudes in **digital counts**; 300 s window
- Strong motion visible without correction; baseline/coda in long window
- Histogram reflects query cutoffs

**Figure:** **`figures/example_waveform_raw.png`** (Report Figure 1)  

**Speaker notes:** Figure 1 is the highest-magnitude manifest event. The report stresses that this is a teaching and QC view, not response-corrected ground motion. Use this slide to connect raw data to later preprocessing panels.

---

## Slide 14 — Results: EDA (catalog views)

**Title:** Results — exploratory data analysis (2/2)  

**Bullets:**
- Temporal clustering May, Jul–Aug, Oct 2024
- Gaps reflect download success, not uniform sampling
- **ADO** supplies **6/8** traces — structural acquisition bias
- **USC:** 2 events (Southern California examples)
- EDA uses manifest-linked files only

**Figure:** **`figures/magnitude_histogram.png`** (Fig. 2), **`figures/events_over_time.png`** (Fig. 3), **`figures/station_usage_frequency.png`** (Fig. 4) — layout: 2+1 or three-panel  

**Speaker notes:** Figures 2–4 support dataset characterisation objectives O2. Station usage directly foreshadows unbalanced feature boxplots later. Emphasise that eight events are illustrative, not statistically representative of California seismicity.

---

## Slide 15 — Results: signal analysis (high-SNR case)

**Title:** Results — signal analysis: aggregates and ci40675215  

**Bullets:**
- Peak raw counts ≈ **1.7×10⁴–3.5×10⁶**
- P pick: **10.15–55.15 s** (mean **31.3 s**)
- SNR (peak): **6.3–778** (median **49.9**)
- **ci40675215:** M **4.87**; early pick ~**10.2 s**; high SNR
- Four-panel figure: raw, normalised, STA/LTA, P marker

**Figure:** **`figures/signal_analysis_ci40675215.png`** (Report Figure 5)  

**Speaker notes:** Table 5 in the report lists aggregate metrics shown in bullets. Figure 5 is the positive example where STA/LTA crosses threshold early. Relate pick time to warning-time budget concepts from EEW literature.

---

## Slide 16 — Results: signal analysis (low-SNR / USC)

**Title:** Results — signal analysis: station contrast & ci40699207  

**Bullets:**
- **CI.ADO (n=6):** mean SNR **169**; mean peak **2.98×10⁵** counts
- **CI.USC (n=2):** mean SNR **42**; mean peak **1.83×10⁶** counts
- **ci40699207:** SNR **~6**; signal duration **0 s**
- Origin-aligned “noise” window may include early energy
- SNR is QC indicator, not detection probability

**Figure:** **`figures/signal_analysis_ci40699207.png`** (Report Figure 6)  

**Speaker notes:** Table 6 documents station contrasts. USC higher peaks but lower SNR illustrate noise-window contamination, not necessarily poor seismological quality. This supports limitations on STA/LTA tuning without pre-event data.

---

## Slide 17 — Results: preprocessing

**Title:** Results — preprocessing effects  

**Bullets:**
- Mean peak-SNR: **137** (raw) → **1684** (filtered)
- Filtered/raw ratio **2.5–27.6** (mean **17.1**)
- Four stages: raw → detrended → filtered → normalised
- Visual stabilisation for ML comparison
- **Without response removal:** filtered **counts** ≠ physical motion

**Figure:** **`figures/preprocessing_ci40675215.png`** (Fig. 7), **`figures/preprocessing_ci40699207.png`** (Fig. 8) — side-by-side or sequential  

**Speaker notes:** Table 7 summarises SNR aggregates. Interpret SNR rise as processing sensitivity given fixed 0–5 s noise window, not guaranteed operational gain. Figures 7–8 mirror the signal examples from slides 15–16.

---

## Slide 18 — Results: feature engineering (spectra & correlations)

**Title:** Results — feature matrix, spectra, correlations  

**Bullets:**
- **8×18** matrix: `reports/features/feature_matrix.csv`
- Crest factor mean ≈ **11.4**
- Dominant frequency / centroid ≈ **2.3–2.6 Hz** (band-pass **0.1–15 Hz**)
- Strong collinearity among amplitude-derived features
- Shape features: crest factor, entropies, zero-crossing rate
- **N=8:** illustrative only; no ML training performed

**Figure:** **`figures/feature_engineering_fft_spectra.png`** (Fig. 9), **`figures/feature_correlation_heatmap.png`** (Fig. 10)  

**Speaker notes:** The report explicitly states no predictive performance metrics exist. Correlation heatmap motivates future feature selection. FFT figure shows band-limited power per event without generalisable statistics.

---

## Slide 19 — Results: feature distributions and stations

**Title:** Results — feature distributions & ADO vs USC  

**Bullets:**
- Histograms: pilot dashboards, not density estimates
- Large spread on amplitude-derived features (gain/path)
- Boxplots: USC upper tails on peak/RMS/PGM proxies
- ADO (n=6) vs USC (n=2) — unbalanced
- PGM/Arias columns are counts proxies only

**Figure:** **`figures/feature_distributions.png`** (Fig. 11), **`figures/feature_boxplots_by_station.png`** (Fig. 12)  

**Speaker notes:** Figures 11–12 close the results section before discussion. Tie back to station usage Figure 4. Reinforce that feature extraction is complete but model training is proposed work O8.

---

## Slide 20 — Discussion

**Title:** Discussion — integration and ML readiness  

**Bullets:**
- Script-driven path: FDSN → tabular features + normalised NPZ stages
- STA/LTA panels link theory to P-time features
- Late picks + origin noise limit trigger tuning on this dataset alone
- Feature matrix: exploratory baselines only
- **No ML training** — no accuracy metrics in repository
- EarthESND: future Western comparison with deviation log

**Figure:** None (optional revisit small **`figures/station_usage_frequency.png`** if time)  

**Speaker notes:** Section 9 of the report is the authority here. Do not claim operational EEW or model performance. EarthESND validation on California data did not occur in completed work.

---

## Slide 21 — Limitations

**Title:** Limitations of the California pilot  

**Bullets:**
- **N = 8**; single **BHZ** component
- Origin-aligned windows; biased noise/SNR
- **0/8** instrument response removal
- Station bias: ADO-heavy; USC **n=2**
- Mixed **mw** / **ml**; unvalidated P picks
- Not comparable to EarthESND K-NET metrics

**Figure:** None  

**Speaker notes:** List mirrors report section 10.1 from RESULTS_AND_DISCUSSION. Legacy MiniSEED files and four off-manifest traces are documented but omitted from bullets to stay within six; mention verbally if asked.

---

## Slide 22 — Threats to validity

**Title:** Threats to validity (summary)  

**Bullets:**
- Construct: counts vs physical motion → response removal
- Internal: SNR after filter with fixed noise window
- External: California CI ≠ European networks → EIDA/ORFEUS pilot
- Statistical: **N=8** → larger catalogues, bootstrap CIs
- Selection: first-eight downloads → stratified sampling
- Confirmation: fixed STA/LTA **2.5** → threshold sweeps

**Figure:** None (optional: **Table 9** from report)  

**Speaker notes:** Table 9 pairs each threat with proposed mitigation. Present mitigations as future work, not completed tasks. This slide bridges limitations to European transfer.

---

## Slide 23 — European relevance and transfer

**Title:** European context — why California supports EU goals  

**Bullets:**
- **Primary programme focus:** Europe; California validates **methods**
- Demonstrates ObsPy/FDSN reproducibility for graduate research
- Surfaces pitfalls: origin windows, response metadata, station bias
- **Proposed transfer:** manifest + reports + scripts with EU endpoints
- **ORFEUS/EIDA** intended data plane; **no EU data yet**
- Challenges: access policies, event rates, station density, regulations

**Figure:** None  

**Speaker notes:** Section 11 lists benefits and challenges from the report. Do not imply European deployment or cross-region feature comparisons were executed. GDPR note applies to future integrations per appendix C themes in D-F1.

---

## Slide 24 — Future work, conclusion, acknowledgements, references

**Title:** Future work, conclusions, and closing  

**Bullets:**
- **Future:** 50–200+ events; EU pilot; response fix; 3-component; AI baselines; SeedLink; publication
- **Conclusion:** Reproducible chain to **8×18** features established
- Response failure blocks physical amplitude EEW today
- Europe = intended scaled context
- **Acknowledgements:** USGS & EarthScope FDSN data; ObsPy (Krischer et al., 2015)
- **Key refs:** Allen & Kanamori 2003; Hoshiba et al. 2008; Joshi et al. 2026 (reference only)

**Figure:** None  

**Speaker notes:** Conclusions are the six numbered points from report section 13, compressed into the narrative above. Acknowledgements are limited to data/software providers named in D-F1 §14 and Appendix C— the report does not list personal supervisors. End with Q&A; full bibliography is report §14.

---

## Appendix to outline — timing guide (10–15 min)

| Block | Slides | ~Minutes |
|-------|--------|----------|
| Intro, gap, objectives | 1–5 | 2–3 |
| Literature & dataset | 6–9 | 2–3 |
| Workflow & methods | 10–12 | 2 |
| Results (EDA → features) | 13–19 | 4–5 |
| Discussion, limits, Europe, close | 20–24 | 2–3 |

---

## Appendix to outline — figure index (all repository PNGs)

| Report figure | File | Slide |
|---------------|------|-------|
| 1 | `figures/example_waveform_raw.png` | 13 |
| 2 | `figures/magnitude_histogram.png` | 14 |
| 3 | `figures/events_over_time.png` | 14 |
| 4 | `figures/station_usage_frequency.png` | 14 (optional 20) |
| 5 | `figures/signal_analysis_ci40675215.png` | 15 |
| 6 | `figures/signal_analysis_ci40699207.png` | 16 |
| 7 | `figures/preprocessing_ci40675215.png` | 17 |
| 8 | `figures/preprocessing_ci40699207.png` | 17 |
| 9 | `figures/feature_engineering_fft_spectra.png` | 18 |
| 10 | `figures/feature_correlation_heatmap.png` | 18 |
| 11 | `figures/feature_distributions.png` | 19 |
| 12 | `figures/feature_boxplots_by_station.png` | 19 |
| D1–D12 | Other `signal_analysis_*.png`, `preprocessing_*.png` | Backup / optional deep-dive (not on core 24) |

---

**Document control:** Presentation outline D-F2 v1.0 — derived only from `reports/Research_Report_Final.md`, 29 July 2026. No source code modified.
