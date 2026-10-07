"""Exact own saved reading field locator: ID/version, whole data+caveat minimum; no grades."""
import json,hashlib,copy,re,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-final-five-scope-own-current-field-join-v9'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(k):return str(k).replace('~','~0').replace('/','~1')
def resolve(p):
 if not isinstance(p,str):return None
 q=Path(p)
 if p.startswith('evaluations/') or q.is_absolute():return q
 if p.startswith(('implementation/','source-review/','preparation/','fresh-independent-review/')):return B/q
 return None
F=B/'implementation/five-expanded-exactnative-pointer-join-v2/full-frozen-native-residual-dictionary-v1.json';assert sha(F)=='8ec9b8a2f55b70f72a4ef140896b20553ff84dd0addad6490083a0901ed0ddc0';native=load(F)['objects']
N=B/'implementation/resumed-five-no-pointer-compact-routing-v1/ordered-five-scope-no-pointer-compact-routing-inventory-v1.json';assert sha(N)=='800b3f2cd1aa9fde9328396d582e42a0a97110a8ddd4140c2d42765a783fb781';nr=load(N)['rows']
def getptr(doc,ptr):
 for token in ptr.lstrip('/').split('/') if ptr else []:
  token=token.replace('~1','/').replace('~0','~');doc=doc[int(token)] if isinstance(doc,list) else doc[token]
 return doc
nativepins=[pin(F)]
for name in ['current-full-native-objects-v1.json','additional-context-full-native-objects-v2.json']:
 q=B/'implementation/dependency-preparation-v1'/name;nativepins.append(pin(q))
 for x in load(q)['objects'].values():
  if x['id'] in native:assert native[x['id']]['data']==x['data'] and native[x['id']]['caveat']==x['caveat']
  else:native[x['id']]=x
nrids={scope:{r['revision_id'] for r in nr if any(a['scope']==scope for a in r['routing_aliases'])} for scope in ['C-0044','C-0563','C-0561','C-0106']}
scopeids={};exclusionpins=[]
for scope in ['C-0044','C-0563','C-0561','C-0106']:
 q=B/'implementation/five-expanded-exactnative-pointer-join-v2'/f'{scope}-exact-ordered-scope-tuples-v1.json';ids=[r['whole_routing_tuple']['revision_id'] for r in load(q)['ordered_scope']]
 if scope in ['C-0044','C-0563']:scopeids[scope+'-prior-pointer']=[rid for rid in ids if rid not in nrids[scope]]
 else:
  scopeids[scope+'-no-pointer']=list(rid for rid in ids if rid in nrids[scope]);scopeids[scope+'-prior-pointer']=list(rid for rid in ids if rid not in nrids[scope])
C=B/'source-review/resumed-C0685-unbound109-individual-source-dispositions-v1.json';scopeids['C-0685-primary109']=[x['revision_id'] for x in load(C)['objects']]
assert len(scopeids['C-0044-prior-pointer'])==111 and len(scopeids['C-0563-prior-pointer'])==103
assert len(scopeids['C-0561-no-pointer'])==571 and len(scopeids['C-0106-no-pointer'])==114
del scopeids['C-0561-no-pointer']
assert set().union(*map(set,scopeids.values()))<=set(native)
targets=set().union(*map(set,scopeids.values()))
receipts={};candidates={};inputbindings={};cache={}
def cached(p):
 key=str(p)
 if key not in cache:cache[key]=load(p)
 return cache[key]
def claims(doc):return {k:v for k,v in doc.items() if k in ['scope','status','method','coverage','read_scope','verification','whole_reading','reading','checks','limits','pending','retains_context']} if isinstance(doc,dict) else {}
def ownwalk(x,ptr,rp,parent,parentptr,inputpin=None):
 if isinstance(x,dict):
  rid=x.get('revision_id',x.get('id'))
  api_snapshot=isinstance(rid,str) and '@' not in rid and isinstance(x.get('expectedVersion'),int) and isinstance(x.get('data'),dict) and 'caveat' in x
  if api_snapshot:rid=rid+'@'+str(x['expectedVersion'])
  if rid in targets and isinstance(x.get('data'),dict) and 'caveat' in x:
   predicates={k:v for k,v in parent.items() if k in ['disposition','decision','reason','rationale','review','judgment','full_native_read','full_current_data_and_caveat_read','source_disposition','whole_native_fields_read']} if isinstance(parent,dict) else {}
   if inputpin is not None or predicates:
    candidates.setdefault(rid,[]).append({'own_receipt_pin':rp,'snapshot_input_pin':inputpin or rp,'snapshot_pointer':ptr,'literal_individual_assertion':predicates,'individual_assertion_pointer':parentptr,'literal_own_reading_scope':claims(receipts[rp['path']]),'snapshot':x,'native_API_projection_required':api_snapshot})
  for k,v in x.items():
   if isinstance(v,(dict,list)):ownwalk(v,ptr+'/'+esc(k),rp,x,ptr,inputpin)
 elif isinstance(x,list):
  for i,v in enumerate(x):
   if isinstance(v,(dict,list)):ownwalk(v,ptr+'/'+str(i),rp,v if isinstance(v,dict) else parent,ptr+'/'+str(i),inputpin)
# Bind actual paths+hashes, including legacy input+sha schema, and selected input hashes.
selected={sha(p):p for p in (B/'preparation/selected').glob('*source-relevant-current-context*.json')}
for p in sorted((B/'fresh-independent-review').glob('*.json')):
 if any(s in p.name for s in ['semantic-scan','expanded-military-scan','search-input','exact-routing-for-own','routing-for-own-prior','resumed-C0425-expanded69-exact-whole-current-reuse']):continue
 doc=cached(p);rp=pin(p);receipts[str(p)]=doc;ownwalk(doc,'',rp,None,'')
 def refs(x,ptr):
  if isinstance(x,dict):
   for k in ['path','input','source','source_path']:
    q=resolve(x.get(k))
    if not q or q.suffix!='.json' or not q.exists():continue
    for hk in ['sha256','input_sha256','source_sha256']:
     h=x.get(hk)
     if isinstance(h,str) and h==sha(q) and (str(q).startswith(str(B/'source-review')) or str(q).startswith(str(B/'preparation/selected')) or q.name=='C-0069-outside-selected-semantic-search-input-v1.json'):
      inputbindings.setdefault(str(q),[]).append({'own_receipt_pin':rp,'own_input_pin_pointer':ptr,'literal_own_reading_scope':claims(doc),'input_pin':pin(q)})
   for k,v in x.items():
    if k in ['input_sha256','source_input_sha256','selected_input_sha256'] and isinstance(v,str) and v in selected:
     q=selected[v];inputbindings.setdefault(str(q),[]).append({'own_receipt_pin':rp,'own_input_pin_pointer':ptr+'/'+esc(k),'literal_own_reading_scope':claims(doc),'input_pin':pin(q),'binding':'exact input SHA uniquely identifies preserved selected input'})
    if isinstance(v,(dict,list)):refs(v,ptr+'/'+esc(k))
  elif isinstance(x,list):
   for i,v in enumerate(x):
    if isinstance(v,(dict,list)):refs(v,ptr+'/'+str(i))
 refs(doc,'')
# Explicit complete selected-reading enumerations: exact hash, ID, and index.
for receiptpath,doc in receipts.items():
 rp=pin(Path(receiptpath));hs=[doc.get(k) for k in ['input_sha256','source_input_sha256','selected_input_sha256']];qs=[selected[h] for h in hs if isinstance(h,str) and h in selected]
 for q in qs:
  sd=cached(q)
  for key in ['read_complete_selected_objects','coverage','objects','full_read_revisions']:
   arr=doc.get(key)
   if not isinstance(arr,list):continue
   for i,row in enumerate(arr):
    if isinstance(row,str) and key=='full_read_revisions':row={'revision_id':row,'index':doc.get('indices',[None]*len(arr))[i]}
    if not isinstance(row,dict):continue
    rid=row.get('revision_id',row.get('id',row.get('object')));index=row.get('index')
    if rid in targets and index is None and key=='objects' and isinstance(row.get('disposition'),str) and row['disposition'] not in ['recorded','accepted','rejected','pending']:
     positions=[j for j,x in enumerate(sd.get('objects',[])) if x.get('revision_id',x.get('id'))==rid]
     if len(positions)==1:index=positions[0]
    if rid not in targets or not isinstance(index,int) or index<0 or index>=len(sd.get('objects',[])):continue
    cur=sd['objects'][index]
    if cur.get('revision_id',cur.get('id'))!=rid:continue
    explicit=key in ['read_complete_selected_objects','full_read_revisions'] or (key=='objects' and 'read whole body,caveat' in str(doc.get('scope','')) and isinstance(row.get('disposition'),str)) or (key=='coverage' and isinstance(doc.get('status'),str) and 'ALL327SELECTED WHOLE OBJECTS READ' in doc['status'])
    if not explicit:continue
    candidates.setdefault(rid,[]).append({'own_receipt_pin':rp,'snapshot_input_pin':pin(q),'snapshot_pointer':'/objects/'+str(index),'literal_individual_assertion':{'selected_reading_enumeration':row,'whole_selected_reading_scope':doc.get('reading_note',doc.get('status')),'parent_array_key':key},'individual_assertion_pointer':'/'+key+'/'+str(i),'literal_own_reading_scope':claims(doc),'snapshot':cur,'direct_exact_individual_reading_predicate':True,'whole_metadata_scope_not_inferred':True})
# Exact individual own row plus a complete pinned native input, never blanket dictionary credit.
for receiptpath,doc in receipts.items():
 rp=pin(Path(receiptpath));inputpin=doc.get('native_input_pin',doc.get('native_dictionary_pin',doc.get('input_pin')))
 if not isinstance(inputpin,dict):continue
 q=resolve(inputpin.get('path'))
 if not q or not q.exists() or sha(q)!=inputpin.get('sha256'):continue
 def direct(x,ptr):
  if isinstance(x,dict):
   rid=x.get('revision_id');sptr=x.get('native_pointer',x.get('full_native_pointer'))
   reading=x.get('whole_current_data_and_caveat_read') is True or x.get('full_data_and_caveat_read') is True or x.get('full_current_data_and_caveat_read') is True or x.get('exact_full_current_data_caveat_reuse') is True
   assertion={k:v for k,v in x.items() if k in ['disposition','rationale','reason','whole_current_data_and_caveat_read','full_native_metadata_read','full_data_and_caveat_read','full_current_data_and_caveat_read','full_metadata_read','exact_full_current_data_caveat_reuse','own_prior_receipt','own_prior_pointer','C0561_scope_reassessment','metadata_credit_inferred']}
   if rid in targets and reading and isinstance(sptr,str) and 'disposition' in assertion:
    try:payload=getptr(cached(q),sptr)
    except KeyError:
     assert sptr=='/objects/'+rid and rid in cached(q)['objects'];payload=cached(q)['objects'][rid];assert payload['id']==rid;sptr='/objects/'+esc(rid)
    assert payload.get('id',payload.get('revision_id'))==rid
    candidates.setdefault(rid,[]).append({'own_receipt_pin':rp,'snapshot_input_pin':pin(q),'snapshot_pointer':sptr,'literal_individual_assertion':assertion,'individual_assertion_pointer':ptr,'literal_own_reading_scope':claims(doc),'snapshot':payload,'direct_exact_individual_reading_predicate':True})
   for key,val in x.items():
    if isinstance(val,(dict,list)):direct(val,ptr+'/'+esc(key))
  elif isinstance(x,list):
   for i,val in enumerate(x):
    if isinstance(val,(dict,list)):direct(val,ptr+'/'+str(i))
 direct(doc,'')
for path,bindings in inputbindings.items():
 for binding in bindings:ownwalk(cached(path),'',binding['own_receipt_pin'],None,'',binding['input_pin'])
out={};counts={}
for scope,ids in scopeids.items():
 result=[]
 for rid in ids:
  base=native[rid];comp=[];seen=set()
  for s in candidates.get(rid,[]):
   key=(s['own_receipt_pin']['path'],s['snapshot_input_pin']['path'],s['snapshot_pointer'])
   if key in seen:continue
   seen.add(key);a=copy.deepcopy(s['snapshot']);projection={'current':a.pop('current',None),'origin_extensions':[]}
   for origin in a.get('origins',[]):projection['origin_extensions'].append({k:origin.pop(k) for k in ['document_path','start_line','end_line','raw'] if k in origin})
   identity=a.pop('revision_id',None)
   if identity is not None:assert identity==rid
   if 'id' not in a and identity is not None:a['id']=identity
   equalfields={k:a[k]==v for k,v in base.items() if k in a}
   if s.get('native_API_projection_required'):
    projected_native_data={k:json.loads(v) if k.endswith('_json') and isinstance(v,str) else v for k,v in base['data'].items() if k!='revision_id'}
    equalfields['data']=a['data']==projected_native_data
    projection['explicit_native_data_to_API_projection']={'omit_only_revision_id':True,'parse_only_native_JSONtext_fields':[k for k,v in base['data'].items() if k.endswith('_json') and isinstance(v,str)],'ordered_arrays_preserved':True,'native_identity_version_equals_API_expectedVersion':a['id']==rid.rsplit('@',1)[0] and a['expectedVersion']==int(rid.rsplit('@',1)[1])}
   missing={k:v for k,v in base.items() if k not in a};differences=[{'field':k,'own_exact_value':a[k],'frozen_exact_value':base.get(k)} for k in a if a[k]!=base.get(k)]
   comp.append({**{k:v for k,v in s.items() if k!='snapshot'},'whole_data_and_caveat_exact_equal':equalfields.get('data',False) and equalfields.get('caveat',False),'all_present_native_field_equalities':equalfields,'missing_native_fields_exact_values':missing,'all_remaining_field_differences':differences,'explicit_presentation_projection':projection,'identity_wrapper_revision_id_mapped_to_id':identity,'whole_native_ordered_equal':a==base,'own_reading_assertion_scope_requires_individual_reviewer_confirmation':True,'no_metadata_or_sourcecredit_inferred':True})
  result.append({'revision_id':rid,'frozen_current_pointer':'/objects/'+esc(rid),'own_reading_comparisons':comp,'at_least_one_exact_whole_data_and_caveat_locator':any(z['whole_data_and_caveat_exact_equal'] for z in comp),'at_least_one_exact_whole_native_locator':any(z['whole_native_ordered_equal'] for z in comp)})
 out[scope]=result;counts[scope]={'remaining_scope_targets':len(result),'exact_whole_data_caveat_locator':sum(x['at_least_one_exact_whole_data_and_caveat_locator'] for x in result),'exact_whole_native_locator':sum(x['at_least_one_exact_whole_native_locator'] for x in result),'no_exact_whole_data_caveat_locator':sum(not x['at_least_one_exact_whole_data_and_caveat_locator'] for x in result)}
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
rp=save('five-scope-exact-own-current-field-reading-locators-v9.json',{'task':'T-0780','routing_pin':pin(N),'frozen_native_pins':nativepins,'already_own_reviewed_exclusion_pins':exclusionpins,'counts':counts,'scopes':out,'no_sourcegrade_or_readcredit_automatically_granted':True,'all_native_and_structured_array_order_preserved':True})
pp=save('five-scope-mechanical-current-field-join-production-v9.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result_pin':rp,'counts':counts,'own_receipts_pinned':len(receipts),'source_specific_saved_input_dictionaries_pinned':len(inputbindings),'elapsed_seconds':time.time()-START,'failed_attempts':[],'stage_canonical_probe':'UNRUN','actual_model_usage':'Root collects after worker final; unknown here'})
print(json.dumps({'result':rp,'production':pp,'counts':counts},indent=2))
