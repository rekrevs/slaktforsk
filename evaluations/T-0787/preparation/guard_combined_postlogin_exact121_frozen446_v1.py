"""Bounded readonly121 guards/incoming; no operation, stage or MAIN connection."""
from pathlib import Path
import json,copy,importlib.util,traceback
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('proven',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
bp=R/'evaluations/T-0786/resume-current446-v1/baseline-j446.sqlite';assert h.sha(bp)=='1e8e6b4079df557d9dd904578178321381b6c2ef5d54ac15ff74eacdac942541';c=h.conn(bp);assert h.state(c)=={'journal_head':446,'pending':0}
files=[('fifteen-core-source-and-current-identity-copy-exact-fields-spec-v3.json','9b632920f0aaa6baf45981e1c0de7f0aed9b7d86a71e69e85e42effda7ca0b79'),('finite-necessary-current-copy-exact-fields-spec-v3.json','b8de718f1d474d486124897cb2483cefc977a5b6e5aed9be238af899b26ffe53')]
rows=[];sourcepins=[];callers={};incoming=[];historymap={};issues=[];headmap={};targetids=set();rawfields=0
try:
 for filename,digest in files:
  p=R/'evaluations/T-0787/source-review'/filename;assert h.sha(p)==digest;j=json.loads(p.read_text());sourcepins.append(h.pin(p))
  if 'source_core_order' in j:assert [v['object_id'] for v in j['rows']]==j['source_core_order']
  for i,v in enumerate(j['rows']):
   oid=v['object_id'];assert oid not in targetids;targetids.add(oid);rid=oid+'@'+str(v['expected_version']);assert h.current(c,oid)==rid;old=h.native(c,rid);assert old==v['whole_old_native'],('whole-old mismatch',oid)
   a=h.api(old);a['expectedVersion']=v['expected_version'];olda=copy.deepcopy(a)
   for f in v['field_edits']:
    target=a;keys=f['field'].split('.')
    for key in keys[:-1]:target=target[key]
    assert target[keys[-1]]==f['old'],('literal-old mismatch',oid,f['field']);target[keys[-1]]=copy.deepcopy(f['new']);rawfields+=1
   for reb in v.get('evidence_rebinds',[]):
    matches=[e for e in a['evidence'] if (e['object'],e['version'],e['role'])==(reb['basis_object_id'],reb['old_version'],reb['role'])];assert len(matches)==1,('zero/multiple rebind match',oid,reb);matches[0]['version']=reb['new_version']
   for e in v.get('evidence_additions',[]):
    assert not any((z['object'],z['version'],z['role'])==(e['object'],e['version'],e['role']) for z in a['evidence']);a['evidence'].append(copy.deepcopy(e))
   for e in a['evidence']:
    actual=headmap[e['object']] if e['object'] in headmap else int(h.current(c,e['object']).rsplit('@',1)[1])
    if actual!=e['version']:issues.append({'target':oid,'ordered_edge':e,'actual_current_basis_head_at_step':actual,'source_disposition_required':'No automatic current-basis rebind'})
   headmap[oid]=v['expected_version']+1
   hist=[z[0] for z in c.execute('select id from revision where object_id=? order by version',(oid,))];historymap[oid]=hist;edges=[]
   for basis in hist:
    for er in c.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(basis,)):
     edge=dict(er);n=h.native(c,edge['revision_id']);curr=h.current(c,n['object_id']);edge.update({'changed_target_object_id':oid,'target_current_revision_id':rid,'basis_is_current':basis==rid,'caller_current_revision_id':curr,'caller_is_current':curr==edge['revision_id']});edges.append(edge);incoming.append(edge);callers[n['id']]=n;callers[curr]=h.native(c,curr)
   rows.append({'spec_pin':h.pin(p),'spec_row_pointer':'/rows/'+str(i),'object_id':oid,'expected_version':v['expected_version'],'old_current_revision_id':rid,'full_old_native':old,'full_old_API':olda,'exact_new_fields_and_supports_NOT_OPERATION':a,'field_edits':v['field_edits'],'literal_guards_PASS':True,'whole_old_PASS':True,'source_disposition':v.get('source_disposition',v.get('individual_source_disposition')),'source_3011_addendum':v.get('source_disposition_3011_addendum',v.get('individual_source_disposition_3011_addendum')),'incoming_disposition':v['incoming_disposition'],'all_history_incoming_edges':edges,'source_individual_incoming_grades_required':bool(edges)})
 assert len(rows)==len(targetids)==121
 protected=json.loads((R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json').read_text())['objects'];assert len(protected)==42;assert not targetids.intersection(n['object_id'] for n in protected.values())
 absent={}
 for person in ['P0241','P0246']:
  for axis in ['IDENTITY-REVIEW','TREE-EFFECT']:
   oid=axis+'-T0787-'+person;absent[oid]={'object_absent':c.execute('select id from object where id=?',(oid,)).fetchone() is None,'history':list(c.execute('select id from revision where object_id=?',(oid,)))};assert absent[oid]['object_absent']
 examples={};axes={}
 for person in ['P-0241','P-0246','P-0003']:
  rr=[dict(z) for z in c.execute("select r.id,r.object_id,a.criteria from current_revision r join assessment a on a.revision_id=r.id where a.subject_id=? and a.criteria in ('identity_review/1','tree_effect/1') order by a.criteria",(person,))];axes[person]=rr
  for z in rr:examples[z['id']]={'full_native':h.native(c,z['id']),'schema_example_API':h.api(h.native(c,z['id']))}
 assert h.sha(bp)=='1e8e6b4079df557d9dd904578178321381b6c2ef5d54ac15ff74eacdac942541'
 pin=h.write(O/'combined121-postlogin-whole-old-fields-support-head-and-all-history-incoming-frozen446-guard-v1.json',{'task':'T-0787','source_spec_pins':sourcepins,'frozen_baseline_pin':h.pin(bp),'actual_frozen_state':h.state(c),'MAIN_not_opened':True,'fresh447_current_head_binding':'PENDING root actual1additive-search447 preservation proof, no sourcecredit from equality','rows':rows,'source_target_histories':historymap,'all_history_incoming':incoming,'full_exact_and_current_incoming_caller_native_payloads':callers,'sequential_current_basis_head_issues':issues,'counts':{'targets':121,'field_edits':rawfields,'all_history_incoming':len(incoming),'current_basis_incoming':sum(e['basis_is_current'] for e in incoming),'current_callers':sum(e['caller_is_current'] for e in incoming),'unique_caller_payloads':len(callers)},'four_suggested_new_review_ID_absence':absent,'existing_current_native_axis_locators':axes,'whole_native_and_API_schema_examples':examples,'media3011_API_pin':h.pin(R/'evaluations/T-0786/resume-current446-v1/actual-3011-stage-media-root-authorized-output-v1.json'),'schema_contract':'assessment data{subject_id,criteria,outcome,body}; identity_review/1 passed|failed; tree_effect/1 supporting|waiting|non_supporting; newexpectedVersion null, orderedorigins/evidence, operationnumericpolicy2; onlyAstra definesnewAPI/grade','operations_constructed':False,'stage_or_canonical_or_Wotan_mutation':False,'status':'GUARDS_PASS_PENDING_INDIVIDUAL_INCOMING_AND_FRESH447_BINDING' if not issues else 'SOURCE_HEAD_QUESTIONS_PRESERVED','usage':'UNKNOWN pending root collector'})
 print(json.dumps({'guard_pin':pin,'targets':121,'fields':rawfields,'incoming':len(incoming),'head_issues':len(issues)}))
except BaseException as e:
 h.write(O/'combined121-postlogin-guard-STOP-preserved-v1.json',{'error':repr(e),'traceback':traceback.format_exc(),'no_operation_build_or_MAIN_access':True});raise
finally:c.close()
