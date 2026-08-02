# ARCHITECTURE.md

High-level architecture for **AMGCR Earthquake Research**: Western-region EEW research with an **EarthESND reference** layer.

**Scope:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md)  
**Release:** **v1.0.0 — Submission Release** (29 July 2026)

---

## Implementation status

| Layer | Status |
|-------|--------|
| EarthESND reference (`src/models/` stub, optional track) | ✅ **Documented** (not in v1.0.0 tree) |
| USA FDSN pilot (`data/manifests/`, local `data/raw/iris/`) | ✅ **Complete** |
| Analysis pipeline (EDA → features) | ✅ **Complete** |
| Interpretation & submission deliverables | ✅ **Complete** |
| FINAL_SUBMISSION exports | ✅ **Complete** (validation **PASS**) |

---

## Dual tracks

```text
┌──────────────────────────────────────────────────────────────┐
│  v1.0 CERTIFICATE RESEARCH (complete, frozen 2026-07-29)    │
│  FDSN → reports/ → docs/*_REPORT.md → Research_Report_Final │
│  → FINAL_SUBMISSION/ (PDF, PPTX, D-S1/S2)                     │
└──────────────────────────────────────────────────────────────┘
                              │  optional comparison (v2.0)
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  REFERENCE: EarthESND (Japan-oriented literature benchmark)   │
└──────────────────────────────────────────────────────────────┘
```

---

## Completed data flow (California pilot)

```text
scripts/download/download_iris_california_pilot.py
      → data/raw/iris/ + data/manifests/
      → docs/IRIS_DATASET_REPORT.md

scripts/analysis/
      run_california_pilot_eda.py           → reports/eda/
      run_california_signal_analysis.py     → reports/signal_analysis/
      run_california_preprocessing.py       → reports/preprocessing/
      run_california_feature_engineering.py → reports/features/

docs/EDA_REPORT.md … FEATURE_ENGINEERING_REPORT.md
docs/RESULTS_AND_DISCUSSION.md
reports/Research_Report_Final.md
FINAL_SUBMISSION/  (exported artefacts)
```

Analysis scripts are **standalone** from EarthESND `src/`.

---

## Version 2.0 architecture (implemented)

**Status:** Complete — see [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md) and live implementation in `website/`.

The v2.0 platform adds a **static Next.js site** that reads repository Markdown and synced artefacts at build time. No changes to v1.0 analysis modules.

**Future:** Version 2.1 maintenance; Version 3.0 science expansion — [ROADMAP.md](ROADMAP.md).

```text
✅ Web / dashboard / interactive viz  →  website/ v2.0.0 (complete)
⬜ European FDSN → same report layout → cross-region evaluation (v3.0)
⬜ AI models (Western data) ↔ EarthESND-inspired benchmarks (v3.0)
⬜ Real-time stream (SeedLink) → latency + onsite features (v3.0)
⬜ Production deployment layer (operations, governance) (v3.0)
```

Details: [ROADMAP.md](ROADMAP.md).

---

## Core paths

| Path | Role |
|------|------|
| `FINAL_SUBMISSION/` | Official v1.0 PDF/DOCX/PPTX bundle |
| `data/manifests/` | Event metadata (tracked) |
| `data/raw/iris/` | Immutable pilot MiniSEED (local; gitignored) |
| `reports/eda/`, `signal_analysis/`, `preprocessing/`, `features/` | Phase outputs |
| `reports/figures/`, `reports/tables/` | Publication artefacts (figures often gitignored) |
| `reports/Research_Report_Final.md` | Primary submission narrative (D-F1) |
| `reports/Research_Proposal_v1.md` | Superseded proposal v1 |
| `configs/` | Acquisition and project YAML |

---

## Design principles

- **Modular** — pilot analysis separate from EarthESND benchmark  
- **Reproducible** — manifests, JSON configs, D-S1/D-S2  
- **Europe-forward** — pilot validates method; Version 3.0 targets EU data and ops  
- **Documentation-first** — status in PROJECT_STATUS / CHARTER / RELEASE_SUMMARY  

---

Version: **1.3.0** (v1.0.0 submission release)
