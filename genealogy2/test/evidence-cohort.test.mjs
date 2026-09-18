import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,importBaseline,exportData,restore,verifyDB} from '../lib/store.mjs';
import {applyOperation,inspect,readCurrent} from '../lib/domain.mjs';
import {buildPilot} from '../import/pilot.mjs';
import {buildRegistry} from '../import/registry.mjs';
import {buildEvidence} from '../import/evidence.mjs';
import {canonical,sha} from '../lib/archive.mjs';
import {migrationReport} from '../lib/migration.mjs';

const read=name=>JSON.parse(fs.readFileSync(new URL(`../migration/${name}.json`,import.meta.url),'utf8'));

function createCohortFixture(t,prior) {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-next-cohort-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  importBaseline(db,new URL('../import/baseline/',import.meta.url).pathname);
  applyOperation(db,buildPilot(db),{legacy:true});applyOperation(db,buildRegistry(db,read('retirement-decisions')));
  for(let i=1;i<=prior;i++) {
    if(i===4)for(const suffix of ['media-links','media-review'])applyOperation(db,JSON.parse(fs.readFileSync(new URL(`../operations/T-0649-${suffix}-v1.json`,import.meta.url),'utf8')));
    if(i===5)for(const suffix of ['source-definitions','source-controls','media-links','media-review'])applyOperation(db,JSON.parse(fs.readFileSync(new URL(`../operations/T-0650-${suffix}-v1.json`,import.meta.url),'utf8')));
    applyOperation(db,JSON.parse(fs.readFileSync(new URL(`../operations/T-${String(645+i).padStart(4,'0')}-evidence-${String(i).padStart(2,'0')}-v1.json`,import.meta.url),'utf8')));
  }
  return {dir,db};
}

function verifyCohortTransfer(db,dir,group,request,reviews,before) {
  assert.ok(request.changes.every(c=>['record','transcription','assessment'].includes(c.kind)));
  assert.deepEqual(db.prepare('SELECT * FROM revision WHERE operation_id<>? ORDER BY id').all(request.id),before);
  assert.equal(canonical(buildEvidence(db,reviews,{group})),canonical(request));
  assert.equal(applyOperation(db,request).unchanged,true);
  const report=migrationReport(db);
  for(const u of report.units.filter(u=>u.group===group)) {
    const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(u.id);
    assert.ok(d,`${u.path}:${u.id}`);assert.equal(d.operation_id,request.id);
    if(d.state==='pending_interpretation')assert.ok(d.question.trim());
    if(d.state==='mapped_complete')assert.ok(d.target_id);
  }
  for(const c of request.changes.filter(c=>c.kind==='transcription')) {
    const origin=c.origins.find(o=>o.coverage==='complete');
    assert.equal(c.data.text,db.prepare('SELECT raw FROM unit WHERE id=?').get(origin.unit).raw);
  }
  assert.equal(verifyDB(db).ok,true);
  const exported=exportData(db),digest=sha(canonical(exported));restore(exported,path.join(dir,'restored.sqlite'));
  const restored=openDB(path.join(dir,'restored.sqlite'));
  try{assert.equal(sha(canonical(exportData(restored))),digest);}finally{restored.close();}
}

test('första verkliga evidenskohorten bevarar postgränser, rättelser, sökomfång och alla textenheter',t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-cohort-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  importBaseline(db,new URL('../import/baseline/',import.meta.url).pathname);
  applyOperation(db,buildPilot(db),{legacy:true});applyOperation(db,buildRegistry(db,read('retirement-decisions')));
  const before=db.prepare('SELECT * FROM revision ORDER BY id').all();
  const reviews=['a','b','c'].flatMap(p=>read(`evidence-01-${p}`));
  const request=buildEvidence(db,reviews);assert.equal(reviews.length,200);
  assert.ok(request.changes.every(c=>['record','transcription','assessment'].includes(c.kind)));
  applyOperation(db,request);
  assert.deepEqual(db.prepare('SELECT * FROM revision WHERE operation_id<>? ORDER BY id').all(request.id),before);
  assert.equal(canonical(buildEvidence(db,reviews)),canonical(request));
  assert.equal(applyOperation(db,request).unchanged,true);
  const objects=id=>inspect(db,id).representations;
  const records=id=>objects(id).filter(r=>r.kind==='record');
  const recordIds=id=>records(id).map(r=>r.object_id).sort();
  for(const [a,b] of [['C-0007','C-0021'],['C-0015','C-0019'],['C-0164','C-0166'],['C-0170','C-0173']]) {
    assert.equal(recordIds(a).filter(id=>recordIds(b).includes(id)).length,1,`${a}/${b}`);
  }
  const arrival=records('C-0094');
  assert.equal(arrival.length,2);
  const adela=arrival.find(r=>r.object_id!=='R-C0094-85-86');
  assert.match(adela.locator,/nr 84/);assert.match(adela.caveat,/datum.*olöst/);
  assert.match(objects('C-0094').filter(r=>r.kind==='transcription').map(r=>r.reading_note).join('\n'),/85–86/);
  assert.equal(recordIds('C-0075').includes('R-C0075-29'),true);
  const corrected=records('C-0107');assert.equal(corrected.length,1);
  assert.match(corrected[0].caveat,/upphävt/);assert.match(corrected[0].caveat,/Jon Andersson/);
  assert.match(corrected[0].dependence_note,/C-0872/);
  assert.equal(records('C-0146').length,1);
  assert.match(records('C-0146')[0].caveat,/LEAD/);
  assert.ok(inspect(db,'C-0146').conversionDecisions.some(d=>/exakt 20 oktober/.test(d.question)));
  assert.equal(records('C-0191').length,0);
  assert.ok(inspect(db,'C-0191').conversionDecisions.some(d=>/aktivt noll/.test(d.question)));
  const census=records('C-0060');assert.equal(census.length,2);
  assert.ok(census.every(r=>/Ingen bild har öppnats/.test(r.caveat)));
  assert.ok(census.every(r=>readCurrent(db,r.object_id).media.some(m=>m.sha256==='bb8a2206f147fbaea4795773e2f13773b1c3eb09eb8bc8243dc3db3b7d2c9c8b')));
  const report=migrationReport(db),group=report.groups.find(g=>g.id==='evidence-01');
  assert.equal(group.citations.length,200);assert.equal(group.sources.length,135);
  for(const u of report.units.filter(u=>u.group==='evidence-01')) {
    const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(u.id);
    assert.ok(d,`${u.path}:${u.id}`);assert.equal(d.operation_id,request.id);
    if(d.state==='pending_interpretation')assert.ok(d.question.trim());
    if(d.state==='mapped_complete')assert.ok(d.target_id);
  }
  for(const c of request.changes.filter(c=>c.kind==='transcription')) {
    const origin=c.origins.find(o=>o.coverage==='complete');
    assert.equal(c.data.text,db.prepare('SELECT raw FROM unit WHERE id=?').get(origin.unit).raw);
  }
  assert.equal(verifyDB(db).ok,true);
  const exported=exportData(db),digest=sha(canonical(exported));restore(exported,path.join(dir,'restored.sqlite'));
  const restored=openDB(path.join(dir,'restored.sqlite'));t.after(()=>restored.close());
  assert.equal(sha(canonical(exportData(restored))),digest);
});

test('femte kohorten bevarar härledda index, positiva kontrollposter i söknoll och oförenliga råuppgifter',t=> {
  const {db,dir}=createCohortFixture(t,4);
  const reviews=['a','b','c','d'].flatMap(p=>read(`evidence-05-${p}`));assert.equal(reviews.length,200);
  const initial=db.prepare('SELECT * FROM revision ORDER BY id').all();
  const prep=name=>JSON.parse(fs.readFileSync(new URL(`../operations/T-0650-${name}-v1.json`,import.meta.url),'utf8'));
  for(const name of ['source-definitions','source-controls']) {
    const source=prep(name);applyOperation(db,source);
    for(const c of source.changes) {
      const current=readCurrent(db,c.id);assert.equal(current.source_class,null);
      assert.equal(current.disposition,'recorded');assert.equal(current.origins.length,1);
      const origin=current.origins[0];assert.equal(origin.coverage,'complete');
      assert.ok(current.description.includes(db.prepare('SELECT raw FROM unit WHERE id=?').get(origin.unit_id).raw));
    }
  }
  assert.deepEqual(db.prepare("SELECT * FROM revision WHERE operation_id NOT LIKE 'T-0650/source-%' ORDER BY id").all(),initial);
  assert.equal(readCurrent(db,'S-0817').archive_reference,'SE/GLA/13300/C/6');
  assert.throws(()=>buildEvidence(db,reviews,{group:'evidence-05'}),/Medielänk.*ny version/);
  const media=prep('media-links');assert.equal(media.changes.length,4);
  const previous=media.changes.map(c=>readCurrent(db,c.id));applyOperation(db,media);
  for(const old of previous) {
    const now=readCurrent(db,old.object_id);assert.equal(now.version,old.version+1);
    for(const key of ['source_id','record_type','locator','dependence_note','caveat','disposition','evidence_status'])assert.equal(now[key],old[key]);
    assert.equal(now.media.length,old.media.length+1);
    for(const a of old.media)assert.ok(now.media.some(b=>canonical(a)===canonical(b)));
    for(const o of old.origins)assert.ok(now.origins.some(n=>n.unit_id===o.unit_id&&n.coverage===o.coverage&&n.note===o.note));
    assert.deepEqual(now.evidence.map(({revision_id,...e})=>e),old.evidence.map(({revision_id,...e})=>e));
  }
  assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,8);
  applyOperation(db,prep('media-review'));assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
  const before=db.prepare('SELECT * FROM revision ORDER BY id').all();
  const request=buildEvidence(db,reviews,{group:'evidence-05'});applyOperation(db,request);
  const records=id=>inspect(db,id).representations.filter(r=>r.kind==='record');
  const visible=id=>records(id).map(r=>r.caveat+'\n'+r.dependence_note+'\n'+r.readings.map(x=>x.body+'\n'+x.caveat).join('\n')).join('\n');
  const questions=id=>inspect(db,id).conversionDecisions.map(d=>d.question).join('\n');
  assert.match(visible('C-0820'),/ingen tvåkällorskonflikt/);
  assert.match(visible('C-0833'),/kopplingen.*P-0123 återöppnad/);
  assert.match(visible('C-0846'),/avvisad personbindning/);
  assert.match(visible('C-0899'),/Signe.*Sigrid/);assert.match(visible('C-0899'),/enhet normaliseras inte/);
  assert.match(visible('C-0907'),/fyra.*möjligheter/);assert.match(visible('C-0907'),/postnummer, inte 27 juli/);
  assert.ok(records('C-0910').some(r=>r.record_type==='place_index_entry'&&r.media.some(a=>/00153993_00004/.test(a.path))));
  assert.match(visible('C-0916'),/C0899.*utdrag ur samma församlingsbok/);
  assert.match(visible('C-0919'),/4\/3.*11\/3/);
  const c954=records('C-0954');assert.equal(c954.length,2);
  assert.ok(c954.some(r=>r.record_type==='census_index'&&/Ingrid/.test(r.caveat)));
  assert.ok(c954.some(r=>r.record_type==='census_household'&&/bara Axel, Hulda och Axel Ivar/.test(r.caveat)));
  const trs=inspect(db,'C-0954').representations.filter(r=>r.kind==='transcription');
  assert.ok(trs.length>=3);assert.ok(trs.every(r=>!r.text.includes('### Hushållet')));
  assert.equal(records('C-0955').length,8);assert.match(visible('C-0955'),/Bror Erik1902|Bror Erik född1902/);
  assert.match(questions('C-0956'),/falska noll/);assert.match(questions('C-0957'),/nedre dopgräns/);
  assert.match(visible('C-0958'),/Flen\/Lerbo/);assert.match(visible('C-0959'),/endast en hypotes/);
  assert.match(visible('C-0981'),/1258/);assert.match(visible('C-0981'),/stadsägonoteringen/);
  assert.equal(records('C-0992').filter(r=>r.source_id==='S-0817').length,5);
  assert.equal(records('C-0995').length,7);assert.match(questions('C-0995'),/post 40/);
  assert.match(questions('C-0997'),/1808.*1829/);
  const birth=records('C-0114');assert.ok(records('C-1003').some(r=>birth.some(b=>b.object_id===r.object_id)));
  for(const [a,b]of[['C-0896','C-0021'],['C-0926','C-0675'],['C-0930','C-0677']])assert.ok(records(a).some(r=>r.version===2&&records(b).some(x=>x.object_id===r.object_id)));
  verifyCohortTransfer(db,dir,'evidence-05',request,reviews,before);
});

test('andra verkliga kohorten bevarar rättade flyttkedjor och omfång samt återbrukar tidigare källposter',t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-cohort2-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  importBaseline(db,new URL('../import/baseline/',import.meta.url).pathname);
  applyOperation(db,buildPilot(db),{legacy:true});applyOperation(db,buildRegistry(db,read('retirement-decisions')));
  applyOperation(db,JSON.parse(fs.readFileSync(new URL('../operations/T-0646-evidence-01-v1.json',import.meta.url),'utf8')));
  const before=db.prepare('SELECT * FROM revision ORDER BY id').all();
  const reviews=['a','b','c'].flatMap(p=>read(`evidence-02-${p}`));
  const request=buildEvidence(db,reviews,{group:'evidence-02'});assert.equal(reviews.length,200);
  assert.ok(request.changes.every(c=>['record','transcription','assessment'].includes(c.kind)));
  applyOperation(db,request);
  assert.deepEqual(db.prepare('SELECT * FROM revision WHERE operation_id<>? ORDER BY id').all(request.id),before);
  assert.equal(canonical(buildEvidence(db,reviews,{group:'evidence-02'})),canonical(request));
  assert.equal(applyOperation(db,request).unchanged,true);
  const records=id=>inspect(db,id).representations.filter(r=>r.kind==='record');
  assert.ok(records('C-0252').some(r=>r.object_id==='R-C0252-family'));
  const portraits=records('C-0264');assert.equal(portraits.length,6);
  assert.ok(portraits.every(r=>r.media.some(m=>m.path.endsWith('.jpeg'))));
  assert.ok(portraits.every(r=>/inte bosättnings/.test(r.caveat)));
  const chronicle=records('C-0266');assert.equal(chronicle.filter(r=>r.record_type==='photograph_caption').length,11);
  assert.ok(records('C-0262').some(r=>/612751/.test(r.locator)&&/1900-tal/.test(r.caveat)));
  const first=records('C-0218'),later=records('C-0378');
  assert.ok(first.filter(r=>/460/.test(r.locator)).every(r=>later.some(l=>l.object_id===r.object_id)));
  assert.ok(first.some(r=>/460/.test(r.locator)));
  assert.ok(later.some(r=>/Skön/.test(r.caveat+' '+r.readings.map(x=>x.body+' '+x.caveat).join('\n'))));
  assert.ok(later.some(r=>/Bernhard/.test(r.caveat+' '+r.readings.map(x=>x.body+' '+x.caveat).join('\n'))));
  assert.equal(records('C-0203').length,0);
  const decisions=inspect(db,'C-0203').conversionDecisions;
  assert.ok(decisions.some(d=>/bildbundet|bildbundna/.test(d.rationale+' '+d.question)));
  assert.ok(decisions.some(d=>/intervall|september/.test(d.rationale+' '+d.question)));
  const chain=records('C-0212');
  assert.ok(chain.some(r=>/1814|övre/.test(r.locator+' '+r.caveat)));
  assert.ok(chain.some(r=>/1821|nedre/.test(r.locator+' '+r.caveat)));
  assert.ok(chain.some(r=>/avvis|inte.*P-0058|ingen.*P-0058/.test(r.caveat)));
  assert.ok(inspect(db,'C-0280').conversionDecisions.some(d=>/1878/.test(d.question)));
  const census=records('C-0348');assert.equal(census.length,1);
  assert.match(census[0].caveat+' '+census[0].dependence_note,/utdrag|härledd|avskrift/);
  assert.match(census[0].caveat+' '+census[0].readings.map(r=>r.body).join('\n'),/åtta|8 yngre/);
  const report=migrationReport(db),group=report.groups.find(g=>g.id==='evidence-02');
  assert.equal(group.citations.length,200);assert.equal(group.sources.length,135);
  for(const u of report.units.filter(u=>u.group==='evidence-02')) {
    const d=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(u.id);
    assert.ok(d,`${u.path}:${u.id}`);assert.equal(d.operation_id,request.id);
    if(d.state==='pending_interpretation')assert.ok(d.question.trim());
    if(d.state==='mapped_complete')assert.ok(d.target_id);
  }
  assert.equal(verifyDB(db).ok,true);
  const exported=exportData(db),digest=sha(canonical(exported));restore(exported,path.join(dir,'restored.sqlite'));
  const restored=openDB(path.join(dir,'restored.sqlite'));t.after(()=>restored.close());
  assert.equal(sha(canonical(exportData(restored))),digest);
});

test('tredje verkliga kohorten skiljer rättelser, återbrukad gammal text och kvarstående källkonflikter',t=> {
  const {db,dir}=createCohortFixture(t,2);
  const reviews=['a','b','c','d'].flatMap(p=>read(`evidence-03-${p}`));assert.equal(reviews.length,200);
  const before=db.prepare('SELECT * FROM revision ORDER BY id').all();
  const request=buildEvidence(db,reviews,{group:'evidence-03'});applyOperation(db,request);
  const records=id=>inspect(db,id).representations.filter(r=>r.kind==='record');
  const visible=id=>records(id).map(r=>r.caveat+'\n'+r.readings.map(x=>x.body+'\n'+x.caveat).join('\n')).join('\n');
  assert.match(visible('C-0408'),/1891-04-01/);assert.match(visible('C-0408'),/1891-04-12/);
  assert.match(visible('C-0408'),/ålder|Ålder/);
  assert.match(visible('C-0410'),/1882-11-20/);
  assert.match(visible('C-0411'),/1895-03-02/);assert.match(visible('C-0411'),/1896-10-15/);
  const previous=records('C-0413');
  assert.ok(records('C-0414').some(r=>previous.some(p=>p.object_id===r.object_id)));
  assert.match(visible('C-0414'),/felaktig|ogiltig|upphä|ofullständig/);
  assert.match(visible('C-0421'),/24/);assert.match(visible('C-0421'),/29/);assert.match(visible('C-0421'),/konflikt/);
  assert.match(visible('C-0485'),/första[^.\n]*blad/i);
  assert.match(visible('C-0485'),/235–254 är inte omverifierad/);
  assert.match(visible('C-0545'),/OWNER_CONFIRMED/);
  assert.match(visible('C-0545'),/Johannes Ivar Fredberg P-0287 är far till Anders Ivar Höök P-0239/);
  assert.match(visible('C-0549'),/1880-07-21/);assert.match(visible('C-0549'),/1876-05-24/);
  assert.match(visible('C-0549'),/REJECTED/);assert.match(visible('C-0549'),/TRANSCRIBED\/medel/);
  assert.match(visible('C-0549'),/källberoende|beroendet/);
  const reused=records('C-0550');assert.equal(reused.length,3);
  for(const id of ['C-0002','C-0061','C-0058'])assert.ok(records(id).some(r=>reused.some(x=>x.object_id===r.object_id)));
  assert.ok(reused.every(r=>!request.changes.some(c=>c.id===r.object_id)));
  assert.ok(records('C-0542').every(r=>!records('C-0452').some(x=>x.object_id===r.object_id)));
  assert.match(visible('C-0552'),/1892-04-20/);assert.match(visible('C-0552'),/otolkad/);
  assert.match(visible('C-0554'),/CONFLICT/);
  verifyCohortTransfer(db,dir,'evidence-03',request,reviews,before);
});

test('fjärde verkliga kohorten versionsbevarar nya bildlänkar och skiljer råkolumner, omprövningar och projektslutledningar',t=> {
  const {db,dir}=createCohortFixture(t,3);
  const reviews=['a','b','c','d'].flatMap(p=>read(`evidence-04-${p}`));assert.equal(reviews.length,200);
  assert.throws(()=>buildEvidence(db,reviews,{group:'evidence-04'}),/Medielänk.*ny version/);
  const media=JSON.parse(fs.readFileSync(new URL('../operations/T-0649-media-links-v1.json',import.meta.url),'utf8'));
  const previous=media.changes.map(c=>readCurrent(db,c.id));assert.equal(previous.length,8);
  const oldRevisions=db.prepare('SELECT * FROM revision ORDER BY id').all();
  applyOperation(db,media);
  assert.deepEqual(db.prepare('SELECT * FROM revision WHERE operation_id<>? ORDER BY id').all(media.id),oldRevisions);
  let additions=0;
  for(const old of previous) {
    const current=readCurrent(db,old.object_id);assert.equal(current.version,2);
    for(const key of ['source_id','record_type','locator','dependence_note','caveat','disposition','evidence_status'])assert.equal(current[key],old[key]);
    for(const asset of old.media)assert.ok(current.media.some(a=>canonical(a)===canonical(asset)));
    for(const origin of old.origins)assert.ok(current.origins.some(o=>o.unit_id===origin.unit_id&&o.coverage===origin.coverage&&o.note===origin.note));
    for(const evidence of old.evidence)assert.ok(current.evidence.some(e=>e.basis_revision_id===evidence.basis_revision_id&&e.role===evidence.role&&e.note===evidence.note));
    additions+=current.media.length-old.media.length;
  }
  assert.equal(additions,9);assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,9);
  applyOperation(db,JSON.parse(fs.readFileSync(new URL('../operations/T-0649-media-review-v1.json',import.meta.url),'utf8')));
  assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
  const before=db.prepare('SELECT * FROM revision ORDER BY id').all();
  const request=buildEvidence(db,reviews,{group:'evidence-04'});applyOperation(db,request);
  const records=id=>inspect(db,id).representations.filter(r=>r.kind==='record');
  const visible=id=>records(id).map(r=>r.caveat+'\n'+r.readings.map(x=>x.body+'\n'+x.caveat).join('\n')).join('\n');
  const questions=id=>inspect(db,id).conversionDecisions.map(d=>d.question).join('\n');
  assert.match(visible('C-0606'),/James→Jonas/);assert.match(visible('C-0606'),/1849.*1839/);
  assert.match(visible('C-0654'),/rad 9/);assert.match(visible('C-0654'),/inte.*Anna Stina/);
  assert.match(visible('C-0675'),/Tuna, inte Timrå/);assert.match(visible('C-0675'),/Egnar.*Eugen/);
  assert.match(visible('C-0675'),/09-28.*12-28.*olöst/);
  assert.equal(records('C-0699').length,0);assert.match(questions('C-0699'),/vänstersidesstarter/);
  assert.match(questions('C-0699'),/536/);assert.match(questions('C-0699'),/562/);
  const drill=records('C-0708').find(r=>/1851/.test(r.locator));assert.ok(drill);
  assert.ok(records('C-0752').some(r=>r.object_id===drill.object_id));
  assert.match(visible('C-0763'),/1845-07-07/);assert.match(visible('C-0763'),/Inget hustrunamn eller inskriven vigseldag/);
  assert.match(visible('C-0767'),/28\/27.*modern/);assert.match(visible('C-0767'),/förlossningsbiträde, inte religion/);
  assert.match(visible('C-0768'),/32\/31.*modern/);assert.match(visible('C-0768'),/nöddöpt 9 juli.*bekräftelse 12 juli/);
  assert.match(visible('C-0793'),/avvisar.*Carl Fredric Pehrsson/);
  assert.match(visible('C-0798'),/Ulla, inte Ella/);assert.match(visible('C-0798'),/28, inte 23/);
  const halla=records('C-0725').find(r=>/1822.*post 3/.test(r.locator));assert.ok(halla);
  assert.ok(records('C-0798').some(r=>r.object_id===halla.object_id));
  assert.match(visible('C-0733'),/Skelefte/);assert.match(visible('C-0733'),/räkne|resonemang/);
  assert.match(visible('C-0744'),/LEAD/);assert.match(visible('C-0744'),/dagbråk och årsläsning/);
  assert.equal(records('C-0751').length,4);assert.match(visible('C-0751'),/sammanlagt fyra familjegrupper/);
  assert.match(visible('C-0751'),/inte exakta födelseintervall/);
  for(const id of ['C-0649','C-0651','C-0688','C-0741','C-0777'])assert.ok(records(id).some(r=>r.version===2&&r.media.some(a=>a.path.includes(id))));
  assert.ok(records('C-0688')[0].media.some(a=>a.path.includes('C0045752_00064')));
  assert.match(visible('C-0688'),/afflyttad och afliden/);
  verifyCohortTransfer(db,dir,'evidence-04',request,reviews,before);
});

test('sista evidenskohorten bevarar sena identitetsgränser, råkonflikter och katalogåtkomst utan personslutsatser',t=> {
  const {db,dir}=createCohortFixture(t,5);
  const prep=name=>JSON.parse(fs.readFileSync(new URL(`../operations/T-0651-${name}-v1.json`,import.meta.url),'utf8'));
  const initial=db.prepare('SELECT * FROM revision ORDER BY id').all();let sources=0;
  for(const name of ['source-definitions','source-controls','source-volumes']) {
    const operation=prep(name);sources+=operation.changes.length;applyOperation(db,operation);
    for(const c of operation.changes) {
      const current=readCurrent(db,c.id);assert.equal(current.source_class,null);assert.equal(current.disposition,'recorded');
      assert.ok(current.origins.length);
      for(const origin of current.origins)assert.ok(current.description.includes(db.prepare('SELECT raw FROM unit WHERE id=?').get(origin.unit_id).raw));
    }
  }
  assert.equal(sources,13);assert.equal(readCurrent(db,'S-0830'),null);
  assert.deepEqual(db.prepare("SELECT * FROM revision WHERE operation_id NOT LIKE 'T-0651/source-%' ORDER BY id").all(),initial);
  const reviews=['a','b','c','d'].flatMap(p=>read(`evidence-06-${p}`));assert.equal(reviews.length,111);
  assert.throws(()=>buildEvidence(db,reviews,{group:'evidence-06'}),/Medielänk.*ny version/);
  const media=prep('media-links');assert.equal(media.changes.length,1);
  const old=readCurrent(db,media.changes[0].id);applyOperation(db,media);
  const now=readCurrent(db,old.object_id);assert.equal(now.version,old.version+1);
  for(const k of ['source_id','record_type','locator','dependence_note','caveat','disposition','evidence_status'])assert.equal(now[k],old[k]);
  for(const asset of old.media)assert.ok(now.media.some(a=>canonical(a)===canonical(asset)));
  assert.equal(now.media.length,old.media.length+1);assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,1);
  applyOperation(db,prep('media-review'));assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
  const before=db.prepare('SELECT * FROM revision ORDER BY id').all();
  const request=buildEvidence(db,reviews,{group:'evidence-06'});applyOperation(db,request);
  const records=id=>inspect(db,id).representations.filter(r=>r.kind==='record');
  const visible=id=>records(id).map(r=>r.caveat+'\n'+r.dependence_note+'\n'+r.readings.map(x=>x.body+'\n'+x.caveat).join('\n')).join('\n');
  assert.match(visible('C-1005'),/30\/1.*dokumentationsavvikelse/);
  assert.ok(records('C-1005').every(r=>!r.locator.includes('30/1')));
  const birth=records('C-1017').find(r=>r.record_type==='birth_baptism');assert.ok(birth);
  assert.ok(records('C-0509').some(r=>r.object_id===birth.object_id));
  assert.ok(!birth.readings.some(r=>r.body.includes('Samma positiva post som C-0435/C-0512')));
  assert.match(visible('C-1017'),/38.*Indalsposter|Indalsposter/);assert.match(visible('C-1017'),/Svarskopian är inte återfunnen/);
  assert.match(visible('C-1035'),/hustru är onamngiven/);
  assert.match(visible('C-1054'),/1,40 kr/);assert.match(visible('C-1054'),/235–254/);
  assert.ok(records('C-1054').some(r=>records('C-0485').some(x=>x.object_id===r.object_id)));
  assert.match(visible('C-1055'),/interna motsägelsen/);
  assert.match(visible('C-1055'),/A I\/8b s\. 536 bär Maria Brita 1847.*A I\/7b s\. 400:s 1845/);
  assert.match(visible('C-1060'),/inte.*biologiska faderskap/);
  assert.match(visible('C-1072'),/1\/6→10\/6→16\/6/);assert.match(visible('C-1072'),/Tomt Hvarifrån/);
  assert.match(visible('C-1087'),/27 år till omkring 17 år/);
  assert.ok(records('C-1088').some(r=>r.source_id==='S-0556'));
  assert.match(visible('C-1092'),/faktisk flytt 1860/);
  assert.match(visible('C-1110'),/vuxenkedjans positiva dödspost/);assert.match(visible('C-1110'),/födel.*återöppnad som kandidat/);
  const death=records('C-1110').find(r=>r.record_type==='death_burial');assert.ok(death);
  const deathTR=inspect(db,'C-1110').representations.filter(r=>r.kind==='transcription'&&r.record_id===death.object_id);
  assert.equal(deathTR.length,2);assert.ok(deathTR.every(r=>!r.text.includes('fysisk dödsplats')));
  assert.equal(records('C-1112').length,34);assert.ok(records('C-1112').every(r=>r.record_type.startsWith('catalog')));
  assert.ok(records('C-1114').some(r=>r.object_id===old.object_id&&r.version===2&&r.media.some(a=>a.path.endsWith('C-1114-motala-register-utsnitt.jpg'))));
  assert.equal(records('C-1115').length,0);
  assert.ok(inspect(db,'C-1115').conversionDecisions.some(d=>/119.*personantal/.test(d.rationale)));
  verifyCohortTransfer(db,dir,'evidence-06',request,reviews,before);
});
