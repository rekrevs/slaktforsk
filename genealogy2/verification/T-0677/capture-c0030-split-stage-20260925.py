"""Capture full pending at a C0030 split temp stage; no mutations."""
import hashlib,json,sqlite3,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2];STAGE=sys.argv[1]
assert STAGE in ('source','after')
DB=Path('/private/tmp/t0677-c0030-split-preflight-20260925/research.sqlite')
c=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);c.row_factory=sqlite3.Row
rows=lambda q,a=():[dict(x) for x in c.execute(q,a)]
def full(rid):
 rev=rows('SELECT * FROM revision WHERE id=?',(rid,))[0];kind=rows('SELECT kind FROM object WHERE id=?',(rev['object_id'],))[0]['kind']
 data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rid,))[0];data.pop('revision_id')
 for k,v in list(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origin=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rid,))]
 evidence=[]
 for x in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rid,)):
  o,v=x['basis_revision_id'].rsplit('@',1);evidence.append({'object':o,'version':int(v),'role':x['role'],'note':x['note']})
 return {'kind':kind,'revision':rev,'data':data,'origins':origin,'evidence':evidence}
requests=[]
for r in rows('SELECT rr.* FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id WHERE rs.request_id IS NULL ORDER BY rr.id'):
 requests.append({**r,'affected_full':full(r['affected_revision_id']),'changed_full':full(r['changed_revision_id'])})
head=sorted(Path('/private/tmp/t0677-c0030-split-preflight-20260925/journal').glob('*.json'))[-1].name
p=H/f'c0030-split-temp-{STAGE}-pending-full-20260925.json'
p.write_text(json.dumps({'task':'T-0677','state':f'TEMP_SPLIT_{STAGE.upper()}_PENDING_UNRESOLVED','journal':head,'count':len(requests),'requests':requests},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'stage':STAGE,'journal':head,'pending':len(requests),'pending_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'ids':[x['id'] for x in requests]}))
