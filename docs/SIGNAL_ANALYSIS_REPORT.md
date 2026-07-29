# SIGNAL_ANALYSIS_REPORT.md

**Phase A.2 — Waveform signal analysis**  
California IRIS / EarthScope pilot (manifest waveforms only)

| Field | Value |
|-------|--------|
| Report date (UTC) | 2026-07-29 |
| Script | `scripts/analysis/run_california_signal_analysis.py` |
| Manifest | `data/manifests/iris_california_pilot_events.csv` |
| Prior EDA | [EDA_REPORT.md](EDA_REPORT.md) |
| Data context | [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) |

Re-run:

```powershell
python scripts/analysis/run_california_signal_analysis.py
```

---

## 1. Scope and methods

All **8** manifest-linked **BHZ** MiniSEED files were analysed independently. Processing uses **ObsPy** only in this script (no EarthESND `src/` pipeline changes).

### 1.1 Amplitude metrics

| Metric | Definition |
|--------|------------|
| **Peak amplitude** | max \|counts\| over the full 300 s trace |
| **RMS amplitude** | RMS over the full trace |
| **RMS (signal window)** | RMS from estimated **P onset** to trace end |
| **Noise level** | RMS in a noise window (see below) |
| **SNR (peak)** | peak / noise RMS |
| **SNR (RMS)** | signal-window RMS / noise RMS |
| **Signal duration** | Time from P pick until the last sample with \|x(t)\| ≥ 3× noise RMS |

### 1.2 Noise window (pilot limitation)

FDSN downloads start at **catalog origin time**, so there is **no true pre-event quiet period** in the files. Noise is estimated from:

- **Preferred:** 0 s to min(5 s, P_pick − 0.5 s) when the pick is late enough (`samples_before_sta_lta_pick`), or  
- **Fallback:** first ~1–5 s (`initial_segment_proxy_no_pre_event_data`).

All eight events used the **first 5 s** window (`0–5 s`) because P picks occur after 10 s. Early seconds may still contain **ambient noise plus precursory energy**; SNR for some records is therefore **optimistic or unstable** (see §5).

### 1.3 P-wave onset (STA/LTA)

- **Algorithm:** ObsPy `classic_sta_lta` + `trigger_onset`  
- **STA window:** 0.5 s (20 samples at 40 Hz)  
- **LTA window:** 10 s (400 samples)  
- **Threshold:** 2.5 (literature-aligned; **not** wired to EarthESND YAML)  
- **Pick:** first trigger onset sample; vertical dashed red line on figures  

Picks are **approximate onsite triggers** for EEW-style exploration, not reviewed seismological phase picks.

---

## 2. Aggregate summary statistics

| Quantity | Value |
|----------|--------|
| Waveforms analysed | **8** |
| Stations | **CI.ADO** (6), **CI.USC** (2) |
| Sampling rate | **40 Hz** |
| Trace length | **300 s** each |
| Magnitude range | **4.05 – 4.87** |
| Peak amplitude (counts) | min **17 408**, max **3 486 065**, mean **680 591** |
| SNR (peak) | min **6.3**, max **778**, mean **137**, median **49.9** |
| P pick time (s from trace start) | min **10.15**, max **55.15**, mean **31.3** |
| Signal duration (s) | min **0**, max **289.5**, mean **183.2** |

Machine-readable: `reports/signal_analysis/signal_analysis_summary.json`.

---

## 3. Waveform characteristics

- **Single vertical component (BHZ)** at **40 Hz**; amplitudes are in **raw digitizer counts** (no response removal).
- **Dynamic range** varies by orders of magnitude: moderate events at **ADO** (peaks ~10⁴–10⁵ counts) vs very large peaks at **USC** and the **M 4.87** **ADO** record (~10⁶–10⁷ counts), reflecting **path, magnitude, and site gain** differences rather than a homogeneous scaling.
- **Full-trace RMS** is dominated by energetic portions of the record; **post-P RMS** is lower when P arrives late and coda is weaker.
- **Normalized waveforms** (÷ peak) in the figures allow shape comparison without unit calibration.

---

## 4. P-wave observations

| Event (short id) | Station | M | P pick (s) | SNR (peak) |
|------------------|---------|---|------------|------------|
| ci40675215 | CI.ADO | 4.87 | 12.55 | 778 |
| ci40964384 | CI.ADO | 4.54 | 10.15 | 86 |
| ci40735352 | CI.USC | 4.11 | 12.05 | 78 |
| ci40964128 | CI.ADO | 4.72 | 38.40 | 97 |
| ci40964048 | CI.ADO | 4.16 | 38.95 | 20 |
| ci40593503 | CI.ADO | 4.05 | 35.63 | 22 |
| nn00882322 | CI.ADO | 4.39 | 47.50 | 8.7 |
| ci40699207 | CI.USC | 4.39 | 55.15 | 6.3 |

**Patterns:**

- **Early picks (~10–13 s)** on the strongest or nearer-path examples (e.g. M 4.87 at ADO, M 4.11 at USC).
- **Late picks (35–55 s)** on several ADO/USC records — consistent with **larger source–receiver distance** or **weaker first arrivals** on BHZ before STA/LTA triggers on later phases/coda.
- STA/LTA **characteristic functions** show clear threshold crossings on most traces; late triggers often coincide with **stronger later energy** rather than the true first P.

---

## 5. Station-to-station differences

| Station | Events | Mean P pick (s) | Mean peak (counts) | Mean SNR (peak) |
|---------|--------|-----------------|--------------------|-----------------|
| **CI.ADO.--.BHZ** | 6 | 30.5 | 297 982 | 169 |
| **CI.USC.--.BHZ** | 2 | 33.6 | 1 828 417 | 42 |

- **USC** shows **higher peak counts** on average but **lower mean SNR (peak)** because the fixed **0–5 s noise window** can include **high-amplitude early energy** (e.g. **ci40699207**), inflating noise RMS and yielding **SNR ≈ 6** and **signal duration 0 s**.
- **ADO** dominates the pilot (**6/8** events) due to download station ranking, not uniform network sampling.
- Without **distance metadata** per trace in the manifest, epicentral distance cannot be tabulated here; latitude/longitude in the event table support future distance–pick studies.

---

## 6. Figures

Each event has a **four-panel** figure (300 DPI PNG) in `reports/figures/`:

| File | Panels |
|------|--------|
| `signal_analysis_ci40964384.png` | Raw, normalized, STA/LTA, raw + P marker |
| `signal_analysis_ci40964128.png` | same |
| `signal_analysis_ci40964048.png` | same |
| `signal_analysis_nn00882322.png` | same |
| `signal_analysis_ci40699207.png` | same |
| `signal_analysis_ci40675215.png` | same |
| `signal_analysis_ci40593503.png` | same |
| `signal_analysis_ci40735352.png` | same |

**How to read each panel:**

1. **Raw waveform** — counts vs time from trace start (origin-aligned FDSN window).  
2. **Normalized waveform** — divided by peak amplitude; compares shape.  
3. **STA/LTA** — ObsPy characteristic function; horizontal dotted line at threshold **2.5**.  
4. **P marker** — raw trace with vertical line and dot at the **estimated P onset**.

---

## 7. Tables and per-event JSON

| Output | Description |
|--------|-------------|
| `reports/tables/signal_analysis_per_event.csv` | One row per event: all metrics + pick metadata |
| `reports/signal_analysis/<short_id>_metrics.json` | Per-event machine-readable metrics (8 files) |
| `reports/signal_analysis/signal_analysis_summary.json` | Cohort aggregates |
| `reports/signal_analysis/run_metadata.json` | Figure and table index |

---

## 8. Pilot dataset limitations

1. **Origin-aligned windows** — no pre-event noise; SNR uses a **proxy** noise segment.  
2. **Single component (BHZ)** — no horizontal energy or polarization.  
3. **No instrument response** — counts are not ground motion in gal/cm/s².  
4. **STA/LTA parameters fixed** — not tuned per station; picks are **not** validated against a reference catalog.  
5. **Small N = 8**, **2 stations**, magnitude band **M 4–5** — not representative of full California seismicity.  
6. **Station selection bias** — distance-ranked candidate list from the download script.  

---

## 9. Relevance to future EEW research

This phase demonstrates a **reproducible onsite analysis chain** suitable for the certificate programme and later **European** data:

1. **Triggering** — STA/LTA on streaming-style windows is the same class of algorithm used in EEW **P detection** (Phase B will add filtering and tuning).  
2. **SNR and duration** — quantify **data quality** before ML (EarthESND-inspired or other models on Western datasets).  
3. **Station effects** — peak/SNR spread motivates **per-station calibration**, **3-component** data, and **pre-event buffers** in future acquisitions.  
4. **Proposal content** — figures and tables support **Methodology** (signal processing) and **Expected outcomes** (automated pick latency, quality gates).  
5. **Next steps (Phase B)** — band-pass filtering, detrending, optional **pre-origin download** (−30 s) for honest noise estimates, and comparison with catalog **travel-time** predictions.

---

## 10. Output index

| Path | Type |
|------|------|
| `docs/SIGNAL_ANALYSIS_REPORT.md` | This report |
| `reports/signal_analysis/*.json` | Metrics + summary |
| `reports/figures/signal_analysis_*.png` | 8 figure sets |
| `reports/tables/signal_analysis_per_event.csv` | Summary table |

---

Version: **1.0.0** (Phase A.2)
