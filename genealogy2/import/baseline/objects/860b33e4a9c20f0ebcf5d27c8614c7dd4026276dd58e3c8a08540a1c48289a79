#!/usr/bin/env node
// Beräknar probandens anor och vilka anspetsar som saknar kända föräldrar.
// Svarar på frågan "hur långt bakåt har vi kommit på varje gren?"

import { readFileSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { buildParentMap, deriveDepths } from "./lib/genealogy-relations.mjs";
import { readTerminalStatus } from "./lib/terminal-status.mjs";

const root = resolve(import.meta.dirname, "..");
const peopleDir = join(root, "genealogy", "people");
const PROBAND = process.env.PROBAND ?? "P-0004";
const throughArg = process.argv.find((arg) => arg.startsWith("--through-depth="));
const THROUGH_DEPTH = throughArg
  ? Number.parseInt(throughArg.split("=", 2)[1], 10)
  : Number.POSITIVE_INFINITY;

if (Number.isNaN(THROUGH_DEPTH) || THROUGH_DEPTH < 0) {
  throw new Error("--through-depth måste vara ett icke-negativt heltal");
}

const people = new Map();
for (const name of readdirSync(peopleDir)) {
  const match = name.match(/^(P-\d{4})-/);
  if (!match) continue;
  const text = readFileSync(join(peopleDir, name), "utf8");
  people.set(match[1], {
    file: name,
    title: text.split("\n", 1)[0].replace(/^#\s*P-\d{4}:\s*/, ""),
    text,
  });
}

const parents = buildParentMap(people);
const depth = deriveDepths(parents, PROBAND);

const ancestors = [...depth.keys()].filter((id) => id !== PROBAND);
const tips = ancestors.filter((id) => (parents.get(id)?.size ?? 0) === 0).sort();
const auditedTips = tips.filter((id) => depth.get(id) <= THROUGH_DEPTH);

const byDepth = new Map();
for (const id of ancestors) {
  const d = depth.get(id);
  byDepth.set(d, (byDepth.get(d) ?? 0) + 1);
}

// --- Slutstatus -------------------------------------------------------------
// Parsern delas med scripts/goal-state.mjs; se scripts/lib/terminal-status.mjs.

const citationsDir = join(root, "genealogy", "citations");
const citationFiles = readdirSync(citationsDir);
const citationExists = (cid) => citationFiles.some((name) => name.startsWith(`${cid}-`));
const readStatus = (id) => readTerminalStatus(people.get(id).text, citationExists);

const verdicts = new Map(auditedTips.map((id) => [id, readStatus(id)]));
const unresolved = auditedTips.filter((id) => !verdicts.get(id).ok);

console.log(`Proband: ${PROBAND}`);
console.log(`Kända anor: ${ancestors.length} av teoretiskt ${[...byDepth.keys()].reduce((a, d) => a + 2 ** d, 0)} till och med djup ${Math.max(...byDepth.keys())}`);
for (const d of [...byDepth.keys()].sort((a, b) => a - b)) {
  console.log(`  djup ${d}: ${byDepth.get(d)} av ${2 ** d}`);
}

console.log(
  `\nGranskningsdjup: ${Number.isFinite(THROUGH_DEPTH) ? `0–${THROUGH_DEPTH}` : "alla djup"}`,
);
console.log(`Anspetsar utan kända föräldrar inom granskningsdjupet: ${auditedTips.length}`);
for (const id of auditedTips.sort((a, b) => depth.get(a) - depth.get(b) || a.localeCompare(b))) {
  const v = verdicts.get(id);
  const mark = v.ok ? `${v.status}` : `SAKNAS — ${v.why}`;
  console.log(`  ${id} (djup ${depth.get(id)})  ${people.get(id).title}\n      ${mark}`);
}

const nextFrontier = tips
  .filter((id) => depth.get(id) > THROUGH_DEPTH)
  .sort((a, b) => depth.get(a) - depth.get(b) || a.localeCompare(b));
if (nextFrontier.length) {
  console.log(`\nRegistrerad front utanför granskningsdjupet: ${nextFrontier.length}`);
  for (const id of nextFrontier) {
    console.log(`  ${id} (djup ${depth.get(id)})  ${people.get(id).title}`);
  }
}

// Breddförst: den lägsta djupnivån med osökta anspetsar är den enda som får
// bearbetas.
if (unresolved.length) {
  const nextDepth = Math.min(...unresolved.map((id) => depth.get(id)));
  const queue = unresolved.filter((id) => depth.get(id) === nextDepth);
  console.log(`\nNärmaste djup med formellt ofullständig slutstatus: ${nextDepth}`);
  for (const id of queue) console.log(`  ${id}  ${people.get(id).title}`);
}

console.log(
  `\nAnspetsar utan formellt giltig slutstatus: ${unresolved.length}. ` +
    "Strukturkontrollen prövar inte källuttömning, livsbilder eller north stars uppfyllelse.",
);
process.exitCode = unresolved.length ? 1 : 0;
