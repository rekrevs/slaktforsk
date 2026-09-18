import {readCurrent} from './domain.mjs';

// These are assessment criteria, not person/evidence statuses. A replacement
// should revise the same object (or explicitly retire the previous assessment).
// Body, rationale, caveat, origins and versioned evidence remain mandatory
// context for the decision; this reader neither writes nor regrades them.
export const REVIEW_CRITERIA=Object.freeze({
  identity_review:Object.freeze({criteria:'identity_review/1',outcomes:Object.freeze(['passed','failed'])}),
  tree_effect:Object.freeze({criteria:'tree_effect/1',outcomes:Object.freeze(['supporting','waiting','non_supporting'])}),
  life_picture_review:Object.freeze({criteria:'life_picture_review/1',outcomes:Object.freeze(['passed','failed'])})
});
const legacyCriteria=new Set(['legacy_review_header','Befintlig person-research/v1; ursprungliga datum och kriterier i body']);
const labels={identity_review:'Identitetsgranskning',tree_effect:'Trädverkan',life_picture_review:'Kontraktsgranskning'};
const legacyValues={
  identity_review:{GODKÄND:'passed',UNDERKÄND:'failed','EJ GRANSKAD':'unreviewed'},
  tree_effect:{BÄRANDE:'supporting',AVVAKTAR:'waiting','EJ BÄRANDE':'non_supporting'},
  life_picture_review:{GODKÄND:'passed',UNDERKÄND:'failed','EJ GRANSKAD':'unreviewed'}
};
const issue=(code,axis,assessments,message)=>({code,axis,revision_ids:assessments.map(a=>a.revision_id),message});

function header(body) {
  const fields={};let fence=null;
  for(const [index,line] of body.split(/\r?\n/).entries()) {
    const marker=line.match(/^ {0,3}(`{3,}|~{3,})/);
    if(marker){if(!fence)fence=marker[1];else if(marker[1][0]===fence[0]&&marker[1].length>=fence.length)fence=null;continue;}
    if(fence)continue;
    // Only the preface's own header rows, never quoted examples, later sections,
    // title words, a PK table, or prose containing an old KLAR/GRANSKAD label.
    if(/^ {0,3}#{2,6}(?:\s|$)/.test(line))break;
    const match=line.match(/^- (Kontrakt|Person|Identitetsläge|Livsbildsläge|Identitetsgranskning|Trädverkan|Kontraktsgranskning):[ \t]*(.*?)[ \t]*$/);
    if(!match)continue;
    const raw=match[2],value=/^`[^`]+`$/.test(raw)?raw.slice(1,-1):raw;
    (fields[match[1]]??=[]).push({line:index+1,raw,value});
  }
  return fields;
}

function validity(db,assessment,axis) {
  const problems=[];
  if(!['recorded','accepted'].includes(assessment.disposition))problems.push(issue('assessment_disposition',axis,[assessment],`Bedömningen är ${assessment.disposition}; inget giltigt granskningsutfall kan tillgodoräknas.`));
  if(['CONFLICT','REJECTED'].includes(assessment.evidence_status))problems.push(issue('assessment_evidence_conflict',axis,[assessment],`Bedömningen är märkt ${assessment.evidence_status}.`));
  if(assessment.pending_reviews.length)problems.push(issue('assessment_pending',axis,[assessment],'Bedömningen väntar på dokumenterad omprövning.'));
  const stale=assessment.evidence.filter(e=>['supports','derived_from'].includes(e.role)).filter(e=>{
    const basis=db.prepare('SELECT object_id FROM revision WHERE id=?').get(e.basis_revision_id);
    return !basis||db.prepare('SELECT id FROM current_revision WHERE object_id=?').get(basis.object_id)?.id!==e.basis_revision_id;
  });
  if(stale.length)problems.push({...issue('assessment_basis_revised',axis,[assessment],'Bedömningen åberopar ersatt underlag; en uttrycklig aktuell omprövning behövs.'),basis_revision_ids:stale.map(e=>e.basis_revision_id)});
  return problems;
}

function selectAxis(db,personId,axis,all,legacy) {
  const native=all.filter(a=>a.criteria===REVIEW_CRITERIA[axis].criteria);
  // Even an unusable native criterion is an explicit decision to handle: an
  // older positive header must not silently revive it. Retired competitors are
  // kept visible but do not compete with one active replacement.
  const pool=native.length?native:legacy,active=pool.filter(a=>a.disposition!=='retired');
  const selected=active.length?active:pool;
  const result={source:native.length?'native':legacy.length?'legacy_header':'missing',
    criteria:REVIEW_CRITERIA[axis].criteria,outcome:null,usable:false,
    assessments:selected,ignored_assessments:pool.filter(a=>!selected.includes(a)),fields:[],issues:[]};
  if(native.length)result.ignored_assessments.push(...legacy);
  if(axis==='life_picture_review')result.scope=native.length?'life_picture':'legacy_full_contract';
  if(!selected.length){result.issues.push(issue('assessment_missing',axis,[],`Uttrycklig bedömning för ${labels[axis]} saknas.`));return result;}
  if(selected.length!==1){result.issues.push(issue('assessment_conflict',axis,selected,`Flera aktuella bedömningar konkurrerar om ${labels[axis]}; datum eller objekt-id avgör inte företrädet.`));return result;}
  const assessment=selected[0];
  result.issues.push(...validity(db,assessment,axis));
  if(native.length) {
    if(REVIEW_CRITERIA[axis].outcomes.includes(assessment.outcome))result.outcome=assessment.outcome;
    else result.issues.push(issue('assessment_outcome_invalid',axis,[assessment],`Okänt utfall för ${result.criteria}: ${assessment.outcome}.`));
  } else {
    const fields=header(assessment.body),rows=fields[labels[axis]]??[];
    result.fields=rows;result.header_fields=fields;
    if(rows.length!==1)result.issues.push(issue(rows.length?'header_conflict':'header_missing',axis,[assessment],`Bedömningshuvudet kräver exakt en rad för ${labels[axis]}; ${rows.length} finns.`));
    else if(Object.hasOwn(legacyValues[axis],rows[0].value))result.outcome=legacyValues[axis][rows[0].value];
    else result.issues.push(issue('header_outcome_invalid',axis,[assessment],`Okänt eller kvalificerat rubrikutfall för ${labels[axis]}: ${rows[0].raw}.`));
    for(const [label,expected] of [['Person',personId],['Kontrakt','person-research/v1']]) {
      const context=fields[label]??[];
      if(context.length&&(context.length!==1||context[0].value!==expected))result.issues.push(issue('header_context_conflict',axis,[assessment],`Bedömningshuvudets ${label} motsäger dess ämne eller kontrakt.`));
    }
    const states=fields.Identitetsläge??[];
    if(axis==='tree_effect'&&result.outcome==='supporting'&&states.length&&(states.length!==1||states[0].value!=='PRÖVAT'))result.issues.push(issue('header_identity_state_conflict',axis,[assessment],'BÄRANDE motsägs av bedömningshuvudets identitetsläge; ingen passerad grind härleds.'));
  }
  result.usable=result.issues.length===0;
  return result;
}

/** Read-only person-contract identity gate; not a life-picture approval or a
 * proof of particular parent edges. Only current revision heads are read.
 * Native criteria override legacy headers separately per axis. A pending
 * aggregate legacy header blocks its identity/tree use because its unresolved
 * review cannot be safely allocated to the life level by text heuristics.
 * Legacy Kontraktsgranskning is reported as a full-contract result, never
 * rebranded as an independent native life-picture approval. Other assessments
 * remain visible as qualifications; free prose is not interpreted as a gate.
 */
export function identityGate(db,personId) {
  if(typeof personId!=='string'||!personId.trim())throw TypeError('Person-id krävs för identitetsgrinden');
  const person=readCurrent(db,personId);
  const all=db.prepare('SELECT r.object_id FROM current_revision r JOIN assessment a ON a.revision_id=r.id WHERE a.subject_id=? ORDER BY r.object_id').all(personId).map(row=>readCurrent(db,row.object_id));
  const legacy=all.filter(a=>legacyCriteria.has(a.criteria));
  const axes=Object.fromEntries(Object.keys(REVIEW_CRITERIA).map(axis=>[axis,selectAxis(db,personId,axis,all,legacy)]));
  const reasons=[];
  if(person?.kind!=='person')reasons.push(issue('person_missing','person',[],'Aktuell personidentitet saknas.'));
  else {
    if(person.disposition!=='accepted'||person.legacy_state==='retired')reasons.push(issue('person_not_accepted','person',[person],'Personidentiteten är inte aktuell och accepterad.'));
    if(person.pending_reviews.length)reasons.push(issue('person_pending','person',[person],'Personidentiteten väntar på dokumenterad omprövning.'));
  }
  for(const [axis,required] of [['identity_review','passed'],['tree_effect','supporting']]) {
    const assessment=axes[axis];reasons.push(...assessment.issues);
    if(assessment.usable&&assessment.outcome!==required)reasons.push(issue('gate_outcome_not_supporting',axis,assessment.assessments,`${labels[axis]} är ${assessment.outcome}; grinden kräver ${required}.`));
  }
  const used=new Map();
  const register=(o,role)=>{if(!o)return;const r=used.get(o.revision_id)??{object_id:o.object_id,revision_id:o.revision_id,version:o.version,roles:[]};r.roles.push(role);used.set(o.revision_id,r);};
  register(person,'person');
  for(const [axis,data] of Object.entries(axes))for(const a of data.assessments)register(a,axis);
  const relevant=new Set([...legacy,...all.filter(a=>Object.values(REVIEW_CRITERIA).some(v=>v.criteria===a.criteria))].map(a=>a.object_id));
  return {person_id:personId,criteria:'identity_gate/1',passed:reasons.length===0,status:reasons.length?'blocked':'passed',reasons,
    explanation:reasons.length?'Identitetsgrinden stoppas av de uttryckliga skälen; detta ändrar ingen person, ägarkunskap eller relation.':'Godkänd identitetsgranskning och bärande trädverkan är uttryckligen registrerade. Livsbildens utfall är separat.',
    person,...axes,used_revisions:[...used.values()],other_assessments:all.filter(a=>!relevant.has(a.object_id))};
}
