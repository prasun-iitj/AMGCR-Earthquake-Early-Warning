# Certificate wrap presentation outline (13 November 2026)

**Deck:** `reports/Certificate_Wrap_Presentation.pptx`  
**AI/ML close:** [docs/AI_ML_CERTIFICATE_WRAP.md](../docs/AI_ML_CERTIFICATE_WRAP.md)  
**Length:** 16 slides · ~10–12 minutes  

Regenerate:

```text
python scripts/presentation/build_certificate_wrap_pptx.py
```

Do **not** claim operational EEW, trained ML, optimal threshold 8.0, or ground-truth P picks.

---

## Slide 1 — Title

**Reproducible AI-Assisted EEW Methods Research**  
California pilot · Swiss independent validation · Honest ML close-out  
AMGCR certificate programme · November 2026

## Slide 2 — What this talk is

- A completed **methods** chain, not a deployed warning system
- California = frozen methods laboratory (v1.0.0)
- Switzerland = methods transfer + independent STA/LTA validation
- AI/ML = literature reference + leakage audit; **no model trained**

## Slide 3 — Research design

- Europe: long-term programme target
- California IRIS/EarthScope: 8 events, completed analysis freeze 29 Jul 2026
- Swiss SED/ETH: Set A (20 events, development) vs Set C (15 events, locked test)
- EarthESND: architecture/literature only — K-NET tables not reproduced

## Slide 4 — What was built

- ObsPy FDSN acquisition, StationXML, physical units (Swiss)
- California: EDA → signal → preprocess → **8×18** feature matrix
- Swiss Set A: causal 0.1–15 Hz HHZ STA/LTA diagnosis → **proposed 8.0**
- Swiss Set C: frozen evaluation, threshold **not** retuned

## Slide 5 — California result (frozen)

- 8 events, single-component BHZ pilot
- Feature matrix 8 × 18 (time, frequency, onset proxies)
- Too small for supervised ML — used to **design the method**, not to train
- Response/units limitations documented in v1.0 report

## Slide 6 — Swiss development (Set A)

- 20 earthquakes, 120 CH HH 3C records
- True pre-event noise; response to velocity (m/s)
- Threshold 2.5 (California copy) **fails** on real pre-event Swiss noise
- Pre-declared rule selected **trigger ON = 8.0** for later independent test

## Slide 7 — Frozen detector (do not retune)

- Causal 0.1–15 Hz HHZ · STA 0.5 s · LTA 10 s
- ON **8.0** / OFF 0.5 · edge mute unchanged
- Detection window: **origin → origin + 90 s** (not before origin)
- 8.0 is **pre-declared**, not claimed optimal

## Slide 8 — Independent Set C

- 15 locked events, **550** CH HHZ records
- Same-station SED/manual first-P as **independent reference**, not ground truth
- 9/15 immediate-border — named Independent Swiss/Adjacent-Border Validation Set
- Set C membership frozen; not used to search thresholds

## Slide 9 — Validation headline (STEP 2K)

- 550/550 usable · **401** detected (72.9%) · **149** NO DETECTION (27.1%)
- Median |trigger − reference P| = **1.24 s**
- 381/401 (95.0%) at or after independent reference P
- Pre-event noise-trigger rate 69/550 (**12.5%**)
- Failures preserved; hard events not dropped

## Slide 10 — How to read the timing

- Positive error = automatic onset **after** the independent first-P
- Median signed error **+0.88 s** — consistent with a ratio detector
- Coverage is **heterogeneous** (e.g. 15% vs 100% by event)
- This is **not** a validated P picker

## Slide 11 — AI/ML: three layers

1. EarthESND paper: lightweight ESN+DENN **reference**
2. AI-assisted **workflow** (reproducible pipeline, features, validation)
3. Supervised learning on Swiss tables: **audited, not trained**

## Slide 12 — Why we did not train (the ML result)

- No independent Set A first-P file
- Detector outputs are not labels
- Set C must stay untouched as the test
- N=8 (California) and 9 misses / 120 at 8.0 (Set A) cannot support a detector
- Inventing labels to “add AI” would invalidate the science

## Slide 13 — Leakage we refused

- Event ID, origin time, trigger time, STA/LTA CFT as features
- Training on Set C picks
- Random split of 120 station-rows (same earthquake, six stations)
- Post-event amplitude to “predict” a detection that already used that window

## Slide 14 — Future ML (out of this close-out)

- Acquire Set A same-station first-P **without** touching Set C
- Build window-level Swiss features (not STA/LTA as the target)
- Event-grouped CV; L2 logistic / ridge only
- Freeze the model, **then** test on Set C

## Slide 15 — Limitations (say them)

- Not operational EEW
- Mixed MLh/MLhc; CH network; N small
- Catalogue origin ≠ P time
- Mute on 150 s traces covers last 10 s of search (documented, not “fixed”)
- EarthESND numeric tables not reproduced

## Slide 16 — Close

- Methods chain complete and frozen
- Independent Swiss validation of a **pre-declared** STA/LTA configuration
- AI/ML contribution: **knowing when not to train**
- Next programme steps are data/labels, not a last-minute network
