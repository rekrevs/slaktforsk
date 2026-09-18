import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';
const val=(db,id)=>JSON.parse(readCurrent(db,id).value_json);
const date=(db,id)=>JSON.parse(readCurrent(db,id).date_json);
export function checkPersons10ParentsRisks(db){
 for(const id of ['P-0476','P-0477','P-0478','P-0479']){
  const p=readCurrent(db,id);assert.equal(p.disposition,'accepted');assert.equal(p.evidence_status,'CORROBORATED');assert.equal(p.sex,null);
  assert.match(readCurrent(db,'ASSESSMENT-'+id).body,/GODKÄND/);assert.match(readCurrent(db,'ASSESSMENT-'+id).body,/BÄRANDE/);
  assert.equal(db.prepare("select count(*) n from current_revision r join relation a on a.revision_id=r.id where a.to_person=? and a.relation_type='parent'").get(id).n,0);
  assert.equal(readCurrent(db,'E-death-'+id),null);
 }
 for(const id of ['ID-P-0476-Jan1791-candidate','ID-P-0477-Helena1785-candidate']){const r=readCurrent(db,id);assert.equal(r.decision,'candidate');assert.equal(r.disposition,'candidate');assert.equal(r.evidence_status,'LEAD');}
 assert.equal(date(db,'E-birth-P-0476').value,'1791-09-05');assert.equal(date(db,'E-birth-P-0477').precision,'unknown');assert.equal(readCurrent(db,'E-birth-P-0477').evidence_status,'CONFLICT');
 assert.equal(readCurrent(db,'E-baptism-P-0476'),null);assert.equal(readCurrent(db,'E-baptism-P-0477'),null);
 const cand=readCurrent(db,'O-P-0476-Jan1791-candidate');assert.equal(cand.record_id,'R-de8eeb46e6961ce1353920c1');
 assert.equal(val(db,cand.object_id).baptism,'1791-09-06');assert.equal(val(db,cand.object_id).baptism_place,'St. Malms [kyrka?]');
 const oldSearch=readCurrent(db,'SEARCH-P-0476-historical-May1791');assert.equal(oldSearch.disposition,'retired');assert.equal(oldSearch.outcome,'negative');assert.equal(JSON.parse(oldSearch.scope_json).bounds.whole_year,false);assert.match(oldSearch.body,/säger inget om5september/);
 assert.equal(val(db,'F-P-0476-source_assessment-May-correction').old_conflict_rejected,true);
 const l=val(db,'F-P-0477-birth_assessment-three-bases');assert.equal(l.household_date,'1783-10-21');assert.deepEqual(l.derived_window_if_completed_years,{from:'1784-05-31',to:'1785-05-30'});assert.equal(l.household_date_gives_age,35);assert.equal(l.candidate_date_gives_age,33);assert.equal(l.chosen,null);assert.equal(l.candidate_identity_unproved,true);
 const h=val(db,'F-P-0477-family_hypothesis-Anders-children');assert.deepEqual(h.older_children_Jans_completed_ages,[14,18,20]);assert.equal(h.age_alone_does_not_exclude_fatherhood,true);assert.equal(h.older_children_are_Lenas_unproven,true);assert.equal(h.childbearing_does_not_itself_prove_marriage,true);assert.equal(h.window_conditional_on_family_hypothesis,true);
 const children=val(db,'F-P-0476-household_membership-Walla-six-children').children;assert.equal(children.length,6);assert.equal(children[1].birth,'1809-09-27');assert.equal(children[2].birth,'1812-04-12');
 assert.equal(val(db,'F-P-0477-research_limits-own-life').own_literacy_knowledge_smallpox_annual_church_fields_unextracted,true);
 const janHome=val(db,'O-P-0476-C0721-Walla');assert.equal(janHome.smallpox_cell,'tom');assert.equal(janHome.arrival_year,1815);
 const lenaHome=val(db,'O-P-0477-C0721-Walla');assert.deepEqual(lenaHome,{birth_literal:'1783 21/10 Malm'});
 assert.equal(date(db,'E-registered_arrival-P-0476').value,'1815');assert.equal(readCurrent(db,'E-registered_arrival-P-0477'),null);
 for(const key of ['CarlEricErsson','MajaJonsdotter','PehrLarsson','GretaLenaLarsdotter']){const ep=readCurrent(db,`EP-E-baptism-P-0475-${key}-witness`);assert.equal(ep.role,'witness');assert.equal(ep.event_id,'E-baptism-P-0475');assert.equal(ep.person_id,null);}
 const a=val(db,'F-P-0478-birth_assessment-three-books');assert.equal(a.AI2.year,1777);assert.equal(a.AI3.cannot_read_1777,true);assert.equal(a.AI3.year_literal,'17[??]');assert.equal(a.AI3.day_literal,'[1?]⁴/₁₀');assert.equal(a.AI4.year_literal,'1768');assert.equal(a.chosen_year,null);assert.equal(a.day_readings_are_compatible_not_equal_certain,true);
 assert.equal(date(db,'E-birth-P-0478').precision,'unknown');assert.equal(readCurrent(db,'E-birth-P-0478').evidence_status,'CONFLICT');
 const sara=val(db,'F-P-0479-birth_assessment-raw-year-and-inference');assert.equal(sara.AI4_literal,'17[9?]7');assert.equal(sara.year1797_exclusion_conditional_on_same_mother_identity,true);assert.equal(sara.exclusion_does_not_read1777_in_AI4,true);
 assert.equal(readCurrent(db,'M-P-0479-AI4-own').name_literal,'Sara Lisa A[nders?]dotter');assert.equal(val(db,'O-P-0479-AI4-own').birth_literal,'17[9?]7');assert.equal(date(db,'E-birth-P-0479').precision,'year');
 const marks=val(db,'F-P-0478-source_comparison-daughter-margins');assert.equal(marks.child_death_proven,false);assert.equal(marks.not_whole_AI3_negative,true);assert.equal(marks.AI2.find(x=>x.name==='Beata').struck,false);assert.equal(marks.AI3_Sophia_reference,'17[?]');
 assert.equal(val(db,'F-P-0479-identity_assessment-daughter-namesake').separate_referents,true);
 for(const id of ['P-0478','P-0479']){assert.equal(val(db,`F-${id}-research_limits-book-periods`).book_period_not_proof_of_survival1842,true);assert.equal(val(db,`F-${id}-household_position-sequence`).undantag_hypothesis_only,true);assert.equal(readCurrent(db,`REL-parent-${id}-P-0473`).nature,'recorded_parent');}
 return {ok:true,groups:13};
}
