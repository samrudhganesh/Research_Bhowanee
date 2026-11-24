# Validation results

| Check | Result |
|---|---|
| Independent OOXML reconciliation | PASS — 8,183 slots, 2,085 formulas, 5,903 semantic fields, 303 rows, 71 selected calculations; 0 mismatches |
| Original JSON tables, sheets and charts equality | PASS — all three equal original application snapshot |
| Original workbook SHA-256 | PASS — byte-for-byte copy |
| Structural verification | PASS — 17 checks, including corrected parser visiting all 7 TS/TSX source modules |
| Executed Node analytical unit assertions | PASS — 9 period/concept counts, exact filtering, null handling, derived cost, drought breakdown, schema counts, coverage |
| Static TypeScript transpilation / CSS parsing | PASS — seven modules, CSS parsed; not semantic type checking |
| npm registry ping | BLOCKED — EAI_AGAIN DNS lookup |
| Offline lockfile generation | BLOCKED — ENOTCACHED for @types/react |
| npm run build | BLOCKED — Vite unavailable because dependencies not installed |
| npm run typecheck | BLOCKED — unresolved React/Lucide/Recharts modules and dependent diagnostics |
| Browser screenshots, viewport/interaction/accessibility tests | NOT RUN — no runnable dependency installation |
| Vercel deployment | NOT RUN — configuration prepared, actual deploy not performed |

Run `npm install`, `npm run typecheck`, `npm test`, `npm run build` on a connected machine. Inspect light and dark modes and mobile navigation before treating the project as release-certified.
