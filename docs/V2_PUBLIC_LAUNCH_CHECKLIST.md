# Version 2.0 Public Launch Checklist

**Use this checklist before the first production deployment.**  
Phase 12 prepares but does **not** execute deployment or publication.

---

## Pre-launch — repository

- [ ] Version 1.0 science unchanged (`src/`, `FINAL_SUBMISSION/`, analysis scripts)
- [ ] `website/` builds cleanly: `npm run build`
- [ ] `npm run lint` passes (0 errors, 0 warnings)
- [ ] Hero images present: `website/public/hero/slide-1.png` … `slide-5.png` (committed)
- [ ] OG image present: `website/public/og-image.png`
- [ ] Git tag planned: `v2.0.0-website-release` or team convention
- [ ] `siteConfig.version` is `2.0.0` in `website/lib/navigation.ts`
- [ ] `website/CHANGELOG.md` reviewed
- [ ] Release docs complete:
  - [ ] [V2_RELEASE_NOTES.md](V2_RELEASE_NOTES.md)
  - [ ] [V2_DEPLOYMENT_GUIDE.md](V2_DEPLOYMENT_GUIDE.md)
  - [ ] [V2_TEST_REPORT.md](V2_TEST_REPORT.md)
  - [ ] [V2_KNOWN_LIMITATIONS.md](V2_KNOWN_LIMITATIONS.md)

---

## Pre-launch — environment

- [ ] `NEXT_PUBLIC_SITE_URL` set to production URL (Vercel)
- [ ] `NEXT_PUBLIC_GITHUB_REPO_URL` set if using a fork (default: `prasun-iitj/AMGCR-Earthquake-Early-Warning`)
- [ ] `.env.local` not committed (secrets check)
- [ ] Node.js 20 on CI/hosting platform

---

## Pre-launch — Vercel (primary)

- [ ] Vercel project created
- [ ] Root directory = `website`
- [ ] Build command = `npm run build`
- [ ] Environment variables configured
- [ ] Preview deployment tested
- [ ] Custom domain DNS configured (if applicable)
- [ ] HTTPS certificate active

---

## Pre-launch — functional smoke test (production URL)

### Pages
- [ ] `/` — Homepage hero, slideshow, all sections scroll
- [ ] `/dashboard` — Metrics load
- [ ] `/research` — Portal cards
- [ ] `/research/report` — Full report renders
- [ ] `/workflow` — Stage accordion works
- [ ] `/results` — Figures and tables visible
- [ ] `/dataset` — Dataset cards and journey
- [ ] `/waveforms` — Waveform list and viewer
- [ ] `/map` — Map tiles and markers
- [ ] `/resources` — Resource grid
- [ ] `/docs` — Documentation index
- [ ] `/docs/readme`, `/docs/project-charter`, `/docs/project-status`
- [ ] `/about` — Researcher profile
- [ ] `/contact` — Page loads
- [ ] `/github` — Links open correctly

### Platform
- [ ] Global search (`Ctrl+K`) returns results
- [ ] `/downloads` redirects to `/resources`
- [ ] Custom 404 page on bad URL
- [ ] Back-to-top button appears on scroll
- [ ] Mobile navigation opens/closes
- [ ] Skip link focuses main content

### SEO
- [ ] `/robots.txt` accessible
- [ ] `/sitemap.xml` lists all routes with correct domain
- [ ] Page titles and descriptions correct (view source)
- [ ] Open Graph preview checked (optional tool)

### Assets
- [ ] Hero images load (no blank hero)
- [ ] Result figures load
- [ ] Waveform charts render

---

## Pre-launch — accessibility & performance

- [ ] Lighthouse run on `/` (target: A11y ≥ 90, SEO ≥ 95)
- [ ] Lighthouse run on `/dashboard`
- [ ] Keyboard-only navigation test (header → main → footer)
- [ ] Screen reader spot check (one page)
- [ ] `prefers-reduced-motion`: hero static / no animation

---

## Launch day

- [ ] Merge to `main` (or release branch)
- [ ] Promote Vercel deployment to **Production**
- [ ] Verify production smoke test (section above)
- [ ] Announce release (programme / LinkedIn / repository README)

---

## Post-launch

- [ ] Monitor Vercel analytics (bandwidth, errors) — first 48 hours
- [ ] Create GitHub release notes linking to `docs/V2_RELEASE_NOTES.md`
- [ ] Update `docs/PROJECT_STATUS.md` with v2.0 platform live status (optional)
- [ ] Archive preview/staging URLs

---

## GitHub Pages fallback (optional)

- [ ] Only if Vercel unavailable
- [ ] Enable `output: 'export'` per deployment guide
- [ ] Configure `basePath` if using project Pages URL
- [ ] Deploy `out/` directory
- [ ] Re-run smoke tests on GH Pages URL

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| Programme lead | | | |

**Deployment executed:** ☐ No (Phase 12 — preparation only)
