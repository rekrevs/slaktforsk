#!/usr/bin/env node
// Härledd inventering och strukturgrind, aldrig automatisk genealogisk bevisning.
import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { loadRetired } from "./lib/retired.mjs";
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
// Identitetsnivån är antavlans grind; livsbildsnivån får ligga efter. Se
// person-contract.md, avsnittet "Två färdignivåer".
export const IDENTITY_REQUIREMENTS = ["PK-01", "PK-02", "PK-05", "PK-07", "PK-09", "PK-11", "PK-12"];
export const BIOGRAPHY_REQUIREMENTS = REQUIREMENTS.filter((id) => !IDENTITY_REQUIREMENTS.includes(id));
const OPTIONAL_FIELDS = {
  "Identitetsgranskning": ["EJ GRANSKAD", "UNDERKÄND", "GODKÄND"],
  "Trädverkan": ["BÄRANDE", "EJ BÄRANDE", "AVVAKTAR"],
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
  if (text === null) return { present: false, identity: "EJ BEDÖMT", biography: "EJ BEDÖMT", strategy: "EJ BEDÖMT", review: "EJ INFÖRT", identityReview: "EJ INFÖRT", identityReviewDerived: false, treeEffect: "AVVAKTAR", themes: {}, dependencies: {}, recordedApproval: false, recordedIdentityApproval: false, errors: [] };
  const errors = [];
  function one(key, allowed) {
    const values = fieldValues(text, key);
    if (values.length !== 1 || !values[0] || (allowed && !allowed.includes(values[0]))) errors.push(`${key}: kräver exakt ett giltigt värde`);
    return values[0] ?? null;
  }
  one("Kontrakt", ["person-research/v1"]);
  one("Person", [personId]);
  const states = Object.fromEntries(Object.entries(FIELDS).map(([key, values]) => [key, one(key, values)]));
  // Valfria fält: saknas de gäller nolläget. Äldre profiler blir därmed inte
  // ogiltiga av att nivåuppdelningen införs, men de blir heller inte godkända.
  function optional(key, allowed, fallback) {
    const values = fieldValues(text, key);
    if (values.length === 0) return null;
    if (values.length !== 1 || !values[0] || !allowed.includes(values[0])) { errors.push(`${key}: kräver exakt ett giltigt värde`); return null; }
    return values[0];
  }
  const statedIdentityReview = optional("Identitetsgranskning", OPTIONAL_FIELDS["Identitetsgranskning"]);
  const treeEffect = optional("Trädverkan", OPTIONAL_FIELDS["Trädverkan"]) ?? "AVVAKTAR";
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
  // Full granskning är en övermängd av identitetsnivån. Saknas det uttryckliga
  // fältet härleds det därför ur GODKÄND; ett uttryckligt avvikande värde är
  // däremot en motsägelse och inte något som får härledas bort.
  if (approved && statedIdentityReview && statedIdentityReview !== "GODKÄND") errors.push("Kontraktsgranskning GODKÄND kräver godkänd identitetsgranskning");
  const identityApproved = statedIdentityReview === "GODKÄND" || (approved && statedIdentityReview === null);
  const identityReviewDerived = identityApproved && statedIdentityReview === null;
  if (statedIdentityReview === "GODKÄND") {
    if (!["PRÖVAT", "OLÖST"].includes(states.Identitetsläge)) errors.push("Identitetsgranskning GODKÄND kräver prövad eller sakligt avgränsad identitet");
    const date = one("Granskningsdatum");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date ?? "") || Number.isNaN(Date.parse(date)) || new Date(date).toISOString().slice(0, 10) !== date) errors.push("Identitetsgranskning GODKÄND kräver giltigt granskningsdatum");
    if (!hasLink(one("Granskningsbelägg") ?? "")) errors.push("Identitetsgranskning GODKÄND kräver beläggslänk i Granskningsbelägg");
    for (const id of IDENTITY_REQUIREMENTS) {
      const found = rows.filter((row) => row[0] === id);
      if (found.length !== 1 || found[0][1] !== "STYRKT" || !hasLink(found[0][2] ?? "")) errors.push(`Identitetsgranskning GODKÄND kräver beläggslänkad prövning av ${id}`);
    }
  }
  // Grinden: en olöst identitet kan vara korrekt avgränsad, men får aldrig
  // bära en anlinje uppåt.
  if (treeEffect === "BÄRANDE") {
    if (!identityApproved) errors.push("Trädverkan BÄRANDE kräver godkänd identitetsgranskning");
    if (states.Identitetsläge !== "PRÖVAT") errors.push("Trädverkan BÄRANDE kräver Identitetsläge PRÖVAT");
  }
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
    strategy: states.Källstrategiläge, review: states.Kontraktsgranskning,
    identityReview: statedIdentityReview ?? (identityApproved ? "GODKÄND" : "EJ GRANSKAD"),
    identityReviewDerived, treeEffect, themes, dependencies: Object.fromEntries(dependencies),
    recordedApproval: approved && errors.length === 0,
    recordedIdentityApproval: identityApproved && errors.length === 0, errors,
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
  // Avvecklade akter (PCD-2026-09-11-034) står kvar men räknas inte.
  const retired = loadRetired(root);
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
      retired: retired.has(id),
    };
  });
  const active = records.filter((r) => !r.retired);
  if (existsSync(profileDir)) for (const file of readdirSync(profileDir)) {
    if (/^P-.*\.md$/.test(file) && (!/^P-\d{4}\.md$/.test(file) || !repository.people.has(file.slice(0, -3)))) errors.push(`profil utan entydig personakt: ${file}`);
  }
  errors.push(...dependencyCycles(Object.assign({}, ...records.map((r) => r.contract.dependencies))));
  return {
    schema: "research-inventory/v1", meaning: "Struktur och registrerade bedömningar; inte saklig måluppfyllelse eller arbetskö.",
    contractSha256: sha(readFileSync(join(root, "genealogy/person-contract.md"), "utf8")), sourceStrategySha256: sha(strategy),
    summary: {
      people: active.length, retired: records.length - active.length,
      withProfile: active.filter((r) => r.contract.present).length,
      withoutProfile: active.filter((r) => !r.contract.present).length,
      recordedApprovals: active.filter((r) => r.contract.recordedApproval).length,
      recordedIdentityApprovals: active.filter((r) => r.contract.recordedIdentityApproval).length,
      treeBearing: active.filter((r) => r.contract.treeEffect === "BÄRANDE").length,
      tiers: tierSummary(active), structuralErrors: errors.length,
    },
    records, errors,
  };
}

// Nivåerna redovisas per djup och slås aldrig ihop till ett mått: en
// generation kan vara trädklar utan att vara livsbildsklar, och den
// uppskjutna skulden ska synas i stället för att döljas.
export function tierSummary(records) {
  const rows = new Map();
  for (const record of records) {
    const depth = record.registeredDepth;
    if (depth === null || depth === undefined) continue;
    const row = rows.get(depth) ?? { depth, known: 0, identityApproved: 0, treeBearing: 0, fullApproved: 0 };
    row.known += 1;
    if (record.contract.recordedIdentityApproval) row.identityApproved += 1;
    if (record.contract.treeEffect === "BÄRANDE") row.treeBearing += 1;
    if (record.contract.recordedApproval) row.fullApproved += 1;
    rows.set(depth, row);
  }
  return [...rows.values()].sort((a, b) => a.depth - b.depth);
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
    `Aktiva personakter: ${s.people}; profiler: ${s.withProfile}; ännu ej införda: ${s.withoutProfile}. Avvecklade: ${s.retired ?? 0}.`,
    `Registrerade GODKÄND med giltig struktur: ${s.recordedApprovals}; sakrevision krävs vid avslut.`,
    `Identitetsnivå: ${s.recordedIdentityApprovals} godkända, varav ${s.treeBearing} med Trädverkan BÄRANDE.`,
    "djup | kända | identitetsgodkända | bärande | livsbildsgodkända",
    ...s.tiers.map((t) => `${String(t.depth).padStart(4)} | ${String(t.known).padStart(5)} | ${String(t.identityApproved).padStart(18)} | ${String(t.treeBearing).padStart(7)} | ${String(t.fullApproved).padStart(17)}`),
    ...["identity", "biography", "strategy", "identityReview", "treeEffect"].map((key) => {
      const counts = {};
      for (const record of inventory.records.filter((r) => !r.retired)) counts[record.contract[key] ?? "OGILTIGT"] = (counts[record.contract[key] ?? "OGILTIGT"] ?? 0) + 1;
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
