import json,hashlib,copy
from pathlib import Path
p=Path('/Users/sverker/repos/slaktforsk/evaluations/T-0812')
read=lambda f:json.loads(Path(f).read_text())
hashfile=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
op=read(p/'implementation/operation-v1.json'); table=read(p/'implementation/consequence-table-v1.json'); design=read(p/'primary-complete-source-design-v3.json')
assert hashfile(p/'implementation/operation-v1.json')=='f4c93141988777743cd4dfc56ce26acd84cb8c14c98a52ae944197f602972914'
assert hashfile(p/'implementation/consequence-table-v1.json')=='65aab307977831cdac3d663ee4d081a740d349995fc40993f3007d305122fef2'
specs=[read(q['path']) for q in design['components']]
changes={};new={}
for s in specs:
 for c in s.get('changes',[]): changes.setdefault(c['id'],[]).append(c)
 for c in s.get('newObjects',[]): assert c['id'] not in new;new[c['id']]=c

def decode(v):
 if isinstance(v,str):
  try:return json.loads(v)
  except:pass
 return v

def nativeapi(o):
 d={k:decode(v) if k.endswith('_json') else v for k,v in o['data'].items() if k!='revision_id'}
 a=dict(id=o['object_id'],kind=o['kind'],expectedVersion=o['version'],data=d,origins=[dict(unit=z['unit_id'],coverage=z['coverage'],note=z['note']) for z in o.get('origins',[])],evidence=[])
 for z in o.get('evidence',[]):
  ob,ver=z['basis_revision_id'].rsplit('@',1);a['evidence'].append(dict(object=ob,version=int(ver),role=z['role'],note=z['note']))
 for k,v in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')]:a[v]=o[k]
 if 'assets' in o:a['assets']=[dict(path=z['asset_path'],region=z['region']) for z in o['assets']]
 if 'media' in o:a['media']=copy.deepcopy(o['media'])
 return a

def reportdiff(a,b,path=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):return sum([reportdiff(a.get(k),b.get(k),path+'/'+k) for k in a.keys()|b.keys()],[])
 return [(path,a,b)]
issues=[];reconstructed=[]
for row,c in zip(table['changes'],op['changes']):
 assert row['new_api']==c
 oid=c['id']; old=row['old_native']
 if old:
  expected=nativeapi(old)
  for s in changes[oid]:
   for f in s['fields']:
    ks=f['field'].split('.');node=expected
    for k in ks[:-1]:node=node[k]
    assert decode(node[ks[-1]])==decode(f['old']),(oid,f['field'])
    node[ks[-1]]=copy.deepcopy(f['new'])
   for r in s.get('support_rebinds',[]):
    idx=[i for i,e in enumerate(expected['evidence']) if e['object']+'@'+str(e['version'])==r['old']]
    assert len(idx)==1,(oid,r,idx)
    obj,ver=r['new'].rsplit('@',1);expected['evidence'][idx[0]]['object']=obj;expected['evidence'][idx[0]]['version']=int(ver)
   expected['evidence']+=copy.deepcopy(s.get('appendEvidence',[]))
 else:
  s=copy.deepcopy(new[oid]);expected=s
  if 'data' not in s:
   fields=['record_id','text','reading_note'] if s['kind']=='transcription' else ['subject_id','criteria','outcome','body']
   expected['data']={k:expected.pop(k) for k in fields}
  expected.setdefault('expectedVersion',None)
 dif=reportdiff(expected,c)
 if dif:issues.append({'id':oid,'diff':dif})
 reconstructed.append(oid)
assert len(reconstructed)==111 and len(set(reconstructed))==111
print('issues',json.dumps(issues,ensure_ascii=False)[:8000])
# independent earlier captured current source objects, not table selfcomparison
current={o['object_id']:o for o in read(p/'independent-global-current-copy-search-v1.json')['objects']}
for person in ['0254','0255']:current.update({o['object_id']:o for o in read(p/f'preparation/P-{person}-current-native-v1.json')['current']})
for o in read(p/'preparation/exact-death-READ-TR-native-supplement-v1.json')['objects']:current[o['id']]=o['full_current_native']
def collect(z):
 if isinstance(z,dict):
  if 'object_id' in z and 'data' in z and 'version' in z:
   old=current.get(z['object_id'])
   if old is None or old['version']<z['version']:current[z['object_id']]=z
  for v in z.values():collect(v)
 elif isinstance(z,list):
  for v in z:collect(v)
collect(read(p/'preparation/two-unit-parent-date-copy-routing-and-schema-v1.json'))
collect(read(p/'preparation/exact-support-native-v1.json'))
oldchecks=[];missing=[]
for row in table['changes']+table['retains']:
 o=row['old_native']
 if o is None:continue
 if o['object_id'] not in current:missing.append(o['object_id']);continue
 # full semantically native may decoder string vs object differ; normalize recursivelyjson
 def norm(x):
  if isinstance(x,dict):return {k:norm(decode(v) if k.endswith('_json') else v) for k,v in x.items()}
  if isinstance(x,list):return [norm(v) for v in x]
  return x
 aa=norm(o);bb=norm(current[o['object_id']]);
 for k in ['assets','media']:
  aa.setdefault(k,[]);bb.setdefault(k,[])
 if aa!=bb:oldchecks.append([o['object_id'],reportdiff(aa,bb)])
print('oldmismatch',len(oldchecks),'missing',len(missing));print('mismatchdetails',str(oldchecks)[:2500]);print('missingids',missing)
out={'operationSha256':hashfile(p/'implementation/operation-v1.json'),'consequenceSha256':hashfile(p/'implementation/consequence-table-v1.json'),'sourceDesignSha256':hashfile(p/'primary-complete-source-design-v3.json'),'reconstructed':len(reconstructed),'literalIssues':issues,'oldNativeComparisonIssues':oldchecks,'missingIndependentOldCapture':missing}
(p/'independent-literal-reconstruction-v1.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
