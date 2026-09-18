import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {DatabaseSync} from 'node:sqlite';
import {openDB,restore,search,verifyDB,SCHEMA_VERSION} from '../lib/store.mjs';
import {DOMAIN_TABLES,readCurrent} from '../lib/domain.mjs';
import {sha} from '../lib/archive.mjs';
import {restoreBundle} from '../lib/recovery.mjs';

for(const version of [1,2,3,4,5])test(`schema ${version}: explicit migrering och återställning av äldre export`,async t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-version-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const file=path.join(dir,'old.sqlite'),old=new DatabaseSync(file);
  const schemas=Array.from({length:version},(_,i)=>fs.readFileSync(new URL(`../schema/00${i+1}.sql`,import.meta.url),'utf8'));
  old.exec(schemas.join('\n'));
  const hash=sha(schemas.join('\n'));old.prepare('INSERT INTO meta VALUES (?,?)').run('schema_hash',hash);
  old.exec(`PRAGMA application_id=${0x47454e32}; PRAGMA user_version=${version}`);
  if(version>=2) {
    old.exec(`INSERT INTO operation VALUES ('old','unused','test','2026-09-01T00:00:00.000Z','Äldre post');
      INSERT INTO object VALUES ('S','source');
      INSERT INTO revision VALUES ('S@1','S',1,'old','recorded',NULL,'Äldre motivering','Äldre förbehåll',NULL);
      INSERT INTO source VALUES ('S@1','Gammelkälltest',NULL,NULL,'Bevarad beskrivning')`);
  }
  if(version>=4)old.exec("INSERT INTO object_search(object_id,kind,text) VALUES ('S','source','Gammelkälltest')");
  const tables=['meta','import_batch','document','asset','legacy_entity','unit','legacy_assertion',...(version>=2?DOMAIN_TABLES:[]),...(version>=3?['legacy_mapping']:[]),...(version>=4?['native_asset','record_media','operation_payload']:[]),...(version>=5?['unit_decision']:[])];
  for(const table of tables.filter(x=>x!=='meta'))for(const op of ['UPDATE','DELETE'])old.exec(`CREATE TRIGGER protect_${table}_${op} BEFORE ${op} ON ${table} BEGIN SELECT RAISE(ABORT,'oföränderlig'); END`);
  const data={format:`genealogy2-export/${version===1?1:version===5?4:version===4?3:2}`,schemaHash:hash,tables:Object.fromEntries(tables.map(t=>[t,old.prepare(`SELECT * FROM ${t}`).all()]))};
  old.close();
  if(version>=4) {
    const bundle=path.join(dir,'old-bundle');fs.mkdirSync(bundle);
    const bytes=fs.readFileSync(file);fs.writeFileSync(path.join(bundle,'research.sqlite'),bytes);
    fs.writeFileSync(path.join(bundle,'manifest.json'),JSON.stringify({format:'genealogy2-backup/1',files:[{path:'research.sqlite',sha256:sha(bytes),bytes:bytes.length}]}));
    await restoreBundle(bundle,path.join(dir,'bundle-restored'));
    const restoredBundle=openDB(path.join(dir,'bundle-restored/genealogy2/data/research.sqlite'));
    assert.equal(restoredBundle.prepare('PRAGMA user_version').get().user_version,SCHEMA_VERSION);
    assert.equal(readCurrent(restoredBundle,'S').caveat,'Äldre förbehåll');restoredBundle.close();
  }
  assert.throws(()=>openDB(file),/migrering krävs/);
  const migrated=openDB(file,{migrate:true});t.after(()=>migrated.close());
  assert.equal(migrated.prepare('PRAGMA user_version').get().user_version,SCHEMA_VERSION);
  assert.equal(verifyDB(migrated).ok,true);
  const dest=path.join(dir,'restored.sqlite');restore(data,dest);
  const restored=openDB(dest);t.after(()=>restored.close());
  assert.equal(verifyDB(restored).ok,true);
  if(version>=2)for(const db of [migrated,restored]) {
    assert.equal(readCurrent(db,'S').caveat,'Äldre förbehåll');
    assert.equal(search(db,'Gammelkälltest')[0].object_id,'S');
    assert.throws(()=>db.exec("UPDATE source SET title='tyst ändring'"),/oföränderlig/);
  }
  assert.throws(()=>restore({...data,schemaHash:'unknown'},path.join(dir,'invalid.sqlite')),/Okänd exportversion/);
  assert.equal(fs.existsSync(path.join(dir,'invalid.sqlite')),false);
});
