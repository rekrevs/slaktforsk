// New negative receipts are bounded research evidence, never source exhaustion.
const text=x=>typeof x==='string'&&x.trim().length>0;
const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
export function validateSearchMemory(db,change) {
  const fail=message=>{throw Error(`Sökminne ${change.id}: ${message}`);};
  const scope=change.data.scope_json,m=scope?.search_memory;
  if(!object(m)||m.format!=='search-memory/1')fail('search-memory/1 krävs för nytt negativt sökresultat');
  if(!text(scope.description)||!text(scope.query)||!object(scope.bounds)||!Object.keys(scope.bounds).length||Object.values(scope.bounds).some(x=>x==null||x===''||(Array.isArray(x)&&!x.length)||(object(x)&&!Object.keys(x).length)))fail('exakt beskrivning, sökfråga och icke-tomma gränser krävs');
  if(!Array.isArray(m.subjects)||!m.subjects.length||m.subjects.some(id=>!text(id)||!db.prepare('SELECT id FROM object WHERE id=?').get(id)))fail('subjects kräver befintliga objekt');
  const question=change.data.question_id&&db.prepare('SELECT q.subject_id FROM current_revision r JOIN question q ON q.revision_id=r.id WHERE r.object_id=?').get(change.data.question_id);
  if(!question||!m.subjects.includes(question.subject_id))fail('fråga och dess verkliga subject_id måste ingå');
  if(!text(m.performed_at)||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(m.performed_at)||Number.isNaN(Date.parse(m.performed_at)))fail('performed_at kräver ISO-tid med tidszon');
  // Date.parse normalizes impossible calendar dates; reject those explicitly.
  const [year,month,day]=m.performed_at.slice(0,10).split('-').map(Number);
  const days=[31,(year%4===0&&(year%100!==0||year%400===0))?29:28,31,30,31,30,31,31,30,31,30,31];
  if(month<1||month>12||day<1||day>days[month-1]||Number(m.performed_at.slice(11,13))>23||Number(m.performed_at.slice(14,16))>59||Number(m.performed_at.slice(17,19))>59)fail('ogiltigt kalenderdatum eller klockslag');
  if(!text(m.method))fail('faktisk sökmetod krävs');
  const material=m.material;
  if(!object(material)||!text(material.identifier)||!Number.isSafeInteger(material.source_version)||material.source_version<1)fail('materialidentifierare och positiv source_version krävs');
  const source=db.prepare('SELECT version,kind FROM current_revision WHERE object_id=?').get(change.data.source_id);
  if(!source||source.kind!=='source'||source.version!==material.source_version)fail('material.source_version måste motsvara aktuell källa');
  if(!(change.evidence??[]).some(e=>e.object===change.data.source_id&&e.version===material.source_version&&['supports','context'].includes(e.role)))fail('källan/versionen måste vara explicit supports/context-belägg');
  const provider=material.provider_version;
  if(!object(provider)||(provider.value===null?!text(provider.unknown_reason):!text(provider.value)))fail('leverantörsversion eller motiverat uttryckligt okänd krävs');
  const snapshot=material.snapshot;
  if(!object(snapshot)||(snapshot.sha256===null?!text(snapshot.unavailable_reason):typeof snapshot.sha256!=='string'||! /^[a-fA-F0-9]{64}$/.test(snapshot.sha256)||!text(snapshot.reference)))fail('snapshot-hash/referens eller motiverat otillgänglig krävs');
  if(!object(m.coverage)||m.coverage.completed!==true||!text(m.coverage.limitations))fail('genomfört exakt omfång och begränsningar krävs; åtkomsthinder är access_problem');
  if(!Array.isArray(m.reactivation)||!m.reactivation.length||m.reactivation.some(x=>!text(x)))fail('uttryckliga återstartvillkor krävs');
}
