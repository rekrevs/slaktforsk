import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {openDB,importBaseline,exportData,restore,verifyDB,search} from '../lib/store.mjs';
import {applyOperation,personView,head} from '../lib/domain.mjs';
import {buildPilot} from '../import/pilot.mjs';
import {buildRegistry,registryReport} from '../import/registry.mjs';
import {canonical,sha} from '../lib/archive.mjs';

test('fullständiga register bevarar 805 källor och skiljer 25 sidpersoner, en dubblett och ett felläsningsförslag',t=> {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'genealogy2-registry-'));t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
  const db=openDB(path.join(dir,'db.sqlite'),{create:true});t.after(()=>db.close());
  importBaseline(db,new URL('../import/baseline/',import.meta.url).pathname);applyOperation(db,buildPilot(db),{legacy:true});
  const decisions=JSON.parse(fs.readFileSync(new URL('../migration/retirement-decisions.json',import.meta.url),'utf8'));
  assert.throws(()=>buildRegistry(db,{}),/27 avvecklingar/);
  const request=buildRegistry(db,decisions),requestHash=sha(canonical(request));
  const pilotBefore=db.prepare("SELECT * FROM revision WHERE operation_id='T-0641/pilot-v1' ORDER BY id").all();
  applyOperation(db,request);
  assert.equal(sha(canonical(buildRegistry(db,decisions))),requestHash);
  assert.equal(applyOperation(db,request).unchanged,true);
  const report=registryReport(db);
  assert.equal(report.legacyPeople,538);assert.equal(report.persons,536);assert.equal(report.sources,805);
  assert.deepEqual(report.missingPeople,[]);assert.deepEqual(report.missingSources,[]);
  assert.deepEqual(report.retirementOutcomes.map(r=>({...r})),[{outcome:'historical_proposal',n:1},{outcome:'same_identity',n:1},{outcome:'separate_person',n:25}]);
  assert.equal(head(db,'P-0412'),undefined);assert.equal(head(db,'P-0295'),undefined);
  assert.equal(personView(db,'P-0412').importAssessments[0].outcome,'historical_proposal');
  assert.equal(personView(db,'P-0295').importAssessments[0].outcome,'same_identity');
  assert.equal(db.prepare("SELECT count(*) n FROM legacy_mapping WHERE mapping_type='same_identity'").get().n,1);
  assert.equal(db.prepare("SELECT target_id FROM legacy_mapping WHERE legacy_id='P-0412'").get().target_id,'P-0453');
  for(const id of ['P-0008','P-0058','P-0060','P-0077','P-0079','P-0080','P-0081','P-0146','P-0147','P-0400']) {
    const p=personView(db,id).person;
    assert.equal(p.object_id,id);assert.equal(p.legacy_state,'retired');assert.equal(p.disposition,'recorded');assert.equal(p.sex,null);assert.ok(p.caveat);
  }
  assert.equal(personView(db,'P-0060').person.display_name,'Jonas Petter Johansson');
  assert.match(personView(db,'P-0077').person.caveat,/OLÖST/);
  assert.match(personView(db,'P-0080').person.caveat,/utvecklas inte/);
  assert.match(personView(db,'P-0453').assessments.find(a=>a.object_id==='IMPORT-P-0412').caveat,/faders-\/civilståndskonflikt/);
  assert.equal(db.prepare("SELECT count(*) n FROM current_relation").get().n,5);
  assert.equal(db.prepare("SELECT count(*) n FROM person WHERE sex IS NOT NULL").get().n,0);
  assert.equal(db.prepare("SELECT count(*) n FROM pending_review").get().n,0);
  assert.deepEqual(db.prepare("SELECT * FROM revision WHERE operation_id='T-0641/pilot-v1' ORDER BY id").all(),pilotBefore);
  // Every source is compared with its preserved bytes, including amendments.
  for(const e of db.prepare("SELECT e.id,d.text FROM legacy_entity e JOIN document d ON d.path=e.document_path WHERE e.kind='source'").all()) {
    const source=db.prepare('SELECT s.* FROM source s JOIN current_revision r ON r.id=s.revision_id WHERE r.object_id=?').get(e.id);
    assert.equal(source.description,e.text,e.id);assert.equal(source.source_class,null,e.id);
  }
  assert.ok(search(db,'Jonas Petter Johansson').some(r=>r.object_id==='P-0060'));
  assert.equal(verifyDB(db).ok,true);
  const data=exportData(db),digest=sha(canonical(data));restore(data,path.join(dir,'restored.sqlite'));
  const restored=openDB(path.join(dir,'restored.sqlite'));assert.equal(sha(canonical(exportData(restored))),digest);restored.close();
});
