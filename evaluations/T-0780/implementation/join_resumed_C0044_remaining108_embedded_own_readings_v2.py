"""Own embedded native and semantic snapshots, exact equality and scope pointers only."""
import json,hashlib,copy,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-C0044-remaining108-own-prior-input-join-v2'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(k):return str(k).replace('~','~0').replace('/','~1')
R=B/'implementation/resumed-C0044-remaining108-exact-own-prior-routing-v1.json';assert sha(R)=='4e580e7a3897fd0e95768e9a1bfc9ed08c93e7fcd9cb88a2fcc06c3f10fe0fc1'
F=B/'implementation/five-expanded-exactnative-pointer-join-v2/full-frozen-native-residual-dictionary-v1.json';assert sha(F)=='8ec9b8a2f55b70f72a4ef140896b20553ff84dd0addad6490083a0901ed0ddc0'
rows=load(R)['objects'];targets={x['revision_id'] for x in rows};native=load(F)['objects'];snaps={};semantic={'object_id','kind','disposition','evidence_status','rationale','caveat','data','evidence'}
receiptpins=[]
for p in sorted((B/'fresh-independent-review').glob('*.json')):
 if any(z in p.name for z in ['semantic-scan','search-input','routing-for-own','resumed-C0425-expanded69-exact-whole-current-reuse']):continue
 doc=load(p);pp=pin(p);receiptpins.append(pp)
 topclaims={k:v for k,v in doc.items() if k in ['status','scope','method','coverage','read_scope','verification','whole_reading','reading','checks','limits','pending']} if isinstance(doc,dict) else {}
 def walk(x,ptr,parent,parentptr):
  if isinstance(x,dict):
   rid=x.get('revision_id',x.get('id'))
   if rid in targets and semantic<=set(x):
    # Parent individual disposition/read assertion is required to distinguish own reading from scan routing.
    predicates={k:v for k,v in parent.items() if k in ['disposition','reason','rationale','decision','source_disposition','full_native_read','full_current_data_and_caveat_read','full_current_and_new_API_read','whole_native_fields_read','judgment']} if isinstance(parent,dict) else {}
    if predicates:snaps.setdefault(rid,[]).append({'receipt_pin':pp,'snapshot_pointer':ptr,'individual_assertion_pointer':parentptr,'literal_individual_reading_or_disposition':predicates,'literal_receipt_scope':topclaims,'snapshot':x})
   for k,v in x.items():
    if isinstance(v,(dict,list)):walk(v,ptr+'/'+esc(k),x,ptr)
  elif isinstance(x,list):
   for i,v in enumerate(x):
    if isinstance(v,(dict,list)):walk(v,ptr+'/'+str(i),v if isinstance(v,dict) else parent,ptr+'/'+str(i))
 walk(doc,'',None,'')
out=[];fullcount=0;semcount=0
for r in rows:
 rid=r['revision_id'];base=native[rid];cc=[]
 for s in snaps.get(rid,[]):
  actual=copy.deepcopy(s['snapshot']);removed={'current':actual.pop('current',None),'origin_extensions':[]}
  for o in actual.get('origins',[]):removed['origin_extensions'].append({k:o.pop(k) for k in ['document_path','start_line','end_line','raw'] if k in o})
  identity=actual.pop('revision_id',None)
  if identity is not None:assert identity==rid
  if 'id' not in actual and identity is not None:actual['id']=identity
  semequal=all(actual[k]==base[k] for k in semantic)
  missing={k:v for k,v in base.items() if k not in actual}
  differences=[{'field':k,'own_snapshot_exact_value':actual.get(k),'frozen_current_exact_value':base.get(k)} for k in sorted(set(actual)|set(base)) if k in actual and actual.get(k)!=base.get(k)]
  cc.append({**{k:v for k,v in s.items() if k!='snapshot'},'whole_native_exact_order_equal_after_explicit_presentation_projection':actual==base,'whole_semantic_fields_exact_order_equal':semequal,'semantic_fields_compared':sorted(semantic),'missing_native_wrapper_metadata_exact_values':missing,'all_other_exact_differences':differences,'identity_wrapper_revision_id_mapped_to_id':identity,'only_projected_presentation_values':removed,'no_new_read_or_sourcecredit_inferred':True})
 f=any(x['whole_native_exact_order_equal_after_explicit_presentation_projection'] for x in cc);sem=any(x['whole_semantic_fields_exact_order_equal'] for x in cc);fullcount+=f;semcount+=sem
 out.append({'revision_id':rid,'C44_index':r['C44_index'],'frozen_current_pointer':'/objects/'+esc(rid),'own_embedded_individual_reading_comparisons':cc,'exact_whole_native_own_embedded_reading_available':f,'exact_whole_semantic_own_embedded_reading_available':sem,'no_semantic_or_fullnative_equality_explicit':not sem})
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
rp=save('remaining108-exact-own-embedded-reading-and-semantic-field-equality-v2.json',{'task':'T-0780','routing_pin':pin(R),'frozen_current_pin':pin(F),'objects':out,'no_sourcegrading_or_new_sourceinterpretation':True,'scope_and_metadata_omissions_for_independent_reviewer':True})
pp=save('bounded-remaining108-own-embedded-reading-join-production-v2.json',{'task':'T-0780','result_pin':rp,'targets':108,'exact_fullnative':fullcount,'exact_fullsemantic':semcount,'neither':108-semcount,'own_receipt_pins_searched':receiptpins,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.time()-START,'failed_attempts':[],'stage_canonical_probe':'UNRUN','actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'result':rp,'production':pp,'fullnative':fullcount,'semantic':semcount,'neither':108-semcount},indent=2))
