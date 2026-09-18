import assert from 'node:assert/strict';
import {readCurrent,personView} from '../lib/domain.mjs';
const val=(db,id)=>JSON.parse(readCurrent(db,id).value_json);
const date=(db,id)=>JSON.parse(readCurrent(db,id).date_json);
export function checkPersons10HallinRisks(db){
 for(const p of ['P-0467','P-0468','P-0469']){
  assert.equal(readCurrent(db,p).disposition,'accepted');assert.equal(readCurrent(db,p).evidence_status,'TRANSCRIBED');assert.equal(readCurrent(db,p).sex,null);
  assert.match(readCurrent(db,'ASSESSMENT-'+p).body,/EJ BÄRANDE/);
 }
 // A correction of the same image cannot silently correct a different book.
 assert.deepEqual(date(db,'E-birth-P-0467').values,['1875-01-19','1875-01-17']);
 assert.equal(readCurrent(db,'E-birth-P-0467').evidence_status,'CONFLICT');
 const a=readCurrent(db,'M-P-0467-p384-own'),b=readCurrent(db,'M-P-0467-p392-own');
 assert.notEqual(a.record_id,b.record_id);assert.equal(a.name_literal,'Nils August Hallin');assert.equal(b.name_literal,'Nils August Hallén');
 assert.equal(val(db,'O-P-0467-p384-own').birth,'1875-01-19');assert.equal(val(db,'O-P-0467-p392-own').birth_literal,'1875 17/1');
 assert.equal(val(db,'F-P-0467-name_form-post-specific').later_variant_not_erased_by_earlier_correction,true);
 assert.equal(date(db,'E-death-P-0467').value,'1951-06-18');assert.equal(readCurrent(db,'E-death-P-0467').place_id,null);
 const deathObs=readCurrent(db,'O-P-0467-p388-death');assert.equal(deathObs.mention_id,null);assert.equal(deathObs.record_id,'R-606339082d269e79c0bde039');
 const search=readCurrent(db,'SEARCH-P-0467-death1951'),scope=JSON.parse(search.scope_json);
 assert.equal(search.outcome,'negative');assert.equal(scope.bounds.year,1951);assert.equal(scope.bounds.pages,'67–68');assert.deepEqual(scope.bounds.images,['00205416_00071','00205416_00072']);
 assert.match(search.body,/missad rad/i);assert.match(search.body,/inte bevisad/);
 const legal=val(db,'F-P-0467-legal_context-acknowledgment');
 assert.equal(legal.signature_date_unknown,true);assert.equal(legal.signature_physical_place_unknown,true);assert.equal(legal.two_year_continuous_relationship_unproven,true);assert.equal(legal.same_underlying_record,true);
 assert.equal(val(db,'F-P-0467-civil_status-first-widowhood').exact_date_does_not_prove_extant_identified_death_record,true);
 assert.deepEqual(val(db,'F-P-0467-family_chronology-source-intervals').wife_older_by_if_birth19jan,{days:27,months:10});
 const fatherRoute=val(db,'F-P-0467-source_reference-registration-sequence');
 assert.equal(fatherRoute.p389_departure_reported,'1942-03-31');assert.equal(fatherRoute.p392_arrival_reread,'1931-12-04');assert.equal(fatherRoute.date_pair_unresolved,true);
 assert.equal(fatherRoute.arrival_used_only_as_chronology_point,true);
 const ep=db.prepare('select p.person_id from current_revision r join participation p on p.revision_id=r.id where p.event_id=? order by p.person_id').all('E-marriage-P-0247-P-0467-1918').map(r=>r.person_id);
 assert.deepEqual(ep,['P-0247','P-0467']);
 const parentRows=personView(db,'P-0467').relations.filter(r=>r.relation_type==='parent');
 assert.deepEqual(parentRows.map(r=>r.to_person).sort(),['P-0468','P-0469']);
 for(const r of parentRows)assert.equal(r.nature,'recorded_parent');
 const n=val(db,'F-P-0468-name_form-source-and-normalization');assert.equal(n.rejected_p384_transcription,'Nils Eugen');assert.equal(n.index1930_form,'Nils Ejnar');assert.equal(n.family_surname_not_written_on_own_row,true);
 assert.equal(readCurrent(db,'P-0468').display_name,'Nils Egnar Hallin');
 assert.equal(readCurrent(db,'M-P-0468-p384-own').name_literal,'Nils Egnar');assert.equal(readCurrent(db,'M-P-0468-index1930-own').name_literal,'Nils Ejnar');
 assert.equal(date(db,'E-birth-P-0468').value,'1915-12-09');
 assert.equal(val(db,'F-P-0468-civil_status-marriage-certificate').completed_marriage_unproven,true);
 const egnarView=personView(db,'P-0468');assert.equal(egnarView.relations.filter(r=>r.relation_type==='spouse').length,0);assert.equal(egnarView.events.filter(e=>e.event_type==='marriage').length,0);
 assert.deepEqual(date(db,'E-birth-P-0469').values,['1918-09-28','1918-12-28']);
 assert.equal(readCurrent(db,'E-birth-P-0469').evidence_status,'CONFLICT');
 const iv=val(db,'F-P-0469-family_chronology-unresolved-birth-month');assert.equal(iv.chosen,null);assert.equal(iv.conception_dates_not_established,true);assert.equal(iv.chronology_does_not_choose,true);assert.equal(iv.not_a_negative_archival_search,true);assert.deepEqual(iv.mother_ages,[{days:5,months:7,years:44},{days:5,months:10,years:44}]);
 for(const [p,job,military,dest,year] of [['P-0468','byggnadsarb.','335 65/…','sida179',1941],['P-0469','jordbruksarb.','129 65/1938','nya boken388',1943]]){
  assert.equal(val(db,`F-${p}-occupation-p392`).literal,job);assert.equal(val(db,`F-${p}-military_registration-p392`).literal,military);assert.equal(val(db,`F-${p}-military_registration-p392`).service_or_unit_not_proven,true);
  const route=val(db,`F-${p}-source_reference-own-later-row`);assert.equal(route.reference_destination,dest);assert.equal(route.reference_year,year);assert.equal(route.reference_is_not_proof_of_physical_move,true);assert.equal(route.father_death1951_is_not_child_life_point,true);assert.equal(route.older_nothing_after1927_statement_outdated,true);
  assert.equal(personView(db,p).events.filter(e=>['death','burial','registered_departure'].includes(e.event_type)).length,0);
  for(const half of ['P-0241','P-0248','P-0249'])assert.equal(readCurrent(db,`REL-sibling-${half}-${p}`).nature,'maternal_sibling');
  const raw=val(db,`O-${p}-p392-own`);assert.equal(Object.hasOwn(raw,'death'),false);assert.equal(Object.hasOwn(raw,'Sundsvall'),false);
 }
 return {ok:true,groups:14};
}
