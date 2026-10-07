"""Finite saved-own-reading schema recovery. Equality and locators, never grades."""
import copy, datetime, hashlib, json
from pathlib import Path
B=Path('evaluations/T-0780')
W=B/'implementation/resumed-final-selected-and-prior-own-predicate-join-v1'
def load(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'sha256':sha(p)}
def esc(s): return str(s).replace('~','~0').replace('/','~1')
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,(dict,list)): yield from walk(v,p+'/'+esc(k))
 elif isinstance(x,list):
  for i,v in enumerate(x): yield from walk(v,p+'/'+str(i))
def get(d,p):
 for t in p.strip('/').split('/') if p else []:
  t=t.replace('~1','/').replace('~0','~');d=d[int(t)] if isinstance(d,list) else d[t]
 return d
def ridof(x):
 if isinstance(x,str): return x if '@' in x else None
 if not isinstance(x,dict):return None
 for k in ['revision_id','revision','id','object_id']:
  v=x.get(k)
  if isinstance(v,str):
   if '@' in v:return v
   ver=x.get('version',x.get('expectedVersion'))
   if isinstance(ver,int):return v+'@'+str(ver)
 if isinstance(x.get('object'),dict):return ridof(x['object'])
 if isinstance(x.get('object'),str):return ridof(x['object'])
 return None
def projection(x):
 d=copy.deepcopy(x.get('data'));d.pop('revision_id',None)
 for k,v in d.items():
  if k.endswith('_json') and isinstance(v,str):d[k]=json.loads(v)
 return d,x.get('caveat')
strictpath=W/'compact-strict-own-predicates-input-index-and-current-field-equality-v1.json'
rawpath=W/'five-scope-exact-own-current-field-reading-locators-v10.json'
strict=load(strictpath);raw=load(rawpath)
scopes={k:[x['revision_id'] for x in v] for k,v in strict['scopes'].items()}
targets=set().union(*map(set,scopes.values()))
F=B/'implementation/five-expanded-exactnative-pointer-join-v2/full-frozen-native-residual-dictionary-v1.json'
native=load(F)['objects'];nativepins=[pin(F)]
for name in ['current-full-native-objects-v1.json','additional-context-full-native-objects-v2.json']:
 p=B/'implementation/dependency-preparation-v1'/name;nativepins.append(pin(p))
 for x in load(p)['objects'].values():native.setdefault(x['id'],x)
oldcomparisons={}
for rows in raw['scopes'].values():
 for row in rows:
  for c in row['own_reading_comparisons']:
   oldcomparisons.setdefault((c['own_receipt_pin']['path'],row['revision_id']),[]).append(c)
cache={};matches={};unbound={};shapes={}
def cached(p):
 p=str(p)
 if p not in cache:cache[p]=load(p)
 return cache[p]
def record(rid,rp,predicate,snapshotpin,sptr,snap,schema):
 if rid not in targets:return
 if ridof(snap)!=rid or not isinstance(snap.get('data'),dict) or 'caveat' not in snap:return
 eq=projection(snap)==projection(native[rid])
 entry={'own_receipt_pin':rp,'literal_own_reading_predicate':predicate,'schema':schema,'saved_input_pin':snapshotpin,'saved_input_pointer':sptr,'exact_ID_version':rid,'full_data_caveat_equal':eq,'comparison_projection':'Native revision_id removed from data; *_json text parsed only to the exact structured API value. All list order preserved. No metadata projection credit.','scope_confirmation_required':True,'no_metadata_or_original_readcredit_inferred':True}
 matches.setdefault(rid,[]).append(entry)
def sourcepath(v):
 if not isinstance(v,str):return None
 p=Path(v)
 if not p.is_absolute() and not v.startswith('evaluations/'):p=B/p
 return p if p.exists() and p.suffix=='.json' else None
for p in sorted((B/'fresh-independent-review').glob('*.json')):
 if any(t in p.name for t in ['routing-for-own','exact-routing','semantic-scan','expanded-military-scan','search-input']):continue
 doc=cached(p);rp=pin(p)
 literal={k:doc[k] for k in ['scope','status','method','verification','whole_current_reuse','reading','limits'] if k in doc}
 # Explicit entire current/source/actual read ID arrays; no count-only predicates.
 predicates=[]
 for k in ['whole_read','full_read_revisions','read_ids']:
  if isinstance(doc.get(k),list):
   for i,x in enumerate(doc[k]):
    r=ridof(x)
    if r in targets:predicates.append((r,{'pointer':'/'+k+'/'+str(i),'literal':x,'own_scope':literal},k))
 # Whole own embedded current objects, including nested dispositions[].object.
 full_scope=any(('read' in str(v).lower() and any(t in str(v).lower() for t in ['full','whole','complete'])) for v in literal.values())
 for ptr,x in walk(doc):
  if not isinstance(x,dict):continue
  r=ridof(x)
  if r not in targets:continue
  flags={k:v for k,v in x.items() if isinstance(v,bool) and v and ('read' in k or 'reuse' in k) and ('current' in k or 'data' in k or 'native' in k)}
  if isinstance(x.get('data'),dict) and 'caveat' in x and full_scope and ('/full_read_objects/' in ptr or '/objects/' in ptr or '/dispositions/' in ptr):
   record(r,rp,{'pointer':ptr,'literal_own_complete_read_scope':literal},rp,ptr,x,'own_embedded_full_read_objects_or_nested_disposition_object')
  if flags:
   predicate={'pointer':ptr,'literal_read_flags':flags,'literal_disposition':x.get('disposition'),'own_scope':literal}
   # Explicit own native input pin + any supported pointer spelling.
   ip=x.get('complete_current_input',doc.get('input_pin',doc.get('native_input_pin',doc.get('native_dictionary_pin'))))
   sp=next((x[k] for k in ['input_pointer','whole_native_pointer','native_pointer','full_native_pointer','current_pointer'] if isinstance(x.get(k),str)),None)
   if isinstance(ip,dict) and sp:
    q=sourcepath(ip.get('path'))
    if q and sha(q)==ip.get('sha256'):
     sd=cached(q)
     try:snap=get(sd,sp)
     except (KeyError,ValueError,TypeError):
      snap=sd.get('objects',{}).get(r) if sp=='/objects/'+r and isinstance(sd.get('objects'),dict) else None
      if snap:sp='/objects/'+esc(r)
     if isinstance(snap,dict):record(r,rp,predicate,pin(q),sp,snap,'own_full_semantic_read_exact_native_input_pointer')
   predicates.append((r,predicate,'explicit_individual_read_flags'))
 # Exact own per-ID predicates qualify already located snapshots, never the whole input.
 for r,pred,schema in predicates:
  cs=oldcomparisons.get((str(p),r),[])
  for c in cs:
   if not c['whole_data_and_caveat_exact_equal']:continue
   q=Path(c['snapshot_input_pin']['path']);sd=cached(q)
   try:snap=get(sd,c['snapshot_pointer'])
   except (KeyError,ValueError,TypeError):continue
   if isinstance(snap,dict):record(r,rp,pred,c['snapshot_input_pin'],c['snapshot_pointer'],snap,schema+'_with_exact_prior_saved_snapshot')
  # Explicit whole_read receipts pin source specifications but old parser missed predicate.
  if schema=='whole_read':
   for ptr,ref in walk(doc):
    if not isinstance(ref,dict):continue
    q=sourcepath(ref.get('path'))
    if not q or str(B/'source-review') not in str(q) or sha(q)!=ref.get('sha256'):continue
    for sp,x in walk(cached(q)):
     if isinstance(x,dict) and ridof(x)==r and isinstance(x.get('data'),dict) and 'caveat' in x:
      record(r,rp,pred,pin(q),sp,x,'explicit_whole_read_ID_with_exact_pinned_source_current_snapshot')
  if not any(z['own_receipt_pin']==rp and z['full_data_caveat_equal'] for z in matches.get(r,[])):
   unbound.setdefault(r,[]).append({'own_receipt_pin':rp,'schema':schema,'literal_own_reading_predicate':pred,'reason':'Explicit predicate exists; no complete exact input snapshot binding recovered by this bounded supplement'})
out={};counts={}
supp=load(W/'supplemental-explicit-own-selected-read-predicates-with-unhashed-input-locators-v1.json')
for scope,ids in scopes.items():
 rows=[]
 for r in ids:
  old=next(x for x in strict['scopes'][scope] if x['revision_id']==r)
  ms=matches.get(r,[]);unique=[];seen=set()
  for m in ms:
   key=(m['own_receipt_pin']['path'],m['saved_input_pin']['path'],m['saved_input_pointer'],m['literal_own_reading_predicate']['pointer'])
   if key not in seen:seen.add(key);unique.append(m)
  has=bool(old['exact_whole_data_caveat_matches']) or any(m['full_data_caveat_equal'] for m in unique)
  rows.append({'revision_id':r,'prior_strict_qualified_binding':bool(old['exact_whole_data_caveat_matches']),'additional_explicit_own_predicate_bindings':unique,'exact_binding_available':has,'unbound_explicit_own_read_predicates':unbound.get(r,[]),'unhashed_selected_ID_locator_available':any(x['revision_id']==r for x in supp['scopes'][scope]),'actual_target_assertion_locators':old['all_saved_own_actual_target_assertion_locators'],'no_scope_grade_inferred':True})
 out[scope]=rows
 missing=[x for x in rows if not x['exact_binding_available']]
 grouped={}
 for x in missing:
  refs=x['unbound_explicit_own_read_predicates']+x['actual_target_assertion_locators']
  if not refs:grouped.setdefault('no_exact_saved_predicate_locator',[]).append(x['revision_id'])
  for ref in refs:grouped.setdefault(ref['own_receipt_pin']['path'],[]).append(x['revision_id'])
 counts[scope]={'scope_rows':len(rows),'exact_full_data_caveat_binding_with_explicit_own_predicate':len(rows)-len(missing),'remaining_without_strict_binding':len(missing),'remaining_grouped_by_own_receipt_schema':{k:sorted(set(v)) for k,v in grouped.items()}}
latest=B/'implementation/resumed-six-P0066-P0002-P0049-source-route-queue-v1/concrete-current142-partial-sequence-and-constraint-proposal-v1.json'
p=W/'finite-additional-own-full-reading-schema-bindings-and-residual-map-v1.json';assert not p.exists()
p.write_text(json.dumps({'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prior_strict_pin':pin(strictpath),'additional_unhashed_scope_locators_pin':pin(W/'supplemental-explicit-own-selected-read-predicates-with-unhashed-input-locators-v1.json'),'frozen_native_input_pins':nativepins,'latest_candidate_pin':pin(latest),'counts':counts,'scopes':out,'rules':'These are exact own literal reading predicates and full data+caveat equality, preserving metadata/scope limits and native arrays. Whole-operation/native-source checks only qualify explicitly named IDs. No grade, approval, original reading, whole-input reading or canonical writes inferred.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result_pin':pin(p),'counts':{k:{a:b for a,b in v.items() if a!='remaining_grouped_by_own_receipt_schema'} for k,v in counts.items()}},indent=2))
