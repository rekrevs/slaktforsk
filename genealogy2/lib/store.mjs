import fs from 'node:fs';
import path from 'node:path';
import {DatabaseSync,backup} from 'node:sqlite';
import {sha,canonical,readBaseline} from './archive.mjs';
import {extract,EXTRACTOR} from './extract.mjs';
import {DOMAIN_TABLES,verifyDomain,indexObject,readCurrent} from './domain.mjs';

const schema=fs.readFileSync(new URL('../schema/001.sql',import.meta.url),'utf8');
const domainSchema=fs.readFileSync(new URL('../schema/002.sql',import.meta.url),'utf8');
const mappingSchema=fs.readFileSync(new URL('../schema/003.sql',import.meta.url),'utf8');
const runtimeSchema=fs.readFileSync(new URL('../schema/004.sql',import.meta.url),'utf8');
const conversionSchema=fs.readFileSync(new URL('../schema/005.sql',import.meta.url),'utf8');
const targetsSchema=fs.readFileSync(new URL('../schema/006.sql',import.meta.url),'utf8');
const schemaHash2=sha(schema+'\n'+domainSchema);
const schemaHash3=sha(schema+'\n'+domainSchema+'\n'+mappingSchema);
const schemaHash4=sha(schema+'\n'+domainSchema+'\n'+mappingSchema+'\n'+runtimeSchema);
const schemaHash5=sha(schema+'\n'+domainSchema+'\n'+mappingSchema+'\n'+runtimeSchema+'\n'+conversionSchema);
const schemaHash=sha(schema+'\n'+domainSchema+'\n'+mappingSchema+'\n'+runtimeSchema+'\n'+conversionSchema+'\n'+targetsSchema);
export const SCHEMA_VERSION=6;
const runtimeTables=['native_asset','record_media','operation_payload'];
const legacyTables=['meta','import_batch','document','asset','legacy_entity','unit','legacy_assertion'];
const immutable=legacyTables.filter(t=>t!=='meta');
const allTables=()=>[...legacyTables,...DOMAIN_TABLES,'legacy_mapping',...runtimeTables,'unit_decision','unit_decision_target'];
const applicationId=0x47454e32;

export function openDB(file,{create=false,readOnly=false,migrate=false}={}) {
  if(!fs.existsSync(file)&&!create) throw Error(`Databas saknas: ${file}`);
  if(create) fs.mkdirSync(path.dirname(file),{recursive:true});
  const db=new DatabaseSync(file,{readOnly});
  try {
    db.exec('PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;');
    const version=db.prepare('PRAGMA user_version').get().user_version;
    if(version!==0&&db.prepare('PRAGMA application_id').get().application_id!==applicationId)throw Error('Okänd schemaversion eller annan databas');
    if(version===0&&create) {
      if(db.prepare("SELECT count(*) AS n FROM sqlite_master").get().n) throw Error('Okänt befintligt schema');
      db.exec('BEGIN IMMEDIATE');
      db.exec(schema);
      for(const t of immutable)for(const op of ['UPDATE','DELETE'])db.exec(`CREATE TRIGGER protect_${t}_${op} BEFORE ${op} ON ${t} BEGIN SELECT RAISE(ABORT,'Bevarat underlag är oföränderligt'); END`);
      db.prepare('INSERT INTO meta VALUES (?,?)').run('schema_hash',sha(schema));
      db.exec(`PRAGMA application_id=${applicationId}; PRAGMA user_version=1; COMMIT`);
    }
    if((version===0&&create || migrate) && db.prepare('PRAGMA user_version').get().user_version===1) {
      if(db.prepare("SELECT value FROM meta WHERE key='schema_hash'").get()?.value!==sha(schema))throw Error('Ändrat basschema');
      transaction(db,()=> {
        db.exec(domainSchema);
        for(const t of DOMAIN_TABLES)for(const op of ['UPDATE','DELETE'])db.exec(`CREATE TRIGGER protect_${t}_${op} BEFORE ${op} ON ${t} BEGIN SELECT RAISE(ABORT,'Revisionshistorik är oföränderlig'); END`);
        db.prepare("UPDATE meta SET value=? WHERE key='schema_hash'").run(schemaHash2);
        db.exec('PRAGMA user_version=2');
      });
    }
    if((version===0&&create || migrate) && db.prepare('PRAGMA user_version').get().user_version===2) {
      if(db.prepare("SELECT value FROM meta WHERE key='schema_hash'").get()?.value!==schemaHash2)throw Error('Ändrat domänschema');
      transaction(db,()=> {
        db.exec(mappingSchema);
        for(const op of ['UPDATE','DELETE'])db.exec(`CREATE TRIGGER protect_legacy_mapping_${op} BEFORE ${op} ON legacy_mapping BEGIN SELECT RAISE(ABORT,'Importbeslut är oföränderliga'); END`);
        db.prepare("UPDATE meta SET value=? WHERE key='schema_hash'").run(schemaHash3);
        db.exec('PRAGMA user_version=3');
      });
    }
    if((version===0&&create || migrate) && db.prepare('PRAGMA user_version').get().user_version===3) {
      if(db.prepare("SELECT value FROM meta WHERE key='schema_hash'").get()?.value!==schemaHash3)throw Error('Ändrat mappningsschema');
      transaction(db,()=> {
        db.exec(runtimeSchema);
        for(const t of runtimeTables)for(const op of ['UPDATE','DELETE'])db.exec(`CREATE TRIGGER protect_${t}_${op} BEFORE ${op} ON ${t} BEGIN SELECT RAISE(ABORT,'Revisionshistorik är oföränderlig'); END`);
        for(const r of db.prepare('SELECT object_id FROM current_revision').all())indexObject(db,r.object_id);
        db.prepare("UPDATE meta SET value=? WHERE key='schema_hash'").run(schemaHash4);
        db.exec('PRAGMA user_version=4');
      });
    }
    if((version===0&&create || migrate) && db.prepare('PRAGMA user_version').get().user_version===4) {
      if(db.prepare("SELECT value FROM meta WHERE key='schema_hash'").get()?.value!==schemaHash4)throw Error('Ändrat runtimeschema');
      transaction(db,()=> {
        db.exec(conversionSchema);
        for(const op of ['UPDATE','DELETE'])db.exec(`CREATE TRIGGER protect_unit_decision_${op} BEFORE ${op} ON unit_decision BEGIN SELECT RAISE(ABORT,'Konverteringsbeslut är oföränderliga'); END`);
        db.prepare("UPDATE meta SET value=? WHERE key='schema_hash'").run(schemaHash5);
        db.exec('PRAGMA user_version=5');
      });
    }
    if((version===0&&create || migrate) && db.prepare('PRAGMA user_version').get().user_version===5) {
      if(db.prepare("SELECT value FROM meta WHERE key='schema_hash'").get()?.value!==schemaHash5)throw Error('Ändrat konverteringsschema');
      transaction(db,()=> {
        db.exec(targetsSchema);
        for(const op of ['UPDATE','DELETE'])db.exec(`CREATE TRIGGER protect_unit_decision_target_${op} BEFORE ${op} ON unit_decision_target BEGIN SELECT RAISE(ABORT,'Konverteringsmål är oföränderliga'); END`);
        db.prepare("UPDATE meta SET value=? WHERE key='schema_hash'").run(schemaHash);
        db.exec('PRAGMA user_version=6');
      });
    }
    if(db.prepare('PRAGMA user_version').get().user_version!==SCHEMA_VERSION || db.prepare('PRAGMA application_id').get().application_id!==applicationId || db.prepare("SELECT value FROM meta WHERE key='schema_hash'").get()?.value!==schemaHash)throw Error('Okänd schemaversion eller ändrat schema; explicit migrering krävs');
    return db;
  }catch(e){db.close();throw e;}
}

export function transaction(db,fn) {
  db.exec('BEGIN IMMEDIATE');
  try { const result=fn(); db.exec('COMMIT'); return result; }
  catch(e){db.exec('ROLLBACK');throw e;}
}
function inserter(db,table) {
  const columns=db.prepare(`PRAGMA table_info(${table})`).all().map(c=>c.name);
  const stmt=db.prepare(`INSERT INTO ${table} (${columns.join(',')}) VALUES (${columns.map(()=>'?').join(',')})`);
  return row=>stmt.run(...columns.map(c=>row[c]??null));
}

export function importBaseline(db,directory,{failAfter=Infinity}={}) {
  const m=readBaseline(directory);
  const existing=db.prepare('SELECT id,extractor FROM import_batch').all();
  if(existing.length) {
    if(existing.length!==1||existing[0].id!==m.id||existing[0].extractor!==EXTRACTOR)throw Error('Ändrad importbas/extraktor kräver uttrycklig skillnadsimport');
    return {unchanged:true,...coverage(db)};
  }
  return transaction(db,()=> {
    db.prepare('INSERT INTO import_batch VALUES (?,?,?)').run(m.id,canonical(m),EXTRACTOR);
    const addDoc=inserter(db,'document'),addAsset=inserter(db,'asset'),addEntity=inserter(db,'legacy_entity'),addUnit=inserter(db,'unit'),addAssertion=inserter(db,'legacy_assertion');
    const search=db.prepare('INSERT INTO document_search(path,text) VALUES (?,?)');
    let n=0;
    for(const f of m.files) {
      if(++n>failAfter) throw Error('Simulerat importavbrott');
      const shared={path:f.path,batch_id:m.id,sha256:f.sha256,bytes:f.bytes,frozen:Number(f.frozen)};
      if(f.encoding!=='utf-8') {addAsset(shared);continue;}
      const text=fs.readFileSync(path.join(directory,'objects',f.sha256),'utf8');
      // Recheck immediately before insertion: do not trust a file changed after validation.
      if(sha(text)!==f.sha256||Buffer.byteLength(text)!==f.bytes)throw Error(`Ändrat importobjekt: ${f.path}`);
      addDoc({...shared,text});search.run(f.path,text);
      if(!f.path.endsWith('.md'))continue;
      const {entity,units}=extract(f,text);
      if(entity)addEntity({...entity,document_path:f.path});
      for(const u of units) {
        addUnit(u);
        if(u.kind==='assertion'&&!u.historical && entity?.kind==='person') {
          const {cells}=JSON.parse(u.parsed_json);
          addAssertion({id:u.legacy_id,unit_id:u.id,owner_id:u.owner_id,status_raw:cells[2]??null,reliability_raw:cells[3]??null});
        }
      }
    }
    return {unchanged:false,...coverage(db)};
  });
}

export function coverage(db) {
  return {
    documents:db.prepare('SELECT count(*) n FROM document').get().n,
    assets:db.prepare('SELECT count(*) n FROM asset').get().n,
    entities:db.prepare('SELECT kind,count(*) n FROM legacy_entity GROUP BY kind ORDER BY kind').all(),
    units:db.prepare('SELECT kind,count(*) n FROM unit GROUP BY kind ORDER BY kind').all(),
    assertions:db.prepare('SELECT count(*) n FROM legacy_assertion').get().n,
    interpretation:'Bevarat och mekaniskt utvunnet. Ingen ny genealogisk bedömning.'
  };
}

export function verifyDB(db) {
  const errors=[];
  const integrity=db.prepare('PRAGMA integrity_check').all();
  if(integrity.length!==1||integrity[0].integrity_check!=='ok')errors.push(...integrity);
  errors.push(...db.prepare('PRAGMA foreign_key_check').all());
  errors.push(...verifyDomain(db));
  for(const d of db.prepare('SELECT * FROM document').iterate()) {
    if(sha(d.text)!==d.sha256||Buffer.byteLength(d.text)!==d.bytes)errors.push(`Dokumenthash: ${d.path}`);
    const bytes=Buffer.from(d.text);
    for(const u of db.prepare('SELECT * FROM unit WHERE document_path=?').all(d.path)) {
      if(bytes.subarray(u.start_byte,u.end_byte).toString()!==u.raw)errors.push(`Textspann: ${u.id}`);
    }
  }
  for(const b of db.prepare('SELECT * FROM import_batch').all()) {
    const {id,...m}=JSON.parse(b.manifest_json);
    if(sha(canonical(m))!==b.id||id!==b.id)errors.push('Importhash');
    const actual=[...db.prepare('SELECT path,sha256,bytes FROM document').all(),...db.prepare('SELECT path,sha256,bytes FROM asset').all()];
    if(actual.length!==m.files.length)errors.push('Filantal');
    const byPath=new Map(actual.map(f=>[f.path,f]));
    for(const f of m.files){const a=byPath.get(f.path);if(!a||a.sha256!==f.sha256||a.bytes!==f.bytes)errors.push(`Filmanifest: ${f.path}`);}
  }
  return {ok:!errors.length,errors};
}

export function search(db,query) {
  // Treat user text as literal words, not executable FTS operators.
  const q=query.split(/\s+/).filter(Boolean).map(w=>'"'+w.replaceAll('"','""')+'"').join(' AND ');
  if(!q)return [];
  const domain=db.prepare("SELECT object_id,kind,snippet(object_search,2,'[',']',' … ',35) AS excerpt FROM object_search WHERE object_search MATCH ? ORDER BY rank LIMIT 30").all(q)
    .map(r=>({...r,layer:'current',object:readCurrent(db,r.object_id)}));
  const legacy=db.prepare("SELECT path,snippet(document_search,1,'[',']',' … ',35) AS excerpt FROM document_search WHERE document_search MATCH ? ORDER BY rank LIMIT 30").all(q).map(r=>({...r,layer:'legacy'}));
  return [...domain,...legacy];
}
export function showLegacy(db,id) {
  return db.prepare('SELECT kind,title,document_path,text FROM legacy_entity JOIN document ON path=document_path WHERE id=? ORDER BY kind').all(id);
}

export function exportData(db) {
  return {format:'genealogy2-export/5',schemaHash,tables:Object.fromEntries(allTables().map(t=>[t,db.prepare(`SELECT * FROM ${t} ORDER BY ${db.prepare(`PRAGMA table_info(${t})`).all().filter(c=>c.pk).sort((a,b)=>a.pk-b.pk).map(c=>c.name).join(',')}`).all()]))};
}
export function restore(data,file) {
  const staging=file+'.restoring';
  if(fs.existsSync(file)||fs.existsSync(staging))throw Error('Återställning kräver en ny databasfil utan avbruten återställning');
  const versions=[['genealogy2-export/1',sha(schema),legacyTables],
    ['genealogy2-export/2',schemaHash2,[...legacyTables,...DOMAIN_TABLES]],
    ['genealogy2-export/2',schemaHash3,[...legacyTables,...DOMAIN_TABLES,'legacy_mapping']],
    ['genealogy2-export/3',schemaHash4,[...legacyTables,...DOMAIN_TABLES,'legacy_mapping',...runtimeTables]],
    ['genealogy2-export/4',schemaHash5,allTables().filter(t=>t!=='unit_decision_target')],
    ['genealogy2-export/5',schemaHash,allTables()]];
  const match=versions.find(([format,hash])=>data.format===format&&data.schemaHash===hash);
  if(!match||canonical(Object.keys(data.tables).sort())!==canonical([...match[2]].sort()))throw Error('Okänd exportversion');
  const tables=match[2];
  const db=openDB(staging,{create:true});
  let closed=false;
  try {
    transaction(db,()=> {
      const expectedMeta=[{key:'schema_hash',value:data.schemaHash}];
      if(canonical(data.tables.meta)!==canonical(expectedMeta))throw Error('Felaktig schemametadata');
      db.exec('PRAGMA defer_foreign_keys=ON');
      for(const t of tables.filter(t=>t!=='meta')) {
        const insert=inserter(db,t);for(const row of data.tables[t])insert(row);
      }
      db.exec('INSERT INTO document_search(path,text) SELECT path,text FROM document');
      for(const r of db.prepare('SELECT object_id FROM current_revision').all())indexObject(db,r.object_id);
      const v=verifyDB(db);if(!v.ok)throw Error(`Exportintegritet: ${JSON.stringify(v.errors)}`);
    });
    const result=coverage(db);db.close();closed=true;
    fs.linkSync(staging,file);fs.rmSync(staging);return result;
  }catch(e){if(!closed){db.close();closed=true;}fs.rmSync(staging,{force:true});throw e;}
  finally{if(!closed)db.close();}
}
export async function backupDB(db,destination) {
  if(fs.existsSync(destination))throw Error('Backupmålet finns redan');
  await backup(db,destination);
  return {file:destination};
}
