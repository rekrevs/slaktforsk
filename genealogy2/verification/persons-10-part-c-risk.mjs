import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';
// Fasta sakprov från genomlästa akter och kompletta C-tillägg. Ingen förväntning hämtas ur migrationspaketet.
export function checkPersons10PartCRisks(db){
 const r=id=>{const x=readCurrent(db,id);assert.ok(x,id);return x;};
 const v=id=>JSON.parse(r(id).value_json),d=id=>JSON.parse(r(id).date_json);
 const participants=id=>db.prepare('select p.* from current_revision c join participation p on p.revision_id=c.id where p.event_id=?').all(id);
 const parents=id=>db.prepare("select x.* from current_revision c join relation x on x.revision_id=c.id where x.relation_type='parent' and x.to_person=? and c.disposition='accepted'").all(id);
 const absent=id=>assert.equal(readCurrent(db,id),null,id+' ska inte finnas');
 // C0751: åtta separata barnrader, endast årsdata och en censuskälla.
 const children=[['P-0481',1881],['P-0482',1884],['P-0483',1887],['P-0484',1889],['P-0485',1891],['P-0486',1894],['P-0487',1896],['P-0488',1899]];
 for(const[id,y]of children){assert.equal(d('E-birth-'+id).precision,'year');assert.equal(d('E-birth-'+id).value,String(y));assert.equal(r(id).evidence_status,'TRANSCRIBED');assert.equal(v(`O-${id}-C0751-own`).surname,null);assert.equal(v(`F-${id}-identity_limits-ektrask1900`).last_own_evidence,1900);assert.deepEqual(parents(id).map(x=>x.from_person).sort(),['P-0437','P-0480']);}
 assert.match(v('F-P-0481-source_interpretation-individual-limits').search,/1902/);
 assert.match(v('F-P-0482-source_interpretation-individual-limits').correction,/Per August/);
 assert.match(v('F-P-0483-source_interpretation-individual-limits').correction,/1868-08-14/);
 assert.match(v('F-P-0484-source_interpretation-individual-limits').correction,/namngivningsorsak/);
 assert.match(v('F-P-0485-source_interpretation-individual-limits').limits,/annan person/);
 assert.match(v('F-P-0486-source_interpretation-individual-limits').limits,/kan inte vara ursprung/);
 assert.match(v('F-P-0487-source_interpretation-individual-limits').name_matches[0],/P0439/);
 assert.match(v('F-P-0488-source_interpretation-individual-limits').correction,/42eller43/);
 absent('REL-sibling-P-0488-P-0488');
 // C0806/C0774/C0945: gravdagar är administrativa, årskonflikt och tomt gravsättningsfält består.
 assert.equal(d('E-birth-P-0489').value,'1890-09-05');assert.equal(d('E-burial-P-0489').value,'1975-06-18');assert.equal(v('F-P-0489-source_interpretation-individual-corrections').age_1910,20);assert.equal(v('F-P-0489-source_interpretation-individual-corrections').age_at_death,84);
 assert.equal(d('E-death-P-0490').value,'1967-11-09');absent('E-burial-P-0490');assert.equal(v('O-P-0490-C0945-own').burial,null);assert.equal(v('F-P-0490-source_interpretation-individual-corrections').age_at_death,75);
 assert.equal(r('E-birth-P-0491').evidence_status,'CONFLICT');assert.equal(d('E-birth-P-0491').precision,'unknown');assert.deepEqual(v('F-P-0491-source_interpretation-individual-corrections').birth_years,[1894,1895]);assert.equal(v('O-P-0491-C0945-own').birth,'1894-04-13');assert.equal(v('O-P-0491-C0774-own').birth_year,1895);assert.equal(v('F-P-0491-source_interpretation-individual-corrections').twins_proven,false);
 assert.equal(r('M-P-0492-C0945-own').name_literal,'Fredberg, Oscar Fredrik');assert.equal(r('M-P-0492-C0806-own').name_literal,'Oskar Fredrik');assert.equal(v('F-P-0492-source_interpretation-individual-corrections').age_1910,15);assert.equal(d('E-death-P-0492').value,'1966-10-30');
 absent('O-P-0493-C0806-own');assert.equal(v('F-P-0493-source_interpretation-individual-corrections').source_count,2);assert.equal(v('F-P-0493-source_interpretation-individual-corrections').age_at_death,85);assert.equal(d('E-burial-P-0493').value,'1988-11-24');
 for(const id of['P-0489','P-0490','P-0491','P-0492','P-0493']){assert.equal(r(id).evidence_status,'CORROBORATED');assert.equal(r('E-death-'+id).place_id,null);assert.equal(v(`F-${id}-source_assessment-names-dates-and-grave`).grave_entry_creation_date,null);}
 // C0763: CarlJohan oäkta och namnlös far. Mönstring1845-07-07 är ingen vigseldag.
 assert.equal(d('E-birth-P-0494').value,'1843-01-04');assert.equal(d('E-baptism-P-0494').value,'1843-01-06');assert.deepEqual(parents('P-0494').map(x=>x.from_person),['P-0475']);assert.equal(v('O-P-0494-C0763-birth-own').father,null);assert.equal(v('F-P-0494-source_interpretation-parental-chronology').marriage_date,null);assert.equal(v('F-P-0494-source_interpretation-parental-chronology').muster_date,'1845-07-07');
 // C0794Anna + C0749: egen1846post och senareA.L.1860; faderns rättade rånamn.
 assert.equal(d('E-birth-P-0495').value,'1846-01-14');assert.equal(v('O-P-0495-C0794-birth-own').father,'Carl Fr. Drill');assert.equal(v('O-P-0495-C0794-birth-own').maternal_churching,'1/2[?]');assert.equal(r('M-P-0495-C0749-own').name_literal,'A. L.');
 // C0702/C0749/C0794: LarsPetter, man,1848; inget Lovisa-noll på rätt datum konstruerat.
 assert.equal(r('P-0496').display_name,'Lars Petter');assert.equal(r('P-0496').sex,'male');assert.equal(d('E-birth-P-0496').value,'1848-02-27');assert.equal(r('M-P-0496-C0749-own').role_literal,'Son');assert.equal(v('O-P-0496-C0702-AI12-own').vaccination,'v');const search=r('SEARCH-P-0496-C0794-corrected-birth');assert.equal(search.outcome,'negative');assert.equal(JSON.parse(search.scope_json).bounds.image,'C0005882_00041');assert.equal(JSON.parse(search.scope_json).query.name,'Lars Petter');
 // C0729/C0794: januari1854 och felriktad aprilkontroll. SCB1870kollektiv ingen egen rad.
 assert.equal(d('E-birth-P-0497').value,'1854-01-21');assert.equal(v('F-P-0497-source_correction-birth-and-search-scope').negative_applies_to_corrected_date,false);assert.match(v('F-P-0497-source_interpretation-own-boundaries').own_columns,/outvunna/);absent('O-P-0497-C0729-SCB1870-own');
 // C0732: äldre1859Hedda skild från yngre79[?], död1883. Intern218/1ej kalenderdag.
 assert.equal(d('E-birth-P-0498').value,'1859-10-29');assert.equal(v('O-P-0498-C0732-AI19-own').internal_reference,'218/1 81');assert.equal(v('O-P-0498-C0732-AI19-own').remarks,'Deflorata');assert.equal(v('F-P-0498-source_interpretation-two-heddas-and-notes').normalized_move_date,null);absent('E-death-P-0498');assert.equal(d('E-death-younger-Hedda-Gatstugan1883').value,'1883-11-10');assert.ok(participants('E-death-younger-Hedda-Gatstugan1883').every(x=>x.person_id===null));assert.equal(r('M-P-0474-younger-Hedda').record_id,r('M-P-0498-C0732-AI19-own').record_id);
 // C0794/C0729: MariaSofiaFeb27+Mar8; HHMar27bevarat; ingen tolvårig intilliggande barnlucka.
 assert.equal(d('E-birth-P-0499').value,'1863-02-27');assert.equal(d('E-baptism-P-0499').value,'1863-03-08');assert.equal(v('O-P-0499-C0729-own').birth,'1863-03-27');assert.equal(v('O-P-0499-C0794-birth-own').home,'Hagby soldattorp[?]');assert.equal(v('O-P-0499-C0794-birth-own').home_role,'faderns hemvist');assert.equal(v('F-P-0499-source_interpretation-birth-context-and-siblings').closest_known_older_sibling,'P-0498');assert.equal(v('F-P-0499-source_interpretation-birth-context-and-siblings').twelve_year_gap_is_not_adjacent,true);
 for(const id of['P-0494','P-0495','P-0499'])assert.equal(participants('E-baptism-'+id).filter(x=>x.role==='witness').length,4);
 // C0798: Ulla28; rågenitiv, villkorligt födelsefönster och sannolikab tolkas inte till säkerhändelse.
 assert.equal(r('P-0500').evidence_status,'TRANSCRIBED');assert.equal(r('M-P-0500-C0798-mother').name_literal,'Ulla Ersdotters');assert.equal(r('M-P-0500-C0798-mother').role_literal,'Pig.');assert.equal(v('O-P-0500-C0798-mother').age,28);assert.equal(v('O-P-0500-C0798-mother').child_sex_literal,'[P]iltbarn');assert.equal(r('F-P-0500-church_hypothesis-ab').disposition,'candidate');assert.deepEqual(v('F-P-0500-age_assessment-reported28').conditional_completed_age_window,['1793-04-10','1794-04-09']);assert.equal(v('F-P-0500-network_hypothesis-baptism-witnesses').one_household_proven,false);assert.equal(v('F-P-0500-source_assessment-household-page-controls').same_place_proven,false);absent('E-birth-P-0500');
 // Alla nya föräldrarelationer ska ha föräldrainnebörd. En wrapper-default får aldrig göra dem till syskon.
 const relevant=db.prepare("select r.* from current_revision c join relation r on r.revision_id=c.id where r.relation_type='parent' and r.to_person between'P-0481'and'P-0499'").all();assert.ok(relevant.length>=30);for(const x of relevant)assert.equal(x.nature,'recorded_parent',`${x.from_person}→${x.to_person}`);
 return{ok:true,groups:20};
}
