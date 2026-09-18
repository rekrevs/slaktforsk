import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { checkPersonFormat, boldDensity } from './person-format.mjs';
const template = readFileSync(new URL('../genealogy/templates/person.md', import.meta.url), 'utf8');
const minimal = template.replaceAll('P-NNNN', 'P-0004');
const check = text => checkPersonFormat({ text, personId: 'P-0004' });
test('minimal dossier with empty tables passes', () => assert.deepEqual(check(minimal), []));
test('missing, duplicate and reordered mandatory headings fail', () => {
  for (const text of [minimal.replace('## Identitet\n', ''), minimal.replace('## Identitet', '## Identitet\n\n## Identitet'), minimal.replace('## Identitet', '## TEMP').replace('## Namnformer', '## Identitet').replace('## TEMP', '## Namnformer')]) assert.ok(check(text).some(e => e.includes('H2')));
});
test('optional sections permitted only once between questions and history', () => {
  const valid = minimal.replace('## Historik och rättelser', '## Integritetsnot\n\nPrivat.\n\n## Slutstatus\n\nAvgränsad.\n\n## Historik och rättelser');
  assert.deepEqual(check(valid), []);
  assert.ok(check(minimal.replace('## Identitet', '## Slutstatus\n\n## Identitet')).some(e => e.includes('Slutstatus:')));
  assert.ok(check(valid.replace('## Slutstatus', '## Integritetsnot')).some(e => e.includes('Integritetsnot:')));
});
test('wrong header, width and missing delimiter rejected', () => {
  assert.ok(check(minimal.replace('| Form |', '| Namn |')).some(e => e.includes('fel tabellhuvud')));
  assert.ok(check(minimal.replace('| Form |', '| Form | Extra |')).some(e => e.includes('kolumner')));
  assert.ok(check(minimal.replace('|---|---|---|---|---|', '|---|no|---|---|---|')).some(e => e.includes('tabellavskiljare')));
});
test('historical and H3 tables do not become current tables', () => {
  const text = minimal.replace('## Påståenden', '### Äldre namntabell\n\n| Äldre |\n|---|\n| X |\n\n## Påståenden') + '\n### Äldre struktur\n\n| Vad | När |\n|---|---|\n| Test | Då |\n';
  assert.deepEqual(check(text), []);
});
test('fenced examples and escaped pipe do not add headings or columns', () => {
  const text = minimal.replace('|---|---|---|---|---|', '|---|---|---|---|---|\n| Namn \\| variant | okänd | LEAD | C-0001 | kommentar |') + '\n```md\n## Identitet\n```\n';
  assert.deepEqual(check(text), []);
});
test('profile headings and duplicate fields are independently checked', () => {
  const profile = readFileSync(new URL('../genealogy/templates/research-profile.md', import.meta.url), 'utf8').replaceAll('P-NNNN', 'P-0004');
  const checkProfile = text => checkPersonFormat({ text, personId: 'P-0004', kind: 'profile' });
  assert.deepEqual(checkProfile(profile), []);
  assert.ok(checkProfile(profile + '\n- Trädverkan: `BÄRANDE`\n').some(e => e.startsWith('Trädverkan:')));
  assert.ok(checkProfile(profile.replace('## Söknycklar', '## Annat')).some(e => e.includes('otillåten H2')));
});
test('blank-line table continuation is reported instead of losing later claims', () => {
  const rows = '| A-0001 | Ett påstående | LEAD | låg | C-0001 | kommentar |';
  const split = minimal.replace('## Relationer', `${rows}\n\n${rows}\n\n## Relationer`);
  assert.ok(check(split).some(e => e.startsWith('Påståenden: kräver exakt en huvudtabell')));
});
test('rubrikstandarden fångar nivåhopp, fetstil och underrubrik i Identitet', () => {
  assert.ok(check(minimal.replace('## Namnformer', '#### Hoppad nivå\n\n## Namnformer')).some(e => e.includes('rubriknivå hoppas över')));
  assert.ok(check(minimal.replace('## Identitet', '## **Identitet**')).some(e => e.includes('fetstil')));
  assert.ok(check(minimal.replace('## Namnformer', '### Egen underrubrik\n\n## Namnformer')).some(e => e.includes('Identitet är sammanhållen prosa')));
  assert.deepEqual(check(minimal.replace('## Historik och rättelser', '## Historik och rättelser\n\n### Rättelse, 2026-09-10')), []);
});
test('bevarade citatblock undantas från rubrikstandarden', () => {
  assert.deepEqual(check(minimal.replace('## Historik och rättelser', '## Historik och rättelser\n\n> #### Bevarad äldre rubrik\n')), []);
});
test('fetstilstätheten räknas utan citatblock', () => {
  assert.deepEqual(boldDensity('> **ett** **två**\nvanlig text här'), { words: 3, spans: 0 });
  assert.equal(boldDensity('**ett** två tre fyra').spans, 1);
});
