import assert from 'node:assert/strict';
import {head} from '../lib/domain.mjs';
import {sha} from '../lib/archive.mjs';

const path='genealogy/citations/C-0976-ekholm-alund-vigsel-1903-adolf-fredrik.md';
const sourceHash='dc1d302a68e85f577b10109b2a8e42c9c2d0795d178f2d6664548e0658452f60';
const record='R-C0976-banns86';
const days=['05','12','19'];
const eventId=day=>`E-banns-P-0016-P-0532-1903-04-${day}`;
const factId=day=>`F-T0663-banns-${day}-month-interpretation`;
const reason='C0976:s hela text skiljer inledningens aprilnormalisering från fältets 5,12,19—03, där månaden uttryckligen inte är utskriven. Den positiva lysningen består; exakt april är en bevarad tolkning, inte ett avläst exakt datum.';
const caveat='Lysningspost86 i E I/17, år1903. Månad ej utskriven enligt C0976:s uttryckliga läsreservation. April är den äldre tolkningen mot vigsel1903-05-01 och söndagar; ingen ny originalbildsläsning. Det historiska objekt-id:ts 04 är ingen ny datumuppgift.';

function change(db,id){
 const h=head(db,id);assert(h,id);const {revision_id,...data}=db.prepare(`SELECT * FROM ${h.kind} WHERE revision_id=?`).get(h.id);
 for(const key of Object.keys(data))if(key.endsWith('_json')&&data[key]!==null)data[key]=JSON.parse(data[key]);
 return {id,kind:h.kind,expectedVersion:h.version,data,disposition:h.disposition,evidenceStatus:h.evidence_status,rationale:h.rationale,caveat:h.caveat,
  origins:db.prepare('SELECT unit_id AS unit,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id').all(h.id),
  evidence:db.prepare('SELECT b.object_id AS object,b.version,d.role,d.note FROM dependency d JOIN revision b ON b.id=d.basis_revision_id WHERE d.revision_id=? ORDER BY b.id,d.role').all(h.id)};
}

// Explicit, bounded proposal. No apply, source editing or inferred new dates.
export function buildBannsReview(db){
 const doc=db.prepare('SELECT * FROM document WHERE path=?').get(path);assert.equal(doc?.sha256,sourceHash);assert.equal(sha(doc.text),sourceHash);
 assert(doc.text.includes('månaden i'));assert(doc.text.includes('står inte utskriven'));
 const span={path,sha256:sourceHash,start:0,end:doc.bytes,owner:'C-0976',section:'Hela C0976 inklusive senare reservationer'};
 span.id=sha(`${path}\0${sourceHash}\0curated_span\0${span.start}\0${span.end}`);
 const origin={unit:span.id,coverage:'partial',note:'Hela texten läst, men denna rättelse gäller endast lysningsdatumens källtext/tolkning och den gemensamma registreringskedjan.'};
 const changes=[],dependencyReviews=[];
 const r=head(db,record);assert.equal(r.version,1);
 for(const day of days){
  const id=eventId(day),e=change(db,id);assert.equal(e.expectedVersion,1);assert.equal(e.kind,'event');assert.equal(e.data.date_json.value,`1903-04-${day}`);
  e.data.event_type='banns';e.data.date_json={precision:'year',value:'1903',literal:`${Number(day)} — 03; månad ej utskriven`};e.rationale=reason;e.caveat=caveat;
  if(!e.origins.some(o=>o.unit===span.id))e.origins.push(origin);
  changes.push(e);
  const affected=db.prepare(`WITH RECURSIVE affected(id) AS (SELECT revision_id FROM dependency WHERE basis_revision_id=? UNION SELECT d.revision_id FROM dependency d JOIN affected a ON a.id=d.basis_revision_id)
   SELECT DISTINCT c.object_id FROM affected a JOIN revision old ON old.id=a.id JOIN current_revision c ON c.object_id=old.object_id ORDER BY c.object_id`).all(`${id}@1`).map(x=>x.object_id);
  const expected=['P-0016','P-0532'].map(p=>`EP-${id}-${p}-subject`).sort();assert.deepEqual(affected,expected,`Lysningens beroenden har ändrats: ${id}`);
  for(const epId of expected){
   const ep=change(db,epId);assert.equal(ep.expectedVersion,1);assert.equal(ep.data.event_id,id);
   ep.evidence=ep.evidence.map(b=>b.object===id?{...b,version:2,note:'Individuellt omprövat deltagande: samma namngivna par och lysningspost; datumets månad är nu reserverad.'}:b);
   ep.bindings={[id]:2};ep.rationale=`${ep.data.person_id} namnges fortsatt i samma lysningspost. Månadspreciseringens rättelse ändrar inte deltagaridentiteten eller den accepterade lysningen.`;ep.caveat=caveat;
   changes.push(ep);dependencyReviews.push({object:epId,basis:id,decision:'rebound_after_individual_review',rationale:ep.rationale});
  }
  changes.push({id:factId(day),kind:'fact',expectedVersion:null,disposition:'recorded',evidenceStatus:'INFERRED',rationale:reason,caveat,
   data:{subject_id:id,property:'date_interpretation',value_type:'structured',value_json:{persons:['P-0016','P-0532'],source_literal:'Lyses Söndagarne den 5, 12, 19 — 03',own_day:Number(day),year:1903,month_written:false,legacy_interpretation:`1903-04-${day}`,interpretation_status:'inferred_month_not_direct_transcription',wedding_date:'1903-05-01',argument:'Äldre text kopplar de tre söndagarna till vigseln1maj. Kalenderargumentet ensamt ger inte en unik månad: även juli1903 har söndagar5,12,19; vigselns placering gör april rimlig men ingen månad har lästs ut här.',new_original_reading:false}},
   origins:[origin],evidence:[{object:record,version:r.version,role:'supports',note:'Samma registreringskedja, inte ytterligare oberoende källa.'},{object:id,version:2,role:'context',note:'Bevarar äldre månadstolkning som uttrycklig kvalificering av den reviderade händelsen.'}]});
 }
 const units=new Set();for(const day of days)for(const u of db.prepare('SELECT unit_id FROM current_unit_target WHERE target_id=?').all(eventId(day)))units.add(u.unit_id);
 const unitDecisions=[...units].sort().map(unit=>{
  const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(unit);
  const targets=db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=? ORDER BY target_id').all(unit).map(t=>t.target_id);
  for(const day of days)if(targets.includes(eventId(day)))targets.push(factId(day));
  return {unit,expectedVersion:d.version,state:d.state,target:d.target_id,targets:[...new Set(targets)].sort(),question:d.question,rationale:d.rationale+' T0663: lysningarnas datum har versionsrättats; separat F bevarar april som uttrycklig tolkning. Befintlig frågas avgränsning består.'};
 });
 if(!db.prepare('SELECT 1 FROM current_unit_decision WHERE unit_id=?').get(span.id))unitDecisions.push({unit:span.id,expectedVersion:null,state:'preserved_text',target:factId('05'),targets:days.map(factId),question:'',rationale:'Hela citationstexten är bevarad. Dessa mål täcker endast den avgränsade datumrättelsen; övriga uppgifter behåller sina befintliga objekt och textutfall.'});
 return {changes,spans:[span],unitDecisions,dependencyReviews,review:{source:{path,sha256:sourceHash},events:days.map(eventId),positive_marriage_unchanged:'1903-05-01',old_versions_preserved:true}};
}
