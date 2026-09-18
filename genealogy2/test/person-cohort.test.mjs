import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,importBaseline,exportData,restore,verifyDB} from '../lib/store.mjs';
import {applyOperation,inspect,readCurrent,personView} from '../lib/domain.mjs';
import {buildPilot} from '../import/pilot.mjs';
import {buildRegistry} from '../import/registry.mjs';
import {buildPersons} from '../import/persons.mjs';
import {canonical,sha} from '../lib/archive.mjs';

const read=file=>JSON.parse(fs.readFileSync(new URL('../'+file,import.meta.url),'utf8'));

test('första personkohorten bevarar rättelser, gemensamma källomnämnanden, riktade relationer och avvecklade frågor',t=> {
 const reviews=['a','b','c','d'].flatMap(s=>read(`migration/persons-01-${s}.json`));
 assert.equal(reviews.length,50,'Hela godkända kohorten krävs; ingen delmängd får räknas som färdig.');
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-person-cohort-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
 importBaseline(db,new URL('../import/baseline/',import.meta.url).pathname);
 applyOperation(db,buildPilot(db),{legacy:true});applyOperation(db,buildRegistry(db,read('migration/retirement-decisions.json')));
 const preparations={4:['media-links','media-review'],5:['source-definitions','source-controls','media-links','media-review'],6:['source-definitions','source-controls','source-volumes','media-links','media-review']};
 for(let i=1;i<=6;i++){
  const task=String(645+i).padStart(4,'0');for(const suffix of preparations[i]??[])applyOperation(db,read(`operations/T-${task}-${suffix}-v1.json`));
  applyOperation(db,read(`operations/T-${task}-evidence-${String(i).padStart(2,'0')}-v1.json`));
 }
 applyOperation(db,read('operations/T-0652-source-lulea-v1.json'));
 const old=db.prepare('SELECT * FROM revision ORDER BY id').all(),request=buildPersons(db,reviews);
 applyOperation(db,request);
 assert.equal(canonical(buildPersons(db,reviews)),canonical(request));assert.equal(applyOperation(db,request).unchanged,true);
 assert.deepEqual(db.prepare('SELECT * FROM revision WHERE operation_id<>? ORDER BY id').all(request.id),old);
 const cohort=read('migration/cohorts.json').groups.find(g=>g.id==='persons-01');
 for(const doc of cohort.documents)for(const u of db.prepare('SELECT id,kind,legacy_id FROM unit WHERE document_path=?').all(doc)){
  const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(u.id);assert.ok(d,`${doc}: ${u.id}`);assert.equal(d.operation_id,request.id);
  if(d.state==='pending_interpretation')assert.ok(d.question.trim());
 }
 const targets=id=>inspect(db,id).conversionDecisions.find(d=>d.state==='mapped_complete')?.targets??[];
 assert.equal(targets('A-1711').filter(id=>readCurrent(db,id)?.kind==='relation').length,6);
 const maternal=readCurrent(db,'REL-parent-P-0007-P-0005');assert.equal(maternal.from_person,'P-0007');assert.equal(maternal.to_person,'P-0005');assert.equal(maternal.evidence_status,'CORROBORATED');assert.match(maternal.rationale,/T0150/);assert.match(maternal.caveat,/h\.f\./);
 for(const parent of ['P-0042','P-0043']){const r=readCurrent(db,`REL-foster_parent-${parent}-P-0003`);assert.equal(r.from_person,parent);assert.equal(r.to_person,'P-0003');}
 assert.equal(db.prepare("SELECT count(*) n FROM current_relation WHERE relation_type='foster_parent' AND from_person='P-0003' AND to_person IN ('P-0042','P-0043')").get().n,0);
 const witnesses=db.prepare("SELECT p.* FROM current_revision r JOIN participation p ON p.revision_id=r.id WHERE p.event_id='E-baptism-P-0001' AND p.role='witness'").all();assert.equal(witnesses.length,10);assert.ok(witnesses.every(w=>w.person_id===null));
 const wives=witnesses.map(w=>readCurrent(db,w.mention_id)).filter(m=>m.name_literal==='hans hustru');assert.equal(wives.length,2);assert.notEqual(wives[0].object_id,wives[1].object_id);
 const repeated=db.prepare("SELECT count(DISTINCT m.object_id) n FROM current_revision m JOIN mention x ON x.revision_id=m.id JOIN identity i ON i.mention_id=m.object_id JOIN current_revision ir ON ir.id=i.revision_id WHERE x.record_id='R-1061d792a13da3adb41953c7' AND i.person_id='P-0042' AND i.decision='accepted'").get();assert.ok(repeated.n<=1,'Två sakuppgifter på samma Karl-rad får inte skapa två omnämnanden.');
 for(const id of ['O-P-0042-A-3929-family_identifiers','O-P-0042-A-3930-registration_columns']){const o=readCurrent(db,id);assert.equal(o.record_id,'R-1061d792a13da3adb41953c7');assert.equal(o.mention_id,null,'Ett kanoniskt visningsnamn får inte förvandlas till källans namnform.');}
 const f1006=JSON.parse(readCurrent(db,'O-P-0006-f1006-daughter').value_json);assert.equal(f1006.birth_parish,null);assert.equal(f1006.birth_parish_cell_empty,true);assert.match(readCurrent(db,'E-birth-P-0006').place_role,/Burträsk/);assert.match(readCurrent(db,'E-birth-P-0006').caveat,/f275/);
 const p8=personView(db,'P-0008');assert.equal(p8.person.legacy_state,'retired');assert.equal(p8.person.sex,'female');assert.ok(p8.research.questions.every(q=>!q.active&&q.disposition==='retired'));assert.equal(p8.relations.find(r=>r.to_person==='P-0003').disposition,'rejected');
 const twins=['P-0018','P-0019'].map(id=>personView(db,id).relations.find(r=>r.object_id==='REL-sibling-P-0018-P-0019').qualifications.find(f=>f.property==='twin_relationship'));assert.ok(twins[0]);assert.deepEqual(twins[0],twins[1]);assert.equal(twins[0].evidence_status,'INFERRED');
 assert.equal(readCurrent(db,'IDRES-P-0008-P-0009').decision,'different_people');
 const pageContext=readCurrent(db,'R-C0009-Strangnas1910-page13-context');assert.equal(pageContext.record_type,'census_page_context');assert.equal(readCurrent(db,'O-P-0008-staff-context').record_id,pageContext.object_id);assert.equal(readCurrent(db,'O-P-0008-communion-controls').record_id,pageContext.object_id);assert.equal(inspect(db,pageContext.object_id).revisions[0].assets[0].path,'genealogy/media/C-0009-riksarkivet-folkrakning-1910-strangnas-land-bild-13.jpg');
 assert.ok(p8.interpretationQuestions.some(q=>/13kvinnor/.test(q.question)));
 assert.ok(personView(db,'P-0016').interpretationQuestions.some(q=>/C-0919:128/.test(q.question)),'Den källbundna änkedatumkonflikten måste vara nåbar från personen.');
 assert.ok(personView(db,'P-0036').interpretationQuestions.some(q=>/C-0889:42/.test(q.question)),'Frågan om redan bevarad hustru och son får inte försvinna utanför dokumentomfånget.');
 const p7=personView(db,'P-0007');assert.equal(readCurrent(db,'ASSESSMENT-P-0007-rad16-correction').outcome,'old_absence_conclusion_withdrawn');assert.ok(p7.observations.some(o=>o.record_id==='R-88c4d51debd66f79529f0e5b'));assert.equal(readCurrent(db,'E-death-P-0007').place_id,null);assert.match(readCurrent(db,'E-death-P-0007').caveat,/Lokal postkopia/);
 assert.equal(JSON.parse(readCurrent(db,'E-birth-P-0038').date_json).precision,'year');assert.match(readCurrent(db,'E-birth-P-0038').caveat,/väntar/);
 assert.equal(readCurrent(db,'O-P-0010-C0018-death-lead').evidence_status,'LEAD');assert.ok(!personView(db,'P-0010').events.some(e=>e.event_type==='death'&&e.disposition==='accepted'));
 assert.equal(readCurrent(db,'E-confirmation-P-0047').event_type,'confirmation');assert.equal(readCurrent(db,'E-divorce-P-0047').event_type,'divorce');assert.match(readCurrent(db,'E-divorce-P-0047').caveat,/inte avgjort/);
 assert.equal(verifyDB(db).ok,true);
 const exported=exportData(db),digest=sha(canonical(exported));restore(exported,path.join(dir,'restore.sqlite'));const restored=openDB(path.join(dir,'restore.sqlite'));try{assert.equal(sha(canonical(exportData(restored))),digest);}finally{restored.close();}
});
