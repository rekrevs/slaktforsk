import assert from 'node:assert/strict';
import {checkPersons10PartARisks} from './persons-10-part-a-risk.mjs';
import {checkPersons10PartBRisks} from './persons-10-part-b-risk.mjs';
import {checkPersons10PartCRisks} from './persons-10-part-c-risk.mjs';
import {checkPersons10PartDRisks} from './persons-10-part-d-risk.mjs';
export function checkPersons10Risks(db){
 const parts=[checkPersons10PartARisks(db),checkPersons10PartBRisks(db),checkPersons10PartCRisks(db),checkPersons10PartDRisks(db)];
 for(const part of parts)assert.equal(part.ok,true);
 // Fångar den konkreta wrapperregressionen där föräldrar fick syskonart.
 const relations=db.prepare("SELECT r.object_id,k.* FROM revision r JOIN relation k ON k.revision_id=r.id WHERE r.operation_id='T-0661/persons-10-v1'").all();
 assert.ok(relations.length>0);
 for(const r of relations){
  if(r.relation_type==='parent')assert.equal(r.nature,'recorded_parent',r.object_id);
  if(r.relation_type==='spouse')assert.equal(r.nature,'recorded_spouse',r.object_id);
  if(r.relation_type==='sibling')assert.ok(['recorded_sibling','maternal_sibling'].includes(r.nature),r.object_id);
 }
 return {ok:true,groups:1+parts.reduce((n,p)=>n+p.groups,0),parts};
}
