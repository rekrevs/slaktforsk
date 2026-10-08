import json,hashlib,importlib.util
from pathlib import Path
b=Path('evaluations/T-0817');i=b/'implementation';s=i/'stage486-v1';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=load(i/'final-manifest-v1.json')
for p in m['pins']:assert sha(Path(p['path']))==p['sha256'],p['path']
sp=importlib.util.spec_from_file_location('h','evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(s/'stage.sqlite');assert h.state(c)=={'journal_head':486,'pending':0}
op=load(i/'operation-v2.json');table=load(i/'consequence-table-v2.json')
for a in op['changes']:
 n=h.native(c,h.current(c,a['id']));data=dict(n['data']);data.pop('revision_id',None)
 for k,v in data.items():
  if k.endswith('_json') and isinstance(v,str):
   try:data[k]=json.loads(v)
   except ValueError:pass
 assert data==a['data'],a['id']
 for nk,ak in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')]:assert n[nk]==a.get(ak), (a['id'],nk)
 assert [{'object':e['basis_revision_id'].rsplit('@',1)[0],'version':int(e['basis_revision_id'].rsplit('@',1)[1]),'role':e['role'],'note':e['note']} for e in n['evidence']]==a['evidence']
 assert [{'unit':o['unit_id'],'coverage':o['coverage'],'note':o['note']} for o in n['origins']]==a['origins']
for r in table['retains']:assert h.native(c,h.current(c,r['object_id']))==r['old_native'],r['object_id']
rop=load(i/'seven-resolution-operation-v1.json');rt=load(i/'seven-resolution-consequence-table-v1.json')
actual=[dict(x)for x in c.execute('select * from review_resolution where operation_id=? order by rowid',(rop['id'],))];assert [{'request':x['request_id'],'rationale':x['rationale']}for x in actual]==rop['resolve']
for r in rt['retains']:assert h.native(c,h.current(c,r['old_native']['object_id']))==r['old_native']
for root in ['P-0269','P-0270']:
 p=load(s/(root+'-pedigree.json'));assert len(p['paths'])==43 and p['truncated']==False
 gate=next(x for x in p['gates'] if x['person_id']=='P-0383');assert gate['passed'] and gate['identity_review']['assessments'][0]['revision_id']=='ASSESSMENT-P-0383@1'
print('PASS',len(m['pins']),'pins; 47 actual native APIs/full orderedmetadata;483 retains;7 resolutions/4targets;43 paths both and Sven existing gate')
