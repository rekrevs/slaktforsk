import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {bootstrapFromFiles} from '../lib/rebuild.mjs';

test('bootstrap preserves existing database and interrupted restore before reading inputs',t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-bootstrap-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  for(const suffix of ['', '.restoring']){
    const destination=path.join(root,suffix?'interrupted.sqlite':'existing.sqlite');
    fs.writeFileSync(destination+suffix,'valuable existing bytes');
    assert.throws(()=>bootstrapFromFiles(root,destination),/nytt mål/);
    assert.equal(fs.readFileSync(destination+suffix,'utf8'),'valuable existing bytes');
    if(suffix)assert.equal(fs.existsSync(destination),false);
  }
});

test('bootstrap rejects substituted historical operation without creating database',t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-bootstrap-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  fs.mkdirSync(path.join(root,'genealogy2/operations'),{recursive:true});
  fs.writeFileSync(path.join(root,'genealogy2/operations/T-0641-pilot-v1.json'),JSON.stringify({id:'T-0641/pilot-v1',changes:[]}));
  const destination=path.join(root,'fresh.sqlite');
  assert.throws(()=>bootstrapFromFiles(root,destination),/bevarade historiken/);
  assert.equal(fs.existsSync(destination),false);
  assert.equal(fs.existsSync(destination+'.restoring'),false);
});
