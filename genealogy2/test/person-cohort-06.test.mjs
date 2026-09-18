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

test('sjätte personkohorten bevarar rättelser, kandidatgränser och källomfång efter faktisk införsel',async t=> {
 const reviews=['a','b','c','d','e','f'].flatMap(s=>read(`migration/persons-06-${s}.json`));
 assert.equal(reviews.length,50,'Kohorten ska vara komplett före verifiering.');
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-person-cohort06-'));
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
 const originalAlvaReview=currentSnapshot('ASSESSMENT-P-0027');
 const originalAlvaStory=currentSnapshot('BIO-P-0027');
 function currentSnapshot(id){return readCurrent(db,id);}
 const request=buildPersons(db,reviews,{group:'persons-06'});
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

 await t.test('Stinas senare datumrättelse bevaras utan att decemberbarnet eller 1867 års piga blir hon',()=> {
  assert.equal(date('E-birth-P-0251').precision,'year');
  const readings=value('F-P-0251-birth_date_conflict-source-readings');
  assert.equal(readings.C0530_latest_day_fraction,'19/2');assert.equal(readings.selected_day,null);
  assert.equal(readings.candidate_identified,false);
  for(const e of ['E-birth-C1042-candidate','E-baptism-C1042-candidate','E-registered_departure-C0551-Stina1867']) {
   assert.ok(participants(e).length);assert.ok(participants(e).every(p=>p.person_id===null));
  }
  assert.equal(date('E-registered_departure-P-0251').value,'1871-11-11');
  assert.equal(current('SEARCH-P0251-census1870-ALTCHA').outcome,'access_problem');
  assert.equal(JSON.parse(current('SEARCH-P0251-census1870-reopened').scope_json).bounds.coverage_excludes,'Västernorrlands län');
  assert.equal(decision('A-2353').state,'pending_interpretation');
 });
 await t.test('Olivas ägartitel bevisar inte en överlåtelse och Erik har egna källposter för flytt och födelse',()=> {
  assert.equal(value('F-P-0252-household_title_comparison-1900-1910').conveyance_established,false);
  assert.equal(value('F-P-0252-household_title_comparison-1900-1910').father_later_known_death,'1916-01-22');
  assert.equal(value('F-P-0252-reported_civil_status-1910').directly_transcribed_for_own_row_in_C0242,false);
  assert.equal(decision('A-7895').state,'pending_interpretation');
  assert.equal(date('E-birth-P-0253').value,'1860-01-23');
  assert.equal(value('F-P-0253-birth_date_conflict-three-readings').dependent_SCB,true);
  assert.notEqual(current('O-P-0253-C0243-own').mention_id,current('O-P-0250-C0243-1900').mention_id);
  const death=value('F-P-0253-death_context-source-term');assert.equal(death.cause_literal,'Lunginflammation');
  assert.deepEqual(death.sons_ages_at_death,{'P-0241':9,'P-0248':3,'P-0249':1});
  assert.equal(value('F-P-0253-military_registration-number').service,null);
 });
 await t.test('Larssonfamiljens sena läsrättelser ändrar inte olästa fält till säkra slutsatser',()=> {
  assert.equal(current('P-0255').sex,null);
  assert.equal(date('E-death-P-0255').value,'1921-12-11');
  assert.equal(value('F-P-0255-death_date_conflict-4-versus11').household_reading,'1921-12-04');
  assert.equal(value('F-P-0255-birth_record_reading-fullpost').father_remaining_title,'T.');
  assert.equal(value('F-P-0255-religious_registration-bounded').lifelong_unconfirmed,null);
  assert.equal(value('F-P-0255-religious_registration-bounded').entire_household_unbaptized,false);
  assert.deepEqual(participants('E-marriage-P-0254-P-0255-1888').map(p=>p.person_id).sort(),['P-0254','P-0255']);
  assert.equal(current('P-0256').evidence_status,'TRANSCRIBED');
  assert.equal(value('F-P-0257-name_conflict-Kristina-Viktoria').chosen,null);
  const child=participants('E-birth-M-C0925-Ture-Attilio');
  assert.equal(child.find(p=>p.role==='principal').person_id,null);
  assert.equal(child.find(p=>p.role==='mother').person_id,'P-0257');
  assert.ok(!child.some(p=>p.role==='father'));
 });
 await t.test('Henrikssonbarnen delar rätt familjeflytt utan att ett senare barn deltar',()=> {
  const e='E-registered_arrival-Henriksson-family-arrival1936';
  assert.equal(date(e).value,'1936-11-14');
  assert.deepEqual(participants(e).map(p=>p.person_id).sort(),['P-0241','P-0246','P-0258','P-0259','P-0260','P-0261','P-0262']);
  assert.equal(date('E-birth-P-0258').value,'1922-01-17');
  assert.equal(date('E-birth-P-0262').value,'1933-08-19');
 });
 await t.test('Urbom och Ajax behåller olösta ursprung, villkorad ålder och rättade barnposter',()=> {
  assert.equal(current('REL-parent-P-0264-P-0123').disposition,'candidate');
  assert.equal(current('REL-parent-P-0265-P-0123').disposition,'candidate');
  assert.equal(current('REL-spouse-P-0264-P-0265').disposition,'accepted');
  assert.equal(value('F-P-0264-source_assessment-unheaded28').father_age_from_original,null);
  assert.equal(value('F-P-0265-reported_birth_range-conditional28').chosen_year,null);
  assert.equal(value('F-P-0265-source_assessment-childbirth-survival').survival_independently_attested,false);
  assert.equal(current('ID-M-C0862-Peter-Magnus').disposition,'candidate');
  assert.equal(acceptedParents('P-0266').length,0);
  assert.equal(date('E-birth-P-0325').value,'1830-05-09');
  assert.equal(date('E-baptism-P-0325').value,'1830-05-10');
  assert.equal(value('F-P-0267-reported_age-seven-birth-posts').exact_two_year_intervals,false);
  assert.equal(current('SEARCH-P-0266-Motala1791').outcome,'inconclusive');
 });
 await t.test('Högsjös hushållsmedlemskap skapar inga nya föräldrar och civilståndskonflikten består',()=> {
  assert.equal(acceptedParents('P-0273').length,0);
  assert.ok(!acceptedParents('P-0274').some(p=>p.from_person==='P-0271'));
  assert.ok(acceptedParents('P-0274').some(p=>p.from_person==='P-0272'));
  assert.equal(date('E-birth-P-0272').value,'1844-12-04');
  assert.equal(value('F-P-0272-birth_date_conflict-4-vs7').later_reported,'1844-12-07');
  assert.equal(value('F-P-0271-household_membership-eight-listed').listed_count,8);
  assert.equal(value('F-P-0271-household_membership-eight-listed').lifetime_child_total,null);
  assert.equal(value('F-P-0271-civil_status_conflict-1906').remarriage_proven,false);
 });
 await t.test('Hökfamiljens rättade datum och postbundna uppgifter följer rätt person',()=> {
  assert.equal(date('E-death-P-0276').value,'1911-01-16');
  assert.equal(date('E-birth-P-0283').value,'1882-11-20');
  assert.equal(value('F-P-0279-birth-order-conflict').positionInExplicitKnownList,7);
  assert.equal(value('F-P-0279-birth-order-conflict').olderProjectOrdinal,9);
  assert.equal(date('E-registered_arrival-Hok-family-Hudiksvall1910').value,'1910-12-31');
  assert.equal(date('E-marriage-P-0282-Sara-Kristina1927').value,'1927-09-03');
  assert.equal(current('ID-M-C0260-P-0282-row6').person_id,current('ID-M-C0260-P-0282-row7').person_id);
  assert.notEqual(current('ID-M-C0260-P-0282-row6').mention_id,current('ID-M-C0260-P-0282-row7').mention_id);
  assert.equal(value('F-P-0282-wife-and-daughters').children[0].registeredArrival1930,'1930-09-20');
  assert.equal(value('F-P-0282-wife-and-daughters').sendingOrganization,null);
  assert.equal(current('ID-M-C0260-Gustaf-Hook-father').disposition,'candidate');
  assert.equal(current('F-P-0283-adult-family-candidate').disposition,'candidate');
  assert.equal(current('REL-sibling-P-0282-P-0370').evidence_status,'INFERRED');
 });
 await t.test('barnamodern blir inte Johannes egen mor och ägarfastställt faderskap består',()=> {
  assert.deepEqual(acceptedParents('P-0287').map(p=>p.from_person).sort(),['P-0336','P-0337']);
  assert.equal(current('REL-parent-P-0287-P-0239').disposition,'accepted');
  assert.equal(current('REL-parent-P-0287-P-0239').evidence_status,'OWNER_CONFIRMED');
  assert.equal(current('REL-parent-P-0275-P-0239').disposition,'accepted');
  assert.ok(!db.prepare("SELECT * FROM current_relation WHERE from_person='P-0275' AND to_person='P-0287' AND relation_type='parent'").get());
  assert.equal(date('E-death-P-0287').value,'1949-02-10');
 });
 await t.test('kärnfamiljens ägarbekräftelse består samtidigt som motstridiga gamla betyg syns',()=> {
  for(const [id,birth] of [['P-0269','1989-03-08'],['P-0270','1993-08-26']]) {
   assert.equal(current(id).evidence_status,'OWNER_CONFIRMED');
   assert.equal(date('E-birth-'+id).value,birth);assert.equal(current('E-birth-'+id).place_id,null);
   assert.deepEqual(acceptedParents(id).map(p=>p.from_person).sort(),['P-0004','P-0210']);
   assert.ok(acceptedParents(id).every(p=>p.evidence_status==='OWNER_CONFIRMED'));
   assert.match(current(`AS-${id}-profile-PCD029-boundary`).body,/PK08 faller/);
   assert.ok(personView(db,id).interpretationQuestions.some(q=>q.question.includes('PCD-2026-09-09-029')));
  }
  assert.equal(value('F-P-0270-name_form-owner-C0252').later_name_change_established,false);
 });
 await t.test('Korsbergaberättelsens kandidater blir inga säkra anor och sidnoll behåller sitt omfång',()=> {
  for(const n of [288,291,292,293,294]) {
   const id='P-0'+n;assert.equal(current(id).disposition,'candidate');assert.equal(acceptedParents(id).length,0);
  }
  assert.equal(current('REL-parent-P-0288-P-0289').disposition,'candidate');
  assert.equal(current('REL-spouse-P-0289-P-0290').disposition,'accepted');
  assert.equal(date('E-birth-P-0289').precision,'year');
  assert.equal(date('E-baptism-P-0290').value,'1810-07-20');
  assert.equal(current('SEARCH-P0289-C0840-JanFeb1808').outcome,'negative');
  assert.match(current('SEARCH-C0820-AI8-s157-family').body,/sid|sida/i);
  const auction=value('O-P-0294-C0262-auction-context');assert.equal(auction.dating,'1900-tal');
  assert.notEqual(current('O-P-0294-C0262-auction-context').record_id,current('O-P-0294-C0262-reported-work').record_id);
 });
 await t.test('Alvas gamla dubblett får historiskt forskningsläge utan ny person eller ändrad aktuell Alvaprofil',()=> {
  assert.equal(readCurrent(db,'P-0295'),null);
  assert.deepEqual(current('ASSESSMENT-P-0027'),originalAlvaReview);
  assert.deepEqual(current('BIO-P-0027'),originalAlvaStory);
  const v=personView(db,'P-0295');assert.ok(v.research.questions.length);
  assert.ok(v.research.questions.every(q=>q.subject_id==='IMPORT-P-0295'&&q.active===false&&q.disposition==='retired'));
  assert.ok(v.narratives.every(n=>n.subject_id==='IMPORT-P-0295'&&n.disposition==='retired'));
  assert.equal(value('F-P-0295-alias_source_context').canonical_person,'P-0027');
  assert.equal(value('F-P-0295-alias_source_context').separate_person,false);
  assert.equal(readCurrent(db,'P-0412'),null);
 });
 await t.test('sidogrenarnas namn, yrkesberättelser och olösta identiteter behåller egna gränser',()=> {
  assert.equal(current('M-C0871-Bjorn-Flemming').name_literal,'Björn Flemming');
  assert.equal(value('F-P-0296-occupation-family-report').reported_area_hectares,800);
  assert.equal(value('F-P-0297-name_form-family-report').reported_surname,'Drake af Hagelsrum');
  assert.equal(value('F-P-0298-name_form-family-report').surname,null);
  assert.equal(value('F-P-0298-occupation-family-report').organisation,null);
  assert.equal(current('IDENTITY-P0299-P0535').decision,'unresolved');
  assert.ok(!participants('E-marriage-P-0009-P-0535-1922').some(p=>p.person_id==='P-0299'));
  assert.equal(date('E-birth-P-0300').precision,'year');assert.equal(current('E-birth-P-0300').place_id,null);
  assert.equal(value('F-P-0300-residence-historical-family-places').reported_Vaxholm_year,'2011');
  assert.equal(date('E-divorce-P-0300-P-0302-unknown').precision,'unknown');
 });
 assert.equal(verifyDB(db).ok,true);
});
