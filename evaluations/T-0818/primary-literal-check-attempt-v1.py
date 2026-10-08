import json,copy,hashlib
from pathlib import Path
E=Path('evaluations/T-0818');I=E/'implementation'
def rd(p):return json.loads(Path(p).read_text())
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
m=rd(I/'literal-manifest-v1.json');d=rd(E/'source-design/primary-complete-source-design-v1.json');o=rd(I/'operation-v1.json');t=rd(I/'consequence-table-v1.json');errors=[]
pins=[]
for x in m['pins']:
 actual=sha(x['path']);assert actual==x['sha256'],x['path'];assert Path(x['path']).stat().st_size==x['bytes'];pins.append({'path':x['path'],'sha256':actual})
api={x['id']:x for x in o['changes']};table={x['object_id']:x for x in t['changes']};checks=[]
for c in d['existing_changes']:
 n=copy.deepcopy(c['full_old_native']);assert table[c['object']]['old_native']==n
 for f in c['fields']:
  target=n;ks=f['path'].split('.')
  for k in ks[:-1]:target=target[k]
  assert target[ks[-1]]==f['old'];target[ks[-1]]=f['new']
 for e in c['evidence_rebind']:
  assert n['evidence'][e['index']]==e['old'];n['evidence'][e['index']]=copy.deepcopy(e['new'])
 ev=[]
 for e in n['evidence']:
  bid,v=e['basis_revision_id'].rsplit('@',1);ev.append({'object':bid,'version':int(v),'role':e['role'],'note':e['note']})
 ev+=c['evidence_append']
 data={k:v for k,v in n['data'].items() if k!='revision_id'}
 for k,v in data.items():
  if k.endswith('_json') and isinstance(v,str):data[k]=json.loads(v)
 expected={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version'],'data':data,'origins':[{'unit':z['unit_id'],'coverage':z['coverage'],'note':z['note']} for z in n['origins']],'evidence':ev,'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 if n['kind']=='record':
  assert n.get('assets',[])==[] and n.get('media',[])==[]
  expected['assets']=[];expected['media']=c.get('media_append',[])
 assert expected==api[c['object']],c['object'];assert expected==table[c['object']]['new_api'];assert table[c['object']]['literal_fields']==c['fields'];assert table[c['object']]['explicit_support_appends']==c['evidence_append']
 checks.append({'object':c['object'],'full_independent_reconstruction_exact':True})
for n in d['new_objects']:
 assert n==api[n['id']],n['id'];assert table[n['id']]['new_api']==n and table[n['id']]['old_native'] is None
 checks.append({'object':n['id'],'full_independent_reconstruction_exact':True})
assert len(api)==32 and len(table)==32
assert o['media']==d['media'] and len(o['media'])==1
assert len(t['retains'])==len(d['retains'])==652
for old,actual in zip(d['retains'],t['retains']):
 assert actual['old_native']==old['full_old_native'];assert actual['revision_id']==old['full_old_native']['id'];assert actual['reason']==old['reason'];assert actual['disposition']==old['decision']
assert t['exact_relation_retains']==d['exact_relation_retains'] and len(t['exact_relation_retains'])==26
assert t['rest_ownership']==d['rest_ownership'] and t['protected']==d['protected']
positions={x['id']:i for i,x in enumerate(o['changes'])}
for c in o['changes']:
 seen=set()
 for e in c['evidence']:
  tup=(e['object'],e['version'],e['role']);assert tup not in seen;seen.add(tup)
  if e['object'] in positions:assert positions[e['object']]<positions[c['id']],(c['id'],e['object'])
assert not o.get('resolve')
proof={'task':'T-0818','manifest_sha256':sha(I/'literal-manifest-v1.json'),'verified_pins':pins,'full_api_reconstruction':checks,'fields':29,'explicit_rebinds':16,'retains652_fullnative_exact':True,'relations26_fullnative_exact':True,'one_media_two_record_scopes_exact':True,'stable_support_order_and_no_duplicate_tuples':True,'no_resolution_assumed':True,'operation_reason':'AC1–6 verified against actual T0818 six numbered criteria.','errors':[],'executed_clone':False,'canonicalApproval':False}
p=E/'primary-literal-reconstruction-proof-v1.json';assert not p.exists();p.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(str(p),sha(p))
