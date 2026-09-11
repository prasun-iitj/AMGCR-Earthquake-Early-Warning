# Independent Swiss / adjacent-border validation results (STEP 2K)

**Frozen automatic-onset validation only.**  
Threshold **8.0** was evaluated exactly as pre-declared. It was **not** retuned, searched, or declared optimal. SED/manual first-P picks are **independent reference P picks**, not ground truth. This is **not** an operational earthquake-early-warning demonstration and is **not** a claim of validated P-wave picking.

| Field | Value |
|-------|--------|
| Document date | 2026-09-11 |
| Dataset | **Independent Swiss/Adjacent-Border Validation Set** (locked 15 events, 550 CH HHZ records) |
| Script | `scripts/analysis/run_swiss_independent_validation.py` |
| Configuration | `configs/sed_switzerland_validation.yaml` |
| Trace metrics | `reports/switzerland_validation/validation_trace_metrics.csv` |
| Event summary | `reports/switzerland_validation/validation_event_summary.csv` |
| JSON summary | `reports/switzerland_validation/validation_summary.json` |
| Processing snapshot | `reports/switzerland_validation/processing_config.json` |
| Failures | `reports/switzerland_validation/failures.json` |
| California v1.0.0 | **Unchanged** |
| Set A (20-event development) | **Unchanged** |
| Set C membership | **Unchanged** |

**8.0 is the pre-declared/proposed threshold selected from the development dataset and reserved for this independent evaluation.** The numbers below describe that frozen configuration on Set C. They are not a licence to change 8.0.

---

## What was evaluated

The established Swiss detection recipe was applied once, without a threshold grid:

| Item | Frozen value |
|------|----------------|
| Input | Locked Set C MiniSEED + per-record StationXML (`StationXML_path` in the waveform manifest) |
| Component | **HHZ only** (Set C files are not HH 3C; 3C was not required) |
| Preprocess | Demean, linear detrend, Hann taper 5% |
| Response | Station-specific `remove_response(output=VEL, water_level=60)`, Nyquist-aware `pre_filt`; velocity in m/s |
| Detection filter | **Causal** 0.1–15 Hz, 4 corners |
| STA / LTA / on / off | **0.5 s / 10 s / 8.0 / 0.5** |
| Edge mute | `max(LTA, 5% of duration)` at each end (unchanged) |
| Detection / search | **origin → origin + 90 s** (must not begin before catalogue origin) |
| Trigger used | **First** muted onset in the detection window; later onsets were not preferred |
| If none | **NO DETECTION** (retained) |
| Reference | Same-station SED/manual first-P from `data/manifests/sed_switzerland_validation_picks.csv` |

Acquisition window (already downloaded in STEP 2J): origin − 60 s → origin + 90 s.  
Pre-event noise/QC window: origin − 60 s → origin − 10 s. That interval is diagnostic only and was **not** used as the detection window.

On 150 s Set C traces the established mute is **10 s** at each end. The start mute overlaps the first 10 s of the noise window; the end mute covers origin + 80 s to origin + 90 s. The mute was **not** redesigned to recover that last 10 s of the search window.

---

## Pre-declared metrics (all 550 records retained)

| Metric | Result |
|--------|--------|
| 1. Usable station–event records | **550 / 550** (processing failures: **0**) |
| 2. Valid automatic trigger | **401 / 550 (72.9%)** |
| 3. NO DETECTION | **149 / 550 (27.1%)** |
| 4. Automatic trigger time vs catalogue origin | Per record in `validation_trace_metrics.csv` (`trigger_latency_s`) |
| 5. Same-station independent first-P vs origin | Per record (`reference_p_latency_s`) |
| 6. Trigger − reference-P timing error | Per paired detection (`trigger_minus_p_s`) |
| 7. Median absolute timing error | **1.24 s** (401 paired detections) |
| 8. Detected triggers at or after the reference P | **381 / 401 (95.0%)** |
| 9. Pre-event noise-trigger rate `[origin−60, origin−10)` | **69 / 550 (12.5%)** |
| 10. Records with usable same-station independent P | **550 / 550** |

Median **signed** timing error (trigger − reference P) among paired detections is **+0.88 s**. A positive value means the automatic onset is later than the independent reference P.

NO-DETECTION rows were not removed. Difficult events (`2024bvrces`, `2024ftcvhn`, `2020flmsvb`, `2022gzvhhy`) were not dropped after seeing the scores.

---

## Event-level coverage

| Event | Mag (MLh) | Region | Class | Records | Detected | Detection % | Median error (s) | Median \|error\| (s) | % at/after P |
|-------|----------:|--------|-------|--------:|---------:|------------:|-----------------:|---------------------:|-------------:|
| 2020flmsvb | 2.59 | Montreux VD | swiss_territory | 52 | 8 | 15.4 | +2.23 | 2.23 | 100 |
| 2020vcnoon | 3.60 | Elm GL | swiss_territory | 29 | 26 | 89.7 | +0.80 | 0.80 | 100 |
| 2021ffattd | 3.21 | Bern | swiss_territory | 58 | 51 | 87.9 | +0.63 | 0.72 | 98.0 |
| 2021toxjpc | 4.11 | Arolla VS | swiss_territory | 61 | 61 | 100 | +0.49 | 0.51 | 98.4 |
| 2022gzvhhy | 2.60 | Giswil OW | swiss_territory | 59 | 20 | 33.9 | +3.52 | 12.74 | 75.0 |
| 2022isnvgj | 2.82 | St. Anton am Arlberg A | immediate_border | 22 | 17 | 77.3 | +2.15 | 2.53 | 94.1 |
| 2022ugepue | 3.13 | Vaduz FL | immediate_border | 51 | 47 | 92.2 | +1.52 | 1.67 | 95.7 |
| 2023ksedgz | 3.56 | Mulhouse F | immediate_border | 62 | 62 | 100 | +0.55 | 0.60 | 96.8 |
| 2024bvrces | 3.70 | Imst A | immediate_border | 3 | 1 | 33.3 | +2.41 | 2.41 | 100 |
| 2024cxfhdh | 3.41 | Vesoul F | immediate_border | 19 | 17 | 89.5 | +0.67 | 0.72 | 94.1 |
| 2024ftcvhn | 2.79 | Albstadt D | immediate_border | 7 | 4 | 57.1 | +9.72 | 9.72 | 100 |
| 2024ujblmf | 2.69 | Bludenz A | immediate_border | 13 | 7 | 53.8 | +0.44 | 6.49 | 57.1 |
| 2025phgpma | 3.01 | Strada GR | immediate_border | 27 | 18 | 66.7 | +1.71 | 1.71 | 100 |
| 2025rtcqvh | 2.66 | Stockach D | immediate_border | 34 | 27 | 79.4 | +0.47 | 0.48 | 96.3 |
| 2026bklhob | 3.60 | Zermatt VS | swiss_territory | 53 | 35 | 66.0 | +2.46 | 2.57 | 91.4 |

Detection percentage is heterogeneous. Two events reach 100% record coverage (`2021toxjpc`, `2023ksedgz`). Several smaller or sparse-station events remain well below that (`2020flmsvb` 15.4%, `2022gzvhhy` 33.9%, `2024bvrces` 33.3% on only three records). Those misses are part of the validation result.

---

## How to read the timing comparison

Among the **401** records that produced a detection **and** a same-station independent first-P:

- 95.0% of automatic onsets occur **at or after** the independent reference P.
- The median absolute difference is **1.24 s**.
- The median signed difference is **+0.88 s** (automatic onset later than the reference P).
- **20 / 401** detections are earlier than the independent reference P.
- Event-level absolute errors are not uniform: `2022gzvhhy` and `2024ftcvhn` have median absolute errors of **12.7 s** and **9.7 s**, so some automatic onsets are not close to the first-P reference even when a trigger exists.

That pattern is consistent with a **ratio detector** that fires after enough post-arrival energy accumulates. It does **not** by itself demonstrate a validated P picker. Records with **NO DETECTION** have no timing error and are excluded from the timing denominators; they remain in the coverage denominators.

Figures (local; `figures/` is gitignored and regenerable):

- `reports/switzerland_validation/figures/fig01_trigger_vs_reference_timing.png`
- `reports/switzerland_validation/figures/fig02_timing_error_distribution.png`
- `reports/switzerland_validation/figures/fig03_event_detection_coverage.png`

---

## Pre-event noise window

**69 / 550 (12.5%)** usable records have at least one muted STA/LTA onset in `[origin−60, origin−10)`. That rate is a QC diagnostic for the frozen threshold on this independent set. It is not a false-alarm rate for an operational network, and it was not used to change 8.0.

---

## Failures

Processing failures: **none**. All 550 MiniSEED/StationXML pairs produced a causal-velocity CFT.

Scientific non-detections: **149**, retained in `validation_trace_metrics.csv` with `detection_status=NO_DETECTION`.

---

## What this does and does not support

**Supported as written:**

- Independent evaluation of the **frozen** automatic-onset configuration on locked Set C, with detection restricted to `[origin, origin+90 s]`.
- Same-station independent first-P comparison on every acquired record (550/550).
- Transparent retention of misses, early onsets, late onsets, and sparse-station events.

**Not supported, and not claimed:**

- That 8.0 is optimal, universal, or ready for operational EEW.
- That automatic STA/LTA times are confirmed P arrivals.
- That SED/manual picks are ground truth.
- That California v1.0.0 or Set A should be rewritten from these numbers.
- That the configuration should now be retuned on Set C.

---

## Reproducibility

```text
python scripts/analysis/run_swiss_independent_validation.py
python -m pytest tests/test_switzerland_validation.py tests/test_switzerland_validation_audit.py tests/test_switzerland_validation_acquisition.py tests/test_switzerland_pilot.py tests/test_switzerland_signal_analysis.py tests/test_switzerland_sta_lta_transfer.py
```

Set C IDs, MiniSEED, StationXML, picks, and threshold 8.0 were not changed after the metrics were observed.

---

## Explicitly out of scope after this step

- ML training
- Threshold optimisation or a new STA/LTA grid
- Additional datasets
- Operationalization / EEW alerting

**Stop.**
