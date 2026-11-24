#!/usr/bin/env python3
"""Validate the workbook extraction and static project before packaging."""
import json, re, sys, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'src' / 'data' / 'workbookData.json'
obj = json.loads(DATA.read_text(encoding='utf-8'))
t = obj['tables']
checks = {
    '10 worksheets': len(obj['sheets']) == 10,
    '11 crops': len(t['crops']) == 11,
    '40 cost records': len(t['costRecords']) == 40,
    'C001–C040 IDs': {x.get('Record ID') for x in t['costRecords']} == {f'C{i:03d}' for i in range(1,41)},
    '10 agro-climatic zones': len(t['zones']) == 10,
    '49 zone × crop rows': len(t['zoneCropRecords']) == 49,
    '99 crop × hazard rows': len(t['cropHazardRecords']) == 99,
    '18 sources': len(t['sources']) == 18,
    '11 crop composition rows': len(t['costCompositionByCrop']) == 11,
    'S01–S18 IDs': {x.get('Source ID') for x in t['sources']} == {f'S{i:02d}' for i in range(1,19)},
    '10 embedded chart records': len(obj['charts']) == 10,
    'Formula and cached-value modes recorded': obj['meta']['modes'] == ['data_only=False', 'data_only=True'],
}
raw = DATA.read_text(encoding='utf-8')
checks['Blank cells retained as null'] = all(len(row['cells']) == sh['maxColumn'] for sh in obj['sheets'].values() for row in sh['rows']) and all('value' in cell and 'cachedValue' in cell and (cell['value'] is None or isinstance(cell['value'], (str, int, float, bool))) for sh in obj['sheets'].values() for row in sh['rows'] for cell in row['cells'])
checks['No NaN tokens'] = not re.search(r'(?<![A-Za-z])NaN(?![A-Za-z])|\bInfinity\b|-Infinity', raw)
# Verify every authored relative import resolves to a project file.
imports = []
for file in (ROOT / 'src').rglob('*'):
    if file.suffix not in ('.ts', '.tsx', '.js', '.jsx'): continue
    text = file.read_text(encoding='utf-8')
    for spec in re.findall(r"(?:from\s*|import\s*)['\"]([^'\"]+)['\"]", text):
        if spec.startswith('.'):
            base = (file.parent / spec)
            candidates = [base, *(Path(str(base) + ext) for ext in ('.ts','.tsx','.js','.jsx','.json')),
                          base / 'index.ts', base / 'index.tsx', base / 'index.js']
            imports.append((file.relative_to(ROOT), spec, any(p.is_file() for p in candidates)))
checks['All local imports resolve'] = all(x[2] for x in imports)
# Reject unfinished copy; ordinary HTML input placeholder attributes are not dummy content.
source_files = [p for p in ROOT.rglob('*') if p.is_file() and p.suffix in ('.ts','.tsx','.js','.jsx','.css','.html','.md')]
all_source = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in source_files)
checks['No TODO / dummy copy'] = not re.search(r'\bTODO\b|Lorem ipsum|Coming soon|Under construction|Replace this text', all_source, re.I)
# Use the TypeScript parser to verify TSX syntax and JSX tag structure.
js = r"""
const fs=require('fs'),path=require('path');
let ts; try { ts=require('typescript'); } catch(e) { ts=require(path.join(require('child_process').execSync('npm root -g',{encoding:'utf8'}).trim(),'typescript')); }
const root=process.argv[1]; let failed=false, parsed=0;
function walk(d){ for(const n of fs.readdirSync(d)){const p=path.join(d,n),s=fs.statSync(p);if(s.isDirectory())walk(p);else if(/\.tsx?$/.test(n)){parsed++;const sf=ts.createSourceFile(p,fs.readFileSync(p,'utf8'),ts.ScriptTarget.Latest,true,n.endsWith('.tsx')?ts.ScriptKind.TSX:ts.ScriptKind.TS);if(sf.parseDiagnostics.length){failed=true;for(const x of sf.parseDiagnostics)process.stderr.write(p+': '+ts.flattenDiagnosticMessageText(x.messageText,' ')+'\\n');}}}}
walk(path.join(root,'src'));console.log('Parsed '+parsed+' TypeScript files');process.exit(failed||!parsed?1:0);
"""
try:
    p = subprocess.run(['node', '-e', js, str(ROOT)], capture_output=True, text=True)
    checks['TS / JSX syntax parses'] = p.returncode == 0
    if p.stdout: print(p.stdout.strip())
    if p.stderr: print(p.stderr.strip())
except Exception as exc:
    checks['TS / JSX syntax parses'] = False
    print('Parser error:', exc)
for name, ok in checks.items(): print(('PASS' if ok else 'FAIL') + '  ' + name)
if not all(checks.values()):
    for f,spec,ok in imports:
        if not ok: print('Unresolved import:', f, spec)
    sys.exit(1)
print(f"Verified: {len(t['crops'])} crops, {len(t['costRecords'])} cost records, {len(t['zones'])} zones, {len(t['zoneCropRecords'])} zone-crop rows, {len(t['cropHazardRecords'])} crop-hazard rows, {len(t['sources'])} sources, {len(obj['charts'])} charts.")
