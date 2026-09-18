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

test('fjärde personkohorten bevarar rättelser, kandidatgränser och källomfång efter faktisk införsel',async t=> {
 const reviews=['a','b','c','d'].flatMap(s=>read(`migration/persons-04-${s}.json`));
 assert.equal(reviews.length,50,'Kohorten ska vara komplett före verifiering.');
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-person-cohort04-'));
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
 for(const operation of ['T-0652-source-lulea-v1','T-0652-persons-01-v1','T-0653-persons-02-v1','T-0653-review-v1','T-0654-persons-03-v1','T-0654-review-v1']) {
  applyOperation(db,read(`operations/${operation}.json`));
 }
 const request=buildPersons(db,reviews,{group:'persons-04'});
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

 await t.test('Rödåbarnens olika radmarkeringar blir inte påhittade livshändelser',()=> {
  const arrival=current('E-arrival-P-0152-1861');assert.equal(arrival.event_type,'registered_arrival');assert.equal(date(arrival.object_id).value,'1861-12-02');
  assert.equal(value('F-P-0152-migration-arrival1861').later_crossing_date,null);
  assert.deepEqual(value('F-P-0151-church_participation-Roda483').year_marks,[1861]);
  assert.equal(value('F-P-0153-source_reference-internal_transfer').parish_departure,false);
  assert.ok(!personView(db,'P-0153').events.some(e=>e.event_type==='registered_departure'));
  assert.equal(value('O-P-0155-C0111-own_limits').diagonal_ink_line,'sidmärke, ingen egen notering');
  assert.equal(date('E-birth-P-0156').precision,'year');assert.equal(date('E-birth-P-0156').value,'1852');
  assert.equal(value('F-P-0156-birth_registration-reported').day_reading_reserved,true);
  assert.equal(value('O-P-0156-C0111-own_limits').older_birth_number_crossed,true);
  assert.equal(decision('A-0648').state,'preserved_history');assert.equal(decision('A-7846').state,'pending_interpretation');
 });
 await t.test('Carl Petters vuxennamn och sonfamilj bevaras utan nya säkra barnidentiteter',()=> {
  assert.ok(value('F-P-0153-name_form-Roda483').attested.includes('Carl Petter Andersson'));
  const family=value('F-P-0153-household_membership-own_family');assert.equal(family.wife.reported_birth,'1841-01-16');assert.equal(family.wife.from_folio,536);
  assert.equal(family.children[1].reported_birth_literal,'1865-03-27[?]');assert.equal(family.children[1].day_reserved,true);
  const marriage='E-marriage-P-0153-Ulla-Carolina-1863';assert.equal(date(marriage).precision,'year');assert.equal(date(marriage).value,'1863');
  const wife=participants(marriage).find(x=>x.role==='spouse');assert.ok(wife);assert.equal(wife.person_id,null);assert.equal(wife.mention_id,family.wife.mention);
 });
 await t.test('Maria Johannas identitetskandidat behåller rätt ort, full dag och olöst slutsats',()=> {
  const f=value('F-P-0155-identity_boundary-maid1870');assert.equal(f.candidate_person,'P-0084');assert.match(f.candidate_context,/Buberget/);assert.ok(f.matching.includes('1849-08-02'));assert.equal(f.same_person_established,false);
  assert.equal(current('F-P-0155-identity_boundary-maid1870').disposition,'candidate');
  assert.ok(supports('F-P-0155-identity_boundary-maid1870').includes('O-P-0084-hfl-servant'));
  assert.equal(db.prepare("SELECT count(*) n FROM current_revision r JOIN identity_resolution i ON i.revision_id=r.id WHERE i.decision='same_person' AND (i.person_a='P-0155' OR i.person_b='P-0155')").get().n,0);
 });
 await t.test('Hans dop får fyra originalvittnen och ingen summering med den motsagda privatlistan',()=> {
  const own='E-baptism-P-0158';assert.equal(date(own).value,'1800-09-28');assert.equal(date('E-birth-P-0158').value,'1800-09-23');
  assert.deepEqual(participants(own).filter(x=>x.role==='witness').map(x=>x.person_id).sort(),['P-0183','P-0184','P-0185','P-0186']);
  const conflict=value('F-E-baptism-P-0158-witness_conflict');assert.equal(conflict.conflicting_secondary_mentions.length,3);assert.equal(conflict.merge_lists,false);
  assert.equal(current('E-birth-P-0158').place_role,'recording_parish');assert.equal(value('O-P-0158-C0129-birth').family_place,'Åkullsjön');
  assert.equal(current('E-death-P-0158').disposition,'candidate');
  for(let n=184;n<=186;n++) {
   const rows=db.prepare("SELECT u.id,u.parsed_json FROM unit u JOIN legacy_entity e ON e.document_path=u.document_path WHERE e.id='P-0158' AND e.kind='person' AND u.kind='relation_row'").all();
   const name={184:'Anna Johansdotter',185:'Abram Abramsson',186:'Brita Stina Abramsdotter'}[n];
   const row=rows.find(r=>JSON.parse(r.parsed_json).cells[0]===name);assert.ok(row);
   assert.ok(db.prepare('SELECT 1 FROM current_unit_target WHERE unit_id=? AND target_id=?').get(row.id,`O-P-0${n}-C0129-witness-fields`),'Vittnets ort/ditto ska finnas i hela relationsradens aktuella mål.');
  }
 });
 await t.test('privata barnuppgifter skapar inga accepterade ankanter och namnarna förblir skilda',()=> {
  for(let n=197;n<=206;n++){const child='P-'+String(n).padStart(4,'0');for(const parent of ['P-0158','P-0159'])assert.equal(current('REL-parent-'+parent+'-'+child).disposition,'candidate');assert.ok(!acceptedParents(child).some(r=>['P-0158','P-0159'].includes(r.from_person)));}
  assert.deepEqual(acceptedParents('P-0095').map(r=>r.from_person).sort(),['P-0158','P-0159']);
  const group=value('F-REL-spouse-P-0158-P-0159-secondary-children');assert.equal(group.reported_count,11);assert.deepEqual(group.distinct_namesakes,['P-0205','P-0095']);
  assert.equal(current('F-REL-parent-P-0158-P-0198-secondary-family').kind,'fact');assert.equal(value('F-REL-parent-P-0158-P-0198-secondary-family').death_place,'Olsiden, Bygdeå (AC)');
  const titles=value('F-REL-parent-P-0158-P-0197-secondary-family').occupation_rows;
  assert.match(titles.find(r=>r.title==='Krononybyggare').place,/Sjöbäck/);assert.equal(titles.find(r=>r.title==='Hemmansägare').place,null);
  for(const n of [199,201,202,203,204]) {
   const f=value(`F-REL-parent-P-0158-P-0${n}-secondary-family`);
   assert.equal(f.birth_place,null);assert.equal(f.reported_family_place,'Åkullsjön');assert.equal(f.legacy_parent_dossier_birth_place,'Åkullsjön');
  }
 });
 await t.test('Bettnafallet bevarar rättad dagläsning utan påhittat noll eller säker biologisk mor',()=> {
  assert.equal(date('E-birth-P-0168').precision,'year');assert.equal(date('E-birth-P-0168').value,'1852');
  assert.equal(value('F-P-0168-reported_birth-household').day_literal,'1/11[?]');
  assert.equal(value('F-P-0168-reported_birth-household').superseded_is_source_variant,false);
  assert.equal(current('ASSESS-P-0168-Bettna-old-search').outcome,'unsubstantiated_prior_search');
  assert.ok(!personView(db,'P-0168').searches.some(s=>s.source_id==='S-0116'&&s.outcome==='negative'));
  const mother=value('F-P-0167-identity_assessment-mother-conflict');assert.equal(mother.biological_mother_P0126_established,false);assert.equal(mother.birth_mother_age_raw,27);assert.equal(mother.calculated_completed_age_at1848,18);
  assert.ok(!acceptedParents('P-0167').some(r=>r.from_person==='P-0126'));
 });
 await t.test('Anna Stinas olösta födelse, fysiska volymlucka och verkliga noll har skilda omfång',()=> {
  assert.equal(acceptedParents('P-0159').length,0);assert.equal(current('P-0159').disposition,'accepted');
  assert.equal(current('E-birth-P-0159').disposition,'candidate');assert.equal(current('E-death-P-0159').disposition,'candidate');
  const age=value('F-P-0159-reported_age-daughter1840');assert.equal(age.years,45);assert.equal(age.secondary_date_confirmed,false);assert.deepEqual(age.conditional_birth_interval,{from:'1794-10-18',to:'1795-10-17'});
  const gap=value('F-S0102-physical-gap-P0159-context');assert.equal(gap.cause,'fysiskt förlorade blad');assert.equal(gap.person_birth_parish_established,false);
  const search=current('SEARCH-P-0159-Umea-C4-1794-12');assert.equal(search.outcome,'negative');assert.equal(search.source_id,'S-0104');assert.equal(JSON.parse(search.scope_json).bounds.image,178);
  assert.ok(!personView(db,'P-0159').searches.some(s=>s.source_id==='S-0102'&&s.outcome==='negative'));
  assert.equal(value('F-S0103-register-periods-P0159-context').historical_Ytteratrask_jurisdiction_established,false);
  assert.equal(value('F-P-0159-source_dependence-private_pages').independent_information_paths,1);
 });
 await t.test('en senare komplett vittneslista upphäver den gamla negativa premissen utan att bevisa släktskap',()=> {
  assert.equal(current('ASSESS-P-0161-witness-premise-correction').outcome,'superseded_negative_premise');
  assert.equal(decision('A-7371').state,'preserved_history');
  for(const id of ['F-P-0160-kinship_candidate-P-0173','F-P-0161-kinship_candidate-P-0175'])assert.equal(current(id).disposition,'candidate');
  for(const pair of [['P-0160','P-0173'],['P-0161','P-0175']])assert.ok(!db.prepare("SELECT * FROM current_relation WHERE relation_type='sibling' AND disposition='accepted' AND from_person=? AND to_person=?").get(...pair));
  for(const aid of ['A-7360','A-7370'])for(let n=172;n<=175;n++)assert.ok(decision(aid).targets.includes('M-C0124-P-0'+n));
 });
 assert.equal(verifyDB(db).ok,true);
});
