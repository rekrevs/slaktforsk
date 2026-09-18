import assert from 'node:assert/strict';
import fs from 'node:fs';
import {sha,canonical} from '../lib/archive.mjs';
import {head,readCurrent} from '../lib/domain.mjs';
import {buildObservationCorrectionsC,OBSERVATION_C_REVISIONS} from '../migration/T-0663-observation-c.mjs';

const suffixes=['Britta-Anders','Britta-Erics','Kjerstin','Namndeman','Olof'];
const witnessF='F-P-0383-identity_boundary-own-baptism-witnesses';
const scopeF='F-P-0383-source_scope-readings-and-life-limits';
const parentFs=['F-P-0513-source_assessment-witness-count-and-limits','F-P-0514-source_assessment-witness-count-and-limits'];
const loadProposal=()=>JSON.parse(fs.readFileSync(new URL('../migration/T-0663-observation-c-review.json',import.meta.url),'utf8'));
const plain=x=>JSON.parse(JSON.stringify(x));

function source(db,id,kind='citation') {
  const rows=db.prepare('SELECT d.* FROM document d JOIN legacy_entity e ON e.document_path=d.path WHERE e.id=? AND e.kind=?').all(id,kind);
  assert.equal(rows.length,1);return rows[0];
}

function checkSourceBoundaries(db,p) {
  const changes=new Map(p.changes.map(c=>[c.id,c]));
  const value=id=>{assert(changes.has(id),`Förslag saknas ${id}`);return changes.get(id).data.value_json;};
  const c266=source(db,'C-0266').text,c267=source(db,'C-0267').text;
  assert.match(c266,/5\. Arne mellan Vilhelmina och Fredrik; Ada sittande till höger om Fredrik\./);
  assert.match(c266,/7\. Arne, May, Jan-Christer och Anita vid den nybyggda stugan vid Orrestaö\s+1941\./);
  assert.match(c267,/Jan-Christer identifierar på gruppfotot Arne, fyra år, stående i bakre raden/);
  const cabins=value('O-P-0003-C0266-cabins');
  assert(!('familyPhotoYear' in cabins.buildings[0]));assert(!('ownershipProved' in cabins));
  assert.equal(value('F-P-0003-family_account-cabins-and-photo1941').photograph.year,'1941');
  assert.equal(value('F-P-0003-family_account-cabins-and-photo1941').ownership_proven,false);
  const caption=value('O-P-0003-C0266-photo-childhood');
  assert.equal(caption.caption,'Arne mellan Vilhelmina och Fredrik; Ada sittande till höger om Fredrik.');
  assert(!('approximateAge' in caption));assert.doesNotMatch(JSON.stringify(caption),/fyra|stående|Sverker/);
  assert.equal(value('O-P-0003-C0267-photo-childhood-explanation').reported_age,'fyra år');
  const photo=value('F-P-0003-photograph_identification-childhood');
  assert.equal(photo.letter_author,'Jan-Christer Janson');assert.equal(photo.mediator,'Sverker Adam Janson');
  assert.equal(photo.independent_face_analysis,false);
  assert.notEqual(changes.get('O-P-0003-C0266-photo-childhood').data.record_id,changes.get('O-P-0003-C0267-photo-childhood-explanation').data.record_id);

  const c919=source(db,'C-0919').text,c19=source(db,'C-0019').text;
  assert.match(c919,/> 10 \| .*Gunborg Elisabet/);
  assert.match(c19,/familj 1:[\s\S]*?döttrarna Birgit Cecilia och Gunborg Elisabet/);
  const mother=value('O-P-0019-mother-not-named'),mother1930=value('O-P-0019-C0019-mother-not-named');
  assert.equal(mother.named_mother,null);assert.doesNotMatch(mother.scope,/C-0019|1930/);
  assert.match(mother1930.scope,/C-0019.*1930.*familj1/);
  assert.notEqual(changes.get('O-P-0019-mother-not-named').data.record_id,changes.get('O-P-0019-C0019-mother-not-named').data.record_id);
  const maternal=value('F-P-0019-source_scope-mother-two-records');
  assert.equal(maternal.candidate,'P-0117');assert.equal(maternal.candidate_accepted_as_mother,false);
  assert.equal(maternal.mother_unknown_to_contemporaries_proven,false);

  const c911=source(db,'C-0911').text,c910=source(db,'C-0910').text;
  assert.match(c911,/> 9 \| \*\*Elin Augusta Larsson\*\* \| sömmerska/);
  assert.match(c911,/\| 16 \| `Ture Alexius Jaensson`[\s\S]*?14 ³¹\/₁₂/);
  assert.match(c911,/\| 17 \| `h\. Elin Augusta Larsson`/);
  const elin=value('O-P-0043-related125-household_role_report');
  assert.equal(elin.row,9);assert.equal(elin.registered_arrival,'1914-10-15');
  assert.doesNotMatch(JSON.stringify(elin),/sonhustru|1914-12-31|marriage/);
  const elinF=value('F-P-0043-family_context-Elin-household-sequence');
  assert.deepEqual(elinF.later_rows,[16,17]);assert.equal(elinF.registered_marriage,'1914-12-31');
  assert.equal(elinF.physical_move_proven,false);assert.equal(elinF.wedding_place,null);
  assert.equal(readCurrent(db,'O-P-0046-A-4239-marriage_household').record_id,elinF.later_record);
  for(const [n,name,row,nextRow,id] of [[122,'Karl Harry',6,5,'Karl-Harry'],[123,'Karin Elisabet',7,6,'Karin-Elisabet']]) {
    const earlier=value(`O-P-0043-related${n}-household_role_report`),later=value(`O-C0910-${id}-row${nextRow}`);
    assert.equal(earlier.name_literal,name);assert.equal(earlier.row,row);
    assert.equal(earlier.registered_transfer,'1914-10-30');assert.equal(earlier.from_folio,420);
    assert.doesNotMatch(JSON.stringify(earlier),/1918|Elin|Jansson/);
    assert.equal(later.row,nextRow);assert.equal(later.role_literal,'fb.');
    assert.notEqual(changes.get(`O-P-0043-related${n}-household_role_report`).data.record_id,changes.get(`O-C0910-${id}-row${nextRow}`).data.record_id);
    const f=value(`F-P-0043-family_context-${id}-sequence`);
    assert.equal(f.reported_summary_period,'1914–1918');assert.equal(f.registered_anchors[1].own_arrival_date,null);
    assert.equal(f.continuous_physical_care_proven,false);assert.equal(f.biological_parenthood_of_foster_household_proven,false);
  }
  assert.match(c910,/> 5 \| fb\. \*\*Karl Harry Jansson\*\*[\s\S]*?`Son till Elin Augusta Larsson-Jansson`/);
  assert.match(c910,/> 6 \| fb\. \*\*Karin Elisabet\*\*/);
  assert.equal(value('O-C0910-Karl-Harry-row5').mother_note_literal,'Son till Elin Augusta Larsson-Jansson');
  assert(!('mother_note_literal' in value('O-C0910-Karin-Elisabet-row6')));

  const c510=source(db,'C-0510').text;
  assert.match(c510,/Andra hustruns namn läses Lisa Stina Jonsd:r/);
  assert.match(c510,/egen födelsenotis namnger Lisa Stina\s+Larsdotter/);
  const household=value('O-P-0315-C0510-household');
  assert(!('stepmother' in household));assert(!('father' in household));
  assert.equal(household.head_spouse_name_literal,'Lisa Stina Jonsd:r');assert.equal(household.head_spouse_role_literal,'h/2');
  assert.equal(household.departure.book_year,1858);assert.equal(household.departure.destination,null);
  assert.equal(household.own_communion,'1858-08-22');
  assert.equal(JSON.parse(readCurrent(db,'F-P-0315-family_context-six-known-children').value_json).stepmother,'P-0405');
  assert.equal(readCurrent(db,'REL-step-P-0405-P-0315').nature,'recorded_step_parent');

  const c1016=source(db,'C-1016').text;
  assert.match(c1016,/Britta Anders Dotr i Mjöstan\[\?\], Britta Erics Dotr i Kjerrbogärda/);
  assert.match(c1016,/Kjerstin Anders Dotr i Kåsegl\[\?\], Nämndeman i Hattholt\[\?\]/);
  assert.match(c1016,/Olof Anderss\[on\] i Wässenbo/);
  for(const s of suffixes){
    const id=`O-C0848-witness-${s}`,original=db.prepare('SELECT * FROM observation WHERE revision_id=?').get(id+'@1');
    const expected=JSON.parse(original.value_json);assert.equal(expected.kinship_proven,false);delete expected.kinship_proven;
    assert.deepEqual(value(id),expected);assert.equal(changes.get(id).data.value_literal,original.value_literal);
    assert.equal(changes.get(id).data.mention_id,original.mention_id);
  }
  const limits=JSON.parse(readCurrent(db,witnessF).value_json);
  assert.equal(limits.maternal_siblings_not_proven,true);assert.equal(limits.candidate_not_confirmed,true);
  assert.equal(limits.no_Hansson_witness_does_not_exclude_fathers_kin,true);
  assert.equal(limits.explicit_list_Anders_daughters,2);assert.equal(limits.T0170_claim_Anders_daughters,3);
  assert.equal(readCurrent(db,'M-C0848-witness-Namndeman').name_literal,'');
  for(const id of parentFs) {
    const f=readCurrent(db,id),v=JSON.parse(f.value_json);
    assert.equal(v.direct_Anders_bearers,3);assert.deepEqual(v.named_Anders_daughters,['Britta Anders Dotr','Kjerstin Anders Dotr']);
    assert.equal(v.named_Anders_son,'Olof Anderss.');assert.equal(v.named_Erics_daughter,'Britta Erics Dotr');
    assert.equal(v.no_sibling_links,true);assert.equal(v.all_kinship_routes_closed,false);
    assert.equal(v.statistical_excess_over_chance_not_established,true);assert.equal(v.no_Hansson_does_not_exclude_fathers_kin,true);
    assert.equal(v.candidate_fourth,'Johannes Andersson endast om nämndemannen är samma man');
    assert.equal(v.A7591_Erics_is_not_Anders,true);assert.equal(v.A7592_fifth_Anders_count_incorrect,true);
    assert(f.evidence.some(e=>e.basis_revision_id===witnessF+'@1'));
  }
}

function checkOriginsAndPreservation(db,p) {
  const spans=new Map(p.spans.map(s=>[s.id,s]));
  assert.equal(spans.size,p.spans.length);
  for(const s of spans.values()) {
    const doc=db.prepare('SELECT * FROM document WHERE path=?').get(s.path);assert(doc);
    assert.equal(doc.sha256,s.sha256);assert.equal(sha(Buffer.from(doc.text)),s.sha256);
    assert(s.start>=0&&s.end>s.start&&s.end<=doc.bytes);
    assert(Buffer.from(doc.text).subarray(s.start,s.end).toString().trim());
    assert.equal(s.id,sha(`${s.path}\0${s.sha256}\0curated_span\0${s.start}\0${s.end}`));
  }
  for(const c of p.changes)for(const o of c.origins)assert(spans.has(o.unit)||db.prepare('SELECT id FROM unit WHERE id=?').get(o.unit),`Ogiltigt ursprung ${c.id}/${o.unit}`);
  for(const original of p.review.preservedRevisions) {
    const revision=db.prepare('SELECT r.*,o.kind FROM revision r JOIN object o ON o.id=r.object_id WHERE r.id=?').get(original.id);assert(revision);
    const payload=db.prepare(`SELECT * FROM ${revision.kind} WHERE revision_id=?`).get(original.id);
    const origins=db.prepare('SELECT * FROM origin WHERE revision_id=? ORDER BY unit_id').all(original.id);
    const dependencies=db.prepare('SELECT * FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role').all(original.id);
    assert.equal(sha(canonical({revision,payload,origins,dependencies})),original.sha256,`Äldre revision ändrad ${original.id}`);
  }
  for(const d of p.unitDecisions) {
    const old=db.prepare('SELECT * FROM unit_decision WHERE unit_id=? AND version=?').get(d.unit,d.expectedVersion);assert(old);
    for(const [a,b] of [['state','state'],['question','question'],['target','target_id']])assert.equal(d[a],old[b]);
    const oldTargets=db.prepare('SELECT target_id FROM unit_decision_target WHERE decision_id=?').all(old.id);
    for(const {target_id} of oldTargets)assert(d.targets.includes(target_id));
  }
  assert.equal(p.review.alreadyMappedUnits.length,5);
  for(const d of p.review.alreadyMappedUnits) {
    const old=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(d.unit);
    assert.equal(old.state,d.state);assert.equal(old.question,d.question);
    assert(d.targets.includes(witnessF));
    assert(db.prepare('SELECT 1 FROM current_unit_target WHERE unit_id=? AND target_id=?').get(d.unit,witnessF));
  }
}

function checkDependencyReview(db,p,applied) {
  const expected=[];
  for(const s of suffixes)for(const object of [`EP-E-baptism-P-0383-${s}`,witnessF,scopeF,...parentFs])expected.push(`${object}@1|O-C0848-witness-${s}@2`);
  assert.deepEqual(p.dependencyReviews.map(r=>`${r.affected_revision_id}|${r.changed_revision_id}`).sort(),expected.sort());
  assert.equal(new Set(p.dependencyReviews.map(r=>r.affectedObject)).size,9);
  for(const r of p.dependencyReviews) {
    const x=readCurrent(db,r.affectedObject);assert.equal(x.revision_id,r.affected_revision_id);
    const data=db.prepare(`SELECT * FROM ${x.kind} WHERE revision_id=?`).get(x.revision_id);delete data.revision_id;
    for(const k of Object.keys(data))if(k.endsWith('_json')&&data[k]!==null)data[k]=JSON.parse(data[k]);
    assert.equal(sha(canonical(data)),r.retainedPayloadHash);
    assert.deepEqual(plain(db.prepare('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role').all(x.revision_id)),plain(r.retainedEvidenceBindings));
    assert.equal(r.outcome,'retain_existing_revision');assert.match(r.rationale,/äldre beläggsbindningar behålls/);
    if(applied) {
      const requests=db.prepare('SELECT * FROM review_request WHERE affected_revision_id=? AND changed_revision_id=?').all(r.affected_revision_id,r.changed_revision_id);
      assert.equal(requests.length,1,`Exakt omprövningspar saknas ${r.affected_revision_id}/${r.changed_revision_id}`);
      const resolution=db.prepare('SELECT * FROM review_resolution WHERE request_id=?').get(requests[0].id);
      assert(resolution,`Individuell omprövning kvarstår ${requests[0].id}`);
      assert(resolution.rationale.includes(r.rationale),`Sakmotiveringen saknas ${requests[0].id}`);
    }
  }
  if(!applied)for(const id of OBSERVATION_C_REVISIONS) {
    const actual=db.prepare(`WITH RECURSIVE ds(id) AS (SELECT revision_id FROM dependency WHERE basis_revision_id=?
      UNION SELECT d.revision_id FROM dependency d JOIN ds ON d.basis_revision_id=ds.id)
      SELECT DISTINCT cr.id FROM ds JOIN revision r ON r.id=ds.id JOIN current_revision cr ON cr.object_id=r.object_id ORDER BY cr.id`).all(id+'@1').map(x=>x.id);
    assert.deepEqual(actual,p.dependencyReviews.filter(r=>r.changedObject===id).map(r=>r.affectedRevision).sort());
  }
}

export function checkT0663ObservationCPreparation(db,p=buildObservationCorrectionsC(db)) {
  assert.equal(p.changes.length,22);assert.equal(p.changes.filter(c=>c.kind==='fact').length,6);
  assert.equal(p.unitDecisions.length,13);
  assert.equal(p.changes.filter(c=>c.kind==='observation'&&c.expectedVersion===null).length,4);
  assert.deepEqual(p.changes.filter(c=>c.expectedVersion===1).map(c=>c.id).sort(),[...OBSERVATION_C_REVISIONS].sort());
  const proposed=new Map();
  for(const c of p.changes) {
    assert(['observation','fact'].includes(c.kind));assert.equal(head(db,c.id)?.version??null,c.expectedVersion);
    for(const e of c.evidence)assert.equal(e.version,proposed.get(e.object)??head(db,e.object)?.version);
    if(c.kind==='observation') {
      assert.equal(c.bindings[c.data.record_id],head(db,c.data.record_id).version);
      if(c.data.mention_id){assert.equal(readCurrent(db,c.data.mention_id).record_id,c.data.record_id);assert.equal(c.bindings[c.data.mention_id],head(db,c.data.mention_id).version);}
      assert(c.evidence.every(e=>[c.data.record_id,c.data.mention_id].includes(e.object)),'Rå-O har åter fått annat postsammanhang som belägg');
    }
    proposed.set(c.id,(c.expectedVersion??0)+1);
  }
  checkSourceBoundaries(db,p);checkOriginsAndPreservation(db,p);checkDependencyReview(db,p,false);
  assert.equal(p.review.proposalHash,sha(canonical({changes:p.changes,spans:p.spans,unitDecisions:p.unitDecisions,dependencyReviews:p.dependencyReviews})));
  return {ok:true,groups:12,changes:22,revisedObservations:12,newObservations:4,newFacts:6,dependencyPairs:25,retainedDependents:9};
}

// Integration-only: call after native apply and the twenty-five exact review resolutions.
export function checkT0663ObservationCRisks(db,p=loadProposal()) {
  checkSourceBoundaries(db,p);checkOriginsAndPreservation(db,p);checkDependencyReview(db,p,true);
  for(const c of p.changes) {
    const x=readCurrent(db,c.id);assert.equal(x.version,(c.expectedVersion??0)+1);
    assert.equal(x.disposition,c.disposition);assert.equal(x.evidence_status,c.evidenceStatus);
    for(const [key,expected] of Object.entries(c.data))assert.deepEqual(key.endsWith('_json')&&x[key]!==null?JSON.parse(x[key]):x[key],expected,`Fel infört värde ${c.id}/${key}`);
    for(const e of c.evidence)assert(x.evidence.some(actual=>actual.basis_revision_id===`${e.object}@${e.version}`&&actual.role===e.role));
  }
  for(const d of p.unitDecisions) {
    const current=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(d.unit);
    assert.equal(current.state,d.state);assert.equal(current.question,d.question);
    const targets=db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=?').all(d.unit).map(x=>x.target_id);
    for(const target of d.targets)assert(targets.includes(target));
  }
  return {ok:true,groups:12,changes:22,dependencyPairsResolved:25};
}
