"""Mechanical own-review input locator and ordered full-native equality, no grades."""
import json,hashlib,copy,datetime,time
from pathlib import Path
START=time.time();B=Path('evaluations/T-0780');W=B/'implementation/resumed-C0425-remaining59-own-prior-input-join-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def esc(k):return str(k).replace('~','~0').replace('/','~1')
R=B/'fresh-independent-review/resumed-C0425-remaining59-exact-routing-for-own-prior-join-v1.json';assert sha(R)=='9e778d8446f051f8c4ce0a47e10dca6a92b6c299026ebd2dd954825991fcbe83'
F=B/'implementation/five-expanded-exactnative-pointer-join-v2/full-frozen-native-residual-dictionary-v1.json';assert sha(F)=='8ec9b8a2f55b70f72a4ef140896b20553ff84dd0addad6490083a0901ed0ddc0'
rows=load(R)['objects'];assert len(rows)==59;native=load(F)['objects'];targets={r['revision_id'] for r in rows}
I=B/'implementation/resumed-current130-independent-receipt-join-v2/exact-review-receipt-input-index-v1.json';index=load(I)
refs=[r for r in index['explicit_structured_path_hash_pairs'] if Path(r['resolved_path']).suffix=='.json' and r['declared_hash_matches_file'] and r['structural_type']!='actual_operation' and any(s in Path(r['receipt_pin']['path']).name for s in ['C-0425','C-0069','resumed-eleven']) and (r['resolved_path'].startswith(str(B/'source-review')) or Path(r['resolved_path']).name=='C-0069-outside-selected-semantic-search-input-v1.json')]
byinput={}
for r in refs:byinput.setdefault(r['resolved_path'],[]).append(r)
snaps={};assertions={}
for path,rs in byinput.items():
 p=Path(path);d=load(p)
 for r in rs:
  doc=load(r['receipt_pin']['path']);claims=[]
  if isinstance(doc,dict):
   for key in ['coverage','method','verification','whole_reading','whole_current_read','reading','read_method','checks','review','scope']:
    if key in doc:claims.append({'pointer':'/'+key,'literal_value':doc[key]})
  assertions[r['receipt_pin']['path']]=claims
 def walk(x,ptr):
  if isinstance(x,dict):
   rid=x.get('id');needed={'id','object_id','version','kind','data','evidence','origins','disposition','evidence_status','rationale','caveat'}
   if rid in targets and needed<=set(x):snaps.setdefault(rid,[]).append({'input_pin':pin(p),'input_pointer':ptr,'own_review_input_pin_bindings':rs,'snapshot':x})
   for k,v in x.items():
    if isinstance(v,(dict,list)):walk(v,ptr+'/'+esc(k))
  elif isinstance(x,list):
   for i,v in enumerate(x):
    if isinstance(v,(dict,list)):walk(v,ptr+'/'+str(i))
 walk(d,'')
out=[];equalcount=0
for r in rows:
 rid=r['revision_id'];base=native[rid];comparisons=[]
 for s in snaps.get(rid,[]):
  actual=copy.deepcopy(s['snapshot']);omissions={'current':actual.pop('current',None),'origin_extensions':[]}
  for origin in actual['origins']:
   omitted={k:origin.pop(k) for k in ['document_path','start_line','end_line','raw'] if k in origin};omissions['origin_extensions'].append(omitted)
  equal=actual==base;diff=[]
  for k in sorted(set(actual)|set(base)):
   if actual.get(k)!=base.get(k):diff.append({'field':k,'own_saved_input_exact_value':actual.get(k),'frozen_current_exact_value':base.get(k),'present_in_own_input':k in actual,'present_in_frozen':k in base})
  comparisons.append({**{k:v for k,v in s.items() if k!='snapshot'},'whole_native_ordered_equal_after_only_declared_presentation_projection':equal,'projection_exact_removed_values':omissions,'all_remaining_full_field_differences':diff,'own_literal_reading_assertions':[{'receipt_pin':v['receipt_pin'],'assertions':assertions[v['receipt_pin']['path']]} for v in s['own_review_input_pin_bindings']],'no_sourcegrade_or_readcredit_inferred':True})
 anyequal=any(x['whole_native_ordered_equal_after_only_declared_presentation_projection'] for x in comparisons);equalcount+=anyequal
 out.append({'revision_id':rid,'C425_index':r['C425_index'],'frozen_current_pointer':'/objects/'+esc(rid),'own_prior_input_comparisons':comparisons,'at_least_one_exact_own_pinned_input_full_native_equality':anyequal,'unmatched_full_native_equality_explicit':not anyequal,'primary_routing_used_for_target_ID_only':True})
assert not W.exists();W.mkdir()
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
rp=save('remaining59-exact-own-reading-input-locator-and-fullnative-equality-v1.json',{'task':'T-0780','routing_pin':pin(R),'frozen_current_pin':pin(F),'own_review_reference_index_pin':pin(I),'objects':out,'no_individual_disposition_or_sourceapproval':True,'whole_native_arrays_order_preserved':True})
pp=save('bounded-remaining59-own-input-join-production-v1.json',{'task':'T-0780','result_pin':rp,'targets':59,'targets_with_exact_ordered_full_native_own_pinned_input':equalcount,'unmatched_targets':59-equalcount,'source_specific_pinned_inputs_searched':len(byinput),'failed_prep_attempts':[{'error':'KeyError reading_snapshot_pointer in ad hoc source grouping','candidate_or_DB_writes':False},{'error':'UnicodeDecodeError from image routing pin; repaired exact .json input filter before writes','candidate_or_DB_writes':False}],'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.time()-START,'stage_canonical_probe':'UNRUN','actual_model_usage':'Root collects after worker final; unknown here'})
print(json.dumps({'result':rp,'production':pp,'exact':equalcount,'unmatched':59-equalcount},indent=2))
