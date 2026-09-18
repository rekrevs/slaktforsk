import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,importBaseline,verifyDB,exportData,restore} from '../lib/store.mjs';
import {applyOperation,inspect,readCurrent,personView} from '../lib/domain.mjs';
import {canonical,sha} from '../lib/archive.mjs';
import {buildPersons} from '../import/persons.mjs';
import {buildPilot} from '../import/pilot.mjs';

const base=new URL('../',import.meta.url).pathname;
const read=file=>JSON.parse(fs.readFileSync(path.join(base,file)));

test('nionde kohorten bevarar källrättelser och avgränsningar med full radtäckning, omkörning och återställning',async()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-persons09-test-'));
 const db=openDB(path.join(dir,'original.sqlite'),{create:true});let restored;
 try {
  importBaseline(db,path.join(base,'import/baseline'));
  // Piloten föregår den beständiga journalens införande.
  applyOperation(db,buildPilot(db),{legacy:true});
  // Det fastställda utgångsläget: journalposter1–34, inklusive de sju
  // källpreciseringarna och deras uttryckliga följdgranskningar.
  const entries=fs.readdirSync(path.join(base,'journal')).filter(f=>/^\d{9}-[a-f0-9]{64}\.json$/.test(f)&&Number(f.slice(0,9))<=34).sort();
  assert.equal(entries.length,34);
  for(const file of entries){const e=read('journal/'+file);assert.equal(sha(canonical(e.request)),e.requestHash);applyOperation(db,e.request,{legacy:e.policy==='legacy/1',recordedAt:e.recordedAt});}
  console.info('persons-09: bas, pilot och journalposter 1–34 återspelade');
  const {checkPersons09Risks}=await import('../verification/persons-09-risk-checks.mjs');
 const reviews=['a','b','c','d'].flatMap(k=>read(`migration/persons-09-${k}.json`)).sort((a,b)=>a.person.localeCompare(b.person));
 assert.equal(reviews.length,50);
 assert.deepEqual(reviews.map(r=>r.person),Array.from({length:50},(_,i)=>`P-${String(401+i).padStart(4,'0')}`));

  assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
  const before=exportData(db);
  const operation=buildPersons(db,reviews,{group:'persons-09'});
  assert.equal(canonical(operation),canonical(read('operations/T-0660-persons-09-v1.json')));
  applyOperation(db,operation);
  assert.equal(applyOperation(db,operation).unchanged,true);
  assert.equal(checkPersons09Risks(db).ok,true);
  // Det äldre underlaget och alla tidigare revisioner är oförändrade.
  const after=exportData(db);
  for(const [table,rows]of Object.entries(before.tables)){
   const hashes=new Set(after.tables[table].map(r=>sha(canonical(r))));
   for(const row of rows)assert.ok(hashes.has(sha(canonical(row))),`Äldre rad ändrad i ${table}`);
  }
  // Alla akter/profiler och varje aktuell A-/relationsrad har ett eget utfall.
  const documents=reviews.flatMap(r=>r.documents.map(d=>d.path));assert.equal(new Set(documents).size,100);
  for(const doc of documents){
   const missing=db.prepare('SELECT u.id FROM unit u LEFT JOIN current_unit_decision d ON d.unit_id=u.id WHERE u.document_path=? AND d.unit_id IS NULL').all(doc);
   assert.deepEqual(missing,[],doc);
  }
  function checkRow(review,row,unit,label){
   const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(unit);
   assert.ok(d,label);
   const pending=review.pending.filter(p=>p.origin===unit||p.origin===row.id);
   assert.equal(d.state,pending.length?'pending_interpretation':row.state,label);
   const targets=db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=?').all(unit).map(t=>t.target_id);
   for(const target of row.targets)assert.ok(targets.includes(target),`${label}: ${target}`);
   for(const p of pending)assert.ok(d.question.includes(p.question),label);
  }
  for(const review of reviews){
   for(const a of review.assertions){const u=inspect(db,a.id).legacyUnits.filter(x=>!x.historical);assert.equal(u.length,1,a.id);checkRow(review,a,u[0].id,a.id);}
   for(const r of review.relations)checkRow(review,r,r.unit,r.unit);
  }
  // Även profiler och särskilt kuraterade textspann lagras med hela sitt beslut.
  for(const expected of operation.unitDecisions){
   const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(expected.unit);
   assert.equal(d.state,expected.state,expected.unit);
   assert.equal(d.question,expected.question,expected.unit);
   const targets=db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=? ORDER BY target_id').all(expected.unit).map(t=>t.target_id);
   assert.deepEqual(targets,[...expected.targets].sort(),expected.unit);
  }
  assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
  assert.equal(verifyDB(db).ok,true);
  console.info('persons-09: införsel, omkörning, semantiska riskfall, historik och full enhetstäckning godkända');
  const data=exportData(db),digest=sha(canonical(data));
  restore(data,path.join(dir,'restored.sqlite'));
  restored=openDB(path.join(dir,'restored.sqlite'),{readOnly:true});
  assert.equal(sha(canonical(exportData(restored))),digest);
  assert.equal(verifyDB(restored).ok,true);
  assert.equal(checkPersons09Risks(restored).ok,true);
  // P-0412 är en avvisad läsning, inte en person eller ett identitetsalias.
  const archived=personView(restored,'P-0412');
  assert.equal(archived.person,null);
  assert.equal(readCurrent(restored,'IMPORT-P-0412').outcome,'historical_proposal');
  assert.equal(readCurrent(restored,'ASSESSMENT-P-0412').subject_id,'IMPORT-P-0412');
  assert.equal(readCurrent(restored,'BIO-P-0412').subject_id,'IMPORT-P-0412');
  assert.equal(readCurrent(restored,'BIO-P-0412').disposition,'retired');
  assert.ok(archived.research.questions.length>0);
  assert.ok(archived.research.questions.every(q=>!q.active&&q.subject_id==='IMPORT-P-0412'));
  assert.equal(archived.relations.length,0);
  assert.equal(archived.events.length,0);
  assert.ok(archived.identityMappings.every(m=>m.mapping_type==='archival_reference'));
  assert.equal(canonical(personView(db,'P-0412')),canonical(archived));
  assert.notEqual(readCurrent(restored,'P-0424').object_id,readCurrent(restored,'P-0028').object_id);
  assert.equal(readCurrent(restored,'P-0424').disposition,'accepted');
  console.info('persons-09: identisk återställning; avvecklad forskning och avvisad läsning bevarade');
 }finally{restored?.close();db.close();fs.rmSync(dir,{recursive:true,force:true});}
});
