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
canonical,temp=db(ROOT/'genealogy2/data/research.sqlite'),db(TMP)
approval=load('c0032-root-content-approval-for-temp-20260926.json')
amendment=load('c0032-root-specific-split-amendment-20260926.json')
assert all(sha(H/x['file'])==x['sha256'] for x in approval['inputs'])
assert sha(H/amendment['input_person']['file'])==amendment['input_person']['sha256']
assert max(int(p.name[:9]) for p in (ROOT/'genealogy2/journal').glob('*.json'))==198
assert rows(canonical,'select count(*) n from review_request q left join review_resolution z on z.request_id=q.id where z.request_id is null')[0]['n']==0
assert max(int(p.name[:9]) for p in Path('/private/tmp/t0677-c0032-preflight-20260926/journal').glob('*.json'))==201
source=load('c0032-source-proposed-operation-20260926.json')
person=load('c0032-person-split-proposed-operation-20260926.json')
death=load('c0032-death-observation-split-proposed-operation-20260926.json')
source_proposal=load('c0032-native-source-proposal-v2-20260926.json')['operation']
person_proposal=load('c0032-person-impact-proposal-v3-20260926.json')['operation']
def normal_changes(changes):
 out=json.loads(json.dumps(changes))
 for x in out:
  if x['expectedVersion']==0:x['expectedVersion']=None
 return out
assert source['changes']==normal_changes(source_proposal['changes']) and source['dependencyReviewVersion']==2
expected_person=normal_changes(person_proposal['changes'])
edge=amendment['specific_edge_change']
assert len(expected_person)==51 and len(person['changes'])==50 and len(death['changes'])==1
expected_p=[x for x in expected_person if x['id']!='O-P-0042-death1937-death_entry']
event=next(x for x in expected_p if x['id']==edge['dependent'])
edge_matches=[e for e in event['evidence'] if e['object']==edge['basis'] and e['version']==edge['old_version'] and e['role']==edge['role'] and e['note']==edge['old_note']]
assert len(edge_matches)==1
edge_matches[0]['version']=edge['new_version'];edge_matches[0]['note']=edge['new_note']
assert person['changes']==expected_p and death['changes']==[x for x in expected_person if x['id']=='O-P-0042-death1937-death_entry']
assert person['dependencyReviewVersion']==death['dependencyReviewVersion']==2
ops=[source,person,death]
before_snapshot=load('c0032-proposal-full-before-j198-20260926.json')['objects']
def same(a,b):
 return a['kind']==b['kind'] and a['revision']==b['revision'] and a['data']==b['data'] and norm(a['origins'])==norm(b['origins']) and norm(a['evidence'])==norm(b['evidence']) and norm(a['media'])==norm(b['media'])
items=[]
for op in ops:
 for x in op['changes']:
  oid=x['id'];v=x['expectedVersion'];old=full(canonical,f'{oid}@{v}') if v else None
  assert rows(canonical,'select max(version) v from revision where object_id=?',(oid,))[0]['v']==v,oid
  snap=before_snapshot.get(oid)
  if old is None:assert snap is None,oid
  else:
   assert snap is not None and snap['kind']==old['kind'] and snap['revision']==old['revision'] and snap['data']==old['data'] and norm(snap['origins'])==norm(old['origins']) and norm(snap['evidence'])==norm(old['evidence']) and norm([{**a,'origin':'legacy'} for a in snap['assets']])==norm(old['media']),oid
  rid=f'{oid}@{(v or 0)+1}';new=full(temp,rid)
  assert new['kind']==x['kind'] and new['data']==x['data'] and new['revision']['operation_id']==op['id'],oid
  assert new['revision']['version']==(v or 0)+1 and new['revision']['previous_id']==(old['revision']['id'] if old else None),oid
  assert all(new['revision'][k]==x[y] for k,y in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')]),oid
  assert norm(new['origins'])==norm(x.get('origins',[])) and norm(new['evidence'])==norm(x.get('evidence',[])),oid
  if x['kind']=='record':
   assets=[{'path':a['path'],'sha256':rows(temp,'select sha256 from asset where path=?',(a['path'],))[0]['sha256'],'bytes':rows(temp,'select bytes from asset where path=?',(a['path'],))[0]['bytes'],'region':a['region'],'origin':'legacy'} for a in x.get('assets',[])]
   assert norm(new['media'])==norm(assets) and norm(old['media'])==norm(new['media']),oid
  else:assert not new['media'],oid
  assert rows(temp,'select id from current_revision where object_id=?',(oid,))[0]['id']==rid
  items.append({'id':oid,'operation_id':op['id'],'before':old,'after':new,'changed_typed_fields':[] if old is None else [k for k in sorted(set(old['data'])|set(new['data'])) if old['data'].get(k)!=new['data'].get(k)]})
assert len(items)==57 and len({x['id'] for x in items})==57
pending=load('c0032-split-temp-pending-full-20260926.json')
assert pending['count']==45
for q in pending['requests']:
 to=full(temp,q['changed_revision_id']);assert same(to,q['changed_to_full'])
 assert same(full(temp,to['revision']['previous_id']),q['changed_from_full'])
 assert same(full(temp,q['affected_revision_id']),q['affected_full'])
assert all(load(f'c0032-temp-{n}-20260926.json')['ok'] is True for n in ('verify','verify-assets','verify-source'))
fh=write('c0032-split-temp-full-diffcheck-20260926.json',{'task':'T-0677','state':'ISOLATED_SPLIT_TEMP_FULL_DIFF_NOT_CANONICAL','canonical_base_journal':198,'temp_journal':201,'items':items,'counts':{'objects':57,'source':6,'person':50,'death_observation':1,'creates':7,'revisions':50}})
summary={'task':'T-0677','state':'ISOLATED_SPLIT_TEMP_VALIDATED_FOR_ROOT_REVIEW_NOT_CANONICAL','canonical_base_journal':198,'canonical_pending':0,'operation_sha256':{n:sha(H/f'c0032-{n}-proposed-operation-20260926.json') for n in ('source','person-split','death-observation-split')},'full_diff_sha256':fh,'pending_full_sha256':sha(H/'c0032-split-temp-pending-full-20260926.json'),'counts':{'objects':57,'pending':45},'apply_results':{n:load(f'c0032-temp-{n}-apply-result-20260926.json') for n in ('source','person-split','death-observation')},'validator_results':{n:load(f'c0032-temp-{n}-20260926.json')['ok'] for n in ('verify','verify-assets','verify-source')},'no_canonical_apply_or_resolution':True}
sh=write('c0032-split-temp-preflight-summary-20260926.json',summary)
print(json.dumps({'full_diff_sha256':fh,'summary_sha256':sh,'pending_sha256':summary['pending_full_sha256'],'objects':57,'pending':45}))
