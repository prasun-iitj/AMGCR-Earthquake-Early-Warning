# AMGCR Earthquake Research — Website

Version **2.0.0** interactive research platform (Phases 1–12 complete · production audit PASS).

This application is **separate** from the v1.0 scientific codebase. It lives entirely under `website/` and does not modify analysis scripts, reports, or documentation in the parent repository.

## Release documentation (v2.0)

- [docs/V2_RELEASE_NOTES.md](../docs/V2_RELEASE_NOTES.md)
- [docs/V2_DEPLOYMENT_GUIDE.md](../docs/V2_DEPLOYMENT_GUIDE.md)
- [docs/V2_TEST_REPORT.md](../docs/V2_TEST_REPORT.md)
- [docs/V2_KNOWN_LIMITATIONS.md](../docs/V2_KNOWN_LIMITATIONS.md)
- [docs/V2_PUBLIC_LAUNCH_CHECKLIST.md](../docs/V2_PUBLIC_LAUNCH_CHECKLIST.md)
- [CHANGELOG.md](CHANGELOG.md) — website changelog

## Stack

- Next.js (App Router)
- TypeScript
- Tailwind CSS v4
- Framer Motion
- ESLint

## Local development

From the repository root:

```powershell
cd website
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Build

```powershell
cd website
npm run build
npm run start
```

## Lint

```powershell
cd website
npm run lint
```

## Deployment

Compatible with **Vercel Hobby** (recommended). Set project root directory to `website/` in Vercel project settings.

Copy `.env.example` to `.env.local` and set `NEXT_PUBLIC_SITE_URL` before production deploy.

See [docs/V2_DEPLOYMENT_GUIDE.md](../docs/V2_DEPLOYMENT_GUIDE.md) and [docs/V2_PUBLIC_LAUNCH_CHECKLIST.md](../docs/V2_PUBLIC_LAUNCH_CHECKLIST.md).

Legacy planning docs:

- `docs/V2_ARCHITECTURE.md`
- `docs/V2_UI_PLAN.md`
- `docs/V2_ROADMAP.md`
- `docs/V2_DEPLOYMENT_PLAN.md`

## ML Evaluation page (`/ml-evaluation`)

Server-rendered at build time from saved results in `../reports/ml/` and `../reports/features/` (no model is run in the browser). `npm run build` first runs `scripts/sync-results-assets.mjs`, which copies `reports/figures/final/*.png` to `public/final-figures/` and selected reports/JSON/CSV to `public/ml-downloads/` (both git-ignored, regenerated on every build). Charts are plain HTML/CSS in `components/ml/MlCharts.tsx`; loader: `lib/ml/loader.ts`. Final figures are produced by `scripts/reporting/make_final_figures.py` in the repository root.
