import fs from 'node:fs';
import {openDB} from '../../lib/store.mjs';
import {inspect,personView} from '../../lib/domain.mjs';
import {impact} from '../../lib/impact.mjs';
const db=openDB('genealogy2/data/research.sqlite',{readOnly:true}),dir='genealogy2/verification/T-0675/';
const scope=JSON.parse(fs.readFileSync(dir+'scope.json')).records.filter(r=>[12,18,23,40,46].includes(r.number));
const firstA=JSON.parse(fs.readFileSync(dir+'ebbamoves-first-initial.json')),firstB=JSON.parse(fs.readFileSync(dir+'root-ebba-two-first-initial.json')),second=JSON.parse(fs.readFileSync(dir+'ebba-five-second-initial.json'));
const reason='T-0675 AK1–4: fem fulla egna flytt-/hushållsrader, två låsta avskriftsblinda pass och källargument; rätta läsning, kolumnsemantik och individuella följder. Inga nya identitets- eller trädgrindar.';
const changes=new Map(),reviews=[];
const notes={12:'Egen rad19 har utflytt30 23/10 och separat not fl[?]30 20/10; tidigare påstående om22/10 i flyttboken upphävs av post23. Kol11 a och kol12 våg-/n-tecken är skilda kolumner; kol13 är tom.64 och34 är små marginaltal vid tryckt radnummer19, inte datum eller död.',18:'Egen rad24 har inflytt Östhammar30 23/10, inte äldre22/10. ord. folkskoll. är källans titel, inte bevisat exakt anställningsdatum. Kol13 Bevistat husförhör år bär svagt30 på rad24s sida av övre linjen. Överföring1006 år32, inget exakt överföringsdatum.',23:'Betyg20/10 och utflytt23/10. Roots låsta FIRST20/10 i utflyttningsfältet förkastas efter eget större utsnitt: sista3 har två öppna bågar, skilt från betygsfältets slutna0 och grannarnas2. SECOND23/10 stöds lokalt av tecknen, inte genom harmonisering med andra poster. K.13[initial något reserverad], inte tidigareN.13. Födelsedatumfält tomt.',40:'Inflytt15/12 under rubrik1928; folkskoll. tillhör egen namnrad. K.13[ornamenterad initial], inte äldreN.13; uppslag19. Födelsedatumfält tomt. Ingen exakt skola eller examen anges.',46:'Betyg4/7 och utflytt7/7 under rubrik1930, inte två4/7. FIRST reserverade födelsedag22[?], SECOND läser22; ingen födelsedagsändring. Uppslag73 enligt SECOND och tidigare text; FIRST79[?] är kvarstående grafisk reservation och är inte stöd för att ändra söknyckeln till79. Frånort ditto till Bastuträsk; lär. titeln avser kyrkobokföring, inte exakt tjänstematrikel. Församlingsstämpeln oläst i båda passen.'};
const common='Samma original och registreringskedja är inte oberoende historiska vittnen. Råförkortningar, blankfält och osäkra tecken bevaras. Person-/ortkunskap fanns före passen, men deras aktuella avskrifter var låsta före modelljämförelse.';
function ev(n){return {object:`TR-T0675-EM-${n}`,version:1,role:'supports',note:'Avgränsad fullpostkontroll med två låsta läsningar och efterföljande teckenargument.'};}
function add(id,kind,data,evidence,caveat){changes.set(id,{id,kind,expectedVersion:null,data,disposition:'recorded',rationale:reason,caveat,origins:[],evidence});}
function revise(id,edit,evidence,note,{caveat=null}={}){
 if(changes.has(id))throw Error('duplicate '+id);
 const x=inspect(db,id),r=x.revisions.at(-1),data={...r.data};delete data.revision_id;
 for(const k of Object.keys(data))if(k.endsWith('_json')&&typeof data[k]==='string')data[k]=JSON.parse(data[k]);
 edit(data);
 const oldEv=r.evidence.map(e=>{let a=e.basis_revision_id.lastIndexOf('@');return{object:e.basis_revision_id.slice(0,a),version:+e.basis_revision_id.slice(a+1),role:e.role,note:e.note};});
 const all=[...oldEv,...evidence],dedup=[...new Map(all.map(e=>[`${e.object}@${e.version}/${e.role}`,e])).values()];
 changes.set(id,{id,kind:x.kind,expectedVersion:x.currentVersion,data,disposition:r.disposition,evidenceStatus:r.evidence_status,rationale:note,caveat:caveat??(note+'\n\nTidigare förbehåll bevaras som historik där ovan preciserat:\n'+r.caveat),origins:r.origins.map(o=>({unit:o.id,coverage:o.coverage,note:o.note})),evidence:dedup});
 reviews.push({object:id,revision:x.current.revision_id,decision:'revise',rationale:note});
}
for(const s of scope){const n=s.number,rc=inspect(db,s.record),read=rc.current.readings[0]?.object_id;
 add(`TR-T0675-EM-${n}`,'transcription',{record_id:s.record,text:JSON.stringify({first:(firstA.records.find(r=>r.number===n)||firstB.records.find(r=>r.number===n)),second:second.records.find(r=>r.number===n),adjudication:notes[n],limits:common},null,2),reading_note:notes[n]+' '+common},[{object:s.record,version:rc.currentVersion,role:'derived_from',note:'Exakt bevarad fullbild och hash i båda låsta protokollen.'}],notes[n]);
 add(`AUDIT-T0675-EM-${n}`,'assessment',{subject_id:s.record,criteria:'original_revision/1',outcome:'bounded_fields_examined_with_reservations',body:notes[n]+' '+common},[ev(n)],reason);
 revise(s.record,d=>{},[],notes[n]);
 changes.get(s.record).assets=rc.current.media.filter(m=>m.origin==='legacy').map(m=>({path:m.path,region:m.region}));
 const tr=db.prepare('SELECT v.object_id FROM transcription t JOIN current_revision v ON v.id=t.revision_id WHERE t.record_id=?').all(s.record);
 for(const t of tr)revise(t.object_id,d=>{d.reading_note=notes[n]+'\n\nTidigare läsanteckning bevarad som historik:\n'+d.reading_note;},[ev(n)],notes[n]);
 if(read)revise(read,d=>{d.body=notes[n]+'\n\nTidigare avgränsning bevarad:\n'+d.body;},[ev(n)],notes[n]);
}
const chronology='T-0675 aktuell flyttkronologi: Östhammars betyg20/10 1930 hålls skilt från utflyttningsdag23/10 i B/6 nr34 och23/10 i AIIa5 rad19. Burträsk AIIa3c fol959 rad24 anger egen inflyttning23/10. Äldre22/10 och22/23-alternativ var avskriftsfel, inte kvarstående källkonflikt. Kyrkobokföring och ord./e.o. folkskoll.-titlar daterar inte exakt anställningsstart, skolår eller examen.';
revise('O-P-0002-C0892-columns',d=>{d.property='vaccination_and_church_columns';d.value_literal='kol6 v; kol11 a; kol12 våg-/n-liknande tecken; kol13 tom';d.value_json={vaccination_raw:'v',christian_knowledge_raw:'a',communion_symbol_raw:'våg-/n-liknande tecken',household_examination_year:null,prior_value_preserved:d.value_json};},[ev(12)],'Kol11 kristendom och kol12 nattvard ska inte slås ihop till religiousKnowledge=a N. Grafiskt tecken kvar med reservation; ingen konkret nattvardshändelse eller skolexamen härleds.');
for(const type of ['arrival','departure']){
 const id=`E-${type}-P-0002-Burtrask-1930`,old=inspect(db,id);
 revise(id,d=>{d.date_json={literal:'1930-10-23',precision:'exact',value:'1930-10-23'};},type==='arrival'?[ev(18)]:[ev(12),ev(23)],chronology);
 revise(`EP-${id}-P-0002-migrant`,d=>{},[{object:id,version:old.currentVersion+1,role:'supports',note:'Samma migrant och oförändrade orter; reviderad egen händelsedag.'}],`Deltagaren P-0002 och migrantrollen består i ${id}; endast händelsens datum rättas med egen källpost. ${chronology}`);
}
revise('F-P-0002-residence-Osthammar1928-1930',d=>{d.value_json={...d.value_json,endReadings:['1930-10-23']};},[ev(12),ev(23),ev(40)],'Boställe Kyrkokvarteret n:o13/folio19 och början1928-12-15 består; slutdagens äldre22/23-läsningar rättas till23/10 efter varsin egen källa. '+chronology);
revise('F-P-0002-occupation-Gammelbyn1930',d=>{const v={...d.value_json};delete v.from;d.value_json={...v,registered_arrival:'1930-10-23',occupation_raw:'ord. folkskoll.',appointment_start:null};},[ev(18)],'Källraden bär ord. folkskoll. och inflytt23/10, inte anställning från22/10. Byt från-fält till registrerad ankomst och uttryckligt okänd anställningsstart; yrket/orten och reservation om kontinuitet består.');
const currentP=JSON.parse(fs.readFileSync(dir+'ebbamoves-comparison-current-snapshot.json'));
// Review actual current heads, not snapshots, for all person-local text objects.
const candidateIds=new Set();
function collect(v){if(Array.isArray(v)){for(const x of v)collect(x);}else if(v&&typeof v==='object'){if(v.object_id)candidateIds.add(v.object_id);for(const [k,x]of Object.entries(v))if(!['origins','legacy','evidence','conversion'].includes(k))collect(x);}}
collect(currentP['P-0002']);collect(currentP['P-0001']);
const p2Specific={
 'P-0002/Q-01':'Utbildningsfrågan förblir öppen; tjänste-/bostadskronologins slut22/10 ska läsas23/10 och ger inte exakta skolår.',
 'THEME-P-0002-ARB':'Yrkesbanans registreringsdatum23/10 ersätter22/10; ordinarietiteln är belagd men exakt tillsättningsdag förblir okänd.',
 'PATH-P-0002-KP-04':'Skolråds-/skolstyrelsevägens datumankare rättas till registrerad ankomst23/10; pröva fortfarande tjänstebeslut och skola separat.',
 'BIO-P-0002':'Biografins egen Östhammar/Burträskkronologi rättas till23/10, betyg20/10; övriga livsskeden och aktuella gravregisterreservationer består.',
 'RESEARCH-P-0002-9d76f0343410':'Egen samlad forskningskronologi och äldre återgiven fol959-rad22/10 rättas till23/10. Tidigare native rättelser av husförhörsrader1006/275 och Uppsala Dk/omärkt gravfält bevaras.',
 'ASSESSMENT-P-0002':'Profilens kopierade tids-/yrkeskronologi kvalificeras; identitets-/träd-/helkontraktsgranskningens utfall omprövas inte av läsfelet.'
};
const folionote='Bastuträsks sökuppslag behålls som73 enligt SECOND och tidigare läsning, men FIRST79[?] dokumenteras som grafisk reservation; ingen övergång till79 och själva hushållsuppslaget förblir oläst. Betyg4/7 och utflytt7/7 är skilda. Detta är inte nytt belägg för tidigare tjänsteår.';
for(const id of [...candidateIds].sort()){
 if(changes.has(id))continue;
 let x;try{x=inspect(db,id);}catch{continue;}
 const r=x.revisions.at(-1),d=r.data;
 if(!['assessment','question','narrative','fact','observation'].includes(x.kind))continue;
 const fields=['body','markdown','title'];const text=fields.map(k=>d[k]||'').join('\n');
 const ownP2=(d.subject_id==='P-0002'||id.startsWith('RESEARCH-P-0002')||id.startsWith('BIO-P-0002'));
 const oldCaveat=(r.caveat||'').includes('Utflyttningsdagen 1930 behåller 22/23 oktober.');
 const historicCaveat=(r.caveat||'').includes('Föregående förbehåll ordagrant bevarat som historik:');
 if(ownP2&&(p2Specific[id]||(oldCaveat&&!historicCaveat))){
  const note=(p2Specific[id]||`Objektets sakutfall och huvudinnehåll består; dess delade aktuella caveat22/23 kvalificeras för just ${id}.` )+' '+chronology;
  revise(id,data=>{if(p2Specific[id]){const key=('body'in data?'body':('markdown'in data?'markdown':null));if(key)data[key]=note+'\n\nTidigare innehåll bevarat; endast ovan nämnda sakfält ersätts:\n'+data[key];}},[ev(12),ev(18),ev(23)],note);
 }else if(id.includes('P-0001')&&(/uppslag 73/.test(text)||id==='O-P-0001-C0893-certificate1930')){
  revise(id,data=>{const key=('body'in data?'body':('markdown'in data?'markdown':null));if(key)data[key]=folionote+'\n\nTidigare text:\n'+data[key];},[ev(46)],`Individuell kontroll av ${id}: ${folionote}`);
 }else if(ownP2&&oldCaveat&&historicCaveat){reviews.push({object:id,revision:x.current.revision_id,decision:'historical_text_retain',rationale:'22/23 finns i uttryckligt historikblock i caveat. Aktuell egenfältsprecisering gäller gravregister/annan fråga och påstår inte22/23 på nytt. Ingen sakrevision behövs.'});}
}
// A source-bound certificate observation is relevant even if not surfaced in the person snapshot.
if(!changes.has('O-P-0001-C0893-certificate1930'))revise('O-P-0001-C0893-certificate1930',d=>{},[ev(46)],'Betygsdag1930-07-04, lär., från Bastuträsk till Burträsk består; den skilda utflyttdagen7/7 gör inte betygsfältet fel. '+folionote);
// Reviewed final bindings: same bounded records now carry current caveats; event roles
// preserve the same migrant while binding to the corrected dated event revision.
const rebinding=[];
for(const c of changes.values()){
 for(const e of c.evidence){const target=changes.get(e.object);if(target){const final=(target.expectedVersion??0)+1;if(e.version!==final){rebinding.push({object:c.id,basis:e.object,old:e.version,final,reason:c.kind==='participation'?'Samma migrantroll, rättad händelsedag.':'Samma avgränsade källpost; egen rättad läsning/kolumnsemantik prövad ovan.'});e.version=final;}}}
 c.evidence=[...new Map(c.evidence.map(e=>[`${e.object}@${e.version}/${e.role}`,e])).values()];
}
const ordered=[],done=new Set(),active=new Set();
function visit(id){if(done.has(id))return;if(active.has(id))throw Error('Cyclic proposed evidence '+id);active.add(id);const c=changes.get(id);for(const e of c.evidence)if(changes.has(e.object))visit(e.object);active.delete(id);done.add(id);ordered.push(c);}
for(const id of changes.keys())visit(id);
fs.writeFileSync(dir+'ebbamoves-final-bindings.json',JSON.stringify({rebinding,cycle_check:'PASS',record_media_preserved:true},null,2)+'\n');
const op={id:'T-0675/Ebba-moves-five-v1',actor:'codex',reason,changes:ordered};
fs.writeFileSync(dir+'ebbamoves-proposed-operation.json',JSON.stringify(op,null,2)+'\n');
fs.writeFileSync(dir+'ebbamoves-individual-followup.json',JSON.stringify({task:'T-0675',stage:'proposed_not_applied',chronology,notes,common,folio_reservation:folionote,individual:reviews,requires_after_apply:'Root ska pröva faktiska pending ids efter apply; inga påhittade resolve här. Reread stale versions if other work updates shared objects.'},null,2)+'\n');
console.log({changes:changes.size,reviews:reviews.length});
