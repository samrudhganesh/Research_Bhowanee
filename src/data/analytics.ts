import snapshot from './workbookData.json';
export type CellValue = string | number | boolean | null;
export type RecordRow = Record<string, CellValue>;
export type Concept = 'A2' | 'A2+FL' | 'C2';
export const tables = snapshot.tables as unknown as Record<string, RecordRow[]>;
export const costs = tables.costRecords;
export const crops = tables.crops;
export const zones = tables.zones;
export const sources = tables.sources;
export const finite = (value: unknown): number | null => typeof value === 'number' && Number.isFinite(value) ? value : null;
export const format = (value: unknown, digits=2): string => finite(value) === null ? 'Not available' : (value as number).toLocaleString('en-IN', {maximumFractionDigits: digits});
export const shortCrop = (value: unknown) => String(value ?? '').split('/')[0].trim();
export const perQuintal = (row: RecordRow, concept: string) => finite(row[`${concept} (₹/quintal, source unit)`]);
export const impliedAcre = (row: RecordRow, concept: string) => {
  const cost = perQuintal(row, concept), yieldAcre = finite(row['Yield (quintal/acre)']);
  return cost === null || yieldAcre === null ? null : cost * yieldAcre;
};
export const national = (row: RecordRow) => String(row['Data scope (do not mix)']).startsWith('All-India CACP');
export const benchmark = (year: string, concept: string) => costs.filter(r => national(r) && r['Data year'] === year && perQuintal(r, concept) !== null);
export const costFields = ['A2 paid-out cost (₹/ha, source unit)','A2+FL cost (₹/ha, source unit)','A2 (₹/quintal, source unit)','A2+FL (₹/quintal, source unit)','C2 (₹/quintal, source unit)'];
export const hasCost = (r: RecordRow) => costFields.some(k => finite(r[k]) !== null);
export const componentHeads = Object.keys(costs[0]).filter(k => k.startsWith('% of total: '));
export const isKAPC = (row: RecordRow) => String(row['Data scope (do not mix)']).includes('KAPC');
export function sheetCell(sheet: keyof typeof snapshot.sheets, row: number, column: string): CellValue {
  const cell = snapshot.sheets[sheet].rows.find(r => r.row === row)?.cells.find(c => c.column === column);
  return (cell?.isFormula ? cell.cachedValue : cell?.value) ?? null;
}
const eventFields = ['Event','Season','Geography','Metric','Value','Unit','Evidence class','Source ID','Remark'];
export const weatherEvents: RecordRow[] = snapshot.sheets['Weather & Risk'].rows.filter(r => r.row >= 21 && r.row <= 26).map(r => Object.fromEntries([['_excelRow',r.row], ...eventFields.map((k,i)=>[k,sheetCell('Weather & Risk',r.row,String.fromCharCode(65+i))])]) as RecordRow);
export const eventValue = (row: number) => sheetCell('Weather & Risk',row,'E');
export const droughtBreakdown = () => {
  const remark = String(sheetCell('Weather & Risk',23,'I') ?? '');
  const m = remark.match(/([\d.]+) lakh ha crops \+ ([\d.]+) lakh ha horticulture/i);
  if (!m) return [];
  return [{name:'Agricultural crops',value:Number(m[1])},{name:'Horticulture',value:Number(m[2])}];
};
export const chartRecord = (r: RecordRow) => ({name:shortCrop(r.Crop),record:r['Record ID'],source:r['Source ID'],year:r['Data year'],scope:r['Data scope (do not mix)'],basis:r.Basis});
export const coverage = () => [
  {name:'Karnataka numeric total-cost crops',n:new Set(costs.filter(r=>!national(r)&&hasCost(r)).map(r=>r.Crop)).size,d:crops.length},
  {name:'Production observations',n:crops.filter(r=>finite(r['Karnataka production 2023-24 (million tonnes)'])!==null).length,d:crops.length},
  {name:'Zone rainfall profiles',n:zones.filter(r=>finite(r['Rainfall min (mm)'])!==null&&finite(r['Rainfall max (mm)'])!==null).length,d:zones.length},
  {name:'Crop drought area observations',n:tables.droughtArea2026.filter(r=>finite(r['Reported affected area (lakh ha)'])!==null).length,d:crops.length},
  {name:'Measured hazard yield loss',n:tables.cropHazardRecords.filter(r=>finite(r['Yield loss % (measured)'])!==null).length,d:tables.cropHazardRecords.length},
  {name:'Rainfed + irrigated numeric cost pairs',n:tables.rainfedIrrigated.filter(r=>finite(r['Rainfed cost (₹/acre)'])!==null&&finite(r['Irrigated cost (₹/acre)'])!==null).length,d:crops.length},
  {name:'Zone–crop numeric cost records',n:tables.zoneCropRecords.filter(r=>finite(r['Cost of cultivation (₹/acre)'])!==null).length,d:tables.zoneCropRecords.length},
];
