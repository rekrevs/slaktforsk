import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,exportData} from '../lib/store.mjs';
import {applyOperation,head,personView} from '../lib/domain.mjs';
import {writeOperation,replayJournal} from '../lib/recovery.mjs';
import {canonical} from '../lib/archive.mjs';
import {spawnSync} from 'node:child_process';
const c=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,disposition:'recorded',rationale:'Syntetiskt prov',...extra});
function setup(t){const dir=fs.mkdtempSync(path.join(os.tmpdir(),'search-memory-'));const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>{db.close();fs.rmSync(dir,{recursive:true,force:true});});applyOperation(db,{id:'initial',actor:'test',reason:'Fixture',changes:[c('S','source',{title:'Source',description:''}),c('P','person',{display_name:'Person'},{evidence:[{object:'S',version:1,role:'context'}]}),c('P2','person',{display_name:'Other'},{evidence:[{object:'S',version:1,role:'context'}]}),c('P3','person',{display_name:'Unrelated'},{evidence:[{object:'S',version:1,role:'context'}]}),c('Q','question',{subject_id:'P',title:'Query',outcome:'open',body:'Scope'})]});return {db,options:{root:dir,journal:path.join(dir,'journal')}};}
function request(id='negative'){return {id,actor:'test',reason:'Bounded search fixture',changes:[c('SEARCH','search',{question_id:'Q',source_id:'S',outcome:'negative',body:'No match in these pages only',scope_json:{description:'Index entries within exact pages',query:'Person/name variants',bounds:{pages:'1–3',years:'1900–1901'},search_memory:{format:'search-memory/1',subjects:['P'],performed_at:'2026-10-07T12:00:00+02:00',method:'Read every index entry on declared pages',material:{identifier:'archive/item/1',source_version:1,provider_version:{value:null,unknown_reason:'Provider exposes no edition'},snapshot:{sha256:null,unavailable_reason:'No response copy retained'}},coverage:{completed:true,limitations:'Only exact pages, index omissions possible'},reactivation:['New name key or newly available pages']}}},{evidence:[{object:'S',version:1,role:'context'}]})]};}
test('new native negatives enforce complete scope atomically; known and explicitly unknown material alternatives accepted',async t=>{
 const {db,options}=setup(t),before=canonical(exportData(db));
 const bad=[x=>delete x.data.scope_json.search_memory,x=>x.data.scope_json.bounds={},x=>x.data.scope_json.search_memory.coverage.completed=false,x=>x.data.scope_json.search_memory.subjects=['P2'],x=>x.data.scope_json.search_memory.material.source_version=2,x=>x.evidence=[],x=>x.data.scope_json.search_memory.material.snapshot={sha256:'wrong',reference:'file'},x=>x.data.scope_json.search_memory.performed_at='2026-02-30T12:00:00Z',x=>x.data.scope_json.search_memory.performed_at='2026-10-07T12:00:00',x=>x.data.scope_json.search_memory.material.provider_version={value:null},x=>x.data.scope_json.search_memory.reactivation=[]];
 for(const [i,mutate]of bad.entries()){const r=request('bad'+i);mutate(r.changes[0]);await assert.rejects(()=>writeOperation(db,r,options));assert.equal(canonical(exportData(db)),before);}
 await assert.rejects(()=>writeOperation(db,{...request(),searchMemoryVersion:0},options),/searchMemoryVersion/);
 await writeOperation(db,request(),options);assert.equal(head(db,'SEARCH').version,1);
 const r=request('known');r.changes[0].id='KNOWN';r.changes[0].data.scope_json.search_memory.material.provider_version={value:'edition2'};r.changes[0].data.scope_json.search_memory.material.snapshot={sha256:'a'.repeat(64),reference:'saved-index-response'};await writeOperation(db,r,options);
 const access=request('access');access.changes[0].id='ACCESS';access.changes[0].data.outcome='access_problem';delete access.changes[0].data.scope_json.search_memory;await writeOperation(db,access,options);assert.equal(personView(db,'P').searches.find(s=>s.object_id==='ACCESS').outcome,'access_problem');
});
test('old requests and replay preserve hashes; marked retries survive source revision; new native explicit policy downgrade fails',async t=>{
 const {db,options}=setup(t);const old=request('old');delete old.changes[0].data.scope_json.search_memory;applyOperation(db,old);const hash=db.prepare('SELECT request_hash FROM operation WHERE id=?').get('old').request_hash;await writeOperation(db,old,options);assert.equal(db.prepare('SELECT request_hash FROM operation WHERE id=?').get('old').request_hash,hash);
 const r=request('new');r.changes[0].id='NEW';await writeOperation(db,r,options);const stored=db.prepare('SELECT request_json FROM operation_payload WHERE operation_id=?').get('new').request_json;assert.equal(JSON.parse(stored).searchMemoryVersion,1);
 applyOperation(db,{id:'source-change',actor:'test',reason:'new edition',changes:[c('S','source',{title:'New title',description:''},{expectedVersion:1})]});assert.equal((await writeOperation(db,r,options)).unchanged,true);assert.equal(db.prepare('SELECT request_json FROM operation_payload WHERE operation_id=?').get('new').request_json,stored);
 assert.throws(()=>applyOperation(db,{...request('unknown'),searchMemoryVersion:2}),/searchMemoryVersion/);
 // The journal contains old and marked native operations, plus later source revision.
 const restored=openDB(path.join(options.root,'restored.sqlite'),{create:true});t.after(()=>restored.close());await writeOperation(db,{id:'sync',actor:'test',reason:'sync receipt',changes:[c('Q2','question',{subject_id:'P',title:'second',outcome:'open',body:''})]},options);await replayJournal(restored,options.journal,{root:options.root});assert.equal(canonical(exportData(restored)),canonical(exportData(db)));
});
test('explicit subjects retrieve a receipt even with another question subject and no legacy origins',async t=>{
 const {db,options}=setup(t),r=request();r.changes[0].data.scope_json.search_memory.subjects=['P','P2'];await writeOperation(db,r,options);assert.equal(personView(db,'P2').searches[0].object_id,'SEARCH');assert.equal(personView(db,'P3').searches.length,0);
});

test('actual apply-legacy CLI cannot bypass negative standard; valid memory accepts, old legacy retry and replay retain exact policy/hash',async t=>{
 const {db,options}=setup(t),file=path.join(options.root,'db.sqlite');
 const cli=r=>{const p=path.join(options.root,r.id+'.json');fs.writeFileSync(p,JSON.stringify(r));return spawnSync(process.execPath,['genealogy2/cli.mjs','apply-legacy',p,'--db',file,'--source',options.root,'--journal',options.journal],{encoding:'utf8'});};
 const before=canonical(exportData(db)),bad=request('legacy-bad');delete bad.changes[0].data.scope_json.search_memory;
 assert.equal(cli(bad).status,1);assert.equal(canonical(exportData(db)),before);assert.equal(fs.readdirSync(options.journal).length,0);
 assert.equal(cli({...request('legacy-downgrade'),searchMemoryVersion:0}).status,1);assert.equal(canonical(exportData(db)),before);
 const good=request('legacy-good');assert.equal(cli(good).status,0);const goodReceipt=db.prepare('SELECT * FROM operation_payload WHERE operation_id=?').get(good.id);assert.equal(goodReceipt.policy,'legacy/1');assert.equal(JSON.parse(goodReceipt.request_json).searchMemoryVersion,1);assert.equal(cli(good).status,0);assert.equal(db.prepare('SELECT request_json FROM operation_payload WHERE operation_id=?').get(good.id).request_json,goodReceipt.request_json);
 const old=request('old-legacy');old.changes[0].id='OLD-LEGACY';delete old.changes[0].data.scope_json.search_memory;applyOperation(db,old,{legacy:true});const oldReceipt=db.prepare('SELECT * FROM operation_payload WHERE operation_id=?').get(old.id);assert.equal(cli(old).status,0);assert.deepEqual(db.prepare('SELECT * FROM operation_payload WHERE operation_id=?').get(old.id),oldReceipt);assert.equal(Object.hasOwn(JSON.parse(oldReceipt.request_json),'searchMemoryVersion'),false);
 const restored=openDB(path.join(options.root,'legacy-restored.sqlite'),{create:true});t.after(()=>restored.close());await replayJournal(restored,options.journal,{root:options.root});assert.equal(canonical(exportData(restored)),canonical(exportData(db)));
});
