import assert from 'node:assert/strict';
import {sha,canonical} from '../lib/archive.mjs';
import {buildObservationA} from './T-0663-observation-a.mjs';
import {buildObservationCorrectionsC} from './T-0663-observation-c.mjs';
import {buildStatusReview} from './T-0663-status-review.mjs';
import {buildBannsReview} from './T-0663-banns-review.mjs';

export function buildCorrections(db){
 const parts=[buildObservationA(db),buildObservationCorrectionsC(db),buildStatusReview(db),buildBannsReview(db)];
 const id='T-0663/reviewed-corrections-v1',changes=parts.flatMap(p=>p.changes);
 assert.equal(new Set(changes.map(c=>c.id)).size,changes.length,'Överlappande objekt kräver gemensam sakprövning');
 const spanMap=new Map(),decisionMap=new Map();
 for(const p of parts){
  for(const s of p.spans??[]){
   const previous=spanMap.get(s.id);if(previous)for(const k of ['path','sha256','start','end'])assert.equal(s[k],previous[k]);else spanMap.set(s.id,s);
  }
  for(const d of p.unitDecisions??[]){
   const prior=decisionMap.get(d.unit);
   if(!prior){decisionMap.set(d.unit,structuredClone(d));continue;}
   for(const k of ['expectedVersion','state','target','question'])assert.equal(d[k],prior[k],`Skilda utfall på ${d.unit}/${k}`);
   prior.targets=[...new Set([...prior.targets,...d.targets])].sort();prior.rationale+='\n'+d.rationale;
  }
 }
 const dependencyReviews=parts.flatMap(p=>p.dependencyReviews??[]);
 const retained=dependencyReviews.filter(r=>r.outcome==='retain_existing_revision');assert.equal(retained.length,25);
 const resolve=retained.map(r=>({request:sha(`${id}:${r.affected_revision_id}:${r.changed_revision_id}`),rationale:r.rationale}));
 assert.equal(new Set(resolve.map(r=>r.request)).size,25);
 const result={id,actor:'Codex',reason:'Individuellt granskade migrationsrättelser: 22 observationers post-/bedömningsgränser, 44 importorsakade säkerhetsetiketter och tre lysningars månadsreservation. Tidigare revisioner och sakliga konflikter bevaras.',
  changes,spans:[...spanMap.values()].sort((a,b)=>a.id.localeCompare(b.id)),unitDecisions:[...decisionMap.values()].sort((a,b)=>a.unit.localeCompare(b.unit)),resolve,
  review:{parts:parts.map(p=>p.review),dependencyReviews}};
 assert.equal(changes.length,111);
 return result;
}
