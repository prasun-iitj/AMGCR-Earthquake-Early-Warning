# AI/ML certificate wrap (final scientific position)

**This is the AI/ML ending of the project.**  
No model was trained. Threshold **8.0**, Set A, Set C, and California v1.0.0 are unchanged.

> **Update 2026-11-12 (historical note):** This wrap reflects the position of 2026-11-11. The STEP 3A NO-GO was later resolved: STEP ML-1A acquired 120/120 SED analyst picks for Set A, and STEP ML-2 to ML-4 trained Random Forest and XGBoost models on Set A and evaluated them on Set C. See [PROJECT_STATUS.md](PROJECT_STATUS.md) and [SET_C_VERTICAL_ML_EVALUATION_REPORT.md](SET_C_VERTICAL_ML_EVALUATION_REPORT.md). These are offline, windowed research benchmarks, not an operational EEW system. The text below is preserved unchanged as the 2026-11-11 record.

| Field | Value |
|-------|--------|
| Date | 2026-11-11 |
| Role | Certificate close-out: what AI/ML means in this work, and what it does not |
| Presentation | `reports/Certificate_Wrap_Presentation.pptx` |
| Outline | `reports/Presentation_Certificate_Wrap_Outline.md` |

---

## One-sentence position

This project is **AI-assisted, leakage-aware EEW methods research**. It is **not** a trained earthquake detector, **not** EarthESND reproduced on Swiss data, and **not** operational early warning.

---

## Where AI/ML actually sits

| Layer | What was done | What it is not |
|-------|----------------|----------------|
| **1. Literature / architecture** | EarthESND documented as a lightweight ESN+DENN **reference** for onsite magnitude ideas | K-NET tables were **not** reproduced; no EarthESND training run |
| **2. AI-assisted workflow** | Reproducible ObsPy pipeline: catalogue → waveforms → response → features (California) → STA/LTA → independent Swiss validation | Not a neural network; not a black-box alert system |
| **3. Supervised ML on Swiss tables** | STEP 3A feasibility audit | **NO-GO** — existing Set A files lack independent labels and a Swiss feature matrix |

The scientifically honest “ML result” is **layer 3**: a documented decision **not** to train when labels would be circular or invented.

---

## Why training was refused (keep this on a slide)

1. California `feature_matrix.csv` is **8 events × 18 features** — too small for supervised generalisation.
2. Swiss Set A has **120 records / 20 events** of STA/LTA **diagnostics**, not independent first-P labels.
3. Set C **does** have same-station SED/manual first-P picks, but it is the **frozen independent test**. Using it to train would destroy the validation.
4. Binary columns such as `trigger_class` and `has_post_origin_onset` **are the detector**. Training on them is circular.
5. All Set A rows are catalogue earthquakes — there is **no noise-only class**.

STEP 3A details: [SWISS_ML_FEASIBILITY_AUDIT.md](SWISS_ML_FEASIBILITY_AUDIT.md).

---

## What *was* validated (the scientific core)

Frozen automatic-onset configuration on Independent Swiss/Adjacent-Border Set C (not retuned after seeing scores):

| Metric | Result |
|--------|--------|
| Records | 550 / 550 usable |
| Automatic trigger | 401 / 550 (72.9%) |
| NO DETECTION | 149 / 550 (27.1%) |
| Median absolute trigger − independent reference P | 1.24 s |
| Triggers at or after independent reference P | 381 / 401 (95.0%) |
| Pre-event noise-trigger rate | 69 / 550 (12.5%) |

SED/manual first-P times are **independent reference picks**, not ground truth. Automatic times are **candidate onsets**, not confirmed P arrivals. Threshold 8.0 is **pre-declared**, not optimal.

Full write-up: [SWISS_INDEPENDENT_VALIDATION_RESULTS.md](SWISS_INDEPENDENT_VALIDATION_RESULTS.md).

---

## If ML is ever added later (not this certificate close-out)

Minimum conditions, already recorded in STEP 3A:

- Independent **Set A** same-station first-P (new acquisition — not Set C reuse)
- Leakage-safe Swiss **window features** (not STA/LTA outputs as inputs)
- **Event-grouped** cross-validation (do not randomly split 120 station-rows)
- Set C remains a **held-out** test after the model is frozen
- Model class: L2 logistic / ridge — **not** a deep net at N=20 events

Until those exist, do not add an AI layer for the sake of adding AI.

---

## Certificate talking points (safe language)

**Say:**
- AI-assisted, reproducible EEW **methods** for Western / European networks
- California = methods laboratory (frozen v1.0)
- Switzerland = methods transfer + independent validation of a frozen STA/LTA configuration
- EarthESND = literature benchmark for future onsite models
- Supervised training was **audited and declined** because the labels are not defensible yet

**Do not say:**
- We trained a model / we have an ML detector
- 8.0 is optimal
- SED picks are ground truth
- This is operational earthquake early warning
- STA/LTA times are validated P-wave picks

---

## Stop

Science freeze stands. Presentation wrap is the remaining delivery for 13 November 2026.
