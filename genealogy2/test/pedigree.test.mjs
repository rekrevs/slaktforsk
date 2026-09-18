import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB} from '../lib/store.mjs';
import {applyOperation,readCurrent} from '../lib/domain.mjs';
import {pedigree} from '../lib/pedigree.mjs';
const basis=object=>({object,version:1,role:'supports'});
const c=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,disposition:'accepted',rationale:'Syntetiskt antavleprov',evidence:[basis('S')],...extra});
const parent=(id,from,to,extra={})=>c(id,'relation',{from_person:from,to_person:to,relation_type:'parent',nature:'recorded_parent',date_json:{precision:'unknown',literal:'okänt'}},extra);
test('antavlefrågan skiljer säkra länkar, osäker/avvisad identitet, roller, riktning, cykler och väntande prövningar',t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-pedigree-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  applyOperation(db,{id:'tree',actor:'test',reason:'Test',changes:[
    c('S','source',{title:'Syntetisk källa',description:''},{evidence:[]}),
    c('R','record',{source_id:'S',record_type:'test',locator:'1',dependence_note:''}),
    ...['child','parent','grandparent','uncertain','rejected','badIdentity','witness','retired'].map(id=>c(id,'person',{display_name:id},{disposition:id==='retired'?'retired':'accepted'})),
    c('M','mention',{record_id:'R',name_literal:'Namn',role_literal:'far'}),
    c('I','identity',{mention_id:'M',person_id:'badIdentity',decision:'rejected'},{disposition:'rejected'}),
    parent('good','parent','child'),parent('grand','grandparent','parent'),
    parent('candidate','uncertain','child',{disposition:'candidate'}),parent('no','rejected','child',{disposition:'rejected'}),
    parent('unjustified','badIdentity','child',{evidence:[basis('I')]}),parent('inactive','retired','child'),
    c('E','event',{event_type:'baptism',date_json:{precision:'unknown',literal:'?'},place_role:''}),
    c('witness-role','participation',{event_id:'E',person_id:'witness',role:'witness'}),
    parent('cycle','child','grandparent')]});
  const tree=pedigree(db,'child',{mode:'typed'});
  assert.deepEqual(tree.paths.map(x=>x.person),['child','parent','grandparent']);
  assert.equal(tree.excluded.length,5);
  assert.ok(tree.excluded.some(x=>x.reasons.some(r=>r.includes('Åberopad identitet I@1'))));
  assert.ok(tree.excluded.some(x=>x.reasons.includes('Cykel i föräldralänkarna')));
  assert.ok(!tree.edges.some(x=>x.from_person==='witness'));
  assert.equal(pedigree(db,'child',{mode:'typed',maxDepth:1}).truncated,true);
  assert.equal(pedigree(db,'child',{mode:'typed',maxPaths:1}).truncated,true);
  applyOperation(db,{id:'correct-source',actor:'test',reason:'Rättelse',changes:[c('S','source',{title:'Ny källa',description:''},{evidence:[],expectedVersion:1})]});
  const pending=pedigree(db,'child',{mode:'typed'});assert.equal(pending.paths.length,1);assert.match(pending.excluded[0].reasons.join(','),/Omprövning/);
});

function treeFixture(t,people,changes=[]) {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-verified-pedigree-'));
  t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  applyOperation(db,{id:'fixture',actor:'test',reason:'Verifierad antavla.',changes:[
    c('S','source',{title:'Bevarat syntetiskt underlag',description:'Avgränsat underlag för fixture.'},{evidence:[]}),
    ...people.map(id=>c(id,'person',{display_name:id,legacy_state:'active'})),...changes]});
  return db;
}
function reviews(id,{identity='passed',tree='supporting',life='failed',legacy=false}={}) {
  if(legacy)return [c('ASSESSMENT-'+id,'assessment',{subject_id:id,criteria:'legacy_review_header',outcome:'UNDERKÄND',
    body:`# Forskningsprofil\n\n- Person: ${id}\n- Identitetsläge: PRÖVAT\n- Identitetsgranskning: GODKÄND\n- Trädverkan: BÄRANDE\n- Kontraktsgranskning: UNDERKÄND\n\nAvgränsad livsbild och fullständigt bevarat argument.`},{disposition:'recorded',caveat:'Livsbilden är uttryckligen ofullständig.'})];
  return [['identity_review',identity],['tree_effect',tree],['life_picture_review',life]].map(([criterion,outcome])=>
    c(id+'-'+criterion,'assessment',{subject_id:id,criteria:criterion+'/1',outcome,body:`Individuell prövning av ${id}: ${criterion}. Hela argumentet — även förbehållet — bevaras.`},{disposition:'recorded',caveat:'Kriterierna prövas var för sig.'}));
}

test('verified är standard och passerar rot samt förälder med underkänd livsbild men stoppar båda ofärdiga mor-/farföräldrarna',t=>{
  const db=treeFixture(t,['root','parent','grand-identity','grand-tree'],[
    ...reviews('root'),...reviews('parent',{legacy:true}),
    ...reviews('grand-identity',{identity:'failed'}),...reviews('grand-tree',{tree:'waiting'}),
    parent('01-parent','parent','root'),parent('02-grand','grand-identity','parent'),parent('03-grand','grand-tree','parent')]);
  const before=db.prepare('SELECT count(*) n FROM revision').get().n;
  db.exec('PRAGMA query_only=ON');
  const tree=pedigree(db,'root');
  assert.equal(tree.mode,'verified');
  assert.match(tree.rules,/godkänd identitetsgranskning och bärande trädverkan/);
  assert.deepEqual(tree.paths.map(p=>p.person),['root','parent']);
  assert.equal(tree.excluded.length,2);
  assert.equal(tree.root_gate.passed,true);
  assert.equal(tree.gates.find(g=>g.person_id==='parent').life_picture_review.outcome,'failed');
  const grand=tree.excluded.find(e=>e.relation.from_person==='grand-identity');
  assert.equal(grand.gate.passed,false);
  assert(grand.gate.reasons.some(r=>r.axis==='identity_review'));
  assert.deepEqual(grand.gate.identity_review.assessments[0],readCurrent(db,'grand-identity-identity_review'));
  assert(grand.gate.used_revisions.some(r=>r.revision_id==='grand-identity-identity_review@1'));
  assert.equal(grand.gate.identity_review.assessments[0].evidence[0].basis_revision_id,'S@1');
  const waiting=tree.excluded.find(e=>e.relation.from_person==='grand-tree');
  assert(waiting.gate.reasons.some(r=>r.axis==='tree_effect'));
  assert.equal(db.prepare('SELECT count(*) n FROM revision').get().n,before);
  const typed=pedigree(db,'root',{mode:'typed'});
  assert.deepEqual(typed.paths.map(p=>p.person),['root','parent','grand-identity','grand-tree']);
  assert.equal(typed.root_gate,null);assert.deepEqual(typed.gates,[]);
  assert.match(typed.rules,/grind prövas inte/);
});

test('saknad eller underkänd rotgranskning stoppar passage trots accepterad person och säkra typade länkar',t=>{
  const db=treeFixture(t,['root','parent'],[...reviews('parent'),parent('link','parent','root')]);
  let tree=pedigree(db,'root');
  assert.deepEqual(tree.paths,[{person:'root',depth:0,via:[]}]);
  assert.equal(tree.edges.length,0);assert.equal(tree.excluded[0].person,'root');
  assert(tree.excluded[0].gate.reasons.some(r=>r.code==='assessment_missing'));
  assert.equal(tree.gates.length,1,'föräldern traverseras inte genom en stoppad rot');
  assert.deepEqual(pedigree(db,'root',{mode:'typed'}).paths.map(p=>p.person),['root','parent']);
  applyOperation(db,{id:'failed-review',actor:'test',reason:'Uttryckligt granskningsutfall.',changes:reviews('root',{identity:'failed'})});
  tree=pedigree(db,'root');
  assert.equal(tree.root_gate.identity_review.outcome,'failed');
  assert.equal(tree.edges.length,0);
  assert(tree.excluded[0].gate.used_revisions.some(r=>r.revision_id==='root-identity_review@1'));
  assert.throws(()=>pedigree(db,'unknown'),/personidentitet/);
  for(const mode of ['VERIFIED','',null,false,'all'])assert.throws(()=>pedigree(db,'root',{mode}),/verified eller typed/);
});

test('godkända profiler upphäver inte kandidatkanter, fel relationsart, avvisade/ersatta identiteter, väntande omprövning eller cykler',t=>{
  const people=['root','good','candidate','wrong-nature','bad-identity','stale-identity','spouse'];
  const wrong=parent('wrong','wrong-nature','root');wrong.data.nature='guardian';
  const spouse=parent('spouse-link','spouse','root');spouse.data.relation_type='spouse';spouse.data.nature='recorded_spouse';
  const db=treeFixture(t,people,[
    ...people.flatMap(id=>reviews(id)),
    c('R','record',{source_id:'S',record_type:'test',locator:'1',dependence_note:''}),
    c('M-bad','mention',{record_id:'R',name_literal:'Den avvisade',role_literal:'far'}),
    c('M-stale','mention',{record_id:'R',name_literal:'Den omprövade',role_literal:'far'}),
    c('I-bad','identity',{mention_id:'M-bad',person_id:'bad-identity',decision:'rejected'},{disposition:'rejected'}),
    c('I-stale','identity',{mention_id:'M-stale',person_id:'stale-identity',decision:'accepted'}),
    parent('good-link','good','root'),parent('candidate-link','candidate','root',{disposition:'candidate'}),wrong,spouse,
    parent('bad-id','bad-identity','root',{evidence:[basis('I-bad')]}),
    parent('stale-id','stale-identity','root',{evidence:[basis('I-stale')]}),parent('cycle','root','good')]);
  applyOperation(db,{id:'revise-identity',actor:'test',reason:'Nytt underlag kräver omprövning av relationen.',changes:[
    c('I-stale','identity',{mention_id:'M-stale',person_id:'stale-identity',decision:'accepted'},{expectedVersion:1,evidence:[basis('M-stale')]})]});
  const tree=pedigree(db,'root');
  assert.deepEqual(tree.paths.map(p=>p.person),['root','good']);
  assert(tree.excluded.every(e=>e.gate.passed),'granskningen är godkänd men kanterna måste ändå prövas');
  const reasons=id=>tree.excluded.find(e=>e.relation.object_id===id).reasons.join('\n');
  assert.match(reasons('candidate-link'),/candidate/);
  assert.match(reasons('wrong'),/guardian/);
  assert.match(reasons('bad-id'),/Åberopad identitet I-bad@1 är rejected/);
  assert.match(reasons('stale-id'),/Omprövning väntar/);
  assert.match(reasons('stale-id'),/I-stale@1 är ersatt/);
  assert.match(reasons('cycle'),/Cykel/);
  assert(!tree.paths.some(p=>p.person==='spouse'));
});

test('en senare underkänd identitetsgranskning stoppar grenen utan revision av person eller föräldralänk',t=>{
  const db=treeFixture(t,['root','parent','grand'],[
    ...['root','parent','grand'].flatMap(id=>reviews(id)),parent('link','parent','root'),parent('grand-link','grand','parent')]);
  assert.equal(pedigree(db,'root').paths.length,3);
  const unchanged=[readCurrent(db,'parent'),readCurrent(db,'link')];
  applyOperation(db,{id:'correct-review',actor:'test',reason:'Identitetsgranskningen rättas.',changes:[
    {...reviews('parent',{identity:'failed'})[0],expectedVersion:1,rationale:'Den tidigare godkända identitetsgranskningen är uttryckligen underkänd.'}]});
  const tree=pedigree(db,'root');
  assert.deepEqual(tree.paths.map(p=>p.person),['root']);
  assert.equal(tree.excluded[0].gate.identity_review.assessments[0].revision_id,'parent-identity_review@2');
  assert.deepEqual([readCurrent(db,'parent'),readCurrent(db,'link')],unchanged);
  assert.equal(pedigree(db,'root',{mode:'typed'}).paths.length,3);
});

test('verified behåller djup- och antalsgränser samt typad frågas gränsvalidering',t=>{
  const db=treeFixture(t,['root','parent','grand'],[
    ...['root','parent','grand'].flatMap(id=>reviews(id)),parent('link','parent','root'),parent('grand-link','grand','parent')]);
  const depth0=pedigree(db,'root',{maxDepth:0});
  assert.equal(depth0.paths.length,1);assert.equal(depth0.truncated,true);assert.equal(depth0.gates.length,1);
  const depth1=pedigree(db,'root',{maxDepth:1});
  assert.deepEqual(depth1.paths.map(p=>p.person),['root','parent']);assert.equal(depth1.truncated,true);
  assert(!depth1.gates.some(g=>g.person_id==='grand'));
  const count=pedigree(db,'root',{maxPaths:1});assert.equal(count.paths.length,1);assert.equal(count.truncated,true);
  assert.equal(pedigree(db,'root',{maxDepth:2,maxPaths:3}).truncated,false);
  for(const options of [{maxDepth:-1},{maxDepth:101},{maxDepth:0.5},{maxPaths:0},{maxPaths:1.5}])assert.throws(()=>pedigree(db,'root',options),/Ogiltig gräns/);
});

test('biological_parent är ett läsalias med bevarad ägarkunskap; correlated_parent och saknad granskning ger ingen passage',t=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'g2-parent-nature-')),db=openDB(path.join(dir,'test.sqlite'),{create:true});
 t.after(()=>{db.close();fs.rmSync(dir,{recursive:true,force:true});});
 applyOperation(db,{id:'nature',actor:'test',reason:'Uttryckligt prövat ordförråd',changes:[
  c('S','source',{title:'Syntetisk ägaruppgift',description:''},{evidence:[]}),
  ...['child','biological-owner','secondary'].map(id=>c(id,'person',{display_name:id})),
  c('owner-parent','relation',{from_person:'biological-owner',to_person:'child',relation_type:'parent',nature:'biological_parent',date_json:{precision:'unknown',literal:'okänt'}},{evidenceStatus:'OWNER_CONFIRMED'}),
  c('secondary-parent','relation',{from_person:'secondary',to_person:'child',relation_type:'parent',nature:'correlated_parent',date_json:{precision:'unknown',literal:'okänt'}},{evidenceStatus:'CORROBORATED',caveat:'Sekundärens grad har en uttrycklig invändning.'})
 ]});
 const typed=pedigree(db,'child',{mode:'typed'});assert.deepEqual(typed.paths.map(p=>p.person),['child','biological-owner']);
 assert.equal(typed.edges[0].nature,'biological_parent');assert.equal(typed.edges[0].evidence_status,'OWNER_CONFIRMED');
 assert(typed.excluded.some(e=>e.reasons.includes('Föräldrarelationens art: correlated_parent')));
 const verified=pedigree(db,'child');assert.equal(verified.paths.length,1);assert.equal(verified.root_gate.passed,false);
 assert.equal(db.prepare("SELECT nature FROM relation WHERE revision_id='owner-parent@1'").get().nature,'biological_parent');
});
