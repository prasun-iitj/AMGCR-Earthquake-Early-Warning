# V2_UI_PLAN.md

**Version 2.0 — User Interface and Experience Plan**

**Status:** **Implemented** — see live UI in `website/`  
**Baseline:** v1.0.0 Submission Release · Presentation: [Presentation_Outline_D-F2.md](../reports/Presentation_Outline_D-F2.md)  
**Architecture:** [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md)

---

## 1. Purpose

Define the user experience, information architecture, visual language, and page-level wireframes for the AMGCR Earthquake Research interactive platform. The UI must communicate rigorous science to diverse audiences without requiring visitors to navigate the GitHub repository first.

---

## 2. Design principles

| Principle | Application |
|-----------|-------------|
| **Science first** | Lead with findings, evidence, and limitations—not framework marketing |
| **Progressive disclosure** | Simple overview → detailed reports → raw data tables |
| **Source transparency** | Every chart and claim links to repository file or report section |
| **Accessible by default** | WCAG 2.1 AA; keyboard navigation; readable contrast |
| **Mobile-ready** | All core flows usable on phone and tablet |
| **No dark patterns** | Clear distinction between pilot results and future roadmap |
| **Restrained motion** | Framer Motion for polish, not distraction |

---

## 3. User personas

### 3.1 Primary personas

| Persona | Goals | Key pages | Success metric |
|---------|-------|-----------|----------------|
| **Professor / examiner** | Assess methodology, reproducibility, European framing, limitations | Report, Pipeline, Submission, Timeline | Finds D-F1 narrative and D-S1/D-S2 within 2 clicks |
| **Earthquake scientist / researcher** | Evaluate pipeline, inspect features, compare STA/LTA metrics | Explore (events, features, waveforms), Phase docs | Can inspect 8×18 matrix and per-event JSON metrics |
| **Recruiter / hiring manager** | Understand scope, skills, deliverables in <5 minutes | Homepage, About, Timeline, GitHub link | Grasps project scale (ObsPy, FDSN, ML-ready features) quickly |
| **Certificate peer / student** | Learn workflow structure for own projects | Pipeline, Docs, Beginner Guide | Can follow EDA → features path as template |
| **Non-technical visitor** | Understand what EEW is and what this project did | Homepage, Research overview, Report (executive summary) | Leaves with clear "Europe focus, California pilot" message |

### 3.2 Secondary personas

| Persona | Needs |
|---------|-------|
| **Open-source contributor** | GitHub link, CONTRIBUTING.md, architecture docs |
| **Journal reviewer (future)** | PDF report, data availability, reproducibility statements |
| **Future self (v3 AI user)** | Search entry point placeholder, consistent nav for chat widget |

---

## 4. Information architecture

### 4.1 Site map

```text
Home
├── Research
│   ├── Overview
│   ├── Pipeline (EDA → Features)
│   ├── California Pilot
│   └── Europe Roadmap (future work)
├── Explore
│   ├── Events (map + table)
│   ├── Features (matrix + charts)
│   └── Waveforms (stage viewer)
├── Documentation
│   ├── Project docs (docs/*)
│   └── Phase reports (grouped)
├── Final Report (MD + PDF)
├── Submission Package (FINAL_SUBMISSION)
├── Timeline
├── About
└── GitHub (external)
```

### 4.2 Content priority matrix

| Content | Audience breadth | Depth | Page type |
|---------|------------------|-------|-----------|
| Executive summary | All | Low | Homepage + Report header |
| Pipeline diagram | All | Medium | Research / Pipeline |
| Event map | Scientists, students | Medium | Explore / Events |
| Feature charts | Scientists | High | Explore / Features |
| Phase reports | Researchers | High | Docs |
| Full final report | Examiners | Very high | Report |
| Submission PDFs | Examiners | High | Submission |
| v2/v3 roadmap | Contributors | Medium | Timeline + Europe Roadmap |

### 4.3 Navigation model

**Desktop:** Horizontal top nav with dropdown for Research, Explore, and Documentation.

**Mobile:** Hamburger menu with accordion sections mirroring desktop hierarchy.

**Persistent elements:**
- Logo / project title (links home)
- "v1.0 Science · v2.0 Platform" badge
- GitHub icon (external)
- Breadcrumbs on all pages below top level

**Footer:**
- Programme context (AMGCR, Swiss certificate)
- Links: Charter, Reproducibility, Data Availability
- "Source of truth: GitHub repository"
- Build timestamp and commit SHA (small text)

---

## 5. Wireframe descriptions

Wireframes are **structural descriptions** for implementation. Visual mockups are deferred to Phase 1.

### 5.1 Homepage (`/`)

```text
┌────────────────────────────────────────────────────────────────┐
│ [Logo]  Research ▾  Explore ▾  Docs ▾  Report  Submission  [GH]│
├────────────────────────────────────────────────────────────────┤
│                                                                │
│     Reproducible AI-Assisted Earthquake Early Warning          │
│     Research for Western Seismic Regions                       │
│                                                                │
│     Europe-focused programme · California FDSN pilot complete  │
│                                                                │
│     [Read Final Report]  [Explore Data]  [View on GitHub]      │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ 8 Events │ │ 18 Feat. │ │ 24 Figs  │ │ VALID ✓  │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
├────────────────────────────────────────────────────────────────┤
│  Research Pipeline (horizontal stepper)                        │
│  [Acquire] → [EDA] → [Signal] → [Preprocess] → [Features]     │
│  (each step links to doc + explore page)                       │
├────────────────────────────────────────────────────────────────┤
│  Featured Figures (horizontal scroll / grid)                   │
│  [waveform] [heatmap] [magnitude hist] [preprocessing]           │
├────────────────────────────────────────────────────────────────┤
│  Two-column: "European focus" | "California pilot"             │
│  Brief text from charter + link to Research overview           │
├────────────────────────────────────────────────────────────────┤
│  Footer                                                        │
└────────────────────────────────────────────────────────────────┘
```

**Interactions:**
- Metric cards animate count-up on scroll (Framer Motion)
- Pipeline stepper highlights on hover; click navigates
- Figure carousel auto-advances slowly; pauses on hover

**Content sources:** `feature_summary.json`, `dataset_summary.json`, `VALIDATION_SUMMARY.json`, `reports/figures/`

---

### 5.2 Research overview (`/research`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Hero: "From FDSN waveforms to ML-ready features"               │
├────────────────────────────────────────────────────────────────┤
│ Three cards:                                                   │
│  [Pipeline] — end-to-end workflow                              │
│  [California Pilot] — 8 events, IRIS/EarthScope                │
│  [Europe Roadmap] — ORFEUS/EIDA transfer path                  │
├────────────────────────────────────────────────────────────────┤
│ Key findings (5 bullets from Research_Report_Final executive)  │
├────────────────────────────────────────────────────────────────┤
│ Limitations callout (amber box): N=8, no response removal, etc.│
└────────────────────────────────────────────────────────────────┘
```

---

### 5.3 Pipeline page (`/research/pipeline`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Vertical timeline (left rail) + detail panel (right)           │
│                                                                │
│ ● Phase A.1 — EDA          │  Summary stats                   │
│ ● Phase A.2 — Signal       │  STA/LTA config                  │
│ ● Phase B.1 — Preprocess   │  SNR improvement chart           │
│ ● Phase B.2 — Features     │  18 feature names                │
│ ● Phase C   — Results      │  Link to interpretation doc      │
│                                                                │
│ Each phase: [Read full report ↗] [View artefacts ↗]            │
└────────────────────────────────────────────────────────────────┘
```

**Interactive element:** Mini SNR before/after bar chart (from `preprocessing_summary.json`).

---

### 5.4 California pilot (`/research/california-pilot`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Dataset summary cards (magnitude range, stations, channel)    │
├────────────────────────────────────────────────────────────────┤
│ Split view:                                                    │
│  Left: Leaflet map (8 event markers, 2 station icons)           │
│  Right: Sortable event table                                   │
├────────────────────────────────────────────────────────────────┤
│ Station usage bar chart (ADO vs USC frequency)                   │
├────────────────────────────────────────────────────────────────┤
│ Link: IRIS_DATASET_REPORT.md · manifest CSV on GitHub          │
└────────────────────────────────────────────────────────────────┘
```

---

### 5.5 Explore — Events (`/explore/events`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Full-width map (California bbox, clustered markers)            │
├────────────────────────────────────────────────────────────────┤
│ Filters: magnitude slider · station · date range               │
├────────────────────────────────────────────────────────────────┤
│ Data table: event_id, time, mag, lat, lon, station             │
│ Row click → slide-over panel with event details + links        │
└────────────────────────────────────────────────────────────────┘
```

**Map styling:** Subtle topographic OSM tiles; magnitude-proportional marker radius; popup with event summary.

---

### 5.6 Explore — Features (`/explore/features`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Tab bar: [Matrix] [Correlation] [Distributions] [By Station]   │
├────────────────────────────────────────────────────────────────┤
│ Tab: Matrix — scrollable 8×18 table with column tooltips       │
│ Tab: Correlation — Plotly heatmap (feature_correlation_matrix) │
│ Tab: Distributions — Plotly histograms / boxplots              │
│ Tab: By Station — grouped boxplots ADO vs USC                  │
├────────────────────────────────────────────────────────────────┤
│ Feature glossary accordion (18 terms + units note)               │
└────────────────────────────────────────────────────────────────┘
```

**UX note:** Amplitude features show "counts-based; no response correction" disclaimer prominently.

---

### 5.7 Explore — Waveforms (`/explore/waveforms`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Event dropdown (8 events, show short_id + magnitude)           │
├────────────────────────────────────────────────────────────────┤
│ Stage toggle: [Raw trace] [Filtered] [STA/LTA overlay]         │
├────────────────────────────────────────────────────────────────┤
│ Plotly line chart (time vs amplitude, downsampled)             │
│ Vertical marker at P-pick time                                 │
├────────────────────────────────────────────────────────────────┤
│ Metrics sidebar: SNR, P-pick, duration (from per-event JSON)   │
│ Link: preprocessing figure PNG · NPZ on GitHub                 │
└────────────────────────────────────────────────────────────────┘
```

**Fallback state:** If NPZ conversion not run, show static preprocessing figures with explanation.

---

### 5.8 Documentation hub (`/docs/[[...slug]]`)

```text
┌──────────────┬─────────────────────────────────────────────────┐
│ Sidebar      │ Document title                                  │
│              │ ─────────────────────────────────────────────── │
│ Governance   │ Rendered Markdown body                          │
│  Charter     │                                                 │
│  Status      │ Tables, code blocks, images                     │
│ Phase reports│                                                 │
│  EDA         │ ─────────────────────────────────────────────── │
│  Signal      │ [View on GitHub] · Last updated · Related →     │
│  ...         │                                                 │
│ Reference    │                                                 │
└──────────────┴─────────────────────────────────────────────────┘
```

**Sidebar groups:**
1. Governance (Charter, Status, Roadmap, Research Direction)
2. Phase reports (EDA through Results)
3. Submission (Reproducibility, Data Availability)
4. Reference (Glossary, Beginner Guide, EarthESND notes)

Mobile: sidebar collapses to sticky TOC dropdown at top.

---

### 5.9 Final report (`/report`)

```text
┌────────────────────────────────────────────────────────────────┐
│ [Markdown view | PDF view] toggle                              │
├────────────────────────────────────────────────────────────────┤
│ Sticky TOC (right on desktop, collapsible on mobile)           │
│ Full Research_Report_Final.md rendered                         │
│ OR PDF.js viewer for Research_Report_Final.pdf                 │
├────────────────────────────────────────────────────────────────┤
│ Download links: MD on GitHub · PDF in FINAL_SUBMISSION         │
└────────────────────────────────────────────────────────────────┘
```

---

### 5.10 Submission package (`/submission`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Validation banner: PASS (from VALIDATION_SUMMARY.json)         │
├────────────────────────────────────────────────────────────────┤
│ Grid of deliverable cards:                                     │
│  D-F1 Report · D-F2 Presentation · D-F3 Script                 │
│  D-S1 Reproducibility · D-S2 Data Availability                 │
│ Each card: icon, description, [View PDF] [Source MD]           │
├────────────────────────────────────────────────────────────────┤
│ Embedded PDF viewer when card selected                         │
└────────────────────────────────────────────────────────────────┘
```

---

### 5.11 Timeline (`/timeline`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Vertical timeline with two tracks:                             │
│  ● v1.0 (complete, grey/green) — acquisition through submission│
│  ○ v2.0 (planned, blue) — website phases from V2_ROADMAP       │
│  ○ v3.0 (future, dashed) — AI, live data, Europe expansion     │
├────────────────────────────────────────────────────────────────┤
│ Milestone cards expand to show deliverables + doc links        │
└────────────────────────────────────────────────────────────────┘
```

---

### 5.12 About (`/about`)

```text
┌────────────────────────────────────────────────────────────────┐
│ Programme context (AMGCR, Swiss certificate)                     │
│ Author / affiliation (if added to repo)                        │
│ Technology stack (Python v1 · Next.js v2)                      │
│ EarthESND reference disclaimer                                   │
│ Licence and citations                                          │
│ Contact / LinkedIn (optional, user-provided)                   │
└────────────────────────────────────────────────────────────────┘
```

---

## 6. Interactive pages summary

| Page | Primary interaction | Library |
|------|---------------------|---------|
| Events map | Pan, zoom, marker popups | Leaflet |
| Feature correlation | Hover values, zoom | Plotly |
| Feature distributions | Toggle features | Plotly |
| Waveform viewer | Event select, stage toggle | Plotly |
| Report PDF | Page nav, zoom | PDF.js |
| Doc pages | Anchor TOC scroll-spy | Native + Intersection Observer |
| Homepage pipeline | Hover/click steps | Framer Motion |

**Performance rule:** Lazy-load Plotly, Leaflet, and PDF.js only on routes that need them (`next/dynamic` with `ssr: false` where appropriate).

---

## 7. Mobile responsiveness

### 7.1 Breakpoints (Tailwind defaults)

| Breakpoint | Width | Layout changes |
|------------|-------|----------------|
| `sm` | ≥640px | Single → two-column where noted |
| `md` | ≥768px | Sidebar docs visible |
| `lg` | ≥1024px | Full desktop nav; TOC sidebar on report |
| `xl` | ≥1280px | Max content width 1280px centred |

### 7.2 Mobile-specific patterns

| Component | Mobile behaviour |
|-----------|------------------|
| Navigation | Hamburger + full-screen overlay |
| Data tables | Horizontal scroll with shadow hint; sticky first column |
| Plotly charts | Full viewport width; simplified toolbars |
| Leaflet map | Fixed height 300px; touch gestures enabled |
| PDF viewer | Full-screen mode option |
| Metric strip | 2×2 grid instead of 4-column |
| Figure carousel | Swipe gestures |

### 7.3 Touch targets

Minimum 44×44 px for all interactive elements (buttons, nav items, map controls).

---

## 8. Accessibility

### 8.1 WCAG 2.1 AA targets

| Requirement | Implementation |
|-------------|----------------|
| **Colour contrast** | Text ≥4.5:1; large text ≥3:1; test semantic colours |
| **Keyboard navigation** | All nav, tabs, tables, modals reachable via Tab |
| **Focus indicators** | Visible focus rings on all interactives |
| **Alt text** | All figures: alt from report captions or auto-generated descriptive text |
| **Heading hierarchy** | One h1 per page; logical h2–h4 in docs |
| **Skip link** | "Skip to main content" as first focusable element |
| **Reduced motion** | Respect `prefers-reduced-motion`; disable count-up and carousel auto-advance |
| **Chart accessibility** | Plotly: include data table fallback toggle ("View as table") |
| **Map accessibility** | List view alternative for all map data (Events table) |
| **PDF accessibility** | Link to tagged PDF; MD alternative always available |

### 8.2 Screen reader considerations

- Announce route changes (Next.js `aria-live` region in layout)
- Table headers properly associated (`<th scope="col">`)
- Chart summaries as visually hidden text (e.g. "Correlation heatmap showing high collinearity among amplitude features")

### 8.3 Testing checklist (implementation phase)

- [ ] axe-core zero critical violations on 6 key pages
- [ ] Keyboard-only navigation end-to-end
- [ ] VoiceOver / NVDA spot check on Report and Explore pages
- [ ] Lighthouse Accessibility ≥ 95

---

## 9. Visual design language

### 9.1 Brand personality

**Professional research portfolio** — credible, calm, evidence-led. Not a startup landing page; not a generic Bootstrap admin template.

**Tone:** Scientific clarity with subtle seismic motif (restrained, not literal disaster imagery).

### 9.2 Colour palette

| Token | Hex (proposed) | Usage |
|-------|----------------|-------|
| `--color-primary` | `#1e3a5f` | Nav, headings, links (deep seismic blue) |
| `--color-primary-light` | `#2d5a87` | Hover states |
| `--color-accent` | `#c45c26` | CTAs, P-wave marker, timeline active (warm accent) |
| `--color-success` | `#2d6a4f` | Validation PASS, completed milestones |
| `--color-warning` | `#b8860b` | Limitations callouts |
| `--color-surface` | `#f8f9fb` | Page background |
| `--color-surface-elevated` | `#ffffff` | Cards |
| `--color-text` | `#1a1a2e` | Body text |
| `--color-text-muted` | `#5c6370` | Captions, metadata |
| `--color-border` | `#e2e8f0` | Dividers, table borders |

**Dark mode:** Optional Phase 7 enhancement; not required for v2.0 MVP. Design tokens in CSS variables to enable later.

### 9.3 Typography

| Role | Font (proposed) | Fallback |
|------|-----------------|----------|
| Headings | **Source Serif 4** (Google Fonts, free) | Georgia, serif |
| Body | **Inter** (Google Fonts, free) | system-ui, sans-serif |
| Code / data | **JetBrains Mono** | monospace |

**Scale:** Tailwind `text-base` (16px) body; `text-4xl`/`text-5xl` hero; line-height 1.6 for prose.

### 9.4 Spacing and layout

- Max content width: `max-w-7xl` (1280px)
- Prose width for long-form MD: `max-w-3xl` or `prose lg:prose-lg`
- Card padding: `p-6`; section vertical rhythm: `py-16`/`py-24`
- Border radius: `rounded-lg` cards; `rounded-md` buttons

### 9.5 Iconography and imagery

- **Icons:** Lucide (outline, 20–24px)
- **Figures:** Render v1.0 PNGs at native resolution; lazy load
- **Hero:** Optional subtle topographic pattern (CSS/SVG, no stock photo)
- **No gratuitous earthquake disaster imagery**

### 9.6 Motion design (Framer Motion)

| Element | Animation | Duration |
|---------|-----------|----------|
| Page enter | Fade + slight y translate | 300ms |
| Metric count-up | Number tween on viewport enter | 800ms |
| Card hover | Scale 1.02 + shadow | 200ms |
| Timeline nodes | Stagger reveal on scroll | 400ms |
| Chart enter | Fade in after data load | 250ms |

All animations disabled when `prefers-reduced-motion: reduce`.

### 9.7 Component styling patterns

| Component | Style |
|-----------|-------|
| **MetricCard** | White card, large number, small label, optional trend icon |
| **PhaseStepper** | Connected dots; completed = green fill; current = accent ring |
| **Callout** | Left border accent; icons for info/warning/limitation |
| **DataTable** | Zebra striping; sticky header; monospace for IDs |
| **DocProse** | Tailwind Typography plugin; styled tables and code blocks |
| **GitHubLink** | Button variant with GitHub icon; opens new tab |

---

## 10. v3 UI hooks (future, no v2 implementation)

| Hook | Location | Purpose |
|------|----------|---------|
| Search bar | Header (disabled/placeholder in v2) | Semantic search |
| Chat FAB | Bottom-right floating button slot | AI assistant |
| Live layer toggle | Event map | Real-time earthquakes |
| "Ask about this section" | Report page margin | Contextual RAG chat |

v2.0 ships with **placeholder-free** layout unless explicitly approved; hooks are **CSS grid reservations** only (documented in component comments during implementation).

---

## 11. Content tone and microcopy

| Context | Example copy |
|---------|--------------|
| Pilot disclaimer | "Results from 8 California events (2024). Illustrative only—not operational EEW." |
| Source link | "View source file on GitHub" |
| Missing figure | "Figure not bundled. Regenerate per Reproducibility Statement (D-S1)." |
| Europe roadmap | "Planned Version 2.0+ science track—not included in v1.0 submission." |
| EarthESND | "Literature reference (optional v3.0 track). Not the geographic endpoint." |

---

## 12. Document control

| Field | Value |
|-------|-------|
| **Version** | 2.0.0-plan |
| **Date** | 2026-08-01 |
| **Status** | Awaiting approval before implementation |
| **Related** | [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md) · [V2_ROADMAP.md](V2_ROADMAP.md) · [V2_DEPLOYMENT_PLAN.md](V2_DEPLOYMENT_PLAN.md) |
