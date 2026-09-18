import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {openDB,exportData,restore,verifyDB} from '../lib/store.mjs';
import {applyOperation} from '../lib/domain.mjs';
import {canonical,sha} from '../lib/archive.mjs';
import {migrationReport} from '../lib/migration.mjs';
import {contextList,contextDocument} from '../lib/context.mjs';
import {checkT0663Risks} from './T-0663-risk.mjs';

const base=new URL('../',import.meta.url).pathname,read=p=>JSON.parse(fs.readFileSync(p));
const priorPath='/private/tmp/T0663-prior-row-hashes.json';
function preserved(db){
 const prior=read(priorPath),data=exportData(db),counts={};
 for(const [table,hashes]of Object.entries(prior.tables)){
  const after=new Set(data.tables[table].map(row=>sha(canonical(row))));
  for(const hash of hashes)assert(after.has(hash),`Äldre rad ändrad: ${table}/${hash}`);counts[table]=hashes.length;
 }
 return {data,digest:sha(canonical(data)),unchangedRows:counts};
}
function checks(db){
 assert.equal(verifyDB(db).ok,true);const risks=checkT0663Risks(db),report=migrationReport(db);
 const undecided=db.prepare('SELECT count(*) n FROM unit u LEFT JOIN current_unit_decision d ON d.unit_id=u.id WHERE d.id IS NULL').get().n;
 assert.equal(undecided,0);assert.equal(report.summary.documents,3717);assert.equal(report.summary.assets,5067);
 assert(!('mapped_partial' in report.summary.unitStates));assert(!('preserved_context' in report.summary.unitStates));
 const documents=contextList(db,{group:'research-context'});assert.equal(documents.length,51);
 for(const d of documents){const view=contextDocument(db,d.path);assert(view.integrity.sha256_verified);assert.equal(view.classification.semantic_review,'not_asserted');}
 const prior=read(priorPath);
 for(const old of prior.interpretationQuestions){const current=db.prepare('SELECT state,question FROM current_unit_decision WHERE unit_id=?').get(old.unit_id);assert.equal(current.state,'pending_interpretation');assert.equal(current.question,old.question);}
 return {risks,undecided,coverage:report.summary,contextDocuments:documents.length,unchangedInterpretationQuestions:prior.interpretationQuestions.length};
}
if(process.argv[2]==='prepare'){
 const db=openDB(base+'data/research.sqlite',{readOnly:true});try{
  assert.equal(db.prepare("SELECT count(*) n FROM operation WHERE id LIKE 'T-0663/%'").get().n,0);
  const data=exportData(db),prior={digest:sha(canonical(data)),tables:Object.fromEntries(Object.entries(data.tables).map(([t,rows])=>[t,rows.map(r=>sha(canonical(r)))])),interpretationQuestions:db.prepare("SELECT unit_id,question FROM current_unit_decision WHERE state='pending_interpretation' ORDER BY unit_id").all()};
  fs.writeFileSync(priorPath,JSON.stringify(prior)+'\n',{flag:'wx'});console.log({prepared:true,digest:prior.digest,questions:prior.interpretationQuestions.length});
 }finally{db.close();}
}else if(process.argv[2]==='preflight'){
 const {dbPath,dir}=read('/private/tmp/T0663-preflight-path.json'),db=openDB(dbPath);let restored;
 try{
  const operation=read(base+'operations/T-0663-context-accounting-v1.proposal.json');console.log(applyOperation(db,operation));assert.equal(applyOperation(db,operation).unchanged,true);
  const result=checks(db),before=preserved(db);console.log({stage:'Semantik, 0 beslutslösa enheter, oförändrade frågor och samtliga äldre rader PASS',...result});
  const target=path.join(dir,'restored.sqlite');restore(before.data,target);restored=openDB(target,{readOnly:true});
  assert.equal(sha(canonical(exportData(restored))),before.digest);const restoredChecks=checks(restored);
  fs.writeFileSync(base+'verification/T-0663-preflight-result.json',JSON.stringify({ok:true,digest:before.digest,checks:result,restored:restoredChecks,unchangedRows:before.unchangedRows,dbPath},null,2)+'\n');
  console.log({PASS:true,digest:before.digest,dbPath});
 }finally{restored?.close();db.close();}
}else if(process.argv[2]==='verify'){
 const results=[];
 for(const rel of ['data/research.sqlite','verification/T-0644-restored-root/genealogy2/data/research.sqlite']){
  const db=openDB(base+rel,{readOnly:true});try{
   const result=checks(db),before=preserved(db);const journal=db.prepare('SELECT count(*) entries,max(sequence) last FROM operation_payload').get();assert.equal(journal.entries,39);assert.equal(journal.last,39);
   results.push({path:rel,digest:before.digest,...result,journal,unchangedRows:before.unchangedRows});
  }finally{db.close();}
 }
 assert.equal(results[0].digest,results[1].digest);
 const result={ok:true,task:'T-0663',operations:['reviewed-corrections','context-accounting'].map(name=>{const operation=read(base+`operations/T-0663-${name}-v1.json`);return{id:operation.id,hash:sha(canonical(operation)),changes:operation.changes.length,decisions:operation.unitDecisions.length};}),results};
 fs.writeFileSync(base+'verification/T-0663-result.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
}else throw Error('Ange prepare, preflight eller verify');
