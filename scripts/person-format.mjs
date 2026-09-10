#!/usr/bin/env node
// Read-only presentation check. This never certifies genealogical evidence.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const DOSSIER_HEADINGS = ['Arbetsläge', 'Identitet', 'Namnformer', 'Påståenden', 'Relationer', 'Tidslinje', 'Boställen och flyttar', 'Yrke, utbildning och ekonomi', 'Militärt, civilt och rättsligt', 'Hälsa och död', 'Media och personliga källor', 'Biografisk sammanfattning', 'Forskningsfrågor och konflikter', 'Historik och rättelser'];
export const PROFILE_HEADINGS = ['Identitetsbedömning', 'Söknycklar', 'Livsteman', 'Forskningsfrågor', 'Källvägar', 'Kontraktsgranskning'];
const OPTIONAL = ['Integritetsnot', 'Slutstatus'];
const FIELDS = ['Kontrakt', 'Person', 'Identitetsläge', 'Livsbildsläge', 'Källstrategiläge', 'Identitetsgranskning', 'Trädverkan', 'Kontraktsgranskning', 'Granskningsdatum', 'Granskningsbelägg', 'Tidslinje', 'Livsberättelse'];

// Fenced examples are not headings, fields or tables in the document.
function linesOutsideFences(text) {
  let fence = null;
  return text.split(/\r?\n/).map((line, i) => {
    const match = line.match(/^\s{0,3}(`{3,}|~{3,})/);
    if (match) {
      if (!fence) fence = match[1];
      else if (match[1][0] === fence[0] && match[1].length >= fence.length) fence = null;
      return { line: '', number: i + 1 };
    }
    return { line: fence ? '' : line, number: i + 1 };
  });
}
function cells(line) {
  // GFM escaped pipes belong to a cell, not its column boundary.
  return line.trim().slice(1, -1).split(/(?<!\\)\|/).map(x => x.trim());
}
function sections(lines) {
  const result = [];
  let current = null;
  let nested = false;
  for (const entry of lines) {
    const h2 = entry.line.match(/^## (.+?)\s*$/);
    if (h2) {
      current = { name: h2[1], number: entry.number, direct: [] };
      result.push(current);
      nested = false;
    } else if (/^#{3,6} /.test(entry.line)) nested = true;
    else if (current && !nested) current.direct.push(entry);
  }
  return result;
}
function tables(entries) {
  const found = [];
  let current = null;
  for (const e of entries) {
    if (/^\s*\|.*\|\s*$/.test(e.line)) {
      if (!current) { current = []; found.push(current); }
      current.push({ ...e, cells: cells(e.line) });
    } else current = null;
  }
  return found;
}
function templateHeaders(text) {
  return new Map(sections(linesOutsideFences(text)).flatMap(s => {
    const t = tables(s.direct)[0];
    return t ? [[s.name, t[0].cells]] : [];
  }));
}
export function checkPersonFormat({ text, kind = 'dossier', personId, templateText }) {
  if (!['dossier', 'profile'].includes(kind)) throw new Error(`Unknown document kind: ${kind}`);
  const errors = [];
  if (text === null) return ['saknad fil'];
  const lines = linesOutsideFences(text);
  const h1 = lines.filter(x => /^# /.test(x.line));
  const prefix = kind === 'dossier' ? `# ${personId}: ` : `# Forskningsprofil för ${personId}`;
  if (h1.length !== 1 || !h1[0].line.startsWith(prefix)) errors.push('H1: kräver personens entydiga titel');
  const actual = sections(lines);
  const expected = kind === 'dossier' ? DOSSIER_HEADINGS : PROFILE_HEADINGS;
  const allowed = kind === 'dossier' ? [...expected, ...OPTIONAL] : expected;
  for (const name of expected) if (actual.filter(s => s.name === name).length !== 1) errors.push(`${name}: kräver exakt en H2`);
  for (const s of actual) if (!allowed.includes(s.name)) errors.push(`rad ${s.number}: otillåten H2 ${s.name}`);
  const mandatory = actual.filter(s => expected.includes(s.name)).map(s => s.name);
  if (JSON.stringify(mandatory) !== JSON.stringify(expected)) errors.push('H2: fel rubrikordning eller antal');
  if (kind === 'dossier') {
    const question = actual.findIndex(s => s.name === 'Forskningsfrågor och konflikter');
    const history = actual.findIndex(s => s.name === 'Historik och rättelser');
    for (const name of OPTIONAL) {
      const matches = actual.map((s, i) => s.name === name ? i : -1).filter(i => i >= 0);
      if (matches.length > 1 || matches.some(i => i <= question || i >= history)) errors.push(`${name}: får finnas en gång mellan frågor och historik`);
    }
  } else {
    for (const field of FIELDS) {
      const values = lines.filter(e => e.line.startsWith(`- ${field}:`));
      if (values.length !== 1 || !values[0].line.slice(field.length + 3).trim()) errors.push(`${field}: kräver exakt ett icke-tomt status-/profilfält`);
    }
  }
  const template = templateText ?? readFileSync(join(ROOT, 'genealogy/templates', kind === 'dossier' ? 'person.md' : 'research-profile.md'), 'utf8');
  for (const [name, header] of templateHeaders(template)) {
    const section = actual.find(s => s.name === name);
    if (!section) continue;
    const found = tables(section.direct);
    if (found.length !== 1) errors.push(`${name}: kräver exakt en huvudtabell före eventuella H3`);
    if (!found[0]) continue;
    const rows = found[0];
    if (JSON.stringify(rows[0].cells) !== JSON.stringify(header)) errors.push(`${name}: fel tabellhuvud; väntat ${header.join(' | ')}`);
    if (!rows[1] || rows[1].cells.some(c => !/^:?-{3,}:?$/.test(c))) errors.push(`${name}: saknad eller felaktig tabellavskiljare`);
    for (const row of rows) if (row.cells.length !== header.length) errors.push(`${name}, rad ${row.number}: ${row.cells.length} kolumner, väntat ${header.length}`);
  }
  errors.push(...checkHeadingStyle(lines, kind));
  return errors;
}
// Rubrikstandarden (T-0633). Rader inne i bevarade citatblock börjar med '>'
// och matchas därför aldrig av dessa mönster.
export function checkHeadingStyle(lines, kind) {
  const errors = [];
  let previous = 0;
  let section = null;
  for (const entry of lines) {
    const heading = entry.line.match(/^(#{1,6}) (.*)$/);
    if (!heading) continue;
    const level = heading[1].length;
    if (previous && level > previous + 1) errors.push(`rad ${entry.number}: rubriknivå hoppas över, H${previous} följs av H${level}`);
    if (heading[2].includes('**')) errors.push(`rad ${entry.number}: rubrik får inte innehålla fetstil`);
    if (level === 2) section = heading[2].trim();
    else if (level >= 3 && kind === 'dossier' && section === 'Identitet') errors.push(`rad ${entry.number}: Identitet är sammanhållen prosa och tar inga underrubriker`);
    previous = level;
  }
  return errors;
}
export function boldDensity(text) {
  const body = text.split(/\r?\n/).filter(l => !/^\s*>/.test(l)).join('\n');
  const spans = body.match(/\*\*[\s\S]+?\*\*/g)?.length ?? 0;
  return { words: body.split(/\s+/).filter(Boolean).length, spans };
}
export function checkRepositoryPeople(root, ids) {
  const files = readdirSync(join(root, 'genealogy/people'));
  const result = [];
  for (const personId of ids) {
    const matched = files.filter(f => f.startsWith(`${personId}-`) && f.endsWith('.md'));
    if (matched.length !== 1) { result.push({ personId, kind: 'dossier', errors: ['kräver exakt en personakt'] }); continue; }
    for (const kind of ['dossier', 'profile']) {
      const file = join(root, 'genealogy', kind === 'dossier' ? `people/${matched[0]}` : `research-profiles/${personId}.md`);
      const templateText = readFileSync(join(root, 'genealogy/templates', kind === 'dossier' ? 'person.md' : 'research-profile.md'), 'utf8');
      result.push({ personId, kind, errors: checkPersonFormat({ personId, kind, text: existsSync(file) ? readFileSync(file, 'utf8') : null, templateText }) });
    }
  }
  return result;
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const args = process.argv.slice(2);
  if (!args.length || (args.includes('--all') && args.length !== 1) || args.some(a => a !== '--all' && !/^P-\d{4}$/.test(a))) {
    console.error('Usage: node scripts/person-format.mjs P-0004 P-0293 | --all');
    process.exitCode = 2;
  } else {
    const ids = args[0] === '--all' ? readdirSync(join(ROOT, 'genealogy/people')).map(f => f.match(/^(P-\d{4})-.*\.md$/)?.[1]).filter(Boolean).sort() : [...new Set(args)];
    const results = checkRepositoryPeople(ROOT, ids);
    for (const r of results) for (const error of r.errors) console.error(`${r.personId} ${r.kind}: ${error}`);
    const count = results.reduce((sum, r) => sum + r.errors.length, 0);
    console.log(`person-dossier/v1: ${ids.length} personer, ${count} formatfel. Ingen saklig bevisprövning.`);
    const density = ids.flatMap(id => ['people', 'research-profiles'].map(dir => {
      const file = dir === 'people'
        ? readdirSync(join(ROOT, 'genealogy/people')).filter(f => f.startsWith(`${id}-`)).map(f => join(ROOT, 'genealogy/people', f))[0]
        : join(ROOT, 'genealogy/research-profiles', `${id}.md`);
      return file && existsSync(file) ? boldDensity(readFileSync(file, 'utf8')) : null;
    })).filter(Boolean).reduce((a, b) => ({ words: a.words + b.words, spans: a.spans + b.spans }), { words: 0, spans: 0 });
    const perSpan = density.spans ? Math.round(density.words / density.spans) : 0;
    console.log(`fetstil: ${perSpan} ord per spann${perSpan && perSpan < 60 ? ' — under 60, se T-0633:s standard B1–B4' : ''}. Varning, inte formatfel.`);
    if (count) process.exitCode = 1;
  }
}
