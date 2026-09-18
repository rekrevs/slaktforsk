import test from 'node:test';
import assert from 'node:assert/strict';
import { checkReviewCoverage, cohortMembers } from './person-review-coverage.mjs';
function fixture() {
  return {
    expectedCount: 3,
    baseline: { schema: 'person-review-baseline/v1', records: [{ id: 'P-0001', reviewTask: 'T-0113', sha256: 'old' }, { id: 'P-0002', reviewTask: 'T-0117' }, { id: 'P-0003', reviewTask: 'T-0117' }] },
    currentPeople: ['P-0001', 'P-0002', 'P-0003'],
    tasks: [{ id: 'T-0113' }, { id: 'T-0117' }, { id: 'T-0110' }, { id: 'T-0114' }, { id: 'T-0115', after: ['T-0110', 'T-0114', 'T-0117'] }],
    devLogs: { 'T-0113': 'Äldre urval: P-0099.\nFast slutligt urval: P-0001.\n## Utfall\nP-0001', 'T-0117': '# Task\n## Kohortmedlemmar\n\nP-0002, P-0003\n\n## Underlag\nP-0001 och P-0002 omnämns som släkt.' },
  };
}
test('valid frozen mapping passes without comparing mutable content hashes', () => assert.deepEqual(checkReviewCoverage(fixture()), []));
test('missing and duplicate baseline persons are rejected', () => {
  const missing = fixture(); missing.baseline.records.pop();
  assert.ok(checkReviewCoverage(missing).some(e => e.includes('väntat 3')));
  const duplicate = fixture(); duplicate.baseline.records[2] = { ...duplicate.baseline.records[1] };
  assert.ok(checkReviewCoverage(duplicate).some(e => e.includes('dubbel person')));
});
test('missing, duplicate and wrongly assigned cohort member fail', () => {
  const missing = fixture(); missing.devLogs['T-0117'] = '## Kohortmedlemmar\nP-0002\n';
  assert.ok(checkReviewCoverage(missing).some(e => e.includes('saknad kohortmedlem P-0003')));
  const duplicate = fixture(); duplicate.devLogs['T-0117'] = '## Kohortmedlemmar\nP-0002, P-0003, P-0003\n';
  assert.ok(checkReviewCoverage(duplicate).some(e => e.includes('dubbel kohortmedlem')));
  const wrong = fixture(); wrong.baseline.records[1].reviewTask = 'T-0113';
  assert.ok(checkReviewCoverage(wrong).some(e => e.includes('felplacerad medlem P-0002')));
});
test('new and vanished current dossiers require explicit reconciliation', () => {
  const added = fixture(); added.currentPeople.push('P-0004');
  assert.ok(checkReviewCoverage(added).some(e => e.includes('nytillkommen akt')));
  const removed = fixture(); removed.currentPeople.pop();
  assert.ok(checkReviewCoverage(removed).some(e => e.includes('saknar aktuell akt')));
});
test('missing final dependency and missing task are detected', () => {
  const dependency = fixture(); dependency.tasks.at(-1).after.pop();
  assert.ok(checkReviewCoverage(dependency).some(e => e.includes('saknar slutberoende T-0117')));
  const task = fixture(); task.tasks = task.tasks.filter(t => t.id !== 'T-0117');
  assert.ok(checkReviewCoverage(task).some(e => e.includes('saknad Wotan-uppgift: T-0117')));
});
test('membership parser ignores references outside membership section and rejects repeated sections', () => {
  assert.deepEqual(cohortMembers(fixture().devLogs['T-0117'], 'T-0117'), ['P-0002', 'P-0003']);
  assert.equal(cohortMembers('## Kohortmedlemmar\nP-0002\n## Kohortmedlemmar\nP-0003', 'T-0117'), null);
  assert.deepEqual(cohortMembers(fixture().devLogs['T-0113'], 'T-0113'), ['P-0001']);
});
