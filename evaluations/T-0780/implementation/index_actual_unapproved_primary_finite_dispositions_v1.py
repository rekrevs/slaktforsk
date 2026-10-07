"""Finite literal primary disposition index entries/rows for actual affected current revisions."""
import datetime,hashlib,json
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/actual2128-readonly-preparation-v1'
def load(p):return json.loads(Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def esc(s):return str(s).replace('~','~0').replace('/','~1')
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+esc(k))
 elif isinstance(x,list):
  for i,v in enumerate(x):
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+str(i))
def rid(x):
 if not isinstance(x,dict):return None
 for key in ['revision_id','revision','id','object_id','object_revision']:
  value=x.get(key)
  if isinstance(value,str):
   if '@' in value:return value
   ver=x.get('version',x.get('native_version',x.get('expectedVersion')))
   if isinstance(ver,int):return value+'@'+str(ver)
 return None
JP=W/'all2128-actual-request-to-primary-individual-grade-context-and-current-equality-locators-v2.json';joined=load(JP)['requests'];AP=W/'all893-full-actual-native-targets-in-journal-insertion-order-v1.json';targets=load(AP)['objects'];BP=W/'all-existing-actual-request-support-full-baseline-native-payloads-v1.json';baseline=load(BP)['objects']
groups={}
for x in joined:
 r=x['affected_latest_current_revision_id']
 if r in targets:continue
 groups.setdefault(r,[]).append(x)
sourcepaths=set()
for pattern in ['*finite*source*index*.json','*source-disposition*index*.json','*selected*reuse-index*.json','*remaining532*reuse*.json','resumed-*-source-dispositions-v1.json','resumed-five-partial97-source-field-dispositions-v1.json']:
 sourcepaths.update((B/'source-review').glob(pattern))
matches={};scopes={};inputs=[]
for p in sorted(sourcepaths):
 d=load(p);pp=pin(p);inputs.append(pp);scope={k:d[k] for k in ['status','scope','limits','limitations','mandatory_overlays','reading_credit','coverage'] if k in d}
 for ptr,x in walk(d):
  r=rid(x)
  if r not in groups:continue
  assertions={k:x[k] for k in ['disposition','decision','source_disposition','primary_disposition','prior_disposition','prior_rationale','rationale','reading_level','reading_credit','mandatory_latest_overlays','metadata_residual_disposition','scope_fields_read','evaluation_level','category','limitation'] if k in x}
  linked={k:x[k] for k in ['source_pin','decision_pin','decision_pointer','pointer','join_pointer','individual_decision_pointer','reading_snapshot_pointer','prior_index_pin','prior_pointer','source_disposition_pointer','source_decision_pin','source_decision_pointer','full_native_pointer','primary_decision','prior_decision','reading_reuse','native_reading_reuse'] if k in x}
  if not assertions and not linked:continue
  if isinstance(x.get('data'),dict) and 'kind' in x:continue
  entry={'primary_finite_index_pin':pp,'exact_individual_entry_pointer':ptr,'exact_ID_version':r,'literal_primary_individual_assertions':assertions,'exact_prior_disposition_and_snapshot_references':linked,'literal_enclosing_source_scope':scope,'no_new_source_grade_or_whole_reading_level_inferred':True}
  matches.setdefault(r,[]).append(entry)
out=[]
for r,rs in sorted(groups.items()):
 assert r in baseline,r
 direct=[];oldedge=[]
 for x in rs:
  direct.extend(x['primary_other_individual_exact_affected_revision_contexts'] if x['actual_request']['affected_revision_id']==r else x['primary_other_individual_exact_current_revision_contexts'])
  oldedge.extend(x['exact_same_affected_revision_and_old_changed_basis_individual_primary_dependency_grade_locators'])
 def unique(a):
  found={}
  for x in a:found[(x['source_pin']['path'],x['individual_context_pointer'])]=x
  return list(found.values())
 direct=unique(direct);oldedge=unique(oldedge)
 out.append({'affected_current_revision_id':r,'kind':baseline[r]['kind'],'actual_request_IDs':[x['actual_request']['id'] for x in rs],'affected_exact_revision_IDs':sorted({x['actual_request']['affected_revision_id'] for x in rs}),'current_native_pointer':'/objects/'+esc(r),'current_native_whole_equals_stage_before':True,'actual_current_has_no_approved_revision_target':True,'existing_exact_primary_individual_context_locators':direct,'existing_exact_prior_dependency_grade_locators':oldedge,'additional_exact_finite_primary_index_entries':matches.get(r,[]),'no_exact_primary_individual_or_finite_disposition_locator':not(direct or oldedge or matches.get(r)),'source_scope_grade_and_actual_request_disposition':'PENDING','no_automatic_retain_or_rebind':True})
p=W/'unique-actual-unapproved-current-primary-finite-disposition-locators-v1.json';assert not p.exists();d={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual2128_join_pin':pin(JP),'baseline_current_payload_pin':pin(BP),'primary_finite_input_pins':inputs,'objects':out,'counts':{'unique_affected_current_without_approved_API':len(out),'actual_requests_represented':sum(len(x['actual_request_IDs']) for x in out),'with_exact_prior_individual_or_finite_disposition_locator':sum(not x['no_exact_primary_individual_or_finite_disposition_locator'] for x in out),'additional_finite_index_matches':sum(bool(x['additional_exact_finite_primary_index_entries']) for x in out),'remaining_no_exact_primary_locator':[x['affected_current_revision_id'] for x in out if x['no_exact_primary_individual_or_finite_disposition_locator']]},'rules':'Finite index entries/rows and explicitly linked prior disposition scopes only; no metadata routing approval or inferred reading level. Actual2128 requests require Astra judgment.'};p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result_pin':pin(p),'counts':{k:v for k,v in d['counts'].items() if not isinstance(v,list)},'remaining_unique_no_locator':len(d['counts']['remaining_no_exact_primary_locator'])},indent=2))
