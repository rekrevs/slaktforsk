// Kompletterar ännu ej infört paket med redan befintliga deluppgifter i relationsrader.
import fs from'node:fs';import{units,db}from'./genealogy2-persons08-combined.mjs';
const file='genealogy2/migration/persons-08-a.json',rows=JSON.parse(fs.readFileSync(file));
function link(person,needle,ids){const p=rows.find(r=>r.person===person),u=units(person,'person').find(u=>u.kind==='relation_row'&&JSON.parse(u.parsed_json).cells[0].includes(needle));if(!u)throw Error(person+needle);const decision=p.relations.find(r=>r.unit===u.id);for(const id of ids){if(!decision.targets.includes(id))decision.targets.push(id);if(!p.changes.some(m=>m.id===id)){let reused=p.reuse.find(r=>r.object===id);if(!reused){reused={object:id,origins:[],rationale:'Relationsradens redan belagda datum/namn/kvalifikation återbrukas uttryckligen.'};p.reuse.push(reused);}if(!reused.origins.includes(u.id))reused.origins.push(u.id);}}}
link('P-0388','Cajsa',['F-P-0388-family_context-childhood']);
link('P-0389','P-0311',['E-birth-P-0311']);
link('P-0394','P-0253',['E-birth-P-0253']);link('P-0394','P-0366',['E-birth-P-0366']);
for(const id of ['P-0390','P-0391','P-0392','P-0393']){const p=rows.find(r=>r.person===id),o=p.changes.find(c=>c.id===`F-${id}-source_assessment-own-row-limits`);delete o.data.value_json.old_all_children_v_literal_rejected_for_P0393;o.data.value_json.old_all_children_v_literal_conflicts_with_P0393_own_reading=true;}
// Personen0397 saknar egen förekomst i gravrätten; dess elva poster är endast bakgrund.
for(const id of ['P-0398','P-0399','P-0400']){const p=rows.find(r=>r.person===id);if(!p.reuse.some(r=>r.object===`IMPORT-${id}`))p.reuse.push({object:`IMPORT-${id}`,origins:[units(id,'person').find(u=>u.kind==='section'&&u.section==='Arbetsläge').id],rationale:'Bevarat ägarbeslut om avvecklad forskning; ingen ny forskningskö.'});}
fs.writeFileSync(file,JSON.stringify(rows,null,2)+'\n');
