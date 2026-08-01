# Website CHANGELOG

All notable changes to the **Version 2.0 interactive platform** (`website/`).  
Scientific releases remain documented in the repository root [CHANGELOG.md](../CHANGELOG.md) (v1.0.0 frozen).

---

## [2.0.0] — 2026-08-02 (Public release preparation)

### Added
- Full interactive research platform (Phases 1–12)
- Homepage hero slideshow with earthquake/seismic imagery
- Research Dashboard (`/dashboard`)
- Workflow Explorer (`/workflow`)
- Results Explorer (`/results`) — figures and tables
- Dataset Explorer (`/dataset`)
- Waveform Explorer (`/waveforms`)
- Earthquake Map (`/map`) — Leaflet + OpenStreetMap
- Resources hub (`/resources`)
- Documentation portal (`/docs`, `/research/report`)
- Global search (`Ctrl+K`) — build-time search index
- GitHub integration page (`/github`)
- Researcher About page (`/about`)
- Contact page (`/contact`)
- SEO: sitemap, robots.txt, Open Graph, Twitter cards, JSON-LD
- Error pages: 404, error boundary, global error, loading skeletons
- Back-to-top control, focus-visible polish, empty states

### Infrastructure
- Build pipeline: asset sync + search index + Next.js static generation
- Vercel Hobby deployment configuration documented
- GitHub Pages fallback documented (static export path)

### Unchanged
- **Version 1.0 science** — no modifications to analysis scripts, reports, or submission package

---

## Pre-release phases (summary)

| Phase | Focus |
|-------|--------|
| 1–5 | Foundation, docs portal, homepage, workflow, results |
| 6–9 | Dataset, waveforms, map, dashboard |
| 10 | Global search, GitHub page, navigation |
| 11 | Performance, SEO, accessibility, UX polish |
| 12 | Testing, deployment prep, release documentation |

---

## [0.1.0] — 2026-07-29

- Initial Next.js scaffold (Phase 1 foundation)
