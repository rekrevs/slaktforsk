#!/usr/bin/env node

import { createHash } from "node:crypto";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const genealogy = join(root, "genealogy");
const errors = [];

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? walk(path) : [path];
  });
}

const markdown = walk(genealogy).filter((path) => path.endsWith(".md"));

for (const path of markdown) {
  const text = readFileSync(path, "utf8");
  for (const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
    const target = match[1].split("#", 1)[0];
    if (!target || /^[a-z]+:/i.test(target)) continue;
    const absolute = resolve(dirname(path), target);
    if (!existsSync(absolute)) {
      errors.push(`broken link: ${relative(root, path)} -> ${target}`);
    }
  }
}

for (const [directory, prefix] of [
  ["people", "P"],
  ["sources", "S"],
  ["citations", "C"],
]) {
  const ids = new Map();
  for (const name of readdirSync(join(genealogy, directory))) {
    const match = name.match(new RegExp(`^${prefix}-(\\d{4})-`));
    if (!match) continue;
    const id = `${prefix}-${match[1]}`;
    if (ids.has(id)) errors.push(`duplicate ${id}: ${ids.get(id)}, ${name}`);
    ids.set(id, name);
  }
}

const assertions = new Map();
for (const path of markdown.filter((path) => path.includes("/people/"))) {
  const text = readFileSync(path, "utf8");
  for (const match of text.matchAll(/^\| (A-\d{4}) \|/gm)) {
    if (assertions.has(match[1])) {
      errors.push(
        `duplicate assertion ${match[1]}: ${relative(root, assertions.get(match[1]))}, ${relative(root, path)}`,
      );
    }
    assertions.set(match[1], path);
  }
}

for (const path of markdown.filter((path) => path.includes("/citations/"))) {
  const text = readFileSync(path, "utf8");
  const fileMatches = [
    ...text.matchAll(/- Fil: \[[^\]]+\]\((\.\.\/media\/[^)]+)\)/g),
  ];
  const hashMatches = [...text.matchAll(/- SHA-256: `([0-9a-f]{64})`/g)];
  if (!fileMatches.length && !hashMatches.length) continue;
  if (!fileMatches.length || fileMatches.length !== hashMatches.length) {
    errors.push(`incomplete media provenance: ${relative(root, path)}`);
    continue;
  }
  for (let index = 0; index < fileMatches.length; index += 1) {
    const mediaPath = resolve(dirname(path), fileMatches[index][1]);
    if (!existsSync(mediaPath) || !statSync(mediaPath).isFile()) continue;
    const actual = createHash("sha256").update(readFileSync(mediaPath)).digest("hex");
    if (actual !== hashMatches[index][1]) {
      errors.push(`checksum mismatch: ${relative(root, mediaPath)}`);
    }
  }
}

const backlogPath = join(root, "wotan", "backlog.json");
const backlog = JSON.parse(readFileSync(backlogPath, "utf8"));
const ongoing = backlog.tasks.filter((task) => task.status === "ONGOING");
if (ongoing.length > 1) errors.push(`multiple ONGOING Wotan tasks: ${ongoing.map((t) => t.id).join(", ")}`);

if (errors.length) {
  console.error(errors.join("\n"));
  process.exitCode = 1;
} else {
  console.log(
    `OK: ${assertions.size} assertions; ${markdown.length} Markdown records; ` +
      `${walk(join(genealogy, "media")).length} media files; Wotan JSON valid.`,
  );
}
