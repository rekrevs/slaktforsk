import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';
// Fasta kontrollfall mot helakternas/citationernas rättelser, inte genererade förväntningar.
export function checkPersons09PartCRisks(db){
 const r=id=>{const row=readCurrent(db,id);assert.ok(row,id);return row;};
 const v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
 const participants=id=>db.prepare('select p.* from current_revision c join participation p on p.revision_id=c.id where p.event_id=?').all(id);
 const parents=id=>db.prepare("select x.* from current_revision c join relation x on x.revision_id=c.id where x.relation_type='parent' and x.to_person=? and c.disposition='accepted'").all(id);
 // C0552T0161/A6270: positiv rapporterad dödskolumn; äldre personreservation och oläst dödbok kvar.
 assert.equal(d('E-birth-P-0434').value,'1887-06-16');assert.equal(d('E-death-P-0434').value,'1891-01-11');assert.equal(v('F-P-0434-source_interpretation-reported-death').own_death_register_read,false);assert.equal(v('F-P-0434-source_interpretation-reported-death').contract_review_changed,false);
 assert.equal(v('F-P-0434-family_context-botsmark').mother_age_at_birth,44);
 assert.match(v('F-P-0434-family_context-botsmark').oldest_claim.correction,/Sophia Beata1851/);
 assert.match(v('F-P-0434-source_interpretation-crossings').unread,/inte tomma/);
 // C0562/C0561: rätt födelsepost, inga fiktiva moderåldrar, personlig utgång668/1877.
 assert.equal(v('O-P-0435-C0562-own').mother_age_column,'saknas');
 assert.equal(v('O-P-0435-C0561-own').destination,'668');assert.equal(d('E-registered_departure-P-0435').precision,'year');
 assert.equal(participants('E-baptism-P-0435').filter(x=>x.role==='witness').length,6);
 // C0562/0685/0563/0561: tre skrivna förnamnsformer, inte tre nya kvinnor.
 assert.equal(r('M-P-0436-C0562-own').name_literal,'Christina Wilhelmina');
 assert.equal(r('M-P-0436-C0685-own').name_literal,'Sophia Wilhelmina');
 assert.equal(r('M-P-0436-C0561-own').name_literal,'Cajsa Wilhelmina');
 assert.equal(d('E-registered_departure-P-0436').value,'1876-01-14');
 assert.equal(v('O-P-0436-C0561-own').communion.length,2);
 assert.match(v('F-P-0436-source_interpretation-scb1860').limits,/Inte individuellt/);
 // C0751: egen hustru, åtta barn och fadern i separat normaliserad familj.
 const maria=v('F-P-0437-family_context-ektrask1900');assert.equal(maria.children.length,8);
 assert.equal(d('E-registered_departure-P-0437').value,'1875-10-15');
 assert.match(maria.father.separate_record,/familj3/);assert.match(maria.children_surnames,/ej angivna/);
 assert.equal(r('F-P-0437-family_hypothesis-naming').disposition,'candidate');
 assert.equal(v('F-P-0437-family_context-degerfors-network').routes.length,5);
 // C0564: Sara får varken systerns vittnen, exakt nöddopdag eller moderns negativkontroll.
 assert.equal(d('E-birth-P-0438').value,'1868-02-12');
 assert.equal(d('E-baptism-P-0438').precision,'unknown');assert.equal(d('E-death-P-0438').precision,'unknown');
 assert.equal(participants('E-baptism-P-0438').filter(x=>x.role==='witness').length,0);
 assert.equal(r('F-P-0438-twinship-pair').subject_id,'REL-sibling-P-0428-P-0438');
 assert.deepEqual(v('F-P-0438-twinship-pair').births,['1868-02-12','1868-02-13']);
 assert.match(v('F-P-0438-source_interpretation-undated-emergency').negative_scope,/inte SaraRebecka/);
 // C0565/0566: Axel 23mars, hans egna vittnen och tom dödsorsak; åldersavvikelse kvar.
 assert.equal(d('E-birth-P-0439').value,'1864-03-23');assert.equal(d('E-death-P-0439').value,'1865-02-18');
 assert.equal(d('E-burial-P-0439').value,'1865-03-05');
 assert.equal(v('O-P-0439-C0566-own').cause,'tomt');assert.equal(v('O-P-0439-C0566-own').age_days,25);
 assert.equal(participants('E-baptism-P-0439').filter(x=>x.role==='witness').length,6);
 assert.match(v('O-P-0439-C0565-own').officiant,/Strinnholm/);
 assert.match(v('F-P-0439-source_interpretation-age-discrepancy').elapsed,/10m26d/);
 assert.deepEqual(v('F-P-0439-twinship-pair').births,['1864-03-23','1864-03-24']);
 // C0567 + redan prövade C0562: villkorligt moderintervall, rätt riktning för löpande levnadsår.
 const ages=v('F-P-0440-source_interpretation-maternal-age-series');
 assert.deepEqual(ages.completed_age_window,['1829-03-24','1829-05-28']);assert.equal(ages.inclusive_days,66);
 assert.match(ages.running_age_correction,/FRAMÅT/);assert.match(ages.additional_existing,/1853\/1854 saknar/);
 assert.equal(d('E-registered_departure-P-0440').precision,'year');
 // C0574 klammer17–20: samma registrering, separata barnrader utan uppfunna efternamn.
 assert.equal(r('E-emigration-P-0430-family-1907').event_type,'registered_departure');
 assert.equal(d('E-emigration-P-0430-family-1907').value,'1907-04-08');
 for(const id of['P-0441','P-0442','P-0443'])assert.ok(participants('E-emigration-P-0430-family-1907').some(x=>x.person_id===id));
 assert.equal(r('M-P-0442-C0574-own').name_literal,'Alvar Rudolf');assert.equal(r('M-P-0443-C0574-own').name_literal,'Anders Gideon Nikanor');
 assert.equal(v('F-P-0442-family_context-rosinedahl').age_at_registration,'1år10m4d');
 assert.equal(v('F-P-0443-family_context-rosinedahl').age_at_registration,'5m10d');
 assert.equal(r('E-marriage-P-0430-P-0441-1904').place_id,null);
 // C0576: rättelser är avskriftsfel; återbruk av Matildas födelse och befintliga föräldralänkar.
 assert.equal(v('O-P-0444-C0576-own').home,'Stenkulla');assert.equal(v('O-P-0445-C0576-own').mother_age,'20');
 assert.equal(v('F-P-0445-source_correction-C0576').original_conflict,false);
 assert.deepEqual(v('F-P-0445-birth_constraint-age20').if_completed_age,['1839-08-09','1840-08-08']);
 assert.equal(v('F-P-0445-birth_constraint-age20').exact_year,null);assert.equal(r('M-P-0445-C0576-own').name_literal,'Stina Lotta');
 assert.ok(participants('E-birth-P-0135').some(x=>x.person_id==='P-0444'&&x.role==='parent'));
 assert.ok(participants('E-birth-P-0135').some(x=>x.person_id==='P-0445'&&x.role==='parent'));
 // C0580 är kandidat, C0579 binder modern. Kandidatens dop/faddrar blir inga egna personhändelser.
 assert.equal(r('ID-P-0446-C0580-candidate').decision,'candidate');assert.equal(r('ID-P-0446-C0580-candidate').disposition,'candidate');
 assert.equal(r('ID-P-0446-C0579-own').decision,'accepted');
 assert.deepEqual(d('E-birth-P-0446').values,['1880-11-01','1880-11-11']);
 assert.equal(v('F-P-0446-identity_conflict-birth-candidate').candidate_mother_proven,false);
 assert.equal(v('F-P-0446-identity_conflict-birth-candidate').independent_illegitimacy_sources_for_person,1);
 assert.ok(parents('P-0446').some(x=>x.from_person==='P-0135'));
 assert.ok(parents('P-0446').every(x=>x.from_person!=='P-0133'));
 const candidatePeople=participants('E-baptism-C0580-candidate');assert.equal(candidatePeople.length,5);assert.ok(candidatePeople.every(x=>x.person_id===null));
 assert.equal(v('F-P-0446-source_interpretation-departure-correction').crossed_date,null);
 assert.equal(v('O-P-0446-C0579-own').departure_crossed,'Björkvik');assert.equal(v('O-P-0446-C0579-own').departure_current,'Helgesta');
 assert.match(v('F-P-0446-family_context-bergatorp').own_age_at_departure,/16år2d/);
 // C0590/1024: parets egna fält hålls individuella, positiv vigsel ersätter inte födelsebryggor.
 assert.equal(d('E-birth-P-0447').value,'1805-08-21');assert.equal(d('E-marriage-P-0447-P-0448-1830').value,'1830-04-13');
 assert.equal(v('O-P-0447-C0590-own').communion['1833'],'3[?]/4');assert.equal(v('O-P-0448-C0590-own').communion['1833'],'7[?]/4');
 for(const id of['P-0447','P-0448']){assert.equal(parents(id).length,0);assert.equal(d(`E-communion-${id}-1842-11-06`).value,'1842-11-06');}
 const cajsa=v('F-P-0448-source_interpretation-name-and-age');assert.equal(cajsa.age_in1840,28);assert.equal(cajsa.computed_completed_age,27);assert.equal(cajsa.selected_birthyear1811,false);assert.equal(cajsa.father_identified,false);assert.equal(cajsa.churching_exact_date,null);
 assert.equal(r('F-P-0448-origin_lead-hullsjo-before1830').disposition,'candidate');
 assert.equal(r('M-C0333-witness-wife-Jons-Pehrsson').name_literal,'');
 assert.equal(participants('E-baptism-P-0250').filter(x=>x.role==='witness').length,4);
 // Årsnot på namnlös källperson, inte exakt död/namngissning eller syskonens egna ankare.
 assert.equal(v('O-C0590-unnamed-child1831').name_reading,null);assert.equal(v('O-C0590-unnamed-child1831').sex,null);
 assert.equal(d('E-drowning-C0590-unnamed-child1841').precision,'year');assert.equal(participants('E-drowning-C0590-unnamed-child1841')[0].person_id,null);
 assert.equal(r('M-C0590-unnamed-child1831').name_literal,'');
 assert.equal(v('F-P-0449-source_interpretation-own-family-limits').age_at_drowning,'6eller7');
 assert.equal(v('F-P-0450-source_interpretation-own-family-limits').age_at_drowning,'3eller4');
 for(const id of['P-0449','P-0450']){const scope=v(`F-${id}-source_interpretation-own-family-limits`);assert.equal(scope.own_dated1842_anchor,false);assert.equal(scope.birthplace_proven,false);assert.equal(scope.military_record_impossible,false);assert.equal(parents(id).length,2);}
 const hull=r('SEARCH-P0250-Hullsjö1843-1850');assert.equal(hull.outcome,'negative');assert.equal(JSON.parse(hull.scope_json).bounds.pages,'92–93');assert.match(hull.body,/Ingen daterad utflyttning/);
 assert.match(v('F-P-0447-family_context-hullsjo').provenance,/22routingbilder/);
 // P0429: tre egna namnformer; det obevarade759namnet är kandidat utan makeidentitet.
 assert.equal(r('M-P-0429-C0563-own').name_literal,'Anna Margaretha');assert.equal(r('M-P-0429-C0561-own').name_literal,'Anna Margretha');assert.equal(r('M-P-0429-C0552-own').name_literal,'Anna Margreta');
 assert.equal(d('E-banns-P-0429').value,'1893-07-23');assert.equal(d('E-marriage-P-0429').value,'1893-08-12');assert.equal(r('E-registered_transfer-P-0429').event_type,'registered_departure');
 assert.equal(r('F-P-0429-partner_hypothesis-aberg').disposition,'candidate');assert.equal(v('F-P-0429-partner_hypothesis-aberg').rejected,false);assert.equal(v('F-P-0429-partner_hypothesis-aberg').archival_mention_created,false);
 assert.equal(v('F-P-0429-source_interpretation-bounds').birth_book.outcome,'coverage_boundary');assert.equal(v('F-P-0429-source_interpretation-bounds').banns_to_marriage_days,20);
 assert.equal(db.prepare("select count(*) n from current_revision c join relation x on x.revision_id=c.id where x.relation_type='spouse' and (x.from_person='P-0429' or x.to_person='P-0429') and c.disposition='accepted'").get().n,0);
 // P0430: eget1907deltagande; rad25 är internflytt och fräjd/värnpliktsuppgifter är inte tjänst.
 assert.equal(d('E-registered_departure-P-0430').value,'1898-04-29');assert.equal(d('E-registered_arrival-P-0430').value,'1899-11-28');
 assert.equal(v('O-P-0430-C0571-own').folio,'104/3');assert.equal(v('O-P-0430-C0574-row25').conduct,'L.B.30/1 4[?]');assert.equal(v('F-P-0430-source_interpretation-chain-and-limits').LB_exact_date,null);
 assert.equal(v('F-P-0430-military_status-inscription').military_service_proven,false);assert.equal(v('F-P-0430-family_context-rosinedahl').mother_death_current_reading,'1895-02-27');
 assert.deepEqual(participants('E-emigration-P-0430-family-1907').map(x=>x.person_id).sort(),['P-0430','P-0441','P-0442','P-0443']);
 assert.ok(participants('E-marriage-P-0430-P-0441-1904').some(x=>x.person_id==='P-0430'&&x.role==='spouse'));
 // P0431: tom attestkolumn, reserverad medgivandefortsättning och endast bokdestination Nordamerika.
 assert.equal(r('M-P-0431-C0563-own').name_literal,'Emanuël');assert.equal(d('E-registered_departure-P-0431').value,'1892-08-20');
 assert.equal(v('O-P-0431-C0552-own').certificate_number,'tomt');assert.match(v('O-P-0431-C0552-own').consent_tail,/olästa/);
 assert.equal(v('F-P-0431-family_context-chronology').known_second_kull_order,3);assert.equal(v('F-P-0431-source_interpretation-own-limits').american_country_proven,false);
 // P0432: överstrykning ger ingen egen död/flytt; äldre egen rad men ingen själv-syskonrelation.
 assert.equal(v('O-P-0432-C0552-own').crossed,true);assert.equal(v('O-P-0432-C0561-own').own_date_extracted,false);
 assert.equal(v('F-P-0432-source_interpretation-crossings').self_sibling,false);
 assert.equal(db.prepare("select count(*) n from current_revision c join participation p on p.revision_id=c.id join current_revision e on e.object_id=p.event_id join event v on v.revision_id=e.id where p.person_id='P-0432' and v.event_type in ('death','registered_departure')").get().n,0);
 assert.equal(db.prepare("select count(*) n from current_revision c join relation x on x.revision_id=c.id where x.from_person='P-0432' and x.to_person='P-0432'").get().n,0);
 // P0433: B3 har tom födelsecell; två ankomstdagar och25år bevaras, ingen Atlantresa eller hälsodiagnos.
 assert.equal(v('O-P-0433-C0571-own').birth,'tomt');assert.deepEqual(d('E-registered_arrival-P-0433').values,['1900-10-13','1900-10-14']);
 assert.equal(r('E-registered_arrival-P-0433').evidence_status,'CONFLICT');assert.equal(d('E-registered_departure-P-0433').value,'1904-09-02');
 const konrad=v('F-P-0433-source_interpretation-emigration-frikallad');assert.equal(konrad.age_at_registration,25);assert.equal(konrad.exact_freedom_date,null);assert.equal(konrad.medical_condition,null);assert.equal(konrad.actual_atlantic_journey_proven,false);assert.equal(konrad.fitness_for_travel_proven,false);
 assert.equal(r('E-drowning-C0590-unnamed-child1841').event_type,'death');for(const id of['P-0447','P-0448'])assert.equal(r(`E-communion-${id}-1842-11-06`).event_type,'other');
 return{ok:true,groups:22};
}
