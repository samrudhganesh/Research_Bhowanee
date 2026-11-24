# v2.0.0 — Workbook intelligence enhancement

**Preserved:** original Excel file; all extracted sheets, tables, formulas, cached values, and chart metadata; six original analytical areas and their primary charts, risk matrix, presence matrix and source register.

**Added:** per-acre benchmark calculated from same-record cost and yield; C006 Ragi returns and family-labour detail; dedicated production/yield and rainfed/irrigated views; regional GCA/rainfall detail; weather history and affected-area breakdown; qualitative risk chart; crop-specific economics/hazards; all-field cost explorer with independent filters, column controls, paging, sorting, expanded details and CSV export; workbook CSV export; evidence availability; source links; SHA-256 provenance.

**Corrected:** exact period matching; KAPC terminology on summary cards and detailed explorer; benchmark coverage labels; dynamic production, drought and record-count indicators; 17 component-head count; tooltip metadata for benchmark records; static snapshot wording; selected-crop water information; original syntax verifier regex that did not reliably visit TS files.

**Refined:** coordinated light/dark palettes and chart tokens, persistence and system preference on first visit, accessible control labels, responsive panels, legibility and focus styling, null-preserving chart selection, stacked family labour comparison, error boundary, hash navigation.

**Validation:** independent OOXML reconciliation and executable analytics tests added. Package installation/build/browser verification and lockfile generation remain blocked by unavailable npm access. Existing stack preserved; no external agricultural data added.
