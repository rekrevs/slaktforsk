"""Exact own saved reading field locator: ID/version, whole data+caveat minimum; no grades."""
import json,hashlib,copy,re,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-four-scope-own-current-field-join-v1'
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
exclude={};exclusionpins=[]
for name,scope in [('resumed-C0044-first18-other-context-independent-dispositions-v1.json','C-0044'),('resumed-C0044-next26-other-context-independent-dispositions-v1.json','C-0044'),('resumed-C0044-seventeen-P0050-current-retains-v1.json','C-0044'),('resumed-C0561-seventynine-homonym-context-exclusions-v1.json','C-0561')]:
 p=B/'fresh-independent-review'/name;d=load(p);exclusionpins.append(pin(p));exclude.setdefault(scope,set()).update(x['revision_id'] for x in d['objects'])
exclude['C-0044'].update(['CONTRACT-P-0050-PK-03@2','THEME-P-0050-BO@2'])
scopeids={scope:[r['revision_id'] for r in nr if any(a['scope']==scope for a in r['routing_aliases']) and r['revision_id'] not in exclude.get(scope,set())] for scope in ['C-0044','C-0563','C-0561','C-0106']};targets=set().union(*map(set,scopeids.values()))
receipts={};candidates={};inputbindings={};cache={}
def cached(p):
 key=str(p)
 if key not in cache:cache[key]=load(p)
 return cache[key]
def claims(doc):return {k:v for k,v in doc.items() if k in ['scope','status','method','coverage','read_scope','verification','whole_reading','reading','checks','limits','pending','retains_context']} if isinstance(doc,dict) else {}
def ownwalk(x,ptr,rp,parent,parentptr,inputpin=None):
 if isinstance(x,dict):
  rid=x.get('revision_id',x.get('id'))
  if rid in targets and isinstance(x.get('data'),dict) and 'caveat' in x:
   predicates={k:v for k,v in parent.items() if k in ['disposition','decision','reason','rationale','review','judgment','full_native_read','full_current_data_and_caveat_read','source_disposition','whole_native_fields_read']} if isinstance(parent,dict) else {}
   if inputpin is not None or predicates:
    candidates.setdefault(rid,[]).append({'own_receipt_pin':rp,'snapshot_input_pin':inputpin or rp,'snapshot_pointer':ptr,'literal_individual_assertion':predicates,'individual_assertion_pointer':parentptr,'literal_own_reading_scope':claims(receipts[rp['path']]),'snapshot':x})
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
    if k=='input_sha256' and v in selected:
     q=selected[v];inputbindings.setdefault(str(q),[]).append({'own_receipt_pin':rp,'own_input_pin_pointer':ptr+'/'+esc(k),'literal_own_reading_scope':claims(doc),'input_pin':pin(q),'binding':'exact input SHA uniquely identifies preserved selected input'})
    if isinstance(v,(dict,list)):refs(v,ptr+'/'+esc(k))
  elif isinstance(x,list):
   for i,v in enumerate(x):
    if isinstance(v,(dict,list)):refs(v,ptr+'/'+str(i))
 refs(doc,'')
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
   equalfields={k:a[k]==v for k,v in base.items() if k in a};missing={k:v for k,v in base.items() if k not in a};differences=[{'field':k,'own_exact_value':a[k],'frozen_exact_value':base.get(k)} for k in a if a[k]!=base.get(k)]
   comp.append({**{k:v for k,v in s.items() if k!='snapshot'},'whole_data_and_caveat_exact_equal':equalfields.get('data',False) and equalfields.get('caveat',False),'all_present_native_field_equalities':equalfields,'missing_native_fields_exact_values':missing,'all_remaining_field_differences':differences,'explicit_presentation_projection':projection,'identity_wrapper_revision_id_mapped_to_id':identity,'whole_native_ordered_equal':a==base,'own_reading_assertion_scope_requires_individual_reviewer_confirmation':True,'no_metadata_or_sourcecredit_inferred':True})
  result.append({'revision_id':rid,'frozen_current_pointer':'/objects/'+esc(rid),'own_reading_comparisons':comp,'at_least_one_exact_whole_data_and_caveat_locator':any(z['whole_data_and_caveat_exact_equal'] for z in comp),'at_least_one_exact_whole_native_locator':any(z['whole_native_ordered_equal'] for z in comp)})
 out[scope]=result;counts[scope]={'remaining_scope_targets':len(result),'exact_whole_data_caveat_locator':sum(x['at_least_one_exact_whole_data_and_caveat_locator'] for x in result),'exact_whole_native_locator':sum(x['at_least_one_exact_whole_native_locator'] for x in result),'no_exact_whole_data_caveat_locator':sum(not x['at_least_one_exact_whole_data_and_caveat_locator'] for x in result)}
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
rp=save('four-scope-exact-own-current-field-reading-locators-v1.json',{'task':'T-0780','routing_pin':pin(N),'frozen_native_pin':pin(F),'already_own_reviewed_exclusion_pins':exclusionpins,'counts':counts,'scopes':out,'no_sourcegrade_or_readcredit_automatically_granted':True,'all_native_and_structured_array_order_preserved':True})
pp=save('four-scope-mechanical-current-field-join-production-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result_pin':rp,'counts':counts,'own_receipts_pinned':len(receipts),'source_specific_saved_input_dictionaries_pinned':len(inputbindings),'elapsed_seconds':time.time()-START,'failed_attempts':[],'stage_canonical_probe':'UNRUN','actual_model_usage':'Root collects after worker final; unknown here'})
print(json.dumps({'result':rp,'production':pp,'counts':counts},indent=2))
