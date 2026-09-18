import assert from 'node:assert/strict';
import {readCurrent,personView} from '../lib/domain.mjs';
import {checkPersons09PartARisks} from './persons-09-part-a-risk.mjs';
import {checkPersons09PartBRisks} from './persons-09-part-b-risk.mjs';
import {checkPersons09PartCRisks} from './persons-09-part-c-risk.mjs';
import {checkPersons09PartDRisks} from './persons-09-part-d-risk.mjs';

export function checkPersons09Risks(db) {
  const parts=[checkPersons09PartARisks(db),checkPersons09PartBRisks(db),checkPersons09PartCRisks(db),checkPersons09PartDRisks(db)];
  for(const result of parts)assert.equal(result.ok,true);
  // Oberoende granskning av hela P-0412-akten/profilen samt registerbeslutet:
  // ett avvisat läsningsförslag får inte återuppstå som person eller alias.
  assert.equal(readCurrent(db,'P-0412'),null);
  const decision=readCurrent(db,'IMPORT-P-0412');
  assert.equal(decision.outcome,'historical_proposal');
  assert.equal(decision.subject_id,'P-0453');
  assert.match(decision.caveat,/faders-\/civilståndskonflikt/);
  const view=personView(db,'P-0412');
  assert.equal(view.person,null);
  assert.equal(view.relations.length,0);
  assert.equal(view.events.length,0);
  assert.ok(view.research.questions.length>0);
  assert.ok(view.research.questions.every(q=>q.subject_id==='IMPORT-P-0412'&&!q.active));
  assert.equal(readCurrent(db,'ASSESSMENT-P-0412').disposition,'retired');
  assert.equal(readCurrent(db,'BIO-P-0412').disposition,'retired');
  assert.equal(db.prepare("SELECT count(*) n FROM legacy_mapping WHERE legacy_id='P-0412' AND mapping_type='same_identity'").get().n,0);
  return {ok:true,groups:1+parts.reduce((n,p)=>n+p.groups,0),parts};
}
