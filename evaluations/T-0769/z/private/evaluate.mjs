import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {openDB,restore,verifyDB,exportData} from '../../../../genealogy2/lib/store.mjs';
import {applyOperation,readCurrent} from '../../../../genealogy2/lib/domain.mjs';
import {canonical} from '../../../../genealogy2/lib/archive.mjs';
import {verifyAssets} from '../../../../genealogy2/lib/recovery.mjs';
const here=path.dirname(new URL(import.meta.url).pathname),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const fixture=read(path.join(here,'fixture.json')),input=read(path.join(here,'../public/input.json')),reference=read(path.join(here,'reference.json'));
const checks=[],check=(name,pass,detail='')=>checks.push({name,pass:Boolean(pass),detail});
let answer,error=null,applied=false;
try{answer=read(process.argv[2]);check('valid_json',true);}catch(e){check('valid_json',false);error=e.message;}
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'T-0769-Z-eval-'));restore(fixture,path.join(dir,'fixture.sqlite'));const db=openDB(path.join(dir,'fixture.sqlite'));
for(const [p,bytes] of Object.entries(read(path.join(here,'media-content.json')))){fs.mkdirSync(path.dirname(path.join(dir,p)),{recursive:true});fs.writeFileSync(path.join(dir,p),bytes);}
const before=Object.fromEntries(['P-A','F-OWNER','S-B'].map(id=>[id,canonical(readCurrent(db,id))]));
if(answer){
check('bounded_four_changes',Array.isArray(answer.changes)&&canonical(answer.changes.map(c=>c.id).sort())===canonical(['F-B','O-B','R-B','S-A']));
check('policy_and_task_trace',answer.dependencyReviewVersion===2&&/T-0769/.test(answer.reason??'')&&Boolean(answer.actor));
try{applyOperation(db,answer);applied=true;check('real_apply',true);}catch(e){error=e.message;check('real_apply',false,e.message);}
}
if(applied){
check('simple_title',readCurrent(db,'S-A').title==='Provförsamlingen');
check('record_locator',readCurrent(db,'R-B').locator==='folio 20, rad 3, utflyttning nr 17');
const o=readCurrent(db,'O-B'),f=readCurrent(db,'F-B');
for(const v of [o,f])if(typeof v.value_json==='string')v.value_json=JSON.parse(v.value_json);
check('observation_date',o.value_literal==='23/10 1930'&&o.value_json?.value==='1930-10-23');
check('fact_date_and_caveat',f.value_json?.value==='1930-10-23'&&f.value_json?.literal==='23/10 1930'&&f.caveat===input.currentChanges.find(x=>x.id==='F-B').caveat);
check('protected_objects_unchanged',Object.entries(before).every(([id,v])=>canonical(readCurrent(db,id))===v));
check('current_bindings',db.prepare("SELECT basis_revision_id FROM dependency WHERE revision_id='O-B@2'").all().some(x=>x.basis_revision_id==='R-B@3')&&db.prepare("SELECT basis_revision_id FROM dependency WHERE revision_id='F-B@2'").all().some(x=>x.basis_revision_id==='O-B@2'));
check('individual_resolves',answer.resolve?.length===2&&new Set(answer.resolve.map(x=>x.request)).size===2&&answer.resolve.every(r=>r.rationale?.length>=15)&&db.prepare('SELECT count(*) n FROM pending_review').get().n===0);
check('media_preserved_and_added',canonical(db.prepare("SELECT asset_id,region FROM record_media WHERE revision_id='R-B@3' ORDER BY asset_id").all())===canonical([{asset_id:'MED-full',region:'helbild'},{asset_id:'MED-old',region:'utsnitt'}])&&(await verifyAssets(db,dir)).ok);
check('all_other_fields_preserved',reference.changes.every(w=>{const got=answer.changes.find(x=>x.id===w.id);return got&&['kind','expectedVersion','disposition','origins','evidence','evidenceStatus','caveat'].every(k=>canonical(got[k])===canonical(w[k]))&&canonical(got.data)===canonical(w.data);}));
check('database_valid',verifyDB(db).ok);
check('history_preserved',fixture.tables.revision.every(r=>canonical(db.prepare('SELECT * FROM revision WHERE id=?').get(r.id))===canonical(r))&&fixture.tables.observation.every(o=>canonical(db.prepare('SELECT * FROM observation WHERE revision_id=?').get(o.revision_id))===canonical(o)));
}
const names=['valid_json','bounded_four_changes','policy_and_task_trace','real_apply','simple_title','record_locator','observation_date','fact_date_and_caveat','protected_objects_unchanged','current_bindings','individual_resolves','media_preserved_and_added','all_other_fields_preserved','database_valid','history_preserved'];
for(const n of names)if(!checks.some(c=>c.name===n))check(n,false,'Inte uppnått eftersom föregående införsel/parsing misslyckades.');
const result={format:'T-0769-Z-score/1',passed:checks.every(c=>c.pass),score:checks.filter(c=>c.pass).length,maxScore:names.length,applied,error,checks,limitations:['Automatisk kontroll bedömer att motiveringar finns, men inte deras fulla sakliga kvalitet.','Syntetiskt fryst material; detta prövar implementation av fastställt beslut, inte egen forskning.']};
db.close();fs.rmSync(dir,{recursive:true,force:true});console.log(JSON.stringify(result,null,2));
