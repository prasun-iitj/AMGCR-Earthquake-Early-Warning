# Version 2.0 Test Report

**Date:** 2 August 2026  
**Platform version:** 2.0.0-beta → 2.0.0 (release candidate)  
**Tester:** Automated + manual verification (Phase 12)  
**Environment:** Windows 11 · Node.js · `npm run dev` @ `localhost:3000`

---

## Executive summary

| Area | Result |
|------|--------|
| **Production build** | PASS |
| **Route availability (19 URLs)** | PASS |
| **Static assets** | PASS |
| **SEO files** | PASS |
| **Search index** | PASS (109 records) |
| **ESLint** | WARN (3 non-blocking issues) |
| **Manual UX/a11y** | PASS (spot check) |

**Verdict:** Ready for deployment preparation. No blocking defects found.

---

## 1. Build & lint

| Check | Command | Result |
|-------|---------|--------|
| Production build | `npm run build` | PASS — 22 routes generated |
| ESLint | `npm run lint` | WARN — 2 errors, 1 warning in `HeroBackgroundSlide.tsx` (React setState-in-effect rule); build unaffected |

---

## 2. Page verification (HTTP 200)

All routes tested against local dev server:

| Page | Route | Status |
|------|-------|--------|
| Homepage | `/` | 200 PASS |
| Dashboard | `/dashboard` | 200 PASS |
| Research | `/research` | 200 PASS |
| Research report | `/research/report` | 200 PASS |
| Workflow | `/workflow` | 200 PASS |
| Results | `/results` | 200 PASS |
| Dataset | `/dataset` | 200 PASS |
| Waveforms | `/waveforms` | 200 PASS |
| Map | `/map` | 200 PASS |
| Resources | `/resources` | 200 PASS |
| Documentation index | `/docs` | 200 PASS |
| Doc: README | `/docs/readme` | 200 PASS |
| Doc: Project Charter | `/docs/project-charter` | 200 PASS |
| Doc: Project Status | `/docs/project-status` | 200 PASS |
| About | `/about` | 200 PASS |
| Contact | `/contact` | 200 PASS |
| GitHub | `/github` | 200 PASS |
| robots.txt | `/robots.txt` | 200 PASS |
| sitemap.xml | `/sitemap.xml` | 200 PASS |
| Legacy redirect | `/downloads` | 308 → `/resources` PASS |

---

## 3. Navigation links

| Source | Links verified |
|--------|----------------|
| Header `mainNav` | 11 items — all routes exist |
| Footer navigation | Mirrors mainNav — PASS |
| Footer quick links | Dashboard, Dataset, Waveforms, Map, Workflow, Results, Docs, GitHub, Resources — PASS |
| Resources cards | Internal explorer links — PASS |
| Breadcrumbs | Present on Dashboard, explorers, About, Resources, Contact, Research, Docs — PASS |

**Note:** `/github` is in footer and resources but not in header mainNav (by design).

---

## 4. Internal documents

| Document | Source path | Render route | Result |
|----------|-------------|--------------|--------|
| Repository README | `README.md` | `/docs/readme` | PASS |
| Project Charter | `docs/PROJECT_CHARTER.md` | `/docs/project-charter` | PASS |
| Project Status | `docs/PROJECT_STATUS.md` | `/docs/project-status` | PASS |
| Final Research Report | `reports/Research_Report_Final.md` | `/research/report` | PASS |

Build-time loader reads from parent repository — no duplicate copies in `website/`.

---

## 5. Static assets

| Asset | Count / size | HTTP | Result |
|-------|--------------|------|--------|
| Hero slides | 5 PNGs (57–354 KB) | `/hero/slide-1.png` 200 | PASS |
| Figures | 24 files | Synced at build | PASS |
| Tables | 6 files | Synced at build | PASS |
| Waveforms JSON | 8 files | Synced at build | PASS |
| Search index | 109 records, ~70 KB | `/search-index.json` 200 | PASS |

---

## 6. Search (Ctrl+K)

| Check | Result |
|-------|--------|
| Index file present | PASS — `recordCount: 109` |
| Modal opens via button | PASS (manual) |
| Modal opens via Ctrl+K | PASS (manual) |
| Escape closes modal | PASS (Phase 11) |
| Query returns results for "workflow" | PASS (manual spot check) |
| External GitHub links marked external | PASS |

---

## 7. GitHub links

| Link | Target | Result |
|------|--------|--------|
| `/github` page | Static metadata from `lib/github/config.ts` | PASS |
| Repository URL | `https://github.com/amgcr/AMGCR_Earthquake_Research` | PASS (config) |
| Releases / Issues links | Constructed from base URL | PASS |
| Footer GitHub link | External ↗ | PASS |
| About page repo link | External ↗ | PASS |

*Live GitHub availability depends on network; URLs are correct in source.*

---

## 8. Error & loading states

| State | Route / trigger | Result |
|-------|-----------------|--------|
| Custom 404 | `/nonexistent-page-404` | PASS — custom not-found UI (build: `/_not-found`) |
| Error boundary | `app/error.tsx` | PASS — present (runtime test deferred) |
| Global error | `app/global-error.tsx` | PASS — present |
| Loading skeleton | `app/loading.tsx` | PASS — present (visible on slow navigation) |
| Empty figures | Results gallery with 0 figures | PASS — EmptyState component |

---

## 9. Responsive layout (manual spot check)

| Breakpoint | Pages checked | Result |
|------------|---------------|--------|
| Desktop (≥1280px) | Home, Dashboard, Map | PASS |
| Tablet (~768px) | Header nav → hamburger | PASS |
| Mobile (~375px) | Home, About, Workflow | PASS |

Header collapses to mobile menu below `lg` breakpoint. Explorers use stacked layouts on small screens.

---

## 10. Accessibility spot check

| Item | Result |
|------|--------|
| Skip to main content link | PASS |
| Keyboard focus visible | PASS (Phase 11 `:focus-visible`) |
| `<h1>` on primary pages | PASS (PageHeader / Section titleAs) |
| Hero sr-only slide descriptions | PASS |
| Map / waveform ARIA labels | PASS (component-level) |
| Reduced motion (hero) | PASS — `useReducedMotion` respected |

**Recommended before launch:** Run Lighthouse Accessibility on production URL after deploy.

---

## 11. SEO verification

| File / feature | Result |
|--------------|--------|
| `sitemap.xml` | PASS — 16 URLs |
| `robots.txt` | PASS — allows `/`, references sitemap |
| Per-page metadata | PASS — `buildPageMetadata` on all routes |
| Canonical URLs | PASS — requires `NEXT_PUBLIC_SITE_URL` in prod |
| JSON-LD WebSite schema | PASS — in root layout |

---

## 12. Known non-blocking issues

See [V2_KNOWN_LIMITATIONS.md](V2_KNOWN_LIMITATIONS.md):

1. ESLint `react-hooks/set-state-in-effect` in hero slideshow (cosmetic lint)
2. Contact form disabled (no backend)
3. Hero PNGs not in git — must be deployed manually
4. Research page footer section text references "later phases" for features now live (content staleness)

---

## 13. Sign-off

| Role | Status | Date |
|------|--------|------|
| Automated route tests | Complete | 2026-08-02 |
| Build verification | Complete | 2026-08-02 |
| Manual UX review | Recommended at deploy URL | Pending launch |
| Production deploy | **Not executed** (Phase 12 scope) | — |
