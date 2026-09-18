#!/usr/bin/env node
// Räknar projektets läge mot north star (NORTH-STAR.md, avsnittet "Mått").
//
// Generationerna räknas från Adam och Axel (P-0269, P-0270): djup 1 är deras
// föräldrar Sverker (P-0004) och Kristina (P-0210), djup d har 2^d anpositioner.
// För varje djup rapporteras kända personer, positioner som stängts av en
// giltig arkivfront, öppna positioner, konsoliderade (GRANSKAD) personer,
// källbredd-klara personer och om generationen är behandlad. Därefter det
// gemensamma djupet och nästa skiva, fördelad per sida.
//
//   node scripts/goal-state.mjs            läsbar rapport
//   node scripts/goal-state.mjs --json     maskinläsbart läge
//   node scripts/goal-state.mjs --depth=N  visa skivan för djup N i stället

import { readFileSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { buildParentMap } from "./lib/genealogy-relations.mjs";
import { readTerminalStatus, readWorkState } from "./lib/terminal-status.mjs";

export const ROOT_ID = "ROOT";
export const SONS = ["P-0269", "P-0270"];
export const SIDES = { "P-0004": "S", "P-0210": "K" };
export const SIDE_NAMES = { S: "Sverkers sida", K: "Kristinas sida", B: "båda sidor" };
export const COVERAGE_COLUMNS = ["F", "H", "M", "V", "D", "R", "B", "T", "J", "O"];

export function parseCoverage(text) {
  const rows = new Map();
  const cell = String.raw`\s*\`([^\`]*)\`\s*\|`;
  const re = new RegExp(String.raw`^\|\s*(P-\d{4})[^|]*\|[^|]*\|((?:${cell}){10})\s*$`, "gm");
  for (const m of text.matchAll(re)) {
    const cells = [...m[2].matchAll(/`([^`]*)`/g)].map((c) => c[1].trim());
    rows.set(m[1], Object.fromEntries(COVERAGE_COLUMNS.map((k, i) => [k, cells[i]])));
  }
  return rows;
}

export function computeGoalState({ people, coverageText, citationExists }) {
  const parents = buildParentMap(people);
  const notes = [];
  for (const son of SONS) {
    const p = parents.get(son) ?? new Set();
    for (const parent of Object.keys(SIDES)) {
      if (!p.has(parent)) notes.push(`${son} saknar propagerande relation till ${parent}`);
    }
  }
  parents.set(ROOT_ID, new Set(Object.keys(SIDES)));

  // Djup och sida via BFS från roten.
  const depth = new Map([[ROOT_ID, 0]]);
  const side = new Map();
  const queue = [ROOT_ID];
  while (queue.length) {
    const cur = queue.shift();
    for (const parent of parents.get(cur) ?? []) {
      const s = SIDES[parent] ?? side.get(cur) ?? "B";
      if (!depth.has(parent)) {
        depth.set(parent, depth.get(cur) + 1);
        side.set(parent, s);
        queue.push(parent);
      } else if (side.get(parent) !== s) {
        side.set(parent, "B");
      }
    }
  }

  const coverage = parseCoverage(coverageText);
  const ancestors = [...depth.keys()].filter((id) => id !== ROOT_ID);
  const persons = new Map();
  for (const id of ancestors) {
    const text = people.get(id).text;
    const known = parents.get(id)?.size ?? 0;
    const missing = 2 - known;
    const front = missing > 0 ? readTerminalStatus(text, citationExists) : null;
    const work = readWorkState(text);
    const row = coverage.get(id) ?? null;
    const openCells = row ? COVERAGE_COLUMNS.filter((k) => row[k] === "1") : [];
    const coverageReady = row !== null
      ? openCells.length === 0
      : work.coverageOverride === "INTEGRITETSMINIMERAD" ||
        (work.coverageOverride === "KLAR" && Boolean(work.coverageJustification));
    persons.set(id, {
      id,
      title: people.get(id).title ?? id,
      depth: depth.get(id),
      side: side.get(id),
      knownParents: known,
      missingParents: missing,
      front: front ? { valid: front.ok, status: front.status ?? null, why: front.why ?? null } : null,
      reviewed: work.reviewed,
      reviewedOn: work.reviewedOn,
      reviewRef: work.reviewRef,
      coverageRow: row !== null,
      coverageOverride: work.coverageOverride,
      coverageOpenCells: openCells,
      coverageReady,
    });
  }

  const maxDepth = Math.max(0, ...ancestors.map((id) => depth.get(id)));
  const depths = [];
  let sharedDepth = 0;
  let sharedBroken = false;
  for (let d = 1; d <= maxDepth; d += 1) {
    const at = [...persons.values()].filter((p) => p.depth === d);
    const per = (list) => ({
      known: list.length,
      reviewed: list.filter((p) => p.reviewed).length,
      coverageReady: list.filter((p) => p.coverageReady).length,
      frontOpen: list.filter((p) => p.front && !p.front.valid).length,
    });
    // Positioner på djup d som stängts av en giltig arkivfront på djup k < d.
    let closed = 0;
    let unsearched = 0;
    for (const p of persons.values()) {
      if (p.depth < d && p.missingParents > 0) {
        const n = p.missingParents * 2 ** (d - p.depth - 1);
        if (p.front?.valid) closed += n;
        else unsearched += n;
      }
    }
    const positions = 2 ** d;
    const open = Math.max(0, positions - at.length - closed);
    const collapse = at.length + closed + unsearched - positions;
    const frontOpenUpTo = [...persons.values()].filter(
      (p) => p.depth <= d && p.front && !p.front.valid,
    ).length;
    const treated =
      at.length > 0 &&
      frontOpenUpTo === 0 &&
      at.every((p) => p.reviewed && p.coverageReady);
    if (!treated) sharedBroken = true;
    if (!sharedBroken) sharedDepth = d;
    depths.push({
      depth: d,
      positions,
      ...per(at),
      closed,
      open,
      collapse: collapse > 0 ? collapse : 0,
      frontOpenUpTo,
      treated,
      sides: {
        S: per(at.filter((p) => p.side === "S")),
        K: per(at.filter((p) => p.side === "K")),
      },
    });
  }

  const sliceDepth = Math.min(sharedDepth + 1, maxDepth);
  const slice = { depth: sliceDepth, sides: {} };
  for (const s of ["S", "K", "B"]) {
    const inSide = (p) => p.side === s;
    const frontOpen = [...persons.values()]
      .filter((p) => p.depth <= sliceDepth && inSide(p) && p.front && !p.front.valid)
      .sort(byDepthId);
    const unreviewed = [...persons.values()]
      .filter((p) => p.depth === sliceDepth && inSide(p) && !p.reviewed)
      .sort(byDepthId);
    const coverageOpen = [...persons.values()]
      .filter((p) => p.depth === sliceDepth && inSide(p) && !p.coverageReady)
      .sort(byDepthId);
    if (frontOpen.length || unreviewed.length || coverageOpen.length || s !== "B") {
      slice.sides[s] = { frontOpen, unreviewed, coverageOpen };
    }
  }

  return {
    root: { sons: SONS, depth1: Object.keys(SIDES) },
    notes,
    persons: [...persons.values()].sort(byDepthId),
    depths,
    sharedDepth,
    nextSlice: slice,
  };
}

function byDepthId(a, b) {
  return a.depth - b.depth || a.id.localeCompare(b.id);
}

export function formatReport(state, { sliceDepth } = {}) {
  const out = [];
  out.push("Registrerade indikatorer; formell giltighet och frånvaro av prioritet 1 bevisar inte north stars uppfyllelse. Villkorliga 2-celler kräver sakprövning.");
  out.push(`Proband: Adam och Axel (${SONS.join(", ")}); djup 1 = ${state.root.depth1.join(", ")}`);
  out.push("Personernas separata kontrakts-/livsbildsläge: node scripts/research-inventory.mjs (äldre KLAR är inte nytt godkännande).");
  for (const n of state.notes) out.push(`VARNING: ${n}`);
  out.push("");
  out.push("djup | positioner | kända | stängda | öppna | granskade | källbredd-klara | osökta fronter ≤ djup | behandlad");
  for (const d of state.depths) {
    out.push(
      `${String(d.depth).padStart(4)} | ${String(d.positions).padStart(10)} | ${String(d.known).padStart(5)} | ` +
        `${String(d.closed).padStart(7)} | ${String(d.open).padStart(5)} | ${String(d.reviewed).padStart(9)} | ` +
        `${String(d.coverageReady).padStart(15)} | ${String(d.frontOpenUpTo).padStart(21)} | ${d.treated ? "ja" : "nej"}` +
        (d.collapse ? `   (anförlust/överlapp: ${d.collapse})` : ""),
    );
  }
  out.push("");
  out.push(`Registrerat gemensamt djup: ${state.sharedDepth}`);
  const slice = sliceDepth
    ? recomputeSlice(state, sliceDepth)
    : state.nextSlice;
  out.push(`Nästa skiva: djup ${slice.depth}`);
  for (const [s, part] of Object.entries(slice.sides)) {
    const sd = state.depths.find((d) => d.depth === slice.depth)?.sides?.[s];
    out.push(`  ${SIDE_NAMES[s]}${sd ? ` (kända ${sd.known}, granskade ${sd.reviewed}, källbredd-klara ${sd.coverageReady})` : ""}`);
    list(out, "anspetsar utan giltig arkivfront", part.frontOpen, (p) => `${p.front.status ? `${p.front.status}: ` : ""}${p.front.why ?? ""}`);
    list(out, "ej granskade", part.unreviewed, () => "");
    list(out, "ej källbredd-klara", part.coverageOpen, (p) =>
      p.coverageRow ? `oprövade: ${p.coverageOpenCells.join(" ")}` : "ingen matrisrad",
    );
  }
  return out.join("\n");
}

function recomputeSlice(state, d) {
  const slice = { depth: d, sides: {} };
  for (const s of ["S", "K", "B"]) {
    const ps = state.persons.filter((p) => p.side === s);
    const part = {
      frontOpen: ps.filter((p) => p.depth <= d && p.front && !p.front.valid),
      unreviewed: ps.filter((p) => p.depth === d && !p.reviewed),
      coverageOpen: ps.filter((p) => p.depth === d && !p.coverageReady),
    };
    if (s !== "B" || part.frontOpen.length || part.unreviewed.length || part.coverageOpen.length) {
      slice.sides[s] = part;
    }
  }
  return slice;
}

function list(out, label, items, detail) {
  out.push(`    ${label}: ${items.length}`);
  for (const p of items) {
    const extra = detail(p);
    out.push(`      ${p.id} (djup ${p.depth})  ${p.title}${extra ? `  — ${extra}` : ""}`);
  }
}

export function loadRepository(root) {
  const peopleDir = join(root, "genealogy", "people");
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
  const citationFiles = readdirSync(join(root, "genealogy", "citations"));
  const citationExists = (cid) => citationFiles.some((name) => name.startsWith(`${cid}-`));
  const coverageText = readFileSync(join(root, "genealogy", "source-coverage.md"), "utf8");
  return { people, coverageText, citationExists };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const root = resolve(import.meta.dirname, "..");
  const state = computeGoalState(loadRepository(root));
  const depthArg = process.argv.find((a) => a.startsWith("--depth="));
  const sliceDepth = depthArg ? Number.parseInt(depthArg.split("=")[1], 10) : undefined;
  if (process.argv.includes("--json")) {
    const { persons, ...rest } = state;
    console.log(JSON.stringify({ generatedAt: new Date().toISOString(), ...rest, persons }, null, 2));
  } else {
    console.log(formatReport(state, { sliceDepth }));
  }
}
