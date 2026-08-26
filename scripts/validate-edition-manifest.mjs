#!/usr/bin/env node

import { existsSync, readFileSync, readdirSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const root = resolve(scriptDir, "..");
const manifestPath = resolve(
  root,
  process.argv[2] ?? "genealogy/editions/adam-axel-depth4-v1.json",
);

const errors = [];
const allowedStatuses = new Set([
  "CORROBORATED",
  "TRANSCRIBED",
  "LEAD",
  "CONFLICT",
  "UNKNOWN",
]);
const allowedPrecisions = new Set([
  "exact-date",
  "year",
  "year-cluster",
  "approximate-year",
  "bounded-period",
  "decade",
]);

function idsIn(directory, prefix) {
  return new Set(
    readdirSync(directory)
      .map((name) => name.match(new RegExp(`^(${prefix}-\\d{4})`))?.[1])
      .filter(Boolean),
  );
}

function checkStatus(value, context) {
  if (!allowedStatuses.has(value)) errors.push(`${context}: invalid status ${value}`);
}

function checkCitations(citations, context, { allowEmpty = false } = {}) {
  if (!Array.isArray(citations) || (!allowEmpty && citations.length === 0)) {
    errors.push(`${context}: missing citations`);
    return;
  }
  for (const id of citations) {
    if (!citationIds.has(id)) errors.push(`${context}: unknown citation ${id}`);
  }
}

if (!existsSync(manifestPath)) {
  console.error(`Edition manifest not found: ${manifestPath}`);
  process.exit(1);
}

const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
const personIds = idsIn(join(root, "genealogy", "people"), "P");
const citationIds = idsIn(join(root, "genealogy", "citations"), "C");

if (manifest.schema !== "slaktforsk.family-edition.v1") {
  errors.push(`unsupported schema: ${manifest.schema}`);
}
if (manifest.roots?.length !== 2) errors.push("exactly two sibling roots are required");
for (const rootPerson of manifest.roots ?? []) {
  if (!personIds.has(rootPerson.person_id)) errors.push(`unknown root ${rootPerson.person_id}`);
  if (!rootPerson.display_name.endsWith(" Janson")) {
    errors.push(`root surname must be Janson: ${rootPerson.display_name}`);
  }
  checkCitations(rootPerson.citations, `root ${rootPerson.person_id}`);
}

const expectedDepthCounts = new Map([
  [0, 2],
  [1, 2],
  [2, 4],
  [3, 8],
  [4, 16],
]);
const positions = manifest.pedigree?.positions ?? [];
for (const [depth, expected] of expectedDepthCounts) {
  const actual = positions.filter((position) => position.depth === depth).length;
  if (actual !== expected) errors.push(`depth ${depth}: expected ${expected} positions, got ${actual}`);
}
const positionCodes = new Set();
for (const position of positions) {
  if (positionCodes.has(position.code)) errors.push(`duplicate pedigree position ${position.code}`);
  positionCodes.add(position.code);
  if (position.person_id && !personIds.has(position.person_id)) {
    errors.push(`${position.code}: unknown person ${position.person_id}`);
  }
  if (!position.person_id) {
    if (!position.terminal_status) errors.push(`${position.code}: null person without terminal status`);
    checkCitations(position.citations, `${position.code} terminal position`);
  }
}

const links = manifest.pedigree?.parent_links ?? [];
if (links.length !== 32) errors.push(`expected 32 parent links, got ${links.length}`);
for (const [index, link] of links.entries()) {
  const context = `parent link ${index + 1} (${link.child})`;
  if (!personIds.has(link.child)) errors.push(`${context}: unknown child`);
  if (link.parent && !personIds.has(link.parent)) errors.push(`${context}: unknown parent ${link.parent}`);
  if (!link.parent && link.status !== "UNKNOWN") errors.push(`${context}: null parent must be UNKNOWN`);
  if (link.status === "LEAD" && !link.display_warning) {
    errors.push(`${context}: LEAD must carry a display warning`);
  }
  checkStatus(link.status, context);
  checkCitations(link.citations, context);
}

const pedigreePersonIds = new Set(positions.map((position) => position.person_id).filter(Boolean));
for (const lead of manifest.leads_not_promoted ?? []) {
  if (!personIds.has(lead.person_id)) errors.push(`unknown unpromoted lead ${lead.person_id}`);
  if (pedigreePersonIds.has(lead.person_id)) {
    errors.push(`lead was promoted into pedigree: ${lead.person_id}`);
  }
  if (lead.status !== "LEAD") errors.push(`${lead.person_id}: unpromoted lead must have LEAD status`);
  checkCitations(lead.citations, `unpromoted lead ${lead.person_id}`);
}

for (const portrait of manifest.portraits ?? []) {
  if (!personIds.has(portrait.person_id)) errors.push(`portrait: unknown person ${portrait.person_id}`);
  if (!portrait.summary) errors.push(`portrait ${portrait.person_id}: missing summary`);
  if (!portrait.siblings?.text) errors.push(`portrait ${portrait.person_id}: missing sibling context`);
  checkStatus(portrait.siblings?.status, `portrait ${portrait.person_id} siblings`);
  checkCitations(portrait.citations, `portrait ${portrait.person_id}`);
  checkCitations(
    portrait.siblings?.citations,
    `portrait ${portrait.person_id} siblings`,
    { allowEmpty: portrait.siblings?.status === "UNKNOWN" },
  );
}

const generation4 = manifest.generation4_profiles ?? [];
if (generation4.length !== 16) errors.push(`generation 4: expected 16 profiles, got ${generation4.length}`);
for (const profile of generation4) {
  if (profile.person_id && !personIds.has(profile.person_id)) {
    errors.push(`generation 4: unknown person ${profile.person_id}`);
  }
  checkStatus(profile.status, `generation 4 ${profile.display_name}`);
  checkCitations(profile.citations, `generation 4 ${profile.display_name}`);
}

const placeIds = new Set();
for (const place of manifest.map?.places ?? []) {
  const context = `map place ${place.id}`;
  if (placeIds.has(place.id)) errors.push(`duplicate ${context}`);
  placeIds.add(place.id);
  for (const field of [
    "label",
    "region",
    "coordinate_query",
    "coordinate_match",
    "period",
    "branch",
  ]) {
    if (!place[field]) errors.push(`${context}: missing ${field}`);
  }
  if (!Number.isFinite(place.lat) || !Number.isFinite(place.lon)) {
    errors.push(`${context}: invalid coordinates`);
  }
  if (typeof place.approximate !== "boolean") errors.push(`${context}: approximation flag missing`);
  if (!Array.isArray(place.people) || place.people.length === 0) errors.push(`${context}: no linked people`);
  for (const personId of place.people ?? []) {
    if (!personIds.has(personId)) errors.push(`${context}: unknown person ${personId}`);
  }
  if (!Array.isArray(place.events) || place.events.length === 0) errors.push(`${context}: no events`);
  checkCitations(place.citations, context);
}
for (const movement of manifest.map?.movements ?? []) {
  const context = `map movement ${movement.from} -> ${movement.to}`;
  if (!placeIds.has(movement.from) || !placeIds.has(movement.to)) {
    errors.push(`${context}: unknown endpoint`);
  }
  if (!allowedPrecisions.has(movement.precision)) errors.push(`${context}: invalid precision`);
  checkStatus(movement.status, context);
  checkCitations(movement.citations, context);
}

for (const [index, event] of (manifest.timeline ?? []).entries()) {
  const context = `timeline event ${index + 1}`;
  if (!event.date || !event.text) errors.push(`${context}: missing date or text`);
  if (!allowedPrecisions.has(event.precision)) errors.push(`${context}: invalid precision ${event.precision}`);
  checkStatus(event.status, context);
  checkCitations(event.citations, context);
  for (const personId of event.people ?? []) {
    if (!personIds.has(personId)) errors.push(`${context}: unknown person ${personId}`);
  }
}

if (!existsSync(resolve(root, manifest.close_reading?.image ?? ""))) {
  errors.push(`close reading image missing: ${manifest.close_reading?.image}`);
}
checkCitations([manifest.close_reading?.citation], "close reading");

for (const section of manifest.source_explanations ?? []) {
  if (!section.heading || !section.explanation) errors.push("source explanation missing prose");
  checkCitations(section.used_citations, `source explanation ${section.type}`);
}

if (errors.length > 0) {
  console.error(`Edition manifest invalid: ${basename(manifestPath)}`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(
  `OK: ${basename(manifestPath)}; ${positions.length} positions; ${links.length} parent links; ` +
    `${manifest.map.places.length} map places; ${manifest.timeline.length} timeline events.`,
);
