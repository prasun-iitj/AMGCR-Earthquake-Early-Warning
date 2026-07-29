# GitHub Release Notes — v1.0.0 (Submission Release)

**Tag:** `v1.0.0`  
**Project:** AMGCR Earthquake Research  
**Date:** 29 July 2026  

Overview: [RELEASE_SUMMARY_v1.0.md](../RELEASE_SUMMARY_v1.0.md)

---

## Summary

Official **v1.0.0 Submission Release** for the Swiss certificate programme: completed **California FDSN pilot** (acquisition → **8×18** feature matrix), full analysis documentation, formal **D-F1–F4** and **D-S1/S2** deliverables, and **validation PASS**.

---

## Deliverables in `FINAL_SUBMISSION/`

| Asset | Description |
|-------|-------------|
| `Research_Report_Final.pdf` / `.docx` | D-F1 final research report |
| `Presentation.pptx` / `Presentation.pdf` | D-F2 oral presentation (24 slides) |
| `Presentation_Script.pdf` / `.docx` | D-F3 speaker script |
| `REPRODUCIBILITY_STATEMENT.pdf` | D-S1 |
| `DATA_AVAILABILITY_STATEMENT.pdf` | D-S2 |
| `VALIDATION_SUMMARY.md` / `.json` | Automated artefact check (**PASS**) |

---

## Repository science (frozen 2026-07-29)

- California manifest: `data/manifests/iris_california_pilot_events.csv`
- Analysis artefacts: `reports/tables/`, `reports/features/`, JSON/NPZ summaries
- Phase documentation: `docs/IRIS_DATASET_REPORT.md` through `docs/RESULTS_AND_DISCUSSION.md`
- EarthESND reference in `src/` — **complete**; not part of California pilot results

---

## Known packaging notes

- **`reports/figures/*.png`**, **`data/raw/`**, and **`logs/`** may be excluded by `.gitignore`. Regenerate per [docs/REPRODUCIBILITY_STATEMENT.md](../docs/REPRODUCIBILITY_STATEMENT.md) or use PDFs in this folder.
- **Version 2.0** (website, Europe, ML, streaming, deployment): [docs/ROADMAP.md](../docs/ROADMAP.md)

---

## Suggested tag message

```text
v1.0.0 — AMGCR certificate submission release (D-F1–F4, D-S1–S2, validation PASS)
```

---

**Version:** 1.0.0
