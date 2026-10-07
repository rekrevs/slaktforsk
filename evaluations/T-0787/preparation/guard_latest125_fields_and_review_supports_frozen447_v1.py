"""Exact source-settled125 reconstruction guards; not operations, no MAIN connection."""
from pathlib import Path
import json,copy,importlib.util,traceback
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
proofp=O/'fresh447-physical-backup-full50-logical-equality-and-protected42-proof-v1.json';assert h.sha(proofp)=='b26805071faa41f0d5abf982b87c80202831a058a378890c7425b540e095161c';proof=json.loads(proofp.read_text());bp=R/proof['baseline_pin']['path'];assert h.sha(bp)==proof['baseline_pin']['sha256'];c=h.conn(bp);assert h.state(c)=={'journal_head':447,'pending':0}
files=[('fifteen-core-source-and-current-identity-copy-exact-fields-spec-v5.json','928f6d760a530500661fb9125a32e69c8813e45489f6f3d8e12195ade1340b58'),('finite-necessary-current-copy-exact-fields-spec-v4.json','8d31b0f2486ac69a031511a8347b1d031db486472d9ba062561529f84ffef0e7')]
rows=[];pins=[];headmap={};issues=[];ids=set();supportnative={};formats=[]
try:
 for fn,digest in files:
  p=R/'evaluations/T-0787/source-review'/fn;assert h.sha(p)==digest;j=json.loads(p.read_text());pins.append(h.pin(p))
  if 'source_core_order' in j:assert [x['object_id'] for x in j['rows']]==j['source_core_order']
  for i,v in enumerate(j['rows']):
   oid=v['object_id'];assert oid not in ids;ids.add(oid);rid=oid+'@'+str(v['expected_version']);assert h.current(c,oid)==rid;n=h.native(c,rid);assert n==v['whole_old_native'];a=h.api(n);a['expectedVersion']=v['expected_version'];olda=copy.deepcopy(a)
   for f in v['field_edits']:
    target=a;keys=f['field'].split('.')
    for key in keys[:-1]:target=target[key]
    assert target[keys[-1]]==f['old'],(oid,f['field']);target[keys[-1]]=copy.deepcopy(f['new'])
    if 'native_old_literal_preserved' in f or 'native_new_literal_preserved' in f:formats.append({'object_id':oid,'field':f,'API_old_exact':True,'explicit_source_projection_used':True})
   for reb in v.get('evidence_rebinds',[]):
    matches=[e for e in a['evidence'] if (e['object'],e['version'],e['role'])==(reb['basis_object_id'],reb['old_version'],reb['role'])];assert len(matches)==1,('zero/multiple explicit rebind',oid,reb);matches[0]['version']=reb['new_version']
   for e in v.get('evidence_additions',[]):
    assert not any((z['object'],z['version'],z['role'])==(e['object'],e['version'],e['role']) for z in a['evidence']);a['evidence'].append(copy.deepcopy(e))
   for e in a['evidence']:
    actual=headmap[e['object']] if e['object'] in headmap else int(h.current(c,e['object']).rsplit('@',1)[1])
    if actual!=e['version']:issues.append({'target':oid,'edge':e,'actual_current_basis_head_at_step':actual,'required_source_disposition':'No automatic rebind'})
    elif e['object'] not in headmap:supportnative[e['object']+'@'+str(e['version'])]=h.native(c,e['object']+'@'+str(e['version']))
   headmap[oid]=v['expected_version']+1
   rows.append({'source_spec_pin':h.pin(p),'source_row_pointer':'/rows/'+str(i),'object_id':oid,'current_revision_id':rid,'full_old_native':n,'full_old_API':olda,'settled_new_API_reconstruction_NOT_OPERATION':a,'literal_fields_exact':True,'whole_old_exact':True,'source_disposition':v.get('source_disposition',v.get('individual_source_disposition')),'incoming_disposition':v['incoming_disposition']})
 p=R/'evaluations/T-0787/source-review/four-new-individual-identity-and-tree-full-API-source-spec-v1.json';assert h.sha(p)=='9cd8bad6845045f8d328ee4b6a067ca1b589541fe26c54baa9a126992ff22be9';j=json.loads(p.read_text());pins.append(h.pin(p));assert len(j['rows'])==4
 for i,v in enumerate(j['rows']):
  a=v['full_new_API'];oid=a['id'];assert oid not in ids;ids.add(oid);assert a['expectedVersion'] is None and a['kind']=='assessment';assert not c.execute('select id from object where id=?',(oid,)).fetchone();assert set(a['data'])=={'subject_id','criteria','outcome','body'};assert c.execute('select kind from object where id=?',(a['data']['subject_id'],)).fetchone()[0]=='person'
  assert a['data']['criteria'] in ['identity_review/1','tree_effect/1'];assert a['data']['outcome'] in ({'passed','failed'} if a['data']['criteria']=='identity_review/1' else {'supporting','waiting','non_supporting'})
  for e in a['evidence']:
   actual=headmap.get(e['object']);actual=actual if actual is not None else int(h.current(c,e['object']).rsplit('@',1)[1])
   if actual!=e['version']:issues.append({'target':oid,'edge':e,'actual_current_basis_head_at_step':actual,'required_source_disposition':'No automatic rebind'})
   elif e['object'] not in headmap:supportnative[e['object']+'@'+str(e['version'])]=h.native(c,e['object']+'@'+str(e['version']))
  headmap[oid]=1;rows.append({'source_spec_pin':h.pin(p),'source_row_pointer':'/rows/'+str(i),'object_id':oid,'full_old_native':None,'expected_absent_exact':True,'full_new_API_NOT_OPERATION':a,'individual_source_disposition':v['source_rows'],'incoming_disposition':v['incoming_disposition']})
 assert len(ids)==125
 previous=O/'exact121-current447-wholeold-native-API-field-sides-and-all-history-incoming-v1.json';assert h.sha(previous)=='748e57edbbbb4aace6ff4d8cc4d2e8e6a12a254cb68419eef2977cc014c39c3a';oldinput=json.loads(previous.read_text());oldmap={x['object_id']:x['full_old_native'] for x in oldinput['rows']};assert all(oldmap[r['object_id']]==r['full_old_native'] for r in rows[:121]);assert h.sha(bp)==proof['baseline_pin']['sha256']
 ap=R/'evaluations/T-0787/source-review/exact-five-structured-field-and-core-rule-additive-format-amendment-v1.json';assert h.sha(ap)=='e031af01850c29fb86a0ab4679bc52b6ffed26ffe3193e0bd42abd22187f8cb0'
 out=h.write(O/'latest125-field-reconstruction-absent-review-ordered-support-head-guards-NOT-OPERATIONS-v1.json',{'task':'T-0787','source_spec_pins':pins,'explicit_API_projection_source_amendment_pin':h.pin(ap),'frozen447_backup_proof_pin':h.pin(proofp),'baseline_pin':h.pin(bp),'rows':rows,'unchanged121_whole_old_to_prior_guard':True,'prior_full_incoming_input_pin':h.pin(previous),'exact65incoming_credit':'Unchanged nativeold/head references only; individual source65grades still required','baseline_existing_support_fullnative':supportnative,'sequential_current_basis_head_issues':issues,'source_required_order':['core15 ordered source_core_order','copy106 current spec rows','four native review APIs explicit source row order'],'counts':{'targets':125,'existing_revisions':121,'new_review_objects':4,'support_head_issues':len(issues)},'protected42_intersection':'No protectedtarget alteration; new reviewers are new axis objects, oldprotected retained','no_operations_stage_canonical_or_Wotan_mutation':True,'status':'GUARDS_PASS_PENDING_65_INDIVIDUAL_SOURCE_DISPOSITIONS_3011_ADOPTION_AND_ROOT_RELEASE' if not issues else 'STOP_SOURCE_SUPPORT_HEAD_QUESTIONS','usage':'UNKNOWN pending root collector'})
 print(json.dumps({'guard_pin':out,'targets':125,'support_head_issues':issues}))
except BaseException as e:
 h.write(O/'latest125-guard-STOP-preserved-v1.json',{'error':repr(e),'traceback':traceback.format_exc(),'no_operation_or_MAIN_access':True});raise
finally:c.close()
