// A read-only, compact projection of personView. It never grades evidence or
// parses legacy review headers; the optional gate is supplied by identityGate.
const oneLine=value=>String(value??'').replace(/\s+/g,' ').trim();
const text=value=>oneLine(value).replace(/\|/g,'\\|');
const code=value=>'`'+String(value??'').replace(/`/g,'')+'`';
const list=value=>Array.isArray(value)?value:[];
const parse=value=>{if(typeof value!=='string')return value;try{return JSON.parse(value);}catch{return value;}};
const ref=o=>code(o.revision_id??o.object_id??o.id);
const disposition={accepted:'accepterad',recorded:'registrerad',candidate:'kandidat',rejected:'avvisad',retired:'avvecklad'};
const state=o=>`${disposition[o.disposition]??o.disposition??'ej angiven'}${o.evidence_status?`; ${o.evidence_status}`:''}`;
const eventNames={birth:'Födelse',baptism:'Dop',confirmation:'Konfirmation',banns:'Lysning',marriage:'Vigsel',divorce:'Skilsmässa',death:'Död',burial:'Begravning',registered_arrival:'Registrerad inflyttning',registered_departure:'Registrerad utflyttning',residence:'Bosättning',other:'Annan händelse'};
const roles={principal:'huvudperson',child:'barn',mother:'mor',father:'far',spouse:'make/maka',bride:'brud',groom:'brudgum',witness:'vittne',baptism_witness:'dopvittne',officiant:'förrättare',resident:'boende',arriving:'inflyttande',departing:'utflyttande'};
const placeRoles={place_of_event:'händelseort',registered_birth_parish:'registrerad födelseförsamling',recorded_birth_parish:'uppgiven födelseförsamling',registered_parish:'registrerad församling',registered_residence:'bokförd bosättning',registered_arrival_place:'registrerad inflyttningsort',registered_departure_place:'registrerad utflyttningsort'};
const relationNatures={recorded_parent:'källangiven förälder',biological:'biologisk',recorded_spouse:'källangivet äktenskap',spouse:'äktenskap',recorded_partner:'källangiven partner',recorded_sibling:'källangivet syskonskap',paternal_sibling:'syskonskap genom fadern',maternal_sibling:'syskonskap genom modern'};
const properties={name_form:'Namnformer',civil_status:'Civilstånd',known_children:'Kända barn',reported_children:'Uppgivna barn',household_membership:'Hushåll',occupation:'Försörjning',residence:'Bosättning',reported_birth_place:'Uppgiven födelseort',birth_context:'Födelseuppgifter',family_context:'Familjesammanhang',life_scope:'Livsbildens gränser',source_scope:'Källans räckvidd',source_reference:'Källhänvisning',source_assessment:'Källbedömning',source_interpretation:'Källtolkning',source_conflict:'Källkonflikt',source_comparison:'Källjämförelse',identity_comparison:'Identitetsjämförelse',migration_date_conflict:'Motstridiga flyttdatum'};
const label=o=>o.title??properties[o.property]??o.property??o.criteria??o.kind??'Uppgift';
const substantive=o=>['candidate','rejected'].includes(o.disposition)||['CONFLICT','REJECTED'].includes(o.evidence_status)||['candidate','rejected','different_people','unresolved'].includes(o.decision);
const fieldNames={conclusion:'Slutsats',interpretation:'Tolkning',scope:'Omfång',unknown:'Olöst',unread:'Oläst',basis:'Underlag',raw:'Källform',name:'Namn',cause:'Orsak',burial:'Begravning',reported_date:'Rapporterat datum',date_error:'Datumfel',column:'Kolumn',older_person_reservation:'Äldre reservation',own_death_register_read:'Egen dödbok läst',contract_review_changed:'Kontraktsgranskning ändrad',correction:'Rättelse',old:'Äldre uppgift',chosen_actual_move_date:'Vald faktisk flyttdag',receiver_literal:'Mottagarens uppgift',sender_literal:'Avsändarens uppgift',same_route:'Samma väg',place:'Plats',year:'År',date:'Datum',status:'Status',role:'Roll',children:'Barn',father:'Far',mother:'Mor',parents:'Föräldrar',siblings_without_own_row:'Syskon utan egen rad',age_caveat:'Åldersreservation',household_link:'Hushållskoppling',oldest_claim:'Uppgift om äldsta barnet',mother_age_at_birth:'Moderns ålder vid födelsen',father_age_at_birth:'Faderns ålder vid födelsen'};
function structured(value){
  if(value===null||value===undefined)return 'ej angivet';
  if(typeof value==='boolean')return value?'ja':'nej';
  if(Array.isArray(value))return value.map(structured).join('; ');
  if(typeof value==='object')return Object.entries(value).map(([k,v])=>`${fieldNames[k]??k.replaceAll('_',' ')}: ${structured(v)}`).join('; ');
  return String(value);
}
const hasBoundary=value=>value&&typeof value==='object'&&Object.entries(value).some(([k,v])=>/(?:caveat|conflict|correction|reservation|scope|unknown|unread|limit)/i.test(k)||hasBoundary(v));

function dateInfo(raw) {
  const d=parse(raw)??{},precision=d.precision??'unknown';
  const names={exact:'exakt datum',year:'år',circa:'omkring',range:'intervall',alternatives:'alternativ',unknown:'okänt datum'};
  let value='';
  if(['exact','year','circa'].includes(precision))value=d.value??'';
  if(precision==='range')value=`${d.from}–${d.to}`;
  if(precision==='alternatives')value=list(d.values).join(' eller ');
  const literal=d.literal&&d.literal!==value?`; källform: ${d.literal}`:'';
  // Sort only typed date fields. Alphabetic source literals are never parsed as
  // dates, and a range/alternative remains a range/alternative in the display.
  const dates=(precision==='range'?[d.from]:precision==='alternatives'?list(d.values):precision==='unknown'?[]:[d.value])
    .filter(v=>typeof v==='string'&&/^\d{4}(?:-\d{2}-\d{2})?$/.test(v)).sort();
  return {sort:dates[0]??'\uffff',display:`${value?`${value} — `:''}${names[precision]??precision}${literal}`};
}

function objects(view,gate) {
  const found=new Map();
  const add=o=>{if(!o?.object_id)return;found.set(o.object_id,o);add(o.participation);for(const q of list(o.qualifications))add(q);};
  add(view.person);
  for(const value of Object.values(view))if(Array.isArray(value))for(const o of value)add(o);
  for(const value of Object.values(view.research??{}))for(const o of list(value))add(o);
  for(const axis of ['identity_review','tree_effect','life_picture_review'])for(const o of [...list(gate?.[axis]?.assessments),...list(gate?.[axis]?.ignored_assessments)])add(o);
  for(const o of list(gate?.other_assessments))add(o);
  return [...found.values()];
}

/** Full details stay in renderPerson/inspect. No source text, status, date or
 * caveat is altered; repeated caveats are folded by whitespace only. */
export function renderPersonOverview(view,{gate}={}) {
  if(!view?.id)throw TypeError('Personvyn måste ha ett id');
  if(gate&&gate.person_id!==view.id)throw Error('Identitetsgrinden gäller en annan person');
  const all=objects(view,gate);
  const caveats=new Map();
  for(const o of all)if(oneLine(o.caveat)){
    const key=oneLine(o.caveat),entry=caveats.get(key)??{number:caveats.size+1,objects:[]};
    entry.objects.push(ref(o));caveats.set(key,entry);
  }
  const note=o=>oneLine(o?.caveat)?` [F${caveats.get(oneLine(o.caveat)).number}]`:'';
  const mappings=list(view.identityMappings),ownMappings=mappings.filter(m=>m.legacy_id===view.id);
  const alias=ownMappings.find(m=>m.mapping_type==='same_identity');
  const archived=!view.person&&!alias&&ownMappings.some(m=>m.mapping_type==='archival_reference');
  const legacyTitle=list(view.legacy).find(x=>x.kind==='person')?.title;
  const title=view.person?.display_name??legacyTitle?.replace(new RegExp(`^${view.id}:\\s*`),'')??view.id;
  const lines=[`# ${text(title)} — ${text(view.id)}`,''];
  if(view.person)lines.push(`Verklig person i modellen. Personkärna: ${state(view.person)}.${note(view.person)}`);
  else if(alias)lines.push(`Alias för ${code(alias.target_id)}. Ingen separat personkärna; läs målpersonens översikt.`);
  else if(archived)lines.push('Arkivreferens utan egen personkärna. Den äldre akten ska inte användas som en separat person.');
  else lines.push('Ingen aktuell personkärna finns i denna vy.');
  if(view.person?.legacy_state==='retired')lines.push('Forskningen i den äldre akten är avvecklad. Detta avvisar inte personens existens.');
  lines.push('','## Granskningsnivåer','');
  const outcomes={passed:'GODKÄND',failed:'UNDERKÄND',unreviewed:'EJ GRANSKAD',supporting:'BÄRANDE',waiting:'AVVAKTAR',non_supporting:'EJ BÄRANDE'};
  for(const [axis,name] of [['identity_review','Identitetsgranskning'],['tree_effect','Trädverkan'],['life_picture_review','Livsbild']]){
    const a=gate?.[axis];
    if(!a){lines.push(`- **${name}:** ej läst; inget utfall härlett ur personkärnans status.`);continue;}
    let result=outcomes[a.outcome]??a.outcome??'uttryckligt utfall saknas';
    if(axis==='life_picture_review'&&a.scope==='legacy_full_contract'&&a.source!=='missing')result=`separat livsbildsgranskning saknas i grinden; äldre fullkontrakt: ${result}`;
    lines.push(`- **${name}:** ${text(result)}${a.usable?'':' — kan inte tillgodoräknas som giltigt utfall'}. ${list(a.assessments).map(ref).join(', ')}`.trim());
  }
  if(gate)lines.push(`- **Identitetsgrind:** ${gate.passed?'passerar':'passerar inte'}. Livsbildens utfall prövas separat.`);
  const issues=new Map();
  for(const x of [...list(gate?.reasons),...['identity_review','tree_effect','life_picture_review'].flatMap(a=>list(gate?.[a]?.issues))]){
    if(x.code==='gate_outcome_not_supporting')continue; // The exact axis outcome is already printed above.
    const k=oneLine(x.message);if(k)issues.set(k,[...new Set([...(issues.get(k)??[]),...list(x.revision_ids)])]);
  }
  for(const [message,refs] of issues)lines.push(`- ${text(message)}${refs.length?` (${refs.map(code).join(', ')})`:''}`);

  const visibleMappings=mappings.filter(m=>!(view.person&&m.mapping_type==='archival_reference'&&m.legacy_id===view.id&&m.target_id===view.id));
  if(visibleMappings.length||list(view.importAssessments).length){
    lines.push('','## Akt och identitet','');
    const mappingNames={same_identity:'alias',archival_reference:'arkivreferens',rejected_identity:'avvisad identifikation'};
    for(const m of visibleMappings)lines.push(`- ${code(m.legacy_id)} → ${code(m.target_id)} (${mappingNames[m.mapping_type]??m.mapping_type}): ${text(m.rationale)}`);
    for(const a of list(view.importAssessments))lines.push(`- ${ref(a)} — ${state(a)}; ${text(a.outcome)}. ${text(a.body)}${note(a)}`);
  }

  const pending=new Map();
  for(const o of all)for(const p of list(o.pending_reviews)){
    const key=p.id??JSON.stringify(p),entry=pending.get(key)??{p,objects:new Set()};entry.objects.add(ref(o));pending.set(key,entry);
  }
  if(pending.size){lines.push('','## Omprövning väntar','');for(const {p,objects} of pending.values())lines.push(`- ${code(p.id)}: ${text(p.reason)} Ändrat underlag: ${code(p.changed_revision_id)}. Berör: ${[...objects].join(', ')}.`);}

  lines.push('','## Händelser och egna roller','');
  const events=new Map();
  for(const e of list(view.events)){
    const id=e.event_id??e.object_id,entry=events.get(id)??{event:e,participations:new Map()};
    if(e.participation)entry.participations.set(e.participation.object_id??e.participation.role,e.participation);
    events.set(id,entry);
  }
  const ordered=[...events.values()].sort((a,b)=>{
    const aa=dateInfo(a.event.date_json).sort,bb=dateInfo(b.event.date_json).sort;
    return aa<bb?-1:aa>bb?1:String(a.event.object_id).localeCompare(String(b.event.object_id),'sv');
  });
  if(!ordered.length)lines.push('Inga händelser med eget deltagande finns i denna vy.');
  for(const {event:e,participations} of ordered){
    const placeRole=placeRoles[e.place_role]??e.place_role;
    const place=e.place_id?` Plats: ${code(e.place_id)}; platsroll: ${text(placeRole||'ej angiven')}.`:e.place_role?` Plats ej angiven; platsroll: ${text(placeRole)}.`:'';
    lines.push(`- **${text(dateInfo(e.date_json).display)}:** ${eventNames[e.event_type]??text(e.event_type)} — ${state(e)}. ${ref(e)}${note(e)}.${place}`);
    for(const p of participations.values())lines.push(`  - Egen roll: **${roles[p.role]??text(p.role)}** — ${state(p)}. ${ref(p)}${note(p)}`);
    for(const f of list(e.qualifications))lines.push(`  - ${text(label(f))}: ${text(structured(parse(f.value_json)))}. ${state(f)}; ${ref(f)}${note(f)}`);
  }

  if(list(view.relations).length){
    lines.push('','## Familjerelationer','');
    const types={parent:'förälder till',spouse:'make/maka till',partner:'partner till',sibling:'syskon till'};
    for(const r of view.relations)lines.push(`- ${code(r.from_person)} ${types[r.relation_type]??text(r.relation_type)} ${code(r.to_person)} — ${state(r)}; art: ${text(relationNatures[r.nature]??r.nature)}. ${ref(r)}${note(r)}${list(r.qualifications).map(f=>` Precisering ${ref(f)}${note(f)}.`).join('')}`);
  }

  const risks=all.filter(o=>substantive(o)&&!['event','participation','relation','person'].includes(o.kind));
  if(risks.length){
    lines.push('','## Kandidater, avvisat och konflikter','');
    for(const o of risks){
      const value=o.kind==='fact'?`; uppgift: ${structured(parse(o.value_json))}`:o.kind==='identity'?`; omnämnande ${o.mention_id} → ${o.person_id}, beslut ${o.decision}`:o.kind==='identity_resolution'?`; ${o.person_a} / ${o.person_b}, beslut ${o.decision}`:'';
      lines.push(`- ${text(label(o))} — ${state(o)}${text(value)}. ${text(o.rationale)} ${ref(o)}${note(o)}`);
    }
  }

  // Native comparisons may carry their reservation in the payload rather than
  // the caveat column. Show all such judgments, including accepted ones.
  const judgments=[...list(view.facts),...list(view.contextFacts),...list(view.relations).flatMap(r=>list(r.qualifications))]
    .filter(f=>!risks.includes(f)&&(/(?:scope|assessment|interpretation|comparison|conflict)/.test(f.property??'')||hasBoundary(parse(f.value_json))));
  if(judgments.length){lines.push('','## Källbedömningar och livsbildens gränser','');for(const f of judgments)lines.push(`- ${text(label(f))}${f.subject_id!==view.id?` (gäller ${code(f.subject_id)})`:''}: ${text(structured(parse(f.value_json)))}. ${ref(f)}${note(f)}`);}

  const reviews=new Map();
  const excluded=new Set(['themes','requirements','paths','keys'].flatMap(k=>list(view.research?.[k]).map(x=>x.object_id)));
  for(const a of [...list(view.research?.reviews),...list(gate?.other_assessments)])if(!excluded.has(a.object_id)&&!list(view.importAssessments).some(x=>x.object_id===a.object_id)&&!['legacy_review_header','Befintlig person-research/v1; ursprungliga datum och kriterier i body'].includes(a.criteria))reviews.set(a.object_id,a);
  if(reviews.size){lines.push('','## Övriga uttryckliga bedömningar','');for(const a of reviews.values()){
    const body=a.criteria?.startsWith('legacy_profile_section/')?`Bevarat profilavsnitt: ${a.criteria.slice('legacy_profile_section/'.length)}. Läs hela texten och dess rättelser med inspect.`:a.body;
    lines.push(`- ${ref(a)} — ${text(a.outcome)}; ${state(a)}. ${text(body)}${note(a)}`);
  }}

  lines.push('','## Frågor och kunskapsläge','');
  const questions=list(view.research?.questions??view.questions),active=questions.filter(q=>q.active??q.disposition!=='retired');
  const unresolved=active.filter(q=>!['established','rejected','supported','passed','reviewed','bounded','privacy_bounded'].includes(q.outcome_code));
  lines.push(`Forskningsfrågor: ${questions.length} totalt, ${active.length} aktiva, ${questions.length-active.length} inaktiva. ${unresolved.length} aktiva frågor saknar ett uttryckligt avslutande utfall i frågekoden.`);
  for(const q of questions)lines.push(`- ${text(q.title)} — ${text(q.outcome||'utfall saknas')}; ${(q.active??q.disposition!=='retired')?'aktiv':'inaktiv'}. ${ref(q)}${note(q)}`);
  const interpretations=new Map();
  for(const q of list(view.interpretationQuestions)){
    const key=oneLine(q.question);if(!interpretations.has(key))interpretations.set(key,[]);interpretations.get(key).push(`${q.document_path}:${q.start_line}–${q.end_line}`);
  }
  lines.push(`Bevarade tolkningsenheter: ${list(view.interpretationQuestions).length}; skilda frågetexter: ${interpretations.size}. ${pending.size} väntande beroendeomprövningar.`);
  for(const [question,sources] of interpretations)lines.push(`- ${text(question)} (${[...new Set(sources)].map(code).join(', ')})`);
  for(const [key,name] of [['themes','Livsteman'],['requirements','Kontraktskrav']]){
    const counts=new Map();for(const a of list(view.research?.[key])){const outcome=oneLine(a.outcome)||'utfall saknas';counts.set(outcome,(counts.get(outcome)??0)+1);}
    if(counts.size)lines.push(`${name}, bevarade utfall: ${[...counts].map(([outcome,n])=>`${outcome}: ${n}`).join('; ')}. Detaljer finns i fullvyn.`);
  }
  lines.push('Antalen beskriver dokumenterat kunskapsläge och överlappande underlag; de betyder inte att forskningen är färdig.');

  if(caveats.size){lines.push('','## Förbehåll','');for(const [body,entry] of caveats)lines.push(`- **[F${entry.number}]** ${text(body)} (${entry.objects.slice(0,3).join(', ')}${entry.objects.length>3?`; samma förbehåll finns på ytterligare ${entry.objects.length-3} objekt i fullvyn`:''})`);}
  lines.push('','## Läs vidare','',
    `Full personvy: ${code(`node genealogy2/cli.mjs person ${view.id} --full --format markdown`)}.`,
    `Full JSON: ${code(`node genealogy2/cli.mjs person ${view.id} --format json`)}.`,
    `Alla versioner, belägg och ursprung: ${code('node genealogy2/cli.mjs inspect OBJEKT-ID')} (använd id utan @version).`,
    `Bevarad äldre akt och profil: ${code(`node genealogy2/cli.mjs show ${view.id}`)}.`,
    `I fullvyn: egna sakuppgifter ${list(view.facts).length}; kontextuppgifter ${list(view.contextFacts).length}; källobservationer ${list(view.observations).length}; omnämnanden ${list(view.mentions).length}; sökningar ${list(view.searches).length}.`,
    'Råuppgifter och provenans återges där i sin helhet; frånvaro i översikten är inte ett negativt forskningsresultat.','');
  return lines.join('\n');
}
