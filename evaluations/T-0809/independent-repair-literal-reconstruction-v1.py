import json,sqlite3,pathlib,copy,hashlib
p=pathlib.Path('evaluations/T-0809'); load=lambda n:json.loads((p/n).read_text());op=load('implementation/repair-operation-v1.json');tab=load('implementation/repair-consequence-table-v1.json');s=load('primary-actual96-repair-and-resolve-spec-v2.json');s['newObjects']=[];a={'changes':[],'newObjects':[]}; c=sqlite3.connect('file:evaluations/T-0809/implementation/stage472-v2/stage.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
specs={z['id']:z for z in s['changes']+a['changes']};news={z['id']:z for z in s['newObjects']+a['newObjects']}; actual={z['id']:z for z in op['changes']}
def native(n):
 r=dict(c.execute('select * from revision where id=?',(n['id'],)).fetchone());r['kind']=c.execute('select kind from object where id=?',(n['object_id'],)).fetchone()[0];r['data']=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(n['id'],)).fetchone())
 for key,t in [('origins','origin'),('evidence','dependency')]:r[key]=[dict(v) for v in c.execute('select * from '+t+' where revision_id=? order by rowid',(n['id'],))]
 if r['kind']=='record':
  for key,t in [('assets','record_asset'),('media','record_media')]:r[key]=[dict(v) for v in c.execute('select * from '+t+' where revision_id=? order by rowid',(n['id'],))]
 assert r==n, n['id']
 return r
checks=[]
for row in tab['changes']:
 ident=row['object_id'];got=row['new_api'];assert actual[ident]==got
 if row['old_native']:
  n=native(row['old_native']);z=specs[ident]
  exp={'id':ident,'kind':n['kind'],'expectedVersion':n['version'],'data':{k:v for k,v in n['data'].items() if k!='revision_id'},'origins':[{'unit':v['unit_id'],'coverage':v['coverage'],'note':v['note']} for v in n['origins']],'evidence':[{'object':v['basis_revision_id'].rsplit('@',1)[0],'version':int(v['basis_revision_id'].rsplit('@',1)[1]),'role':v['role'],'note':v['note']} for v in n['evidence']],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
  if n['kind']=='record':exp['assets']=[{'path':v['asset_path'],'region':v['region']} for v in n['assets']];exp['media']=[{'id':v['asset_id'],'region':v['region']} for v in n['media']]
  for f in z['fields']:
   d=exp if f['field'] in ['caveat','rationale','disposition','evidenceStatus'] else exp['data'];assert d[f['field']]==f['old'];d[f['field']]=f['new']
  for e in z.get('evidenceRebinds',[]):
   assert exp['evidence'][e['index']]['object']==e['object'];assert exp['evidence'][e['index']]['version']==e['oldVersion'];exp['evidence'][e['index']]['version']=e['newVersion']
  exp['evidence']+=z.get('supportAppend',[])
  for m in z.get('media_append_exact',[]):exp['media'].append({'id':m['id'],'region':'helbild'})
 else:
  z=news[ident]; meta=['disposition','evidenceStatus','rationale','caveat','origins','evidence'];exp={'id':ident,'kind':z['kind'],'expectedVersion':None,'data':{k:v for k,v in z.items() if k not in meta+['id','kind']},**{k:z[k] for k in meta}}
 assert exp==got,(ident,[(k,exp.get(k),got.get(k)) for k in exp.keys()|got.keys() if exp.get(k)!=got.get(k)])
 checks.append(ident)
for r in tab['retains']:native(r['old_native'])
assert set(actual)==set(specs)|set(news)
assert op['resolve']==[{'request':r['request'],'rationale':r['rationale']} for r in s['resolve']]
assert len(op['resolve'])==96
for z in op['changes']:
 cols=list(c.execute('pragma table_info('+z['kind']+')'));names={r['name'] for r in cols if r['name']!='revision_id'};assert set(z['data'])<=names
 for r in cols:
  if r['name']!='revision_id' and r['notnull']:assert z['data'].get(r['name']) is not None
res={'task':'T-0809','exact_api_reconstruction_pass':True,'changes':checks,'native_retains':len(tab['retains']),'full_current_native_metadata_array_order_checked':True,'operation_sha256':hashlib.sha256((p/'implementation/repair-operation-v1.json').read_bytes()).hexdigest(),'consequence_sha256':hashlib.sha256((p/'implementation/repair-consequence-table-v1.json').read_bytes()).hexdigest()};f=p/'independent-repair-literal-reconstruction-v1.json';f.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print('PASS',len(checks),len(tab['retains']),hashlib.sha256(f.read_bytes()).hexdigest())
