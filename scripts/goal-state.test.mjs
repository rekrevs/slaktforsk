#!/usr/bin/env node

import assert from "node:assert/strict";
import test from "node:test";

import { computeGoalState, parseCoverage } from "./goal-state.mjs";
import { readTerminalStatus, readWorkState } from "./lib/terminal-status.mjs";

const person = (title, body) => ({ title, text: `# ${title}\n\n${body}` });
const rel = (rows) =>
  `## Relationer\n\n| Person | Relation | Status | Belägg |\n|---|---|---|---|\n${rows
    .map(([id, r, s]) => `| [${id} x](${id}-x.md) | ${r} | ${s ?? "TRANSCRIBED"} | C-0001 |`)
    .join("\n")}\n`;
const work = (state, extra = "") => `## Arbetsläge\n\n- Konsolidering: \`${state}\` 2026-09-04 (test)\n${extra}`;
const front = (status) =>
  `## Slutstatus\n\n- Status: \`${status}\`\n- Förväntad källa: x\n- Genomsökt: y\n- Negativ kontroll: [C-0001](../citations/C-0001-x.md)\n`;

function fixture({ reviewedDepth1 = true, coverageOverride = true, validFront = true } = {}) {
  const people = new Map([
    ["P-0269", person("Adam", rel([["P-0004", "far"], ["P-0210", "mor"]]))],
    ["P-0270", person("Axel", rel([["P-0004", "far"], ["P-0210", "mor"]]))],
    [
      "P-0004",
      person(
        "Sverker",
        rel([["P-0005", "far"], ["P-0006", "mor"]]) +
          (reviewedDepth1 ? work("GRANSKAD", coverageOverride ? "- Källbredd: `INTEGRITETSMINIMERAD`\n" : "") : ""),
      ),
    ],
    [
      "P-0210",
      person("Kristina", rel([["P-0211", "mor", "LEAD"]]) + work("GRANSKAD", "- Källbredd: `INTEGRITETSMINIMERAD`\n") + front(validFront ? "ÅTKOMSTSPÄRR" : "OKÄND")),
    ],
    ["P-0005", person("Far", work("GRANSKAD") + front("KÄLLOR SLUT"))],
    ["P-0006", person("Mor", work("EJ GRANSKAD") + front("KÄLLOR SLUT"))],
    ["P-0211", person("Evy", "")],
  ]);
  const coverageText = `| Person | Nuvarande kärnfråga | F | H | M | V | D | R | B | T | J | O |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P-0005 Far | q | \`✓\` | \`✓\` | \`N\` | \`✓\` | \`✓\` | \`✓\` | \`—\` | \`2\` | \`—\` | \`—\` |
| P-0006 Mor | q | \`✓\` | \`✓\` | \`1\` | \`✓\` | \`✓\` | \`✓\` | \`—\` | \`2\` | \`—\` | \`—\` |
`;
  return { people, coverageText, citationExists: (cid) => cid === "C-0001" };
}

test("coverage rows parse ten backticked cells and ignore other tables", () => {
  const rows = parseCoverage(fixture().coverageText + "| P-0210 K | `I`: text | no | no |\n");
  assert.deepEqual([...rows.keys()], ["P-0005", "P-0006"]);
  assert.equal(rows.get("P-0006").M, "1");
  assert.equal(rows.get("P-0005").T, "2");
});

test("work state defaults to EJ GRANSKAD and reads the coverage override", () => {
  assert.equal(readWorkState("# x\n\n## Påståenden\n").reviewed, false);
  const w = readWorkState("# x\n\n## Arbetsläge\n\n- Konsolidering: `GRANSKAD` 2026-09-04 (identity-review-2026-09-04.md)\n- Källbredd: `INTEGRITETSMINIMERAD`\n\n## Annat\n");
  assert.equal(w.reviewed, true);
  assert.equal(w.reviewedOn, "2026-09-04");
  assert.equal(w.reviewRef, "identity-review-2026-09-04.md");
  assert.equal(w.coverageOverride, "INTEGRITETSMINIMERAD");
});

test("terminal status requires a resolvable negative control unless VERIFIERAD", () => {
  assert.equal(readTerminalStatus(front("KÄLLOR SLUT"), () => false).ok, false);
  assert.equal(readTerminalStatus(front("KÄLLOR SLUT"), () => true).ok, true);
  assert.equal(readTerminalStatus("## Slutstatus\n\n- Status: `VERIFIERAD`\n", () => false).ok, true);
});

test("depth 1 is treated when both parents are reviewed and coverage-ready, LEAD does not propagate", () => {
  const state = computeGoalState(fixture());
  assert.deepEqual(state.notes, []);
  const d1 = state.depths.find((d) => d.depth === 1);
  assert.equal(d1.known, 2);
  assert.equal(d1.treated, true);
  assert.equal(state.sharedDepth, 1);
  const d2 = state.depths.find((d) => d.depth === 2);
  // Kristina has no propagating parent: two positions closed by her valid front.
  assert.equal(d2.known, 2);
  assert.equal(d2.closed, 2);
  assert.equal(d2.open, 0);
  assert.equal(d2.treated, false);
  assert.equal(state.nextSlice.depth, 2);
  assert.deepEqual(state.nextSlice.sides.S.unreviewed.map((p) => p.id), ["P-0006"]);
  assert.deepEqual(state.nextSlice.sides.S.coverageOpen.map((p) => p.id), ["P-0006"]);
  assert.deepEqual(state.nextSlice.sides.K.frontOpen, []);
  assert.equal(state.persons.find((p) => p.id === "P-0211"), undefined);
});

test("an invalid front on a half-tip keeps the generation untreated and counts unsearched positions", () => {
  const state = computeGoalState(fixture({ validFront: false }));
  const d1 = state.depths.find((d) => d.depth === 1);
  assert.equal(d1.treated, false);
  assert.equal(d1.frontOpenUpTo, 1);
  assert.equal(state.sharedDepth, 0);
  assert.deepEqual(state.nextSlice.sides.K.frontOpen.map((p) => p.id), ["P-0210"]);
  const d2 = state.depths.find((d) => d.depth === 2);
  assert.equal(d2.closed, 0);
  assert.equal(d2.open, 2);
});

test("a missing coverage row without override is not coverage-ready", () => {
  const state = computeGoalState(fixture({ coverageOverride: false }));
  const s = state.persons.find((p) => p.id === "P-0004");
  assert.equal(s.coverageRow, false);
  assert.equal(s.coverageReady, false);
  assert.equal(state.sharedDepth, 0);
});
