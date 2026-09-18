import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {DatabaseSync} from 'node:sqlite';
import {applyOperation,head,readCurrent} from '../lib/domain.mjs';
import {identityGate,REVIEW_CRITERIA} from '../lib/review.mjs';

const P='P-0001',H='ASSESSMENT-'+P;
function legacy({identity='GODKÄND',tree='BÄRANDE',life='UNDERKÄND',state='PRÖVAT',extra=''}={}) {
  return `# Forskningsprofil för ${P}\r\n\r\n- Kontrakt: \`person-research/v1\`\r\n- Person: ${P}\r\n- Identitetsläge: \`${state}\`\r\n- Livsbildsläge: \`EJ BEDÖMT\`\r\n- Identitetsgranskning: \`${identity}\`\r\n- Trädverkan: \`${tree}\`\r\n- Kontraktsgranskning: \`${life}\`\r\n${extra}\r\nHela argumentet — även osäkerheten — bevaras.\r\n`;
}
function fixture(t,{disposition='accepted',evidenceStatus=null}={}) {
  const db=new DatabaseSync(':memory:');
  db.exec('PRAGMA foreign_keys=ON');
  for(let i=1;i<=6;i++)db.exec(fs.readFileSync(new URL(`../schema/${String(i).padStart(3,'0')}.sql`,import.meta.url),'utf8'));
  db.prepare('INSERT INTO import_batch VALUES (?,?,?)').run('test','{}','test');
  const raw='Belägg.\n',bytes=Buffer.byteLength(raw);
  db.prepare('INSERT INTO document VALUES (?,?,?,?,?,?)').run('test.md','test','fixture',bytes,raw,1);
  db.prepare('INSERT INTO unit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)').run('unit','test.md','prose',null,P,'',0,bytes,1,1,raw,'{}',0);
  let serial=0;
  const operation=request=>applyOperation(db,{id:'op-'+(++serial),actor:'test',reason:'Avgränsat test.',changes:[],...request});
  const change=(id,kind,data,options={})=>operation({changes:[{id,kind,data,expectedVersion:head(db,id)?.version??null,disposition:'recorded',rationale:'Hela individuella motiveringen.',caveat:'Avgränsat förbehåll.',origins:[{unit:'unit',coverage:'complete',note:'Exakt bevarad proveniens.'}],...options}]});
  const assessment=(id,criteria,outcome,body='',options={})=>change(id,'assessment',{subject_id:P,criteria,outcome,body},options);
  const source=()=>change('S','source',{title:'Ett underlag',archive_reference:null,source_class:'test',description:'Underlagets version.'});
  const header=(body=legacy(),options={})=>assessment(H,'legacy_review_header','GODKÄND',body,options);
  change(P,'person',{display_name:'Testpersonen',sex:null,legacy_state:'active'},{disposition,evidenceStatus});
  t.after(()=>db.close());
  return {db,change,assessment,header,source,operation};
}
const codes=gate=>gate.reasons.map(r=>r.code);

test('accepterad och ägarbekräftad person saknar grind utan uttryckliga bedömningar',t=>{
  const {db}=fixture(t,{evidenceStatus:'OWNER_CONFIRMED'});
  const before=readCurrent(db,P);
  db.exec('PRAGMA query_only=ON');
  const gate=identityGate(db,P);
  assert.equal(gate.passed,false);
  assert.equal(gate.identity_review.source,'missing');
  assert.deepEqual(codes(gate),['assessment_missing','assessment_missing']);
  assert.deepEqual(readCurrent(db,P),before);
  assert.equal(gate.person.evidence_status,'OWNER_CONFIRMED');
  assert.equal(identityGate(db,'P-9999').status,'blocked');
  assert(codes(identityGate(db,'P-9999')).includes('person_missing'));
  assert.throws(()=>identityGate(db,''),/Person-id/);
});

test('exakta äldre rubrikrader passerar identitetsnivån trots livsbild UNDERKÄND och sammanblandat outcome',t=>{
  const {db,assessment}=fixture(t);
  const body=legacy();
  assessment(H,'Befintlig person-research/v1; ursprungliga datum och kriterier i body','UNDERKÄND',body);
  const gate=identityGate(db,P);
  assert.equal(gate.passed,true);
  assert.equal(gate.identity_review.outcome,'passed');
  assert.equal(gate.tree_effect.outcome,'supporting');
  assert.equal(gate.life_picture_review.outcome,'failed');
  assert.equal(gate.life_picture_review.scope,'legacy_full_contract');
  assert.equal(gate.identity_review.assessments[0].body,body);
  assert.deepEqual(gate.identity_review.assessments[0],readCurrent(db,H));
  assert.deepEqual(gate.used_revisions,[{object_id:P,revision_id:P+'@1',version:1,roles:['person']},{object_id:H,revision_id:H+'@1',version:1,roles:['identity_review','tree_effect','life_picture_review']}]);
  assert.equal(gate.identity_review.fields[0].raw,'`GODKÄND`');
  assert.equal(gate.identity_review.fields[0].line,7);
});

test('accepterad enpostidentitet med UNDERKÄND och EJ BÄRANDE stoppas oberoende av positivt aggregate outcome',t=>{
  const {db,header}=fixture(t,{evidenceStatus:'TRANSCRIBED'});
  header(legacy({identity:'UNDERKÄND',tree:'EJ BÄRANDE'}));
  const gate=identityGate(db,P);
  assert.equal(gate.passed,false);
  assert.equal(gate.person.disposition,'accepted');
  assert.deepEqual(gate.reasons.map(r=>r.axis),['identity_review','tree_effect']);
  assert.equal(gate.identity_review.outcome,'failed');
});

test('KLAR, citat, kodexempel och senare avsnitt blir inte aktuella granskningsrader',t=>{
  const {db,header}=fixture(t);
  header('# Profil KLAR / GRANSKAD\n\n> - Identitetsgranskning: GODKÄND\n\n```md\n- Identitetsgranskning: GODKÄND\n- Trädverkan: BÄRANDE\n```\n\n## Äldre granskning\n- Identitetsgranskning: GODKÄND\n- Trädverkan: BÄRANDE\n');
  const gate=identityGate(db,P);
  assert.equal(gate.passed,false);
  assert.deepEqual(codes(gate),['header_missing','header_missing']);
});

test('dubbla, kvalificerade och motsägande rubrikvärden stoppas utan gissning',t=>{
  const {db,header}=fixture(t);
  header(legacy({extra:'- Identitetsgranskning: UNDERKÄND'}));
  assert(codes(identityGate(db,P)).includes('header_conflict'));
  header(legacy({identity:'GODKÄND (äldre; rättad)'}));
  assert(codes(identityGate(db,P)).includes('header_outcome_invalid'));
  header(legacy({state:'OLÖST'}));
  assert(codes(identityGate(db,P)).includes('header_identity_state_conflict'));
  header(legacy().replace('- Person: P-0001','- Person: P-0002'));
  assert(codes(identityGate(db,P)).includes('header_context_conflict'));
});

test('native kriterier går före äldre import per nivå och bevarar argument, belägg och rättelsekvalifikationer',t=>{
  const {db,header,assessment,source}=fixture(t);
  header(legacy({identity:'UNDERKÄND',tree:'AVVAKTAR',state:'OLÖST'}));
  source();
  assessment('N-ID','identity_review/1','passed','Aktuell identitetsprövning.',{evidence:[{object:'S',version:1,role:'supports',note:'Namngivet underlag.'}]});
  assert.equal(identityGate(db,P).passed,false,'trädverkan har ännu bara AVVAKTAR');
  assessment('N-TREE','tree_effect/1','supporting','Trädverkan prövad separat.');
  assessment('N-LIFE','life_picture_review/1','failed','Livsbilden återstår.');
  assessment('QUALIFICATION','source_path_policy_correction','life_picture_requires_review','Äldre positiva PK08-granskningen är rättad; identiteten består.');
  const gate=identityGate(db,P);
  assert.equal(gate.passed,true);
  assert.equal(gate.identity_review.source,'native');
  assert.equal(gate.tree_effect.source,'native');
  assert.equal(gate.life_picture_review.scope,'life_picture');
  assert.equal(gate.life_picture_review.outcome,'failed');
  assert.equal(gate.identity_review.ignored_assessments[0].revision_id,H+'@1');
  assert.deepEqual(gate.identity_review.assessments[0],readCurrent(db,'N-ID'));
  assert.deepEqual(gate.other_assessments,[readCurrent(db,'QUALIFICATION')]);
  assert.equal(gate.identity_review.assessments[0].evidence[0].basis_revision_id,'S@1');
});

test('konkurrerande nativebedömningar stoppas även med samma utfall; uttrycklig pensionering löser konkurrensen',t=>{
  const {db,header,assessment}=fixture(t);header();
  assessment('N-ID-1','identity_review/1','passed','Första granskningen.');
  assessment('N-ID-2','identity_review/1','passed','Andra granskningen.');
  let gate=identityGate(db,P);
  assert(codes(gate).includes('assessment_conflict'));
  assert.deepEqual(gate.identity_review.assessments.map(a=>a.object_id),['N-ID-1','N-ID-2']);
  assessment('N-ID-2','identity_review/1','failed','Det andra utfallet motsäger också det första.');
  assert(codes(identityGate(db,P)).includes('assessment_conflict'));
  assessment('N-ID-1','identity_review/1','passed','Ersatt av den andra granskningen.',{disposition:'retired'});
  gate=identityGate(db,P);
  assert.equal(gate.identity_review.outcome,'failed');
  assert.equal(gate.identity_review.usable,true);
  assert.equal(gate.passed,false);
  assert(gate.identity_review.ignored_assessments.some(a=>a.revision_id==='N-ID-1@2'));
});

test('rättad, pensionerad, föreslagen eller ogiltig nativebedömning återupplivar inte äldre godkännande',t=>{
  const {db,header,assessment}=fixture(t);header();
  assessment('N-ID','identity_review/1','passed','Godkänt.');
  assert.equal(identityGate(db,P).passed,true);
  assessment('N-ID','identity_review/1','failed','Uttrycklig senare rättelse.');
  assert.equal(identityGate(db,P).identity_review.assessments[0].revision_id,'N-ID@2');
  assert.equal(identityGate(db,P).passed,false);
  assert.equal(db.prepare('SELECT outcome FROM assessment WHERE revision_id=?').get('N-ID@1').outcome,'passed');
  for(const options of [{disposition:'retired'},{disposition:'candidate'},{disposition:'rejected'},{evidenceStatus:'CONFLICT'},{evidenceStatus:'REJECTED'}]) {
    assessment('N-ID','identity_review/1','passed','Behöver uttrycklig aktuell prövning.',options);
    assert.equal(identityGate(db,P).passed,false,JSON.stringify(options));
  }
  assessment('N-ID','identity_review/1','KLAR','Äldre arbetsstatus duger inte.');
  assert(codes(identityGate(db,P)).includes('assessment_outcome_invalid'));
});

test('versionsändrat belägg stoppar pending granskning även om en ny revision återger samma positiva utfall',t=>{
  const {db,header,assessment,source,operation}=fixture(t);header();source();
  assessment('N-ID','identity_review/1','passed','Prövat mot källa 1.',{evidence:[{object:'S',version:1,role:'supports'}]});
  assert.equal(identityGate(db,P).passed,true);
  source();
  let gate=identityGate(db,P);
  assert(codes(gate).includes('assessment_pending'));
  assert(codes(gate).includes('assessment_basis_revised'));
  const pending=readCurrent(db,'N-ID').pending_reviews;
  assessment('N-ID','identity_review/1','passed','Prövat mot källa 2.',{evidence:[{object:'S',version:2,role:'supports'}]});
  gate=identityGate(db,P);
  assert(codes(gate).includes('assessment_pending'),'äldre revisions olösta omprövning försvinner inte av ny revision');
  assert(!codes(gate).includes('assessment_basis_revised'));
  operation({resolve:pending.map(p=>({request:p.id,rationale:'Den ändrade källan har prövats i N-ID@2.'}))});
  assert.equal(identityGate(db,P).passed,true);
});

test('pending livsbildskriterium blockerar inte identitet; pending gemensamt äldre bedömningshuvud måste avgränsas uttryckligt',t=>{
  const {db,header,assessment,source}=fixture(t);header();source();
  assessment('N-LIFE','life_picture_review/1','failed','Ofullständig livsbild.',{evidence:[{object:'S',version:1,role:'supports'}]});
  source();
  let gate=identityGate(db,P);
  assert.equal(gate.passed,true);
  assert(gate.life_picture_review.issues.some(i=>i.code==='assessment_pending'));
  assert.equal(gate.life_picture_review.usable,false);
  header(legacy(),{evidence:[{object:'S',version:2,role:'supports'}]});
  source();
  gate=identityGate(db,P);
  assert.equal(gate.passed,false);
  assert(gate.reasons.some(r=>r.axis==='identity_review'&&r.code==='assessment_pending'));
});

test('saknad eller okänd livsbild sänker inte godkänd identitetsnivå; kandidatperson passerar ändå inte',t=>{
  const {db,header,assessment,change}=fixture(t);
  header(legacy().replace('- Kontraktsgranskning: `UNDERKÄND`\r\n',''));
  assert.equal(identityGate(db,P).passed,true);
  assessment('N-LIFE','life_picture_review/1','UNDEFINED','Inget giltigt livsbildsutfall.');
  assert.equal(identityGate(db,P).passed,true);
  change(P,'person',{display_name:'Testpersonen',sex:null,legacy_state:'active'},{disposition:'candidate'});
  assert(codes(identityGate(db,P)).includes('person_not_accepted'));
  assert.deepEqual(REVIEW_CRITERIA.tree_effect.outcomes,['supporting','waiting','non_supporting']);
});
