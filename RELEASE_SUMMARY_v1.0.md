# RELEASE_SUMMARY_v1.0.md

**AMGCR Earthquake Research**  
**GitHub release:** `v1.0.0` (Submission Release)  
**Date:** 29 July 2026  

---

## Project overview

Swiss certificate programme research in **Assessment and Management of Geological and Climate Related Risk (AMGCR)**. The repository delivers a **reproducible, ObsPy/FDSN-based Earthquake Early Warning (EEW) research workflow** with **Europe** as the long-term focus and a **completed California IRIS/EarthScope pilot** (eight events, **8×18** feature matrix). **EarthESND** remains a **complete reference implementation**, not the geographic scientific endpoint.

Authoritative scope: [docs/PROJECT_CHARTER.md](docs/PROJECT_CHARTER.md).

---

## Major accomplishments (v1.0)

| Area | Outcome |
|------|---------|
| Reference software | EarthESND-aligned pipeline in `src/` (**88 tests** on full checkout) |
| Data acquisition | USGS + EarthScope FDSN; manifest + [IRIS_DATASET_REPORT.md](docs/IRIS_DATASET_REPORT.md) |
| Analysis pipeline | EDA → signal (STA/LTA) → preprocessing → features → interpretation |
| Science narrative | Phase reports + [RESULTS_AND_DISCUSSION.md](docs/RESULTS_AND_DISCUSSION.md) |
| Formal reporting | [Research_Report_Final.md](reports/Research_Report_Final.md) (D-F1) |
| Compliance | [REPRODUCIBILITY_STATEMENT.md](docs/REPRODUCIBILITY_STATEMENT.md), [DATA_AVAILABILITY_STATEMENT.md](docs/DATA_AVAILABILITY_STATEMENT.md) |
| Oral defence assets | 24-slide deck + script (D-F2/D-F3) |
| Submission package | [FINAL_SUBMISSION/](FINAL_SUBMISSION/) with PDF/DOCX/PPTX |
| Validation | **PASS** — [VALIDATION_SUMMARY.md](FINAL_SUBMISSION/VALIDATION_SUMMARY.md) |

Pilot science **freeze date:** 2026-07-29. No ML training or operational EEW claims in v1.0.

---

## Repository statistics (indicative)

| Metric | Value |
|--------|--------|
| Git-tracked files | ~113 (at submission tagging) |
| Markdown docs under `docs/` | ~28 tracked |
| California manifest events | **8** |
| Feature matrix | **8 × 18** |
| Pilot figures (`reports/figures/`) | **24** PNG (local/regenerable; often gitignored) |
| Analysis scripts (California) | 4 under `scripts/analysis/` + 1 download script |
| EarthESND tests (full tree) | **88** per charter/README |

---

## Deliverables

| ID | Deliverable | Location |
|----|-------------|----------|
| D-F1 | Final Research Report | `reports/Research_Report_Final.md` · `FINAL_SUBMISSION/Research_Report_Final.pdf` |
| D-F2 | Presentation (24 slides) | `FINAL_SUBMISSION/Presentation.pptx` |
| D-F3 | Presentation script | `reports/Presentation_Script_D-F3.md` · `FINAL_SUBMISSION/Presentation_Script.pdf` |
| D-F4 | Submission bundle | `FINAL_SUBMISSION/` |
| D-S1 | Reproducibility Statement | `docs/REPRODUCIBILITY_STATEMENT.md` · PDF in `FINAL_SUBMISSION/` |
| D-S2 | Data Availability Statement | `docs/DATA_AVAILABILITY_STATEMENT.md` · PDF in `FINAL_SUBMISSION/` |

Supporting: [docs/FINAL_DELIVERABLE_PLAN.md](docs/FINAL_DELIVERABLE_PLAN.md), [docs/FINAL_DELIVERABLE_AUDIT.md](docs/FINAL_DELIVERABLE_AUDIT.md), [FINAL_SUBMISSION/SUBMISSION_CHECKLIST.md](FINAL_SUBMISSION/SUBMISSION_CHECKLIST.md).

---

## Known limitations (documented)

- **N = 8**; single **BHZ**; mixed **mw/ml**; **ADO-heavy** station sampling  
- **Origin-aligned** 300 s windows; SNR and STA/LTA biases  
- **Instrument response removal 0/8** in completed preprocessing run  
- **Unvalidated** automatic P picks  
- Raw MiniSEED, logs, and figures may be **absent from Git clones** (`.gitignore`) — regenerate per D-S1  
- **No European waveform data** or **EarthESND California training** in v1.0  

Details: [Research_Report_Final.md](reports/Research_Report_Final.md) §10–11.

---

## Version 2.0 / future roadmap

Planned extensions (not part of v1.0 submission):

1. **Interactive project website** and **public dashboard**  
2. **Interactive visualisations** for pilot and future catalogues  
3. **Europe dataset expansion** (ORFEUS/EIDA pattern)  
4. **EarthESND model training and evaluation** on Western data (with deviation log)  
5. **Real-time streaming support** (e.g. SeedLink) and latency profiling  
6. **Additional datasets** (scaled California/Western USA, optional K-NET reproduction track)  
7. **Production deployment** considerations (operational EEW integration, governance)  

Full list: [docs/ROADMAP.md](docs/ROADMAP.md) § Version 2.0.

---

## GitHub release

Suggested tag: **`v1.0.0`**  
Release notes template: [FINAL_SUBMISSION/GITHUB_RELEASE_NOTES_v1.0.md](FINAL_SUBMISSION/GITHUB_RELEASE_NOTES_v1.0.md)

---

**Document version:** 1.0.0 (submission summary)
