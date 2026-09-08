import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { checkPersonFormat } from './person-format.mjs';
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
