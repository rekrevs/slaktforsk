import json,pathlib,hashlib
b=pathlib.Path('evaluations/T-0814');s=b/'implementation/stage483-v1';load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();m=load(b/'implementation/final-manifest-v1.json')
for f in m['pins']:
 p=pathlib.Path(f['path']);assert sha(p)==f['sha256'] and p.stat().st_size==f['bytes'],f['path']
assert sha(m['stage_database'])==m['stage_sha256'];proof=load(s/'final-exact-native-package-proof.json');op=load(b/'implementation/operation-v1.json');mp={z['id']:z for z in op['changes']}
for row in proof['full20_native_APIs']:
 o=row['current_full_native'];a=mp[o['object_id']];d={k:v for k,v in o['data'].items() if k!='revision_id'}
 for k in ['value_json','date_json']:
  if isinstance(d.get(k),str):d[k]=json.loads(d[k])
 assert d==a['data'];assert o['disposition']==a['disposition'] and o['evidence_status']==a['evidenceStatus'] and o['rationale']==a['rationale'] and o['caveat']==a['caveat']
 assert [{'unit':v['unit_id'],'coverage':v['coverage'],'note':v['note']} for v in o['origins']]==a['origins']
 assert [{'object':v['basis_revision_id'].rsplit('@',1)[0],'version':int(v['basis_revision_id'].rsplit('@',1)[1]),'role':v['role'],'note':v['note']} for v in o['evidence']]==a['evidence']
res=load(b/'implementation/42-resolution-operation-v1.json');assert [{'request':r['request_id'],'rationale':r['rationale']} for r in proof['ordered42stored_resolutions']]==res['resolve'];assert load(s/'actual-pending-full.json')==load(s/'actual-pending-full-contexts.json')==[]
inv=load(s/'inventory-full.json');print('inventorykeys',list(inv) if isinstance(inv,dict) else 'list');print('PASS1133pins/full20APIdata+allmetadata/origins/evidenceorder/exact42actualrationales/no pending')
for p in ['P-0336','P-0337']:
 per=load(s/(p+'-person.json'))
 for z in per['research']['reviews']:
  if z['object_id'].startswith(('IDENTITY-REVIEW-T0814','TREE-EFFECT-T0814')):
   assert z['body']==mp[z['object_id']]['data']['body'];print(z['object_id'],z['outcome'],'fullbody exact')
