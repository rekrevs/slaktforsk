import assert from 'node:assert/strict';
import {readCurrent,personView} from '../lib/domain.mjs';
// Fixed expectations from complete P0501–0508 acts/profiles and latest local
// C0262/0820/0830/0831/0837/0838/0841/0842/0858/0354 text, not packet-derived.
export function checkPersons11PartARisks(db){
 const r=id=>{const x=readCurrent(db,id);assert.ok(x,id);return x;},v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
 const parents=id=>db.prepare("select k.* from current_revision c join relation k on k.revision_id=c.id where c.disposition='accepted' and k.relation_type='parent' and k.to_person=?").all(id);
 const ownEvents=id=>db.prepare('select e.event_type,e.date_json,p.* from current_revision c join participation p on p.revision_id=c.id join current_revision ec on ec.object_id=p.event_id join event e on e.revision_id=ec.id where p.person_id=?').all(id);
 let groups=0;
 for(const id of ['P-0501','P-0507'])assert.equal(r(id).evidence_status,'CORROBORATED');
 for(const id of ['P-0502','P-0503','P-0504','P-0505','P-0506','P-0508'])assert.equal(r(id).evidence_status,'TRANSCRIBED');
 for(let n=501;n<=508;n++){const id=`P-0${n}`;assert.equal(r(id).disposition,'accepted');assert.equal(r(id).sex,null);assert.ok(personView(db,id).research.questions.length>0);}
 groups++;

 assert.equal(r('M-P-0501-C0820-own').name_literal,'Margaretha Sofia');assert.equal(r('M-P-0501-C0820-own').role_literal,'Dr');
 assert.equal(r('M-P-0501-C0262-own').name_literal,'Margareta Sofia Gabrielsdotter');assert.equal(d('E-birth-P-0501').value,'1842-07-30');
 assert.deepEqual(parents('P-0501').map(x=>x.from_person).sort(),['P-0289','P-0290']);assert.equal(r('REL-sibling-P-0020-P-0501').relation_type,'sibling');
 assert.equal(v('F-P-0501-family_context-primary-and-limits').grandmother_via,'P-0290');assert.deepEqual(v('F-P-0501-family_context-primary-and-limits').other_son_rows_birth_years,[1836,1840,1844]);groups++;

 const g=v('F-P-0501-kinship_report-Gabrielsson');assert.deepEqual(g.claimed_maternal_grandchildren,['Assar Gabrielsson','Börje Gabrielsson']);assert.equal(g.intermediate_daughter_unidentified,true);assert.equal(g.no_accepted_grandchild_edges,true);assert.equal(r('F-P-0501-kinship_report-Gabrielsson').evidence_status,'LEAD');
 assert.equal(v('F-P-0501-research_limits-own-life').AI8_not_volume_or_person_negative,true);assert.equal(v('F-P-0501-research_limits-own-life').PDF_photographs_are_Per_Wilhelm_and_Bernhard,true);assert.ok(ownEvents('P-0501').every(x=>!['death','marriage'].includes(x.event_type)));groups++;

 for(const id of ['P-0506','P-0507']){assert.equal(r(`M-C0841-${id}`).record_id,'R-1350fe75998068861ad4298a');const o=v(`O-${id}-C0841-own`);assert.equal(o.child_birth,'1810-07-20');assert.equal(o.child_baptism,'1810-07-20');assert.equal(o.home_preliminary,'Västerg. Djursätra');assert.equal(r(`REL-parent-${id}-P-0290`).nature,'recorded_parent');assert.equal(v(`F-${id}-research_limits-own-person`).no_Elias_death_interval_from_widow_title,true);}
 assert.equal(r('M-C0841-P-0506').name_literal,'Elias');assert.equal(v('F-P-0506-research_limits-own-person').surname_not_reconstructed,true);assert.equal(readCurrent(db,'E-birth-P-0506'),null);assert.ok(ownEvents('P-0506').every(x=>!['death','marriage'].includes(x.event_type)));groups++;

 assert.equal(d('E-birth-P-0507').precision,'year');assert.equal(d('E-birth-P-0507').value,'1779');assert.equal(r('M-C0820-Grete-Gabrielsdr').role_literal,'Moren Enk.');
 const greta=v('F-P-0507-household_membership-AI7-mother');assert.equal(greta.exact_birth_day_month_reserved,true);assert.equal(greta.deceased_spouse_identity_unknown,true);assert.equal(greta.book_period_not_exact_residence_or_survival,true);assert.equal(parents('P-0507').length,0);groups++;

 assert.equal(r('M-P-0502-C0830-own').name_literal,'Lars Larssons');assert.equal(r('M-P-0503-C0830-own').name_literal,'Anna Jonsd:r');assert.equal(v('F-P-0502-source_assessment-age-column').mother_age,27);assert.equal(v('F-P-0502-source_assessment-age-column').father_age_given,false);assert.equal(readCurrent(db,'E-birth-P-0502'),null);
 const anna=v('F-P-0503-birth_assessment-age27');assert.deepEqual(anna.reported_search_interval,{from:'1785-09',to:'1786-09'});assert.equal(anna.additional_search_year_possible,1784);assert.equal(anna.chosen_year,null);assert.equal(d('E-birth-P-0503').precision,'unknown');groups++;

 for(const id of ['P-0502','P-0503']){const se=r(`SEARCH-${id}-C0858-Gardtjarn`);assert.equal(se.source_id,'S-0672');assert.equal(se.outcome,'negative');const b=JSON.parse(se.scope_json).bounds;assert.equal(b.volume,'Sättna AI4');assert.equal(b.section,'Gårdtjärn');assert.equal(b.pages,'86–102');assert.equal(b.boundary_page,103);assert.equal(v(`F-${id}-source_assessment-Gardttjarn-Byn`).Byn_section_unsearched,true);assert.equal(v(`F-${id}-source_assessment-Gardttjarn-Byn`).target_home_not_corrected,true);}
 const no=r('O-P-0502-C0830-neighbor-Anders');assert.equal(no.record_id,'R-9b37c4f73bbf14ed3a0ff580');const nv=JSON.parse(no.value_json);assert.equal(nv.birth,'1813-10-02');assert.equal(nv.home_replacement,'Byn');assert.equal(nv.parents_literal,'T. Lars Jonssons och H. Stina Lisa Vallins');groups++;

 for(const key of ['Pahl','Lindgren','Nils','Greta','Johanna','Brita'])assert.equal(r(`M-C0830-witness-${key}`).record_id,'R-634df506ea8656f8b52add26');
 assert.equal(r('M-C0830-witness-Johanna').role_literal,'D:o');assert.equal(v('O-C0830-witness-Johanna').ditto_title_interpretation,null);
 assert.equal(v('F-P-0503-kinship_assessment-Jonsson-neighborhood').no_quantitative_chance_estimate_justified,true);assert.equal(v('F-P-0503-kinship_assessment-Jonsson-neighborhood').no_parent_or_sibling_identified,true);assert.equal(parents('P-0502').length,0);assert.equal(parents('P-0503').length,0);groups++;

 for(const id of ['P-0503','P-0505'])assert.equal(v(`F-${id}-source_assessment-maternal-survival`).survival_after_delivery_not_established_by_silence,true);
 assert.equal(v('F-P-0503-source_assessment-maternal-survival').other_child_death_not_maternal_reporting_rule,true);assert.equal(v('F-P-0505-source_assessment-maternal-survival').stillbirth_record_not_maternal_reporting_rule,true);groups++;

 assert.equal(r('M-P-0504-C0838-own').role_literal,'Bond.');assert.equal(r('M-P-0505-C0838-own').role_literal,'hu');assert.equal(readCurrent(db,'E-birth-P-0504'),null);
 for(const id of ['P-0504','P-0505']){assert.equal(v(`F-${id}-residence-Wiiklo1796`).home_literal,'Wiiklo[?]');assert.equal(v(`F-${id}-residence-Wiiklo1796`).modern_place_identity,null);assert.equal(v(`F-${id}-source_assessment-age-column`).mother_age,38);assert.equal(v(`F-${id}-source_assessment-age-column`).father_age_given,false);}
 const b=v('F-P-0505-birth_assessment-age38');assert.deepEqual(b.reported_search_interval,{from:'1757-10',to:'1758-10'});assert.equal(b.additional_search_year_possible,1756);assert.equal(d('E-birth-P-0505').precision,'unknown');groups++;

 for(const id of ['P-0504','P-0505']){assert.equal(v(`F-${id}-kinship_assessment-witnesses`).no_patronymic_match_not_kinship_exclusion,true);assert.equal(v(`F-${id}-kinship_assessment-witnesses`).affinal_or_maternal_kinship_not_excluded,true);assert.equal(parents(id).length,0);}
 assert.equal(r('M-P-0360-C0838-witness-Anders-Andersson').name_literal,'Anders And[ers]son');assert.equal(v('O-P-0360-C0838-witness-Lena-Andersdotter').home_literal,'ibid');
 assert.equal(r('EP-E-birth-P-0360-P-0504-father').role,'father');assert.equal(r('EP-E-baptism-P-0360-P-0505-mother').role,'mother');assert.equal(d('E-baptism-P-0360').value,'1796-10-30');groups++;

 assert.equal(r('M-P-0508-C0842-own').record_id,'R-a16f5104a561a23ef1ddde84');assert.equal(r('M-P-0508-C0842-own').name_literal,'Brita Hillberg');assert.equal(d('E-birth-P-0508').value,'1805-05-13');assert.equal(r('E-birth-P-0508').place_id,null);
 const forsa=v('F-P-0508-place_assessment-Forsa-candidate');assert.equal(forsa.reading_candidate,'Forsa[?]');assert.equal(forsa.confirmed_birthplace,null);assert.equal(r('F-P-0508-place_assessment-Forsa-candidate').evidence_status,'LEAD');assert.deepEqual(forsa.incompatible_comparison_forms,['Njutånger','Hudiksvall','Stockholm','Mo']);groups++;

 const church=v('O-P-0508-C0842-own-church');assert.deepEqual(church.annual_marks_present,[1857,1858,1859,1860,1861]);assert.deepEqual(church.examples,[{year:1857,literals:['12/1','19/10']},{year:1861,literals:['21/7']}]);assert.equal(church.small_dates_reserved,true);
 assert.equal(v('F-P-0508-life_scope-own-annual-marks').survival_into1861_supported_by_marks,true);assert.equal(v('F-P-0508-life_scope-own-annual-marks').no_survival_after1861_proven,true);assert.equal(v('F-P-0508-life_scope-own-annual-marks').continuous_physical_residence_not_proven,true);
 assert.equal(v('O-P-0508-C0842-own-knowledge').reading_mark,'a');assert.deepEqual(v('O-P-0508-C0842-own-knowledge').following_three_marks,['ab','ab','ab']);groups++;

 assert.equal(r('M-P-0508-C0842-Olof-context').record_id,'R-eacc3975efcfe16f97ed8488');assert.equal(v('O-P-0508-C0842-Olof-context').birth_reported,'1832-01-06');assert.equal(v('O-P-0508-C0842-Olof-context').birth_parish,'Hudiksvall');assert.equal(v('O-P-0508-C0842-Olof-context').wife_birth_year,1839);
 assert.equal(r('F-P-0508-kinship_assessment-Olof-candidate').evidence_status,'LEAD');assert.equal(v('F-P-0508-kinship_assessment-Olof-candidate').relation_accepted,false);assert.equal(readCurrent(db,'ID-P-0508-C0842-Olof-context'),null);groups++;

 const family=v('F-P-0508-family_context-own-and-grandchildren');assert.equal(family.son_birthplace_latest,'Njutånger');assert.equal(family.Per_Eric_death_latest_reported,'1859-09-15');assert.equal(family.widow_spouse_not_automatically_sons_father,true);assert.equal(family.no_widowhood_date_before1857_proven,true);assert.equal(family.pigan_Brita_Chr_Hillberg_witness_not_identified_as_own,true);assert.equal(parents('P-0508').length,0);assert.deepEqual(parents('P-0350').map(x=>x.from_person),['P-0508']);assert.ok(ownEvents('P-0508').every(x=>!['death','marriage'].includes(x.event_type)));groups++;
 return {ok:true,groups};
}
