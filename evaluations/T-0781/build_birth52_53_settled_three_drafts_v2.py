"""Source-approved three birth/EP revisions with exact guards, no runtime."""
import json,copy
from pathlib import Path
B=Path('evaluations/T-0781');parent=B/'build_settled_core_and_PATH98_drafts_v2.py';exec(compile(parent.read_text().split('assert W.exists();')[0],str(parent),'exec'));W=B/'implementation/birth52-53-settled-three-drafts-v1';assert W.exists() and not list(W.iterdir())
scope={};prep=B/'prepare_bounded_consequence_inputs_v1.py';exec(compile(prep.read_text().split('assert not W.exists();')[0],str(prep),'exec'),scope);c=scope['conn'](scope['BASE']);live=scope['conn'](scope['MAIN']);native=scope['native'];current=scope['current']
sp=B/'source-review/P0052-P0053-structured-birth-place-three-revision-and-one-retain-decisions-v1.json';assert pin(sp)['sha256']=='dd4b20552b49851b3a55d040c34ef65ed6e76360888c0a8258bc0217e2f460ac';s=load(sp);ip=load(s['input_pin']['path']);assert pin(Path(s['input_pin']['path']))==s['input_pin'];existing={}
for p in (B/'implementation').rglob('*draft-operation-v*.json'):
 for x in load(p)['changes']:existing.setdefault(x['id'],[]).append(pin(p))
rows=[];cs=[]
for x in s['objects']:
 oid=x['object_id'];rid=current(c,oid);n=native(c,rid);assert n==native(live,rid)==x['current'];assert not existing.get(oid)
 hs=[r[0] for r in c.execute('select id from revision where object_id=? order by version',(oid,))];edges=[]
 for h in hs:
  for e in c.execute('select rowid as native_edge_rowid,* from dependency where basis_revision_id=? order by rowid',(h,)):
   edge=dict(e);edges.append(edge)
   assert any(edge==a['edge'] for rr in ip['rows'] for a in rr['all_history_incoming']),('Unexpected incoming',oid,edge)
 if oid.startswith('EP-'):assert not edges
 old,new=revise({**x,'evidence_addition':None,'evidence_rebinds':[]},n)
 for rebind in x['evidence_rebinds']:
  i=rebind['ordered_index'];edge=n['evidence'][i];assert edge['basis_revision_id']==rebind['old_basis_revision_id'] and edge['role']==rebind['role'] and edge['note']==rebind['note'];obj,ver=rebind['new_basis_revision_id'].rsplit('@',1);new['evidence'][i]['object']=obj;new['evidence'][i]['version']=int(ver)
 for addition in x['evidence_additions']:
  obj,ver=addition['basis_revision_id'].rsplit('@',1);e={'object':obj,'version':int(ver),'role':addition['role'],'note':addition['note']};assert e not in new['evidence'];new['evidence'].append(e)
 expected_prefix=copy.deepcopy(old['evidence'])
 for rebind in x['evidence_rebinds']:
  i=rebind['ordered_index'];obj,ver=rebind['new_basis_revision_id'].rsplit('@',1);expected_prefix[i]['object']=obj;expected_prefix[i]['version']=int(ver)
 assert new['evidence'][:len(expected_prefix)]==expected_prefix
 cs.append(new);rows.append({'object_id':oid,'complete_current':n,'old_API':old,'new_API':new,'ordered_history_revision_ids':hs,'allhistory_incoming':edges,'source_explicit_incoming_dispositions':s['incoming_dispositions'],'source_row_pointer':'/objects/'+str(s['objects'].index(x)),'exact_edits':x['edits'],'explicit_ordered_rebinds':x['evidence_rebinds'],'explicit_ordered_additions':x['evidence_additions'],'retains':x['preserve'],'reason':x['reason'],'oldfields_and_fullcurrent_exact':True,'prior_draft_overlap':[]})
retains=[]
for r in s['retains']:
 n=native(c,r['current_revision_id']);assert n==ip['objects'][r['current_revision_id']]==native(live,r['current_revision_id']);retains.append({'full_current':n,'source_disposition':r})
op=operation(1,'P0052-P0053-structured-birth-place-three-revisions',cs,pin(sp));result=save('three-exact-revisions-and-one-retain-complete-guard-consequence-index-v1.json',{'task':'T-0781','operation_pin':op,'source_spec_pin':pin(sp),'rows':rows,'retains':retains,'source_execution_order':s['execution_order'],'scope_grade_not_inferred':True,'main425_pin':pin(scope['MAIN']),'stage':'UNRUN','canonical_apply':'UNRUN'});assert pin(scope['MAIN'])['sha256']=='efea4dfa8feec3f2f5bff8167792b01513ebb5689d9d2ec5278983a23ca208b3';c.close();live.close();print(json.dumps({'index_pin':result,'operation_pin':op},indent=2))
