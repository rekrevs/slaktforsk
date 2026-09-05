#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const genealogy = join(root, "genealogy");
const data = JSON.parse(
  readFileSync(join(root, "dashboard", "public", "data", "project.json"), "utf8"),
);

// En beställd ögonblicksbild får ligga kvar medan forskningen fortsätter.
assert.equal(data.stats.people, data.people.length, "personantalet ska stämma inom ögonblicksbilden");
assert.equal(data.stats.assertions, data.people.reduce((sum, person) => sum + person.claims.length, 0), "påståenderäkningen ska stämma inom ögonblicksbilden");
assert.equal(new Set(data.people.map((person) => person.id)).size, data.people.length, "person-id ska vara unika");
if (data.activeWork) {
  assert.ok(["ONGOING", "READY"].includes(data.activeWork.status), "sparat aktivt arbete är pågående eller nästa READY");
}

// Aktualitet kontrolleras uttryckligen efter en beställd uppdatering.
if (process.env.GENEALOGY_DASHBOARD_CHECK_CURRENT === "1") {
  const markdownCount = (dir) =>
    readdirSync(dir).filter((name) => name.endsWith(".md")).length;

  const peopleFiles = readdirSync(join(genealogy, "people")).filter((name) => name.endsWith(".md"));
  const assertionCount = peopleFiles.reduce((sum, file) => {
    const text = readFileSync(join(genealogy, "people", file), "utf8");
    return sum + [...text.matchAll(/^\|\s*A-\d{4}\s*\|/gm)].length;
  }, 0);

  assert.equal(data.stats.people, peopleFiles.length, "personantalet ska följa personakterna");
  assert.equal(data.stats.assertions, assertionCount, "alla påståenderader ska tas med");
  assert.equal(data.stats.sources, markdownCount(join(genealogy, "sources")));
  assert.equal(data.stats.citations, markdownCount(join(genealogy, "citations")));
  const backlog = JSON.parse(readFileSync(join(root, "wotan", "backlog.json"), "utf8"));
  const isDone = (id) => backlog.tasks.find((task) => task.id === id)?.status === "DONE";
  const expectedActive =
    backlog.tasks.find((task) => task.status === "ONGOING") ??
    backlog.tasks.find((task) => task.status === "READY" && (task.after ?? []).every(isDone)) ??
    null;
  if (expectedActive) {
    assert.equal(data.activeWork?.id, expectedActive.id, "aktiv eller nästa körbar uppgift ska visas");
    assert.ok(["ONGOING", "READY"].includes(data.activeWork.status), "aktivt arbete är pågående eller nästa READY");
  } else {
    assert.equal(data.activeWork, null, "tom körbar kö ska visas som viloläge");
  }
}

const people = new Set(data.people.map((person) => person.id));
const directedEdges = new Set();
const parentCounts = new Map();
const parentsByChild = new Map();
for (const edge of data.parentEdges) {
  assert.ok(people.has(edge.child), `okänt barn i trädet: ${edge.child}`);
  assert.ok(people.has(edge.parent), `okänd förälder i trädet: ${edge.parent}`);
  assert.notEqual(edge.child, edge.parent, `självrefererande föräldralänk: ${edge.child}`);
  const key = `${edge.child}->${edge.parent}`;
  assert.ok(!directedEdges.has(key), `duplicerad föräldralänk: ${key}`);
  directedEdges.add(key);
  parentCounts.set(edge.child, (parentCounts.get(edge.child) ?? 0) + 1);
  if (!parentsByChild.has(edge.child)) parentsByChild.set(edge.child, []);
  parentsByChild.get(edge.child).push(edge.parent);
}

assert.ok(
  ["P-0001", "P-0002"].every((parent) =>
    data.parentEdges.some((edge) => edge.child === "P-0006" && edge.parent === parent),
  ),
  "P-0006:s OWNER_CONFIRMED-föräldrar ska visas som verifierade länkar",
);

for (const child of ["P-0039", "P-0040", "P-0041"]) {
  assert.ok(
    ["P-0001", "P-0002"].every((parent) =>
      data.parentEdges.some((edge) => edge.child === child && edge.parent === parent),
    ),
    `${child}:s OWNER_CONFIRMED-föräldrar ska visas som verifierade länkar`,
  );
}

for (const child of ["P-0012", "P-0013", "P-0014"]) {
  const person = data.people.find((entry) => entry.id === child);
  assert.ok(
    person?.relations.some(
      (relation) => relation.target === "P-0010" && relation.status === "OWNER_CONFIRMED",
    ),
    `${child}:s relation till P-0010 ska vara OWNER_CONFIRMED`,
  );
}

for (const edge of data.parentEdges) {
  assert.ok(
    !directedEdges.has(`${edge.parent}->${edge.child}`),
    `ömsesidig föräldralänk: ${edge.child}<->${edge.parent}`,
  );
}

for (const [child, count] of parentCounts) {
  assert.ok(count <= 2, `fler än två föräldrar för ${child}: ${count}`);
}

const visiting = new Set();
const visited = new Set();
const assertAcyclic = (person) => {
  if (visited.has(person)) return;
  assert.ok(!visiting.has(person), `cykel i föräldragrafen vid ${person}`);
  visiting.add(person);
  for (const parent of parentsByChild.get(person) ?? []) assertAcyclic(parent);
  visiting.delete(person);
  visited.add(person);
};
for (const person of people) assertAcyclic(person);

for (const branch of data.progress) {
  const ancestors = new Set();
  const collect = (id) => {
    for (const parent of parentsByChild.get(id) ?? []) {
      if (ancestors.has(parent)) continue;
      ancestors.add(parent);
      collect(parent);
    }
  };
  collect(branch.id);
  assert.equal(branch.knownAncestors, ancestors.size, `anantalet ska följa den sparade grafen för ${branch.id}`);
}

for (const person of data.people) {
  for (const claim of person.claims) {
    assert.ok(claim.id.startsWith("A-"), `ogiltigt påstående-id hos ${person.id}`);
    assert.ok(claim.status, `status saknas för ${claim.id}`);
    assert.equal(
      new Set(claim.citations).size,
      claim.citations.length,
      `duplicerat belägg i ${claim.id}`,
    );
  }
}

const changeKeys = data.recentChanges.map((entry) => `${entry.date}-${String(entry.batch).padStart(4, "0")}`);
assert.deepEqual(changeKeys, [...changeKeys].sort().reverse(), "senaste forskning ska ligga först");

console.log(process.env.GENEALOGY_DASHBOARD_CHECK_CURRENT === "1"
  ? "Dashboarddata och aktualitet verifierade"
  : "Dashboardens sparade ögonblicksbild verifierad (ingen uppdatering eller aktualitetskontroll)");
