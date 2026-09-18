import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';
// Sakförväntningar från fullständigt lästa akter/profiler och C0064/0869/0872/1055/1071/1072/0110.
// Inga förväntade datum eller råläsningar hämtas från migrationspaketet.
export function checkPersons11PartCRisks(db){
 const r=id=>{const x=readCurrent(db,id);assert.ok(x,id);return x;};
 const v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
 const absent=id=>assert.equal(readCurrent(db,id),null,id+' får inte konstrueras');
 const parents=id=>db.prepare("select x.* from current_revision c join relation x on x.revision_id=c.id where x.relation_type='parent' and x.to_person=? and c.disposition='accepted'").all(id);
 // P0519: egen moder i1839födelsepost jämte hushållskedjan; egen död1867, inte makens1876.
 assert.equal(r('P-0519').evidence_status,'CORROBORATED');
 assert.equal(d('E-death-P-0519').value,'1867-11-23');assert.equal(r('E-death-P-0519').evidence_status,'TRANSCRIBED');
 assert.equal(d('E-birth-P-0519').precision,'year');assert.equal(d('E-birth-P-0519').value,'1804');
 assert.equal(r('M-P-0519-Anders1839-mother').record_id,'R-46eab7158175a81e60468858');
 assert.equal(v('O-P-0519-Anders1839-mother').own_age_unresolved,true);
 assert.equal(v('O-P-0519-AI9-own').year1868,'överarbetad/utsuddad fläck utan säkert eget datum');
 assert.equal(v('F-P-0519-source_assessment-birth-place-cell').chosen_AI8_reading,null);
 assert.equal(v('F-P-0519-source_assessment-blank-arrival-inference-rejected').no_arrival_before1825_proven,true);
 const marriageSearch=r('SEARCH-P-0082-marriage1831');assert.equal(marriageSearch.outcome,'negative');
 assert.match(marriageSearch.scope_json,/22/);assert.match(marriageSearch.scope_json,/1831/);
 // Fyra1839faddrar är namngivna fragment/en namnlös hustru, inga konstruerade personidentiteter.
 const witnesses=db.prepare("select p.* from current_revision c join participation p on p.revision_id=c.id where p.event_id='E-baptism-P-0065' and p.role='witness'").all();
 assert.equal(witnesses.length,4);assert.ok(witnesses.every(x=>x.person_id===null));
 assert.equal(r('M-P-0519-Anders1839-PerWife').name_literal,'');assert.equal(r('M-P-0519-Anders1839-NilsEricsson').role_literal,'Dr.');
 // C1055:s positiva lista upphävs inte av senare felaktig frånvaromening. Samma källa räknas inte flera gånger.
 const list=v('F-P-0519-source_assessment-C1055-positive-child-list');
 assert.deepEqual(list.earlier_positive_children,['P-0522','P-0523','P-0065','P-0524','P-0525','P-0526']);
 assert.deepEqual(list.not_listed,['P-0520','P-0521','P-0527']);assert.equal(list.no_new_image_review,true);
 // P0520: ett överarbetat AI6år har1832/33, destination478 bevisar inteWesterliden477.
 assert.deepEqual(d('E-birth-P-0520').values,['1832-02-05','1833-02-05']);
 assert.equal(v('F-P-0520-birth_assessment-book-readings').conflict_is_two_readings_of_same_AI6_cell,true);
 assert.equal(v('O-P-0520-AI6-own').destination_reference,'478');
 assert.equal(v('F-P-0520-source_reference-unread-destination').destination_place,null);
 assert.equal(v('F-P-0520-family_context-known-siblings').known_sibling_count,8);
 // P0521: Lisa i originalraderna, Eva är avskriftsfel. Mars/december kvar, f.g. ingen konfirmation.
 assert.equal(r('M-P-0521-AI5-own').name_literal,'Lisa Catharina');
 assert.equal(v('F-P-0521-name_form-Eva-rejected').rejected_form_is_transcription_error_not_source_variant,true);
 assert.deepEqual(d('E-birth-P-0521').values,['1834-03-06','1834-12-06']);
 assert.equal(v('O-P-0521-AI6-own').destination_reference,'44[4/7?]');absent('E-confirmation-P-0521');
 // P0522: sonens27maj/26augusti,464; faderns event eller rådiga skolnivåer får inte läggas på honom.
 assert.deepEqual(d('E-birth-P-0522').values,['1835-05-27','1835-08-26']);
 assert.equal(v('O-P-0522-AI8-own').destination_reference,'464');assert.equal(v('O-P-0522-AI8-own').knowledge_sign,'tom');
 assert.deepEqual(v('F-P-0522-chronology_assessment-age1851').completed_ages,[16,15]);
 assert.equal(r('IDENTITY-P-0082-P-0088').decision,'same_person');
 // P0523:41,4 är rågrupp, inte464/414; egen1866rad och inga egna1867–75årstecken.
 assert.deepEqual(d('E-birth-P-0523').values,['1836-12-24','1836-12-29']);
 assert.equal(v('O-P-0523-AI9-own').destination_reference,'41,4');
 assert.equal(v('O-P-0523-AI9-own').empty_annual_fields,'1867–1875');
 assert.equal(v('F-P-0523-source_reference-unread-destination').normalised_page,null);
 assert.equal(v('O-P-0523-AI8-own').birth_place_ditto_on_line_unattributed,true);
 // P0524: samma cell rättad1→10→16juni;4[8?]3 ej403; tredje exakta nattvard1862okt12.
 assert.equal(d('E-birth-P-0524').value,'1841-06-16');assert.equal(r('E-birth-P-0524').evidence_status,'TRANSCRIBED');
 assert.deepEqual(v('F-P-0524-birth_reading-same-cell-correction').superseded,['1/6 1841','10/6 1841']);
 assert.equal(v('O-P-0524-AI8-own').destination_reference,'4[8?]3');
 assert.equal(v('F-P-0524-source_reference-unread-destination').old403_rejected,true);
 assert.equal(v('F-P-0524-chronology_assessment-known-child-order').order_in_known_list,6);
 assert.equal(r('M-P-0524-AI7-own').name_literal,'Ulla Carolina');
 // P0525:20sep1843; pagina26, egna1866–68markeringar utan utvunna dagar. Oktoberbilden ger bara sju-postnoll.
 assert.equal(d('E-birth-P-0525').value,'1843-09-20');assert.equal(v('O-P-0525-AI8-own').struck,false);
 assert.equal(v('O-P-0525-AI9-own').destination_reference,'26');assert.equal(v('O-P-0525-AI9-own').day_numbers_not_finally_transcribed,true);
 assert.deepEqual(Object.keys(v('O-P-0525-AI9-own').own_annual_fields),['1866','1867','1868']);
 assert.equal(v('F-P-0525-chronology_assessment-known-child-order').order_in_known_list,7);
 const s=r('SEARCH-P-0525-October1843-image78'),scope=JSON.parse(s.scope_json);
 assert.equal(s.outcome,'negative');assert.equal(s.source_id,'S-0083');assert.equal(scope.bounds.record_count,7);assert.equal(scope.bounds.image,'A0001456_00078');
 assert.equal(v('F-P-0525-source_assessment-birth-search-routing').own_Carl_targeted_birth_search_still_unperformed,true);
 absent('E-baptism-P-0525');
 // P0526:1845 iAI7 mot1847 i andra rader; AI9positiv fjärde rad och84. A7985:s argument är inte råkälla.
 assert.equal(d('E-birth-P-0526').precision,'unknown');assert.equal(r('E-birth-P-0526').evidence_status,'CONFLICT');
 assert.equal(v('O-P-0526-AI7-own').birth_year,1845);assert.equal(v('O-P-0526-AI9-own').birth_literal,'1847 23/6');
 assert.equal(v('O-P-0526-AI9-own').destination_reference,'84');
 assert.equal(v('F-P-0526-source_assessment-later-evidence-and-routing').old_three_volume_summary_incomplete,true);
 const interval=v('F-P-0526-chronology_assessment-A7985-interval-argument').assessment;
 assert.equal(interval.stable_early_interval_claim_false,true);assert.equal(interval.tightest1845_claim_false,true);
 assert.deepEqual(interval.mother_completed_age_ranges,{at1845:[40,41],at1847:[42,43],at1850:[45,46]});
 assert.equal(interval.preferred_year_not_accepted,true);
 // P0527: dödsdag positivt rapporterad men egen atomär slutsats spärrad; korrekt villkorlig kalender-/dagräkning.
 assert.equal(d('E-birth-P-0527').value,'1850-12-05');assert.equal(d('E-death-P-0527').value,'1852-06-06');
 assert.equal(r('E-death-P-0527').disposition,'candidate');assert.equal(r('E-death-P-0527').evidence_status,'TRANSCRIBED');
 assert.equal(v('F-P-0527-death_assessment-reported-household-note').separate_final_check_done,false);
 const life=v('F-P-0527-chronology_assessment-conditional-lifespan');assert.equal(life.elapsed_days,549);assert.deepEqual(life.calendar_interval,{years:1,months:6,days:1});assert.deepEqual(life.mothers_completed_age_range,[45,46]);
 assert.equal(v('F-P-0527-source_scope-AI8-child-list-absence').not_independent_death_proof,true);absent('E-burial-P-0527');
 // Alla nio personers egna råobservationer håller rätt bok/familjepost. Inga kopierade personkärnor korroboreras genom antal.
 const records={AI3:'R-dcab035cc525fa01b6631828',AI4:'R-ee9afd95459534c05d5e3e8d',AI5:'R-8e70b63bdefd0550e21eba3c',AI6:'R-efca6e283ff6a0bd4048e02e',AI7:'R-b0e359298b9139018c7eff63',AI8:'R-ac67b2b327159ad11e766cc6',AI9:'R-6be04582ec19e700c612f06c'};
 for(let n=519;n<=527;n++){
  const id='P-0'+n;
  if(n>519){assert.equal(r(id).evidence_status,'TRANSCRIBED');assert.deepEqual(parents(id).map(x=>x.from_person).sort(),['P-0082','P-0519']);}
  // Rå son/dotter/moder/hustru är relationsuppgifter; inget separat könsfält är utvunnet.
  assert.equal(r(id).sex,null);
  for(const[b,record]of Object.entries(records)){
   const m=readCurrent(db,`M-${id}-${b}-own`),o=readCurrent(db,`O-${id}-${b}-own`);if(!m)continue;
   assert.equal(m.record_id,record);assert.equal(o.record_id,record);assert.equal(o.mention_id,m.object_id);
   assert.notEqual(m.name_literal,'Eva Catharina');assert.equal(r(`ID-${id}-${b}-own`).evidence_status,'TRANSCRIBED');
  }
  if(n<527&&n>519){absent('E-death-'+id);absent('E-marriage-'+id);}
 }
 // Typ/natur- och kyrkoeventgrind: en föräldrakant får aldrig bli recorded_sibling genom wrapperdefault.
 const edges=db.prepare("select x.* from current_revision c join relation x on x.revision_id=c.id where (x.from_person between'P-0519'and'P-0527' or x.to_person between'P-0519'and'P-0527') and x.relation_type in('parent','spouse','sibling')").all();
 for(const edge of edges)assert.equal(edge.nature,'recorded_'+edge.relation_type);
 const church=db.prepare("select c.object_id,e.* from current_revision c join event e on e.revision_id=c.id where c.object_id glob'E-church-P05[12][0-9]-*'").all();
 assert.ok(church.length>=70);for(const e of church)assert.equal(e.event_type,'other');
 return{ok:true,groups:13};
}
