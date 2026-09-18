// Förfinar endast denna agents ofrysta delpaket, aldrig huvuddatabasen.
import fs from 'node:fs';import{cs}from './part-c-common.mjs';
const file='genealogy2/migration/persons-09-c.json';const ps=JSON.parse(fs.readFileSync(file));
for(const p of ps){for(const c of p.changes){const m=c.id.match(/C(\d{4})-w\d+$/);if(m&&['mention','observation'].includes(c.kind)){const origin=cs(`C-${m[1]}`);if(!c.origins.some(o=>JSON.stringify(o)===JSON.stringify(origin)))c.origins.push(origin);}}}
const c=ps.find(p=>p.person==='P-0442').changes.find(c=>c.id==='F-P-0442-family_context-rosinedahl');c.data.value_json.half_cousin=c.data.value_json.half_cousin.replace('D eg er fors','Degerfors');
fs.writeFileSync(file+'.tmp',JSON.stringify(ps,null,2)+'\n');fs.renameSync(file+'.tmp',file);
