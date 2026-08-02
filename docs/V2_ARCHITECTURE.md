# V2_ARCHITECTURE.md

**Version 2.0 — Interactive Research Platform Architecture**

**Status:** **Implemented** — see `website/` and [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md)  
**Baseline:** v1.0.0 Submission Release (frozen 2026-07-29)  
**Authoritative scope:** [PROJECT_CHARTER.md](PROJECT_CHARTER.md) · v1.0 layout: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 1. Purpose

This document defines the technical architecture for transforming the AMGCR Earthquake Research repository into a **professional interactive research platform** while preserving v1.0 as the immutable scientific baseline.

**Core principle:** The GitHub repository remains the **single source of truth**. The website **renders** existing content; it does not fork, duplicate, or maintain parallel scientific narratives.

---

## 2. Goals and non-goals

### Goals

| Goal | Description |
|------|-------------|
| **Communicate science** | Present the full v1.0 workflow visually to professors, researchers, recruiters, students, and non-technical visitors |
| **Render, not duplicate** | Markdown reports, JSON summaries, CSV tables, figures, and PDFs are read from repository paths at build time |
| **Zero recurring cost** | Free hosting, free maps, free analytics, no paid APIs or databases |
| **Static-first** | Pre-render pages wherever possible; client-side interactivity only where needed |
| **v3-ready** | Architecture supports future AI features without redesign |

### Non-goals (Version 2.0)

- Re-running or modifying v1.0 analysis scripts
- Duplicating scientific text into website-only Markdown files
- Backend services, user accounts, or databases
- Real-time earthquake streaming (Version 3.0)
- ML model training or inference (Version 3.0)
- European dataset acquisition (separate science track; website displays roadmap only)

---

## 3. Overall architecture

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                     GITHUB REPOSITORY (source of truth)                  │
│  docs/ · reports/ · data/manifests/ · FINAL_SUBMISSION/ · README.md     │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ build-time ingestion (read-only)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    website/  —  Next.js App Router (SSG)                 │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌───────────────┐  │
│  │ Content     │  │ Static page  │  │ Interactive │  │ Asset         │  │
│  │ loaders     │→ │ generator    │→ │ client      │→ │ pipeline      │  │
│  │ (MD/JSON/   │  │ (SSG/ISR)    │  │ components  │  │ (figures/PDF) │  │
│  │  CSV)       │  │              │  │             │  │               │  │
│  └─────────────┘  └──────────────┘  └─────────────┘  └───────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │ static export / edge deploy
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              DEPLOYMENT (GitHub Pages or Vercel Hobby — free)            │
│              CDN · HTTPS · optional custom domain                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Architectural layers

| Layer | Responsibility | v1.0 touch? |
|-------|----------------|-------------|
| **Content layer** | `docs/`, `reports/`, `data/manifests/`, `FINAL_SUBMISSION/` | Read only |
| **Ingestion layer** | Parse MD, JSON, CSV; resolve internal links; build search index stub | New code in `website/` |
| **Presentation layer** | React pages, layouts, interactive widgets | New code in `website/` |
| **Deployment layer** | CI/CD, static export, figure bundling | New workflows only |

---

## 4. Technology stack

| Category | Choice | Rationale |
|----------|--------|-----------|
| **Framework** | Next.js 15+ (App Router) | SSG, file-based routing, strong TypeScript support |
| **Language** | TypeScript | Type safety for manifest schemas and JSON contracts |
| **Styling** | Tailwind CSS | Utility-first; fast iteration; responsive defaults |
| **Animation** | Framer Motion | Subtle page transitions, scroll reveals, chart entrance |
| **Charts** | Plotly.js (`react-plotly.js`) | Interactive scatter, heatmap, box plots for feature matrix |
| **Maps** | Leaflet + OpenStreetMap tiles | Event/station map; no API key; free tiles |
| **Markdown** | `react-markdown` + `remark-gfm` + `rehype-slug` | Render phase reports and final report from repo |
| **PDF** | PDF.js (`react-pdf` or `@react-pdf-viewer/core`) | In-browser viewing of FINAL_SUBMISSION PDFs |
| **CSV/JSON** | Native `fetch` + Papa Parse (CSV) | Parse tables at build time or client-side for small files |
| **Icons** | Lucide React | Lightweight, consistent icon set |
| **Hosting** | Vercel Hobby (primary) or GitHub Pages (fallback) | Both free for static sites |
| **Analytics** | Plausible self-hosted *or* Umami Cloud free tier *or* none | Privacy-friendly; no Google Analytics required |
| **CI** | GitHub Actions | Build, validate content, deploy |

**Explicitly excluded:** paid APIs, Supabase/Firebase, serverless databases, Auth0, Mapbox (paid tier), AWS/GCP billable services.

---

## 5. Folder structure

Version 2.0 adds a **self-contained web application** at repository root. v1.0 paths are unchanged.

```text
AMGCR_Earthquake_Research/
├── website/                          # NEW — Version 2.0 web platform
│   ├── app/                          # Next.js App Router pages
│   │   ├── layout.tsx                # Root layout (nav, footer, metadata)
│   │   ├── page.tsx                  # Homepage
│   │   ├── research/
│   │   │   ├── page.tsx              # Research overview
│   │   │   ├── pipeline/page.tsx     # EDA → features workflow
│   │   │   ├── california-pilot/page.tsx
│   │   │   └── europe-roadmap/page.tsx
│   │   ├── explore/
│   │   │   ├── events/page.tsx       # Event map + table
│   │   │   ├── features/page.tsx     # Feature matrix explorer
│   │   │   └── waveforms/page.tsx    # Waveform stage viewer
│   │   ├── docs/
│   │   │   └── [[...slug]]/page.tsx  # Dynamic doc renderer
│   │   ├── report/page.tsx           # Final report (MD + PDF toggle)
│   │   ├── submission/page.tsx       # FINAL_SUBMISSION index + PDFs
│   │   ├── timeline/page.tsx         # Research milestone timeline
│   │   └── about/page.tsx            # Programme context, credits
│   ├── components/
│   │   ├── layout/                   # Header, Footer, Nav, Breadcrumb
│   │   ├── content/                  # MarkdownRenderer, DocSidebar, Callout
│   │   ├── charts/                   # PlotlyChart wrappers, FeatureHeatmap
│   │   ├── maps/                     # EventMap, StationMarker
│   │   ├── data/                     # DataTable, MetricCard, StatGrid
│   │   ├── media/                    # FigureGallery, PDFViewer
│   │   └── motion/                   # FadeIn, PageTransition
│   ├── lib/
│   │   ├── content/                  # Loaders for MD, JSON, CSV
│   │   │   ├── markdown.ts
│   │   │   ├── manifest.ts
│   │   │   ├── reports.ts
│   │   │   └── paths.ts              # Repo-relative path constants
│   │   ├── data/                     # Typed schemas (Zod)
│   │   │   ├── event.ts
│   │   │   ├── feature.ts
│   │   │   └── summary.ts
│   │   └── utils/                    # Formatting, slugify, link rewriting
│   ├── public/
│   │   └── .gitkeep                  # Build copies figures here (CI)
│   ├── scripts/
│   │   ├── sync-content.ts           # Prebuild: copy JSON/CSV/figures
│   │   ├── validate-content.ts       # Schema check against v1.0 outputs
│   │   └── generate-nav.ts         # Auto-build doc sidebar from docs/
│   ├── content-manifest.json         # Generated: file inventory + checksums
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── README.md                     # Website-specific dev/deploy instructions
├── docs/                             # UNCHANGED — includes V2_* planning docs
├── reports/                          # UNCHANGED — read at build time
├── data/manifests/                   # UNCHANGED — read at build time
├── FINAL_SUBMISSION/                 # UNCHANGED — PDFs served via sync or direct path
├── scripts/analysis/                 # UNCHANGED (frozen)
├── src/                              # UNCHANGED (reference + acquisition)
└── .github/workflows/
    └── deploy-website.yml            # NEW — CI/CD for website/
```

**Naming convention:** All Version 2.0 application code lives under `website/`. No v1.0 Python or report files are modified.

---

## 6. Data flow

### 6.1 Build-time ingestion pipeline

```text
prebuild (npm run sync-content)
    │
    ├─ Read data/manifests/iris_california_pilot_events.csv
    ├─ Read reports/tables/*.csv
    ├─ Read reports/eda/dataset_summary.json
    ├─ Read reports/signal_analysis/signal_analysis_summary.json
    ├─ Read reports/preprocessing/preprocessing_summary.json
    ├─ Read reports/features/feature_summary.json
    ├─ Read FINAL_SUBMISSION/VALIDATION_SUMMARY.json
    ├─ Copy reports/figures/*.png → website/public/figures/ (if present)
    ├─ Copy FINAL_SUBMISSION/*.pdf → website/public/submission/ (optional)
    ├─ Scan docs/*.md + reports/*.md → build navigation manifest
    └─ Write website/content-manifest.json (checksums, paths, timestamps)

next build (SSG)
    │
    ├─ generateStaticParams for /docs/[...slug]
    ├─ Server components load MD from ../docs, ../reports (fs.readFile)
    ├─ Serialize JSON/CSV into page props or import as modules
    └─ Output static HTML + client JS bundles
```

### 6.2 Runtime data flow (client)

```text
Static page load
    │
    ├─ Pre-rendered HTML (metrics, tables, markdown body)
    ├─ Hydrate interactive islands:
    │     ├─ Plotly charts (feature correlation, distributions)
    │     ├─ Leaflet map (event lat/lon from manifest)
    │     ├─ Waveform viewer (NPZ-derived JSON slices — see §6.4)
    │     └─ PDF.js viewer (submission PDFs)
    └─ External links → GitHub repo (source files)
```

### 6.3 Content source mapping

| Website feature | Repository source | Format |
|-----------------|-------------------|--------|
| Homepage metrics | `reports/features/feature_summary.json`, `reports/eda/dataset_summary.json` | JSON |
| Event map/table | `data/manifests/iris_california_pilot_events.csv`, `reports/tables/event_summary.csv` | CSV |
| Feature explorer | `reports/tables/feature_matrix.csv`, `feature_correlation_matrix.csv` | CSV |
| Phase reports | `docs/EDA_REPORT.md` … `docs/RESULTS_AND_DISCUSSION.md` | Markdown |
| Final report | `reports/Research_Report_Final.md` | Markdown |
| Submission PDFs | `FINAL_SUBMISSION/*.pdf` | PDF |
| Figures | `reports/figures/*.png` (24 expected per VALIDATION_SUMMARY.json) | PNG |
| Validation status | `FINAL_SUBMISSION/VALIDATION_SUMMARY.json` | JSON |
| Roadmap / v3 | `docs/ROADMAP.md`, `docs/V2_ROADMAP.md` | Markdown |
| GitHub metadata | GitHub REST API (build-time fetch, cached) | JSON |

### 6.4 Waveform data strategy (NPZ handling)

v1.0 stores waveform stages in `reports/preprocessing/*_stages.npz` (NumPy binary). Browsers cannot read NPZ directly.

**Version 2.0 approach (no Python backend):**

1. **Prebuild conversion script** (new, in `website/scripts/`): one-time Python helper invoked in CI that reads NPZ files and emits lightweight JSON arrays (downsampled time series for display). Output: `website/public/waveforms/{event_id}.json`.
2. Script is **read-only** against v1.0 NPZ files; does not alter them.
3. Full-resolution data remains in repo; website shows decimated preview only.
4. Link each waveform view to GitHub source NPZ path for reproducibility.

This keeps the site static while enabling interactive waveform exploration.

---

## 7. Component hierarchy

```text
RootLayout
├── SiteHeader
│   ├── Logo / Title
│   ├── MainNav (Research · Explore · Docs · Report · Submission · Timeline · About)
│   └── GitHubLink (external)
├── PageTransition (Framer Motion)
│   └── {children}
└── SiteFooter
    ├── VersionBadge (v1.0.0 science · v2.0 website)
    ├── Licence / programme note
    └── SourceRepoLink

HomePage
├── HeroSection (title, subtitle, CTA buttons)
├── MetricsStrip (8 events · 18 features · 24 figures · validation PASS)
├── PipelineOverview (EDA → Signal → Preprocess → Features diagram)
├── FeaturedFigures (carousel from reports/figures/)
└── QuickLinks (Report · Explore · GitHub)

ResearchPipelinePage
├── PhaseTimeline (vertical stepper)
├── PhaseCard × 5 (links to docs + interactive widgets)
└── ReproducibilityBanner (D-S1 link)

ExploreEventsPage
├── EventMap (Leaflet)
├── EventDataTable (sortable)
└── EventDetailDrawer (magnitude, station, link to waveform)

ExploreFeaturesPage
├── FeatureMatrixTable
├── CorrelationHeatmap (Plotly)
├── BoxplotByStation (Plotly)
└── FeatureGlossary (from feature_summary.json names)

ExploreWaveformsPage
├── EventSelector
├── WaveformPlot (Plotly or canvas)
└── ProcessingStageToggle (raw / filtered / STA-LTA overlay)

DocsPage (dynamic)
├── DocSidebar (auto-generated from docs/ tree)
├── MarkdownRenderer
└── EditOnGitHub link

ReportPage
├── ViewToggle (Markdown | PDF)
├── MarkdownRenderer (Research_Report_Final.md)
└── PDFViewer (FINAL_SUBMISSION/Research_Report_Final.pdf)

SubmissionPage
├── DeliverableGrid (D-F1 … D-S2 cards)
└── PDFViewer per asset

TimelinePage
├── MilestoneTimeline (v1.0 archived + v2.0 planned)
└── ReleaseMarkers (v1.0.0 tag)
```

---

## 8. Rendering strategy

### 8.1 Markdown rendering

| Concern | Approach |
|---------|----------|
| **Source** | Read directly from `docs/` and `reports/` via Node `fs` in Server Components |
| **Links** | Rewrite relative `.md` links to website routes; external links unchanged |
| **Images** | Rewrite `reports/figures/` paths to `/figures/` public URLs |
| **Tables** | GFM table support via `remark-gfm` |
| **Code blocks** | Syntax highlight via `rehype-highlight` or Shiki |
| **Front matter** | Parse YAML front matter in `Research_Report_Final.md` for metadata display |
| **Anchor headings** | `rehype-slug` + `rehype-autolink-headings` for TOC navigation |

**No duplicated Markdown:** If a page needs a summary, extract the first paragraph from the source file at build time; never maintain a separate copy.

### 8.2 Static generation modes

| Route | Mode | Rebuild trigger |
|-------|------|-----------------|
| `/` | SSG | Content manifest change |
| `/research/*` | SSG | docs/ or summary JSON change |
| `/explore/*` | SSG + client hydration | CSV/JSON change |
| `/docs/[...slug]` | SSG (`generateStaticParams`) | Any docs/*.md change |
| `/report` | SSG | Research_Report_Final.md change |
| `/submission` | SSG | FINAL_SUBMISSION/ change |
| `/timeline` | SSG | ROADMAP / V2_ROADMAP change |

**ISR (optional):** Not required for v2.0; full rebuild on push is sufficient for a research portfolio site.

### 8.3 Figure availability

Figures live in `reports/figures/` and may be absent in Git clones (local generation; some paths gitignored). Strategy:

1. CI workflow runs `scripts/analysis/*.py` (or a lightweight figure-check script) before website build when figures are missing.
2. `sync-content.ts` validates against `VALIDATION_SUMMARY.json` expected figure list.
3. Build **fails visibly** if required figures are missing (prevents broken submission showcase).
4. Document regeneration steps in `website/README.md` pointing to D-S1.

---

## 9. Content management strategy

### 9.1 Single source of truth rules

| Rule | Implementation |
|------|----------------|
| Scientific text lives in `docs/` and `reports/` only | Website loaders read files; no `website/content/*.md` duplicates |
| Metrics come from JSON/CSV outputs | Typed Zod schemas validate at build time |
| PDFs are exports of Markdown sources | Website shows both; labels clarify source hierarchy |
| Navigation reflects doc tree | `generate-nav.ts` scans `docs/`; manual override via `website/nav.config.ts` only for ordering |
| Version badges | Display v1.0.0 science freeze date; website semver independent (e.g. site v2.0.0) |

### 9.2 Link-back pattern

Every rendered document page includes:

- **View source on GitHub** — deep link to exact file and commit SHA (from CI env)
- **Last updated** — from git log or JSON `generated_at_utc` fields
- **Related artefacts** — cross-links to tables, figures, and explore pages

### 9.3 Content manifest

`website/content-manifest.json` (generated, committed or CI artefact):

```json
{
  "science_version": "1.0.0",
  "science_freeze_date": "2026-07-29",
  "website_version": "2.0.0",
  "generated_at": "ISO-8601",
  "git_sha": "abc123",
  "files": [
    { "path": "reports/features/feature_summary.json", "sha256": "...", "used_by": ["/", "/explore/features"] }
  ],
  "figures": { "expected": 24, "present": 24, "missing": [] },
  "validation": { "status": "PASS", "source": "FINAL_SUBMISSION/VALIDATION_SUMMARY.json" }
}
```

---

## 10. Deployment architecture

See [V2_DEPLOYMENT_PLAN.md](V2_DEPLOYMENT_PLAN.md) for full detail. Summary:

| Target | Pattern |
|--------|---------|
| **Primary** | Vercel Hobby — connect repo, root directory `website/`, auto-deploy on push to `main` |
| **Alternative** | GitHub Pages — `output: 'export'` in Next.js, deploy `website/out/` via Actions |
| **Domain** | Optional free subdomain (`*.vercel.app` or `*.github.io`) or custom domain |
| **Assets** | Figures and PDFs bundled in static export or served from `/public` |

```text
git push → main
    → GitHub Actions: validate v1.0 artefacts + build website
    → (optional) regenerate figures if missing
    → npm run sync-content && npm run build
    → deploy to Vercel / GitHub Pages
```

---

## 11. Future scalability

### 11.1 Version 2.0 scale limits (acceptable)

| Dimension | v2.0 design limit | Mitigation path |
|-----------|-------------------|-----------------|
| Events | ~100 | CSV + static pages sufficient |
| Figures | ~500 | Lazy loading, pagination |
| Docs | ~50 MD files | Sidebar + search index stub |
| Waveforms | 8–50 events | Downsampled JSON in `/public` |

### 11.2 Horizontal extension (no redesign)

| Future need | Extension point |
|-------------|-----------------|
| Europe dataset | Add manifest CSV + report MD; same loaders |
| More pipeline phases | Extend `PhaseTimeline` + doc routes |
| Dashboard metrics | New JSON summaries from analysis scripts |
| Multi-language | i18n layer on existing MD (v3+) |

---

## 12. Version 3.0 extensibility (AI and live data)

Version 2.0 is designed so Version 3.0 features plug in without architectural rewrite.

### 12.1 Extension architecture

```text
┌──────────────────────────────────────────────────────────────┐
│  Version 2.0 static site (unchanged core)                     │
│  SSG pages · content loaders · component library              │
└────────────────────────────┬─────────────────────────────────┘
                             │ optional adapter layer
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  Version 3.0 optional services (additive)                     │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────────────────┐ │
│  │ /api/search │ │ /api/chat    │ │ /api/live-earthquakes  │ │
│  │ (RAG index) │ │ (LLM + RAG)  │ │ (FDSN proxy/edge fn)   │ │
│  └─────────────┘ └──────────────┘ └────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### 12.2 v3 features mapped to v2 hooks

| v3 feature | v2 preparation |
|------------|----------------|
| **AI assistant** | Floating chat widget slot in `RootLayout`; `/api/chat` route (Vercel serverless, free tier) |
| **Semantic document search** | Build-time embedding index → `website/search-index.json`; upgrade to vector DB later |
| **Chat over reports** | Markdown chunks generated in `sync-content.ts`; chunk IDs map to doc anchors |
| **Interactive earthquake explorer** | Extend `EventMap` + add live layer; FDSN fetch via edge function |
| **RAG pipeline** | Content manifest + chunk index = retrieval corpus; no duplicate docs |
| **Live earthquake integration** | New data provider implementing `lib/data/providers/EarthquakeProvider` interface |

### 12.3 Interface contracts (define in v2, implement in v3)

```typescript
// website/lib/data/providers/types.ts (stub in v2)

interface EarthquakeProvider {
  getCatalogEvents(filters: CatalogFilters): Promise<Event[]>;
  getWaveformMeta(eventId: string): Promise<WaveformMeta | null>;
}

interface SearchProvider {
  search(query: string, limit?: number): Promise<SearchResult[]>;
}

interface ChatProvider {
  ask(question: string, context?: ChatContext): AsyncIterable<string>;
}
```

v2.0 ships **static implementations** (CSV/JSON only). v3.0 adds **remote implementations** behind the same interfaces.

### 12.4 What v2 must NOT do (to keep v3 clean)

- Do not embed API keys in client bundles
- Do not hard-code FDSN endpoints in components (use provider abstraction)
- Do not duplicate Markdown into embedding-friendly copies (chunk from source at build time)
- Do not choose a paid vector DB in v2 (JSON index is sufficient stub)

---

## 13. Security and compliance

| Topic | Approach |
|-------|----------|
| **Secrets** | None required for v2.0 static site |
| **External links** | `rel="noopener noreferrer"` on GitHub/external targets |
| **PDF viewing** | Client-side PDF.js; no upload |
| **CSP** | Restrict script sources; allow OSM tile domains |
| **Privacy** | No cookies by default; optional privacy-friendly analytics |
| **Licence** | Display repo licence; credit USGS/EarthScope data per D-S2 |

---

## 14. Testing strategy (implementation phase)

| Level | Scope |
|-------|-------|
| **Content validation** | `validate-content.ts` — JSON schema, figure inventory, broken links |
| **Component tests** | Vitest + React Testing Library for tables, maps, charts |
| **E2E** | Playwright smoke tests: homepage, report, explore, docs navigation |
| **Visual regression** | Optional Percy free tier or manual checklist |
| **Accessibility** | axe-core in CI; WCAG 2.1 AA target (see V2_UI_PLAN.md) |
| **Lighthouse** | CI gate: Performance ≥ 90, Accessibility ≥ 95 on key pages |

---

## 15. Dependencies on v1.0 artefacts

| Artefact | Required for v2? | Fallback if missing |
|----------|------------------|---------------------|
| `reports/figures/*.png` (24) | Yes (CI regenerate) | Block deploy; show regenerate instructions |
| JSON summaries | Yes | Build fails |
| CSV tables | Yes | Build fails |
| NPZ stages | Optional (waveform explorer) | Disable waveform page section |
| Raw MiniSEED | No (not served on web) | Link to D-S2 download instructions |
| FINAL_SUBMISSION PDFs | Recommended | Markdown-only report view |

---

## 16. Document control

| Field | Value |
|-------|-------|
| **Version** | 2.0.0-plan |
| **Date** | 2026-08-01 |
| **Status** | Awaiting approval before implementation |
| **Next step** | Review → Approval → Phase 1 in [V2_ROADMAP.md](V2_ROADMAP.md) |
| **Related** | [V2_UI_PLAN.md](V2_UI_PLAN.md) · [V2_ROADMAP.md](V2_ROADMAP.md) · [V2_DEPLOYMENT_PLAN.md](V2_DEPLOYMENT_PLAN.md) |
