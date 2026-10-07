import json,hashlib
from pathlib import Path
b=Path('evaluations/T-0777');x=json.load(open(b/'final-full-stage-check-v2.json'));out=[]
for name in x['operations']:
 p=b/name;op=json.load(open(p));cs=[]
 for c in op['changes']:
  if c['expectedVersion'] is None:continue
  ip=b/'current'/('inspect-'+c['id'].replace('/','__')+'.json')
  if not ip.exists(): raise Exception('Missing full capture '+c['id'])
  z=json.load(open(ip));r=next(r for r in z['revisions'] if r['version']==z['currentVersion']);ds=[]
  for k,v in c['data'].items():
   if v!=r['data'].get(k):ds.append({'field':'data.'+k,'before':r['data'].get(k),'after':v})
  for k,k2 in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')]:
   if r[k]!=c.get(k2):ds.append({'field':k,'before':r[k],'after':c.get(k2)})
  origins=[{'unit':o['id'],'coverage':o['coverage'],'note':o['note']} for o in r['origins']]
  cs.append({'id':c['id'],'baselineVersion':z['currentVersion'],'expectedVersion':c['expectedVersion'],'diff':ds,'origins_preserved':c['origins']==origins,'old_evidence':r['evidence'],'new_evidence':c['evidence']})
 out.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'changes':cs})
q=b/'independent-review'/'thirteen-operation-full-diff-v2.json';q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('saved',len(out),'operations',sum(len(o['changes']) for o in out),'existing changes');print('origins mismatch',[c['id'] for o in out for c in o['changes'] if not c['origins_preserved']]);print('protectedFieldChanges',[(c['id'],d['field']) for o in out for c in o['changes'] for d in c['diff'] if d['field'] in ['disposition','evidence_status','data.sex','data.display_name','data.outcome']])
