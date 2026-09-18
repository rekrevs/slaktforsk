import assert from 'node:assert/strict';
import fs from 'node:fs';
import {migrationReport} from '../lib/migration.mjs';
import {sha,canonical} from '../lib/archive.mjs';
import {head} from '../lib/domain.mjs';

// Representation accounting, not a genealogical review. Only undecided units
// are assigned here; existing concrete interpretation questions stay intact.
export function buildContextDecisions(db){
 const report=migrationReport(db),groups=new Map(report.units.map(u=>[u.id,u.group]));
 const orphanReview=JSON.parse(fs.readFileSync(new URL('./T-0663-unused-spans-review.json',import.meta.url)));
 assert.equal(orphanReview.entries.length,5);
 const orphans=new Map(orphanReview.entries.map(e=>[e.unit,e]));
 const missing=db.prepare(`SELECT u.* FROM unit u LEFT JOIN current_unit_decision d ON d.unit_id=u.id WHERE d.id IS NULL ORDER BY u.id`).all();
 const counts={},unitDecisions=[];
 for(const u of missing){
  const group=groups.get(u.id);assert(group,u.id);
  if(orphans.has(u.id)){
   const reviewed=orphans.get(u.id);assert.equal(u.document_path,reviewed.document.path);assert.equal(sha(u.raw),reviewed.rawHash);
   assert.equal(db.prepare('SELECT sha256 FROM document WHERE path=?').get(u.document_path).sha256,reviewed.document.sha256);
   assert.equal(db.prepare('SELECT count(*) n FROM origin WHERE unit_id=?').get(u.id).n,0);
   for(const target of reviewed.currentTargets){
    const current=head(db,target.id);assert.equal(current.id,target.revision);
    const {revision_id,...payload}=db.prepare(`SELECT * FROM ${current.kind} WHERE revision_id=?`).get(current.id);
    assert.equal(canonical(payload),canonical(target.payload),`Ändrat underlag för byggspann ${u.id}/${target.id}`);
   }
   for(const previous of reviewed.existingCoverageUnits){const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(previous.id);assert.equal(d.state,previous.state);assert.equal(d.question,previous.question);}
   unitDecisions.push(reviewed.proposedDecision);counts[`${group}/preserved_text`]=(counts[`${group}/preserved_text`]??0)+1;continue;
  }
  const targets=db.prepare(`SELECT DISTINCT r.object_id FROM origin o JOIN current_revision r ON r.id=o.revision_id WHERE o.unit_id=? ORDER BY r.object_id`).all(u.id).map(r=>r.object_id);
  let state,rationale;
  if(group==='archive-context'){
   state='preserved_history';rationale='Fryst projekt-/kod-/Wotanunderlag från importögonblicket, ordagrant tillgängligt via context. Historisk styrning och utförandestatus; nuvarande instruktioner och Wotan gäller. Inte konverterat till nya personfakta eller en parallell arbetskö.';
  }else if(group==='research-context'){
   state='preserved_text';rationale='Äldre forskningssammanhang bevarat ordagrant med dokumenthash och navigationsanknytningar i context: metoder, kontrakt, daterad logg, indikator eller utgåveunderlag enligt katalogens dokumentklass. Textbevarande räknas inte som full semantisk konvertering. Aktuella personfrågor och källvägar läses i de individuellt överförda nativeprofilerna; utförandestatus i nuvarande Wotan.';
  }else{
   assert.equal(u.kind,'curated_span',`Oväntad oprövad kärnenhet: ${u.document_path}/${u.kind}/${u.id}`);
   state='preserved_text';rationale='Senare tillagt överlappande ursprungsspann. Originaldokumentets tidigare enhetsbeslut och mål består; denna text finns ordagrant och de uttryckliga nativeanknytningarna redovisas. Spannets hela bredd upphöjs inte till en ny semantisk uppgift eller en ny oläst källa.';
   assert(targets.length>0,`Ursprungsspann utan aktuellt mål behöver individuell avstämning: ${u.id}`);
  }
  unitDecisions.push({unit:u.id,expectedVersion:null,state,target:targets[0]??null,targets,question:'',rationale});
  const key=`${group}/${state}`;counts[key]=(counts[key]??0)+1;
 }
 assert.equal(unitDecisions.filter(d=>orphans.has(d.unit)).length,5);
 return {id:'T-0663/context-accounting-v1',actor:'Codex',reason:'Slutavstämning av återstående representationsenheter: historisk kontext, synligt textmaterial och överlappande ursprungsspann. Ingen forskningsstatus eller befintlig konkret tolkningsfråga ändras.',changes:[],unitDecisions,review:{counts,unusedSpansReviewHash:sha(canonical(orphanReview)),scope:'Alla vid byggningen beslutslösa importenheter. Endast kontext och kända överlappande kuraterade spann tillåts; oväntad person-/citationskärna stoppar byggningen.'}};
}
