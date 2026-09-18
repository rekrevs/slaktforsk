import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,importBaseline,verifyDB,exportData,restore} from '../lib/store.mjs';
import {applyOperation,inspect,readCurrent} from '../lib/domain.mjs';
import {buildEvidence} from '../import/evidence.mjs';
import {snapshot,canonical} from '../lib/archive.mjs';
import {migrationReport} from '../lib/migration.mjs';

test('två citationer återbrukar samma källpost, läsningar hålls skilda och söknoll blir ingen positiv post',async t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-evidence-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  for(const d of ['sources','citations','media'])fs.mkdirSync(path.join(dir,'genealogy',d),{recursive:true});
  fs.writeFileSync(path.join(dir,'genealogy/media/later.bin'),'Syntetiskt bevarat medium');
  fs.writeFileSync(path.join(dir,'genealogy/sources/S-0001.md'),'# S-0001: Syntetisk bok\n\n## Innehåll\n\nTestbok\n');
  for(const [n,text] of [[1,'27/28; ingen läsning väljs.'],[2,'Senare läsning: 28.'],[3,'Ingen person funnen i posterna 51–96.'],[4,'Senare reservation utan ny avskrift.']])fs.writeFileSync(path.join(dir,`genealogy/citations/C-000${n}.md`),`# C-000${n}: Test\n\n## Avskrift\n\n${text}\n`);
  const base=path.join(dir,'baseline');const snapshotResult=await snapshot(dir,base);
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());importBaseline(db,base);
  applyOperation(db,{id:'source',actor:'test',reason:'Syntetiskt',changes:[{id:'S-0001',kind:'source',expectedVersion:null,disposition:'recorded',rationale:'Syntetiskt',data:{title:'Testbok',description:'Testbok'}}]});
  const ids=['C-0001','C-0002','C-0003'],cohorts={baseline:snapshotResult.id,groups:[{id:'evidence-01',citations:ids,sources:['S-0001']}]};
  const reviews=ids.map((id,i)=>{
    const d=db.prepare('SELECT d.* FROM document d JOIN legacy_entity e ON e.document_path=d.path WHERE e.id=?').get(id);
    return {citation:id,path:d.path,sha256:d.sha256,disposition:i===2?'preserved_text':'bounded_records',
      readingNote:i===0?'Äldre alternativ väljs inte bort.':i===1?'Senare rättelse är separat läshistorik.':'Söknoll endast för posterna 51–96.',
      pending:i===2?[{question:'Hur avgränsas datumintervallet för 51–96? Ingen träff utanför omfånget utesluts.',startLine:5,endLine:5}]:[],
      records:i===2?[]:[{key:'S-0001:bok1:sida1:post1',source:'S-0001',type:'birth',locator:'bok1 sida1 post1',dependence:'Två citationer av samma originalpost, inte två oberoende vittnen.',caveat:'Åldern har läshistorik.',evidence:[{startLine:1,endLine:5}],transcriptions:[{startLine:5,endLine:5}]}]};
  });
  assert.throws(()=>buildEvidence(db,reviews.slice(1),{cohorts}),/varje citation/);
  const mismatched=structuredClone(reviews);mismatched[1].records[0].type='unrelated_document_type';
  assert.throws(()=>buildEvidence(db,mismatched,{cohorts}),/Motstridiga avgränsningar/);
  const request=buildEvidence(db,reviews,{cohorts});applyOperation(db,request);
  assert.equal(canonical(buildEvidence(db,reviews,{cohorts})),canonical(request));
  assert.equal(applyOperation(db,request).unchanged,true);
  assert.equal(db.prepare("SELECT count(*) n FROM object WHERE kind='record'").get().n,1);
  assert.equal(db.prepare("SELECT count(*) n FROM object WHERE kind='transcription'").get().n,2);
  assert.equal(db.prepare("SELECT count(*) n FROM object WHERE kind='person'").get().n,0);
  const record=db.prepare("SELECT caveat FROM current_revision WHERE kind='record'").get();
  assert.match(record.caveat,/Äldre alternativ/);assert.match(record.caveat,/Senare rättelse/);
  const report=migrationReport(db);
  assert.ok(report.units.filter(u=>u.path!=='genealogy/citations/C-0004.md').every(u=>u.state!=='pending_interpretation'||u.reason.includes('datumintervallet')));
  assert.ok(inspect(db,'C-0003').conversionDecisions.some(d=>d.state==='pending_interpretation'));
  assert.ok(inspect(db,'C-0001').representations.some(o=>o.kind==='record'));
  const d=db.prepare("SELECT d.* FROM document d JOIN legacy_entity e ON e.document_path=d.path WHERE e.id='C-0004'").get();
  const later={...reviews[0],citation:'C-0004',path:d.path,sha256:d.sha256,readingNote:'Senare reservation utan ny avskrift.',records:[{...reviews[0].records[0],transcriptions:[],assets:[{path:'genealogy/media/later.bin',region:'post1'}]}]};
  assert.throws(()=>buildEvidence(db,[later],{group:'evidence-02',cohorts:{...cohorts,groups:[{id:'evidence-02',citations:['C-0004'],sources:[]}]}}),/Medielänk.*ny version/);
  const conflictingLater=structuredClone(later);conflictingLater.records[0].type='unrelated_document_type';
  assert.throws(()=>buildEvidence(db,[conflictingLater],{group:'evidence-02',cohorts:{...cohorts,groups:[{id:'evidence-02',citations:['C-0004'],sources:[]}]}}),/manuell jämförelse/);
  const before=db.prepare("SELECT * FROM current_revision WHERE kind='record'").get();
  const payload=db.prepare('SELECT * FROM record WHERE revision_id=?').get(before.id);delete payload.revision_id;
  applyOperation(db,{id:'attach-preserved-media',actor:'test',reason:'Bara den saknade bildlänken tillkommer; postens innehåll är oförändrat.',changes:[{
    id:before.object_id,kind:'record',expectedVersion:1,disposition:before.disposition,
    rationale:'Versionsbevarat tillägg av redan arkiverad bildlänk.',caveat:before.caveat,data:payload,
    bindings:{'S-0001':1},origins:db.prepare('SELECT unit_id AS unit,coverage,note FROM origin WHERE revision_id=?').all(before.id),
    assets:later.records[0].assets
  }]});
  assert.equal(db.prepare('SELECT count(*) n FROM record_asset WHERE revision_id=?').get(before.id).n,0);
  assert.equal(readCurrent(db,before.object_id).media[0].path,'genealogy/media/later.bin');
  const pending=db.prepare('SELECT id FROM pending_review').all();assert.equal(pending.length,4);
  applyOperation(db,{id:'review-media-addition',actor:'test',reason:'Alla fyra äldre avskrifter/läsningar jämförda mot oförändrat postinnehåll.',changes:[],
    resolve:pending.map(r=>({request:r.id,rationale:'Endast en mediekoppling tillkom. Källa, postgräns, rådata, förbehåll och de åberopade äldre revisionerna är oförändrade; bedömningen består.'}))});
  const next=buildEvidence(db,[later],{group:'evidence-02',cohorts:{...cohorts,groups:[{id:'evidence-02',citations:['C-0004'],sources:[]}]}});
  assert.ok(next.changes.every(c=>c.kind==='assessment'));
  applyOperation(db,next);
  const shared=inspect(db,'C-0004').representations.filter(o=>o.kind==='record');
  assert.equal(shared.length,1);assert.equal(shared[0].version,2);
  assert.equal(shared[0].media[0].path,'genealogy/media/later.bin');
  assert.equal(shared[0].readings.length,3);
  assert.equal(inspect(db,shared[0].object_id).current.readings.length,3);
  assert.ok(readCurrent(db,shared[0].object_id).readings.some(r=>/Senare reservation/.test(r.body)));
  assert.equal(canonical(buildEvidence(db,[later],{group:'evidence-02',cohorts:{...cohorts,groups:[{id:'evidence-02',citations:['C-0004'],sources:[]}]}})),canonical(next));
  assert.equal(verifyDB(db).ok,true);
  const data=exportData(db);restore(data,path.join(dir,'restored.sqlite'));
  const restored=openDB(path.join(dir,'restored.sqlite'));assert.equal(canonical(exportData(restored)),canonical(data));restored.close();
});
