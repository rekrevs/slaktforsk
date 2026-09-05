#!/usr/bin/env node
// Härledd inventering och strukturgrind, aldrig automatisk genealogisk bevisning.
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { computeGoalState, loadRepository } from "./goal-state.mjs";
import { readWorkState } from "./lib/terminal-status.mjs";

export const THEMES = ["ID", "REL", "BO", "ARB", "EKO", "MIL", "SAM", "HAL", "PER", "SYN"];
export const REQUIREMENTS = Array.from({ length: 12 }, (_, i) => `PK-${String(i + 1).padStart(2, "0")}`);
const THEME_STATES = ["EJ BEDÖMT", "ÖPPET", "GENOMGÅNGET", "AVGRÄNSAT", "EJ RELEVANT", "INTEGRITETSMINIMERAT"];
const CLOSED_THEMES = THEME_STATES.slice(2);
const FIELDS = {
  "Identitetsläge": ["EJ BEDÖMT", "PÅGÅR", "PRÖVAT", "OMSTRITT", "OLÖST"],
  "Livsbildsläge": ["EJ BEDÖMT", "PÅGÅR", "GENOMGÅNGEN", "AVGRÄNSAD", "INTEGRITETSMINIMERAD"],
  "Källstrategiläge": ["EJ BEDÖMT", "PÅGÅR", "GENOMGÅNGEN"],
  "Kontraktsgranskning": ["EJ GRANSKAD", "UNDERKÄND", "GODKÄND"],
};
const HEADINGS = ["Identitetsbedömning", "Söknycklar", "Livsteman", "Forskningsfrågor", "Källvägar", "Kontraktsgranskning"];
const PATH_FIELDS = ["Frågor/teman", "Källklass", "Tid/plats och arkivbildare", "Förväntad information", "Ingång och söknycklar", "Beroenden", "Föregående källvägar", "Leverantörer och åtkomst", "Undersökt omfång och utfall", "Bedömning och återaktivering", "Wotan"];
const QUESTION_FIELDS = ["Fråga och betydelse", "Känt underlag", "Alternativ och motprövning", "Källvägar", "Slutsatsläge", "Argument och konflikter", "Påverkade personer/påståenden"];
const LINK = /\[[^\]]+\]\(([^)]+)\)/g;
const sha = (text) => createHash("sha256").update(text).digest("hex");
const clean = (value) => value.trim().replace(/^`|`$/g, "");
const fieldValues = (text, key) => text.split("\n").filter((line) => line.startsWith(`- ${key}:`)).map((line) => clean(line.slice(key.length + 3)));
const hasLink = (text) => /\[[^\]]+\]\([^)]+\)/.test(text);

export function markdownAnchor(text) {
  return text.toLowerCase().replace(/[^\p{L}\p{N}_\s-]/gu, "").replace(/\s/g, "-");
}

export function checkLocalLink(root, baseFile, target) {
  if (/^[a-z]+:/i.test(target)) return null;
  const [path, fragment] = target.split("#");
  const file = path ? resolve(dirname(baseFile), path) : baseFile;
  if (!existsSync(file)) return `bruten länk ${relative(root, baseFile)} -> ${target}`;
  if (fragment && file.endsWith(".md")) {
    const headings = [...readFileSync(file, "utf8").matchAll(/^#{1,6}\s+(.+)$/gm)].map((m) => markdownAnchor(m[1]));
    if (!headings.includes(decodeURIComponent(fragment))) return `saknat ankare ${relative(root, baseFile)} -> ${target}`;
  }
  return null;
}

export function assessProfile({ personId, text, linkError = () => null, classIds = new Set(Array.from({ length: 40 }, (_, i) => `K-${String(i + 1).padStart(2, "0")}`)), taskIds = null, pathExists = null }) {
  if (text === null) return { present: false, identity: "EJ BEDÖMT", biography: "EJ BEDÖMT", strategy: "EJ BEDÖMT", review: "EJ INFÖRT", themes: {}, dependencies: {}, recordedApproval: false, errors: [] };
  const errors = [];
  function one(key, allowed) {
    const values = fieldValues(text, key);
    if (values.length !== 1 || !values[0] || (allowed && !allowed.includes(values[0]))) errors.push(`${key}: kräver exakt ett giltigt värde`);
    return values[0] ?? null;
  }
  one("Kontrakt", ["person-research/v1"]);
  one("Person", [personId]);
  const states = Object.fromEntries(Object.entries(FIELDS).map(([key, values]) => [key, one(key, values)]));
  for (const heading of HEADINGS) {
    if (text.split("\n").filter((line) => line === `## ${heading}`).length !== 1) errors.push(`kräver exakt ett avsnitt ${heading}`);
  }
  const rows = text.split("\n").filter((line) => line.startsWith("| ")).map((line) => line.split("|").slice(1, -1).map(clean));
  const themes = {};
  for (const id of THEMES) {
    const found = rows.filter((row) => row[0] === id);
    if (found.length !== 1 || found[0].length !== 4 || !THEME_STATES.includes(found[0][1])) {
      errors.push(`${id}: kräver en giltig temarad med fyra fält`);
      continue;
    }
    themes[id] = found[0][1];
    if (!found[0][2] || (found[0][1] !== "EJ BEDÖMT" && (!found[0][3] || found[0][3] === "—"))) errors.push(`${id}: bedömningen saknar motivering eller underlag/källväg`);
  }
  const questionHeadings = [...text.matchAll(/^### (Q-\d{2,}): (.+)$/gm)];
  const questionIds = new Set(questionHeadings.map((m) => m[1]));
  if (questionIds.size !== questionHeadings.length) errors.push("dubbla fråge-id:n");
  const pathHeadings = [...text.matchAll(/^### (KP-\d{2,}): (.+)$/gm)];
  const pathIds = new Set(pathHeadings.map((m) => m[1]));
  if (pathIds.size !== pathHeadings.length) errors.push("dubbla källvägs-id:n");
  for (const m of questionHeadings) {
    const block = text.slice(m.index + m[0].length).split(/^#{1,3} /m)[0];
    for (const field of QUESTION_FIELDS) if (fieldValues(block, field).length !== 1 || !fieldValues(block, field)[0]) errors.push(`${m[1]}: saknar entydigt ${field}`);
    const status = (fieldValues(block, "Slutsatsläge")[0] ?? "").replace(/\.$/, "");
    if (!["ÖPPEN", "STÖDD", "FASTSTÄLLD", "OMSTRIDD", "AVVISAD", "OLÖST INOM PRÖVAT OMFÅNG"].includes(status)) errors.push(`${m[1]}: ogiltigt slutsatsläge`);
    for (const kp of (fieldValues(block, "Källvägar")[0] ?? "").match(/KP-\d{2,}/g) ?? []) if (!pathIds.has(kp)) errors.push(`${m[1]}: okänd källväg ${kp}`);
  }
  for (const id of REQUIREMENTS) {
    const found = rows.filter((row) => row[0] === id);
    if (found.length !== 1 || found[0].length !== 3 || !["EJ GRANSKAT", "EJ STYRKT", "STYRKT"].includes(found[0][1])) errors.push(`${id}: saknar entydig kravbedömning`);
  }
  const dependencies = new Map();
  for (const m of pathHeadings) {
    const block = text.slice(m.index + m[0].length).split(/^#{1,3} /m)[0];
    for (const field of PATH_FIELDS) {
      const values = fieldValues(block, field);
      if (values.length !== 1 || !values[0]) errors.push(`${m[1]}: saknar entydigt ${field}`);
    }
    const classes = (fieldValues(block, "Källklass")[0] ?? "").match(/K-\d{2,}/g) ?? [];
    if (!classes.length || classes.some((id) => !classIds.has(id))) errors.push(`${m[1]}: saknad/okänd källklass`);
    const refs = fieldValues(block, "Frågor/teman")[0] ?? "";
    for (const q of refs.match(/Q-\d{2,}/g) ?? []) if (!questionIds.has(q)) errors.push(`${m[1]}: okänd fråga ${q}`);
    const rawDeps = fieldValues(block, "Föregående källvägar")[0] ?? "";
    const declared = rawDeps === "INGA" ? [] : rawDeps.split(",").map((s) => s.trim());
    const deps = declared.map((dep) => dep.includes("/") ? dep : `${personId}/${dep}`);
    dependencies.set(`${personId}/${m[1]}`, deps);
    for (const dep of deps) {
      if (!/^P-\d{4}\/KP-\d{2,}$/.test(dep) || !(pathExists ? pathExists(dep) : dep.startsWith(`${personId}/`) && pathIds.has(dep.split("/")[1]))) errors.push(`${m[1]}: okänt beroende ${dep}`);
    }
    const task = fieldValues(block, "Wotan")[0] ?? "";
    if (!task.includes("EJ BESLUTAT UTFÖRANDE") && !/T-\d{4}/.test(task)) errors.push(`${m[1]}: saknar Wotan-disposition`);
    for (const tid of task.match(/T-\d{4}/g) ?? []) if (taskIds && !taskIds.has(tid)) errors.push(`${m[1]}: okänd Wotan ${tid}`);
  }
  const visiting = new Set(), visited = new Set();
  function visit(id) {
    if (visiting.has(id)) { errors.push(`cirkulärt källberoende vid ${id}`); return; }
    if (visited.has(id)) return;
    visiting.add(id);
    for (const dep of dependencies.get(id) ?? []) visit(dep);
    visiting.delete(id); visited.add(id);
  }
  for (const id of dependencies.keys()) visit(id);
  for (const [, target] of text.matchAll(LINK)) {
    const error = linkError(target);
    if (error) errors.push(error);
  }
  const approved = states.Kontraktsgranskning === "GODKÄND";
  if (approved) {
    if (!["PRÖVAT", "OLÖST"].includes(states.Identitetsläge)) errors.push("GODKÄND kräver prövad eller sakligt avgränsad identitet");
    if (!["GENOMGÅNGEN", "AVGRÄNSAD", "INTEGRITETSMINIMERAD"].includes(states.Livsbildsläge)) errors.push("GODKÄND kräver avslutad livsbildsbedömning");
    if (states.Källstrategiläge !== "GENOMGÅNGEN") errors.push("GODKÄND kräver genomgången källstrategi");
    if (THEMES.some((id) => !CLOSED_THEMES.includes(themes[id]))) errors.push("GODKÄND får inte dölja öppna eller ej bedömda teman");
    const date = one("Granskningsdatum");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date ?? "") || Number.isNaN(Date.parse(date)) || new Date(date).toISOString().slice(0, 10) !== date) errors.push("GODKÄND kräver giltigt granskningsdatum");
    for (const key of ["Granskningsbelägg", "Tidslinje", "Livsberättelse"]) {
      const value = one(key);
      if (!hasLink(value ?? "")) errors.push(`GODKÄND kräver beläggslänk i ${key}`);
    }
    for (const id of REQUIREMENTS) {
      const found = rows.filter((row) => row[0] === id);
      if (found.length !== 1 || found[0][1] !== "STYRKT" || !hasLink(found[0][2] ?? "")) errors.push(`GODKÄND kräver beläggslänkad prövning av ${id}`);
    }
    if (/^- Slutsatsläge: (ÖPPEN|STÖDD|OMSTRIDD)\b/m.test(text)) errors.push("GODKÄND innehåller öppen materiell fråga");
    if (/^- Undersökt omfång och utfall: (EJ UNDERSÖKT|ÅTKOMSTHINDER)\b/m.test(text)) errors.push("GODKÄND innehåller oprövad/hindrad källpassage");
  }
  return {
    present: true, identity: states.Identitetsläge, biography: states.Livsbildsläge,
    strategy: states.Källstrategiläge, review: states.Kontraktsgranskning, themes, dependencies: Object.fromEntries(dependencies),
    recordedApproval: approved && errors.length === 0, errors,
  };
}

export function validateWotan(backlog, logExists = () => true) {
  const errors = [], ids = new Set();
  for (const task of backlog.tasks) {
    if (!/^T-\d{4}$/.test(task.id) || ids.has(task.id)) errors.push(`ogiltigt/dubbelt Wotan-id ${task.id}`);
    ids.add(task.id);
    if (!["IDEA", "READY", "ONGOING", "BLOCKED", "DONE"].includes(task.status)) errors.push(`${task.id}: ogiltig status`);
    if (task.status !== "IDEA" && !logExists(task.id)) errors.push(`${task.id}: saknar dev-log`);
    if (task.status === "BLOCKED" && !task.blocker?.trim()) errors.push(`${task.id}: saknar blockerare`);
    if (task.status === "DONE" && task.phase) errors.push(`${task.id}: DONE har aktiv fas`);
  }
  if (!Number.isInteger(backlog.next_id) || backlog.next_id <= Math.max(0, ...backlog.tasks.map((t) => Number(t.id.slice(2))))) errors.push("Wotan next_id är inte ledigt");
  const byId = new Map(backlog.tasks.map((t) => [t.id, t]));
  for (const task of backlog.tasks) for (const dep of task.after ?? []) {
    if (!ids.has(dep)) errors.push(`${task.id}: okänd föregångare ${dep}`);
    if (["READY", "ONGOING"].includes(task.status) && byId.get(dep)?.status !== "DONE") errors.push(`${task.id}: körbar trots ofärdigt beroende ${dep}`);
  }
  const visiting = new Set(), visited = new Set();
  function visit(id) {
    if (visiting.has(id)) { errors.push(`cyklisk Wotan-kö vid ${id}`); return; }
    if (visited.has(id)) return;
    visiting.add(id);
    for (const dep of byId.get(id)?.after ?? []) visit(dep);
    visiting.delete(id); visited.add(id);
  }
  for (const id of ids) visit(id);
  if (backlog.tasks.filter((t) => t.status === "ONGOING").length > 1) errors.push("Wotan har flera ONGOING");
  return errors;
}

export function buildInventory(root) {
  const repository = loadRepository(root);
  const state = computeGoalState(repository);
  const ancestors = new Map(state.persons.map((p) => [p.id, p]));
  const profileDir = join(root, "genealogy/research-profiles");
  const backlog = JSON.parse(readFileSync(join(root, "wotan/backlog.json"), "utf8"));
  const taskIds = new Set(backlog.tasks.map((t) => t.id));
  const allPaths = new Set();
  if (existsSync(profileDir)) for (const file of readdirSync(profileDir).filter((f) => /^P-\d{4}\.md$/.test(f))) {
    for (const m of readFileSync(join(profileDir, file), "utf8").matchAll(/^### (KP-\d{2,}): /gm)) allPaths.add(`${file.slice(0, -3)}/${m[1]}`);
  }
  const strategy = readFileSync(join(root, "genealogy/source-strategy.md"), "utf8");
  const classIds = new Set([...strategy.matchAll(/^\| (K-\d{2,}) /gm)].map((m) => m[1]));
  const errors = validateWotan(backlog, (id) => existsSync(join(root, `wotan/dev-log/${id}.md`)));
  const records = [...repository.people].sort(([a], [b]) => a.localeCompare(b)).map(([id, person]) => {
    const profile = join(profileDir, `${id}.md`);
    const text = existsSync(profile) ? readFileSync(profile, "utf8") : null;
    const contract = assessProfile({ personId: id, text, classIds, taskIds, pathExists: (key) => allPaths.has(key), linkError: (target) => checkLocalLink(root, profile, target) });
    errors.push(...contract.errors.map((e) => `${id}: ${e}`));
    const work = readWorkState(person.text), ancestor = ancestors.get(id);
    return {
      id, dossier: `genealogy/people/${person.file}`, dossierSha256: sha(person.text),
      registeredDepth: ancestor?.depth ?? null, registeredSide: ancestor?.side ?? null,
      legacyReviewed: work.reviewed, legacyCoverage: ancestor?.coverageReady ?? null,
      structure: { timelineHeading: /^## Tidslinje\s*$/m.test(person.text), narrativeHeading: /^## (Biografisk sammanfattning|Livsberättelse|Konsoliderad livsbild|Aktuell livsbild)/m.test(person.text) },
      profile: text === null ? null : `genealogy/research-profiles/${id}.md`,
      profileSha256: text === null ? null : sha(text), contract,
    };
  });
  if (existsSync(profileDir)) for (const file of readdirSync(profileDir)) {
    if (/^P-.*\.md$/.test(file) && (!/^P-\d{4}\.md$/.test(file) || !repository.people.has(file.slice(0, -3)))) errors.push(`profil utan entydig personakt: ${file}`);
  }
  errors.push(...dependencyCycles(Object.assign({}, ...records.map((r) => r.contract.dependencies))));
  return {
    schema: "research-inventory/v1", meaning: "Struktur och registrerade bedömningar; inte saklig måluppfyllelse eller arbetskö.",
    contractSha256: sha(readFileSync(join(root, "genealogy/person-contract.md"), "utf8")), sourceStrategySha256: sha(strategy),
    summary: { people: records.length, withProfile: records.filter((r) => r.contract.present).length, withoutProfile: records.filter((r) => !r.contract.present).length, recordedApprovals: records.filter((r) => r.contract.recordedApproval).length, structuralErrors: errors.length },
    records, errors,
  };
}

export function dependencyCycles(graph) {
  const errors = [], visiting = new Set(), visited = new Set();
  function visit(id) {
    if (visiting.has(id)) { errors.push(`cirkulärt källberoende mellan profiler vid ${id}`); return; }
    if (visited.has(id)) return;
    visiting.add(id);
    for (const dep of graph[id] ?? []) visit(dep);
    visiting.delete(id); visited.add(id);
  }
  for (const id of Object.keys(graph)) visit(id);
  return errors;
}

export function formatInventory(inventory) {
  const { summary: s } = inventory;
  return [
    "Personkontrakt: struktur och registrerade bedömningar, inte genealogisk bevisning.",
    `Samtliga personakter: ${s.people}; profiler: ${s.withProfile}; ännu ej införda: ${s.withoutProfile}.`,
    `Registrerade GODKÄND med giltig struktur: ${s.recordedApprovals}; sakrevision krävs vid avslut.`,
    ...["identity", "biography", "strategy"].map((key) => {
      const counts = {};
      for (const record of inventory.records) counts[record.contract[key] ?? "OGILTIGT"] = (counts[record.contract[key] ?? "OGILTIGT"] ?? 0) + 1;
      return `${key}: ${Object.entries(counts).map(([k, v]) => `${k} ${v}`).join(", ")}`;
    }),
    `Strukturfel: ${s.structuralErrors}. Äldre GRANSKAD/KLAR konverteras inte.`,
  ].join("\n");
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const root = resolve(import.meta.dirname, "..");
  const args = process.argv.slice(2), allowed = new Set(["--write", "--check", "--json"]);
  if (args.some((a) => !allowed.has(a)) || (args.includes("--write") && args.includes("--check"))) {
    console.error("Använd: node scripts/research-inventory.mjs [--write | --check] [--json]");
    process.exitCode = 1;
  } else {
    const inventory = buildInventory(root);
    const file = join(root, "genealogy/research-inventory.json");
    const serialized = `${JSON.stringify(inventory, null, 2)}\n`;
    if (inventory.errors.length) { console.error(inventory.errors.join("\n")); process.exitCode = 1; }
    if (args.includes("--write") && !inventory.errors.length) writeFileSync(file, serialized);
    if (args.includes("--check") && (!existsSync(file) || readFileSync(file, "utf8") !== serialized)) {
      console.error("Inventeringen saknas eller är inaktuell; granska ändringarna och kör --write."); process.exitCode = 1;
    }
    console.log(args.includes("--json") ? serialized.trimEnd() : formatInventory(inventory));
  }
}
