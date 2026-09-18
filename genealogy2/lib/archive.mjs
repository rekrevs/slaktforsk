import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createReadStream } from 'node:fs';

export const sha = value => crypto.createHash('sha256').update(value).digest('hex');
export const canonical = value => JSON.stringify(value, (_, v) =>
  v && typeof v === 'object' && !Array.isArray(v)
    ? Object.fromEntries(Object.keys(v).sort().map(k => [k,v[k]])) : v);

export function walk(root, relative = '') {
  return fs.readdirSync(path.join(root,relative),{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name,'en')).flatMap(e => {
    if (e.name === '.DS_Store' || e.name === '__pycache__' || /\.py[cod]$/.test(e.name)) return [];
    const p = path.posix.join(relative,e.name);
    if (e.isSymbolicLink()) throw Error(`Symlink måste hanteras uttryckligen: ${p}`);
    return e.isDirectory() ? walk(root,p) : [p];
  });
}

export async function hashFile(file) {
  const h = crypto.createHash('sha256');
  for await (const chunk of createReadStream(file)) h.update(chunk);
  return h.digest('hex');
}

export function sourcePaths(root) {
  const p = walk(path.join(root,'genealogy')).map(x=>'genealogy/'+x);
  for (const f of ['README.md','AGENTS.md','CLAUDE.md','NORTH-STAR.md','PROJECT-CONTROL.md','MEDIA-PRESERVATION.md','wotan/README.md','wotan/backlog.json']) {
    if (fs.existsSync(path.join(root,f))) p.push(f);
  }
  for (const dir of ['wotan/dev-log','scripts']) if (fs.existsSync(path.join(root,dir))) {
    p.push(...walk(path.join(root,dir)).filter(f => dir !== 'wotan/dev-log' || /^T-\d{4}\.md$/.test(f) && Number(f.slice(2,6)) < 640).map(f=>dir+'/'+f));
  }
  return p.sort();
}

export async function snapshot(root, destination) {
  if (fs.existsSync(destination)) throw Error(`Importbasen finns redan: ${destination}`);
  const staging = destination+'.building';
  if (fs.existsSync(staging)) throw Error(`Avbruten snapshot finns; inspektera ${staging}`);
  fs.mkdirSync(path.join(staging,'objects'),{recursive:true});
  try {
    const files = [];
    for (const relative of sourcePaths(root)) {
      const file = path.join(root,relative);
      const size = fs.statSync(file).size;
      let isText = !relative.startsWith('genealogy/media/') && /\.(md|json|jsonl|mjs|js|ts|txt|csv|yaml|yml|sql|sh|py|html|css|xml|ged|svg)$/i.test(relative);
      let encoding=null;
      let digest;
      if (isText) {
        const bytes = fs.readFileSync(file);
        try {new TextDecoder('utf-8',{fatal:true}).decode(bytes);encoding='utf-8';}
        catch {isText=false;} // Exact bytes retained as an opaque object, never lossy replacement characters.
        digest = sha(bytes);
        const target = path.join(staging,'objects',digest);
        if (!fs.existsSync(target)) fs.writeFileSync(target,bytes,{flag:'wx'});
      } else {
        const fd=fs.openSync(file,'r');
        const prefix=Buffer.alloc(128); fs.readSync(fd,prefix,0,128,0); fs.closeSync(fd);
        if (prefix.toString().startsWith('version https://git-lfs.github.com/spec/v1')) throw Error(`LFS-innehåll saknas: ${relative}`);
        digest = await hashFile(file);
      }
      const object=fs.existsSync(path.join(staging,'objects',digest));
      files.push({path:relative,sha256:digest,bytes:size,storage:object?'object':'external',encoding,frozen:relative.startsWith('genealogy/')});
    }
    const body={format:'genealogy2-baseline/1',files};
    const manifest={...body,id:sha(canonical(body))};
    fs.writeFileSync(path.join(staging,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
    fs.renameSync(staging,destination);
    return {id:manifest.id,files:files.length,objects:files.filter(f=>f.storage==='object').length,external:files.filter(f=>f.storage==='external').length};
  } catch(e) { fs.rmSync(staging,{recursive:true,force:true}); throw e; }
}

export function readBaseline(directory) {
  const manifest=JSON.parse(fs.readFileSync(path.join(directory,'manifest.json'),'utf8'));
  const {id,...body}=manifest;
  if (body.format!=='genealogy2-baseline/1' || sha(canonical(body))!==id) throw Error('Felaktigt importmanifest');
  const seen=new Set();
  for(const f of manifest.files) {
    if (typeof f.path!=='string' || f.path.startsWith('/') || f.path.split('/').some(x=>['..','.',''].includes(x)) || seen.has(f.path) || !/^[a-f0-9]{64}$/.test(f.sha256) || !['object','external'].includes(f.storage)) throw Error('Ogiltig fil i importmanifest');
    seen.add(f.path);
    if(f.storage==='object') {
      const bytes=fs.readFileSync(path.join(directory,'objects',f.sha256));
      if(bytes.length!==f.bytes || sha(bytes)!==f.sha256) throw Error(`Skadat importobjekt: ${f.path}`);
    }
  }
  return manifest;
}

export async function verifySource(root,directory,{media=true}={}) {
  const manifest=readBaseline(directory), problems=[];
  const expected=new Set(manifest.files.filter(f=>f.frozen).map(f=>f.path));
  const actual=walk(path.join(root,'genealogy')).map(f=>'genealogy/'+f);
  for(const f of actual) if(!expected.has(f)) problems.push(`Tillkommen: ${f}`);
  for(const f of manifest.files.filter(f=>f.frozen)) {
    const file=path.join(root,f.path);
    if(!fs.existsSync(file)) problems.push(`Saknas: ${f.path}`);
    else if ((f.storage==='object'||media) && (fs.statSync(file).size!==f.bytes || await hashFile(file)!==f.sha256)) problems.push(`Ändrad: ${f.path}`);
  }
  return {ok:!problems.length,mediaVerified:media,problems};
}
