import assert from 'node:assert/strict';
import {readCurrent,personView} from '../lib/domain.mjs';

// Expectations chosen from complete local dossiers and citation texts, including
// C0593/0623/0678 corrections, C0606's four columns and C0543's row boundaries.
// The checks deliberately do not derive expected values from migration packets.
export function checkPersons10PartARisks(db) {
 const r=id=>{const x=readCurrent(db,id);assert.ok(x,id);return x;};
 const v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
 const acceptedParents=id=>db.prepare("SELECT t.* FROM current_revision c JOIN relation t ON t.revision_id=c.id WHERE c.disposition='accepted' AND t.relation_type='parent' AND t.to_person=?").all(id);
 const ownEvents=id=>db.prepare('SELECT e.event_type,e.date_json,p.role,p.event_id FROM current_revision c JOIN participation p ON p.revision_id=c.id JOIN current_revision ec ON ec.object_id=p.event_id JOIN event e ON e.revision_id=ec.id WHERE p.person_id=?').all(id);
 let groups=0;
 for(const id of ['P-0454','P-0455','P-0457','P-0458','P-0459','P-0460','P-0461','P-0462'])assert.equal(r(id).evidence_status,'TRANSCRIBED',id);
 for(const id of ['P-0451','P-0452','P-0456','P-0463','P-0464','P-0465'])assert.equal(r(id).evidence_status,'CORROBORATED',id);
 groups++;

 const hb=v('F-P-0451-birth_assessment-three-forms');
 assert.equal(hb.household_date,'1796-11-02');assert.equal(hb.Familia_AI2_s27,'1796-11-08');assert.equal(hb.Nyberg_year,1797);assert.equal(hb.birthplace_chosen,null);
 assert.equal(v('O-P-0451-C0593-biography').rows[0].name,'Henric Winroht');
 assert.equal(v('F-P-0451-occupation-source-sequence').monotonic_later_name_change_proven,false);
 assert.equal(v('O-P-0451-C0626-own').right_page_year_fields_outside_crop,true);groups++;

 const list=v('F-P-0451-family_context-overlapping-child-lists');
 assert.deepEqual(list.original_C0624.map(c=>c.birth),['1819-02-12','1824-03-13','1826-01-02']);
 assert.equal(list.register_count,8);assert.equal(list.Familia_links,6);assert.equal(list.not_eleven_distinct_children,true);assert.equal(list.lifetime_total_unknown,true);
 assert.deepEqual(list.Ingrid_Stina_Familia_dates,['1828-01-12','1828-01-18']);assert.equal(list.Ingrid_departure1864_not_fathers,true);groups++;

 assert.equal(d('E-marriage-P-0451-P-0452-1819').value,'1819-10-31');
 assert.equal(r('E-marriage-P-0451-P-0452-1819').evidence_status,'CONFLICT');
 assert.equal(r('E-death-P-0451').disposition,'candidate');assert.equal(d('E-death-P-0451').value,'1875-01-05');
 assert.equal(v('F-P-0451-source_assessment-own-life-limits').dissolution1850_02_13_is_Britas_death,false);
 assert.equal(v('F-P-0452-source_assessment-own-life-limits').not_Britas_death_date,true);
 assert.ok(ownEvents('P-0452').every(x=>x.event_type!=='death'));groups++;

 const brita=v('F-P-0452-birth_assessment-December-variants');
 assert.deepEqual(d('E-birth-P-0452').values,['1795-12-06','1795-12-08']);
 assert.equal(brita.original_AI2_s28_day_unreadable_after_test,true);assert.equal(brita.Ljustorp_database_field,'boendeförsamling');
 assert.equal(Object.hasOwn(v('O-P-0452-C0854-s28'),'birth'),false);
 assert.equal(v('F-P-0452-household_membership-service-context').none_identified_as_parents,true);
 assert.equal(acceptedParents('P-0452').length,0);groups++;

 const birthSearch=r('SEARCH-P-0452-Ljustorp-birth1795');assert.equal(birthSearch.source_id,'S-0517');
 assert.equal(JSON.parse(birthSearch.scope_json).query,'Brita/Britta född6eller8dec1795');
 const lack=v('F-P-0451-source_assessment-own-life-limits');assert.equal(lack['1797_full_year_negative'],false);assert.equal(lack.AI2damaged_page15_negative,false);assert.equal(lack.C0678_linked_files_present,41);assert.equal(lack.C0678_extra_openings_missing,4);
 assert.deepEqual(JSON.parse(r('SEARCH-P-0461-family98-birth-years').scope_json).bounds.years,[1796,1801,1804]);groups++;

 for(const id of ['P-0461','P-0462']){
  const rel=r(`REL-parent-${id}-P-0451`);assert.equal(rel.disposition,'candidate');assert.equal(rel.evidence_status,'CONFLICT');
  assert.equal(v(`F-${id}-identity_assessment-register-person`).original_person_identified,false);
  assert.equal(v(`F-${id}-source_route-conditional-mantal`).mantal1772_1800_names_men_only,true);
 }
 assert.equal(acceptedParents('P-0451').length,0);assert.equal(r('REL-spouse-P-0461-P-0462').disposition,'candidate');
 assert.equal(v('O-P-0462-C0623-f98').death_literal,'18');assert.ok(ownEvents('P-0462').every(x=>x.event_type!=='death'));
 assert.equal(v('O-P-0461-C0678-other-Marten').father,'Anders Olofsson');assert.equal(readCurrent(db,'ID-P-0461-C0678-other-Marten'),null);groups++;

 assert.equal(r('P-0454').display_name,'Jonas Schölin');assert.equal(r('M-P-0454-C0606-father').name_literal,'Jonas Schölin');
 const name=v('F-P-0454-name_assessment-Jonas-correction');assert.equal(name.rejected_transcription,'James Schölin');assert.equal(name.English_manufacturing_environment_hypothesis_withdrawn,true);
 assert.equal(r('SEARCH-P-0454-C0608-James').outcome,'negative');assert.equal(JSON.parse(r('SEARCH-P-0454-C0608-James').scope_json).query.given_name,'James');
 for(const key of ['Maria968','Ladugard1959']){assert.equal(r(`ID-P-0454-C0608-${key}`).decision,'candidate');assert.equal(r(`ID-P-0454-C0608-${key}`).disposition,'candidate');}
 assert.equal(v('F-P-0454-candidate_context-C0608-six-index-rows').rows.length,6);groups++;

 assert.equal(r('REL-parent-P-0454-P-0339').nature,'recorded_parent');assert.equal(r('REL-foster_parent-P-0455-P-0339').nature,'recorded_foster_parent');
 assert.ok(acceptedParents('P-0339').every(x=>x.from_person!=='P-0455'));
 const roll=v('F-P-0454-source_assessment-roll2532-columns');assert.equal(roll.columns.length,4);assert.equal(roll.columns[0].content.bottom,'1849 Aug');
 assert.deepEqual(roll.columns[0].content.days,['21','15']);assert.equal(roll.columns[2].content.amount,20);assert.equal(roll.columns[3].content.year_prefix,'18');
 assert.equal(roll.no_end_move_or_death_date_from_bottom,true);assert.equal(v('F-P-0454-source_assessment-own-life-limits').child_age_in_June1831_completed_years,5);groups++;

 const net=v('F-P-0455-network_assessment-Lofberg1856');assert.equal(net.distribution.Lofberg_ditto_interpretation,9);assert.equal(net.own_name_absent,true);assert.equal(net.Anna_Nilsdotter.relation_accepted,false);assert.equal(net.stillborn_twin_not_baptized,true);
 assert.equal(net.village_network_does_not_prove_personal_foster_relation_continued,true);
 const money=v('F-P-0455-economic_assessment-maintenance');assert.equal(money.payment_not_proven,true);assert.equal(money.no_end_date_proven,true);assert.deepEqual(money.child_age_Aug1849_range,[23,24]);
 assert.ok(ownEvents('P-0455').every(x=>!['death','marriage','baptism'].includes(x.event_type)));groups++;

 assert.equal(d('E-birth-P-0456').value,'1857-04-20');
 const place=v('F-P-0456-birth_assessment-corrected-date-place');assert.equal(place.rejected_misreading,'1857-07-24');assert.equal(place.Rundb_in_C0469_C0519_is_fathers_birthplace,true);assert.equal(place.own_Rundbacken_birthplace_not_proven,true);
 assert.equal(v('O-P-0456-C0543-adult').from,'G.B. 222');assert.equal(r('ID-P-0456-C0621-Hinkestorpet').disposition,'candidate');
 assert.equal(d('E-marriage-P-0456-P-0457-1881').precision,'unknown');assert.equal(v('F-P-0456-marriage_assessment-C0543').tentative_date,'1881-04-09');groups++;

 const gaps=v('F-P-0456-family_assessment-birth-intervals');
 assert.deepEqual(gaps.dates,['1881-08-09','1887-07-02','1891-02-22']);
 assert.deepEqual(gaps.intervals,[{years:5,months:10,days:23},{years:3,months:7,days:20}]);
 assert.equal(gaps.wedding_calculation_conditional,true);assert.equal(gaps.two_intervals_not_norm,true);assert.equal(gaps.household_can_include_dead_children,true);assert.equal(gaps.year_boundaries_1881_1887_not_exhausted_by_middle_years,true);assert.equal(gaps.search_not_done,true);groups++;

 assert.equal(v('F-P-0457-birthplace-reported-Indal').not_continuous_residence1855_1881,true);
 assert.equal(v('F-P-0457-source_assessment-own-life-limits').Ingrid_Gustafva_Henriksson_not_attested,true);
 const sons=[['P-0458','Erik Petter','1881-08-09'],['P-0459','Johan Vilhelm','1887-07-02'],['P-0460','Anders Jonas','1891-02-22']];
 for(const [id,name,birth] of sons){assert.equal(r(`M-${id}-C0543-child`).name_literal,name);assert.equal(r(`M-${id}-C0543-child`).role_literal,'');assert.equal(d(`E-birth-${id}`).value,birth);assert.equal(v(`O-${id}-C0543-child`).own_birthplace_not_extracted,true);assert.deepEqual(acceptedParents(id).map(x=>x.from_person).sort(),['P-0456','P-0457']);assert.ok(ownEvents(id).every(x=>!['registered_departure','baptism'].includes(x.event_type)));}
 groups++;

 const youngest=v('F-P-0460-source_assessment-own-life-limits');assert.deepEqual(youngest.mother_age_from_dates,{years:35,months:10,days:12});assert.equal(youngest.military_route_estimated_year,1912);assert.equal(youngest.relation_row_age32_is_error,true);
 assert.equal(v('F-P-0458-name_assessment-individual-pattern').sole_matching_child_claim_false_Anders_Jonas_also_matches,true);
 assert.equal(v('F-P-0460-name_assessment-individual-pattern').Jonas_not_only_repeated_name_Erik_Petter_also_repeat,true);groups++;

 for(const [id,name,date] of [['P-0463','Jonas','1835-01-01'],['P-0464','Cecilia','1836-02-14']]){
  assert.equal(d(`E-birth-${id}`).value,date);const ep=r(`EP-C0470-${name}`);assert.equal(ep.person_id,id);assert.equal(ep.event_id,'E-baptism-P-0394');assert.equal(ep.role,'witness');
  const grade=v(`F-${id}-source_assessment-kinship-grade`);assert.equal(grade.only_explicit_kinship_source,'Nyberg familj99 C0623');assert.equal(grade.relations_withdrawn,false);assert.equal(grade.familia_parent_label,'ej bestämd');assert.equal(grade.no_biological_inference,true);
  assert.equal(v(`F-${id}-source_assessment-own-life-limits`).Bredsjo_is_residence_not_birthplace,true);
 }
 assert.equal(r('REL-sibling-P-0463-P-0464').nature,'recorded_sibling');groups++;

 assert.equal(v('F-P-0463-source_assessment-later-Rundbacken').database_C0593.destination,'Ljustorp');assert.equal(v('F-P-0464-source_assessment-later-Rundbacken').database_C0593.destination,'Sundsvall');
 assert.equal(d('E-registered_departure-P-0463-1860').value,'1860');assert.equal(d('E-registered_departure-P-0464-1860').value,'1860');
 assert.equal(r('M-P-0463-C0704-candidate').name_literal,'Höglin, Jonas');assert.equal(r('ID-P-0463-C0704-candidate').disposition,'candidate');assert.equal(v('O-P-0463-C0704-candidate').reference,'Ljustorp P. 2 nr 7');assert.equal(v('F-P-0463-identity_assessment-C0704-candidate').register_year_not_proof_alive,true);assert.ok(ownEvents('P-0463').every(x=>x.event_type!=='death'));groups++;

 assert.equal(d('E-marriage-P-0346-P-0465-1906').value,'1906-07-14');assert.equal(r('E-marriage-P-0346-P-0465-1906').place_id,null);
 assert.equal(r('EP-E-marriage-P-0346-P-0465-1906-P-0465-principal').person_id,'P-0465');assert.equal(d('E-registered_arrival-P-0465').value,'1906-06-22');
 const nyberg=v('O-P-0465-C0657-bride');assert.equal(nyberg.rejected_reading,'barnmorska?');assert.equal(nyberg.marriage_type,'borgerligt');assert.equal(nyberg.both_marriage_number,1);assert.equal(nyberg.own_note,'baptist');
 assert.equal(v('O-P-0465-C0654-row9').community_note_literal,'utträde t. baptistsamfundet 14[?]/2 87');assert.ok(ownEvents('P-0465').every(x=>x.event_type!=='baptism'));groups++;

 const next=v('F-P-0465-residence_assessment-Hogsjo-route');assert.equal(next.next_book_page,138);assert.equal(next.not_same_book_Jonas_page138,true);
 const access=v('F-P-0465-source_route-B2-access');assert.equal(access.own1906_entry_not_read,true);assert.equal(access.no_current_volume_wide_block_proven,true);assert.equal(access.no_own_migration_negative,true);
 assert.equal(v('F-P-0465-source_assessment-own-life-limits').Hoglund_not_own_attested_name,true);
 assert.equal(acceptedParents('P-0465').length,0);groups++;

 // These remain active real persons despite failed contracts and unresolved lines.
 for(const id of ['P-0454','P-0455','P-0461','P-0462','P-0463','P-0464','P-0465']){
  assert.equal(r(id).disposition,'accepted');assert.ok(personView(db,id).research.questions.length>0);
 }
 groups++;
 return {ok:true,groups};
}
