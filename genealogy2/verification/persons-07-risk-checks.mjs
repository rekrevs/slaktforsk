import assert from 'node:assert/strict';
import {readCurrent,inspect} from '../lib/domain.mjs';

// Sakprov mot de genomlästa källornas skillnader, även när äldre aktprosa
// ger ett starkare eller annat besked. Körs efter faktisk SQLite-införsel.
export function checkPersons07Risks(db) {
 const current=id=>{const r=readCurrent(db,id);assert.ok(r,`Saknat objekt ${id}`);return r;};
 const value=id=>JSON.parse(current(id).value_json);
 const date=id=>JSON.parse(current(id).date_json);
 const participants=id=>db.prepare('SELECT p.* FROM current_revision r JOIN participation p ON p.revision_id=r.id WHERE p.event_id=?').all(id);
 const acceptedParents=id=>db.prepare("SELECT * FROM current_relation WHERE to_person=? AND relation_type='parent' AND disposition='accepted'").all(id);
 let groups=0;
 // C0467:s sena Samuel/Eugén-rättelser; bruden fyller19dagen efter vigseln.
 assert.equal(date('E-birth-P-0311').value,'1843-09-27');
 assert.equal(value('F-P-0311-source_correction-marriage-ages').bride.completed_years,18);
 assert.equal(value('F-P-0311-source_correction-marriage-ages').groom.completed_years,36);
 const childhood=value('F-P-0311-family_context-childhood');
 assert.equal(childhood.siblings.find(s=>s.person==='P-0393').birth,'1846-11-03');
 assert.match(childhood.siblings.find(s=>s.person==='P-0390').name,/Samuel/);
 assert.equal(value('F-P-0311-residence-anchors-and-gap').possible_move.own_move_established,false);
 assert.equal(value('F-P-0311-family_context-seven-known-births').causal_link_to_mother_death_established,false);
 assert.equal(value('F-P-0311-death_context-1874').modern_diagnosis,null);groups++;
 // C0365 gäller fel födelsemånad. C0557 skiljer moderns samtycke från egen hand.
 assert.equal(date('E-birth-P-0312').value,'1844-08-28');
 assert.equal(date('E-marriage-P-0312-P-0313-1870').value,'1870-10-14');
 assert.equal(value('F-P-0312-marriage_context-consent').own_signature_or_literacy_proven,false);
 assert.equal(value('F-P-0312-death_context-1920').physical_death_place,null);
 assert.equal(value('F-P-0312-property_reference-Gaddestad1').individual_share_proven,false);
 assert.equal(value('F-P-0313-birth_context-home-and-age').mother_age_confirmed,false);
 assert.equal(date('E-death-P-0313').value,'1891-04-01');
 assert.equal(date('E-burial-P-0313').value,'1891-04-12');
 assert.equal(value('F-P-0313-source_correction-dates-and-ages').completed_years_at_death,41);
 assert.equal(value('F-P-0313-source_correction-dates-and-ages').youngest_child.completed_years_at_mothers_death,7);
 assert.equal(value('F-P-0314-birth_assessment-household-only').birth_record_read,false);
 assert.equal(value('F-P-0314-life_scope-own-row-boundaries').departure_date,null);
 assert.equal(value('F-P-0314-life_scope-own-row-boundaries').alive_in1906_proven,false);
 assert.equal(value('F-P-0314-source_route-parental-probates').own_survival_to1920_proven,false);groups++;
 // C0511 är lysning; C0274:s senare folio85 och verkliga, bevarade vittneslista.
 assert.equal(date('E-birth-P-0315').value,'1836-12-27');
 assert.equal(date('E-baptism-P-0315').value,'1836-12-28');
 assert.equal(date('E-burial-P-0315').value,'1904-12-18');
 assert.equal(value('F-P-0315-marriage_assessment-banns-not-wedding').actual_wedding_date,null);
 assert.equal(readCurrent(db,'E-marriage-P-0315-P-0316-1858'),null);
 assert.equal(participants('E-banns-P-0315-P-0316-1858').length,2);
 assert.equal(value('O-P-0315-C0274-child').folio,85);
 assert.equal(value('O-P-0316-C0274-child').folio,85);
 assert.equal(current('M-P-0316-C0274-child').name_literal,'Cajsa Märta Dahlsten');
 assert.equal(value('F-P-0315-source_route-remaining').Sattna,'AI9aBynfolio85,oläst');
 const witnesses=participants('E-baptism-P-0254').filter(p=>p.role==='witness');
 assert.equal(witnesses.length,10);assert.ok(witnesses.every(w=>w.person_id===null));
 assert.equal(witnesses.filter(w=>current(w.mention_id).name_literal==='').length,3);
 assert.equal(value('F-P-0254-source_correction-C0274').documentation_conflict_unresolved,true);
 assert.equal(value('F-P-0315-documentation_conflict-extraction').AI12.resolution,'unresolved');
 assert.equal(acceptedParents('P-0315').some(r=>r.from_person==='P-0405'),false);
 assert.equal(current('REL-step-P-0405-P-0315').relation_type,'other');groups++;
 // Egna fält får inte ärvas från make/föräldrar; två Anders Olof är två personer.
 assert.equal(value('O-P-0316-C0436-childhood').birthplace_column,false);
 assert.equal(value('O-P-0316-C0437-childhood').birthplace_column,true);
 assert.equal(value('O-P-0316-C0512-household').own_remaining_columns_extracted,false);
 const sib=value('F-P-0316-family_context-parents-and-siblings');
 assert.equal(sib.siblings.find(s=>s.id==='P-0380').death,'1843-01-18');
 assert.equal(sib.siblings.find(s=>s.id==='P-0381').birth,'1844-08-22');
 assert.equal(value('F-P-0316-death_context-bounded-interpretation').age_difference_days,3);
 assert.equal(value('F-P-0316-death_context-bounded-interpretation').exact_death_building_proven,false);
 assert.match(current('ASSESSMENT-P-0316').outcome,/UNDERKÄND/);groups++;
 // Cat4[5?]ger varken säkert år eller överlevnad till bokslut; datumfel ur familjeakt.
 assert.equal(date('E-birth-P-0325').value,'1830-05-09');
 assert.equal(value('F-P-0325-interpretation-Cat-note').exact_year_selected,null);
 assert.equal(value('F-P-0325-interpretation-Cat-note').meaning_status,'SANNOLIKT');
 assert.equal(value('F-P-0325-source_assessment-life-boundary').alive_at_book_end_proven,false);
 assert.equal(value('F-P-0325-source_assessment-life-boundary').old_Motala1838_wrong_person,'P-0124');
 assert.equal(value('O-P-0266-C304-witness-c').home_literal,null);
 assert.equal(value('O-P-0266-C304-witness-d').home_literal,'L:a Häg…[?]');
 assert.equal(value('F-P-0325-source_assessment-witness-limits').Stina_surname,null);groups++;
 // Adelia i den äldre boken är kandidat, inte andra säkra föräldrar.
 assert.equal(current('ID-P-0326-C0296-candidate').decision,'candidate');
 assert.equal(current('ID-P-0326-C0291-child').decision,'accepted');
 assert.equal(acceptedParents('P-0326').length,0);
 assert.equal(current('SEARCH-P-0326-C0305-reference-conflict').outcome,'inconclusive');
 assert.equal(JSON.parse(current('SEARCH-P-0326-C0305-reference-conflict').scope_json).bounds.right_header,1834);
 assert.equal(value('F-P-0326-identity_assessment-household-not-parents').biological_parents_decided,false);groups++;
 // Två bröders57/67och en dotters felaktigt tilldeladeNorrköping får inte blandas.
 assert.equal(date('E-birth-P-0327').value,'1818-12-05');
 assert.equal(value('O-P-0327-C0296-child').birth,'1818-12-05');
 assert.equal(value('O-P-0327-C0291-own').reported_birth,'1818-12-17');
 assert.equal(value('O-P-0327-C0291-own').arrival.certificate,57);
 assert.equal(value('O-P-0327-C0291-own').departure.certificate,62);
 assert.equal(date('E-registered_arrival-P-0327').value,'1840');
 assert.equal(date('E-registered_departure-P-0327').value,'1841');
 assert.equal(value('F-P-0327-source_route-own-followup').C0821_is_own_identity_exhaustion,false);groups++;
 // Dödsmärket +1829 ger bara år; frånvaron gäller en familjegrupp,inte hela boken.
 assert.deepEqual(date('E-death-P-0328'),{literal:'+1829',precision:'year',value:'1829'});
 assert.equal(value('F-P-0328-name_assessment-rejected-Johanna').rejected_reading,'Anna Johanna');
 assert.equal(value('F-P-0328-source_assessment-death-and-biography').death_day,null);
 assert.equal(value('F-P-0328-source_assessment-death-and-biography').unread_death_record_guarantees_cause,false);
 assert.equal(JSON.parse(current('SEARCH-P-0328-C0291-family-absence').scope_json).bounds.rows,'Ajaxfamiljens nio rader');
 const unit=inspect(db,'A-7660');assert.ok(unit.conversionDecisions.some(d=>d.state==='mapped_complete'));groups++;
 // December utan dag blir ett månadstäckande intervall;1880är beroende årsuppgift.
 assert.deepEqual(date('E-birth-P-0343'),{precision:'range',from:'1815-12-01',to:'1815-12-31',literal:'1815, månad12, dag tom'});
 assert.equal(value('O-P-0343-C0346-s94').birth_day,null);
 assert.equal(value('F-P-0343-source_assessment-chain-and-household').census_independent,false);
 assert.equal(value('O-P-0344-C0832-census').birth_day_given,false);
 assert.equal(participants('E-baptism-P-0344').filter(p=>p.role==='witness').length,6);
 assert.equal(value('F-P-0344-source_correction-witnesses-and-neighbour').old_profile_unread_claim_superseded,true);
 assert.equal(value('F-P-0344-source_correction-witnesses-and-neighbour').neighbour_father_is_own_father,false);
 assert.equal(JSON.parse(current('SEARCH-C0858-Gardtjarn-family').scope_json).bounds.Byn_included,false);
 assert.equal(value('F-P-0344-source_assessment-identity-and-limits').distinct_namesake,'P-0376');groups++;
 // Hushållsordning ger inga biologiska kanter eller ärvt Höglund/odöpt.
 for(const id of ['P-0345','P-0347','P-0348'])assert.equal(acceptedParents(id).length,0);
 assert.equal(date('E-registered_departure-P-0345').value,'1900-02-10');
 assert.equal(value('F-P-0345-life_scope-household-and-departure').arrival_in_Timra_verified,false);
 for(const id of ['P-0347','P-0348']){
  assert.equal(value(`F-${id}-life_scope-household-only`).own_surname_attested,false);
  assert.equal(value(`F-${id}-life_scope-household-only`).own_baptism_status,null);
  assert.equal(value(`F-${id}-life_scope-household-only`).missing_from_partial_lists_is_negative_evidence,false);
 }groups++;
 // Två olikafolio138; egen födelse12nov väger före två senare22nov,ej röstning.
 assert.equal(date('E-birth-P-0346').value,'1874-01-31');
 assert.equal(value('F-P-0346-life_scope-individual-fields').marriage_place,null);
 assert.equal(value('F-P-0346-life_scope-individual-fields').wifes_baptist_note_is_his,false);
 assert.equal(value('F-P-0346-life_scope-individual-fields').conscription_cause,null);
 assert.equal(value('F-P-0346-source_route-row4-row8-next-book').incorrect_page4_rejected,true);
 assert.equal(value('F-P-0346-source_route-row4-row8-next-book').next_book_identified_and_read,false);
 assert.equal(date('E-birth-P-0349').value,'1880-11-12');
 assert.equal(value('O-P-0349-C0457-hh').reported_birth,'1880-11-22');
 assert.equal(value('O-P-0349-C0654-row5').reported_birth,'1880-11-22');
 assert.equal(value('F-P-0349-birth_assessment-12-not22').dates_equally_plausible,false);
 assert.equal(current('E-book-transfer-P-0349-1901').event_type,'other');
 assert.equal(value('F-P-0349-life_scope-notes-and-internal-transfer').transfer.same_book,true);
 assert.equal(value('F-P-0349-life_scope-notes-and-internal-transfer').transfer.person_bound_destination_extraction_done,false);
 assert.equal(current('REL-sibling-P-0274-P-0349').nature,'maternal_sibling');groups++;
 // Tvillingarnas vittnen hör till varsitt dop; änka anger inte barnets fars dödsdag.
 assert.equal(value('O-P-0350-C0842-own').birthplace_literal,'Njutånger');
 assert.equal(value('O-P-0350-C0842-own').vaccination_column_present,false);
 assert.equal(value('F-P-0350-identity_assessment-mother-not-father').fathers_death_before1857_proven,false);
 assert.equal(value('F-P-0350-identity_assessment-mother-not-father').Olof_Hillberg1832.brother_proven,false);
 assert.equal(value('F-P-0350-source_correction-witness-count').total_participant_mentions,12);
 assert.equal(participants('E-baptism-P-0277').filter(p=>p.role==='witness').length,6);
 assert.equal(participants('E-baptism-P-0352').filter(p=>p.role==='witness').length,6);
 assert.equal(date('E-death-Per-Eric-Hillberg1859').value,'1859-09-15');
 assert.equal(value('F-P-0350-life_scope-own-rows-and-family').Mo1817_missing_November_pages_proven,false);groups++;
 // Civilståndsmarkeringar är positiva; oskuggat tomfält och oläst nummer skiljs.
 assert.equal(current('P-0340').sex,'male');
 assert.equal(date('E-birth-P-0340').value,'1872-04-28');
 assert.equal(value('O-P-0340-C0529-birth').legitimate_male,'1');
 assert.equal(value('O-P-0340-C0529-birth').mother_married,'1');
 assert.equal(value('O-P-0340-C0529-birth').annual_number,'unread in page-edge shadow');
 assert.equal(value('F-P-0340-source_assessment-birth-and-marriage-conflict').home_birth_building_proven,false);
 assert.equal(value('F-P-0340-source_assessment-birth-and-marriage-conflict').Sattna_whole_calendar_year_proven,false);
 assert.equal(value('F-P-0340-migration_assessment-three-person-family').child_separately_named_in_departure,false);
 assert.equal(value('F-P-0340-migration_assessment-three-person-family').separate_arrival_register_read,false);
 assert.equal(value('F-P-0340-life_scope-after1880-unresolved').absence_from_entire_census_proven,false);groups++;
 // Samma sex vittnen återbrukas från båda föräldrarna; ålder är ingen exakt födelse.
 assert.equal(participants('E-baptism-P-0271').filter(p=>p.role==='witness').length,6);
 assert.equal(participants('E-baptism-P-0271').filter(p=>p.role==='mother').length,1);
 assert.equal(participants('E-baptism-P-0271').filter(p=>p.role==='father').length,1);
 assert.equal(value('F-P-0342-life_scope-one-family-record').estimated_year_is_exact,false);
 assert.equal(value('F-P-0342-life_scope-one-family-record').postpartum_survival_proven,false);
 assert.equal(value('F-P-0341-social_network-six-witnesses').maternal_relatives_absent_proven,false);
 assert.equal(value('F-P-0341-source_assessment-Hogsjo-search-bounds').whole_parish_search,false);
 assert.equal(value('F-P-0341-source_assessment-Hogsjo-search-bounds').old_profile_missing_addendum_claim_outdated,true);
 assert.equal(acceptedParents('P-0341').length,0);
 assert.equal(acceptedParents('P-0342').length,0);groups++;
 // Rullans rättade Jonas/1849/20; positiva dödsdatum består trots avgränsat noll.
 assert.equal(value('O-P-0339-C0606-roll').father,'Jonas Schölin');
 assert.equal(value('O-P-0339-C0606-roll').bottom_year,1849);
 assert.equal(value('O-P-0339-C0606-roll').annual_support,20);
 assert.equal(value('O-P-0339-C0606-roll').selected_admission_day,null);
 assert.equal(value('F-P-0339-source_assessment-roll-corrections-and-identity').payee_proven,false);
 assert.equal(value('F-P-0339-source_assessment-roll-corrections-and-identity').printed18_is_amount,false);
 assert.deepEqual(date('E-birth-P-0339').values,['1825-08-12','1825-08-13']);
 assert.equal(date('E-death-P-0339').value,'1901-04-19');
 assert.equal(current('SEARCH-P-0339-household1902-1921').outcome,'inconclusive');
 assert.equal(current('SEARCH-P-0339-death1901-1902').outcome,'negative');
 assert.equal(value('F-P-0339-family_context-census-boundaries').census1890.shared_page_proves_shared_household,false);
 assert.equal(value('F-P-0339-family_context-census-boundaries').census1900.own_family_members,1);
 assert.equal(acceptedParents('P-0339').some(r=>r.from_person==='P-0455'),false);
 assert.equal(current('REL-foster_parent-P-0455-P-0339').relation_type,'foster_parent');groups++;
 // Ett dop,tolv vittnen; svaga kommunionsår blir inte exakta händelser.
 assert.equal(participants('E-baptism-P-0394').filter(p=>p.role==='witness').length,12);
 assert.equal(participants('E-baptism-P-0394').filter(p=>p.role==='witness'&&current(p.mention_id).name_literal==='').length,3);
 assert.equal(value('F-P-0338-family_context-children-and-witnesses').stillborn_boy_baptized,false);
 assert.equal(value('F-P-0338-family_context-children-and-witnesses').continued_foster_arrangement_proven,false);
 assert.equal(value('F-P-0338-source_assessment-dates-and-life-limits').reported_marriage_age,23);
 assert.equal(value('F-P-0338-source_assessment-dates-and-life-limits').calculated_completed_years,24);
 for(const id of ['P-0338','P-0339'])assert.equal(value(`O-${id}-C0519-s54`).communion_years,null);
 assert.equal(date('E-move-Henrik-family-out1854').value,'1854-11-05');
 assert.equal(date('E-move-Henrik-family-in1855').value,'1855-12-02');
 assert.equal(value('F-P-0338-identity_assessment-parents-and-secondary-conflicts').late_2026_09_10_grade_objection_preserved,true);
 assert.equal(value('F-P-0338-identity_assessment-parents-and-secondary-conflicts').original_witness_role_is_sibling_proof,false);
 assert.equal(current('ID-P-0338-C0520-Erik').decision,'rejected');groups++;
 // Sena C0445-rättelser; sidregistret är ingen fjärde bevarad personbild.
 assert.equal(current('M-C0445-father').role_literal,'Hem.');
 assert.equal(current('M-C0445-mother').name_literal,'Catharina Andreas dotter');
 assert.equal(current('M-C0445-witness-Carl').name_literal,'Carl Johan Magnusson');
 assert.equal(current('M-C0445-witness-Anna').name_literal,'Anna Lena Thorstensd:r');
 assert.equal(participants('E-baptism-P-0337').filter(p=>p.role==='witness').length,6);
 assert.equal(participants('E-baptism-P-0367').filter(p=>p.role==='witness').length,4);
 assert.equal(date('E-baptism-P-0367').value,'1878-07-08');
 assert.equal(value('O-P-0337-C0651-death').home_literal,'37 D');
 assert.equal(value('F-P-0337-source_assessment-death-and-home').physical_death_place,null);
 assert.equal(value('F-P-0337-source_assessment-death-and-home').three_independent_death_chains,false);
 assert.equal(value('F-P-0337-source_assessment-death-and-home').previous_row_death_same_day,false);
 assert.equal(value('F-P-0337-source_route-estate-and-tax').old_no_series_claim_superseded,true);
 assert.equal(value('F-P-0337-source_route-estate-and-tax').own_volume_or_act_read,false);
 assert.equal(value('F-P-0337-preservation_assessment-explicit-gaps').AI5_preserved_search_pages.length,3);
 assert.equal(value('F-P-0337-preservation_assessment-explicit-gaps').Hemsjo_total,16);
 assert.equal(value('F-P-0337-family_context-four-children').second_marriage_five_children_are_hers,false);groups++;

 // Olaus vuxenkedja är inte en löst födelse; gamla avskriftsfel räknas inte som alternativa originaldatum.
 const birth336=value('F-P-0336-birth_assessment-source-conflicts');
 assert.deepEqual(birth336.reported_dates,['1852-09-04','1852-09-24']);
 assert.deepEqual(birth336.other_reported_years,[1853,1854]);
 assert.equal(birth336.preferred_actual_birth,null);
 assert.equal(birth336.rejected_transcription,'1852-05-24');
 assert.equal(readCurrent(db,'E-birth-P-0336'),null);
 assert.equal(acceptedParents('P-0336').length,0);
 for(const key of ['C0367-Brattas','C0368-Brattas','C0747-Lundby','C0803-seaman-1874','C0803-seaman-1875'])assert.equal(current(`ID-P-0336-${key}`).decision,'rejected');
 assert.equal(value('F-P-0336-family_hypothesis-Fredric-Anna').margin_expansion,null);
 assert.equal(value('F-P-0336-family_hypothesis-Fredric-Anna').probate_search_already_done_1853,true);
 assert.equal(value('O-P-0336-C0383-arrival').from,'Alnö');
 assert.equal(value('O-P-0336-C0383-arrival').home,'15 Upplandsgatan');
 assert.equal(value('O-P-0336-C0601-certificate').reported_birth,'1852-09-04');
 assert.equal(value('O-P-0336-C0474-groom').reported_birth,'1852-09-24');
 assert.equal(value('O-P-0336-C0866-tax').income_from_office_or_pension,670);
 assert.equal(value('O-P-0336-C0866-tax').ownership_proven,false);groups++;
 // Delade händelser, skilda giften; planerad klocktid och gemensam civilståndskolumn förblir öppna.
 assert.equal(participants('E-marriage-P-0336-P-0337-1877').filter(x=>x.person_id==='P-0336').length,1);
 assert.equal(participants('E-marriage-P-0336-P-0397-1888').filter(x=>x.person_id==='P-0336').length,1);
 assert.equal(participants('E-birth-P-0287').filter(x=>x.person_id==='P-0287'&&x.role==='principal').length,1);
 assert.equal(participants('E-birth-P-0287').filter(x=>x.person_id==='P-0336'&&x.role==='father').length,1);
 assert.equal(value('F-P-0336-family_context-nine-known-children').known_total,9);
 assert.equal(value('F-P-0336-family_context-nine-known-children').twins_proven,false);
 assert.equal(value('O-P-0336-C0800-census').family_count,7);
 assert.equal(value('O-P-0336-C0800-census').original_visible_rows.length,4);
 assert.equal(value('O-P-0336-C0800-census').last_three_children_index_only,true);
 assert.equal(value('F-P-0336-death_assessment-source-boundaries').own_folio,587);
 assert.equal(value('F-P-0336-death_assessment-source-boundaries').selected_marital_state,null);
 assert.equal(value('F-P-0336-death_assessment-source-boundaries').physical_death_place_in_book,null);
 assert.equal(value('F-P-0336-death_assessment-source-boundaries').actual_funeral_time_proven,false);
 assert.equal(date('E-death-P-0336').value,'1925-08-06');
 assert.equal(date('E-burial-P-0336').value,'1925-08-12');
 assert.equal(value('F-P-0336-residence_assessment-Klara-dates').physical_move_date,null);groups++;
 // Originalnoll, otäckta register och OCR-nomineringar är olika resultat. Senare läsesalsbesked ersätter historisk CAPTCHA.
 const scope=id=>JSON.parse(current(`SEARCH-P-0336-${id}`).scope_json);
 assert.equal(current('SEARCH-P-0336-DDS-birth-coverage').outcome,'inconclusive');
 assert.equal(current('SEARCH-P-0336-HII1-all-OCR').outcome,'inconclusive');
 assert.equal(scope('HII1-all-OCR').bounds.images,908);
 assert.equal(scope('HII1-all-OCR').bounds.full_visual_read,false);
 assert.equal(scope('HII1-window').bounds.count,55);
 assert.equal(scope('HII1-window').bounds.complete_year,false);
 assert.equal(scope('Bjarke1853').bounds.count,117);
 assert.equal(scope('Bjarke1853').bounds.start,'höger209,akt1,7feb');
 assert.equal(scope('Sollentuna1920-OCR').bounds.count,46);
 assert.equal(scope('Sollentuna1920-OCR').bounds.full_visual_name_read,false);
 assert.equal(value('F-P-0336-source_route-confirmation-gap').StoraLundby1869_digital_range_missing,true);
 assert.equal(value('F-P-0336-source_access-military-catalog-history').old_captcha_is_current_block,false);
 assert.equal(value('F-P-0336-source_route-Stockholm1876-1877').rescan42digitalvolumes_required,false);
 assert.equal(value('F-P-0336-preservation_assessment-gaps-and-life-limits').rote_full_local_copies_missing,7);
 assert.match(current('ASSESSMENT-P-0336').outcome,/UNDERKÄND/);groups++;
 return {groups,ok:true};
}
