// Bounded additions after the complete source reading. Does not touch earlier frozen packets.
import fs from 'node:fs';
import{db,doc,units,origins,exact,unknown,person,add,assertion,relationRow,section,reuse,known,core,fact,relation,event,src,cs}from './genealogy2-persons10-combined.mjs';
const path='genealogy2/migration/persons-10-b.json',rows=JSON.parse(fs.readFileSync(path));
const p=rows.find(p=>p.person==='P-0474'),q=rows.find(p=>p.person==='P-0475');
if(p.changes.some(x=>x.id==='F-P-0474-occupation-documented-service'))throw Error('Refinements already present');
const job=fact(p,'occupation','documented-service',{attested_service:{place:'Jernbol',employer:'Anders Andersson',from:'hösten1837',attestation:'1840-12-14',title:'dräng'},military:{unit:'Livkompaniet,Södermanlandsregemente',rote36:'Glippsta',rote38:'Hagby',status1841_1855:'soldat'},later:{status:'avskedad soldat, gratialist',sources:'egnaHFL1876–1895',retirement_date:null,pension_amount:null},probate1883_spouse_index_title:'torpare',ownership_not_implied:true},[section(p,'Yrke, utbildning och ekonomi'),cs('C-0793'),cs('C-0752'),cs('C-0732'),cs('C-0759')]);
const approval=event(p,'other',exact('1841-02-15'),['A-3038',cs('C-0793')],'Approberas är daterat15feb; GMR1842s18feb separat ersättningsuppgift.',null,'TRANSCRIBED','E-military-approval-P-0474-1841');
const replacement=event(p,'other',exact('1841-02-18'),['A-2966',cs('C-0763')],'GMR1842s rapporterade ersättningsdag, inte harmoniserad med rekryteringsbladets15feb.',null,'TRANSCRIBED','E-military-replacement-P-0474-1841');
const transport=event(p,'other',{precision:'unknown',literal:'25[?] juli1851[?]'},['A-2937','A-4626',cs('C-0752')],'Positivtransport36Glippsta→38Hagby, dag/årreserverat; inte personligtavsked.',null,'TRANSCRIBED','E-military-transfer-P-0474-Hagby');
for(const[k,ids]of[['A-3038',approval],['A-2966',replacement],['A-2937',transport],['A-4626',transport]])p.assertions.find(x=>x.id===k).targets.push(...ids);
// A source-bound mother's/father's role is distinct from the child's principal role.
for(const target of [p,q]){
 const pairs=target.person==='P-0474'?[['P-0133','M-P-0474-Erik-father']]:[['P-0494','M-P-0475-CarlJohan-mother'],['P-0495','M-P-0475-AnnaLotta-mother'],['P-0499','M-P-0475-MariaSofia-mother'],['P-0133','M-P-0475-Erik-mother']];
 for(const[child,m]of pairs)for(const kind of ['birth','baptism']){const id=`E-${kind}-${child}`;reuse(target,id,[section(target,'Relationer')]);const ep=`EP-${id}-${target.person}-parent`;if(!known(ep))add(target,ep,'participation',{event_id:id,person_id:target.person,mention_id:m,role:'parent'},[section(target,'Relationer')],[],'Egen föräldraroll i barnets post, inte överfört eget födelsedatum.');else reuse(target,ep,[section(target,'Relationer')]);}
}
// Attach the actual reused witness participations to each individual relation decision.
for(const target of [p,q])for(const[c,entries]of[
 ['0494',[['Jonas Andersson','JonasAndersson'],['Maja St. Gustafsdotter','MajaStGustafsdotter'],['Cajsa Greta Ersdotter','CajsaGretaErsdotter'],['Petter Ersson','PetterErsson']]],
 ['0495',[['Nils Thor','NilsThor'],['Ann. St. Jansdotter','AnnStJansdotter'],['Carl Otto Nilsson','CarlOttoNilsson'],['Ann. M. Söderberg','AnnMSoderberg']]],
 ['0499',[['August Werner','AugustWerner'],['Eva Lotta Olsdotter','EvaLottaOlsdotter'],['Carl Joh. Jansson','CarlJohJansson'],['Gustafva Olsdotter','GustafvaOlsdotter']]]])for(const[name,key]of entries){const u=units(target.person,'person').find(u=>u.kind==='relation_row'&&JSON.parse(u.parsed_json).cells[0].includes(name));target.relations.find(x=>x.unit===u.id).targets.push(`EP-E-baptism-P-${c}-${key}-witness`);}
// Preserve the exact negative searches on marriage sequences without merging sources.
const query='Carl/Carl Fredric Grill/Drill och Johanna Jansdotter/Jonsdotter';
for(const[key,sid,cid,bounds]of[
 ['Bettna-marriage1840-1843','S-0553','C-0718',{volume:'BettnaEI2',period:'1840–1843',images:'C0005885_00036–00042'}],
 ['Bettna-marriage1844-1845','S-0592','C-0763',{volume:'BettnaEI2',period:'1844–1845',images:'C0005885_00043–00046'}],
 ['Bjorkvik-marriage1841','S-0553','C-0718',{volume:'BjörkvikEI2',year:1841,images:'C0005942_00191–00192',boundary:'193börjar1842'}],
 ['Bjorkvik-marriage1842-1845','S-0592','C-0763',{volume:'BjörkvikEI2',period:'1842–1845',images:'C0005942_00193–00196'}],
 ['StoraMalm-marriage1842-1845','S-0592','C-0763',{volume:'StoraMalmEI2',period:'1842–1845',images:'C0007593_00076–00087'}]
]){const id=`SEARCH-P-0475-${key}`;add(q,id,'search',{source_id:sid,question_id:null,outcome:'negative',scope_json:{description:'Fullt avgränsad vigselföljd utan paret, inte generellt vigselnoll.',query,bounds},body:'Komplett relevant följd enligt C0718/C0763, ingen införd vigsel för paret; lysning1841/1843 är separat positivuppgift.'},['A-2972',cs(cid)],[],'Inga bredare perioder eller personfrånvaro.','NEGATIVE','recorded');q.assertions.find(x=>x.id==='A-2972').targets.push(id);reuse(p,id,[section(p,'Militärt, civilt och rättsligt')]);}
const mainsources=fact(p,'source_assessment','source-forms-not-globalized',{Carl_Eric_in_HFL_rejected:true,C0147_latest_own_raw:'Soldaten Carl Er. Grill',Er_abbreviation_not_silently_changed_to_Fr:true,other_C0702_C0794_Fr_Drill_corrections_are_post_specific:true},['A-2837',cs('C-0147'),cs('C-0702'),cs('C-0794')]);p.assertions.find(x=>x.id==='A-2837').targets.push(mainsources);
// New origin aliases are resolved exactly as save() resolves them, without re-adding people.
for(const target of [p,q]){const own=new Map(units(target.person,'person').filter(u=>u.kind==='assertion'&&!u.historical).map(u=>[u.legacy_id,u.id]));for(const m of [...target.changes,...target.reuse])m.origins=m.origins.map(o=>typeof o==='string'&&own.has(o)?own.get(o):o);}
const tmp=path+'.writing-'+process.pid;fs.writeFileSync(tmp,JSON.stringify(rows,null,2)+'\n');fs.renameSync(tmp,path);
