"""Mechanical exact receipt/payload join; never source approval or read credit."""
import copy
import datetime
import hashlib
import json
import re
import sqlite3
import time
from pathlib import Path

START=time.time()
B=Path('evaluations/T-0780')
W=B/'implementation/resumed-current126-independent-receipt-join-v1'
MP=B/'implementation/resumed-two-marriage-path-residual-queue-v1/current126-candidate-membership-inventory-v1.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
cache={}
def load(p):
 p=str(p)
 if p not in cache:cache[p]=json.loads(Path(p).read_text())
 return cache[p]
assert sha(MP)=='0523725227af7b0e02dcd93e474706248a6ad80f459c83cb9d0e344e6a52cec5'
m=load(MP);members=m['candidate_members'];assert len(members)==126
refs=[];hashonly=[];objectrows=[];snapshots={};receiptpins=[]
def resolve(s):
 if not isinstance(s,str):return None
 p=Path(s)
 if p.is_absolute() or s.startswith('evaluations/'):return str(p)
 if s.startswith(('implementation/','source-review/','fresh-independent-review/')):return str(B/p)
 return None
def ptrkey(s):return str(s).replace('~','~0').replace('/','~1')
def walk(x,ptr,pin):
 if isinstance(x,dict):
  for k in ['path','actual_path','operation_path','candidate_path','file','new_path','old_path']:
   path=resolve(x.get(k))
   if path:
    keys=['sha256','actual_sha256','operation_sha256','candidate_sha256']
    if k in ['new_path','old_path']:keys.append(k.removesuffix('_path')+'_sha256')
    for h in keys:
     if isinstance(x.get(h),str) and re.fullmatch('[0-9a-f]{64}',x[h]):refs.append({'receipt_pin':pin,'json_pointer':ptr,'resolved_path':path,'declared_sha256':x[h]})
  if isinstance(x.get('object_id'),str):objectrows.append({'receipt_pin':pin,'json_pointer':ptr,'row':x})
  needed={'id','object_id','version','disposition','evidence_status','rationale','caveat','kind','data','origins','evidence'}
  if needed<=set(x) and isinstance(x['data'],dict):snapshots.setdefault(x['id'],[]).append({'receipt_pin':pin,'json_pointer':ptr,'snapshot':x})
  for k,v in x.items():
   p=ptr+'/'+ptrkey(k)
   if isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v):
    path=resolve(k)
    if path:refs.append({'receipt_pin':pin,'json_pointer':p,'resolved_path':path,'declared_sha256':v})
    else:hashonly.append({'receipt_pin':pin,'json_pointer':p,'sha256':v})
   walk(v,p,pin)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,ptr+'/'+str(i),pin)
for p in sorted((B/'fresh-independent-review').rglob('*.json')):
 pin={'path':str(p),'sha256':sha(p)};receiptpins.append(pin);walk(load(p),'',pin)
for r in refs:
 p=Path(r['resolved_path']);r['file_exists']=p.exists();r['actual_file_sha256']=sha(p) if p.is_file() else None;r['declared_hash_matches_file']=r['actual_file_sha256']==r['declared_sha256'];r['structural_type']='non_operation_or_missing'
 if p.is_file() and p.suffix=='.json':
  try:
   d=load(p)
   if isinstance(d,dict) and isinstance(d.get('id'),str) and isinstance(d.get('changes'),list):r['structural_type']='actual_operation';r['operation_id']=d['id'];r['target_ids']=[x['id'] for x in d['changes']]
  except (json.JSONDecodeError,KeyError):r['structural_type']='nonparseable_input'
# Explicit reviewer preservation is pertarget, never a whole renewed op grade.
presp=B/'fresh-independent-review/resumed-eleven-plus-two-whole-member-preservation-v1.json'
assert sha(presp)=='beeafc6920dc67d9e86a8fbb8c4fd906c2df44bb66bd632eed088ed53d286982'
pres=load(presp);reuses={}
for i,row in enumerate(pres['rows']):
 assert sha(row['old_path'])==row['old_sha256'] and sha(row['new_path'])==row['new_sha256']
 old=load(row['old_path']);new=load(row['new_path']);assert [x['id'] for x in old['changes']]==[x['id'] for x in new['changes']]
 for oid in row['unchanged_whole_payloads']:
  a=next(x for x in old['changes'] if x['id']==oid);z=next(x for x in new['changes'] if x['id']==oid);assert a==z
  reuses[oid]={'reviewer_preservation_pin':{'path':str(presp),'sha256':sha(presp)},'json_pointer':'/rows/'+str(i),'old_path':row['old_path'],'old_sha256':row['old_sha256'],'new_path':row['new_path'],'new_sha256':row['new_sha256'],'full_API_payload_exact_unchanged':True,'sourcecredit_requires_prior_individual_receipt':True}
assert len(reuses)==13
c=sqlite3.connect('file:'+str((B/'preparation/baseline-j281.sqlite').resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
def native(rid):
 z=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone()
 if not z:return None
 n=dict(z);n['data']=dict(c.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone());n['origins']=[dict(z) for z in c.execute('select * from origin where revision_id=?',(rid,))];n['evidence']=[dict(z) for z in c.execute('select * from dependency where revision_id=?',(rid,))];return n
result=[];targets_count=0;missingpins=0;uncoveredtargets=0
for member in members:
 assert sha(member['path'])==member['sha256'];op=load(member['path']);exact=[r for r in refs if r['resolved_path']==member['path'] and r['declared_sha256']==member['sha256'] and r['declared_hash_matches_file'] and r['structural_type']=='actual_operation'];missingpins+=not bool(exact);per=[]
 for i,x in enumerate(op['changes']):
  targets_count+=1;oid=x['id'];assert hashlib.sha256(canon(x).encode()).hexdigest()==member['targets'][i]['payload_sha256'];readrows=[]
  for rr in objectrows:
   row=rr['row']
   if row['object_id']!=oid:continue
   path=resolve(row.get('actual_path'))
   currentpath=path==member['path'];index=row.get('actual_change_index');indexequal=index is None or index==i
   # Assertions retained literally for reviewer, not upgraded to sourceapproval.
   assertion={k:v for k,v in row.items() if not isinstance(v,(dict,list)) and k not in ['old','new','body','markdown','text','description','caveat']}
   readrows.append({'receipt_pin':rr['receipt_pin'],'json_pointer':rr['json_pointer'],'actual_member_path_equal':currentpath,'actual_index_equal_or_unspecified':indexequal,'literal_review_assertions':assertion})
  rid=oid+'@'+str(x['expectedVersion']) if x['expectedVersion'] is not None else None;baseline=native(rid) if rid else None;comparisons=[]
  for snap in snapshots.get(rid,[]):
   ss=snap['snapshot'];ordered=all(ss[k]==v for k,v in baseline.items());restore=copy.deepcopy(ss);restore['evidence']=baseline['evidence'];multiset=sorted(map(canon,ss['evidence']))==sorted(map(canon,baseline['evidence'])) and all(restore[k]==v for k,v in baseline.items())
   comparisons.append({'receipt_pin':snap['receipt_pin'],'json_pointer':snap['json_pointer'],'full_native_baseline_ordered_equal':ordered,'full_native_evidence_multiset_only':multiset and not ordered,'not_new_candidate_sourceapproval':True})
  reuse=reuses.get(oid);priorpins=[]
  if reuse:
   priorpins=[r for r in refs if r['resolved_path']==reuse['old_path'] and r['declared_sha256']==reuse['old_sha256'] and r['declared_hash_matches_file'] and r['structural_type']=='actual_operation']
  assertions=[r for r in readrows if r['actual_member_path_equal'] and r['actual_index_equal_or_unspecified']]
  explicituncovered=not assertions and not reuse;uncoveredtargets+=explicituncovered
  per.append({'target_id':oid,'native_expected_version':x['expectedVersion'],'actual_change_index':i,'actual_payload_sha256':member['targets'][i]['payload_sha256'],'whole_native_snapshot_receipt_comparisons':comparisons,'whole_snapshot_equality_unavailable':not comparisons,'actual_target_review_row_pointers':readrows,'unchanged_API_reuse_proof':reuse,'prior_unchanged_operation_receipt_pointers':priorpins,'no_explicit_latest_individual_review_row_or_preservation_pointer':explicituncovered,'no_source_readcredit_grade_inferred':True})
 result.append({'current_member':member,'exact_current_operation_receipt_path_hash_pointers':exact,'missing_exact_current_operation_pin':not bool(exact),'per_target':per,'hash_only_mentions_not_operation_binding':[r for r in hashonly if r['sha256']==member['sha256']],'no_global_or_wholemember_sourcecredit':True})
assert targets_count==830
assert not W.exists();W.mkdir()
def save(n,z):
 p=W/n;assert not p.exists();p.write_text(json.dumps(z,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
rp=save('per-current126-operation-and-target-receipt-join-v1.json',{'task':'T-0780','rules':'Exact structured actualoperation path AND byteSHA; pins, literal targetassertions, embedded native snapshot equality and explicit unchanged API proofs kept separate. None alone grants sourceapproval or readcredit. No hash-only/stringmention credit.','members':result,'no_blanket1494coverage':True})
ip=save('exact-review-receipt-input-index-v1.json',{'membership_pin':{'path':str(MP),'sha256':sha(MP)},'review_receipt_pins':receiptpins,'explicit_structured_path_hash_pairs':refs,'reviewer_preservation_pin':{'path':str(presp),'sha256':sha(presp)}})
pp=save('bounded-current126-review-join-production-receipt-v1.json',{'task':'T-0780','saved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result_pin':rp,'input_index_pin':ip,'members':126,'targets':830,'members_with_exact_structured_operation_receipt_pins':126-missingpins,'members_missing_exact_structured_operation_receipt_pins':missingpins,'targets_without_explicit_latest_individual_row_or_preservation_pointer':uncoveredtargets,'review_json_receipts_pinned':len(receiptpins),'thirteen_API_reuses_verified':len(reuses),'status':'MECHANICAL_ROUTING_NOT_SOURCE_APPROVAL','failed_attempts':[],'elapsed_seconds':time.time()-START,'stage_canonical_probe':'UNRUN','actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'production':pp,'exact_current_memberpins':126-missingpins,'missing_memberpins':missingpins,'targets_without_latestrow_or_preservation':uncoveredtargets,'result':rp},indent=2))
