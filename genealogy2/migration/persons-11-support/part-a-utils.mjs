export * from './genealogy2-persons11-combined.mjs';
import {db,units,origins,add,record,reuse,known,relationRow as baseRelationRow} from './genealogy2-persons11-combined.mjs';
import {readCurrent} from '../../lib/domain.mjs';
export const full=p=>[origins(p.person,'person',1,Math.max(...units(p.person,'person').map(u=>u.end_line)))];
export function relationRow(p,target,targets,rationale){return baseRelationRow(p,target,targets,rationale);}
export function use(p,id,os,expected={}){const v=readCurrent(db,id);if(!v)throw Error('Återbruk saknas '+id);for(const[k,x]of Object.entries(expected))if(v[k]!==x)throw Error(id+' fel '+k);return reuse(p,id,os);}
export function ownObservation(p,key,r,m,value,os,caveat=''){return add(p,`O-${p.person}-${key}`,'observation',{record_id:r,mention_id:m,property:'person_fields',value_literal:JSON.stringify(value),value_json:value},os,[r],caveat,'TRANSCRIBED','recorded');}
export function participation(p,e,m,role,os,caveat=''){const id=`EP-${e}-${p.person}-${role}`;if(known(id))return reuse(p,id,os);return add(p,id,'participation',{event_id:e,person_id:p.person,mention_id:m,role},os,[e,m].filter(Boolean),caveat);}
export function search(p,key,source,query,bounds,body,os,outcome='negative'){return add(p,`SEARCH-${p.person}-${key}`,'search',{question_id:null,source_id:source,scope_json:{description:body,query,bounds},outcome,body},os,[],body,outcome==='negative'?'NEGATIVE':'TRANSCRIBED','recorded');}
export function ev(p,id,bases){const m=p.changes.find(m=>m.id===id);if(!m)throw Error(id);m.evidence=bases.map(object=>({object,role:'supports',note:'Samma bevarade underlag; ingen extra oberoende röst.'}));return id;}
