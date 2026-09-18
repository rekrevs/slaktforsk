export * from './genealogy2-persons10-combined.mjs';
import {doc,units,origins,relation} from './genealogy2-persons10-combined.mjs';
export const all=p=>[origins(p.person,'person',1,doc(p.person,'person').text.trimEnd().split('\n').length)];
export const year=value=>({precision:'year',value:String(value),literal:String(value)});
export function kin(p,other,type='sibling',nature=type==='parent'?'recorded_parent':'recorded_sibling',os=all(p)){return relation(p,type==='parent'?other:p.person,type==='parent'?p.person:other,type,os,nature);}
export function relRows(p,map){for(const u of units(p.person,'person').filter(u=>u.kind==='relation_row'&&!u.historical)){const cells=JSON.parse(u.parsed_json).cells;if(cells[0]==='Person')continue;const key=Object.keys(map).find(x=>cells[0].includes(x));if(!key)throw Error(`Ej granskad relation ${p.person}: ${cells[0]}`);p.relations.push({unit:u.id,state:'mapped_complete',targets:map[key],rationale:'Individuellt granskad relation och dess uttryckliga avgränsning återfinns i målen.',question:''});}}
