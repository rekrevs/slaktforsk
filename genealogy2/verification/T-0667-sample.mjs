// Bounded recovery evidence. Prefix replay is exact; the later domain sample
// is an explicitly labelled projection, never a replacement recovery format.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {bootstrapFromFiles,PILOT_HISTORY} from '../lib/rebuild.mjs';
import {openDB,backupDB,verifyDB} from '../lib/store.mjs';
import {applyOperation} from '../lib/domain.mjs';
import {replayJournal} from '../lib/recovery.mjs';
import {canonical,sha,readBaseline} from '../lib/archive.mjs';

const root=fileURLToPath(new URL('../../',import.meta.url));
const base=path.join(root,'genealogy2'),start=performance.now();
const timings={};
const timed=async(name,fn)=>{const t=performance.now();const value=await fn();timings[name]=Math.round(performance.now()-t);console.log(name,timings[name]+'ms');return value;};
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const journalDir=path.join(base,'journal');
const files=fs.readdirSync(journalDir).filter(f=>/^\d{9}-[a-f0-9]{64}\.json$/.test(f)).sort();
const receipts=files.map(f=>read(path.join(journalDir,f)));
const pilot=read(path.join(base,'operations/T-0641-pilot-v1.json'));
const operations=[pilot,...receipts.map(r=>r.request)];
const original=openDB(path.join(base,'data/research.sqlite'),{readOnly:true});
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-T0667-'));
let prefix,sample;
const result={date:'2026-09-18',inputCommit:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),
  scope:'Exact import/pilot/journal-prefix plus dependency-closed projected domain histories; not full reconstruction',timings};
try {
  result.inputs=await timed('inputAudit',()=>{
    const manifest=readBaseline(path.join(base,'import/baseline'));
    const tracked=new Set(execFileSync('git',['ls-files','-z'],{cwd:root,encoding:'utf8',maxBuffer:8*1024*1024}).split('\0'));
    for(const f of manifest.files){
      const rel=f.storage==='object'?`genealogy2/import/baseline/objects/${f.sha256}`:f.path;
      assert(tracked.has(rel),`Not committed: ${rel}`);
      assert.equal(fs.statSync(path.join(root,rel)).size,f.bytes);
    }
    assert.equal(sha(canonical(pilot)),PILOT_HISTORY.requestHash);
    assert.equal(original.prepare('SELECT recorded_at FROM operation WHERE id=?').get(pilot.id).recorded_at,PILOT_HISTORY.recordedAt);
    assert.equal(original.prepare('SELECT count(*) n FROM operation').get().n,operations.length);
    assert.equal(original.prepare('SELECT count(*) n FROM operation_payload').get().n,receipts.length);
    for(let i=0;i<receipts.length;i++){
      const r=receipts[i];assert.equal(r.sequence,i+1);assert.equal(sha(canonical(r.request)),r.requestHash);
      assert.equal(files[i],`${String(i+1).padStart(9,'0')}-${r.requestHash}.json`);
      const stored=original.prepare('SELECT o.*,p.sequence,p.policy,p.request_json FROM operation o JOIN operation_payload p ON p.operation_id=o.id WHERE o.id=?').get(r.request.id);
      assert.equal(stored.request_hash,r.requestHash);assert.equal(stored.sequence,r.sequence);assert.equal(stored.policy,r.policy);
      assert.equal(stored.recorded_at,r.recordedAt);assert.equal(canonical(JSON.parse(stored.request_json)),canonical(r.request));
      assert(tracked.has('genealogy2/journal/'+files[i]));
    }
    return {documents:manifest.files.filter(f=>f.storage==='object').length,assets:manifest.files.filter(f=>f.storage!=='object').length,
      operations:operations.length,journal:receipts.length,baselineId:manifest.id};
  });

  // Normal bootstrap refuses an existing target before doing any work.
  const prefixFile=path.join(dir,'prefix.sqlite');
  await timed('bootstrap',()=>bootstrapFromFiles(root,prefixFile));
  assert.throws(()=>bootstrapFromFiles(root,prefixFile),/nytt mål/);
  prefix=openDB(prefixFile);
  assert.equal(prefix.prepare('SELECT count(*) n FROM operation_payload').get().n,0);
  assert.equal(canonical(prefix.prepare('SELECT * FROM operation').get()),canonical(original.prepare('SELECT * FROM operation WHERE id=?').get(pilot.id)));
  // Compare imported document/registry tables before the domain projections.
  for(const table of ['import_batch','document','asset','legacy_entity','legacy_assertion']){
    assert.equal(canonical(prefix.prepare(`SELECT * FROM ${table} ORDER BY 1`).all()),canonical(original.prepare(`SELECT * FROM ${table} ORDER BY 1`).all()),table);
  }
  const sampleFile=path.join(dir,'sample.sqlite');await backupDB(prefix,sampleFile);sample=openDB(sampleFile);
  const first=path.join(dir,'prefix-journal');fs.mkdirSync(first);fs.copyFileSync(path.join(journalDir,files[0]),path.join(first,files[0]));
  result.prefix=await timed('exactPrefixReplay',async()=>{
    assert.deepEqual(await replayJournal(prefix,first,{root}),{applied:1,entries:1});
    assert.deepEqual(await replayJournal(prefix,first,{root}),{applied:0,entries:1});
    assert.equal(canonical(prefix.prepare('SELECT * FROM operation_payload WHERE sequence=1').get()),canonical(original.prepare('SELECT * FROM operation_payload WHERE sequence=1').get()));
    assert.equal(verifyDB(prefix).ok,true);
    return {journalEntries:1,objects:prefix.prepare('SELECT count(*) n FROM object').get().n,idempotent:true,firstReceiptExact:true};
  });

  const allIds=new Set(operations.flatMap(o=>o.changes.map(c=>c.id)));
  const selected=new Set([...pilot.changes.map(c=>c.id),'O-P-0027-children-book-sequence',
    'F-P-0027-household_comparison-children-book-sequence','O-P-0362-C1013-rejected-Carolina','E-death-P-0368']);
  for(const id of selected)assert(allIds.has(id),id);
  const latest=receipts.at(-1).request,corrections=receipts.at(-2).request;
  assert.equal(receipts.at(-1).sequence,39);assert.equal(receipts.at(-2).sequence,38);
  const selectedUnits=new Set([corrections.unitDecisions[0].unit,
    ...[0,Math.floor(latest.unitDecisions.length/2),latest.unitDecisions.length-1].map(i=>latest.unitDecisions[i].unit)]);
  function references(v){
    if(typeof v==='string'){if(allIds.has(v))selected.add(v);}
    else if(v&&typeof v==='object')for(const x of Object.values(v))references(x);
  }
  let previous;
  do {
    previous=selected.size;
    for(const o of operations){for(const c of o.changes)if(selected.has(c.id))references(c);
      for(const d of o.unitDecisions??[])if(selectedUnits.has(d.unit))references(d);}
    // Curated provenance spans can be introduced by an earlier operation
    // without a selected domain change. Retain a real change from that
    // operation so the span is introduced with its original operation id.
    const neededUnits=new Set(selectedUnits);
    for(const o of operations)for(const c of o.changes)if(selected.has(c.id))for(const origin of c.origins??[])neededUnits.add(origin.unit);
    for(const o of operations)if((o.spans??[]).some(s=>neededUnits.has(s.id))&&!o.changes.some(c=>selected.has(c.id))){
      assert(o.changes.length,'Required span has no selectable defining operation');selected.add(o.changes[0].id);
    }
  }while(selected.size!==previous);
  assert(selected.size<=500,'Sample dependency closure exceeded its budget');

  let projectedOperations=0,projectedChanges=pilot.changes.length,resolutions=0;
  await timed('projectedReplay',()=>{
    for(const r of receipts){
      const request=r.request;
      const projected={...request,changes:request.changes.filter(c=>selected.has(c.id)),
        unitDecisions:(request.unitDecisions??[]).filter(d=>selectedUnits.has(d.unit)),
        mappings:(request.mappings??[]).filter(m=>selected.has(m.target)),resolve:[]};
      if(projected.changes.length||projected.unitDecisions.length||projected.mappings.length){
        applyOperation(sample,projected,{legacy:r.policy==='legacy/1',recordedAt:r.recordedAt});
        projectedOperations++;projectedChanges+=projected.changes.length;
      }
      const resolve=(request.resolve??[]).filter(x=>sample.prepare('SELECT 1 FROM pending_review WHERE id=?').get(x.request));
      if(resolve.length){
        applyOperation(sample,{id:request.id+'/sample-resolutions',actor:request.actor,reason:'Projected verification only',changes:[],resolve},{recordedAt:r.recordedAt});
        resolutions+=resolve.length;
      }
    }
  });
  let comparedRows=0;
  const equalRows=(table,key,value)=>{
    const a=sample.prepare(`SELECT * FROM ${table} WHERE ${key}=?`).all(value),b=original.prepare(`SELECT * FROM ${table} WHERE ${key}=?`).all(value);
    assert.equal(canonical(a.map(canonical).sort()),canonical(b.map(canonical).sort()),`${table}/${value}`);comparedRows+=a.length;
  };
  await timed('sampleComparison',()=>{
    for(const id of selected){
      equalRows('object','id',id);equalRows('revision','object_id',id);
      const revisions=sample.prepare('SELECT r.id,o.kind FROM revision r JOIN object o ON o.id=r.object_id WHERE r.object_id=?').all(id);
      for(const r of revisions){
        for(const table of [r.kind,'origin','dependency'])equalRows(table,'revision_id',r.id);
        if(r.kind==='record')for(const table of ['record_asset','record_media'])equalRows(table,'revision_id',r.id);
      }
      // Full person/record views can include other, deliberately unselected
      // objects. Compare the exact current revision and payload above instead.
      equalRows('current_revision','object_id',id);
    }
    for(const unit of selectedUnits){
      equalRows('unit_decision','unit_id',unit);
      for(const d of sample.prepare('SELECT id FROM unit_decision WHERE unit_id=?').all(unit))equalRows('unit_decision_target','decision_id',d.id);
    }
    assert.equal(verifyDB(sample).ok,true);
  });
  result.sample={objects:selected.size,revisions:projectedChanges,projectedOperations,resolutions,units:selectedUnits.size,comparedRows,
    objectIds:[...selected].sort(),unitIds:[...selectedUnits].sort(),
    limitation:'Filtered operations have different request hashes and a compact sequence; their receipts and full-person completeness are not compared. Resolutions are separate sample operations. Exact journal sequence is tested only in prefix.'};
  result.ok=true;result.totalMs=Math.round(performance.now()-start);
  result.verifierSha256=sha(fs.readFileSync(fileURLToPath(import.meta.url)));
  result.bootstrapSha256=sha(fs.readFileSync(path.join(base,'lib/rebuild.mjs')));
  fs.writeFileSync(path.join(base,'verification/T-0667-result.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({...result,sample:{...result.sample,objectIds:undefined,unitIds:undefined}},null,2));
}finally{prefix?.close();sample?.close();original.close();fs.rmSync(dir,{recursive:true,force:true});}
