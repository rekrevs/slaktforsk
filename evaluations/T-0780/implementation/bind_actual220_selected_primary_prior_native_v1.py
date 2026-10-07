"""Bounded exact220 selected source-prior snapshot/current bindings, no grades."""
import copy,datetime,hashlib,json
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
def get(x,p):
 for k in p.strip('/').split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
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
 v=x.get('revision_id',x.get('id',x.get('object_id')))
 if not isinstance(v,str):return None
 if '@' in v:return v
 ver=x.get('version',x.get('expectedVersion'))
 return v+'@'+str(ver) if isinstance(ver,int) else None
def path(v):
 if not isinstance(v,str):return None
 p=Path(v)
 if not p.is_absolute() and not v.startswith('evaluations/'):p=B/p
 return p if p.exists() and p.suffix=='.json' else None
def diff(a,b,p=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append({'field':p+'/'+k,'old_present':k in a,'new_present':k in b,'old':a.get(k),'new':b.get(k)})
   else:out.extend(diff(a[k],b[k],p+'/'+k))
  return out
 return [{'field':p,'old':a,'new':b,'array_order_preserved':True}]
def semantic(n,fields=None):
 d=n['data'] if isinstance(n.get('data'),dict) else {k:n[k] for k in fields if k in n}
 d={k:v for k,v in d.items() if k!='revision_id'}
 for k,v in d.items():
  if k.endswith('_json') and isinstance(v,str):d[k]=json.loads(v)
 return {'data':d,'caveat':n.get('caveat')}
def persisted(n,actual):
 rid_=actual['id'];d=copy.deepcopy(n);projection={};data=semantic(n,actual['data'])['data'];data['revision_id']=rid_
 out={k:d[k] for k in actual if k in d and k not in ['data','origins','evidence','assets','media']};out['data']=data
 if 'id' not in out and n.get('revision_id')==rid_:out['id']=rid_;projection['revision_id_wrapper_to_id']=True
 if not isinstance(n.get('data'),dict):projection['flattened_data_fields']=[k for k in actual['data'] if k!='revision_id']
 if 'origins' in n:
  out['origins']=[{'revision_id':rid_,'unit_id':o.get('unit_id',o.get('unit')),'coverage':o.get('coverage','partial'),'note':o.get('note','')} for o in n['origins']]
  projection['origin_enrichment_field_names_only']=[sorted(set(o)-{'revision_id','unit_id','unit','coverage','note'}) for o in n['origins']]
 if 'evidence' in n:
  out['evidence']=[{'revision_id':rid_,'basis_revision_id':e.get('basis_revision_id',e.get('object','')+'@'+str(e.get('version',''))),'role':e['role'],'note':e.get('note','')} for e in n['evidence']]
 if actual['kind']=='record':
  if 'assets' in n:out['assets']=[{'revision_id':rid_,'asset_path':a.get('asset_path',a.get('path')),'region':a.get('region','helbild')} for a in n['assets']]
  if 'media' in n or 'nativeAssets' in n:out['media']=[{'revision_id':rid_,'asset_id':a.get('asset_id',a.get('id')),'region':a.get('region','helbild')} for a in n.get('media',n.get('nativeAssets',[]))]
  projection['asset_shapes_mapped_to_exact_record_relation_columns']=True
 projection['rich_CLI_wrapper_fields_not_persisted_in_native']=[k for k in n if k not in actual and k not in actual['data']]
 return out,projection
T=Path('/tmp/t0780_220.json');target=load(T);assert len(target)==220
F=W/'primary-selected-actual220-prior-native-input-frozen-v1.json';assert not F.exists();F.write_bytes(T.read_bytes())
NP=W/'all-existing-actual-request-support-full-baseline-native-payloads-v1.json';baseline=load(NP)['objects'];AP=W/'all893-full-actual-native-targets-in-journal-insertion-order-v1.json';actual=load(AP)['objects'];alln={**baseline,**actual};default=load(S/'actual-handoff-v1/full-actual-request-current-and-direct-support-native-payloads-v1.json')['objects']
refs=[];out=[]
for i,row in enumerate(target):
 request=row['request']['actual_request'];r=request['affected_revision_id'];ac=row['request']['affected_latest_current_revision_id'];decision=row['prior_decision'];loc=row['selected_prior_locator'];sp=loc['source_pin'];assert sha(sp['path'])==sp['sha256'];assert get(load(sp['path']),loc['individual_context_pointer'])==decision
 candidates=[]
 # Embedded prior snapshot stays exactly in its original individual source row.
 for ptr,x in walk(decision):
  if isinstance(x,dict) and rid(x)==r and 'caveat' in x and (isinstance(x.get('data'),dict) or all(k in x for k in alln[r]['data'] if k!='revision_id')):candidates.append((sp,loc['individual_context_pointer']+ptr,x,'embedded_selected_prior'))
 # Exact selected reuse/source input pins, plus direct declared object indices.
 for ptr,x in walk(decision):
  if not isinstance(x,dict):continue
  for pk in ['path','input_path','source_path']:
   q=path(x.get(pk))
   if not q:continue
   h=x.get('sha256',x.get('input_sha256',x.get('source_sha256')))
   if not isinstance(h,str) or sha(q)!=h:continue
   d=load(q);idx=x.get('objects_index',x.get('object_index'));nptr=x.get('pointer',x.get('json_pointer',x.get('whole_native_input_pointer')))
   if isinstance(idx,int) and isinstance(d.get('objects'),list):
    node=d['objects'][idx];np='/objects/'+str(idx)
    for key in ['current','full_current','full_native']:
     if isinstance(node,dict) and isinstance(node.get(key),dict):node=node[key];np+='/'+key;break
    if isinstance(node,dict) and rid(node)==r and 'caveat' in node:candidates.append((pin(q),np,node,'exact_reuse_input_index'))
   if isinstance(nptr,str):
    try:node=get(d,nptr)
    except (KeyError,ValueError,TypeError):node=None
    if isinstance(node,dict) and rid(node)==r and 'caveat' in node:candidates.append((pin(q),nptr,node,'exact_reuse_input_pointer'))
   # Find only the exact immutable revision, not other payloads or guessed sources.
   for np,node in walk(d):
    if isinstance(node,dict) and rid(node)==r and 'caveat' in node and (isinstance(node.get('data'),dict) or all(k in node for k in alln[r]['data'] if k!='revision_id')):candidates.append((pin(q),np,node,'exact_ID_version_in_declared_reuse_input'))
 matches=[];seen=set()
 for ip,ptr,n,schema in candidates:
  key=(ip['path'],ptr)
  if key in seen:continue
  seen.add(key);actualn=alln[r];projected,projection=persisted(n,actualn);sem=diff(semantic(n,actualn['data']),semantic(actualn));persist_actual={k:v for k,v in actualn.items() if k in projected};persist_source=projected;pd=diff(persist_source,persist_actual)
  defn=default.get(r);defp={k:v for k,v in defn.items() if k in projected} if defn else None
  matches.append({'input_pin':ip,'snapshot_pointer':ptr,'schema':schema,'exact_immutable_ID_version':r,'full_data_caveat_equal_actual':not sem,'semantic_field_differences':sem,'all_present_persisted_native_fields_equal_rowid_order':not pd,'all_present_persisted_native_fields_equal_default_SQL_order':projected==defp if defp else None,'all_present_native_field_differences_in_rowid_order':pd,'missing_native_metadata_field_names':[k for k in actualn if k not in projected],'explicit_presentation_projection':projection,'no_unread_metadata_credit_inferred':True})
 hp=decision.get('whole_native_sha256');rawhashes={}
 if isinstance(hp,str):
  for name,n in [('rowid_order',alln[r]),('default_SQL_order',default.get(r))]:
   if n is not None:rawhashes[name]=hashlib.sha256(json.dumps(n,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==hp
 out.append({'actual_request_id':request['id'],'affected_revision_id':r,'actual_current_revision_id':ac,'selected_prior_locator':loc,'source_selected_prior_decision_exact_bound':True,'raw_canonical_native_hash_equalities':rawhashes,'exact_prior_snapshot_bindings':matches,'actual_current_is_exact_approved_target':ac in actual,'source_grading':'PENDING','no_match_is_not_semantic_difference_or_unread':True})
p=W/'actual220-selected-primary-prior-native-current-equality-bindings-v1.json';assert not p.exists();result={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_exact220_input_pin':pin(F),'baseline_native_pin':pin(NP),'actual893_native_pin':pin(AP),'objects':out,'counts':{'requests':len(out),'raw_hash_exact':sum(any(x['raw_canonical_native_hash_equalities'].values()) for x in out),'full_semantic_snapshot_equal':sum(any(m['full_data_caveat_equal_actual'] for m in x['exact_prior_snapshot_bindings']) for x in out),'actual_current_approved_API':sum(x['actual_current_is_exact_approved_target'] for x in out),'no_hash_or_semantic_snapshot_or_approved_API':[x['actual_request_id'] for x in out if not any(x['raw_canonical_native_hash_equalities'].values()) and not any(m['full_data_caveat_equal_actual'] for m in x['exact_prior_snapshot_bindings']) and not x['actual_current_is_exact_approved_target']]},'rules':'Source selected220 locators exact; canonical hash representation mismatch never implies a source field difference. Persisted projections and all array differences explicit. No grades/resolutions.'};p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result_pin':pin(p),'counts':{k:v for k,v in result['counts'].items() if not isinstance(v,list)},'unbound_requests':len(result['counts']['no_hash_or_semantic_snapshot_or_approved_API'])},indent=2))
