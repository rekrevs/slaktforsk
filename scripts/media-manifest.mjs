#!/usr/bin/env node

import { createHash } from "node:crypto";
import {
  existsSync,
  readFileSync,
  readdirSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { basename, join, relative, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const genealogy = join(root, "genealogy");
const mediaDirectory = join(genealogy, "media");
const citationDirectory = join(genealogy, "citations");
const sourceDirectory = join(genealogy, "sources");
const manifestPath = join(genealogy, "media-manifest.json");

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function records(directory, prefix) {
  return readdirSync(directory)
    .filter((name) => new RegExp(`^${prefix}-\\d{4}-.*\\.md$`).test(name))
    .sort()
    .map((name) => {
      const id = name.match(new RegExp(`^(${prefix}-\\d{4})-`))[1];
      const path = join(directory, name);
      return {
        id,
        name,
        path,
        repositoryPath: relative(root, path),
        text: readFileSync(path, "utf8"),
      };
    });
}

const citations = records(citationDirectory, "C");
const sources = records(sourceDirectory, "S");
const sourceById = new Map(sources.map((source) => [source.id, source]));

const media = readdirSync(mediaDirectory, { withFileTypes: true })
  .filter((entry) => entry.isFile() && entry.name !== ".gitkeep")
  .map((entry) => entry.name)
  .sort();

const entries = media.map((name) => {
  const path = join(mediaDirectory, name);
  const digest = sha256(path);
  const filenameCitationId = name.match(/^(C-\d{4})(?:[^0-9]|$)/)?.[1] ?? null;
  const exactMentions = citations.filter((citation) => citation.text.includes(name));
  const filenameCitation = filenameCitationId
    ? citations.find((citation) => citation.id === filenameCitationId)
    : null;
  const linkedCitations = exactMentions.length
    ? exactMentions
    : filenameCitation
      ? [filenameCitation]
      : [];
  const sourceIds = [
    ...new Set(
      linkedCitations.flatMap((citation) =>
        [...citation.text.matchAll(/\[(S-\d{4})\]\(\.\.\/sources\/[^)]+\)/g)].map(
          (match) => match[1],
        ),
      ),
    ),
  ].sort();
  const sourceRecords = sourceIds
    .map((id) => sourceById.get(id)?.repositoryPath ?? null)
    .filter(Boolean);
  const exactChecksumDeclared = exactMentions.some((citation) =>
    citation.text.includes(digest),
  );
  let provenanceLevel = "unlinked";
  if (exactMentions.length && exactChecksumDeclared && sourceRecords.length) {
    provenanceLevel = "exact";
  } else if (linkedCitations.length && sourceRecords.length) {
    provenanceLevel = "source-scoped";
  } else if (linkedCitations.length) {
    provenanceLevel = "citation-scoped";
  }

  return {
    path: relative(root, path),
    bytes: statSync(path).size,
    sha256: digest,
    filename_citation_id: filenameCitationId,
    citation_records: linkedCitations.map((citation) => citation.repositoryPath),
    source_ids: sourceIds,
    source_records: sourceRecords,
    individually_named_in_citation: exactMentions.length > 0,
    exact_checksum_declared_in_citation: exactChecksumDeclared,
    provenance_level: provenanceLevel,
  };
});

const levels = ["exact", "source-scoped", "citation-scoped", "unlinked"];
const summary = Object.fromEntries(
  levels.map((level) => [level.replace("-", "_"), entries.filter((entry) => entry.provenance_level === level).length]),
);
const manifest = {
  schema: "slaktforsk-media-manifest/v1",
  root: "genealogy/media",
  algorithm: "sha256",
  entry_count: entries.length,
  provenance_summary: summary,
  entries,
};
const serialized = `${JSON.stringify(manifest, null, 2)}\n`;

if (process.argv.includes("--write")) {
  writeFileSync(manifestPath, serialized);
  console.log(`Wrote ${relative(root, manifestPath)} with ${entries.length} entries.`);
} else if (process.argv.includes("--check")) {
  if (!existsSync(manifestPath)) {
    console.error(`Missing ${relative(root, manifestPath)}; run with --write.`);
    process.exitCode = 1;
  } else if (readFileSync(manifestPath, "utf8") !== serialized) {
    console.error(`Stale ${relative(root, manifestPath)}; run with --write.`);
    process.exitCode = 1;
  } else {
    console.log(
      `OK: ${entries.length} media files; ` +
        levels.map((level) => `${summary[level.replace("-", "_")]} ${level}`).join(", "),
    );
  }
} else {
  console.error("Usage: node scripts/media-manifest.mjs --write|--check");
  process.exitCode = 2;
}
