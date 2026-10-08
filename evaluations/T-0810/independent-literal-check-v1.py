import json,sqlite3,pathlib,copy,hashlib
P=pathlib.Path('evaluations/T-0810');load=lambda f:json.load(open(P/f));c=sqlite3.connect('file:'+str(P/'preparation/baseline473.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
op=load('implementation/operation-v3.json');tab=load('implementation/consequence-table-v3.json');spec=load('primary-complete-source-design-v3.json');am=load('primary-four-version-bindings-amendment-v1.json');issues=[]
def norm(v):
 if isinstance(v,str):
  try:return json.loads(v)
  except:return v
 return v
def native(n):
 r=dict(c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(n['id'],)).fetchone());r['data']=dict(c.execute('select * from "'+r['kind']+'" where revision_id=?',(n['id'],)).fetchone())
 for k in r['data']:
  if k.endswith('_json'):r['data'][k]=norm(r['data'][k])
 for k,t in [('origins','origin'),('evidence','dependency')]:r[k]=[dict(z)for z in c.execute('select * from '+t+' where revision_id=? order by rowid',(n['id'],))]
 nn=copy.deepcopy(n)
 for k in nn['data']:
  if k.endswith('_json'):nn['data'][k]=norm(nn['data'][k])
 for k in r:
  if r[k]!=nn.get(k):issues.append(('native',n['id'],k))
 return r
def edge(e):
 id,v=e['basis_revision_id'].rsplit('@',1);return dict(object=id,version=int(v),role=e['role'],note=e['note'])
old={x['object_id']:x['old_native']for x in tab['changes'] if x['old_native']};expected={};components=[json.load(open(x['path'])) for x in spec['components']]
for comp in components:
 for s in comp.get('changes',[]):
  id=s['id']
  if id not in expected:
   n=old[id];r=native(n);data=copy.deepcopy(r['data']);data.pop('revision_id');a=dict(id=id,kind=r['kind'],expectedVersion=r['version'],data=data,origins=[dict(unit=e['unit_id'],coverage=e['coverage'],note=e['note'])for e in r['origins']],evidence=[edge(e) for e in r['evidence']])
   for k in ['disposition','rationale','caveat']:a[k]=r[k]
   a['evidenceStatus']=r['evidence_status']
   if r['kind']=='record':
    a['assets']=[dict(path=e['asset_path'],region=e['region'])for e in n.get('assets',[])];a['media']=[dict(id=e['media_id'],region=e['region'])for e in n.get('media',[])]
   expected[id]=a
  a=expected[id]
  for f in s.get('fields',[s] if 'field'in s else []):
   field=f['field'];dest=a['data'] if field.startswith('data.') else a;k=field[5:]if field.startswith('data.') else field;k='evidenceStatus' if k=='evidence_status' else k
   if norm(dest[k])!=norm(f['old']):issues.append(('old',id,field))
   dest[k]=norm(f['new']) if k.endswith('_json') else f['new']
  for e in s.get('support_rebinds',[]):
   oid,v=e['old'].rsplit('@',1);newid,nv=e['new'].rsplit('@',1);matches=[z for z in a['evidence']if z['object']==oid and z['version']==int(v)];assert len(matches)==1;matches[0].update(object=newid,version=int(nv))
  for e in s.get('rebindEvidence',[]):
   assert a['evidence'][e['index']]==edge(e['old']);a['evidence'][e['index']].update(object=e['newObject'],version=e['newVersion'])
  for e in s.get('appendEvidence',[]):
   e=copy.deepcopy(e)
   if 'id'in e:e['object']=e.pop('id')
   a['evidence'].append(e)
  for m in s.get('media_append_exact',[]):a['media'].append(dict(id=m['id'],region=a['data']['locator']))
 for s in comp.get('newObjects',[]):
  a={k:copy.deepcopy(s[k])for k in ['id','kind','disposition','rationale','caveat','origins','evidenceStatus','evidence']};a['data']={k:copy.deepcopy(v)for k,v in s.items()if k not in a};expected[a['id']]=a
for e in am['amendments']:
 a=expected[e['target']];assert a['evidence'][e['index']]==e['old'];a['evidence'][e['index']]=e['new']
for a in op['changes']:
 b=expected[a['id']]
 for k in set(a)|set(b):
  if a.get(k)!=b.get(k):issues.append(('API',a['id'],k,a.get(k) if k=='media' else None,b.get(k) if k=='media' else None))
assert len(op['changes'])==len(expected)
for t in tab['changes']:
 assert t['new_api']==next(a for a in op['changes']if a['id']==t['object_id'])
for t in tab['retains']:native(t['old_native'])
print(json.dumps({'issues':issues,'APIs':len(expected),'retains':len(tab['retains'])},ensure_ascii=False))
(P/'independent-literal-check-result-v1.json').write_text(json.dumps({'issues':issues,'APIs':len(expected),'retains':len(tab['retains'])},ensure_ascii=False,indent=2)+'\n')
