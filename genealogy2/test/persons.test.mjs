import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {openDB,importBaseline,exportData,restore,verifyDB} from '../lib/store.mjs';
import {applyOperation,personView,inspect,readCurrent} from '../lib/domain.mjs';import {renderPerson} from '../lib/render.mjs';
import {snapshot,canonical} from '../lib/archive.mjs';import {buildPersons} from '../import/persons.mjs';

for(const retired of [false,true])test(`personimporten bevarar flera mål, gemensamma relationer och ${retired?'avvecklade':'aktiva'} forskningsbedömningar`,async t=> {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-persons-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 fs.mkdirSync(path.join(dir,'genealogy/people'),{recursive:true});fs.mkdirSync(path.join(dir,'genealogy/research-profiles'),{recursive:true});
 fs.mkdirSync(path.join(dir,'genealogy/citations'),{recursive:true});fs.writeFileSync(path.join(dir,'genealogy/citations/C-0001-test.md'),'# C-0001: Extern källa\n\nEn konflikt i källan.\n');
 const pp='genealogy/people/P-0001-test.md',pr='genealogy/research-profiles/P-0001.md';
 fs.writeFileSync(path.join(dir,pp),'# P-0001: Test\n\n## Identitet\n\nExempelperson.\n\n## Påståenden\n\n| ID | Påstående | Status | Tillförlitlighet | Belägg | Kommentar |\n|---|---|---|---|---|---|\n| A-0001 | Född 1900; kolumn 27/28. | TRANSCRIBED | medel | C-0001 | Ingen ålder väljs. |\n\n## Relationer\n\n| Person | Relation | Tid/plats | Status | Belägg |\n|---|---|---|---|---|\n| P-0002 | far | — | TRANSCRIBED | C-0001 |\n\n## Biografisk sammanfattning\n\nBefintlig berättelse med förbehåll.\n');
 fs.writeFileSync(path.join(dir,pr),'# Forskningsprofil\n\n- Identitetsgranskning: GODKÄND\n- Kontraktsgranskning: UNDERKÄND\n\n## Identitetsbedömning\n\nIdentiteten är bedömd separat.\n\n## Livsteman\n\n| Tema | Bedömning | Omfång | Belägg |\n|---|---|---|---|\n| BO | ÖPPET | Hemvist behöver prövas. | C-0001 |\n\n## Forskningsfrågor\n\n### Q-01: Vilken ålder?\n\n- Slutsatsläge: ÖPPEN.\n- Omfång: endast kolumn27/28.\n\n## Källvägar\n\n### KP-01: Rätt födelsebok\n\n- Undersökt omfång och utfall: EJ UNDERSÖKT\n- Wotan: EJ BESLUTAT UTFÖRANDE\n\n#### KP-01: Äldre länkankare\n\nDetta gamla ankare bevaras inom den omdöpta källvägen.\n\n## Kontraktsgranskning\n\n| Krav | Bedömning | Motivering |\n|---|---|---|\n| PK-08 | EJ STYRKT | En genomförbar passage kvarstår. |\n');
 const base=path.join(dir,'baseline'),manifest=await snapshot(dir,base);const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());importBaseline(db,base);
 const docs=[pp,pr].map(p=>db.prepare('SELECT path,sha256 FROM document WHERE path=?').get(p));
 const a=db.prepare("SELECT id FROM unit WHERE legacy_id='A-0001'").get().id;
 const r=db.prepare("SELECT id FROM unit WHERE kind='relation_row' AND raw LIKE '%P-0002%'").get().id;
 const basic=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,disposition:'recorded',rationale:'Syntetiskt prov',...extra});
 applyOperation(db,{id:'setup',actor:'test',reason:'Tidigare införda objekt',changes:[basic('S','source',{title:'S',description:'Syntetiskt'}),basic('R','record',{source_id:'S',record_type:'test',locator:'1',dependence_note:'samma post'}),...['P-0001','P-0002'].map(id=>basic(id,'person',{display_name:id},{origins:[{unit:a}]})),basic('O-old','observation',{record_id:'R',mention_id:null,property:'age',value_literal:'27/28',value_json:{selected:null,alternatives:[27,28]}})]});
 const review={person:'P-0001',documents:docs,readingNote:'Ålder väljs inte. Identitets- och livsbildsgranskning är skilda.',changes:[
  {...basic('E','event',{event_type:'birth',date_json:{precision:'year',value:'1900',literal:'1900'},place_id:null,place_role:'församling, inte byggnad'}),origins:['A-0001'],caveat:'Platsen är inte preciserad.'},
  {...basic('EP','participation',{event_id:'E',person_id:'P-0001',mention_id:null,role:'principal'}),origins:['A-0001'],caveat:'Deltagandets eget förbehåll.'},
  {...basic('REL','relation',{from_person:'P-0002',to_person:'P-0001',relation_type:'parent',nature:'recorded_parent',date_json:{precision:'unknown',literal:'ej angivet'}}),origins:[r],caveat:'Ingen biologisk art antas.'},
  {...basic('REL-qualification','fact',{subject_id:'REL',property:'record_wording',value_type:'text',value_json:'far i den angivna posten'}),origins:[r],caveat:'Förbehållet tillhör relationens precisering.'}
 ],reuse:[{object:'O-old',origins:['A-0001'],rationale:'Samma redan införda observation.'},{object:'O-span-old',origins:[{entity:'P-0001',kind:'person',startLine:5,endLine:5},'A-0001'],rationale:'Återbruk även utanför A-/relationsrader ska ha ett kvarvarande delursprung.'}],assertions:[{id:'A-0001',state:'mapped_complete',targets:['E','EP','O-old'],rationale:'Datum, deltagande och åldersfält har skilda mål.'}],relations:[{unit:r,state:'mapped_complete',targets:['REL'],rationale:'Förälder till barn.'}],pending:[{origin:'A-0001',question:'Vad betyder åldersalternativen? Ingen väljs.'}]};
 applyOperation(db,{id:'setup-span',actor:'test',reason:'Tidigare observation utan personkoppling',changes:[{...basic('O-span-old','observation',{record_id:'R',mention_id:null,property:'partial_detail',value_literal:'Bevarad detalj',value_json:{detail:'bevarad'}}),bindings:{R:1}}]});
 if(retired)review.researchState={disposition:'retired',origins:[{entity:'P-0001',kind:'profile',startLine:1,endLine:5}],rationale:'Explicit syntetiskt avvecklingsbeslut; tidigare öppna frågor bevaras som historik.'};
 const cohorts={baseline:manifest.id,groups:[{id:'persons-01',persons:['P-0001'],documents:[pp,pr]}]};
 assert.throws(()=>buildPersons(db,[{...review,assertions:[]}],{cohorts}),/Alla aktuella A-rader/);
 assert.throws(()=>buildPersons(db,[{...review,pending:[{origin:{entity:'C-0001',kind:'citation',startLine:3,endLine:3},question:'Källfråga utan ankare i den granskade personen.'}]}],{cohorts}),/Tolkningsfråga måste förankras/,'Ett beslut utanför kohortens dokument får inte tyst försvinna.');
 const old=db.prepare('SELECT * FROM revision ORDER BY id').all(),op=buildPersons(db,[review],{cohorts});applyOperation(db,op);
 assert.equal(canonical(buildPersons(db,[review],{cohorts})),canonical(op));assert.equal(applyOperation(db,op).unchanged,true);
 assert.deepEqual(db.prepare('SELECT * FROM revision WHERE operation_id<>? ORDER BY id').all(op.id),old);
 const decision=inspect(db,'A-0001').conversionDecisions.find(d=>d.unit_id===a);assert.equal(decision.state,'pending_interpretation');assert.deepEqual(decision.targets,['E','EP','O-old','O-span-old']);
 const view=personView(db,'P-0001');assert.equal(view.observations.length,2);assert.equal(view.observations[0].object_id,'O-old');assert.equal(view.observations[0].mention_id,null);assert.equal(view.facts.length,0);
 const partial=inspect(db,'O-span-old').conversionOrigins;assert.equal(partial.length,2);const prose=partial.find(x=>x.start_line===5);assert.equal(prose.state,'preserved_text');assert.equal(prose.end_line,5);assert.ok(partial.some(x=>x.state==='pending_interpretation'));
 assert.equal(personView(db,'P-0002').relations[0].object_id,view.relations[0].object_id);assert.equal(view.relations[0].from_person,'P-0002');
 assert.deepEqual(personView(db,'P-0002').relations[0].qualifications,view.relations[0].qualifications);assert.equal(view.relations[0].qualifications[0].object_id,'REL-qualification');assert.match(renderPerson(view),/Förbehållet tillhör relationens precisering/);
 assert.equal(view.events[0].caveat,'Platsen är inte preciserad.');assert.equal(view.events[0].participation.caveat,'Deltagandets eget förbehåll.');
 assert.equal(view.questions[0].outcome,'ÖPPEN.');assert.equal(view.research.questions[0].outcome_code,'open');
 assert.equal(view.research.questions[0].active,!retired);assert.equal(view.questions[0].disposition,retired?'retired':'recorded');
 assert.equal(view.research.paths[0].disposition,retired?'retired':'recorded');
 assert.equal(view.research.themes.length,1);assert.equal(view.research.paths.length,1);assert.equal(view.research.requirements[0].outcome,'EJ STYRKT');assert.match(view.research.paths[0].body,/EJ BESLUTAT UTFÖRANDE/);
 assert.match(view.research.paths[0].body,/Äldre länkankare/);
 const alias=db.prepare("SELECT id FROM unit WHERE kind='source_path' AND json_extract(parsed_json,'$.level')=4").get();
 assert.equal(db.prepare('SELECT state FROM current_unit_decision WHERE unit_id=?').get(alias.id).state,'mapped_complete');
 assert.equal(db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=?').get(alias.id).target_id,'PATH-P-0001-KP-01');
 assert.match(renderPerson(view),/Källuppgifter i personens underlag/);assert.match(renderPerson(view),/27\/28/);assert.match(renderPerson(view),/Ingen väljs/);assert.equal(inspect(db,'O-old').conversionOrigins.length,1);
 if(!retired){
  const next={...review,changes:[],reuse:[...review.reuse,...review.changes.map(m=>({object:m.id,origins:m.origins,rationale:'Samma tidigare införda objekt.'}))],researchState:{disposition:'retired',origins:[{entity:'P-0001',kind:'profile',startLine:1,endLine:5}],rationale:'Nytt explicit avvecklingsbeslut.'}};
  assert.throws(()=>buildPersons(db,[next],{group:'persons-02',cohorts:{...cohorts,groups:[{...cohorts.groups[0],id:'persons-02'}]}}),/forskningsobjekt kräver uttrycklig omprövning/,'Samma råtext får inte göra ett ändrat avvecklingsbeslut osynligt vid återbruk.');
  // En redan införd pilotprofil ska däremot kunna avvecklas med uttryckliga
  // revisioner inom samma personoperation. Råtext och äldre version består.
  const research=op.changes.filter(c=>['assessment','question'].includes(c.kind));
  const revised={...next,changes:research.map(c=>({id:c.id,kind:c.kind,data:c.data,
   revises:1,disposition:'retired',evidenceStatus:null,
   rationale:'Uttrycklig avveckling av tidigare införd forskningsrepresentation.',
   origins:c.origins.map(o=>o.unit)}))};
  const nextOptions={group:'persons-02',cohorts:{...cohorts,groups:[{...cohorts.groups[0],id:'persons-02'}]}};
  const wrong=structuredClone(revised);wrong.changes[0].data.body='En annan text än det bevarade underlaget.';
  assert.throws(()=>buildPersons(db,[wrong],nextOptions),/Gemensamt objekt kräver saklig avstämning/);
  const stale=structuredClone(revised);stale.changes[0].revises=0;
  assert.throws(()=>buildPersons(db,[stale],nextOptions),/explicit revises/);
  const retirement=buildPersons(db,[revised],nextOptions);
  applyOperation(db,retirement);
  assert.equal(applyOperation(db,retirement).unchanged,true);
  assert.equal(canonical(buildPersons(db,[revised],nextOptions)),canonical(retirement));
  for(const c of research){
   const current=readCurrent(db,c.id);
   assert.equal(current.version,2);assert.equal(current.disposition,'retired');
   assert.equal(current.body,c.data.body);assert.equal(current.outcome,c.data.outcome);
   assert.equal(db.prepare('SELECT disposition FROM revision WHERE object_id=? AND version=1').get(c.id).disposition,'recorded');
  }
  assert.equal(personView(db,'P-0001').research.questions[0].active,false);
  assert.equal(readCurrent(db,'P-0001').disposition,'recorded','Forskningsavveckling avvisar inte personen.');
 }
 assert.equal(verifyDB(db).ok,true);const data=exportData(db);restore(data,path.join(dir,'restored.sqlite'));const restored=openDB(path.join(dir,'restored.sqlite'));assert.equal(canonical(exportData(restored)),canonical(data));restored.close();
});

test('personvyn visar återbrukade fakta som separat kontext med verkligt ämne utan dubblering',async t=> {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-context-facts-'));
 fs.mkdirSync(path.join(dir,'genealogy/people'),{recursive:true});
 for(const [person,assertion] of [['P-0001','A-0001'],['P-0002','A-0002']]) {
  fs.writeFileSync(path.join(dir,`genealogy/people/${person}-test.md`),`# ${person}: Test\n\n## Påståenden\n\n| ID | Påstående | Status | Tillförlitlighet | Belägg | Kommentar |\n|---|---|---|---|---|---|\n| ${assertion} | Familjekontext. | TRANSCRIBED | medel | C-0001 | Flera personers uppgifter. |\n`);
 }
 const base=path.join(dir,'baseline');await snapshot(dir,base);
 const db=openDB(path.join(dir,'db.sqlite'),{create:true});
 t.after(()=>{db.close();fs.rmSync(dir,{recursive:true,force:true});});
 importBaseline(db,base);
 const first=db.prepare("SELECT id FROM unit WHERE legacy_id='A-0001'").get().id;
 const other=db.prepare("SELECT id FROM unit WHERE legacy_id='A-0002'").get().id;
 const basic=(id,kind,data,unit=other,extra={})=>({id,kind,data,expectedVersion:null,disposition:'recorded',rationale:'Avgränsat syntetiskt läsvyprov.',origins:[{unit}],...extra});
 const fact=(id,subject,unit=other,extra={})=>basic(id,'fact',{subject_id:subject,property:'family_context',value_type:'structured',value_json:{birth_reported:'1858-04-20',death_reported:'1861-11-16'}},unit,extra);
 const relation=(id,from,to)=>basic(id,'relation',{from_person:from,to_person:to,relation_type:'sibling',nature:'recorded_sibling',date_json:{precision:'unknown',literal:'Ej angivet'}});
 applyOperation(db,{id:'context-setup',actor:'test',reason:'Fakta som redan finns innan återbruket.',changes:[
  ...['P-0001','P-0002','P-0003','P-0004'].map(id=>basic(id,'person',{display_name:id})),
  basic('S','source',{title:'Provkälla',description:'Syntetiskt'}),
  basic('R','record',{source_id:'S',record_type:'test',locator:'1',dependence_note:'Samma post'}),
  basic('M','mention',{record_id:'R',name_literal:'Källnamn',role_literal:''}),
  basic('ID','identity',{mention_id:'M',person_id:'P-0001',decision:'accepted'},other,{disposition:'accepted'}),
  relation('REL-own','P-0001','P-0004'),relation('REL-other','P-0002','P-0003'),
  basic('E','event',{event_type:'residence',date_json:{precision:'year',value:'1861',literal:'1861'},place_id:null,place_role:'registered_residence'}),
  basic('EP','participation',{event_id:'E',person_id:'P-0001',mention_id:null,role:'principal'}),
  fact('F-own','P-0001',first),fact('F-own-mention','M',first),
  fact('F-own-relation','REL-own',first),fact('F-own-event','E',first),
  fact('F-context-origin','REL-other',first,{caveat:'Syskonets data är kontext, inte läsarpersonens födelse eller död.'}),
  fact('F-context-target','REL-other',other,{caveat:'Återbruk av en flerpostsbedömning; ingen extra oberoende källa.'}),
  fact('F-context-both','P-0003',first),fact('F-unlinked','P-0003')
 ]});
 const targetIds=['F-context-target','F-context-both','F-own','F-own-mention','F-own-relation','F-own-event'];
 const reuse={id:'context-reuse',actor:'test',reason:'Återbruk på en annan persons aktuella rad.',changes:[],unitDecisions:[{
  unit:first,expectedVersion:null,state:'mapped_complete',target:targetIds[0],targets:targetIds,rationale:'Samma fakta behåller sina verkliga ämnen.'
 }]};
 applyOperation(db,reuse);
 const view=personView(db,'P-0001');
 assert.deepEqual((view.contextFacts??[]).map(f=>f.object_id),['F-context-both','F-context-origin','F-context-target'],
  'Både råursprung och aktuellt återbruk ska föra in kontext, men egna fakta/preciseringar och orelaterade fakta ska uteslutas.');
 assert.deepEqual(view.facts.map(f=>f.object_id),['F-own','F-own-mention']);
 assert.equal(view.relations[0].qualifications[0].object_id,'F-own-relation');
 assert.equal(view.events[0].qualifications[0].object_id,'F-own-event');
 const context=view.contextFacts.find(f=>f.object_id==='F-context-target');
 assert.equal(context.subject_id,'REL-other');assert.equal(context.revision_id,'F-context-target@1');
 assert.ok(context.origins.every(o=>o.document_path.includes('P-0002')),'Återbruk ska inte skriva om det äldre faktats ursprung.');
 const rendered=renderPerson(view),section=rendered.split('## Kontext från personens underlag\n')[1]?.split('\n## ')[0];
 assert.ok(section);assert.match(section,/Ämne: REL-other/);
 assert.match(section,/Syskonets data är kontext, inte läsarpersonens födelse eller död/);
 assert.match(section,/Återbruk av en flerpostsbedömning/);
 for(const id of [...targetIds,'F-context-origin'])assert.equal(rendered.split(`— ${id}\n`).length-1,1,`${id} ska visas en gång.`);
 assert.doesNotMatch(rendered,/F-unlinked/);
 // En ersatt målmappning ger inte en evig kontextlänk; självständiga ursprung består.
 applyOperation(db,{...reuse,id:'context-replace',unitDecisions:[{...reuse.unitDecisions[0],expectedVersion:1,target:'F-own',targets:['F-own']}]});
 assert.deepEqual(personView(db,'P-0001').contextFacts.map(f=>f.object_id),['F-context-both','F-context-origin']);
 assert.equal(inspect(db,'F-context-target').currentVersion,1,'Vyn och återbruket får inte kopiera eller revidera faktat.');
 assert.equal(verifyDB(db).ok,true);
});


test('icke-personakters historiska profiler förblir skilda från målpersonens aktuella forskning',async t=> {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-non-person-'));
 t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 for(const sub of ['people','research-profiles'])fs.mkdirSync(path.join(dir,'genealogy',sub),{recursive:true});
 const people=['P-0001','P-0003'];
 for(const id of people) {
  fs.writeFileSync(path.join(dir,`genealogy/people/${id}-test.md`),`# ${id}: Gammal akt\n\n## Identitet\n\nAvvecklad akt.\n\n## Biografisk sammanfattning\n\nGammal berättelse för ${id}.\n`);
  fs.writeFileSync(path.join(dir,`genealogy/research-profiles/${id}.md`),`# Forskningsprofil för ${id}\n\n- Identitetsgranskning: GODKÄND\n\n## Forskningsfrågor\n\n### Q-01: Gammal fråga\n\n- Slutsatsläge: ÖPPEN\n`);
 }
 const base=path.join(dir,'baseline'),manifest=await snapshot(dir,base);
 const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());importBaseline(db,base);
 const origin=db.prepare("SELECT id FROM unit WHERE owner_id='P-0001' AND kind='section' LIMIT 1").get().id;
 const basic=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,disposition:'recorded',rationale:'Syntetiskt beslutat fall',origins:[{unit:origin}],...extra});
 applyOperation(db,{id:'setup',actor:'test',reason:'En verklig person och två olika avvecklingsbeslut',changes:[
  basic('P-0002','person',{display_name:'Verklig person'}),
  basic('ASSESSMENT-P-0002','assessment',{subject_id:'P-0002',criteria:'current_research',outcome:'UNDERKÄND',body:'Aktuell prövning.'}),
  basic('BIO-P-0002','narrative',{subject_id:'P-0002',title:'Aktuell berättelse',markdown:'Aktuell berättelse.'}),
  basic('IMPORT-P-0001','assessment',{subject_id:'P-0002',criteria:'legacy_dossier_identity_import/1',outcome:'same_identity',body:'Dubblett.'}),
  basic('IMPORT-P-0003','assessment',{subject_id:'P-0002',criteria:'legacy_dossier_identity_import/1',outcome:'historical_proposal',body:'Avvisad läsning, inte en annan personidentitet.'})
 ],mappings:[
  {id:'MAP-1',legacyId:'P-0001',target:'P-0002',type:'same_identity',unit:origin,rationale:'Explicit sammanföring.'},
  {id:'MAP-3',legacyId:'P-0003',target:'P-0002',type:'archival_reference',unit:origin,rationale:'Enbart historisk läskontext.'}
 ]});
 const reviews=people.map(id=>({person:id,documents:db.prepare('SELECT d.path,d.sha256 FROM document d JOIN legacy_entity e ON e.document_path=d.path WHERE e.id=?').all(id),readingNote:'Tidigare övergiven akt, inte självständig aktuell person.',changes:[],reuse:[],assertions:[],relations:[],pending:[],researchState:{disposition:'retired',rationale:'Separat beslutad avveckling.',origins:[{entity:id,kind:'person',startLine:5,endLine:5}]}}));
 const cohorts={baseline:manifest.id,groups:[{id:'persons-01',persons:people,documents:reviews.flatMap(r=>r.documents.map(d=>d.path))}]};
 assert.throws(()=>buildPersons(db,reviews.map((r,i)=>i?r:{...r,researchState:undefined}),{cohorts}),/Icke-personakt kräver/);
 assert.throws(()=>buildPersons(db,reviews.map((r,i)=>i?r:{...r,changes:[basic(r.person,'person',{display_name:'Falsk person'})]}),{cohorts}),/får inte återuppstå/);
 const prior=canonical(exportData(db)),request=buildPersons(db,reviews,{cohorts});
 const currentBefore=readCurrent(db,'ASSESSMENT-P-0002'),bioBefore=readCurrent(db,'BIO-P-0002');
 applyOperation(db,request);
 for(const id of people) {
  assert.equal(readCurrent(db,id),null,'Ingen person eller ersättningsidentitet skapas.');
  const view=personView(db,id);assert.equal(view.person,null);assert.equal(view.research.questions.length,1);
  assert.equal(view.research.questions[0].active,false);assert.equal(view.research.questions[0].subject_id,'IMPORT-'+id);
  assert.equal(view.research.reviews[0].disposition,'retired');assert.equal(view.narratives[0].disposition,'retired');
  assert.match(view.narratives[0].title,/Historik från avvecklad akt/);assert.match(renderPerson(view),/Gammal berättelse/);
 }
 assert.deepEqual(readCurrent(db,'ASSESSMENT-P-0002'),currentBefore);assert.deepEqual(readCurrent(db,'BIO-P-0002'),bioBefore);
 const target=personView(db,'P-0002');assert.equal(target.research.questions.length,0);assert.equal(target.narratives.length,1);
 assert.ok(!target.research.reviews.some(r=>r.object_id==='ASSESSMENT-P-0001'||r.object_id==='ASSESSMENT-P-0003'));
 assert.equal(db.prepare("SELECT count(*) n FROM current_revision WHERE kind='person'").get().n,1);
 assert.equal(db.prepare("SELECT count(*) n FROM legacy_mapping WHERE legacy_id='P-0003' AND mapping_type='same_identity'").get().n,0);
 assert.equal(canonical(buildPersons(db,reviews,{cohorts})),canonical(request));assert.equal(applyOperation(db,request).unchanged,true);
 assert.equal(verifyDB(db).ok,true);assert.notEqual(canonical(exportData(db)),prior);
 const data=exportData(db),restoredPath=path.join(dir,'restored.sqlite');restore(data,restoredPath);
 const restored=openDB(restoredPath);assert.equal(canonical(exportData(restored)),canonical(data));restored.close();
});
