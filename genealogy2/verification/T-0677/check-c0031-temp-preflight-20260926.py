"""Exact read-only C0031 temp/canonical comparison; writes verification JSON only."""
import hashlib,json,sqlite3
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
TMP=Path('/private/tmp/t0677-c0031-preflight-20260926/research.sqlite')
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
canonical,temp=db(ROOT/'genealogy2/data/research.sqlite'),db(TMP)
approval=load('c0031-root-content-approval-for-temp-20260926.json')
assert all(sha(H/x['file'])==x['sha256'] for x in approval['inputs'])
assert max(int(p.name[:9]) for p in (ROOT/'genealogy2/journal').glob('*.json'))==195
assert rows(canonical,'select count(*) n from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null')[0]['n']==0
ops=[load('c0031-source-proposed-operation-20260926.json'),load('c0031-person-proposed-operation-20260926.json')]
proposals=[load('c0031-native-source-proposal-20260926.json')['operation'],load('c0031-person-impact-proposal-20260926.json')['operation']]
for op,proposal in zip(ops,proposals):
 assert op['id']==proposal['id'] and op['actor']==proposal['actor'] and op['reason']==proposal['reason'] and op['dependencyReviewVersion']==2
 expected=json.loads(json.dumps(proposal['changes']))
 for x in expected:
  if x['expectedVersion']==0:x['expectedVersion']=None
 assert op['changes']==expected
 assert all(x['expectedVersion'] is None or x['expectedVersion']>=1 for x in op['changes'])
items=[]
for op in ops:
 for x in op['changes']:
  oid=x['id'];v=x['expectedVersion'];old=full(canonical,f'{oid}@{v}') if v else None
  current=rows(canonical,'select max(version) v from revision where object_id=?',(oid,))[0]['v'];assert current==v,(oid,current,v)
  rid=f'{oid}@{(v or 0)+1}';new=full(temp,rid)
  assert new['kind']==x['kind'] and new['data']==x['data'] and new['revision']['operation_id']==op['id']
  assert new['revision']['version']==(v or 0)+1 and new['revision']['previous_id']==(old['revision']['id'] if old else None)
  assert all(new['revision'][k]==x[y] for k,y in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')])
  assert norm(new['origins'])==norm(x.get('origins',[])) and norm(new['evidence'])==norm(x.get('evidence',[]))
  if x['kind']=='record':
   assets=[{'path':a['path'],'sha256':rows(temp,'select sha256 from asset where path=?',(a['path'],))[0]['sha256'],'bytes':rows(temp,'select bytes from asset where path=?',(a['path'],))[0]['bytes'],'region':a['region'],'origin':'legacy'} for a in x.get('assets',[])]
   assert norm(new['media'])==norm(assets)
   assert norm(old['media'])==norm(new['media']) # retained exactly across R revision
  else:assert not new['media']
  head=rows(temp,'select id from current_revision where object_id=?',(oid,))[0]['id'];assert head==rid
  items.append({'id':oid,'operation_id':op['id'],'before':old,'after':new,'changed_typed_fields':[] if old is None else [k for k in sorted(set(old['data'])|set(new['data'])) if old['data'].get(k)!=new['data'].get(k)]})
assert len(items)==15 and len({x['id'] for x in items})==15
pending=[]
for q in rows(temp,'select q.* from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null order by q.id'):
 changed_to=full(temp,q['changed_revision_id']);changed_from=full(temp,changed_to['revision']['previous_id'])
 pending.append({**q,'affected_full':full(temp,q['affected_revision_id']),'changed_from_full':changed_from,'changed_to_full':changed_to})
assert len(pending)==4
assert all(load(f'c0031-temp-{n}-20260926.json')['ok'] is True for n in ['verify','verify-assets','verify-source'])
full_sha=write('c0031-temp-full-diffcheck-20260926.json',{'task':'T-0677','state':'ISOLATED_TEMP_FULL_DIFF_NOT_CANONICAL','canonical_base_journal':195,'items':items,'counts':{'objects':15,'source':6,'person':9,'creates':7,'revisions':8}})
pending_sha=write('c0031-temp-pending-full-20260926.json',{'task':'T-0677','state':'ISOLATED_TEMP_PENDING_UNRESOLVED','canonical_base_journal':195,'count':len(pending),'requests':pending})
summary={'task':'T-0677','state':'TEMP_VALIDATED_FOR_ROOT_REVIEW_NOT_CANONICAL','canonical_base_journal':195,'canonical_pending':0,'operation_sha256':{n:sha(H/f'c0031-{n}-proposed-operation-20260926.json') for n in ('source','person')},'temp_journal':[p.name for p in sorted(Path('/private/tmp/t0677-c0031-preflight-20260926/journal').glob('*.json'))],'source_apply':load('c0031-temp-source-apply-result-20260926.json'),'person_apply':load('c0031-temp-person-apply-result-20260926.json'),'full_diff_sha256':full_sha,'pending_full_sha256':pending_sha,'validator_results':{n:load(f'c0031-temp-{n}-20260926.json')['ok'] for n in ['verify','verify-assets','verify-source']},'no_canonical_apply_or_resolution':True}
summary_sha=write('c0031-temp-preflight-summary-20260926.json',summary)
print(json.dumps({'full_diff_sha256':full_sha,'pending_full_sha256':pending_sha,'summary_sha256':summary_sha,'objects':len(items),'pending':len(pending)}))
