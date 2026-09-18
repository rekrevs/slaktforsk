import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {DatabaseSync} from 'node:sqlite';
import {sha} from '../lib/archive.mjs';
import {extract} from '../lib/extract.mjs';
import {contextList,contextDocument,renderContextDocument} from '../lib/context.mjs';

const cohorts=JSON.parse(fs.readFileSync(new URL('../migration/cohorts.json',import.meta.url),'utf8'));

function fixture(t) {
  const db=new DatabaseSync(':memory:');
  db.exec(fs.readFileSync(new URL('../schema/001.sql',import.meta.url),'utf8'));
  db.prepare('INSERT INTO import_batch VALUES (?,?,?)').run(cohorts.baseline,'{}','test');
  t.after(()=>db.close());
  const add=(path,text)=>{
    const file={path,sha256:sha(text),bytes:Buffer.byteLength(text)};
    db.prepare('INSERT INTO document VALUES (?,?,?,?,?,?)').run(path,cohorts.baseline,file.sha256,file.bytes,text,1);
    const result=extract(file,text);
    if(result.entity)db.prepare('INSERT INTO legacy_entity VALUES (?,?,?,?)').run(result.entity.id,result.entity.kind,path,result.entity.title);
    for(const u of result.units)db.prepare('INSERT INTO unit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)').run(u.id,u.document_path,u.kind,u.legacy_id,u.owner_id,u.section,u.start_byte,u.end_byte,u.start_line,u.end_line,u.raw,u.parsed_json,u.historical?1:0);
  };
  return {db,add};
}

test('arkivtext behåller UTF-8-byte, radslut, hash, enhetsspann och avslut utan ny rad',t=>{
  const {db,add}=fixture(t);
  const path='genealogy/research-log/2026-09-10.md';
  const text='# Äldre logg\r\n\r\n## Återupptagning\r\n\r\nÅäö — a\u030a. P-0001. 50%\r\n\r\n```text\r\nbevara\r\n```\r\nslut';
  add(path,text);
  const before=db.prepare('SELECT * FROM document').all();
  const doc=contextDocument(db,path);
  assert.equal(doc.text,text);
  assert.equal(doc.sha256,sha(Buffer.from(text)));
  assert.equal(doc.bytes,Buffer.byteLength(text));
  assert.equal(doc.import_group,'research-context');
  assert.equal(doc.cohort_baseline_matches,true);
  assert.deepEqual(doc.integrity,{bytes_verified:true,sha256_verified:true});
  const original=Buffer.from(text);
  for(const u of doc.units){const row=db.prepare('SELECT raw FROM unit WHERE id=?').get(u.id);assert.equal(original.subarray(u.start_byte,u.end_byte).toString(),row.raw);}
  const rendered=renderContextDocument(doc);
  assert(rendered.endsWith(text));
  assert.match(rendered,/historiska/);
  assert.match(rendered,/ingen full semantisk granskning/);
  assert.deepEqual(db.prepare('SELECT * FROM document').all(),before);
  // A corrupt text column must not be shown as verified merely because its hash is present.
  db.prepare('UPDATE document SET text=? WHERE path=?').run(text+'!',path);
  assert.throws(()=>contextDocument(db,path),/byte\/hash avviker/);
});

test('P/S/C/T-länkar kräver exakta textomnämnanden och verkliga importerade mål',t=>{
  const {db,add}=fixture(t);
  for(const n of ['0001','0002','0003'])add(`genealogy/people/P-${n}-test.md`,`# P-${n}: Namn ${n}\n`);
  add('genealogy/research-profiles/P-0001.md','# P-0001: Profil\n');
  add('genealogy/sources/S-0001-test.md','# S-0001: Källvolym\n');
  add('genealogy/citations/C-0001-test.md','# C-0001: Posten\n');
  add('wotan/dev-log/T-0001.md','# T-0001: Historisk uppgift\nStatus: DONE\n');
  const path='genealogy/access-register.md';
  const text='# Åtkomst\r\n\r\nP-0001–P-0003; S-0001 / C-0001; T-0001.\r\n[[P-0001]] igen.\nP-9999, T-9999. XP-0001 P-00011 P-0001x _P-0001 P-0001_ ID-P-0001';
  add(path,text);
  const doc=contextDocument(db,path);
  assert.deepEqual(doc.references.map(r=>r.id),['C-0001','P-0001','P-0003','P-9999','S-0001','T-0001','T-9999']);
  const person=doc.references.find(r=>r.id==='P-0001');
  assert.equal(person.occurrences.length,2);
  assert.deepEqual(person.targets.map(t=>t.kind),['person','profile']);
  assert.equal(person.relation,'text_mention_only');
  assert.equal(doc.references.some(r=>r.id==='P-0002'),false,'intervallet får inte expanderas');
  for(const ref of doc.references)for(const o of ref.occurrences){assert.equal(Buffer.from(text).subarray(o.start_byte,o.end_byte).toString(),ref.id);assert.equal(Buffer.from(text).subarray(0,o.start_byte).toString().split('\n').length,o.line);}
  for(const id of ['P-9999','T-9999']){const ref=doc.references.find(r=>r.id===id);assert.equal(ref.resolved,false);assert.deepEqual(ref.targets,[]);}
  assert.equal(doc.references.find(r=>r.id==='T-0001').targets[0].href,'wotan/dev-log/T-0001.md');
  const rendered=renderContextDocument(doc);
  assert.match(rendered,/\[P-0001: Namn 0001 \(person\)\]\(<genealogy\/people\/P-0001-test.md>\)/);
  assert.match(rendered,/P-9999, T-9999/);
  assert.doesNotMatch(rendered,/\[P-9999/);
  assert.equal(Object.hasOwn(doc,'facts'),false);
  assert.equal(Object.hasOwn(doc,'tasks'),false);
});

test('tomma filter ger inga tomma SQL-villkor och sökningen är bokstavlig',t=>{
  const {db,add}=fixture(t);
  add('genealogy/access-register.md','# Åtkomst\nEn uppgift: 50%.\n');
  add('genealogy/README.md','# Regler\nSvenska: ÅÄÖ.\n');
  add('wotan/dev-log/T-0001.md','# Arkiverat utförande\n');
  add('genealogy/people/P-0001-sverker.md','# P-0001: Utanför standardlistan\n');
  const all=contextList(db);
  assert.equal(all.length,3);
  assert.deepEqual(contextList(db,{}),all);
  assert.deepEqual(contextList(db,{group:'',query:'  '}),all);
  assert.deepEqual(contextList(db,{group:null,query:null}),all);
  assert.equal(contextList(db,{group:'research-context'}).length,2);
  assert.equal(contextList(db,{group:'archive-context'}).length,1);
  assert.deepEqual(contextList(db,{group:'no-such-group'}),[]);
  assert.deepEqual(contextList(db,{query:"' OR 1=1 --"}),[]);
  assert.deepEqual(contextList(db,{query:'%'}).map(r=>r.path),['genealogy/access-register.md']);
  assert.deepEqual(contextList(db,{query:'åäö'}).map(r=>r.path),['genealogy/README.md']);
  assert.throws(()=>contextList(db,{query:[]}),/måste vara text/);
  assert.equal(contextDocument(db,'../../not-imported.md'),null);
  assert.throws(()=>contextDocument(db,''),/exakta importsökväg krävs/);
});

test('alla 51 forskningskontextdokument har sakligt avgränsade historiska ändamål',t=>{
  const {db,add}=fixture(t);
  const paths=cohorts.groups.find(g=>g.id==='research-context').documents;
  assert.equal(paths.length,51);
  for(const path of paths)add(path,'# Bevarad text\n');
  const listed=contextList(db,{group:'research-context'});
  assert.equal(listed.length,51);
  assert(listed.every(d=>d.classification.kind!=='preserved_material'));
  assert(listed.every(d=>d.classification.authority==='historical_context'&&d.classification.semantic_review==='not_asserted'));
  const item=p=>listed.find(d=>d.path==='genealogy/'+p);
  assert.equal(item('research-log/2026-09-10.md').classification.kind,'historical_log');
  assert.match(item('research-log/handover-archive-2026-09-04.md').classification.purpose,/inte bli en parallell återupptagningskö/);
  assert.equal(item('research-inventory.json').classification.kind,'historical_indicator');
  assert.equal(item('frontier.md').classification.kind,'historical_indicator');
  assert.match(item('access-register.md').classification.purpose,/daterade.*upphävda/);
  assert.equal(item('source-coverage.md').classification.kind,'historical_coverage');
  assert.match(item('source-contexts/README.md').classification.purpose,/belägger inte personförekomst/);
  assert.equal(item('kinship-roles.json').classification.kind,'historical_register');
  assert.match(item('avvecklade-akter.json').classification.purpose,/inte nya sammanslagningar/);
  assert.match(item('editions/assets/README.md').classification.purpose,/inte exakta historiska fastighetskoordinater/);
  assert.equal(item('editions/adam-axel-depth5-v4.json').classification.kind,'edition_material');
  assert.equal(item('templates/person.md').classification.kind,'historical_template');
});
