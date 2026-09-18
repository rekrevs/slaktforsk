import assert from 'node:assert/strict';
import {readCurrent,personView} from '../lib/domain.mjs';
import {checkPersons10HallinRisks} from './persons-10-part-d-hallin-risk.mjs';
import {checkPersons10ParentsRisks} from './persons-10-part-d-parents-risk.mjs';
const val=(db,id)=>JSON.parse(readCurrent(db,id).value_json);
export function checkPersons10PartDRisks(db){
 const olo=readCurrent(db,'P-0453'), fred=readCurrent(db,'P-0466');
 assert.equal(olo.disposition,'accepted');assert.equal(olo.evidence_status,'TRANSCRIBED');assert.equal(olo.sex,null);
 assert.equal(fred.disposition,'accepted');assert.equal(fred.evidence_status,'CORROBORATED');assert.equal(fred.sex,null);
 const name=val(db,'F-P-0453-name_form-source-and-normalization');assert.deepEqual(name.source_first_name_alternatives,['Ole','Olo']);assert.equal(name.normalization_is_attested_form,false);assert.equal(name.rejected_transcription,'Andris Jacobson');
 assert.equal(readCurrent(db,'M-P-0453-C0521-father').name_literal,'Ole/Olo Andersson');assert.equal(readCurrent(db,'M-P-0453-C0521-father').role_literal,'Fadr:');assert.equal(readCurrent(db,'ID-P-0453-C0521-father').evidence_status,'TRANSCRIBED');
 assert.equal(readCurrent(db,'P-0412'),null);assert.equal(readCurrent(db,'IMPORT-P-0412').outcome,'historical_proposal');
 const ownSearch=readCurrent(db,'SEARCH-P-0453-own-row-AI10'),scope=JSON.parse(ownSearch.scope_json);assert.equal(ownSearch.source_id,'S-0414');assert.equal(ownSearch.outcome,'negative');assert.deepEqual(scope.bounds.full_page_ranges,['10–13','88–101','114–115']);assert.equal(scope.bounds.name_field_derivatives,'14–24');assert.equal(scope.bounds.whole_book,false);assert.equal(scope.bounds.own_Hjallsnas_Sag_heading_read,false);
 assert.equal(val(db,'F-P-0453-identity_assessment-Andreas-row-rejected').decision,'rejected');assert.equal(val(db,'F-P-0453-research_limits-one-post').C0688_death_search_is_not_Olo_negative,true);
 for(const id of ['REL-parent-P-0453-P-0411','REL-spouse-P-0413-P-0453']){assert.equal(readCurrent(db,id).disposition,'candidate');assert.equal(readCurrent(db,id).evidence_status,'CONFLICT');}
 assert.equal(readCurrent(db,'REL-spouse-P-0413-P-0466').disposition,'accepted');
 const ov=personView(db,'P-0453'),fv=personView(db,'P-0466');
 assert.equal(ov.events.length,0);assert.equal(fv.relations.filter(r=>r.relation_type==='parent').length,0);assert.equal(fv.relations.filter(r=>r.relation_type==='spouse').length,1);
 for(const pid of ['P-0453','P-0466','P-0413'])assert.equal(db.prepare("select count(*) n from current_revision r join relation x on x.revision_id=r.id where x.from_person=? and x.to_person='P-0336' and x.relation_type='parent'").get(pid).n,0);
 const birth=readCurrent(db,'E-birth-P-0466');assert.equal(JSON.parse(birth.date_json).value,'1824-10-02');assert.equal(birth.evidence_status,'TRANSCRIBED');assert.equal(birth.place_id,null);
 for(const [id,date] of [['E-banns-P-0413-P-0466-1849','1849-01-28'],['E-marriage-P-0413-P-0466-1849','1849-04-15']]){assert.equal(JSON.parse(readCurrent(db,id).date_json).value,date);const participants=db.prepare('select p.person_id from current_revision r join participation p on p.revision_id=r.id where p.event_id=? order by p.person_id').all(id).map(p=>p.person_id);assert.deepEqual(participants,['P-0413','P-0466']);}
 const afl=val(db,'F-P-0466-source_assessment-afl53');assert.equal(afl.literal,'afl.53');assert.equal(afl.chosen,null);assert.deepEqual(afl.alternatives,['afflyttad','afliden']);assert.equal(afl.confirmed_departure1853,false);assert.equal(afl.confirmed_death1853,false);assert.equal(afl.not_proof_of_living_until1853,true);
 assert.equal(fv.events.filter(e=>['death','burial','registered_departure'].includes(e.event_type)).length,0);
 const ages=val(db,'F-P-0466-age_comparison-marriage1849');assert.deepEqual(ages.groom.computed_age,{days:13,months:6,years:24});assert.deepEqual(ages.bride.computed_age,{days:26,months:1,years:25});assert.equal(ages.whole_year_ages_do_not_verify_exact_birth_days_or_months,true);assert.equal(ages.age_reports_may_derive_from_same_church_data,true);
 const chronology=val(db,'F-P-0466-family_chronology-1849');assert.equal(chronology.marriage_to_child_birth.days_total,81);assert.equal(chronology.assertion_dess_hustru_wrong_is_conditional_on_same_woman,true);assert.equal(chronology.two_women_hypothesis_not_excluded,true);assert.equal(chronology.older_pregnancy_inference.conception_month_unproven,true);assert.equal(chronology.older_pregnancy_inference.gestational_stage_not_established,true);
 assert.equal(val(db,'F-P-0466-household_membership-Hjallsnas94').Johan_August_identified_on_page94,false);
 const strategy=val(db,'F-P-0466-source_assessment-symmetric-negative-results');assert.equal(strategy.meaning_chosen,null);assert.equal(strategy.register_is_not_complete,true);
 for(const [id,source,needle] of [['family-next-household','S-0526','Fredric'],['family-out1853','S-0512','Fredric'],['death1853','S-0526','Fredric']]){const s=readCurrent(db,'SEARCH-P-0336-'+id);assert.equal(s.source_id,source);assert.equal(s.outcome,'negative');assert.match(JSON.parse(s.scope_json).query,new RegExp(needle));}
 assert.match(readCurrent(db,'ASSESSMENT-P-0453').body,/UNDERKÄND/);assert.match(readCurrent(db,'ASSESSMENT-P-0466').body,/EJ BÄRANDE/);
 const hallin=readCurrent(db,'F-P-0467-legal_context-acknowledgment')?checkPersons10HallinRisks(db):{groups:0};
 const parents=readCurrent(db,'F-P-0477-birth_assessment-three-bases')?checkPersons10ParentsRisks(db):{groups:0};
 return {ok:true,groups:9+hallin.groups+parents.groups};
}
