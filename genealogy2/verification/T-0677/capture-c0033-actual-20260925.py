"""Capture exact canonical C0033 result and compare every full object with isolated temp."""
import hashlib,json,sqlite3
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[2]
OP=H/'c0033-combined-proposed-operation-20260925.json'
TEMP_DIFF=H/'c0033-combined-full-diffcheck-20260925.json'
TEMP_PENDING=H/'c0033-temp-pending-full-20260925.json'
DB=R/'genealogy2/data/research.sqlite'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
op,diff,tp=load(OP),load(TEMP_DIFF),load(TEMP_PENDING)
assert sha(OP)=='a90a78f4ccfc6ffd745a31cf2ea8af2f9ef988c794cee36d2e2a53ffd10fe1fd'
assert diff['operation_sha256']==sha(OP) and tp['operation_sha256']==sha(OP)
con=sqlite3.connect(f'file:{DB}?mode=ro',uri=True);con.row_factory=sqlite3.Row
rows=lambda q,a=():[dict(x) for x in con.execute(q,a)]
def full(rid):
 rev=rows('SELECT * FROM revision WHERE id=?',(rid,));assert len(rev)==1,rid
 rev=rev[0];kind=rows('SELECT kind FROM object WHERE id=?',(rev['object_id'],))[0]['kind']
 data=rows(f'SELECT * FROM {kind} WHERE revision_id=?',(rid,))[0];data.pop('revision_id')
 for k,v in list(data.items()):
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origins=[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in rows('SELECT unit_id,coverage,note FROM origin WHERE revision_id=?',(rid,))]
 evidence=[]
 for r in rows('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=?',(rid,)):
  o,v=r['basis_revision_id'].rsplit('@',1);evidence.append({'object':o,'version':int(v),'role':r['role'],'note':r['note']})
 return {'kind':kind,'revision':rev,'data':data,'origins':origins,'evidence':evidence}
def normalized(x):
 y={**x,'origins':sorted(x['origins'],key=lambda e:(e['unit'],e['coverage'],e['note'])),'evidence':sorted(x['evidence'],key=lambda e:(e['object'],e['version'],e['role'],e['note']))}
 return y
actual=[];issues=[]
for item in diff['items']:
 oid=item['id'];latest=rows('SELECT id FROM revision WHERE object_id=? ORDER BY version DESC LIMIT 1',(oid,))[0]['id']
 new=full(latest)
 if normalized(new)!=normalized(item['after']):issues.append(oid)
 actual.append({'id':oid,'action':item['action'],'before':item['before'],'after':new,'changed_typed_data_fields':item['changed_typed_data_fields'],'origins_preserved':item['origins_preserved']})
assert len(actual)==21 and not issues,issues
newhead=sorted((R/'genealogy2/journal').glob('*.json'))[-1].name
assert newhead.startswith('000000190-'),newhead
pending=rows('SELECT rr.* FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id WHERE rr.operation_id=? AND rs.request_id IS NULL ORDER BY rr.id',(op['id'],))
requests=[{**r,'affected_full':full(r['affected_revision_id']),'changed_full':full(r['changed_revision_id'])} for r in pending]
assert requests==tp['requests']
pending_all=rows('SELECT rr.id FROM review_request rr LEFT JOIN review_resolution rs ON rs.request_id=rr.id WHERE rs.request_id IS NULL')
assert len(pending_all)==0
outdiff=H/'c0033-actual-full-diffcheck-20260925.json'
outdiff.write_text(json.dumps({'task':'T-0677','state':'CANONICAL_ACTUAL_FULL_DIFF','journal':newhead,'operation_sha256':sha(OP),'items':actual,'exact_temp_match':True,'mismatch_ids':[]},ensure_ascii=False,indent=2)+'\n')
outpend=H/'c0033-actual-pending-full-20260925.json'
outpend.write_text(json.dumps({'task':'T-0677','state':'CANONICAL_ACTUAL_PENDING','journal':newhead,'operation_sha256':sha(OP),'count':len(requests),'requests':requests,'exact_temp_match':True},ensure_ascii=False,indent=2)+'\n')
results={n:{'sha256':sha(H/f'c0033-actual-{n}-result-20260925.json'),'result':load(H/f'c0033-actual-{n}-result-20260925.json')} for n in ('apply','verify','verify-assets','verify-source')}
assert results['apply']['result']['changes']==21 and results['apply']['result']['pendingReviews']==0
assert all(results[n]['result']['ok'] for n in ('verify','verify-assets','verify-source'))
summary={'task':'T-0677','state':'CANONICAL_APPLIED_AWAITING_ROOT_INDEPENDENT_CHECK','journal':newhead,'pending':0,'operation_sha256':sha(OP),'actual_full_diff_sha256':sha(outdiff),'actual_pending_full_sha256':sha(outpend),'exact_temp_match':True,'validator_results':results,'no_resolution':True}
out=H/'c0033-actual-apply-summary-20260925.json';out.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'journal':newhead,'pending':0,'diff_sha256':sha(outdiff),'pending_sha256':sha(outpend),'summary_sha256':sha(out)}))
