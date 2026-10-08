// Task-local read-only extraction. No new queue, interpretation or research write.
import fs from 'node:fs';import path from 'node:path';
import {openDB} from '../../../genealogy2/lib/store.mjs';
import {head,personView,inspect} from '../../../genealogy2/lib/domain.mjs';
import {identityGate} from '../../../genealogy2/lib/review.mjs';
import {researchInventory} from '../../../genealogy2/lib/inventory.mjs';
import {pedigree} from '../../../genealogy2/lib/pedigree.mjs';
import {sha,canonical} from '../../../genealogy2/lib/archive.mjs';
const R=process.cwd(),D=path.join(R,'evaluations/T-0813/preparation'),scope=JSON.parse(fs.readFileSync(path.join(D,'fixed-scope-v1.json'))),baseline=JSON.parse(fs.readFileSync(path.join(D,'baseline-v1.json'))),start=Date.now(),db=openDB(path.join(R,baseline.main.path),{readOnly:true});
const save=(name,value)=>{const p=path.join(D,name);if(fs.existsSync(p))throw Error('Refuse overwrite '+p);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(value,null,2)+'\n');return 'evaluations/T-0813/preparation/'+name;};
const heads=new Map(db.prepare('SELECT * FROM current_revision').all().map(r=>[r.object_id,r]));
const revs=new Map(db.prepare('SELECT r.*,o.kind FROM revision r JOIN object o ON o.id=r.object_id').all().map(r=>[r.id,r]));
function native(r){if(!r)return null;const data=db.prepare(`SELECT * FROM ${r.kind} WHERE revision_id=?`).get(r.id);for(const key of Object.keys(data))if(key.endsWith('_json')&&data[key]!==null)data[key]=JSON.parse(data[key]);return {...r,data,origins:db.prepare('SELECT * FROM origin WHERE revision_id=? ORDER BY rowid').all(r.id),evidence:db.prepare('SELECT * FROM dependency WHERE revision_id=? ORDER BY rowid').all(r.id),...(r.kind==='record'?{assets:db.prepare('SELECT * FROM record_asset WHERE revision_id=? ORDER BY rowid').all(r.id),media:db.prepare('SELECT * FROM record_media WHERE revision_id=? ORDER BY rowid').all(r.id)}:{})};}
const revisions=new Map();function register(r){if(r&&!revisions.has(r.id))revisions.set(r.id,native(r));return r?.id;}
function objectRefs(value,ids=new Set()){if(typeof value==='string'){if(heads.has(value))ids.add(value);else if(revs.has(value))ids.add(revs.get(value).object_id);}else if(value&&typeof value==='object')for(const v of Object.values(value))objectRefs(v,ids);return ids;}
const old=JSON.parse(fs.readFileSync('evaluations/T-0812/preparation/all-current-OWNER-scope-v1.json'));const current=[...heads.values()].filter(r=>r.evidence_status==='OWNER_CONFIRMED').map(native);const before=new Map(old.OWNER_full_native.map(r=>[r.id,r]));const matches=current.map(r=>({id:r.id,unchanged:canonical(r)===canonical(before.get(r.id))}));if(matches.some(r=>!r.unchanged)||current.length!==45)throw Error('OWNER delta requires explicit capture');save('all-current-OWNER-scope-v1.json',{...old,current481_exact_check:matches});db.close();
