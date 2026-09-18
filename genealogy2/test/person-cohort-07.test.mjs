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
import {checkPersons07Risks} from '../verification/persons-07-risk-checks.mjs';

const base=new URL('../',import.meta.url).pathname;
const read=file=>JSON.parse(fs.readFileSync(path.join(base,file)));

test('sjunde kohorten bevarar källrättelser och avgränsningar med full radtäckning, omkörning och återställning',()=>{
 const reviews=['a','b','c','d'].flatMap(k=>read(`migration/persons-07-${k}.json`)).sort((a,b)=>a.person.localeCompare(b.person));
 assert.equal(reviews.length,50);
 assert.deepEqual(reviews.map(r=>r.person),Array.from({length:50},(_,i)=>`P-${String(301+i).padStart(4,'0')}`));
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-persons07-test-'));
 const db=openDB(path.join(dir,'original.sqlite'),{create:true});let restored;
 try {
  importBaseline(db,path.join(base,'import/baseline'));
  // Piloten föregår den beständiga journalens införande.
  applyOperation(db,buildPilot(db),{legacy:true});
  // Det fastställda utgångsläget: journalposter1–31, inklusive de sju
  // källpreciseringarna och deras uttryckliga följdgranskningar.
  const entries=fs.readdirSync(path.join(base,'journal')).filter(f=>/^\d{9}-[a-f0-9]{64}\.json$/.test(f)&&Number(f.slice(0,9))<=31).sort();
  assert.equal(entries.length,31);
  for(const file of entries){const e=read('journal/'+file);assert.equal(sha(canonical(e.request)),e.requestHash);applyOperation(db,e.request,{legacy:e.policy==='legacy/1',recordedAt:e.recordedAt});}
  assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
  const before=exportData(db);
  const operation=buildPersons(db,reviews,{group:'persons-07'});
  assert.equal(canonical(operation),canonical(read('operations/T-0658-persons-07-v1.json')));
  applyOperation(db,operation);
  assert.equal(applyOperation(db,operation).unchanged,true);
  assert.deepEqual(checkPersons07Risks(db),{groups:20,ok:true});
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
  for(const review of reviews){
   for(const a of review.assertions){const i=inspect(db,a.id),u=i.legacyUnits.filter(x=>!x.historical);assert.equal(u.length,1,a.id);const d=i.conversionDecisions.find(x=>x.unit_id===u[0].id);assert.ok(d,a.id);assert.equal(d.state,a.state,a.id);}
   for(const r of review.relations){const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(r.unit);assert.ok(d,r.unit);assert.equal(d.state,r.state);}
  }
  // Två beroenden av den rättade vittnesorten behöver egna bedömningar.
  assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,2);
  const review=read('operations/T-0658-review-v1.json');applyOperation(db,review);
  assert.equal(applyOperation(db,review).unchanged,true);
  assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
  assert.equal(verifyDB(db).ok,true);
  const data=exportData(db),digest=sha(canonical(data));
  restore(data,path.join(dir,'restored.sqlite'));
  restored=openDB(path.join(dir,'restored.sqlite'),{readOnly:true});
  assert.equal(sha(canonical(exportData(restored))),digest);
  assert.equal(verifyDB(restored).ok,true);
  assert.deepEqual(checkPersons07Risks(restored),{groups:20,ok:true});
  // Läsaren tar med den nya kunskapen och samma öppna granskning efter restore.
  assert.equal(canonical(personView(db,'P-0336')),canonical(personView(restored,'P-0336')));
  assert.match(readCurrent(restored,'ASSESSMENT-P-0336').outcome,/UNDERKÄND/);
 }finally{restored?.close();db.close();fs.rmSync(dir,{recursive:true,force:true});}
});
