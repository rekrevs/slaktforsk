"""Capture and compare the sole canonical C-0004 pending request; no resolve."""
import hashlib
import json
import sqlite3
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
TEMP=HERE/'c0004-temp-pending-full-20260925.json'
OP=HERE/'c0004-combined-proposed-operation-20260925.json'
OUT=HERE/'c0004-actual-pending-full-20260925.json'
MATCH=HERE/'c0004-actual-pending-match-20260925.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
temp=json.loads(TEMP.read_text())
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(r) for r in conn.execute(sql,args)]
def full(rid):
    rev=rows('SELECT * FROM revision WHERE id=?',(rid,));assert len(rev)==1
    rev=rev[0];obj=rows('SELECT kind FROM object WHERE id=?',(rev['object_id'],));assert len(obj)==1
    kind=obj[0]['kind'];data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rid,));assert len(data)==1
    data=data[0];data.pop('revision_id')
    for key,value in list(data.items()):
        if key.endswith('_json') and value is not None:data[key]=json.loads(value)
    origins=[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']}
             for r in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rid,))]
    evidence=[]
    for r in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rid,)):
        basis,version=r['basis_revision_id'].rsplit('@',1)
        evidence.append({'object':basis,'version':int(version),'role':r['role'],'note':r['note']})
    return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}
rs=rows('''SELECT rr.* FROM review_request rr
           LEFT JOIN review_resolution res ON res.request_id=rr.id
           WHERE rr.operation_id=? AND res.request_id IS NULL ORDER BY rr.id''',
        ('T-0677/C0004-source-impact-adoptions-v1',))
assert len(rs)==1
requests=[{**r,'affected_full':full(r['affected_revision_id']),
           'changed_full':full(r['changed_revision_id'])} for r in rs]
actual={'task':'T-0677','state':'CANONICAL_ACTUAL_PENDING_NOT_RESOLVED',
        'canonical_journal_head':183,'operation_sha256':sha(OP),'count':1,
        'requests':requests,'no_resolution':True}
OUT.write_text(json.dumps(actual,ensure_ascii=False,indent=2)+'\n')
assert temp['operation_sha256']==sha(OP) and len(temp['requests'])==1
t=temp['requests'][0];r=requests[0]
fields=('id','operation_id','reason','affected_revision_id','changed_revision_id',
        'affected_full','changed_full')
discrepancies=[{'field':f,'temp':t[f],'actual':r[f]} for f in fields if t[f]!=r[f]]
assert not discrepancies,discrepancies
match={'task':'T-0677','state':'CANONICAL_ACTUAL_PENDING_EXACT_TEMP_MATCH_NOT_RESOLVED',
       'canonical_journal_head':183,'operation_sha256':sha(OP),
       'actual_pending_sha256':sha(OUT),'temp_pending_sha256':sha(TEMP),
       'request_id':r['id'],'affected_revision_id':r['affected_revision_id'],
       'changed_revision_id':r['changed_revision_id'],'full_payload_match':True,
       'discrepancies_only':discrepancies,'no_resolution':True}
MATCH.write_text(json.dumps(match,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'actual_sha256':sha(OUT),'match_sha256':sha(MATCH),
                  'request_id':r['id'],'discrepancies':len(discrepancies)}))
