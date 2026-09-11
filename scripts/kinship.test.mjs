import test from "node:test";
import assert from "node:assert/strict";
import { kinTerm, inferSexes, ancestorPaths, ancestorBlock, render, parseRole, sideBlocks } from "./kinship.mjs";
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


test("rollord tolkas ur huvudledet, med reservation och hushållsform", () => {
  assert.equal(parseRole("syster").kind, "K");
  assert.deepEqual(parseRole("möjlig son"), { noun: "son", hedge: "möjlig", prefix: "", qual: "", kind: "R" });
  assert.equal(parseRole("person i familjehushållet").noun, "hushållsmedlem");
  assert.equal(parseRole("son i hushållet").prep, "hos");
  assert.equal(parseRole("halvsyster på fädernet").qual, "på fädernet");
  assert.equal(parseRole("bror och dopvittne"), null);
});

const family = () => new Map([
  dossier("P-0269", "Adam", row("P-0004", "far")),
  dossier("P-0270", "Axel", row("P-0004", "far")),
  dossier("P-0004", "Sverker", row("P-0010", "far"), row("P-0022", "syster"), row("P-0031", "hustru"), row("P-0040", "dopvittne"), row("P-0050", "bror och dopvittne")),
  dossier("P-0010", "Farfar"),
  dossier("P-0022", "Faster"),
  dossier("P-0023", "Kusin", row("P-0022", "mor")),
  dossier("P-0031", "Ingift", row("P-0004", "make")),
  dossier("P-0040", "Vittne"),
  dossier("P-0050", "Oklar"),
  dossier("P-0060", "Osäker", row("P-0004", "bror")),
]);
const sidePhrases = new Map([["P-0004", "far"], ["P-0010", "farfar"]]);
const flat = (text) => text.replace(/\n/g, " ").replace(/\]\([^)]*\)/g, "]");

test("sidopersoner: släkt får kompakt etikett, ingifta och vittnen sin roll", () => {
  const people = family();
  const { blocks } = sideBlocks(people, inferSexes(people), sidePhrases);
  assert.equal(flat(blocks.get("P-0022").text), "**Släktled:** faster till [Adam] och [Axel] — syster till [Sverker].");
  // Inget i raderna anger P-0023:s kön, så ordet blir könsneutralt.
  assert.equal(flat(blocks.get("P-0023").text), "**Släktled:** fasters barn till [Adam] och [Axel] — barn till [Faster].");
  assert.equal(flat(blocks.get("P-0031").text), "**Släktled:** hustru till [Sverker], far till [Adam] och [Axel].");
  assert.equal(flat(blocks.get("P-0040").text), "**Släktled:** dopvittne vid dopet av [Sverker], far till [Adam] och [Axel].");
  assert.match(flat(blocks.get("P-0050").text), /^\*\*Släktled:\*\* ingen känd släktskap/);
});

test("en reservation i endera aktens rad gör relationen obekräftad", () => {
  const people = family();
  people.get("P-0004").text = people.get("P-0004").text.replace("## Tidslinje", `${row("P-0060", "syskon").replace("TRANSCRIBED", "LEAD")}\n\n## Tidslinje`);
  const { blocks } = sideBlocks(people, inferSexes(people), sidePhrases);
  assert.match(flat(blocks.get("P-0060").text), /^\*\*Släktled:\*\* obekräftat syskon till \[Sverker\]/);
});
