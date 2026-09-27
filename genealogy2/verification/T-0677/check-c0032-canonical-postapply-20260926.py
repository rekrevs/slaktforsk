"""Exact read-only C0031 temp/canonical comparison; writes verification JSON only."""
import hashlib,json,sqlite3
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
TMP=Path('/private/tmp/t0677-c0032-preflight-20260926/research.sqlite')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda n:json.loads((H/n).read_text())
def rows(c,q,a=()):return [dict(x) for x in c.execute(q,a)]
def db(p):
 c=sqlite3.connect(f'file:{p}?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
def full(c,rid):
 if rid is None:return None
 rev=rows(c,'select * from revision where id=?',(rid,))[0]
 kind=rows(c,'select kind from object where id=?',(rev['object_id'],))[0]['kind']
 data=rows(c,f'select * from {kind} where revision_id=?',(rid,))[0];data.pop('revision_id')
 for k,v in list(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in rows(c,'select unit_id,coverage,note from origin where revision_id=?',(rid,))]
 evidence=[]
 for x in rows(c,'select basis_revision_id,role,note from dependency where revision_id=?',(rid,)):
  o,v=x['basis_revision_id'].rsplit('@',1);evidence.append({'object':o,'version':int(v),'role':x['role'],'note':x['note']})
 media=[]
 if kind=='record':
  media.extend([{'path':x['path'],'sha256':x['sha256'],'bytes':x['bytes'],'region':x['region'],'origin':'legacy'} for x in rows(c,'select a.path,a.sha256,a.bytes,ra.region from record_asset ra join asset a on a.path=ra.asset_path where ra.revision_id=?',(rid,))])
  media.extend([{'path':x['storage_path'],'sha256':x['sha256'],'bytes':x['bytes'],'region':x['region'],'origin':'native','id':x['id']} for x in rows(c,'select a.id,a.storage_path,a.sha256,a.bytes,rm.region from record_media rm join native_asset a on a.id=rm.asset_id where rm.revision_id=?',(rid,))])
 return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence,'media':media}
def norm(x):
 if isinstance(x,dict):return {k:norm(v) for k,v in x.items()}
 if isinstance(x,list):return sorted((norm(v) for v in x),key=lambda z:json.dumps(z,sort_keys=True,ensure_ascii=False))
 return x
def write(n,obj):
 p=H/n;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');return sha(p)
# Run only after root-approved three-step canonical apply; no resolution yet.
actual=db(ROOT/'genealogy2/data/research.sqlite')
assert max(int(p.name[:9]) for p in (ROOT/'genealogy2/journal').glob('*.json'))==201
expected=load('c0032-split-temp-full-diffcheck-20260926.json')['items']
def same(a,b):
 return a['kind']==b['kind'] and a['revision']==b['revision'] and a['data']==b['data'] and norm(a['origins'])==norm(b['origins']) and norm(a['evidence'])==norm(b['evidence']) and norm(a['media'])==norm(b['media'])
items=[]
for e in expected:
 rid=e['after']['revision']['id'];a=full(actual,rid)
 assert same(a,e['after']),rid
 assert rows(actual,'select id from current_revision where object_id=?',(e['id'],))[0]['id']==rid
 items.append({'id':e['id'],'operation_id':e['operation_id'],'before':e['before'],'after':a,'changed_typed_fields':e['changed_typed_fields']})
assert len(items)==57
pending=[]
for q in rows(actual,'select q.* from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null order by q.id'):
 to=full(actual,q['changed_revision_id']);before=full(actual,to['revision']['previous_id'])
 pending.append({**q,'affected_full':full(actual,q['affected_revision_id']),'changed_from_full':before,'changed_to_full':to})
expected_pending=load('c0032-split-temp-pending-full-20260926.json')['requests']
assert len(pending)==len(expected_pending)==45
for a,e in zip(pending,expected_pending):
 assert all(a[k]==e[k] for k in ('id','operation_id','affected_revision_id','changed_revision_id','reason'))
 for k in ('affected_full','changed_from_full','changed_to_full'):assert same(a[k],e[k]),(a['id'],k)
fh=write('c0032-canonical-actual-full-diffcheck-20260926.json',{'task':'T-0677','state':'CANONICAL_ACTUAL_FULL_MATCHES_SPLIT_TEMP','journal':201,'items':items,'counts':{'objects':57,'source':6,'person':50,'death_observation':1,'creates':7,'revisions':50}})
ph=write('c0032-canonical-actual-pending-full-20260926.json',{'task':'T-0677','state':'CANONICAL_ACTUAL_PENDING_UNRESOLVED','journal':201,'count':45,'requests':pending})
print(json.dumps({'full_diff_sha256':fh,'pending_sha256':ph,'objects':57,'pending':45,'exact_match':True}))
