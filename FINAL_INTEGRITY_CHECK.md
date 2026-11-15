# FINAL INTEGRITY CHECK: AMGCR (ML-1A to ML-4)

Date: 2026-11-12. Read-only audit of existing artifacts. Nothing was retrained, reprocessed or modified, and the test suite was not run.

## 1. Feature importance

**Status: INCONSISTENT**

**Finding:** The saved models and the JSON summaries agree. Both lead with `z_spectral_entropy` (RF 0.1937, XGB 0.3791), then `z_spectral_centroid_hz` (RF 0.1511, XGB 0.1913). `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md` §6 is correct for ranks 1–5 but wrong for ranks 6–8. `reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md` §7 uses feature names not in the schema (`z_stalta_max`, `z_dominant_freq_hz`) and wrong values.

Actual ranks 6–9:

| Rank | RF | XGB |
|---|---|---|
| 6 | `z_peak_velocity_m_s` 0.0782 | `z_peak_velocity_m_s` 0.0521 |
| 7 | `z_zero_crossing_rate_hz` 0.0510 | `z_kurtosis` 0.0259 |
| 8 | `z_spectral_rolloff_95_hz` 0.0405 | `z_zero_crossing_rate_hz` 0.0183 |
| 9 | `sta_lta_max` 0.0387 | `z_signal_energy_m2_s` 0.0162 |

**Source:**
- `reports/ml/vertical_rf_model_set_a.joblib` and `vertical_xgb_model_set_a.joblib` (`feature_importances_`)
- `reports/ml/vertical_set_c_evaluation_summary.json`
- `reports/ml/vertical_set_a_evaluation_summary.json`

**Correction:** Fix §7 of the comprehensive report and ranks 6–8 of §6 in the evaluation report, using the artifact values. The artifacts are authoritative.

## 2. 18-feature schema

**Status: INCONSISTENT** (names and order agree; a feature definition differs between training and Set C)

**Finding:** The 18 names and their order are identical in `VERTICAL_FEATURE_COLUMNS`, `vertical_feature_schema.json`, the `feature_columns` stored in both `.joblib` files, and the Set C inference call. Both models report 18 input features. However, `sta_lta_max` and `sta_lta_mean` use STA = 0.5 s in the Set A extraction and STA = 1.0 s in the Set C extraction. The reports claim "identical preprocessing". The comprehensive report's 24-feature list (§3.1) also has wrong names, omits `z_std` and lists `z_cav` twice.

**Source:**
- `src/models/vertical_models.py`
- `reports/ml/vertical_feature_schema.json`
- `scripts/analysis/run_swiss_set_a_feature_engineering.py` (`STA_WINDOW_S = 0.5`)
- `scripts/analysis/run_swiss_set_c_feature_engineering.py` (`STA_WINDOW_S = 1.0`)
- `scripts/ml/evaluate_vertical_models_set_c.py`

**Correction:**
- Disclose the STA window mismatch and remove or qualify "identical preprocessing".
- Fix the comprehensive report §3.
- The effect of the mismatch on the Set C metrics is NOT VERIFIED. Quantifying it would require re-extraction, which is out of scope.

## 3. Dataset independence

**Status: VERIFIED for events; stations are NOT unseen**

**Finding:** Set A has 20 events and 54 stations. Set C has 15 events and 79 stations. The two sets share no events and no short IDs. All 54 Set A stations also appear in Set C (54 of 79 shared, 25 Set C only). Event-level independence is proven; station-level independence is not.

**Source:**
- `reports/features/swiss_set_a_feature_matrix.csv`
- `reports/features/swiss_set_c_feature_matrix.csv`
- `data/manifests/sed_switzerland_validation_waveforms.csv` (550 rows)
- `data/manifests/sed_switzerland_set_a_picks.csv` (120 rows)

**Correction:** In `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md` §1 and the comprehensive report, replace "79 completely distinct/different stations" with "15 unseen events; 54 of 79 stations also appear in Set A". Do not claim unseen stations.

## 4. STA/LTA threshold 8.0

**Status: NOT VERIFIED** for "frozen before Set C evaluation" by version control. The origin is VERIFIED.

**Finding:**
- **Origin:** 8.0 was selected from a threshold grid on the 20-event Set A (120 records) using a pre-written rule (lowest threshold with noise-record fraction below 0.25 and post-origin coverage at least 0.75). It is not the California threshold, which was 2.5.
- **Freeze:** The plan, configs and results docs state it was pre-declared and not retuned. Git cannot confirm the order, because they all arrive in one commit (`a348316`, 2026-09-12).
- **Baselines:** The ML-4 "STA/LTA" baseline (`sta_lta_max ≥ 8.0`, STA 1.0 s, 4 s windows, recall 0.3345) is a window-level re-implementation. It is not the STEP 2K record-level detector (STA 0.5 s, 401/550 detected, 72.9%).

**Source:**
- `configs/swiss_sta_lta_transfer.yaml` (grid and `proposal_rule`)
- `docs/SWISS_STA_LTA_TRANSFER_ANALYSIS.md` (lines 95, 186–194)
- `docs/SWISS_INDEPENDENT_VALIDATION_PLAN.md`
- `configs/sed_switzerland_validation.yaml`
- `reports/switzerland_validation/validation_summary.json`
- `scripts/ml/evaluate_vertical_models_set_c.py` (`sta_preds = (sta_lta_vals >= 8.0)`)

**Correction:**
- Remove "transferred from California".
- State that 8.0 is Swiss Set A-derived and that the pre-declaration is documented but not git-verifiable.
- Label the ML-4 baseline as distinct from the STEP 2K result.

## 5. Documentation consistency

**Status: INCONSISTENT**

**Finding:**
- **Version labeling:** v1.0.0 is the frozen submission release (29 July 2026): `pyproject.toml`, `CITATION.cff`, `README.md`. v1.8.0 appears only as a documentation counter in the `docs/PROJECT_STATUS.md` footer and the comprehensive report's version table. It is not a software release.
- **Wrong claims:** "77.9% fewer missed detections" applies to XGBoost only (RF is 76.5%). The comprehensive report's per-event magnitudes and distances (§6, §8) differ from the evaluation report §7 and were not checked against the CSV (NOT VERIFIED).
- **Stale files:** `README.md` and `PROJECT_HANDOFF_SUMMARY.md` still say ML is NO-GO.

**Source:**
- `pyproject.toml`
- `CITATION.cff`
- `docs/PROJECT_STATUS.md`
- `reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md`
- `docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md`
- `README.md`
- `PROJECT_HANDOFF_SUMMARY.md`

**Correction:**
- Add a line to `docs/PROJECT_STATUS.md` and `CHANGELOG.md` saying v1.0.0 is the frozen submission release and v1.8.0 is an internal research and documentation milestone.
- Qualify the 77.9% figure as XGBoost.
- Update the stale ML-status statements.

## Verdict

**READY AFTER DOCUMENTATION CORRECTIONS**

No leakage was found, and the headline Set C results are consistent with the saved artifacts. The corrections above are needed before freezing. The STA window mismatch (point 2) is a limitation that must be disclosed; its numerical effect is NOT VERIFIED.

## Addendum (2026-11-15, found while preparing the review package)

**Zero-phase filtering before windowing: DISCLOSED, effect NOT VERIFIED.** `scripts/analysis/run_swiss_set_a_feature_engineering.py` (line 303) and `run_swiss_set_c_feature_engineering.py` (line 208) call `filter("bandpass", ..., corners=4, zerophase=True)` on the full trace and then cut 4 s windows. Window samples are therefore influenced by neighbouring samples, including later ones, so earlier wording such as "zero future sample leakage" applies to window placement only. Positive windows start at the analyst pick; noise windows start at origin - 35 s (same rule in both sets, confirmed in both scripts). Both classes and both sets are treated alike, so this is not evidence of leakage between Set A and Set C, but it means the benchmark is not a causal real-time test. It does not change the verdict.

**Also resolved:** the Set C noise window is origin - 35 s to origin - 31 s, as for Set A (previously listed as not verified). `requirements.txt` lacks scikit-learn, xgboost and joblib; `requirements-ml.txt` was added.
