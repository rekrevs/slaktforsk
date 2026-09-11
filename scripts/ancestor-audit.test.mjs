#!/usr/bin/env node

import assert from "node:assert/strict";
import test from "node:test";

import { buildParentMap, deriveDepths } from "./lib/genealogy-relations.mjs";

const person = (text) => ({ text });

test("Swedish prose labels terminate the preceding relationship block", () => {
  const people = new Map([
    ["P-0001", person("# parent one")],
    ["P-0002", person("# parent two")],
    ["P-0004", person(`# proband

## Relationer

Dotter: [P-0005 Child](P-0005-child.md).
Föräldrar: [P-0001 Parent one](P-0001-parent.md)
och [P-0002 Parent two](P-0002-parent.md).
`)],
    ["P-0005", person("# child")],
  ]);

  const parents = buildParentMap(people);
  assert.deepEqual([...parents.get("P-0004")].sort(), ["P-0001", "P-0002"]);
  assert.deepEqual([...parents.get("P-0005")], ["P-0004"]);
});

test("multiword and year-bearing labels terminate parent blocks", () => {
  const people = new Map([
    ["P-0001", person("# parent one")],
    ["P-0002", person("# parent two")],
    ["P-0003", person("# spouse")],
    ["P-0004", person(`# proband

## Relationer

Föräldrar: [P-0001 Parent one](P-0001-parent.md) och
[P-0002 Parent two](P-0002-parent.md).
Make 1930: [P-0003 Spouse](P-0003-spouse.md).
Uppgivna senare barn: [P-0005 Child](P-0005-child.md).
Historisk kandidatpost: [P-0006 Alias](P-0006-alias.md).
`)],
    ["P-0005", person("# child")],
    ["P-0006", person("# alias")],
  ]);

  const parents = buildParentMap(people);
  assert.deepEqual([...parents.get("P-0004")].sort(), ["P-0001", "P-0002"]);
  assert.deepEqual([...parents.get("P-0005")], []);
  assert.deepEqual([...parents.get("P-0006")], []);
});

test("table relations include parents and exclude grandparents and uncertain links", () => {
  const people = new Map([
    ["P-0001", person("# parent")],
    ["P-0002", person("# grandparent")],
    ["P-0003", person("# possible parent")],
    ["P-0005", person("# conflicted parent")],
    ["P-0006", person("# rejected parent")],
    ["P-0007", person("# unverified parent")],
    ["P-0008", person("# owner-confirmed parent")],
    ["P-0004", person(`# child

## Relationer

| Person | Relation | Status |
|---|---|---|
| [P-0001 Parent](P-0001-parent.md) | far | CORROBORATED |
| [P-0002 Grandparent](P-0002-grandparent.md) | morfar | CORROBORATED |
| [P-0003 Possible](P-0003-possible.md) | möjlig mor | LEAD |
| [P-0005 Conflicted](P-0005-conflicted.md) | mor | CONFLICT |
| [P-0006 Rejected](P-0006-rejected.md) | far | REJECTED |
| [P-0007 Unverified](P-0007-unverified.md) | far | LEAD |
| [P-0008 Owner confirmed](P-0008-owner-confirmed.md) | mor | OWNER_CONFIRMED |
`)],
  ]);

  const parents = buildParentMap(people);
  assert.deepEqual([...parents.get("P-0004")], ["P-0001", "P-0008"]);
});

test("derived depths follow the corrected direction", () => {
  const people = new Map([
    ["P-0001", person("# parent")],
    ["P-0004", person("# child\n\n## Relationer\n\nMor: [P-0001 Parent](P-0001-parent.md).")],
  ]);
  const depths = deriveDepths(buildParentMap(people), "P-0004");
  assert.equal(depths.get("P-0001"), 1);
});

test("a colon inside a table cell does not start a prose block", () => {
  const people = new Map([
    ["P-0149", person("# farmor")],
    ["P-0150", person(`# brother

## Relationer

| Person | Relation | Tid/plats | Status | Belägg |
|---|---|---|---|---|
| [P-0151 Sister](P-0151-sister.md) | syskon, förda under \`Barn:\` på samma uppslag | Rödå | TRANSCRIBED | C-0111 |
| [P-0149 Farmor](P-0149-farmor.md) | farmor — förd som \`Moder:\` i hushållet | Rödå | TRANSCRIBED | C-0111 |
`)],
    ["P-0151", person("# sister")],
  ]);

  const parents = buildParentMap(people);
  assert.deepEqual([...parents.get("P-0149")], []);
  assert.deepEqual([...parents.get("P-0150")], []);
  assert.deepEqual([...parents.get("P-0151")], []);
});

test("a kinship word outside the relation head describes someone else", () => {
  const row = (id, relation) => `| [P ${id}](${id}-x.md) | ${relation} | plats | TRANSCRIBED | C-0001 |`;
  const table = (...rows) => `# x\n\n## Relationer\n\n| Person | Relation | Tid/plats | Status | Belägg |\n|---|---|---|---|---|\n${rows.join("\n")}\n`;
  const people = new Map([
    ["P-0009", person(table(row("P-0010", "Arnes far; relation med Ada enligt familjen")))],
    ["P-0010", person(table(row("P-0009", "sonens mor")))],
    ["P-0441", person(table(row("P-0422", "svärfar; död innan hon fick sina barn")))],
    ["P-0422", person("# svärfar")],
    ["P-0214", person(table(row("P-0220", "gemensam son")))],
    ["P-0220", person("# son")],
  ]);
  const parents = buildParentMap(people);
  assert.deepEqual([...parents.get("P-0009")], []);
  assert.deepEqual([...parents.get("P-0010")], []);
  assert.deepEqual([...parents.get("P-0422")], []);
  assert.deepEqual([...parents.get("P-0220")], ["P-0214"]);
});

test("an explicit reservation in the relation cell keeps the edge out", () => {
  const row = (id, relation) => `| [P ${id}](${id}-x.md) | ${relation} | plats | TRANSCRIBED | C-0001 |`;
  const table = (...rows) => `# x\n\n## Relationer\n\n| Person | Relation | Tid/plats | Status | Belägg |\n|---|---|---|---|---|\n${rows.join("\n")}\n`;
  const people = new Map([
    ["P-0225", person(table(
      row("P-0221", "far enligt dotterrollen; biologiskt faderskap inte separat säkrat"),
      row("P-0224", "son i hushållet; biologiskt syskonskap öppet"),
    ))],
    ["P-0221", person("# far?")],
    ["P-0224", person("# son?")],
  ]);
  const parents = buildParentMap(people);
  assert.deepEqual([...parents.get("P-0225")], []);
  assert.deepEqual([...parents.get("P-0224")], []);
});
