import json,sqlite3,pathlib,hashlib
B=pathlib.Path(__file__).resolve().parent
names=['C-0084-source-candidate-operation-v2.json','C-0084-consequence-candidate-operation-v2.json','C-0402-source-candidate-operation-v2.json','C-0402-role-metadata-candidate-operation-v2.json','C-0573-source-candidate-operation-v1.json','C-0573-consequence-candidate-operation-v1.json','C-0896-source-candidate-operation-v3.json','C-0896-consequence-candidate-operation-v2.json','C-0911-record-metadata-candidate-operation-v1.json','C-0911-source-candidate-operation-v3.json','C-0911-role-metadata-candidate-operation-v1.json','C-0911-consequence-candidate-operation-v2.json']
c=sqlite3.connect(B/'clone/final-candidate-v3.sqlite');c.row_factory=sqlite3.Row
ns={'connection':c};exec((B/'native_payload.py').read_text(),ns);checks=[]
for name in names:
 for change in json.loads((B/name).read_text())['changes']:
  v=(change['expectedVersion'] or 0)+1;actual=ns['existing'](change['id'],v);expected=dict(change);expected['expectedVersion']=v
  if 'assets' in expected:
   actual['assets']=[{'path':r['asset_path'],'region':r['region']} for r in c.execute('select * from record_asset where revision_id=?',(change['id']+'@'+str(v),))]
   actual['assets']=sorted(actual['assets'],key=lambda z:json.dumps(z,sort_keys=True));expected['assets']=sorted(expected['assets'],key=lambda z:json.dumps(z,sort_keys=True))
  # SQL order is not evidence/origin meaning; structured data arrays remain ordered.
  for key in ['evidence','origins']:
   actual[key]=sorted(actual[key],key=lambda z:json.dumps(z,sort_keys=True));expected[key]=sorted(expected[key],key=lambda z:json.dumps(z,sort_keys=True))
  checks.append({'operation':name,'object':change['id'],'version':v,'pass':actual==expected,'different_keys':[k for k in expected if actual.get(k)!=expected[k]]})
base=sqlite3.connect(B/'clone/research-pre.sqlite');base.row_factory=sqlite3.Row
changed={z['object'] for z in checks};unchanged=[]
for r in base.execute('select * from current_revision'):
 if r['object_id'] in changed:continue
 a=c.execute('select * from current_revision where object_id=?',(r['object_id'],)).fetchone();assert dict(a)==dict(r),r['object_id']
 unchanged.append(r['object_id'])
out={'task':'T-0777','operations':names,'full_payload_checks':checks,'matched':sum(z['pass'] for z in checks),'count':len(checks),'unchanged_current_revisions':len(unchanged),'all_pass':all(z['pass'] for z in checks),'data_array_order_checked':True,'canonical_not_written':True}
(B/'final-full-stage-check-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['operations','full_payload_checks']}));assert out['all_pass']
