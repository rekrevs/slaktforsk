// One-shot individually curated T-0660 packet; not a second editable domain model.
import {person,core,fact,event,exact,origins,section,src,cs,assertion,relation,relationRow,save,add,record} from './genealogy2-persons09-combined.mjs';
const own=(p)=>[section(p,'Identitet')];
function family(p,a){const out=[];for(const other of ['P-0415','P-0416','P-0251','P-0419','P-0420','P-0421'].filter(x=>x!==p.person)){const parental=['P-0415','P-0416'].includes(other),r=relation(p,parental?other:p.person,parental?p.person:other,parental?'parent':'sibling',a,parental?'recorded_parent':'recorded_sibling','TRANSCRIBED');out.push(r);try{relationRow(p,other,[r],'Egen föräldra-/syskonrad i C-0530; en informationsväg, inget separat dopbevis.');}catch(e){if(!e.message.endsWith(':0'))throw e;}}return out;}
{
 const p=person('P-0419','Hela akt/profil och C-0530/C-1030 lästa. Egen sonrad är avgränsad från fadern och brodern. 1860 är en utflytt till Stöde, inte död. Dagen 25/27 med äldre30 olöst; hushållshärlett Nordlund inte rånamn. En källa bär födelsen.');
 core(p,own(p),'Personen i den egna raden är accepterad; identitetsnivån godkänd men EJ BÄRANDE och full kontraktsnivå underkänd.');
 p.changes.find(m=>m.id===p.person).evidenceStatus='TRANSCRIBED';p.changes.find(m=>m.id===p.person).rationale='Egen separat personrad i C-0530; en källväg. Accepterad personidentitet ändrar inte kontraktsgranskningen.';
 const os=['A-2362','A-6950','A-6951','A-6952','A-6953','A-6954','A-6955'];
 const o=src(p,'C-0530','','C0530-own','Stefan Eri[k]','son',{birth_literal:'1842 25/2',birthplace_literal:'Holm',smallpox_literal:'v.',reading_literal:'klammer med sex punkter',conduct_literal:'g.',departure_literal:'Stöde d. 2[5/7]/10 60.',crossed_fields:['namn','födelsedata'],number_tax_literal:'två korta noteringar, övre inf/int, diagonalstreck',own_blank_fields:['Giftoår och dag','Hvarifrån.','Anmärkningar.','förhör och nattvard 1850–1858']},os,'Rånamnets sista bokstav under överstrykning. Dag30 är äldre kvarstående alternativ. Blanka egna rutor betyder inte frånvaro.');
 const birth=event(p,'birth',exact('1842-02-25'),['A-2362'],'Retrospektiv hushållsuppgift; egen Holm C/1-födelsepost oläst.');
 const born=fact(p,'birthplace','household',{name:'Holm',source:'retrospektiv husförhörsuppgift',own_birth_record_read:false},['A-2362']);
 const fam=family(p,['A-2362',section(p,'Relationer')]);
 const nf=fact(p,'name_form','household',{literal:'Stefan Eri[k]',normalized:'Stefan Erik',project_surname:'Nordlund',own_surname_attested:false},[section(p,'Namnformer')]);
 const home=fact(p,'household_membership','Norafors-Stormyran',{parish:'Sättna',locality:'Norafors–Stormyran',folio:'255',book_period:'1850–1861',continuous_presence_proven:false,father_arrival_literal:'58 Stöde',own_arrival_field:'blank',father_occupation_not_inherited:true},[section(p,'Boställen och flyttar')]);
 const move=event(p,'registered_departure',{precision:'range',from:'1860-10-01',to:'1860-10-31',literal:'Stöde d. 2[5/7]/10 60.; äldre30[?] ej helt uteslutet'},['A-6953'],'Dagen och mottagande hushåll olösta. Ingen reciprok inflyttningspost läst.',null,'TRANSCRIBED','E-departure-P-0419-Stode1860');
 const bounds=fact(p,'life_scope','source-limits',{occupation:null,death:null,burial:null,after_October1860:'okänt',old_death1860_reading:'upphävd genom kolumnen Hvarthän',no_communion_from_blank_proven:false,military_title_belongs_to_father:true},[section(p,'Hälsa och död'),section(p,'Militärt, civilt och rättsligt')]);
 const cmp=fact(p,'family_context','birth-before-marriage',{book_birth:'1842-02-25',parents_marriage:'1842-04-10',elapsed_days:44,independent_birth_sources:1,both_unmarried_refers_to_parents:true,child_legal_status_inferred:false},['A-3829',cs('C-1030')],'CORROBORATED','C-1030 återger C-0530 för barnets datum; vigseldatumet är en annan källa.');
 assertion(p,'A-2362',[...o,...birth,born,...fam,nf,home,...move,bounds],'Egen sonrad, retroaktiv födelse, personrelationer och upphävd dödsläsning hålls isär.');
 assertion(p,'A-3829',[cmp],'44 dagar; födelsedatumet har bara en informationsväg.');
 for(const a of ['A-6950','A-6951','A-6952','A-6954','A-6955'])assertion(p,a,[...o,home,bounds],'Hela egna råfält och gränser bevarade; betyg moderniseras inte och faderns yrke är inte sonens.');
 assertion(p,'A-6953',[...o,...move],'Månad säker, dag olöst och mottagande post oläst.');
 p.pending.push({origin:'A-6953',question:'Avgör egna utgående dagbråket i C-0530 (25/27, äldre30[?]) med Sättnas utflyttning och Stödes mottagande post; oktober1860 är bevarad utan vald dag.'});
 save(p);
}
{
 const p=person('P-0420','Hela akt/profil och C-0530 lästa. Jonas1850 hålls skild från fadern Jonas1816. År1850 och Holm via dittokedja accepterade, 22/2 mot29/3 olöst. Frånvaro av egen flyttnot bevisar varken fortsatt boende eller överlevnad.');
 core(p,own(p),'Egen personidentitet i separat barnrad består trots omstridd dag; ingen kontraktsuppgradering.');
 p.changes.find(m=>m.id===p.person).evidenceStatus='TRANSCRIBED';p.changes.find(m=>m.id===p.person).rationale='Egen separat personrad i C-0530; en källväg. Accepterad personidentitet ändrar inte kontraktsgranskningen.';
 const os=['A-2363','A-6960','A-6961','A-6962','A-6963','A-6964','A-6965','A-6966'];
 const o=src(p,'C-0530','','C0530-own','Jonas','son',{birth_year:1850,birth_fraction_readings:['22/2','29/3'],birthplace_literal:'do',smallpox_literal:'v.',reading_literal:'vågrätt streck med en punkt',number_literal:'Ob[s] med diagonalstreck',own_blank_fields:['Giftoår och dag','Frejd,','Hvarifrån.','Hvarthän.','Anmärkningar.','förhör och nattvard 1850–1858'],row_crossed:false,death_note:null},os,'Två bevarade läsningar av samma cell, ingen vald dag. Följden av ortsdittot är en separat tolkning.');
 const birth=event(p,'birth',{precision:'year',value:'1850',literal:'1850; dagkonflikt22/2 mot29/3'},['A-2363','A-6961'],'Ingen exakt födelsedag antagen. Holm C/1 1850 oläst.');
 const conflict=fact(p,'birth_reading','same-cell-conflict',{year:1850,alternatives:['1850-02-22','1850-03-29'],chosen_date:null,source_count:1,second_reading:'29/3',argument:'9 har ögla/svans;3 går under linjen, jämförelse samma hand'},['A-6961',cs('C-0530')],'CONFLICT');
 const place=fact(p,'birthplace','ditto-Holm',{name:'Holm',raw:'do',chain:['Stefan Erik:Holm','Stina Cajsa:do','Jonas:do'],next_row:'Ingrid Brita:Stöde',own_birth_record_read:false},['A-6962']);
 const nf=fact(p,'name_form','household',{literal:'Jonas',project_surname:'Nordlund',own_surname_attested:false,heading_year1850:'redaktionellt särskiljande tillägg',father_same_name_is_distinct:'P-0415'},['A-6960',section(p,'Namnformer')]);
 const fam=family(p,['A-2363',section(p,'Relationer')]);
 const home=fact(p,'household_membership','Norafors-Stormyran',{parish:'Sättna',locality:'Norafors–Stormyran',folio:'255',book_period:'1850–1861',continuous_presence_proven:false,father_arrival_literal:'58 Stöde',own_arrival_field:'blank',own_departure_field:'blank',continuation_after1861_read:false,continued_residence_or_survival_proven:false},[section(p,'Boställen och flyttar'),'A-6965']);
 const scope=fact(p,'life_scope','source-limits',{birth_day_unresolved:true,death:null,burial:null,own_occupation:null,after1861:'oläst',blank_fields_prove_absence:false,reading_score_modern_translation:null,reading_score_not_intelligence_measure:true,military_title_belongs_to_father:true},[section(p,'Hälsa och död'),section(p,'Yrke, utbildning och ekonomi')]);
 assertion(p,'A-2363',[...o,...birth,conflict,place,...fam,home],'Egen sonrad och år/ort bevarade; äldre exaktdatum ersätts av uttrycklig konflikt.');
 assertion(p,'A-6960',[...o,nf],'Eget rånamn Jonas; familjenamn är en projekthärledning.');assertion(p,'A-6961',[...o,conflict,...birth],'Två läsningar i en källa, ingen dag vald.');assertion(p,'A-6962',[...o,place],'Dittokedjans råtecken och ortstolkning separerade.');
 for(const a of ['A-6963','A-6964','A-6965','A-6966'])assertion(p,a,[...o,home,scope],'Egna kolumnvärden, olöst marginalnot och begränsningar bevarade.');
 p.pending.push({origin:'A-6961',question:'Avgör 22/2 mot29/3 och eventuell hushållsboksfelskrivning med Holms egen födelsepost1850; accepterad händelse har endast år1850.'});
 save(p);
}
{
 const p=person('P-0421','Hela akt/profil och C-0530 lästa. Aktens senare påstående om saknad fullbild motsägs av citationens fil/hash och redan gjorda omläsningar; inga bilder öppnade nu. C-0530:s senare1/8 står mot aktens4/8, och systerns totala Holm1844-noll var redan supersederat. Historiska underkända kontraktsbedömningar bevaras.');
 core(p,own(p),'En avgränsad dotter i hushållet, utan konkurrerande person. UNDERKÄND identitets-/kontraktsnivå består; bevarandekorrigering är ingen automatisk ny granskning.');
 p.changes.find(m=>m.id===p.person).evidenceStatus='TRANSCRIBED';p.changes.find(m=>m.id===p.person).rationale='Egen separat personrad i C-0530; en källväg. Accepterad personidentitet ändrar inte kontraktsgranskningen.';
 const o=src(p,'C-0530','','C0530-own','Ingrid Brita','',{birth_year:1853,birth_fraction_readings:['4/8','1/8'],birthplace_literal:'Stöde',other_fields_individually_unextracted:true},['A-2364',cs('C-0530')],'Ingen separat råroll återgiven i avskriften; dotterrollen är en personslutsats. Senare1/8 och äldre4/8 bevaras som olöst läskonflikt.');
 const birth=event(p,'birth',{precision:'year',value:'1853',literal:'1853; 4/8 i akt, 1/8 i C-0530:s daterade omläsning'},['A-2364',cs('C-0530')],'Ingen vald exakt dag. Egen födelsepost i Stöde oläst.');
 const conflict=fact(p,'birth_reading','August-conflict',{year:1853,alternatives:['1853-08-04','1853-08-01'],chosen_date:null,source_count:1},['A-2364',cs('C-0530')],'CONFLICT');
 const bp=fact(p,'birthplace','household',{name:'Stöde',source:'retrospektiv hushållsuppgift',own_birth_record_read:false},['A-2364']);
 const fam=family(p,['A-2364',section(p,'Relationer')]);
 const home=fact(p,'household_membership','Norafors-Stormyran',{parish:'Sättna',locality:'Norafors–Stormyran',folio:'255',father_arrival_literal:'58 Stöde',own_move_fields:'inte individuellt utvunna',own_date_or_route_proven:false},['A-7941',cs('C-0530')],'TRANSCRIBED','Olika födelse-/bokföringssocknar anger två källortuppgifter, inte ensam en daterad egen eller samtidig familjeflytt.');
 const correction=fact(p,'source_assessment','preserved-image-and-stale-claims',{dossier_claim_image_missing:true,correction:'C-0530 anger bevarat fulloriginal C0033642_00280 med SHA256 samt omläsningar2026-09-07–09',image_sha256:'e891d66aa8dfb6759d069462a3a7b93f433ad7a1448fe90ef81313161d0510f0',new_archive_read:false,new_contract_review:false,sister_total_Holm1844_negative:'supersederat av ännu oidentifierad decemberpost17 i C-1042',own_birth_record_unread:true,own_other_columns_unextracted:true},['A-7941',cs('C-0530')],'CORROBORATED','Akt och profil bevaras med den daterade felbedömningen; motsägelsen synliggörs och forskningsstatus uppgraderas inte.');
 const nf=fact(p,'name_form','household',{literal:'Ingrid Brita',project_surname:'Nordlund',own_surname_attested:false,unattested_search_forms:['Britta','Ingeborg','Jonsdotter']},[section(p,'Namnformer')]);
 const bounds=fact(p,'life_scope','source-limits',{death:null,burial:null,death_absence_read:false,own_military_records_impossible:false,life_after_household:'okänt',full_contract:'UNDERKÄND',identity_review:'UNDERKÄND'},[section(p,'Hälsa och död'),section(p,'Militärt, civilt och rättsligt')],'TRANSCRIBED','Underlagets allmänna påstående att inga militära uppgifter kan finnas begränsas till dåtida värnplikt; ingen generell källomöjlighet sluts.');
 assertion(p,'A-2364',[...o,...birth,conflict,bp,...fam,nf],'Dotteridentitet och ort består; senare dagläsning redovisas uttryckligt utan vald dag.');
 assertion(p,'A-7941',[correction,home,bounds],'Sammansatt rad bevaras med explicit motuppgift om bild, systerns äldre noll och flyttslutsatsens gräns.');
 p.pending.push({origin:'A-2364',question:'Pröva 1853-08-04 i akt/profil mot 1/8 i C-0530:s tillägg2026-09-09 genom Stödes födelsepost. Ingen exakt dag har valts.'},{origin:'A-7941',question:'Ompröva profilens PK-/källvägsbedömningar som bygger på saknad C-0530-bild och totalt Holm1844-noll: fullbild/hash och decemberkandidat var redan bevarade. Själva dagkonflikten och egna kolumner återstår.'});
 save(p);
}
