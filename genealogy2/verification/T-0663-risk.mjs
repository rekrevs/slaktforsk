import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';
import {checkT0663ObservationARisks} from './T-0663-observation-a-risk.mjs';
import {checkT0663ObservationCRisks} from './T-0663-observation-c-risk.mjs';
import {checkT0663StatusReviewRisks} from './T-0663-status-risk.mjs';

export function checkT0663Risks(db){
 const results=[checkT0663ObservationARisks(db),checkT0663ObservationCRisks(db),checkT0663StatusReviewRisks(db)];
 for(const day of ['05','12','19']){
  const id=`E-banns-P-0016-P-0532-1903-04-${day}`,event=readCurrent(db,id);
  assert.equal(event.version,2);assert.equal(event.event_type,'banns');assert.equal(event.disposition,'accepted');
  const date=JSON.parse(event.date_json);assert.equal(date.precision,'year');assert.equal(date.value,'1903');assert.match(date.literal,/månad ej utskriven/);
  const old=db.prepare('SELECT * FROM event WHERE revision_id=?').get(`${id}@1`);assert.equal(JSON.parse(old.date_json).value,`1903-04-${day}`);
  const fact=readCurrent(db,`F-T0663-banns-${day}-month-interpretation`),value=JSON.parse(fact.value_json);
  assert.equal(value.month_written,false);assert.equal(value.legacy_interpretation,`1903-04-${day}`);assert.equal(value.new_original_reading,false);
  for(const person of ['P-0016','P-0532']){
   const ep=readCurrent(db,`EP-${id}-${person}-subject`);assert.equal(ep.version,2);assert.equal(ep.person_id,person);assert.equal(ep.disposition,'accepted');
   assert(ep.evidence.some(e=>e.basis_revision_id===`${id}@2`));
  }
 }
 assert.equal(JSON.parse(readCurrent(db,'E-P0016-marriage1903').date_json).value,'1903-05-01');
 assert.equal(db.prepare('SELECT count(*) n FROM pending_review').get().n,0);
 assert.equal(db.prepare("SELECT count(*) n FROM review_resolution WHERE operation_id='T-0663/reviewed-corrections-v1'").get().n,25);
 return {ok:true,groups:results.reduce((n,r)=>n+r.groups,0)+3,components:results,banns:3,participations:6,resolvedPairs:25};
}
