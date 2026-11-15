# Independent Scientific Compatibility Audit: Swiss Set C for Supervised ML

**Project:** AMGCR Earthquake Research  
**Evaluation Target:** Feasibility of Independent Model Evaluation of Trained Random Forest & XGBoost on Swiss Set C  
**Date:** 2026-11-12  
**Context:** Preparation for Final IIT Jodhpur Project Evaluation  
**Auditor:** Automated Scientific Integrity Agent (Antigravity)  
**Mode:** Strictly Read-Only Audit (No retraining, no tuning, no feature substitution, no predictions executed)  

---

## 1. Executive Summary & Audit Verdict

This audit rigorously evaluated whether Swiss Set C (15 events, 550 records) can be used immediately as an independent held-out evaluation dataset for the Random Forest and XGBoost models trained in **STEP ML-3**.

### Canonical Audit Verdict

# **VERDICT: C. NOT READY – FEATURE OR DATA INCOMPATIBILITY**

### Core Audit Finding

The saved Random Forest and XGBoost models (`swiss_rf_model.joblib` and `swiss_xgb_model.joblib`) were trained on **24 multi-domain features**, of which **6 features explicitly require three-component (3C) seismic data** (horizontal and vector magnitude velocity metrics). 

A forensic audit of `data/raw/switzerland_validation/` reveals that **Swiss Set C contains exclusively 550 single-component vertical (`HHZ`) records**. There are **zero horizontal components (`HHN`, `HHE`)** present in the Set C waveform archive or its StationXML metadata.

Because scikit-learn and XGBoost estimators require the exact 24-feature schema, passing vertical-only data would trigger an immediate dimension mismatch error. Furthermore, **zero-filling or synthetically imputing missing horizontal features would corrupt 29.4% of Random Forest decision splits and 33.8% of XGBoost decision splits**, violating scientific integrity.

---

## 2. Check-by-Check Audit Matrix

| Check # | Audit Item | Status | Key Finding |
| :---: | :--- | :---: | :--- |
| **1** | Model Feature Requirements | **FAIL (for Set C)** | Models require exactly 24 features. 18 are vertical-only; 6 require 3-component data (`HHZ`, `HHN`, `HHE`). |
| **2** | Set C Waveform Channel Availability | **FAIL** | All 550 MiniSEED files in Set C are strictly `HHZ`. Zero horizontal channels exist on disk. |
| **3** | Feature Extraction Identicality | **FAIL** | 6 features cannot be extracted without horizontal waveforms (`h_peak`, `h_rms`, `vec3c_peak`, `vec3c_rms`, `vh_ratio`, and `snr_db`). |
| **4** | 3-Component Feature Impact | **CRITICAL** | The missing 3C features account for **29.4%** of Random Forest feature importance (Gini) and **33.8%** of XGBoost importance (Gain). |
| **5** | Analyst Ground Truth Picks in Set C | **PASS** | 550 / 550 (100%) verified manual first-P picks from certified SED analysts (`eval_mode = manual`, Pg: 390, P1: 87, Pn: 73). |
| **6** | Record-to-Pick Mapping in Set C | **PASS** | Perfect 1-to-1 mapping (550 waveforms to 550 picks). Causal time windows ($[t_{\text{origin}}-35, t_{\text{origin}}-31]$ and $[t_{\text{pick}}, t_{\text{pick}}+4.0]$) fit inside 150 s duration. |
| **7** | Preprocessing, Sampling & Filtering | **PASS (for HHZ)** | StationXML exists for all 550 records for `HHZ`; physical deconvolution to ground velocity ($\text{m/s}$, $0.1 - 15.0\text{ Hz}$) is fully functional for vertical traces. |

---

## 3. Detailed Audit Findings

### 3.1 Check 1 & 4: Model Feature Requirements & 3C Feature Importance

The saved production models expect a 24-dimensional feature vector $\mathbf{x} \in \mathbb{R}^{24}$. We analyzed the exact mathematical definitions and their trained feature importances:

#### Vertical-Component Features (18 Features — Extractable from HHZ)
1. `z_peak_velocity_m_s` (Max absolute vertical velocity)
2. `z_p2p_amplitude_m_s` (Peak-to-peak amplitude)
3. `z_rms_velocity_m_s` (Root-mean-square vertical velocity)
4. `z_variance` (Signal variance)
5. `z_std` (Signal standard deviation)
6. `z_zero_crossing_rate_hz` (Wave oscillation rate)
7. `z_signal_energy_m2_s` (Integrated squared velocity)
8. `z_crest_factor` (Peak-to-RMS impulsiveness)
9. `z_kurtosis` (Spectral peakedness)
10. `z_skewness` (Waveform asymmetry)
11. `z_cav_m_s` (Cumulative absolute velocity)
12. `z_dominant_frequency_hz` (Peak FFT frequency)
13. `z_spectral_centroid_hz` (Spectral center of mass)
14. `z_spectral_bandwidth_hz` (Spectral spread)
15. `z_spectral_rolloff_95_hz` (95% spectral power cutoff)
16. `z_spectral_entropy` (Shannon entropy of power spectrum — **Rank #1 Feature**)
17. `sta_lta_max` (Peak STA/LTA ratio on vertical channel)
18. `sta_lta_mean` (Mean STA/LTA ratio on vertical channel)

#### Three-Component Features (6 Features — MISSING IN SET C)
19. `h_peak_velocity_m_s`: $\max \sqrt{v_N^2 + v_E^2}$ (Requires North and East channels)
20. `h_rms_velocity_m_s`: $\sqrt{\text{mean}(v_N^2 + v_E^2)}$ (Requires North and East channels)
21. `vec3c_peak_velocity_m_s`: $\max \sqrt{v_Z^2 + v_N^2 + v_E^2}$ (Requires all 3 components)
22. `vec3c_rms_velocity_m_s`: $\sqrt{\text{mean}(v_Z^2 + v_N^2 + v_E^2)}$ (Requires all 3 components)
23. `vh_ratio`: $v_{Z,\text{rms}} / \max(v_{H,\text{rms}}, 10^{-12})$ (Requires horizontal channels)
24. `snr_db`: In Set A feature extraction (`run_swiss_set_a_feature_engineering.py` line 200), SNR was defined as $20 \log_{10}(v_{3C,\text{rms}} / \text{noise}_{\text{baseline},\text{rms}})$, requiring all 3 components.

#### Importance of Missing Features in Saved Models

| Missing Feature | RF Rank | RF Gini Importance | XGBoost Rank | XGBoost Relative Gain |
| :--- | :---: | :---: | :---: | :---: |
| `snr_db` | **#2** | **12.52%** | **#2** | **24.79%** |
| `vec3c_peak_velocity_m_s` | **#4** | **9.49%** | **#5** | **6.28%** |
| `h_peak_velocity_m_s` | #12 | 2.15% | #14 | 0.81% |
| `h_rms_velocity_m_s` | #14 | 1.95% | #16 | 0.45% |
| `vec3c_rms_velocity_m_s` | #15 | 1.83% | #15 | 0.52% |
| `vh_ratio` | #16 | 1.48% | #13 | 0.94% |
| **Cumulative Missing Weight** | — | **29.42%** | — | **33.79%** |

Nearly **one-third of the total predictive power** of the trained models is concentrated in features that cannot be calculated from Set C.

---

### 3.2 Check 2: Waveform Channel Audit of Set C

An exhaustive scan of `data/raw/switzerland_validation/` shows:
- **Total MiniSEED files:** 550 files across 15 event directories.
- **Channel breakdown:**
  ```
  HHZ: 550 records (100.0%)
  HHN:   0 records (  0.0%)
  HHE:   0 records (  0.0%)
  HH1:   0 records (  0.0%)
  HH2:   0 records (  0.0%)
  ```
- **Total StationXML files in `data/metadata/switzerland_validation/`:** 550 XML files.
  - Every StationXML inventory contains exclusively the `HHZ` channel (verified via ObsPy inventory check on `CH.ACB.--.HHZ.xml`).

**Why did this occur?**  
In STEP 2J (September 2026), Set C was designed specifically to validate the single-channel California STA/LTA detector (threshold 8.0) transferred to Switzerland (STEP 2K). Because traditional STA/LTA operated solely on the vertical channel (`HHZ`), only `HHZ` MiniSEED traces and StationXML were requested and archived.

---

### 3.3 Check 5 & 6: Analyst Ground Truth Picks & Mapping in Set C

The ground-truth labeling for Set C is in pristine condition:
- **Manifest:** `data/manifests/sed_switzerland_validation_picks.csv` (550 rows).
- **Evaluation Mode:** **100% manual** (550 / 550 picks by SED certified analysts; 0 automatic, 0 missing).
- **Phases:** Pg (390), P1 (87), Pn (73).
- **Waveform Mapping:** Every waveform in `data/manifests/sed_switzerland_validation_waveforms.csv` maps 1-to-1 with its corresponding same-station manual first-P pick (`same_station_pick_status = 'manual_ch_first_p'`).
- **Trace Coverage:** Every waveform has a duration of exactly 150.0 seconds ($[t_{\text{origin}} - 60\text{ s}, t_{\text{origin}} + 90\text{ s}]$).
  - The pre-origin ambient noise window ($[t_{\text{origin}} - 35\text{ s}, t_{\text{origin}} - 31\text{ s}]$) is fully covered.
  - The positive P-wave window ($[t_{\text{pick}}, t_{\text{pick}} + 4.0\text{ s}]$) is fully covered.

---

## 4. Scientific Integrity & Anti-Pattern Warnings

To protect the integrity of tomorrow's IIT Jodhpur evaluation, the following anti-patterns are strictly prohibited:

1. **PROHIBITED: Zero-Imputation of Horizontal Features**  
   Artificially setting missing horizontal channels to zero (e.g. $h_{\text{peak}} = 0, \text{vec3c} = z, \text{vh\_ratio} = 1.0$) would feed fabricated inputs into trees at decision nodes representing 30%+ of the model's structure. This would yield distorted, unscientific evaluation metrics and would fail any external peer review.
2. **PROHIBITED: Retraining on Set C**  
   Set C was pre-declared in `PROJECT_CHARTER.md` and `docs/ROADMAP.md` as an independent validation set. Training or tuning models on Set C would violate its independent test status.

---

## 5. Strategic Options for IIT Jodhpur Evaluation

Given the timeline (tomorrow's presentation), here are the concrete options:

### Option A: Primary Defense on Set A Benchmark + Set C Integrity Case (RECOMMENDED)
- **Action:** Present the completed, fully audited **STEP ML-3 benchmark on Swiss Set A** (240 causal windows, 20 events, 20-fold Leave-One-Group-Out CV, 99.17% RF, 98.33% XGB, 0 false alarms, zero leakage).
- **Set C Narrative:** Present this compatibility audit (`SET_C_ML_COMPATIBILITY_AUDIT.md`) directly in your presentation slides. Frame it as a **major demonstration of scientific rigor**:
  > *"When preparing to evaluate our models on the independent Swiss Set C archive, an automated integrity audit discovered that Set C was historically acquired as single-component HHZ for STA/LTA validation. Rather than performing unscientific zero-imputation of the missing horizontal components, we strictly maintained academic standards and flagged the dataset as requiring 3-component acquisition prior to evaluation."*
- **Assessment:** This turns an apparent blocker into a major academic strength, showcasing methodological maturity.

### Option B: Acquire 3-Component Waveforms for Set C (Set C 3C Upgrade)
- **Action:** Write an acquisition script to download the corresponding `HHN` and `HHE` channels and StationXML for the exact 15 events and 79 stations in Set C from the SED FDSN service (`eida.ethz.ch`).
- **Feasibility:** SED stations are permanent 3-component stations. Downloading 1,100 additional MiniSEED traces (550 N + 550 E) would take approximately 30–45 minutes of network transfer. Once downloaded, the existing 24-feature pipeline can run without changing a single line of model code.
- **Risk:** High network / time dependency on the night before the evaluation.

### Option C: Train a Dedicated Vertical-Only (18-Feature) Model on Set A
- **Action:** Fit a companion `SwissZRandomForestModel` and `SwissZXGBoostModel` using only the 18 vertical-component features on Set A. Evaluate them via LOGO CV on Set A, and then evaluate them on the 550 vertical records of Set C.
- **Feasibility:** Fully reproducible in under 2 minutes without external downloads.
- **Scientific Caveat:** Must be clearly presented as a separate "Vertical-Only Reference Baseline", distinct from the primary 24-feature 3C models.

---

## 6. Audit Conclusion & Next Action

**Final Verdict:** **C. NOT READY – FEATURE OR DATA INCOMPATIBILITY**

**Recommended Action:**
1. Do not run model inference on Set C in its current state.
2. Present Option A at the IIT Jodhpur evaluation (highlighting the audited Set A ML benchmark and the Set C integrity audit).
3. If the evaluation committee explicitly requests Set C empirical figures, adopt Option C (the 18-feature vertical reference model) as a documented companion experiment.

---
*Report generated and verified against repository state on 2026-11-12.*
