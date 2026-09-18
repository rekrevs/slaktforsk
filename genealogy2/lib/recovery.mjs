import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {sha,canonical,hashFile,readBaseline} from './archive.mjs';
import {openDB,backupDB,verifyDB} from './store.mjs';
import {applyOperation} from './domain.mjs';

function safePath(root,relative) {
  if(typeof relative!=='string'||relative.startsWith('/')||relative.split('/').some(p=>['','.','..'].includes(p)))throw Error(`Ogiltig relativ sökväg: ${relative}`);
  let current=path.resolve(root);
  if(fs.existsSync(current)&&fs.lstatSync(current).isSymbolicLink())throw Error('Rot får inte vara symlink');
  for(const part of relative.split('/')) {
    current=path.join(current,part);
    if(fs.existsSync(current)&&fs.lstatSync(current).isSymbolicLink())throw Error(`Symlink i lagringen: ${relative}`);
  }
  return current;
}
function syncFile(file) {const fd=fs.openSync(file,'r');try{fs.fsyncSync(fd);}finally{fs.closeSync(fd);}}
function durableFile(file,bytes) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  // An interrupted temporary write may remain; a unique temporary filename is
  // never mistaken for a committed journal entry.
  const temp=file+`.writing-${process.pid}-${crypto.randomUUID()}`;
  try {
    fs.writeFileSync(temp,bytes,{flag:'wx'});syncFile(temp);
    try{fs.linkSync(temp,file);}catch(e){if(e.code!=='EEXIST'||!fs.readFileSync(file).equals(Buffer.from(bytes)))throw e;}
    syncFile(path.dirname(file));
  }finally{fs.rmSync(temp,{force:true});}
}
async function checkFile(file,meta) {
  if(!fs.existsSync(file)||fs.statSync(file).size!==meta.bytes||await hashFile(file)!==meta.sha256)throw Error(`Media/fil saknas eller har ändrats: ${file}`);
}

export async function stageMedia(root,file,provenance) {
  if(!provenance?.trim())throw Error('Ange mediets provenans');
  const bytes=fs.readFileSync(file);
  if(bytes.subarray(0,128).toString().startsWith('version https://git-lfs.github.com/spec/v1'))throw Error('LFS-innehåll saknas');
  const digest=sha(bytes),storagePath=`genealogy2/media/objects/${digest}`;
  durableFile(safePath(root,storagePath),bytes);
  return {id:`M-${digest}`,storagePath,sha256:digest,bytes:bytes.length,originalName:path.basename(file),provenance};
}

export function syncJournal(db,directory) {
  let written=0;
  for(const row of db.prepare(`SELECT p.*,o.request_hash,o.recorded_at FROM operation_payload p JOIN operation o ON o.id=p.operation_id ORDER BY p.sequence`).all()) {
    const request=JSON.parse(row.request_json);
    if(sha(canonical(request))!==row.request_hash)throw Error(`Skadat operationsinnehåll: ${row.operation_id}`);
    const envelope={format:'genealogy2-journal/1',sequence:row.sequence,policy:row.policy,recordedAt:row.recorded_at,requestHash:row.request_hash,request};
    const file=safePath(directory,`${String(row.sequence).padStart(9,'0')}-${row.request_hash}.json`);
    const exists=fs.existsSync(file);durableFile(file,canonical(envelope)+'\n');if(!exists)written++;
  }
  return {written};
}

async function checkOperationMedia(db,request,root) {
  for(const a of request.media??[])await checkFile(safePath(root,a.storagePath),a);
  for(const c of request.changes??[]) {
    for(const a of c.assets??[]) {
      const meta=db.prepare('SELECT * FROM asset WHERE path=?').get(a.path);
      if(!meta)throw Error(`Okänt äldre medium: ${a.path}`);
      await checkFile(safePath(root,meta.path),meta);
    }
    for(const a of c.media??[]) {
      const meta=(request.media??[]).find(m=>m.id===a.id)??db.prepare('SELECT *,storage_path AS storagePath FROM native_asset WHERE id=?').get(a.id);
      if(!meta)throw Error(`Okänt medium: ${a.id}`);
      await checkFile(safePath(root,meta.storagePath),meta);
    }
  }
}

// Success is reported only after both SQLite commit and a durable journal copy.
// If the process dies between them, SQLite is authoritative; repeating apply or
// running journal regenerates the missing receipt, without executing twice.
export async function writeOperation(db,request,{root,journal,legacy=false,afterCommit}={}) {
  await checkOperationMedia(db,request,root);
  fs.mkdirSync(journal,{recursive:true});
  const result=applyOperation(db,request,{legacy});
  try {afterCommit?.();return {...result,journal:syncJournal(db,journal)};}
  catch(e){throw Error(`Operationen finns i databasen men journalen kunde inte säkras. Upprepa samma operation eller kör journal. ${e.message}`);}
}

export async function replayJournal(db,directory,{root}={}) {
  const files=fs.readdirSync(directory).filter(f=>/^\d{9}-[a-f0-9]{64}\.json$/.test(f)).sort();
  let applied=0;
  for(const f of files) {
    const row=JSON.parse(fs.readFileSync(safePath(directory,f),'utf8'));
    if(row.format!=='genealogy2-journal/1'||!['legacy/1','native/2'].includes(row.policy)||sha(canonical(row.request))!==row.requestHash||f!==`${String(row.sequence).padStart(9,'0')}-${row.requestHash}.json`)throw Error('Skadad journalpost');
    const existing=db.prepare('SELECT sequence FROM operation_payload WHERE operation_id=?').get(row.request.id);
    const next=db.prepare('SELECT coalesce(max(sequence),0)+1 n FROM operation_payload').get().n;
    if(existing?existing.sequence!==row.sequence:next!==row.sequence)throw Error('Journalen har en lucka eller hör till en annan databasgren');
    await checkOperationMedia(db,row.request,root);
    if(!applyOperation(db,row.request,{legacy:row.policy==='legacy/1',recordedAt:row.recordedAt}).unchanged)applied++;
  }
  return {applied,entries:files.length};
}

export async function verifyAssets(db,root) {
  const errors=[];
  for(const a of [...db.prepare('SELECT path,sha256,bytes FROM asset').all(),...db.prepare('SELECT storage_path AS path,sha256,bytes FROM native_asset').all()]) {
    try{await checkFile(safePath(root,a.path),a);}catch(e){errors.push(e.message);}
  }
  return {ok:!errors.length,errors};
}

export async function backupBundle(db,destination,{root,baseline}={}) {
  const staging=destination+'.building';
  if(fs.existsSync(destination)||fs.existsSync(staging))throw Error('Backup kräver ett nytt mål utan avbruten byggkatalog');
  fs.mkdirSync(staging,{recursive:true});
  let copy;
  try {
    await backupDB(db,path.join(staging,'research.sqlite'));
    copy=openDB(path.join(staging,'research.sqlite'),{readOnly:true});
    const verified=verifyDB(copy);if(!verified.ok)throw Error(JSON.stringify(verified.errors));
    const files=[];
    const add=async(from,relative,expected)=> {
      const target=safePath(staging,relative);fs.mkdirSync(path.dirname(target),{recursive:true});
      fs.copyFileSync(from,target,fs.constants.COPYFILE_EXCL);syncFile(target);
      const meta={path:relative,sha256:await hashFile(target),bytes:fs.statSync(target).size};
      if(expected&&(meta.sha256!==expected.sha256||meta.bytes!==expected.bytes))throw Error(`Backupfilen skiljer sig: ${relative}`);
      files.push(meta);
    };
    for(const a of [...copy.prepare('SELECT path,sha256,bytes FROM asset').all(),...copy.prepare('SELECT storage_path AS path,sha256,bytes FROM native_asset').all()]) {
      if(files.some(f=>f.path===`files/${a.path}`))continue;
      await add(safePath(root,a.path),`files/${a.path}`,a);
    }
    const batches=copy.prepare('SELECT id FROM import_batch').all();
    if(batches.length) {
      const base=readBaseline(baseline);
      if(batches.length!==1||batches[0].id!==base.id)throw Error('Backupbasen och databasen skiljer sig');
      await add(path.join(baseline,'manifest.json'),'baseline/manifest.json');
      for(const hash of new Set(base.files.filter(f=>f.storage==='object').map(f=>f.sha256))) {
        const f=base.files.find(f=>f.sha256===hash);
        await add(path.join(baseline,'objects',hash),`baseline/objects/${hash}`,f);
      }
    }
    copy.close();copy=null;
    syncFile(path.join(staging,'research.sqlite'));
    files.push({path:'research.sqlite',sha256:await hashFile(path.join(staging,'research.sqlite')),bytes:fs.statSync(path.join(staging,'research.sqlite')).size});
    const manifest={format:'genealogy2-backup/1',files:files.sort((a,b)=>a.path.localeCompare(b.path))};
    durableFile(path.join(staging,'manifest.json'),canonical(manifest)+'\n');
    fs.renameSync(staging,destination);syncFile(path.dirname(destination));
    return {directory:destination,files:files.length,bytes:files.reduce((n,f)=>n+f.bytes,0)};
  }catch(e){copy?.close();fs.rmSync(staging,{recursive:true,force:true});throw e;}
}

export async function restoreBundle(directory,destination) {
  const staging=destination+'.building';
  if(fs.existsSync(destination)||fs.existsSync(staging))throw Error('Återställning kräver en ny katalog');
  const m=JSON.parse(fs.readFileSync(path.join(directory,'manifest.json'),'utf8'));
  if(m.format!=='genealogy2-backup/1'||!Array.isArray(m.files)||new Set(m.files.map(f=>f.path)).size!==m.files.length)throw Error('Ogiltigt backupmanifest');
  fs.mkdirSync(staging,{recursive:true});
  let db;
  try {
    for(const f of m.files) {
      const from=safePath(directory,f.path);await checkFile(from,f);
      const relative=f.path==='research.sqlite'?'genealogy2/data/research.sqlite':f.path.startsWith('files/')?f.path.slice(6):f.path.startsWith('baseline/')?'genealogy2/import/'+f.path:null;
      if(!relative)throw Error('Okänd filtyp i backup');
      const target=safePath(staging,relative);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(from,target,fs.constants.COPYFILE_EXCL);
      await checkFile(target,f);
    }
    db=openDB(path.join(staging,'genealogy2/data/research.sqlite'),{migrate:true});
    const v=verifyDB(db),a=await verifyAssets(db,staging);if(!v.ok||!a.ok)throw Error(JSON.stringify([...v.errors,...a.errors]));
    if(db.prepare('SELECT count(*) n FROM import_batch').get().n) {
      const base=readBaseline(path.join(staging,'genealogy2/import/baseline'));
      if(!db.prepare('SELECT id FROM import_batch WHERE id=?').get(base.id))throw Error('Fel importbas i backup');
    }
    // Reconstruct frozen textual research files, never current governance files.
    for(const d of db.prepare('SELECT path,text FROM document WHERE frozen=1').all()) {
      const target=safePath(staging,d.path);fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,d.text,{flag:'wx'});
    }
    syncJournal(db,path.join(staging,'genealogy2/journal'));
    db.close();db=null;fs.renameSync(staging,destination);
    return {directory:destination,ok:true};
  }catch(e){db?.close();fs.rmSync(staging,{recursive:true,force:true});throw e;}
}
