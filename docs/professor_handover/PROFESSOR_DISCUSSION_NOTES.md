# Professor Discussion Notes

Concise answers to likely questions. Each answer is based on repository documents; where the repository does not give the answer, the notes say that the project does not establish it. Navigation: [PROFESSOR_HANDOVER_GUIDE.md](PROFESSOR_HANDOVER_GUIDE.md).

**1. What is the exact research problem?**
Given a pre-cut 4-second window of vertical ground velocity, decide whether it contains the first P-wave arrival or only ambient noise, and compare supervised classifiers (Random Forest, XGBoost) with an STA/LTA threshold rule on earthquakes the classifiers have not seen. It is a window-classification benchmark, not continuous detection ([methodology](RESEARCH_METHODOLOGY.md)).

**2. Why did we use California first?**
The project charter records the professor's requirements: download data with ObsPy, use IRIS/EarthScope for USA events, and build a project with real datasets, waveform analysis, graphs and tables. California served as the completed pilot and methods laboratory; v1.0.0 is its frozen submission ([PROJECT_CHARTER.md](../PROJECT_CHARTER.md), [RESEARCH_DIRECTION.md](../RESEARCH_DIRECTION.md)).

**3. Why did we move to Swiss seismic data?**
The charter names Europe as the primary long-term focus, and California as the experimental pilot. Switzerland adds three-component and vertical broadband records with SED manual first-P picks, which are labels independent of the STA/LTA detector. California had automatic STA/LTA picks only, so supervised labels were not independent there ([SWISS_ML_FEASIBILITY_AUDIT.md](../SWISS_ML_FEASIBILITY_AUDIT.md), STEP ML-1A in [PROJECT_STATUS.md](../PROJECT_STATUS.md)).

**4. What is the difference between Set A and Set C?**
Set A: 20 events, 120 three-component records, 54 stations, 240 windows; used for development, training and cross-validation. Set C: 15 events, 550 vertical-only records, 79 stations, 1,100 windows; used once for independent evaluation. No shared events; all Set A stations also occur in Set C.

**5. Why do we have only 20 events in Set A?**
The 20 event IDs were taken from an earlier feasibility audit and acquired as a fixed list (6 stations each). The repository does not document why the number is 20 or why those events were chosen. Twenty events is small, and this is a limitation ([limitations A1, B2](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md)).

**6. Why does Set C have 15 events?**
The audit configuration sets 15 proposed events with year quotas 4/4/4/3, at least 6 in Swiss territory, a 15 km minimum separation and magnitude bins, chosen without ranking by detector performance. The project does not document why 15 rather than another number, nor the exact ranking steps behind the final IDs. 9 of the 15 are border events ([DATA_COLLECTION_AND_ANALYSIS_REPORT.md](../DATA_COLLECTION_AND_ANALYSIS_REPORT.md) section 4.3).

**7. Why are the records not equivalent to independent earthquakes?**
A record is one station's recording of one earthquake; windows from the same earthquake share source and path. There are 20 and 15 earthquakes behind 120 and 550 records and 240 and 1,100 windows. That is why validation is grouped by event.

**8. Why does Set C use only HHZ?**
The Set C acquisition rule downloaded the vertical channel for every station with a same-station first-P pick, consistent with the frozen STEP 2K detector, which uses HHZ. Horizontal channels were not requested. The repository records no other reason. As a result the three-component features cannot be computed for Set C, and a separate 18-feature vertical model was needed. Acquiring HHN/HHE is a documented option that was not carried out ([SET_C_ML_COMPATIBILITY_AUDIT.md](../../reports/ml/SET_C_ML_COMPATIBILITY_AUDIT.md)).

**9. Why were Random Forest and XGBoost selected?**
They are tree ensembles for small tabular data; the project notes say tree-based models suit 240 windows and that deep networks would need regularisation or augmentation ([PROJECT_STATUS.md](../PROJECT_STATUS.md) STEP ML-2, [ML_RESULTS_REPORT.md](../ML_RESULTS_REPORT.md) limitations). No systematic comparison against other model families is recorded, so the project does not establish that these are the best choice.

**10. Why was a CNN not implemented?**
A 1D CNN was listed as a possible step in earlier status notes, but only Random Forest and XGBoost were implemented. The ML-3 report states that a CNN would need data augmentation or transfer learning at this sample size. The repository does not record a further decision; the project did not test a CNN.

**11. What is Leave-One-Group-Out cross-validation?**
The data are split into 20 groups, one per earthquake. In each of 20 folds one earthquake (all its stations and windows) is the test set and the other 19 are the training set. Scores are pooled over the folds. See [Fig. 6](../../reports/figures/final/fig06_logo_cross_validation.png).

**12. How did we avoid event-level data leakage?**
Cross-validation groups by `short_id` so no earthquake appears in both training and test folds; Set C events are different from Set A events (0 overlap) and Set C was never used for training, selection or thresholding. What this does not exclude: shared stations, the Set A-derived threshold 8.0, the preprocessing differences, and the full-trace zero-phase filter. The integrity audit found no event leakage but did not quantify these ([FINAL_INTEGRITY_CHECK.md](../../FINAL_INTEGRITY_CHECK.md)).

**13. What do precision and recall mean here?**
Positive means a P-wave window. Precision is the fraction of windows flagged as P-wave that are P-wave; recall is the fraction of P-wave windows that are found. On Set C, XGBoost has precision 0.9915 and recall 0.8527 (4 false positives, 81 false negatives); the window-level baseline has precision 1.0000 and recall 0.3345 (0 and 366).

**14. Why is Set C evaluation important?**
Cross-validation within Set A tests generalisation to new earthquakes inside one dataset. Set C tests frozen models on 15 different earthquakes recorded at 79 stations, acquired later and by a separate rule. Scores fall from F1 about 0.98 (Set A, 18 features) to about 0.91 (Set C); the reason is not established.

**15. Why are the models not operational early-warning systems?**
They classify pre-cut windows aligned to analyst picks. They do not scan continuous data, estimate magnitude or location, measure warning time, or have a measured false-alert rate. The filter is zero-phase over full traces, which is not causal. No real-time test was done.

**16. What are the main scientific limitations?**
Few events; shared stations; vertical-only Set C; STA window and pre-filter differences; full-trace zero-phase filtering; unverified noise-window cleanliness; no confidence intervals; no operational test ([full list](RESEARCH_LIMITATIONS_AND_OPEN_QUESTIONS.md)).

**17. What additional data would strengthen the research?**
More independent earthquakes and stations; station-held-out splits; horizontal channels for Set C; continuous recordings with labelled events and long noise periods; further regions. These are options, not done.

**18. What would be the next research phase?**
The roadmap lists European network expansion, streaming tests and optional EarthESND work ([ROADMAP.md](../ROADMAP.md)). Before that, the open scientific checks are the sensitivity of Set C scores to the STA window, pre-filter and filter differences, and a causal-filter re-evaluation. None has been carried out.
