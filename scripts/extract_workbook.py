import openpyxl, json, os, re, math, sys, hashlib
from pathlib import Path
from datetime import datetime, date, timezone
from openpyxl.utils import get_column_letter, range_boundaries
ROOT=str(Path(__file__).resolve().parents[1])
src=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'reference-data','Karnataka_Crop_Cost_Risk_Analysis.xlsx'))
out=ROOT
if not os.path.exists(src): raise FileNotFoundError(f'Workbook not found: {src}. Pass the .xlsx path as the first argument.')
wf=openpyxl.load_workbook(src,data_only=False)
wv=openpyxl.load_workbook(src,data_only=True)
def clean(v):
    if v is None: return None
    if isinstance(v,(datetime,date)): return v.isoformat()
    if isinstance(v,float) and (math.isnan(v) or math.isinf(v)): return None
    if isinstance(v,(str,int,float,bool)): return v
    return str(v)
def chart_title(ch):
    try:
        t=ch.title
        if t and t.tx and t.tx.rich:
            return ''.join(r.t for p in t.tx.rich.p for r in p.r)
        if t and t.tx and t.tx.strRef and t.tx.strRef.f: return t.tx.strRef.f
    except: pass
    return None
def chart_formula_refs(ch):
    refs=[]
    def walk(x):
        if x is None: return
        if isinstance(x,str):
            if '!' in x or ':' in x: refs.append(x)
            return
        if isinstance(x,(list,tuple)):
            for y in x: walk(y)
            return
        if hasattr(x,'__dict__'):
            for k,v in vars(x).items():
                if k in ('parent','_parent'): continue
                walk(v)
    # inspect chart series references explicitly
    for ser in getattr(ch,'ser',[]) or []:
        for attr in ('tx','val','cat','xVal','yVal','zVal'):
            obj=getattr(ser,attr,None)
            if obj:
                for sub in ('strRef','numRef','multiLvlStrRef'):
                    q=getattr(obj,sub,None)
                    if q and getattr(q,'f',None): refs.append(q.f)
                if getattr(obj,'v',None) is not None: refs.append(str(obj.v))
    return sorted(set(refs))
sheets={}
for s in wf:
    sv=wv[s.title]
    rows=[]
    for ri in range(1,s.max_row+1):
        cells=[]
        row_has_data=False
        for ci in range(1,s.max_column+1):
            c=s.cell(ri,ci); cv=sv.cell(ri,ci).value
            if c.value is not None or cv is not None: row_has_data=True
            val=clean(c.value)
            cells.append({'address':c.coordinate,'column':get_column_letter(ci),'value':val,'cachedValue':clean(cv),'isFormula':isinstance(c.value,str) and c.value.startswith('=')})
        if row_has_data: rows.append({'row':ri,'cells':cells})
    charts=[]
    for i,ch in enumerate(getattr(s,'_charts',[]),1):
        charts.append({'id':f'{s.title} chart {i}','title':chart_title(ch),'type':type(ch).__name__,'anchor':str(getattr(ch,'anchor',None)._from if hasattr(getattr(ch,'anchor',None),'_from') else getattr(ch,'anchor',None)),'seriesRanges':chart_formula_refs(ch)})
    validations=[]
    try:
        for dv in s.data_validations.dataValidation:
            validations.append({'type':dv.type,'formula1':dv.formula1,'sqref':str(dv.sqref)})
    except: pass
    # row-level values as column-addressed map; blanks preserved via dimensions in raw sheet shape
    sheets[s.title]={'maxRow':s.max_row,'maxColumn':s.max_column,'nonEmptyCells':sum(1 for r in rows for c in r['cells'] if c['value'] is not None or c['cachedValue'] is not None),'cellSlots':sum(len(r['cells']) for r in rows),'rows':rows,'charts':charts,'dataValidations':validations,'mergedRanges':[str(x) for x in s.merged_cells.ranges]}
# semantic table extraction: rows keyed by headers, with blank values explicitly null

def rowmap(sheet, header_row, start_row=None):
    s=wf[sheet]; headers=[clean(s.cell(header_row,c).value) for c in range(1,s.max_column+1)]
    out=[]
    for r in range(start_row or header_row+1,s.max_row+1):
        vals=[]
        for c in range(1,s.max_column+1):
            raw=wf[sheet].cell(r,c).value
            cached=wv[sheet].cell(r,c).value
            vals.append(clean(cached if isinstance(raw,str) and raw.startswith('=') else raw))
        if not any(v is not None for v in vals): continue
        # skip repeated section titles unless has id or first column meaningful
        d={str(h) if h is not None else f'column_{i+1}':vals[i] for i,h in enumerate(headers) if h is not None}
        d['_excelRow']=r
        out.append(d)
    return out
crops=[x for x in rowmap('Crop Master',4,5) if isinstance(x.get('Crop'),str) and x.get('Crop') not in ('Crop',)]
crops=[x for x in crops if x.get('_excelRow',0) <= 15 and x.get('Crop')]
costs=[x for x in rowmap('Cost of Cultivation',4,5) if isinstance(x.get('Record ID'),str) and re.fullmatch(r'C\d{3}',x.get('Record ID'))]
zones=[x for x in rowmap('Regional Comparison',5,6) if isinstance(x.get('No.'),(int,float)) and 1 <= x.get('No.') <= 10]
# Exact table ranges from inspected worksheet headings
rs=wf['Regional Comparison']; presence=[x for x in rowmap('Regional Comparison',20,21) if 21 <= x.get('_excelRow',0) <= 31]
zone_crop=rowmap('Regional Comparison',35,36)
zone_crop=[x for x in zone_crop if x.get('Zone') is not None and x.get('Crop') is not None]
ws=wf['Weather & Risk']
# Exact matrix and detail table ranges from worksheet section headings
vuln=rowmap('Weather & Risk',5,6)[:11]
hazards=rowmap('Weather & Risk',46,47)[:99]
droughtArea=rowmap('Weather & Risk',30,31)[:11]
rainfed=rowmap('Rainfed vs Irrigated',4,5)[:11]
kapcGaps=rowmap('Rainfed vs Irrigated',19,20)[:3]
compositionShares=rowmap('Cost Composition',20,21)[:7]
costCompositionByCrop=[x for x in rowmap('Cost Composition',33,34) if x.get('Crop') and x.get('_excelRow',0)<=44]
sources=rowmap('Source Register',4,5)
# drought rows, cost comp table, rainfed tables remain accessible raw, and notes key/value
notes=[]
ns=wf['Notes & Data Gaps']
for r in range(1,ns.max_row+1):
    a,b=clean(ns.cell(r,1).value),clean(ns.cell(r,2).value)
    if a is not None or b is not None: notes.append({'topic':a,'detail':b,'_excelRow':r})
# formula/cached summary
formula_count=sum(1 for s in wf for row in s.iter_rows() for c in row if isinstance(c.value,str) and c.value.startswith('='))
cached_blank=sum(1 for s in wf for row in s.iter_rows() for c in row if isinstance(c.value,str) and c.value.startswith('=') and wv[s.title][c.coordinate].value is None)
allcharts=[{'sheet':sn,**ch} for sn,sh in sheets.items() for ch in sh['charts']]
# ids extracted from records
payload={'meta':{'workbook':'Karnataka_Crop_Cost_Risk_Analysis.xlsx','extractedAt':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(Path(src).read_bytes()).hexdigest(),'datasetVersion':'2.0.0','referencePath':'reference-data/Karnataka_Crop_Cost_Risk_Analysis.xlsx','engine':'openpyxl','modes':['data_only=False','data_only=True'],'sheetCount':len(sheets),'formulaCount':formula_count,'formulaCellsWithoutCachedValue':cached_blank,'chartCount':len(allcharts),'nullPolicy':'Blank cells are null; formulas and cached values are stored separately.'},'sheets':sheets,'tables':{'crops':crops,'costRecords':costs,'zones':zones,'cropPresence':presence,'zoneCropRecords':zone_crop,'vulnerabilityMatrix':vuln,'cropHazardRecords':hazards,'droughtArea2026':droughtArea,'rainfedIrrigated':rainfed,'kapcMspGaps':kapcGaps,'karnatakaPooledCostShares':compositionShares,'costCompositionByCrop':costCompositionByCrop,'sources':sources,'notes':notes},'charts':allcharts}
os.makedirs(out+'/src/data',exist_ok=True)
with open(out+'/src/data/workbookData.json','w',encoding='utf-8') as f: json.dump(payload,f,ensure_ascii=False,indent=2,allow_nan=False)
print('EXTRACTED',len(sheets),'sheets','crops',len(crops),'costs',len(costs),'zones',len(zones),'presence',len(presence),'zoneCrop',len(zone_crop),'vulnerability',len(vuln),'hazards',len(hazards),'sources',len(sources),'charts',len(allcharts),'formulas',formula_count,'uncached',cached_blank)
for sn,sh in sheets.items(): print(sn,sh['nonEmptyCells'],len(sh['charts']))
for c in allcharts: print('CHART',c['sheet'],c['title'],c['seriesRanges'])
