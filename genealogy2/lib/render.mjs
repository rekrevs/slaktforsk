// Render the same complete objects as JSON. No separate SQL projection and no
// hard-coded list that could silently drop a new payload field or qualification.
const metadata=new Set(['object_id','revision_id','version','kind','disposition','evidence_status','rationale','caveat','origins','evidence','pending_reviews','participation','event_id','qualifications']);
const labels={event_type:'Händelse',date_json:'Datum',place_id:'Plats',place_role:'Platsens roll',role:'Deltagarroll',subject_id:'Ämne',outcome:'Utfall',body:'Text',markdown:'Berättelse',display_name:'Namn',sex:'Kön',legacy_state:'Äldre aktstatus'};
const value=v=>typeof v==='string'?v:JSON.stringify(v);
function renderObject(o,level=3) {
  const lines=[`${'#'.repeat(level)} ${o.title??o.display_name??o.event_type??o.property??o.kind} — ${o.object_id}`,'',
    `Version ${o.version}. Bedömning: ${o.disposition}. Beläggsstatus: ${o.evidence_status??'ej angiven'}.`,'',
    `Motivering: ${o.rationale}`,''];
  if(o.caveat)lines.push(`**Förbehåll:** ${o.caveat}`,'');
  for(const r of o.pending_reviews)lines.push(`**Omprövning väntar (${r.id}):** ${r.reason} Ändrat underlag: ${r.changed_revision_id}.`,'');
  for(const [k,v] of Object.entries(o))if(!metadata.has(k)&&v!==null&&v!=='')lines.push(`${labels[k]??k}: ${value(v)}`,'');
  lines.push('Ursprung: '+(o.origins.map(x=>`${x.document_path}:${x.start_line}–${x.end_line} (${x.coverage}; ${x.note})`).join('; ')||'inget äldre textspann')+'.','');
  lines.push('Belägg: '+(o.evidence.map(x=>`${x.basis_revision_id} (${x.role}${x.note?'; '+x.note:''})`).join('; ')||'inga explicita beläggslänkar')+'.','');
  if(o.participation)lines.push(renderObject(o.participation,level+1));
  for(const qualification of o.qualifications??[])lines.push(renderObject(qualification,level+1));
  return lines.join('\n');
}
export function renderPerson(view) {
  const lines=[`# ${view.person?.display_name??view.id}`,'',view.note,''];
  if(view.person)lines.push(renderObject(view.person,2));
  for(const [key,title] of Object.entries({identityMappings:'Äldre identitetsmappning',importAssessments:'Prövning av äldre akt',identities:'Identiteter',identityResolutions:'Identitetsprövningar',facts:'Sakuppgifter',contextFacts:'Kontext från personens underlag',observations:'Källuppgifter i personens underlag',mentions:'Källornas personomnämnanden',searches:'Genomförda sökningar',relations:'Relationer',events:'Händelser',questions:'Forskningsfrågor',assessments:'Bedömningar',narratives:'Berättelser'})) {
    if(!view[key]?.length)continue;
    lines.push(`## ${title}`,'');
    if(key==='contextFacts')lines.push('Uppgifterna gäller de angivna ämnena och återbrukas som kontext i personens underlag.','');
    for(const o of view[key])lines.push(o.revision_id?renderObject(o):JSON.stringify(o,null,2),'');
  }
  if(view.interpretationQuestions?.length) {
    lines.push('## Bevarade tolkningsfrågor','');
    for(const q of view.interpretationQuestions)lines.push(`- ${q.question} (${q.document_path}:${q.start_line}–${q.end_line})`);
    lines.push('');
  }
  lines.push('## Återstående äldre underlag','',...view.remaining.map(x=>`- ${x.kind}: ${x.n}`),'',
    ...view.legacy.map(x=>`Äldre ${x.kind}: ${x.document_path}`),'');
  return lines.join('\n');
}
