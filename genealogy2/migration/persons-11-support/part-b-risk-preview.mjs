// Read-only projection preview. The root also runs these checks after actual scratch import.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {buildPersons} from '../../import/persons.mjs';
import {openDB} from '../../lib/store.mjs';
import {checkPersons11PartBRisks} from '../../verification/persons-11-part-b-risk.mjs';
const source=openDB('genealogy2/data/research.sqlite',{readOnly:true});
const changes=new Map();
for(const cohort of ['10','11'])for(const part of ['a','b','c','d'])if(fs.existsSync(`genealogy2/migration/persons-${cohort}-${part}.json`))for(const p of JSON.parse(fs.readFileSync(`genealogy2/migration/persons-${cohort}-${part}.json`)))for(const x of p.changes)changes.set(x.id,x);
const payload=x=>Object.fromEntries(Object.entries(x.data).map(([k,v])=>[k,k.endsWith('_json')?JSON.stringify(v):v]));
const merged=kind=>{
  const rows=new Map(source.prepare(`select c.object_id,c.disposition,x.* from current_revision c join ${kind} x on x.revision_id=c.id`).all().map(x=>[x.object_id,x]));
  for(const x of changes.values())if(x.kind===kind)rows.set(x.id,{...payload(x),object_id:x.id,disposition:x.disposition});
  return [...rows.values()];
};
const fake={prepare(sql){return {
  get(id){const x=changes.get(id);if(!x)return source.prepare(sql).get(id);
    if(sql==='SELECT * FROM current_revision WHERE object_id=?')return {id:x.id,object_id:x.id,kind:x.kind,version:1,disposition:x.disposition,evidence_status:x.evidenceStatus,rationale:x.rationale,caveat:x.caveat};
    if(sql.startsWith('SELECT * FROM '))return payload(x);
    throw Error(sql);
  },
  all(id){
    if(sql.includes("x.relation_type='parent'"))return merged('relation').filter(x=>x.relation_type==='parent'&&x.to_person===id&&x.disposition==='accepted');
    if(sql.includes("p.role='witness'"))return merged('participation').filter(x=>x.event_id===id&&x.role==='witness');
    if(changes.has(id)&&(/FROM origin |FROM dependency |FROM pending_review /.test(sql)))return [];
    return source.prepare(sql).all(id);
  }
};}};
try {
  const own=JSON.parse(fs.readFileSync('genealogy2/migration/persons-11-b.json'));
  const allowed=['birth','baptism','confirmation','banns','marriage','divorce','death','burial','registered_arrival','registered_departure','residence','other'];
  for(const p of own)for(const x of p.changes){
    assert.ok(x.origins?.length,x.id);
    if(x.kind==='event')assert.ok(allowed.includes(x.data.event_type),x.id);
    if(x.kind==='search'){
      assert.equal(x.data.question_id,null,x.id);assert.ok(x.data.source_id,x.id);
      assert.ok(x.data.scope_json.query,x.id);assert.equal(Array.isArray(x.data.scope_json.bounds),false,x.id);
    }
  }
  const cohorts=JSON.parse(fs.readFileSync('genealogy2/migration/cohorts.json'));
  const group=cohorts.groups.find(g=>g.id==='persons-11');
  group.persons=own.map(p=>p.person);group.documents=own.flatMap(p=>p.documents.map(d=>d.path));
  const op=buildPersons(source,own,{group:'persons-11',cohorts});
  console.log({readOnlyBuild:true,changes:op.changes.length,decisions:op.unitDecisions.length});
  console.log(checkPersons11PartBRisks(fake));
  console.log({preview:'read-only; actual import validation remains root-owned',people:own.length,changes:own.reduce((n,p)=>n+p.changes.length,0)});
}finally{source.close();}
