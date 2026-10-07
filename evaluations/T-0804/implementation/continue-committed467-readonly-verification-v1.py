"""Read-only continuation after successful467commit and failed FTS shadow-table expectation. NO APPLY."""
import json,hashlib,importlib.util,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0804/implementation';PRE=D/'stage466-v1';S=D/'stage467-v1';start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pin=lambda p:{'path':str(p.relative_to(R)),'sha256':sha(p)};sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def native(c,rid):
 n=h.native(c,rid)
 for key,t in [('origins','origin'),('evidence','dependency')]:n[key]=[dict(z)for z in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
def cli(args,p):
 z=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);save(p.with_suffix('.process.json'),{'args':args,'returncode':z.returncode,'stderr':z.stderr});assert not p.exists();p.write_text(z.stdout);assert z.returncode==0,z.stderr;return json.loads(z.stdout)
OP=D/'candidate-P0005-life-basis-repair-operation-v1.json';assert sha(OP)=='3f8f3d7007169e2afb66b771d19da9ad57887b010de20824b88ed42215c4db1c';op=json.load(open(OP));bs=json.load(open(R/'evaluations/T-0804/preparation/baseline-state-v1.json'));MAIN=R/bs['main']['path'];assert sha(MAIN)==bs['main']['sha256'];db=S/'stage.sqlite';db_preimage=sha(db);base=h.conn(PRE/'stage.sqlite');c=h.conn(db);assert h.state(c)=={'journal_head':467,'pending':0};assert json.loads(c.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone()[0])==op;before=h.all50(base);after=h.all50(c);assert before['schema']==after['schema'];oid='ASSESSMENT-T0790-P0005-life';old=native(base,h.current(base,oid));new=native(c,h.current(c,oid));api=h.api(old);api['expectedVersion']=1;api['evidence'][25]['version']=2;actual=h.api(new);assert op['changes']==[api]and actual==h.expected_defaults(api,actual)
expected_changed={'revision','assessment','dependency','operation','operation_payload'}
for name in before['tables']:
 if name in h.DERIVED:continue
 if name not in expected_changed:assert before['tables'][name]==after['tables'][name],name
 sql=base.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
 if 'WITHOUT ROWID' in sql.upper():assert before['tables'][name]==after['tables'][name];continue
 maximum=base.execute('select max(rowid)from "'+name+'"').fetchone()[0]
 if maximum is not None:assert h.rows(c,name,True,maximum)==h.rows(base,name,True),name
for row in base.execute('select object_id,id from current_revision'):
 if row['object_id']!=oid:assert h.current(c,row['object_id'])==row['id']and native(c,row['id'])==native(base,row['id'])
untouched=lambda db:[dict(z)for z in db.execute('select *from object_search where object_id<>?order by object_id',(oid,))];assert untouched(base)==untouched(c)
expected_text='\n'.join(str(z)for z in [oid,new['disposition'],new['evidence_status'],new['rationale'],new['caveat'],*new['data'].values()]if z is not None);assert [dict(z)for z in c.execute('select object_id,kind,text from object_search where object_id=?',(oid,))]==[{'object_id':oid,'kind':new['kind'],'text':expected_text}]
save(S/'literal-repair-full-native-and-all50-proof.json',{'passed':True,'old_native':old,'new_native':new,'approved_api':api,'actual_api':actual,'before_all50':before,'after_all50':after,'only_edge_index25_version_changed':True,'all_other_current_objects_full_native_exact':True,'all_old_native_rows_and_array_order_exact':True,'derivedFTSQualification':{'failed_original_expectation':'object_search_content incorrectly treated as immutable although indexObject rebuilds current search representation','actual_changed_derived_tables':[name for name in h.DERIVED if before['tables'][name]!=after['tables'][name]],'untouched_search_rows_exact':True,'updated_search_text_exact_current_native':True,'full_native_api_source_approved_exact':True},'no_reapply_no_DB_mutation':True,'canonical_unchanged':True});save(S/'actual-requests-full-context.json',{'actual_state':h.state(c),'requests':[],'objects':{},'source_individual_disposition_required':False});c.close();base.close()
for label,args in [('verify',['verify']),('inventory',['inventory']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]:
 z=cli(args+['--db',str(db),'--journal',str(S/'journal')],S/(label+'.json'))
 if label=='verify':assert z['ok']is True
assert sha(db)==db_preimage and sha(MAIN)==bs['main']['sha256'];save(S/'result.json',{'passed':True,'state':{'journal_head':467,'pending':0},'stage_db':pin(db),'literal_repair_equal':True,'all_old_rows_and_order_preserved':True,'all_other_current_objects_exact':True,'canonical_unchanged':True,'read_only_continuation':True,'no_reapply':True,'source_media_assets_checks_reuse':{'proof':'All source/record/assets/media tables exact unchanged from stage465 source checks via466 and467all50 proof.','first_stage_result':pin(D/'stage465-v1/result.json')},'source_final_approval':False,'failed_original_helper_pin':pin(D/'stage-P0005-life-repair-v1.py'),'failed_attempt_pin':pin(S/'failure-preserved.json'),'readonly_verification_elapsed_seconds':time.monotonic()-start});print('467 readonly verification PASS; no reapply')
