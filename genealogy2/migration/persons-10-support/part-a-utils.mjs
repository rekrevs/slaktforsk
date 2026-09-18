export * from './genealogy2-persons10-combined.mjs';
import {units,origins,add,cs,record,relationRow as mapRelationRow} from './genealogy2-persons10-combined.mjs';
export function relationRow(p,target,targets,rationale='Individuellt bedömd relation; sakuppgifter och förbehåll bevaras i målobjekten.') {return mapRelationRow(p,target,targets,rationale);}
export const full=p=>[origins(p.person,'person',1,Math.max(...units(p.person,'person').map(x=>x.end_line)))];
export function observation(p,key,cid,filter,value,os,caveat='') {
  const r=record(cid,filter);
  return add(p,`O-${p.person}-${key}`,'observation',{record_id:r,mention_id:null,property:'source_fields',value_literal:JSON.stringify(value),value_json:value},[...os,cs(cid)],[r],caveat,'TRANSCRIBED','recorded');
}
export function search(p,key,source,query,bounds,body,os,outcome='negative') {
  return add(p,`SEARCH-${p.person}-${key}`,'search',{question_id:null,source_id:source,scope_json:{description:body,query,bounds},outcome,body},os,[],body,outcome==='negative'?'NEGATIVE':'TRANSCRIBED','recorded');
}
export function setLast(p,{status,disposition,rationale,caveat}={}) {const c=p.changes.at(-1);if(status)c.evidenceStatus=status;if(disposition)c.disposition=disposition;if(rationale)c.rationale=rationale;if(caveat)c.caveat=caveat;return c.id;}
export function rowTargets(p,target,targets,rationale) {
  const rows=units(p.person,'person').filter(u=>u.kind==='relation_row'&&!u.historical&&JSON.parse(u.parsed_json).cells[0]===target);
  if(rows.length!==1)throw Error(`Relationsrad ${p.person}/${target}:${rows.length}`);
  p.relations.push({unit:rows[0].id,state:'mapped_complete',targets,rationale,question:''});
}
