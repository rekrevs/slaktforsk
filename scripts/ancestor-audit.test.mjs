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
    ["P-0004", person(`# child

## Relationer

| Person | Relation | Status |
|---|---|---|
| [P-0001 Parent](P-0001-parent.md) | far | CORROBORATED |
| [P-0002 Grandparent](P-0002-grandparent.md) | morfar | CORROBORATED |
| [P-0003 Possible](P-0003-possible.md) | möjlig mor | LEAD |
`)],
  ]);

  const parents = buildParentMap(people);
  assert.deepEqual([...parents.get("P-0004")], ["P-0001"]);
});

test("derived depths follow the corrected direction", () => {
  const people = new Map([
    ["P-0001", person("# parent")],
    ["P-0004", person("# child\n\n## Relationer\n\nMor: [P-0001 Parent](P-0001-parent.md).")],
  ]);
  const depths = deriveDepths(buildParentMap(people), "P-0004");
  assert.equal(depths.get("P-0001"), 1);
});
