import fs from 'node:fs';
import {sha,canonical} from '../lib/archive.mjs';
import {head} from '../lib/domain.mjs';

const operationId='T-0645/registry-v1';
const pilot=JSON.parse(fs.readFileSync(new URL('../operations/T-0641-pilot-v1.json',import.meta.url),'utf8'));
const reused=new Set(pilot.changes.filter(c=>['source','person'].includes(c.kind)).map(c=>c.id));

export function buildRegistry(db,decisions) {
  const cohorts=JSON.parse(fs.readFileSync(new URL('../migration/cohorts.json',import.meta.url),'utf8'));
  if(db.prepare('SELECT id FROM import_batch').get()?.id!==cohorts.baseline)throw Error('Fel importbas för registren');
  const retired=JSON.parse(db.prepare('SELECT text FROM document WHERE path=?').get('genealogy/avvecklade-akter.json').text).akter;
  if(canonical(Object.keys(decisions).sort())!==canonical(Object.keys(retired).sort()))throw Error('Alla 27 avvecklingar måste ha individuella beslut');
  const request={id:operationId,actor:'Codex/T-0645',reason:'Förlustfri registeröverföring och separat prövning av avvecklade akters betydelse. Ingen ny släktforskning eller uppgradering av forskningsstatus.',spans:[],changes:[],mappings:[]};
  const document=path=>{
    const d=db.prepare('SELECT * FROM document WHERE path=?').get(path);if(!d)throw Error(`Saknat dokument: ${path}`);return d;
  };
  const span=(d,startLine=1,endLine=d.text.split('\n').length)=> {
    const lines=d.text.split(/(?<=\n)/);
    if(startLine<1||endLine<startLine||endLine>lines.length+1)throw Error('Ogiltigt granskningsspann');
    const start=Buffer.byteLength(lines.slice(0,startLine-1).join('')),end=Buffer.byteLength(lines.slice(0,endLine).join(''));
    const id=sha(`${d.path}\0${d.sha256}\0curated_span\0${start}\0${end}`);
    if(!request.spans.some(s=>s.id===id))request.spans.push({id,path:d.path,sha256:d.sha256,start,end,section:`Registerunderlag ${startLine}–${endLine}`});
    return id;
  };
  const origin=(unit,coverage='partial')=>({unit,coverage,note:'Återanvändning av äldre forskningsunderlag; inte ett nytt oberoende belägg.'});
  const add=(id,kind,data,origins,rationale,caveat='')=> {
    const existing=head(db,id);
    if(existing&&existing.operation_id!==operationId)throw Error(`Oväntat befintligt registerobjekt: ${id}`);
    request.changes.push({id,kind,data,expectedVersion:null,disposition:'recorded',rationale,caveat,origins});
  };
  const entries=kind=>{
    const rows=db.prepare('SELECT e.*,d.text,d.sha256,d.bytes FROM legacy_entity e JOIN document d ON d.path=e.document_path WHERE e.kind=? ORDER BY e.id').all(kind);
    const expected=cohorts.groups.flatMap(g=>g[kind==='person'?'persons':'sources']).sort();
    if(canonical(rows.map(r=>r.id))!==canonical(expected))throw Error(`Registeromfånget avviker: ${kind}`);
    return rows;
  };
  for(const e of entries('source')) {
    if(reused.has(e.id))continue;
    const unit=span({...e,path:e.document_path});
    add(e.id,'source',{title:e.title,archive_reference:null,source_class:null,description:e.text},[origin(unit,'complete')],
      'Den fullständiga äldre källbeskrivningen och dess metadata bevaras ordagrant. Separata normaliserade arkivfält och källklass tilldelas inte genom gissning.');
  }
  const people=entries('person');
  for(const e of people) {
    const decision=decisions[e.id];
    if(decision&&!['separate_person','same_identity','historical_proposal','unresolved'].includes(decision.outcome))throw Error(`Okänt avvecklingsbeslut: ${e.id}`);
    if(decision&&['same_identity','historical_proposal'].includes(decision.outcome))continue;
    const identity=db.prepare("SELECT id FROM unit WHERE document_path=? AND kind='section' AND section='Identitet'").all(e.document_path);
    if(identity.length!==1)throw Error(`Identitetsavsnittet är inte entydigt: ${e.id}`);
    if(!reused.has(e.id))add(e.id,'person',{
      display_name:decision?.displayName??e.title.replace(/^P-\d{4}:\s*/,''),sex:null,legacy_state:decision?'retired':'active'
    },[origin(identity[0].id),...(decision?.evidence??[]).map(e=>origin(span(document(e.path),e.startLine,e.endLine)))],decision?.rationale??'En registrerad personkärna bevarar det äldre id:t och visningsnamnet. Sammanföringar, släktrelationer, kön och forskningsbedömningar har inte omprövats av registeröverföringen.',
    decision?.caveat??'Registeröverföring; fortsatta identitets- och sakbedömningar läses i det bevarade underlaget tills personkohorten är konverterad.');
    request.mappings.push({id:`MAP-T0645-${e.id}`,legacyId:e.id,target:e.id,type:'archival_reference',unit:identity[0].id,
      rationale:decision?.rationale??'Samma befintliga person-id förs vidare som registrerad kärna; detta förenar inte två personidentiteter.'});
  }
  for(const [id,d] of Object.entries(decisions).sort(([a],[b])=>a.localeCompare(b))) {
    if(!d.rationale?.trim()||!d.caveat?.trim()||!Array.isArray(d.evidence)||!d.evidence.length)throw Error(`Ofullständigt avvecklingsbeslut: ${id}`);
    const target=['same_identity','historical_proposal'].includes(d.outcome)?d.target:id;
    if(!target||!people.some(p=>p.id===target))throw Error(`Beslut saknar personmål: ${id}`);
    const units=d.evidence.map(e=>span(document(e.path),e.startLine,e.endLine));
    add(`IMPORT-${id}`,'assessment',{subject_id:target,criteria:'legacy_dossier_identity_import/1',outcome:d.outcome,
      body:`Äldre akt: ${id}. Tidigare avvecklingsmotsvarighet: ${retired[id].motsvarighet}.\n\n${d.rationale}\n\n${d.caveat}`},units.map(u=>origin(u)),d.rationale,d.caveat);
    if(['same_identity','historical_proposal'].includes(d.outcome)) {
      const type=d.outcome==='same_identity'?'same_identity':'archival_reference';
      const existing=db.prepare('SELECT * FROM legacy_mapping WHERE legacy_id=? AND mapping_type=? AND operation_id!=?').all(id,type,operationId);
      if(existing.some(m=>m.target_id!==target))throw Error(`Mappningen motsäger äldre beslut: ${id}`);
      if(!existing.length)request.mappings.push({id:`MAP-T0645-${id}`,legacyId:id,target,type,unit:units[0],rationale:d.rationale+' '+d.caveat});
    }
  }
  return request;
}

export function registryReport(db) {
  const people=db.prepare("SELECT e.id,p.object_id,m.mapping_type,m.target_id FROM legacy_entity e LEFT JOIN current_revision p ON p.object_id=e.id AND p.kind='person' LEFT JOIN legacy_mapping m ON m.legacy_id=e.id WHERE e.kind='person' ORDER BY e.id,m.id").all();
  const missingPeople=[...new Set(people.filter(p=>!p.object_id&&!p.target_id).map(p=>p.id))];
  const missingSources=db.prepare("SELECT e.id FROM legacy_entity e LEFT JOIN current_revision r ON r.object_id=e.id AND r.kind='source' WHERE e.kind='source' AND r.id IS NULL ORDER BY e.id").all().map(r=>r.id);
  const outcomes=db.prepare("SELECT a.outcome,count(*) n FROM assessment a JOIN current_revision r ON r.id=a.revision_id WHERE a.criteria='legacy_dossier_identity_import/1' GROUP BY a.outcome ORDER BY a.outcome").all();
  return {legacyPeople:new Set(people.map(p=>p.id)).size,persons:db.prepare("SELECT count(*) n FROM current_revision WHERE kind='person'").get().n,
    sources:db.prepare("SELECT count(*) n FROM current_revision WHERE kind='source'").get().n,missingPeople,missingSources,retirementOutcomes:outcomes,
    personDispositions:db.prepare("SELECT disposition,count(*) n FROM current_revision WHERE kind='person' GROUP BY disposition").all(),
    note:'Registertäckning är inte full konvertering av personernas forskning. Bibliografiska metadata ligger ordagrant i source.description tills de normaliserats med uttryckligt underlag.'};
}
