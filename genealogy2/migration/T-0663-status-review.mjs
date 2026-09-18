import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {head} from '../lib/domain.mjs';

const reviewUrl = new URL('./T-0663-status-review.json', import.meta.url);
const digest = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const normalized = value => JSON.stringify(value, Object.keys(value).sort());

export function loadStatusReview() {
  const review = JSON.parse(fs.readFileSync(reviewUrl, 'utf8'));
  assert.equal(review.format, 'genealogy2-status-review/v1');
  assert.equal(review.mode, 'proposal_only');
  assert.equal(review.decisions.length, 51);
  assert.equal(new Set(review.decisions.map(d => d.object_id)).size, 51);
  assert.deepEqual(review.decisions.map(d => d.object_id).sort(), [...review.scope.object_ids].sort());
  assert.equal(review.decisions.filter(d => d.decision === 'retain').length, 7);
  assert.equal(review.decisions.filter(d => d.decision === 'propose_revision').length, 44);
  return review;
}

function currentOrigins(db, revisionId) {
  return db.prepare('SELECT unit_id,coverage,note FROM origin WHERE revision_id=? ORDER BY unit_id').all(revisionId);
}

function currentDependencies(db, revisionId) {
  return db.prepare(`SELECT d.basis_revision_id,b.object_id,d.role,d.note FROM dependency d
    JOIN revision b ON b.id=d.basis_revision_id WHERE d.revision_id=? ORDER BY d.basis_revision_id,d.role`).all(revisionId);
}

// Builds explicit native changes only. This module performs no writes or apply.
export function buildStatusReview(db) {
  const review = loadStatusReview();
  const changes = [];
  for (const decision of review.decisions) {
    const {object_id: id, current: expected} = decision;
    const current = head(db, id);
    assert(current, id);
    assert.equal(current.id, expected.revision_id, `Föråldrad statusgranskning: ${id}`);
    assert.equal(current.version, decision.expected_version);
    assert.equal(current.kind, decision.kind);
    assert.equal(current.evidence_status, expected.evidence_status);
    assert.equal(current.disposition, expected.disposition);
    assert.notEqual(current.evidence_status, 'OWNER_CONFIRMED');
    const payload = db.prepare(`SELECT * FROM ${current.kind} WHERE revision_id=?`).get(current.id);
    assert.equal(digest(payload), expected.payload_sha256, `Ändrat sakinnehåll: ${id}`);
    assert.equal(current.rationale, expected.rationale);
    assert.equal(current.caveat, expected.caveat);
    const origins = currentOrigins(db, current.id);
    const expectedOrigins = decision.import_cause_review.current_origins
      .map(o => ({unit_id:o.unit_id,coverage:o.coverage,note:o.note})).sort((a,b) => a.unit_id.localeCompare(b.unit_id));
    assert.deepEqual(origins.map(normalized), expectedOrigins.map(normalized), `Ändrat ursprung: ${id}`);
    const dependencies = currentDependencies(db, current.id);
    const expectedDependencies = decision.import_cause_review.current_dependencies
      .map(d => ({basis_revision_id:d.basis_revision_id,object_id:d.object_id,role:d.role,note:d.note}));
    assert.deepEqual(dependencies.map(normalized), expectedDependencies.map(normalized), `Ändrat beroende: ${id}`);
    if (decision.decision === 'retain') {
      assert.equal(decision.proposed_evidence_status, current.evidence_status);
      continue;
    }
    assert.equal(decision.proposed_evidence_status, 'TRANSCRIBED');
    const dependents = db.prepare(`WITH RECURSIVE dependents(id) AS (
      SELECT revision_id FROM dependency WHERE basis_revision_id=?
      UNION SELECT d.revision_id FROM dependency d JOIN dependents p ON d.basis_revision_id=p.id
    ) SELECT DISTINCT c.id FROM dependents d JOIN revision old ON old.id=d.id
      JOIN current_revision c ON c.object_id=old.object_id ORDER BY c.id`).all(current.id);
    assert.equal(dependents.length, 0, `Nya beroenden kräver individuell granskning: ${id}`);
    const {revision_id, ...data} = payload;
    const evidence = dependencies.map(d => {
      const basis = head(db, d.object_id);
      assert.equal(basis?.id, d.basis_revision_id, `Underlaget måste omprövas före byggning: ${id} → ${d.basis_revision_id}`);
      return {object:d.object_id,version:basis.version,role:d.role,note:d.note};
    });
    const change = {
      id,kind:current.kind,expectedVersion:current.version,data,
      disposition:current.disposition,evidenceStatus:'TRANSCRIBED',
      rationale:decision.individual_rationale,
      caveat:current.caveat,
      origins:origins.map(o => ({unit:o.unit_id,coverage:o.coverage,note:o.note})),
      evidence
    };
    if (current.kind === 'identity') {
      assert.equal(data.decision, 'accepted');
      const mention = head(db, data.mention_id);
      assert(evidence.some(e => e.object === mention.object_id && e.version === mention.version), `Saknad bevarad M-bindning: ${id}`);
      change.bindings = {[mention.object_id]:mention.version};
    }
    changes.push(change);
  }
  assert.equal(changes.length, 44);
  assert.equal(changes.filter(c => c.kind === 'person').length, 24);
  assert.equal(changes.filter(c => c.kind === 'identity').length, 20);
  return {changes,unitDecisions:[],dependencyReviews:[],review};
}
