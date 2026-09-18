import fs from 'node:fs';
import assert from 'node:assert/strict';
import {openDB,exportData,verifyDB} from '../lib/store.mjs';
import {canonical,sha} from '../lib/archive.mjs';
import {domainStatus} from '../lib/domain.mjs';
import {checkPersons08Risks} from './persons-08-risk-checks.mjs';
const base=new URL('../',import.meta.url).pathname;
const priorPath='/private/tmp/T0659-prior-row-hashes.json';
const read=p=>JSON.parse(fs.readFileSync(p));
if(process.argv[2]==='prepare'){
 const db=openDB(base+'data/research.sqlite',{readOnly:true});
 try{const data=exportData(db);assert.equal(db.prepare("SELECT count(*) n FROM operation WHERE id='T-0659/persons-08-v1'").get().n,0);assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);const prior={digest:sha(canonical(data)),tables:Object.fromEntries(Object.entries(data.tables).map(([t,rows])=>[t,rows.map(r=>sha(canonical(r)))]))};fs.writeFileSync(priorPath,JSON.stringify(prior)+'\n',{flag:'wx'});console.log({priorDigest:prior.digest,counts:Object.fromEntries(Object.entries(data.tables).map(([t,r])=>[t,r.length]))});}finally{db.close();}
}else if(process.argv[2]==='verify'){
 const prior=read(priorPath),op=read(base+'operations/T-0659-persons-08-v1.json'),reviews=read(base+'migration/persons-08-a.json');
 const paths=['data/research.sqlite','verification/T-0644-restored-root/genealogy2/data/research.sqlite'];
 const results=[];let priorCounts;
 for(const rel of paths){const db=openDB(base+rel,{readOnly:true});try{const data=exportData(db);const verification=verifyDB(db),riskChecks=checkPersons08Risks(db),pending=db.prepare('SELECT count(*) n FROM pending_review').get().n;assert.equal(verification.ok,true);assert.equal(pending,0);if(rel===paths[0]){priorCounts={};for(const[t,hashes]of Object.entries(prior.tables)){const after=new Set(data.tables[t].map(r=>sha(canonical(r))));for(const h of hashes)assert.ok(after.has(h),`Äldre rad ändrad:${t}/${h}`);priorCounts[t]=hashes.length;}}
 const stored=db.prepare('SELECT request_hash FROM operation WHERE id=?').get(op.id);
 assert.equal(stored?.request_hash,sha(canonical(op)));
 const journal=db.prepare('SELECT count(*) entries,max(sequence) last FROM operation_payload').get();
 assert.deepEqual({...journal},{entries:34,last:34});
 // Två pilotbiografier utanför de åtta hela kohorterna är inte fulla konverteringar.
 const convertedDossiers=db.prepare("SELECT count(*) n FROM object WHERE id GLOB 'BIO-P-[0-9][0-9][0-9][0-9]' AND id BETWEEN 'BIO-P-0001' AND 'BIO-P-0400'").get().n;
 assert.equal(convertedDossiers,400);
 results.push({path:rel,digest:sha(canonical(data)),verification,riskChecks,pending,convertedDossiers,journal,domain:domainStatus(db)});}finally{db.close();}}
 assert.equal(results[0].digest,results[1].digest);
 const result={task:'T-0659',people:reviews.length,documents:reviews.flatMap(p=>p.documents).length,assertions:reviews.reduce((n,p)=>n+p.assertions.length,0),relationRows:reviews.reduce((n,p)=>n+p.relations.length,0),operation:{id:op.id,requestHash:sha(canonical(op))},reviewHash:sha(fs.readFileSync(base+'migration/persons-08-a.json')),changes:op.changes.length,spans:op.spans.length,decisions:op.unitDecisions.reduce((a,d)=>(a[d.state]=(a[d.state]??0)+1,a),{}),prior:{digest:prior.digest,unchangedRows:priorCounts},replay:read('/private/tmp/T0659-replay.json'),results,verification:{riskGroups:41,existingModelTests:78,newFullCohortTest:1,legacyTests:67,sourceCheck:read('/private/tmp/T0659-source-check.json'),assetCheck:read('/private/tmp/T0659-asset-check.json'),restoredAssetCheck:read('/private/tmp/T0659-restored-asset-check.json')}};
 fs.writeFileSync(base+'verification/T-0659-result.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({task:result.task,people:result.people,assertions:result.assertions,relationRows:result.relationRows,changes:result.changes,spans:result.spans,decisions:result.decisions,hash:results[0].digest,pending:0},null,2));
}else throw Error('Ange prepare före införsel eller verify efter införsel och återspelning.');
