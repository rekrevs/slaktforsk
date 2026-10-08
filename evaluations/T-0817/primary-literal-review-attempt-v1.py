import json,hashlib,copy,datetime
from pathlib import Path
b=Path('evaluations/T-0817');i=b/'implementation'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=load(b/'primary-complete-source-design-v2.json');op=load(i/'operation-v2.json');t=load(i/'consequence-table-v2.json');m=load(i/'literal-manifest-v2.json');issues=[]
for p in m['pins']:
 if sha(p['path'])!=p['sha256']:issues.append(['pin',p['path']])
expected={}
for c in d['existing_changes']:
 o=copy.deepcopy(c['full_old_native'])
 for f in c['fields']:
  z=o;ps=f['path'].split('.')
  for k in ps[:-1]:z=z[k]
  assert z[ps[-1]]==f['old'];z[ps[-1]]=f['new']
 for r in c['evidence_rebind']:
  assert o['evidence'][r['index']]==r['old_edge'];o['evidence'][r['index']]=r['new_edge']
 ev=[]
 for e in o['evidence']:
  ob,ver=e['basis_revision_id'].rsplit('@',1);ev.append({'object':ob,'version':int(ver),'role':e['role'],'note':e['note']})
 ev+=c['evidence_append']
 data={k:v for k,v in o['data'].items() if k!='revision_id'}
 a={'id':o['object_id'],'kind':o['kind'],'expectedVersion':o['version'],'data':data,'origins':[{'unit':z['unit_id'],'coverage':z['coverage'],'note':z['note']} for z in o['origins']],'evidence':ev,'disposition':o['disposition'],'evidenceStatus':o['evidence_status'],'rationale':o['rationale'],'caveat':o['caveat']}
 expected[a['id']]=a
for a in d['new_objects']:expected[a['id']]=a
assert len(expected)==47==len(op['changes'])
for a in op['changes']:
 if a!=expected[a['id']]:issues.append(['api',a['id'],[k for k in set(a)|set(expected[a['id']]) if a.get(k)!=expected[a['id']].get(k)]])
 assert next(z for z in t['changes'] if z['object_id']==a['id'])['new_api']==a
for c in d['existing_changes']:
 row=next(z for z in t['changes'] if z['object_id']==c['object']);assert row['old_native']==c['full_old_native']
assert len(t['retains'])==len(d['retains'])==483
for a,z in zip(d['retains'],t['retains']):assert a['object']==z['object_id'] and a['full_native']==z['old_native'] and a['reason']==z['reason']
assert t['exact_relation_retains']==d['exact_relation_retains']
old=load(i/'operation-v1.json');expected_v2=copy.deepcopy(old);expected_v2['reason']=old['reason'].replace('AC1–6','AC1–5');assert expected_v2==op
assert t['operation_sha256']==sha(i/'operation-v2.json')
# All explicit projected changes occur after their accepted dependency in topological operation order.
ix={a['id']:n for n,a in enumerate(op['changes'])};heads={a['id']:(a['expectedVersion'] or 0)+1 for a in op['changes']}
for a in op['changes']:
 for e in a['evidence']:
  if e['object'] in heads:
   assert e['version']==heads[e['object']],(a['id'],e)
   assert ix[e['object']]<ix[a['id']],(a['id'],e)
x={'task':'T-0817','reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ready_for_root_clone_authorization':not issues,'cloneApproval':False,'canonicalApproval':False,'literalManifestSha256':sha(i/'literal-manifest-v2.json'),'operationSha256':sha(i/'operation-v2.json'),'consequenceSha256':sha(i/'consequence-table-v2.json'),'helperSha256':sha(i/'stage-initial-UNRUN-v2.py'),'sourceDesignSha256':sha(b/'primary-complete-source-design-v2.json'),'independent_reconstruction':{'apis':47,'existing':45,'new':2,'retains_full_native_exact':483,'relation_retains':7,'explicit_rebinds':10,'all_manifest_pins':len(m['pins']),'ordered_origins_evidence_fields_exact':True,'projected_topological_supports_checked':True},'issues':issues,'administrative_amendment':'Explicit approval of sole operation.reason AC1–6→AC1–5. Task has five numbered AC. V1 operation/table/manifest retained; all47 API values unchanged. No sourcejudgment/data amendment.','source_result':'Exact fullownrow/rawlimits/adoption and individual passed/supporting pair from approved source design, stronger C0445date and historicalnegative/LIFE/OWNER scope preserved. No nativeLIFE or other-person gate.','helper_review':'Full UNRUN helper read: clone pinned484 into newstage485, apply one exact operation, capture actual pending full contexts before any resolutions, prove native APIs/483retains and main unchanged. No worker invocation or canonical write authorized by this gate.','remaining':'Root alone authorizes clone after dual exact gates; every actual dependency requires independent own sealed dispositions and rootcomparisonrelease. Final source/reader/protected state review separate.'}
assert not issues,issues
q=b/'primary-literal-source-gate-v2.json';assert not q.exists();q.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'path':str(q),'sha256':sha(q),'manifest':x['literalManifestSha256'],'issues':issues}))
