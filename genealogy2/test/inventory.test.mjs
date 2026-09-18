import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB} from '../lib/store.mjs';
import {applyOperation} from '../lib/domain.mjs';
import {researchInventory} from '../lib/inventory.mjs';

test('inventeringen skiljer aktiva akter, oregistrerad granskning, identitetsgrind och livsbild',t=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'g2-inventory-')),db=openDB(path.join(dir,'test.sqlite'),{create:true});
 t.after(()=>{db.close();fs.rmSync(dir,{recursive:true,force:true});});
 const c=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,disposition:'accepted',rationale:'Syntetisk registrerad bedömning',evidence:[{object:'S',version:1,role:'supports'}],...extra});
 applyOperation(db,{id:'seed',actor:'test',reason:'Separata indikatorer',changes:[
  c('S','source',{title:'Syntetisk källa',description:''},{evidence:[]}),
  ...['reviewed','unreviewed','retired'].map(id=>c(id,'person',{display_name:id,legacy_state:id==='retired'?'retired':'active'})),
  ...['reviewed','retired'].flatMap(id=>[
   c(`${id}-identity`,'assessment',{subject_id:id,criteria:'identity_review/1',outcome:'passed',body:'Identitetsnivån är prövad.'}),
   c(`${id}-tree`,'assessment',{subject_id:id,criteria:'tree_effect/1',outcome:'supporting',body:'Uttrycklig bärande bedömning.'}),
   c(`${id}-life`,'assessment',{subject_id:id,criteria:'life_picture_review/1',outcome:'failed',body:'Livsbild återstår.'})])
 ]});
 const inventory=researchInventory(db);assert.equal(inventory.active.persons,2);assert.equal(inventory.all.persons,3);
 assert.equal(inventory.active.identityPassed,1);assert.equal(inventory.all.identityPassed,2);
 assert.equal(inventory.active.identityGatePassed,1);assert.equal(inventory.all.identityGatePassed,1);
 assert.equal(inventory.active.explicitNativeLifePassed,0);assert.equal(inventory.active.legacyContractPassed,0);
 assert.equal(inventory.people.find(p=>p.id==='unreviewed').identityReview.outcome,null);
 assert.equal(inventory.people.find(p=>p.id==='unreviewed').identityGate,false);
 assert.equal(inventory.people.find(p=>p.id==='reviewed').lifePictureReview.outcome,'failed');
 assert.equal(inventory.people.find(p=>p.id==='reviewed').identityGate,true);
});
