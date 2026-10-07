import json,pathlib,hashlib,re,time,collections
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/current121-independent-operation-pin-inventory-v1';w.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();load=lambda p:json.loads(pathlib.Path(p).read_text())
def save(n,x):
 p=w/n;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
mp=b/'implementation/C0069-six-older-source-metadata-queue-v1/current121-candidate-membership-inventory-v1.json';membership=load(mp);members=membership['candidate_members'];assert len(members)==121
inputs=w/'frozen-inputs';inputs.mkdir();pins=[];refs=[];hashonly=[]
def resolve(s):
 p=pathlib.Path(s)
 if p.is_absolute():return p
 if s.startswith('evaluations/'):return p
 if s.startswith(('implementation/','source-review/','fresh-independent-review/')):return b/p
 return None
def record(path,h,ptr,pin):
 p=resolve(path)
 if p is not None:refs.append({'receipt_pin':pin,'json_pointer':ptr,'declared_path':path,'resolved_path':str(p),'declared_sha256':h})
def walk(x,ptr,pin):
 if isinstance(x,dict):
  for key in ['path','actual_path','operation_path','candidate_path','file']:
   if isinstance(x.get(key),str):
    for hk in ['sha256','actual_sha256','operation_sha256','candidate_sha256']:
     if isinstance(x.get(hk),str) and re.fullmatch('[0-9a-f]{64}',x[hk]):record(x[key],x[hk],ptr,pin)
  for k,v in x.items():
   if isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v):
    if resolve(k) is not None:record(k,v,ptr+'/'+k.replace('~','~0').replace('/','~1'),pin)
    else:hashonly.append({'receipt_pin':pin,'json_pointer':ptr+'/'+k,'sha256':v,'no_explicit_path_pair':True})
   walk(v,ptr+'/'+str(k).replace('~','~0').replace('/','~1'),pin)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,ptr+'/'+str(i),pin)
for i,p in enumerate(sorted((b/'fresh-independent-review').rglob('*.json'))):
 h=sha(p);cp=inputs/(str(i).zfill(3)+'-'+p.name);cp.write_bytes(p.read_bytes());assert sha(cp)==h;pin={'path':str(p),'sha256':h,'frozen_path':str(cp)};pins.append(pin);walk(load(cp),'',pin)
# Classification by actual JSON structure, never receipt filename or grade words.
for r in refs:
 p=pathlib.Path(r['resolved_path']);r['file_exists']=p.exists();r['actual_file_sha256']=sha(p) if p.exists() else None;r['declared_hash_matches_file']=r['actual_file_sha256']==r['declared_sha256'];r['structural_type']='missing_or_non_operation_input'
 if p.exists() and p.suffix=='.json':
  try:
   obj=load(p)
   if isinstance(obj,dict) and isinstance(obj.get('changes'),list) and isinstance(obj.get('id'),str):r['structural_type']='actual_operation_file';r['operation_id']=obj['id'];r['target_ids']=[x['id'] for x in obj['changes']]
   else:r['structural_type']='source_raw_current_reading_or_other_nonoperation_file'
  except (ValueError,KeyError):r['structural_type']='nonparseable_input'
rows=[];missing=0
for i,m in enumerate(members):
 p=pathlib.Path(m['path']);assert sha(p)==m['sha256'];op=load(p);ids={x['id'] for x in op['changes']};cp=inputs/('member-'+str(i).zfill(3)+'-'+p.name);cp.write_bytes(p.read_bytes());assert sha(cp)==m['sha256']
 exact=[r for r in refs if r['resolved_path']==str(p) and r['declared_sha256']==m['sha256'] and r['declared_hash_matches_file'] and r['structural_type']=='actual_operation_file']
 samehashother=[r for r in refs if r['declared_sha256']==m['sha256'] and r['resolved_path']!=str(p)]
 other=[r for r in refs if r['structural_type']=='actual_operation_file' and r['declared_sha256']!=m['sha256'] and ids.intersection(r.get('target_ids',[]))]
 missing+=not exact
 rows.append({'current_member':m,'frozen_operation_path':str(cp),'whole_actual_operation_payload':op,'exact_current_path_and_hash_receipt_pointers':exact,'same_hash_other_path_not_exact_path_binding':samehashother,'older_or_other_overlapping_target_operation_pins_not_automatically_superseded':other,'hash_only_mentions_not_operation_binding':[r for r in hashonly if r['sha256']==m['sha256']],'missing_exact_current_operation_receipt_pin':not bool(exact),'no_grade_approval_or_read_credit_inferred':True})
result=save('per-current121-member-exact-receipt-pointers-and-missing-bindings-v1.json',{'rules':'Match exact resolved actual operation path AND SHA only. Structural operation must have id and changes. Source/raw/current-reading inputs separated structurally, not by receipt name, review wording, counts or grade. Older overlapping-target operation pins listed but not assumed formally superseded. Hash-only or same-hash-other-path mentions distinct. No PASS/coverage/approval inference.','members':rows,'all_explicit_receipt_path_hash_pairs':refs,'all_hash_only_mentions':hashonly})
idx=save('frozen-review-and-membership-input-index-v1.json',{'membership_pin':{'path':str(mp),'sha256':sha(mp),'full_membership':membership},'review_receipt_pins':pins})
r=save('bounded-operation-pin-inventory-production-receipt-v1.json',{'membership_pin':{'path':str(mp),'sha256':sha(mp)},'result_pin':result,'input_index_pin':idx,'members':121,'targets':817,'members_with_exact_path_hash_receipt_pins':121-missing,'members_missing_exact_path_hash_receipt_pins':missing,'review_json_receipts_frozen':len(pins),'explicit_path_hash_pairs':len(refs),'failed_attempts':[],'elapsed_seconds':time.time()-start,'no_source_independent_approval_or_grade_inferred':True,'no_candidate_stage_apply_or_diagnostic_changes':True});print(json.dumps(r))
