import fs from'node:fs';
const path='genealogy2/migration/persons-10-c.json',rows=JSON.parse(fs.readFileSync(path));
for(const p of rows){
 for(const m of p.changes){
  if(m.kind==='relation'&&m.data.relation_type==='parent'&&m.data.nature==='recorded_sibling')m.data.nature='recorded_parent';
  if(m.id==='E-birth-P-0491')m.data.date_json={precision:'unknown',literal:'Födelseår1894eller1895; gravregisterrapporterar1894-04-13. Ingenår/dagvald.'};
  if(m.id.endsWith('source_assessment-names-dates-and-grave')){delete m.data.value_json.own_adult_civil_status;m.data.value_json.civil_status_after_1910=null;}
  if(m.id==='F-P-0499-source_interpretation-birth-context-and-siblings'){m.data.value_json.birth_home_role='Faderns rapporterade hemvist, inte belagd exakt fysisk födelseplats.';}
  if(m.id==='O-P-0499-C0794-birth-own'){m.data.value_json.home_role='faderns hemvist';m.data.value_literal=JSON.stringify(m.data.value_json);}
 }
 if(p.person==='P-0498'){
  const extras=['M-P-0474-younger-Hedda','O-P-0474-younger-Hedda','E-death-younger-Hedda-Gatstugan1883','EP-E-death-younger-Hedda-Gatstugan1883-younger-Hedda-principal'];
  for(const id of extras)if(!p.reuse.some(r=>r.object===id))p.reuse.push({object:id,origins:p.changes[0].origins,rationale:'Återbrukar den separata yngre barnradens omnämnande/dödsnot utan identitetslänk till den äldre Hedda.'});
  const a=p.assertions.find(a=>a.id==='A-4764');a.targets=[...new Set([...a.targets,...extras])];
  const rr=p.relations.find(r=>r.targets.includes('F-P-0474-family_context-two-Heddas'));rr.targets=[...new Set([...rr.targets,...extras])];
 }
}
const temp=path+'.writing-'+process.pid;fs.writeFileSync(temp,JSON.stringify(rows,null,2)+'\n');fs.renameSync(temp,path);
console.log({people:rows.length,changedParentNature:rows.flatMap(p=>p.changes).filter(m=>m.kind==='relation'&&m.data.relation_type==='parent').map(m=>[m.id,m.data.nature])});
