import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';

// Fasta sakprov från fullständiga akter, profiler och citationernas senare rättelser.
// Förväntningarna läses inte ur migrationspaketet.
export function checkPersons10PartBRisks(db) {
  const r=id=>{const row=readCurrent(db,id);assert.ok(row,id);return row;};
  const v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
  const parents=id=>db.prepare("select x.* from current_revision c join relation x on x.revision_id=c.id where x.relation_type='parent' and x.to_person=? and c.disposition='accepted'").all(id);
  const witnesses=id=>db.prepare("select p.* from current_revision c join participation p on p.revision_id=c.id where p.event_id=? and p.role='witness'").all(id);

  // C0681 och C0563: sonens datum och den inskjutna faderns senare rättelser är skilda.
  assert.equal(d('E-birth-P-0470').value,'1785-11-04');
  assert.equal(d('E-arrival-P-0470-folio603').value,'1869-11-08');
  assert.equal(d('E-death-P-0470').value,'1870-12-27');
  assert.equal(v('F-P-0470-birthplace-reported-Bygdea').own_birth_record_read,false);
  const early=v('F-P-0470-family_context-seven-recorded-children');
  assert.equal(early.minimum_count,7);assert.equal(early.children.length,7);
  assert.equal(early.children.find(x=>x.name==='Carolina Sophia').birth_literal,'1816 34/4');
  assert.equal(early.children.find(x=>x.name==='Carolina Sophia').impossible_literal_day,true);
  assert.equal(early.children.find(x=>x.name==='Carl Eric').day_unread,true);
  assert.equal(early.child_surnames_not_written_in_rows,true);
  assert.equal(v('F-P-0470-marriage_context-undated').before_first_child_independently_proven,false);
  assert.equal(r('F-P-0470-identity_hypothesis-Anna-Johanna').disposition,'candidate');
  assert.equal(v('F-P-0470-identity_hypothesis-Anna-Johanna').same_person_proven,false);
  assert.equal(v('F-P-0470-life_context-limits').spouse_death_before1869_unproven,true);
  assert.equal(parents('P-0470').length,0);

  // C0681: 32 står i oläst marginalrubrik; grannpostens Holmström är inte hennes föräldrar.
  assert.equal(d('E-birth-P-0471').precision,'year');assert.equal(d('E-birth-P-0471').value,'1792');
  const age=v('F-P-0471-source_interpretation-maternal-margin32');
  assert.equal(age.literal,'32.');assert.equal(age.column_heading_unread,true);
  assert.equal(age.interpretation_reserved,true);assert.equal(age.independent_exact_birthdate_proven,false);
  assert.equal(v('O-P-0471-C0681-own').blank_fields.length,6);
  assert.equal(v('F-P-0471-social_network-Holmstrom-lead').kinship_to_Anna_Sophia_proven,false);
  assert.equal(r('F-P-0471-social_network-Holmstrom-lead').disposition,'candidate');
  assert.notEqual(r('M-P-0471-C0681-neighbour-father').record_id,r('M-P-0471-C0681-mother').record_id);
  assert.equal(v('F-P-0471-life_context-limits').missing_on_husbands1869_row_not_death,true);
  assert.equal(parents('P-0471').length,0);

  // C0733/C0744: Skelefte-noten är på en grannrad; Åskilje är kandidat och Petrio avvisad.
  assert.equal(d('E-birth-P-0472').precision,'year');
  assert.equal(d('E-marriage-P-0472-P-0473-1826').precision,'year');
  const misplaced=v('F-P-0472-source_assessment-misassigned-Skelefte-note');
  assert.equal(misplaced.actual_literal,'flyttad til Skelefte. med attest');
  assert.equal(misplaced.belongs_to_P0472,false);assert.equal(misplaced.neighbour_assignment_unresolved,true);
  assert.equal(r('ID-P-0472-C0744-candidate').decision,'candidate');
  assert.equal(r('ID-P-0472-C0744-candidate').evidence_status,'LEAD');
  assert.equal(v('F-P-0472-identity_assessment-Askilje-candidate').own_accepted_Lycksele_residence,false);
  assert.equal(r('ID-P-0472-C0744-rejected-Petrio').decision,'rejected');
  assert.equal(r('ID-P-0472-C0744-rejected-Petrio').disposition,'rejected');
  assert.equal(v('O-P-0472-C0744-rejected-Petrio').father,'Olof Ersson');
  assert.equal(parents('P-0472').length,0);
  assert.equal(r('SEARCH-P-0472-Lycksele-C2-1798').source_id,'S-0577');
  assert.deepEqual(JSON.parse(r('SEARCH-P-0472-Lycksele-C2-1798').scope_json).bounds.images,['C0034150_00111–00112']);
  assert.equal(v('F-P-0472-life_context-Anaset-limits').book_end1857_not_own_last_dated_contact,true);

  // C0733 T0173 ersätter två-mot-en-modellen; 1852-kataloggap är inget personnegativ.
  assert.equal(d('E-death-P-0473').precision,'year');assert.equal(d('E-death-P-0473').value,'1852');
  const pc=v('F-P-0473-source_assessment-parents-latest-conflict');
  assert.equal(r('F-P-0473-source_assessment-parents-latest-conflict').evidence_status,'CONFLICT');
  assert.equal(pc.AI3.father_year,'17[??] överstrivet, ej läsbart som1777');
  assert.deepEqual(pc.father_day_readings,[4,14]);assert.equal(pc.resolution_selected,false);
  assert.equal(pc.mother_arithmetic_not_independent_reading,true);
  assert.equal(v('F-P-0473-birth_constraint-marriage-age17').original1808_unsearched,true);
  assert.equal(v('F-P-0473-birth_constraint-marriage-age17').three_independent_birth_sources_proven,false);
  assert.equal(v('F-P-0473-source_route-death1852-catalogue-gap').person_death_negative,false);
  assert.equal(v('F-P-0473-family_context-five-daughters-origin-household').no_child_death_dates,true);
  assert.equal(v('F-P-0473-life_context-source-limits').never_moved_proven,false);

  // Grill: C0798 Ulla/oäkta; C0793 juli står mot april, intygsdagar är inte livslånga slutsatser.
  assert.equal(d('E-birth-P-0474').value,'1822-04-09');assert.equal(d('E-baptism-P-0474').value,'1822-04-12');
  assert.equal(v('O-P-0474-birth').mother,'Pig. Ulla Ersdotters');assert.equal(v('O-P-0474-birth').mother_age,28);
  assert.equal(v('F-P-0474-parentage-unknown-father').father,null);
  assert.deepEqual(parents('P-0474').map(x=>x.from_person),['P-0500']);
  assert.equal(witnesses('E-baptism-P-0474').length,4);
  const birth=v('F-P-0474-birth_conflict-April-July');
  assert.equal(birth.accepted,'1822-04-09');assert.equal(birth.opposing,'1822-07-09');
  assert.equal(r('F-P-0474-birth_conflict-April-July').evidence_status,'CONFLICT');
  for(const key of ['Carlsson-rejected','Jernbol-rejected'])assert.equal(r(`ID-P-0474-${key}`).decision,'rejected');
  assert.equal(r('ID-P-0474-CarlEric-candidate').decision,'candidate');
  assert.equal(d('E-permission-P-0474-1840').value,'1840-12-20');
  assert.equal(v('F-P-0474-attestation_limits-1840').exercise_performed_not_proven,true);
  assert.equal(v('F-P-0474-attestation_limits-1840').no_epilepsy_diagnosis,true);
  assert.equal(d('E-military-approval-P-0474-1841').value,'1841-02-15');
  assert.equal(d('E-military-replacement-P-0474-1841').value,'1841-02-18');
  assert.equal(d('E-military-transfer-P-0474-Hagby').precision,'unknown');
  assert.equal(v('F-P-0474-military_registration-transport-and-admission').Landin_admission1854_08_26_not_own_discharge,true);
  assert.equal(v('F-P-0474-marriage_assessment-undated').marriage_date,null);
  assert.equal(v('F-P-0474-marriage_assessment-undated').CarlJohan_oakta_not_safe_marriage_lower_bound,true);
  assert.equal(v('F-P-0474-source_assessment-source-forms-not-globalized').C0147_latest_own_raw,'Soldaten Carl Er. Grill');
  assert.equal(d('E-death-younger-Hedda-Gatstugan1883').value,'1883-11-10');
  assert.equal(r('EP-E-death-younger-Hedda-Gatstugan1883-younger-Hedda-principal').person_id,null);
  assert.equal(d('E-death-P-0474').value,'1895-01-04');assert.equal(d('E-burial-P-0474').value,'1895-01-13');
  assert.equal(v('F-P-0474-source_route-probate1895').act_unread,true);

  // Johanna: C0721 egen födelse30maj; barnens åldrar skiljer inte maj från senare aprilform.
  assert.equal(d('E-birth-P-0475').value,'1819-05-30');assert.equal(d('E-baptism-P-0475').value,'1819-05-31');
  assert.equal(witnesses('E-baptism-P-0475').length,4);
  const jb=v('F-P-0475-birth_conflict-May-April');
  assert.equal(r('F-P-0475-birth_conflict-May-April').evidence_status,'CONFLICT');
  assert.equal(jb.ages_fit_both_April_and_May,true);assert.equal(jb.independent_exact_age_proof,false);
  assert.equal(jb.C0721_late26Feb1863_is_not_birth_record_date,true);
  const walla=v('F-P-0475-family_context-Walla-children');
  assert.equal(walla.no_sibling_or_half_sibling_assertions,true);assert.equal(walla.age15_in_late_text_arithmetic_error,true);
  assert.equal(walla.age_alone_does_not_exclude_fatherhood,true);
  assert.equal(d('E-departure-P-0475-Bettna1841').precision,'year');
  assert.equal(d('E-death-P-0475').value,'1883-02-24');assert.equal(d('E-burial-P-0475').value,'1883-03-04');
  assert.equal(v('F-P-0475-life_context-limits').physical_death_place,null);
  const sm=r('SEARCH-P-0475-StoraMalm-marriage1842-1845');
  assert.equal(sm.source_id,'S-0592');assert.equal(sm.question_id,null);
  assert.equal(JSON.parse(sm.scope_json).bounds.images,'C0007593_00076–00087');

  // C0751: Degerfors är födelsesocken; Ekträsk hemvist, morfar egen familj och Sara annan rad.
  assert.equal(r('P-0480').evidence_status,'TRANSCRIBED');
  assert.equal(d('E-birth-P-0480').precision,'year');assert.equal(d('E-birth-P-0480').value,'1856');
  assert.equal(v('F-P-0480-birth_place-reported-Degerfors').Ektrask_is_residence_not_birth_village,true);
  assert.equal(v('F-P-0480-occupation-farmer1900').property_ownership_not_proven,true);
  const household=v('F-P-0480-household_assessment-scope');
  assert.equal(household.grandfather_API_family,3);assert.equal(household.grandfather_API_status,'ensamstående');
  assert.equal(household.Sara_own_family,true);assert.equal(household.same_roof_unproven,true);
  assert.equal(household.grandfather_1903_death_not_own_life_or_residence_anchor,true);
  assert.equal(household.marriage1875_1881_search_priority_not_bounds,true);
  assert.notEqual(r('M-P-0480-Sara-neighbour').record_id,r('M-P-0480-C0751-own').record_id);
  const gaps=v('F-P-0480-family_comparison-birth-year-gaps');
  assert.equal(gaps.exact_birth_intervals_unknown,true);assert.equal(gaps.infant_deaths_not_excluded,true);
  assert.equal(gaps.control_does_not_establish_abnormality,true);
  assert.equal(parents('P-0480').length,0);
  for(let n=481;n<=488;n++){
    const link=r(`REL-parent-P-0480-P-0${n}`);
    assert.equal(link.relation_type,'parent');assert.equal(link.nature,'recorded_parent');
  }
  return {ok:true,groups:7};
}
