"""Readonly exact8 source copies and incoming; no operation or runtime mutation."""
from pathlib import Path
import json,copy,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
pp=O/'fresh447-physical-backup-full50-logical-equality-and-protected42-proof-v1.json';assert h.sha(pp)=='b26805071faa41f0d5abf982b87c80202831a058a378890c7425b540e095161c';proof=json.loads(pp.read_text());bp=R/proof['baseline_pin']['path'];assert h.sha(bp)==proof['baseline_pin']['sha256'];c=h.conn(bp)
p=R/'evaluations/T-0787/source-review/eight-direct-incoming-small-current-copy-exact-source-spec-v1.json';assert h.sha(p)=='73d8dfc884f75a6c1bc591dd8eb322880f47fccc8c3f86b51f10f0ecd5ff7ee4';j=json.loads(p.read_text());assert len(j['rows'])==8
prior=O/'latest125-field-reconstruction-absent-review-ordered-support-head-guards-NOT-OPERATIONS-v2.json';assert h.sha(prior)=='2207109bdffc073d0eafe07af2dcdd2d1f6f1a6826897781efd1d032a3e08f8c';old=json.loads(prior.read_text());heads={r['object_id']:(r['full_old_native']['version']+1 if r['full_old_native'] else 1) for r in old['rows']};priorids=set(heads);rows=[];incoming=[];callers={};issues=[];targets=set()
for i,v in enumerate(j['rows']):
 oid=v['object_id'];assert oid not in priorids and oid not in targets;targets.add(oid);rid=oid+'@'+str(v['expected_version']);assert h.current(c,oid)==rid;n=h.native(c,rid);assert n==v['whole_old_native'];a=h.api(n);a['expectedVersion']=v['expected_version'];before=copy.deepcopy(a)
 for f in v['field_edits']:
  target=a;keys=f['field'].split('.')
  for key in keys[:-1]:target=target[key]
  assert target[keys[-1]]==f['old'],(oid,f['field']);target[keys[-1]]=copy.deepcopy(f['new'])
 for rb in v.get('evidence_rebinds',[]):
  matches=[idx for idx,e in enumerate(a['evidence']) if e==rb['old']];assert len(matches)==1;assert rb['old']['object']==rb['new']['object'] and rb['old']['role']==rb['new']['role'] and rb['old']['note']==rb['new']['note'];a['evidence'][matches[0]]=copy.deepcopy(rb['new'])
 for e in v.get('evidence_additions',[]):
  assert not any((e['object'],e['version'],e['role'])==(z['object'],z['version'],z['role']) for z in a['evidence']);a['evidence'].append(copy.deepcopy(e))
 for e in a['evidence']:
  actual=heads.get(e['object']);actual=actual if actual is not None else int(h.current(c,e['object']).rsplit('@',1)[1])
  if actual!=e['version']:issues.append({'target':oid,'edge':e,'actual_current_basis_head_at_step':actual,'required_source_disposition':'No automatic rebind'})
 heads[oid]=v['expected_version']+1;history=[z[0] for z in c.execute('select id from revision where object_id=? order by version',(oid,))];edges=[]
 for basis in history:
  for er in c.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(basis,)):
   e=dict(er);cn=h.native(c,e['revision_id']);curr=h.current(c,cn['object_id']);e.update({'changed_target_object_id':oid,'target_current_revision_id':rid,'basis_is_current':basis==rid,'caller_current_revision_id':curr,'caller_is_current':curr==e['revision_id']});edges.append(e);incoming.append(e);callers[cn['id']]=cn;callers[curr]=h.native(c,curr)
 rows.append({'source_row_pointer':'/rows/'+str(i),'object_id':oid,'current_revision_id':rid,'full_old_native':n,'full_old_API':before,'exact_new_API_NOT_OPERATION':a,'whole_old_and_fields_exact':True,'individual_source_disposition':v['individual_source_disposition'],'incoming_disposition':v['incoming_disposition'],'history':history,'all_history_incoming':edges})
assert h.sha(bp)==proof['baseline_pin']['sha256'];out=h.write(O/'eight-direct-copy-whole-old-field-support-order-and-all-history-incoming-guards-NOT-OPERATIONS-v2.json',{'task':'T-0787','source_spec_pin':h.pin(p),'baseline_proof_pin':h.pin(pp),'baseline_state':h.state(c),'prior125_guard_pin':h.pin(prior),'eight_targets_disjoint_prior125':True,'rows':rows,'all_history_incoming':incoming,'full_exact_and_current_incoming_callers':callers,'sequential_current_basis_head_issues':issues,'counts':{'newly_proposed_existing_targets':8,'total_existing_revisions_union':129,'total_including_four_new_reviews':133,'all_history_incoming':len(incoming),'caller_native':len(callers),'head_issues':len(issues)},'initial125issues_retained_not_automatically_resolved':True,'no_operation_stage_canonical_Wotan_mutation':True,'status':'GUARDS_PASS_PENDING_INDIVIDUAL_NEW_INCOMING_SOURCE_DISPOSITIONS' if not issues else 'STOP_SOURCE_HEAD_QUESTIONS','usage':'UNKNOWN pending root collector'});print(json.dumps({'guard_pin':out,'incoming':len(incoming),'head_issues':issues}));c.close()
