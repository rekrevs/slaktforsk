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
W=B/'implementation/resumed-current132-independent-receipt-join-v4'
MP=B/'implementation/resumed-P0069-military-path-qualification-queue-v1/current132-candidate-membership-inventory-v1.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
cache={}
def load(p):
 p=str(p)
 if p not in cache:cache[p]=json.loads(Path(p).read_text())
 return cache[p]
assert sha(MP)=='5ced9d896f7dea1a7af707dc613e4fc84c7699c131e03bd40aec064387ac4058'
m=load(MP);members=m['candidate_members'];assert len(members)==132
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
  for k in ['path','actual_path','operation_path','candidate_path','file','new_path','old_path','candidate']:
   path=resolve(x.get(k))
   if path:
    keys=['sha256','actual_sha256','operation_sha256','candidate_sha256']
    if k in ['new_path','old_path','candidate']:keys.append(k.removesuffix('_path')+'_sha256')
    for h in keys:
     if isinstance(x.get(h),str) and re.fullmatch('[0-9a-f]{64}',x[h]):refs.append({'receipt_pin':pin,'json_pointer':ptr,'resolved_path':path,'declared_sha256':x[h]})
  if isinstance(x.get('object_id',x.get('id')),str):objectrows.append({'receipt_pin':pin,'json_pointer':ptr,'row':x})
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
# Whole-operation hash schemas require structured operation_sha256, unique exact
# current operation, complete matching pertarget IDs/versions and explicit reading assertion.
for pin in receiptpins:
 doc=load(pin['path'])
 if not isinstance(doc,dict):continue
 h=doc.get('operation_sha256');matching=[z for z in members if z['sha256']==h]
 if len(matching)!=1:continue
 member=matching[0];op=load(member['path']);rows=doc.get('dispositions',[])
 if not isinstance(rows,list) or not rows:continue
 actual=[(x['id'],x['expectedVersion']) for x in op['changes']]
 declared=[(x.get('id'),x.get('expectedVersion')) for x in rows if isinstance(x,dict)]
 readassertion=doc.get('full_payload_read') is True or any(isinstance(doc.get(k),str) and doc[k] for k in ['read_method','reading_method'])
 if actual==declared and readassertion:
  refs.append({'receipt_pin':pin,'json_pointer':'/operation_sha256','resolved_path':member['path'],'declared_sha256':h,'file_exists':True,'actual_file_sha256':sha(member['path']),'declared_hash_matches_file':True,'structural_type':'actual_operation','operation_id':op['id'],'target_ids':[x['id'] for x in op['changes']],'binding_schema':'unique actual structured operation SHA + complete ordered ID/version dispositions + explicit reading assertion'})
# Enumerate literal operation-level attestations separately, never infer source grades.
operationattestations=[]
for pin in receiptpins:
 doc=load(pin['path'])
 if not isinstance(doc,dict):continue
 exactdoc=[r for r in refs if r['receipt_pin']==pin and r['structural_type']=='actual_operation' and r['declared_hash_matches_file']]
 for r in exactdoc:
  claims=[]
  for key in ['full_payload_read','method','read_method','reading_method','verification','checks','coverage','reading','review','whole_reading','read_scope','all_four_actual_payloads_read_whole','actual_full_reconstruction','actual_complete_reconstruction','whole_actual_verification','all_complete_actual_reconstructions_exact','actual_operation_bindings','actual_bindings','preserved']:
   v=doc.get(key)
   if isinstance(v,(str,dict,list)) or v is True:claims.append({'json_pointer':'/'+key,'literal_value':v})
  if claims:operationattestations.append({'receipt_pin':pin,'operation_path':r['resolved_path'],'operation_sha256':r['declared_sha256'],'pin_pointer':r['json_pointer'],'literal_reading_assertions':claims,'not_automatically_sourceapproval_or_alltarget_credit':True})
# Native pertarget actual reconstruction schemas may use string IDs instead of rows.
# Keep literal scoped claims and exact operation associations, never infer a grade.
for pin in receiptpins:
 doc=load(pin['path'])
 if not isinstance(doc,dict):continue
 for key in ['actual_complete_reconstruction','actual_full_reconstruction','objects','all_changes_read']:
  arr=doc.get(key)
  if not isinstance(arr,list):continue
  for i,v in enumerate(arr):
   if isinstance(v,str):
    oid,sep,version=v.rpartition('@')
    row={'object_id':oid if sep and version.isdigit() else v,'version':int(version) if sep and version.isdigit() else None,'literal_schema_array_key':key,'literal_value':v}
    objectrows.append({'receipt_pin':pin,'json_pointer':'/'+key+'/'+str(i),'row':row})
 # Preserve all top-level literal actual/full assertions for reviewer scope confirmation.
 for key,v in doc.items():
  if isinstance(v,str) and re.search(r'(actual|API)',v,re.I) and re.search(r'(whole|full|complete|reconstruct|rebuilt|byte.identical)',v,re.I):
   for r in refs:
    if r['receipt_pin']==pin and r['structural_type']=='actual_operation' and r['declared_hash_matches_file']:
     operationattestations.append({'receipt_pin':pin,'operation_path':r['resolved_path'],'operation_sha256':r['declared_sha256'],'pin_pointer':r['json_pointer'],'literal_reading_assertions':[{'json_pointer':'/'+key,'literal_value':v}],'literal_scope_requires_reviewer_confirmation':True,'not_automatically_sourceapproval_or_alltarget_credit':True})
# Compare every exact same-receipt prior/current operation target overlap.
# Output full field differences and exact API equality; renewal requires earlier reading.
renewals={};renewalrecords=[]
for member in members:
 currentop=load(member['path'])
 currentrefs=[r for r in refs if r['resolved_path']==member['path'] and r['declared_sha256']==member['sha256'] and r['structural_type']=='actual_operation' and r['declared_hash_matches_file']]
 for currentref in currentrefs:
  for oldref in refs:
   if oldref['receipt_pin']!=currentref['receipt_pin'] or oldref['resolved_path']==member['path'] or oldref['structural_type']!='actual_operation' or not oldref['declared_hash_matches_file']:continue
   oldop=load(oldref['resolved_path']);older={x['id']:x for x in oldop['changes']}
   for i,x in enumerate(currentop['changes']):
    if x['id'] not in older:continue
    previous=older[x['id']]
    if previous.get('expectedVersion')!=x['expectedVersion']:continue
    differences=[]
    def diff(a,z,path=''):
     if isinstance(a,dict) and isinstance(z,dict):
      for key in sorted(set(a)|set(z)):
       if key not in a or key not in z:differences.append({'field':path+'/'+ptrkey(key),'old_present':key in a,'new_present':key in z,'old':a.get(key),'new':z.get(key)})
       else:diff(a[key],z[key],path+'/'+ptrkey(key))
     elif a!=z:differences.append({'field':path,'old':a,'new':z})
    diff(previous,x)
    prior_receipt_refs=[r for r in refs if r['resolved_path']==oldref['resolved_path'] and r['declared_sha256']==oldref['declared_sha256'] and r['declared_hash_matches_file'] and r['structural_type']=='actual_operation' and r['receipt_pin']!=currentref['receipt_pin']]
    rec={'target_id':x['id'],'actual_change_index':i,'current_operation_pin':{'path':member['path'],'sha256':member['sha256']},'renewal_receipt_pin':currentref['receipt_pin'],'current_pin_pointer':currentref['json_pointer'],'prior_operation_pin':{'path':oldref['resolved_path'],'sha256':oldref['declared_sha256']},'prior_pin_pointer':oldref['json_pointer'],'whole_API_exact_unchanged':previous==x,'all_actual_full_field_differences':differences,'earlier_exact_operation_review_bindings':prior_receipt_refs,'prior_actual_reading_still_mandatory':True,'no_scope_or_sourcecredit_inferred':True}
    renewalrecords.append(rec);renewals.setdefault(x['id'],[]).append(rec)
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
   if row.get('object_id',row.get('id'))!=oid:continue
   path=resolve(row.get('actual_path'))
   docpins=[r for r in exact if r['receipt_pin']==rr['receipt_pin']]
   currentpath=path==member['path'] or bool(docpins)
   index=row.get('actual_change_index')
   if index is None and isinstance(row.get('actual_pointer'),str) and re.fullmatch('/changes/[0-9]+',row['actual_pointer']):index=int(row['actual_pointer'].split('/')[-1])
   indexequal=index is None or index==i
   version=row.get('expectedVersion',row.get('expected_version',row.get('version')))
   versionequal=version is None or version==x['expectedVersion']
   currentpath=currentpath and versionequal
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
  wholeattestations=[a for a in operationattestations if a['operation_path']==member['path'] and a['operation_sha256']==member['sha256']]
  explicituncovered=not assertions and not reuse and not wholeattestations;uncoveredtargets+=explicituncovered
  if reuse:
   earlier=next(q for q in load(reuse['old_path'])['changes'] if q['id']==oid);assert earlier==x
   reuse=copy.deepcopy(reuse);reuse['exact_latest_API_equal_prior_payload']=True
  per.append({'target_id':oid,'native_expected_version':x['expectedVersion'],'actual_change_index':i,'actual_payload_sha256':member['targets'][i]['payload_sha256'],'whole_native_snapshot_receipt_comparisons':comparisons,'whole_snapshot_equality_unavailable':not comparisons,'actual_target_review_row_pointers':readrows,'unchanged_API_reuse_proof':reuse,'exact_operation_literal_reading_attestations':wholeattestations,'prior_unchanged_operation_receipt_pointers':priorpins,'actual_prior_current_payload_renewal_chains':renewals.get(oid,[]),'no_explicit_latest_individual_review_row_or_preservation_pointer':explicituncovered,'no_source_readcredit_grade_inferred':True})
 result.append({'current_member':member,'exact_current_operation_receipt_path_hash_pointers':exact,'missing_exact_current_operation_pin':not bool(exact),'per_target':per,'hash_only_mentions_not_operation_binding':[r for r in hashonly if r['sha256']==member['sha256']],'no_global_or_wholemember_sourcecredit':True})
assert targets_count==843
assert not W.exists();W.mkdir()
def save(n,z):
 p=W/n;assert not p.exists();p.write_text(json.dumps(z,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
rp=save('per-current132-operation-and-target-receipt-join-v1.json',{'task':'T-0780','rules':'Exact structured actualoperation path AND byteSHA, or unique structured operation SHA plus complete ordered ID/version dispositions and explicit reading assertion; pins, literal targetassertions, embedded native snapshot equality and explicit unchanged API proofs kept separate. None alone grants sourceapproval or readcredit. No hash-only/stringmention credit.','members':result,'no_blanket1494coverage':True})
ip=save('exact-review-receipt-input-index-v1.json',{'membership_pin':{'path':str(MP),'sha256':sha(MP)},'review_receipt_pins':receiptpins,'explicit_structured_path_hash_pairs':refs,'literal_operation_reading_attestations':operationattestations,'actual_prior_current_API_renewal_chains':renewalrecords,'reviewer_preservation_pin':{'path':str(presp),'sha256':sha(presp)}})
pp=save('bounded-current132-review-join-production-receipt-v1.json',{'task':'T-0780','saved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result_pin':rp,'input_index_pin':ip,'members':132,'targets':843,'members_with_exact_structured_operation_receipt_pins':132-missingpins,'members_missing_exact_structured_operation_receipt_pins':missingpins,'targets_without_explicit_latest_individual_row_or_preservation_pointer':uncoveredtargets,'review_json_receipts_pinned':len(receiptpins),'thirteen_API_reuses_verified':len(reuses),'status':'MECHANICAL_ROUTING_NOT_SOURCE_APPROVAL','failed_attempts':[],'elapsed_seconds':time.time()-START,'stage_canonical_probe':'UNRUN','actual_model_usage':'Root collects after final; unknown here'})
print(json.dumps({'production':pp,'exact_current_memberpins':132-missingpins,'missing_memberpins':missingpins,'targets_without_latestrow_or_preservation':uncoveredtargets,'result':rp},indent=2))
