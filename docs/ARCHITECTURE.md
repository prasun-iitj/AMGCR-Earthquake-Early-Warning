# ARCHITECTURE.md

High-level architecture for **AMGCR Earthquake Research**: Western-region EEW research with an **EarthESND reference** layer.

**Scope:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md)

---

## Implementation status

| Layer | Status |
|-------|--------|
| EarthESND reference (`src/models/`, configs, tests) | ✅ **Complete** |
| USA FDSN pilot (`data/raw/iris/`, manifest) | ✅ **Complete** |
| Analysis pipeline (EDA → features) | ✅ **Complete** |
| Interpretation & proposal | ✅ **Complete** |

---

## Dual tracks

```text
┌──────────────────────────────────────────────────────────────┐
│  CERTIFICATE RESEARCH (complete pilot + proposal)             │
│  FDSN → reports/ → docs/*_REPORT.md → Research_Proposal_v1  │
└──────────────────────────────────────────────────────────────┘
                              │  optional comparison
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
reports/Research_Proposal_v1.md
```

Analysis scripts are **standalone** from EarthESND `src/`.

---

## Future architecture (planned)

```text
European FDSN → same report layout → cross-region evaluation
AI models (Western data) ↔ optional EarthESND-inspired benchmarks
Real-time EEW stream → latency + onsite features
```

---

## Core paths

| Path | Role |
|------|------|
| `data/raw/iris/` | Immutable pilot MiniSEED |
| `data/manifests/` | Event metadata |
| `reports/eda/`, `signal_analysis/`, `preprocessing/`, `features/` | Phase outputs |
| `reports/figures/`, `reports/tables/` | Publication artefacts |
| `reports/Research_Proposal_v1.md` | Deliverable 1 |
| `configs/earthesnd/`, `src/models/` | Reference only |

---

## Design principles

- **Modular** — pilot analysis separate from EarthESND benchmark  
- **Reproducible** — manifests, JSON configs, versioned docs  
- **Europe-forward** — pilot validates method; EU data is next geography  
- **Documentation-first** — status in PROJECT_STATUS / CHARTER  

---

Version: **1.2.0**
