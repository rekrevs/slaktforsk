"""Exactly ten source-settled edge-version supersessions and immutable package renewal."""
import json,hashlib,copy,sqlite3
from pathlib import Path
B=Path('evaluations/T-0781');W=B/'implementation/ten-exact-current-record-support-version-supersessions-v1';assert not W.exists();W.mkdir();P=B/'implementation/complete-two-source-settled-draft-package-v3';assert not P.exists();P.mkdir()
def load(p):return json.loads(Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def save(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
sp=B/'source-review/ten-exact-current-record-support-version-amendments-v1.json';assert pin(sp)['sha256']=='a1ef23847dbaa6ba538229fbe5ab66e5ee05bbdc3a55ff087fd2b7e9c17e2e1e';s=load(sp);assert len(s['rows'])==10
prior=B/'implementation/complete-two-source-settled-draft-package-v2/complete-two-source-draft-package-proposal-v1.json';proposal=load(prior);oldmembership=load(proposal['membership_pin']['path']);oldtable=load(proposal['full_individual_consequence_table_pin']['path']);members=copy.deepcopy(proposal['operations']);groups={}
for r in s['rows']:
 pp=r['prior_operation_pin'];assert pin(Path(pp['path']))==pp;groups.setdefault(pp['path'],[]).append(r)
proof=[];replacements={}
for no,(path,rs) in enumerate(groups.items(),1):
 op=load(path);new=copy.deepcopy(op)
 for r in rs:
  i=int(r['consumer_pointer'].rsplit('/',1)[1]);assert op['changes'][i]==r['entire_before_candidate_API'];assert op['changes'][i]['id']==r['consumer_object_id'];j=r['edge_index'];assert op['changes'][i]['evidence'][j]==r['old_exact_API_edge']
  x=copy.deepcopy(op['changes'][i]);x['evidence'][j]=r['new_exact_API_edge'];assert x==r['entire_after_candidate_API'];assert set(r['old_exact_API_edge'])==set(r['new_exact_API_edge']);assert {k:v for k,v in r['old_exact_API_edge'].items() if k!='version'}=={k:v for k,v in r['new_exact_API_edge'].items() if k!='version'};assert r['old_exact_API_edge']['version']==1 and r['new_exact_API_edge']['version']==2;new['changes'][i]=x
 out=W/(str(no).zfill(2)+'-same-version-exact-current-support-operation-v1.json');np=save(out,new);replacements[path]=np;proof.append({'prior_operation_pin':pin(Path(path)),'renewed_operation_pin':np,'changed_targets':[r['consumer_object_id'] for r in rs],'source_pin':pin(sp),'source_row_pointers':['/rows/'+str(s['rows'].index(r)) for r in rs],'entire_after_APIs_equal_explicit_source_rows':True,'only_specified_ordered_edge_version_fields_change':True})
api_by_id={}
for m in members:
 oldpath=m['path']
 if oldpath in replacements:m.update(replacements[oldpath])
 op=load(m['path']);assert op['id']==m['operation_id']
 for t,a in zip(m['targets'],op['changes']):
  assert t['object_id']==a['id'];api_by_id[a['id']]=a;t['payload_sha256']=hashlib.sha256(json.dumps(a,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
  t['ordered_evidence_availability']=[{'exact_API_edge':e,'basis_revision_id':e['object']+'@'+str(e['version']),'available_before_target':True,'prior_baseline_or_earlier_producer':True} for e in a['evidence']]
  if a['id'] in {r['consumer_object_id'] for r in s['rows']}:t['explicit_current_record_support_version_amendment_pin']=pin(sp)
  if a['id'] in ['AUDIT-T0781-C0049-fullpost','AUDIT-T0781-C0067-fullpost']:t['explicit_audit_rationale_amendment_pin']=pin(B/'source-review/two-full-audit-final-status-rationale-metadata-amendments-v1.json')
c=sqlite3.connect('file:evaluations/T-0781/mechanical-current425-preparation-v1/baseline-j425.sqlite?mode=ro',uri=True);heads=dict(c.execute('select object_id,max(version) from revision group by object_id'));static=[]
for m in members:
 for i,a in enumerate(load(m['path'])['changes']):
  assert heads.get(a['id'])==a['expectedVersion'];edges=[]
  for e in a['evidence']:
   assert heads.get(e['object'])==e['version'],('Still stale current-head edge',a['id'],e,heads.get(e['object']));edges.append({'exact_edge':e,'actual_sequential_head':heads[e['object']]})
  static.append({'operation_index':m['index'],'change_index':i,'object_id':a['id'],'expected_current_version':a['expectedVersion'],'new_absence_or_existing_current_exact':True,'ordered_edge_current_heads':edges});heads[a['id']]=(a['expectedVersion'] or 0)+1
assert len(static)==174 and len(set(x['object_id'] for x in static))==174;c.close()
newmembership=copy.deepcopy(oldmembership);newmembership['operations']=members;newmembership['superseded_candidates']+= [{'pin':x['prior_operation_pin'],'reason':'Exact individually source-settled current-record support version amendment; historical candidate preserved and excluded.'} for x in proof];newmembership['strict_native_CLI_sequential_current_head_guard']=True;membershippin=save(P/'complete16-operation174-target-ordered-membership-v1.json',newmembership)
newtable=copy.deepcopy(oldtable);newtable['membership_pin']=membershippin
for r in newtable['rows']:
 oid=r['object_id'];r['entire_exact_after_API']=api_by_id[oid];m=next(x for x in members if any(t['object_id']==oid for t in x['targets']));r['operation_pin']={k:m[k] for k in ['path','sha256']};r['payload_sha256']=next(t['payload_sha256'] for t in m['targets'] if t['object_id']==oid);am=[x for x in s['rows'] if x['consumer_object_id']==oid]
 if am:r['explicit_source_current_record_support_version_amendment']={'source_pin':pin(sp),'source_pointer':'/rows/'+str(s['rows'].index(am[0])),'entire_exact_source_row':am[0]}
 if oid in ['AUDIT-T0781-C0049-fullpost','AUDIT-T0781-C0067-fullpost']:
  ap=B/'source-review/two-full-audit-final-status-rationale-metadata-amendments-v1.json';x=next(x for x in load(ap)['objects'] if x['object_id']==oid);r['source_metadata_amendment']={'source_pin':pin(ap),'entire_exact_source_row':x}
tablepin=save(P/'complete174-individual-full-API-consequence-and-source-disposition-table-v1.json',newtable)
proofpin=save(W/'ten-individual-exact-edge-API-supersession-and-all174-current-head-guard-proof-v1.json',{'source_spec_pin':pin(sp),'prior_package_pin':pin(prior),'operations':proof,'strict_all174_sequential_current_heads':static,'counts':{'amended_operations':len(proof),'amended_edges':10,'ordered_operations':16,'unique_targets':174},'source_or_native_semantic_changes_beyond_exact10_versions':False,'stage':'UNRUN'})
proposal['operations']=members;proposal['membership_pin']=membershippin;proposal['full_individual_consequence_table_pin']=tablepin;proposal['ten_current_record_support_version_amendment_pin']=pin(sp);proposal['ten_edge_supersession_and_static_CLI_head_proof_pin']=proofpin;proposal['prior_package_preserved_pin']=pin(prior);proposal['global_primary_exact_package_gate']='PENDING';proposal['global_independent_exact_pre_stage_gate']='PENDING';proposalpin=save(P/'complete-two-source-draft-package-proposal-v1.json',proposal);print(json.dumps({'proposal_pin':proposalpin,'membership_pin':membershippin,'table_pin':tablepin,'ten_edge_and174_CLI_head_proof_pin':proofpin},indent=2))
