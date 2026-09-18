// Idempotenta schemaanpassningar efter avgränsat förprov. Inga nya sakläsningar.
import fs from'node:fs';import{units}from'./genealogy2-persons11-combined.mjs';
const file='genealogy2/migration/persons-11-d.json';
const reviews=JSON.parse(fs.readFileSync(file,'utf8').replaceAll('E-migration-P-0529','E-registered_arrival-P-0529'));
const by=id=>reviews.flatMap(p=>p.changes).find(c=>c.id===id);
by('E-registered_arrival-P-0529').data.event_type='registered_arrival';
by('E-death-P-0531').data.date_json={precision:'range',from:'1997-04-01',to:'1997-04-30',literal:'1997-04; dag saknas'};
for(const id of ['ID-P-0537-C1049-other-Lars','ID-P-0538-C1048-rejected-apr','ID-P-0538-C1048-rejected-aug'])by(id).evidenceStatus='REJECTED';
const scopes={
 'SEARCH-P-0536-Mofalla1824':{description:'Mofalla C/2, bevarad namn- och dagspassage1824 på bilder59–60',bounds:{year:1824,images:['C0051784_00059','C0051784_00060'],calendar_error_in_transcription:true}},
 'SEARCH-P-0536-Kyrkefalla1824':{description:'Kyrkefalla C/4, födelseåret1824 på bilder131–133, datum och namn',bounds:{year:1824,images:[131,132,133]}},
 'SEARCH-P-0537-birth1791':{description:'Kyrkefalla C/4 hela födelseåret1791 på datum och namn',bounds:{year:1791,target_image:'C0052885_00044',year_heading:'C0052885_00043'}},
 'SEARCH-P-0538-Varola1799':{description:'Varolaavsnittet1799 i pastoratsbokC/4, alla22dop',query:'Stina Jansdotter/Christina/Chierstin och1mars1799',bounds:{year:1799,parish:'Varola',image:'C0053282_00054',from_heading:'Varola1799',to_heading:'Värsås1799',entries:22}},
 'SEARCH-P-0538-pastorat1799-January3':{description:'Januaridatum1799 i fyra pastoratsavsnitt',bounds:{year:1799,month:'januari',parishes:['Varola','Värsås','Ljunghem','Edåsa'],March1_not_in_scope:true}}
};
for(const[id,extra]of Object.entries(scopes))Object.assign(by(id).data.scope_json,extra);
const path=units('P-0536','profile').find(u=>u.kind==='source_path'&&u.legacy_id==='P-0536/KP-02');if(!path)throw Error('KP02 saknas');
const movement=by('F-P-0536-source_search_report-B3-1848');movement.data.value_json.origin='profilKP02';const old=units('P-0536','profile').find(u=>u.kind==='source_path'&&u.legacy_id==='P-0536/KP-01');movement.origins=movement.origins.filter(x=>x!==old?.id);if(!movement.origins.includes(path.id))movement.origins.push(path.id);
fs.writeFileSync(file,JSON.stringify(reviews,null,2)+'\n');
