# AMGCR Earthquake Research — Website

Version 2.0 interactive research platform (Phase 1 foundation).

This application is **separate** from the v1.0 scientific codebase. It lives entirely under `website/` and does not modify analysis scripts, reports, or documentation in the parent repository.

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

## Phase 2 scope

- Markdown rendering from repository sources at build time (no duplicated content)
- Documentation index at `/docs`
- Research report at `/research/report`
- Table of contents, breadcrumbs, and previous/next navigation
- Supported documents: `README.md`, `docs/PROJECT_CHARTER.md`, `docs/PROJECT_STATUS.md`, `reports/Research_Report_Final.md`

## Phase 1 scope (complete)

- Global layout, navigation, footer
- Placeholder pages: Home, Research, Downloads, About, Contact
- Theme, typography, reusable UI components
- No repository content rendering
- No backend, database, charts, maps, or API integrations

## Deployment

Compatible with **Vercel Hobby** (recommended). Set project root directory to `website/` in Vercel project settings.

See parent repo planning docs:

- `docs/V2_ARCHITECTURE.md`
- `docs/V2_UI_PLAN.md`
- `docs/V2_ROADMAP.md`
- `docs/V2_DEPLOYMENT_PLAN.md`
