const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
let ts;try{ts=require('typescript')}catch{ts=require(path.join(require('node:child_process').execSync('npm root -g',{encoding:'utf8'}).trim(),'typescript'))}
const file=path.resolve(__dirname,'../src/data/analytics.ts');const code=ts.transpileModule(fs.readFileSync(file,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,esModuleInterop:true,target:ts.ScriptTarget.ES2020}}).outputText;const moduleObject={exports:{}};new Function('require','module','exports',code)(createRequire(file),moduleObject,moduleObject.exports);const a=moduleObject.exports;
assert.equal(a.costs.length,40);assert.equal(a.crops.length,11);assert.equal(a.zones.length,10);assert.equal(a.sources.length,18);assert.equal(a.costs.filter(a.hasCost).length,26);
for (const [year,expected] of Object.entries({'KMS 2022-23':[5,8,5],'KMS 2023-24':[4,4,8],'RMS 2025-26':[0,2,0]})) ['A2','A2+FL','C2'].forEach((c,i)=>assert.equal(a.benchmark(year,c).length,expected[i]));
assert.equal(a.benchmark('2023-24','A2').length,0);assert.equal(a.benchmark('KMS 2023-24','A2+FL').every(a.national),true);
assert.equal(a.finite(null),null);assert.equal(a.finite('0'),null);assert.equal(a.finite(0),0);assert.equal(a.finite(Infinity),null);
const toor=a.costs.find(r=>r['Record ID']==='C016');assert.equal(a.perQuintal(toor,'A2+FL'),4444);assert.ok(Math.abs(a.impliedAcre(toor,'A2+FL')-toor['Implied A2+FL (₹/acre)'])<1e-8);assert.equal(a.impliedAcre(a.costs.find(r=>r['Record ID']==='C019'),'C2'),null);
assert.deepEqual(a.droughtBreakdown().map(r=>r.value),[53.92,4.01]);assert.equal(a.eventValue(23),57.93);assert.equal(a.weatherEvents.length,6);assert.equal(a.componentHeads.length,17);assert.equal(a.coverage().find(r=>r.name==='Measured hazard yield loss').n,0);
console.log('Analytics tests passed: exact filters, nulls, cost/yield derivation, scope, counts, weather breakdown and coverage');
