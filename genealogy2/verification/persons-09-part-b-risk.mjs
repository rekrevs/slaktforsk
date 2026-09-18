import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';

// Fasta sakprov från de fulla personakterna och citationernas rättelser.
// Inga förväntningar härleds genom att läsa migrationspaketet.
export function checkPersons09PartBRisks(db) {
  const r=id=>{const row=readCurrent(db,id);assert.ok(row,id);return row;};
  const v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
  const participants=id=>db.prepare('select p.* from current_revision c join participation p on p.revision_id=c.id where p.event_id=?').all(id);
  const parents=id=>db.prepare("select x.* from current_revision c join relation x on x.revision_id=c.id where x.relation_type='parent' and x.to_person=? and c.disposition='accepted'").all(id);
  const witnesses=id=>participants(id).filter(x=>x.role==='witness');

  // C0857/C0532: ålder36 avviker från 1776-09-13; patronymikon ger inga föräldrar.
  const segrin=v('F-P-0418-birth_reading-age-conflict');
  assert.equal(segrin.source_age,36);assert.equal(segrin.completed_age_if_household_date,35);
  assert.equal(segrin.rounding_rule_established,false);assert.deepEqual(segrin.birth_search_years,[1775,1776]);
  assert.equal(r('M-P-0418-C0857-own').name_literal,'Segrin Jonsdot[ter]');
  assert.equal(d('E-marriage-P-0417-P-0418-1806').precision,'year');
  assert.equal(r('F-P-0418-family_hypothesis-Ingrid-and-Jon').disposition,'candidate');
  assert.equal(parents('P-0418').length,0);
  assert.equal(v('F-P-0418-social_network-Gertrud-four-witnesses').kinship_ruled_out,false);
  assert.ok(witnesses('E-baptism-C0532-Cajsa-Brita').some(x=>x.person_id==='P-0418'&&x.mention_id==='M-P-0418-C0532-witness'));

  // C0530/C1030: 1860 ligger i Hvarthän, inte Död; barnet föddes44dagar före vigseln.
  assert.equal(d('E-birth-P-0419').value,'1842-02-25');
  const stefan=d('E-departure-P-0419-Stode1860');
  assert.equal(stefan.precision,'range');assert.equal(stefan.from,'1860-10-01');assert.equal(stefan.to,'1860-10-31');
  assert.equal(v('F-P-0419-life_scope-source-limits').death,null);
  assert.equal(v('F-P-0419-family_context-birth-before-marriage').elapsed_days,44);
  assert.equal(v('F-P-0419-family_context-birth-before-marriage').independent_birth_sources,1);
  assert.equal(v('O-P-0419-C0530-own').conduct_literal,'g.');

  // C0530 T0164: Jonas22/2 och29/3 är två läsningar av samma cell, inte två födelser.
  assert.equal(d('E-birth-P-0420').precision,'year');assert.equal(d('E-birth-P-0420').value,'1850');
  const jonas=v('F-P-0420-birth_reading-same-cell-conflict');
  assert.deepEqual(jonas.alternatives,['1850-02-22','1850-03-29']);assert.equal(jonas.chosen_date,null);assert.equal(jonas.source_count,1);
  assert.deepEqual(v('F-P-0420-birthplace-ditto-Holm').chain,['Stefan Erik:Holm','Stina Cajsa:do','Jonas:do']);
  assert.equal(v('F-P-0420-household_membership-Norafors-Stormyran').continued_residence_or_survival_proven,false);
  assert.equal(v('O-P-0420-C0530-own').row_crossed,false);

  // C0530 har bevarad fullbild; Ingrids senare1/8 får inte tappas eller bli avgjord4/8.
  assert.equal(d('E-birth-P-0421').precision,'year');
  assert.deepEqual(v('F-P-0421-birth_reading-August-conflict').alternatives,['1853-08-04','1853-08-01']);
  assert.equal(v('F-P-0421-birth_reading-August-conflict').chosen_date,null);
  const ingrid=v('F-P-0421-source_assessment-preserved-image-and-stale-claims');
  assert.equal(ingrid.image_sha256,'e891d66aa8dfb6759d069462a3a7b93f433ad7a1448fe90ef81313161d0510f0');
  assert.equal(ingrid.new_contract_review,false);assert.match(ingrid.sister_total_Holm1844_negative,/C-1042/);
  assert.equal(v('F-P-0421-life_scope-source-limits').identity_review,'UNDERKÄND');
  for(const id of ['P-0419','P-0420','P-0421'])assert.equal(r(id).evidence_status,'TRANSCRIBED');

  // C0553 postgräns olöst; C0563 far/son åtskilda; C0584 har såg.arb. utan f.d.
  assert.equal(d('E-marriage-P-0422-P-0423-1850').value,'1850-11-24');
  assert.equal(d('E-marriage-P-0422-P-0425-1870').value,'1870-07-02');
  assert.equal(d('E-banns-P-0422-P-0425-1870').value,'1870-06-19');
  const marriage=v('F-P-0422-source_assessment-1870-marriage-fields');
  assert.equal(marriage.folio,603);assert.equal(marriage.same_folio_proves_own_household_service,false);
  assert.equal(marriage.consent_document_read,false);assert.equal(marriage.first_wife_named,false);
  assert.equal(v('F-P-0422-family_context-two-marriages-sixteen-known').total_minimum,16);
  const father=v('F-P-0422-family_context-father-own-late-row');
  assert.equal(father.arrival_later,'1869 8/11');assert.equal(father.death_later,'1870 27/12');assert.equal(father.belongs_to_father_only,true);
  assert.equal(r('M-P-0422-C0584-death').role_literal,'såg. arb.');
  assert.equal(v('O-P-0422-C0584-death').former_prefix_present,false);
  assert.equal(v('O-P-0422-C0585-own').occupation_blank,true);
  assert.equal(d('E-death-P-0422').value,'1903-07-24');assert.equal(d('E-burial-P-0422').value,'1903-08-02');
  assert.equal(v('F-P-0422-family_context-Ektrask-inlaws').grandchildren.length,8);
  assert.equal(v('F-P-0422-source_route-mantal').all_volumes_individually_access_tested,false);
  assert.equal(v('F-P-0422-civil_status-widower1895').current_transcription,'1895-02-27');

  // C0995/96 T0133 återtar dödsortsslutsatsen och felåldern; C0699 är rektumprov.
  assert.equal(v('F-P-0423-birthplace-reported-Degerfors').hamlet,null);
  const death=d('E-death-P-0423');assert.equal(death.precision,'range');
  assert.equal(death.from,'1868-02-13');assert.equal(death.to,'1870-07-02');
  const sara=v('F-P-0423-death_reading-household-date');
  assert.equal(sara.reported_date,'1868-08-14');assert.equal(sara.exact_date_established,false);assert.equal(sara.return_to_Anaset_excluded,false);
  for(const suffix of['C0695-Rusele','C0686-Bygdea','C0711-child']){
    const id=r(`ID-P-0423-${suffix}`);assert.equal(id.decision,'rejected');assert.equal(id.disposition,'rejected');
  }
  const probate=JSON.parse(r('SEARCH-P-0423-probate-right-pages').scope_json);
  assert.equal(probate.bounds.count,562);assert.equal(probate.bounds.left_page_start_coverage_proven,false);assert.equal(probate.bounds.not_chronological,true);
  assert.equal(r('SEARCH-P-0423-Lycksele-marriage1850').source_id,'S-0523');
  const degerfors=r('SEARCH-P-0423-Degerfors-death1868');assert.equal(degerfors.source_id,'S-0816');
  assert.equal(JSON.parse(degerfors.scope_json).bounds.correct_age_at_1868_08_14,'39år2m24d');
  assert.equal(r('SEARCH-P-0423-Degerfors-death1869-1870').source_id,'S-0816');
  assert.equal(r('SEARCH-P-0423-Savar-F1-death1868-1870').source_id,'S-0442');
  assert.equal(r('SEARCH-P-0423-Savar-Botsmark1845-1854').source_id,'S-0524');
  assert.equal(r('SEARCH-P-0423-Savar-candidate-arrival1845-1849').source_id,'S-0146');
  assert.equal(JSON.parse(r('SEARCH-P-0423-Savar-death1868-1870').scope_json).bounds.to,'1868-09-10');
  assert.equal(v('F-P-0423-source_assessment-multivolume-search-scopes').Savar_death.no_date_gap,true);
  assert.equal(v('F-P-0423-source_assessment-SCB-dependent-scope').other_ranges_window_only,26);
  assert.equal(v('F-P-0423-source_route-limits-and-copies').probate_missing,536);
  assert.equal(v('F-P-0423-family_context-ten-children-eight-deliveries').deliveries,8);

  // P0425 T0161: egen aktuella27/2-cell, äldre2/7 och oläst dödbok; sex egna, sju listade styvbarn.
  assert.equal(d('E-death-P-0425').value,'1895-02-27');
  const kajsa=v('F-P-0425-death_reading-same-cell-correction');
  assert.equal(kajsa.current_transcription,'1895-02-27');assert.equal(kajsa.superseded_transcription,'1895-07-02');
  assert.equal(kajsa.independent_death_record_read,false);assert.equal(kajsa.anniversary_coincidence_retracted,true);
  assert.equal(v('F-P-0425-source_assessment-servant-to-wife').physical_journey,false);
  assert.equal(v('F-P-0425-source_assessment-servant-to-wife').servant_row_record_boundary_unresolved,true);
  assert.equal(v('F-P-0425-family_context-named-father').actual_consent_document_read,false);
  const secondFamily=v('F-P-0425-family_context-own-and-stepchildren');
  assert.equal(secondFamily.own_children_count,6);assert.equal(secondFamily.listed_stepchildren_count,7);
  assert.equal(secondFamily.never_shared_with_Sophia_not_independently_proven,true);

  // C0562/C0552: åtta dopvittnen inklusive två namnlösa hustrur; ingen bevisad1890vigsel.
  assert.equal(d('E-birth-P-0426').value,'1858-10-26');assert.equal(d('E-baptism-P-0426').value,'1858-10-29');
  assert.equal(witnesses('E-baptism-P-0426').length,8);
  assert.equal(v('F-P-0426-social_network-eight-witnesses').anonymous_wives,2);
  const per=d('E-departure-P-0426-folio738');assert.equal(per.precision,'range');assert.equal(per.from,'1888-10-01');assert.equal(per.to,'1888-10-31');
  assert.deepEqual(v('F-P-0426-residence-folio738').possible_days,[21,31]);
  assert.equal(r('F-P-0426-notation_interpretation-9Kl87').disposition,'candidate');
  assert.equal(v('F-P-0426-notation_interpretation-9Kl87').service_proven,false);
  assert.equal(v('F-P-0426-source_history-unpreserved-adult-claims').marriage_created,false);

  // P0427 A6270–73: dödkolumnen20/4, marsrättelse och arbetsnoter utan tjänstebevis.
  assert.equal(d('E-birth-P-0427').value,'1864-03-24');assert.equal(d('E-death-P-0427').value,'1892-04-20');
  assert.equal(v('O-P-0427-C0561-own').month_not_overwritten,true);
  assert.equal(r('F-P-0427-birth-rejected-May').disposition,'rejected');
  assert.equal(r('F-P-0427-notation_interpretation-arb-and-class').disposition,'candidate');
  assert.equal(v('F-P-0427-notation_interpretation-arb-and-class').service_proven,false);
  assert.equal(witnesses('E-baptism-P-0427').length,6);
  assert.equal(v('F-P-0427-social_network-own-six-witnesses').sibling_relation_to_child,false);
  assert.equal(v('F-P-0427-life_context-recorded-not-continuous').unmarried_status_not_proven_by_age_or_son,true);

  // C0564/C0552: Esters ordinarie dop, sju vittnen och eget hushåll; fyra barn utan påhittat råefternamn.
  assert.equal(d('E-birth-P-0428').value,'1868-02-13');assert.equal(d('E-baptism-P-0428').value,'1868-02-16');
  assert.equal(witnesses('E-baptism-P-0428').length,7);
  const twin=v('F-P-0428-birth_context-mother-and-twin');
  assert.equal(twin.own_emergency_baptism,false);assert.equal(twin.sister_emergency_baptism_date,null);
  assert.equal(r('M-P-0428-C0552-wife').name_literal,'Esther Amalia Zingmark');
  const own=v('F-P-0428-family_context-Johan-and-four-children');
  assert.equal(own.children.length,4);assert.ok(own.children.every(x=>x.surname_written===false));
  assert.equal(own.child_name_Johan_Oskar_not_P0028,true);
  assert.equal(v('O-P-0428-C0552-child-Anders-Alexius').month_reserved,true);
  assert.equal(r('EP-E-marriage-P-0428-Johan-Jacobsson-1886-mention-spouse').person_id,null);
  assert.equal(v('F-P-0428-household_context-row22-unassigned').membership_in_Jacobsson_household,null);
  assert.equal(v('F-P-0428-life_context-book-limits').own_folio714_unread,true);
  return {ok:true,groups:10};
}
