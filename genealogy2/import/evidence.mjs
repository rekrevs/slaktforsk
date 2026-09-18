import fs from 'node:fs';
import {sha,canonical} from '../lib/archive.mjs';
import {head} from '../lib/domain.mjs';

export function buildEvidence(db,reviews,{group='evidence-01',cohorts=JSON.parse(fs.readFileSync(new URL('../migration/cohorts.json',import.meta.url),'utf8'))}={}) {
  const scope=cohorts.groups.find(g=>g.id===group);
  if(!scope||db.prepare('SELECT id FROM import_batch').get()?.id!==cohorts.baseline)throw Error('Fel evidensgrupp eller importbas');
  if(canonical(reviews.map(r=>r.citation).sort())!==canonical([...scope.citations].sort()))throw Error('Granskningen måste omfatta varje citation exakt en gång');
  const request={id:`T-${String(646+Number(group.split('-')[1])-1).padStart(4,'0')}/${group}-v1`,actor:'Codex/evidence-conversion',
    reason:'Avgränsade källposter och bevarade avskrifter ur tidigare forskning. Alla textenheter får ett motiverat representationsbeslut; osäkerhet och rättelser bevaras.',spans:[],changes:[],unitDecisions:[]};
  const documents=new Map(),records=new Map(),transcriptions=new Map(),readings=new Map(),decisions=new Map();
  const read=(id,kind)=> {
    const row=db.prepare('SELECT d.*,e.id AS legacy_id FROM legacy_entity e JOIN document d ON d.path=e.document_path WHERE e.id=? AND e.kind=?').get(id,kind);
    if(!row)throw Error(`Saknat underlag: ${id}/${kind}`);documents.set(row.path,row);return row;
  };
  const span=(d,range)=> {
    const lines=d.text.split(/(?<=\n)/);
    const from=range?.startLine??1,to=range?.endLine??lines.length;
    if(!Number.isInteger(from)||!Number.isInteger(to)||from<1||to<from||to>lines.length)throw Error(`Fel granskningsspann: ${d.path}:${from}–${to}`);
    const start=Buffer.byteLength(lines.slice(0,from-1).join('')),raw=lines.slice(from-1,to).join(''),end=start+Buffer.byteLength(raw);
    const id=sha(`${d.path}\0${d.sha256}\0curated_span\0${start}\0${end}`);
    if(!request.spans.some(s=>s.id===id))request.spans.push({id,path:d.path,sha256:d.sha256,start,end,owner:d.legacy_id,section:`Källpost/avskrift ${from}–${to}`});
    return {id,document_path:d.path,start_byte:start,end_byte:end,start_line:from,end_line:to,raw,kind:'curated_span',historical:0};
  };
  const origin=(u,coverage='partial')=>({unit:u.id,coverage,note:'Samma tidigare forskningsunderlag; ingen ny oberoende evidensröst.'});
  const mergeOrigins=(to,from)=>{for(const x of from)if(!to.some(o=>o.unit===x.unit))to.push(x);};
  const uniqueOrigins=items=>{const out=[];mergeOrigins(out,items);return out;};
  for(const review of [...reviews].sort((a,b)=>a.citation.localeCompare(b.citation))) {
    const d=read(review.citation,'citation');
    if(d.path!==review.path||d.sha256!==review.sha256||!Array.isArray(review.records)||!Array.isArray(review.pending)||!review.readingNote?.trim()||!['bounded_records','preserved_text'].includes(review.disposition))throw Error(`Ofullständig eller inaktuell granskning: ${review.citation}`);
    if(review.disposition==='bounded_records'&&!review.records.length)throw Error(`Avgränsad citation saknar poster: ${review.citation}`);
    for(const p of review.pending) {if(!p.question?.trim())throw Error('Tom tolkningsfråga');span(d,p);}
    const full=span(d),typed=[];
    for(const r of review.records) {
      if(!r.key||!r.locator?.trim()||!r.type?.trim()||!r.dependence?.trim()||!Array.isArray(r.evidence)||!r.evidence.length||!Array.isArray(r.transcriptions))throw Error(`Ofullständig postavgränsning: ${review.citation}`);
      const source=head(db,r.source);if(source?.kind!=='source')throw Error(`Källpost saknar källbeskrivning: ${r.source}`);
      const recordId=r.reuse??`R-${sha(r.key).slice(0,24)}`;
      const caveat=[r.caveat,`${review.citation}: ${review.readingNote}`].filter(Boolean).join('\n');
      const data={source_id:r.source,record_type:r.type,locator:r.locator,dependence_note:r.dependence};
      const evidenceSpans=r.evidence.map(e=>span(d,e));
      const existing=head(db,recordId);
      if(r.reuse) {
        if(existing?.kind!=='record'||db.prepare('SELECT source_id FROM record WHERE revision_id=?').get(existing.id)?.source_id!==r.source)throw Error(`Återbrukad post saknas eller har annan källa: ${recordId}`);
      }else if(existing&&existing.operation_id!==request.id) {
        const old=db.prepare('SELECT * FROM record WHERE revision_id=?').get(existing.id);
        if(existing.kind!=='record'||old.source_id!==r.source||old.locator!==r.locator||old.record_type!==r.type)throw Error(`Postnyckel kräver manuell jämförelse: ${r.key}`);
      }else if(records.has(recordId)) {
        const earlier=records.get(recordId);
        if(earlier.data.source_id!==data.source_id||earlier.data.locator!==data.locator||earlier.data.record_type!==data.record_type)throw Error(`Motstridiga avgränsningar för samma postnyckel: ${r.key}`);
        mergeOrigins(earlier.origins,[...evidenceSpans.map(u=>origin(u)),origin(full,'context')]);
        if(!earlier.caveat.includes(caveat))earlier.caveat+='\n'+caveat;
        if(!earlier.data.dependence_note.includes(r.dependence))earlier.data.dependence_note+='\n'+r.dependence;
        for(const a of r.assets??[])if(!earlier.assets.some(x=>x.path===a.path))earlier.assets.push(a);
      }else {
        records.set(recordId,{id:recordId,kind:'record',expectedVersion:null,disposition:'recorded',data,bindings:{[r.source]:source.version},
          rationale:`Källpost avgränsad i ${review.citation}. ${r.dependence}`,caveat,
          origins:uniqueOrigins([...evidenceSpans.map(u=>origin(u)),origin(full,'context')]),assets:r.assets??[]});
      }
      for(const a of r.assets??[])if(!db.prepare('SELECT path FROM asset WHERE path=?').get(a.path))throw Error(`Medielänk saknas i den bevarade basen: ${a.path}`);
      // A reused record is not revised by this importer. A new attachment
      // must go through the ordinary versioned write path before reuse;
      // silently validating and then discarding it loses the media link.
      if(existing&&existing.operation_id!==request.id)for(const a of r.assets??[]) {
        if(!db.prepare('SELECT 1 FROM record_asset WHERE revision_id=? AND asset_path=?').get(existing.id,a.path))throw Error(`Medielänk till återbrukad post kräver ny version: ${recordId} → ${a.path}`);
      }
      // A later citation can qualify an existing record without supplying a new
      // transcription. Keep that reading attached to the shared record too.
      const readingId=`READ-${sha(`${review.citation}:${recordId}`).slice(0,24)}`;
      readings.set(readingId,{id:readingId,kind:'assessment',expectedVersion:null,disposition:'recorded',
        data:{subject_id:recordId,criteria:'legacy_record_boundary',outcome:'record_located',body:`${review.citation}: ${review.readingNote}\n${r.dependence}`},
        rationale:`Dokumenterad avgränsning och läshistorik i ${review.citation}; ingen ny oberoende evidensröst.`,caveat:r.caveat??'',
        evidence:[{object:recordId,version:existing?.version??1,role:'derived_from',note:'Avser denna version av den återbrukade källposten.'}],
        origins:uniqueOrigins([...evidenceSpans.map(u=>origin(u)),origin(full,'context')])});
      for(const range of r.transcriptions) {
        const u=span(d,range),id=`TR-${sha(`${recordId}:${u.id}`).slice(0,24)}`;
        const before=head(db,id);
        if(before&&before.operation_id!==request.id)throw Error(`Oväntad befintlig avskrift: ${id}`);
        if(transcriptions.has(id))continue;
        transcriptions.set(id,{id,kind:'transcription',expectedVersion:null,disposition:'recorded',
          data:{record_id:recordId,text:u.raw,reading_note:review.readingNote+(r.caveat?'\n'+r.caveat:'')},
          bindings:{[recordId]:existing?.version??1},rationale:`Ordagrant bevarad äldre avskrift/sammanfattning ur ${review.citation}; ingen ny originalavläsning.`,
          caveat:r.caveat??'',origins:[origin(u,'complete'),...(u.id===full.id?[]:[origin(full,'context')])]});
        typed.push({span:u,target:id});
      }
    }
    const units=db.prepare('SELECT * FROM unit WHERE document_path=?').all(d.path);
    for(const s of request.spans.filter(s=>s.path===d.path))if(!units.some(u=>u.id===s.id))units.push({id:s.id,document_path:s.path,start_byte:s.start,end_byte:s.end,start_line:Buffer.from(d.text).subarray(0,s.start).toString().split('\n').length,end_line:Buffer.from(d.text).subarray(0,s.end).toString().replace(/\n$/,'').split('\n').length,historical:0});
    for(const u of units) {
      const pending=review.pending.filter(p=>p.startLine<=u.end_line&&p.endLine>=u.start_line);
      const representation=typed.find(t=>t.span.start_byte<=u.start_byte&&t.span.end_byte>=u.end_byte);
      const state=u.historical?'preserved_history':pending.length?'pending_interpretation':representation?'mapped_complete':'preserved_text';
      decisions.set(u.id,{unit:u.id,expectedVersion:null,state,target:representation?.target??null,
        rationale:`${review.citation}: ${state==='mapped_complete'?'Hela enheten återges ordagrant i avskriften; inte ett godkännande av uppgifterna.':state==='preserved_history'?'Historisk text bevaras; används inte som aktuell personslutsats.':'Texten finns kvar i den fullständiga frysta citationen.'} ${review.readingNote}`,
        question:pending.map(p=>p.question).join('\n')});
    }
  }
  for(const id of scope.sources) {
    const d=read(id,'source');
    const source=head(db,id);if(source?.kind!=='source')throw Error(`Saknat källregister: ${id}`);
    for(const u of db.prepare('SELECT id FROM unit WHERE document_path=?').all(d.path))decisions.set(u.id,{unit:u.id,expectedVersion:null,state:'mapped_complete',target:id,
      rationale:'Hela äldre källbeskrivningen inklusive metadata och senare tillägg finns ordagrant i source.description. Arkivfält och källklass är inte därmed normaliserade.',question:''});
  }
  request.changes=[...records.values(),...transcriptions.values(),...readings.values()];
  request.unitDecisions=[...decisions.values()].sort((a,b)=>a.unit.localeCompare(b.unit));
  return request;
}
