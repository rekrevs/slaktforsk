import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,importBaseline,verifyDB} from '../lib/store.mjs';
import {applyOperation,inspect,readCurrent,personView} from '../lib/domain.mjs';
import {buildPilot} from '../import/pilot.mjs';
import {buildRegistry} from '../import/registry.mjs';
import {buildPersons} from '../import/persons.mjs';

const read=file=>JSON.parse(fs.readFileSync(new URL('../'+file,import.meta.url),'utf8'));

test('källprecision rättas med bevarad historik och uttrycklig följdprövning',async t=> {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-source-precision07-'));
 const db=openDB(path.join(dir,'db.sqlite'),{create:true});
 t.after(()=>{db.close();fs.rmSync(dir,{recursive:true,force:true});});
 importBaseline(db,new URL('../import/baseline/',import.meta.url).pathname);
 applyOperation(db,buildPilot(db),{legacy:true});
 applyOperation(db,buildRegistry(db,read('migration/retirement-decisions.json')));
 const preparations={4:['media-links','media-review'],5:['source-definitions','source-controls','media-links','media-review'],6:['source-definitions','source-controls','source-volumes','media-links','media-review']};
 for(let i=1;i<=6;i++) {
  const task=String(645+i).padStart(4,'0');
  for(const suffix of preparations[i]??[])applyOperation(db,read(`operations/T-${task}-${suffix}-v1.json`));
  applyOperation(db,read(`operations/T-${task}-evidence-${String(i).padStart(2,'0')}-v1.json`));
 }
 for(const operation of ['T-0652-source-lulea-v1','T-0652-persons-01-v1','T-0653-persons-02-v1','T-0653-review-v1','T-0654-persons-03-v1','T-0654-review-v1','T-0655-persons-04-v1','T-0655-review-v1','T-0656-persons-05-v1','T-0656-review-v1']) {
  applyOperation(db,read(`operations/${operation}.json`));
 }
 applyOperation(db,read('operations/T-0657-persons-06-v1.json'));
 const before=db.prepare('SELECT * FROM revision ORDER BY id').all();
 const correction=read('operations/T-0658-source-precision-v1.json');
 applyOperation(db,correction);
 const value=id=>JSON.parse(readCurrent(db,id).value_json);
 await t.test('rårollen make avgör inte offentlig personidentitet',()=>{
  assert.equal(readCurrent(db,'M-P-0013-C0263-Birger').role_literal,'make');
  assert.equal(readCurrent(db,'ID-M-P-0013-C0263-Birger-P-0301').decision,'candidate');
  assert.equal(readCurrent(db,'REL-spouse-P-0013-P-0301').disposition,'candidate');
 });
 await t.test('Edlas egna flyttar bryter sammanboendet men inte syskonskapet',()=>{
  for(const id of ['F-P-0263-family_context-bounded-siblings','F-P-0268-family_context-siblings-and-parents']){
   const e=value(id).siblings.find(s=>s.person==='P-0317');
   assert.equal(e.individual_gap.start_year,1859);assert.equal(e.individual_gap.end_year,1860);
   assert.equal(e.individual_gap.return_from,'Blacksta');
   assert.equal(e.individual_gap.next_departure.date,'1861-10-19');
   assert.equal(e.individual_gap.next_departure.destination,'Lerbo');
  }
  assert.equal(readCurrent(db,'REL-sibling-P-0268-P-0317').disposition,'accepted');
 });
 await t.test('vittnets ort och oetiketterad ålder får rätt räckvidd även i följdöversikten',()=>{
  assert.equal(value('O-P-0266-C300-witness-a').home_literal,null);
  assert.equal(value('O-P-0266-C300-witness-b').home_literal,'Ö…m[?]');
  assert.equal(value('O-P-0266-C300-child-family').unheaded_age_column.heading,null);
  assert.equal(value('O-P-0266-C300-child-family').unheaded_age_column.literal,'29[?]');
  const age=value('F-P-0267-reported_age-seven-birth-posts').ages.find(a=>a.year===1821);
  assert.equal(age.age,null);assert.equal(age.raw_column,'29[?]');
  const witnesses=db.prepare("SELECT p.* FROM current_revision r JOIN participation p ON p.revision_id=r.id WHERE event_id='E-baptism-P-0322' AND role='witness'").all();
  assert.equal(witnesses.length,2);assert.ok(witnesses.every(p=>p.person_id===null));
 });
 await t.test('gamla revisioner består och följdprövningen krävs innan allt är avstämt',()=>{
  for(const r of before)assert.deepEqual(db.prepare('SELECT * FROM revision WHERE id=?').get(r.id),r);
  assert.equal(db.prepare('SELECT COUNT(*) n FROM pending_review').get().n,31);
  const review=read('operations/T-0658-source-precision-review-v1.json');
  applyOperation(db,review);assert.equal(db.prepare('SELECT COUNT(*) n FROM pending_review').get().n,0);
  assert.equal(applyOperation(db,correction).unchanged,true);assert.equal(applyOperation(db,review).unchanged,true);
  assert.equal(verifyDB(db).ok,true);
 });
});
