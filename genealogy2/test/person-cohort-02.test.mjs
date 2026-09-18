import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,importBaseline,exportData,restore,verifyDB} from '../lib/store.mjs';
import {applyOperation,readCurrent,personView} from '../lib/domain.mjs';
import {buildPilot} from '../import/pilot.mjs';
import {buildRegistry} from '../import/registry.mjs';
import {buildPersons} from '../import/persons.mjs';
import {canonical,sha} from '../lib/archive.mjs';

const read=file=>JSON.parse(fs.readFileSync(new URL('../'+file,import.meta.url),'utf8'));

test('andra personkohorten skiljer källpersoner, kandidatföräldrar, registreringsdagar och avvecklad forskning',t=> {
 const reviews=['a','b','c','d','e','f'].flatMap(s=>read(`migration/persons-02-${s}.json`));
 assert.equal(reviews.length,50,'Kohorten ska vara komplett före verifiering.');
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-person-cohort02-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
 importBaseline(db,new URL('../import/baseline/',import.meta.url).pathname);
 applyOperation(db,buildPilot(db),{legacy:true});applyOperation(db,buildRegistry(db,read('migration/retirement-decisions.json')));
 const preparations={4:['media-links','media-review'],5:['source-definitions','source-controls','media-links','media-review'],6:['source-definitions','source-controls','source-volumes','media-links','media-review']};
 for(let i=1;i<=6;i++) {
  const task=String(645+i).padStart(4,'0');
  for(const suffix of preparations[i]??[])applyOperation(db,read(`operations/T-${task}-${suffix}-v1.json`));
  applyOperation(db,read(`operations/T-${task}-evidence-${String(i).padStart(2,'0')}-v1.json`));
 }
 applyOperation(db,read('operations/T-0652-source-lulea-v1.json'));
 applyOperation(db,read('operations/T-0652-persons-01-v1.json'));
 const old=db.prepare('SELECT * FROM revision ORDER BY id').all();
 const request=buildPersons(db,reviews,{group:'persons-02'});
 applyOperation(db,request);
 assert.equal(canonical(buildPersons(db,reviews,{group:'persons-02'})),canonical(request));
 assert.equal(applyOperation(db,request).unchanged,true);
 assert.deepEqual(db.prepare('SELECT * FROM revision WHERE operation_id<>? ORDER BY id').all(request.id),old);
 for(const doc of read('migration/cohorts.json').groups.find(g=>g.id==='persons-02').documents) {
  for(const u of db.prepare('SELECT id FROM unit WHERE document_path=?').all(doc)) {
   const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(u.id);
   assert.equal(d?.operation_id,request.id,`${doc}/${u.id}`);
   if(d.state==='pending_interpretation')assert.ok(d.question.trim());
  }
 }
 for(const id of ['P-0058','P-0059','P-0074','P-0075']) {
  const v=personView(db,id);assert.equal(v.person.disposition,'accepted');
  assert.equal(v.person.legacy_state,'retired');assert.ok(v.research.questions.length);
  assert.ok(v.research.questions.every(q=>q.active===false&&q.disposition==='retired'));
 }
 assert.equal(readCurrent(db,'ID-P-0051-Bodan_candidate').decision,'candidate');
 assert.equal(readCurrent(db,'ID-C0108-Johannes-P0058').decision,'candidate');
 assert.equal(readCurrent(db,'ID-C0146-Cathrina-P0059').decision,'candidate');
 for(const person of ['P-0051','P-0058','P-0059','P-0077']) {
  assert.equal(db.prepare("SELECT count(*) n FROM current_relation WHERE to_person=? AND relation_type='parent' AND disposition='accepted'").get(person).n,0,'En kandidat eller oidentifierad förälder får inte bli accepterad föräldrakant.');
 }
 for(const parent of ['P-0058','P-0059'])for(const child of ['P-0238','P-0060','P-0061','P-0424','P-0062','P-0063','P-0064']) {
  const r=readCurrent(db,`REL-parent-${parent}-${child}`);assert.equal(r.from_person,parent);assert.equal(r.to_person,child);
 }
 assert.equal(readCurrent(db,'IDENTITY-P0424-P0028').decision,'different_people');
 assert.equal(readCurrent(db,'IDENTITY-P-0082-P-0088').decision,'same_person');
 assert.equal(db.prepare("SELECT count(*) n FROM legacy_mapping WHERE legacy_id='P-0088' AND mapping_type='same_identity'").get().n,0,'Forskningsbedömningen får inte bli en ännu ej beslutad administrativ sammanslagning.');
 const witnesses=event=>db.prepare('SELECT p.* FROM current_revision r JOIN participation p ON p.revision_id=r.id WHERE p.event_id=? AND p.role=?').all(event,'witness');
 const w1854=witnesses('E-baptism-P-0238');assert.equal(w1854.length,8);
 const wives=w1854.map(w=>readCurrent(db,w.mention_id)).filter(m=>m?.name_literal==='hustru');
 assert.equal(wives.length,3);assert.equal(new Set(wives.map(m=>m.object_id)).size,3,'Tre verkliga namnlösa hustrur får inte kollapsa till en person.');
 const w1861=witnesses('E-baptism-P-0424');assert.equal(w1861.length,6);
 assert.equal(w1861.filter(w=>w.person_id==='P-0080').length,1);assert.equal(w1861.filter(w=>w.person_id==='P-0081').length,1);
 assert.equal(readCurrent(db,'M-C0050-Jon-Olsson').name_literal,'Jon Olsson');
 assert.match(readCurrent(db,'O-C0050-Jon-Olsson').value_literal,/Gunnismark eller Bullmark/);
 const reg=JSON.parse(readCurrent(db,'F-P-0058-migration_registration-1856').value_json);
 assert.equal(reg.departure_record.number,7);assert.equal(reg.arrival_record.number,6);
 assert.equal(reg.departure_record.date_literal,'2/4[?] 1856');assert.equal(reg.household_note.date,'1856-04-04');
 const sharedRegistration=['P-0058','P-0059'].map(id=>personView(db,id).events.find(e=>e.event_id==='E-registered_departure-P0058-family-Degerfors1856').qualifications);
 assert.ok(sharedRegistration[0].some(f=>f.object_id==='F-P-0058-migration_registration-1856'));
 assert.deepEqual(sharedRegistration[0],sharedRegistration[1]);
 assert.equal(JSON.parse(readCurrent(db,'E-marriage-P-0058-P-0059-1854').date_json).precision,'alternatives');
 for(const id of ['E-death-P-0059','E-burial-P-0059'])assert.equal(readCurrent(db,id).place_id,null,'Registrerande bok och hemvist får inte bli fysisk döds-/gravplats.');
 assert.match(readCurrent(db,'E-death-P-0059').caveat,/Alvik är hemvist/);
 const probateSearch=JSON.parse(readCurrent(db,'SEARCH-P-0059-A-2276').scope_json);
 assert.equal(probateSearch.bounds.queries.length,3);
 assert.equal(probateSearch.bounds.queries[1].geography,'hela landet','Den nationella sökningen får inte begränsas till orten genom en gemensam ortetikett.');
 assert.equal(probateSearch.bounds.place,undefined);
 assert.equal(readCurrent(db,'REL-parent-P-0074-P-0076').disposition,'accepted');
 assert.equal(db.prepare("SELECT count(*) n FROM current_relation WHERE from_person='P-0075' AND to_person='P-0076' AND relation_type='parent' AND disposition='accepted'").get().n,0);
 for(const [id,role] of [['M-P-0049-relative-father',/avliden/],['M-P-0049-relative-mother',/avliden/]]) {
  const m=readCurrent(db,id);assert.equal(m.version,2);assert.match(m.role_literal,role);
 }
 const oldHousehold=readCurrent(db,'O-P-0049-A-5522-grandparents_household');
 assert.equal(oldHousehold.version,2);assert.doesNotMatch(oldHousehold.value_literal,/1880|förgångsmor|familj\s?2/);
 const laterHousehold=readCurrent(db,'O-P-0094-mother-census1880');
 assert.notEqual(oldHousehold.record_id,laterHousehold.record_id);
 assert.equal(JSON.parse(laterHousehold.value_json).year,1880);
 assert.ok(personView(db,'P-0049').observations.some(o=>o.object_id===laterHousehold.object_id),'Den uppdelade källuppgiften ska förbli nåbar från den gamla personvyn.');
 const pending=db.prepare('SELECT * FROM pending_review').all();
 for(const who of ['father','mother'])assert.ok(pending.some(r=>JSON.stringify(r).includes(`O-P-0049-A-5525-${who}-relative_death_context`)),'Källrollsrättelse ska kräva uttrycklig omprövning av den äldre beroende observationen.');
 assert.equal(verifyDB(db).ok,true);
 const exported=exportData(db),digest=sha(canonical(exported));restore(exported,path.join(dir,'restore.sqlite'));
 const restored=openDB(path.join(dir,'restore.sqlite'));try{assert.equal(sha(canonical(exportData(restored))),digest);}finally{restored.close();}
});
