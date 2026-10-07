"""Mechanical complete manifest from both final exact-ID gates. Does NOT invoke builder."""
import datetime,hashlib,json,sqlite3
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/resumed-all2128-complete-approval-manifest-v1'
assert not W.exists()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
cache={};pins={}
def loadpin(x):
 k=x['path'];h=x['sha256'];assert k not in pins or pins[k]==h
 if k not in cache:
  p=Path(k);assert sha(p)==h,(k,h);cache[k]=json.loads(p.read_text());pins[k]=h
 return cache[k]
def ptr(x,p):
 for v in p.split('/')[1:]:
  v=v.replace('~1','/').replace('~0','~');x=x[int(v)] if isinstance(x,list) else x[v]
 return x
pp={'path':str(B/'source-review/actual143-all2128-complete-primary-source-resolution-gate-v2.json'),'sha256':'54005a67bff3f7c3c92137fe8d7fdf2132b1094d4d1c94dbf9f031665ed3d5f2'}
ip={'path':str(B/'fresh-independent-review/actual143-all2128-complete-independent-pre-resolution-gate-v1.json'),'sha256':'aab1081e4a1ca61281eb97c5c31e2f02ca6b3ec2c49b5756d741c5e63d3930a6'}
p=loadpin(pp);i=loadpin(ip);assert p['primary_all2128_ready'] is i['independent_all2128_ready'] is True
assert i['primary_complete_resolution_gate_pin']==pp
assert p['stage_DB_pin']==i['stage_DB_pin'];assert p['expected_actual_stage_state']==i['expected_actual_stage_state']=={'journal_head':424,'pending':2128}
assert p['actual_request_index_pin']==i['actual_request_index_pin'];requestindex=loadpin(p['actual_request_index_pin']);requests={x['actual_request']['id']:x for x in requestindex['requests']};assert len(requests)==2128
pg={x['request_id']:x for x in p['individual_approvals']};ig={x['request_id']:x for x in i['individual_approvals']};assert len(pg)==len(p['individual_approvals'])==len(ig)==len(i['individual_approvals'])==2128
assert set(pg)==set(ig)==set(requests)==set(p['approved_actual_request_ids'])==set(i['approved_actual_request_ids'])
expectedcounts=[16,49,142,220,330,28,222,1121];assert [x['count'] for x in p['modules']]==expectedcounts
primarykeys=['primary_decision_pin','primary_row_pointer','primary_resolution_instruction_pointer','primary_current_revision_pointer','primary_individual_scope_pointer'];ordered=[];moduleproof=[]
for module in p['modules']:
 d=loadpin(module);rows=d['rows'];assert len(rows)==module['count'];moduleIDs=[]
 for n,pr in enumerate(rows):
  rid=pr['actual_request']['id'];a=ig[rid];pa=pg[rid];assert all(a[k]==pa[k] for k in primarykeys),rid
  assert a['primary_decision_pin']['path']==module['path'] and a['primary_decision_pin']['sha256']==module['sha256'] and a['primary_row_pointer']=='/rows/'+str(n)
  ir=ptr(loadpin(a['independent_decision_pin']),a['independent_row_pointer']);q=requests[rid]
  assert pr['actual_request']==ir['actual_request']==q['actual_request']
  instruction=ptr(pr,a['primary_resolution_instruction_pointer']);assert instruction==ptr(ir,a['independent_approved_resolution_instruction_pointer'])
  assert set(instruction)=={'request','rationale'} and instruction['request']==rid and instruction['rationale'].strip()
  assert ptr(pr,a['primary_current_revision_pointer'])==ptr(ir,a['independent_current_revision_pointer'])==q['affected_latest_current_revision_id']
  assert ptr(pr,a['primary_individual_scope_pointer']) and ptr(ir,a['independent_individual_scope_pointer'])
  ordered.append(a);moduleIDs.append(rid)
 moduleproof.append({'module_pin':module,'manifest_range_start_zero_based':len(ordered)-len(rows),'manifest_range_end_exclusive':len(ordered),'ordered_request_IDs':moduleIDs})
assert len({x['request_id'] for x in ordered})==2128
stage=Path(p['stage_DB_pin']['path']);assert sha(stage)==p['stage_DB_pin']['sha256'];c=sqlite3.connect(stage.resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
state={'journal_head':c.execute('select max(sequence) from operation_payload').fetchone()[0],'pending':c.execute('select count(*) from pending_review').fetchone()[0]};assert state==p['expected_actual_stage_state']
pending={r['id']:dict(r) for r in c.execute('select * from pending_review')};assert set(pending)==set(requests) and all(pending[rid]==requests[rid]['actual_request'] for rid in requests)
c.close();assert sha(stage)==p['stage_DB_pin']['sha256']
for path,h in pins.items():assert sha(path)==h
manifest={'task':'T-0780','status':'COMPLETE_APPROVED_ALL2128_INDIVIDUAL_RESOLUTIONS','no_canonical_apply_authorized':True,'actual_request_index_pin':p['actual_request_index_pin'],'stage_DB_pin':p['stage_DB_pin'],'expected_actual_stage_state':state,'primary_complete_resolution_gate_pin':pp,'independent_complete_resolution_gate_pin':ip,'primary_gate_ready_pointer':'/primary_all2128_ready','independent_gate_ready_pointer':'/independent_all2128_ready','primary_gate_stage_pin_pointer':'/stage_DB_pin','independent_gate_stage_pin_pointer':'/stage_DB_pin','primary_gate_approved_IDs_pointer':'/approved_actual_request_ids','independent_gate_approved_IDs_pointer':'/approved_actual_request_ids','operation_id_prefix':'T-0780/actual143-all2128-individually-approved-resolutions-v1','operation_actor':'codex','operation_reason':'T-0780 AC3: explicit individually adjudicated actual2128 dependency resolutions; exact primary complete gate '+pp['sha256']+' and independent complete gate '+ip['sha256']+'. Each approved request/rationale retained verbatim; no native revision, rebind, review-level upgrade or source inference.','max_resolutions_per_operation':2128,'individual_approvals':ordered,'explicit_order':'Primary approved module order16/49/142/220/330/28/222/1121, within each literal source row order.','builder_execution_authorized':False,'runtime_apply_authorized':False}
W.mkdir();mp=W/'exact-all2128-dual-approved-individual-resolution-builder-manifest-v1.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
proof={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_pin':pin(mp),'primary_complete_gate_pin':pp,'independent_complete_gate_pin':ip,'stage_DB_pin':p['stage_DB_pin'],'actual_readonly_stage_state':state,'module_order_and_each_exact_request_ID':moduleproof,'all2128_primary_and_independent_literal_instructions_exact':True,'all2128_actual_pending_IDs_requests_and_current_revisions_bound':True,'all_unique_input_pins_rechecked':len(pins),'coverage':{'requests':2128,'missing':0,'unexpected':0,'duplicate':0,'intended_resolution_only_operations':1,'native_changes':0},'builder_UNRUN':True,'runtime_apply_UNRUN':True,'program_acceptance':False,'source_grading_inferred':False}
fp=W/'exact-all2128-dual-approved-manifest-preparation-proof-v1.json';fp.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'manifest_pin':pin(mp),'proof_pin':pin(fp),'exact_approved_IDs':2128,'builder_run':False,'runtime_mutations':0},indent=2))
