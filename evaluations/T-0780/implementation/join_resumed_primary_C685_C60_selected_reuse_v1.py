"""Mechanical primary-Astra decision/input join: exact field values and retained scopes, no grades."""
import json,hashlib,copy,re,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-primary-C685-C60-selected-reuse-join-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(k):return str(k).replace('~','~0').replace('/','~1')
def getptr(doc,ptr):
 for token in ptr.lstrip('/').split('/') if ptr else []:
  token=token.replace('~1','/').replace('~0','~');doc=doc[int(token)] if isinstance(doc,list) else doc[token]
 return doc
cache={}
def cached(p):
 key=str(p)
 if key not in cache:cache[key]=load(p)
 return cache[key]
native={};nativeptr={};nativepins=[]
for name in ['current-full-native-objects-v1.json','additional-context-full-native-objects-v2.json']:
 p=B/'implementation/dependency-preparation-v1'/name;d=cached(p);nativepins.append(pin(p))
 for oid,x in d['objects'].items():
  if x['id'] in native:assert native[x['id']]==x
  native[x['id']]=x;nativeptr[x['id']]={'input_pin':pin(p),'pointer':'/objects/'+esc(oid)}
H=B/'source-review/consequences-two/C-0685-source-consequence-handoff-v6.json';h=cached(H);assert len(h['expanded_routing_dispositions'])==448
S=B/'preparation/selected/C-0060-semantic-consequence-input-v1.json';s=cached(S);assert len(s['candidates'])==168
groups={'C0685-routing448':[(x['revision_id'],{'input_pin':pin(H),'pointer':'/expanded_routing_dispositions/'+str(i),'original_routing_disposition':x}) for i,x in enumerate(h['expanded_routing_dispositions'])],'C0060-semantic168':[(x['revision_id'],{'input_pin':pin(S),'pointer':'/candidates/'+str(i)}) for i,x in enumerate(s['candidates'])]}
for cid,n in [('C-0561',288),('C-0060',61),('C-0563',327)]:
 p=B/'preparation/selected'/f'{cid}-source-relevant-current-context-v1.json';d=cached(p);assert len(d['objects'])==n,(cid,len(d['objects']));groups[cid+'-selected'+str(n)]=[(x['revision_id'],{'input_pin':pin(p),'pointer':'/objects/'+str(i)}) for i,x in enumerate(d['objects'])]
targets={rid for g in groups.values() for rid,_ in g};assert targets<=set(native),targets-set(native)
D=B/'implementation/five-expanded-exactnative-pointer-join-v2/deduplicated-full-source-decision-contexts-v1.json';contexts=cached(D)['contexts'];bindings={};seen=set()
def project(cur):
 a=copy.deepcopy(cur);removed={'current':a.pop('current',None),'origin_extensions':[]}
 for origin in a.get('origins',[]):removed['origin_extensions'].append({k:origin.pop(k) for k in ['document_path','start_line','end_line','raw'] if k in origin})
 rid=a.pop('revision_id',None)
 if rid is not None and 'id' not in a:a['id']=rid
 return a,removed
def add(rid,cur,meta):
 if rid not in targets or not isinstance(cur,dict):return
 a,removed=project(cur);base=native[rid];eq={k:a[k]==v for k,v in base.items() if k in a};missing={k:v for k,v in base.items() if k not in a};diff=[{'field':k,'prior_source_snapshot_exact_value':a[k],'current_exact_value':base.get(k)} for k in a if a[k]!=base.get(k)]
 key=(rid,meta['source_pin']['path'],meta['decision_pointer'],meta.get('snapshot_pointer'))
 if key in seen:return
 seen.add(key);bindings.setdefault(rid,[]).append({**meta,'strict_whole_native_equal':cur==base,'ordered_whole_native_equal_after_only_explicit_presentation_projection':a==base,'exact_whole_data_caveat_equal':eq.get('data',False) and eq.get('caveat',False),'exact_ordered_evidence_equal':eq.get('evidence',False),'actual_field_equalities':eq,'missing_native_fields_full_exact_values':missing,'all_remaining_full_field_differences':diff,'projected_presentation_exact_values':removed,'no_read_scope_enlargement_or_sourceapproval_inferred':True})
for key,c in contexts.items():
 x=c['full_context']
 if not isinstance(x,dict):continue
 cur=x.get('current',x.get('full_current',x.get('current_full_object')))
 if not isinstance(cur,dict):continue
 rid=cur.get('revision_id',cur.get('id'))
 if rid not in targets:continue
 disposition=x.get('disposition',x.get('decision'))
 if not isinstance(disposition,str) or 'routing_only' in disposition or disposition in ['recorded','accepted','rejected','pending']:continue
 add(rid,cur,{'source_pin':c['source_pin'],'decision_pointer':c['json_pointer'],'snapshot_pointer':c['json_pointer']+'/'+next(k for k in ['current','full_current','current_full_object'] if k in x),'explicit_primary_disposition':disposition,'explicit_primary_rationale':x.get('rationale',x.get('reason')),'declared_scope_literal':x.get('scope'),'governing_edits':x.get('edits'),'source_context_key':key})
# Later decisions after the prior context dictionary, and five finite indices.
finitepins=[]
for p in sorted((B/'source-review').glob('resumed-*.json')):
 doc=cached(p)
 if not isinstance(doc,dict):continue
 if 'finite-fullscope-source-index' in p.name or p.name=='resumed-C0425-outside215-source-disposition-index-v1.json':finitepins.append(pin(p))
 def walk(x,ptr,parent,parentptr):
  if isinstance(x,dict):
   cur=x.get('current')
   if isinstance(cur,dict):
    rid=cur.get('revision_id',cur.get('id'));disposition=x.get('disposition')
    if isinstance(disposition,str) and 'routing' not in disposition:add(rid,cur,{'source_pin':pin(p),'decision_pointer':ptr,'snapshot_pointer':ptr+'/current','explicit_primary_disposition':disposition,'explicit_primary_rationale':x.get('rationale'),'declared_scope_literal':doc.get('scope'),'governing_edits':x.get('edits')})
   rid=x.get('revision_id')
   if rid in targets and isinstance(x.get('disposition'),str) and ('finite-fullscope-source-index' in p.name or p.name=='resumed-C0425-outside215-source-disposition-index-v1.json'):
    joined=x.get('source_join_pointer');fullptr=x.get('full_native_pointer')
    payload=None;sptr=None;spin=None
    if isinstance(joined,dict):
     q=Path(joined['path']);row=getptr(cached(q),joined['json_pointer']);key='no_pointer_full_residual_object';payload=row.get(key)
     if payload is None:
      fk=row.get('full_native_dictionary_key');q2=B/'implementation/five-expanded-exactnative-pointer-join-v2/full-frozen-native-residual-dictionary-v1.json';payload=cached(q2)['objects'][fk];spin=pin(q2);sptr='/objects/'+esc(fk)
     else:spin=pin(q);sptr=joined['json_pointer']+'/'+key
    elif isinstance(fullptr,dict):
     q=Path(fullptr['path']);payload=getptr(cached(q),fullptr['pointer']);spin=pin(q);sptr=fullptr['pointer']
    if payload is not None:add(rid,payload,{'source_pin':pin(p),'decision_pointer':ptr,'snapshot_input_pin':spin,'snapshot_pointer':sptr,'explicit_primary_disposition':x['disposition'],'explicit_primary_rationale':x.get('rationale',x.get('current_scope_rationale')),'reading_level_literal':x.get('reading_level'),'declared_scope_literal':doc.get('scope'),'mandatory_latest_overlay_pointer':x.get('primary_decision'),'prior_substantive_decision_pointers':x.get('reused_substantive_source_decisions'),'finite_current_reading_not_blanket_wholemetadata_credit':True})
   for k,v in x.items():
    if isinstance(v,(dict,list)):walk(v,ptr+'/'+esc(k),x,ptr)
  elif isinstance(x,list):
   for i,v in enumerate(x):
    if isinstance(v,(dict,list)):walk(v,ptr+'/'+str(i),x,ptr)
 walk(doc,'',None,'')
out={};counts={}
for name,rows in groups.items():
 result=[]
 for rid,routing in rows:
  b=bindings.get(rid,[]);result.append({'revision_id':rid,'routing_input_pointer':routing,'complete_locked_native_input_pointer':nativeptr[rid],'explicit_primary_source_decision_field_bindings':b,'exact_whole_data_caveat_prior_primary_binding':any(x['exact_whole_data_caveat_equal'] for x in b),'exact_whole_data_caveat_and_ordered_evidence_prior_primary_binding':any(x['exact_whole_data_caveat_equal'] and x['exact_ordered_evidence_equal'] for x in b),'ordered_fullnative_primary_binding':any(x['ordered_whole_native_equal_after_only_explicit_presentation_projection'] for x in b),'no_explicit_primary_binding':not b})
 out[name]=result;counts[name]={'routing_targets':len(result),'exact_whole_data_caveat':sum(x['exact_whole_data_caveat_prior_primary_binding'] for x in result),'exact_whole_data_caveat_ordered_evidence':sum(x['exact_whole_data_caveat_and_ordered_evidence_prior_primary_binding'] for x in result),'ordered_fullnative':sum(x['ordered_fullnative_primary_binding'] for x in result),'without_explicit_primary_decision_binding':sum(x['no_explicit_primary_binding'] for x in result)}
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
rp=save('primary-C685448-C60168-and-selected-exact-source-field-reuse-v1.json',{'task':'T-0780','primary_context_dictionary_pin':pin(D),'locked_native_dictionary_pins':nativepins,'new_primary_finite_index_pins':finitepins,'counts':counts,'groups':out,'rules':'Primary Astra decisions only. Routing-only never source approval. All actual equality/missing fields/order/presentation omissions explicit; prior stated field/time/source scopes and latest overlays remain mandatory. Independent receipts do not grant primary approval.'})
pp=save('bounded-primary-reuse-join-production-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result_pin':rp,'counts':counts,'unique_routing_native_targets':len(targets),'elapsed_seconds':time.time()-START,'failed_attempts':[],'stage_canonical_probe':'UNRUN','actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'result':rp,'production':pp,'counts':counts},indent=2))
