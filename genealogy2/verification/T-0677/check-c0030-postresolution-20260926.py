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
assert max(int(p.name[:9]) for p in (R/'genealogy2/journal').glob('*.json'))==195
expected=load('c0030-split-temp-full-diffcheck-20260925.json')['items']
actual=[]
for e in expected:
 rid=e['after']['revision']['id'];now=full(rid)
 assert norm(now)==norm(e['after']),rid
 assert rows('select max(version) as v from revision where object_id=?',(e['id'],))[0]['v']==now['revision']['version'],rid
 actual.append({'id':e['id'],'before':e['before'],'after':now,'changed_typed_fields':e['changed_typed_fields']})
assert len(actual)==12
# Resolution verification after exact source/person checks.
assert rows('select count(*) as n from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null')[0]['n']==0
approval=load('c0030-root-canonical-approval-20260926.json')
operation=load('c0030-4-actual-retains-proposed-operation-20260926.json')
expected_pending=load('c0030-split-temp-after-pending-full-20260925.json')['requests']
judgements={x['request_id']:x for x in approval['dependency_judgements']}
actual_resolutions=[]
for req in expected_pending:
 q=rows('select q.*,z.operation_id as resolution_operation,z.rationale as resolution_rationale from review_request q join review_resolution z on z.request_id=q.id where q.id=?',(req['id'],))
 assert len(q)==1 and q[0]['operation_id']==req['operation_id'] and q[0]['affected_revision_id']==req['affected_revision_id'] and q[0]['changed_revision_id']==req['changed_revision_id'] and q[0]['reason']==req['reason']
 assert q[0]['resolution_operation']==operation['id'] and q[0]['resolution_rationale']==judgements[req['id']]['rationale']
 actual_resolutions.append(q[0])
assert len(actual_resolutions)==4 and {x['id'] for x in actual_resolutions}=={x['request'] for x in operation['resolve']}
assert operation['changes']==[]
for n in ('verify','verify-assets','verify-source'):
 assert load(f'c0030-canonical-{n}-20260926.json')['ok'] is True
fh=write('c0030-postresolution-full-objects-20260926.json',{'task':'T-0677','state':'CANONICAL_J195_FULL_12_MATCHES_TEMP','journal':195,'objects':actual})
rh=write('c0030-actual-resolutions-20260926.json',{'task':'T-0677','state':'CANONICAL_FOUR_EXACT_RESOLUTIONS','journal':195,'pending':0,'resolutions':actual_resolutions})
print(json.dumps({'full_objects_sha256':fh,'resolutions_sha256':rh,'objects':len(actual),'resolutions':len(actual_resolutions),'pending':0,'validators':'3 PASS'}))
