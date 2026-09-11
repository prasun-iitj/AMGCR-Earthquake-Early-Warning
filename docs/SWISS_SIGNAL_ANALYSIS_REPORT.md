# Swiss Pilot Signal Analysis

**Swiss seismic-data acquisition — methods-transfer signal analysis**  
**Not** an operational EEW system, **not** validated Swiss EEW, **not** a European EEW model, and **not** a machine-learning study.

Automatic STA/LTA times in this document are **triggers**, not manually validated P arrivals.

| Field | Value |
|-------|--------|
| Analysis date (UTC) | 2026-09-06 |
| Script | `scripts/analysis/run_swiss_signal_analysis.py` |
| Configuration | `configs/swiss_signal_analysis.yaml` |
| Manifest (source of truth) | `data/manifests/sed_switzerland_pilot_events.csv` |
| Raw MiniSEED | `data/raw/switzerland/` (**not modified**) |
| StationXML | `data/metadata/switzerland/` |
| Outputs | `reports/swiss_signal_analysis/` |
| California v1.0.0 | **Unchanged** (frozen) |

Re-run:

```powershell
python scripts/analysis/run_swiss_signal_analysis.py
```

---

## 1. Purpose

Analyse the already-acquired Swiss pilot MiniSEED (20 events, 120 CH event–station records) with a pipeline that is **separate** from `scripts/analysis/run_california_*.py`.

The Swiss data allow steps the California pilot could not complete: true pre-event noise, HH 3-component records, local StationXML, and instrument-response correction to physical units.

This is a **methods-transfer** comparison with California v1.0.0, not a controlled performance experiment.

---

## 2. Processing chain (as executed)

For every manifest row:

1. Read MiniSEED with ObsPy; merge same-id traces only if split (`method=0`, no gap filling).
2. Require HHZ, HHN, HHE at a common sampling rate and a common overlapping interval.
3. Demean, linear detrend, Hann taper (5%).
4. `remove_response(inventory=StationXML, output=VEL, water_level=60)` with a **Nyquist-aware** `pre_filt` (not the California 40 Hz corners 20–25 Hz).
5. Zero-phase band-pass **0.1–15 Hz**, 4 corners (amplitude / SNR / PGV).
6. Band-limited PGA: time derivative of that velocity (same passband).
7. Causal (non-zero-phase) copy of the same band-pass for STA/LTA only.

Raw files are never overwritten. Derived numbers live under `reports/swiss_signal_analysis/`.

---

## 3. Window definitions

Offsets are relative to the SED catalogue origin.

| Window | Interval | Role |
|--------|----------|------|
| Noise | origin − 60 s to origin − 10 s | SNR denominator (true pre-event; **not** the first 5 s of an origin-aligned trace) |
| Event / amplitude | origin to origin + 180 s | Peak, RMS, SNR numerator, PGV/PGA. 180 s is long enough that S at the farthest selected station (~162 km) remains inside the window |
| Expected P-class window | origin to origin + 90 s | Labels whether a search-window trigger is a plausible first-arrival candidate |
| STA/LTA search | origin − 5 s to origin + 90 s | **Official** automatic trigger |

STA/LTA 0.5 s / 10 s / threshold 2.5 matches the California baseline **parameters**, but not California’s search rule. California used the first onset on an origin-aligned raw BHZ trace. On Swiss traces that start ~90 s before origin, the first-on-trace onset is dominated by taper/filter startup. That first-on-trace time is stored as a diagnostic (`trigger_latency_unmasked_s`, `trigger_latency_first_after_mute_s`); it is **not** the official trigger.

---

## 4. Filter choice (not copied blindly)

California B.1 used 0.1–15 Hz on **40 Hz BHZ** (Nyquist 20 Hz). Swiss HH is **120 or 200 Hz** (Nyquist 60 or 100 Hz), so 15 Hz is **not** a sampling constraint.

The same 0.1–15 Hz passband is used so amplitude and SNR are a methods-transfer comparison, not a new EEW decision band. Regional M ~3–4.7 body-wave energy is typically below ~20 Hz; a higher Swiss-only `fmax` remains possible later and was **not** applied here.

`pre_filt` corners 3–4 scale with Nyquist (0.40 and 0.80 × Nyquist). Copying California’s 20 and 25 Hz cosine taper onto 200 Hz data would be incorrect.

---

## 5. Units and amplitude names

| Quantity | Definition | Name used |
|----------|------------|-----------|
| After `remove_response(output=VEL)` | millimetres to metres per second | **m/s** on all 120 records |
| Peak \|HHZ\| in the event window | max \|v\| after VEL + 0.1–15 Hz | **band-limited PGV** (0.1–15 Hz) |
| Horizontal peak | max √(HHN² + HHE²) in the same window | band-limited horizontal PGV |
| Acceleration | d/dt of the band-limited velocity | **band-limited PGA** (0.1–15 Hz), m/s² |

These are not unfiltered strong-motion PGA/PGV and not intensity measures.

Physical-range flags (`peak_vel > 0.2` m/s or `peak_acc > 5` m/s²) were **not** raised (120 / 120 `ok`).

---

## 6. Results

### 6.1 Completeness

| Quantity | Count |
|----------|------:|
| Manifest event–station rows | 120 |
| Analysed OK | **120** |
| Partial / fail | **0** |
| Complete HH 3C | **120** |
| Noise window fully covered | **120** |
| Event window fully covered | **120** |
| Response attempted | **120** |
| Response successful (units m/s) | **120** |
| Response failed | **0** |
| MiniSEED gaps after merge | **0** |
| Unique events | 20 |
| Unique CH stations | 54 |
| Sampling 200 Hz / 120 Hz | 108 / 12 |

Failed records: **none**. None were discarded.

### 6.2 Response correction

Every record used the matching StationXML. Output units are **m/s**. Peak HHZ velocity range **1.25×10⁻⁶ – 5.90×10⁻³ m/s** (median **5.56×10⁻⁵ m/s** ≈ 0.056 mm/s). Peak HHZ band-limited acceleration range **3.84×10⁻⁵ – 0.186 m/s²** (median **1.67×10⁻³ m/s²**). These magnitudes are consistent with M ~3–4.7 at ~6–162 km; they are not digitizer-count artefacts.

The earlier 9-station technical `remove_response` test is therefore confirmed on the **full** 120-record set, not assumed from that test alone.

### 6.3 SNR

Formula (dimensionless; **not** detection probability):

```text
snr_peak = max(|x|) in [origin, origin+180 s]  /  RMS(x) in [origin−60 s, origin−10 s]
snr_rms  = RMS(x) in event window              /  RMS(x) in noise window
```

Computed on zero-phase 0.1–15 Hz velocity (and the matching horizontal / vector envelopes).

| Metric | min | median | mean | max |
|--------|----:|-------:|-----:|----:|
| SNR peak HHZ | 4.49 | 280 | 1633 | 4.23×10⁴ |
| SNR peak horizontal | 5.16 | 369 | 1991 | 4.37×10⁴ |
| SNR peak 3C vector | 4.89 | 323 | 1691 | 3.74×10⁴ |

The mean is pulled by quiet-site / strong-signal pairs (e.g. DIX, HAUIG). **Medians are the preferred location statistics.** Extreme SNR is a small noise RMS after band-pass, not a 4×10⁴ detection probability.

Lowest-SNR event: **2025ovpxfj** (MLhc 2.97, Affoltern am Albis), median SNR peak HHZ **6.3**.

### 6.4 STA/LTA (automatic triggers)

Parameters: STA **0.5 s**, LTA **10 s**, threshold **2.5**, causal 0.1–15 Hz HHZ, edge onsets inside the 5% taper / LTA warm-up ignored.

| Class | N (of 120) |
|-------|-----------:|
| First search-window onset in [origin, origin+90 s] (`expected_event_window`) | 48 |
| First search-window onset in [origin−5 s, origin) (`search_window_pre_origin`) | 72 |
| No trigger in search window | 0 |
| ≥1 onset in the noise window (`false_trigger_candidate`) | **119** |

Official trigger latency relative to origin: min **−4.97 s**, median **−2.01 s**, mean **1.06 s**, max **74.8 s** (late onsets on the smallest event, 2025ovpxfj).

**Evaluation of California parameters on Swiss HH:** threshold 2.5 is too sensitive once true pre-event data exist. Almost every record has at least one noise-window crossing. The official trigger then often sits in the 5 s immediately before catalogue origin (catalogue origin error, early filter energy, or a lingering CFT from pre-event transients). These times are **not** validated P picks and should not be used as such in later feature work without a higher threshold or an STA/LTA retune.

Example used in figures (not chosen for a clean pick): **2020btnrcj CH.EMBD**, ~9.3 km, SNR peak HHZ 943, official latency **−4.56 s**, class `search_window_pre_origin`. Figure `fig04b` shows a different trigger class from the same run.

### 6.5 Amplitude and distance

| Metric | min | median | max |
|--------|----:|-------:|----:|
| Epicentral distance (km) | 6.13 | 56.9 | 162 |
| Hypocentral distance (km) | 7.36 | 57.0 | 162 |
| Band-limited PGV HHZ (m/s) | 1.25×10⁻⁶ | 5.56×10⁻⁵ | 5.90×10⁻³ |
| Band-limited horizontal PGV (m/s) | 1.11×10⁻⁶ | 9.15×10⁻⁵ | 1.50×10⁻² |
| Band-limited PGA HHZ (m/s²) | 3.84×10⁻⁵ | 1.67×10⁻³ | 0.186 |

Largest PGV: **2022rvutkg** (MLhc 4.74, Mulhouse) at HAUIG. No attenuation relationship is fitted; Figure 9 is a scatter only.

Selected stations did not reach the 250–400 km bin of the acquisition policy (observed max ~162 km).

### 6.6 Event- and station-level summaries

- `swiss_event_summary.csv` — 20 rows (6 stations each; all 6 response-successful).
- `swiss_station_summary.csv` — 54 stations. Stations with median SNR peak HHZ below 30% of the station-median SNR: **AIGLE, BRANT, DAGMA, FUSIO, MUGIO, MUO, SALAN, VDR** (`low_median_snr`). Noise-window STA/LTA onsets at threshold 2.5 are **cohort-wide**, not used as a station-unusual flag.

Catalogue magnitude types: **MLh** (2 events), **MLhc** (18 events). Magnitudes are not interchangeable with California mw/ml.

---

## 7. Figures

All under `reports/swiss_signal_analysis/figures/` (not California `reports/figures/`).

| File | Content |
|------|---------|
| `fig01_representative_3c_waveform.png` | 2020btnrcj EMBD, 3C velocity |
| `fig02_response_correction_hhz.png` | Same HHZ, counts vs m/s |
| `fig03_noise_vs_event_window.png` | Noise and event windows shaded |
| `fig04_sta_lta_example.png` | Causal STA/LTA on that record (pre-origin official trigger) |
| `fig04b_sta_lta_additional_class.png` | A second record with a different trigger class (not success-only) |
| `fig05_snr_distribution.png` | All 120 SNR peak HHZ |
| `fig06_trigger_latency_distribution.png` | All official latencies |
| `fig07_peak_amplitude_distribution.png` | All band-limited PGV HHZ |
| `fig08_station_event_map.png` | Events and selected CH stations |
| `fig09_distance_vs_amplitude.png` | Distance vs PGV (no model) |
| `fig10_california_swiss_structural_comparison.png` | Methods-transfer table |

---

## 8. California comparison (methods transfer only)

| Item | California v1.0.0 (frozen) | Swiss pilot (this analysis) |
|------|----------------------------|-----------------------------|
| Events / records | 8 / 8 | 20 / 120 |
| Component | BHZ | HH 3C |
| Sampling | 40 Hz | 120 or 200 Hz |
| Window | origin-aligned 300 s | origin − 90 s to + 210 s |
| Noise | first 5 s proxy | origin − 60 s to − 10 s |
| Response removal | **0 / 8** | **120 / 120** (m/s) |
| Amplitude units | counts | band-limited PGV / PGA |
| STA/LTA parameters | 0.5 / 10 s, thr 2.5 | same numbers |
| STA/LTA search | first onset on origin-aligned raw trace | first onset in [−5, +90] s on causal 0.1–15 Hz HHZ |

SNR and trigger latency are **not** interchangeable: different noise windows, instrumentation, sampling, magnitude types (California mixed mw/ml vs Swiss MLh/MLhc), geography, and station mix (California 6/8 ADO). This is not a detection-performance shoot-out.

---

## 9. Variability and uncertainty (no advanced modelling)

- **Event-to-event:** median SNR peak HHZ from **6.3** (2025ovpxfj) to **~2.9×10³** (2022rvutkg).
- **Station-to-station:** 54 stations, uneven repeat counts (PANIX 7 events; many stations once).
- **Component-to-component:** horizontal median SNR (369) exceeds vertical (280); peak horizontal PGV exceeds HHZ, as expected for S-dominated windows.
- **Sample size:** N = 20 events is larger than California N = 8 but still a pilot.
- **Clustering:** Alpine and Jura/border events; CH network only; distance-bin selection still yields a median epicentral distance of ~57 km.
- **Picks:** automatic, threshold 2.5 too low for this band/data; 119/120 noise-window onsets.
- **Response:** water_level 60 and band-limited PGV/PGA; not a full strong-motion processing review.
- **Magnitudes:** SED MLh / MLhc, not moment magnitude.

---

## 10. Reproducibility

| Artefact | Path |
|----------|------|
| Parameters | `configs/swiss_signal_analysis.yaml`, `reports/swiss_signal_analysis/processing_config.json` |
| Trace metrics | `reports/swiss_signal_analysis/swiss_trace_metrics.csv` |
| Event / station summaries | `swiss_event_summary.csv`, `swiss_station_summary.csv` |
| Machine-readable summary | `swiss_signal_summary.json` |
| Failures | `failures.json` (empty list) |
| Log | `logs/switzerland/swiss_signal_analysis.log` |
| Tests | `tests/test_switzerland_signal_analysis.py` |

California analysis scripts, California reports, `FINAL_SUBMISSION/`, README, and the website were not used as write targets for this step.

---

## 11. Limitations

1. STA/LTA threshold 2.5, carried from California raw BHZ, produces near-universal pre-event onsets on Swiss causal HH. Official latencies are therefore **not** a P-travel-time data set.
2. Band-limited PGV/PGA are 0.1–15 Hz research measures, not code-style strong-motion values.
3. Horizontal-vs-vertical “earlier trigger” in the trace CSV used first-after-mute onsets on HHE/HHN versus the search-window HHZ pick; it is **not** a 3C phase comparison.
4. No ML, no EEW onsite decision metric, no Swiss performance claim relative to SED.
5. Availability-batch timeouts during acquisition may have omitted some CH stations; analysis uses only the downloaded 120 records.

---

## 12. Recommendation for the next step

Do **not** train ML on these traces yet.

Priority scientific follow-up:

1. **STA/LTA retune** (higher threshold and/or recursive STA/LTA) with the same windows, reporting how many noise-window onsets remain.
2. Then a **Swiss preprocessing / feature** layer that uses band-limited PGV and true pre-event SNR, still separate from frozen California features.

Until picks are retuned, treat STA/LTA columns as trigger diagnostics, not arrival times.
