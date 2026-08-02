# Version 2.0 Known Limitations

**Platform:** AMGCR Earthquake Early Warning Research (website/)  
**Science baseline:** v1.0.0 (unchanged)  
**Platform version:** 2.0.0

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
| **Hero images in repository** | `public/hero/slide-*.png` (five PNGs) are committed with the website — included on clone and deploy. |
| **Build-generated assets** | Figures, tables, waveforms, and search index are created by `npm run build` — not committed. |
| **Canonical URL dependency** | Production SEO requires `NEXT_PUBLIC_SITE_URL` environment variable. |
| **GitHub Pages** | Requires static export (`output: 'export'`) — not the default configuration. Vercel is recommended. |
| **GitHub repo URL** | Default points to `prasun-iitj/AMGCR-Earthquake-Early-Warning`; override with `NEXT_PUBLIC_GITHUB_REPO_URL` if the repository moves. |

---

## 3. Content & UI

| Limitation | Detail |
|------------|--------|
| **GitHub not in header** | `/github` accessible via footer, resources, and search — not main navigation. |
| **Presentation PDF** | Linked externally on GitHub; not embedded in site (Version 2.1 candidate). |
| **Europe dataset** | Documented as Version 3.0 direction; platform shows California pilot only. |

---

## 4. Technical debt (non-blocking)

| Item | Severity | Detail |
|------|----------|--------|
| **No automated E2E tests** | Medium | Manual and HTTP verification only; no Playwright/Cypress suite (Version 2.1). |
| **Turbopack NFT warning** | Low | Build-time trace warning from `lib/content/stats.ts` filesystem reads — build succeeds. |

---

## 5. Browser & accessibility

| Limitation | Detail |
|------------|--------|
| **Light theme only** | Site forces light colour scheme; dark mode OS setting is overridden. |
| **Map tile dependency** | Earthquake map requires OpenStreetMap tile servers (external network). |
| **Leaflet bundle size** | Map page loads larger client JS — acceptable on broadband; slower on 2G. |
| **Lighthouse on localhost** | Scores vary; run on production URL for authoritative metrics. |
| **Decorative hero images** | Background slides use `alt=""` with sr-only descriptions — intentional for decorative imagery. |

---

## 6. Out of scope for v2.0 (Version 2.1 / 3.0)

The following remain on [ROADMAP.md](ROADMAP.md):

**Version 2.1:** production deployment hardening, contact-form backend, embedded PDF, E2E tests  
**Version 3.0:** Europe dataset expansion (ORFEUS/EIDA), ML model training UI, real-time SeedLink streaming, operational EEW deployment, K-NET paper reproduction track

---

## 7. Reporting issues

For platform bugs: GitHub Issues on [prasun-iitj/AMGCR-Earthquake-Early-Warning](https://github.com/prasun-iitj/AMGCR-Earthquake-Early-Warning) (`website/` label).  
For science questions: refer to v1.0 submission report and reproducibility statement.
