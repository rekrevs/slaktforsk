import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';

// Förväntningar från kompletta C0845/0848/0849/0850/0851, senare rättelser och
// respektive persons akt/profil. Ingen förväntning hämtas ur migrationspaketet.
export function checkPersons11PartBRisks(db){
 const r=id=>{const x=readCurrent(db,id);assert.ok(x,id);return x;};
 const v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
 const parents=id=>db.prepare("select x.* from current_revision c join relation x on x.revision_id=c.id where x.relation_type='parent' and x.to_person=? and c.disposition='accepted'").all(id);
 const witnesses=id=>db.prepare("select p.* from current_revision c join participation p on p.revision_id=c.id where p.event_id=? and p.role='witness'").all(id);
 for(let n=509;n<=518;n++){
  const id=`P-0${n}`;assert.equal(r(id).sex,null,id);
  assert.equal(r(id).disposition,'accepted',id);
  assert.equal(r(id).evidence_status,[515,516].includes(n)?'CORROBORATED':'TRANSCRIBED',id);
  assert.equal(parents(id).length,0,id+' saknar belagda egna föräldrar');
  assert.equal(readCurrent(db,`E-birth-${id}`),null,id+' ingen egen exakt eller vald födelse');
 }
 for(const [a,b] of [['0509','0510'],['0511','0512'],['0513','0514'],['0515','0516'],['0517','0518']]){
  const rel=r(`REL-spouse-P-${a}-P-${b}`);assert.equal(rel.nature,'recorded_spouse');
  assert.equal(JSON.parse(rel.date_json).precision,'unknown');
 }

 // P0509: senaste C0845 skriver Klåckaren, inte mäskaren; ingen egen ålder.
 assert.equal(r('M-C0845-P-0329-parent-P-0509').name_literal,'Anders Åhlund');
 assert.equal(r('M-C0845-P-0329-parent-P-0509').role_literal,'Klåckaren');
 assert.equal(v('F-P-0509-source_assessment-corrected-forms').rejected_old_title,'mäskaren');
 assert.equal(v('F-P-0509-source_interpretation-age-interval').own_conditional_birth,null);
 const clerk=v('F-P-0509-occupation-clerk1808');
 assert.equal(clerk.private_ownership_proven,false);assert.equal(clerk.teacher_role_proven,false);
 assert.equal(clerk.own_hand_identified,false);assert.equal(clerk.tenure_contract_unread,true);
 assert.equal(v('F-P-0509-residence-reported1808').child_later_Gryt_Helgesta_not_own_migration,true);
 assert.equal(witnesses('E-baptism-P-0329').length,6);
 assert.equal(d('E-birth-P-0329').value,'1808-09-02');
 assert.equal(d('E-baptism-P-0329').value,'1808-09-04');

 // P0510: Hedda Molander och ett villkorligt intervall; Hedvig är sökform.
 assert.equal(r('M-C0845-P-0329-parent-P-0510').name_literal,'Hedda Molander');
 const molander=v('F-P-0510-name_context-Molander');
 assert.equal(molander.rejected,'Hedda Morander');assert.ok(molander.search_forms.includes('Hedvig Molander'));
 assert.equal(molander.no_witness_named_Molander,true);assert.equal(molander.all_baptism_kinship_routes_exhausted,false);
 assert.equal(v('F-P-0510-residence-reported1808').own_occupation,null);
 const hedAge=v('F-P-0510-source_interpretation-age-interval');
 assert.equal(hedAge.probable_subject,'modern');assert.equal(hedAge.rule_proven,false);
 assert.equal(hedAge.one_interval_not_two_ages,true);assert.equal(hedAge.own_date_selected,false);
 assert.equal(hedAge.own_conditional_birth,'omkring1773–1778');

 // P0511: Stocktorp rättar Hökstorp, Bonden bevisar varken ägande eller rotehållning.
 assert.equal(r('M-C0845-P-0330-parent-P-0511').name_literal,'Carl Carlsson');
 assert.equal(r('M-C0845-P-0330-parent-P-0511').role_literal,'Bonden');
 const farmer=v('F-P-0511-occupation-farmer1808');assert.equal(farmer.place,'Stocktorp,Ludgo');
 assert.equal(farmer.property_ownership_not_proven,true);assert.equal(farmer.roteholder_or_soldier_role_not_proven,true);
 assert.equal(farmer.neighbour_landsvarnist_not_this_man,true);assert.equal(farmer.torp_suffix_not_farm_tenure,true);
 assert.equal(v('F-P-0511-source_assessment-corrected-forms').rejected_old_place,'Hökstorp');
 assert.equal(v('F-P-0511-source_interpretation-age-interval').own_definite_age,null);
 assert.equal(d('E-birth-P-0330').value,'1808-12-23');assert.equal(d('E-baptism-P-0330').value,'1808-12-26');

 // P0512: två utpekade namn är inte hela listan; Lena Anders Dr är en tredje.
 const anna=v('F-P-0512-social_network-own-child-baptism');
 assert.deepEqual(anna.Anders_patronymic_bearers,['Pehr Andersson','Lena Anders Dr.','Cathrina Anders dr']);
 assert.equal(anna.own_surname_match_count,3);assert.equal(anna.two_highlighted_not_exhaustive,true);
 assert.equal(anna.kinship_proven,false);assert.equal(anna.independent_record_corroboration,false);
 assert.equal(anna.Sattersta_reserved,true);assert.equal(witnesses('E-baptism-P-0330').length,6);
 const aa=v('F-P-0512-source_interpretation-age-interval');
 assert.equal(aa.comparison_posts,21);assert.equal(aa.single_mother_posts,4);
 assert.equal(aa.comparison_covers_whole1808,false);assert.equal(aa.parish_annual_total33_not_family_count,true);
 assert.equal(aa.matching_interval_other_mother_not_rule_confirmation,true);
 assert.equal(v('F-P-0512-life_context-unknowns').named_as_parent_not_independent_survival_certificate,true);

 // P0513: åboen ger ingen upplåtelsehandling; Månsson är annan man i novemberposten.
 assert.equal(r('M-C0848-father').name_literal,'Olof Hansson');assert.equal(r('M-C0848-father').role_literal,'åboen');
 assert.equal(v('F-P-0513-birth_constraint-age1815').father_age,null);
 const ol=v('F-P-0513-life_context-Bodarne1815');
 assert.equal(ol.abo_word_not_read_title_deed,true);assert.equal(ol.self_ownership_excluded_by_title_alone,false);
 assert.equal(ol.child_later_household_not_own_life,true);
 assert.equal(v('F-P-0513-identity_boundary-Olof-Mansson').different_men_on_current_reading,true);
 assert.notEqual(r('M-C0848-Nov1814-witness').record_id,r('M-C0848-father').record_id);
 assert.equal(r('F-P-0513-identity_hypothesis-unnamed-assessor').disposition,'candidate');
 assert.equal(r('F-P-0513-identity_hypothesis-unnamed-assessor').evidence_status,'LEAD');
 assert.equal(v('F-P-0513-identity_hypothesis-unnamed-assessor').same_person_proven,false);
 assert.equal(r('M-C0848-witness-Namndeman').name_literal,'');

 // P0514:33gäller modern; tre Anders-bärare, Ericsdotter är inte en tredje Andersdotter.
 assert.equal(r('M-C0848-mother').name_literal,'Britta Anders Dotr');
 const ba=v('F-P-0514-birth_constraint-age1815');
 assert.equal(ba.reported_mother_age,33);assert.equal(ba.age_subject,'P-0514');
 assert.equal(ba.own_conditional_window,'februari1781–februari1782');
 assert.equal(ba.completed_year_model_unverified,true);assert.deepEqual(ba.own_search_years,[1780,1781,1782]);
 const bc=v('F-P-0514-source_assessment-witness-count-and-limits');
 assert.equal(bc.direct_Anders_bearers,3);assert.equal(bc.named_Erics_daughter,'Britta Erics Dotr');
 assert.equal(bc.T0170_three_daughter_count_incorrect,true);assert.equal(bc.A7592_fifth_Anders_count_incorrect,true);
 assert.equal(bc.statistical_excess_over_chance_not_established,true);assert.equal(bc.no_Hansson_does_not_exclude_fathers_kin,true);
 assert.equal(v('F-P-0514-life_context-Bodarne1815').absence_of_maternal_death_note_not_proof_of_survival,true);
 assert.equal(witnesses('E-baptism-P-0383').length,5);

 // P0515:positiva juni1801 före1810–11, aprilfamiljen fortfarande annan.
 assert.equal(r('M-P-0515-C0850-parent').name_literal,'Olof Nilssons');
 assert.equal(r('M-P-0515-C0850-parent').role_literal,'Hemansbrukaren');
 assert.equal(r('M-P-0515-C0850-parent').record_id,'R-fd22c70b1722defa9431f314');
 assert.equal(r('M-P-0515-C0849-own').record_id,'R-b24107f8ee54d50e319c37d6');
 assert.equal(r('M-P-0515-C0849-Sjostrom').record_id,'R-f407321f3b278ee8f1e0e2b1');
 assert.equal(r('M-P-0515-C0849-own').role_literal,'');
 assert.deepEqual(v('O-P-0515-C0849-own').columns,{'1810':'49. abs.','1811':'50.'});
 assert.deepEqual(v('F-P-0515-birth_constraint-own-age1810-1811').conditional_birth_years,[1760,1761]);
 const pl=v('F-P-0515-life_context-positive1801-and-later');
 assert.deepEqual(pl.own_positive_original_years,[1801,1810,1811]);assert.equal(pl.old_only1810_1811_claim_superseded,true);
 assert.equal(pl.later_household_heading,'Inhyses.');assert.equal(pl.continued_farmer_status_not_proven,true);
 assert.equal(pl.occupational_change_explanation,null);assert.equal(pl.child_education_does_not_prove_farm_wealth,true);
 assert.equal(v('F-P-0515-source_assessment-positive-child-not-null').april_identity_still_rejected,true);
 assert.equal(d('E-birth-P-0388').value,'1801-06-25');assert.equal(d('E-baptism-P-0388').value,'1801-06-28');
 assert.equal(witnesses('E-baptism-P-0388').length,4);
 assert.equal(r('EP-E-baptism-P-0388-P-0515-parent').mention_id,'M-P-0515-C0850-parent');

 // P0516:marginalens senare705/Komintet ges ingen person eller analfabetism.
 assert.equal(r('M-P-0516-C0850-parent').name_literal,'Maja Jons D:r');
 assert.equal(r('M-P-0516-C0849-own').name_literal,'Maja Jonsd:r');
 assert.deepEqual(v('O-P-0516-C0849-own').columns,{'1810':'40. abs.','1811':'41. abs.'});
 assert.deepEqual(v('F-P-0516-birth_constraint-own-age1810-1811').conditional_birth_years,[1769,1770]);
 assert.equal(v('F-P-0516-birth_constraint-own-age1810-1811').one_year_increment_internal_only,true);
 const marg=v('F-P-0516-source_assessment-unread-margin');
 assert.deepEqual(marg.latest_partial,['705.[?]','Kom intet']);assert.equal(marg.next_column,'x');
 assert.equal(marg.person_assignment,null);assert.equal(marg.illiteracy_proven_for_anyone,false);
 assert.equal(marg.physical_move_proven,false);assert.equal(marg.death_inferred,false);
 const fam=v('F-P-0516-family_context-Rinkaby');
 assert.equal(fam.daughter.person_created,false);assert.equal(fam.reported_child_age_difference,7);
 assert.equal(fam.calculated_ages_are_not_exact,true);assert.equal(fam.no_children_in_gap_assumed,true);
 assert.equal(fam.marriage_around1790_search_priority_not_fact,true);
 assert.deepEqual(v('F-P-0516-religious_participation-abs-columns').own_marked_years,[1810,1811]);
 assert.equal(v('F-P-0516-religious_participation-abs-columns').unmarked_1811_proves_attendance,false);

 // P0517:två egna poster; post21dop22juli är inte dotterns sjunde vittne eller13dagarsgap.
 assert.equal(r('M-P-0517-C0851-parent').name_literal,'Samuel Bökelunds');
 assert.equal(r('M-P-0517-C0851-parent').role_literal,'Kyrkoherdens i Mortorp');
 assert.equal(r('M-P-0517-C0851-own-witness').name_literal,'Samuel Bökelund');
 assert.equal(r('M-P-0517-C0851-own-witness').record_id,'R-af2a47cb7585de686f59c380');
 assert.notEqual(r('M-P-0517-C0851-parent').record_id,r('M-P-0517-C0851-own-witness').record_id);
 assert.equal(d('E-baptism-C0851-post21-1809').value,'1809-07-22');
 const ep=r('EP-E-baptism-C0851-post21-1809-P-0517-witness');assert.equal(ep.role,'witness');assert.equal(ep.person_id,'P-0517');
 assert.equal(ep.mention_id,'M-P-0517-C0851-own-witness');
 assert.equal(witnesses('E-baptism-P-0389').length,6);
 const post=v('F-P-0517-source_assessment-post18-post21-dates');assert.equal(post.baptism_gap_days,16);
 assert.equal(post.old_thirteen_days_claim_incorrect,true);assert.equal(post.three_life_anchors_span_days,19);
 assert.equal(post.mother_participation_in_post21_unproven,true);
 assert.equal(v('F-P-0517-occupation_context-vicar1809').churchbook_writer_not_proven_from_office,true);
 assert.equal(v('F-P-0517-occupation_context-vicar1809').parsonage_as_own_address_proven,false);
 assert.equal(v('F-P-0517-family_hypothesis-Gustava-Christina-Bokelund').relationship_proven,false);

 // P0518:Rybergsd:r ersätterKylenstjerna, och åldern33 blir inget valt födelseår.
 assert.equal(r('M-P-0518-C0851-parent').name_literal,'Gustava Maria Rybergsd:r');
 assert.equal(r('F-P-0518-name_claim-Kylenstjerna-rejected').evidence_status,'REJECTED');
 assert.equal(r('F-P-0518-name_claim-Kylenstjerna-rejected').disposition,'rejected');
 const nr=v('F-P-0518-source_assessment-name-and-dependence');
 assert.equal(nr.old_nobility_premise_rejected,true);assert.equal(nr.rejected_form_not_search_key,true);
 assert.equal(nr.C0467_names_neither_parent,true);assert.equal(nr.independent_parent_sources_from_adult_child,0);
 assert.equal(nr.child_raw,'Johanna Chri-stiana');
 const ga=v('F-P-0518-birth_constraint-age33');assert.equal(ga.raw_age,'33');
 assert.deepEqual(ga.search_years,[1774,1775,1776]);assert.equal(ga.exact_birth_selected,false);
 assert.equal(ga.comparison_not_independent_birthdate_evidence,true);
 assert.equal(v('F-P-0518-family_hypothesis-Johanna-Ryberg').relationship_proven,false);
 assert.equal(r('F-P-0518-family_hypothesis-Johanna-Ryberg').disposition,'candidate');
 assert.equal(v('F-P-0518-life_context-unresolved').maternal_survival_proven_from_absent_note,false);
 assert.equal(v('F-P-0518-life_context-unresolved').child_baptism_three_days_later_not_maternal_health_evidence,true);
 assert.equal(v('F-P-0518-occupation_context-vicar1809').own_occupation,null);
 assert.equal(v('F-P-0518-occupation_context-vicar1809').sergeant_witness_not_own_military_service,true);
 assert.equal(r('M-P-0389-C0851-witness-Andersson').name_literal,'Peter Anders[son?]');
 assert.equal(r('M-P-0389-C0851-witness-Andersson').role_literal,'S. Min[?]. Adjuncten H:r');
 return {ok:true,groups:10};
}
