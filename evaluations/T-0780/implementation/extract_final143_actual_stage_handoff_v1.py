"""Read-only actual completed stage request/current/support extraction, never dispositions."""
import datetime,hashlib,json,sqlite3
from pathlib import Path
B=Path('evaluations/T-0780');S=B/'full10-stage-final143-v1';W=S/'actual-handoff-v1'
def load(p):return json.loads(Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def save(name,x):
 p=W/name;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
assert (S/'stage-result.json').exists(),'No incomplete/failed stage may be labelled complete'
assert not W.exists();W.mkdir()
c=sqlite3.connect((S/'stage.sqlite').resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
def state():return {'journal_head':c.execute('select max(sequence) from operation_payload').fetchone()[0],'pending':c.execute('select count(*) from review_request r left join review_resolution s on r.id=s.request_id where s.request_id is null').fetchone()[0]}
objects={}
def native(rid):
 if rid in objects:return rid
 row=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone();assert row is not None,rid;n=dict(row)
 n['data']=dict(c.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone())
 n['origins']=[dict(x) for x in c.execute('select * from origin where revision_id=?',(rid,))]
 n['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=?',(rid,))]
 if n['kind']=='record':
  n['assets']=[dict(x) for x in c.execute('select * from record_asset where revision_id=?',(rid,))]
  n['media']=[dict(x) for x in c.execute('select * from record_media where revision_id=?',(rid,))]
 objects[rid]=n;return rid
def current(oid):
 x=c.execute('select id from revision where object_id=? order by version desc limit 1',(oid,)).fetchone();assert x is not None,oid;return native(x[0])
pending=[dict(x) for x in c.execute('select r.* from review_request r left join review_resolution s on r.id=s.request_id where s.request_id is null order by r.id')]
assert pending==sorted(load(S/'pending-after.json'),key=lambda x:x['id'])
requests=[]
for request in pending:
 a=native(request['affected_revision_id']);ch=native(request['changed_revision_id']);ac=current(objects[a]['object_id']);cc=current(objects[ch]['object_id'])
 previous=objects[ch]['previous_id'];previous=native(previous) if previous else None
 bases=[native(x['basis_revision_id']) for x in objects[ac]['evidence']]
 requests.append({'actual_request':request,'affected_exact_revision_pointer':'/objects/'+a.replace('~','~0').replace('/','~1'),'affected_latest_current_revision_id':ac,'changed_exact_revision_id':ch,'changed_previous_revision_id':previous,'changed_latest_current_revision_id':cc,'ordered_affected_current_support_revision_ids':bases,'source_individual_grading':'PENDING','automatic_rebind_or_resolution':False})
nativepin=save('full-actual-request-current-and-direct-support-native-payloads-v1.json',{'task':'T-0780','state':state(),'objects':objects,'deduplication':'Immutable exact revision ID only; no semantic merging. Native text and array order preserved.'})
requestpin=save('all-actual-pending-individual-request-routing-v1.json',{'task':'T-0780','state':state(),'native_payload_pin':nativepin,'requests':requests,'all_actual_pending_count':len(pending),'no_grades_or_resolutions':True})
steps=[]
for i in range(1,144):
 p=S/f'step-{i:03}-database-state-before-after.json';d=load(p)
 assert d['step']==i and d['after']['journal_head']==d['before']['journal_head']+1
 if steps:assert steps[-1]['actual_state']['after']==d['before']
 steps.append({'actual_state':d,'state_receipt_pin':pin(p),'apply_receipt_pin':pin(S/f'step-{i:03}-apply.json')})
assert steps[0]['actual_state']['before']=={'journal_head':281,'pending':0};assert steps[-1]['actual_state']['after']==state()
steppin=save('all143-exact-operation-and-actual-before-after-state-index-v1.json',{'task':'T-0780','steps':steps,'state':state(),'no_diagnostic_inferred_counts':True})
validatorpins=[pin(S/(x+'.json')) for x in ['verify','verify-assets','verify-source','inventory','pedigree-verified-P0269']]
assert load(S/'protected-before.json')==load(S/'protected-after.json')
result=save('complete-authorized-stage-handoff-index-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage_result_pin':pin(S/'stage-result.json'),'authorization_pin':pin(B/'root-fresh143-stage-authorization-v1.json'),'stage_gate_pin':pin(S/'package-gate.json'),'state':state(),'request_index_pin':requestpin,'full_native_payload_index_pin':nativepin,'all143_step_index_pin':steppin,'validator_pins':validatorpins,'protected_before_pin':pin(S/'protected-before.json'),'protected_after_pin':pin(S/'protected-after.json'),'protected_equal':True,'canonical_untouched':load(S/'stage-result.json')['canonical_untouched'],'canonical_apply_or_resolutions':False,'source_and_independent_actual_request_review_required':True,'actual_model_usage':'Unobservable here; root collects after worker final.'})
c.close();print(json.dumps({'handoff':result,'request_index':requestpin,'native_payloads':nativepin,'step_index':steppin,'actual_pending_count':len(pending),'native_revision_payloads':len(objects)},indent=2))
