#!/usr/bin/env python3
"""Independent OOXML value-level reconciliation; standard library only.
No dependency on extraction implementation, no source workbook writes.
"""
import hashlib, json, math, re, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from posixpath import join, normpath
ROOT=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'reference-data/Karnataka_Crop_Cost_Risk_Analysis.xlsx'
obj=json.loads((ROOT/'src/data/workbookData.json').read_text(encoding='utf-8'))
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
rel='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
def tag(name):return '{'+ns['m']+'}'+name
errors=[]; counts={'cell_slots':0,'populated_cells':0,'formulas':0,'structured_fields':0,'structured_rows':0,'calculations':0,'blank_normalizations':0}
def same(a,b):
    if a=='' and b is None: return True
    if isinstance(a,bool) or isinstance(b,bool):return type(a)==type(b) and a==b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-10)
    return a==b
def check(a,b,where):
    if not same(a,b):errors.append({'location':where,'expected':a,'actual':b})
def numeric(v):return isinstance(v,(int,float)) and not isinstance(v,bool)
with zipfile.ZipFile(source) as z:
    workbook=ET.fromstring(z.read('xl/workbook.xml'));rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'));targets={x.get('Id'):x.get('Target') for x in rels}
    strings=[]
    if 'xl/sharedStrings.xml' in z.namelist():strings=[''.join(t.text or '' for t in x.iter(tag('t'))) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
    sheets={}
    for sh in workbook.find('m:sheets',ns):
        name=sh.get('name');target=targets[sh.get('{'+rel+'}id')];path=target.lstrip('/') if target.startswith('/') else normpath(join('xl',target)); cells={}
        for c in ET.fromstring(z.read(path)).iter(tag('c')):
            addr=c.get('r');f=c.find(tag('f'));v=c.find(tag('v'));typ=c.get('t','n');text=v.text if v is not None else None
            if typ=='inlineStr':val=''.join(t.text or '' for t in c.iter(tag('t')))
            elif text is None:val=None
            elif typ=='s':val=strings[int(text)]
            elif typ=='b':val=text=='1'
            elif typ in ('str','e','d'):val=text
            else:
                try:val=float(text);val=int(val) if val.is_integer() else val
                except ValueError:val=text
            formula='='+f.text if f is not None and f.text else None
            cells[addr]=(formula if formula is not None else val,val,formula is not None)
        sheets[name]=cells
check(sorted(sheets),sorted(obj['sheets']),'worksheet names')
for name,cells in sheets.items():
    stored={c['address']:c for row in obj['sheets'][name]['rows'] for c in row['cells']}
    for addr,c in stored.items():
        raw,cached,formula=cells.get(addr,(None,None,False));counts['cell_slots']+=1
        if raw is not None and raw!='':counts['populated_cells']+=1
        if formula:counts['formulas']+=1
        if raw=='' and c['value'] is None:counts['blank_normalizations']+=1
        check(raw,c['value'],f'{name}!{addr} raw');check(cached,c['cachedValue'],f'{name}!{addr} cache');check(formula,c['isFormula'],f'{name}!{addr} formula flag')
    for addr,(raw,cache,formula) in cells.items():
        if raw not in (None,'') and addr not in stored:errors.append({'location':f'{name}!{addr}','expected':raw,'actual':'not retained'})
# Semantic rows: header identity and direct original cached value, independently mapped by worksheet headers.
headers={'crops':('Crop Master',4),'costRecords':('Cost of Cultivation',4),'zones':('Regional Comparison',5),'cropPresence':('Regional Comparison',20),'zoneCropRecords':('Regional Comparison',35),'vulnerabilityMatrix':('Weather & Risk',5),'cropHazardRecords':('Weather & Risk',46),'droughtArea2026':('Weather & Risk',30),'rainfedIrrigated':('Rainfed vs Irrigated',4),'kapcMspGaps':('Rainfed vs Irrigated',19),'karnatakaPooledCostShares':('Cost Composition',20),'costCompositionByCrop':('Cost Composition',33),'sources':('Source Register',4)}
for table,(name,hr) in headers.items():
    cells=sheets[name];mapping={value:re.match(r'[A-Z]+',addr).group() for addr,(value,_,_) in cells.items() if int(re.search(r'\d+',addr).group())==hr and value is not None and value!=''}
    for row in obj['tables'][table]:
        counts['structured_rows']+=1
        check(sorted(mapping),sorted(k for k in row if k!='_excelRow'),f'{table} row {row["_excelRow"]} fields')
        for k,col in mapping.items():
            addr=f'{col}{row["_excelRow"]}';counts['structured_fields']+=1;check(cells.get(addr,(None,None,False))[1],row.get(k),f'{table} {name}!{addr} {k}')
for row in obj['tables']['notes']:
    counts['structured_rows']+=1
    for k,col in [('topic','A'),('detail','B')]:
        counts['structured_fields']+=1;addr=f'{col}{row["_excelRow"]}';check(sheets['Notes & Data Gaps'].get(addr,(None,None,False))[1],row[k],f'notes {addr}')
# Recalculate supported cost quantities only when all source operands exist.
for r in obj['tables']['costRecords']:
    def calc(key,expected):
        counts['calculations']+=1;check(expected,r.get(key),f'{r["Record ID"]} {key}')
    for orig,dest in [('A2 paid-out cost (₹/ha, source unit)','A2 paid-out (₹/acre)'),('A2+FL cost (₹/ha, source unit)','A2+FL (₹/acre)'),('Imputed family labour (₹/ha) [derived]','Imputed family labour (₹/acre)'),('Yield (quintal/ha, source unit)','Yield (quintal/acre)')]:
        if numeric(r[orig]):calc(dest,r[orig]/2.47105)
    for first,second in [('A2+FL cost (₹/ha, source unit)','A2 paid-out cost (₹/ha, source unit)'),('Gross returns over A2 (₹/ha)','Gross returns over A2+FL (₹/ha)')]:
        if numeric(r[first]) and numeric(r[second]) and (first.startswith('A2+FL') or not (numeric(r['A2 paid-out cost (₹/ha, source unit)']) and numeric(r['A2+FL cost (₹/ha, source unit)']))):calc('Imputed family labour (₹/ha) [derived]',r[first]-r[second])
    for c,key in [('A2','Implied A2 (₹/acre) = ₹/qtl × q/acre'),('A2+FL','Implied A2+FL (₹/acre)'),('C2','Implied C2 (₹/acre)')]:
        a=r[f'{c} (₹/quintal, source unit)'];b=r['Yield (quintal/acre)'];
        if numeric(a) and numeric(b):calc(key,a*b)
ratings={'Low':1,'Medium':2,'High':3}; hazard_names=['Drought','Delayed monsoon','Monsoon failure','Excess rainfall','Flooding / waterlogging','Heat stress','Unseasonal rainfall','Hailstorm','Pest & disease outbreak']; matrix={r['Crop']:r for r in obj['tables']['vulnerabilityMatrix']}
for r in matrix.values():
    counts['calculations']+=1;check(sum(ratings[r[k]] for k in hazard_names)/len(hazard_names),r['Overall risk score (1-3)'],f'{r["Crop"]} risk average')
for r in obj['tables']['cropHazardRecords']:
    check(matrix[r['Crop']][r['Hazard']],r['Vulnerability rating (analyst)'],f'{r["Crop"]} {r["Hazard"]}')
zone_codes=dict(zip(['NETZ','NEDZ','NDZ','CDZ','EDZ','SDZ','STZ','NTZ','Hilly','Coastal'],[r['Agro-climatic zone'] for r in obj['tables']['zones']]))
expected={(r['Crop'],zone_codes[k]) for r in obj['tables']['cropPresence'] for k in zone_codes if r[k] in ('P','p')};actual={(r['Crop'],r['Zone']) for r in obj['tables']['zoneCropRecords']};check(sorted(expected),sorted(actual),'zone presence relationships')
ids={r['Source ID'] for r in obj['tables']['sources']}
for table,rows in obj['tables'].items():
    for r in rows:
        for k in ['Source ID','Source IDs']:
            for token in re.findall(r'S\d{2}',str(r.get(k) or '')):
                if token not in ids:errors.append({'location':table,'expected':'registered source','actual':token})
report={'status':'PASS' if not errors else 'FAIL','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'counts':counts,'mismatches':errors,'scope':'OOXML cells/formulas/caches, semantic fields, selected independent calculations and relationships; not full formula execution or external source verification'}
(ROOT/'docs').mkdir(exist_ok=True);(ROOT/'docs/reconciliation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
