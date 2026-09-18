import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {openDB,importBaseline,exportData,search,verifyDB,backupDB} from '../lib/store.mjs';
import {applyOperation,head,personView,readCurrent} from '../lib/domain.mjs';
import {stageMedia,writeOperation,syncJournal,replayJournal,backupBundle,restoreBundle,verifyAssets} from '../lib/recovery.mjs';
import {snapshot,verifySource,canonical} from '../lib/archive.mjs';

const basis=(object,version=1)=>({object,version,role:'supports'});
const change=(id,kind,data,extra={})=>({id,kind,data,expectedVersion:null,disposition:'recorded',rationale:'Syntetiskt arbetsflödesprov',...extra});
test('hel arbetscykel med nya media, versionsbundna referenser, avbrott, journal och full återställning',async t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-workflow-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  fs.mkdirSync(path.join(dir,'genealogy/media'),{recursive:true});
  fs.writeFileSync(path.join(dir,'genealogy/README.md'),'# Fryst testunderlag\n');
  fs.writeFileSync(path.join(dir,'genealogy/media/old.bin'),Buffer.from([1,2,3]));
  const base=path.join(dir,'baseline');await snapshot(dir,base);
  const file=path.join(dir,'db.sqlite'),db=openDB(file,{create:true});t.after(()=>db.close());importBaseline(db,base);
  const image=path.join(dir,'new.bin');fs.writeFileSync(image,Buffer.from([4,5,6]));
  const media=await stageMedia(dir,image,'Syntetiskt medieunderlag; inte en arkivkälla');
  const journal=path.join(dir,'genealogy2/journal'),options={root:dir,journal};
  const obs=change('O','observation',{record_id:'R',mention_id:'M',property:'name',value_literal:'felläsningsexempel',value_json:null});
  const initial={id:'workflow-1',actor:'test',reason:'Hel cykel',media:[media],changes:[
    change('S','source',{title:'Syntetisk källa',description:'Test'}),
    change('R','record',{source_id:'S',record_type:'test',locator:'post 1',dependence_note:''},{media:[{id:media.id,region:'rad 1'}]}),
    change('M','mention',{record_id:'R',name_literal:'Åsa',role_literal:'barn'}),obs,
    change('P','person',{display_name:'Åsa'},{disposition:'accepted',evidence:[basis('O')]}),
    change('I','identity',{mention_id:'M',person_id:'P',decision:'accepted'},{disposition:'accepted'}),
    change('F','fact',{subject_id:'P',property:'name',value_type:'text',value_json:'Åsa'},{disposition:'candidate',evidence:[basis('O'),basis('I')],caveat:'Osäkert namn'}),
    change('Q','question',{subject_id:'P',title:'Vilket namn?',outcome:'ÖPPEN',body:'Arbetsfrågetest'},{evidence:[basis('F')]}),
    change('N','narrative',{subject_id:'P',title:'Berättelse',markdown:'Nyberättelsetest med förbehåll'},{evidence:[basis('F')]})]};
  await writeOperation(db,initial,options);
  assert.ok(search(db,'Nyberättelsetest').some(r=>r.object_id==='N'));
  assert.ok(search(db,'Arbetsfrågetest').some(r=>r.object_id==='Q'));
  assert.deepEqual(db.prepare("SELECT basis_revision_id FROM dependency WHERE revision_id='O@1' ORDER BY basis_revision_id").all().map(r=>r.basis_revision_id),['M@1','R@1']);
  assert.equal(db.prepare('SELECT count(*) n FROM asset').get().n,1);
  assert.equal(db.prepare('SELECT count(*) n FROM native_asset').get().n,1);
  assert.equal(readCurrent(db,'R').media[0].sha256,media.sha256);
  assert.equal(readCurrent(db,'R').media[0].provenance,media.provenance);
  assert.equal((await verifyAssets(db,dir)).ok,true);
  const bundle=path.join(dir,'bundle');await backupBundle(db,bundle,{root:dir,baseline:base});
  const correction={id:'workflow-2',actor:'test',reason:'Rättad observation',changes:[{...obs,expectedVersion:1,bindings:{R:1,M:1},data:{...obs.data,value_literal:'rättläsningsexempel'}}]};
  const unbound={id:'bad-binding',actor:'test',reason:'Test',changes:[{...obs,id:'O2'}]};
  assert.throws(()=>applyOperation(db,unbound),/Versionsbundet underlag/);
  assert.equal(head(db,'O2'),undefined);
  await assert.rejects(()=>writeOperation(db,correction,{...options,afterCommit:()=>{throw Error('Simulerat avbrott efter commit');}}),/finns i databasen/);
  assert.equal(head(db,'O').version,2);
  assert.equal(fs.readdirSync(journal).filter(f=>f.endsWith('.json')).length,1);
  const other=openDB(file);t.after(()=>other.close());
  assert.throws(()=>applyOperation(other,{...correction,id:'competing-writer'}),/Versionskonflikt/);
  assert.equal((await writeOperation(db,correction,options)).unchanged,true);
  assert.equal(syncJournal(db,journal).written,0);
  assert.ok(personView(db,'P').facts[0].pending_reviews.length);
  assert.ok(!search(db,'felläsningsexempel').some(r=>r.object_id==='O'));
  assert.ok(search(db,'rättläsningsexempel').some(r=>r.object_id==='O'));
  const rendered=execFileSync(process.execPath,['genealogy2/cli.mjs','person','P','--db',file,'--format','markdown'],{encoding:'utf8'});
  assert.match(rendered,/Osäkert namn/);assert.match(rendered,/Omprövning väntar/);
  const restoredRoot=path.join(dir,'restored');await restoreBundle(bundle,restoredRoot);
  assert.equal((await verifySource(restoredRoot,path.join(restoredRoot,'genealogy2/import/baseline'))).ok,true);
  const recovered=openDB(path.join(restoredRoot,'genealogy2/data/research.sqlite'));t.after(()=>recovered.close());
  assert.equal((await replayJournal(recovered,journal,{root:restoredRoot})).applied,1);
  assert.equal((await replayJournal(recovered,journal,{root:restoredRoot})).applied,0);
  assert.equal(canonical(exportData(recovered)),canonical(exportData(db)));
  assert.equal(verifyDB(recovered).ok,true);
  // The media are verified, not merely listed in a successful SQLite backup.
  fs.writeFileSync(path.join(dir,media.storagePath),'corrupt');
  assert.equal((await verifyAssets(db,dir)).ok,false);
  await assert.rejects(()=>backupBundle(db,path.join(dir,'bad-backup'),{root:dir,baseline:base}),/skiljer sig/);
  assert.equal(fs.existsSync(path.join(dir,'bad-backup')),false);
  fs.writeFileSync(path.join(bundle,'files',media.storagePath),'corrupt');
  await assert.rejects(()=>restoreBundle(bundle,path.join(dir,'bad-restore')),/ändrats/);
  assert.equal(fs.existsSync(path.join(dir,'bad-restore')),false);
});

test('fel i sista ändringen lämnar varken operation, sökindex eller journal; föråldrat belägg inom samma operation stoppas',async t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-atomic-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  const s=change('S','source',{title:'Första',description:''});
  applyOperation(db,{id:'create',actor:'test',reason:'Test',changes:[s]});
  const before=canonical(exportData(db)),journal=path.join(dir,'journal');
  await assert.rejects(()=>writeOperation(db,{id:'invalid',actor:'test',reason:'Test',changes:[
    change('NEW','source',{title:'Uniktatomtest',description:''}),change('BAD','record',{source_id:'missing',record_type:'test',locator:'1',dependence_note:''})]},
  {root:dir,journal}),/Fel referens/);
  assert.equal(canonical(exportData(db)),before);assert.equal(search(db,'Uniktatomtest').length,0);assert.equal(fs.readdirSync(journal).length,0);
  assert.throws(()=>applyOperation(db,{id:'stale-in-operation',actor:'test',reason:'Test',changes:[
    change('R','record',{source_id:'S',record_type:'test',locator:'1',dependence_note:''},{bindings:{S:1}}),
    {...s,expectedVersion:1,data:{...s.data,title:'Andra'}}]}),/inaktuellt inom operationen/);
  assert.equal(canonical(exportData(db)),before);
});

test('senare journaloperation måste kontrollera även återbrukade gamla och nya medier',async t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-replay-media-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  fs.mkdirSync(path.join(dir,'genealogy/media'),{recursive:true});
  const legacyPath='genealogy/media/old.bin',old=Buffer.from([1,2,3]),fresh=Buffer.from([4,5,6]);
  fs.writeFileSync(path.join(dir,legacyPath),old);fs.writeFileSync(path.join(dir,'new.bin'),fresh);
  const base=path.join(dir,'baseline');await snapshot(dir,base);
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());importBaseline(db,base);
  const media=await stageMedia(dir,path.join(dir,'new.bin'),'Syntetiskt test');
  const journal=path.join(dir,'journal');
  await writeOperation(db,{id:'first',actor:'test',reason:'Bas före återbruk',media:[media],changes:[change('S','source',{title:'S',description:''})]},{root:dir,journal});
  await backupDB(db,path.join(dir,'backup.sqlite'));
  await writeOperation(db,{id:'later',actor:'test',reason:'Återbruk utan ny mediedeklaration',changes:[change('R','record',{
    source_id:'S',record_type:'test',locator:'1',dependence_note:''},{bindings:{S:1},assets:[{path:legacyPath}],media:[{id:media.id}]})]},{root:dir,journal});
  const later=path.join(dir,'later-journal');fs.mkdirSync(later);
  const receipt=fs.readdirSync(journal).find(f=>f.startsWith('000000002-'));fs.copyFileSync(path.join(journal,receipt),path.join(later,receipt));
  const recovered=openDB(path.join(dir,'backup.sqlite'));t.after(()=>recovered.close());
  const before=canonical(exportData(recovered));
  fs.unlinkSync(path.join(dir,legacyPath));
  await assert.rejects(()=>replayJournal(recovered,later,{root:dir}),/saknas eller har ändrats/);
  assert.equal(canonical(exportData(recovered)),before);
  fs.writeFileSync(path.join(dir,legacyPath),old);fs.writeFileSync(path.join(dir,media.storagePath),'corrupt');
  await assert.rejects(()=>replayJournal(recovered,later,{root:dir}),/saknas eller har ändrats/);
  assert.equal(canonical(exportData(recovered)),before);
  fs.writeFileSync(path.join(dir,media.storagePath),fresh);
  assert.equal((await replayJournal(recovered,later,{root:dir})).applied,1);
  assert.equal(canonical(exportData(recovered)),canonical(exportData(db)));
});
