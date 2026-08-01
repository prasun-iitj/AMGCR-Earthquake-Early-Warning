# Version 2.0 Release Notes

**AMGCR Earthquake Early Warning Research — Interactive Platform**  
**Release date:** 2 August 2026  
**Platform version:** 2.0.0  
**Science baseline:** v1.0.0 (frozen 29 July 2026)

---

## Overview

Version 2.0 delivers a public-facing **interactive research platform** for the AMGCR Swiss certificate programme. The website presents reproducible earthquake early warning science, pilot results, and documentation without requiring visitors to navigate the GitHub repository first.

**Version 1.0 science is unchanged.** All analysis scripts, reports, figures, and the FINAL_SUBMISSION package remain frozen.

---

## What's new

### Research exploration
- **Dashboard** — build-time project metrics, pipeline progress, repository inventory
- **Workflow Explorer** — interactive pipeline stages with links to artefacts
- **Results Explorer** — pilot figures (24) and CSV tables (6) with lightbox viewer
- **Dataset Explorer** — California FDSN pilot sources and data journey
- **Waveform Explorer** — eight pilot events with processing-stage previews
- **Earthquake Map** — Leaflet map of pilot event locations

### Documentation & dissemination
- **Documentation portal** — README, Project Charter, Project Status from repository Markdown
- **Research report** — full D-F1 narrative rendered at `/research/report`
- **Resources hub** — curated entry points to explorers and documentation
- **GitHub page** — repository structure, releases, and external links

### Homepage & identity
- Cinematic hero slideshow (earthquake/seismic imagery)
- Project highlights, workflow preview, timeline, featured downloads
- **About page** — researcher profile, academic supervision, technologies

### Platform quality (Phases 11–12)
- Global search (`Ctrl+K`) — 109 indexed records
- SEO: sitemap, robots.txt, Open Graph, Twitter cards, canonical URLs
- Accessibility: skip link, keyboard nav, ARIA, focus states, heading hierarchy
- Error handling: custom 404, error boundary, loading skeletons
- Performance: lazy hero slides, code-split search modal

---

## Technical stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS v4 |
| Motion | Framer Motion |
| Maps | Leaflet + react-leaflet |
| Content | Build-time Markdown from repository |
| Hosting | Vercel Hobby (primary) |

---

## Repository layout

```
website/                 ← Version 2.0 platform (this release)
├── app/                 ← Routes and pages
├── components/          ← UI and explorers
├── lib/                 ← Data loaders, SEO, navigation
├── public/              ← Synced assets + search index
├── scripts/             ← Build-time sync and index scripts
└── CHANGELOG.md         ← Website changelog

src/, scripts/analysis/  ← v1.0 science (FROZEN)
FINAL_SUBMISSION/        ← v1.0 submission (FROZEN)
```

---

## Upgrade from v1.0

There is no migration path — v2.0 is an **additive** communication layer. Scientists and reviewers should continue to cite:

- **Science release:** `v1.0.0` tag (29 July 2026)
- **Platform release:** `website/` at v2.0.0

---

## Acknowledgements

Developed as part of the Swiss certificate programme (AMGCR) under academic supervision at IIT Jodhpur (AIDE). See `/about` for full credits.

---

## Related documents

- [V2_DEPLOYMENT_GUIDE.md](V2_DEPLOYMENT_GUIDE.md)
- [V2_TEST_REPORT.md](V2_TEST_REPORT.md)
- [V2_KNOWN_LIMITATIONS.md](V2_KNOWN_LIMITATIONS.md)
- [V2_PUBLIC_LAUNCH_CHECKLIST.md](V2_PUBLIC_LAUNCH_CHECKLIST.md)
- [ROADMAP.md](ROADMAP.md) — future work beyond v2.0
