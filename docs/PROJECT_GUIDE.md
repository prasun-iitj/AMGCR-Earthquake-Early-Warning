# PROJECT_GUIDE.md

Master operating guide for **AMGCR_Earthquake_Research**.

**Authoritative definition:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md).  
**Release:** **v1.0.0 — Submission Release** (29 July 2026)

---

## Project vision

Reproducible **AI-assisted EEW** research for **Western regions**: **Europe** as programme focus, **California** as **completed pilot**. EarthESND = **reference only**. **v1.0 submission is complete.**

---

## Current status (synchronized)

| Component | Status |
|-----------|--------|
| EarthESND literature / optional track | ✅ Documented |
| USA / California IRIS pilot | ✅ Complete |
| EDA · Signal · Preprocessing · Features | ✅ Complete |
| Results & discussion | ✅ Complete |
| D-S1 / D-S2 statements | ✅ Complete |
| Final report & FINAL_SUBMISSION | ✅ Complete |
| Validation | ✅ PASS |

**Active stage:** **Version 2.0 platform live** (2026-08-02) — see [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md) and [website/README.md](../website/README.md). **Future work:** [ROADMAP.md](ROADMAP.md) (v2.1 / v3.0).

Primary narrative: [Research_Report_Final.md](../reports/Research_Report_Final.md) · Package: [FINAL_SUBMISSION/](../FINAL_SUBMISSION/)

Details: [PROJECT_STATUS.md](PROJECT_STATUS.md) · Summary: [RELEASE_SUMMARY_v1.0.md](../RELEASE_SUMMARY_v1.0.md)

---

## Repository layout

```text
FINAL_SUBMISSION/        # v1.0 official PDF/DOCX/PPTX
data/manifests/          # Event CSV (tracked)
data/raw/iris/           # MiniSEED (local; gitignored)
docs/                    # Charter, phase reports, statements
reports/                 # Final report, figures, tables, presentation
scripts/download/        # Acquisition (executed)
scripts/analysis/        # EDA → features (frozen)
src/                     # acquisition + EarthESND reference
website/                 # Version 2.0 interactive platform (Next.js)
```

---

## AI agents

Read [AI_AGENT.md](AI_AGENT.md) and [PROJECT_CHARTER.md](PROJECT_CHARTER.md) before changes. **Do not** alter v1.0 science without explicit approval.

---

Version: **1.4.0** (v2.0.0 platform release · science v1.0.0 frozen)
