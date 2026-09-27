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
temp=db(TMP)
assert max(int(p.name[:9]) for p in Path('/private/tmp/t0677-c0032-preflight-20260926/journal').glob('*.json'))==201
pending=[]
for q in rows(temp,'select q.* from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null order by q.id'):
 to=full(temp,q['changed_revision_id']);before=full(temp,to['revision']['previous_id'])
 pending.append({**q,'affected_full':full(temp,q['affected_revision_id']),'changed_from_full':before,'changed_to_full':to})
assert len(pending)==45
ph=write('c0032-split-temp-pending-full-20260926.json',{'task':'T-0677','state':'ISOLATED_TEMP_PENDING_UNRESOLVED','canonical_base_journal':198,'temp_journal':201,'count':len(pending),'requests':pending})
print(json.dumps({'pending_full_sha256':ph,'count':len(pending)}))
