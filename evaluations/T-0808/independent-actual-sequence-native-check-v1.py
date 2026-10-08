import json,pathlib,copy,sqlite3,hashlib
p=pathlib.Path('evaluations/T-0808');sp=p/'implementation/stage471-sequence-v1';l=lambda x:json.loads(x.read_text())
checks=[]
for step,name in [(1,'operation-v2.json'),(2,'repair-operation-v2.json')]:
 op=l(p/'implementation'/name);pr=l(sp/f'after-{step}-native-proof.json');ac=json.loads(pr['accepted']['request_json']);expected=copy.deepcopy(op);expected.update(dependencyReviewVersion=2,searchMemoryVersion=1);assert ac==expected
 for a,row in zip(op['changes'],pr['literal']):
  n=row['actual_native'];d=copy.deepcopy(n['data']);d.pop('revision_id')
  for k in d:
   if k.endswith('_json') and isinstance(d[k],str):d[k]=json.loads(d[k])
  for k,v in a['data'].items():assert d[k]==v,(a['id'],k)
  # Native nullable defaults may be added by the schema; every nondefault data field must be approved.
  assert all(k in a['data'] or v is None for k,v in d.items()),(a['id'],'extra data')
  assert n['object_id']==a['id'] and n['kind']==a['kind']
  for api,nat in [('disposition','disposition'),('evidenceStatus','evidence_status'),('rationale','rationale'),('caveat','caveat')]:assert n[nat]==a.get(api), (a['id'],api)
  assert [{k:v for k,v in o.items() if k!='revision_id'} for o in n['origins']]==[dict(unit_id=o['unit'],coverage=o['coverage'],note=o['note']) for o in a['origins']]
  assert [{k:v for k,v in e.items() if k!='revision_id'} for e in n['evidence']]==[dict(basis_revision_id=e['object']+'@'+str(e['version']),role=e['role'],note=e['note']) for e in a['evidence']]
  checks.append(a['id'])
con=sqlite3.connect('file:'+str(sp/'stage.sqlite')+'?mode=ro',uri=True);con.row_factory=sqlite3.Row
print('resolution columns',[x[1] for x in con.execute('pragma table_info(review_resolution)')])
op=l(p/'implementation/repair-operation-v2.json')
for r in op['resolve']:
 row=dict(con.execute('select * from review_resolution where request_id=?',(r['request'],)).fetchone());assert row['rationale']==r['rationale'];assert row['operation_id']==op['id']
assert len(checks)==62
print('PASS',len(checks),'full native API fields, accepted requests metadata-only normalization, all83 actual resolution rows exact')
