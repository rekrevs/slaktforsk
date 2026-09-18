import assert from 'node:assert/strict';
import{readCurrent,personView}from'../lib/domain.mjs';
const data=(db,id)=>JSON.parse(readCurrent(db,id).value_json);
export function checkPersons09PartDRisks(db){
 const p=readCurrent(db,'P-0424');assert.equal(p.disposition,'accepted');assert.equal(p.legacy_state,'retired');assert.equal(p.sex,'male');
 assert.equal(readCurrent(db,'IDENTITY-P0424-P0028').decision,'different_people');
 assert.equal(JSON.parse(readCurrent(db,'E-birth-P-0424').date_json).value,'1861-05-16');
 assert.equal(JSON.parse(readCurrent(db,'E-baptism-P-0424').date_json).value,'1861-05-17');
 assert.equal(readCurrent(db,'E-birth-P-0424').place_id,null);
 assert.equal(data(db,'O-P-0424-C0050-own').number,48);
 assert.equal(data(db,'O-P-0424-C0050-own').father_literal,'Landtb. Joh. Peterson');
 const view=personView(db,'P-0424');assert.ok(view.research.questions.length>=2);
 assert.ok(view.research.questions.every(q=>!q.active&&q.disposition==='retired'));
 for(const id of ['ASSESSMENT-P-0424','P-0424/Q-01','P-0424/Q-02']){
  const now=readCurrent(db,id);assert.equal(now.version,2);assert.equal(now.disposition,'retired');
  const old=db.prepare(`select x.* from ${now.kind} x join revision r on r.id=x.revision_id where r.object_id=? and r.version=1`).get(id);
  assert.equal(now.body,old.body);assert.equal(now.outcome,old.outcome);
 }
 assert.equal(readCurrent(db,'BIO-P-0424').disposition,'recorded');
 const change=data(db,'F-P-0424-migration_date_conflict-445-to-243');assert.equal(change.sender_literal,'1878 8[5?]/12');assert.equal(change.receiver_literal,'1878-05-21');assert.equal(change.chosen_actual_move_date,null);
 assert.equal(data(db,'O-P-0424-C0055-own').departure_literal,'1878 8[5?]/12');
 assert.equal(data(db,'O-P-0424-C0057-own').arrival_literal,'1878 21/5');
 assert.equal(data(db,'O-P-0424-C0058-own').arrival_literal,'1879 29/11');
 assert.equal(readCurrent(db,'M-P-0424-C0057-own').name_literal,'Johan Aug.');
 assert.equal(data(db,'F-P-0424-name_form-own-records').own_Lundstrom_attestation,false);
 const scb=data(db,'F-P-0424-source_assessment-SCB1880-household-and-dependency');
 assert.equal(scb.independent_birth_evidence,false);assert.equal(scb.own_index_family_number,3);assert.equal(scb.index_family_number_is_original_household_number,false);assert.equal(scb.Backstrom_household_ends_above_own_row,true);assert.equal(scb.household_head_identified,false);assert.equal(scb.own_unfinished_block.length,3);assert.equal(scb.own_spouse_or_child_inferred,false);
 assert.equal(readCurrent(db,'O-P-0424-C0059-own').record_id,'R-442619fd8ec5fdc8d92b1f45');
 assert.equal(data(db,'O-P-0424-C0059-own').birthplace_literal,'d:o');
 const witnesses=db.prepare("select p.* from current_revision r join participation p on p.revision_id=r.id where p.event_id='E-baptism-P-0424' and p.role in ('witness','baptism_witness')").all();assert.equal(witnesses.length,6);
 assert.ok(witnesses.some(w=>w.mention_id==='M-C0050-Jon-Olsson-wife'));assert.ok(witnesses.some(w=>w.mention_id==='M-C0050-O-Dahl-wife'));
 for(const [id,role]of [['M-C0050-Jon-Olsson-wife','hustru'],['M-C0050-O-Dahl-wife','Hustru']]){assert.equal(readCurrent(db,id).name_literal,'');assert.equal(readCurrent(db,id).role_literal,role);assert.equal(readCurrent(db,id).version,2);}
 assert.equal(readCurrent(db,'M-C0050-O-Dahl').role_literal,'Nybygg.');assert.equal(readCurrent(db,'M-C0050-Erik-Dahl').role_literal,'');assert.equal(readCurrent(db,'M-C0050-Maja').role_literal,'Nybyttaren');
 for(const id of ['F-P-0080-civil_status-1861','F-P-0080-occupation-1861','F-P-0080-relationship_assessment-other_Dahl','F-P-0080-residence-1861','F-P-0081-relationship_assessment-other_Dahl','F-P-0081-residence-1861']){assert.equal(readCurrent(db,id).value_json,db.prepare('select value_json from fact where revision_id=?').get(id+'@1').value_json);}
 const network=data(db,'F-P-0424-source_assessment-baptism-network');assert.deepEqual(network.Jon_place_alternatives,['Gunnismark','Bullmark']);assert.equal(network.Drakfors_reading_rejected,true);assert.equal(network.churching_subject,'P-0059');assert.equal(network.kinship_inferred,false);
 assert.equal(readCurrent(db,'M-C0050-Strinnholm').record_id,'R-b099923e3f21b3ff681da8a9');assert.equal(readCurrent(db,'M-C0050-Strinnholm').role_literal,'');
 const half=data(db,'F-P-0424-family_context-paternal-half-sister');assert.equal(half.common_father,'P-0058');assert.equal(half.mother_identified,false);assert.equal(half.own_co_residence,false);assert.equal(half.reported_death,'1853-06-30');
 assert.equal(view.relations.filter(r=>r.relation_type==='parent'&&r.to_person==='P-0424').length,2);
 assert.equal(view.relations.filter(r=>['spouse','partner'].includes(r.relation_type)).length,0);
 assert.equal(view.relations.filter(r=>r.relation_type==='parent'&&r.from_person==='P-0424').length,0);
 assert.equal(view.events.filter(e=>['death','burial','marriage'].includes(e.event_type)).length,0);
 assert.equal(view.events.some(e=>e.object_id==='E-birth-P-0028'),false);
 return{ok:true,groups:7};
}
