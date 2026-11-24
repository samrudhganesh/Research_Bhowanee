# Karnataka Crop Cost & Risk Intelligence · v2.0

A preservation-first enhancement of the supplied React / TypeScript / Vite application. Eight analytical views cover executive benchmarks, economics, production and yield, rainfed and irrigated systems, regional intelligence, weather risk, crop profiles, and sources/workbook exploration. All data comes from the supplied workbook; no new agricultural observations have been invented.

## Start locally

Use Node.js 22 LTS (or a compatible supported Node release). From this directory:

```sh
npm install
npm run dev
```

Open the local URL printed by Vite. To build and preview:

```sh
npm run build
npm run preview
```

The supplied dependencies are version-pinned directly in package.json. A lockfile could not be produced in the packaging environment because the npm registry and cache were unavailable. `npm install` creates it; commit the resulting package-lock.json to GitHub and then use `npm ci` for reproducible installs. No backend or environment variables are needed.

## Deploy on Vercel

Extract the ZIP. Open the extracted project folder (the one containing package.json). Upload its contents to a GitHub repository, then import that repository in Vercel. Use the Vite framework preset, `npm install` (or `npm ci` once the lockfile is committed), `npm run build`, and output directory `dist`. The included vercel.json configures the initial install and SPA fallback. Hash-based navigation preserves internal views on refresh. The reference workbook is not placed in public assets, but it will be visible to anyone who can access the repository. Use a private repo if necessary.

## Data and verification

The unchanged original XLSX is in `reference-data/`. `src/data/workbookData.json` contains all original extracted tables, worksheets, cached values, formulas, and chart metadata, plus added provenance. `src/data/analytics.ts` provides analytical selectors and calculations; `src/components/Intelligence.tsx` adds dedicated analytical views and record exploration. `src/styles.css` provides shared theme tokens. `src/components/Charts.tsx` centralizes charts.

Install Python 3 for the verification utilities. The independent reconciliation uses the standard library. The original extraction utility requires openpyxl:

```sh
python -m pip install openpyxl
python scripts/extract_workbook.py
python scripts/reconcile_workbook.py
npm test
npm run typecheck
```

On Windows, run the individual Python commands using `python` or `py -3` if `python3` is not available, and `npm run test:analytics`. Recalculate and save changed workbooks in Excel before extraction if formula inputs change; the extractor reads cached results, not a live formula engine. The current schema and expected row counts are tied to this workbook edition; review and adjust mappings and verification expectations before ingesting a structurally different workbook. See `docs/` for audit results, field definitions, limitations and deployment guidance.

## Verification status

Independent workbook reconciliation, analytics tests, structural checks, TypeScript/JSX parsing and static transpilation passed. Dependency installation, full type checking, production build, browser-rendered testing and live deployment are not certified: the packaging environment could not reach npm and did not have the required frontend dependencies. Do not treat static checks as proof of runtime or visual perfection. See `docs/VALIDATION_REPORT.md`.
