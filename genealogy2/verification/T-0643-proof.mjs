import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {openDB,exportData,verifyDB} from '../lib/store.mjs';
import {canonical,sha,verifySource} from '../lib/archive.mjs';
import {personView,readCurrent,domainStatus} from '../lib/domain.mjs';
import {renderPerson} from '../lib/render.mjs';
import {renderPersonOverview} from '../lib/overview.mjs';
import {identityGate} from '../lib/review.mjs';
import {researchInventory} from '../lib/inventory.mjs';
import {pedigree} from '../lib/pedigree.mjs';
import {findParticipations,questionOutcomeView} from '../lib/vocabulary.mjs';
import {contextList,contextDocument} from '../lib/context.mjs';
import {migrationReport} from '../lib/migration.mjs';
import {verifyAssets} from '../lib/recovery.mjs';
import {checkT0663Risks} from './T-0663-risk.mjs';

const root=new URL('../../',import.meta.url).pathname;
const main=path.join(root,'genealogy2/data/research.sqlite');
const output=path.join(root,'genealogy2/verification/T-0643');
fs.mkdirSync(output,{recursive:true});
const save=(name,value)=>fs.writeFileSync(path.join(output,name),typeof value==='string'?value:JSON.stringify(value,null,2)+'\n');
const cli=(...args)=>execFileSync(process.execPath,[path.join(root,'genealogy2/cli.mjs'),...args],{cwd:root,encoding:'utf8',maxBuffer:128*1024*1024});
const people=['P-0059','P-0412','P-0424','P-0434'];

function functional(db){
 const coverage=migrationReport(db).summary;
 assert.equal(coverage.documents,3717);assert.equal(coverage.assets,5067);
 assert.equal(coverage.units,97854);assert.equal(coverage.domainObjects,43366);
 assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
 assert.equal(db.prepare('SELECT count(*) n FROM operation_payload').get().n,39);
 assert.equal(db.prepare('SELECT count(*) n FROM unit u LEFT JOIN current_unit_decision d ON d.unit_id=u.id WHERE d.id IS NULL').get().n,0);
 const inventory=researchInventory(db);
 assert.equal(inventory.all.persons,536);assert.equal(inventory.active.persons,511);
 assert.equal(inventory.active.identityPassed,199);assert.equal(inventory.active.identityGatePassed,51);
 assert.equal(inventory.active.legacyContractPassed,5);assert.equal(inventory.active.explicitNativeLifePassed,0);
 const gates=Object.fromEntries(['P-0004','P-0269','P-0453',...Array.from({length:8},(_,i)=>`P-0${481+i}`)].map(id=>{
  const gate=identityGate(db,id);
  return [id,{passed:gate.passed,identity:gate.identity_review.outcome,tree:gate.tree_effect.outcome,life:gate.life_picture_review.outcome,reasons:gate.reasons,used:gate.used_revisions}];
 }));
 assert(gates['P-0004'].passed);assert(gates['P-0269'].passed);
 assert.equal(gates['P-0004'].life,'failed');
 for(const [id,g]of Object.entries(gates))if(!['P-0004','P-0269'].includes(id))assert.equal(g.passed,false,id);
 const verified=pedigree(db,'P-0269'),typed=pedigree(db,'P-0269',{mode:'typed'});
 assert.equal(verified.mode,'verified');assert.equal(verified.truncated,false);assert.equal(typed.truncated,false);
 assert(typed.edges.length>verified.edges.length);assert(verified.gates.every(g=>g.passed||verified.excluded.some(e=>e.gate?.person_id===g.person_id)));
 assert(typed.edges.some(e=>e.object_id==='REL-parent-P-0287-P-0239'&&e.nature==='biological_parent'&&e.evidence_status==='OWNER_CONFIRMED'));
 assert(!typed.edges.some(e=>e.nature==='correlated_parent'));
 assert(!verified.paths.some(p=>p.person==='P-0287'));
 const witnesses=findParticipations(db,{role:'witness',eventType:'baptism'});
 assert.equal(witnesses.length,479);assert.equal(witnesses.filter(w=>w.storedRole==='baptism_witness').length,8);
 assert(witnesses.every(w=>w.canonicalRole==='witness'));
 const questions=db.prepare('SELECT object_id FROM current_revision r JOIN question q ON q.revision_id=r.id ORDER BY object_id').all().map(r=>questionOutcomeView(readCurrent(db,r.object_id)));
 assert.equal(questions.length,1306);assert.equal(questions.filter(q=>!q.active).length,76);
 const alias=personView(db,'P-0295'),archived=personView(db,'P-0412');
 assert.equal(alias.person,null);assert.equal(archived.person,null);
 assert(alias.identityMappings.some(m=>m.target_id==='P-0027'));
 assert(archived.identityMappings.some(m=>m.target_id==='P-0453'));
 const contexts=contextList(db,{group:'research-context'});assert.equal(contexts.length,51);
 for(const c of contexts)assert(contextDocument(db,c.path).integrity.sha256_verified);
 const views=people.map(id=>{
  const view=personView(db,id),full=renderPerson(view),short=renderPersonOverview(view,{gate:identityGate(db,id)});
  assert(short.length<full.length/6,`${id}: översikten är fortfarande för lång`);
  return {id,jsonHash:sha(canonical(view)),shortHash:sha(short),fullHash:sha(full),shortChars:short.length,fullChars:full.length,shortLines:short.split('\n').length,fullLines:full.split('\n').length};
 });
 return {coverage,inventory:{active:inventory.active,all:inventory.all},gates,
  pedigree:{verified:{paths:verified.paths.length,edges:verified.edges.length,stops:verified.excluded.length,hash:sha(canonical(verified))},typed:{paths:typed.paths.length,edges:typed.edges.length,hash:sha(canonical(typed))}},
  witnesses:{total:witnesses.length,legacySpelling:8,hash:sha(canonical(witnesses))},questions:{total:questions.length,retired:76,knownOutcomes:questions.filter(q=>q.knownOutcome).length,hash:sha(canonical(questions))},
  contextDocuments:contexts.length,views,risks:checkT0663Risks(db),domain:domainStatus(db)};
}

if(process.argv[2]==='usability'){
 const db=openDB(main,{readOnly:true});try{
  const result=functional(db),probes=[];
  for(const id of people){
   const short=cli('person',id),full=cli('person',id,'--full','--format','markdown'),json=JSON.parse(cli('person',id,'--format','json'));
   const view=personView(db,id);
   assert.equal(short,renderPersonOverview(view,{gate:identityGate(db,id)})+'\n');
   assert.equal(full,renderPerson(view)+'\n');assert.equal(canonical(json),canonical(view));
   save(id+'-overview.md',short);probes.push({person:id,short:sha(short),full:sha(full),json:sha(canonical(json))});
  }
  const inv=JSON.parse(cli('inventory'));assert.deepEqual(inv.active,result.inventory.active);
  const ped=JSON.parse(cli('pedigree','P-0269'));assert.equal(sha(canonical(ped)),result.pedigree.verified.hash);
  const ws=JSON.parse(cli('participations','--role','witness','--event','baptism'));assert.equal(ws.length,479);
  const ctx=JSON.parse(cli('context','--group','research-context'));assert.equal(ctx.length,51);
  const final={ok:true,task:'T-0643',...result,cliProbes:probes};
  save('usability-result.json',final);console.log(JSON.stringify(final,null,2));
 }finally{db.close();}
}else if(process.argv[2]==='restored'){
 const restoredRoot=path.join(root,'genealogy2/verification/T-0643-restored-root');
 const databases=[{file:main,root},{file:path.join(restoredRoot,'genealogy2/data/research.sqlite'),root:restoredRoot}];
 const results=[];
 for(const entry of databases){
  const db=openDB(entry.file,{readOnly:true});try{
   const integrity=verifyDB(db);assert.equal(integrity.ok,true);
   const assets=await verifyAssets(db,entry.root);assert.equal(assets.ok,true);
   const source=await verifySource(entry.root,path.join(entry.root,'genealogy2/import/baseline'));assert.equal(source.ok,true);
   const functionalResult=functional(db);
   results.push({file:path.relative(root,entry.file),digest:sha(canonical(exportData(db))),integrity,assets,source,functional:functionalResult});
   console.log({verified:entry.file,digest:results.at(-1).digest});
  }finally{db.close();}
 }
 assert.equal(results[0].digest,results[1].digest);assert.equal(canonical(results[0].functional),canonical(results[1].functional));
 const final={ok:true,task:'T-0643',results};
 save('restored-result.json',final);fs.writeFileSync(path.join(root,'genealogy2/verification/T-0643-result.json'),JSON.stringify(final,null,2)+'\n');
 console.log({ok:true,digest:results[0].digest});
}else throw Error('Ange usability eller restored');
