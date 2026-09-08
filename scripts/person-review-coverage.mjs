#!/usr/bin/env node
// Frozen coverage mapping only; never proof of completed substantive review.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const idsIn = text => text.match(/\bP-\d{4}\b/g) ?? [];
export function cohortMembers(text, taskId) {
  if (taskId === 'T-0113') {
    const matches = [...text.matchAll(/Fast slutligt urval:\s*([^.]*)\./g)];
    return matches.length === 1 ? idsIn(matches[0][1]) : null;
  }
  const matches = [...text.matchAll(/^## Kohortmedlemmar\s*\n([\s\S]*?)(?=^## |$(?![\s\S]))/gm)];
  return matches.length === 1 ? idsIn(matches[0][1]) : null;
}
export function checkReviewCoverage({ baseline, tasks, currentPeople, devLogs, expectedCount = 538 }) {
  const errors = [];
  if (baseline?.schema !== 'person-review-baseline/v1' || !Array.isArray(baseline.records)) return ['ogiltig baslinje'];
  const records = baseline.records;
  if (records.length !== expectedCount) errors.push(`baslinjen innehåller ${records.length} poster; väntat ${expectedCount}`);
  const mapping = new Map();
  const cohorts = new Map();
  for (const r of records) {
    if (!/^P-\d{4}$/.test(r.id ?? '')) errors.push(`ogiltigt person-id ${r.id}`);
    if (mapping.has(r.id)) errors.push(`dubbel person i baslinjen: ${r.id}`);
    mapping.set(r.id, r.reviewTask);
    if (!/^T-\d{4}$/.test(r.reviewTask ?? '')) { errors.push(`${r.id}: saknad/giltig reviewTask krävs`); continue; }
    if (!cohorts.has(r.reviewTask)) cohorts.set(r.reviewTask, []);
    cohorts.get(r.reviewTask).push(r.id);
  }
  const current = new Set();
  for (const id of currentPeople) {
    if (current.has(id)) errors.push(`flera aktuella personakter för ${id}`);
    current.add(id);
    if (!mapping.has(id)) errors.push(`nytillkommen akt utanför baslinjen: ${id}; kräver uttrycklig tilläggstäckning`);
  }
  for (const id of mapping.keys()) if (!current.has(id)) errors.push(`baslinjeperson saknar aktuell akt: ${id}`);
  const taskMap = new Map();
  for (const task of tasks) {
    if (taskMap.has(task.id)) errors.push(`dubbelt Wotan-id: ${task.id}`);
    taskMap.set(task.id, task);
  }
  const allMembers = new Map();
  for (const [taskId, assigned] of cohorts) {
    if (!taskMap.has(taskId)) errors.push(`saknad Wotan-uppgift: ${taskId}`);
    const text = devLogs[taskId];
    if (typeof text !== 'string') { errors.push(`saknad dev-log: ${taskId}`); continue; }
    const members = cohortMembers(text, taskId);
    if (members === null) { errors.push(`${taskId}: saknad/otydlig fryst medlemslista`); continue; }
    const unique = new Set();
    for (const id of members) {
      if (unique.has(id)) errors.push(`${taskId}: dubbel kohortmedlem ${id}`);
      unique.add(id);
      allMembers.set(id, (allMembers.get(id) ?? 0) + 1);
      if (mapping.get(id) !== taskId) errors.push(`${taskId}: felplacerad medlem ${id}; baslinjen anger ${mapping.get(id) ?? 'ingen uppgift'}`);
    }
    for (const id of assigned) if (!unique.has(id)) errors.push(`${taskId}: saknad kohortmedlem ${id}`);
  }
  for (const id of mapping.keys()) if (allMembers.get(id) !== 1) errors.push(`${id}: förekommer ${allMembers.get(id) ?? 0} gånger i medlemslistorna; kräver exakt en`);
  const final = taskMap.get('T-0115');
  if (!final) errors.push('saknad slutrevision T-0115');
  else {
    const after = new Set(final.after ?? []);
    // Pilot is already independently completed; final dependencies include all rollout cohorts.
    for (const id of ['T-0110', 'T-0114', ...[...cohorts.keys()].filter(id => id !== 'T-0113')]) {
      if (!taskMap.has(id)) errors.push(`saknad nödvändig uppgift: ${id}`);
      if (!after.has(id)) errors.push(`T-0115 saknar slutberoende ${id}`);
    }
  }
  return errors;
}
export function checkRepositoryReviewCoverage(root = ROOT) {
  const baseline = JSON.parse(readFileSync(join(root, 'wotan/dev-log/T-0114-inventory.json'), 'utf8'));
  const { tasks } = JSON.parse(readFileSync(join(root, 'wotan/backlog.json'), 'utf8'));
  const currentPeople = readdirSync(join(root, 'genealogy/people')).flatMap(f => f.match(/^(P-\d{4})-.*\.md$/)?.[1] ?? []);
  const devLogs = {};
  for (const taskId of new Set(baseline.records.map(r => r.reviewTask))) {
    if (!/^T-\d{4}$/.test(taskId ?? '')) continue;
    const path = join(root, 'wotan/dev-log', `${taskId}.md`);
    if (existsSync(path)) devLogs[taskId] = readFileSync(path, 'utf8');
  }
  return { personCount: baseline.records.length, errors: checkReviewCoverage({ baseline, tasks, currentPeople, devLogs }) };
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  if (process.argv.length > 2) {
    console.error('Usage: node scripts/person-review-coverage.mjs (read-only)');
    process.exitCode = 2;
  } else {
    const { personCount, errors } = checkRepositoryReviewCoverage();
    for (const error of errors) console.error(error);
    console.log(`Personaktsgranskning: ${personCount} baslinjepersoner, ${errors.length} täckningsfel. Ingen saklig fullständighetsbedömning.`);
    if (errors.length) process.exitCode = 1;
  }
}
