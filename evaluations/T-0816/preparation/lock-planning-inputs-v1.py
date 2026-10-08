from pathlib import Path
import json,hashlib,sqlite3,time,datetime,importlib.util
R=Path.cwd();D=R/'evaluations/T-0816';P=D/'preparation';start=time.monotonic()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.load(open(p))
def save(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
main=R/'genealogy2/data/research.sqlite';assert sha(main)=='f73c9599c70b2938b581593c1250995122d79bfa4451e72be1e040cc6c339d0e'
sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(main);assert h.state(c)=={'journal_head':484,'pending':0}
back=R/'wotan/backlog.json';q=P/'baseline-backlog-v1.json';q.write_bytes(back.read_bytes());b=load(q);assert b['next_id']==818
transfer=R/'evaluations/T-0813/settled-fixed160-successor-transfer-v1.json';assert sha(transfer)=='5d56b741b0761dc443ea86f39ea439acc0bc1a5f2c643e207a6cb7a14d40ca1c';tr=load(transfer);assert len(tr['fixed160'])==160;appendix=tr['full_T0791_T0792_planning_appendices'];assert len(appendix)==4898;assert hashlib.sha256(appendix.encode()).hexdigest()==tr['appendices_sha256'];(P/'exact-T0791-T0792-planning-appendices-v1.md').write_text(appendix)
oldfront=load(R/'evaluations/T-0813/preparation/compact-current30-axes-and-path-index-v1.json');inv=load(R/'evaluations/T-0815/root-actual-inventory-full-v2.json');am={x['id']:x for x in inv['people']};front=[];delta=[];bundle=[]
for x in oldfront['persons']:
 pid=x.get('person_id',x.get('person'));assert pid in am;oldfile=R/f'evaluations/T-0813/preparation/native/{pid}.json';v=load(oldfile);changes=[]
 for o in v['current']:
  rid=h.current(c,o['object_id'])
  if rid!=o['id']:
   changes.append({'object_id':o['object_id'],'old_revision':o['id'],'current_revision':rid});delta.append(h.native(c,rid))
 front.append({'person':pid,'prior_routing_metadata':x,'current_inventory_full_row':am[pid],'reused_fullperson':f'evaluations/T-0813/preparation/current-full/{pid}.json','reused_fullnative':str(oldfile.relative_to(R)),'current_head_deltas':changes,'qualification':'Prior source interpretations reused; routing metadata does not certify new sources. Apply exact current native delta when reading prior bundle.'});bundle.extend([oldfile,R/f'evaluations/T-0813/preparation/current-full/{pid}.json'])
assert len(front)==30;save('current30-planning-input-index-v1.json',{'persons':front,'count':30,'inventory_total':len(am),'no130_source_audit':True});save('current30-exact-native-delta-v1.json',{'revisions':list({x['id']:x for x in delta}.values()),'no_new_review_or_source_interpretation':True})
ownerfile=R/'evaluations/T-0813/preparation/all-current-OWNER-scope-v1.json';owner=load(ownerfile)
for o in owner['OWNER_full_native']:assert h.current(c,o['object_id'])==o['id']
assert len(owner['OWNER_full_native'])==45
save('OWNER45-reuse-proof-v1.json',{'current45_heads_exact':True,'complete_scope_packet':str(ownerfile.relative_to(R)),'exact25bases_and6PCDsections_in_packet':True,'additional_owner_PCD002':'evaluations/T-0814/preparation/PCD-2026-10-08-002-snapshot.md','scope_requires_Astra_judgment':True})
# Accepted484 history reuse, no replay: actual canonical result proves exact reviewed484 and prior483 chain.
resultfile=R/'evaluations/T-0815/root-actual-final-verification-v1.json';rr=load(resultfile);assert rr['main_sha256']==sha(main)
save('accepted484-history-reuse-v1.json',{'state':h.state(c),'actual_main_sha256':sha(main),'accepted484_result':str(resultfile.relative_to(R)),'all50_comparison':'evaluations/T-0815/actual-main-stage-comparison-v1.json','prefix483_reconciliation':'evaluations/T-0815/preparation/actual-accepted-reconciliation-v1.json','new484_receipt':str(next((R/'genealogy2/journal').glob('000000484-*')).relative_to(R)),'no_replay_or_prior_reinterpretation':True})
logs=['T-0816','T-0817','T-0255','T-0237','T-0410','T-0307','T-0217','T-0228']
for tid in logs:
 p=R/f'wotan/dev-log/{tid}.md';q=P/'exact-task-snapshots'/p.name;q.parent.mkdir(exist_ok=True);q.write_bytes(p.read_bytes())
for name in ['AGENTS.md','NORTH-STAR.md','PROJECT-CONTROL.md','wotan/README.md','docs/research/person-contract.md','genealogy2/docs/working.md']:
 p=R/name;q=P/'normative-snapshots'/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
reuse=[transfer,ownerfile,resultfile,R/'evaluations/T-0813/preparation/fixed160-union-rest-proof-v1.json',R/'evaluations/T-0813/preparation/existing-core-life-owner-index-v2.json',R/'evaluations/T-0813/preparation/current-frontier-parent-edge-ledger-v1.json',R/'evaluations/T-0813/settled-source-design-v1.json',R/'evaluations/T-0814/preparation/PCD-2026-10-08-002-snapshot.md',R/'evaluations/T-0814/root-actual-final-verification-v1.json',R/'evaluations/T-0815/actual-main-stage-comparison-v1.json',R/'evaluations/T-0815/preparation/actual-accepted-reconciliation-v1.json',R/'evaluations/T-0815/root-actual-inventory-full-v2.json',R/'evaluations/T-0815/root-actual-pedigree-P0269-v1.json',R/'evaluations/T-0815/root-actual-pedigree-P0270-v1.json',D/'root-start-baseline-v1.json',next((R/'genealogy2/journal').glob('000000484-*'))]+bundle
reuse.extend((R/'evaluations/T-0813/preparation/existing-core-life-logs').glob('*.md'))
for task in ['T-0814','T-0815']:
 reuse.extend((R/f'evaluations/{task}').glob('*final-source-gate-v1.json'))
 reuse.append(R/f'evaluations/{task}/implementation/final-qualified-result-v1.json') if (R/f'evaluations/{task}/implementation/final-qualified-result-v1.json').exists()else None
 reuse.append(R/f'evaluations/{task}/primary-complete-source-'+('spec-v2.json'if task=='T-0814'else'design-v3.json'))
# Full factual current focal read outputs are accepted, already reviewed; no new CLI or original read.
for task,stage,people in [('T-0814','stage483-v1',['P-0336','P-0337']),('T-0815','stage484-v1',['P-0042','P-0043'])]:
 for pid in people:reuse.append(R/f'evaluations/{task}/implementation/{stage}/{pid}-person.json')
assert sha(main)=='f73c9599c70b2938b581593c1250995122d79bfa4451e72be1e040cc6c339d0e'
save('preparation-result-v1.json',{'passed':True,'state':h.state(c),'MAIN_unchanged':True,'fixed160_rows':160,'appendix_characters':4898,'current30':30,'current30_changed_native_heads':len({x['id']for x in delta}),'OWNER45_heads_exact':True,'originals_opened':0,'native_or_queue_writes':0,'elapsed_seconds':time.monotonic()-start,'planning_decisions_by_Sol':0})
files=set(p.resolve()for p in P.rglob('*')if p.is_file());files.update(p.resolve()for p in reuse)
pins=[{'path':str(p.relative_to(R)),'sha256':sha(p)}for p in sorted(files)]
save('locked-input-manifest-v1.json',{'task':'T-0816','state':h.state(c),'main_sha256':sha(main),'original_ceiling':0,'planning_only':True,'pins':pins,'readable_index':'evaluations/T-0816/preparation/current30-planning-input-index-v1.json','fixed160_transfer':str(transfer.relative_to(R)),'full_appendices':'evaluations/T-0816/preparation/exact-T0791-T0792-planning-appendices-v1.md','current_backlog':'evaluations/T-0816/preparation/baseline-backlog-v1.json','full_old_task_scopes':'evaluations/T-0816/preparation/exact-task-snapshots/','qualification':'Inputs only; no strategy, successor allocation, original promotion, native judgment or queue edits.130outerrows not newly source-assessed.'});print('manifest',sha(P/'locked-input-manifest-v1.json'),'pins',len(pins),'changedheads',len({x['id']for x in delta}))
