#!/usr/bin/env node
// Read-only selection over the sole Wotan backlog; never grants execution authority.
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const CORE = new Set(['CORE_IDENTITY', 'CORE_LIFE', 'CORE_SUPPORT']);
const PRIORITIES = new Set([...CORE, 'DEFERRED']);

export function selectCore(backlog) {
  const tasks = backlog.tasks;
  const byId = new Map(tasks.map(t => [t.id, t]));
  if (byId.size !== tasks.length) throw Error('Duplicerade Wotan-ID');
  const committed = tasks.filter(t => ['READY', 'BLOCKED', 'ONGOING'].includes(t.status));
  for (const t of committed) {
    if (!PRIORITIES.has(t.priority) || !t.priority_basis?.trim()) {
      throw Error(`${t.id}: saknar giltig priority/priority_basis; klassning krävs före kärnkörning`);
    }
    if (['CORE_IDENTITY', 'CORE_LIFE'].includes(t.priority) && !/P-\d{4}/.test(t.priority_basis)) {
      throw Error(`${t.id}: kärnprioritet saknar explicit personankare`);
    }
    for (const id of t.after ?? []) if (!byId.has(id)) throw Error(`${t.id}: saknat beroende ${id}`);
  }
  const ongoing = tasks.filter(t => t.status === 'ONGOING');
  if (ongoing.length > 1) throw Error('Flera ONGOING; checkpoint krävs');
  const eligible = t => (t.after ?? []).every(id => byId.get(id).status === 'DONE');
  const common = {
    decision: 'PCD-2026-10-05-001',
    selection_is_not_execution_authorization: true,
    core_committed: committed.filter(t => CORE.has(t.priority)).length,
    deferred_committed: committed.filter(t => t.priority === 'DEFERRED').length,
  };
  if (ongoing.length) {
    const task = ongoing[0];
    if (!CORE.has(task.priority) || !eligible(task)) {
      return {...common, action: 'PROJECT_CONTROL', selected: null, ongoing: task.id,
        reason: 'Bevara pågående checkpoint; pröva prioritet/beroenden, inget tyst avbrott eller fallback.'};
    }
    return {...common, action: 'RESUME_CORE', selected: task.id, priority: task.priority};
  }
  const next = tasks.find(t => t.status === 'READY' && CORE.has(t.priority) && eligible(t));
  if (next) return {...common, action: 'NEXT_CORE', selected: next.id, priority: next.priority};
  return {...common, action: 'PROJECT_CONTROL', selected: null,
    reason: 'Ingen behörig kärn-READY. Pröva faktisk kärngrind/ny bounded passage inom mandat; kör aldrig DEFERRED automatiskt.'};
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  if (args.some(a => a !== '--deferred')) throw Error('Använd utan argument eller --deferred');
  const backlog = JSON.parse(readFileSync(new URL('../wotan/backlog.json', import.meta.url), 'utf8'));
  const result = args.includes('--deferred')
    ? {decision: 'PCD-2026-10-05-001', note: 'Direkt filter av samma backlog; full scope/checkpoint i varje dev-log.',
      tasks: backlog.tasks.filter(t => t.priority === 'DEFERRED' && ['READY', 'BLOCKED', 'ONGOING'].includes(t.status))
        .map(({id, status, summary, priority_basis}) => ({id, status, summary, priority_basis}))}
    : selectCore(backlog);
  console.log(JSON.stringify(result, null, 2));
}
