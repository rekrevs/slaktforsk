import json,pathlib,sqlite3,hashlib,time,collections
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/actual328-reuse-input-v1';w.mkdir(exist_ok=True);d=b/'diagnostic-C0685-C0563-28ops-v1'
def load(p):return json.load(open(p))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def write(n,x):p=w/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'path':str(p),'sha256':sha(p)}
c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
req=load(d/'actual-pending-review-requests-v1.json');native=load(d/'actual-review-request-full-native-dictionary-v1.json')['objects'];assert len(req)==328 and len(native)==343
seqp=b/'implementation/C0685-C0563-split-proposal-v2/concrete-sequence-and-preservation-receipt-v2.json';seq=load(seqp)['sequence'];candidates={};pins=[{'path':str(p),'sha256':sha(p)} for p in [d/'actual-pending-review-requests-v1.json',d/'actual-review-request-full-native-dictionary-v1.json',seqp]]
for s in seq:
 assert sha(s['path'])==s['sha256'];op=load(s['path']);pins.append({'path':s['path'],'sha256':s['sha256']})
 for i,ch in enumerate(op['changes']):candidates[ch['id']+'@'+str((ch['expectedVersion'] or 0)+1)]={'change':ch,'operation_id':op['id'],'path':s['path'],'pointer':'/changes/'+str(i),'sha256':s['sha256']}
def baseline(rid):
 row=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone()
 if not row:return None
 z=dict(row);z['data']=dict(c.execute('select * from '+z['kind']+' where revision_id=?',(rid,)).fetchone());z['origins']=[dict(v) for v in c.execute('select * from origin where revision_id=?',(rid,))];z['evidence']=[dict(v) for v in c.execute('select * from dependency where revision_id=? order by basis_revision_id,role',(rid,))]
 if z['kind']=='record':
  z['assets']=[dict(v) for v in c.execute('select * from record_asset where revision_id=?',(rid,))];z['media']=[dict(v) for v in c.execute('select * from record_media where revision_id=?',(rid,))]
 return z
def normalized(z):
 out={k:z.get(k) for k in ['id','object_id','version','operation_id','disposition','evidence_status','rationale','caveat','previous_id','kind']};out['data']={}
 for k,v in z['data'].items():
  if k=='revision_id':continue
  if k.endswith('_json') and isinstance(v,str):v=json.loads(v)
  out['data'][k]=v
 out['origins']=sorted([{'unit_id':v['unit_id'],'coverage':v['coverage'],'note':v['note']} for v in z['origins']],key=canon)
 out['evidence']=sorted([{'basis_revision_id':v['basis_revision_id'],'role':v['role'],'note':v['note']} for v in z['evidence']],key=canon)
 for key in ['assets','media']:
  if key in z:out[key]=[{k:v for k,v in a.items() if k!='revision_id'} for a in z[key]]
 return out
def expected(ch,opid,rid):
 z={'id':rid,'object_id':ch['id'],'version':(ch['expectedVersion'] or 0)+1,'operation_id':opid,'disposition':ch['disposition'],'evidence_status':ch['evidenceStatus'],'rationale':ch['rationale'],'caveat':ch['caveat'],'previous_id':ch['id']+'@'+str(ch['expectedVersion']) if ch['expectedVersion'] else None,'kind':ch['kind'],'data':ch['data'],'origins':[{'unit_id':v['unit'],'coverage':v['coverage'],'note':v['note']} for v in ch['origins']],'evidence':[{'basis_revision_id':v['object']+'@'+str(v['version']),'role':v['role'],'note':v['note']} for v in ch['evidence']]}
 if ch['kind']=='record':z['assets']=[{'asset_path':v['path'],'region':v['region']} for v in ch.get('assets',[])];z['media']=[{'asset_id':v['id'],'region':v['region']} for v in ch.get('media',[])]
 return normalized(z)
# Only durable individual decision containers; references do not mean whole-payload approval.
index=collections.defaultdict(list)
def walk(x,path,pointer=''):
 if isinstance(x,dict):
  cur=x.get('current');edge=x.get('edge');rid=cur.get('id') if isinstance(cur,dict) else None
  if rid and any(k in x for k in ['disposition','decision','edits','rationale','action']):
   index[rid].append({'path':str(path),'sha256':sha(path),'pointer':pointer,'decision_keys':[k for k in ['disposition','decision','action','rationale','reason'] if k in x], 'current_full_payload_normalized_sha256':digest(normalized(cur)) if all(k in cur for k in ['data','origins','evidence']) and all('unit_id' in v for v in cur['origins']) and all('basis_revision_id' in v for v in cur['evidence']) else None,'individual_edge':edge,'pointer_only_not_new_approval':True})
  for k,v in x.items():
   if k not in ['current','data','origins','evidence']:walk(v,path,pointer+'/'+str(k))
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path,pointer+'/'+str(i))
for p in sorted((b/'source-review').rglob('*.json')):
 if 'decision' in p.name or 'disposition' in p.name or p.name=='C-0685-source-consequence-handoff-v6.json':walk(load(p),p)
extra={};matches={}
for rid,z in native.items():
 n=normalized(z);ca=candidates.get(rid);old=baseline(rid);m=[]
 if ca and n==expected(ca['change'],ca['operation_id'],rid):m.append({'kind':'exact_source_bound_candidate_payload','path':ca['path'],'sha256':ca['sha256'],'pointer':ca['pointer'],'source_approval_binding_required_for_reuse':False,'exact_28_sequence_binding':str(b/'source-review/C0685-C0563-exact-sequence-v2-primary-binding-v2.json')})
 if old and n==normalized(old):m.append({'kind':'exact_frozen_baseline_full_native','path':str(b/'preparation/baseline-j281.sqlite'),'revision':rid,'source_individual_disposition_not_inferred':True})
 matches[rid]={'actual_normalized_full_payload_sha256':digest(n),'matches':m,'match_count':len(m),'needs_primary_whole_payload_reading':len(m)!=1,'prior_individual_source_disposition_pointers':index.get(rid,[])}
rows=[]
for r in req:
 affected=r['affected_revision_id'];after=r['changed_revision_id'];assert affected in native and after in native;before=native[after]['previous_id'];assert before
 if before not in native and before not in extra:
  z=baseline(before);assert z is not None;extra[before]=z
 beforeobj=native.get(before,extra.get(before));ev=[z for z in native[affected]['evidence'] if z['basis_revision_id']==before]
 rows.append({'actual_request':r,'affected_exact_revision':affected,'before_basis':before,'after_basis':after,'actual_matching_old_basis_edges':ev,'zero_old_basis_edges_flag':not ev,'affected_full_native_pointer':{'path':str(d/'actual-review-request-full-native-dictionary-v1.json'),'pointer':'/objects/'+affected},'before_full_native_pointer':{'path':str(d/'actual-review-request-full-native-dictionary-v1.json') if before in native else str(w/'additional-exact-baseline-before-bases-v1.json'),'pointer':'/objects/'+before},'after_full_native_pointer':{'path':str(d/'actual-review-request-full-native-dictionary-v1.json'),'pointer':'/objects/'+after},'affected_match':matches[affected],'before_normalized_full_payload_sha256':digest(normalized(beforeobj)),'after_normalized_full_payload_sha256':digest(normalized(native[after])),'prior_individual_before_version_dispositions':index.get(before,[]),'primary_request_tuple_disposition':None,'no_resolution_or_source_verdict':True})
pins.append(write('additional-exact-baseline-before-bases-v1.json',{'objects':extra,'read_only_from_locked_j281_baseline':True}));pins.append(write('individual-actual328-reuse-input-table-v1.json',{'requests':rows,'normalization':'Canonical JSON object keys; embedded data arrays retain exact order. SQL origin/dependency rows compare exact full row multiset including duplicates. Attachments preserve order. No factual normalization.','no_status_or_source_approval_inferred':True}));pins.append(write('full343-mechanical-match-index-v1.json',matches))
counts=collections.Counter(len(v['matches']) for v in matches.values());receipt={'task':'T-0780','status':'Mechanical individual reuse inputs only; Astra must grade each actual request tuple','requests':len(rows),'native_objects':len(native),'additional_old_basis_objects':len(extra),'whole_payload_match_counts':dict(counts),'request_tuples_needing_whole_payload_reading':sum(v['affected_match']['needs_primary_whole_payload_reading'] for v in rows),'tuples_with_prior_individual_pointers':sum(bool(v['affected_match']['prior_individual_source_disposition_pointers']) for v in rows),'zero_old_basis_edge_tuples':sum(v['zero_old_basis_edges_flag'] for v in rows),'pins':pins,'immutable_probe_modified':False,'applies_resolutions_or_validators':0,'failed_attempts':1,'elapsed_seconds':time.time()-start};write('mechanical-reuse-handoff-and-production-v1.json',receipt);print({k:receipt[k] for k in ['requests','native_objects','additional_old_basis_objects','whole_payload_match_counts','tuples_with_prior_individual_pointers','elapsed_seconds']})
