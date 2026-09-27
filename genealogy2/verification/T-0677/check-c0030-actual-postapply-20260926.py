"""Read-only exact C0030 canonical-vs-isolated comparison; writes verification artifacts only."""
import hashlib,json,sqlite3
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[2];DB=R/'genealogy2/data/research.sqlite'
load=lambda n:json.loads((H/n).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,obj):
 p=H/n;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');return sha(p)
con=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);con.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(x) for x in con.execute(sql,args)]
def full(rid):
 rev=rows('select * from revision where id=?',(rid,))[0]
 kind=rows('select kind from object where id=?',(rev['object_id'],))[0]['kind']
 data=rows(f'select * from {kind} where revision_id=?',(rid,))[0];data.pop('revision_id')
 for k,v in list(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in rows('select unit_id,coverage,note from origin where revision_id=?',(rid,))]
 evidence=[]
 for x in rows('select basis_revision_id,role,note from dependency where revision_id=?',(rid,)):
  o,v=x['basis_revision_id'].rsplit('@',1);evidence.append({'object':o,'version':int(v),'role':x['role'],'note':x['note']})
 return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}
def norm(x):
 if isinstance(x,dict):return {k:norm(v) for k,v in x.items()}
 if isinstance(x,list):return sorted((norm(v) for v in x),key=lambda z:json.dumps(z,ensure_ascii=False,sort_keys=True))
 return x
assert max(int(p.name[:9]) for p in (R/'genealogy2/journal').glob('*.json'))==194
expected=load('c0030-split-temp-full-diffcheck-20260925.json')['items']
actual=[]
for e in expected:
 rid=e['after']['revision']['id'];now=full(rid)
 assert norm(now)==norm(e['after']),rid
 assert rows('select max(version) as v from revision where object_id=?',(e['id'],))[0]['v']==now['revision']['version'],rid
 actual.append({'id':e['id'],'before':e['before'],'after':now,'changed_typed_fields':e['changed_typed_fields']})
assert len(actual)==12
pending=[]
for q in rows('select q.* from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null order by q.id'):
 pending.append({'id':q['id'],'operation_id':q['operation_id'],'affected_revision_id':q['affected_revision_id'],'changed_revision_id':q['changed_revision_id'],'reason':q['reason'],'affected_full':full(q['affected_revision_id']),'changed_full':full(q['changed_revision_id'])})
expected_pending=load('c0030-split-temp-after-pending-full-20260925.json')['requests']
assert len(pending)==4 and norm(pending)==norm(expected_pending)
fh=write('c0030-actual-full-diffcheck-20260926.json',{'task':'T-0677','state':'CANONICAL_ACTUAL_FULL_MATCHES_SPLIT_TEMP','journal':194,'items':actual,'counts':{'objects':12,'creates':6,'revisions':6}})
ph=write('c0030-actual-pending-full-20260926.json',{'task':'T-0677','state':'CANONICAL_ACTUAL_PENDING_UNRESOLVED','journal':194,'count':len(pending),'requests':pending})
print(json.dumps({'actual_full_diff_sha256':fh,'actual_pending_sha256':ph,'objects':len(actual),'pending':len(pending),'exact_match':True}))
