"""Read-only full C-0028 canonical after/diff and zero-pending comparison."""
import hashlib
import json
import sqlite3
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DB=ROOT/'genealogy2/data/research.sqlite'
OP=HERE/'c0028-combined-proposed-operation-20260925.json'
TEMP_DIFF=HERE/'c0028-combined-full-diffcheck-20260925.json'
TEMP_PENDING=HERE/'c0028-temp-pending-full-20260925.json'
OUT=HERE/'c0028-actual-full-diffcheck-20260925.json'
PENDING=HERE/'c0028-actual-pending-full-20260925.json'
MATCH=HERE/'c0028-actual-temp-match-20260925.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
op=load(OP);temp_diff=load(TEMP_DIFF);temp_pending=load(TEMP_PENDING)
assert len(op['changes'])==12 and sha(OP)==temp_diff['operation_sha256']==temp_pending['operation_sha256']
conn=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);conn.row_factory=sqlite3.Row
def rows(sql,args=()):return [dict(x) for x in conn.execute(sql,args)]
def full(rid):
 revs=rows('SELECT * FROM revision WHERE id=?',(rid,));assert len(revs)==1,rid
 rev=revs[0];obj=rows('SELECT kind FROM object WHERE id=?',(rev['object_id'],));assert len(obj)==1
 kind=obj[0]['kind'];data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rid,));assert len(data)==1
 data=data[0];data.pop('revision_id')
 for key,value in tuple(data.items()):
  if key.endswith('_json') and value is not None:data[key]=json.loads(value)
 origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']}
          for x in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rid,))]
 evidence=[]
 for x in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rid,)):
  basis,version=x['basis_revision_id'].rsplit('@',1)
  evidence.append({'object':basis,'version':int(version),'role':x['role'],'note':x['note']})
 return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}
items=[]
for change in op['changes']:
 oid,oldversion=change['id'],change['expectedVersion']
 before=full(f'{oid}@{oldversion}') if oldversion is not None else None
 newversion=(oldversion or 0)+1
 after=full(f'{oid}@{newversion}')
 latest=rows('SELECT id FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))
 assert latest[0]['id']==after['revision']['id']
 items.append({'id':oid,'action':'create' if before is None else 'revise',
  'before':before,'after':after,'changed_typed_data_fields':[] if before is None else
    [k for k in sorted(set(before['data'])|set(after['data'])) if before['data'].get(k)!=after['data'].get(k)],
  'origins_preserved':before is None or before['origins']==after['origins']})
head=sorted((ROOT/'genealogy2/journal').glob('*.json'))[-1].name
assert head.startswith('000000189-')
actual={'task':'T-0677','state':'CANONICAL_ACTUAL_FULL_DIFF_AFTER_APPLY',
 'canonical_journal_head':head,'operation_sha256':sha(OP),'items':items,
 'counts':{'objects':12,'creates':7,'revisions':5}}
OUT.write_text(json.dumps(actual,ensure_ascii=False,indent=2)+'\n')
pending=rows('''SELECT rr.* FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id
 WHERE rr.operation_id=? AND rs.request_id IS NULL ORDER BY rr.id''',(op['id'],))
assert pending==[]
pending_packet={'task':'T-0677','state':'CANONICAL_ACTUAL_PENDING_EMPTY',
 'canonical_journal_head':head,'operation_sha256':sha(OP),'count':0,'requests':[],
 'no_resolution':True}
PENDING.write_text(json.dumps(pending_packet,ensure_ascii=False,indent=2)+'\n')
assert len(temp_diff['items'])==len(items)==12
discrepancies=[]
for actual_item,temp_item in zip(items,temp_diff['items']):
 if actual_item!=temp_item:
  discrepancies.append({'id':actual_item['id'],'actual':actual_item,'temp':temp_item})
assert temp_pending['count']==0 and temp_pending['requests']==[]
assert not discrepancies,discrepancies
match={'task':'T-0677','state':'CANONICAL_ACTUAL_EXACT_TEMP_MATCH_PENDING_ZERO',
 'canonical_journal_head':head,'operation_sha256':sha(OP),
 'actual_diff_sha256':sha(OUT),'temp_diff_sha256':sha(TEMP_DIFF),
 'actual_pending_sha256':sha(PENDING),'temp_pending_sha256':sha(TEMP_PENDING),
 'full_items_exact':True,'discrepancies_only':[],'actual_pending_count':0,'no_resolution':True}
MATCH.write_text(json.dumps(match,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'actual_diff_sha256':sha(OUT),'pending_sha256':sha(PENDING),
                  'match_sha256':sha(MATCH),'head':head,'pending':0}))
