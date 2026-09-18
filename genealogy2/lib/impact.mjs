// A read-only discovery aid. Neither provenance nor a text match is evidence.
const kinds=['person','source','record','transcription','mention','observation','identity',
  'identity_resolution','place','event','participation','relation','fact','question',
  'search','assessment','narrative'];
const sorted=values=>[...values].sort();
const word=ch=>ch!==undefined&&/[\p{L}\p{N}_-]/u.test(ch);

function matches(text,term,isId) {
  const found=[];
  for(let at=text.indexOf(term);at!==-1;at=text.indexOf(term,at+term.length)) {
    const right=text[at+term.length];
    // Canonical C-id links may continue with a hyphenated filename slug.
    const citationSlug=/^C-\d+$/.test(term)&&right==='-';
    if(isId&&(word(text[at-1])||(word(right)&&!citationSlug)))continue;
    found.push(at);
  }
  if(!found.length)return null;
  const offset=found[0],start=Math.max(0,offset-110),end=Math.min(text.length,offset+term.length+110);
  return {offset,line:text.slice(0,offset).split('\n').length,occurrences:found.length,
    excerpt:text.slice(start,end),excerpt_start:start};
}

export function impact(db,id,{query=null}={}) {
  if(typeof id!=='string'||!id.trim())throw Error('Ange ett objekt-id eller C-id');
  if(query!==null&&(typeof query!=='string'||!query.trim()))throw Error('Sökfrasen får inte vara tom');
  const heads=new Map(db.prepare('SELECT * FROM current_revision ORDER BY object_id').all().map(r=>[r.object_id,r]));
  const revisions=new Map(db.prepare('SELECT r.*,o.kind FROM revision r JOIN object o ON o.id=r.object_id ORDER BY r.id').all().map(r=>[r.id,r]));
  const units=db.prepare(`SELECT u.*,d.sha256 FROM unit u JOIN document d ON d.path=u.document_path
    WHERE u.legacy_id=? OR u.document_path IN (SELECT document_path FROM legacy_entity WHERE id=?)
    ORDER BY u.document_path,u.start_line,u.id`).all(id,id);
  const native=heads.get(id);
  if(!native&&!/^C-\d+$/.test(id))throw Error(`Objektet eller citationen saknas: ${id}`);
  if(!native&&!units.length)throw Error(`Objektet eller citationen saknas: ${id}`);
  const unitIds=new Set(units.map(u=>u.id));
  if(native)for(const r of db.prepare('SELECT unit_id FROM origin WHERE revision_id IN (SELECT id FROM revision WHERE object_id=?)').all(id))unitIds.add(r.unit_id);
  if(native)for(const r of db.prepare('SELECT unit_id FROM current_unit_target WHERE target_id=?').all(id))unitIds.add(r.unit_id);
  const origins=db.prepare(`SELECT o.*,r.object_id,r.version,r.kind,u.document_path,u.start_line,u.end_line,u.historical,d.sha256
    FROM origin o JOIN current_revision r ON r.id=o.revision_id JOIN unit u ON u.id=o.unit_id
    JOIN document d ON d.path=u.document_path ORDER BY r.object_id,u.id`).all().filter(r=>unitIds.has(r.unit_id));
  const targets=db.prepare(`SELECT t.*,d.state,d.rationale,d.question,u.document_path,u.start_line,u.end_line,u.historical,doc.sha256
    FROM current_unit_target t JOIN current_unit_decision d ON d.id=t.decision_id
    JOIN unit u ON u.id=t.unit_id JOIN document doc ON doc.path=u.document_path
    ORDER BY t.target_id,t.unit_id`).all().filter(r=>unitIds.has(r.unit_id));
  const seeds=new Map();
  const addSeed=(object,route)=>{if(!seeds.has(object))seeds.set(object,[]);seeds.get(object).push(route);};
  if(native)addSeed(id,{type:'explicit_object'});
  else {
    // Citation import mapping is routing only, not a new support edge. Prefer
    // its bounded records; retain unmapped representations explicitly below.
    const mapped=new Set([...origins.map(r=>r.object_id),...targets.map(r=>r.target_id)]);
    for(const object of sorted(mapped)) {
      const h=heads.get(object);if(!h)continue;
      let record=null;
      if(h.kind==='record')record=object;
      if(['transcription','mention','observation'].includes(h.kind))record=db.prepare(`SELECT record_id FROM ${h.kind} WHERE revision_id=?`).get(h.id).record_id;
      if(h.kind==='assessment') {
        const subject=db.prepare('SELECT subject_id FROM assessment WHERE revision_id=?').get(h.id).subject_id;
        if(heads.get(subject)?.kind==='record')record=subject;
      }
      if(record)addSeed(record,{type:'citation_representation',via_object:object});
    }
  }
  const describe=r=>({object_id:r.object_id,revision_id:r.id,version:r.version,kind:r.kind,
    disposition:r.disposition,evidence_status:r.evidence_status,current:heads.get(r.object_id)?.id===r.id});
  const edges=db.prepare('SELECT * FROM dependency ORDER BY basis_revision_id,revision_id,role').all();
  const reverse=new Map(),incoming=new Map();
  for(const edge of edges){if(!incoming.has(edge.revision_id))incoming.set(edge.revision_id,[]);incoming.get(edge.revision_id).push(edge);if(!reverse.has(edge.basis_revision_id))reverse.set(edge.basis_revision_id,[]);reverse.get(edge.basis_revision_id).push(edge);}
  const paths=new Map(),queue=[];
  // Policy 2 reachability includes every historical version of the explicit
  // object. Do not silently replace an old link with the latest revision.
  for(const r of revisions.values())if(seeds.has(r.object_id)){paths.set(r.id,[]);queue.push(r.id);}
  for(let i=0;i<queue.length;i++)for(const edge of reverse.get(queue[i])??[]) {
    if(paths.has(edge.revision_id))continue;
    paths.set(edge.revision_id,[...paths.get(queue[i]),edge]);queue.push(edge.revision_id);
  }
  const dependencies={current:[],historical:[]};
  for(const rid of sorted(paths.keys())) {
    const chain=paths.get(rid);if(!chain.length)continue;
    const r=revisions.get(rid),entry={...describe(r),classification:'registered_version_dependency',
      distance:chain.length,path:chain,
      reached_dependencies:(incoming.get(rid)??[]).filter(e=>paths.has(e.basis_revision_id)),limit:'Registered dependency, not proof that the correction changes this claim. Roles remain explicit; path is one shortest witness, not every route.'};
    dependencies[entry.current?'current':'historical'].push(entry);
  }
  const automatic=new Set([id,...seeds.keys()]);
  // An explicit native object can also be found by its own import citation.
  for(const r of db.prepare('SELECT u.id,e.id AS citation FROM unit u JOIN legacy_entity e ON e.document_path=u.document_path WHERE e.kind=?').all('citation'))if(unitIds.has(r.id))automatic.add(r.citation);
  const terms=sorted(automatic).map(value=>({value,source:'identifier',boundary:true}));
  if(query!==null&&!automatic.has(query))terms.push({value:query,source:'user_phrase',boundary:false});
  const texts={current:[],historical:[]};
  for(const kind of kinds)for(const data of db.prepare(`SELECT * FROM ${kind} ORDER BY revision_id`).all()) {
    const r=revisions.get(data.revision_id),fields={...data,rationale:r.rationale,caveat:r.caveat};
    delete fields.revision_id;
    const hits=[];
    for(const [field,value] of Object.entries(fields))if(typeof value==='string')for(const term of terms) {
      const match=matches(value,term.value,term.boundary);if(match)hits.push({field,term:term.value,term_source:term.source,...match});
    }
    if(!hits.length)continue;
    const current=heads.get(r.object_id).id===r.id;
    texts[current?'current':'historical'].push({...describe(r),
      classification:current?'possible_current_text_copy':'historical_text_only',
      registered_dependency:paths.has(r.id)&&paths.get(r.id).length>0,
      seed:seeds.has(r.object_id),hits,
      limit:current?'Candidate only: may be quotation, retraction, namesake or unrelated context. Read the full field.':'Superseded revision, not a current assertion. Do not rewrite history.'});
  }
  for(const group of Object.values(texts))group.sort((a,b)=>a.revision_id.localeCompare(b.revision_id,'en'));
  const pending=db.prepare(`SELECT p.*,r.object_id FROM pending_review p JOIN revision r ON r.id=p.affected_revision_id ORDER BY p.id`).all();
  const worksheet=new Map();
  const add=(object,reason)=>{if(!worksheet.has(object)){const h=heads.get(object);if(!h)return;worksheet.set(object,{...describe(h),reasons:[],pending_requests:pending.filter(r=>r.object_id===object),decision:null,rationale:null});}const entry=worksheet.get(object);if(!entry.reasons.includes(reason))entry.reasons.push(reason);};
  for(const r of dependencies.current)add(r.object_id,'registered_version_dependency');
  for(const r of origins)add(r.object_id,'import_origin_not_evidence');
  for(const r of targets)add(r.target_id,'import_target_not_evidence');
  for(const r of texts.current)if(!r.seed)add(r.object_id,'possible_current_text_copy');
  return {format:'genealogy2-impact/1',input:id,query,
    database_state:{operations:db.prepare('SELECT count(*) n FROM operation').get().n,
      revisions:revisions.size,last_operation:db.prepare('SELECT sequence,operation_id FROM operation_payload ORDER BY sequence DESC LIMIT 1').get()??null},
    seeds:sorted(seeds.keys()).map(object=>({...describe(heads.get(object)),routes:seeds.get(object)})),
    routing_limit:'C-id maps to bounded records through import representations; this routing is provenance, not source support. No record mapping means no inferred dependency graph.',
    dependencies,provenance:{classification:'import_provenance_not_evidence',origins,targets:targets.map(t=>({...t,...describe(heads.get(t.target_id))}))},
    search:{matching:'Case-sensitive literal phrase; identifiers require boundaries. No stemming, date normalization or semantic matching.',terms},
    text_candidates:texts,
    review:{items:[...worksheet.values()].sort((a,b)=>a.object_id.localeCompare(b.object_id,'en')),
      instructions:'Read inspect for each current object and its evidence. Record a reasoned decision in the active Wotan task / authorized operation. Revise through apply only when warranted; resolve only the exact existing pending request after individual review. Text/provenance candidates do not create requests. Null decisions are unreviewed, never approvals.'},
    limitations:['Read-only snapshot, not an execution queue. Re-run after revisions.',
      'Text matches cannot establish copied facts, identity, error, relevance or support. Current text may contain historical retractions.',
      'Unlinked paraphrases or different date/name spellings may be missed; supply relevant --query variants and inspect affected person profiles.',
      'No query mutates data, adds evidence, opens/closes reviews or certifies complete semantic coverage.']};
}
