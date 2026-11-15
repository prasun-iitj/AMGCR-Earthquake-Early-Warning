# Research Executive Summary

Numbers are from the saved result files in `reports/ml/` and the lineage summary in `reports/data_lineage/`. See [PROFESSOR_HANDOVER_GUIDE.md](PROFESSOR_HANDOVER_GUIDE.md) for navigation.

## Research problem

Earthquake early-warning (EEW) systems must recognise the first P-wave arrival in noisy seismic records. The standard approach is a short-term-average over long-term-average (STA/LTA) threshold. This project asks a narrower, testable question: given a pre-cut 4-second window of vertical ground velocity, can a supervised classifier trained on analyst-labelled Swiss earthquakes distinguish a P-wave window from an ambient-noise window better than an STA/LTA threshold rule, on earthquakes it has not seen?

The study is an **offline window-classification benchmark**. It does not detect arrivals in continuous data, measure warning time or false-alert rate, or operate in real time.

## Objective

Build a reproducible workflow from public waveform services to labelled windows, features and models, and report an event-independent evaluation with its limitations stated.

## Data sources

- **California pilot (v1.0.0, frozen):** event list from the USGS FDSN event service; waveforms from EarthScope (IRIS). 8 events, 8 BHZ records at 2 stations (CI.ADO, CI.USC), 40 Hz. P onsets from an automatic STA/LTA trigger; no analyst picks; amplitudes in counts.
- **Swiss data:** Swiss Seismological Service (SED, ETH Zurich) through EIDA: events, MiniSEED, StationXML (instrument response) and manual first-P picks from QuakeML.

## Dataset design

| | Set A (development) | Set C (independent evaluation) |
|---|---|---|
| Events | 20 | 15 |
| Records | 120 (three-component HH) | 550 (HHZ only) |
| Stations | 54 | 79 |
| Manual SED picks | 120 | 550 |
| Windows | 240 (120 P-wave, 120 noise) | 1,100 (550 + 550) |
| Features | 24 (18 vertical used for transfer) | 18 vertical |

Each record yields one positive window (analyst pick to pick + 4 s) and one negative window (origin - 35 s to origin - 31 s). Set A and Set C share no events. All 54 Set A stations also occur in Set C, so independence is by event, not by station. Windows from one earthquake are not independent samples; there are 20 and 15 earthquakes, not 240 and 1,100.

## Methodology

Instrument response was removed to velocity (m/s) and a 0.1 to 15 Hz bandpass applied. Each window is summarised by amplitude, energy, shape, spectral and STA/LTA features. Random Forest (200 trees, depth 6) and XGBoost (100 trees, depth 4) were trained on Set A with 20-fold Leave-One-Group-Out cross-validation, one earthquake held out per fold. Vertical-only 18-feature models were frozen and applied once to Set C. The baseline is a window-level rule, `sta_lta_max >= 8.0`.

## Main results

Set A, event-grouped cross-validation (N = 240):

| Model | F1 | Recall | ROC-AUC |
|---|---|---|---|
| Random Forest, 24 features | 0.9916 | 0.9833 | 0.9990 |
| XGBoost, 24 features | 0.9832 | 0.9750 | 0.9990 |
| Random Forest, 18 features | 0.9789 | 0.9667 | 0.9994 |
| XGBoost, 18 features | 0.9832 | 0.9750 | 0.9984 |
| STA/LTA threshold 8.0 | 0.9386 | 0.8917 | 0.9710 |

Set C, independent evaluation (N = 1,100, 15 unseen events):

| Model | F1 | Recall | Precision | ROC-AUC | FP | FN |
|---|---|---|---|---|---|---|
| XGBoost (18 features) | 0.9169 | 0.8527 | 0.9915 | 0.9780 | 4 | 81 |
| Random Forest (18 features) | 0.9125 | 0.8436 | 0.9936 | 0.9767 | 3 | 86 |
| Window-level STA/LTA >= 8.0 | 0.5014 | 0.3345 | 1.0000 | 0.8448 | 0 | 366 |

Missed P-wave windows fall by 77.9% (XGBoost) and 76.5% (Random Forest) relative to the window-level baseline. Recall is lowest for the smallest Set C events (for example `2020flmsvb`: RF 0.46, XGBoost 0.48). The model scores on Set C are lower than in Set A cross-validation; the cause is not established (event differences, distance and magnitude, and the preprocessing differences below are all candidates).

A separate record-level STA/LTA detector (STEP 2K, threshold 8.0, STA 0.5 s) detected 401 of 550 Set C records (72.9%) with a median absolute timing error of 1.24 s. It is a different procedure from the window-level baseline and the two are not interchangeable.

## Independent evaluation

Set C events were not used for training, model selection or threshold choice. Threshold 8.0 was taken from a Swiss Set A threshold grid (California used 2.5); the documents state it was pre-declared before Set C, but Git history cannot prove the order. Station-level independence does not hold.

## Contributions

- A documented, scripted data path from FDSN services to feature matrices, with manifests and lineage counts.
- Manual-pick labels independent of the STA/LTA detector.
- An event-grouped evaluation with a separate event set, with limitations disclosed.
- An integrity audit that found and documented several inconsistencies.

## Limitations

Small number of events (20 and 15); stations shared between sets; Set C vertical only; STA window, pre-filter corners and full-trace zero-phase filtering differ or are non-causal and are unquantified; `z_cav_m_s` has dimension of length despite its name; pre-cut windows only, with no latency or false-alert measurement; provider licensing and source URLs not verified; the reasons for the original 20 Set A events and for the exact final 15 Set C IDs are not documented beyond the configs. Details: [RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md).

## Future work (from the project roadmap)

More independent events and regions, three-component Set C data, a quantified sensitivity analysis of the preprocessing differences, continuous-stream testing, and European network expansion ([ROADMAP.md](../ROADMAP.md)). None of this has been done.
