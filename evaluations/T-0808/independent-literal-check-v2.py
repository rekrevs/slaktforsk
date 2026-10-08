import json,pathlib,hashlib,copy
p=pathlib.Path('evaluations/T-0808');load=lambda f:json.loads((p/f).read_text());sha=lambda f:hashlib.sha256((p/f).read_bytes()).hexdigest()
op=load('implementation/operation-v2.json');tab=load('implementation/consequence-table-v2.json');specs=[load(f) for f in ['primary-source-adoption-spec-v1.json','primary-current-consequence-spec-v1.json','primary-PK08-and-duplicate-amendment-v1.json']]
base={r['object_id']:r for r in load('preparation/current-native-v1.json')['current']}
base.update({r['object_id']:r for r in load('preparation/exact-support-native-v1.json')['revisions'] if r['object_id'] not in base or r['version']>base[r['object_id']]['version']})
fields=[f for s in specs for f in s.get('field_changes',[])]; new={f['id']:f for s in specs for k in ['new_source_objects','new_reviews'] for f in s.get(k,[])}
rebinds=[f for s in specs for f in s.get('explicit_rebinds',[])]+load('primary-four-evidence-rebind-amendment-v1.json')['decisions']
def norm(z):
 z=copy.deepcopy(z)
 for k,v in z.get('data',{}).items():
  if k.endswith('_json') and isinstance(v,str):z['data'][k]=json.loads(v)
 return z
checks=[]
for row in tab['changes']:
 a=row['new_api'];assert a==next(c for c in op['changes'] if c['id']==a['id']);old=row['old_native']
 if old is None:assert a==new[a['id']];checks.append([a['id'],'exact_new_source_spec']);continue
 assert norm(old)==norm(base[a['id']]),a['id']
 d=copy.deepcopy(norm(old)['data']);d.pop('revision_id',None)
 ev=[]
 for e in old['evidence']:
  obj,v=e['basis_revision_id'].rsplit('@',1);ev.append({'object':obj,'version':int(v),'role':e['role'],'note':e['note']})
 expected={'id':old['object_id'],'kind':old['kind'],'expectedVersion':old['version'],'data':d,'origins':[{'unit':o['unit_id'],'coverage':o['coverage'],'note':o['note']} for o in old['origins']],'evidence':ev,'disposition':old['disposition'],'evidenceStatus':old['evidence_status'],'rationale':old['rationale'],'caveat':old['caveat']}

 for k in ['assets','media']:
  if k in old:expected[k]=[{'path':z['asset_path'],'region':z['region']} for z in old[k]] if k=='assets' else old[k]
 app=[]
 for f in fields:
  if f['id']!=a['id']:continue
  ptr=expected
  for k in f['field'][:-1]:ptr=ptr[k]
  assert ptr[f['field'][-1]]==f['old'],(a['id'],f['field'])
  ptr[f['field'][-1]]=f['new']
  for e in f.get('append_supports',[]):
   if e not in app:app.append(e)
 for r in rebinds:
  if r['id']!=a['id']:continue
  found=[(i,e) for i,e in enumerate(ev) if e['object']==r['basis'] and e['version']==r['old_version']]
  assert len(found)==1,(a['id'],r)
  i,e=found[0]
  if 'index' in r:assert i==r['index']
  e['version']=r['new_version']
 ev.extend(app)
 assert expected==a, (a['id'],[(k,expected[k],a.get(k)) for k in expected if expected[k]!=a.get(k)])
 checks.append([a['id'],'full_literal_metadata_order_exact'])
for r in tab['retains']:assert norm(r['old_native'])==norm(base[r['old_native']['object_id']]),(r['old_native']['object_id'],[(k,norm(r['old_native'])[k],norm(base[r['old_native']['object_id']]).get(k)) for k in norm(r['old_native']) if norm(r['old_native'])[k]!=norm(base[r['old_native']['object_id']]).get(k)])
assert len(checks)==55;assert len(tab['retains'])==226
out={'operationSha256':sha('implementation/operation-v2.json'),'consequenceSha256':sha('implementation/consequence-table-v2.json'),'checks':checks,'retains_exact':226,'method':'Independent reconstruction from locked fullnative and sourcefield judgments, preserving fullmetadata/origin/evidenceorder, explicitindividualrebinds only; new55APIs equal exact source specifications.','canonicalApproval':False}
f=p/'independent-literal-package-check-v2.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS',len(checks),'retains',226,'proofsha',hashlib.sha256(f.read_bytes()).hexdigest())
