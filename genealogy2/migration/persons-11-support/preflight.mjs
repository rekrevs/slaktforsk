// Avgränsat prov på separat databaskopia; huvuddatabasen öppnas endast läsande.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
import {backup} from 'node:sqlite';
import {openDB,verifyDB} from '../../lib/store.mjs';
import {buildPersons} from '../../import/persons.mjs';
import {applyOperation} from '../../lib/domain.mjs';
import {canonical,sha} from '../../lib/archive.mjs';
const base=new URL('../../',import.meta.url).pathname;
const selected=process.argv[2]==='all'?undefined:process.argv[2];if(selected&&!['a','b','c','d'].includes(selected))throw Error('Valfri del ska vara a,b,c,d eller all');
const parts=['a','b','c','d'].filter(k=>(!selected||k===selected)&&fs.existsSync(base+`migration/persons-11-${k}.json`));
const reviews=parts.flatMap(k=>JSON.parse(fs.readFileSync(base+`migration/persons-11-${k}.json`))).sort((a,b)=>a.person.localeCompare(b.person));
assert.ok(reviews.length>0);
const cohorts=JSON.parse(fs.readFileSync(base+'migration/cohorts.json'));
const group=cohorts.groups.find(g=>g.id==='persons-11');
group.persons=reviews.map(r=>r.person);group.documents=reviews.flatMap(r=>r.documents.map(d=>d.path));
const source=openDB(process.argv[3]??base+'data/research.sqlite',{readOnly:true});
let db,sourceClosed=false;
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-T0662-preflight-'));
try {
  assert.equal(source.prepare("SELECT count(*) n FROM operation WHERE id='T-0662/persons-11-v1'").get().n,0);
  const op=buildPersons(source,reviews,{group:'persons-11',cohorts});
  console.log({people:reviews.length,changes:op.changes.length,spans:op.spans.length,decisions:op.unitDecisions.length,requestHash:sha(canonical(op)),dir});
  await backup(source,path.join(dir,'db.sqlite'));source.close();sourceClosed=true;
  db=openDB(path.join(dir,'db.sqlite'));
  console.log(applyOperation(db,op));
  assert.equal(applyOperation(db,op).unchanged,true);
  assert.equal(verifyDB(db).ok,true);
  if(reviews.some(r=>r.person==='P-0538')){const {checkPersons11PartDRisks}=await import('../../verification/persons-11-part-d-risk.mjs');console.log(checkPersons11PartDRisks(db));}
  console.log({pending:db.prepare('select count(*) n from pending_review').get().n});
  if(reviews.length===38){
    const {checkPersons11Risks}=await import('../../verification/persons-11-risk-checks.mjs');
    console.log(checkPersons11Risks(db));
    const target=base+'operations/T-0662-persons-11-v1.json';
    if(fs.existsSync(target))assert.equal(canonical(JSON.parse(fs.readFileSync(target))),canonical(op));
    else if(process.env.GENEALOGY_FREEZE_OPERATION==='1')fs.writeFileSync(target,JSON.stringify(op,null,2)+'\n',{flag:'wx'});
  }
  console.log('Förprov PASS; huvuddatabasen oförändrad.');
}finally{db?.close();if(!sourceClosed)source.close();}
