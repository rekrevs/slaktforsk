import json,hashlib,pathlib,copy
b=pathlib.Path('evaluations/T-0810');load=lambda p:json.loads((b/p).read_text());sha=lambda p:hashlib.sha256((b/p).read_bytes()).hexdigest()
s=load('primary-seven-repairs-and59-resolution-spec-v1.json');o=load('implementation/repair-operation-v1.json');t=load('implementation/repair-consequence-table-v1.json');cx=load('implementation/stage474-v1/actual-pending-contexts-initial.json');nm={r['current_target_native']['object_id']:r['current_target_native'] for r in cx};by={c['id']:c for c in o['changes']};checks=[]
for c in s['changes']:
 n=copy.deepcopy(nm[c['id']]);
 for f in c['fields']:
  z=n; ks=f['field'].split('.')
  for k in ks[:-1]:z=z[k]
  assert z[ks[-1]]==f['old'];z[ks[-1]]=f['new']
 ev=[]
 for e in n['evidence']:
  obj,v=e['basis_revision_id'].rsplit('@',1);ev.append({'object':obj,'version':int(v),'role':e['role'],'note':e['note']})
 for r in c.get('rebindEvidence',[]):
  assert n['evidence'][r['index']]==r['old'];ev[r['index']]['object']=r['newObject'];ev[r['index']]['version']=r['newVersion']
 ev+=c.get('appendEvidence',[])
 expected={'id':c['id'],'kind':n['kind'],'expectedVersion':n['version'],'data':{k:v for k,v in n['data'].items() if k!='revision_id'},'origins':[{'unit':q['unit_id'],'coverage':q['coverage'],'note':q['note']} for q in n['origins']],'evidence':ev,'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 assert expected==by[c['id']],c['id'];checks.append(c['id'])
assert o['resolve']==s['resolve'];assert len(o['changes'])==7;assert len(o['resolve'])==59
for a,c,r,d in zip(t['individual_request_consequences'],cx,o['resolve'],s['individualDispositions']):
 assert a['actual_full_context']==c;assert a['exact_native_resolution']==r;assert a['source_disposition']==d
for r in t['retains']:assert r['old_native']==nm[r['old_native']['object_id']]
assert len(t['retains'])==52
for c in t['changes']:
 assert c['old_native']==nm[c['object_id']];assert c['new_api']==by[c['object_id']]
assert t['operation_sha256']==sha('implementation/repair-operation-v1.json')
out={'full_API_reconstruction':checks,'literal_field_count':sum(len(c['fields']) for c in s['changes']),'explicit_rebinds':sum(len(c.get('rebindEvidence',[])) for c in s['changes']),'all_59_actual_contexts_dispositions_resolutions_exact':True,'all_52_fullnative_retains_exact':True,'issues':[]}
f=b/'independent-repair-literal-check-result-v1.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
