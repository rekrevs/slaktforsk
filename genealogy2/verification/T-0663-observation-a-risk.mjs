import assert from 'node:assert/strict';
import {readCurrent} from '../lib/domain.mjs';
import {canonical} from '../lib/archive.mjs';

const observed=[
  'O-P-0027-children-book-sequence','O-P-0021-bjerg-first-marriage',
  'O-P-0021-household-date-variants','O-P-0021-Thilda-household-row',
  'O-P-0020-C0025-birth1858','O-P-0003-C0008-mother-birth-corrected',
  'O-P-0368-C0559-death','O-P-0021-census-1930',
  'O-P-0344-C0836-s92','O-P-0362-C1013-rejected-Carolina'
];
const unchangedDependents=[
  'F-P-0373-source_correction-wife-fields-already-known','F-P-0373-source_scope-screenshots-and-unread-columns','F-P-0373-life_scope-occupation-and-book-period',
  'E-death-P-0368','E-burial-P-0368','EP-E-death-P-0368-P-0368-principal','EP-E-burial-P-0368-P-0368-principal','F-P-0368-life_scope-raw-death-note-and-open-middle','F-P-0368-name_scope-Adelbert-Adalbert',
  'ID-P-0313-not-C1013-Carolina','SEARCH-P-0362-C1013-page55','F-P-0362-life_scope-secure-father-open-origin','F-P-0362-source_scope-corrected-searches-and-copy-debt','F-P-0363-life_scope-mother-widow-and-unread-consent'
];
const decode=x=>typeof x==='string'?JSON.parse(x):x;

function semanticChecks(get){
  let groups=0;
  const value=id=>decode(get(id).value_json??get(id).data?.value_json);
  const record=id=>get(id).record_id??get(id).data?.record_id;
  assert.deepEqual(value(observed[0]),{s15:['Lars Olof','Barbro Margareta','Björn Flemming']});
  assert.equal(record(observed[0]),'R-54b9a43526242cc9adee6c31');
  const children=value('F-P-0027-household_comparison-children-book-sequence');
  assert.equal(children.later_addition,'Gunilla Birgitta');assert.equal(children.later_record,'R-83ce4c405b6733bac7afd35c');assert.equal(children.exhaustive_lifetime_child_list,false);groups++;
  assert.deepEqual(value(observed[1]).group,['Carl Johan','Emma Charlotta','Anna Sofia','Augusta Victoria']);
  assert.deepEqual(value(observed[2]),{CarlJohan:'1850-04-24',AnnaSofia:'1857-06-24',VictorAlbin:'1874-11-03'});
  assert.deepEqual(value('O-P-0021-C0999-child-date-reports'),{CarlJohan:'1850-07-19',AnnaSofia:'1857-06-02',VictorAlbin:'1874-11-13'});
  assert.equal(record('O-P-0021-C0999-child-date-reports'),'R-8a83ee945b26cabe321fb1ab');groups++;
  assert.deepEqual(value(observed[3]),{birthLiteral:'1861-10-12',crossedOut:true,name:'Thilda Augusta'});
  const bjerg=value('F-P-0021-household_comparison-Bjerg-AI4-AI5');assert.equal(bjerg.Thilda_absent_from_AI5,true);assert.equal(bjerg.Thilda_death_inferred,false);assert.equal(bjerg.biological_full_siblings_proven,false);assert.equal(bjerg.selected_birth_dates,null);groups++;
  assert.deepEqual(value(observed[4]),{year:1858});assert.deepEqual(value('O-P-0020-C0026-birth1850'),{year:1850});
  assert.equal(record('O-P-0020-C0026-birth1850'),'R-9fcd6c77fb3fbdc8a110e24b');
  const years=value('F-P-0020-source_conflict-census1900-1910-birth-years');assert.equal(years.mother.census1900.raw,'67');assert.equal(years.mother.census1910.raw,'63');assert.equal(years.independent_votes,false);assert.equal(years.accepted_birth_date_revised,false);groups++;
  const ada=value(observed[5]);assert.equal(ada.date_literal,'86 19/8[?]');assert.equal(ada.date_selected,null);assert.equal('place' in ada,false);assert.equal('date' in ada,false);
  const adaF=value('F-P-0009-source_comparison-C0008-birth-reading');assert.equal(adaF.own_birth_date,'1886-08-19');assert.equal(adaF.own_birth_parish,'Lerbo');assert.equal(adaF.SCB_independent_of_original,false);assert.equal(adaF.Lerbo_written_in_child1915_record,false);groups++;
  const death=value(observed[6]);assert.equal('comparison_row10_field_filled' in death,false);assert.equal('initial_N_comparisons' in death,false);
  assert.equal(death.death,'1895-01-14');assert.equal(death.burial,'1895-01-25');assert.equal(death.note_corrected,'Liket hämtades till hemmet.');assert.equal(death.extra_note,'E 116');assert.equal(death.death_place_selected,null);assert.equal(death.medical_certificate_field,'blank');
  const controls=value('F-P-0368-source_assessment-C0559-control-rows');assert.deepEqual(controls.initial_N_comparisons,['rad2 Nils Peter Olsson','rad6 Nils Peter Simonsson']);assert.equal(controls.sanatorium_place_selected,null);groups++;
  const code=value(observed[7]);assert.deepEqual(code.occupationCodeReadings,['3-103-21','2-102-21']);assert.equal(code.occupationCode,null);assert.equal(code.occupationCodeChosen,null);assert.equal(code.arrivalFrom,'Värsås');assert.equal(code.schoolCode,'3');assert.equal(code.incomeWealthLiteral,'5 —');groups++;
  const stina=value(observed[8]);assert.equal('birthplace' in stina,false);assert.equal(stina.birth,'1813-09-17');assert.equal(stina.from_literal,'224');assert.equal(stina.vaccination,'v.');assert.equal(stina.individual_days_assigned_to_years,false);
  assert.equal(value('F-P-0344-source_scope-AI6-birthplace-transfer').AI7_reported_birthplace,'Sättna');groups++;
  assert.deepEqual(value(observed[9]),{birth_literal:'29 17/12',birth_parish:'Rönö',household:3});
  const car=value('F-M-C1013-Carolina-household-context');assert.equal(car.reported_spouse_name,'Nils Danielsson');assert.equal(car.spouse_name_record,'R-0910fc8b720c8388a94edf9f');assert.equal(car.rejected_identity_target,'P-0313');assert.equal(car.new_person_created,false);groups++;
  return groups;
}

// Read-only preparation gate; validates proposed data without applying it anywhere.
export function checkPreparedObservationA(db,prepared){
  const map=new Map(prepared.changes.map(x=>[x.id,x]));assert.equal(map.size,prepared.changes.length);
  assert.deepEqual(prepared.review.cases.map(c=>c.observation),observed);assert.equal(prepared.dependencyReviews.length,14);
  const lookup=id=>map.get(id)??readCurrent(db,id);
  let groups=semanticChecks(lookup);
  const done=new Set();
  for(const x of prepared.changes){
    const old=readCurrent(db,x.id);assert.equal(x.expectedVersion,old?.version??null);
    assert(!['person','identity_resolution','relation','record','source','mention'].includes(x.kind),'Utanför avgränsat ändringsmandat');
    const columns=db.prepare(`PRAGMA table_info(${x.kind})`).all().filter(c=>c.name!=='revision_id');
    for(const key of Object.keys(x.data))assert(columns.some(c=>c.name===key),`${x.id}.${key}`);
    for(const col of columns)if(col.notnull)assert(x.data[col.name]!=null,`${x.id}.${col.name}`);
    for(const o of x.origins)assert(db.prepare('SELECT 1 FROM unit WHERE id=?').get(o.unit),`Ursprung ${o.unit}`);
    for(const e of x.evidence){const planned=map.get(e.object);assert(!planned||done.has(e.object),`Beläggsordning ${x.id}→${e.object}`);assert.equal(e.version,planned?(planned.expectedVersion??0)+1:readCurrent(db,e.object)?.version);}
    if(x.kind==='observation'){const r=lookup(x.data.record_id);assert.equal(r.kind,'record');assert(x.evidence.some(e=>e.object===x.data.record_id));if(x.data.mention_id)assert(x.evidence.some(e=>e.object===x.data.mention_id));}
    if(unchangedDependents.includes(x.id)){const data={...db.prepare(`SELECT * FROM ${x.kind} WHERE revision_id=?`).get(old.revision_id)};delete data.revision_id;for(const k of Object.keys(data))if(k.endsWith('_json')&&data[k]!=null)data[k]=JSON.parse(data[k]);assert.equal(canonical(x.data),canonical(data));assert.equal(x.disposition,old.disposition);assert.equal(x.evidenceStatus,old.evidence_status);}
    done.add(x.id);
  }groups++;
  for(const d of prepared.unitDecisions){const before=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(d.unit);assert.equal(d.state,before.state);assert.equal(d.question,before.question);assert.equal(d.target,before.target_id);for(const r of db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=?').all(d.unit))assert(d.targets.includes(r.target_id));}groups++;
  assert.equal(map.get('ID-P-0313-not-C1013-Carolina').data.decision,'rejected');assert.equal(map.get('ID-P-0313-not-C1013-Carolina').evidenceStatus,'REJECTED');groups++;
  return {ok:true,groups,cases:10,changes:prepared.changes.length,unitDecisions:prepared.unitDecisions.length};
}

// For root's eventual isolated/native operation tests, after integration and apply.
export function checkT0663ObservationARisks(db){
  let groups=semanticChecks(id=>{const x=readCurrent(db,id);assert(x,`Saknat ${id}`);return x;});
  for(const id of observed){const now=readCurrent(db,id);assert.equal(now.version,2);const old=db.prepare('SELECT * FROM revision WHERE id=?').get(id+'@1');assert(old);assert.equal(now.evidence_status,old.evidence_status);assert.equal(now.disposition,old.disposition);}
  for(const id of unchangedDependents){const now=readCurrent(db,id);assert.equal(now.version,2);const prior=db.prepare(`SELECT * FROM ${now.kind} WHERE revision_id=?`).get(id+'@1');const current=db.prepare(`SELECT * FROM ${now.kind} WHERE revision_id=?`).get(now.revision_id);delete prior.revision_id;delete current.revision_id;assert.deepEqual(current,prior);const old=db.prepare('SELECT * FROM revision WHERE id=?').get(id+'@1');assert.equal(now.evidence_status,old.evidence_status);assert.equal(now.disposition,old.disposition);}
  groups++;
  assert.equal(decode(readCurrent(db,'O-P-0344-C0346-s94').value_json).birthplace,'Sättna');
  assert.equal(decode(readCurrent(db,'E-birth-P-0009').date_json).value,'1886-08-19');
  assert.equal(readCurrent(db,'ID-P-0313-not-C1013-Carolina').decision,'rejected');groups++;
  const comparisonByObservation={
    [observed[0]]:'F-P-0027-household_comparison-children-book-sequence',
    [observed[1]]:'F-P-0021-household_comparison-Bjerg-AI4-AI5',
    [observed[2]]:'F-P-0021-household_comparison-Bjerg-AI4-AI5',
    [observed[3]]:'F-P-0021-household_comparison-Bjerg-AI4-AI5',
    [observed[4]]:'F-P-0020-source_conflict-census1900-1910-birth-years',
    [observed[5]]:'F-P-0009-source_comparison-C0008-birth-reading',
    [observed[6]]:'F-P-0368-source_assessment-C0559-control-rows',
    [observed[8]]:'F-P-0344-source_scope-AI6-birthplace-transfer',
    [observed[9]]:'F-M-C1013-Carolina-household-context'
  };
  for(const [id,fact] of Object.entries(comparisonByObservation))for(const {unit_id} of db.prepare('SELECT unit_id FROM current_unit_target WHERE target_id=?').all(id)){
    const now=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(unit_id);
    assert(db.prepare('SELECT 1 FROM current_unit_target WHERE unit_id=? AND target_id=?').get(unit_id,fact),`${id}: jämförelse saknas för textenhet`);
    assert(now.previous_id,`${id}: versionsbeslut saknas`);
    const before=db.prepare('SELECT * FROM unit_decision WHERE id=?').get(now.previous_id);
    assert.equal(now.state,before.state);assert.equal(now.question,before.question);
    for(const {target_id} of db.prepare('SELECT target_id FROM unit_decision_target WHERE decision_id=?').all(before.id))assert(db.prepare('SELECT 1 FROM current_unit_target WHERE unit_id=? AND target_id=?').get(unit_id,target_id));
  }groups++;
  for(const row of db.prepare("SELECT object_id,kind FROM current_revision WHERE operation_id=(SELECT operation_id FROM current_revision WHERE object_id='O-P-0027-children-book-sequence')").all()){
    if(!observed.includes(row.object_id))continue;
    const now=readCurrent(db,row.object_id);for(const u of db.prepare('SELECT unit_id FROM current_unit_target WHERE target_id=?').all(row.object_id))assert(db.prepare('SELECT 1 FROM current_unit_decision WHERE unit_id=?').get(u.unit_id));
    for(const e of now.evidence){const b=db.prepare('SELECT object_id FROM revision WHERE id=?').get(e.basis_revision_id);assert.equal(readCurrent(db,b.object_id).revision_id,e.basis_revision_id);}
  }groups++;
  return {ok:true,groups};
}
