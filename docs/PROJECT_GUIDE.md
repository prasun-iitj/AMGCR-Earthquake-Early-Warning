# PROJECT_GUIDE.md

Master operating guide for **AMGCR_Earthquake_Research**.

**Authoritative definition:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md).

---

## Project vision

Reproducible **AI-assisted EEW** research for **Western regions**: **Europe** as programme focus, **California** as **completed pilot**. EarthESND = **reference only**.

---

## Current status (synchronized)

| Component | Status |
|-----------|--------|
| EarthESND reference implementation | ✅ Complete |
| USA / California IRIS pilot | ✅ Complete |
| EDA | ✅ Complete |
| Signal analysis | ✅ Complete |
| Preprocessing | ✅ Complete |
| Feature engineering | ✅ Complete |
| Results & discussion | ✅ Complete |
| Research Proposal & Technical Report | ✅ Complete |

**Active stage:** Deliverable 1 — [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md).

**Future work:** European datasets, AI modelling, real-time EEW, comparative evaluation.

Details: [PROJECT_STATUS.md](PROJECT_STATUS.md).

---

## Repository layout

```text
data/raw/iris/           # Pilot MiniSEED
data/manifests/        # Event CSV
docs/                    # Phase reports + charter
reports/                 # Figures, tables, feature matrix, proposal v1
scripts/download/        # Acquisition (executed)
scripts/analysis/        # EDA → features (executed)
src/                     # acquisition + EarthESND reference
```

---

## AI agents

Read [AI_AGENT.md](AI_AGENT.md) and [PROJECT_CHARTER.md](PROJECT_CHARTER.md) before code changes.

---

Version: **1.2.0**
