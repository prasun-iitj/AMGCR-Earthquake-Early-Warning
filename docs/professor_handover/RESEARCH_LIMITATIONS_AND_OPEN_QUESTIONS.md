# Research Limitations and Open Questions

An honest list of what the research does not establish. Not every item can be resolved within this project. Evidence for each item is in the cited files.

## A. Known scientific limitations

1. **Few independent events.** 20 development events and 15 evaluation events. The 240 and 1,100 windows are not independent samples; windows from one earthquake are correlated. Cross-validation and Set C scores come with no confidence intervals in the repository.
2. **Event-level independence only.** No event is shared between Set A and Set C, but all 54 Set A stations also occur in Set C (25 stations are Set C only; 417 of 550 Set C records come from shared stations). Station-specific effects could help the models; this was not tested. Set C must not be described as an unseen-station validation.
3. **Vertical-only Set C.** Horizontal channels were not acquired, so the three-component features (particle motion, V/H ratio, SNR) cannot be used for evaluation. The Set A three-component models were not evaluated on Set C. Option to acquire HHN/HHE is described in `reports/ml/SET_C_ML_COMPATIBILITY_AUDIT.md`; it was not done.
4. **STA window discrepancy.** `sta_lta_max/mean` use STA 0.5 s (Set A) and 1.0 s (Set C). Together these two features carry roughly 0.16 of Random Forest and 0.14 of XGBoost importance. Their effect on the Set C scores is unquantified.
5. **Response pre-filter differences.** The two feature scripts use different cosine pre-filter corners before the same 0.1 to 15 Hz bandpass. Effect unquantified.
6. **Zero-phase full-trace filtering.** Window samples depend on neighbouring samples, including later ones. "Causal windows" refers to window placement only. The pipeline is not shown to be causal and is not suitable for a real-time claim as built.
7. **Pick-aligned windows.** Positive windows start at the analyst pick, so the task is discrimination, not arrival detection. Detection latency and picking error were not measured.
8. **Noise windows not checked.** The origin -35 s to -31 s windows are assumed quiet; no contamination check was found in the code.
9. **`z_cav_m_s` naming.** It is sum(|v|) x dt on velocity and has dimension of length despite its name. It was not renamed or recalculated, to keep saved models and schemas intact.
10. **`snr_db` baseline.** In Set A it uses a vertical-trace RMS from origin -45 s to -15 s of the same record, a period that also contains the negative window. It is excluded from the 18-feature schema.
11. **Threshold 8.0 provenance.** It was derived on Set A (a threshold grid with a pre-written rule). Documents state it was pre-declared before Set C; Git history cannot prove the order. The ML-3 STA/LTA result on Set A is therefore not an independent baseline.
12. **No operational validation.** No real-time or continuous-stream test, no warning time, no live false-alert rate, no magnitude or location estimation. Different seismic regimes were not tested.
13. **Cross-set score drop unexplained.** Set A cross-validation F1 (0.9789 and 0.9832 for the 18-feature models) versus Set C F1 (0.9125 and 0.9169): the reason is not established.

## B. Documentation gaps

1. **California local files.** 12 California MiniSEED files exist locally; 4 are not listed in the manifest (`CI.ADO.--.BHZ.20240823T153158`, `CI.ADO.--.BHZ.20241114T024035`, `CI.ADO.--.BHZ.20241209T230831`, `CI.USC.--.BHZ.20240912T142821`). Their origin is not established in the current repository evidence. The EDA script marks them as outside the manifest.
2. **Set A event selection.** The 20 event IDs were "taken from the prior feasibility audit"; why those 20 is not documented.
3. **Set C ranking.** The diversity rules are in `configs/sed_switzerland_validation_audit.yaml`; the step-by-step ranking that produced exactly these 15 IDs is not documented. The reason for choosing 15 is not documented beyond the configured quota.
4. **Corrections made during this handover (2026-11-15).** `docs/ML_RESULTS_REPORT.md` listed a noise window of origin -14 s to -10 s, a magnitude range of 1.8 to 4.3, depths of 2.2 to 24.3 km, per-event magnitudes and distances, and "17 of 20" perfect XGBoost events. The code, manifest and per-event CSV give origin -35 s to -31 s, magnitude 2.97 to 4.74, depth 0.06 to 25.17 km, per-event values as now listed, and 16 of 20. The report was corrected from those files; no metric changed. `docs/PROJECT_STATUS.md` was corrected for the same XGBoost count and for an "identical preprocessing" statement. Older documents may still contain other unverified descriptive text (for example the historical `reports/ml/ML3_INDEPENDENT_AUDIT.md`), which was not audited line by line.
5. **Historical documents.** `PROJECT_HANDOFF_SUMMARY.md` (repository root, 2026-11-06) and `docs/AI_ML_CERTIFICATE_WRAP.md` (2026-11-11) predate ML-1A to ML-4 and are marked as historical. There is no `docs/PROJECT_HANDOFF_SUMMARY.md`.
6. **Figure cosmetics.** Truncated y-axis and legend overlap in two result figures, a displaced label in one data figure ([guide, Appendix B](PROFESSOR_HANDOVER_GUIDE.md)).
7. **Live site.** Whether https://amgcr-research.vercel.app/ serves the latest commit was not verified.
8. **Browser check.** The website pages were built and checked over HTTP, but not inspected visually in a browser, and mobile layout was not tested.

## C. Data access and licensing

1. **Provider terms not reviewed.** Licence, attribution and redistribution terms of USGS, EarthScope and SED/ETH have not been reviewed in this repository. Raw MiniSEED, StationXML and QuakeML are therefore not published.
2. **External URLs not verified.** The provider and documentation URLs in the documents were read from scripts and configs and not fetched for this handover.
3. **Re-acquisition may differ.** Catalogue, pick, response and availability changes at the providers can alter new downloads. The California acquisition cannot be pinned to the frozen 8 events ([DATA_ACQUISITION_AND_REPRODUCTION.md](../DATA_ACQUISITION_AND_REPRODUCTION.md), sections 3 and 7).
4. **Raw data local only.** Waveform-level verification needs a fresh download.

## D. Future research opportunities (not done)

- Quantify the sensitivity of Set C scores to the STA window and pre-filter differences (re-extract with harmonised settings and compare).
- Replace the zero-phase filter with a causal filter and re-evaluate.
- Acquire HHN/HHE for Set C and evaluate the three-component models.
- Add independent events and stations; report confidence intervals; evaluate with station-held-out splits.
- Test on continuous data and measure latency and false-alert rate.
- Compare with other classifiers, including the deep models mentioned as future options in the ML-3 report, which need more data or transfer learning.
- Extend to further European networks ([ROADMAP.md](../ROADMAP.md)).
