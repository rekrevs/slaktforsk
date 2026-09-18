// Läsande byggförprov; ingen operation appliceras och ingen DB-kopia skapas.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {db,units} from './genealogy2-persons11-combined.mjs';
import {buildPersons} from '../../import/persons.mjs';
const reviews=JSON.parse(fs.readFileSync('genealogy2/migration/persons-11-c.json'));
assert.deepEqual(reviews.map(x=>x.person),Array.from({length:9},(_,i)=>'P-0'+(519+i)));
for(const p of reviews){
 const u=units(p.person,'person');
 assert.deepEqual(p.assertions.map(x=>x.id).sort(),u.filter(x=>x.kind==='assertion'&&!x.historical).map(x=>x.legacy_id).sort());
 assert.deepEqual(p.relations.map(x=>x.unit).sort(),u.filter(x=>x.kind==='relation_row'&&!x.historical&&JSON.parse(x.parsed_json).cells[0]!=='Person').map(x=>x.id).sort());
 for(const x of p.changes){
  if(x.kind==='relation')assert.equal(x.data.nature,'recorded_'+x.data.relation_type);
  if(x.kind==='observation'){const mention=p.changes.find(m=>m.id===x.data.mention_id);assert.equal(x.data.record_id,mention.data.record_id);}
 }
}
const cohorts=JSON.parse(fs.readFileSync('genealogy2/migration/cohorts.json'));
const scope=cohorts.groups.find(x=>x.id==='persons-11');scope.persons=reviews.map(x=>x.person);scope.documents=reviews.flatMap(x=>x.documents.map(d=>d.path));
const op=buildPersons(db,reviews,{group:'persons-11',cohorts});
console.log({people:reviews.length,curated:reviews.reduce((n,p)=>n+p.changes.length,0),assertions:reviews.reduce((n,p)=>n+p.assertions.length,0),relations:reviews.reduce((n,p)=>n+p.relations.length,0),operation_changes:op.changes.length,spans:op.spans.length,decisions:op.unitDecisions.length,mode:'build-only',ok:true});
