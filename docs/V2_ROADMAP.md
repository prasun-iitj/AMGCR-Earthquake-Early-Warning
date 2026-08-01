# V2_ROADMAP.md

**Version 2.0 — Implementation Roadmap**

**Status:** Planning only (no implementation)  
**Baseline:** v1.0.0 Submission Release (frozen 2026-07-29)  
**Architecture:** [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md) · **UI:** [V2_UI_PLAN.md](V2_UI_PLAN.md) · **Deploy:** [V2_DEPLOYMENT_PLAN.md](V2_DEPLOYMENT_PLAN.md)

---

## 1. Purpose

Break Version 2.0 into **sequential, reviewable implementation phases**. Each phase has clear objectives, deliverables, dependencies, and acceptance criteria. Implementation begins only after plan approval.

**Workflow:** Plan → Review → Approval → Implementation → Testing → Documentation → Release

---

## 2. Version 2.0 scope summary

Transform the repository into a **static interactive research platform** under `website/` that renders existing v1.0 content. No v1.0 science changes. Free hosting only.

**Target release:** v2.0.0 (website) — independent semver from v1.0.0 science release.

---

## 3. Phase overview

| Phase | Name | Est. effort | Depends on |
|-------|------|-------------|------------|
| **1** | Website foundation | 1–2 weeks | Plan approval |
| **2** | Documentation rendering | 1 week | Phase 1 |
| **3** | Interactive charts | 1 week | Phase 1 |
| **4** | Waveform explorer | 1 week | Phase 1, 3 |
| **5** | Dataset explorer | 1 week | Phase 1, 3 |
| **6** | Research timeline | 3–4 days | Phase 1, 2 |
| **7** | GitHub integration | 3–4 days | Phase 1 |
| **8** | Deployment | 1 week | Phases 1–7 |

Phases 3 and 2 can partially overlap after Phase 1 completes. Phase 8 CI hardening runs in parallel with Phases 6–7.

---

## Phase 1 — Website foundation

### Objectives

- Scaffold the Next.js application in `website/` without touching v1.0 code
- Establish layout, navigation, routing, design tokens, and content loader stubs
- Prove build-time read access to parent repository files

### Deliverables

| Deliverable | Path / artefact |
|-------------|-----------------|
| Next.js App Router project | `website/` |
| Root layout with header, footer, nav | `website/app/layout.tsx`, `components/layout/` |
| Homepage (static shell) | `website/app/page.tsx` |
| Tailwind + typography + colour tokens | `tailwind.config.ts`, `app/globals.css` |
| Path constants for repo content | `website/lib/content/paths.ts` |
| Placeholder pages for all routes | `website/app/**/page.tsx` |
| Website README | `website/README.md` |
| Root `.gitignore` update for `website/node_modules`, `.next` | `.gitignore` (append only) |

### Dependencies

- Plan approval (this document + architecture + UI + deployment)
- Node.js 20+ LTS on dev machine
- No v1.0 modifications

### Acceptance criteria

- [ ] `npm run dev` serves homepage at `localhost:3000`
- [ ] All top-level routes return 200 (placeholder content acceptable)
- [ ] Navigation matches [V2_UI_PLAN.md](V2_UI_PLAN.md) site map
- [ ] Responsive layout verified at 375px, 768px, 1280px widths
- [ ] `npm run build` succeeds with zero errors
- [ ] No files under `src/`, `scripts/analysis/`, `reports/*.md` modified
- [ ] Lighthouse Performance ≥ 85 on homepage placeholder

---

## Phase 2 — Documentation rendering

### Objectives

- Render all project Markdown from `docs/` and selected `reports/` files
- Auto-generate documentation sidebar navigation
- Rewrite internal links and figure paths correctly

### Deliverables

| Deliverable | Description |
|-------------|-------------|
| Markdown loader | `lib/content/markdown.ts` — fs read, front matter parse |
| Dynamic docs route | `app/docs/[[...slug]]/page.tsx` |
| `MarkdownRenderer` component | GFM tables, code highlight, slug headings |
| Doc sidebar | Grouped nav from `generate-nav.ts` |
| Link rewriter | Relative `.md` → `/docs/...` routes |
| Figure path resolver | `reports/figures/` → `/figures/` |
| Phase report index | `/research/pipeline` links to each phase doc |
| "View on GitHub" component | Deep links with file path |

**Documents in scope (minimum):**

- Governance: `PROJECT_CHARTER.md`, `PROJECT_STATUS.md`, `ROADMAP.md`, `RESEARCH_DIRECTION.md`, `ARCHITECTURE.md`
- Phase reports: `EDA_REPORT.md` through `RESULTS_AND_DISCUSSION.md`
- Statements: `REPRODUCIBILITY_STATEMENT.md`, `DATA_AVAILABILITY_STATEMENT.md`
- Guides: `GLOSSARY.md`, `BEGINNER_GUIDE.md`

### Dependencies

- Phase 1 complete
- `remark-gfm`, `react-markdown`, `rehype-slug`, syntax highlighter installed in `website/`

### Acceptance criteria

- [ ] All listed docs render without broken MD syntax
- [ ] Internal cross-links navigate within site (manual spot check ≥10 links)
- [ ] Images in docs load when figures present in `/public/figures`
- [ ] Each doc page shows GitHub source link
- [ ] Mobile: sidebar collapses; TOC usable
- [ ] No Markdown content duplicated into `website/`

---

## Phase 3 — Interactive charts

### Objectives

- Visualise v1.0 tabular and summary data with Plotly
- Display key metrics on homepage from JSON summaries

### Deliverables

| Deliverable | Data source |
|-------------|-------------|
| `sync-content.ts` script | Copies JSON/CSV to importable location |
| Zod schemas | `feature_summary.json`, `signal_analysis_summary.json`, etc. |
| Homepage metric strip | Live counts from JSON |
| Correlation heatmap | `reports/tables/feature_correlation_matrix.csv` |
| Feature distribution plots | `reports/tables/feature_matrix.csv` |
| Boxplots by station | `feature_matrix.csv` + station grouping |
| SNR before/after chart | `preprocessing_summary.json` |
| Magnitude histogram | `event_summary.csv` |
| `PlotlyChart` wrapper | Lazy load, responsive, table fallback |
| `/explore/features` page | Full chart suite |

### Dependencies

- Phase 1 complete
- `react-plotly.js`, `papaparse`, `zod`

### Acceptance criteria

- [ ] Homepage shows 8 events, 18 features, validation status from real JSON
- [ ] Correlation heatmap matches values in CSV (spot check 3 cells)
- [ ] Charts resize correctly on mobile
- [ ] "View as table" toggle available for each chart (accessibility)
- [ ] Build fails if required JSON/CSV missing or schema-invalid
- [ ] Plotly bundles lazy-loaded (not on homepage initial JS for unrelated pages)

---

## Phase 4 — Waveform explorer

### Objectives

- Interactive preview of pilot waveforms without a Python backend
- Display P-pick markers and processing stage comparison

### Deliverables

| Deliverable | Description |
|-------------|-------------|
| NPZ → JSON conversion script | `website/scripts/convert-waveforms.py` (read-only on v1.0 NPZ) |
| Downsampled waveform JSON | `website/public/waveforms/{short_id}.json` |
| `/explore/waveforms` page | Event selector, stage toggle, Plotly line chart |
| P-pick marker overlay | From per-event signal analysis JSON |
| Metrics sidebar | SNR, duration, peak amplitude |
| Fallback UI | Static preprocessing PNG if JSON unavailable |
| CI integration | Optional conversion step in GitHub Actions |

### Dependencies

- Phase 1, Phase 3 (Plotly wrapper)
- Python 3.11+ in CI for NPZ conversion only
- `reports/preprocessing/*_stages.npz` present locally/CI

### Acceptance criteria

- [ ] All 8 events selectable; chart renders within 2s
- [ ] P-pick time matches `signal_analysis/*_metrics.json` (±0.1 s)
- [ ] Stage toggle switches between raw/filtered traces
- [ ] Link to source NPZ on GitHub displayed
- [ ] Page degrades gracefully if conversion not run (static figure + message)
- [ ] No modification to v1.0 NPZ files

---

## Phase 5 — Dataset explorer

### Objectives

- Geographic and tabular exploration of the California pilot manifest
- Unified event detail views linking map, table, waveforms, and docs

### Deliverables

| Deliverable | Description |
|-------------|-------------|
| `/explore/events` page | Full event exploration |
| Leaflet map component | OSM tiles, magnitude-scaled markers |
| Station markers | CI.ADO, CI.USC fixed positions from event data |
| Sortable/filterable data table | Manifest + event_summary merged |
| Event detail slide-over | Magnitude, depth, station, waveform link |
| `/research/california-pilot` page | Summary + map + station usage chart |
| CSV export button | Download filtered view (client-generated) |

### Dependencies

- Phase 1, Phase 3
- `leaflet`, `react-leaflet`

### Acceptance criteria

- [ ] All 8 events visible on map at correct lat/lon (±0.01°)
- [ ] Table sort by magnitude, date works
- [ ] Filters reduce visible rows and map markers synchronously
- [ ] List view accessible without map interaction (WCAG)
- [ ] Map works on mobile touch
- [ ] No API keys required for tiles

---

## Phase 6 — Research timeline

### Objectives

- Visualise v1.0 completed milestones and v2.0/v3.0 planned work
- Connect timeline entries to docs, submission, and roadmap

### Deliverables

| Deliverable | Description |
|-------------|-------------|
| `/timeline` page | Interactive vertical timeline |
| v1.0 milestones | From `ROADMAP.md` archived section + `RELEASE_SUMMARY_v1.0.md` |
| v2.0 phases | From this document |
| v3.0 preview | AI, live data, Europe expansion (read-only plan) |
| `/research` overview page | Cards linking pipeline, pilot, Europe roadmap |
| `/research/pipeline` page | Phase stepper with SNR mini-chart |
| `/research/europe-roadmap` page | Rendered from `ROADMAP.md` § Version 2.0 |

### Dependencies

- Phase 1, Phase 2 (doc links)

### Acceptance criteria

- [ ] Timeline shows v1.0 complete status with 2026-07-29 freeze date
- [ ] Each v1.0 milestone links to correct doc or submission asset
- [ ] v2.0 phases match this roadmap document
- [ ] v3.0 section clearly labelled "future" (not shipped)
- [ ] Timeline readable on mobile (single column)

---

## Phase 7 — GitHub integration

### Objectives

- Connect the website to repository metadata without duplicating content
- Surface release info, commit SHA, and contribution entry points

### Deliverables

| Deliverable | Description |
|-------------|-------------|
| GitHub link component | Consistent external link styling |
| Build-time metadata fetch | Latest release tag, commit SHA (CI env vars) |
| `content-manifest.json` generator | File inventory with checksums |
| `/report` page | Toggle MD / PDF view |
| `/submission` page | Deliverable grid + PDF viewer |
| PDF.js integration | View FINAL_SUBMISSION PDFs in browser |
| Release badge | "v1.0.0 Submission Release" in footer |
| Open Graph metadata | Per-page title, description, optional OG image |

**GitHub API usage:** Fetch release info at build time only; cache in manifest. No runtime API calls (rate limit safe).

### Dependencies

- Phase 1, Phase 2 (report MD rendering)
- `react-pdf` or `@react-pdf-viewer/core`

### Acceptance criteria

- [ ] Footer shows build commit SHA and date
- [ ] `/report` renders full `Research_Report_Final.md`
- [ ] `/report` PDF view loads `FINAL_SUBMISSION/Research_Report_Final.pdf`
- [ ] `/submission` lists all D-F1–D-S2 assets with working PDF links
- [ ] Validation PASS banner from `VALIDATION_SUMMARY.json`
- [ ] All GitHub links open correct repo paths
- [ ] OG tags present on homepage and report page

---

## Phase 8 — Deployment

### Objectives

- Production deployment on free tier
- CI/CD pipeline with content validation
- Performance, SEO, and optional analytics

### Deliverables

| Deliverable | Description |
|-------------|-------------|
| GitHub Actions workflow | `.github/workflows/deploy-website.yml` |
| Content validation in CI | `validate-content.ts` |
| Figure regeneration step | Conditional run if figures missing |
| Vercel Hobby deployment | Primary target |
| GitHub Pages fallback config | `next.config.ts` static export option |
| `website/README.md` deploy section | Step-by-step for both targets |
| Lighthouse CI gate | Key pages ≥ thresholds |
| `sitemap.xml` + `robots.txt` | Generated at build |
| Optional analytics | Umami or Plausible (free) |
| v2.0.0 website release tag | GitHub Release notes for platform |

See [V2_DEPLOYMENT_PLAN.md](V2_DEPLOYMENT_PLAN.md) for full deployment detail.

### Dependencies

- Phases 1–7 feature-complete
- Vercel or GitHub Pages account (free)

### Acceptance criteria

- [ ] Push to `main` triggers CI build and deploy
- [ ] Production URL loads all routes with HTTPS
- [ ] CI fails if validation fails (missing JSON, broken links)
- [ ] Lighthouse Performance ≥ 90, Accessibility ≥ 95, SEO ≥ 90 on homepage
- [ ] Static export size < 50 MB (excluding PDFs; PDFs optionally CDN-linked)
- [ ] README documents local dev and deploy process
- [ ] `docs/PROJECT_STATUS.md` updated to reflect v2.0 website complete (post-release only)

---

## 4. Post-release documentation updates

After Phase 8 release (implementation phase—not now):

| Document | Update |
|----------|--------|
| `README.md` | Add website URL and `website/` to structure |
| `docs/PROJECT_STATUS.md` | Mark v2.0 website milestone complete |
| `docs/ROADMAP.md` | Move website items to archived; retain Europe/ML/streaming as v2.1+ |
| `docs/CHANGELOG.md` | v2.0.0 website release entry |
| `RELEASE_SUMMARY_v2.0.md` | New release summary (optional) |
| `AGENTS.md` | Point agents to website architecture docs |

**Rule:** Do not update these until Phase 8 acceptance criteria pass.

---

## 5. Risk register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Figures missing in CI clone | Broken homepage gallery | Regenerate in CI; fail build if still missing |
| NPZ conversion complexity | Waveform phase delayed | Ship Phase 5/6 first; waveform as optional |
| Plotly bundle size | Slow mobile load | Dynamic import; limit chart count per page |
| PDF size in static export | Deploy limit exceeded | Serve PDFs from GitHub Releases or lazy fetch |
| Scope creep into v1.0 science | Breaks frozen baseline | PR checklist: no changes outside `website/`, workflows, v2 docs |
| Free tier deploy limits | Build minutes exhausted | Optimise CI cache; deploy on release tags only |

---

## 6. Version 3.0 preview (out of v2 scope)

After v2.0.0 website release, planned additive features (no architecture redesign):

| Feature | Builds on |
|---------|-----------|
| AI assistant (RAG chat) | Content manifest + doc chunks from Phase 7 |
| Semantic search | Search index stub from Phase 2 |
| Live earthquake layer | Event map from Phase 5 + edge API |
| Europe dataset pages | Same doc/chart patterns from Phases 2–5 |
| EarthESND evaluation dashboard | New JSON outputs from science track |

See [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md) §12 for extensibility design.

---

## 7. Success criteria for Version 2.0 (overall)

Version 2.0 is **complete** when:

1. A non-technical visitor can understand the project from the homepage alone
2. An examiner can read the full report and open submission PDFs without cloning the repo
3. A researcher can explore the 8×18 feature matrix and event map interactively
4. All scientific text is rendered from repository sources (zero duplicate MD)
5. Site deploys automatically on push via free hosting
6. v1.0 analysis scripts and reports remain unmodified
7. v3.0 extension points are documented and unused (no premature AI/backend)

---

## 8. Document control

| Field | Value |
|-------|-------|
| **Version** | 2.0.0-plan |
| **Date** | 2026-08-01 |
| **Status** | Awaiting approval before Phase 1 |
| **Related** | [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md) · [V2_UI_PLAN.md](V2_UI_PLAN.md) · [V2_DEPLOYMENT_PLAN.md](V2_DEPLOYMENT_PLAN.md) |
