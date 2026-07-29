# FINAL_DELIVERABLE_PLAN.md

**AMGCR Earthquake Research — Final Deliverables phase (execution plan only)**  
**Prepared:** 29 July 2026  
**Scope:** Documentation and packaging for Swiss certificate submission. **No report generation in this step.** **No source-code changes** unless explicitly approved in a later task.

**Authoritative context:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md) · [PROJECT_STATUS.md](PROJECT_STATUS.md) · [RESEARCH_DIRECTION.md](RESEARCH_DIRECTION.md)

---

## Phase positioning

| Item | Status |
|------|--------|
| Pilot science (acquisition → features → interpretation) | **Complete** — phase reports under `docs/` |
| Analysis artefacts | **Complete** — `reports/tables/`, `reports/features/`, JSON/NPZ summaries |
| **Deliverable 1** — Research Proposal v1 | **Complete** — [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md) (superseded by D-F1) |
| **D-F1–F4 final deliverables** | **Complete** — [Research_Report_Final.md](../reports/Research_Report_Final.md), presentation, [FINAL_SUBMISSION/](../FINAL_SUBMISSION/) |
| **D-S1 / D-S2** | **Complete** — [REPRODUCIBILITY_STATEMENT.md](REPRODUCIBILITY_STATEMENT.md), [DATA_AVAILABILITY_STATEMENT.md](DATA_AVAILABILITY_STATEMENT.md) |
| **Validation** | **PASS** — [FINAL_DELIVERABLE_AUDIT.md](FINAL_DELIVERABLE_AUDIT.md), [VALIDATION_SUMMARY.md](../FINAL_SUBMISSION/VALIDATION_SUMMARY.md) |
| **This plan** | **Archived** — execution complete; repository at **v1.0.0 Submission Release** |

Deliverable execution is **complete**. See [RELEASE_SUMMARY_v1.0.md](../RELEASE_SUMMARY_v1.0.md) and Version 2.0 items in [ROADMAP.md](ROADMAP.md).

---

## 1. Deliverables to produce

### 1.1 Primary (certificate-facing)

| ID | Deliverable | Description | Primary inputs |
|----|-------------|-------------|----------------|
| **D-F1** | **Final Research Report** | Submission-ready document: full narrative, embedded figures/tables, consistent numbering, front matter (title, abstract, keywords, programme affiliation), references, appendices. Evolves **v1** → **final** (e.g. `reports/Research_Report_Final.md` or export-only PDF). | `Research_Proposal_v1.md`, phase reports §1–12, `reports/figures/`, `reports/tables/` |
| **D-F2** | **Presentation deck** | Oral defence / programme presentation: motivation, European framing, California pilot workflow, key results, limitations, future work. Speaker notes optional. | Same as D-F1; select ~12–15 “hero” figures |
| **D-F1-A** | **Executive summary** (1–2 pages) | Standalone synopsis for reviewers who will not read the full report: goal, methods, main findings, limitations, Europe transfer. Can be §0 of D-F1 or separate PDF. | Abstract + `RESULTS_AND_DISCUSSION.md` §11 |
| **D-F3** | **Figure and table pack** | Curated, captioned set aligned with report numbering (Figure 1…, Table 1…). Ensures every in-text reference resolves to an embedded or appendix asset. | Appendix A index in v1; EDA/signal/preprocessing/feature reports |
| **D-F4** | **Submission archive** | Zip or tagged release: final report export, slides, manifest CSV, key tables, README pointer, **no** large raw MiniSEED unless programme requires (prefer manifest + instructions to reproduce). | Repo root README, `data/manifests/iris_california_pilot_events.csv` |

### 1.2 Supporting (quality and compliance)

| ID | Deliverable | Description |
|----|-------------|-------------|
| **D-S1** | **Reproducibility appendix** | One-page command block: download → EDA → signal → preprocessing → features (PowerShell paths from phase reports). States Python/env assumptions. |
| **D-S2** | **Data availability & ethics statement** | FDSN sources (USGS, EarthScope), citation URLs, limitation that raw data live under `data/raw/iris/`; no personal data. |
| **D-S3** | **Document control sheet** | Version, date, author, list of included commit hash or tag, changelog entry for final submission. |
| **D-S4** | **Documentation sync pass** | Update [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) (still lists Phase B/C as open) and cross-links in README/ROADMAP to **Final Deliverables complete** when done. *Documentation only; not source code.* |

### 1.3 Explicitly out of scope for this final phase (unless programme mandates)

- New FDSN downloads, re-running analysis scripts, or fixing instrument response in code  
- European pilot acquisition, AI training, real-time EEW prototype  
- EarthESND K-NET scientific reproduction (reference track only)  
- Generating the full report body in this planning step (user requested plan only)

---

## 2. Recommended order of work

```text
1. Gap audit          → Compare D-F1 outline vs v1 + professor checklist (§4 below)
2. Figure/table audit → Verify all PNG/CSV exist; map to Figure/Table numbers (D-F3)
3. Draft D-F1         → Merge v1 + missing sections; embed selected figures (not path-only refs)
4. D-F1-A             → Executive summary from frozen results
5. D-S1, D-S2         → Appendices and statements
6. Export D-F1        → PDF/DOCX per programme template (if provided)
7. D-F2               → Slides distilled from D-F1 storyline
8. D-F4 + D-S3        → Archive, version tag, checklist sign-off
9. D-S4               → Doc sync (IMPLEMENTATION_PLAN, PROJECT_STATUS, CHANGELOG)
```

**Rationale:** Lock **artefact inventory** before writing so the final report does not reference missing figures. **Slides last** so they match the frozen report numbering and wording.

---

## 3. Existing material that can be reused

### 3.1 Narrative (copy-edit and restructure; do not recompute)

| Source | Reuse for |
|--------|-----------|
| [Research_Proposal_v1.md](../reports/Research_Proposal_v1.md) | **Backbone** of D-F1: Abstract, Introduction, Literature, Gap, Objectives, Dataset, Methodology, Workflow, Results, Europe, Expected outcomes, Future work, References, Appendix A index |
| [RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md) | Deeper interpretation, validity threats (§7), conclusions (§11), Europe transfer (§9) — lift into Results/Discussion and Limitations |
| [IRIS_DATASET_REPORT.md](IRIS_DATASET_REPORT.md) | Dataset chapter: FDSN endpoints, query params, 8-event table, stations, limitations |
| [EDA_REPORT.md](EDA_REPORT.md) | Dataset summary stats, manifest vs disk note, EDA figure captions |
| [SIGNAL_ANALYSIS_REPORT.md](SIGNAL_ANALYSIS_REPORT.md) | STA/LTA method, aggregate metrics, per-event interpretation, noise-window caveat |
| [PREPROCESSING_REPORT.md](PREPROCESSING_REPORT.md) | EEW rationale per step, parameters, **0/8 response removal** limitation, quality table narrative |
| [FEATURE_ENGINEERING_REPORT.md](FEATURE_ENGINEERING_REPORT.md) | 8×18 catalogue, EEW relevance table, correlation/collinearity narrative |
| [RESEARCH_DIRECTION.md](RESEARCH_DIRECTION.md) | Short “project evolution” box (EarthESND reference vs active research) |
| [PROJECT_CHARTER.md](PROJECT_CHARTER.md) §4 | Professor requirements compliance matrix in checklist |

### 3.2 Quantitative artefacts (cite or paste as tables; no regeneration required)

| Path | Content |
|------|---------|
| `data/manifests/iris_california_pilot_events.csv` | Event list |
| `reports/tables/event_summary.csv`, `station_summary.csv` | Proposal Dataset tables |
| `reports/tables/signal_analysis_per_event.csv` | Signal results |
| `reports/tables/preprocessing_quality_metrics.csv` | Preprocessing QC |
| `reports/features/feature_matrix.csv`, `reports/tables/feature_correlation_matrix.csv` | Features |
| `reports/eda/dataset_summary.json`, `reports/signal_analysis/signal_analysis_summary.json`, `reports/preprocessing/preprocessing_summary.json`, `reports/features/feature_summary.json` | Numeric quotes for text |

### 3.3 Figures (documented index — reuse in D-F1/D-F2)

Per v1 Appendix A and phase reports (~**24 PNG** under `reports/figures/` when analysis has been run):

- **EDA (4):** `example_waveform_raw.png`, `magnitude_histogram.png`, `events_over_time.png`, `station_usage_frequency.png`
- **Signal (8):** `signal_analysis_<event>.png`
- **Preprocessing (8):** `preprocessing_<event>.png`
- **Features (4):** `feature_engineering_fft_spectra.png`, `feature_correlation_heatmap.png`, `feature_distributions.png`, `feature_boxplots_by_station.png`

**Slide subset (recommended):** 1 raw waveform, 1 STA/LTA panel (best SNR event), 1 preprocessing 4-panel, FFT grid, correlation heatmap, station usage, events over time, workflow diagram (new schematic).

### 3.4 Reference / background (cite only)

- EarthESND paper summary: [REFERENCES.md](../references/REFERENCES.md), `references/papers/`, `configs/earthesnd/`
- ObsPy/FDSN: references already in v1 §12
- Optional architecture diagram: adapt from [ARCHITECTURE.md](ARCHITECTURE.md) (documentation diagram, not code)

---

## 4. Missing or weak sections (for D-F1 final)

Sections **present in v1 or phase docs** but needing **final-phase treatment**:

| Gap | Action |
|-----|--------|
| **Inline figures** | v1 references paths; final report must **embed** or appendix-link every cited figure with captions matching phase reports |
| **Dedicated Limitations chapter** | Consolidate preprocessing response failure, origin-aligned noise, N=8, ADO bias, mixed M types, unvalidated P picks (`RESULTS_AND_DISCUSSION` §6–7) |
| **Conclusions** | Short numbered list (already in `RESULTS_AND_DISCUSSION` §11); ensure not buried inside Discussion only |
| **Personal / programme front matter** | Author name, CERG/AMGCR edition, submission date, declaration of originality (template from programme if available) |
| **Acknowledgements** | Supervisor, EarthScope/USGS data providers, ObsPy community |
| **List of figures / list of tables** | Auto from final numbering |
| **Methodology detail depth** | Optional: single workflow figure (mermaid or static) — v1 has text pipeline; slides need one visual |
| **EarthESND boundary** | One explicit paragraph: reference code complete, **not** evaluated on California pilot — avoid reviewer confusion |
| **IMPLEMENTATION_PLAN.md** | **Stale** (Part 4–5 still show open phases); sync in D-S4 |
| **Figure artefact verification** | Confirm all PNGs exist on disk before export; re-run analysis scripts only if audit fails (user currently forbids code change — **verify first**) |

Sections **professor checklist** ([PROJECT_CHARTER](PROJECT_CHARTER.md) §4) — coverage map:

| Requirement | Where covered | Final action |
|-------------|---------------|--------------|
| Theory | v1 §2 Literature, §6 Methodology, preprocessing EEW table | Keep; optional ½-page EEW primer |
| Real datasets | IRIS report + v1 §5 | Embed event table |
| Waveform analysis | Signal + preprocessing reports | Embed 2–3 waveform figures |
| Graphs and tables | `reports/figures/`, `reports/tables/` | D-F3 pack |
| Literature review | v1 §2 | Expand only if page minimum requires |
| Introduction | v1 §1 | Minor polish |
| Dataset | v1 §5 | Align with manifest |
| Methodology | v1 §6–7 | Add workflow figure |
| Expected outcomes | v1 §10–11 | Split **achieved** vs **proposed** clearly |

**Not required for certificate narrative (future work):** European pilot data, ML experiment results, real-time latency measurements.

---

## 5. Estimated page count (final research report)

Estimates assume **A4**, **11–12 pt**, **1.5 line spacing**, body text plus **embedded figures** (not separate figure volume).

| Component | Pages (approx.) |
|-----------|-----------------|
| Front matter (title, abstract, TOC, lists) | 3–4 |
| Introduction + literature + gap + objectives | 6–8 |
| Dataset + methodology + workflow | 6–8 |
| Results & discussion (with 8–12 embedded figures) | 10–14 |
| Europe relevance + expected outcomes + future work | 4–6 |
| Limitations + conclusions | 2–3 |
| References | 2–3 |
| Appendices (reproducibility, full event table, optional 1–2 extra plots) | 3–6 |
| **Total D-F1 (main report)** | **36–52 pages** |

**Practical targets:**

- **Minimum credible certificate report:** ~**25–30 pages** (body) if figure count is capped (~8 figures) and appendices trimmed.  
- **Recommended (matches current artefact richness):** ~**40–45 pages** with ~12–15 figures and 4–6 tables.  
- **Executive summary (D-F1-A):** **2 pages** max.

*Baseline:* v1 markdown is ~**380 lines** (~**6,000–7,500 words**); figures add the majority of page count in PDF export.

---

## 6. Estimated slides (presentation)

Target: **20–25 minutes** certificate presentation.

| Block | Slides |
|-------|--------|
| Title, context (AMGCR / EEW / Europe focus) | 2 |
| Motivation & research questions | 2 |
| Literature & gap (incl. EarthESND as reference only) | 2–3 |
| Dataset (California pilot, FDSN, N=8) | 2 |
| Methodology pipeline (one diagram + STA/LTA + preprocessing) | 3–4 |
| Results (EDA, signal, features — key figures) | 5–6 |
| Limitations (response, noise window, bias) | 2 |
| Europe transfer & future work | 2–3 |
| Conclusions & thank you / Q&A | 1–2 |
| **Total** | **22–28 slides** |

**Recommended default:** **24 slides** (+ optional backup slides: extra preprocessing example, feature correlation, charter roadmap).

---

## 7. Final submission checklist

### 7.1 Content completeness

- [ ] All professor-required sections present (Introduction, Dataset, Methodology, Expected outcomes, literature, theory, waveforms, graphs/tables)
- [ ] Europe as **primary programme focus**; California as **completed pilot** — wording consistent with charter
- [ ] EarthESND described as **reference implementation**, not primary result
- [ ] Every limitation explicitly stated: **N=8**, **BHZ only**, **origin-aligned windows**, **0/8 response removal**, **ADO station bias**, **approximate P picks**
- [ ] No claim of operational EEW deployment or magnitude prediction accuracy (no ML training was run on pilot)
- [ ] References include FDSN, EarthScope, USGS, ORFEUS/EIDA, ObsPy, key EEW papers (as in v1 §12)

### 7.2 Artefacts and reproducibility

- [ ] `data/manifests/iris_california_pilot_events.csv` matches report event list
- [ ] All figures cited in report exist under `reports/figures/` (or appendix explains omission)
- [ ] Table numbers match `reports/tables/` and feature matrix
- [ ] Reproducibility appendix lists four analysis scripts + download script (paths only; no code change)
- [ ] JSON summary statistics quoted in text match files in `reports/*/`

### 7.3 Document quality

- [ ] Consistent figure/table numbering and captions (source: phase reports)
- [ ] Spell-check and notation (M_w, M_l, Hz, SNR, STA/LTA)
- [ ] PDF/DOCX export: fonts, margins, page numbers per programme rules
- [ ] Executive summary readable standalone
- [ ] Document control: version **final**, date, commit hash or release tag

### 7.4 Presentation

- [ ] Slide deck matches report storyline (no contradictory numbers)
- [ ] High-resolution figures (300 DPI PNGs from pipeline)
- [ ] Backup slide for validity threats / limitations
- [ ] Timing rehearsal (~1 min per slide guideline)

### 7.5 Repository and admin

- [ ] README points to final report and this plan completion
- [ ] [PROJECT_STATUS.md](PROJECT_STATUS.md) updated: Final Deliverables **complete**
- [ ] [CHANGELOG.md](../CHANGELOG.md) / [docs/CHANGELOG.md](CHANGELOG.md) entry for final submission
- [ ] [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) aligned with completed phases
- [ ] Submission archive (D-F4) built and checksum verified
- [ ] Programme-specific forms (declaration, grading cover sheet) attached if required — *confirm with CERG/AMGCR coordinator*

### 7.6 Pre-submission sign-off

- [ ] Self-review against [PROJECT_CHARTER.md](PROJECT_CHARTER.md) §4 and §6.3
- [ ] Optional: supervisor review of D-F1-A + slide outline
- [ ] Final read of [RESULTS_AND_DISCUSSION.md](RESULTS_AND_DISCUSSION.md) §11 conclusions reflected verbatim in report Conclusions

---

## 8. Risks and mitigations (planning only)

| Risk | Mitigation |
|------|------------|
| Missing PNGs in checkout | Run artefact audit before writing; document in checklist if figures must be regenerated in a **separate** approved task |
| Report too long for programme limit | Prioritize 8 hero figures + move per-event panels to appendix |
| Reviewer expects ML results | Front-load “methods pilot, ML is future work” in abstract and limitations |
| Stale IMPLEMENTATION_PLAN confuses examiners | D-S4 doc sync before archive |

---

## 9. Next action (after this plan)

When approved to proceed: execute **§2 step 1 (gap audit)** and **step 2 (figure/table audit)** without modifying `scripts/` or `src/` unless audit fails.

---

**Version:** 1.3.0 (archived — v1.0 submission complete)
