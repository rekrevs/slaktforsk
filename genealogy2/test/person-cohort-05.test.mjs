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

test('femte personkohorten bevarar rättelser, kandidatgränser och källomfång efter faktisk införsel',async t=> {
 const reviews=['a','b','c','d'].flatMap(s=>read(`migration/persons-05-${s}.json`));
 assert.equal(reviews.length,50,'Kohorten ska vara komplett före verifiering.');
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-person-cohort05-'));
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
 for(const operation of ['T-0652-source-lulea-v1','T-0652-persons-01-v1','T-0653-persons-02-v1','T-0653-review-v1','T-0654-persons-03-v1','T-0654-review-v1','T-0655-persons-04-v1','T-0655-review-v1']) {
  applyOperation(db,read(`operations/${operation}.json`));
 }
 const request=buildPersons(db,reviews,{group:'persons-05'});
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

 await t.test('privatlistans sex barn behåller kandidatgränser och individuella ort-/yrkesfält',()=> {
  for(let n=201;n<=206;n++) {
   const id='P-0'+n;assert.equal(current(id).disposition,'candidate');assert.equal(acceptedParents(id).length,0);
   assert.equal(current('E-birth-'+id).disposition,'candidate');assert.equal(current('E-death-'+id).disposition,'candidate');
   for(const parent of ['P-0158','P-0159'])assert.equal(current(`REL-parent-${parent}-${id}`).disposition,'candidate');
  }
  for(let n=201;n<=204;n++)assert.equal(value(`F-P-0${n}-event_place-birth-secondary`).place,null);
  assert.equal(value('F-P-0203-occupation-secondary').place,'Åkullsjön nr 1');
  assert.equal(value('F-P-0204-civic_role-secondary').title,'nämndeman');assert.equal(value('F-P-0204-civic_role-secondary').period,null);
  assert.equal(value('F-P-0205-event_place-death-secondary').place,'Åkullsjön, Bygdeå (AC)');
  assert.equal(value('F-P-0205-identity_boundary-P0095').namesake_explanation_proven,false);
  assert.equal(date('E-birth-P-0205').value,'1834-08-11');assert.equal(date('E-birth-P-0095').value,'1840-10-17');
  assert.equal(value('F-P-0206-source_comparison-birth_place').chosen_birth_place,null);
  assert.equal(value('F-P-0206-source_comparison-two_views').independent_information_paths,1);
  assert.equal(value('F-P-0206-source_comparison-two_views').unmarried_or_childless_established,false);
  assert.equal(value('F-P-0206-event_place-death-secondary').Sjoback_specified,false);
  assert.equal(value('F-P-0206-occupation-secondary').tenure_or_ownership,null);
 });
 await t.test('avvisade dopanspråk avvecklar forskning men raderar inte möjliga människor',()=> {
  const part=participants('E-baptism-P-0158');
  for(let n=207;n<=209;n++) {
   const id='P-0'+n;assert.equal(current(id).disposition,'candidate');assert.equal(current(id).legacy_state,'active');
   assert.equal(current(`F-${id}-baptism_witness_claim-rejected`).disposition,'rejected');
   assert.equal(value(`F-${id}-baptism_witness_claim-rejected`).person_existence_rejected,false);
   assert.ok(!part.some(p=>p.person_id===id));
   const research=personView(db,id).research;assert.ok(research.questions.length>0);
   assert.ok(research.questions.every(q=>q.active===false&&q.disposition==='retired'));
   assert.ok(research.paths.every(q=>q.disposition==='retired'));
  }
  assert.equal(current('REL-spouse-P-0207-P-0208').disposition,'candidate');
  assert.equal(value('F-P-0209-identity_boundary-Brita-Stina').same_person_supported,false);
  assert.equal(value('F-P-0207-civic_role-secondary').place,null);
 });
 await t.test('Kristinas ägarbekräftade kärnfamilj och senare granskningsbeslut hålls samman',()=> {
  assert.equal(date('E-birth-P-0210').value,'1964-05-29');assert.equal(current('E-birth-P-0210').evidence_status,'OWNER_CONFIRMED');
  assert.equal(current('E-birth-P-0210').place_id,null);
  assert.deepEqual(acceptedParents('P-0210').map(r=>r.from_person).sort(),['P-0211','P-0212']);
  for(const id of ['P-0269','P-0270'])assert.equal(current(`REL-parent-P-0210-${id}`).evidence_status,'OWNER_CONFIRMED');
  const report=value('O-P-0210-C0225-grandparents');assert.equal(report.paternal_grandfather.birth_year,1903);assert.equal(report.paternal_grandmother.death_date.value,'1991-09-18');assert.equal(report.maternal_grandmother_named,false);
  assert.ok(!db.prepare("SELECT * FROM current_relation WHERE from_person='P-0239' AND to_person='P-0210' AND relation_type='parent'").get());
  assert.match(current('ASSESSMENT-P-0210').body,/Kontraktsgranskning: `UNDERKÄND`/);
  assert.ok(personView(db,'P-0210').interpretationQuestions.some(q=>q.question.includes('PCD2026-09-09-029')));
  assert.equal(current('M-P-0210-C0252-own').name_literal,'Kristina Elisabeth Petronella');
 });
 await t.test('Evys födelseby, familjehemvist och separata söknoll behåller olika räckvidd',()=> {
  const birth=value('F-P-0211-event_place-birth');assert.equal(birth.family_reported_birth_village,'Storbränna');assert.equal(birth.SCB_home,'Storbränna');assert.equal(birth.register_parish,'Sättna');assert.equal(birth.physical_birth_building,null);
  assert.equal(value('O-P-0211-C0240-child').father_occupation_secure,false);
  assert.equal(current('M-P-0211-C0239-own').name_literal,'evy');
  const ss=personView(db,'P-0211').searches.filter(s=>s.object_id.startsWith('SEARCH-P-0211-C0141-'));assert.equal(ss.length,3);assert.ok(ss.every(s=>s.outcome==='negative'));
  assert.equal(JSON.parse(current('SEARCH-P-0211-C0141-index').scope_json).bounds.coverage,'ofullständig och äldre lokalt producerad');
  assert.match(current('ASSESSMENT-P-0211').body,/Identitetsgranskning: `UNDERKÄND`/);
  assert.equal(date('E-marriage-P-0211-P-0212-1962').precision,'year');assert.equal(current('E-marriage-P-0211-P-0212-1962').place_id,null);
  assert.equal(value('O-P-0211-C0901-spouse').meeting_place,'Ibra radio, Stockholm');assert.equal(value('O-P-0211-C0901-spouse').marriage_place,null);
  assert.deepEqual(value('F-P-0241-reported_children-owner-C0238').ordered_names,['Willy','Elsy','Henry','Sally','Berit','Evy']);
 });
 await t.test('Gunnars källnamn och senare rättelser blir inga nya identiteter eller påhittade orter',()=> {
  assert.equal(current('P-0212').sex,'male');assert.equal(current('M-P-0212-C0902-child').name_literal,'');assert.equal(current('M-P-0212-C0902-child').role_literal,'Odöpt gossebarn');
  assert.equal(date('E-birth-P-0212').value,'1933-03-26');assert.equal(value('F-P-0212-event_place-birth').register_parish,'Engelbrekt');
  assert.equal(date('E-death-P-0212').value,'2017-09-22');assert.equal(value('F-P-0212-event_place-death').physical_place,null);assert.equal(value('F-P-0212-event_place-death').reported_home,'Falköping');
  assert.equal(value('F-P-0212-name_form-source_comparison').order_conflict_unresolved,true);assert.equal(value('F-P-0212-name_form-source_comparison').church_grave_independence_established,false);
  assert.equal(current('ID-P-0212-C0228-athlete').disposition,'candidate');
  assert.equal(value('O-P-0212-C0228-athlete').birth_year,1933);assert.equal(value('O-P-0212-C0228-athlete').club_or_competition_place,'Lidingö');
  assert.equal(date('E-death-P-0239').value,'1944-08-14');assert.equal(value('F-P-0239-child_context-P-0309').posthumous_interval_days,17);
  assert.equal(current('REL-parent-P-0287-P-0239').evidence_status,'OWNER_CONFIRMED');
  assert.equal(value('F-P-0212-source_reference-Lidingo1951').to_folio,1719);assert.equal(value('F-P-0212-source_reference-Lidingo1951').own_column9_unread,true);
  assert.equal(value('F-P-0212-meeting-future-spouse').employment_at_Ibra_established,false);
  assert.equal(value('F-P-0212-event_place-Floby').origin,null);assert.equal(value('F-P-0212-event_place-Floby').after_person_birth,'P-0210');
  assert.equal(current('F-P-0212-athletic_activity-candidate1948').disposition,'candidate');
  assert.equal(decision('A-3384').state,'pending_interpretation');assert.match(decision('A-3384').question,/odaterade adresser/);
  assert.equal(value('O-P-0212-C0268-full-siblings').full_siblings,true);
  assert.notEqual(current('O-P-0212-C0268-full-siblings').record_id,current('O-P-0212-C0268-own').record_id);
  assert.ok(decision('A-4800').targets.includes('REL-parent-P-0211-P-0210'));
 });
 await t.test('Maria Sofias nöddop, dopbekräftelse och moderns kyrktagning har rätt subjekt',()=> {
  assert.equal(current('P-0213').sex,'female');assert.equal(value('F-P-0213-name_form-corrected').Elli_is_attested_name,false);
  assert.equal(date('E-baptism-P-0213').value,'1883-07-09');assert.equal(date('E-other-P-0213-baptism-confirmation1883').value,'1883-07-12');assert.equal(date('E-other-P-0134-churching1883').value,'1883-08-12');
  assert.ok(!personView(db,'P-0213').events.some(e=>e.object_id==='E-other-P-0134-churching1883'));
  const raw=value('O-P-0213-C0768-child');assert.deepEqual(raw.mother_age_column_literals,['32','31']);assert.equal(raw.age_values_role_unresolved,true);assert.equal(raw.examined_midwife_column,'Ev./Ex.[?]');
  assert.equal(raw.marriage_duration_years,7);assert.equal(value('F-P-0213-baptism_context-emergency1883').diagnosis,null);
  const ps=participants('E-baptism-P-0213');assert.deepEqual(ps.filter(p=>p.role==='witness').map(p=>p.person_id).sort(),['P-0133','P-0134']);
  assert.equal(ps.find(p=>p.role==='emergency_baptizer').person_id,null);
  const place=value('F-P-0213-event_place-departure1899');assert.equal(place.to,'Vadsbro');assert.equal(place.receiver_read,false);assert.equal(place.post,115);
  const ss=personView(db,'P-0213').searches.filter(s=>s.outcome==='negative');assert.equal(ss.length,4);assert.ok(ss.every(s=>JSON.parse(s.scope_json).bounds));
  assert.deepEqual(JSON.parse(current('SEARCH-P-0213-Lilla-arrival1899').scope_json).bounds.posts,[1,150]);
  assert.deepEqual(JSON.parse(current('SEARCH-P-0213-Lilla-departure1900').scope_json).bounds.posts,[1,149]);
  assert.equal(JSON.parse(current('SEARCH-P-0213-Lilla-census1900').scope_json).bounds.image_count,55);
  assert.deepEqual(JSON.parse(current('SEARCH-P-0213-Stora-arrival1899').scope_json).bounds.posts,[1,126]);
  assert.equal(current('SEARCH-P-0213-C0790-ALTCHA').outcome,'access_problem');
  assert.ok(!Object.hasOwn(value('O-P-0213-C0401-child'),'unrelated_family2'));
 });
 await t.test('Årdalahushållens radägare och identitetskandidater behåller sina gränser',()=> {
  assert.equal(current('P-0214').disposition,'accepted');
  assert.equal(date('E-birth-P-0214').value,'1819-08-07');
  assert.equal(current('ID-M-C0160-Lars-Eric').disposition,'candidate');
  assert.equal(value('O-P-0214-C0160-birth-candidate').birth,'1819-08-09');
  assert.equal(acceptedParents('P-0214').length,0);
  assert.equal(value('F-P-0214-residence-bounded-chain').continuous_chain_established,false);
  assert.deepEqual(JSON.parse(current('SEARCH-P-0214-Ardala-arrivals1844-1847').scope_json).bounds.years,[1844,1845,1846,1847]);
  assert.equal(value('F-P-0221-source_assessment-Erik-versus-Anna-fields').attribution_to_Erik_verified,false);
  assert.equal(JSON.parse(current('SEARCH-P-0221-first-marriage1797-1809').scope_json).bounds.to_year,1809);
  assert.equal(date('E-birth-P-0225').value,'1804-04-16');
  assert.equal(value('F-P-0225-household_membership-Sannerby').biological_father,null);
  assert.equal(value('F-P-0225-household_membership-Sannerby').biological_mother,null);
  assert.equal(value('F-P-0225-source_assessment-church-marks-limits').confirmation_date,null);
 });
 await t.test('Risvattnets ålderskonflikt och dödsnotis behandlas efter skilda källgrunder',()=> {
  assert.equal(current('P-0231').disposition,'accepted');
  assert.equal(current('ID-M-C0199-Magdalena').disposition,'candidate');
  assert.equal(acceptedParents('P-0231').length,0);
  assert.equal(value('F-P-0231-birth_age_conflict').mother_age_report_1835,27);
  assert.equal(value('F-P-0231-birth_age_conflict').computed_age_from_main_date,36);
  assert.equal(decision('A-1396').state,'pending_interpretation');
  assert.equal(current('M-P-0050-C1045-witness1').role_literal,'');
  assert.equal(current('M-P-0050-C1045-witness2').role_literal,'Bonden');
  assert.equal(date('E-death-P-0237').value,'1843-02-11');
  assert.equal(date('E-death-P-0237').precision,'circa');
  assert.equal(value('O-P-0237-C0197-child').death_literal,'† d. 11/2');
  assert.match(current('SEARCH-P-0237-AI9a-s85').body,/bevisar inte självt död/);
  const revised=current('F-P-0050-relation_context-P-0237');
  assert.equal(revised.version,2);assert.doesNotMatch(revised.caveat,/orsaken.*inte.*avgjord/);
 });
 await t.test('Johanna Charlottas existens består när forskningen avvecklas och rånamn rättas',()=> {
  assert.equal(current('P-0238').disposition,'accepted');assert.equal(current('P-0238').legacy_state,'retired');
  assert.equal(value('F-P-0238-birth_date_conflict').resolution,'unresolved');
  assert.equal(current('M-C0208-Charlotta-Johanna').name_literal,'Charlotta Johanna');
  assert.equal(current('M-C0208-Charlotta-Johanna').role_literal,'');
  for(const name of ['A-Strom','Jacob-Johansson','Johan-Gustafsson']) {
   const m=current(`M-C0208-${name}-wife`);assert.equal(m.version,2);assert.equal(m.name_literal,'');assert.equal(m.role_literal,'hustru');
  }
  assert.equal(JSON.parse(current('SEARCH-P-0238-Savar-C2-deaths1856').scope_json).bounds.year,1856);
  assert.equal(date('E-death-P-0238').value,'1857-07-31');
  assert.ok(personView(db,'P-0238').research.questions.every(q=>q.active===false));
  assert.equal(value('F-P-0238-family_identity_boundary').brother_is_P0028,false);
 });
 await t.test('Henrikssonfamiljens källposter, barnantal och personliga dopnoter hålls isär',()=> {
  const arrival='E-registered_arrival-Henriksson-family-arrival1936';
  assert.equal(date(arrival).value,'1936-11-14');
  assert.deepEqual(participants(arrival).map(p=>p.person_id).sort(),['P-0241','P-0246','P-0258','P-0259','P-0260','P-0261','P-0262']);
  assert.notEqual(current('O-P-0241-C0935-own').record_id,current('O-P-0241-C0935-own-arr1936').record_id);
  assert.notEqual(current('O-P-0241-C0935-own').mention_id,current('O-P-0241-C0935-own-arr1936').mention_id);
  assert.equal(value('O-P-0246-C0246-own').note,'Dop vägradt.');
  assert.ok(!Object.hasOwn(value('O-P-0246-C0247-own'),'note'));
  assert.ok(!Object.hasOwn(value('O-P-0241-C0245-own'),'baptism'));
  assert.notEqual(value('O-P-0246-C0925-own').marriage,'1924-09-13');
  assert.doesNotMatch(value('O-P-0246-C0933-own').home,/Storgat/);
  assert.match(current('O-P-0246-C0247-own').caveat,/samma grundregistrering/);
  assert.equal(date('E-marriage-P-0241-P-0246-1924').value,'1924-09-13');
  assert.equal(date('E-registered_arrival-Henriksson-family-book1924').value,'1924-10-15');
  assert.match(value('F-P-0246-religious_registration-bounded').limits,/inget bestämt samfund/);
  assert.match(current('ASSESSMENT-P-0246').body,/Identitetsgranskning: `UNDERKÄND`/);
 });
 assert.equal(verifyDB(db).ok,true);
});
