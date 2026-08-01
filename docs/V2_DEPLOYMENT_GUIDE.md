# Version 2.0 Deployment Guide

**Status:** Ready for manual deployment (Phase 12)  
**Primary host:** Vercel Hobby · **Fallback:** GitHub Pages (static export)

---

## 1. Prerequisites

| Requirement | Version |
|-------------|---------|
| Node.js | 20 LTS (recommended) |
| npm | 10+ |
| Git | Latest |
| Repository clone | Full clone including parent repo for Markdown sources |

**Do not modify** v1.0 science paths (`src/`, `scripts/analysis/`, `FINAL_SUBMISSION/`).

---

## 2. Environment variables

Copy `website/.env.example` to `website/.env.local` for local testing, or set in Vercel **Project → Settings → Environment Variables**:

| Variable | Required | Example |
|----------|----------|---------|
| `NEXT_PUBLIC_SITE_URL` | **Yes (production)** | `https://your-app.vercel.app` |
| `NEXT_PUBLIC_GITHUB_REPO_URL` | No | `https://github.com/amgcr/AMGCR_Earthquake_Research` |

Without `NEXT_PUBLIC_SITE_URL`, canonical URLs, Open Graph links, and sitemap default to `http://localhost:3000`.

---

## 3. Local build verification

From repository root:

```powershell
cd website
npm install
npm run build
npm run start
```

Open `http://localhost:3000` and confirm:
- All navigation links resolve
- `/search-index.json` returns 200
- `/sitemap.xml` and `/robots.txt` return 200
- Hero images load (`public/hero/slide-*.png` — committed in repo; see §6)

---

## 4. Primary deployment — Vercel Hobby

### 4.1 New project

1. Sign in at [vercel.com](https://vercel.com) with GitHub.
2. **Add New Project** → import `AMGCR_Earthquake_Research`.
3. Configure:

| Setting | Value |
|---------|--------|
| **Root Directory** | `website` |
| **Framework Preset** | Next.js (auto-detected) |
| **Build Command** | `npm run build` |
| **Output Directory** | *(leave default — Next.js)* |
| **Install Command** | `npm install` |

4. Add environment variable:
   - `NEXT_PUBLIC_SITE_URL` = `https://<your-vercel-domain>.vercel.app` (update after first deploy if using custom domain)

5. Deploy. Do **not** enable automatic production deploy until [V2_PUBLIC_LAUNCH_CHECKLIST.md](V2_PUBLIC_LAUNCH_CHECKLIST.md) is signed off.

### 4.2 Custom domain (optional)

1. Vercel → Project → **Domains** → add domain.
2. Update DNS per Vercel instructions.
3. Update `NEXT_PUBLIC_SITE_URL` to the custom domain.
4. Redeploy.

### 4.3 `vercel.json`

A minimal `website/vercel.json` is included. Vercel auto-detects Next.js; this file documents the intended build command explicitly.

---

## 5. Fallback deployment — GitHub Pages

GitHub Pages serves **static files only**. Next.js App Router requires static export.

### 5.1 Limitations on GitHub Pages

- No Node.js server (`next start` unavailable)
- Requires `output: 'export'` in `next.config.ts` (not enabled by default — enable only for GH Pages)
- Image optimization API unavailable (site already uses static assets)
- Base path may require `basePath` if publishing to `username.github.io/repo-name`

### 5.2 Static export procedure (manual)

1. In `website/next.config.ts`, add temporarily:
   ```typescript
   const nextConfig: NextConfig = {
     output: "export",
     images: { unoptimized: true },
     // ...existing redirects may need trailingSlash: true for GH Pages
   };
   ```
2. Build:
   ```powershell
   cd website
   npm run build
   ```
3. Output appears in `website/out/`.
4. Deploy `out/` to GitHub Pages (branch `gh-pages` or GitHub Actions artifact).

### 5.3 Recommended approach

Use **Vercel Hobby** for production. Reserve GitHub Pages for offline mirrors or institutional hosting that cannot use Vercel.

---

## 6. Static assets checklist

These paths are **gitignored** or **build-generated** — they must exist at deploy time:

| Path | Source |
|------|--------|
| `public/figures/` | `npm run build` → `sync-results-assets.mjs` |
| `public/tables/` | same |
| `public/waveforms/` | same + Python export |
| `public/search-index.json` | `build-search-index.mjs` |
| `public/hero/slide-*.png` | **Committed** in `website/public/hero/` (homepage slideshow) |

---

## 7. Build pipeline (what `npm run build` does)

```
1. scripts/sync-results-assets.mjs   → copies figures, tables, manifests; exports waveforms
2. scripts/build-search-index.mjs  → writes public/search-index.json
3. next build                        → static HTML for all routes
```

**Build time:** ~60–90 seconds (local, cold).  
**Output:** 22 static routes including `/robots.txt`, `/sitemap.xml`.

---

## 8. Post-deploy smoke test

Run after every production deploy:

```
GET /              → 200, hero visible
GET /dashboard     → 200
GET /search-index.json → 200, recordCount ≥ 100
GET /sitemap.xml   → 200, lists all routes
GET /robots.txt    → 200
GET /nonexistent   → 404 custom page
GET /downloads     → 308 → /resources
```

External (manual):
- GitHub repository link on `/github` opens `github.com/amgcr/AMGCR_Earthquake_Research`
- Open Graph preview (optional): [opengraph.xyz](https://www.opengraph.xyz/)

---

## 9. Rollback

**Vercel:** Deployments → select previous successful deployment → **Promote to Production**.

**GitHub Pages:** Revert commit and re-run Pages deploy workflow.

---

## 10. Related documents

- [V2_DEPLOYMENT_PLAN.md](V2_DEPLOYMENT_PLAN.md) — original architecture planning
- [V2_PUBLIC_LAUNCH_CHECKLIST.md](V2_PUBLIC_LAUNCH_CHECKLIST.md)
- [V2_TEST_REPORT.md](V2_TEST_REPORT.md)
- [V2_KNOWN_LIMITATIONS.md](V2_KNOWN_LIMITATIONS.md)
