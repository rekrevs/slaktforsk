import {test} from 'node:test';
import assert from 'node:assert/strict';
import {selectCore} from './wotan-priority.mjs';

const task = (id, priority, status = 'READY', after = []) => ({id, priority, status, after,
  priority_basis: 'P-0211: exakt grindfråga i dev-log'});
const select = (...tasks) => selectCore({tasks});

test('earlier deferred work cannot displace a runnable core task', () => {
  assert.equal(select(task('T-1', 'DEFERRED'), task('T-2', 'CORE_IDENTITY')).selected, 'T-2');
});
test('an empty core queue never falls through to deferred work', () => {
  assert.equal(select(task('T-1', 'DEFERRED')).action, 'PROJECT_CONTROL');
});
test('blocked core work cannot authorize lower work', () => {
  const r = select(task('T-1', 'DEFERRED'), task('T-2', 'CORE_IDENTITY', 'BLOCKED', ['T-1']));
  assert.equal(r.selected, null);
});
test('a READY core task with unfinished predecessors is skipped', () => {
  const r = select(task('T-1', 'DEFERRED'), task('T-2', 'CORE_IDENTITY', 'READY', ['T-1']),
    task('T-3', 'CORE_IDENTITY'));
  assert.equal(r.selected, 'T-3');
});
test('a deferred ongoing task requires a checkpoint instead of silent abandonment', () => {
  const r = select(task('T-1', 'DEFERRED', 'ONGOING'), task('T-2', 'CORE_IDENTITY'));
  assert.equal(r.action, 'PROJECT_CONTROL');
  assert.equal(r.ongoing, 'T-1');
});
test('core ongoing takes precedence and selection grants no mandate', () => {
  const r = select(task('T-1', 'CORE_IDENTITY'), task('T-2', 'CORE_IDENTITY', 'ONGOING'));
  assert.equal(r.selected, 'T-2');
  assert.equal(r.selection_is_not_execution_authorization, true);
});
test('uncategorized committed work fails closed', () => {
  assert.throws(() => select(task('T-1', undefined)), /priority/);
});
test('IDEA is never selected and multiple ongoing tasks are rejected', () => {
  assert.equal(select(task('T-1', 'CORE_IDENTITY', 'IDEA')).selected, null);
  assert.throws(() => select(task('T-1', 'CORE_IDENTITY', 'ONGOING'),
    task('T-2', 'CORE_IDENTITY', 'ONGOING')), /ONGOING/);
});
