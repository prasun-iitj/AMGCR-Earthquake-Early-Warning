# Swiss ML feasibility audit (STEP 3A)

**Inspection only.** No model was trained. Set C, threshold **8.0**, and frozen validation results were not modified.

| Field | Value |
|-------|--------|
| Document date | 2026-09-11 |
| Decision | **NO-GO** for supervised ML on existing Set A tables |
| Set C | Untouched |
| Frozen STA/LTA | Unchanged (trigger_on **8.0**) |

---

## Why NO-GO

Set A (20 events, 120 CH records) has **metric and STA/LTA diagnostic tables**, not a Swiss feature matrix and **not** independent labels.

- The only `feature_matrix.csv` is **California v1.0.0** (8 × 18 features). It is not Set A.
- Set A has no pick file. Independent first-P picks exist only for **Set C**.
- Existing binary columns (`trigger_class`, `false_trigger_candidate`, frozen-8.0 `has_post_origin_onset`) are **detector outcomes**, not independent references. Using them as training labels would be circular.
- All 120 Set A rows are catalogue earthquakes; there is no noise-only class.
- Frozen 8.0 miss class on Set A is **9 / 120** — too rare for a defensible classifier at this N.

Project docs already forbid training on threshold-2.5 STA/LTA times.

---

## Leakage (if ML is ever revisited)

Do not use event ID, origin time, trigger times/latencies, STA/LTA CFT values, Set C validation outcomes, or a random 120-row split (stations share events). Any later split must be **grouped by event**. Set C remains an independent test only after a model is frozen on Set A with **independent** labels.

---

## What would be required later (not done)

Independent Set A labels (e.g. same-station SED first-P) **and** a leakage-safe Swiss feature table. Until those exist, do not add an AI layer.

**Stop.** No training.
