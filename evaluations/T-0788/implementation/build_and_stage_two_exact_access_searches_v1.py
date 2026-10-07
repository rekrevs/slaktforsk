"""Root-authorized T0788/89 two-note clone stage only. T0787 remains HOLD."""
from pathlib import Path
import json,sqlite3,shutil,traceback,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;S=R/'evaluations/T-0788/two-access-notes-stage-v1';M=R/'genealogy2/data/research.sqlite';EXPECT='fe7369d016ec5150b14d075849caac96d71acfcd42d47357c4fe75afca761792'
s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);assert h.sha(M)==EXPECT
pins=[{'path':'evaluations/T-0788/source-review/one-bounded-access-search-exact-primary-specification-v1.json','sha256':'f1f4ee6185dc7b52c906b32ccbe11e8a42ea2bd786bb5ba72b7177c06385c4c8'},{'path':'evaluations/T-0789/source-review/one-bounded-access-search-exact-primary-specification-v1.json','sha256':'1f1e2c41d4afaf6bfb749a6c61c3675c360d7e7a96022391f040e36aaed31cfc'}]
gatep=R/'evaluations/T-0788/source-review/two-access-only-exact-primary-specification-gate-v1.json';assert h.sha(gatep)=='5df4c98eec0c8faba626eafe87eaa12fbaeeceeca859515034eb45f2590263d2';gate=json.loads(gatep.read_text());assert gate['ready_for_mechanical_draft'] is True and gate['expected_new_searches']==2 and gate['expected_old_revisions']==0
live=h.conn(M);before=h.all50(live);assert h.state(live)=={'journal_head':444,'pending':0}
protectedp=R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json';protected=json.loads(protectedp.read_text())['objects'];assert len(protected)==42
for rid,n in protected.items():assert h.current(live,n['object_id'])==rid and h.native(live,rid)==n
specs=[];ops=[];guards=[];support={}
for i,p in enumerate(pins):
 assert h.sha(R/p['path'])==p['sha256'];spec=json.loads((R/p['path']).read_text());specs.append(spec);x=spec['full_new_API'];assert x['expectedVersion'] is None and x['kind']=='search' and spec['expected_new']==1 and spec['expected_revisions']==0;assert live.execute('select id from object where id=?',(x['id'],)).fetchone() is None
 for e in x['evidence']:
  rid=e['object']+'@'+str(e['version']);assert h.current(live,e['object'])==rid;support[rid]=h.native(live,rid)
 for oid,v in x.get('bindings',{}).items():assert h.current(live,oid)==oid+'@'+str(v)
 op={'id':spec['task']+'/dated-bounded-access-search-note-v1','actor':'Sol; exact settled Astra API under root clone-stage authorization','reason':spec['task']+': preserve only one exact approved dated access observation; every prior knowledge/review retained.','dependencyReviewVersion':2,'changes':[x]};pp=O/('operation-'+str(i+1).zfill(2)+'-'+spec['task']+'-access-search-v1.json');op_pin=h.write(pp,op);ops.append((pp,op,op_pin))
 guards.append({'spec_pin':p,'object_id':x['id'],'expectedVersion':None,'absent':True,'full_new_API_exact':x,'current_retain_disposition':spec['current_disposition'],'no_old_revision_or_grade_change':True})
assert len({op['changes'][0]['id'] for _,op,_ in ops})==2
pkgpin=h.write(O/'two-exact-access-search-ordered-package-v1.json',{'tasks':['T-0788','T-0789'],'source_gate_pin':h.pin(gatep),'operations':[{'operation_id':op['id'],'operation_pin':p} for _,op,p in ops],'new_searches':2,'old_revisions':0,'numeric_dependencyReviewVersion':2,'canonical_authorized':False})
guardpin=h.write(O/'two-exact-access-search-individual-guard-consequence-table-v1.json',{'rows':guards,'full_actual_current_support':support,'protected42_exact':True,'actual_before_state':h.state(live),'actual_main_pin':h.pin(M),'all_other_current_fields_arrays_metadata_retained':True,'source_meaning_and_individual_approval_remain_Astra_owned':True})
# One fresh physical backup, then exactly one immutable-baseline clone; never replace MAIN.
basepath=O/'fresh-baseline-j444.sqlite';assert not basepath.exists();dest=sqlite3.connect(basepath);live.backup(dest);dest.close();base=h.conn(basepath);assert h.all50(base)==before and h.state(base)==h.state(live)
h.write(O/'fresh444-physical-backup-logical-all50-and-protected42-baseline-proof-v1.json',{'main_pin':h.pin(M),'baseline_pin':h.pin(basepath),'actual_state':h.state(live),'all50':before,'all50_main_equals_backup':True,'protected42_exact':True})
assert not S.exists();S.mkdir();db=S/'stage.sqlite';journal=S/'journal';shutil.copyfile(basepath,db);assert h.sha(db)==h.sha(basepath);shutil.copytree(R/'genealogy2/journal',journal)
h.write(S/'root-two-access-stage-authorization-transcript-v1.json',{'sender':'/root','exact_scope':'T0788/89 two settled spec APIs, two new searches, zero old revisions; fresh444→446 clone stage only; T0787 HOLD','source_specs':pins,'source_gate_pin':h.pin(gatep),'canonical_or_Wotan_authorized':False})
c=h.conn(db);steps=[]
try:
 for i,(p,op,pn) in enumerate(ops):
  bef=h.state(c);assert bef=={'journal_head':444+i,'pending':0};assert h.sha(p)==pn['sha256'];assert all(h.sha(R/q['path'])==q['sha256'] for q in pins);assert h.sha(M)==EXPECT;assert c.execute('select id from object where id=?',(op['changes'][0]['id'],)).fetchone() is None
  for e in op['changes'][0]['evidence']:assert h.current(c,e['object'])==e['object']+'@'+str(e['version'])
  for rid,n in protected.items():assert h.native(c,rid)==n
  c.close();h.run_cli(['apply',str(p),'--db',str(db),'--journal',str(journal)],S/('step-'+str(i+1).zfill(2)+'-apply.json'));c=h.conn(db);aft=h.state(c)
  h.write(S/('step-'+str(i+1).zfill(2)+'-actual-before-after-v1.json'),{'operation_pin':pn,'before':bef,'after':aft,'stage_DB_pin':h.pin(db)})
  assert aft=={'journal_head':445+i,'pending':0};stored=dict(c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone());assert json.loads(stored['request_json'])==op
  h.write(S/('step-'+str(i+1).zfill(2)+'-submitted-stored-whole-operation-equality-v1.json'),{'operation_pin':pn,'stored':stored,'whole_request_JSON_equal':True});steps.append({'operation_id':op['id'],'operation_pin':pn,'before':bef,'after':aft})
 final=h.state(c);after=h.all50(c);assert after['schema']==before['schema'];allowed={'operation':2,'operation_payload':2,'object':2,'revision':2,'search':2,'dependency':3};preserved={}
 for name in before['tables']:
  if name in h.DERIVED:continue
  assert after['tables'][name]['rows']==before['tables'][name]['rows']+allowed.get(name,0),name
  sql=base.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
  if 'WITHOUT ROWID' in sql.upper():assert before['tables'][name]==after['tables'][name];preserved[name]={'full_table_equal':True};continue
  limit=base.execute('select max(rowid) from "'+name+'"').fetchone()[0];old=h.rows(base,name,True);got=h.rows(c,name,True,limit) if limit is not None else [];assert old==got,('Old ordered rows changed',name);preserved[name]={'old_rowid_order_and_values_equal':True,'old_order_sha256':h.row_digest(old,True)}
 ids=[op['changes'][0]['id'] for _,op,_ in ops];bsearch=[list(r) for r in base.execute('select object_id,kind,text from object_search order by object_id')];ssearch=[list(r) for r in c.execute('select object_id,kind,text from object_search order by object_id') if r['object_id'] not in ids];assert ssearch==bsearch
 targets={};proofs=[]
 for i,(p,op,pn) in enumerate(ops):
  x=op['changes'][0];rid=x['id']+'@1';n=h.native(c,rid);actual=h.api(n);expected={k:v for k,v in x.items() if k!='bindings'};assert actual==expected,('Exact ordered API mismatch',rid);targets[rid]=n
  txt='\n'.join(str(v) for v in [x['id'],n['disposition'],n['evidence_status'],n['rationale'],n['caveat'],*n['data'].values()] if v is not None);assert [list(r) for r in c.execute('select object_id,kind,text from object_search where object_id=?',(x['id'],))]==[[x['id'],'search',txt]]
  proofs.append({'revision_id':rid,'operation_pin':pn,'source_spec_pin':pins[i],'actual_full_API':actual,'approved_full_API':x,'bindings_are_input_control_not_native_data':True,'ordered_origins_evidence_exact':True})
 for rid,n in protected.items():assert h.current(c,n['object_id'])==rid and h.native(c,rid)==n
 requests=[dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')];assert requests==[] and final=={'journal_head':446,'pending':0}
 api=h.write(S/'two-actual-native-targets-full-API-order-and-current-support-equality-v1.json',{'objects':targets,'source_support_full_native_objects':{rid:h.native(c,rid) for rid in support},'individual_target_proofs':proofs,'no_source_grade':True})
 diff=h.write(S/'all50-old-ordered-rows-fullmetadata-protected42-and-exact-two-search-diff-v1.json',{'before':before,'after':after,'old_rows_preserved':preserved,'exact_new_row_counts':allowed,'derived_current_search_only_two_exact_new_rows':True,'protected42_exact':True,'all_old_current_heads_and_review_state_retained':True})
 req=h.write(S/'actual-individual-requests-v1.json',{'actual_state':final,'requests':requests,'resolutions_applied':0});c.close();validators=[]
 for cmd in ['verify','verify-assets','verify-source','inventory']:
  out=S/(cmd+'.json');h.run_cli([cmd,'--db',str(db),'--journal',str(journal)],out);validators.append(h.pin(out))
 for person in ['P-0269','P-0270']:
  out=S/(person+'-default-verified-pedigree.json');v=h.run_cli(['pedigree',person,'--db',str(db)],out);reference=R/('evaluations/T-0786/one-search-stage-v1/'+person+'-verified-pedigree.json');assert v==json.loads(reference.read_text());validators.append(h.pin(out))
 assert h.sha(M)==EXPECT and h.all50(live)==before and h.state(live)=={'journal_head':444,'pending':0};assert all(h.sha(R/p['path'])==p['sha256'] for p in pins);assert all(h.sha(p)==pn['sha256'] for p,_,pn in ops);c=h.conn(db);assert h.state(c)==final;c.close()
 commands=[['node','genealogy2/cli.mjs','apply',str(p.relative_to(R)),'--db','genealogy2/data/research.sqlite','--journal','genealogy2/journal'] for p,_,_ in ops]
 hand=h.write(S/'complete-two-access-search-stage-result-and-Astra-handoff-v1.json',{'tasks':['T-0788','T-0789'],'ordered_package_pin':pkgpin,'individual_guard_consequence_pin':guardpin,'operation_pins':[pn for _,_,pn in ops],'source_spec_pins':pins,'source_gate_pin':h.pin(gatep),'actual_state':final,'actual_sequential_steps':steps,'actual_native_target_API_pin':api,'full_all50_diff_pin':diff,'actual_individual_request_pin':req,'stage_DB_pin':h.pin(db),'fresh_baseline_pin':h.pin(basepath),'validators':validators,'live_main_pin':h.pin(M),'live_all50_unchanged':True,'protected42_exact':True,'old_revisions':0,'new_searches':2,'executable_root_controlled_apply_commands_REQUIRE_SEPARATE_AUTH':commands,'canonical_or_Wotan_applied':False,'T0787_HOLD_no_operations':True,'usage':'UNKNOWN pending root collector'});print(json.dumps({'handoff_pin':hand,'package_pin':pkgpin,'operation_pins':[pn for _,_,pn in ops],'actual_state':final}))
except BaseException as e:
 try:c=h.conn(db);st=h.state(c);c.close()
 except BaseException:st=None
 h.write(S/'STOP-preserved-failure-and-actual-state-v1.json',{'error':repr(e),'traceback':traceback.format_exc(),'actual_state':st,'stage_DB_pin':h.pin(db),'main_pin':h.pin(M),'no_retry':True});raise
finally:base.close();live.close()
