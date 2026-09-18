#!/usr/bin/env node
// Task-scoped completion guard for the depth-5 research wave.
// The lists below are manually reviewed from the preserved target images.

import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const peopleDir = join(root, "genealogy", "people");
const citationsDir = join(root, "genealogy", "citations");

const fileById = (directory, prefix) =>
  new Map(
    readdirSync(directory).flatMap((name) => {
      const match = name.match(new RegExp(`^(${prefix}-\\d{4})-`));
      return match ? [[match[1], join(directory, name)]] : [];
    }),
  );

const people = fileById(peopleDir, "P");
const citations = fileById(citationsDir, "C");
const errors = [];

// Every named side person read from a target record must have a dossier that
// points back to that record. Existing direct subjects and ancestors are
// covered separately by the structural baseline.
const namedSidePeople = new Map([
  ["C-0121", ["P-0169", "P-0170", "P-0171"]],
  ["C-0124", ["P-0172", "P-0173", "P-0174", "P-0175"]],
  ["C-0125", ["P-0176", "P-0177", "P-0178"]],
  ["C-0126", ["P-0179", "P-0180", "P-0181", "P-0182"]],
  ["C-0127", ["P-0167", "P-0168"]],
  ["C-0128", ["P-0187", "P-0188", "P-0189", "P-0190"]],
  ["C-0129", ["P-0183", "P-0184", "P-0185", "P-0186"]],
  [
    "C-0133",
    [
      "P-0191", "P-0192", "P-0193", "P-0194", "P-0195", "P-0196",
      "P-0197", "P-0198", "P-0199", "P-0200", "P-0201", "P-0202",
      "P-0203", "P-0204", "P-0205", "P-0206", "P-0207", "P-0208",
      "P-0209",
    ],
  ],
  [
    "C-0134",
    [
      "P-0197", "P-0198", "P-0199", "P-0200", "P-0201", "P-0202",
      "P-0203", "P-0204", "P-0205", "P-0206",
    ],
  ],
]);

for (const [citationId, ids] of namedSidePeople) {
  for (const id of ids) {
    const path = people.get(id);
    if (!path) {
      errors.push(`${citationId}: missing dossier ${id}`);
      continue;
    }
    if (!readFileSync(path, "utf8").includes(`[${citationId}]`)) {
      errors.push(`${citationId}: ${id} lacks a linked provenance reference`);
    }
  }
}

// C-0121–C-0139 are the evidence package created by this wave. Each citation
// must identify a source and preserve every local image with an exact checksum.
let sourceImageCount = 0;
for (let number = 121; number <= 139; number += 1) {
  const id = `C-${String(number).padStart(4, "0")}`;
  const path = citations.get(id);
  if (!path) {
    errors.push(`missing wave citation ${id}`);
    continue;
  }
  const text = readFileSync(path, "utf8");
  if (!/^\[S-\d{4}\]\(\.\.\/sources\//m.test(text)) {
    errors.push(`${id}: missing linked source record`);
  }
  const mediaLinks = [
    ...text.matchAll(/- Fil: \[[^\]]+\]\((\.\.\/media\/[^)]+)\)/g),
  ].map((match) => match[1]);
  const expectedHashes = [
    ...text.matchAll(/- SHA-256: `([0-9a-f]{64})`/g),
  ].map((match) => match[1]);
  if (!mediaLinks.length || mediaLinks.length !== expectedHashes.length) {
    errors.push(`${id}: missing local image or checksum`);
    continue;
  }
  sourceImageCount += mediaLinks.length;
  for (let index = 0; index < mediaLinks.length; index += 1) {
    const mediaPath = resolve(dirname(path), mediaLinks[index]);
    if (!existsSync(mediaPath)) {
      errors.push(`${id}: missing media file ${basename(mediaPath)}`);
      continue;
    }
    const actualHash = createHash("sha256").update(readFileSync(mediaPath)).digest("hex");
    if (actualHash !== expectedHashes[index]) errors.push(`${id}: checksum mismatch`);
  }
}

// P-0126 is not a graph tip because its mother is known. Its unknown paternal
// branch therefore needs an explicit task-level guard of its own.
const p0126Path = people.get("P-0126");
const p0126Text = p0126Path ? readFileSync(p0126Path, "utf8") : "";
if (!p0126Text.includes("## Slutstatus för den okända fadersgrenen") ||
    !p0126Text.includes("Status: `IDENTITET OLÖST`") ||
    !["C-0137", "C-0138", "C-0139"].every((id) => p0126Text.includes(`[${id}]`))) {
  errors.push("P-0126: unknown paternal branch lacks explicit sourced terminal status");
}

// The secondary antavla was preserved because it is visible on C-0133, but
// its unverified generations must not silently become part of the pedigree.
for (let number = 191; number <= 196; number += 1) {
  const id = `P-${String(number).padStart(4, "0")}`;
  const path = people.get(id);
  if (path && !readFileSync(path, "utf8").includes("inte forskad eller registrerad som djup-7-ana") &&
      !readFileSync(path, "utf8").includes("inte öppnat en\nverifierad djup-7-front")) {
    errors.push(`${id}: missing explicit depth-7 exclusion`);
  }
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exitCode = 1;
} else {
  const sideCount = new Set([...namedSidePeople.values()].flat()).size;
  console.log(
    `OK: depth-5 wave package has ${sourceImageCount} source images and ${sideCount} named side-person dossiers with provenance`,
  );
}
