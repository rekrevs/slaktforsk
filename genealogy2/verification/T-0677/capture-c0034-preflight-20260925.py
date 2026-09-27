"""Read-only C-0034 temp pending and canonical-before full diff."""
import hashlib
import json
import sqlite3
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
CANON=ROOT/'genealogy2/data/research.sqlite'
TEMP=Path('/private/tmp/t0677-c0034-preflight-20260925/research.sqlite')
OP=HERE/'c0034-combined-proposed-operation-20260925.json'
BUILD=HERE/'c0034-combined-buildcheck-20260925.json'
OUT_DIFF=HERE/'c0034-combined-full-diffcheck-20260925.json'
OUT_PENDING=HERE/'c0034-temp-pending-full-20260925.json'
OUT_SUMMARY=HERE/'c0034-temp-preflight-summary-20260925.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
op=load(OP);build=load(BUILD)
assert build['operation_sha256']==sha(OP) and len(op['changes'])==15
def db(path):
    c=sqlite3.connect(f'file:{path}?mode=ro',uri=True);c.row_factory=sqlite3.Row
    return c
canonical,temp=db(CANON),db(TEMP)
def rows(c,sql,args=()):return [dict(x) for x in c.execute(sql,args)]
def full(c,rid):
    revs=rows(c,'SELECT * FROM revision WHERE id=?',(rid,));assert len(revs)==1,rid
    rev=revs[0]
    obj=rows(c,'SELECT kind FROM object WHERE id=?',(rev['object_id'],));assert len(obj)==1
    kind=obj[0]['kind']
    data=rows(c,f'SELECT * FROM {kind} WHERE revision_id=?',(rid,));assert len(data)==1
    data=data[0];data.pop('revision_id')
    for key,value in list(data.items()):
        if key.endswith('_json') and value is not None:data[key]=json.loads(value)
    origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']}
             for x in rows(c,'SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rid,))]
    evidence=[]
    for x in rows(c,'SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rid,)):
        basis,version=x['basis_revision_id'].rsplit('@',1)
        evidence.append({'object':basis,'version':int(version),'role':x['role'],'note':x['note']})
    return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}

items=[]
for c in op['changes']:
    oid,version=c['id'],c['expectedVersion']
    old=full(canonical,f'{oid}@{version}') if version is not None else None
    latest=rows(temp,'SELECT id,version FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
    assert len(latest)==1
    new=full(temp,latest[0]['id'])
    assert new['revision']['version']==(version+1 if version is not None else 1)
    assert new['data']==c['data'],oid
    assert new['revision']['caveat']==c['caveat'],oid
    assert new['revision']['operation_id']==op['id'],oid
    assert new['revision']['disposition']==c['disposition'],oid
    assert new['revision']['evidence_status']==c['evidenceStatus'],oid
    assert new['revision']['rationale']==c['rationale'],oid
    assert sorted(new['origins'],key=lambda x:x['unit'])==sorted(c.get('origins',[]),key=lambda x:x['unit']),oid
    assert sorted(new['evidence'],key=lambda x:(x['object'],x['version'],x['role'],x['note']))==sorted(
        c['evidence'],key=lambda x:(x['object'],x['version'],x['role'],x['note'])),oid
    items.append({'id':oid,'action':'create' if old is None else 'revise','before':old,'after':new,
                  'changed_typed_data_fields':[] if old is None else [k for k in sorted(set(old['data'])|set(new['data']))
                      if old['data'].get(k)!=new['data'].get(k)],
                  'origins_preserved':old is None or old['origins']==new['origins']})
assert len(items)==15 and sum(x['action']=='create' for x in items)==7
assert all(x['origins_preserved'] for x in items)
diff={'task':'T-0677','state':'TEMP_ACTUAL_FULL_DIFF_NOT_CANONICAL_APPLY',
      'canonical_base_journal':190,'operation_sha256':sha(OP),'items':items,
      'counts':{'objects':15,'creates':7,'revisions':8}}
OUT_DIFF.write_text(json.dumps(diff,ensure_ascii=False,indent=2)+'\n')

results_count=json.loads((HERE/'c0034-temp-apply-result-20260925.json').read_text())['pendingReviews']
pending=rows(temp,'''SELECT rr.* FROM review_request rr
                     LEFT JOIN review_resolution rs ON rs.request_id=rr.id
                     WHERE rr.operation_id=? AND rs.request_id IS NULL ORDER BY rr.id''',(op['id'],))
assert len(pending)==results_count
requests=[{**r,'affected_full':full(temp,r['affected_revision_id']),
           'changed_full':full(temp,r['changed_revision_id'])} for r in pending]
packet={'task':'T-0677','state':'TEMP_ACTUAL_PENDING_NOT_RESOLVED',
        'operation_sha256':sha(OP),'count':len(requests),'requests':requests,'no_resolution':True}
OUT_PENDING.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
results={n:{'sha256':sha(HERE/f'c0034-temp-{n}-result-20260925.json'),
            'result':load(HERE/f'c0034-temp-{n}-result-20260925.json')}
         for n in ('apply','verify','verify-assets','verify-source')}
assert results['apply']['result']['changes']==15
assert results['apply']['result']['pendingReviews']==len(pending)
assert all(results[n]['result']['ok'] for n in ('verify','verify-assets','verify-source'))
summary={'task':'T-0677','state':'TEMP_VALIDATED_FOR_ROOT_REVIEW_NOT_CANONICAL_APPLY',
         'canonical_base_journal':190,'canonical_pending_at_last_check':0,
         'operation_sha256':sha(OP),'buildcheck_sha256':sha(BUILD),
         'full_diff_sha256':sha(OUT_DIFF),'pending_full_sha256':sha(OUT_PENDING),
         'temp_results':results,'temp_pending_count':len(pending),'no_canonical_apply':True,
         'no_pending_resolution':True}
OUT_SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'operation_sha256':sha(OP),'diff_sha256':sha(OUT_DIFF),
                  'pending_sha256':sha(OUT_PENDING),'summary_sha256':sha(OUT_SUMMARY),
                  'pending_request_ids':[r['id'] for r in requests]}))
