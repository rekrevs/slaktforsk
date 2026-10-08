import fs from 'node:fs';
import path from 'node:path';
import {head,personView,readCurrent,researchOutcome} from './domain.mjs';
import {identityGate} from './review.mjs';

const routeKeys=new Set(['id','task_id','person_id','question_id','path_id','summary']);
const expectedRoutes={
 'T0803-R1':['T-0803','P-0240','P-0240/Q-02','PATH-P-0240-KP-02'],
 'T0803-R2':['T-0803','P-0240','P-0240/Q-02','PATH-P-0240-KP-02'],
 'T0803-R3':['T-0803','P-0240','P-0240/Q-03','PATH-P-0240-KP-04'],
 'T0217-Emma-probate':['T-0217','P-0246',null,'PATH-P-0246-KP-03'],
 'T0217-Axel-probate':['T-0217','P-0241','P-0241/Q-02','PATH-P-0241-KP-03'],
 'T0217-Axel-military':['T-0217','P-0241',null,'PATH-P-0241-KP-03']
};
const routeScopes={
 'T0803-R1':'Own childhood1902–1930 metadata only: at most one Ljungby and one Gustav Vasa catalogue unit (two total). No parental itinerary or own original extraction.',
 'T0803-R2':'Proposed Sophiahemmet/Röda korset training metadata only: at most one list each (two total). Neither school is established. Ersta/other schools belong to T-0793 planning.',
 'T0803-R3':'Only death1991/probate custody metadata, two entries total, and later-life subset of Q03. Lidingö is candidate, not established jurisdiction. KP04 also contains1718/1951 work owned by T-0359; excluded. Interviews/books T-0801 and1931–46 T-0079 excluded.',
 'T0217-Emma-probate':'Probate1963 routing, reuse C-0936: at most two catalogue units and one name register for this death-year. No probate text; no Axel military work.',
 'T0217-Axel-probate':'Probate1983 routing: at most two catalogue units and one name register for this death-year. Q02 is broader; no probate text, custodian or property ownership conclusion.',
 'T0217-Axel-military':'Registration28965/21 routing: at most two identified1921 enlistment units. No personal military file or inferred regiment/service; no invented question.'
};
export function validateNodeLinks(db,mapping,backlog) {
 if(mapping?.format!=='wotan-node-links/1'||!Array.isArray(mapping.routes)||!Array.isArray(mapping.pilot_people)||Object.keys(mapping).some(k=>!['format','pilot_people','routes'].includes(k)))throw Error('Ogiltigt nodlänkformat; endast associationsmetadata tillåts');
 if(JSON.stringify([...mapping.pilot_people].sort())!==JSON.stringify(['P-0240','P-0241','P-0246']))throw Error('Exakt begränsad pilotpersonlista krävs');
 if(mapping.routes.length!==6||new Set(mapping.routes.map(x=>x.id)).size!==6)throw Error('Exakt sex unika pilotrutter krävs');
 if(!Array.isArray(backlog?.tasks)||new Set(backlog.tasks.map(x=>x.id)).size!==backlog.tasks.length)throw Error('Ogiltig Wotanbacklog');
 for(const r of mapping.routes) {
  if(Object.keys(r).some(k=>!routeKeys.has(k))||typeof r.summary!=='string'||!r.summary.trim()||JSON.stringify([r.task_id,r.person_id,r.question_id??null,r.path_id])!==JSON.stringify(expectedRoutes[r.id]))throw Error(`Fel exakt association: ${r.id}`);
  if(!backlog.tasks.some(t=>t.id===r.task_id))throw Error(`Task saknas: ${r.task_id}`);
  if(head(db,r.person_id)?.kind!=='person')throw Error(`Person saknas: ${r.person_id}`);
  const p=readCurrent(db,r.path_id),q=r.question_id?readCurrent(db,r.question_id):null;
  if(!p||p.kind!=='assessment'||p.criteria!=='legacy_source_path'||p.subject_id!==r.person_id)throw Error(`Källvägsreferens saknas eller fel person: ${r.path_id}`);
  if(r.question_id&&(!q||q.kind!=='question'||q.subject_id!==r.person_id))throw Error(`Frågereferens saknas eller fel person: ${r.question_id}`);
 }
}
export function workView(db,id,{root,mapping,backlog}={}) {
 mapping??=JSON.parse(fs.readFileSync(path.join(root,'wotan/node-links.json'),'utf8'));
 backlog??=JSON.parse(fs.readFileSync(path.join(root,'wotan/backlog.json'),'utf8'));
 validateNodeLinks(db,mapping,backlog);
 if(!mapping.pilot_people.includes(id))throw Error(`Person utanför begränsad nodpilot: ${id}; omappad betyder inte att arbete saknas`);
 const person=personView(db,id),routes=mapping.routes.filter(r=>r.person_id===id).map(r=>{
  const task=backlog.tasks.find(t=>t.id===r.task_id),after=task.after??[];
  const dependencies=after.map(task_id=>({task_id,status:backlog.tasks.find(t=>t.id===task_id)?.status??'missing'}));
  return {...r,association_scope:routeScopes[r.id]+' Navigation subset; original devlog owns limits/stops and other people do not inherit this route.',task:{id:task.id,status:task.status,phase:task.phase??null,priority:task.priority??null,priority_basis:task.priority_basis??null,after,dependencies,blocker:task.blocker??null,dependencies_satisfied:dependencies.every(d=>d.status==='DONE'),ready_with_dependencies:task.status==='READY'&&dependencies.every(d=>d.status==='DONE'),scope_link:`wotan/dev-log/${task.id}.md`,shared_routes:mapping.routes.filter(x=>x.task_id===task.id).map(x=>({id:x.id,person_id:x.person_id,summary:x.summary,relevant_to_this_person:x.person_id===id})),people_anchor:[...new Set(mapping.routes.filter(x=>x.task_id===task.id).map(x=>x.person_id))].sort()},question:r.question_id?readCurrent(db,r.question_id):null,path:readCurrent(db,r.path_id)};
 });
 const searches=person.searches.map(s=>({...s,scope:JSON.parse(s.scope_json),memory_qualification:JSON.parse(s.scope_json).search_memory?.format==='search-memory/1'?'declared search-memory/1; structural metadata only, not certified source completeness':'older format (legacy/unqualified); missing subjects, performed_at, method, material/source version, provider edition, snapshot, coverage limitations and reactivation metadata; historical scope remains useful, no certified complete negative'}));
 return {format:'genealogy2-work/1',person_id:id,pilot_people:mapping.pilot_people,coverage:'Bounded six-route pilot; not a complete work inventory or new research authority.',note:'Wotan is the sole execution queue. Association summaries do not expand the linked full scope. Knowledge outcomes, execution state and owner approval are separate.',knowledge_text_qualification:'Embedded task/prioritization statements in preserved knowledge bodies are historical text; current execution state/mandate derives only from live Wotan and full devlog.',person:person.person,identity_gate:identityGate(db,id),research:person.research,routes,searches};
}
export function renderWork(v) {
 const lines=[`# Arbetsvy ${v.person_id} — ${v.person?.display_name??''}`,'',v.coverage,v.note,'','## Befintliga granskningsbeslut','',`Identitet: ${v.identity_gate.identity_review?.outcome??'ej bedömt'}; Trädverkan: ${v.identity_gate.tree_effect?.outcome??'ej bedömt'}; livsbild: ${v.identity_gate.life_picture_review?.outcome??'ej bedömt'}. ${v.identity_gate.explanation} Full versionsbunden kvalifikation i work --format json.`,'','## Arbetsdelar',''];
 for(const r of v.routes) {
  lines.push(`### ${r.id}: ${r.summary}`,'',`[${r.task.id}](${r.task.scope_link}): ${r.task.status}; priority ${r.task.priority??'unclassified'}; phase ${r.task.phase??'—'}. Gemensamt personankare: ${r.task.people_anchor.join(', ')}.`,r.association_scope,`Delade arbetsdelar (egna delar markerade): ${r.task.shared_routes.map(x=>x.id+' '+x.person_id+(x.relevant_to_this_person?' [egen]':' [annan person]')).join('; ')}`,`Beroenden: ${r.task.dependencies.map(d=>d.task_id+': '+d.status).join(', ')||'inga'}; uppfyllda: ${r.task.dependencies_satisfied}. ${r.task.blocker?`Hinder: ${r.task.blocker}`:''}`);
  lines.push('Kunskapstexten nedan bevaras ordagrant. Inbäddade Wotan-/prioriteringspåståenden är historisk kunskapstext; aktuellt utförandeläge och mandat hämtas enbart från Wotansektionen ovan och dess fulla dev-log.');
  for(const x of [r.question,r.path].filter(Boolean))lines.push(`Kunskapsobjekt ${x.object_id}@${x.version}: råutfall ${JSON.stringify(x.outcome)}; normaliserat ${researchOutcome(x.outcome)??'legacy/unqualified'}.`,x.body,`Förbehåll: ${x.caveat}`,`Versionsbundet underlag: ${JSON.stringify(x.evidence)}`);
  lines.push('');
 }
 lines.push('## Befintliga sökkvitton','');
 for(const s of v.searches)lines.push(`### ${s.object_id}@${s.version}: ${s.outcome}`,`Källa ${s.source_id}; ${s.memory_qualification}`,JSON.stringify(s.scope,null,2),s.body,`Förbehåll: ${s.caveat}`,`Versionsbundet belägg: ${JSON.stringify(s.evidence)}`,'');
 if(!v.searches.length)lines.push('Inga sökkvitton i denna aktuella personprojektion; detta bevisar inte att sökningar eller arbete saknas.');
 return lines.join('\n')+'\n';
}
