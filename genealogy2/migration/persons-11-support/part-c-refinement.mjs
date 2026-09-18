// Idempotenta preciseringar av ännu ej infört eget c-paket. Ingen DB- eller annan packet-skrivning.
import fs from 'node:fs';
import {units} from './genealogy2-persons11-combined.mjs';
const file='genealogy2/migration/persons-11-c.json';
const rows=JSON.parse(fs.readFileSync(file));
for(const p of rows){
 const core=p.changes.find(x=>x.id===p.person);
 core.data.sex=null;
 core.caveat=core.caveat.replace(' Kön följer den individuellt belagda moders-/hustrurelationen eller son-/dotterrollen, inte namngissning.','');
 if(!core.caveat.includes('Inget separat explicit könsfält'))core.caveat+=' Inget separat explicit könsfält har utvunnits; råroller och relationer bevaras utan att fylla sex.';
 for(const x of p.pending)x.question=x.question.replace('IDENTiTY-','IDENTITY-');
}
const p520=rows.find(p=>p.person==='P-0520'),row521=units('P-0520','person').find(u=>u.kind==='relation_row'&&!u.historical&&JSON.parse(u.parsed_json).cells[0].includes('P-0521'));
const correction='F-P-0521-name_form-Eva-rejected';
if(!p520.reuse.some(x=>x.object===correction))p520.reuse.push({object:correction,origins:[row521.id],rationale:'Lisa-rättelsen gäller även den äldre Eva-benämningen i Annas relationsrad.'});
const relation=p520.relations.find(x=>x.unit===row521.id);if(!relation.targets.includes(correction))relation.targets.push(correction);
for(const key of['AI4','AI6']){
 const o=rows.find(p=>p.person==='P-0523').changes.find(x=>x.id===`O-P-0523-${key}-own`);
 o.data.value_json.empty_fields=o.data.value_json.empty_fields.filter(x=>x!=='anmärkningar'&&(key!=='AI4'||x!=='utflyttning'));
 o.data.value_literal=JSON.stringify(o.data.value_json);
}
// Synka familjekontextens rapporterade dödsdag med dotterns uttryckliga atomärspärr.
const family=rows[0].changes.find(x=>x.id==='F-P-0519-family_context-nine-known-children');
Object.assign(family.data.value_json.known_child_death,{separate_final_check_required:true,separate_final_check_done:false,atomic_event_disposition:'candidate'});
const mother527=rows[0].relations.find(x=>x.targets.includes('REL-parent-P-0519-P-0527'));
if(!mother527.targets.includes('F-P-0527-death_assessment-reported-household-note'))mother527.targets.push('F-P-0527-death_assessment-reported-household-note');
if(!rows[0].reuse.some(x=>x.object==='F-P-0527-death_assessment-reported-household-note'))rows[0].reuse.push({object:'F-P-0527-death_assessment-reported-household-note',origins:[mother527.unit],rationale:'Barnets positiva dödsnot har uttrycklig separat slutkontroll kvar; ingen familjerad får göra den till verifierad atomär död.'});
for(const p of rows)for(const d of[...p.assertions,...p.relations])d.targets=[...new Set(d.targets)];
const tmp=file+'.writing-'+process.pid;fs.writeFileSync(tmp,JSON.stringify(rows,null,2)+'\n');fs.renameSync(tmp,file);
