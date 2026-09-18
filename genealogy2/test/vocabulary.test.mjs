import test from 'node:test';
import assert from 'node:assert/strict';
import {openDB} from '../lib/store.mjs';
import {applyOperation,readCurrent,researchOutcome} from '../lib/domain.mjs';
import {canonicalParticipationRole,findParticipations,canonicalQuestionOutcome,questionOutcomeView,PARTICIPATION_ROLE_VOCABULARY,QUESTION_OUTCOME_VOCABULARY} from '../lib/vocabulary.mjs';

const change=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,disposition:'recorded',rationale:'Syntetiskt ordförrådsprov',...extra});
const support=object=>({object,version:1,role:'supports'});

function fixture(t) {
  const db=openDB(':memory:',{create:true});t.after(()=>db.close());
  const source=change('S','source',{title:'Syntetisk bok',description:'Två dopvittneskoder och åtskilda bedömningar'});
  const participants=[
    ['W-old','E-baptism',null,'M-Carl','baptism_witness','recorded'],
    ['W-new','E-baptism','P-witness','M-Olof','witness','accepted'],
    ['W-candidate','E-baptism','P-candidate','M-candidate','witness','candidate'],
    ['P-baby','E-baptism','P-child','M-child','principal','accepted'],
    ['P-child-role','E-baptism','P-child',null,'child','recorded'],
    ['P-baptized','E-baptism','P-child',null,'baptized','accepted'],
    ['EP-father','E-baptism','P-father',null,'father','accepted'],
    ['P-emergency','E-baptism',null,null,'emergency_baptizer','recorded'],
    ['W-marriage','E-marriage',null,null,'witness','accepted'],
    ['W-misplaced','E-marriage',null,null,'baptism_witness','candidate'],
    ['P-unknown','E-baptism',null,null,'unreviewed_role','recorded'],
    ['P-history','E-baptism',null,null,'baptism_witness','recorded'],
  ];
  applyOperation(db,{id:'vocabulary-fixture',actor:'test',reason:'Isolerad minnesdatabas',changes:[source,
    change('R','record',{source_id:'S',record_type:'baptism',locator:'egen post',dependence_note:''}),
    ...['P-witness','P-candidate','P-child','P-father','P-other'].map(id=>change(id,'person',{display_name:id},{evidence:[support('R')]})),
    ...[['E-baptism','baptism'],['E-marriage','marriage']].map(([id,type])=>change(id,'event',{
      event_type:type,date_json:{precision:'year',value:'1815',literal:'1815'},place_role:'registered_parish',
    },{disposition:'accepted',evidenceStatus:'TRANSCRIBED',caveat:'Händelsens eget förbehåll',evidence:[support('R')]})),
    ...[['M-Carl','Carl Andersson','dräng i Botsmark, dopvittne'],['M-Olof','Olof Anderss[on]',''],['M-candidate','Anna[?]','piga[?]'],['M-child','Sven','barn']].map(([id,name,role])=>change(id,'mention',{
      record_id:'R',name_literal:name,role_literal:role,
    },{evidenceStatus:'TRANSCRIBED',caveat:'Omnämnandets eget förbehåll',evidence:[support('R')]})),
    // Even an accepted identity must not fill participation.person_id implicitly.
    change('ID-Carl','identity',{mention_id:'M-Carl',person_id:'P-witness',decision:'accepted'},{disposition:'accepted',evidence:[support('M-Carl')]}),
    ...participants.map(([id,event,person,mention,role,disposition])=>change(id,'participation',{
      event_id:event,person_id:person??(mention?null:'P-other'),mention_id:mention,role,
    },{disposition,evidenceStatus:disposition==='candidate'?'LEAD':'TRANSCRIBED',caveat:`Deltagarens förbehåll: ${id}`,evidence:[support('R')]})),
  ]});
  // The old witness revision must remain in history without appearing as current.
  applyOperation(db,{id:'role-review',actor:'test',reason:'Syntetisk rättelse av rollen',changes:[
    change('P-history','participation',{event_id:'E-baptism',person_id:'P-other',mention_id:null,role:'officiant'},
      {expectedVersion:1,bindings:{'E-baptism':1},evidence:[support('R')]})]});
  // A later source reading creates pending reviews, which the query must show.
  applyOperation(db,{id:'source-review',actor:'test',reason:'Syntetisk ändrad läsning',changes:[
    {...source,expectedVersion:1,data:{...source.data,description:'Rättad syntetisk källbeskrivning'}}]});
  return db;
}

test('dopvittnesalias är händelsebundet och okända rollord bevaras',()=>{
  assert.equal(canonicalParticipationRole('baptism_witness','baptism'),'witness');
  assert.equal(canonicalParticipationRole('baptism_witness','marriage'),'baptism_witness');
  assert.equal(canonicalParticipationRole('baptism_witness',null),'baptism_witness');
  for(const role of Object.keys(PARTICIPATION_ROLE_VOCABULARY).filter(r=>r!=='baptism_witness'))assert.equal(canonicalParticipationRole(role,'baptism'),role);
  for(const raw of ['new_role','WITNESS',' witness ',''])assert.equal(canonicalParticipationRole(raw,'baptism'),raw);
  assert.equal(canonicalParticipationRole(null,'baptism'),null);
  assert.equal(canonicalParticipationRole(undefined,'baptism'),null);
  assert.throws(()=>canonicalParticipationRole(7,'baptism'),TypeError);
});

test('båda dopvittneskoder hittas, utan dopbarn, föräldrar, förrättare eller vigselvittnen',t=>{
  const db=fixture(t);
  const hits=findParticipations(db,{role:'witness',eventType:'baptism'});
  assert.deepEqual(hits.map(r=>r.object_id),['W-candidate','W-new','W-old']);
  assert.deepEqual(findParticipations(db,{role:'baptism_witness',eventType:'baptism'}),hits);
  assert(hits.every(r=>r.canonicalRole==='witness'&&r.knownRole));
  assert.equal(hits.find(r=>r.object_id==='W-old').storedRole,'baptism_witness');
  assert.deepEqual(findParticipations(db,{role:'principal',eventType:'baptism'}).map(r=>r.object_id),['P-baby']);
  assert.deepEqual(findParticipations(db,{role:'witness',eventType:'marriage'}).map(r=>r.object_id),['W-marriage']);
  assert.equal(db.prepare('SELECT count(*) n FROM relation').get().n,0);
});

test('deltagare, händelse och råomnämnande behåller var sin fulla bedömning',t=>{
  const db=fixture(t),hits=findParticipations(db,{role:'witness',eventType:'baptism'});
  for(const row of hits) {
    const {storedRole,canonicalRole,knownRole,event,mention,...participation}=row;
    assert.deepEqual(participation,readCurrent(db,row.object_id));
    assert.deepEqual(event,readCurrent(db,row.event_id));assert.deepEqual(mention,readCurrent(db,row.mention_id));
    assert(participation.pending_reviews.length);assert(event.pending_reviews.length);assert(mention.pending_reviews.length);
    for(const value of [participation,event,mention]){assert(value.rationale);assert(value.caveat);assert(Array.isArray(value.origins));assert(value.evidence.length);}
    assert.equal(storedRole,participation.role);assert.equal(canonicalRole,'witness');assert(knownRole);
  }
  const candidate=hits.find(r=>r.object_id==='W-candidate');
  assert.equal(candidate.disposition,'candidate');assert.equal(candidate.evidence_status,'LEAD');
  assert.equal(candidate.event.disposition,'accepted');assert.equal(candidate.event.evidence_status,'TRANSCRIBED');
  assert.equal(hits.find(r=>r.object_id==='W-new').disposition,'accepted');
  assert.equal(hits.find(r=>r.object_id==='W-old').mention.role_literal,'dräng i Botsmark, dopvittne');
  assert.equal(hits.find(r=>r.object_id==='W-new').mention.name_literal,'Olof Anderss[on]');
  assert.equal(hits.find(r=>r.object_id==='W-new').mention.role_literal,'');
});

test('personfilter betyder uttrycklig deltagarperson; ett namn eller en identitetslänk fyller inte luckan',t=>{
  const db=fixture(t);
  const hits=findParticipations(db,{role:'witness',eventType:'baptism',personId:'P-witness'});
  assert.deepEqual(hits.map(r=>r.object_id),['W-new']);
  assert.equal(findParticipations(db,{role:'witness',eventType:'baptism',personId:'P-child'}).length,0);
  assert.equal(findParticipations(db,{personId:'P-missing'}).length,0);
  assert.equal(findParticipations(db,{role:'witness',eventType:'baptism'}).find(r=>r.object_id==='W-old').person_id,null);
});

test('tomma filter betyder alla aktuella deltaganden; okända värden förblir sökbara',t=>{
  const db=fixture(t),all=findParticipations(db);
  for(const filters of [{},null,{role:'',eventType:'  ',personId:null},{role:null,eventType:null,personId:''}])assert.deepEqual(findParticipations(db,filters),all);
  assert.equal(all.length,12);
  const unknown=findParticipations(db,{role:'unreviewed_role'});
  assert.equal(unknown.length,1);assert.equal(unknown[0].canonicalRole,'unreviewed_role');assert.equal(unknown[0].knownRole,false);
  const misplaced=all.find(r=>r.object_id==='W-misplaced');assert.equal(misplaced.knownRole,false);assert.equal(misplaced.canonicalRole,'baptism_witness');
  assert.deepEqual(findParticipations(db,{role:"witness' OR 1=1 --"}),[]);
  assert.deepEqual(findParticipations(db,{eventType:"baptism' OR 1=1 --"}),[]);
  assert.deepEqual(findParticipations(db,{personId:"P-witness' OR 1=1 --"}),[]);
  assert.throws(()=>findParticipations(db,{role:[]}),TypeError);assert.throws(()=>findParticipations(db,[]),TypeError);
});

test('frågevyn är läsande och döljer inga äldre revisioner genom omskrivning',t=>{
  const db=fixture(t),snapshot=()=>JSON.stringify({
    revisions:db.prepare('SELECT * FROM revision ORDER BY id').all(),
    roles:db.prepare('SELECT * FROM participation ORDER BY revision_id').all(),
    mentions:db.prepare('SELECT * FROM mention ORDER BY revision_id').all(),
    writes:db.prepare('SELECT total_changes() n').get().n,
  }),before=snapshot();
  findParticipations(db);findParticipations(db,{role:'witness',eventType:'baptism'});
  assert.equal(snapshot(),before);
  assert.equal(db.prepare("SELECT role FROM participation WHERE revision_id='P-history@1'").get().role,'baptism_witness');
  assert.equal(findParticipations(db,{role:'officiant'})[0].revision_id,'P-history@2');
});

test('frågeutfall återbrukar domänens kodning och behåller de verkliga okodade råorden',()=>{
  assert.equal(canonicalQuestionOutcome,researchOutcome);
  const actual=['AVVISAD','FASTSTÄLLD','FASTSTÄLLD.','OLÖST INOM PRÖVAT OMFÅNG','OLÖST INOM PRÖVAT OMFÅNG.','OMSTRIDD','OMSTRIDD.','OPEN','STÖDD','STÖDD.','negative','open','ÖPPEN','ÖPPEN.'];
  for(const raw of actual){const q=questionOutcomeView({outcome:raw,disposition:'recorded'});assert.equal(q.storedOutcome,raw);assert.equal(q.canonicalOutcome,researchOutcome(raw));assert.equal(q.knownOutcome,q.canonicalOutcome!==null);assert(q.active);}
  for(const raw of ['STÖDD','OLÖST INOM PRÖVAT OMFÅNG','open','OPEN','negative','nytt utfall',null,undefined,''])assert.equal(canonicalQuestionOutcome(raw),null);
  assert.equal(canonicalQuestionOutcome(' **ÖPPEN.** '),'open');
  for(const raw of ['ÖPPEN','PÅGÅR','FASTSTÄLLD','AVVISAD','OLÖST','OMSTRIDD','STYRKT','EJ STYRKT','GODKÄND','UNDERKÄND','GENOMGÅNGET','AVGRÄNSAT','INTEGRITETSMINIMERAT'])assert(Object.hasOwn(QUESTION_OUTCOME_VOCABULARY,canonicalQuestionOutcome(raw)));
});

test('en avvecklad öppen fråga förblir inaktiv utan ändrat råutfall eller bedömning',()=>{
  const q={object_id:'Q-old',outcome:'ÖPPEN.',disposition:'retired',rationale:'Avvecklad identitet',caveat:'Historiken skall bevaras',evidence_status:'LEAD',body:'Frågan i den gamla akten',origins:[{unit_id:'legacy'}],pending_reviews:[{id:'request'}]};
  const {storedOutcome,canonicalOutcome,knownOutcome,active,...rest}=questionOutcomeView(q);
  assert.deepEqual(rest,q);assert.equal(storedOutcome,'ÖPPEN.');assert.equal(canonicalOutcome,'open');assert(knownOutcome);assert.equal(active,false);
  assert.equal(questionOutcomeView({...q,outcome:'FASTSTÄLLD',disposition:'recorded'}).active,true);
  assert.equal(questionOutcomeView({...q,outcome:null}).canonicalOutcome,null);
  assert.equal(questionOutcomeView({...q,outcome:null}).active,false);
});
