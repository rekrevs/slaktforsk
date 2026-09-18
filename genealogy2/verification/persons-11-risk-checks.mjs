import assert from'node:assert/strict';
import{checkPersons11PartARisks}from'./persons-11-part-a-risk.mjs';
import{checkPersons11PartBRisks}from'./persons-11-part-b-risk.mjs';
import{checkPersons11PartCRisks}from'./persons-11-part-c-risk.mjs';
import{checkPersons11PartDRisks}from'./persons-11-part-d-risk.mjs';
import{checkPersons11EkholmRisks}from'./persons-11-ekholm-risk.mjs';
export function checkPersons11Risks(db){
 const parts=[checkPersons11PartARisks(db),checkPersons11PartBRisks(db),checkPersons11PartCRisks(db),checkPersons11PartDRisks(db),checkPersons11EkholmRisks(db)];
 for(const part of parts)assert.equal(part.ok,true);
 const relations=db.prepare("SELECT r.object_id,k.* FROM revision r JOIN relation k ON k.revision_id=r.id WHERE r.operation_id='T-0662/persons-11-v1'").all();
 assert.ok(relations.length>0);
 for(const r of relations){if(r.relation_type==='parent')assert.equal(r.nature,'recorded_parent',r.object_id);if(r.relation_type==='spouse')assert.equal(r.nature,'recorded_spouse',r.object_id);if(r.relation_type==='sibling')assert.ok(['recorded_sibling','maternal_sibling','paternal_sibling'].includes(r.nature),r.object_id);}
 return{ok:true,groups:1+parts.reduce((n,p)=>n+p.groups,0),parts};
}
