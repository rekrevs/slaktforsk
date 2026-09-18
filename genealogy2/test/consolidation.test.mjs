import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,exportData} from '../lib/store.mjs';
import {canonical} from '../lib/archive.mjs';
import {writeOperation,syncJournal,replayJournal} from '../lib/recovery.mjs';
import {applyOperation,readCurrent} from '../lib/domain.mjs';
import {pedigree} from '../lib/pedigree.mjs';

const basis=(object,version=1)=>({object,version,role:'supports'});
const change=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,
  disposition:'recorded',rationale:'Syntetiskt konsolideringsprov för T-0115.',...extra});
const source=(id,version=null)=>change(id,'source',{
  title:id,description:`Syntetisk källbeskrivning version ${(version??0)+1}`
},{expectedVersion:version});
const apply=(db,id,changes,extra={})=>applyOperation(db,{
  id,actor:'test',reason:'Avgränsat regressionsprov för T-0115.',changes,dependencyReviewVersion:2,...extra
});
function fixture(t) {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-consolidation-'));
  const db=openDB(path.join(dir,'test.sqlite'),{create:true});
  t.after(()=>{db.close();fs.rmSync(dir,{recursive:true,force:true});});
  return db;
}
const pending=db=>db.prepare('SELECT * FROM pending_review ORDER BY affected_revision_id').all();
function retain(db,id) {
  const requests=pending(db);
  assert.ok(requests.length,'fixturen måste faktiskt ha väntande granskningar');
  apply(db,id,[],{resolve:requests.map(r=>({request:r.id,
    rationale:`Individuellt syntetiskt retain-beslut för ${r.affected_revision_id}: den nya källbeskrivningen ändrar inte den prövade uppgiften. Äldre versionsbindning bevaras.`}))});
  assert.equal(pending(db).length,0);
  return requests;
}
function fact(id,evidence) {
  return change(id,'fact',{subject_id:'P',property:'residence',value_type:'text',value_json:'Testorten'},
    {disposition:'accepted',evidence:[basis(evidence)]});
}

for(const transitive of [false,true])test(
  `ny källrevision efter retain öppnar ${transitive?'även transitiv':'direkt'} omprövning av äldre versionsbundet underlag`,t=>{
    const db=fixture(t);
    apply(db,'setup',[source('S'),source('U'),
      change('P','person',{display_name:'Testpersonen'},{disposition:'accepted',evidence:[basis('U')]}),
      fact('F','S'),...(transitive?[
        fact('G','F'),
        change('Q','question',{subject_id:'P',title:'Kvarstår vistelsen?',outcome:'ÖPPEN',body:'Separat följdfråga.'},{evidence:[basis('G')]})
      ]:[])]);
    const expected=transitive?['F@1','G@1','Q@1']:['F@1'];
    apply(db,'source-v2',[source('S',1)]);
    assert.deepEqual(pending(db).map(r=>r.affected_revision_id),expected);
    const previous=retain(db,'retain-after-v2');
    assert.equal(readCurrent(db,'F').revision_id,'F@1','retain får inte skriva om slutsatsen');
    assert.deepEqual(readCurrent(db,'F').evidence.map(e=>e.basis_revision_id),['S@1'],
      'ett dokumenterat retain-beslut bevarar det ursprungliga versionsbundna belägget');

    apply(db,'source-v3',[source('S',2)]);
    const current=pending(db);
    assert.deepEqual(current.map(r=>r.affected_revision_id),expected,
      'S@3 måste prövas även när slutsatsen efter retain fortfarande åberopar S@1');
    assert.ok(current.every(r=>r.changed_revision_id==='S@3'&&r.operation_id==='source-v3'));
    assert.ok(current.every(r=>!previous.some(old=>old.id===r.id)),
      'en gammal stängd begäran ersätter inte prövning av den nya revisionen');
    assert.equal(db.prepare('SELECT count(*) n FROM review_resolution').get().n,previous.length,
      'tidigare dokumenterade beslut ska bevaras');
  }
);

test('en orelaterad källrevision öppnar inte redan prövade direkta eller transitiva slutsatser',t=>{
  const db=fixture(t);
  apply(db,'setup',[source('S'),source('U'),source('UNRELATED'),
    change('P','person',{display_name:'Testpersonen'},{disposition:'accepted',evidence:[basis('U')]}),
    fact('F','S'),fact('G','F')]);
  apply(db,'source-v2',[source('S',1)]);
  assert.deepEqual(pending(db).map(r=>r.affected_revision_id),['F@1','G@1']);
  retain(db,'retain-after-v2');
  const before=db.prepare('SELECT count(*) n FROM review_request').get().n;
  apply(db,'unrelated-v2',[source('UNRELATED',1)]);
  assert.equal(pending(db).length,0);
  assert.equal(db.prepare('SELECT count(*) n FROM review_request').get().n,before);
  assert.equal(readCurrent(db,'F').revision_id,'F@1');
  assert.equal(readCurrent(db,'G').revision_id,'G@1');
});

test('typad antavla styrs av relationsbeslut, inte släktord i prosa eller fristående CONFLICT-status',t=>{
  const db=fixture(t);
  const relation=(id,parent,disposition='accepted')=>change(id,'relation',{
    from_person:parent,to_person:'child',relation_type:'parent',nature:'recorded_parent',
    date_json:{precision:'unknown',literal:'Ingen säker relationsdatering.'}
  },{disposition,evidenceStatus:'TRANSCRIBED',evidence:[basis('S')]});
  const good=relation('parent-link','parent');
  apply(db,'setup',[source('S'),
    ...['child','parent','candidate','prose-only'].map(id=>change(id,'person',{display_name:id},
      {disposition:'accepted',evidence:[basis('S')]})),
    good,relation('candidate-link','candidate','candidate')]);
  const shape=()=>{
    const tree=pedigree(db,'child',{mode:'typed'});
    return {paths:tree.paths,edges:tree.edges.map(e=>e.object_id),
      excluded:tree.excluded.map(e=>({id:e.relation.object_id,reasons:e.reasons}))};
  };
  const before=shape();
  assert.deepEqual(before.paths.map(p=>p.person),['child','parent']);
  apply(db,'prose-and-field-conflict',[
    change('N','narrative',{subject_id:'child',title:'Far, mor och släkt',
      markdown:'prose-only är barnets far. candidate är en säker förälder. Dessa avsiktligt missvisande testmeningar får inte skapa en typad kant.'},
      {evidence:[basis('S')]}),
    change('F-conflict','fact',{subject_id:'parent',property:'birth_year',value_type:'structured',
      value_json:{alternatives:[1881,1887],selected:null}},
      {evidenceStatus:'CONFLICT',evidence:[basis('S')],caveat:'Årskonflikt; inget nytt identitets- eller föräldrabeslut.'})
  ]);
  assert.deepEqual(shape(),before,'prosa skapar ingen kant och en separat årskonflikt stoppar inte en accepterad kant');
  apply(db,'relation-annotation',[{...good,expectedVersion:1,evidenceStatus:'CONFLICT',
    rationale:'Samma uttryckliga relationsbeslut; status annoterar en olöst datering.',
    caveat:'Orden far, mor och osäker i förbehållet ersätter inget typat beslut.'}]);
  assert.deepEqual(shape(),before,'evidence_status får inte ensam ersätta disposition eller relationsart');
  assert.equal(readCurrent(db,'parent-link').evidence_status,'CONFLICT','statusen ska bevaras, inte normaliseras bort');
  assert.equal(readCurrent(db,'candidate-link').disposition,'candidate');
  apply(db,'explicit-rejection',[{...good,expectedVersion:2,disposition:'rejected',
    evidenceStatus:'CONFLICT',rationale:'Separat uttryckligt avvisat relationsbeslut i syntetiskt test.'}]);
  assert.deepEqual(pedigree(db,'child',{mode:'typed'}).paths.map(p=>p.person),['child'],
    'en faktisk ändring av det typade beslutet måste däremot stoppa kanten');
});


test('v2 följer en kvarvarande gammal kedja men flaggar inte en frikopplad aktuell revision',t=>{
  const db=fixture(t);
  apply(db,'setup',[source('S'),source('U'),
    change('P','person',{display_name:'Testpersonen'},{disposition:'accepted',evidence:[basis('U')]}),
    fact('F','S'),fact('G','F')]);
  apply(db,'source-v2',[source('S',1)]);
  retain(db,'retain-source-v2');
  apply(db,'detach-F',[{...fact('F','U'),expectedVersion:1}]);
  retain(db,'retain-G-old-F');
  apply(db,'source-v3',[source('S',2)]);
  assert.deepEqual(pending(db).map(r=>r.affected_revision_id),['G@1'],
    'G@1 åberopar fortfarande F@1→S@1; F@2 åberopar bara U@1');
  assert.equal(readCurrent(db,'F').pending_reviews.length,0);
  assert.equal(readCurrent(db,'G').pending_reviews[0].changed_revision_id,'S@3');
});

test('gamla råjournaler behåller v1-resultat; native skrivning och retries bevarar vald policy och hash',async t=>{
  const db=fixture(t),restored=fixture(t);
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-review-policy-'));
  t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const journal=path.join(dir,'journal'),options={root:dir,journal};
  const raw=(id,changes,extra={})=>({id,actor:'test',reason:'Historiskt oversionerat test.',changes,...extra});
  const initial=raw('old-setup',[source('S'),source('U'),
    change('P','person',{display_name:'Testpersonen'},{disposition:'accepted',evidence:[basis('U')]}),
    fact('F','S'),fact('G','F')]);
  applyOperation(db,initial);
  applyOperation(db,raw('old-v2',[source('S',1)]));
  const previous=pending(db);
  assert.deepEqual(previous.map(r=>r.affected_revision_id),['F@1','G@1']);
  applyOperation(db,raw('old-retain',[],{resolve:previous.map(r=>({request:r.id,
    rationale:`Historiskt dokumenterad individuell prövning av ${r.affected_revision_id}.`}))}));
  const oldThird=raw('old-v3',[source('S',2)]);
  applyOperation(db,oldThird);
  assert.equal(pending(db).length,0,'historisk v1-semantik får inte ändras vid replay');
  assert.equal(db.prepare('SELECT count(*) n FROM review_request').get().n,2);
  syncJournal(db,journal);
  const oldSnapshot=canonical(exportData(db));
  assert.equal((await replayJournal(restored,journal,{root:dir})).applied,4);
  assert.equal(canonical(exportData(restored)),oldSnapshot,
    'inklusive requests, resolutions, request_json och operationshashar');
  assert.equal((await writeOperation(db,oldThird,options)).unchanged,true,
    'en oversionerad retry av en gammal operation får inte annoteras retroaktivt');
  assert.equal(canonical(exportData(db)),oldSnapshot);
  await assert.rejects(()=>writeOperation(db,{...oldThird,reason:'Ändrat innehåll'},options),/annat innehåll/);
  const next=raw('new-v4',[source('S',3)]);
  await assert.rejects(()=>writeOperation(db,next,{...options,afterCommit:()=>{throw Error('Syntetiskt journalavbrott');}}),/finns i databasen/);
  assert.equal(Object.hasOwn(next,'dependencyReviewVersion'),false,'skrivvägen ska inte mutera indata');
  const stored=JSON.parse(db.prepare('SELECT request_json FROM operation_payload WHERE operation_id=?').get(next.id).request_json);
  assert.equal(stored.dependencyReviewVersion,2);
  assert.deepEqual(pending(db).map(r=>r.affected_revision_id),['F@1','G@1']);
  assert.ok(pending(db).every(r=>r.changed_revision_id==='S@4'));
  const hash=db.prepare('SELECT request_hash FROM operation WHERE id=?').get(next.id).request_hash;
  assert.equal((await writeOperation(db,next,options)).unchanged,true,
    'oannoterad retry efter commit är samma v2-operation');
  assert.equal((await writeOperation(db,stored,options)).unchanged,true,
    'även den lagrade annoterade operationen kan återanvändas');
  assert.equal(db.prepare('SELECT request_hash FROM operation WHERE id=?').get(next.id).request_hash,hash);
  await assert.rejects(()=>writeOperation(db,{...next,dependencyReviewVersion:1},options),/annat innehåll/);
  await assert.rejects(()=>writeOperation(db,{...next,reason:'Ny motivering'},options),/annat innehåll/);
  assert.equal((await replayJournal(restored,journal,{root:dir})).applied,1);
  assert.equal(canonical(exportData(restored)),canonical(exportData(db)),'blandad v1/v2-journal reproduceras exakt');
  assert.equal((await replayJournal(restored,journal,{root:dir})).applied,0);
});

test('okänd omprövningsversion stoppas före mutation; explicit v1 förblir läsbar',t=>{
  const db=fixture(t);
  const request={id:'versioned',actor:'test',reason:'Versionsvalidering',changes:[source('S')]};
  const before=canonical(exportData(db));
  for(const version of [0,3,'2',null,false]) {
    assert.throws(()=>applyOperation(db,{...request,dependencyReviewVersion:version}),/dependencyReviewVersion/);
    assert.equal(canonical(exportData(db)),before);
  }
  applyOperation(db,{...request,dependencyReviewVersion:1});
  assert.equal(JSON.parse(db.prepare('SELECT request_json FROM operation_payload WHERE operation_id=?').get(request.id).request_json).dependencyReviewVersion,1);
});
