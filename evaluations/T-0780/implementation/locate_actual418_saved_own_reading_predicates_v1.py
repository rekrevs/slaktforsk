"""Finite exact own receipt/input locator recovery for the reviewer-named 418 revisions."""
import datetime,hashlib,json
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/actual2128-readonly-preparation-v1';S=B/'full10-stage-final143-v1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
cache={}
def load(p):
 p=str(p)
 if p not in cache:cache[p]=json.loads(Path(p).read_text())
 return cache[p]
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
 if isinstance(x,str):return x if '@' in x else None
 if not isinstance(x,dict):return None
 for k in ['revision_id','revision','id','object_id']:
  v=x.get(k)
  if isinstance(v,str):
   if '@' in v:return v
   ver=x.get('version',x.get('expectedVersion',x.get('current_version')))
   if isinstance(ver,int):return v+'@'+str(ver)
 for k in ['object','current','full_current','current_full_object','full_native']:
  if isinstance(x.get(k),dict):
   r=rid(x[k])
   if r:return r
 return None
def semantic(n):
 d={k:v for k,v in n['data'].items() if k!='revision_id'}
 for k,v in d.items():
  if k.endswith('_json') and isinstance(v,str):d[k]=json.loads(v)
 return d,n.get('caveat')
interim=B/'fresh-independent-review/resumed-actual143-stage-runtime-payload-binding-interim-v1.json'
requests=load(S/'actual-handoff-v1/all-actual-pending-individual-request-routing-v1.json')['requests']
affected={x['actual_request']['affected_revision_id'] for x in requests}|{x['affected_latest_current_revision_id'] for x in requests}
ids=set(load(interim)['unmatched_historical_payloads'])&affected;assert len(ids)==418
NP=W/'all-existing-actual-request-support-full-baseline-native-payloads-v1.json';native=load(NP)['objects'];assert ids<=set(native)
selected={sha(p):p for p in (B/'preparation/selected').glob('*source-relevant-current-context*.json')}
matches={};input_only={};predicates={};receiptpins=[];snapshotcache={}
def path(v):
 if not isinstance(v,str):return None
 q=Path(v)
 if not q.is_absolute() and not v.startswith('evaluations/'):q=B/q
 return q if q.exists() and q.suffix=='.json' else None
def snapshots(q):
 q=str(q)
 if q not in snapshotcache:
  rs={}
  for ptr,x in walk(load(q)):
   if isinstance(x,dict) and rid(x) in ids and isinstance(x.get('data'),dict) and 'caveat' in x:rs.setdefault(rid(x),[]).append((ptr,x))
  snapshotcache[q]=rs
 return snapshotcache[q]
for p in sorted((B/'fresh-independent-review').glob('*.json')):
 if any(t in p.name for t in ['semantic-scan','expanded-military-scan','search-input','routing-for-own','exact-routing','stage-runtime','stage-complete-native','finite-own-reading-reuse-bindings-recomputed']):continue
 doc=load(p);rp=pin(p);scope={k:doc[k] for k in ['status','scope','reading','method','whole_read','whole_reading','read_scope','verification','limits','coverage'] if k in doc};own={};inputs={}
 for ptr,x in walk(doc):
  if isinstance(x,dict):
   r=rid(x)
   assertions={k:v for k,v in x.items() if k in ['decision','judgment','source_disposition','own_disposition','review','whole_current_data_and_caveat_read','full_data_and_caveat_read','full_current_data_and_caveat_read','full_native_read','whole_native_fields_read','full_current_new_API_read','whole_API_reconstruction_equal','scope_fields_read','fields']}
   if isinstance(x.get('data'),dict) and 'kind' in x:assertions={}
   if r in ids and assertions:own.setdefault(r,[]).append({'pointer':ptr,'literal_own_individual_assertions':assertions,'literal_own_reading_scope':scope,'reading_scope_requires_reviewer_confirmation':True})
   for k in ['path','input','source','source_path']:
    q=path(x.get(k))
    if not q:continue
    for hk in ['sha256','input_sha256','source_sha256']:
     if x.get(hk)==sha(q):inputs[str(q)]=(pin(q),ptr+'/'+esc(k))
   for k in ['input_sha256','source_input_sha256','selected_input_sha256']:
    h=x.get(k)
    if isinstance(h,str) and h in selected:inputs[str(selected[h])]=(pin(selected[h]),ptr+'/'+k)
   # Dictionary path→hash pin envelopes.
   for key in ['pins','inputs']:
    if isinstance(x.get(key),dict):
     for name,h in x[key].items():
      q=path(name)
      if q and isinstance(h,str) and sha(q)==h:inputs[str(q)]=(pin(q),ptr+'/'+key+'/'+esc(name))
  elif isinstance(x,list):
   leaf=ptr.rsplit('/',1)[-1]
   if leaf in ['whole_read','full_read_revisions','read_ids','whole_objects_read','read_objects','full_read_objects','read_complete_selected_objects']:
    for i,row in enumerate(x):
     r=rid(row)
     if r in ids:own.setdefault(r,[]).append({'pointer':ptr+'/'+str(i),'literal_own_reading_enumeration':row if not isinstance(row,dict) or 'data' not in row else {'revision_id':r},'literal_own_reading_scope':scope,'reading_scope_requires_reviewer_confirmation':True})
 # Full_read_sections stores whole native snapshots: preserve section assertion, do not infer entire input.
 for ptr,x in walk(doc.get('full_read_sections',{}),'/full_read_sections'):
  r=rid(x)
  if r in ids and isinstance(x,dict) and isinstance(x.get('data'),dict) and 'caveat' in x:
   own.setdefault(r,[]).append({'pointer':ptr,'literal_own_saved_whole_section_scope':scope,'reading_scope_requires_reviewer_confirmation':True})
 for r,ownassert in own.items():predicates.setdefault(r,[]).append({'own_receipt_pin':rp,'literal_own_predicates':ownassert})
 inputs[str(p)]=(rp,'own_embedded_receipt')
 for name,(ip,refptr) in inputs.items():
  # Only actual complete snapshots for exact418 ID/version; input pin alone is not reading.
  for r,rows in snapshots(name).items():
   for sp,x in rows:
    equal=semantic(x)==semantic(native[r]);entry={'own_receipt_pin':rp,'exact_input_pin':ip,'own_input_binding_pointer':refptr,'saved_full_snapshot_pointer':sp,'exact_ID_version':r,'full_data_caveat_equal_actual_baseline':equal,'literal_own_individual_reading_predicates':own.get(r,[]),'literal_own_top_scope':scope,'no_input_pin_only_readcredit':True,'metadata_scope_not_inferred':True,'source_or_reading_grade_confirmation_required':True}
    if own.get(r):matches.setdefault(r,[]).append(entry)
    elif equal:input_only.setdefault(r,[]).append(entry)
 if any(r in own or any(r in snapshots(name) for name in inputs) for r in ids):receiptpins.append(rp)
out=[]
for r in sorted(ids):
 rs=[x['actual_request']['id'] for x in requests if x['actual_request']['affected_revision_id']==r or x['affected_latest_current_revision_id']==r]
 out.append({'revision_id':r,'actual_request_IDs':rs,'exact_saved_own_snapshot_and_literal_individual_predicate_locators':matches.get(r,[]),'literal_own_individual_predicates_without_exact_snapshot_bindings':predicates.get(r,[]),'exact_input_snapshot_pin_only_NOT_reading_predicates':input_only.get(r,[]),'no_exact_saved_individual_snapshot_predicate':not any(x['full_data_caveat_equal_actual_baseline'] for x in matches.get(r,[])),'no_source_or_own_reading_grade':True})
p=W/'actual418-saved-own-reading-predicates-and-input-equality-locators-v1.json';assert not p.exists();p.write_text(json.dumps({'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_interim_unmatched_scope_pin':pin(interim),'actual_baseline_native_pin':pin(NP),'objects':out,'counts':{'actual_scope_revisions':len(ids),'with_exact_saved_snapshot_and_literal_own_individual_predicate':sum(not x['no_exact_saved_individual_snapshot_predicate'] for x in out),'with_literal_own_predicate':sum(bool(x['literal_own_individual_predicates_without_exact_snapshot_bindings']) for x in out),'remaining_explicit_no_exact_binding':[x['revision_id'] for x in out if x['no_exact_saved_individual_snapshot_predicate']]},'rules':'Exact per-ID/version snapshots and literal own scope/predicates only. No generic whole-input pin credit, no grade heuristic. Reviewer confirms reading scope, primary grades source implications.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result_pin':pin(p),'counts':{k:v for k,v in load(p)['counts'].items() if not isinstance(v,list)}},indent=2))
