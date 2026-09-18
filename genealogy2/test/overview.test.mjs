import test from 'node:test';
import assert from 'node:assert/strict';
import {renderPersonOverview} from '../lib/overview.mjs';

const object=(id,kind,data={},extra={})=>({object_id:id,revision_id:`${id}@1`,version:1,kind,disposition:'accepted',evidence_status:'TRANSCRIBED',rationale:'Avgränsat syntetiskt underlag.',caveat:'',pending_reviews:[],...data,...extra});
const view=extra=>({id:'P',person:object('P','person',{display_name:'Exempel'}),events:[],relations:[],facts:[],contextFacts:[],observations:[],mentions:[],identities:[],identityResolutions:[],importAssessments:[],identityMappings:[],questions:[],assessments:[],searches:[],narratives:[],interpretationQuestions:[],legacy:[],research:{questions:[],themes:[],requirements:[],paths:[],keys:[],reviews:[]},...extra});
const event=(id,date,role='principal',extra={})=>object(id,'event',{event_id:id,event_type:'birth',date_json:JSON.stringify(date),place_id:null,place_role:'registered_birth_parish',participation:object(`EP-${id}`,'participation',{event_id:id,person_id:'P',role}),qualifications:[],...extra});
const axis=(outcome,extra={})=>({outcome,usable:true,assessments:[],ignored_assessments:[],issues:[],...extra});
const gate=extra=>({person_id:'P',passed:false,reasons:[],identity_review:axis('failed'),tree_effect:axis('waiting'),life_picture_review:axis('failed',{scope:'legacy_full_contract'}),...extra});

test('kandidathändelse och deltagaridentitet blir inte fastställd genom accepterad personkärna',()=>{
  const e=event('E',{precision:'year',value:'1800',literal:'1800'},'child',{disposition:'candidate',caveat:'Barnet kan vara en annan person.'});
  e.participation.disposition='candidate';e.participation.caveat='Barnidentiteten saknar brygga till den vuxne.';
  const v=view({events:[e],identities:[object('ID','identity',{mention_id:'M',person_id:'P',decision:'candidate'},{disposition:'candidate',evidence_status:'LEAD'})]});
  const before=JSON.stringify(v),out=renderPersonOverview(v);
  assert.match(out,/Födelse — kandidat; TRANSCRIBED/);
  assert.match(out,/Egen roll: \*\*barn\*\* — kandidat/);
  assert.match(out,/kandidat; LEAD/);
  assert.match(out,/Identitetsgranskning:\*\* ej läst/);
  assert.doesNotMatch(out,/GODKÄND/);
  for(const x of [e.caveat,e.participation.caveat])assert(out.includes(x));
  assert.equal(JSON.stringify(v),before,'renderer muterade personvyn');
});

test('kronologin använder typade datum och bevarar intervall, alternativ och alfabetiska råformer',()=>{
  const v=view({events:[
    event('E-first-alphabetic',{precision:'unknown',literal:'April, år oläst'}),
    event('E-A-later',{precision:'exact',value:'1901-01-01',literal:'Nyårsdagen 1901'}),
    event('E-Z-range',{precision:'range',from:'1899-02-01',to:'1899-02-28',literal:'Februari, dagen olöst'}),
    event('E-Q-alternatives',{precision:'alternatives',values:['1900-08-19','1900-08-08'],literal:'8 eller 19 augusti'}),
    event('E-Y-year',{precision:'year',value:'1898',literal:'året 1898'}),
    event('E-X-circa',{precision:'circa',value:'1897-01-02',literal:'omkring 2 januari 1897'})
  ]});
  const out=renderPersonOverview(v);
  const markers=['1897-01-02 — omkring','1898 — år','1899-02-01–1899-02-28 — intervall','1900-08-19 eller 1900-08-08 — alternativ','1901-01-01 — exakt datum','okänt datum; källform: April, år oläst'];
  let previous=-1;for(const marker of markers){const pos=out.indexOf(marker);assert(pos>previous,marker);previous=pos;}
  assert(out.includes('Februari, dagen olöst'));
  assert.doesNotMatch(out,/April, år oläst.*— exakt datum/);
});

test('samma händelse grupperas men båda deltagarrollerna och samtliga hela förbehåll består',()=>{
  const common='Hemvist är inte en fastställd fysisk födelsebyggnad. Reservationen gäller hela jämförelsen.';
  const first=event('E',{precision:'exact',value:'1900-01-01',literal:'1900-01-01'},'mother',{caveat:common});
  first.participation.caveat='Modersrollen har ett eget identitetsförbehåll.';
  const second=structuredClone(first);second.participation=object('EP-other','participation',{event_id:'E',person_id:'P',role:'witness'},{caveat:'Vittnesrollen bevisar inget moderskap.',disposition:'candidate'});
  second.qualifications=[object('F-E','fact',{subject_id:'E',property:'source_scope',value_json:JSON.stringify({scope:'en post'})},{caveat:common})];
  first.qualifications=second.qualifications;
  const out=renderPersonOverview(view({events:[second,first]}));
  assert.equal((out.match(/Födelse —/g)??[]).length,1);
  assert.match(out,/Egen roll: \*\*mor\*\* — accepterad/);
  assert.match(out,/Egen roll: \*\*vittne\*\* — kandidat/);
  assert.equal(out.split(common).length-1,1,'gemensamt förbehåll dubblerades');
  for(const p of [first.participation,second.participation])assert(out.includes(p.caveat));
  assert(out.includes('F-E@1'));
});

test('arkivreferens visar avvisad läsning, inaktiv fråga och väntande omprövning på importbedömningen',()=>{
  const p={id:'review-1',reason:'Rättad källrad behöver följas upp.',changed_revision_id:'O-source@2'};
  const a=object('IMPORT-P','assessment',{outcome:'rejected_reading',body:'Denna namnform är en avvisad läsning. Faderskonflikten är fortfarande olöst.'},{disposition:'rejected',pending_reviews:[p],caveat:'Ingen separat person har belagts.'});
  const q=object('Q','question',{title:'Historisk fråga',outcome:'ÖPPEN',active:false,outcome_code:'open'},{disposition:'retired'});
  const out=renderPersonOverview(view({person:null,identityMappings:[{legacy_id:'P',target_id:'P2',mapping_type:'archival_reference',rationale:'Hänvisning, inte alias.'}],importAssessments:[a],research:{questions:[q]}}),{gate:gate()});
  assert.match(out,/Arkivreferens utan egen personkärna/);
  assert.doesNotMatch(out,/Verklig person i modellen/);
  assert(out.includes(a.body));assert(out.includes(a.caveat));assert(out.includes(p.reason));
  assert.match(out,/0 aktiva, 1 inaktiva/);assert.match(out,/1 väntande beroendeomprövningar/);
  assert.match(out,/Omprövning väntar/);assert.match(out,/IMPORT-P@1/);
});

test('alias och avvecklad verklig person är olika fall',()=>{
  const alias=renderPersonOverview(view({person:null,identityMappings:[{legacy_id:'P',target_id:'P2',mapping_type:'same_identity',rationale:'Samma person.'}]}));
  assert.match(alias,/Alias för `P2`/);assert.doesNotMatch(alias,/Verklig person i modellen/);
  const actual=renderPersonOverview(view({person:object('P','person',{display_name:'Verklig person',legacy_state:'retired'}),identityMappings:[{legacy_id:'P',target_id:'P',mapping_type:'archival_reference',rationale:'Avvecklad forskning, verklig person.'}]}));
  assert.match(actual,/Verklig person i modellen/);assert.match(actual,/Detta avvisar inte personens existens/);
  assert.doesNotMatch(actual,/Arkivreferens utan egen personkärna/);
});

test('granskningsaxlar och fristående rättelser syns utan att äldre fullkontrakt blir aktuell livsbildsgranskning',()=>{
  const correction=object('A-correction','assessment',{criteria:'life_picture_correction/1',outcome:'failed',body:'Tidigare fullkontraktsgodkännande gäller inte den oprövade livsbilden.'});
  const out=renderPersonOverview(view(),{gate:gate({passed:true,identity_review:axis('passed'),tree_effect:axis('supporting'),other_assessments:[correction]})});
  assert.match(out,/Identitetsgranskning:\*\* GODKÄND/);assert.match(out,/Trädverkan:\*\* BÄRANDE/);
  assert.match(out,/separat livsbildsgranskning saknas i grinden; äldre fullkontrakt: UNDERKÄND/);
  assert(out.includes(correction.body));
  assert.throws(()=>renderPersonOverview(view(),{gate:{...gate(),person_id:'OTHER'}}),/annan person/);
});

test('konflikter och korrigerande sakbedömningar syns även när caveat är tomt',()=>{
  const conflict=object('F-conflict','fact',{subject_id:'P',property:'migration_date_conflict',value_json:JSON.stringify({receiver_literal:'1878-05-21',sender_literal:'1878 8[5?]/12',chosen_actual_move_date:null})},{evidence_status:'CONFLICT'});
  const correction=object('F-family','fact',{subject_id:'P',property:'family_context',value_json:JSON.stringify({oldest_claim:{old:'1853 äldst',correction:'Ett äldre barn 1851 är belagt.'}})});
  const out=renderPersonOverview(view({facts:[conflict,correction]}));
  assert.match(out,/Motstridiga flyttdatum — accepterad; CONFLICT/);
  for(const value of ['1878-05-21','1878 8[5?]/12','Vald faktisk flyttdag: ej angivet','Ett äldre barn 1851 är belagt.'])assert(out.includes(value));
  assert.match(out,/--full --format markdown/);assert.match(out,/inspect OBJEKT-ID/);
});
