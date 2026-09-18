import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {openDB,exportData} from '../lib/store.mjs';
import {applyOperation} from '../lib/domain.mjs';
import {canonical,sha} from '../lib/archive.mjs';
import {impact} from '../lib/impact.mjs';

const change=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,disposition:'recorded',rationale:'T-0672 synthetic fixture',...(kind==='source'?{}:{evidence:[{object:'U',version:1,role:'supports'}]}),...extra});
const evidence=(object,version=1,role='supports')=>({object,version,role});
function fixture(t) {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-impact-'));
  const file=path.join(dir,'test.sqlite'),db=openDB(file,{create:true});
  t.after(()=>{db.close();fs.rmSync(dir,{recursive:true,force:true});});
  const doc='genealogy/citations/C-0001-test.md',text='# C-0001\nSyntetisk äldre post.';
  db.prepare('INSERT INTO import_batch VALUES (?,?,?)').run('fixture','{}','test');
  db.prepare('INSERT INTO document VALUES (?,?,?,?,?,?)').run(doc,'fixture',sha(text),Buffer.byteLength(text),text,1);
  db.prepare('INSERT INTO legacy_entity VALUES (?,?,?,?)').run('C-0001','citation',doc,'Test');
  db.prepare('INSERT INTO unit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)').run('u',doc,'paragraph',null,null,'',0,Buffer.byteLength(text),1,2,text,'{}',0);
  const apply=(id,changes,extra={})=>applyOperation(db,{id,actor:'test',reason:'T-0672',changes,dependencyReviewVersion:2,...extra});
  const source=change('S','source',{title:'Source',description:'No borrowed date.'});
  const record=change('R','record',{source_id:'S',record_type:'birth',locator:'row1',dependence_note:''},{evidence:[evidence('S')],origins:[{unit:'u',coverage:'complete',note:'Import reference only.'}]});
  const fact=change('F','fact',{subject_id:'P',property:'birth',value_type:'text',value_json:'1783-10-21'},{evidence:[evidence('R')]});
  apply('setup',[source,change('U','source',{title:'Other',description:''}),
    change('P','person',{display_name:'Lena Jonsdotter'}),record,fact,
    change('G','narrative',{subject_id:'P',title:'Biography',markdown:'Lena Jonsdotter 1783-10-21'},{evidence:[evidence('F')]}),
    change('PROVENANCE','assessment',{subject_id:'P',criteria:'test',outcome:'reserved',body:'No date here.'},{evidence:[],origins:[{unit:'u',coverage:'context',note:'No support relationship.'}]}),
    change('COPY','narrative',{subject_id:'P',title:'Unlinked copy',markdown:'Born 1783-10-21.\nBevarad historik: 1783-10-21 återtaget. C-00010 is a different ID.'}),
    change('OTHER-P','person',{display_name:'Maja Lena Jonsdotter'}),
    change('NAMESAKE','narrative',{subject_id:'OTHER-P',title:'Unrelated namesake',markdown:'Maja Lena Jonsdotter lives elsewhere.'}),
    change('LINK','narrative',{subject_id:'P',title:'Filename only',markdown:'[post](../citations/C-0001-test.md)'}),
    change('LITERAL','narrative',{subject_id:'P',title:'Literal',markdown:'50% _ [.] Åäö'})]);
  db.prepare('INSERT INTO unit_decision VALUES (?,?,?,?,?,?,?,?,?)').run('ud','u',1,'setup','mapped_complete','PROVENANCE','Import conversion, not support.','',null);
  apply('record-v2',[{...record,expectedVersion:1,data:{...record.data,locator:'row1 corrected'}}]);
  apply('detach-F',[{...fact,expectedVersion:1,data:{...fact.data,value_json:'1785-10-31'},evidence:[evidence('U')]}]);
  return {db,file,dir,apply};
}

test('impact traces actual old-version chains while separating detached current objects',t=>{
  const {db}=fixture(t);const r=impact(db,'R');
  const current=r.dependencies.current.map(x=>x.revision_id);
  assert(current.includes('G@1'));assert(!current.includes('F@2'));
  assert(r.dependencies.historical.some(x=>x.revision_id==='F@1'));
  const g=r.dependencies.current.find(x=>x.revision_id==='G@1');
  assert.deepEqual(g.path.map(e=>[e.revision_id,e.basis_revision_id,e.role]),[['F@1','R@1','supports'],['G@1','F@1','supports']]);
  assert.equal(g.distance,2);assert.equal(r.seeds[0].revision_id,'R@2');
  assert(r.review.items.find(x=>x.object_id==='G').pending_requests.length>0);
  assert(r.review.items.every(x=>x.decision===null&&x.rationale===null));
});

test('citation routes bounded records but never converts import origins/targets or text into support',t=>{
  const {db}=fixture(t);const r=impact(db,'C-0001');
  assert.deepEqual(r.seeds.map(x=>x.object_id),['R']);
  assert(r.text_candidates.current.some(x=>x.object_id==='LINK'),'canonical citation filename must be found without label');
  assert(r.provenance.origins.some(x=>x.object_id==='PROVENANCE'));
  const target=r.provenance.targets.find(x=>x.target_id==='PROVENANCE');
  assert.equal(target.version,1);assert.equal(target.kind,'assessment');assert.equal(target.start_line,1);
  assert(!r.dependencies.current.some(x=>x.object_id==='PROVENANCE'));
  assert(!r.text_candidates.current.some(x=>x.object_id==='COPY'),'C-00010 is not C-0001');
  assert(r.review.items.find(x=>x.object_id==='PROVENANCE').reasons.includes('import_target_not_evidence'));
});

test('literal date search finds unlinked copies and keeps superseded revisions separate',t=>{
  const {db}=fixture(t);const r=impact(db,'C-0001',{query:'1783-10-21'});
  const copy=r.text_candidates.current.find(x=>x.object_id==='COPY');
  assert.equal(copy.classification,'possible_current_text_copy');assert.equal(copy.registered_dependency,false);
  const h=copy.hits.find(x=>x.field==='markdown'&&x.term==='1783-10-21');
  assert.equal(h.occurrences,2);assert.equal(h.line,1);assert.equal(h.offset,5);
  assert.match(copy.limit,/retraction/,'history inside latest text must not be claimed current truth');
  assert(r.text_candidates.historical.some(x=>x.revision_id==='F@1'&&x.classification==='historical_text_only'));
  assert(!r.text_candidates.current.some(x=>x.revision_id==='F@1'));
  assert(!r.review.items.some(x=>x.revision_id==='F@1'));
});

test('namesake, case sensitivity and SQL/regex characters never imply identity or evidence',t=>{
  const {db}=fixture(t);let r=impact(db,'R',{query:'Lena Jonsdotter'});
  const name=r.text_candidates.current.find(x=>x.object_id==='NAMESAKE');
  assert.equal(name.registered_dependency,false);assert.equal(name.classification,'possible_current_text_copy');
  assert(!r.dependencies.current.some(x=>x.object_id==='NAMESAKE'));
  for(const query of ['50%','_','[.]','Åäö'])assert(impact(db,'R',{query}).text_candidates.current.some(x=>x.object_id==='LITERAL'));
  r=impact(db,'R',{query:'lena jonsdotter'});assert(!r.text_candidates.current.some(x=>x.object_id==='NAMESAKE'));
  assert.throws(()=>impact(db,'missing'),/saknas/);assert.throws(()=>impact(db,'C-9999'),/saknas/);
  assert.throws(()=>impact(db,'R',{query:''}),/tom/);assert.throws(()=>impact(db),/Ange/);
});

test('read-only CLI and library preserve complete export and do not resolve pending reviews',t=>{
  const {db,file,dir}=fixture(t);const before=canonical(exportData(db));
  const reader=openDB(file,{readOnly:true});
  try {impact(reader,'C-0001',{query:'1783-10-21'});} finally {reader.close();}
  const cli=spawnSync(process.execPath,['genealogy2/cli.mjs','impact','C-0001','--db',file,'--query','1783-10-21'],{encoding:'utf8'});
  assert.equal(cli.status,0,cli.stderr);assert.equal(JSON.parse(cli.stdout).format,'genealogy2-impact/1');
  assert.equal(canonical(exportData(db)),before);assert(!fs.existsSync(path.join(dir,'genealogy2/journal')));
  assert(db.prepare('SELECT count(*) n FROM pending_review').get().n>0);
});
