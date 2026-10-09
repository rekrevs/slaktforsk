import fs from 'node:fs';import {openDB} from '../../../genealogy2/lib/store.mjs';import {readCurrent} from '../../../genealogy2/lib/domain.mjs';import crypto from 'node:crypto';
const db=openDB('genealogy2/data/research.sqlite',{readOnly:true});
const terms=['1852-09-24','24 september 1852','24/9 1852','Thilda Augusta','Carl Jakob','Ernst Johan','1874-11-03','1872-02-20','1850-07-19','1857-06-24','C-0623','C-0626','C-0449','C-0450','Rotte','Roth','faderskonflikt','faderskap','Bodan','folio 66','fol66','Lögdö','Lagforsbruk','Lagfors Bruk','Lundby','Fredberg','James','Schölin','Scholin','1839','1901-04-19','Lungsot','ålderssv'];
const patterns=[/P-00(?:21|51)|P-033[689]/,/CONTRACT-P-00(?:21|51)|CONTRACT-P-033[689]/];
let out=[],owner=[];for(const {object_id} of db.prepare('SELECT object_id FROM current_revision').all()){
 let o=readCurrent(db,object_id);if(o.evidence_status==='OWNER_CONFIRMED')owner.push(o);let hits=[];
 function scan(v,path){if(typeof v==='string'){let found=terms.filter(t=>v.toLocaleLowerCase().includes(t.toLocaleLowerCase()));if(found.length)hits.push({field:path,terms:found,value:v});try{if((v.startsWith('{')||v.startsWith('['))&&path.endsWith('_json'))scan(JSON.parse(v),path+'[parsed]')}catch{}}
 else if(v&&typeof v==='object')for(const[k,z]of Object.entries(v)){if(['origins','evidence','pending_reviews'].includes(k))continue;scan(z,path?path+'.'+k:k)}}scan(o,'');
 if(hits.length||patterns.some(re=>re.test(object_id)))out.push({object_id,revision_id:o.revision_id,kind:o.kind,subject:o.subject_id,disposition:o.disposition,evidence_status:o.evidence_status,hits,current:o});
}
let D='evaluations/T-0826/independent/';fs.writeFileSync(D+'semantic-scan-v2.json',JSON.stringify({performed_at:new Date().toISOString(),terms,source:'Independent readCurrent sweep, not Sol semantic index',objects:out},null,2)+'\n');fs.writeFileSync(D+'owner-all-current-v2.json',JSON.stringify(owner,null,2)+'\n');console.log({objects:out.length,owner:owner.length,hits:out.reduce((n,o)=>n+o.hits.length,0)});db.close();
