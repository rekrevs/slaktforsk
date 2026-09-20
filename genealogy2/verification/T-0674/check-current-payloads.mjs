import fs from 'node:fs';
import {isDeepStrictEqual} from 'node:util';
import {openDB} from '../../lib/store.mjs';
import {inspect} from '../../lib/domain.mjs';
const root='genealogy2/verification/T-0674/';
const entries=fs.readdirSync('genealogy2/journal').filter(n=>n.endsWith('.json')).sort().map(n=>JSON.parse(fs.readFileSync('genealogy2/journal/'+n)));
const latest=new Map();
for(const j of entries)for(const c of j.request?.changes??[])latest.set(c.id,{c,j});
const db=openDB('genealogy2/data/research.sqlite',{readOnly:true});
const errors=[],checked=[];
for(const [id,{c,j}] of latest){if(!j.request.id?.startsWith('T-0674/'))continue;const x=inspect(db,id),r=x.revisions.at(-1);const failures=[];
for(const [k,v] of Object.entries(c.data??{})){let a=r.data[k];if(a===undefined && r.data[k+'_json']!==undefined){try{a=JSON.parse(r.data[k+'_json']);}catch{a=r.data[k+'_json'];}}let expected=v;if(k.endsWith('_json')){try{if(typeof a==='string')a=JSON.parse(a);if(typeof expected==='string')expected=JSON.parse(expected);}catch{}}if(!isDeepStrictEqual(a,expected))failures.push('data.'+k);}
if(r.operation_id!==j.request.id)failures.push('operation');
for(const o of c.origins??[])if(!r.origins.some(a=>a.id===o.unit&&a.coverage===o.coverage&&a.note===(o.note??'')))failures.push('origin:'+o.unit);
for(const e of c.evidence??[])if(!r.evidence.some(a=>a.basis_revision_id===`${e.object}@${e.version}`&&a.role===e.role))failures.push('evidence:'+e.object);
checked.push({id,version:x.currentVersion,operation:j.request.id});if(failures.length)errors.push({id,failures});}
db.close();const report={journalSequence:entries.at(-1).sequence,checked:checked.length,errors,objects:checked};fs.writeFileSync(root+'current-payload-check.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({checked:checked.length,errors}));process.exitCode=errors.length?1:0;
