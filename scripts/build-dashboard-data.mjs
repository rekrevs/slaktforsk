#!/usr/bin/env node

import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { buildParentMap, deriveDepths } from "./lib/genealogy-relations.mjs";

const root = resolve(import.meta.dirname, "..");
const genealogy = join(root, "genealogy");
const peopleDir = join(genealogy, "people");
const outputDir = join(root, "dashboard", "public", "data");
const outputFile = join(outputDir, "project.json");

const markdownFiles = (dir) =>
  readdirSync(dir).filter((name) => name.endsWith(".md")).sort();

const plainText = (value = "") =>
  value
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/`|\*+/g, "")
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/\s+/g, " ")
    .trim();

const section = (text, heading) => {
  const header = text.match(new RegExp(`^## ${heading}\\s*$`, "m"));
  if (!header || header.index === undefined) return "";
  const bodyStart = header.index + header[0].length;
  const rest = text.slice(bodyStart);
  const nextHeading = rest.search(/^## /m);
  return (nextHeading === -1 ? rest : rest.slice(0, nextHeading)).trim();
};

const tableRows = (body) => {
  const lines = body.split("\n").filter((line) => /^\s*\|/.test(line));
  if (lines.length < 2) return [];
  const cells = (line) =>
    line.trim().replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim());
  const headers = cells(lines[0]);
  return lines.slice(2).map((line) =>
    Object.fromEntries(headers.map((header, index) => [header, cells(line)[index] ?? ""])),
  );
};

const personFiles = markdownFiles(peopleDir);
const rawPeople = new Map();

for (const file of personFiles) {
  const id = file.match(/^(P-\d{4})-/)?.[1];
  if (!id) continue;
  const text = readFileSync(join(peopleDir, file), "utf8");
  const name = text.match(/^#\s*P-\d{4}:\s*(.+)$/m)?.[1]?.trim() ?? id;
  rawPeople.set(id, { file, title: name, text });
}

const parentMap = buildParentMap(rawPeople);
const probands = [
  { id: "P-0004", label: "Sverker Adam" },
  { id: "P-0210", label: "Kristina" },
];
const depthsByProband = new Map(
  probands.map(({ id }) => [id, deriveDepths(parentMap, id)]),
);

const relationRows = (text) =>
  tableRows(section(text, "Relationer"))
    .map((row) => {
      const targetCell = row.Person ?? row.Personer ?? "";
      const target = targetCell.match(/\((P-\d{4})[^)]*\)/)?.[1];
      if (!target) return null;
      return {
        target,
        relation: plainText(row.Relation),
        status: plainText(row.Status),
      };
    })
    .filter(Boolean);

const yearFor = (claims, pattern) => {
  for (const claim of claims) {
    const text = claim.statement.toLowerCase();
    const year = text.match(new RegExp(`(?:${pattern.source})[^0-9]{0,36}(1[6-9]\\d{2}|20\\d{2})`))?.[1];
    if (year) return Number(year);
  }
  return null;
};

const people = [...rawPeople.entries()].map(([id, person]) => {
  const claims = tableRows(section(person.text, "Påståenden"))
    .map((row) => ({
      id: plainText(row.ID),
      statement: plainText(row.Påstående),
      status: plainText(row.Status ?? row.Evidensstatus),
      reliability: plainText(row.Tillförlitlighet),
      citations: [...new Set(
        [...(row.Belägg ?? "").matchAll(/C-\d{4}/g)].map((match) => match[0]),
      )],
    }))
    .filter((claim) => claim.id.startsWith("A-"));
  const researchStatus = plainText(section(person.text, "Forskningsstatus"));
  const identity = plainText(section(person.text, "Identitet"));
  const born = yearFor(claims, /född|föddes|födelse/);
  const died = yearFor(claims, /dog|död|dödsdatum|dödstid/);
  const livingPrivate = !died && (born === null || born >= 1926) && /Integritetsnot|Identitet och integritet|Integritetsminimerad/i.test(person.text);
  const hasConflict = claims.some((claim) => claim.status === "CONFLICT");
  const hasCorroborated = claims.some((claim) => claim.status === "CORROBORATED");
  const unresolved = /OLÖST|ÖPPEN|KÄLLLUCKA|ARKIVLUCKA|ÅTKOMSTSPÄRR/i.test(researchStatus);

  return {
    id,
    name: person.title,
    identity,
    researchStatus,
    state: hasConflict ? "conflict" : unresolved ? "open" : hasCorroborated ? "documented" : "lead",
    lifespan: livingPrivate ? "Nutida" : born ? `${born}–${died ?? ""}` : died ? `–${died}` : "Årtal saknas",
    private: livingPrivate,
    claims,
    relations: relationRows(person.text),
    branches: probands.filter(({ id: proband }) => depthsByProband.get(proband)?.has(id)).map(({ id: proband }) => proband),
    depths: Object.fromEntries(
      probands
        .map(({ id: proband }) => [proband, depthsByProband.get(proband)?.get(id)])
        .filter(([, depth]) => depth !== undefined),
    ),
  };
});

const progress = probands.map((proband) => {
  const depths = depthsByProband.get(proband.id);
  const maxDepth = Math.max(...depths.values());
  return {
    ...proband,
    knownAncestors: depths.size - 1,
    generations: Array.from({ length: Math.min(maxDepth, 7) }, (_, index) => {
      const depth = index + 1;
      return {
        depth,
        known: [...depths.values()].filter((value) => value === depth).length,
        possible: 2 ** depth,
      };
    }),
  };
});

const logEntries = markdownFiles(join(genealogy, "research-log")).flatMap((file) => {
  const date = file.replace(/\.md$/, "");
  const text = readFileSync(join(genealogy, "research-log", file), "utf8");
  return text.split(/^## /m).slice(1).map((block) => {
    const [heading, ...bodyLines] = block.split("\n");
    const batch = Number(heading.match(/batch\s+(\d+)/i)?.[1] ?? 0);
    const paragraphs = bodyLines.join("\n").split(/\n\s*\n/).map(plainText).filter(Boolean);
    const summary = paragraphs.find((paragraph) =>
      !/Chrome|runtime|pluginversion|styrd[a]? flik|AppleScript|kakextraktion|sandbox/i.test(paragraph),
    ) ?? paragraphs[0] ?? "";
    return {
      date,
      batch,
      title: plainText(heading.replace(/^T-\d+\s+batch\s+\d+\s*[—–-]\s*/i, "")),
      summary: summary.length > 320 ? `${summary.slice(0, 317)}…` : summary,
    };
  });
});

logEntries.sort((a, b) => a.date === b.date ? b.batch - a.batch : b.date.localeCompare(a.date));

const backlog = JSON.parse(readFileSync(join(root, "wotan", "backlog.json"), "utf8"));
// Wotan är en ändlig kö: mellan två uppgifter finns ingen ONGOING. Visa då
// nästa READY-uppgift vars beroenden är DONE, så att dashboarden alltid pekar
// på det pågående eller nästa arbetet.
const isDone = (id) => backlog.tasks.find((task) => task.id === id)?.status === "DONE";
const activeTask =
  backlog.tasks.find((task) => task.status === "ONGOING") ??
  backlog.tasks.find((task) => task.status === "READY" && (task.after ?? []).every(isDone)) ??
  null;
const assertionStatuses = people.flatMap((person) => person.claims).reduce((counts, claim) => {
  counts[claim.status] = (counts[claim.status] ?? 0) + 1;
  return counts;
}, {});

const data = {
  generatedAt: `${logEntries[0]?.date ?? "1970-01-01"}T12:00:00.000Z`,
  project: {
    title: "Släktforskningsöversikt",
    subtitle: "Människorna, grenarna och det pågående arbetet",
  },
  activeWork: activeTask ? {
    id: activeTask.id,
    status: activeTask.status,
    phase: activeTask.phase ?? "",
    summary: activeTask.summary,
    latest: logEntries[0] ?? null,
  } : null,
  stats: {
    people: people.length,
    assertions: people.reduce((sum, person) => sum + person.claims.length, 0),
    sources: markdownFiles(join(genealogy, "sources")).length,
    citations: markdownFiles(join(genealogy, "citations")).length,
    media: readdirSync(join(genealogy, "media")).filter((name) => !name.startsWith(".")).length,
    assertionStatuses,
  },
  progress,
  people,
  parentEdges: [...parentMap.entries()].flatMap(([child, parents]) =>
    [...parents].map((parent) => ({
      child,
      parent,
      relation: people.find((person) => person.id === child)?.relations.find((relation) => relation.target === parent)?.relation ?? "förälder",
    })),
  ),
  recentChanges: logEntries.slice(0, 8),
};

mkdirSync(outputDir, { recursive: true });
writeFileSync(outputFile, `${JSON.stringify(data, null, 2)}\n`);
console.log(`Dashboarddata: ${data.stats.people} personer, ${data.stats.assertions} påståenden, ${data.parentEdges.length} föräldralänkar`);
