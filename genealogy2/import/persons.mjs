import fs from 'node:fs';
import {sha,canonical} from '../lib/archive.mjs';
import {head,readCurrent} from '../lib/domain.mjs';

const states=new Set(['mapped_complete','preserved_text','preserved_history','pending_interpretation']);
const structural={record:['source_id'],transcription:['record_id'],mention:['record_id'],observation:['record_id','mention_id'],identity:['mention_id','person_id'],identity_resolution:['person_a','person_b'],place:['parent_id'],event:['place_id'],participation:['event_id','person_id','mention_id'],relation:['from_person','to_person'],fact:['subject_id'],question:['subject_id'],search:['question_id','source_id'],assessment:['subject_id'],narrative:['subject_id']};
const uniqueOrigins=items=>[...new Map(items.map(o=>[o.unit,o])).values()];
const combineText=(a,b)=>a===b||!b?a:!a?b:a+'\n'+b;

export function buildPersons(db,reviews,{group='persons-01',cohorts=JSON.parse(fs.readFileSync(new URL('../migration/cohorts.json',import.meta.url),'utf8'))}={}) {
  const scope=cohorts.groups.find(g=>g.id===group);
  if(!scope||db.prepare('SELECT id FROM import_batch').get()?.id!==cohorts.baseline)throw Error('Fel persongrupp eller importbas');
  if(canonical(reviews.map(r=>r.person).sort())!==canonical([...scope.persons].sort()))throw Error('Granskningen måste omfatta varje person exakt en gång');
  const request={id:`T-${String(651+Number(group.split('-')[1])).padStart(4,'0')}/${group}-v1`,actor:'Codex/person-conversion',reason:'Sakgranskad överföring av befintlig personkunskap och forskningsbedömningar. Ingen ny forskning eller automatisk kontraktsuppgradering.',spans:[],changes:[],unitDecisions:[]};
  const docs=new Map(),newSpans=new Map(),changes=new Map(),links=new Map(),decisions=new Map(),reused=new Set();
  const getDoc=(id,kind)=> {
    const d=db.prepare('SELECT d.*,e.id legacy_id,e.kind entity_kind FROM document d JOIN legacy_entity e ON e.document_path=d.path WHERE e.id=? AND e.kind=?').get(id,kind);
    if(!d)throw Error(`Saknat underlag: ${id}/${kind}`);docs.set(d.path,d);return d;
  };
  const unit=id=>db.prepare('SELECT * FROM unit WHERE id=?').get(id)??newSpans.get(id);
  function span(d,start,end,label) {
    const id=sha(`${d.path}\0${d.sha256}\0curated_span\0${start}\0${end}`);
    if(end<=start)throw Error('Tomt ursprungsspann');
    if(!newSpans.has(id)) {
      const raw=Buffer.from(d.text).subarray(start,end).toString();
      request.spans.push({id,path:d.path,sha256:d.sha256,start,end,owner:d.legacy_id,section:label});
      newSpans.set(id,{id,document_path:d.path,raw,start_byte:start,end_byte:end,start_line:Buffer.from(d.text).subarray(0,start).toString().split('\n').length,end_line:Buffer.from(d.text).subarray(0,end).toString().replace(/\n$/,'').split('\n').length,historical:0});
    }
    return id;
  }
  function resolveOrigin(ref) {
    if(typeof ref==='string') {
      if(unit(ref))return ref;
      const rows=db.prepare('SELECT id FROM unit WHERE legacy_id=? AND historical=0').all(ref);
      if(rows.length!==1)throw Error(`Ursprung måste vara entydigt: ${ref}`);return rows[0].id;
    }
    const d=getDoc(ref.entity,ref.kind),lines=d.text.split(/(?<=\n)/),a=ref.startLine,b=ref.endLine;
    if(!Number.isInteger(a)||!Number.isInteger(b)||a<1||b<a||b>lines.length)throw Error(`Fel ursprungsspann: ${ref.entity}:${a}–${b}`);
    return span(d,Buffer.byteLength(lines.slice(0,a-1).join('')),Buffer.byteLength(lines.slice(0,b).join('')),`Personkonvertering ${a}–${b}`);
  }
  function link(id,origins,coverage='partial') {
    for(const u of origins) {
      if(!links.has(u))links.set(u,[]);
      if(!links.get(u).some(x=>x.target===id&&x.coverage===coverage))links.get(u).push({target:id,coverage});
    }
  }
  function add(m,{automatic=false}={}) {
    const originIds=(m.origins??[]).map(resolveOrigin);
    if(!originIds.length)throw Error(`Granskat ursprung krävs: ${m.id}`);
    const current=head(db,m.id);
    // Ett uttryckligt versionsbeslut i review.changes prövas redan ovanför
    // de automatiska profilrepresentationerna. Samma innehåll får förenas
    // med det beslutet; jämförelsen av kind/data/version/disposition nedan
    // stoppar en motstridig eller föråldrad revision. Utan explicit revision
    // krävs fortfarande oförändrat innehåll och oförändrad disposition.
    if(automatic&&current&&current.operation_id!==request.id&&!changes.has(m.id)) {
      const old=readCurrent(db,m.id);
      const content=m.kind==='narrative'?'markdown':'body';
      if(old.kind!==m.kind||old[content]!==m.data[content]||old.subject_id!==m.data.subject_id||old.disposition!==m.disposition)throw Error(`Tidigare forskningsobjekt kräver uttrycklig omprövning: ${m.id}`);
      reused.add(m.id);link(m.id,originIds,'complete');return;
    }
    if(current&&current.operation_id!==request.id&&m.revises!==current.version&&!(automatic&&changes.has(m.id)))throw Error(`Befintligt objekt kräver reuse eller explicit revises: ${m.id}`);
    const expected=current?.operation_id===request.id?current.version-1||null:current?.version??null;
    const change={id:m.id,kind:m.kind,expectedVersion:expected,disposition:m.disposition,evidenceStatus:m.evidenceStatus??null,data:m.data,
      rationale:m.rationale,caveat:m.caveat??'',origins:uniqueOrigins(originIds.map(id=>({unit:id,coverage:automatic?'complete':'partial',note:'Överfört befintligt underlag; ingen ny oberoende evidensröst.'}))),evidence:m.evidence??[]};
    if(m.assets!==undefined)change.assets=m.assets;
    if(!change.rationale?.trim()||!change.disposition)throw Error(`Ofullständig sakbedömning: ${m.id}`);
    if(changes.has(m.id)) {
      const old=changes.get(m.id);
      for(const k of ['kind','data','expectedVersion','disposition','evidenceStatus'])if(canonical(old[k])!==canonical(change[k]))throw Error(`Gemensamt objekt kräver saklig avstämning: ${m.id}/${k}`);
      old.origins=uniqueOrigins([...old.origins,...change.origins]);old.caveat=combineText(old.caveat,change.caveat);old.rationale=combineText(old.rationale,change.rationale);old.evidence.push(...change.evidence);
      if(change.assets)old.assets=[...new Map([...(old.assets??[]),...change.assets].map(a=>[canonical(a),a])).values()];
    }else changes.set(m.id,change);
    link(m.id,originIds,automatic?'complete':'partial');
  }
  function decision(d,u) {
    if(!states.has(d.state)||!d.rationale?.trim()||!Array.isArray(d.targets)||(d.state==='mapped_complete'&&!d.targets.length)||(d.state==='pending_interpretation'&&!d.question?.trim()))throw Error(`Ofullständigt representationsbeslut: ${u.id}`);
    for(const target of d.targets)link(target,[u.id],d.state==='mapped_complete'?'collective':'partial');
    decisions.set(u.id,{state:d.state,targets:d.targets,rationale:d.rationale,question:d.question??''});
  }
  for(const review of [...reviews].sort((a,b)=>a.person.localeCompare(b.person))) {
    if(!review.readingNote?.trim()||!Array.isArray(review.changes)||!Array.isArray(review.assertions)||!Array.isArray(review.relations)||!Array.isArray(review.reuse)||!Array.isArray(review.pending))throw Error(`Ofullständig persongranskning: ${review.person}`);
    const personDoc=getDoc(review.person,'person'),profile=getDoc(review.person,'profile');
    const expected=[personDoc,profile].map(d=>({path:d.path,sha256:d.sha256})).sort((a,b)=>a.path.localeCompare(b.path));
    if(canonical([...review.documents].sort((a,b)=>a.path.localeCompare(b.path)))!==canonical(expected))throw Error(`Fel persondokument/hash: ${review.person}`);
    const researchState=review.researchState;
    if(researchState&&(researchState.disposition!=='retired'||!researchState.rationale?.trim()||!researchState.origins?.length))throw Error(`Forskningsavveckling kräver uttrycklig grund: ${review.person}`);
    // A legacy dossier can be an abandoned reading or a duplicate. Its old
    // research belongs to that documented decision, not to the target person's
    // current profile. A mapping alone never establishes a person identity.
    let researchSubject=review.person,archivedDossier=false;
    if(head(db,review.person)?.kind!=='person') {
      const imported=readCurrent(db,`IMPORT-${review.person}`);
      const mappingType=imported?.outcome==='same_identity'?'same_identity':imported?.outcome==='historical_proposal'?'archival_reference':null;
      const mapping=mappingType&&db.prepare('SELECT id FROM legacy_mapping WHERE legacy_id=? AND target_id=? AND mapping_type=?').get(review.person,imported.subject_id,mappingType);
      if(imported?.kind!=='assessment'||imported.criteria!=='legacy_dossier_identity_import/1'||!mapping||researchState?.disposition!=='retired')throw Error(`Icke-personakt kräver beslutad mappning och uttrycklig forskningsavveckling: ${review.person}`);
      if(review.changes.some(m=>m.id===review.person))throw Error(`Avvecklad icke-personakt får inte återuppstå som objekt: ${review.person}`);
      researchSubject=imported.object_id;archivedDossier=true;
    }
    const researchDisposition=researchState?.disposition??'recorded';
    const researchOrigins=researchState?.origins??[];
    const researchCaveat=combineText(review.readingNote,researchState?.rationale);
    for(const m of review.changes)add(m);
    for(const r of review.reuse) {
      if(!r.rationale?.trim())throw Error(`Återbruk saknar motivering: ${r.object}`);
      const origins=r.origins.map(resolveOrigin);if(!origins.length)throw Error('Återbruk saknar ursprung');
      reused.add(r.object);link(r.object,origins);
    }
    const assertionUnits=db.prepare("SELECT * FROM unit WHERE document_path=? AND kind='assertion' AND historical=0 ORDER BY start_byte").all(personDoc.path);
    if(canonical(review.assertions.map(a=>a.id).sort())!==canonical(assertionUnits.map(u=>u.legacy_id).sort()))throw Error(`Alla aktuella A-rader måste ha eget utfall: ${review.person}`);
    for(const a of review.assertions)decision(a,assertionUnits.find(u=>u.legacy_id===a.id));
    const relationUnits=db.prepare("SELECT * FROM unit WHERE document_path=? AND kind='relation_row' AND historical=0 ORDER BY start_byte").all(personDoc.path).filter(u=>JSON.parse(u.parsed_json).cells[0]!=='Person');
    if(canonical(review.relations.map(r=>r.unit).sort())!==canonical(relationUnits.map(u=>u.id).sort()))throw Error(`Alla relationsrader måste ha eget utfall: ${review.person}`);
    for(const r of review.relations)decision(r,unit(r.unit));
    const profileUnits=db.prepare('SELECT * FROM unit WHERE document_path=? AND historical=0 ORDER BY start_byte').all(profile.path);
    const preface=profile.text.split(/(?=^## )/m)[0],prefix=span(profile,0,Buffer.byteLength(preface),'profilens bevarade bedömningshuvud');
    add({id:'ASSESSMENT-'+review.person,kind:'assessment',data:{subject_id:researchSubject,criteria:'legacy_review_header',outcome:preface.match(/- Identitetsgranskning:\s*(.*)/)?.[1]??'Ej utskrivet',body:preface},disposition:researchDisposition,rationale:'Befintligt bedömningshuvud med ursprungliga kriterier och datum; ingen ny granskning.',caveat:researchCaveat,origins:[prefix,...researchOrigins]},{automatic:true});
    for(const u of profileUnits) {
      const p=JSON.parse(u.parsed_json),c=p.cells;
      let id,kind='assessment',criteria,outcome;
      // A renamed question/path may retain its old link anchor as a nested
      // heading with the same id. Its text already belongs to the enclosing
      // object. Separate, non-contained occurrences must still fail rather
      // than silently choosing one of two competing current descriptions.
      if(['question','source_path'].includes(u.kind)&&profileUnits.some(parent=>
        parent.kind===u.kind&&parent.legacy_id===u.legacy_id&&
        parent.start_byte<u.start_byte&&parent.end_byte>=u.end_byte))continue;
      if(u.kind==='question') {id=u.legacy_id;kind='question';}
      else if(u.kind==='source_path') {id='PATH-'+u.legacy_id.replace('/','-');criteria='legacy_source_path';outcome=p.fields['Undersökt omfång och utfall']??'Ej utskrivet';}
      else if(u.kind==='table_row'&&u.section==='Livsteman'&&c?.[0]!=='Tema') {id=`THEME-${review.person}-${c[0]}`;criteria=`legacy_theme/${c[0]}`;outcome=c[1];}
      else if(u.kind==='table_row'&&u.section==='Kontraktsgranskning'&&/^PK-\d+$/.test(c?.[0])) {id=`CONTRACT-${review.person}-${c[0]}`;criteria=`legacy_person_contract/${c[0]}`;outcome=c[1];}
      else if(u.kind==='table_row'&&u.section==='Söknycklar'&&c?.[0]!=='Nyckel') {id=`KEY-${review.person}-${u.id.slice(0,12)}`;criteria='legacy_search_key';outcome='recorded';}
      else if(u.kind==='section'&&['Identitetsbedömning','Forskningsfrågor','Källvägar'].includes(u.section)) {
        if(u.section!=='Identitetsbedömning'&&profileUnits.some(x=>x.kind===(u.section==='Forskningsfrågor'?'question':'source_path')))continue;
        id=`RESEARCH-${review.person}-${sha(u.section).slice(0,12)}`;criteria=`legacy_profile_section/${u.section}`;outcome='recorded';
      }else continue;
      add({id,kind,disposition:researchDisposition,data:kind==='question'?{subject_id:researchSubject,title:p.heading,outcome:p.fields['Slutsatsläge']??'Ej utskrivet',body:u.raw}:{subject_id:researchSubject,criteria,outcome,body:u.raw},origins:[u.id,...researchOrigins],rationale:'Befintlig personbunden forskningskunskap med ordagranna kriterier, omfång och begränsningar; Wotan äger utförandet.',caveat:researchCaveat},{automatic:true});
    }
    const bios=db.prepare("SELECT * FROM unit WHERE document_path=? AND kind='section' AND section='Biografisk sammanfattning'").all(personDoc.path);
    if(bios.length!==1)throw Error(`Biografi måste avgränsas explicit: ${review.person}`);
    add({id:'BIO-'+review.person,kind:'narrative',disposition:archivedDossier?'retired':'recorded',data:{subject_id:researchSubject,title:archivedDossier?`Historik från avvecklad akt ${review.person}`:'Biografisk sammanfattning',markdown:bios[0].raw},origins:[bios[0].id],rationale:'Tidigare berättelse versionsbevarad; inte en ny oberoende faktakälla.',caveat:review.readingNote},{automatic:true});
    for(const p of review.pending) {
      const id=resolveOrigin(p.origin);if(!p.question?.trim())throw Error('Tom tolkningsfråga');
      if(![personDoc.path,profile.path].includes(unit(id).document_path))throw Error(`Tolkningsfråga måste förankras i personens egen akt eller profil: ${review.person}. Bevara den externa källhänvisningen i frågan och sakobjektens ursprung.`);
      const previous=decisions.get(id);
      decision({state:'pending_interpretation',targets:previous?.targets??[],rationale:combineText(previous?.rationale,review.readingNote),question:combineText(previous?.question,p.question)},unit(id));
    }
  }
  for(const id of reused)if(!head(db,id)&&!changes.has(id))throw Error(`Återbrukat objekt saknas: ${id}`);
  // A partial origin maps only that span. Complete automatic text objects also
  // cover their contained rows, but never promote historical material.
  const covered=[];
  for(const [uid,items]of links)for(const x of items)if(x.coverage==='complete')covered.push({u:unit(uid),target:x.target});
  const wanted=new Set(scope.documents);
  const allUnits=new Map([...db.prepare('SELECT * FROM unit').all().filter(u=>wanted.has(u.document_path)),...newSpans.values()].map(u=>[u.id,u]));
  for(const [id,u]of allUnits) {
    if(!wanted.has(u.document_path))continue;
    let d=decisions.get(id);
    if(!d) {
      const direct=(links.get(id)??[]).find(x=>x.coverage==='complete'),whole=covered.find(x=>x.u.document_path===u.document_path&&x.u.start_byte<=u.start_byte&&x.u.end_byte>=u.end_byte);
      const target=direct?.target??whole?.target;
      d={state:u.historical?'preserved_history':target?'mapped_complete':'preserved_text',targets:target?[target]:[],rationale:u.historical?'Bevarad äldre historik; inte automatiskt aktuell personkunskap.':target?'Hela textenheten bevaras ordagrant i sitt forskningsobjekt, med kriterier och förbehåll.':'Textenheten finns kvar i det frysta underlaget; typade deluppgifter har egna ursprung och beslut.',question:''};
    }
    // A partial reuse is still an explicit provenance link. Keep its targets
    // even outside A-/relation decisions, without claiming complete coverage.
    d={...d,targets:[...new Set([...d.targets,...(links.get(id)??[]).map(x=>x.target)])]};
    for(const target of d.targets)if(!changes.has(target)&&!head(db,target))throw Error(`Beslut hänvisar till saknat mål: ${target}`);
    const previous=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(id);
    const expected=previous?.operation_id===request.id?previous.version-1||null:previous?.version??null;
    request.unitDecisions.push({unit:id,expectedVersion:expected,state:d.state,target:d.targets[0]??null,targets:d.targets,rationale:d.rationale+(d.targets.length>1?' Samverkande mål: '+d.targets.join(', ')+'.':''),question:d.question});
  }
  // Explicit multi-target mappings must remain discoverable through every
  // target, not just the first target_id on the decision.
  for(const [uid,d]of decisions)for(const target of d.targets) {
    const c=changes.get(target);
    if(c&&!c.origins.some(o=>o.unit===uid))c.origins.push({unit:uid,coverage:'partial',note:d.rationale});
  }
  const versions=new Map([...changes].map(([id,m])=>[id,(m.expectedVersion??0)+1]));
  for(const m of changes.values()) {
    m.evidence=[...new Map(m.evidence.map(e=>{const v=versions.get(e.object)??head(db,e.object)?.version;if(!v)throw Error(`Belägg saknas: ${e.object}`);return [e.object+'\0'+e.role,{...e,version:v}];})).values()];
    m.bindings={};for(const field of structural[m.kind]??[]) {const id=m.data[field];if(id!=null)m.bindings[id]=versions.get(id)??head(db,id)?.version;}
  }
  const waiting=new Map(changes),placed=new Set();
  while(waiting.size) {
    let progress=false;
    for(const [id,m]of waiting) {
      const dependencies=[...Object.keys(m.bindings),...m.evidence.map(e=>e.object)];
      if(dependencies.some(x=>x!==id&&changes.has(x)&&!placed.has(x)))continue;
      request.changes.push(m);placed.add(id);waiting.delete(id);progress=true;
    }
    if(!progress)throw Error('Cykel bland konverteringens belägg/strukturreferenser');
  }
  request.unitDecisions.sort((a,b)=>a.unit.localeCompare(b.unit));return request;
}
