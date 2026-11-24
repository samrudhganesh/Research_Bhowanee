# Data dictionary

The following fields are the exact workbook headers. Units are encoded in header names. Null means unavailable; a text value is retained as recorded. `_excelRow` is the row coordinate. Types below are observed in non-null values in this snapshot, not future schema guarantees.

Raw cell objects have `address`, `column`, `value`, `cachedValue`, and `isFormula`.

## crops (11 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Crop | str | 11 |
| Agronomic name | str | 11 |
| Category | str | 11 |
| Major Karnataka producing districts (indicative) | str | 11 |
| Agro-climatic zones | str | 11 |
| Season | str | 11 |
| Sowing window | str | 11 |
| Harvest window | str | 11 |
| Duration (days) | str | 11 |
| Seed rate (kg/acre, indicative) | str | 11 |
| Major varieties / hybrids (indicative) | str | 11 |
| Soil requirements | str | 11 |
| Rainfall requirement | str | 11 |
| Irrigation requirement | str | 11 |
| Fertilizer recommendation (indicative; recommendation, not expenditure) | str | 11 |
| Reference yield (quintal/acre) | float | 6 |
| Yield basis (year, scope) | str | 11 |
| Karnataka production 2023-24 (million tonnes) | float | 2 |
| Karnataka share of India production 2023-24 (%) | float | 2 |
| Major pests & diseases | str | 11 |
| Source IDs | str | 11 |
| Quality | str | 11 |
| _excelRow | int | 11 |

## costRecords (40 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Record ID | str | 40 |
| Crop | str | 40 |
| Data scope (do not mix) | str | 40 |
| District / geography | str | 40 |
| Season | str | 29 |
| Data year | str | 40 |
| Farming system | str | 29 |
| Cost concept / unit in source | str | 40 |
| Source ID | str | 29 |
| Source quality | str | 29 |
| Basis | str | 40 |
| A2 paid-out cost (₹/ha, source unit) | int | 5 |
| A2+FL cost (₹/ha, source unit) | int | 5 |
| Gross returns over A2 (₹/ha) | int | 6 |
| Gross returns over A2+FL (₹/ha) | int | 6 |
| Gross value of output (₹/ha) | int | 5 |
| Imputed family labour (₹/ha) [derived] | int | 6 |
| A2 paid-out (₹/acre) | float | 5 |
| A2+FL (₹/acre) | float | 5 |
| Imputed family labour (₹/acre) | float | 6 |
| A2 (₹/quintal, source unit) | int | 9 |
| A2+FL (₹/quintal, source unit) | int | 17 |
| C2 (₹/quintal, source unit) | int | 16 |
| Yield (quintal/ha, source unit) | float | 11 |
| Yield (quintal/acre) | float | 11 |
| Implied A2 (₹/acre) = ₹/qtl × q/acre | float | 9 |
| Implied A2+FL (₹/acre) | float | 9 |
| Implied C2 (₹/acre) | float | 9 |
| Land preparation (₹/acre) | not available | 0 |
| Seeds (₹/acre) | not available | 0 |
| Seed treatment (₹/acre) | not available | 0 |
| Sowing (₹/acre) | not available | 0 |
| Organic manure (₹/acre) | not available | 0 |
| Fertilizers (₹/acre) | not available | 0 |
| Weed management (₹/acre) | not available | 0 |
| Irrigation (₹/acre) | not available | 0 |
| Plant protection (₹/acre) | not available | 0 |
| Labour - hired (₹/acre) | not available | 0 |
| Labour - imputed family (₹/acre) | float | 6 |
| Machinery (₹/acre) | not available | 0 |
| Harvesting (₹/acre) | not available | 0 |
| Threshing (₹/acre) | not available | 0 |
| Post-harvest prep (₹/acre) | not available | 0 |
| Farm-gate handling (₹/acre) | not available | 0 |
| Other pre-farm-gate (₹/acre) | not available | 0 |
| TOTAL paid-out cost (₹/acre) [A2: reported, else implied] | float | 14 |
| TOTAL incl. family labour (₹/acre) [A2+FL: reported, else implied] | float | 14 |
| Cost per quintal (₹/qtl, A2+FL basis) | int | 17 |
| % of total: Land preparation | not available | 0 |
| % of total: Seeds | not available | 0 |
| % of total: Seed treatment | not available | 0 |
| % of total: Sowing | not available | 0 |
| % of total: Organic manure | not available | 0 |
| % of total: Fertilizers | not available | 0 |
| % of total: Weed management | not available | 0 |
| % of total: Irrigation | not available | 0 |
| % of total: Plant protection | not available | 0 |
| % of total: Labour - hired | not available | 0 |
| % of total: Labour - imputed family | float | 5 |
| % of total: Machinery | not available | 0 |
| % of total: Harvesting | not available | 0 |
| % of total: Threshing | not available | 0 |
| % of total: Post-harvest prep | not available | 0 |
| % of total: Farm-gate handling | not available | 0 |
| % of total: Other pre-farm-gate | not available | 0 |
| Limitations / notes | str | 40 |
| _excelRow | int | 40 |

## zones (10 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| No. | int | 10 |
| Agro-climatic zone | str | 10 |
| Districts (taluk-wise split; see source) | str | 10 |
| Typical soils (analyst) | str | 10 |
| Rainfall min (mm) | int | 5 |
| Rainfall max (mm) | int | 5 |
| Gross cropped area ('000 ha) | int | 5 |
| Irrigated area (% of GCA) | int | 5 |
| Source ID | str | 10 |
| Quality | str | 10 |
| Main agricultural constraints (analyst) | str | 10 |
| _excelRow | int | 10 |

## cropPresence (11 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Crop | str | 11 |
| NETZ | str | 5 |
| NEDZ | str | 7 |
| NDZ | str | 10 |
| CDZ | str | 6 |
| EDZ | str | 4 |
| SDZ | str | 5 |
| STZ | str | 3 |
| NTZ | str | 7 |
| Hilly | str | 1 |
| Coastal | str | 1 |
| _excelRow | int | 11 |

## zoneCropRecords (49 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Zone | str | 49 |
| Representative districts | str | 49 |
| Crop | str | 49 |
| Soil type | str | 49 |
| Rainfall range (mm) | str | 49 |
| Water availability / irrigated share of GCA | str | 49 |
| Typical system | str | 49 |
| Sowing window | str | 49 |
| Harvest window | str | 49 |
| Average yield (q/acre) | not available | 0 |
| Cost of cultivation (₹/acre) | not available | 0 |
| Major input-cost drivers | str | 49 |
| Main constraints | str | 49 |
| _excelRow | int | 49 |

## vulnerabilityMatrix (11 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Crop | str | 11 |
| Drought | str | 11 |
| Delayed monsoon | str | 11 |
| Monsoon failure | str | 11 |
| Excess rainfall | str | 11 |
| Flooding / waterlogging | str | 11 |
| Heat stress | str | 11 |
| Unseasonal rainfall | str | 11 |
| Hailstorm | str | 11 |
| Pest & disease outbreak | str | 11 |
| Overall risk score (1-3) | float | 11 |
| Drought score (1-3) | int | 11 |
| Flood / waterlogging score (1-3) | int | 11 |
| _excelRow | int | 11 |

## cropHazardRecords (99 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Crop | str | 99 |
| Hazard | str | 99 |
| Vulnerability rating (analyst) | str | 99 |
| Principal Karnataka zones | str | 99 |
| Crop stage affected | str | 99 |
| Yield loss % (measured) | not available | 0 |
| Additional expenditure ₹/acre | not available | 0 |
| Re-sowing / rescue irrigation ₹/acre | not available | 0 |
| Drainage & mitigation ₹/acre | not available | 0 |
| Pest & disease consequence | str | 99 |
| Harvest & quality loss (qualitative) | str | 99 |
| Change in cost per quintal | not available | 0 |
| Crop insurance & government relief options | str | 99 |
| Evidence class | str | 99 |
| _excelRow | int | 99 |

## droughtArea2026 (11 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Crop | str | 11 |
| Reported affected area (lakh ha) | float | 5 |
| Source ID | str | 5 |
| Remark | str | 11 |
| _excelRow | int | 11 |

## rainfedIrrigated (11 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Crop | str | 11 |
| Typical Karnataka system | str | 11 |
| Rainfed cost (₹/acre) | not available | 0 |
| Irrigated cost (₹/acre) | not available | 0 |
| Cost difference (₹/acre) | not available | 0 |
| Seed + fertilizer difference (₹/acre) | not available | 0 |
| Irrigation expenditure (₹/acre) | not available | 0 |
| Labour difference (₹/acre) | not available | 0 |
| Rainfed yield (q/acre) | not available | 0 |
| Irrigated yield (q/acre) | not available | 0 |
| Yield difference (q/acre) | not available | 0 |
| Cost per quintal - rainfed (₹) | not available | 0 |
| Cost per quintal - irrigated (₹) | not available | 0 |
| Water dependency (analyst) | str | 11 |
| Economic implications (qualitative) | str | 11 |
| Data status | str | 11 |
| _excelRow | int | 11 |

## kapcMspGaps (3 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Item | str | 3 |
| Geography | str | 3 |
| Metric | str | 3 |
| Value | str | 3 |
| Year | str | 3 |
| Evidence class | str | 3 |
| Source ID | str | 3 |
| _excelRow | int | 3 |

## karnatakaPooledCostShares (7 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Component | str | 7 |
| Share (%) | int | 7 |
| Share (fraction) | float | 7 |
| Source ID | str | 7 |
| Quality | str | 7 |
| _excelRow | int | 7 |

## costCompositionByCrop (11 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Crop | str | 11 |
| Seeds | not available | 0 |
| Land preparation | not available | 0 |
| Fertilizers | not available | 0 |
| Irrigation | not available | 0 |
| Labour (hired + family) | not available | 0 |
| Plant protection | not available | 0 |
| Machinery | not available | 0 |
| Harvesting | not available | 0 |
| Post-harvest prep | not available | 0 |
| _excelRow | int | 11 |

## sources (18 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| Source ID | str | 18 |
| Institution / publisher | str | 18 |
| Document title | str | 18 |
| Publication year | str | 18 |
| Data year | str | 18 |
| Crop | str | 18 |
| District / region | str | 18 |
| Page / table | str | 18 |
| Information extracted | str | 18 |
| Direct URL | str | 17 |
| Source quality | str | 18 |
| Limitations | str | 18 |
| _excelRow | int | 18 |

## notes (11 rows)

| Field | Observed value types | Non-null records |
|---|---|---:|
| topic | str | 11 |
| detail | str | 10 |
| _excelRow | int | 11 |
