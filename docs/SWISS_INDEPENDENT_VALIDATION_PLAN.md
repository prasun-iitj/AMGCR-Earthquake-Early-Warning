# Independent Swiss / adjacent-border validation plan (design / audit)

**STEP 2I.1 — window correction and same-station reference audit.**  
**STEP 2J (2026-09-11) acquired/attempted the locked Set C validation data using the acquisition window origin − 60 s to origin + 90 s.**  
**STEP 2K (2026-09-11) evaluated the frozen STA/LTA configuration (trigger_on 8.0) on the acquired Set C records. The threshold was not retuned.**

| Field | Value |
|-------|--------|
| Document date | 2026-09-11 |
| Dataset name | **Independent Swiss/Adjacent-Border Validation Set** |
| Frozen detection configuration | Causal response-corrected velocity (where response metadata permits), 0.1–15 Hz, HHZ, STA 0.5 s, LTA 10 s, trigger_on **8.0**, trigger_off 0.5 |
| Catalogue | Official SED/ETH FDSN (`https://eida.ethz.ch/fdsnws/event/1/`) |
| Candidate CSV | `data/manifests/sed_switzerland_validation_candidates.csv` |
| Audit summary | `reports/switzerland_validation_audit/audit_summary.json` |
| STEP 2J acquisition report | [SWISS_VALIDATION_ACQUISITION_REPORT.md](SWISS_VALIDATION_ACQUISITION_REPORT.md) |
| STEP 2J waveform manifest | `data/manifests/sed_switzerland_validation_waveforms.csv` (550 CH HHZ records) |
| STEP 2K results | [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md) |
| California v1.0.0 | **Unchanged** |
| 20-event Swiss development set | **Unchanged** (not reused as validation) |
| Set C membership | **Unchanged** (15 locked IDs) |

**8.0 is the pre-declared/proposed threshold selected from the 20-event development dataset and reserved for independent validation.** It is not an optimum and is not yet validated.

---

## Three distinct windows (do not conflate)

These are **not** the same interval.

| Name | Interval | Role | Used for detection? |
|------|----------|------|---------------------|
| **Waveform acquisition window** | origin − 60 s → origin + 90 s | Interval requested from dataselect / checked on FDSN availability | No |
| **Detection / search window** | origin → origin + 90 s | Official EEW search interval for automatic onsets | **Yes — only this** |
| **Pre-event noise / QC window** | origin − 60 s → origin − 10 s | Noise-trigger rate and QC only | **No** |

The detector must **not** treat the pre-origin interval as an earthquake detection interval. Automatic onsets counted as candidate earthquake detections are restricted to **[origin, origin+90 s]**.

The development-set download window (origin − 90 s → origin + 210 s) applies only to **Set A** and is not the validation acquisition window.

---

## Data-leakage statement

The 20-event development set was used to diagnose/propose the configuration. The 15-event validation set was selected without using STA/LTA validation performance. The frozen configuration is not changed after validation results are observed.

---

## A / B / C

| Set | Name | n | Role |
|-----|------|--:|------|
| **A** | Existing Swiss development / tuning dataset | 20 events | Diagnosis and **proposal** of the frozen configuration only |
| **B** | Independent candidate pool | 227 earthquakes | Catalogue-eligible events **not** in A |
| **C** | Independent Swiss/Adjacent-Border Validation Set (proposed subset) | 15 events | Locked diversity sample from B |

Nine of fifteen Set C events are labelled `immediate_border`. The set is therefore named **Independent Swiss/Adjacent-Border Validation Set**. The 15 IDs were **not** silently replaced to make the set predominantly Swiss-interior.

Do not mix A and C. Do not retune STA/LTA using C.

---

## Frozen detection configuration (do not change)

| Item | Frozen value |
|------|----------------|
| Processing | Response-corrected velocity where StationXML/response metadata permits |
| Band | 0.1–15 Hz |
| Component | HHZ |
| STA / LTA | 0.5 s / 10 s |
| trigger_on / trigger_off | **8.0** / 0.5 |
| Edge / LTA warm-up | As currently implemented |
| Detection / search interval | origin → origin + 90 s |

---

## What HH 3C availability means

`n_unique_ch_stations_with_hh_3c` is a **unique CH station-code count**.

It is **not** a channel count, trace count, or station–channel combination count. A station is counted once if FDSN availability shows **HHZ, HHN, and HHE** each fully covering the **acquisition** window (origin − 60 s → origin + 90 s), allowing 1.5 s slack for timestamp truncation.

`n_unique_ch_stations_with_hhz` is the unique-station count for **HHZ only** over the same acquisition window (the channel the detector will use).

`acquisition_window_obtainable=yes` means at least one unique CH station has HHZ availability covering that acquisition interval. This is an availability-service check, **not** a MiniSEED read.

---

## Station-level reference matching

Four layers that must not be collapsed:

| Layer | Meaning |
|-------|---------|
| Event-level picks | QuakeML contains pick objects for the event |
| Station-level picks | Pick has network + station; CH first-P (`P`/`Pg`/`Pn`/`P1`/`Pb`/`Pdiff`) |
| Waveform availability | Unique CH station has HHZ (and optionally HH 3C) covering the acquisition window |
| StationXML / response | Per-station `level=response` metadata — **not yet verified** for Set C |

**Validation reference:** SED/manual CH first-P pick at the **same station** that provides the HHZ trace. STEP 2K used only this same-station reference.

An event-level pick is **not** sufficient. A pick at station X cannot score a waveform at station Y.

`n_same_station_first_p_and_hhz` = unique CH stations that have **both** a first-P pick and HHZ acquisition-window availability.  
`n_same_station_hhz_first_p_and_hhz` = the same intersection restricted to picks already labelled HHZ.

---

## StationXML status

**STEP 2J:** verified **per downloaded station/channel/interval** for all 550 acquired HHZ records (response present in StationXML). The earlier BALST spot-check was not used as coverage.

Records that were not downloaded have no StationXML claim.

---

## Set C acquisition and same-station check

STEP 2I.1 checked FDSN availability only. STEP 2J then downloaded the locked 15 events. Set C IDs were not changed.

| Short ID | Region | Class | Unique CH HHZ | Unique CH HH 3C | Acquisition obtainable | Unique CH stations with first-P | Same-station first-P ∩ HHZ | StationXML | Concern |
|----------|--------|-------|--------------:|----------------:|------------------------|--------------------------------:|---------------------------:|------------|---------|
| `2020flmsvb` | Montreux VD | swiss_territory | 61 | 60 | yes | 92 | 52 | not yet verified per station | — |
| `2020vcnoon` | Elm GL | swiss_territory | 65 | 63 | yes | 73 | 29 | not yet verified per station | — |
| `2021ffattd` | Bern | swiss_territory | 63 | 61 | yes | 99 | 58 | not yet verified per station | — |
| `2021toxjpc` | Arolla VS | swiss_territory | 65 | 63 | yes | 104 | 61 | not yet verified per station | — |
| `2022gzvhhy` | Giswil OW | swiss_territory | 68 | 66 | yes | 110 | 59 | not yet verified per station | — |
| `2022isnvgj` | St. Anton am Arlberg A | immediate_border | 68 | 66 | yes | 27 | 22 | not yet verified per station | — |
| `2022ugepue` | Vaduz FL | immediate_border | 70 | 68 | yes | 82 | 51 | not yet verified per station | Liechtenstein |
| `2023ksedgz` | Mulhouse F | immediate_border | 73 | 71 | yes | 111 | 62 | not yet verified per station | — |
| `2024bvrces` | Imst A | immediate_border | 73 | 70 | yes | 8 | 3 | not yet verified per station | few CH first-P picks |
| `2024cxfhdh` | Vesoul F | immediate_border | 69 | 67 | yes | 56 | 19 | not yet verified per station | — |
| `2024ftcvhn` | Albstadt D | immediate_border | 72 | 69 | yes | 7 | 7 | not yet verified per station | few CH first-P picks |
| `2024ujblmf` | Bludenz A | immediate_border | 68 | 63 | yes | 29 | 13 | not yet verified per station | — |
| `2025phgpma` | Strada GR | immediate_border | 67 | 64 | yes | 33 | 27 | not yet verified per station | eastern GR label may be tight |
| `2025rtcqvh` | Stockach D | immediate_border | 72 | 69 | yes | 50 | 34 | not yet verified per station | — |
| `2026bklhob` | Zermatt VS | swiss_territory | 57 | 30 | yes | 125 | 53 | not yet verified per station | — |

**Acquisition window obtainable (STEP 2I.1 availability): 15 / 15.**  
**At least one same-station first-P ∩ HHZ pair: 15 / 15.**  
**STEP 2J MiniSEED: 15 / 15 events, 550 / 550 HHZ records, 0 failed downloads.**  
**Overlap with Set A: none.**

SED `eventid=<short_id>` returned no QuakeML for these events; picks were retrieved with the full resource ID (`smi:ch.ethz.sed/...`). Short IDs remain the locked identifiers.

---

## Validation metrics (defined, not calculated)

Compute only after Set C MiniSEED exists and STA/LTA is run with the **frozen** configuration. Until then, do not quote detection accuracy.

| Metric | Required inputs |
|--------|-----------------|
| Station/event detection coverage | Readable HHZ trace; automatic onset evaluated only in the **detection** window |
| Automatic trigger time | HHZ trace; frozen STA/LTA; first candidate onset in **[origin, origin+90 s]** after edge mute |
| Same-station independent SED first-P time | SED/manual CH first-P pick at the **same station** as the HHZ trace |
| Trigger − P error | Automatic trigger time **and** same-station SED first-P |
| Median absolute timing error | Paired trigger and same-station P times |
| Percentage of triggers after reference P | Same pairs; `t_automatic ≥ t_sed_p` |
| Pre-event noise-trigger rate | HHZ trace; onsets in the **noise/QC** window only (origin−60 to origin−10 s) |
| N with usable same-station independent picks | Same-station SED first-P **and** readable HHZ |

Records with a waveform but no same-station pick are excluded from timing-error denominators and reported separately.

---

## Catalogue pool (unchanged from STEP 2I)

SED text query 2020-01-01 to 2026-09-11, M ≥ 2.5, ECOS-09 box: **251** rows; **24** excluded (20 in Set A, 1 atmospheric, 3 landslide); **227** independent earthquakes in Set B.

---

## Methodological limitations

- SED/manual picks are a catalogue reference, not absolute ground truth.
- Same-station intersection is smaller than event-level pick counts (picks at non-HH or non-available stations do not pair).
- Availability is not a MiniSEED read; downloaded traces may still fail.
- StationXML was later verified per acquired Set C record in STEP 2J; this design note is retained as a caution for any future download.
- Set C is border-heavy by construction of the locked 15; naming reflects that.
- This remains research validation, not operational EEW validation.

---

## Explicitly out of scope after STEP 2K

- Changing the frozen configuration after seeing results.
- Changing California or Set A results.
- ML training, threshold optimisation, additional datasets, or operationalization.

STEP 2K results: [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md).

---

## Tests

| Tests | Result |
|-------|--------|
| `tests/test_switzerland_validation_audit.py` | Window offsets, detection not before origin, unique-station HH 3C counting, same-station pick matching, locked Set C IDs |
| `tests/test_switzerland_validation_acquisition.py` | Acquisition window origin−60→+90 s; detection never before origin; locked Set C; same-station matching; full resource IDs; MiniSEED inspection; StationXML not falsely verified; failed downloads keep Set C |
| `tests/test_switzerland_validation.py` | Frozen 8.0; detection starts at origin; same-station matching; NO-DETECTION; timing error; noise-trigger; output schema |
| `tests/test_switzerland_pilot.py` | Development acquisition helpers unchanged |
| `tests/test_switzerland_signal_analysis.py` | passed |
| `tests/test_switzerland_sta_lta_transfer.py` | passed |

---

## Remaining blockers

1. Frozen STA/LTA **has been run** on Set C (STEP 2K); metrics are in [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md).
2. Two events (`2024bvrces`, `2024ftcvhn`) still have few same-station pairs (3 and 7); both were acquired and scored, not dropped.
3. Do **not** retune 8.0 from these results.

**Stop.** Do not proceed automatically to ML training, threshold optimisation, additional datasets, or operationalization.
