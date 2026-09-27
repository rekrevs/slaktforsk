"""Full C0030 split temp before/after and validator capture; no canonical write."""
import hashlib,json,sqlite3
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
CAN=ROOT/'genealogy2/data/research.sqlite';TMP=Path('/private/tmp/t0677-c0030-split-preflight-20260925/research.sqlite')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
ops=[H/f'c0030-{n}-split-proposed-operation-20260925.json' for n in ('source','person')]
changes=[x for p in ops for x in load(p)['changes']]
assert len(changes)==12 and len({x['id'] for x in changes})==12
build=load(H/'c0030-combined-buildcheck-20260925.json');assert {x['id'] for x in build['full_before_after']}=={x['id'] for x in changes}
def db(p):
 c=sqlite3.connect(f'file:{p}?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
canonical,temp=db(CAN),db(TMP)
def rows(c,q,a=()):return [dict(x) for x in c.execute(q,a)]
def full(c,rid):
 rev=rows(c,'SELECT * FROM revision WHERE id=?',(rid,))[0];kind=rows(c,'SELECT kind FROM object WHERE id=?',(rev['object_id'],))[0]['kind']
 data=rows(c,f'SELECT * FROM {kind} WHERE revision_id=?',(rid,))[0];data.pop('revision_id')
 for k,v in list(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in rows(c,'SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rid,))]
 evidence=[]
 for x in rows(c,'SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rid,)):
  o,v=x['basis_revision_id'].rsplit('@',1);evidence.append({'object':o,'version':int(v),'role':x['role'],'note':x['note']})
 return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}
def sorted_edges(x):return sorted(x,key=lambda e:(e['object'],e['version'],e['role'],e['note']))
items=[]
for opfile in ops:
 op=load(opfile)
 for x in op['changes']:
  oid=x['id'];v=x['expectedVersion']
  old=full(canonical,f'{oid}@{v}') if v is not None else None
  latest=rows(temp,'SELECT id FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,));assert len(latest)==1
  new=full(temp,latest[0]['id'])
  assert new['revision']['version']==(v+1 if v is not None else 1) and new['revision']['operation_id']==op['id']
  assert new['data']==x['data'] and new['revision']['disposition']==x['disposition'] and new['revision']['evidence_status']==x['evidenceStatus'] and new['revision']['rationale']==x['rationale'] and new['revision']['caveat']==x['caveat'],oid
  assert sorted(new['origins'],key=lambda e:e['unit'])==sorted(x.get('origins',[]),key=lambda e:e['unit']),oid
  assert sorted_edges(new['evidence'])==sorted_edges(x['evidence']),oid
  items.append({'id':oid,'operation_id':op['id'],'action':'create' if old is None else 'revise','before':old,'after':new,'changed_typed_fields':[] if old is None else [k for k in sorted(set(old['data'])|set(new['data'])) if old['data'].get(k)!=new['data'].get(k)]})
assert len(items)==12
p=H/'c0030-split-temp-full-diffcheck-20260925.json'
p.write_text(json.dumps({'task':'T-0677','state':'ISOLATED_SPLIT_FULL_DIFF_NOT_CANONICAL','canonical_base_journal':192,'operation_sha256':{n:sha(f) for n,f in zip(('source','person'),ops)},'items':items,'counts':{'objects':12,'creates':6,'revisions':6}},ensure_ascii=False,indent=2)+'\n')
stages={n:{'sha256':sha(H/f'c0030-split-temp-{n}-pending-full-20260925.json'),'data':load(H/f'c0030-split-temp-{n}-pending-full-20260925.json')} for n in ('source','after')}
assert stages['source']['data']['count']==0 and stages['after']['data']['count']==4
results={n:{'sha256':sha(H/f'c0030-split-temp-{n}-result-20260925.json'),'result':load(H/f'c0030-split-temp-{n}-result-20260925.json')} for n in ('source-apply','person-apply','verify','verify-assets','verify-source')}
assert results['source-apply']['result']['changes']==4 and results['person-apply']['result']['changes']==8
assert all(results[n]['result']['ok'] for n in ('verify','verify-assets','verify-source'))
summary={'task':'T-0677','state':'ISOLATED_SPLIT_VALIDATED_FOR_ROOT_REVIEW_NOT_CANONICAL','canonical_base_journal':192,'canonical_pending_at_last_check':0,'operation_sha256':{n:sha(f) for n,f in zip(('source','person'),ops)},'full_diff_sha256':sha(p),'stage_pending':stages,'results':results,'no_canonical_apply_or_resolution':True}
s=H/'c0030-split-temp-preflight-summary-20260925.json';s.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'full_diff_sha256':sha(p),'summary_sha256':sha(s),'pending_intermediate':0,'pending_after':4,'pending_after_sha256':stages['after']['sha256']}))
