# D-F3 — Presentation script

**Deliverable:** Oral presentation script (10–15 minutes)  
**Sources:** `reports/Research_Report_Final.md` · `reports/Presentation_Outline_D-F2.md`  
**Date:** 29 July 2026  
**Total estimated duration:** ~**14 minutes 8 seconds** (848 s) — adjustable by pacing results slides ±30 s

**Usage:** Read naturally; `[Figure: …]` marks where to advance to the slide visual.

---

## Slide 1 — Title  
**Estimated time: 0:30**

Good morning. Thank you for being here. My presentation is titled *Reproducible AI-Assisted Earthquake Early Warning Research for Western Seismic Regions*, with the subtitle *Method Development on a California FDSN Pilot with Transfer Path to European Networks*.

This talk summarises **AMGCR Earthquake Research** and the final research proposal and technical report—Deliverable D-F1—completed on **29 July 2026**, within the Swiss certificate programme in Assessment and Management of Geological and Climate Related Risk.

Everything I will describe comes from the completed pilot documented in that report and from repository artefacts frozen on **2026-07-29**. I am not presenting new computations today.

**Transition:** I will begin with why earthquake early warning and open methods matter for this programme, before clarifying how Europe and California fit together.

---

## Slide 2 — Introduction: motivation  
**Estimated time: 0:35**

Earthquake early warning aims to deliver alerts in the **seconds to tens of seconds** before destructive shaking arrives at a site. Operational systems rely on **P-wave detection**, **rapid magnitude estimation**, and **ground-motion prediction**.

In Europe and neighbouring regions—including the Mediterranean belt, the Alps, and areas with anthropogenic seismicity—this capability matters for civil protection. In Switzerland and more broadly in the EU, stakeholders increasingly expect **documented, open methodologies**, not opaque prototypes.

That expectation is the motivation for a certificate project that emphasises reproducible data handling, explicit processing steps, and honest limitation statements.

**Transition:** The same report makes clear that the programme’s geographic ambition and the pilot geography are not the same thing. That distinction is on the next slide.

---

## Slide 3 — Programme positioning  
**Estimated time: 0:35**

The **primary long-term target** of this research programme is **European seismic networks**. The **California IRIS and EarthScope pilot** is a **completed methods laboratory**—a place to validate workflow, scripts, and reporting—not the intended final deployment region.

The project began with an **EarthESND** reference implementation. That codebase is **complete** as a benchmark—the report cites **88 passing tests** on a full checkout—but it is **reference only** for this certificate narrative, not the scientific endpoint.

The completed active work uses **real waveforms**, theory, figures, tables, and formal reporting. All pilot science in this presentation reflects the freeze date **2026-07-29**.

**Transition:** Given that framing, it is worth stating briefly which gaps the workflow was designed to address.

---

## Slide 4 — Research gap  
**Estimated time: 0:30**

The report identifies four gap themes.

First, many state-of-the-art ML papers are demonstrated on region-specific archives, while **packaged, documented EEW workflows for European FDSN data** are less common at certificate level.

Second, studies often publish metrics without a full artifact trail from **raw MiniSEED** to **ML-ready feature matrices**.

Third, teams can conflate **implementing benchmark code** with completing **region-relevant science**; this project **decouples** EarthESND software from the Western pilot analysis.

Fourth, a small-**N** pilot can illustrate methodology but **cannot** support operational EEW claims; that distance remains explicit.

**Transition:** The objectives slide maps what was actually completed versus what remains proposed.

---

## Slide 5 — Objectives  
**Estimated time: 0:40**

The **primary objective** is a **reproducible, AI-ready EEW research workflow** aimed ultimately at **European networks**, documented for a Swiss and European research audience.

The **secondary objective**—the California pilot—is **completed**: acquisition through interpretation.

Objectives **O1 through O6** are **completed**: FDSN download, exploratory characterisation, onsite-style signal metrics and STA/LTA analysis, preprocessing toward ML inputs, an **8×18** feature matrix, and scientific interpretation including the European transfer narrative.

Objective **O4** is completed but with an important documented caveat: **instrument response removal was not applied—zero of eight traces** in the pilot run.

Objectives **O7 through O9**—European scale-up, AI training, and real-time prototyping—are **proposed**, not results of this pilot. Objective **O10**, the written proposal and report, is **completed**; D-F1 supersedes version one.

**Transition:** Before the dataset and pipeline, I will anchor the work in the literature the report cites.

---

## Slide 6 — Literature: EEW fundamentals  
**Estimated time: 0:30**

Classical onsite EEW uses triggers such as **STA/LTA** to estimate P-wave onset, then derives alert information from early windows of motion, as discussed by **Allen and Kanamori (2003)** and **Hoshiba et al. (2008)**.

Design trade-offs include **detection latency**, **false alarm rate**, and **magnitude saturation** for very large events.

European deployments additionally stress **standardised metadata**, **latency budgets**, and **uncertainty communication** to end users.

Our pilot signal phase uses ObsPy’s **classic STA/LTA** with documented parameters—it is exploratory, not operational network tuning.

**Transition:** The data and software layer that implements this pilot sits alongside ML literature and reproducibility practice.

---

## Slide 7 — Literature: data, software, and ML context  
**Estimated time: 0:35**

**ObsPy** (Krischer et al., 2015) is the integration layer for MiniSEED, FDSN services, and processing in this repository.

For the California pilot, **USGS** supplies event metadata and **EarthScope** supplies waveforms—the same FDSN abstraction the report intends for **ORFEUS and EIDA** later.

Machine learning and reservoir approaches can learn from early waveform segments, but they require **large, diverse datasets** and careful **instrument response** handling.

**EarthESND**—multiscale ESN with dendritic readout—is cited in a **Japan K-NET** context. Here it exists as **reference pipeline code** in `src/`; the California pilot **did not** use those modules for the published results.

Reproducibility is institutionalised through **manifests**, **JSON configs**, and **phase reports**.

**Transition:** With that background, I turn to the concrete dataset the pilot analysed.

---

## Slide 8 — California pilot dataset  
**Estimated time: 0:35**

The completed pilot comprises **eight** earthquakes with magnitudes from **4.05 to 4.87**, mixing **`mw` and `ml`**, with origin times between **May and October 2024**.

Each retained event has one **BHZ** trace at **40 hertz**, in a **300-second** window starting at **catalog origin time**.

Stations in the manifest are **CI.ADO** for six events and **CI.USC** for two. The authoritative list is the CSV manifest under `data/manifests/`.

Exploratory inspection at one stage found **twelve** MiniSEED files on disk, including **four legacy** files outside the current manifest. **All completed analyses use the eight manifest-linked records only.**

**No European waveforms** are included in the completed pilot.

**Transition:** The next slide summarises how those eight records were selected from FDSN services.

---

## Slide 9 — FDSN acquisition parameters  
**Estimated time: 0:30**

Events were queried from **USGS** over a **2024** California bounding box with magnitude **4.0 to 7.5**, yielding **41** catalog matches before waveform filtering.

Waveforms were requested from **EarthScope** for candidate networks **CI, NC, and BK**, primarily **BHZ**, with **one successful trace per event**.

The pilot retained **eight** events with non-empty waveforms. Station choice follows a **fixed distance-ranked candidate list**, which is **not** uniform network sampling.

Access was **public FDSN**; **no credentials** were required. The download script is `scripts/download/download_iris_california_pilot.py`.

**Transition:** Having described the inputs, I will walk through the end-to-end workflow those scripts and analysis phases implement.

---

## Slide 10 — End-to-end workflow  
**Estimated time: 0:38**

The **completed** chain runs: **download**, then **Phase A.1 EDA**, **Phase A.2 signal analysis**, **Phase B.1 preprocessing**, **Phase B.2 feature engineering**, and **Phase C interpretation**.

Deliverables also include reproducibility and data availability statements—D-S1 and D-S2—and this **D-F1 final report**.

Outputs live under `reports/`—including `eda`, `signal_analysis`, `preprocessing`, `features`, and **figures**.

Critically, the **EarthESND modules in `src/` were not used** to produce these USA pilot results.

**Proposed** extensions—European FDSN acquisition, larger **N**, ML training, and **SeedLink**-style real-time work—are labelled as such in the report. Reproduction commands are in **Appendix B** of D-F1.

**Transition:** I will now split methods across two slides: first EDA and signal analysis, then preprocessing and features.

---

## Slide 11 — Methodology: EDA and signal analysis  
**Estimated time: 0:32**

**Phase A.1** reads MiniSEED under `data/raw/iris/`, inspects files with ObsPy, and summarises **manifest-only** cohort statistics. It produces four exploratory figures.

**Phase A.2** computes peak and RMS amplitudes, estimates noise from a **zero-to-five-second proxy window**, and reports peak SNR. It applies **STA/LTA** with **0.5-second STA**, **10-second LTA**, and threshold **2.5**, yielding a P pick and a signal-duration proxy.

Because downloads start at **origin time**, there is **no true pre-event quiet period**—a limitation that carries through to SNR interpretation.

Scripts: `run_california_pilot_eda.py` and `run_california_signal_analysis.py`.

**Transition:** Preprocessing and feature extraction build directly on those signal metrics and filtered-stage arrays.

---

## Slide 12 — Methodology: preprocessing and features  
**Estimated time: 0:32**

**Phase B.1** applies demean, linear detrend, a **five-percent Hann taper**, and a **0.1 to 15 hertz** zero-phase band-pass. It attempts instrument response removal via EarthScope; in the completed run, response was **skipped for all eight traces**, so filtered data remain in **counts**. Stages are stored in NPZ files, with peak normalisation as the final step.

**Phase B.2** extracts **eighteen features** from **filtered** traces, using P arrival times from Phase A.2. There are **nine** time-domain, **five** frequency-domain, and **four** earthquake-related features; FFT spectra are visualised but not stored as matrix columns.

PGM and Arias entries in the matrix are **counts-based proxies**, not physical PGA or standard Arias intensity.

**Transition:** With methods established, the next seven slides present results, beginning with exploratory views of the raw data.

---

## Slide 13 — Results: EDA (example waveform)  
**Estimated time: 0:38**

**[Figure: `figures/example_waveform_raw.png` — Report Figure 1]**

This panel shows the **highest magnitude** event in the manifest—**M 4.87** at **CI.ADO**—in **raw digital counts** over the full **300-second** window.

The cohort occupies a narrow **M 4 to 5** band, which reflects **query cutoffs**, not completeness of regional seismicity.

Strong motion is visible without correction, but the long window also shows baseline behaviour and coda; amplitudes are **not** ground motion in physical units.

This figure connects the abstract dataset table to what the signal and preprocessing stages actually receive.

**Transition:** The following slide summarises catalog-level views: magnitude distribution, timing, and station usage.

---

## Slide 14 — Results: EDA (catalog views)  
**Estimated time: 0:38**

**[Figures: `figures/magnitude_histogram.png`, `figures/events_over_time.png`, `figures/station_usage_frequency.png` — Figures 2–4]**

The magnitude histogram confirms the **small-sample** M 4–5 pilot band. The events-over-time plot shows clustering in **May**, **July through August**, and **late October 2024**; gaps reflect **download success**, not designed uniform sampling.

Station usage is heavily skewed: **ADO supplies six of eight** traces because of the acquisition script’s distance-ranked list. That **structural bias** reappears in later feature comparisons.

Again, only **manifest-linked** files enter these summaries.

**Transition:** From catalogue statistics we move to waveform-level onsite metrics and STA/LTA behaviour.

---

## Slide 15 — Results: signal analysis (high-SNR case)  
**Estimated time: 0:42**

**[Figure: `figures/signal_analysis_ci40675215.png` — Report Figure 5]**

Across eight events, peak raw counts span roughly **1.7×10⁴ to 3.5×10⁶**. P picks range from **10.15 to 55.15 seconds** after trace start, with mean **31.3 seconds**. Peak SNR runs from **6.3 to 778**, median **49.9**.

Event **ci40675215**—magnitude **4.87**—is the favourable case: early pick near **10.2 seconds** and high SNR. The four-panel figure shows raw and normalised traces, the STA/LTA curve crossing threshold **2.5**, and the pick marker.

This is the kind of record where onsite triggering aligns intuitively with warning-time discussions—subject to the noise-window caveat.

**Transition:** Not every record behaves that way; the USC example on the next slide illustrates the limitation.

---

## Slide 16 — Results: signal analysis (low-SNR / USC)  
**Estimated time: 0:38**

**[Figure: `figures/signal_analysis_ci40699207.png` — Report Figure 6]**

At station level, **CI.ADO**—six events—shows mean peak SNR **169** and mean peak about **2.98×10⁵ counts**. **CI.USC**—two events—shows mean SNR **42** but higher mean peaks, about **1.83×10⁶ counts**.

Event **ci40699207** at USC has SNR near **six** and **zero seconds** signal duration by the post-P proxy—consistent with a **contaminated noise window** when the trace starts at origin.

The report treats SNR here as a **quality indicator**, not a calibrated detection probability.

**Transition:** Preprocessing next shows whether band-limited processing stabilises these traces for comparison and for feature extraction.

---

## Slide 17 — Results: preprocessing  
**Estimated time: 0:38**

**[Figures: `figures/preprocessing_ci40675215.png`, `figures/preprocessing_ci40699207.png` — Figures 7–8]**

Aggregate mean peak-SNR rises from **137** on raw traces to **1684** after filtering, before normalisation. Per-event filtered-to-raw ratios range **2.5 to 27.6**, mean **17.1**.

The four-panel layouts show **raw, detrended, filtered, and normalised** stages for the same two events we just discussed.

Visually, preprocessing **stabilises** traces for ML-oriented comparison. Scientifically, without response correction, filtered **counts** still cannot be read as velocity or acceleration for magnitude estimation.

**Transition:** The feature engineering results compress each trace into an eighteen-dimensional vector and summarise cohort behaviour.

---

## Slide 18 — Results: feature engineering (spectra and correlations)  
**Estimated time: 0:38**

**[Figures: `figures/feature_engineering_fft_spectra.png`, `figures/feature_correlation_heatmap.png` — Figures 9–10]**

The primary artefact is an **8×18** matrix in `reports/features/feature_matrix.csv`. Cohort mean **crest factor** is approximately **11.4**; dominant frequency and spectral centroid cluster near **2.3 to 2.6 hertz**, consistent with the **0.1–15 hertz** band-pass.

The correlation heatmap shows **strong collinearity** among amplitude-derived features. The report highlights **crest factor**, **signal and spectral entropy**, and **zero-crossing rate** as partially complementary shape information.

At **N equals eight**, these views are **illustrative only**. The completed pilot includes **no ML training** and **no predictive performance metrics**.

**Transition:** Distributions and station boxplots close the results section before interpretation.

---

## Slide 19 — Results: feature distributions and stations  
**Estimated time: 0:35**

**[Figures: `figures/feature_distributions.png`, `figures/feature_boxplots_by_station.png` — Figures 11–12]**

Per-feature histograms act as **pilot dashboards**, not density estimates. Amplitude-related features show **large spread**, driven by station gain and path effects in counts.

Boxplots compare **ADO** and **USC** for selected features; **USC** drives upper tails on peak, RMS, and PGM proxies, while counts are **unbalanced—six versus two events**.

PGM and Arias columns remain **counts proxies** only. Feature extraction is **complete**; model training is **proposed** under objective O8.

**Transition:** I will now step back from individual figures to discuss what the integrated pipeline achieves—and what it does not claim.

---

## Slide 20 — Discussion  
**Estimated time: 0:35**

The pilot demonstrates a **script-driven, documented path** from FDSN services to **tabular features** and **normalised NPZ stages**, matching certificate expectations for ObsPy, real data, graphs, and tables.

STA/LTA panels connect EEW theory to **P-time features**, but **late picks** and **origin-aligned noise** mean trigger parameters cannot be responsibly tuned on this dataset alone.

The feature matrix supports **exploratory baselines** in principle—linear models or random forests—but the report is explicit: **no ML training or hold-out evaluation** was performed.

**EarthESND** remains available for **future** Western-data comparison with a **deviation log** from Japan-centric paper metrics; it was **not validated** on California in completed work.

**Transition:** The report separates enumerated pilot limitations from formal threats to validity; I treat those on the next two slides.

---

## Slide 21 — Limitations  
**Estimated time: 0:32**

Key limitations include **eight events** and a **single BHZ component**; **origin-aligned windows** that bias noise and SNR; **zero of eight** successful response removals; **station selection bias** toward ADO with only **two** USC records; **mixed magnitude types**; and **unvalidated P picks**.

Results are **not comparable** to EarthESND **K-NET** paper metrics. Four **legacy MiniSEED** files may exist on disk outside the manifest—the report warns they must not enter summaries without reconciliation.

These points are preconditions for any European operational narrative.

**Transition:** Threats to validity pair each issue with mitigations planned—not yet executed.

---

## Slide 22 — Threats to validity  
**Estimated time: 0:32**

**Construct validity:** using counts where physical motion is required—mitigation: cache StationXML and remove response.

**Internal validity:** SNR inflation after filtering with a fixed early window—mitigation: pre-origin download windows.

**External validity:** California CI networks differ from European networks—mitigation: rerun the same scripts on an **EIDA/ORFEUS** pilot.

**Statistical conclusion validity:** **N equals eight**—mitigation: larger catalogues and bootstrap confidence intervals.

**Selection bias** from the first eight successful downloads and **confirmation bias** from a fixed STA/LTA threshold are documented with mitigations such as stratified sampling and threshold sweeps.

All mitigations are **proposed future work**.

**Transition:** That leads naturally to why a California pilot still supports a Europe-forward programme—and what transfer would look like.

---

## Slide 23 — European relevance and transfer  
**Estimated time: 0:35**

**Europe is the primary programme focus**; California validates **methods**, not final deployment geography.

The pilot demonstrates **ObsPy and FDSN reproducibility** and surfaces pitfalls—origin-aligned windows, response metadata, station bias—that also arise when integrating **ORFEUS and EIDA** data.

The **proposed transfer plan** reuses manifest structure, phase report templates, and the script layout with **European endpoint configuration**, documenting licensing, magnitude conventions, and channel choices per network.

**No European waveform dataset** is included yet. Expected challenges include fragmented access policies, lower event rates in some regions, heterogeneous station density, accelerometer versus broadband choices, and regulatory metadata requirements noted in the report.

**Transition:** I will close with planned extensions, conclusions, acknowledgements, and an invitation for questions.

---

## Slide 24 — Future work, conclusion, acknowledgements, references  
**Estimated time: 0:45**

**Proposed future work** includes expanding to **fifty to two hundred or more** events with stratified splits; a **European FDSN pilot**; fixing **instrument response** and adding **three-component** data and **pre-event noise windows**; **AI baselines** and EarthESND-inspired comparisons with a deviation log; **SeedLink** simulation for real-time latency; and formal publication of European transfer with uncertainty quantification.

**Conclusions from the report:** a **reproducible chain** to an **8×18 feature matrix** is **established**; raw waveforms show strong **station and path effects** and heterogeneous STA/LTA picks; preprocessing improves interpretability and SNR proxies but **response removal failed for all eight traces**, so **physical amplitude EEW is not yet supported**; features highlight redundancy among amplitudes and value in shape statistics at pilot scale; validity threats must be addressed before operational claims; **California proves the method—Europe is the intended scaled context**.

**Acknowledgements:** public data from **USGS** and **EarthScope** via FDSN, and the **ObsPy** project (Krischer et al., 2015). Key references include Allen and Kanamori (2003), Hoshiba et al. (2008), and Joshi et al. (2026) for EarthESND as **reference only**. The full bibliography is in D-F1 section fourteen.

Thank you. I welcome your questions.

---

## Timing summary

| Slides | Block | Est. duration |
|--------|--------|----------------|
| 1–5 | Intro, gap, objectives | 2:50 |
| 6–9 | Literature and dataset | 2:10 |
| 10–12 | Workflow and methods | 1:42 |
| 13–19 | Results | 4:29 |
| 20–24 | Discussion, limits, Europe, close | 2:57 |
| **Total** | **24 slides** | **~14:08** |

*To target **10 minutes**, shorten slides 13–19 by ~30%; to target **15 minutes**, expand results narration on Figures 5–12 by ~20%.*

---

## Q&A preparation — ten likely examiner questions

*Answers based solely on `reports/Research_Report_Final.md`.*

**1. Why use California data if the programme focus is Europe?**  
California provides a **completed FDSN methods laboratory** with mature USGS and EarthScope services and ObsPy practice. The report states Europe is the **primary long-term focus**; California validates **methods**, not deployment geography.

**2. How many earthquakes and stations did you analyse?**  
**Eight** manifest-linked events, magnitudes **4.05–4.87**, each with one **BHZ** trace. Stations are **CI.ADO** (six events) and **CI.USC** (two events).

**3. Did you train a machine learning model for magnitude prediction?**  
**No.** The completed pilot produces an **8×18 feature matrix** and normalized NPZ stages. The report states **no ML training or hold-out evaluation** and **no predictive performance metrics** in repository artefacts.

**4. What is EarthESND’s role in your results?**  
EarthESND is a **complete reference implementation** (**88 tests** on a full checkout) for **future comparative** studies. California pilot results **did not use** EarthESND `src/` modules; K-NET scientific reproduction is **not started**.

**5. Why were instrument responses not applied?**  
Preprocessing **attempted** response removal for all eight traces; **zero of eight** were applied in the completed run, and filtered traces remain in **counts**. The report documents this in preprocessing section 6.4 and limitations.

**6. How reliable are your P-wave picks and SNR values?**  
P picks come from **STA/LTA** (0.5 s / 10 s, threshold **2.5**) and are **not analyst-validated**. Noise is estimated from the **first five seconds** of **origin-aligned** traces, so SNR is a **QC indicator**, not operational detection probability—especially for late picks and USC records such as **ci40699207**.

**7. What does the preprocessing SNR increase from 137 to 1684 mean operationally?**  
The report interprets this as **processing sensitivity** with a **fixed early noise window**, **not** guaranteed operational EEW gain. Without response correction, filtered counts are still not physical ground motion.

**8. Can you generalise feature correlations or station comparisons?**  
**Not statistically.** At **N=8**, distributions and correlations are **illustrative**. USC has **n=2**; ADO dominance reflects **acquisition policy**, not network-wide behaviour.

**9. How would another researcher reproduce your work?**  
Appendix B of D-F1 and D-S1 document commands: download script, then four analysis scripts, from repository root with Python **≥3.11** and dependencies in `pyproject.toml`. Raw MiniSEED, logs, and PNG figures may be **gitignored** and must be **regenerated** or supplied separately per the audit and Appendix C.

**10. What are the next concrete steps toward a European pilot?**  
**Proposed:** mirror the manifest and report pattern for **EIDA/ORFEUS**, configure European FDSN endpoints in the same script layout, document authentication and channel conventions, and rerun Phases A–B before any ML work—addressing response removal, pre-origin windows, and larger **N** as listed in future work (section 12.2).

---

**Document control:** Presentation script D-F3 v1.0 — AMGCR Earthquake Research, 29 July 2026. Derived only from D-F1 and D-F2. No source code modified.
