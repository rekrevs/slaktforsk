"""Compact exact actual producer/source-specification locators; no request grade inferred."""
import datetime,hashlib,json,re
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/actual2128-readonly-preparation-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(s):return str(s).replace('~','~0').replace('/','~1')
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+esc(k))
 elif isinstance(x,list):
  for i,v in enumerate(x):
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+str(i))
def target(x):
 if not isinstance(x,dict):return None
 for k in ['object_id','id','target_id','referring_revision','revision_id','object_revision','target','object']:
  v=x.get(k)
  if isinstance(v,str):return v.rsplit('@',1)[0]
 for k in ['current','full_current','current_full','full_native','object','current_full_native','prospective_full','candidate_full','new_entire_API']:
  if isinstance(x.get(k),dict):
   r=target(x[k])
   if r:return r
 return None
def fieldat(api,f):
 if f.startswith('/'):
  parts=[x.replace('~1','/').replace('~0','~') for x in f.strip('/').split('/')]
 else:parts=f.split('.')
 if parts[0] not in api and parts[0] in api.get('data',{}):parts=['data']+parts
 v=api
 for k in parts:
  if not isinstance(v,dict) or k not in v:return False,None
  v=v[k]
 return True,v
JP=W/'all2128-actual-request-to-primary-individual-grade-context-and-current-equality-locators-v2.json';reqs=load(JP)['requests']
AP=W/'all893-target-full-API-equality-and-native-order-differences-v1.json';aps=load(AP)['objects'];byrid={x['actual_revision_id']:x for x in aps}
groups={}
for q in reqs:
 r=q['affected_latest_current_revision_id']
 if r in byrid:groups.setdefault(r,[]).append(q)
gatep=B/'source-review/all10-global-primary-source-ready-gate-v6.json';gate=load(gatep)
ops={x['path']:load(x['path']) for x in gate['operations']}
sourcehash={sha(p):p for p in (B/'source-review').glob('*.json')}
contexts=load(B/'implementation/five-expanded-exactnative-pointer-join-v2/deduplicated-full-source-decision-contexts-v1.json')['contexts'];contextrows=list(contexts.values())
# Exact reason-declared source files only, plus prior preserved source decision dictionary.
reasonpins={}
known={(x['source_pin']['path'],x['json_pointer']) for x in contextrows}
for path,op in ops.items():
 reasonpins[path]=[]
 for h in re.findall(r'(?<![a-f0-9])[a-f0-9]{64}(?![a-f0-9])',op['reason']):
  if h not in sourcehash:continue
  p=sourcehash[h];pp=pin(p);reasonpins[path].append(pp)
  for ptr,x in walk(load(p)):
   if not isinstance(x,dict) or (str(p),ptr) in known:continue
   if any(k in x for k in ['decision','disposition','Astra_disposition','primary_disposition','source_disposition','edits','changes','new_entire_API','full_new_body']):
    contextrows.append({'source_pin':pp,'json_pointer':ptr,'full_context':x});known.add((str(p),ptr))
byoid={}
for z in contextrows:
 x=z['full_context'];oid=target(x)
 if oid not in {r.rsplit('@',1)[0] for r in groups}:continue
 assertions={k:x[k] for k in ['decision','disposition','Astra_disposition','primary_disposition','source_disposition','rationale','Astra_rationale','reason','field','scope','reading_level','evaluation_level','limitation','basis_retained','basis_to_retain_exactly'] if k in x}
 if isinstance(x.get('data'),dict) and 'kind' in x and 'previous_id' in x:continue
 if not assertions and not any(k in x for k in ['edits','changes','new_entire_API']):continue
 byoid.setdefault(oid,[]).append((z,assertions))
BP=B/'implementation/resumed-current140-settled-spec-API-binding-index-v2/per-resumed-spec-exact-latest-whole-API-and-field-bindings-v1.json';bound=load(BP)['rows'];bd={}
for i,x in enumerate(bound):bd.setdefault(x['object_id'],[]).append((i,x))
RP=B/'implementation/resumed-current140-independent-receipt-join-v2/per-current140-operation-and-target-receipt-join-v1.json';reviews={m['current_member']['path']:m for m in load(RP)['members']}
rows=[]
for r,qs in sorted(groups.items()):
 a=byrid[r];oid=a['object_id'];op=ops[a['operation_pin']['path']];idx=int(a['approved_API_pointer'].split('/')[-1]);api=op['changes'][idx];specs=[]
 for z,assertions in byoid.get(oid,[]):
  x=z['full_context'];ptr=z['json_pointer'];checks=[];whole=[]
  for xp,n in walk(x):
   if not isinstance(n,dict):continue
   if n.get('id')==oid and n.get('expectedVersion')==api['expectedVersion'] and isinstance(n.get('data'),dict) and 'kind' in n:
    whole.append({'source_API_pointer':ptr+xp,'exact_whole_API_equals_actual_producer':n==api,'source_API_sha256':hashlib.sha256(json.dumps(n,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),'API_wrapper_fields_present':list(n)})
   f=n.get('field');nv=n.get('new',n.get('new_value'))
   if isinstance(f,str) and ('new' in n or 'new_value' in n):
    found,value=fieldat(api,f);checks.append({'source_field_edit_pointer':ptr+xp,'exact_field':f,'actual_field_present':found,'literal_new_value_equals_actual_API_field':found and value==nv,'literal_new_value_sha256':hashlib.sha256(json.dumps(nv,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()})
  specs.append({'source_pin':z['source_pin'],'individual_source_pointer':ptr,'literal_individual_disposition_rationale_and_scope':assertions,'source_declared_revision_or_version':{k:x[k] for k in ['revision_id','revision','expectedVersion','version','native_version','object_id'] if k in x},'embedded_candidate_API_checks':whole,'literal_field_edit_equality_checks':checks,'producer_reason_explicitly_pins_this_source':z['source_pin'] in reasonpins[a['operation_pin']['path']],'same_object_context_is_not_automatically_latest_version_or_source_grade':True})
 oldbinding=[{'binding_index_pin':pin(BP),'binding_row_pointer':'/rows/'+str(i),'source_pin':z['source_pin'],'source_object_pointer':z['source_object_pointer'],'exact_whole_source_API_equals_latest':z['exact_whole_source_API_equals_latest'],'all_exact_spec_latest_API_differences':z['all_exact_spec_latest_API_differences'],'explicit_field_checks_pointer':'/rows/'+str(i)+'/explicit_field_checks'} for i,z in bd.get(oid,[]) if z['latest_actual_member_pin']['path']==a['operation_pin']['path']]
 review=reviews.get(a['operation_pin']['path']);rr=[]
 if review:
  for i,z in enumerate(review['per_target']):
   if z['target_id']==oid:rr.append({'independent_review_join_pin':pin(RP),'per_target_pointer':'/members/'+str(a['operation_pin']['index']-1)+'/per_target/'+str(i),'exact_current_operation_receipt_path_hash_pointers':review['exact_current_operation_receipt_path_hash_pointers'],'actual_target_review_row_pointers':z['actual_target_review_row_pointers'],'individual_whole_actual_reading_assertions':z.get('individual_whole_actual_reading_assertions',[]),'mechanical_receipt_join_does_not_expand_reading_scope':True})
 rows.append({'actual_current_revision_id':r,'actual_request_IDs':[q['actual_request']['id'] for q in qs],'affected_exact_revision_IDs':sorted({q['actual_request']['affected_revision_id'] for q in qs}),'actual_producer_pin':a['operation_pin'],'actual_producer_API_pointer':a['approved_API_pointer'],'whole_actual_native_ordered_API_equality_pointer':'/objects/'+str(aps.index(a)),'exact_reason_declared_primary_source_pins':reasonpins[a['operation_pin']['path']],'exact_individual_source_spec_contexts':specs,'prior_strict_latest_API_binding_rows':oldbinding,'exact_prior_independent_current_API_receipt_locators':rr,'no_individual_source_spec_context_locator':not specs,'actual_request_source_grade':'PENDING','no_auto_retain_rebind_resolution':True})
p=W/'unique-approved-actual-current-producer-to-individual-source-spec-locators-v1.json';assert not p.exists();d={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_request_join_pin':pin(JP),'complete_API_equality_pin':pin(AP),'approved_primary_gate_pin':pin(gatep),'objects':rows,'counts':{'unique_approved_current':len(rows),'all_actual_requests_with_approved_current':sum(len(x['actual_request_IDs']) for x in rows),'with_individual_primary_source_spec_context':sum(bool(x['exact_individual_source_spec_contexts']) for x in rows),'with_prior_explicit_whole_latest_API_binding':sum(bool(x['prior_strict_latest_API_binding_rows']) for x in rows),'with_prior_independent_API_review_join':sum(bool(x['exact_prior_independent_current_API_receipt_locators']) for x in rows),'no_individual_source_context_locator':[x['actual_current_revision_id'] for x in rows if x['no_individual_source_spec_context_locator']]},'rules':'Exact producer/order/payload and literal individual source-spec pointers. Contexts may be historical or differing scope/version; all such contexts preserved explicitly. No actual2128 request grade inferred from approved current API or gate counts.'};p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pin':pin(p),'counts':{k:v for k,v in d['counts'].items() if not isinstance(v,list)},'no_individual_source_context_locator':len(d['counts']['no_individual_source_context_locator'])},indent=2))
