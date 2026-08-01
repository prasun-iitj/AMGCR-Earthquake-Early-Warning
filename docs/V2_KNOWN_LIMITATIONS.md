# Version 2.0 Known Limitations

**Platform:** AMGCR Earthquake Early Warning Research (website/)  
**Science baseline:** v1.0.0 (unchanged)

This document lists intentional constraints and known gaps at the v2.0 public release. These are **not bugs** unless marked as defects.

---

## 1. Intentional scope limits

| Limitation | Detail |
|------------|--------|
| **No backend** | Static site + build-time data only. No API, database, or server-side runtime beyond hosting. |
| **No authentication** | All content is public. No user accounts or protected routes. |
| **No live data** | Waveforms, metrics, and manifests reflect the frozen v1.0 pilot — not live FDSN streams. |
| **No contact form submission** | Contact page form is disabled; use email links on About page. |
| **No AI features** | No chatbots, ML inference, or generative AI on the platform. |
| **No global sync** | Content updates require rebuild and redeploy from repository sources. |

---

## 2. Deployment & assets

| Limitation | Detail |
|------------|--------|
| **Hero images not in git** | `public/hero/slide-*.png` is gitignored. Deployments must include these files locally or CI artifact. |
| **Build-generated assets** | Figures, tables, waveforms, and search index are created by `npm run build` — not committed. |
| **Canonical URL dependency** | Production SEO requires `NEXT_PUBLIC_SITE_URL` environment variable. |
| **GitHub Pages** | Requires static export (`output: 'export'`) — not the default configuration. Vercel is recommended. |

---

## 3. Content & UI

| Limitation | Detail |
|------------|--------|
| **Research page stale copy** | "Available in later phases" section lists explorers that now exist (map, waveforms, etc.). Content update deferred to avoid redesign scope. |
| **GitHub not in header** | `/github` accessible via footer, resources, and search — not main navigation. |
| **Presentation PDF** | Linked externally on GitHub; not embedded in site. |
| **Europe dataset** | Documented as future direction; platform shows California pilot only. |

---

## 4. Technical debt (non-blocking)

| Item | Severity | Detail |
|------|----------|--------|
| ESLint in hero slideshow | Low | `react-hooks/set-state-in-effect` warnings in `HeroBackgroundSlide.tsx` — functional, lint-only. |
| Platform version string | Low | `siteConfig.version` may read `2.0.0-beta` until launch tag — update at deploy. |
| No OG image asset | Low | Open Graph uses text metadata only; no dedicated `og-image.png` yet. |
| No automated E2E tests | Medium | Manual and HTTP verification only; no Playwright/Cypress suite. |

---

## 5. Browser & accessibility

| Limitation | Detail |
|------------|--------|
| **Light theme only** | Site forces light colour scheme; dark mode OS setting is overridden. |
| **Map tile dependency** | Earthquake map requires OpenStreetMap tile servers (external network). |
| **Leaflet bundle size** | Map page loads larger client JS — acceptable on broadband; slower on 2G. |
| **Lighthouse on localhost** | Scores vary; run on production URL for authoritative metrics. |

---

## 6. Out of scope for v2.0

The following remain on [ROADMAP.md](ROADMAP.md):

- Europe dataset expansion (ORFEUS/EIDA)
- ML model training UI
- Real-time SeedLink streaming
- Production EEW operational deployment
- K-NET paper reproduction track

---

## 7. Reporting issues

For platform bugs: GitHub Issues on `amgcr/AMGCR_Earthquake_Research` (website/ label).  
For science questions: refer to v1.0 submission report and reproducibility statement.
