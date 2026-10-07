"""Read-only final checks + five read-only validators on ALREADY committed425/0 clone.
No apply command, no operation builder, no database mutations or acceptance markers.
Requires explicit root approval to execute this exact helper.
"""
import datetime,hashlib,importlib.util,json,subprocess
from pathlib import Path
B=Path('evaluations/T-0780');S=B/'full10-stage-final143-v1';W=S/'post-resolution-readonly-finalization-v1';assert not W.exists()
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def readpin(p):
 q=Path(p['path']);assert pin(q)==p;return json.loads(q.read_text())
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
primarypin={'path':str(B/'source-review/actual143-resolution2128-native2-representation-source-amendment-v1.json'),'sha256':'55ded83612acf73f58fffd36a5d3643e7f04b054d5c9bf5073b77db15edccff0'}
ownpin={'path':str(B/'fresh-independent-review/actual143-resolution-native-default-policy-independent-disposition-v1.json'),'sha256':'07518f76a42f4f5a0438db2014a781b8a5110536babeeadf9c440750c9856a0d'}
primary=readpin(primarypin);own=readpin(ownpin);assert primary['source_representation_finding_closed'] is True and own['all_submitted_fields_exact'] is own['all2128_actual_resolution_rows_exact_ordered'] is True
opinp={'path':str(B/'implementation/resumed-all2128-one-resolution-draft-v1/001-individual-source-approved-resolution-operation-v1.json'),'sha256':'31479f6a523088a64df8c7ee218ef91416ae726e2724aae3b0e20e1009389aee'}
submitted=readpin(opinp);assert submitted['changes']==[] and len(submitted['resolve'])==2128 and 'dependencyReviewVersion' not in submitted
assert primary['approved_input_operation_pin']==opinp and own['submitted_operation_pin']==opinp
helper=B/'implementation/stage_settled_package_v3.py';assert pin(helper)['sha256']=='7a3d43742f4aa0b697afddd4b3e11e47bdf6c76f82c556106cbc786b7fa7016e';spec=importlib.util.spec_from_file_location('h',helper);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
dbpath=(S/'stage.sqlite').resolve();original=(S/'pre-resolution-stage-original-ae906-v1.sqlite').resolve();assert pin(dbpath)['sha256']=='f834633262e88405afd7fb0bc454202e1476c824d88c40618df4d949d772b7bd' and pin(original)['sha256']=='ae906e23de24bbded3cf392980c9749fe75d8ba6161fec7a92a1fbfdd17fe5ac'
originalpin=pin(S/'pre-resolution-stage-original-ae906-v1.sqlite');stagepin=pin(S/'stage.sqlite');assert h.database_state(dbpath)=={'journal_head':425,'pending':0} and h.database_state(original)=={'journal_head':424,'pending':2128}
pre=h.connection(original);post=h.connection(dbpath);live=h.connection(h.MAIN)
allbefore=h.table_state(pre);allafter=h.table_state(post);livebefore=h.table_state(live);assert len(allbefore)==len(allafter)==50 and set(allbefore)==set(allafter)
changed=[t for t in allbefore if allbefore[t]!=allafter[t]];assert set(changed)=={'operation','operation_payload','review_resolution'}
assert allbefore==json.loads((S/'individual2128-resolution-apply-v1/all50-stage-table-state-before-v1.json').read_text())
assert livebefore==json.loads((S/'baseline-all-table-state.json').read_text()) and h.database_state(h.MAIN)=={'journal_head':281,'pending':0}
protected=h.protection(pre);assert protected==h.protection(post) and len(protected)==42
current_sql='select * from current_revision order by object_id';assert [dict(r) for r in pre.execute(current_sql)]==[dict(r) for r in post.execute(current_sql)]
orders={}
for t in ['dependency','origin','record_asset','record_media']:
 a=[dict(r) for r in pre.execute('select rowid,* from '+t+' order by rowid')];b=[dict(r) for r in post.execute('select rowid,* from '+t+' order by rowid')];assert a==b
 orders[t]={'rows':len(a),'exact_ordered_rowid_data_equal':True,'sha256':hashlib.sha256(h.canon(a).encode()).hexdigest()}
actualop=dict(post.execute('select * from operation_payload where operation_id=?',(submitted['id'],)).fetchone());assert actualop['sequence']==425 and actualop['policy']=='native/2';stored=json.loads(actualop['request_json']);assert type(stored['dependencyReviewVersion']) is int and stored['dependencyReviewVersion']==2
# Explicitly approved sole normalization. Original bytes and failed raw-equality finding remain unchanged.
normalized={**submitted,'dependencyReviewVersion':2};assert stored==normalized and stored['resolve']==submitted['resolve']
assert hashlib.sha256(actualop['request_json'].encode()).hexdigest()==own['actual_stored_request_json_utf8_sha256']
resolutionrows=[dict(r) for r in post.execute('select rowid,* from review_resolution where operation_id=? order by rowid',(submitted['id'],))];assert len(resolutionrows)==2128 and [(r['request_id'],r['rationale']) for r in resolutionrows]==[(r['request'],r['rationale']) for r in submitted['resolve']]
assert post.execute('select count(*) from pending_review').fetchone()[0]==0
applyreceiptp=S/'individual2128-resolution-apply-v1/one-apply.stdout.json';applyreceipt=json.loads(applyreceiptp.read_text());assert applyreceipt['operation']==submitted['id'] and applyreceipt['unchanged'] is False and applyreceipt['changes']==0 and applyreceipt['pendingReviews']==0
pre.close();post.close();W.mkdir()
proof=save('original-snapshot-to-actual425-all50-normalized-request-and-individual-resolution-proof-v1.json',{'original_snapshot_pin':originalpin,'actual_stage_DB_pin':stagepin,'only_changed_tables':changed,'all47_other_full_knowledge_tables_exact':True,'all_current_revision_rows_exact':True,'protected42_exact':True,'ordered_native_metadata':orders,'all50_original_state':allbefore,'all50_actual_state':allafter,'submitted_operation_pin':opinp,'actual_operation_payload':actualop,'approved_only_added_field':{'field':'dependencyReviewVersion','submitted_present':False,'actual_type':'integer','actual_value':2},'explicit_normalized_request_exact':True,'all2128_resolve_array_and_literal_order_exact':True,'all2128_stored_resolution_rowid_order_and_literals_exact':True,'primary_representation_disposition_pin':primarypin,'independent_representation_disposition_pin':ownpin,'raw_file_and_journal_equality_claimed':False})
rowsproof=save('all2128-actual-stored-individual-resolutions-rowid-order-v1.json',resolutionrows)
print(json.dumps({'milestone':'readonly_normalized_all50_order_protection_checks_PASS','actual_state':{'journal_head':425,'pending':0}}),flush=True)
validators=[]
# The only subprocess commands are this fixed whitelist of read-only CLI validators.
commands=[('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source']),('inventory',['inventory']),('pedigree-verified-P0269',['pedigree','P-0269'])]
for name,args in commands:
 print(json.dumps({'milestone':'readonly_validator_started','validator':name}),flush=True)
 cli=['node','genealogy2/cli.mjs',*args,'--db',str(dbpath)]
 if name!='pedigree-verified-P0269':cli+=['--journal',str((S/'journal').resolve())]
 proc=subprocess.run(cli,capture_output=True,text=True);out=W/(name+'.json');out.write_text(proc.stdout);out.with_suffix('.stderr.txt').write_text(proc.stderr);assert proc.returncode==0,(name,proc.stderr);d=json.loads(proc.stdout)
 if name in ['verify','verify-assets','verify-source']:assert d['ok'] is True
 validators.append({'name':name,'result_pin':pin(out),'stderr_pin':pin(out.with_suffix('.stderr.txt')),'exit_code':proc.returncode})
 print(json.dumps({'milestone':'readonly_validator_PASS','validator':name}),flush=True)
assert h.table_state(live)==livebefore;live.close();assert pin(S/'stage.sqlite')==stagepin and pin(S/'pre-resolution-stage-original-ae906-v1.sqlite')==originalpin
assert h.database_state(dbpath)=={'journal_head':425,'pending':0} and h.database_state(h.MAIN)=={'journal_head':281,'pending':0}
result={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_stage_DB_pin':stagepin,'original_immutable_stage_snapshot_pin':originalpin,'actual_stage_state':h.database_state(dbpath),'live_actual_state':h.database_state(h.MAIN),'submitted_operation_pin':opinp,'root_actual_apply_renewal_pin':pin(B/'root-one-sameclone-individual2128-resolution-runtime-authorization-v2.json'),'original_runtime_authorization_pin':pin(B/'root-one-sameclone-individual2128-resolution-runtime-authorization-v1.json'),'actual_one_apply_receipt_pin':pin(applyreceiptp),'actual_before_after_state_receipt_pin':pin(S/'individual2128-resolution-apply-v1/actual-state-before-after-one-apply-v1.json'),'failed_preCLI_path_presentation_proof_pin':pin(S/'individual2128-resolution-apply-initial-pre-CLI-stop-v1/failed-pre-CLI-path-comparison-actual-unchanged-state-proof-v1.json'),'failed_postCLI_raw_journal_equality_proof_pin':pin(S/'individual2128-resolution-apply-v1/failed-post-apply-journal-input-equality-readonly-difference-proof-v1.json'),'primary_representation_disposition_pin':primarypin,'independent_representation_disposition_pin':ownpin,'whole50_current_protected_and_normalized_operation_comparison_pin':proof,'actual2128_stored_resolution_rows_pin':rowsproof,'validators':validators,'actual_CLI_apply_invocations':1,'this_helper_CLI_apply_invocations':0,'this_helper_DB_writes':0,'all50_live_baseline_and_47_stage_knowledge_tables_unchanged':True,'protected42_and_ordered_native_metadata_exact':True,'five_readonly_validators_PASS':True,'original_submitted_input31479_unchanged':True,'canonical_apply_authorized_or_run':False,'acceptance_marker_or_program_credit':False,'actual_model_usage':None,'usage_observability':'Root collects actual new-turn usage after worker final; unknown here'}
p=save('actual425-zero-pending-readonly-final-stage-handoff-index-v1.json',result);print(json.dumps({'milestone':'COMPLETE','handoff_pin':p,'actual_stage_DB_pin':stagepin,'actual_stage_state':result['actual_stage_state'],'live_actual_state':result['live_actual_state']},indent=2),flush=True)
