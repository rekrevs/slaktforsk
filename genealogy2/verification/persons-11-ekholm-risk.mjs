import assert from 'node:assert/strict';
import {readCurrent,personView} from '../lib/domain.mjs';
// Expected values are grounded in the complete source texts and their dated
// corrections (C0952/54/55/57, C0972/73/76, C0919), not copied from the packet.
export function checkPersons11EkholmRisks(db){
 const r=id=>{const x=readCurrent(db,id);assert.ok(x,id);return x;},v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
 const edges=(id,type)=>db.prepare("select k.* from current_revision c join relation k on k.revision_id=c.id where c.disposition='accepted' and k.relation_type=? and (k.from_person=? or k.to_person=?)").all(type,id,id);
 const ownEvents=id=>db.prepare('select e.event_type,e.date_json,p.* from current_revision c join participation p on p.revision_id=c.id join current_revision ec on ec.object_id=p.event_id join event e on e.revision_id=ec.id where p.person_id=?').all(id);
 let groups=0;
 for(const id of ['P-0532','P-0533','P-0534']){assert.equal(r(id).evidence_status,'CORROBORATED');assert.equal(r(id).disposition,'accepted');assert.equal(r(id).sex,null);assert.ok(personView(db,id).research.questions.length>0);}
 groups++;

 const birth=v('F-P-0532-birth_assessment-three-years');
 assert.equal(birth.reported_date,'1878-02-17');assert.equal(birth.census_original_year,1881);assert.equal(birth.census_index_year,1887);assert.equal(birth.chosen_birth,null);assert.equal(birth.own_birth_record_unread,true);assert.equal(birth.old_resolution_revoked,true);assert.equal(r('F-P-0532-birth_assessment-three-years').evidence_status,'CONFLICT');assert.equal(d('E-birth-P-0532').precision,'unknown');
 assert.equal(r('M-P-0532-C0954-original').record_id,'R-8dbc2cebc0b43d681dbd941d');assert.equal(r('M-P-0532-C0954-index').record_id,'R-57d0fb4d38de5d9ddf259ef0');assert.equal(r('M-P-0532-C0954-original').name_literal,'Ekholm, Axel Vilhelm');assert.equal(r('M-P-0532-C0954-index').name_literal,'Ekholm, Axel Wilhelm');groups++;

 assert.equal(d('E-death-P-0532').value,'1913-03-11');assert.equal(d('E-burial-P-0532').value,'1913-03-17');
 const death=v('F-P-0532-death_context-Helgesta');assert.equal(death.death_place,'Helgesta');assert.equal(death.burial_place,'Helgesta');assert.equal(death.registered_parish,'Katarina, Stockholm');assert.equal(death.recording_parish,'Hyltinge');assert.equal(death.cause_literal,'Lungsot');assert.equal(death.age_conditional_on_reported1878_birth,true);assert.equal(death.why_in_Helgesta_unknown,true);
 const rawDeath=v('O-P-0532-C0952-own');assert.equal(rawDeath.counted_in_parish_literal,'–');assert.equal(rawDeath.married_column,'1');assert.equal(rawDeath.note_literal,'F. m. f. 77. Attest om begrafn. d. Helgesta ¹⁷/₃ 13');groups++;

 assert.equal(r('M-P-0532-C0955-rote23').record_id,'R-689c9cf06d35ed71e5b1e14e');assert.equal(r('M-P-0532-C0955-rote14').record_id,'R-e3ea1b8755f3c260cc78744a');
 const k=v('O-P-0532-C0955-rote23'),s=v('O-P-0532-C0955-rote14');assert.equal(k.arrival,'1910-10-07');assert.equal(k.departure,'1911-09-27');assert.equal(k.from_rote,'27');assert.equal(k.to_rote,'04');assert.equal(k.floor_literal,'Hyr');assert.equal(s.arrival,'1912-12-23');assert.equal(s.from_rote,'10');assert.equal(s.closed,'1913-03-11');assert.equal(s.closure_reason_literal,'Död');assert.equal(s.household_head_literal,'Göth');assert.equal(s.note_literal,'Betyget Felutskr från Rote 4 Ti Ll Rote 10');
 assert.ok(!ownEvents('P-0532').some(x=>x.event_type==='registered_departure'&&JSON.parse(x.date_json).value==='1913-03-11'));groups++;

 const route=v('F-P-0532-residence-reported-route');assert.deepEqual(route.unread_rote_posts,['27','04','10']);assert.equal(route.child_Matteus_births_not_own_address,true);assert.equal(route.inlodging_does_not_prove_economic_decline,true);assert.equal(route.no_continuous_1897_1903_or_1903_1910_residence_proven,true);assert.equal(v('F-P-0532-occupation-locomotive-fireman').SJ_not_proven,true);assert.equal(v('F-P-0532-occupation-locomotive-fireman').continuous_ten_years_work_not_proven,true);groups++;

 assert.equal(r('E-P0016-marriage1903').version,1);assert.equal(d('E-P0016-marriage1903').value,'1903-05-01');assert.equal(r('EP-marriage-P-0532').event_id,'E-P0016-marriage1903');assert.equal(r('REL-P0016-P0532').version,1);
 const mil=v('F-P-0532-military_registration-civil-records');assert.deepEqual(mil.banns_second_number_alternatives,[124,128]);assert.equal(mil.first_number,264);assert.equal(mil.service_not_proven,true);assert.equal(v('O-P-0532-C0976-banns').knowledge_literal,'godkänd');assert.equal(v('O-P-0532-C0976-marriage').home_literal,'Vestmg. 72');groups++;

 const banns=v('F-P-0532-source_assessment-banns-month');assert.deepEqual(banns.days,[5,12,19]);assert.equal(banns.month_not_explicit,true);assert.equal(banns.chosen_raw_month,null);assert.equal(banns.Sunday_pattern_alone_not_unique,true);assert.equal(banns.July1903_also_matches_Sundays,true);
 for(const day of ['05','12','19']){const id=`E-banns-P-0016-P-0532-1903-04-${day}`;assert.equal(r(id).version,1);assert.equal(d(id).value,`1903-04-${day}`);}
 const cert=v('F-P-0532-source_assessment-certificate1903');assert.equal(cert.date_reported,'1903-05-06');assert.equal(cert.person_column_unresolved,true);assert.equal(cert.no_own_migration_inferred,true);assert.ok(!ownEvents('P-0532').some(x=>JSON.parse(x.date_json).value==='1903-05-06'));groups++;

 const chain=v('F-P-0532-source_assessment-widow-chain');assert.deepEqual(chain.folios,[932,744,736,497,83]);assert.equal(chain.one_administrative_chain,true);assert.equal(chain.no_living_presence_in1933_1955,true);assert.equal(chain.C0976_three_documents_same_registration_chain,true);assert.equal(chain.C0919_widow_field_reading,'13 ⁴/₃');assert.equal(chain.other_widow_fields,'13 ¹¹/₃');assert.equal(chain.reading_or_record_discrepancy_unresolved,true);assert.equal(chain.contract_review_not_upgraded,true);
 assert.equal(r('M-P-0532-C0972-late-spouse').record_id,'R-86e25c6dd1c2141e8454c02e');assert.equal(r('M-P-0532-C0973-late-spouse-497').record_id,'R-f39c0fec6478a29ae3e60fb7');groups++;

 const children=edges('P-0532','parent');assert.deepEqual(children.map(x=>x.to_person).sort(),['P-0533','P-0534']);assert.ok(children.every(x=>x.from_person==='P-0532'&&x.nature==='recorded_parent'));assert.equal(v('F-P-0532-family_context-spouse-children').Huldas1920_1921_daughters_not_his,true);
 for(const id of ['P-0533','P-0534'])assert.deepEqual(edges(id,'parent').filter(x=>x.to_person===id).map(x=>x.from_person).sort(),['P-0016','P-0532']);groups++;

 assert.equal(r('M-P-0533-C0954-own').name_literal,'Axel Ivar');assert.equal(r('M-P-0533-C0954-own').role_literal,'s.');assert.equal(r('M-P-0534-C0954-own').name_literal,'Ingrid Amalia');assert.equal(r('M-P-0534-C0954-own').role_literal,'');
 for(const[id,date,record]of[['P-0533','1907-03-09','R-f9a2b7cc4c1c0208b7d245bb'],['P-0534','1910-02-05','R-1167e7918d6e192f5433555e']]){assert.equal(r(`M-${id}-C0955-own`).record_id,record);assert.equal(d(`E-birth-${id}`).value,date);assert.equal(v(`F-${id}-birth_report-Matteus`).own_birth_record_read,false);assert.equal(v(`O-${id}-C0955-own`).status_literal,'Ogift, Barn inom äktenskapet');assert.equal(readCurrent(db,`E-baptism-${id}`),null);}
 groups++;

 for(const id of ['P-0533','P-0534']){assert.equal(r(`M-${id}-C0919-own`).record_id,'R-88c4d51debd66f79529f0e5b');assert.equal(r(`EP-E-registered_departure-P-0016-Helgesta1913-${id}-migrant`).event_id,'E-registered_departure-P-0016-Helgesta1913');assert.equal(v(`F-${id}-family_context-birth-household`).Maj_father,'P-0015');assert.equal(v(`F-${id}-family_context-birth-household`).father_not_propagated_to_half_sisters,true);}
 assert.equal(d('E-registered_departure-P-0016-Helgesta1913').value,'1913-09-12');assert.equal(r('REL-sibling-P-0533-P-0534').nature,'recorded_sibling');assert.equal(r('REL-sibling-P-0007-P-0534').nature,'maternal_sibling');groups++;

 const neg=r('SEARCH-P-0533-C0957-Matteus1907');assert.equal(neg.source_id,'S-0747');assert.equal(neg.outcome,'negative');const bounds=JSON.parse(neg.scope_json).bounds;assert.equal(bounds.posts,'129–182');assert.equal(bounds.pages,'87–93');assert.deepEqual(bounds.baptism_dates,{from:'1907-03-15',to:'1907-04-11'});assert.deepEqual(bounds.birth_dates,{from:'1907-01-11',to:'1907-04-08'});assert.deepEqual(bounds.separate_control_pages,[97,99,101,104,179]);
 assert.equal(v('F-P-0533-source_assessment-birth-search-bounds').five_dates_March10_to14_not_six,true);assert.equal(v('F-P-0533-source_assessment-birth-search-bounds').no_statistical_normal_baptism_interval_proven,true);assert.equal(v('F-P-0534-source_assessment-birth-search-bounds').own_birth_search_performed,false);assert.equal(v('F-P-0534-source_assessment-birth-search-bounds').sister_has_no_negative_search,true);assert.equal(readCurrent(db,'SEARCH-P-0534-C0957-Matteus1907'),null);groups++;

 const early=v('O-P-0533-C0972-own'),late=v('O-P-0533-C0973-497-own');assert.equal(early.military_literal,'frik.');assert.equal(late.military_literal,'Frik.');assert.equal(early.arrival_year,1933);assert.equal(early.arrival_from_folio,1041);assert.equal(early.departure,'1936-12-08');assert.equal(early.departure_folio,687);assert.equal(early.banns_literal,'Lysn. 8/1936');assert.equal(late.arrival_from_folio_reading,'976');assert.equal(late.arrival_from_folio_reserved,true);assert.equal(late.arrival,'1949-01-14');
 assert.equal(r('M-P-0533-C0973-497-own').record_id,'R-f09fab86f6d8a7a845113b6c');assert.equal(v('F-P-0533-occupation-adult-anchors').no_continuous_sea_service1926_1933_proven,true);assert.equal(v('F-P-0533-residence-Stockholm1924-1926').individual_post_id_not_recorded,true);groups++;

 const wife=v('F-P-0533-family_context-adult');assert.equal(wife.spouse_name,'Ingegärd Regina Lindblom');assert.equal(wife.spouse_birth,'1912-06-26');assert.equal(wife.spouse_birth_parish,'Flen');assert.equal(wife.marriage_year,1936);assert.equal(wife.chosen_marriage_day,null);assert.deepEqual(wife.wifes_date_components,['36 ³/₅','³/₅']);assert.equal(d('E-marriage-P-0533').precision,'year');assert.equal(d('E-marriage-P-0533').value,'1936');assert.deepEqual(wife.child,{birth_year:1943,birth_place:'Flen',role_literal:'s.'});assert.equal(wife.child1938_not_assigned_to_this_couple,true);assert.equal(wife.child1938_prefix_d_vs_s_unresolved,true);groups++;

 assert.equal(r('M-P-0534-C0973-497-own').record_id,'R-bd5e8ee5f87a72bf5ffb904a');assert.equal(r('M-P-0534-C0973-497-own').name_literal,'Johansson f. Ekholm, Ingrid Amalia');assert.equal(r('M-P-0534-C0973-497-own').role_literal,'fru');assert.equal(r('M-P-0534-C0973-83-own').record_id,'R-bc999d0e593f532d8f48404a');
 const husband=v('F-P-0534-family_context-adult');assert.equal(husband.spouse_name,'Allan Gerald Johansson');assert.equal(husband.spouse_birth,'1899-02-10');assert.equal(husband.spouse_occupation,'handlande');assert.equal(husband.own_occupation_not_given,true);assert.equal(husband.marriage_place_unknown,true);assert.equal(d('E-marriage-P-0534').value,'1942-03-02');assert.equal(r('E-marriage-P-0534').place_id,null);assert.equal(d('E-registered_arrival-P-0534-Flen1950').value,'1950-01-03');assert.deepEqual(husband.child,{birth_year:1940,birth_place:'Solna',role_literal:'s.'});assert.equal(husband.no_paternity_or_civil_status_inferred_from_child_year,true);groups++;

 for(const id of ['P-0533','P-0534']){const scope=v(`F-${id}-life_scope-gaps-and-minimization`);assert.equal(scope.same_property_folio_not_same_apartment,true);assert.equal(scope.no_shared_economy_or_care_day_proven,true);assert.equal(scope.no1955_survival_from_book_period,true);assert.equal(scope.child_name_and_exact_birth_date_omitted,true);assert.equal(scope.continuous_life_line_not_proven,true);assert.equal(v(`F-${id}-residence-recorded-anchors`).next_transfer_year_unknown,true);assert.equal(readCurrent(db,`E-death-${id}`),null);}
 assert.equal(v('F-P-0534-name_form-recorded-and-search').Johansson_surname_explicit_in_C0973,true);assert.equal(v('F-P-0534-research_limits-military-generalization').male_conscription_rule_not_exclusion_of_all_military_information,true);groups++;
 return {ok:true,groups};
}
