"""Root-authorized one-search clone stage only. No canonical or Wotan mutation."""
from pathlib import Path
import importlib.util,json,hashlib,shutil,traceback
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;S=R/'evaluations/T-0786/one-search-stage-v1';M=R/'genealogy2/data/research.sqlite'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
helper=R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py'
hp=sha(helper);sp=importlib.util.spec_from_file_location('proven',helper);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
specp=R/'evaluations/T-0786/source-review/one-shared-access-search-exact-primary-specification-v2.json';assert sha(specp)=='7e8b6bbec375e18f7ac0db7c2a54891039fcc80ee6edafbb0dc1254d1c3481a9';spec=json.loads(specp.read_text());x=spec['full_new_API']
proofp=R/'evaluations/T-0786/preparation/fresh443-physical-baseline-logical-all50-and-live-unchanged-v1.json';assert sha(proofp)=='57fc1ceec6ebf001fda830ca1f3fa0ac33c41f0c0713ac478b7ac59e2e793a3d';proof=json.loads(proofp.read_text());basepath=R/proof['baseline_pin']['path'];assert sha(basepath)==proof['baseline_pin']['sha256'];assert sha(M)==proof['MAIN_pin']['sha256']
live=h.conn(M);base=h.conn(basepath);before=h.all50(base);assert h.all50(live)==before and h.state(live)==h.state(base)=={'journal_head':443,'pending':0}
assert x['id']=='SEARCH-T0786-Sodertalje-uppslag15-access' and x['kind']=='search' and x['expectedVersion'] is None
assert base.execute('select id from object where id=?',(x['id'],)).fetchone() is None
assert len(x['evidence'])==2 and x['bindings']=={'S-0689':1}
supports={}
for e in x['evidence']:
 rid=e['object']+'@'+str(e['version']);assert h.current(base,e['object'])==rid;assert h.native(base,rid)==h.native(live,rid);supports[rid]=h.native(base,rid)
protectedp=R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json';protected=json.loads(protectedp.read_text())['objects'];assert len(protected)==42
for rid,n in protected.items():assert h.current(base,n['object_id'])==rid and h.native(base,rid)==n
op={'id':'T-0786/shared-Sodertalje-uppslag15-access-note-v1','actor':'Sol; exact settled primary source decision under root stage authorization','reason':'T-0786: preserve one explicitly settled dated shared access observation; all existing knowledge and reviews retained.','dependencyReviewVersion':2,'changes':[x]}
opp=O/'one-shared-access-search-operation-v1.json';op_pin=h.write(opp,op)
proposal=h.write(O/'one-shared-access-search-package-v1.json',{'task':'T-0786','operations':[{'operation_id':op['id'],'operation_pin':op_pin}],'source_spec_pin':h.pin(specp),'targets':[x['id']],'native_revisions':0,'new_objects':1,'all_current_objects_retained':True,'canonical_authorized':False})
guard=h.write(O/'one-shared-access-search-guards-and-individual-consequence-v1.json',{'source_spec_pin':h.pin(specp),'full_old':None,'full_new_API':x,'old_id_absent':True,'source_support_current_heads_exact':supports,'all_old_objects_retained':spec['current_retain_disposition'],'protected42_exact':True,'helper_pin':h.pin(helper),'no_automatic_source_grade':True})
assert not S.exists();S.mkdir();db=S/'stage.sqlite';journal=S/'journal';shutil.copyfile(basepath,db);assert sha(db)==proof['baseline_pin']['sha256'];shutil.copytree(R/'genealogy2/journal',journal)
h.write(S/'root-stage-authorization-transcript-v1.json',{'sender':'/root','scope':'Build minimal one-search stage from primary exact v2 spec7e8b6b; no canonical/Wotanapply; all existing fields retained; exact packagehash/stage proof required','source_spec_pin':h.pin(specp),'canonical_authorized':False})
c=h.conn(db)
try:
 h.write(S/'before-all50-and-actual-state-v1.json',{'all50':before,'actual_state':h.state(c)})
 assert sha(opp)==op_pin['sha256'] and sha(specp)=='7e8b6bbec375e18f7ac0db7c2a54891039fcc80ee6edafbb0dc1254d1c3481a9';c.close()
 h.run_cli(['apply',str(opp),'--db',str(db),'--journal',str(journal)],S/'one-apply-actual-output.json')
 c=h.conn(db);final=h.state(c);h.write(S/'after-apply-actual-state-v1.json',{'actual_state':final,'stage_DB_pin':h.pin(db)})
 assert final=={'journal_head':444,'pending':0},final
 stored=dict(c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone());assert json.loads(stored['request_json'])==op;h.write(S/'exact-submitted-and-stored-operation-v1.json',{'operation_pin':op_pin,'stored':stored,'whole_submitted_API_equal':True})
 actual=h.native(c,x['id']+'@1');a=h.api(actual);expected={k:v for k,v in x.items() if k!='bindings'};assert a==expected,('Actual API difference',a,expected)
 after=h.all50(c);assert before['schema']==after['schema'];preserved={};allowed={'operation':1,'operation_payload':1,'object':1,'revision':1,'search':1,'dependency':2}
 for name in before['tables']:
  if name in h.DERIVED:continue
  assert after['tables'][name]['rows']==before['tables'][name]['rows']+allowed.get(name,0),name
  sql=base.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
  if 'WITHOUT ROWID' in sql.upper():assert before['tables'][name]==after['tables'][name];preserved[name]={'exact_full_table':True};continue
  limit=base.execute('select max(rowid) from "'+name+'"').fetchone()[0];old=h.rows(base,name,True);got=h.rows(c,name,True,limit) if limit is not None else [];assert old==got,('Old row/order changed',name);preserved[name]={'old_rowid_rows_exact':True,'old_row_count':len(old),'old_order_sha256':h.row_digest(old,True)}
 bsearch=[list(r) for r in base.execute('select object_id,kind,text from object_search order by object_id')];ssearch=[list(r) for r in c.execute('select object_id,kind,text from object_search where object_id!=? order by object_id',(x['id'],))];assert bsearch==ssearch
 text='\n'.join(str(y) for y in [x['id'],actual['disposition'],actual['evidence_status'],actual['rationale'],actual['caveat'],*actual['data'].values()] if y is not None);assert [list(r) for r in c.execute('select object_id,kind,text from object_search where object_id=?',(x['id'],))]==[[x['id'],'search',text]]
 for rid,n in protected.items():assert h.current(c,n['object_id'])==rid and h.native(c,rid)==n
 requests=[dict(r) for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')];assert requests==[]
 fullpin=h.write(S/'complete-one-actual-native-target-and-support-v1.json',{'target':actual,'source_support_objects':{rid:h.native(c,rid) for rid in supports},'full_API_equal':True,'ordered_arrays_unchanged':True})
 diffpin=h.write(S/'full-all50-old-row-order-protected42-and-exact-new-search-diff-v1.json',{'before':before,'after':after,'old_rows_preserved':preserved,'exact_new_row_counts':allowed,'derived_search_only_authorized_new_object':True,'protected42_exact':True,'all_old_current_heads_metadata_history_retained':True})
 requestpin=h.write(S/'actual-individual-requests-v1.json',{'actual_state':final,'requests':requests,'automatic_resolutions':False});c.close()
 validators=[]
 for cmd in ['verify','verify-assets','verify-source','inventory']:
  out=S/(cmd+'.json');h.run_cli([cmd,'--db',str(db),'--journal',str(journal)],out);validators.append(h.pin(out))
 for person in ['P-0269','P-0270']:
  out=S/(person+'-verified-pedigree.json');got=h.run_cli(['pedigree',person,'--db',str(db)],out);old=json.loads((R/'evaluations/T-0786/preparation'/('Adam-verified-current443.json' if person=='P-0269' else 'Axel-verified-current443.json')).read_text());assert got==old;validators.append(h.pin(out))
 assert h.all50(live)==before and sha(M)==proof['MAIN_pin']['sha256'];assert sha(opp)==op_pin['sha256'];assert sha(helper)==hp
 c=h.conn(db);assert h.state(c)==final;c.close()
 command=['node','genealogy2/cli.mjs','apply',str(opp.relative_to(R)),'--db','genealogy2/data/research.sqlite','--journal','genealogy2/journal']
 hand=h.write(S/'complete-one-search-stage-result-and-Astra-handoff-v1.json',{'task':'T-0786','package_pin':proposal,'operation_pin':op_pin,'source_spec_pin':h.pin(specp),'guard_consequence_pin':guard,'actual_state':final,'new_objects':1,'old_revisions':0,'native_target_and_support_pin':fullpin,'actual_request_pin':requestpin,'full_all50_diff_pin':diffpin,'stage_DB_pin':h.pin(db),'validators':validators,'main_all50_and_physical_SHA_unchanged':True,'protected42_exact':True,'executable_canonical_command_requires_separate_root_authorization':command,'canonical_applied':False,'source_and_independent_final_byte_approval_pending':True,'usage':'UNKNOWN pending root collector'})
 print(json.dumps({'handoff_pin':hand,'package_pin':proposal,'operation_pin':op_pin,'actual_state':final}))
except BaseException as e:
 try:c=h.conn(db);actual_state=h.state(c);c.close()
 except BaseException:actual_state=None
 h.write(S/'STOP-failure-preserved-v1.json',{'error':repr(e),'traceback':traceback.format_exc(),'actual_state':actual_state,'stage_DB_pin':h.pin(db),'main_pin':h.pin(M),'no_retry':True});raise
finally:base.close();live.close()
