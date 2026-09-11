#!/usr/bin/env node
// Släktledsraden under aktens namn (T-0635, PCD-2026-09-11-033).
//
// Raden räknas ur föräldrakartan i lib/genealogy-relations.mjs och skrivs
// aldrig för hand. `--write` för in den, `--check` rapporterar saknade eller
// inaktuella rader, och validate-genealogy.mjs kör kontrollen.
//
// Etiketten följer ägarens konvention: stegen från Adam och Axel paras två och
// två till farfar/farmor/morfar/mormor, och ett udda sista steg blir far/mor.
// Längre vägar upprepar parorden - `mormors mormors mor` - i stället för att
// bygga längre sammansättningar.

import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { buildParentMap } from "./lib/genealogy-relations.mjs";

const ROOT = resolve(import.meta.dirname, "..");
export const SONS = ["P-0269", "P-0270"];
const SON_NAMES = { "P-0269": "Adam", "P-0270": "Axel" };
const PAIR = { ff: "farfar", fm: "farmor", mf: "morfar", mm: "mormor" };
const ONE = { f: "far", m: "mor" };
const WIDTH = 78;

export function kinTerm(path) {
  const words = [];
  for (let i = 0; i < path.length; i += 2) {
    words.push(i + 1 < path.length ? PAIR[path.slice(i, i + 2)] : ONE[path[i]]);
  }
  return words.map((word, i) => (i < words.length - 1 ? `${word}s` : word)).join(" ");
}

export function loadPeople(root = ROOT) {
  const dir = join(root, "genealogy", "people");
  const people = new Map();
  for (const file of readdirSync(dir).sort()) {
    const match = file.match(/^(P-\d{4})-.*\.md$/);
    if (!match) continue;
    const text = readFileSync(join(dir, file), "utf8");
    people.set(match[1], { file, text, name: text.match(/^# P-\d{4}: (.+)$/m)?.[1] ?? match[1] });
  }
  return people;
}

// Kolumnen `Relation` anger den länkade personens roll mot aktens person, och
// rollen står i cellens huvudled. Könet läses därför ur huvudledet i alla rader
// som pekar på personen.
// `uppgiven far` anger källans fadersuppgift; könet är inte osäkert. Ett huvudled
// med `till` beskriver en roll mot en tredje person och räknas inte.
const MALE = /^(?:biologisk[ae]?\s+|uppgiven\s+)?(?:far|fader|son|bror|helbror|halvbror|make|man)\b/i;
const FEMALE = /^(?:biologisk[ae]?\s+|uppgiven\s+)?(?:mor|moder|dotter|syster|helsyster|halvsyster|hustru|maka)(?![a-zåäö])/i;
const head = (relation) => relation.replace(/[*`_]/g, "").trim().split(/\s*[—–;,(]\s*/)[0].trim();

export function inferSexes(people) {
  const votes = new Map();
  for (const person of people.values()) {
    const section = (person.text.split("## Relationer")[1] ?? "").split(/\n## /)[0];
    for (const row of section.matchAll(/^\|\s*\[[^\]]+\]\((P-\d{4})[^)]*\)\s*\|\s*([^|]+)\|/gm)) {
      const [, target, relation] = row;
      const h = head(relation);
      if (/\btill\b/i.test(h)) continue;
      const sex = MALE.test(h) ? "m" : FEMALE.test(h) ? "f" : null;
      if (!sex) continue;
      const v = votes.get(target) ?? { m: 0, f: 0 };
      v[sex] += 1;
      votes.set(target, v);
    }
  }
  const sexes = new Map();
  for (const [id, v] of votes) sexes.set(id, v.m && v.f ? "?" : v.m ? "m" : "f");
  return sexes;
}

// Alla vägar från Adam; Axel är hans helbror och delar varje ana.
export function ancestorPaths(parents, sexes, from = SONS[0]) {
  const paths = new Map();
  const walk = (id, steps, via) => {
    for (const parent of parents.get(id) ?? []) {
      const sex = sexes.get(parent);
      const step = sex === "m" ? "f" : sex === "f" ? "m" : "?";
      const entry = { steps: steps + step, via: [...via, parent] };
      paths.set(parent, [...(paths.get(parent) ?? []), entry]);
      walk(parent, entry.steps, entry.via);
    }
  };
  walk(from, "", []);
  return paths;
}

// Länkar bryts aldrig; en rad med en lång länk får bli längre än WIDTH.
function wrap(text) {
  const lines = [];
  let line = "";
  for (const word of text.match(/\[[^\]]*\]\([^)]*\)\S*|\S+/g)) {
    if (line && line.length + 1 + word.length > WIDTH) {
      lines.push(line);
      line = word;
    } else line = line ? `${line} ${word}` : word;
  }
  if (line) lines.push(line);
  return lines.join("\n");
}

const link = (people, id, label = people.get(id).name) => `[${label}](${people.get(id).file})`;
const sons = (people) => `${link(people, SONS[0], SON_NAMES[SONS[0]])} och ${link(people, SONS[1], SON_NAMES[SONS[1]])}`;

export function ancestorBlock(people, id, entries) {
  if (entries.some((e) => e.steps.includes("?"))) return { error: `${id}: kön saknas för ett led i vägen` };
  const terms = [...new Set(entries.map((e) => kinTerm(e.steps)))];
  const generations = [...new Set(entries.map((e) => e.steps.length))].sort((a, b) => a - b);
  let text = `**Släktled:** ${terms.join(" och ")} till ${sons(people)}, generation ${generations.join(" och ")}.`;
  const routes = entries
    .filter((e) => e.via.length > 1)
    .map((e) => {
      const pronoun = e.steps.at(-1) === "f" ? "han" : "hon";
      return [...e.via.slice(0, -1).map((v) => link(people, v)), pronoun].join(" → ");
    });
  if (routes.length === 1) text += ` Vägen: ${routes[0]}.`;
  else if (routes.length > 1) text += ` Vägarna: ${routes.join("; ")}.`;
  return { text: wrap(text) };
}

export function sonBlock(people, id) {
  const other = SONS.find((s) => s !== id);
  return { text: wrap(`**Släktled:** ${SON_NAMES[id]} själv, bror till ${link(people, other, SON_NAMES[other])}. Generationerna räknas från dem båda.`) };
}

export function computeBlocks(root = ROOT) {
  const people = loadPeople(root);
  const parents = buildParentMap(people);
  const sexes = inferSexes(people);
  const [adam, axel] = SONS;
  const same = (a, b) => JSON.stringify([...(parents.get(a) ?? [])].sort()) === JSON.stringify([...(parents.get(b) ?? [])].sort());
  const errors = same(adam, axel) ? [] : ["Adam och Axel har olika föräldrar i föräldrakartan"];
  const blocks = new Map();
  for (const id of SONS) blocks.set(id, sonBlock(people, id));
  for (const [id, entries] of ancestorPaths(parents, sexes)) {
    const block = ancestorBlock(people, id, entries);
    if (block.error) errors.push(block.error);
    else blocks.set(id, block);
  }
  return { people, blocks, errors };
}

// Regionen mellan H1 och första H2 ägs av generatorn.
const REGION = /^(# P-\d{4}: [^\n]*\n)([\s\S]*?)(\n## )/;

export function render(text, block) {
  return text.replace(REGION, (_, h1, __, h2) => (block ? `${h1}\n${block}\n${h2}` : `${h1}${h2}`));
}

export function checkKinship(root = ROOT) {
  const { people, blocks, errors } = computeBlocks(root);
  for (const [id, person] of people) {
    const region = person.text.match(REGION)?.[2].trim() ?? "";
    const expected = blocks.get(id)?.text;
    if (expected && region !== expected) errors.push(`${person.file}: släktledsraden saknas eller är inaktuell; kör node scripts/kinship.mjs --write`);
  }
  return errors;
}

function main() {
  const mode = process.argv[2];
  if (mode === "--check") {
    const errors = checkKinship();
    for (const e of errors) console.error(e);
    console.log(errors.length ? `släktled: ${errors.length} fel.` : "släktled: OK.");
    if (errors.length) process.exitCode = 1;
  } else if (mode === "--write") {
    const { people, blocks, errors } = computeBlocks();
    for (const e of errors) console.error(e);
    let changed = 0;
    for (const [id, block] of blocks) {
      const person = people.get(id);
      const next = render(person.text, block.text);
      if (next !== person.text) {
        writeFileSync(join(ROOT, "genealogy", "people", person.file), next);
        changed += 1;
      }
    }
    console.log(`släktled: ${blocks.size} rader beräknade, ${changed} akter ändrade, ${errors.length} fel.`);
    if (errors.length) process.exitCode = 1;
  } else {
    console.error("Usage: node scripts/kinship.mjs --check | --write");
    process.exitCode = 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) main();
