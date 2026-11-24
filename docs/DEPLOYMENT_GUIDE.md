# Deployment guide

1. Extract ZIP and enter the folder containing package.json.
2. Install Node.js 22 and run `npm install`. This creates the absent lockfile. Run `npm run typecheck`, `npm run build`, `npm run preview` and inspect the result. Python 3 is needed for `npm test`.
3. Commit the project and generated lockfile to GitHub. Do not commit node_modules or dist. Review the included reference workbook and repository visibility before publishing.
4. Import the repository in Vercel; select Vite, root directory matching package.json, install `npm install`, build `npm run build`, output `dist`. No environment variables required.
5. After committing the lockfile, change `installCommand` in vercel.json to `npm ci` for reproducible builds. Test navigation, charts, both themes, filtering, source links and mobile layout on the deployment preview before promoting it.

The supplied ZIP is a source distribution, not a prebuilt or independently deployment-tested application. Build confirmation depends on the actual dependency installation.
