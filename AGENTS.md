# AGENTS.md

Cursor and other AI agents must follow:

1. **[docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md)**  
2. **[docs/AI_AGENT.md](docs/AI_AGENT.md)**  
3. **[docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md)**  

**v1.0 submission complete (2026-07-29):** EarthESND literature track documented; California IRIS pilot; EDA; signal analysis; preprocessing; feature engineering; results & discussion; D-S1/D-S2; final report; presentation; **FINAL_SUBMISSION** (validation **PASS**). See [RELEASE_SUMMARY_v1.0.md](RELEASE_SUMMARY_v1.0.md).

**Version 2.0 platform (2026-08-02):** Interactive website in `website/` — **complete** (v2.0.0). See [docs/V2_RELEASE_NOTES.md](docs/V2_RELEASE_NOTES.md) and [website/README.md](website/README.md).

**STEP ML-4 complete (2026-11-12):** Vertical-only 18-feature Random Forest (Set C F1=0.9125, AUC=0.9767) and XGBoost (Set C F1=0.9169, AUC=0.9780) trained on Swiss Set A and independently evaluated on Swiss Set C (N=1,100, 15 events). Missed P-wave windows fell by 77.9% (XGBoost) and 76.5% (Random Forest) vs the ML-4 window-level STA/LTA baseline (distinct from the STEP 2K detector). Independence is event-level: all 54 Set A stations also appear in Set C. `sta_lta_*` features use STA 0.5 s (Set A) vs 1.0 s (Set C); impact unverified. Offline benchmark, not operational EEW. 89/89 tests pass (as documented). v1.0.0 = frozen submission release; v1.8.0 = internal documentation milestone. See [docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md](docs/SET_C_VERTICAL_ML_EVALUATION_REPORT.md) and [reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md](reports/ml/STEP_ML4_COMPREHENSIVE_REPORT.md).

**Future work:** [docs/ROADMAP.md](docs/ROADMAP.md) — Version 2.1 (platform maintenance) and Version 3.0. Swiss Set C STA/LTA validation is **frozen** (STEP 2K). 24-feature Set A models (`swiss_rf_model.joblib`, `swiss_xgb_model.joblib`) are **frozen**. Certificate wrap: [docs/AI_ML_CERTIFICATE_WRAP.md](docs/AI_ML_CERTIFICATE_WRAP.md). EarthESND is **reference only**.
