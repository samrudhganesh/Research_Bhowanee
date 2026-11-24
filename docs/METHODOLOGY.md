# Methodology

The authoritative source is the included workbook, not external research. Its original scopes, units, source IDs, evidence grades and limitations are retained.

- A2: paid-out cost. A2+FL: paid-out plus imputed family labour. C2: broader cost including land rental and capital interest. KAPC excludes/includes land rent using a different methodology; not interchangeable with CACP.
- One hectare = 2.47105 acres (workbook convention). Per-acre values divide per-hectare values by 2.47105. Implied cost per acre multiplies the selected per-quintal concept by yield per acre from the same source record. No yield substitution.
- Family labour is A2+FL minus A2 when both actual costs exist. For Karnataka Ragi C006, returns over A2 minus returns over A2+FL is the workbook's alternative derivation.
- Vulnerability is an analyst scale: Low 1, Medium 2, High 3. The overall score is an average of nine ratings, not a probability. Affected area and damage bands are not measured crop-specific yield losses.
- The 101% pooled cost composition consists of reported rounded component shares. Display values are not silently normalized; donut geometry is proportional to their sum.
- Reported values and cached derived values are stored separately from formula text. The application is a static snapshot, not a recalculating Excel engine.
- Missing source values are null and are never interpreted as zero. Coverage metrics count actual finite numeric observations, not placeholder rows.
