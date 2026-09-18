import fs from 'node:fs';import {DatabaseSync} from 'node:sqlite';
process.chdir('/Users/sverker/repos/slaktforsk');
export const db=new DatabaseSync('genealogy2/data/research.sqlite',{readOnly:true});
export const doc=(id,kind)=>db.prepare('SELECT d.*,e.id legacy_id FROM document d JOIN legacy_entity e ON e.document_path=d.path WHERE e.id=? AND e.kind=?').get(id,kind);
export const units=(id,kind)=>db.prepare('SELECT * FROM unit WHERE document_path=? ORDER BY start_byte').all(doc(id,kind).path);
export const origins=(entity,kind,startLine,endLine=startLine)=>({entity,kind,startLine,endLine});
export const exact=value=>({precision:'exact',value,literal:value});
export const unknown=()=>({precision:'unknown',literal:'Ingen säker datering av relationens början/slut.'});
export function person(id,readingNote) {return {person:id,documents:['person','profile'].map(k=>{const d=doc(id,k);return {path:d.path,sha256:d.sha256};}),readingNote,changes:[],reuse:[],assertions:[],relations:[],pending:[]};}
export function add(p,id,kind,data,origin,evidence=[],caveat='',status='TRANSCRIBED',disposition='accepted',rationale='Återbrukar uttrycklig befintlig kunskap; ingen ny forskning.') {
 const m={id,kind,data,disposition,evidenceStatus:status,rationale,caveat,origins:origin,evidence:evidence.map(e=>typeof e==='string'?{object:e,role:'supports',note:'Tidigare bevarat underlag, inte en extra oberoende röst.'}:e)};p.changes.push(m);return id;
}
export function assertion(p,id,targets,rationale,state='mapped_complete',question='') {p.assertions.push({id,state,targets,rationale,question});}
export function relationRow(p,target,targets,rationale,state='mapped_complete',question='') {const rows=units(p.person,'person').filter(u=>u.kind==='relation_row'&&JSON.parse(u.parsed_json).cells[0].includes(target));if(rows.length!==1)throw Error(target+':'+rows.length);p.relations.push({unit:rows[0].id,state,targets,rationale,question});return rows[0].id;}
export function save(p) {const own=new Map(units(p.person,'person').filter(u=>u.kind==='assertion'&&!u.historical).map(u=>[u.legacy_id,u.id]));for(const m of [...p.changes,...p.reuse])m.origins=m.origins.map(o=>typeof o==='string'&&own.has(o)?own.get(o):o);const part=process.env.GENEALOGY_REVIEW_PART;if(!['a','b','c','d'].includes(part))throw Error('Ange GENEALOGY_REVIEW_PART=a|b|c|d');const path=`genealogy2/migration/persons-09-${part}.json`,rows=fs.existsSync(path)?JSON.parse(fs.readFileSync(path)):[];if(rows.some(r=>r.person===p.person))throw Error('Redan sparad');rows.push(p);rows.sort((a,b)=>a.person.localeCompare(b.person));const temp=path+'.writing-'+process.pid;fs.writeFileSync(temp,JSON.stringify(rows,null,2)+'\n');fs.renameSync(temp,path);}
