import {sha,canonical} from './archive.mjs';

export function migrationReport(db) {
  const batch=db.prepare('SELECT id FROM import_batch').get();
  if(!batch)throw Error('Importbas saknas');
  const people=db.prepare("SELECT id,document_path FROM legacy_entity WHERE kind='person' ORDER BY id").all();
  const citations=db.prepare("SELECT id,document_path FROM legacy_entity WHERE kind='citation' ORDER BY id").all();
  const sources=db.prepare("SELECT id,document_path FROM legacy_entity WHERE kind='source' ORDER BY id").all();
  const groups=[],byOwner=new Map();
  const chunks=(rows,size)=>Array.from({length:Math.ceil(rows.length/size)},(_,i)=>rows.slice(i*size,(i+1)*size));
  for(const [i,rows] of chunks(people,50).entries()) {
    const id=`persons-${String(i+1).padStart(2,'0')}`;
    groups.push({id,kind:'person_core',persons:rows.map(r=>r.id),citations:[],sources:[],documents:[],unitCounts:{}});
    for(const r of rows)byOwner.set(r.id,id);
  }
  const citationChunks=chunks(citations,200),sourceChunks=chunks(sources,Math.ceil(sources.length/citationChunks.length));
  for(const [i,rows] of citationChunks.entries()) {
    const id=`evidence-${String(i+1).padStart(2,'0')}`,ss=sourceChunks[i]??[];
    groups.push({id,kind:'evidence',persons:[],citations:rows.map(r=>r.id),sources:ss.map(r=>r.id),documents:[],unitCounts:{}});
    for(const r of [...rows,...ss])byOwner.set(r.id,id);
  }
  groups.push({id:'research-context',kind:'research_context',persons:[],citations:[],sources:[],documents:[],unitCounts:{}});
  groups.push({id:'archive-context',kind:'preserved_context',persons:[],citations:[],sources:[],documents:[],unitCounts:{}});
  const groupMap=new Map(groups.map(g=>[g.id,g]));
  const documents=db.prepare(`SELECT d.path,d.sha256,d.bytes,e.id AS owner_id FROM document d
    LEFT JOIN legacy_entity e ON e.document_path=d.path ORDER BY d.path`).all();
  const documentGroups=new Map();
  for(const d of documents) {
    const group=byOwner.get(d.owner_id)??(d.path.startsWith('genealogy/')?'research-context':'archive-context');
    documentGroups.set(d.path,group);groupMap.get(group).documents.push(d.path);
  }
  const unitRows=db.prepare(`SELECT u.id,u.document_path,u.kind,u.legacy_id,u.owner_id,u.historical,decision.state AS decided_state,decision.rationale,decision.question,
    EXISTS(SELECT 1 FROM origin o JOIN current_revision r ON r.id=o.revision_id WHERE o.unit_id=u.id AND o.coverage='complete') AS complete,
    EXISTS(SELECT 1 FROM origin o JOIN current_revision r ON r.id=o.revision_id WHERE o.unit_id=u.id AND o.coverage='partial') AS partial
    FROM unit u LEFT JOIN current_unit_decision decision ON decision.unit_id=u.id ORDER BY u.id`).all();
  const unitStates={},units=[];
  for(const u of unitRows) {
    const group=documentGroups.get(u.document_path);
    if(!group)throw Error('Enhet utan dokumentgrupp');
    const state=u.decided_state??(u.complete?'mapped_complete':u.partial?'mapped_partial':u.historical?'preserved_history':group==='archive-context'?'preserved_context':'pending_interpretation');
    const reason=u.rationale?u.rationale+(u.question?' Återstående fråga: '+u.question:''):{mapped_complete:'Hela denna representationsenhet är mappad; det är inget nytt genealogiskt godkännande.',mapped_partial:'Utvalt innehåll är mappat; resten måste läsas tillsammans med förbehåll/rättelser.',preserved_history:'Historiskt avsnitt bevarat ordagrant. Inte aktuella fakta.',preserved_context:'Styrning, äldre genomförande eller kod bevarad som ursprungligt sammanhang.',pending_interpretation:'Exakt bevarat; betydelse och lämplig målrepresentation återstår att fastställa.'}[state];
    units.push({id:u.id,path:u.document_path,kind:u.kind,legacyId:u.legacy_id,group,state,reason});
    unitStates[state]=(unitStates[state]??0)+1;
    const counts=groupMap.get(group).unitCounts;counts[state]=(counts[state]??0)+1;
  }
  const assets=db.prepare('SELECT path,sha256,bytes FROM asset ORDER BY path').all();
  const result={format:'genealogy2-migration/1',baseline:batch.id,
    summary:{documents:documents.length,assets:assets.length,units:units.length,unitStates,domainObjects:db.prepare('SELECT count(*) n FROM object').get().n},
    note:'Enheter inkluderar överlappande avsnitt och tabellrader. Antalen är redovisning, inte procent fullbordad forskning. Media bevaras externt med hash. Grupper anger konverteringsomfång; Wotan äger ordning och status.',
    groups,documents,assets,units};
  return {...result,reportHash:sha(canonical(result))};
}
