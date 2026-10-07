import json,pathlib,hashlib,copy,collections,time
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0069-wide1059-projection-differences-v2';w.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();tablep=b/'implementation/C0069-wide1059-source-input-match-v1/individual-wide1059-exact-source-match-and-differences-v1.json';widep=b/'source-review/consequences-two/C-0069-complete-native-routing-dedup-v1.jsonl';table=json.load(open(tablep));wide={x['id']:x for x in map(json.loads,widep.open())};cache={};group=collections.Counter();remaininggroup=collections.Counter();rows=[];ordered=0;edgeonly=0;unresolved=0;pointercount=0
originextras={'document_path','start_line','end_line','raw'}
def pointed(p):
 file=p['source_path']
 if file not in cache:
  assert sha(file)==p['source_sha256'];cache[file]=json.load(open(file))
 x=cache[file]
 for key in p['json_pointer'].split('/')[1:]:
  key=key.replace('~1','/').replace('~0','~');x=x[int(key)] if isinstance(x,list) else x[key]
 return x
def project(x,other):
 z=copy.deepcopy(x);removed=[]
 if 'current' in z:removed.append({'path':'/current','value':z.pop('current')})
 for i,o in enumerate(z.get('origins',[])):
  for k in originextras:
   if k in o:removed.append({'path':'/origins/'+str(i)+'/'+k,'value':o.pop(k)})
 for field in ['assets']:
  for i,o in enumerate(z.get(field,[])):
   native=other.get(field,[])
   if i>=len(native):continue
   for k in ['sha256','bytes']:
    if k in o and k not in native[i]:removed.append({'path':'/'+field+'/'+str(i)+'/'+k,'value':o.pop(k)})
 return z,removed
def diff(a,z,path=''):
 if type(a)!=type(z):return [{'path':path,'difference':'type','wide_type':type(a).__name__,'source_type':type(z).__name__}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(z)):
   p=path+'/'+k
   if k not in a:out.append({'path':p,'difference':'source_extra_key','source':z[k]})
   elif k not in z:out.append({'path':p,'difference':'source_missing_key','wide':a[k]})
   else:out.extend(diff(a[k],z[k],p))
  return out
 if isinstance(a,list):
  out=[]
  if len(a)!=len(z):out.append({'path':path,'difference':'array_length','wide_length':len(a),'source_length':len(z)})
  for i,(x,y) in enumerate(zip(a,z)):out.extend(diff(x,y,path+'/'+str(i)))
  return out
 return [] if a==z else [{'path':path,'difference':'value','wide':a,'source':z}]
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
for row in table['rows']:
 if not row['same_revision_non_equal_source_pointers']:continue
 obj=wide[row['revision_id']];comparisons=[];hasordered=False;hasedge=False
 for original in row['same_revision_non_equal_source_pointers']:
  pointercount+=1;source=pointed(original['pointer']);assert obj!=source
  for d in original['differences']:group[d['path']]+=1
  projected,removed=project(source,obj);projectwide,removedwide=project(obj,source);remaining=diff(projectwide,projected)
  for d in remaining:remaininggroup[d['path']]+=1
  equal=projectwide==projected;edges_equal=collections.Counter(map(canon,projectwide.get('evidence',[])))==collections.Counter(map(canon,projected.get('evidence',[])));noedgeswide=copy.deepcopy(projectwide);noedgeswide.pop('evidence',None);noedgessource=copy.deepcopy(projected);noedgessource.pop('evidence',None);edge_only=not equal and edges_equal and noedgeswide==noedgessource;hasordered|=equal;hasedge|=edge_only
  comparisons.append({'source_pointer':original['pointer'],'strict_full_equal':False,'persisted_projection_ordered_full_equal':equal,'evidence_edge_multiset_equal_with_duplicate_counts':edges_equal,'evidence_array_order_equal':projectwide.get('evidence')==projected.get('evidence'),'evidence_order_only_difference_after_projection':edge_only,'classification':'projected_ordered_full_equal' if equal else 'evidence_order_only_not_ordered_equal' if edge_only else 'remaining_native_differences','removed_source_enrichment_fields':removed,'removed_wide_enrichment_fields':removedwide,'all_remaining_exact_differences':remaining,'full_projected_source_payload':projected,'source_decision_pointer_only_no_judgment':True})
 rows.append({'revision_id':obj['id'],'full_wide_native_payload':obj,'full_projected_wide_native_payload':projectwide,'strict_match_pointers_preserved':row['exact_full_native_equal_source_pointers'],'per_pointer_comparisons':comparisons,'requires_primary_decision_no_read_credit':True});ordered+=hasordered;edgeonly+=not hasordered and hasedge;unresolved+=not hasordered and not hasedge
assert len(rows)==459
rules={'only_ignored_fields':['top-level current','origins/*/document_path','origins/*/start_line','origins/*/end_line','origins/*/raw','assets/*/sha256 and bytes ONLY when corresponding native attachment lacks those keys'],'always_preserved':'Every native header/data/JSONembedded array, origin array order/native fields, evidence role/note/duplicate edge counts, asset/media array order. No whole-key/path/basis substitution. Dictionary key serialization order only ignored.','evidence_order':'Separate edge multiset equality may explain a difference, NEVER ordered full equality or source approval.'}
def save(n,d):
 p=w/n;assert not p.exists();p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
mp=save('individual459-persisted-projection-and-all-remaining-differences-v2.json',{'projection_rules':rules,'objects':rows});gp=save('exact-JSON-path-difference-groups-v2.json',{'original_path_counts':dict(sorted(group.items())),'remaining_after_projection_path_counts':dict(sorted(remaininggroup.items()))});r=save('bounded-projection-input-output-production-receipt-v2.json',{'input_pins':[{'path':str(p),'sha256':sha(p)} for p in [tablep,widep]],'source_files_verified_pins':[{'path':p,'sha256':sha(p)} for p in sorted(cache)],'individual_fullpayload_output_pin':mp,'path_groups_pin':gp,'projection_rules':rules,'same_revision_objects':459,'pointer_comparisons':pointercount,'objects_with_at_least_one_projected_ordered_full_equal':ordered,'objects_without_orderedmatch_with_evidence_order_only_equivalence':edgeonly,'objects_without_projected_or_edgeorder_only_match':unresolved,'strict77matches_prior_unmodified':True,'unmatched982_original_fullobjects_unmodified_traceable':True,'source_dispositions_read_credit_not_adjudicated':True,'failed_attempts':[],'elapsed_seconds':time.time()-start,'model_usage_root_collect_after_final':True,'no_stage_apply_rebind_actual328_modification':True});print({'receipt':r,'full_output':mp,'groups':gp,'ordered':ordered,'edgeonly':edgeonly,'unresolved':unresolved,'pointers':pointercount})
