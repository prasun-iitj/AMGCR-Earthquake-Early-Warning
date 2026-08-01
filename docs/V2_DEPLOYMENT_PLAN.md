# V2_DEPLOYMENT_PLAN.md

**Version 2.0 — Deployment Plan**

**Status:** Planning only (no implementation)  
**Architecture:** [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md) · **Roadmap:** [V2_ROADMAP.md](V2_ROADMAP.md)

---

## 1. Purpose

Define how the Version 2.0 interactive research platform is built, validated, deployed, and operated on **free infrastructure only**. No paid hosting, APIs, databases, or recurring subscriptions.

---

## 2. Deployment goals

| Goal | Target |
|------|--------|
| **Cost** | $0/month recurring |
| **Availability** | 99%+ (provider SLA on free tier) |
| **Build time** | < 10 minutes CI pipeline |
| **Deploy trigger** | Push to `main` (or manual workflow dispatch) |
| **Rollback** | Redeploy previous commit via CI |
| **Security** | HTTPS everywhere; no secrets in client bundle |

---

## 3. Hosting options comparison

### 3.1 Primary: Vercel Hobby (recommended)

| Aspect | Detail |
|--------|--------|
| **Cost** | Free for personal/non-commercial projects |
| **Next.js support** | Native App Router, SSR/SSG, edge middleware |
| **Custom domain** | Free SSL via Vercel |
| **Limits** | 100 GB bandwidth/month; 6000 build minutes/month (team); 1 concurrent build |
| **Root directory** | Set to `website/` in project settings |
| **Environment** | `NODE_VERSION=20`; `GITHUB_SHA` auto-injected |

**Why primary:** Best Next.js DX; no static export compromises; preview deployments per PR.

### 3.2 Alternative: GitHub Pages

| Aspect | Detail |
|--------|--------|
| **Cost** | Free for public repos |
| **Next.js support** | Requires `output: 'export'` (static HTML export) |
| **Custom domain** | Free via `CNAME` |
| **Limits** | 1 GB repo recommended size; 100 GB bandwidth/month (soft) |
| **Base path** | May require `basePath: '/AMGCR_Earthquake_Research'` for project pages |

**When to use:** Vercel unavailable; preference for all-in-GitHub workflow; fully static site acceptable.

### 3.3 Explicitly not used

| Service | Reason |
|---------|--------|
| AWS / GCP / Azure | Paid beyond free tier |
| Netlify Pro features | Unnecessary |
| Cloudflare Workers (paid) | Not needed for static v2 |
| Railway / Render | Free tier too limited / sleep |
| Supabase / Firebase | No backend in v2 |

---

## 4. Build process

### 4.1 Local development

```powershell
# From repository root
cd website
npm install
npm run dev          # http://localhost:3000
```

```powershell
# Production build (local verification)
npm run sync-content   # Copy JSON, CSV, figures, generate manifest
npm run validate-content
npm run build
npm run start          # or serve static export
```

### 4.2 npm scripts (planned)

| Script | Purpose |
|--------|---------|
| `dev` | Next.js dev server |
| `build` | `sync-content` → `validate-content` → `next build` |
| `sync-content` | Copy assets from parent repo; generate `content-manifest.json` |
| `validate-content` | Schema-check JSON/CSV; verify figure inventory |
| `convert-waveforms` | Optional Python NPZ → JSON (Phase 4) |
| `lint` | ESLint + TypeScript check |
| `test` | Vitest unit tests |
| `test:e2e` | Playwright smoke tests |

### 4.3 Monorepo layout note

The Next.js app lives in `website/` but reads content from parent directories (`../docs`, `../reports`, etc.) at **build time** via Node `fs`. Vercel project settings:

- **Root Directory:** `website`
- **Include source files outside root:** Enable (or use prebuild copy in CI checkout at repo root)

**Recommended Vercel approach:** Deploy from repository root with:

```json
// vercel.json (at repo root or website/)
{
  "buildCommand": "cd website && npm run build",
  "outputDirectory": "website/.next",
  "installCommand": "cd website && npm install",
  "framework": "nextjs"
}
```

Alternatively, configure Vercel "Root Directory" = `website` and ensure `sync-content.ts` uses paths relative to repo root (`path.join(process.cwd(), '..', 'reports')`).

### 4.4 Figure and PDF bundling

| Asset type | Strategy | Size estimate |
|------------|----------|---------------|
| PNG figures (24) | Copy to `website/public/figures/` at sync | ~5–15 MB |
| JSON/CSV summaries | Import or copy to `website/lib/data/generated/` | < 1 MB |
| PDFs (5–8 files) | Copy to `website/public/submission/` **or** link to GitHub Releases | 5–30 MB |
| Waveform JSON (8) | Downsampled, ~500 KB each | ~4 MB |

**PDF strategy (recommended):**

- **Option A (simple):** Bundle PDFs in static export; acceptable if total deploy < 100 MB
- **Option B (lean):** Host PDFs on GitHub Releases v1.0.0 assets; website links directly
- **Option C (hybrid):** Bundle report PDF only; link others to GitHub

Default: **Option C** for Vercel; **Option A** if GitHub Pages and sizes permit.

### 4.5 Figure regeneration in CI

Figures may be absent in clones (`reports/figures/` often local-only). CI step:

```yaml
# Pseudocode — see §6 for full workflow
- name: Check figures
  run: |
    if [ "$(ls reports/figures/*.png 2>/dev/null | wc -l)" -lt 24 ]; then
      pip install -r requirements.txt
      python scripts/analysis/run_california_pilot_eda.py
      python scripts/analysis/run_california_signal_analysis.py
      python scripts/analysis/run_california_preprocessing.py
      python scripts/analysis/run_california_feature_engineering.py
    fi
```

**Important:** Regeneration runs v1.0 scripts **read-only** (outputs only). Does not modify v1.0 source. Requires Python + dependencies in CI (cached).

**Fallback:** If regeneration fails (no raw MiniSEED in CI), deploy with figure-missing UI state and CI warning—not a hard fail for preview builds; **hard fail for production tag**.

---

## 5. Static export strategy

### 5.1 Vercel (default — no export required)

- Use Next.js SSG with Server Components at build time
- Dynamic routes pre-rendered via `generateStaticParams`
- API routes: **none in v2.0** (deferred to v3)

### 5.2 GitHub Pages (static export)

```typescript
// website/next.config.ts (GitHub Pages variant)
const isGithubPages = process.env.DEPLOY_TARGET === 'github-pages';

const nextConfig = {
  output: isGithubPages ? 'export' : undefined,
  basePath: isGithubPages ? '/AMGCR_Earthquake_Research' : '',
  images: { unoptimized: true }, // required for static export
  trailingSlash: true,
};
```

**Limitations with static export:**
- No SSR at request time
- No Next.js API routes (acceptable for v2)
- Image optimisation disabled (`unoptimized: true`)

**Output:** `website/out/` → deployed to `gh-pages` branch or GitHub Actions artifact.

### 5.3 Choosing export mode

| Criterion | Vercel | GitHub Pages export |
|-----------|--------|---------------------|
| Setup complexity | Low | Medium (basePath) |
| Preview PR deploys | Yes | Manual |
| PDF/figure size limits | Generous | Watch repo size |
| Custom domain | Easy | Easy |
| v3 API routes later | Supported | Requires migration |

**Recommendation:** Start with **Vercel Hobby**; maintain GitHub Pages workflow as documented fallback.

---

## 6. CI/CD recommendations

### 6.1 GitHub Actions workflow

File: `.github/workflows/deploy-website.yml`

```yaml
name: Deploy Website

on:
  push:
    branches: [main]
    paths:
      - 'website/**'
      - 'docs/**'
      - 'reports/**'
      - 'data/manifests/**'
      - 'FINAL_SUBMISSION/**'
      - '.github/workflows/deploy-website.yml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write      # only if using GitHub Pages
  id-token: write

jobs:
  validate-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: website/package-lock.json

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Python deps (conditional figure regen)
        run: pip install -r requirements.txt

      - name: Ensure figures exist
        run: bash website/scripts/ci-ensure-figures.sh

      - name: Install website deps
        working-directory: website
        run: npm ci

      - name: Validate content
        working-directory: website
        run: npm run validate-content

      - name: Build website
        working-directory: website
        env:
          NEXT_PUBLIC_GITHUB_SHA: ${{ github.sha }}
          NEXT_PUBLIC_BUILD_DATE: ${{ github.event.head_commit.timestamp }}
        run: npm run build

      - name: Run tests
        working-directory: website
        run: npm test

      # Deploy job splits here — Vercel OR GitHub Pages
```

### 6.2 Vercel deployment integration

**Option A — Vercel Git integration (simplest):**
- Connect GitHub repo in Vercel dashboard
- Root: `website`
- Auto-deploy on push; GitHub Actions runs validation only

**Option B — GitHub Actions → Vercel CLI:**
```yaml
      - name: Deploy to Vercel
        run: npx vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
        working-directory: website
```
Requires `VERCEL_TOKEN` secret (free account).

**Recommendation:** Option A for simplicity; Option B if CI gates must block deploy.

### 6.3 GitHub Pages deployment job

```yaml
  deploy-pages:
    needs: validate-and-build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/upload-pages-artifact@v3
        with:
          path: website/out

      - uses: actions/deploy-pages@v4
        id: deployment
```

Enable GitHub Pages source: "GitHub Actions" in repository settings.

### 6.4 CI caching

| Cache | Path | Benefit |
|-------|------|---------|
| npm | `website/node_modules` | Faster installs |
| pip | `~/.cache/pip` | Faster Python deps |
| Next.js | `website/.next/cache` | Faster rebuilds |
| Figures | `reports/figures/` | Skip regeneration if cached artefact |

### 6.5 Branch and environment strategy

| Branch | Deploy target | Purpose |
|--------|---------------|---------|
| `main` | Production (Vercel prod / gh-pages) | Live site |
| PR branches | Vercel preview (automatic) | Review UI changes |
| `v2.0.0` tag | Immutable release snapshot | Portfolio link stability |

---

## 7. Domain strategy (optional)

All options below are **free** or use domains the user already owns.

### 7.1 Default URLs (no custom domain)

| Provider | URL pattern |
|----------|-------------|
| Vercel | `amgcr-earthquake-research.vercel.app` (project name) |
| GitHub Pages | `username.github.io/AMGCR_Earthquake_Research` |

### 7.2 Custom domain (optional)

If the user owns a domain (e.g. from Namecheap, ~$10/year — **not a platform subscription**):

| Step | Action |
|------|--------|
| 1 | Add domain in Vercel or GitHub Pages settings |
| 2 | Create DNS `CNAME` record pointing to Vercel/`username.github.io` |
| 3 | Enable automatic SSL (Let's Encrypt — free) |
| 4 | Add `www` redirect if desired |

**Suggested subdomain:** `earthquake-research.example.com` or `amgcr.example.com`

**v2.0 default:** Use free provider subdomain unless user supplies a domain.

### 7.3 Canonical URL and SEO

- Set `metadataBase` in Next.js layout to production URL
- Configure single canonical host (apex or www, not both)
- Add `<link rel="canonical">` per page

---

## 8. Performance optimization

### 8.1 Build-time optimizations

| Technique | Application |
|-----------|-------------|
| SSG | Pre-render all public routes |
| Dynamic imports | Plotly, Leaflet, PDF.js loaded on demand |
| Tree shaking | Import only required Plotly chart types |
| Image optimisation | Next.js `<Image>` for figures (Vercel); `unoptimized` on GH Pages |
| Font subsetting | Google Fonts `display=swap`; preload Inter only |
| Content manifest | Avoid runtime file system reads |

### 8.2 Runtime optimizations

| Technique | Application |
|-----------|-------------|
| Lazy loading | Figures below fold use `loading="lazy"` |
| Code splitting | Route-based automatic via Next.js |
| Prefetch | `<Link prefetch>` for nav routes |
| CSV parsing | Parse once at build; serialize to JSON for client pages |
| Debounce | Map/table filter inputs debounced 200ms |

### 8.3 Bundle size targets

| Bundle | Target (gzip) |
|--------|---------------|
| Homepage initial JS | < 150 KB |
| Plotly route | < 500 KB (lazy) |
| Leaflet route | < 200 KB (lazy) |
| PDF viewer route | < 300 KB (lazy) |

### 8.4 Lighthouse targets (production)

| Page | Performance | Accessibility | Best Practices | SEO |
|------|-------------|---------------|----------------|-----|
| Homepage | ≥ 90 | ≥ 95 | ≥ 95 | ≥ 90 |
| Report | ≥ 85 | ≥ 95 | ≥ 95 | ≥ 85 |
| Explore/features | ≥ 80 | ≥ 95 | ≥ 90 | ≥ 80 |

Run Lighthouse in CI with `@lhci/cli` on built static HTML or deployed preview URL.

---

## 9. SEO strategy

### 9.1 On-page SEO

| Element | Implementation |
|---------|----------------|
| **Title template** | `%s · AMGCR Earthquake Research` |
| **Meta description** | Unique per page; homepage ≤ 160 chars |
| **Open Graph** | `og:title`, `og:description`, `og:image` (hero figure or logo) |
| **Twitter card** | `summary_large_image` |
| **Structured data** | JSON-LD `ScholarlyArticle` on report page; `Dataset` on explore page |
| **Sitemap** | Auto-generated `sitemap.xml` at build |
| **robots.txt** | Allow all; point to sitemap |

### 9.2 Homepage meta description (draft)

> Reproducible AI-assisted Earthquake Early Warning research for Western seismic regions. Europe-focused programme with completed California FDSN pilot—8 events, 18 ML-ready features, full open documentation.

### 9.3 Content SEO principles

- Render full report text in HTML (not PDF-only) for indexing
- Use semantic headings matching report structure
- Internal links between related docs and explore pages
- GitHub remains canonical for citations; website adds discoverability

### 9.4 Submission to search engines

- Manual Google Search Console submission (free) after deploy
- Optional Bing Webmaster Tools (free)
- No paid SEO tools

---

## 10. Analytics (free only)

### 10.1 Options

| Tool | Cost | Privacy | Recommendation |
|------|------|---------|----------------|
| **None** | Free | Best | Acceptable for portfolio |
| **Umami Cloud** | Free tier | Good | Lightweight page views |
| **Plausible self-hosted** | Free (self-host) | Excellent | Requires server (skip for v2) |
| **Vercel Analytics** | Free tier (limited) | Good | If already on Vercel |
| **Google Analytics** | Free | Poor privacy | **Avoid** unless user insists |

**Recommendation:** Deploy **without analytics** initially. Add **Umami Cloud free tier** or **Vercel Web Analytics** if traffic metrics needed.

### 10.2 Implementation (if enabled)

```typescript
// website/app/layout.tsx — conditional
{process.env.NEXT_PUBLIC_UMAMI_WEBSITE_ID && (
  <Script
    src="https://cloud.umami.is/script.js"
    data-website-id={process.env.NEXT_PUBLIC_UMAMI_WEBSITE_ID}
    strategy="afterInteractive"
  />
)}
```

- No cookies banner required for Umami (no personal data)
- Document analytics choice in privacy note on About page

---

## 11. Security and headers

### 11.1 HTTP headers (Vercel `vercel.json` or Next.js config)

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://*.tile.openstreetmap.org; connect-src 'self' https://api.github.com;"
        }
      ]
    }
  ]
}
```

Adjust CSP when analytics enabled.

### 11.2 Secrets management

| Secret | Required? | Storage |
|--------|-----------|---------|
| `VERCEL_TOKEN` | Only for CLI deploy | GitHub Secrets |
| `NEXT_PUBLIC_*` | Build metadata only | CI env (not secret) |
| API keys | **None in v2** | — |

---

## 12. Monitoring and maintenance

### 12.1 Free monitoring

| Check | Tool |
|-------|------|
| Deploy status | GitHub Actions + Vercel dashboard |
| Uptime | UptimeRobot free tier (optional, 50 monitors) |
| Broken links | `validate-content.ts` in CI |
| Dependency updates | Dependabot (GitHub, free) |

### 12.2 Maintenance cadence

| Task | Frequency |
|------|-----------|
| Dependency updates | Monthly (Dependabot PRs) |
| Content sync | Automatic on every push affecting docs/reports |
| Lighthouse audit | Each release tag |
| v1.0 science | Frozen — no regen unless explicitly approved |

---

## 13. Rollback procedure

| Scenario | Action |
|----------|--------|
| Bad deploy on Vercel | Redeploy previous deployment in Vercel dashboard (instant) |
| Bad deploy on GitHub Pages | Re-run workflow on previous commit SHA |
| Content error | Fix source MD/JSON in repo; push triggers rebuild |
| CI false fail | `workflow_dispatch` manual trigger after fix |

---

## 14. Version 3.0 deployment extensions (future)

v3 features add **optional serverless** endpoints without changing static core:

| Feature | Deploy impact |
|---------|---------------|
| RAG chat API | Vercel serverless function `/api/chat`; env var for free LLM API |
| Live earthquakes | Edge function proxy to USGS FDSN (rate-limited) |
| Semantic search | Pre-built index in static JSON → upgrade to free vector DB later |

**v2 preparation:** Keep `website/` deploy static-only; add `website/app/api/` in v3 as additive routes. GitHub Pages users would migrate to Vercel for v3 API features.

---

## 15. Pre-deployment checklist

Before first production deploy (Phase 8):

- [ ] All routes return 200 locally and in preview
- [ ] `validate-content.ts` passes
- [ ] 24 figures present or graceful fallback documented
- [ ] PDFs accessible (bundled or linked)
- [ ] GitHub SHA and build date in footer
- [ ] `sitemap.xml` and `robots.txt` generated
- [ ] OG tags verified with social debugger
- [ ] Lighthouse thresholds met
- [ ] No v1.0 source files modified
- [ ] `website/README.md` complete
- [ ] Custom domain DNS configured (if applicable)

---

## 16. Document control

| Field | Value |
|-------|-------|
| **Version** | 2.0.0-plan |
| **Date** | 2026-08-01 |
| **Status** | Awaiting approval before implementation |
| **Related** | [V2_ARCHITECTURE.md](V2_ARCHITECTURE.md) · [V2_UI_PLAN.md](V2_UI_PLAN.md) · [V2_ROADMAP.md](V2_ROADMAP.md) |
