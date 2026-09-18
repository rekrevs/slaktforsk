import {identityGate} from './review.mjs';

// A derived view over current native revisions, never a second review register.
export function researchInventory(db){
 const people=db.prepare('SELECT c.object_id,p.display_name,p.legacy_state FROM current_revision c JOIN person p ON p.revision_id=c.id ORDER BY c.object_id').all();
 const rows=people.map(p=>{
  const gate=identityGate(db,p.object_id);
  const axis=key=>({outcome:gate[key].outcome,usable:gate[key].usable,source:gate[key].source,
   ...(gate[key].scope?{scope:gate[key].scope}:{}),revisions:gate[key].assessments.map(a=>a.revision_id)});
  return {id:p.object_id,name:p.display_name,legacy_state:p.legacy_state,disposition:gate.person.disposition,
   identityGate:gate.passed,identityReview:axis('identity_review'),treeEffect:axis('tree_effect'),lifePictureReview:axis('life_picture_review'),
   stopReasons:gate.reasons,assessmentQualifications:gate.other_assessments.filter(a=>!/^legacy_(theme\/|person_contract\/|source_path$|search_key$|profile_section\/)/.test(a.criteria)).map(a=>({id:a.object_id,revision:a.revision_id,outcome:a.outcome,body:a.body,caveat:a.caveat}))};
 });
 const active=rows.filter(r=>r.legacy_state!=='retired'&&r.disposition!=='retired');
 const count=list=>({persons:list.length,identityPassed:list.filter(r=>r.identityReview.usable&&r.identityReview.outcome==='passed').length,
  treeSupporting:list.filter(r=>r.treeEffect.usable&&r.treeEffect.outcome==='supporting').length,identityGatePassed:list.filter(r=>r.identityGate).length,
  explicitNativeLifePassed:list.filter(r=>r.lifePictureReview.usable&&r.lifePictureReview.source==='native'&&r.lifePictureReview.outcome==='passed').length,
  legacyContractPassed:list.filter(r=>r.lifePictureReview.usable&&r.lifePictureReview.source==='legacy_header'&&r.lifePictureReview.outcome==='passed').length});
 return {format:'genealogy2-research-inventory/1',note:'Registrerade aktuella bedömningar, inte ny sakgranskning eller utförandekö. Identitetsgrind och livsbild är separata. Äldre helkontraktsutfall behåller sitt ursprungliga omfång och sina kvalificeringar.',
  active:count(active),all:count(rows),legacyReferences:db.prepare('SELECT * FROM legacy_mapping ORDER BY id').all(),people:rows};
}
