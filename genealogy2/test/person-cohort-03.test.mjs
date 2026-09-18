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

test('tredje personkohorten bevarar rättelser, kandidatgränser och källomfång efter faktisk införsel',async t=> {
 const reviews=['a','b','c','d'].flatMap(s=>read(`migration/persons-03-${s}.json`));
 assert.equal(reviews.length,50,'Kohorten ska vara komplett före verifiering.');
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-person-cohort03-'));
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
 for(const operation of ['T-0652-source-lulea-v1','T-0652-persons-01-v1','T-0653-persons-02-v1','T-0653-review-v1']) {
  applyOperation(db,read(`operations/${operation}.json`));
 }
 const request=buildPersons(db,reviews,{group:'persons-03'});
 applyOperation(db,request);

 const current=id=>{const value=readCurrent(db,id);assert.ok(value,`Saknat objekt: ${id}`);return value;};
 const value=id=>JSON.parse(current(id).value_json);
 const date=id=>JSON.parse(current(id).date_json);
 const participants=event=>db.prepare('SELECT p.* FROM current_revision r JOIN participation p ON p.revision_id=r.id WHERE p.event_id=?').all(event);
 const supports=id=>db.prepare("SELECT r.object_id FROM dependency d JOIN revision r ON r.id=d.basis_revision_id WHERE d.revision_id=? AND d.role='supports' ORDER BY r.object_id").all(current(id).revision_id).map(r=>r.object_id);
 const acceptedParents=child=>db.prepare("SELECT * FROM current_relation WHERE to_person=? AND relation_type='parent' AND disposition='accepted'").all(child);
 const decision=id=>{
  const result=inspect(db,id),units=result.legacyUnits.filter(u=>!u.historical);
  assert.equal(units.length,1,`Förväntar en aktuell A-rad för ${id}`);
  const found=result.conversionDecisions.find(d=>d.unit_id===units[0].id);
  assert.ok(found,`Saknat utfall för ${id}`);return found;
 };

 await t.test('senare kolumnprövning av C0123 ger tre gemensamma lysningar, ingen läst vigseldag',()=> {
  const days=['1826-09-24','1826-10-01','1826-10-08'];
  const ids=days.map(day=>`E-banns-P-0102-P-0103-${day}`);
  assert.deepEqual(value('O-P-0102-banns').banns,days);
  assert.equal(value('O-P-0102-banns').marriage_date,null);
  assert.equal(current('R-f5e92a8dfe87cc8d7d17be07').record_type,'banns_entry');
  for(const [i,id] of ids.entries()) {
   assert.equal(current(id).event_type,'banns');
   assert.equal(date(id).precision,'exact');assert.equal(date(id).value,days[i]);
   assert.deepEqual(participants(id).map(p=>p.person_id).sort(),['P-0102','P-0103']);
  }
  for(const who of ['P-0102','P-0103']) {
   const events=personView(db,who).events;
   assert.deepEqual(events.filter(e=>e.event_type==='banns').map(e=>e.event_id).sort(),ids);
   assert.equal(events.filter(e=>e.event_type==='marriage'&&JSON.parse(e.date_json).precision!=='unknown').length,0,
    'En lysningsdag får inte samtidigt bli personens säkra vigseldag.');
  }
  const spouse=current('REL-spouse-P-0102-P-0103');
  assert.equal(spouse.disposition,'accepted');assert.equal(JSON.parse(spouse.date_json).precision,'unknown');
 });

 await t.test('C0833:s födelsebarn och föräldrar är bevarade utan säker brygga till vuxne P0123',()=> {
  const identity=current('ID-M-C0833-Johan-Petter-Urbom-P-0123');
  assert.equal(identity.decision,'candidate');assert.equal(identity.disposition,'candidate');
  const child='M-C0833-Johan-Petter-Urbom';
  for(const [event,day] of [['E-birth-C0833-Johan-Petter','1818-06-03'],['E-baptism-C0833-Johan-Petter','1818-06-07']]) {
   assert.equal(current(event).disposition,'accepted');assert.equal(date(event).value,day);
   const principal=participants(event).filter(p=>p.role==='principal');
   assert.equal(principal.length,1);assert.equal(principal[0].mention_id,child);assert.equal(principal[0].person_id,null);
   assert.ok(!personView(db,'P-0123').events.some(e=>e.event_id===event),
    'Säkra händelser för källbarnet får inte visas som den vuxne kandidatens egna händelser.');
  }
  const parents=participants('E-baptism-C0833-Johan-Petter').filter(p=>['father','mother'].includes(p.role));
  assert.deepEqual(parents.map(p=>[p.role,p.person_id,p.mention_id]).sort(),[
   ['father','P-0264','M-C0833-Lorentz-Urbom'],['mother','P-0265','M-C0833-Anna-Maja-Eriksdotter']
  ]);
  assert.equal(acceptedParents('P-0123').length,0,'Barnets källföräldrar får inte bli vuxenmannens accepterade föräldrar.');
 });

 await t.test('Carolina har egen bokförd utflyttning 1857 och följer inte automatiskt familjen 1859',()=> {
  const own='E-registered_departure-P-0109',v=personView(db,'P-0109');
  assert.equal(current(own).event_type,'registered_departure');
  assert.equal(date(own).precision,'year');assert.equal(date(own).value,'1857');
  assert.equal(date(own).literal,'57, Rofhult[?]');assert.equal(current(own).place_id,null);
  assert.ok(v.events.some(e=>e.event_id===own&&e.participation.role==='principal'));
  for(const event of ['E-registered_departure-Urbom-Ajax-Husby1859','E-registered_arrival-Urbom-Ajax-Husby1859']) {
   const people=participants(event).map(p=>p.person_id);
   assert.ok(people.includes('P-0123'),'Familjens senare registrering ska finnas kvar.');
   assert.ok(!people.includes('P-0109'),'Carolina får inte följa familjen efter sin egen utflyttning.');
   assert.ok(!v.events.some(e=>e.event_id===event));
  }
  const d=decision('A-5975');assert.equal(d.state,'pending_interpretation');
  assert.ok(d.targets.includes(own));assert.ok(d.question.trim());
 });

 await t.test('familjesynteser binder sina källposter och moderstalet 38 förblir ett eget råfält',()=> {
  // C0276 och C0277 behövs båda för födelse 1858 och död 1861.
  const family='F-P-0109-family-P-0320',f=current(family);
  assert.equal(f.kind,'fact');assert.equal(f.subject_id,'REL-sibling-P-0109-P-0320');
  assert.equal(value(family).birth_reported,'1858-04-20');assert.equal(value(family).death_reported,'1861-11-16');
  assert.deepEqual(supports(family),['R-41d3a647542e67080e84564b','R-9b65e989ea7512c17bdf70ad']);
  assert.equal(readCurrent(db,'O-P-0109-family-P-0320'),null);
  for(const [person,birthRecord] of [
   ['P-0322','R-0c8b94af7848e998e025df31'],['P-0323','R-d39cc546d905bf3d22daf1ae'],
   ['P-0324','R-c8e60969837aa8c152edc940'],['P-0325','R-7569c3b3622049261725ea5f'],
   ['P-0327','R-48eb895ce62d7e56488f2d3a'],['P-0328','R-f126fa08207fb261ea957f11']
  ]) {
   const id=`F-P-0124-sibling-${person}`,r=current(id);
   assert.equal(r.kind,'fact');assert.equal(r.subject_id,`REL-sibling-P-0124-${person}`);
   assert.deepEqual(supports(id),[birthRecord,'R-831c03a0d3f7910b6f62089c'].sort(),
    'Barnpost och familjeuppslag ska stödja syntesen; den egna syskonkanten är inte ett oberoende belägg.');
   assert.equal(readCurrent(db,`O-P-0124-sibling-${person}`),null);
   for(const who of ['P-0124',person])assert.ok(personView(db,who).relations.some(rel=>rel.object_id===r.subject_id&&rel.qualifications.some(q=>q.object_id===id)));
  }
  const raw='O-P-0103-maternal-number38',observation=current(raw);
  assert.equal(observation.kind,'observation');assert.equal(observation.value_literal,'38');
  assert.equal(observation.record_id,'R-cb44c74498dc1121591aaa0a');
  assert.deepEqual(supports(raw),[observation.record_id]);
  assert.equal(value(raw).header_visible,false);
  assert.deepEqual(Object.keys(value(raw)).sort(),['header_visible','literal','neighbor_values','position','possible_interpretation'],
   'Det osäkert rubriksatta talet ska inte rymma födelseår från ett senare hushåll.');
  const comparison='F-P-0103-maternal_age-comparison';
  assert.equal(current(comparison).kind,'fact');
  assert.deepEqual(supports(comparison),[raw,'O-P-0103-parents-household']);
  assert.notEqual(current('O-P-0103-parents-household').record_id,observation.record_id);
  assert.equal(value(comparison).birth_year_reported_in_later_household,1753);
  assert.equal(value(comparison).superseded_reading,'1754[?]');
 });

 await t.test('C0128 bevarar dop 8 oktober, Stina Cajsa och en annan rå moder utan P0126-moderskant',()=> {
  assert.deepEqual(db.prepare("SELECT r.object_id FROM current_revision r JOIN participation p ON p.revision_id=r.id WHERE r.operation_id=? AND p.role='baptism_witness'").all(request.id),[],
   'Nya dopvittnen använder den gemensamma rollen witness; äldre kohorters roller omprövas separat.');
  const event='E-baptism-P-0167';
  assert.equal(current(event).event_type,'baptism');assert.equal(date(event).value,'1848-10-08');
  assert.equal(value('O-P-0125-child1848').birth,'1848-10-06');
  assert.equal(value('O-P-0125-child1848').baptism,'1848-10-08');
  const witness=current('M-C0128-witness-Stina');
  assert.equal(witness.name_literal,'Stina Cajsa Ersdr');assert.equal(witness.role_literal,'Dotter');
  assert.equal(participants(event).filter(p=>p.person_id==='P-0190'&&p.mention_id===witness.object_id&&p.role==='witness').length,1);
  const mother=current('M-C0128-Brita-Stina-Jansdotter');
  assert.equal(mother.name_literal,'Brita Stina Jansdotter[?]');
  const motherParticipation=participants(event).filter(p=>p.role==='mother');
  assert.equal(motherParticipation.length,1);assert.equal(motherParticipation[0].mention_id,mother.object_id);
  assert.equal(motherParticipation[0].person_id,null);
  assert.equal(db.prepare("SELECT count(*) n FROM current_revision r JOIN identity i ON i.revision_id=r.id WHERE i.mention_id=? AND i.person_id='P-0126' AND i.decision='accepted'").get(mother.object_id).n,0);
  assert.equal(current('Q-P-0167-mother-C0128').outcome,'open');
  assert.ok(acceptedParents('P-0167').some(r=>r.from_person==='P-0125'));
  for(const child of ['P-0167','P-0168'])assert.ok(!acceptedParents(child).some(r=>r.from_person==='P-0126'),
   'Sonrollen i hushållet är bevarad utan att moderns identitet avgörs genom radföljden.');
  assert.equal(value('F-P-0126-household_son_P-0167-curated').biological_mother_established,false);
 });

 await t.test('P0125:s avförda sökning i 1822 får ingen negativ verkan för födelsen 1820',()=> {
  const assessment='ASSESS-P-0125-birth-search-wrong-year',a=current(assessment);
  assert.equal(a.kind,'assessment');assert.equal(a.outcome,'invalid_for_1820');
  assert.equal(decision('A-0723').state,'preserved_history');
  assert.ok(decision('A-0723').targets.includes(assessment));
  assert.equal(decision('A-3803').state,'mapped_complete');
  assert.ok(decision('A-3803').targets.includes(assessment));
  assert.equal(date('E-birth-P-0125').value,'1820-08-21','Rättat sökomfång omväljer inte den uppgivna födelsen.');
  const searches=personView(db,'P-0125').searches;
  assert.ok(!searches.some(s=>s.outcome==='negative'&&s.source_id==='S-0100'),
   'Den fellokaliserade födelsebokssökningen får inte återuppstå som ett negativt native-sökresultat.');
  // Det verkliga, avgränsade negativa dödboksomfånget ska samtidigt finnas kvar.
  const death=searches.find(s=>s.object_id==='SEARCH-P-0125-death1867-1873');
  assert.ok(death);assert.equal(death.outcome,'negative');assert.equal(death.source_id,'S-0430');
  const bounds=JSON.parse(death.scope_json).bounds;
  assert.equal(bounds.fromYear,1867);assert.equal(bounds.toYear,1873);
 });
 assert.equal(verifyDB(db).ok,true);
});
