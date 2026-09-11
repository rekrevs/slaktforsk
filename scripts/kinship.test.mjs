import test from "node:test";
import assert from "node:assert/strict";
import { kinTerm, inferSexes, ancestorPaths, ancestorBlock, render } from "./kinship.mjs";
import { buildParentMap } from "./lib/genealogy-relations.mjs";

test("parorden följer ägarens konvention", () => {
  assert.equal(kinTerm("f"), "far");
  assert.equal(kinTerm("m"), "mor");
  assert.equal(kinTerm("ff"), "farfar");
  assert.equal(kinTerm("fff"), "farfars far");
  assert.equal(kinTerm("ffmm"), "farfars mormor");
  assert.equal(kinTerm("fmfm"), "farmors farmor");
  assert.equal(kinTerm("mmmmm"), "mormors mormors mor");
});

const table = (...rows) => `## Relationer\n\n| Person | Relation | Tid/plats | Status | Belägg |\n|---|---|---|---|---|\n${rows.join("\n")}\n\n## Tidslinje\n`;
const row = (id, relation) => `| [${id}](${id}-x.md) | ${relation} | plats | TRANSCRIBED | C-0001 |`;
const dossier = (id, name, ...rows) => [id, { file: `${id}-x.md`, name, text: `# ${id}: ${name}\n\n## Arbetsläge\n\n${table(...rows)}` }];

test("könet läses ur huvudledet; roller mot en tredje person räknas inte", () => {
  const people = new Map([
    dossier("P-0001", "Barn", row("P-0002", "uppgiven far"), row("P-0003", "mor")),
    dossier("P-0002", "Fadern", row("P-0003", "uppgiven mor till någon annan")),
    dossier("P-0003", "Modern"),
  ]);
  const sexes = inferSexes(people);
  assert.equal(sexes.get("P-0002"), "m");
  assert.equal(sexes.get("P-0003"), "f");
});

test("etikett, generation, väg och pronomen", () => {
  const people = new Map([
    dossier("P-0269", "Adam", row("P-0004", "far")),
    dossier("P-0270", "Axel", row("P-0004", "far")),
    dossier("P-0004", "Sverker", row("P-0005", "far")),
    dossier("P-0005", "Jan-Christer", row("P-0007", "mor")),
    dossier("P-0007", "Maj Amalia"),
  ]);
  const paths = ancestorPaths(buildParentMap(people), inferSexes(people));
  const block = ancestorBlock(people, "P-0007", paths.get("P-0007")).text.replace(/\n/g, " ");
  assert.match(block, /^\*\*Släktled:\*\* farfars mor till \[Adam\]/);
  assert.match(block, /generation 3\./);
  assert.match(block, /Vägen: \[Sverker\]\(P-0004-x\.md\) → \[Jan-Christer\]\(P-0005-x\.md\) → hon\.$/);
});

test("raden står mellan namnet och första avsnittet och skrivs om utan att dubbleras", () => {
  const text = "# P-0007: Maj Amalia\n\n## Arbetsläge\n\ntext\n";
  const once = render(text, "**Släktled:** farfars mor.");
  assert.equal(once, "# P-0007: Maj Amalia\n\n**Släktled:** farfars mor.\n\n## Arbetsläge\n\ntext\n");
  assert.equal(render(once, "**Släktled:** farfars mor."), once);
});
