"""Bounded mechanical draft after two exact comparison-input approvals.
Never apply/clone; source literal_resolutions copied without inference.
"""
from pathlib import Path
import hashlib,json,importlib.util,time
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0790/preparation';S=O/'reviewed-stage-v1';start=time.monotonic()
lib=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';assert hashlib.sha256(lib.read_bytes()).hexdigest()=='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2';sp=importlib.util.spec_from_file_location('h',lib);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def load(rel,digest=None):
 p=R/rel
 if digest:assert h.sha(p)==digest
 return p,json.loads(p.read_text())
sourcep,source=load('evaluations/T-0790/source-review/actual-nine-dependencies-own-freeze-v1.json','9a1faece0dd3b3ad0ca589069a60733a635151eecf0408f57018974ce9a9abea');indep,ind=load('evaluations/T-0790/independent-review/actual-nine-own-freeze-v1.json','7b9655e3ccf7814ae0c7fd7dc14b1328f4973b97ffcb58b0a0b167fe4137ff77')
scp,sc=load('evaluations/T-0790/source-review/actual-nine-comparison-and-draft-release-v1.json','ab9f35b82d6cb1fef1afae9bc8998d215d74795b2b02c2ff75c19c7624d8cbc1');icp,ic=load('evaluations/T-0790/independent-review/actual-nine-comparison-v1.json','b157fb53525c18a9aefcbe7e5d6a821c354896cfd0c12f8743e66f12eedfe31b');assert sc['source_approved_for_literal_draft'] is True and ic['primary_literal_resolutions_approved_as_draft_input'] is True
assert sc['literal_resolutions']==source['literal_resolutions']==ic['approved_literal_resolutions'] and source['new_native_mutations']==[]
result=json.loads((S/'result.json').read_text());assert result['actual_state']=={'journal_head':455,'pending':9};assert h.sha(R/result['stage_db']['path'])==result['stage_db']['sha256'];c=h.conn(R/result['stage_db']['path']);assert h.state(c)==result['actual_state']
ctxp=S/'actual-requests-full-context.json';ctx=json.loads(ctxp.read_text());actual=[dict(q) for q in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')];assert actual==ctx['requests'];ids=[q['id'] for q in actual];literal=source['literal_resolutions'];assert [x['request'] for x in literal]==ids and len(ids)==9
bs=json.loads((O/'baseline-state.json').read_text());assert h.sha(R/'genealogy2/data/research.sqlite')==bs['main']['sha256'];rows=[]
for q,resolve,sd,di in zip(actual,literal,source['individual_decisions'],ind['individual_decisions']):
 assert q['id']==resolve['request']==sd['request_id']==di['id'] and sd['affected_revision']==q['affected_revision_id'] and di['affected_revision_id']==q['affected_revision_id'];assert not sd['mutation_required'] and not di['requires_new_affected_revision'] and not di['requires_evidence_rebind']
 affected=ctx['objects'][q['affected_revision_id']];current=h.current(c,affected['object_id']);assert current==q['affected_revision_id'];affected_current=ctx['objects'][current]
 assert affected==affected_current
 oldbasis=[{'edge':e,'full_basis_native':ctx['objects'][e['basis_revision_id']]} for e in affected['evidence']]
 rows.append({'actual_request':q,'affected_exact_native':affected,'affected_current_revision':current,'affected_current_native':affected_current,'changed_exact_native':ctx['objects'][q['changed_revision_id']],'unchanged_historical_basis_and_order':oldbasis,'source_individual_decision':sd,'independent_individual_decision':di,'literal_resolution':resolve,'mutation_or_rebind':False})
out=O/'exact-nine-request-only-resolution-draft-v1';assert not out.exists();out.mkdir()
op={'id':'T0790-nine-individual-dependency-resolutions-v1','actor':'Codex/Sol-literal-two-Astra-decisions','reason':'T-0790 AC3/5: nio faktiska individuellt source/independent-prövade beroendeomprövningar efter kolumn9-statusrättelse; exakt affectednative och historiska stödkanter behålls utan rebind. Inga nya original eller kataloger.','dependencyReviewVersion':2,'changes':[],'resolve':literal}
op_pin=h.write(out/'resolve-literal.json',op)
first=json.loads((O/'materialized-source-v3-literal-v1/mechanical-validation-result.json').read_text())['operation_pin'];membership={'operations':[dict(first,operation_id='T0790-existing-material-life-six-v1'),dict(op_pin,operation_id=op['id'])],'first_stage_pin':result['stage_db'],'first_stage_state':result['actual_state'],'planned_final_state':{'journal_head':456,'pending':0},'same_stage_only':True}
table_pin=h.write(out/'nine-individual-resolution-table.json',{'resolution_operation_pin':op_pin,'actual_request_context_pin':h.pin(ctxp),'source_own_pin':h.pin(sourcep),'independent_own_pin':h.pin(indep),'source_comparison_input_gate_pin':h.pin(scp),'independent_comparison_input_gate_pin':h.pin(icp),'individual_rows':rows,'two_operation_membership':membership,'no_native_changes_or_rebind':True})
h.write(out/'mechanical-result.json',{'resolver_operation_pin':op_pin,'resolution_table_pin':table_pin,'membership':membership,'actual9IDs_order_exact':True,'literal_resolution_list_exact_two_Astra_inputgates':True,'no_runtime_apply':True,'final_literal_operation_table_two_Astra_gates_required':True,'elapsed_monotonic_seconds':time.monotonic()-start});assert h.sha(R/'genealogy2/data/research.sqlite')==bs['main']['sha256'];print(json.dumps({'operation':op_pin,'table':table_pin,'elapsed':time.monotonic()-start}));c.close()
