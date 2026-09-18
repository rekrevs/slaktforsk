import {sha,canonical} from './archive.mjs';
import {transaction} from './store.mjs';

export const DOMAIN_TABLES=['operation','object','revision','origin','dependency','review_request','review_resolution','person','source','record','record_asset','transcription','mention','observation','identity','identity_resolution','place','event','participation','relation','fact','question','search','assessment','narrative'];
const payloadKinds=new Set(DOMAIN_TABLES.slice(DOMAIN_TABLES.indexOf('person')).filter(k=>k!=='record_asset'));
const references={
  record:{source_id:'source'},transcription:{record_id:'record'},mention:{record_id:'record'},
  observation:{record_id:'record',mention_id:'mention'},identity:{mention_id:'mention',person_id:'person'},
  identity_resolution:{person_a:'person',person_b:'person'},place:{parent_id:'place'},
  event:{place_id:'place'},participation:{event_id:'event',person_id:'person',mention_id:'mention'},
  relation:{from_person:'person',to_person:'person'},fact:{subject_id:'*'},question:{subject_id:'*'},
  search:{question_id:'question',source_id:'source'},assessment:{subject_id:'*'},narrative:{subject_id:'*'}
};
export function head(db,id) {return db.prepare('SELECT * FROM current_revision WHERE object_id=?').get(id);}
const boundReferences={record:['source_id'],transcription:['record_id'],mention:['record_id'],
  observation:['record_id','mention_id'],identity:['mention_id'],participation:['event_id','mention_id']};

export function indexObject(db,id) {
  const r=head(db,id);if(!r)return;
  const data=db.prepare(`SELECT * FROM ${r.kind} WHERE revision_id=?`).get(r.id);
  db.prepare('DELETE FROM object_search WHERE object_id=?').run(id);
  db.prepare('INSERT INTO object_search(object_id,kind,text) VALUES (?,?,?)').run(id,r.kind,
    [id,r.disposition,r.evidence_status,r.rationale,r.caveat,...Object.values(data)].filter(x=>x!=null).join('\n'));
}

function validateDate(d) {
  if(!d||typeof d!=='object'||typeof d.literal!=='string'||!['exact','year','circa','range','alternatives','unknown'].includes(d.precision))throw Error('Datum kräver precision och råform');
  const iso=x=>typeof x==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(x)&&!Number.isNaN(Date.parse(x))&&new Date(x+'T00:00:00Z').toISOString().slice(0,10)===x;
  if(d.precision==='exact'&&!iso(d.value))throw Error('Ogiltigt exakt datum');
  if(d.precision==='year'&&!/^\d{4}$/.test(d.value))throw Error('Ogiltigt år');
  if(d.precision==='range'&&(!iso(d.from)||!iso(d.to)||d.from>d.to))throw Error('Ogiltigt datumintervall');
  if(d.precision==='alternatives'&&(!Array.isArray(d.values)||d.values.length<2||!d.values.every(iso)))throw Error('Ogiltiga datumalternativ');
  if(d.precision==='circa'&&!iso(d.value))throw Error('Ogiltigt ungefärligt datum');
}

function validatePayload(db,m) {
  if(!payloadKinds.has(m.kind)||!m.data||Array.isArray(m.data))throw Error(`Okänd objekttyp: ${m.kind}`);
  const columns=db.prepare(`PRAGMA table_info(${m.kind})`).all().filter(c=>c.name!=='revision_id');
  for(const k of Object.keys(m.data))if(!columns.some(c=>c.name===k))throw Error(`Okänt fält ${m.kind}.${k}`);
  for(const c of columns)if(c.notnull&&(m.data[c.name]===undefined||m.data[c.name]===null))throw Error(`Fält saknas: ${m.kind}.${c.name}`);
  for(const [key,kind] of Object.entries(references[m.kind]??{})) {
    const id=m.data[key]; if(id==null)continue;
    const actual=db.prepare('SELECT kind FROM object WHERE id=?').get(id)?.kind;
    if(!actual||(kind!=='*'&&actual!==kind))throw Error(`Fel referens ${key}: ${id} (kräver ${kind})`);
  }
  if(m.data.date_json)validateDate(m.data.date_json);
  if(m.kind==='event'&&!['birth','baptism','confirmation','banns','marriage','divorce','death','burial','registered_arrival','registered_departure','residence','other'].includes(m.data.event_type))throw Error(`Okänd händelsetyp: ${m.id}/${m.data.event_type}`);
  if(m.kind==='relation'&&!['parent','spouse','partner','foster_parent','guardian','employer','sibling','other'].includes(m.data.relation_type))throw Error('Okänd relationstyp');
  if(m.kind==='fact') {
    const value=m.data.value_json;
    const types={text:'string',number:'number',boolean:'boolean',entity:'string'};
    if(types[m.data.value_type]&&typeof value!==types[m.data.value_type])throw Error('Fel värdetyp för sakuppgift');
    if(m.data.value_type==='number'&&!Number.isFinite(value))throw Error('Ogiltigt numeriskt värde');
    if(m.data.value_type==='structured'&&(!value||typeof value!=='object'))throw Error('Strukturerat värde kräver objekt eller lista');
  }
  if(m.kind==='fact'&&m.data.value_type==='date')validateDate(m.data.value_json);
  if(m.kind==='fact'&&m.data.value_type==='entity'&&!head(db,m.data.value_json))throw Error('Okänd entitetsreferens');
  if(m.kind==='identity'&&m.data.decision!==m.disposition)throw Error('Identitetsbeslut och disposition skiljer sig');
  if(m.kind==='search') {
    const s=m.data.scope_json;
    if(!s||typeof s!=='object'||!s.description||!s.query)throw Error('Sökning kräver omfång och sökfråga');
    if(m.data.outcome==='negative'&&(!s.bounds||typeof s.bounds!=='object'||Array.isArray(s.bounds)||!Object.keys(s.bounds).length))throw Error('Noll kräver uttryckliga sökgränser');
  }
  return columns;
}

export function applyOperation(db,request,{legacy=false,recordedAt=new Date().toISOString()}={}) {
  if(!request.id||!request.actor||!request.reason||!Array.isArray(request.changes))throw Error('Operation kräver id, actor, reason och changes');
  if(request.changes.length===0&&!request.resolve?.length&&!request.mappings?.length&&!request.unitDecisions?.length)throw Error('Tom operation');
  const requestHash=sha(canonical(request));
  return transaction(db,()=> {
    const previous=db.prepare('SELECT request_hash FROM operation WHERE id=?').get(request.id);
    if(previous) {
      if(previous.request_hash!==requestHash)throw Error('Operations-id har redan använts med annat innehåll');
      return {unchanged:true,operation:request.id};
    }
    if(!/^\d{4}-\d\d-\d\dT/.test(recordedAt)||Number.isNaN(Date.parse(recordedAt)))throw Error('Ogiltig operationstid');
    db.prepare('INSERT INTO operation VALUES (?,?,?,?,?)').run(request.id,requestHash,request.actor,recordedAt,request.reason);
    db.prepare('INSERT INTO operation_payload(operation_id,policy,request_json) VALUES (?,?,?)').run(request.id,legacy?'legacy/1':'native/2',canonical(request));
    for(const a of request.media??[]) {
      if(!a.id||!/^[a-f0-9]{64}$/.test(a.sha256)||a.storagePath!==`genealogy2/media/objects/${a.sha256}`||!Number.isSafeInteger(a.bytes)||a.bytes<0||!a.originalName||!a.provenance?.trim())throw Error('Media kräver hash, lagringsplats, storlek och provenans');
      db.prepare('INSERT INTO native_asset VALUES (?,?,?,?,?,?,?)').run(a.id,a.storagePath,a.sha256,a.bytes,a.originalName,a.provenance,request.id);
    }
    for(const s of request.spans??[]) {
      const doc=db.prepare('SELECT * FROM document WHERE path=?').get(s.path);
      if(!doc||doc.sha256!==s.sha256||!Number.isInteger(s.start)||!Number.isInteger(s.end)||s.start<0||s.end>doc.bytes||s.end<=s.start)throw Error('Ogiltigt ursprungsspann');
      const bytes=Buffer.from(doc.text),raw=bytes.subarray(s.start,s.end).toString();
      if(Buffer.byteLength(raw)!==s.end-s.start)throw Error('Textspann bryter UTF-8');
      const id=sha(`${s.path}\0${s.sha256}\0curated_span\0${s.start}\0${s.end}`);
      if(id!==s.id)throw Error('Fel span-id');
      if(!db.prepare('SELECT id FROM unit WHERE id=?').get(id)) {
        db.prepare('INSERT INTO unit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)').run(id,s.path,'curated_span',null,s.owner??null,s.section??'',s.start,s.end,
          bytes.subarray(0,s.start).toString().split('\n').length,bytes.subarray(0,s.end).toString().replace(/\n$/,'').split('\n').length,
          raw,JSON.stringify({extractor:'curation-span/1',operation:request.id}),0);
      }
    }
    const changed=[],seen=new Set();
    for(const m of request.changes) {
      if(!m.id||seen.has(m.id))throw Error('Saknat eller upprepat objekt-id i operationen');seen.add(m.id);
      if(!m.rationale?.trim())throw Error(`Motivering krävs: ${m.id}`);
      const current=head(db,m.id);
      if((current?.version??null)!==m.expectedVersion)throw Error(`Versionskonflikt: ${m.id}; aktuell ${current?.version??'ny'}`);
      if(current?.kind&&current.kind!==m.kind)throw Error('Objekttyp får inte ändras');
      if(current?.evidence_status==='OWNER_CONFIRMED'&&m.evidenceStatus!=='OWNER_CONFIRMED')throw Error('Ägarkunskap får inte tyst nedgraderas; registrera konflikten separat');
      if(current?.evidence_status==='OWNER_CONFIRMED') {
        const old=db.prepare(`SELECT * FROM ${current.kind} WHERE revision_id=?`).get(current.id);
        for(const [key,value] of Object.entries(m.data)) {
          if((key.endsWith('_json')?canonical(value):value)!==old[key])throw Error('Ägarkunskap får inte ändras utan ett nytt uttryckligt ägarbeslut; registrera konflikten separat');
        }
      }
      if(!current) {
        if(db.prepare("SELECT id FROM legacy_mapping WHERE legacy_id=? AND mapping_type='same_identity'").get(m.id))throw Error('Person-id är redan ett dubblettalias');
        db.prepare('INSERT INTO object VALUES (?,?)').run(m.id,m.kind);
      }
      const columns=validatePayload(db,m);
      const version=(current?.version??0)+1,id=`${m.id}@${version}`;
      const origins=m.origins??[],evidence=m.evidence??[];
      const hasBoundReference=!legacy&&(boundReferences[m.kind]??[]).some(field=>m.data[field]!=null);
      if(!origins.length&&!evidence.length&&!hasBoundReference&&!['source','record','place','question','narrative'].includes(m.kind))throw Error(`Ursprung eller belägg krävs: ${m.id}`);
      db.prepare('INSERT INTO revision VALUES (?,?,?,?,?,?,?,?,?)').run(id,m.id,version,request.id,m.disposition,m.evidenceStatus??null,m.rationale,m.caveat??'',current?.id??null);
      db.prepare(`INSERT INTO ${m.kind} (revision_id,${columns.map(c=>c.name).join(',')}) VALUES (?,${columns.map(()=>'?').join(',')})`).run(id,...columns.map(c=>{
        const v=m.data[c.name]??null;return v!==null&&c.name.endsWith('_json')?canonical(v):v;
      }));
      for(const o of origins)db.prepare('INSERT INTO origin VALUES (?,?,?,?)').run(id,o.unit,o.coverage??'partial',o.note??'');
      for(const e of evidence) {
        const basis=head(db,e.object);
        if(!basis||basis.version!==e.version)throw Error(`Beläggsversion saknas eller är inaktuell: ${e.object}@${e.version}`);
        db.prepare('INSERT INTO dependency VALUES (?,?,?,?)').run(id,basis.id,e.role,e.note??'');
      }
      if(!legacy)for(const field of boundReferences[m.kind]??[]) {
        const target=m.data[field];if(target==null)continue;
        const basis=head(db,target);
        const explicit=evidence.find(e=>e.object===target);
        const expected=explicit?.version??m.bindings?.[target]??(seen.has(target)?basis.version:undefined);
        if(expected!==basis.version)throw Error(`Versionsbundet underlag krävs: ${m.id}.${field} → ${target}@${basis.version}`);
        if(!explicit)db.prepare('INSERT INTO dependency VALUES (?,?,?,?)').run(id,basis.id,'derived_from',`Versionsbunden strukturreferens: ${field}`);
      }
      for(const a of m.assets??[]) {
        if(m.kind!=='record')throw Error('Media kopplas till en källpost');
        db.prepare('INSERT INTO record_asset VALUES (?,?,?)').run(id,a.path,a.region??'helbild');
      }
      for(const a of m.media??[]) {
        if(m.kind!=='record')throw Error('Media kopplas till en källpost');
        db.prepare('INSERT INTO record_media VALUES (?,?,?)').run(id,a.id,a.region??'helbild');
      }
      indexObject(db,m.id);
      if(current)changed.push({before:current.id,after:id});
    }
    for(const mapping of request.mappings??[]) {
      if(!mapping.rationale?.trim()||head(db,mapping.target)?.kind!=='person')throw Error('Importidentitet kräver person och motivering');
      if(mapping.type==='same_identity'&&head(db,mapping.legacyId))throw Error('En dubblett ska vara alias, inte en andra person');
      if(mapping.type==='same_identity'&&db.prepare("SELECT id FROM legacy_mapping WHERE legacy_id=? AND mapping_type='same_identity'").get(mapping.legacyId))throw Error('Dubblettalias har redan ett beslutat mål');
      db.prepare('INSERT INTO legacy_mapping VALUES (?,?,?,?,?,?,?,?)').run(mapping.id,'person',mapping.legacyId,mapping.target,request.id,mapping.type,mapping.unit,mapping.rationale);
    }
    const decided=new Set();
    for(const d of request.unitDecisions??[]) {
      if(decided.has(d.unit)||!d.rationale?.trim())throw Error('Konverteringsbeslut kräver entydig enhet och motivering');decided.add(d.unit);
      const previous=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(d.unit);
      if((previous?.version??null)!==d.expectedVersion)throw Error(`Versionskonflikt för textenhet: ${d.unit}`);
      const version=(previous?.version??0)+1;
      db.prepare('INSERT INTO unit_decision VALUES (?,?,?,?,?,?,?,?,?)').run(`UD-${d.unit}@${version}`,d.unit,version,request.id,d.state,d.target??null,d.rationale,d.question??'',previous?.id??null);
      if(d.targets!==undefined) {
        if(!Array.isArray(d.targets)||new Set(d.targets).size!==d.targets.length||d.targets.some(t=>typeof t!=='string'))throw Error('Konverteringsmål kräver en entydig lista');
        if(d.target!=null&&!d.targets.includes(d.target))throw Error('Första konverteringsmålet saknas i mållistan');
        for(const target of d.targets)db.prepare('INSERT INTO unit_decision_target VALUES (?,?)').run(`UD-${d.unit}@${version}`,target);
      }
    }
    // Follow evidence dependencies transitively. Changing an observation never silently rewrites conclusions.
    for(const c of changed) {
      const affected=db.prepare(`WITH RECURSIVE dependents(id) AS (
        SELECT revision_id FROM dependency WHERE basis_revision_id=?
        UNION SELECT d.revision_id FROM dependency d JOIN dependents p ON d.basis_revision_id=p.id
      ) SELECT DISTINCT current.id FROM dependents d JOIN revision old ON old.id=d.id
        JOIN current_revision current ON current.object_id=old.object_id
        WHERE current.operation_id!=?`).all(c.before,request.id);
      for(const r of affected)db.prepare('INSERT INTO review_request VALUES (?,?,?,?,?)').run(sha(`${request.id}:${r.id}:${c.after}`),request.id,r.id,c.after,'Ett åberopat underlag har fått en ny version. Tidigare slutsats bevaras tills omprövningen dokumenterats.');
    }
    for(const resolution of request.resolve??[]) {
      if(!resolution.rationale?.trim())throw Error('Omprövningen kräver motivering');
      if(!db.prepare('SELECT id FROM pending_review WHERE id=?').get(resolution.request))throw Error('Omprövningen saknas eller är redan stängd');
      db.prepare('INSERT INTO review_resolution VALUES (?,?,?)').run(resolution.request,request.id,resolution.rationale);
    }
    const conflicting=db.prepare(`SELECT i.mention_id FROM current_revision r JOIN identity i ON i.revision_id=r.id
      WHERE r.disposition='accepted' GROUP BY i.mention_id HAVING count(DISTINCT i.person_id)>1`).all();
    if(conflicting.length)throw Error('Samma omnämnande har två accepterade personidentiteter');
    if(!legacy&&db.prepare(`SELECT 1 FROM dependency d JOIN revision r ON r.id=d.revision_id
      JOIN revision basis ON basis.id=d.basis_revision_id JOIN current_revision current ON current.object_id=basis.object_id
      WHERE r.operation_id=? AND current.id!=basis.id LIMIT 1`).get(request.id))throw Error('Belägg blev inaktuellt inom operationen; lägg rättelsen före beroende slutsatser');
    return {unchanged:false,operation:request.id,changes:request.changes.length,pendingReviews:db.prepare('SELECT count(*) n FROM pending_review').get().n};
  });
}

export function domainStatus(db) {
  return {objects:db.prepare('SELECT kind,count(*) n FROM object GROUP BY kind ORDER BY kind').all(),
    pendingReviews:db.prepare('SELECT count(*) n FROM pending_review').get().n,
    mappedUnits:db.prepare("SELECT coverage,count(DISTINCT unit_id) n FROM origin GROUP BY coverage").all()};
}

export function verifyDomain(db) {
  const errors=[];
  for(const p of db.prepare('SELECT p.*,o.request_hash FROM operation_payload p JOIN operation o ON o.id=p.operation_id').all()) {
    if(sha(canonical(JSON.parse(p.request_json)))!==p.request_hash)errors.push(`Operationshash: ${p.operation_id}`);
  }
  for(const d of db.prepare('SELECT * FROM unit_decision').all()) {
    const previous=d.previous_id?db.prepare('SELECT unit_id,version FROM unit_decision WHERE id=?').get(d.previous_id):null;
    if(d.version===1?d.previous_id!==null:!previous||previous.unit_id!==d.unit_id||previous.version!==d.version-1)errors.push(`Bruten konverteringskedja: ${d.id}`);
  }
  for(const r of db.prepare('SELECT r.*,o.kind FROM revision r JOIN object o ON o.id=r.object_id').iterate()) {
    const payload=db.prepare(`SELECT * FROM ${r.kind} WHERE revision_id=?`).get(r.id);
    if(!payload) {errors.push(`Innehåll saknas: ${r.id}`);continue;}
    delete payload.revision_id;
    for(const key of Object.keys(payload))if(key.endsWith('_json')&&payload[key]!==null)payload[key]=JSON.parse(payload[key]);
    try{validatePayload(db,{kind:r.kind,data:payload,disposition:r.disposition});}catch(e){errors.push(`${r.id}: ${e.message}`);}
    const previous=r.previous_id?db.prepare('SELECT object_id,version FROM revision WHERE id=?').get(r.previous_id):null;
    if(r.version===1?r.previous_id!==null:!previous||previous.object_id!==r.object_id||previous.version!==r.version-1)errors.push(`Bruten versionskedja: ${r.id}`);
  }
  return errors;
}

// One reader owns revision metadata. Projections select object IDs only; joining
// two objects must never replace one object's qualifications with the other's.
export function readCurrent(db,id) {
  const r=head(db,id);if(!r)return null;
  const data=db.prepare(`SELECT * FROM ${r.kind} WHERE revision_id=?`).get(r.id);
  return {...data,object_id:r.object_id,revision_id:r.id,version:r.version,kind:r.kind,
    disposition:r.disposition,evidence_status:r.evidence_status,rationale:r.rationale,caveat:r.caveat,
    ...(r.kind==='record'?{media:[
      ...db.prepare("SELECT a.path,a.sha256,a.bytes,ra.region,'legacy' AS origin FROM record_asset ra JOIN asset a ON a.path=ra.asset_path WHERE ra.revision_id=? ORDER BY a.path").all(r.id),
      ...db.prepare("SELECT a.storage_path AS path,a.sha256,a.bytes,ra.region,'native' AS origin,a.provenance,a.original_name FROM record_media ra JOIN native_asset a ON a.id=ra.asset_id WHERE ra.revision_id=? ORDER BY a.id").all(r.id)],
      readings:db.prepare("SELECT r.object_id FROM current_revision r JOIN assessment a ON a.revision_id=r.id WHERE a.subject_id=? AND a.criteria='legacy_record_boundary' ORDER BY r.object_id").all(id).map(x=>readCurrent(db,x.object_id))}:{}),
    origins:db.prepare(`SELECT o.*,u.document_path,u.start_line,u.end_line FROM origin o JOIN unit u ON u.id=o.unit_id WHERE o.revision_id=? ORDER BY u.document_path,u.start_line,u.end_line,u.id`).all(r.id),
    evidence:db.prepare('SELECT * FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role').all(r.id),
    pending_reviews:db.prepare(`SELECT q.* FROM pending_review q JOIN revision r ON r.id=q.affected_revision_id WHERE r.object_id=? ORDER BY q.id`).all(id)};
}

export function researchOutcome(raw) {
  const cleaned=String(raw??'').trim().replace(/[`*]/g,'').replace(/[.。]+$/,'').trim();
  return ({'ÖPPEN':'open','PÅGÅR':'in_progress','FASTSTÄLLD':'established','AVVISAD':'rejected','OLÖST':'unresolved','OMSTRIDD':'disputed','STYRKT':'supported','EJ STYRKT':'not_supported','GODKÄND':'passed','UNDERKÄND':'failed','GENOMGÅNGET':'reviewed','AVGRÄNSAT':'bounded','INTEGRITETSMINIMERAT':'privacy_bounded'})[cleaned]??null;
}

export function personView(db,id) {
  const current=head(db,id);
  const raw=db.prepare("SELECT e.kind,e.document_path,e.title FROM legacy_entity e WHERE e.id=? ORDER BY e.kind,e.document_path").all(id);
  const person=current?.kind==='person'?readCurrent(db,id):null;
  const select=(kind,condition,...args)=>db.prepare(`SELECT r.object_id FROM current_revision r JOIN ${kind} x ON x.revision_id=r.id WHERE ${condition} ORDER BY r.object_id`).all(...args).map(r=>readCurrent(db,r.object_id));
  const linked=`EXISTS(SELECT 1 FROM origin origin JOIN unit u ON u.id=origin.unit_id WHERE origin.revision_id=r.id AND u.owner_id=?) OR EXISTS(SELECT 1 FROM current_unit_target t JOIN unit u ON u.id=t.unit_id WHERE t.target_id=r.object_id AND u.owner_id=?)`;
  const importAssessment=person?null:readCurrent(db,`IMPORT-${id}`);
  const researchSubject=importAssessment?.kind==='assessment'?importAssessment.object_id:id;
  const assessments=select('assessment','x.subject_id=?',researchSubject),questions=select('question','x.subject_id=?',researchSubject);
  const research={questions:questions.map(q=>({...q,outcome_code:researchOutcome(q.outcome),active:q.disposition!=='retired'})),
    themes:assessments.filter(a=>a.criteria.startsWith('legacy_theme/')),
    requirements:assessments.filter(a=>a.criteria.startsWith('legacy_person_contract/')),
    paths:assessments.filter(a=>a.criteria==='legacy_source_path'),
    keys:assessments.filter(a=>a.criteria==='legacy_search_key'),
    reviews:assessments.filter(a=>!/^legacy_(theme\/|person_contract\/|source_path$|search_key$)/.test(a.criteria))};
  const conversion=db.prepare(`SELECT d.state,count(*) n FROM current_unit_decision d JOIN unit u ON u.id=d.unit_id WHERE u.owner_id=? GROUP BY d.state ORDER BY d.state`).all(id);
  const facts=select('fact',`x.subject_id=? OR x.subject_id IN (SELECT i.mention_id FROM current_revision ir JOIN identity i ON i.revision_id=ir.id WHERE i.person_id=? AND i.decision='accepted')`,id,id);
  const relations=select('relation','x.from_person=? OR x.to_person=?',id,id).map(relation=>({...relation,
    qualifications:select('fact','x.subject_id=?',relation.object_id)}));
  const events=select('participation','x.person_id=?',id).map(participation=>({
    ...readCurrent(db,participation.event_id),event_id:participation.event_id,participation,
    qualifications:select('fact','x.subject_id=?',participation.event_id)}));
  // Reuse links give context without changing a fact's subject or duplicating
  // facts already shown on the person's own objects.
  const visibleFacts=new Set([...facts,...relations.flatMap(r=>r.qualifications),...events.flatMap(e=>e.qualifications)].map(f=>f.object_id));
  const contextFacts=select('fact',linked,id,id).filter(f=>!visibleFacts.has(f.object_id));
  return {id,person,legacy:raw,research,conversion,
    interpretationQuestions:db.prepare(`SELECT d.unit_id,d.question,d.rationale,u.document_path,u.start_line,u.end_line FROM current_unit_decision d JOIN unit u ON u.id=d.unit_id WHERE u.owner_id=? AND d.state='pending_interpretation' ORDER BY u.document_path,u.start_line,u.end_line,u.id`).all(id),
    observations:select('observation',`(${linked}) OR x.mention_id IN (SELECT i.mention_id FROM current_revision ir JOIN identity i ON i.revision_id=ir.id WHERE i.person_id=? AND i.decision='accepted')`,id,id,id),
    mentions:select('mention',`(${linked}) OR r.object_id IN (SELECT i.mention_id FROM current_revision ir JOIN identity i ON i.revision_id=ir.id WHERE i.person_id=? AND i.decision='accepted')`,id,id,id),
    searches:select('search',`(${linked}) OR x.question_id IN (SELECT qr.object_id FROM current_revision qr JOIN question q ON q.revision_id=qr.id WHERE q.subject_id=?)`,id,id,id),
    importAssessments:person?[]:select('assessment','r.object_id=?',`IMPORT-${id}`),
    identityMappings:db.prepare('SELECT * FROM legacy_mapping WHERE legacy_id=? OR target_id=? ORDER BY id').all(id,id),
    identities:select('identity','x.person_id=?',id),
    identityResolutions:select('identity_resolution','x.person_a=? OR x.person_b=?',id,id),
    facts,contextFacts,relations,events,
    questions,assessments,
    narratives:select('narrative','x.subject_id=?',researchSubject),
    remaining:db.prepare(`SELECT u.kind,count(*) n FROM unit u WHERE u.owner_id=? AND NOT EXISTS (
      SELECT 1 FROM origin o JOIN current_revision r ON r.id=o.revision_id WHERE o.unit_id=u.id AND o.coverage='complete') AND NOT EXISTS(SELECT 1 FROM current_unit_decision d WHERE d.unit_id=u.id AND d.state IN ('mapped_complete','preserved_history')) GROUP BY u.kind ORDER BY u.kind`).all(id),
    note:'Typade uppgifter ovan är ett avgränsat urval. Kvarvarande underlag nås med show; frånvaro här betyder inte frånvaro i forskningen.'};
}

export function inspect(db,id) {
  const current=head(db,id);
  if(!current) {
    const entities=db.prepare('SELECT document_path FROM legacy_entity WHERE id=?').all(id);
    const units=db.prepare('SELECT * FROM unit WHERE legacy_id=?').all(id);
    const ids=new Set(units.map(u=>u.id));
    for(const e of entities)for(const u of db.prepare('SELECT id FROM unit WHERE document_path=?').all(e.document_path))ids.add(u.id);
    const decisions=[],objects=new Set();
    for(const unit of ids) {
      const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(unit);if(d){d.targets=db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=? ORDER BY target_id').all(unit).map(t=>t.target_id);decisions.push(d);for(const target of d.targets)objects.add(target);}
      for(const r of db.prepare('SELECT DISTINCT r.object_id FROM origin o JOIN current_revision r ON r.id=o.revision_id WHERE o.unit_id=?').all(unit))objects.add(r.object_id);
    }
    for(const object of [...objects]) {
      const r=readCurrent(db,object);
      const target=r?.kind==='transcription'?r.record_id:r?.kind==='assessment'?r.subject_id:null;
      if(target&&head(db,target)?.kind==='record')objects.add(target);
    }
    return {legacyUnits:units,conversionDecisions:decisions,representations:[...objects].sort().map(x=>readCurrent(db,x))};
  }
  const revisions=db.prepare('SELECT * FROM revision WHERE object_id=? ORDER BY version').all(id);
  return {object:id,kind:current.kind,currentVersion:current.version,current:readCurrent(db,id),conversionOrigins:db.prepare(`SELECT d.id,d.state,d.rationale,d.question,u.document_path,u.start_line,u.end_line FROM current_unit_target t JOIN current_unit_decision d ON d.id=t.decision_id JOIN unit u ON u.id=t.unit_id WHERE t.target_id=? ORDER BY u.document_path,u.start_line`).all(id),revisions:revisions.map(r=>({...r,
    data:db.prepare(`SELECT * FROM ${current.kind} WHERE revision_id=?`).get(r.id),
    origins:db.prepare(`SELECT o.coverage,o.note,u.*,d.sha256 FROM origin o JOIN unit u ON u.id=o.unit_id JOIN document d ON d.path=u.document_path WHERE o.revision_id=?`).all(r.id),
    evidence:db.prepare('SELECT * FROM dependency WHERE revision_id=?').all(r.id),
    assets:current.kind==='record'?db.prepare('SELECT a.*,ra.region FROM record_asset ra JOIN asset a ON a.path=ra.asset_path WHERE ra.revision_id=?').all(r.id):[]
    ,nativeAssets:current.kind==='record'?db.prepare('SELECT a.*,ra.region FROM record_media ra JOIN native_asset a ON a.id=ra.asset_id WHERE ra.revision_id=?').all(r.id):[]
  }))};
}
