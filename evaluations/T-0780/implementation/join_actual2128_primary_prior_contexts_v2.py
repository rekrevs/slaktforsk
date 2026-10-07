"""Exact actual request IDs to saved primary individual contexts, no source grading."""
import datetime,hashlib,json
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/actual2128-readonly-preparation-v1';S=B/'full10-stage-final143-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(s):return str(s).replace('~','~0').replace('/','~1')
def save(n,x):
 p=W/n.replace('-v1.json','-v2.json');assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+esc(k))
 elif isinstance(x,list):
  for i,v in enumerate(x):
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+str(i))
def rid(x):
 if isinstance(x,str):return x if '@' in x else None
 if not isinstance(x,dict):return None
 for key in ['revision_id','revision','id','object_id','object_revision','current_revision']:
  value=x.get(key)
  if isinstance(value,str):
   if '@' in value:return value
   version=x.get('version',x.get('native_version',x.get('expectedVersion',x.get('expected_current_version'))))
   if isinstance(version,int):return value+'@'+str(version)
 for key in ['object','current','current_full_native','full_current','current_revision','referencer_current','retained_full_native','prospective_full','full_native']:
  if isinstance(x.get(key),dict):
   r=rid(x[key])
   if r:return r
 return None
def diff(a,b,path=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append({'field':path+'/'+k,'old_present':k in a,'new_present':k in b,'old':a.get(k),'new':b.get(k)})
   else:out.extend(diff(a[k],b[k],path+'/'+k))
  return out
 return [{'field':path,'old':a,'new':b,'array_order_preserved':True}]
def semantic(n):
 d={k:v for k,v in n['data'].items() if k!='revision_id'}
 for k,v in d.items():
  if k.endswith('_json') and isinstance(v,str):d[k]=json.loads(v)
 return {'data':d,'caveat':n['caveat']}
RP=S/'actual-handoff-v1/all-actual-pending-individual-request-routing-v1.json';reqs=load(RP)['requests']
NP=W/'all893-full-actual-native-targets-in-journal-insertion-order-v1.json';actual=load(NP)['objects']
BP=W/'all-existing-actual-request-support-full-baseline-native-payloads-v1.json';baseline=load(BP)['objects'];native={**baseline,**actual}
for k,v in load(W/'all-previous-native-target-payloads-stage-before-equality-v1.json')['objects'].items():native.setdefault(k,v)
affected={x['actual_request']['affected_revision_id'] for x in reqs}|{x['affected_latest_current_revision_id'] for x in reqs};oids={x.rsplit('@',1)[0] for x in affected}
CP=B/'implementation/five-expanded-exactnative-pointer-join-v2/deduplicated-full-source-decision-contexts-v1.json';contexts=load(CP)['contexts']
# Reuse exact preserved context index, plus only newer explicit source files needed by current gate.
gatepath=B/'source-review/all10-global-primary-source-ready-gate-v6.json';gate=load(gatepath)
newpaths=set()
for p in gate['operations']:
 op=load(p['path']);reason=op.get('reason','')
 for q in (B/'source-review').glob('resumed-*.json'):
  if sha(q) in reason:newpaths.add(q)
newpaths.update((B/'source-review').glob('*dependency*decisions*.json'))
newpaths.update((B/'source-review').glob('*incoming*dispositions*.json'))
newpaths.update((B/'source-review').glob('*R1-dependency-dispositions*.json'))
newpaths.update((B/'source-review').glob('*event-dependency-dispositions*.json'))
known={(x['source_pin']['path'],x['json_pointer']) for x in contexts.values()}
for p in sorted(newpaths):
 sp=pin(p)
 for ptr,x in walk(load(p)):
  if not isinstance(x,dict) or (str(p),ptr) in known:continue
  if any(key in x for key in ['decision','disposition','Astra_disposition','primary_disposition','source_disposition']) and (rid(x) in affected or isinstance(x.get('edge'),dict)):
   contexts[str(p)+'#'+ptr]={'source_pin':sp,'json_pointer':ptr,'full_context':x}
snapshots={};grades={};gradebyobject={};contextsbyrid={};contextsbyobject={};unversioned={}
for contextkey,z in contexts.items():
 x=z['full_context']
 if not isinstance(x,dict):continue
 sp=z['source_pin'];p=Path(sp['path']);assert p.exists() and sha(p)==sp['sha256']
 r=rid(x)
 declared={k:x[k] for k in ['decision','Astra_disposition','primary_disposition','source_disposition','prior_disposition','prior_individual_disposition','disposition','rationale','Astra_rationale','reason','scope','reading_level','evaluation_level','category','limitation','request_limit','basis_retained','basis_to_retain_exactly','dependency_resolution','new_rebind_or_revision','new_revision_authorized'] if k in x}
 # Native metadata has a disposition; its literal record is not an Astra decision.
 pure_native=isinstance(x.get('data'),dict) and 'kind' in x and 'previous_id' in x
 if pure_native:declared={}
 ref={'source_pin':sp,'individual_context_pointer':z['json_pointer'],'deduplicated_context_pointer':'/contexts/'+esc(contextkey),'literal_primary_assertions':declared,'primary_scope_confirmation_required':True}
 if r in affected and declared:contextsbyrid.setdefault(r,[]).append(ref)
 if isinstance(r,str) and r.rsplit('@',1)[0] in oids and declared:contextsbyobject.setdefault(r.rsplit('@',1)[0],[]).append({**ref,'source_declared_revision_id':r,'requires_version_chain_review':r not in affected})
 for key in ['object_id','object','target','dependent_id']:
  value=x.get(key)
  if isinstance(value,str) and value in oids and not r and declared:unversioned.setdefault(value,[]).append({**ref,'version_not_explicit_no_exact_revision_credit':True})
 for key in ['edge','old_edge','baseline_edge','basis_edge','actual_edge']:
  e=x.get(key)
  if not isinstance(e,dict) or not isinstance(e.get('revision_id'),str) or not isinstance(e.get('basis_revision_id'),str) or not declared:continue
  if e['revision_id'].rsplit('@',1)[0] not in oids:continue
  gr={**ref,'edge_pointer':z['json_pointer']+'/'+key,'exact_prior_edge':e,'source_context_key':contextkey}
  grades.setdefault((e['revision_id'],e['basis_revision_id']),[]).append(gr)
  gradebyobject.setdefault((e['revision_id'].rsplit('@',1)[0],e['basis_revision_id'].rsplit('@',1)[0]),[]).append(gr)
 for ptr,n in walk(x):
  if not isinstance(n,dict):continue
  nr=rid(n)
  if nr not in affected or not isinstance(n.get('data'),dict) or 'caveat' not in n:continue
  snapshots.setdefault(nr,[]).append({**ref,'snapshot_pointer':z['json_pointer']+ptr,'snapshot':n})
fullcontexts=save('exact-primary-individual-context-and-snapshot-locator-input-index-v1.json',{'prior_context_dictionary_pin':pin(CP),'additional_source_pins':[pin(p) for p in sorted(newpaths)],'rules':'Only exact declared individual context/edge ID/version locators. No grades inferred from metadata or source pin alone.'})
apirows=load(W/'all893-target-full-API-equality-and-native-order-differences-v1.json')['objects'];apiindex={x['actual_revision_id']:(i,x) for i,x in enumerate(apirows)}
snapshotproof={}
for nr,entries in snapshots.items():
 assert nr in native,nr
 for e in entries:
  n=e['snapshot'];s=semantic(n);b=semantic(native[nr]);ds=diff(s,b)
  snapshotproof.setdefault(nr,[]).append({**{k:v for k,v in e.items() if k!='snapshot'},'exact_snapshot_ID_version':nr,'data_and_caveat_equal_to_actual_same_revision':not ds,'semantic_field_differences':ds,'native_wrapper_metadata_and_array_differences':diff(n,native[nr]),'native_comparison_array_order':'Actual explicit rowid insertion sequence; source snapshot saved order untouched. Differences explicit, never sort away.'})
SP=save('per-affected-revision-primary-snapshot-exact-semantic-and-order-equality-v1.json',{'baseline_native_pin':pin(BP),'actual893_native_pin':pin(NP),'objects':snapshotproof,'no_scope_or_source_grade_inferred':True})
changed={};requests=[]
for request in reqs:
 q=request['actual_request'];a=q['affected_revision_id'];ac=request['affected_latest_current_revision_id'];ch=q['changed_revision_id'];old=request['changed_previous_revision_id'];exact=grades.get((a,old),[])
 if ch not in changed:
  assert ch in native and old in native
  changed[ch]={'previous_revision_id':old,'actual_revision_id':ch,'full_previous_to_actual_all_field_differences':diff(native[old],native[ch]),'no_semantic_classification':'Differences mechanical only; Astra already grades source effects','actual_native_pointer':'/objects/'+esc(ch),'old_native_pointer':'/objects/'+esc(old)}
 candidates=apiindex.get(ac);snap=snapshotproof.get(a,[]);snapcurrent=snapshotproof.get(ac,[])
 requests.append({'actual_request':q,'affected_latest_current_revision_id':ac,'affected_revision_superseded':a!=ac,'exact_same_affected_revision_and_old_changed_basis_individual_primary_dependency_grade_locators':exact,'same_object_pair_prior_grade_locators_with_version_differences':[] if exact else gradebyobject.get((a.rsplit('@',1)[0],old.rsplit('@',1)[0]),[]),'primary_other_individual_exact_affected_revision_contexts':contextsbyrid.get(a,[]),'primary_other_individual_exact_current_revision_contexts':contextsbyrid.get(ac,[]) if ac!=a else [],'primary_versioned_same_object_contexts_older_or_different_revision_requires_chain_review':contextsbyobject.get(a.rsplit('@',1)[0],[]),'primary_unversioned_object_contexts_no_exact_revision_credit':unversioned.get(a.rsplit('@',1)[0],[]),'prior_primary_full_current_snapshot_equality_pointer':'/objects/'+esc(a) if snap else None,'actual_current_primary_snapshot_equality_pointer':'/objects/'+esc(ac) if snapcurrent else None,'at_least_one_exact_data_caveat_prior_snapshot':any(x['data_and_caveat_equal_to_actual_same_revision'] for x in snap),'affected_latest_is_exact_approved_actual_target':bool(candidates),'approved_target_proof_pointer':'/objects/'+str(candidates[0]) if candidates else None,'changed_fielddiff_pointer':'/objects/'+esc(ch),'source_individual_grade':'PENDING','no_auto_retain_rebind_resolution':True})
DP=save('all68-changed-revisions-full-previous-to-actual-field-differences-v1.json',{'baseline_native_pin':pin(BP),'actual_native_pin':pin(NP),'objects':changed,'changed_revision_count':len(changed)})
JP=save('all2128-actual-request-to-primary-individual-grade-context-and-current-equality-locators-v1.json',{'actual_request_pin':pin(RP),'prior_primary_context_input_index_pin':fullcontexts,'snapshot_equality_pin':SP,'actual893_API_proof_pin':pin(W/'all893-target-full-API-equality-and-native-order-differences-v1.json'),'changed_difference_pin':DP,'requests':requests,'no_source_grade_inferred':True})
summary={'requests':len(requests),'changed_revisions':len(changed),'superseded_affected_requests':sum(x['affected_revision_superseded'] for x in requests),'requests_with_exact_old_edge_primary_grade_locator':sum(bool(x['exact_same_affected_revision_and_old_changed_basis_individual_primary_dependency_grade_locators']) for x in requests),'requests_with_exact_primary_data_caveat_snapshot':sum(x['at_least_one_exact_data_caveat_prior_snapshot'] for x in requests),'requests_affected_current_exact_approved_API':sum(x['affected_latest_is_exact_approved_actual_target'] for x in requests),'unmatched_exact_prior_grade_request_IDs':[x['actual_request']['id'] for x in requests if not x['exact_same_affected_revision_and_old_changed_basis_individual_primary_dependency_grade_locators']]}
assert len(requests)==2128 and len(changed)==68
result=save('primary2128-readonly-locator-and-difference-preparation-index-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'request_join_pin':JP,'snapshot_equality_pin':SP,'changed_all68_difference_pin':DP,'context_input_index_pin':fullcontexts,'counts':summary,'no_grade_or_apply':True});print(json.dumps({'result':result,'request_join':JP,'changed_diff':DP,'counts':{k:v for k,v in summary.items() if not isinstance(v,list)}},indent=2))
