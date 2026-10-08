import json,pathlib,hashlib,copy
b=pathlib.Path('evaluations/T-0814');load=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
m=load(b/'implementation/literal-manifest-v1.json')
for f in m['files']:assert sha(f['path'])==f['sha256'],f
op=load(b/'implementation/operation-v1.json');tab=load(b/'implementation/consequence-table-v1.json');c=load(b/'primary-current-consequence-component-v3.json');r=load(b/'primary-review-and-retain-component-v3.json');ad=load(b/'primary-two-READ-rebind-amendment-v1.json');cs={z['object_id']:z for z in c['changes']};new={z['id']:z for z in r['new_reviews']};apis={z['id']:z for z in op['changes']};assert len(apis)==20
for row in tab['changes']:
 id=row['object_id'];a=apis[id];assert row['new_api']==a
 if id in new:assert a==new[id],id;continue
 old=row['old_native'];exp={'id':id,'kind':old['kind'],'expectedVersion':old['version'],'data':{k:v for k,v in old['data'].items() if k!='revision_id'},'disposition':old['disposition'],'evidenceStatus':old['evidence_status'],'rationale':old['rationale'],'caveat':old['caveat'],'origins':[{'unit':v['unit_id'],'coverage':v['coverage'],'note':v['note']} for v in old['origins']],'evidence':[{'object':v['basis_revision_id'].rsplit('@',1)[0],'version':int(v['basis_revision_id'].rsplit('@',1)[1]),'role':v['role'],'note':v['note']} for v in old['evidence']]}
 if 'assets' in a:exp['assets']=[{'path':v['asset_path'],'region':v['region']} for v in old.get('assets',[])]
 if 'media' in a:exp['media']=copy.deepcopy(old.get('media',[]))
 for key in ['value_json','date_json']:
  if isinstance(exp['data'].get(key),str):exp['data'][key]=json.loads(exp['data'][key])
 for f in cs[id]['fields']:
  parts=f['field'].split('.');target=exp
  for k in parts[:-1]:target=target[k]
  assert target[parts[-1]]==f['old'],(id,f['field']);target[parts[-1]]=copy.deepcopy(f['new'])
 for rb in c.get('explicit_rebinds',[]):
  if rb['object_id']==id:
   e=exp['evidence'][rb['index']];assert e['object']+'@'+str(e['version'])==rb['old_basis'];e['version']=int(rb['new_basis'].rsplit('@',1)[1])
 for rb in ad['individual_decisions']:
  if rb['object_id']==id:assert exp['evidence'][rb['index']]==rb['old_edge'];exp['evidence'][rb['index']]=rb['new_edge']
 for basis in cs[id]['supports']:
  obj,v=basis.rsplit('@',1);exp['evidence'].append({'object':obj,'version':int(v),'role':'supports','note':'T-0814 återbruk av detta accepterade underlag för exakt angiven fälträttelse, ingen ny oberoende evidensröst.'})
 assert exp==a,(id,[k for k in exp if exp[k]!=a.get(k)])
assert len(tab['retains'])==613
for z in tab['retains']:assert z['revision_id']==z['old_native']['id'] and z['disposition']=='RETAIN_EXACT'
q=b/'implementation/queue-candidate-v2';back=load(q/'backlog.json');live=load('wotan/backlog.json');print('back keys',list(back));t=[x for x in back['tasks'] if x['id']=='T-0817'];assert len(t)==1 and t[0]['status']=='READY' and t[0]['after']==[]
assert [x for x in back['tasks'] if x['id']!='T-0817']==live['tasks'];ids=[x['id'] for x in back['tasks']];assert ids.index('T-0817')==ids.index('T-0816')+1
scope=load(b/'primary-proposed-T0817-scope-v1.json');log=(q/'T-0817.md').read_text();assert json.dumps(scope,ensure_ascii=False,indent=2) in log
print('PASS 26pins,20literal fullAPIs,613retains,816oldrecords,after816,no dependencies,fullscope embedded.')
print(json.dumps(t,ensure_ascii=False))
