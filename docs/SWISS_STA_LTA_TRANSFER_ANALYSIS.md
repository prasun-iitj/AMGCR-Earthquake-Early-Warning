# Swiss STA/LTA methods-transfer analysis

**Scientific investigation only.** Automatic STA/LTA onsets are **trigger candidates**, not validated P arrivals.  
**Not** an operational EEW study, **not** a validated detector, and **not** an optimum-threshold search.

| Field | Value |
|-------|--------|
| Date (UTC) | 2026-09-07 |
| Script | `scripts/analysis/run_swiss_sta_lta_transfer.py` |
| Config | `configs/swiss_sta_lta_transfer.yaml` |
| Outputs | `reports/swiss_signal_analysis/sta_lta_transfer/` |
| Existing Swiss signal analysis | Unchanged |
| California v1.0.0 | Unchanged |
| Swiss raw MiniSEED | Unchanged |

The proposal rule was written **before** the grid was interpreted: lowest listed threshold at STA/LTA **0.5 / 10 s**, causal 0.1–15 Hz HHZ, with noise-window record fraction **< 0.25** and post-origin coverage **≥ 0.75**. That rule selects a **proposed** configuration for later validation. It is not an optimum.

---

## 1. Current STA/LTA implementation (as already run)

Inspected in `src/analysis/switzerland_signal.py`, `scripts/analysis/run_swiss_signal_analysis.py`, and `configs/swiss_signal_analysis.yaml`. **This investigation did not change that pipeline.**

| Step | What the Swiss official run does |
|------|----------------------------------|
| Input | Manifest MiniSEED + StationXML |
| Preprocess | Demean, linear detrend, Hann taper 5% |
| Response | `remove_response(output=VEL, water_level=60)`, Nyquist-aware `pre_filt` |
| Amplitude filter | Zero-phase 0.1–15 Hz, 4 corners |
| Detection filter | **Causal** copy of the same 0.1–15 Hz band-pass (`filter_zerophase: false`) |
| Characteristic function | ObsPy `classic_sta_lta` |
| STA / LTA / on / off | **0.5 s / 10 s / 2.5 / 0.5** (California numbers) |
| Edge handling | Mute onsets in the first and last `max(LTA, 5% of duration)` seconds (~15 s). Unmasked first crossing is stored only as a diagnostic |
| Official search | First muted onset in **[origin − 5 s, origin + 90 s]** |
| Noise-window diagnostic | Any muted onset in **[origin − 60 s, origin − 10 s]** |

California v1.0.0 used the **same STA/LTA numbers** on **raw BHZ counts**, first onset on an **origin-aligned 300 s** trace, with **no true pre-event** and a 5 s noise proxy.

Trigger latency in the Swiss official run is (first search-window onset) − origin. That is why the published median was **−2.01 s**.

---

## 2. Edge effects: evidence for and against

Traces start about **90 s before origin**. `classic_sta_lta` zeros the CFT for the first LTA (10 s). Combined mute is ~15 s (until ~origin − 75 s). The **noise window begins at origin − 60 s**, about **30 s after trace start** and **15 s after mute ends**.

| Diagnostic (causal HHZ, 0.5/10 s, threshold 2.5, N=120) | Result |
|----------------------------------------------------------|--------|
| Unmasked (no mute) first onset inside the mute region | **118 / 120** |
| Median unmasked onset after trace start | **10.0 s** (exactly LTA warm-up) |
| Median max CFT in mute region | 7.73 |
| Median max CFT between mute end and noise start | 5.19 |
| Median max CFT in noise window | **5.75** |
| Median fraction of noise-window CFT samples ≥ 2.5 | **0.12** |
| Median max CFT in [origin, origin+90 s] | **19.05** |

**Supported:** first-on-trace onsets are an **initialization / taper-adjacent** effect. The official pipeline already discards them via mute. That is why first-on-trace latency is *not* the published −2.01 s.

**Not supported as the cause of 119/120 noise-window onsets:** those onsets sit in [origin−60, origin−10], after mute. The noise-window CFT itself spends a median **12%** of samples above 2.5, with median peak CFT **5.75**, well above 2.5. That is ambient STA/LTA fluctuation, not a start-of-trace spike.

Filter transients are **not** required to explain the noise-window rate: **raw counts** (no band-pass, no response) still have **117 / 120** records with a noise-window onset at threshold 2.5 (see §5).

---

## 3. Pre-event noise (origin − 60 s to origin − 10 s)

On causal 0.1–15 Hz HHZ velocity:

| Statistic | Value |
|-----------|--------|
| RMS median | 1.49×10⁻⁷ m/s |
| RMS min / max | 1.85×10⁻⁸ / 4.19×10⁻⁶ m/s |
| Peak median | 3.91×10⁻⁷ m/s |
| Median peak / RMS | 2.72 |

Noise RMS varies by more than two orders of magnitude across records (quiet alpine sites vs noisier sites). Station-to-station RMS differences exist, but they do **not** sort stations into “clean” vs “false-triggering” groups at threshold 2.5 (see §6).

The noise **does** produce STA/LTA excursions above 2.5: median noise-window max CFT is 5.75, and 804 separate noise-window onsets were counted on 120 records (median 7 onsets per record on each component).

---

## 4. Threshold sensitivity (STA 0.5 s, LTA 10 s, causal HHZ)

This is a **sensitivity table**, not a validation benchmark.

| Threshold | Records with ≥1 noise-window onset | Records with ≥1 onset in [−5, 0) s | Records with ≥1 onset in [0, 90] s | Search-window first onset pre-origin | Median search latency (s) | Median first **post-origin** latency (s) | No onset in [−5, 90] s |
|-----------|-----------------------------------:|-----------------------------------:|-----------------------------------:|-------------------------------------:|--------------------------:|-----------------------------------------:|-----------------------:|
| 2.5 | 119 (99.2%) | 72 (60%) | 120 (100%) | 72 | −2.01 | 4.44 | 0 |
| 3.0 | 115 | 64 | 119 | 64 | −0.53 | 5.16 | 1 |
| 3.5 | 112 | 57 | 118 | 57 | +1.21 | 6.06 | 1 |
| 4.0 | 107 | 47 | 118 | 47 | +2.88 | 6.93 | 1 |
| 4.5 | 103 | 31 | 118 | 31 | +4.54 | 7.18 | 2 |
| 5.0 | 89 | 28 | 117 | 28 | +4.72 | 9.41 | 2 |
| 6.0 | 50 (42%) | 14 | 115 | 14 | +9.06 | 9.67 | 4 |
| **8.0** | **12 (10%)** | **3 (2.5%)** | **111 (92.5%)** | 3 | +9.83 | **10.07** | 9 |
| 10.0 | 0 | 1 | 110 (91.7%) | 1 | +10.22 | 10.22 | 10 |

Raising the threshold steadily reduces noise-window and [−5, 0) onsets. Post-origin coverage stays high through 8–10, but the **first post-origin** onset occurs later (median 4.4 s at 2.5 vs ~10 s at 8). That later latency is consistent with skipping weak early CFT bumps and firing on stronger later energy. It is **not** evidence of a better P pick.

---

## 5. Processing variants at threshold 2.5 (0.5 / 10 s, HHZ)

| Processing | Noise-window records | [−5, 0) records | Post-origin records |
|------------|---------------------:|----------------:|--------------------:|
| raw_counts (demeaned HHZ, no response, no band-pass) | 117 / 120 | 66 | 120 |
| response_vel (VEL, no extra 0.1–15 Hz) | 119 / 120 | 70 | 119 |
| causal_bandpass (official detection stream) | 119 / 120 | 72 | 120 |
| zerophase_bandpass | 120 / 120 | 74 | 118 |

Causal vs zero-phase vs raw are **almost the same** at threshold 2.5. Filtering and response correction are therefore **not** the primary reason California’s 2.5 threshold fails on Swiss pre-event data. The threshold sits below typical HH noise CFT maxima whether or not the trace is band-limited.

---

## 6. STA/LTA window sensitivity (threshold 2.5, causal HHZ)

| STA / LTA (s) | Noise-window records | [−5, 0) records | Post-origin records | Median search latency (s) |
|---------------|---------------------:|----------------:|--------------------:|--------------------------:|
| 0.5 / 10 | 119 | 72 | 120 | −2.01 |
| 1 / 10 | 117 | 52 | 118 | +1.84 |
| 1 / 20 | 117 | 50 | 117 | +1.88 |
| 2 / 20 | 98 | 28 | 109 | +5.21 |

Longer STA reduces pre-event onset counts somewhat but **does not** bring the noise-window record rate near a usable false-trigger level at threshold 2.5. Threshold, not STA/LTA length, is the dominant lever in this grid.

---

## 7. Station-level behaviour (threshold 2.5, causal HHZ)

54 stations. **53 / 54** have a noise-window onset on **every** record in this pilot. The exception is **SLE** (4 / 5 records, rate 0.8).

False-trigger candidates are **not** concentrated at a few bad sites. They are a **network-wide** property of threshold 2.5 on these HH traces. Station RMS and SNR vary, but they do not identify a small subset that “causes” the 119/120 result.

---

## 8. Component comparison (threshold 2.5, causal 0.1–15 Hz, 0.5 / 10 s)

| Channel | Noise-window record fraction | [−5, 0) fraction | Post-origin coverage | Median onsets in noise window |
|---------|-----------------------------:|-----------------:|---------------------:|------------------------------:|
| HHZ | 0.992 | 0.600 | 1.00 | 7 |
| HHN | 0.992 | 0.508 | 1.00 | 7 |
| HHE | 1.000 | 0.517 | 1.00 | 7 |

Pre-event triggering is **broadly similar on all three components**. HHZ is not uniquely noisy; it is slightly more likely to place the *first search-window* onset before origin (60% vs ~51%). There is no evidence here that switching the official channel to HHN/HHE would repair threshold 2.5.

---

## 9. Magnitude, distance, and SNR

On the 120 causal HHZ records at threshold 2.5:

| Pair | Pearson correlation |
|------|--------------------:|
| Magnitude vs noise-window onset count | 0.12 |
| Epicentral distance vs noise-window onset count | −0.09 |
| SNR peak HHZ vs noise-window onset count | 0.01 |
| Magnitude vs presence of a [−5, 0) onset | 0.00 |

No useful detection or attenuation relationship is claimed. Low-SNR records (SNR peak < 20, N=10) still have a 0.9 noise-window onset rate and 1.0 post-origin coverage at threshold 2.5 — the threshold is not “failing only on weak events.”

The **−5 s search allowance** does contribute **materially** to the published pre-origin *official* trigger rate: 72 / 120 first search onsets are in [origin−5, origin) at threshold 2.5, versus 48 in [origin, origin+90]. That split is a search-window effect on top of the separate 119 / 120 noise-window problem. Both numbers are reported; neither is hidden.

---

## 10. Interpretation (supported by the measurements)

Poor transfer of California STA/LTA **2.5** to Swiss HH is explained primarily by **threshold vs ambient CFT level**, exposed by **true pre-event data** that California never had.

1. **Threshold sensitivity (main).** Median noise-window max CFT is ~5.7 at 0.5/10 s. Threshold 2.5 is below ordinary HH noise excursions. Raising the threshold reduces noise-window records monotonically (99% → 0% from 2.5 to 10).
2. **Pre-event duration (main, structural).** California’s origin-aligned BHZ traces had no [origin−60, origin−10] interval in which to count false onsets. The same numerical threshold can look acceptable there and fail here without any Swiss “bug.”
3. **Instrumentation / sampling (contributing context, not isolated).** Swiss HH is 120/200 Hz vs California 40 Hz BHZ. Raw (unfiltered) Swiss HH still yields 117/120 noise-window records at 2.5, so the failure is not created by the 0.1–15 Hz filter alone.
4. **Edge / LTA initialization (real, but already handled for official picks).** 118/120 unmasked first onsets fall in the mute/LTA warm-up. This explains first-on-trace times near −80 s; it does **not** explain noise-window onsets after origin−60 s.
5. **The −5 s search window (contributes to pre-origin *official* latency, not to 119/120 noise onsets).**
6. **Not supported as primary:** a few bad stations; HHZ uniquely worse than horizontals; magnitude or distance controlling false-trigger rate; response-correction transients (raw counts behave the same).

---

## 11. Proposed Swiss configuration (not validated)

**Proposed configuration** (from the pre-declared rule in `configs/swiss_sta_lta_transfer.yaml`):

| Item | Proposed value |
|------|----------------|
| Processing | Causal 0.1–15 Hz after VEL response (same as current official detection stream) |
| Channel | HHZ |
| STA / LTA | **0.5 s / 10 s** (unchanged) |
| On / off thresholds | **8.0 / 0.5** |
| Edge mute | Keep current mute (`max(LTA, 5% duration)`) |
| Official search (suggested for the next study) | **[origin, origin + 90 s]** — drop the −5 s pre-origin allowance unless catalogue-origin uncertainty is modelled separately |
| Noise diagnostic | Keep [origin−60, origin−10] |

**Why this row, and not 10.0 or 6.0:** it is the **lowest** listed threshold that meets the pre-declared cuts (noise-window record fraction **0.10 < 0.25**, post-origin coverage **0.925 ≥ 0.75**). Threshold 6.0 still has 42% noise-window records. Threshold 10.0 meets a stricter noise cut but was not selected, because the rule takes the lowest qualifying threshold, not the highest.

**Observed trade-off at 8.0 (same 120 records — not a test set):** 9 records have no onset in [−5, 90] s; median first post-origin latency is ~10 s rather than ~4 s. That is expected if weak early CFT bumps are ignored.

---

## 12. Why it is not validated

- The same 20 events / 120 records were used to diagnose failure and to apply the proposal rule.
- There is no independent analyst P catalogue, no SED pick comparison, and no held-out time period.
- Coverage at threshold 8.0 is “has some post-origin CFT crossing,” not “the onset is the P wave.”
- Off-threshold 0.5 was not re-studied.
- No recursive STA/LTA, no frequency-dependent detector, and no site-specific thresholds.

Until a **separate** validation set and an independent arrival reference exist, this remains a **proposed configuration**.

---

## 13. Limitations

- Pilot N=20 events, CH network only, mixed MLh/MLhc.
- `classic_sta_lta` only.
- Band-pass 0.1–15 Hz held fixed except in the processing-variant check.
- Catalogue origin is not a P time; travel-time residuals are not estimated.
- Figures include configured examples (EMBD, JAUN on 2020btnrcj), not a success-only gallery.

---

## 14. Recommendation for the next research step

Do **not** train ML on STA/LTA times from threshold 2.5.

Do **not** treat threshold 8.0 as operational.

Next scientific step: **independent validation** of the proposed configuration (causal 0.1–15 Hz HHZ, 0.5/10 s, threshold 8.0, search starting at origin) against SED/manual arrivals on a **new** Swiss event set or a pre-declared held-out subset, reporting missed post-origin onsets and residual noise-window onsets. Only after that should Swiss features that need an onset time be built.

---

## Artefacts

| File | Role |
|------|------|
| `threshold_sensitivity.csv` | Threshold grid, causal HHZ 0.5/10 s |
| `window_sensitivity.csv` | STA/LTA length grid at threshold 2.5 |
| `processing_variant_comparison.csv` | Raw / VEL / causal / zerophase at 2.5 |
| `station_trigger_summary.csv` | Per-station rates |
| `component_trigger_summary.csv` | HHZ / HHN / HHE |
| `noise_window_statistics.csv` | RMS, peak, std |
| `edge_effect_diagnostics.csv` | CFT maxima by time region |
| `record_trigger_grid.csv` | Full record-level grid |
| `trigger_analysis.json` | Machine-readable summary + proposal |
| `figures/fig01`–`fig12` | Sensitivity and diagnostic plots |

Reproduce:

```powershell
python scripts/analysis/run_swiss_sta_lta_transfer.py
python -m pytest tests/test_switzerland_sta_lta_transfer.py tests/test_switzerland_signal_analysis.py -q
```
