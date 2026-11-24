# Data integrity audit

## Reconciliation

The supplied workbook and original JSON agree on all 8,183 retained cell slots (4,852 populated, 2,085 formula expressions), 5,903 fields across 303 structured rows, and 71 independently recalculated numerical results. Eight original empty strings were normalized to null by the existing extractor. All source records and crop–zone/crop–hazard relationships passed the implemented checks. The original JSON's `sheets`, `tables` and `charts` objects are unchanged. Only metadata was augmented. See reconciliation.json for machine-readable output.

## Implementation reconciliation matrix

| ID | Source / range or records | Original issue | Action / status |
|---|---|---|---|
| 01 | Cost of Cultivation row 10, C006 | Ragi returns/FL absent from main view | Dedicated card and details added |
| 02 | Executive Dashboard I10:I20; projected cost records | Implied acre cost not plotted | Dynamic same-record chart added |
| 03 | Cost of Cultivation C016, C028–C029 | Toor yield comparison underused | Dedicated yield view and complete yield table added |
| 04 | Cost of Cultivation A:BN, C001–C040 | Limited cost explorer columns | Full field selection, filters, records, CSV, paging added |
| 05 | Cost of Cultivation C027 | KAPC values presented as CACP | Method-specific labels added in cards/table; original field names retained in export |
| 06 | Crop Master rows 5–15 | Seed rate, districts, zones omitted | Added to selected crop profile |
| 07 | Regional Comparison rows 6–15, 36 onward | GCA, regional detail and cost drivers underused | Added region table, GCA/rainfall chart and cost drivers |
| 08 | Weather & Risk rows 21–26 | Historic cases and area breakdown missing | Added derived breakdown from remark and historical table |
| 09 | Weather & Risk rows 6–16, 47–145 | Overall/drought/flood comparison and some qualitative fields omitted | Added comparison and remaining hazard fields |
| 10 | Crop Master production fields, Weather & Risk E21:E24 | Hardcoded primary KPI values | Primary values now selected from data; fixed explanatory text remains tied to current workbook edition |
| 11 | Cost of Cultivation headers AC:AS | 16 vs 17 cost-component heads | Count derived from schema |
| 12 | Cost of Cultivation data year | Substring year matching | Exact matching |
| 13 | Rainfed vs Irrigated rows 5–15 | All crop information on selected crop page | Selected water record only; dedicated all-crop view added |
| 14 | Source Register rows 5 onward | Source references not linked in detailed view | Source-ID links for record details and cost explorer |
| 15 | All sheets | Snapshot described as connected | Accurate static snapshot wording and checksum added |
| 16 | All sheets | Structural verifier not value-level | Independent OOXML reconciliation added; parser fixed |
| 17 | Cost Composition rows 21–27 | Reported shares total 101% | Source percentages unchanged; donut normalization disclosed |
| 18 | Deployment | No npm lockfile | Registry unavailable; unresolved; normal npm install configured |

## Methodological findings retained

For C001–C005, gross-return columns are separately state-weighted, so family labour is derived from cost difference, not gross-return difference. For C006, the returns difference is the valid available basis, as explicitly described in the workbook. No values were modified. National projections remain separate from Karnataka observations. Missing observations remain null. No external publications were independently validated.
