import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {head} from '../lib/domain.mjs';
import {loadStatusReview, buildStatusReview} from '../migration/T-0663-status-review.mjs';

const digest = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const json = rows => JSON.parse(JSON.stringify(rows));
const kept = ['P-0052','P-0053','P-0153','ID-P-0052-C0049','ID-P-0053-C0049',
  'ID-M-C0111-child-Carl-Petter','ID-C0111-family-Carl-Petter-P0153'];

function checkPreservation(db, review) {
  for (const d of review.decisions) {
    const old = db.prepare('SELECT * FROM revision WHERE id=?').get(d.current.revision_id);
    assert(old, `Äldre version saknas: ${d.current.revision_id}`);
    assert.equal(old.evidence_status, 'CORROBORATED');
    assert.equal(old.disposition, 'accepted');
    assert.equal(old.version, d.current.version);
    assert.equal(old.rationale, d.current.rationale);
    assert.equal(old.caveat, d.current.caveat);
    assert.equal(old.operation_id, d.current.operation_id);
    const payload = db.prepare(`SELECT * FROM ${d.kind} WHERE revision_id=?`).get(old.id);
    assert.equal(digest(payload), d.current.payload_sha256, `Äldre sakdata ändrade: ${old.id}`);
    const origins = db.prepare('SELECT unit_id,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id').all(old.id);
    const expectedOrigins = d.import_cause_review.current_origins.map(o => ({unit_id:o.unit_id,coverage:o.coverage,note:o.note})).sort((a,b) => a.unit_id.localeCompare(b.unit_id));
    assert.deepEqual(json(origins), expectedOrigins, `Äldre ursprung ändrat: ${old.id}`);
    const deps = db.prepare('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role').all(old.id);
    assert.deepEqual(json(deps), d.import_cause_review.current_dependencies.map(e => ({basis_revision_id:e.basis_revision_id,role:e.role,note:e.note})), `Äldre belägg ändrade: ${old.id}`);
  }
  const owner = head(db, 'P-0269');
  assert.equal(owner.id, 'P-0269@2');
  assert.equal(owner.evidence_status, 'OWNER_CONFIRMED');
  assert.equal(owner.disposition, 'accepted');
  assert.equal(digest(db.prepare('SELECT * FROM person WHERE revision_id=?').get(owner.id)), 'f0911883ea29593b24d5f18019c4f349cfea165be2e6690aff6836dfaa80720e');
  const nanny = head(db, 'P-0434');
  assert.equal(nanny.id, 'P-0434@2');
  assert.equal(nanny.evidence_status, 'TRANSCRIBED');
  assert.equal(nanny.disposition, 'accepted');
}

function checkIndependentBoundaries(db, review) {
  assert.deepEqual(review.decisions.filter(d => d.decision === 'retain').map(d => d.object_id).sort(), [...kept].sort());
  // C0111 has two own passages, one R, plus its explicit internal routing.
  const carl = ['ID-M-C0111-child-Carl-Petter','ID-C0111-family-Carl-Petter-P0153'].map(id => {
    const identity = db.prepare('SELECT * FROM identity WHERE revision_id=?').get(head(db,id).id);
    return db.prepare('SELECT * FROM mention WHERE revision_id=?').get(head(db,identity.mention_id).id);
  });
  assert.notEqual(carl[0].revision_id, carl[1].revision_id);
  assert.equal(carl[0].record_id, carl[1].record_id);
  assert.equal(carl[0].record_id, 'R-3439566e8bf9a5cdd2f48dfb');
  assert.match(carl[1].name_literal, /Carl Petter Andersson/);
  const c0111 = review.reviewed_documents.find(d => d.entity === 'C-0111');
  const citation = db.prepare('SELECT text FROM document WHERE path=?').get(c0111.path).text;
  assert.match(citation, /Carl Petter.*?fördes.*?nedan/s);
  assert.match(citation, /Gifte son Carl Petter Andersson/);
  // C0044 positively repeats these two daughters, while it does not repeat Margareta.
  const c0044 = review.reviewed_documents.find(d => d.entity === 'C-0044');
  const jomark = db.prepare('SELECT text FROM document WHERE path=?').get(c0044.path).text;
  assert.match(jomark, /Catarina Johanna \| 65 11\/5/);
  assert.match(jomark, /Anna Albertina \| 71 28\/9/);
  assert.doesNotMatch(jomark, /Margareta Euphrosyne/);
  for (const id of ['P-0057','P-0326','P-0370','P-0390','P-0393','P-0237','ID-P-0434-C0552-own']) {
    const d = review.decisions.find(d => d.object_id === id);
    assert.equal(d.decision, 'propose_revision');
    assert.equal(d.proposed_evidence_status, 'TRANSCRIBED');
    assert(d.individual_rationale.length > 200);
    assert(d.conflicts_and_limits.length >= 2);
  }
  for (const id of ['P-0237','ID-M-C0197-Brit-Maria-child']) {
    assert.equal(review.decisions.find(d => d.object_id === id).import_cause_review.mechanism, 'explicit_import_grade_without_demonstrated_helper');
  }
}

export function checkT0663StatusReviewPreparation(db) {
  const review = loadStatusReview();
  checkPreservation(db, review);
  checkIndependentBoundaries(db, review);
  const {changes} = buildStatusReview(db);
  assert.equal(changes.length, 44);
  assert(changes.every(c => c.disposition === 'accepted' && c.evidenceStatus === 'TRANSCRIBED'));
  assert(changes.every(c => ['person','identity'].includes(c.kind)));
  assert(!changes.some(c => kept.includes(c.id) || c.id === 'P-0269' || c.id === 'P-0434'));
  return {ok:true,groups:6,changes:44,retained:7};
}

// Run by the integrating agent only after applying the reviewed native changes to a test DB.
export function checkT0663StatusReviewRisks(db) {
  const review = loadStatusReview();
  checkPreservation(db, review);
  checkIndependentBoundaries(db, review);
  for (const d of review.decisions) {
    const current = head(db,d.object_id);
    assert.equal(current.disposition,'accepted');
    if (d.decision === 'retain') {
      assert.equal(current.id,d.current.revision_id);
      assert.equal(current.evidence_status,'CORROBORATED');
      continue;
    }
    assert.equal(current.version,d.current.version+1);
    assert.equal(current.previous_id,d.current.revision_id);
    assert.equal(current.evidence_status,'TRANSCRIBED');
    assert.equal(current.rationale,d.individual_rationale);
    assert.equal(current.caveat,d.current.caveat);
    const payload = db.prepare(`SELECT * FROM ${d.kind} WHERE revision_id=?`).get(current.id);
    payload.revision_id=d.current.revision_id;
    assert.equal(digest(payload),d.current.payload_sha256, `Oavsiktlig sakändring: ${d.object_id}`);
    const oldOrigins=db.prepare('SELECT unit_id,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id').all(d.current.revision_id);
    const newOrigins=db.prepare('SELECT unit_id,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id').all(current.id);
    assert.deepEqual(json(newOrigins),json(oldOrigins));
    const oldDeps=db.prepare('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role').all(d.current.revision_id);
    const newDeps=db.prepare('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role').all(current.id);
    assert.deepEqual(json(newDeps),json(oldDeps));
  }
  return {ok:true,groups:7,changed:44,retained:7};
}
