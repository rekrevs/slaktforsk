"""ONE root-authorized exact sameclone resolution CLI apply. Never main apply.
Preserves original bytes and each actual receipt; stops on mismatch, no retries.
"""
import datetime,hashlib,importlib.util,json,shutil,sqlite3,subprocess
from pathlib import Path
B=Path('evaluations/T-0780');S=B/'full10-stage-final143-v1';W=S/'individual2128-resolution-apply-v1';assert not W.exists()
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def load(p):return json.loads(Path(p).read_text())
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
authp=B/'root-one-sameclone-individual2128-resolution-runtime-authorization-v1.json';a=load(authp);assert a['authorization']=='ONE_EXACT_SAMECLONE_RESOLUTION_CLI_APPLY_ONLY' and a['canonical_apply_authorized'] is False
for k in ['pre_stage_DB_pin','operation_pin','independent_exact_constructed_bytes_review_pin']:
 p=Path(a[k]['path']);assert pin(p)==a[k],k
op=Path(a['operation_pin']['path']);payload=load(op);assert payload['changes']==[] and len(payload['resolve'])==len({x['request'] for x in payload['resolve']})==a['expected_resolutions']==2128
helper=B/'implementation/stage_settled_package_v3.py';assert pin(helper)['sha256']=='7a3d43742f4aa0b697afddd4b3e11e47bdf6c76f82c556106cbc786b7fa7016e'
spec=importlib.util.spec_from_file_location('immutable_stage_helper',helper);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
dbp=Path(a['pre_stage_DB_pin']['path']).resolve();main=h.MAIN;assert dbp!=main and dbp== (S/'stage.sqlite').resolve();journal=Path(a['journal_path']).resolve();assert journal==(S/'journal').resolve()
before=h.database_state(dbp);assert before==a['expected_before']=={'journal_head':424,'pending':2128};assert h.database_state(main)==a['live_baseline_state']=={'journal_head':281,'pending':0}
live=h.connection(main);live_before=h.table_state(live);assert live_before==load(S/'baseline-all-table-state.json')
pre=h.connection(dbp);allbefore=h.table_state(pre);protected=h.protection(pre);assert protected==load(S/'protected-before.json') and len(protected)==42
ordered_tables=['dependency','origin','record_asset','record_media']
def ordered_hashes(db):
 out={}
 for t in ordered_tables:
  rows=[dict(r) for r in db.execute('select rowid,* from '+t+' order by rowid')]
  out[t]={'rows':len(rows),'sha256':hashlib.sha256(h.canon(rows).encode()).hexdigest()}
 return out
ordersbefore=ordered_hashes(pre);currentbefore=[dict(r) for r in pre.execute('select * from current_revision order by object_id')]
pending={r['id']:dict(r) for r in pre.execute('select * from pending_review')};assert set(pending)=={x['request'] for x in payload['resolve']};pre.close()
snapshot=Path(a['preserve_original_byte_snapshot_path']);assert not snapshot.exists();shutil.copyfile(dbp,snapshot);assert pin(snapshot)['sha256']==a['pre_stage_DB_pin']['sha256'];assert pin(dbp)==a['pre_stage_DB_pin']
W.mkdir();save('authorization-and-original-byte-snapshot-proof-v1.json',{'authorization_pin':pin(authp),'snapshot_pin':pin(snapshot),'actual_original_stage_DB_pin':pin(dbp),'original_byte_equality':True,'actual_before':before});save('all50-stage-table-state-before-v1.json',allbefore);save('ordered-evidence-origins-assets-media-rowid-before-v1.json',ordersbefore);save('protected42-before-v1.json',protected);save('live-all50-table-state-before-v1.json',live_before)
state={'operation_pin':pin(op),'before':before,'actual_state_read_from_DB':True,'CLI_invocations':0};save('actual-state-before-one-apply-v1.json',state)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
 state['CLI_invocations']=1
 args=['node','genealogy2/cli.mjs','apply',str(op),'--db',str(dbp),'--journal',str(journal)]
 proc=subprocess.run(args,capture_output=True,text=True)
 (W/'one-apply.stdout.json').write_text(proc.stdout);(W/'one-apply.stderr.txt').write_text(proc.stderr);state['exit_code']=proc.returncode
 assert proc.returncode==0,('one authorized CLI apply failed',proc.stderr)
 receipt=json.loads(proc.stdout);assert receipt['unchanged'] is False and receipt['operation']==payload['id'] and receipt['changes']==0
finally:
 state['after']=h.database_state(dbp);state['actual_stage_DB_pin_after']=pin(dbp);save('actual-state-before-after-one-apply-v1.json',state)
assert state['after']['pending']==a['expected_pending_after']==0
post=h.connection(dbp);allafter=h.table_state(post);assert set(allafter)==set(allbefore) and len(allbefore)==50
allowed={'operation','operation_payload','review_resolution'};actualchanged={t for t in allbefore if allbefore[t]!=allafter[t]};assert actualchanged==allowed,actualchanged
ordersafter=ordered_hashes(post);assert ordersafter==ordersbefore
assert h.protection(post)==protected
currentafter=[dict(r) for r in post.execute('select * from current_revision order by object_id')];assert currentafter==currentbefore
newres=[dict(r) for r in post.execute('select * from review_resolution where operation_id=? order by rowid',(payload['id'],))];assert len(newres)==2128
assert [(r['request_id'],r['rationale']) for r in newres]==[(r['request'],r['rationale']) for r in payload['resolve']]
actualop=dict(post.execute('select * from operation_payload where operation_id=?',(payload['id'],)).fetchone());assert json.loads(actualop['request_json'])==payload
assert post.execute('select count(*) from pending_review').fetchone()[0]==0;post.close()
save('all50-stage-table-state-after-v1.json',allafter);save('all50-only-three-authorized-review-journal-tables-changed-proof-v1.json',{'table_count':50,'allowed_changed_tables':list(sorted(allowed)),'actual_changed_tables':list(sorted(actualchanged)),'all47_other_full_tables_exact':True,'all_current_full_revision_records_exact':True,'protected42_exact':True,'ordered_rowid_evidence_origins_assets_media_exact':True,'actual2128_stored_resolution_rationale_rowid_order_equals_approved_literal_API':True,'actual_operation_payload':actualop,'before_pin':pin(W/'all50-stage-table-state-before-v1.json'),'after_pin':pin(W/'all50-stage-table-state-after-v1.json')});save('ordered-evidence-origins-assets-media-rowid-after-v1.json',ordersafter);save('protected42-after-v1.json',protected);save('actual2128-stored-individual-resolution-rows-v1.json',newres)
print(json.dumps({'milestone':'exact_sameclone_resolution_applied_once','actual_state':state['after'],'changed_tables':sorted(actualchanged),'knowledge_and_ordered_metadata_unchanged':True}),flush=True)
validatorpins=[]
for command,args in [('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source']),('inventory',['inventory']),('pedigree-verified-P0269',['pedigree','P-0269'])]:
 print(json.dumps({'milestone':'validator_started','validator':command}),flush=True)
 cli=['node','genealogy2/cli.mjs',*args,'--db',str(dbp)]
 if command!='pedigree-verified-P0269':cli+=['--journal',str(journal)]
 proc=subprocess.run(cli,capture_output=True,text=True);out=W/(command+'.json');out.write_text(proc.stdout);out.with_suffix('.stderr.txt').write_text(proc.stderr);assert proc.returncode==0,(command,proc.stderr);d=json.loads(proc.stdout)
 if command in ['verify','verify-assets','verify-source']:assert d['ok'] is True,(command,d)
 validatorpins.append(pin(out));print(json.dumps({'milestone':'validator_pass','validator':command}),flush=True)
assert h.table_state(live)==live_before;live.close();save('live-all50-table-state-after-v1.json',live_before);assert h.database_state(main)==a['live_baseline_state'];assert h.database_state(dbp)==state['after'];assert pin(snapshot)['sha256']==a['pre_stage_DB_pin']['sha256']
result={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'started_at_utc':started,'authorization_pin':pin(authp),'original_immutable_stage_snapshot_pin':pin(snapshot),'actual_stage_DB_pin':pin(dbp),'operation_pin':pin(op),'actual_before_after_receipt_pin':pin(W/'actual-state-before-after-one-apply-v1.json'),'actual_state':state['after'],'actual_apply_receipt_pin':pin(W/'one-apply.stdout.json'),'actual_one_CLI_apply_count':1,'stored_resolutions':2128,'native_changes':0,'all50_table_comparison_pin':pin(W/'all50-only-three-authorized-review-journal-tables-changed-proof-v1.json'),'validator_pins':validatorpins,'protected42_and_ordered_all_knowledge_metadata_unchanged':True,'all50_live_baseline_unchanged':True,'live_actual_state':a['live_baseline_state'],'canonical_apply_or_program_acceptance':False,'actual_model_usage':None,'usage_observability':'Root collects actual new-turn usage after worker final; unavailable here'}
p=save('one-sameclone-2128-resolution-actual-complete-handoff-index-v1.json',result);print(json.dumps({'milestone':'COMPLETE','result_pin':p,'actual_stage_DB_pin':result['actual_stage_DB_pin'],'actual_state':state['after']},indent=2),flush=True)
