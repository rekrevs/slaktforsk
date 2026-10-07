import json,hashlib,importlib.util,shutil,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0804/implementation';PRE=D/'stage466-v1';S=D/'stage467-v1';assert not S.exists();start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pin=lambda p:{'path':str(p.relative_to(R)),'sha256':sha(p)}
sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def native(c,rid):
 n=h.native(c,rid)
 for key,t in [('origins','origin'),('evidence','dependency')]:n[key]=[dict(z)for z in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
def cli(args,p):
 z=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);save(p.with_suffix('.process.json'),{'args':args,'returncode':z.returncode,'stderr':z.stderr});assert not p.exists();p.write_text(z.stdout);assert z.returncode==0,z.stderr;return json.loads(z.stdout)
OP=D/'candidate-P0005-life-basis-repair-operation-v1.json';assert sha(OP)=='3f8f3d7007169e2afb66b771d19da9ad57887b010de20824b88ed42215c4db1c';op=json.loads(OP.read_text());T=D/'P0005-life-basis-repair-consequence-v1.json';assert sha(T)=='94d5e2013aa7b582326c86723823b9798a1b52d4c5208dfff6bc8ca45fb105c7'
gates=[]
for path,expected in [('primary-P0005-life-repair-clone-gate-v1.json','b3813d8fd11d6b2127d1d0b66ba6993d1e0e5f391bde7fcd34d6c6f72b3ae5c7'),('independent-P0005-life-repair-clone-gate-v1.json','59d738c97e9426c6def10b55e8b8d6a86eb45c05d98f2351d3d6c067293e0fec')]:
 p=R/'evaluations/T-0804'/path;assert sha(p)==expected;g=json.loads(p.read_text());assert g['ready_for_clone_stage']is True and g['operationSha256']==sha(OP);gates.append(pin(p))
bs=json.load(open(R/'evaluations/T-0804/preparation/baseline-state-v1.json'));MAIN=R/bs['main']['path'];assert sha(MAIN)==bs['main']['sha256'];base=h.conn(PRE/'stage.sqlite');assert h.state(base)=={'journal_head':466,'pending':0};before=h.all50(base);oid='ASSESSMENT-T0790-P0005-life';old=native(base,h.current(base,oid));api=h.api(old);api['expectedVersion']=1;assert api['evidence'][25]['object']=='REL-parent-P-0007-P-0005'and api['evidence'][25]['version']==1;api['evidence'][25]['version']=2;assert op['changes']==[api] and not op.get('resolve');S.mkdir();db=S/'stage.sqlite';shutil.copyfile(PRE/'stage.sqlite',db);journal=S/'journal';journal.mkdir();save(S/'preimage-and-repair-gates.json',{'before_all50':before,'preimage':pin(PRE/'stage.sqlite'),'operation':pin(OP),'consequence':pin(T),'source_gates':gates,'old_native':old,'no_canonical':True})
try:
 cli(['apply',str(OP),'--db',str(db),'--journal',str(journal)],S/'apply.json');c=h.conn(db);assert h.state(c)['journal_head']==467;after=h.all50(c);assert before['schema']==after['schema'];new=native(c,h.current(c,oid));actual=h.api(new);assert actual==h.expected_defaults(api,actual);assert json.loads(c.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone()[0])==op
 for name in before['tables']:
  if name in h.DERIVED:continue
  sql=base.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
  if 'WITHOUT ROWID' in sql.upper():assert before['tables'][name]==after['tables'][name];continue
  maximum=base.execute('select max(rowid) from "'+name+'"').fetchone()[0]
  if maximum is not None:assert h.rows(c,name,True,maximum)==h.rows(base,name,True),name
 for name in before['tables']:
  if name not in ['revision','assessment','dependency','operation','operation_payload','object_search','review_request']:assert before['tables'][name]==after['tables'][name],name
 assert h.rows(c,'review_resolution',True)==h.rows(base,'review_resolution',True)
 for row in base.execute('select object_id,id from current_revision'):
  if row['object_id']!=oid:assert h.current(c,row['object_id'])==row['id'] and native(c,row['id'])==native(base,row['id'])
 pending=[dict(z)for z in c.execute('select q.*from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.id')];pool={}
 def add(rid):
  if rid in pool:return
  pool[rid]=native(c,rid)
  for e in pool[rid]['evidence']:add(e['basis_revision_id'])
 for q in pending:add(q['affected_revision_id']);add(q['changed_revision_id']);add(h.current(c,pool[q['affected_revision_id']]['object_id']))
 save(S/'actual-requests-full-context.json',{'actual_state':h.state(c),'requests':pending,'objects':pool,'source_individual_disposition_required':bool(pending)});save(S/'literal-repair-full-native-and-all50-proof.json',{'passed':True,'old_native':old,'new_native':new,'approved_api':api,'actual_api':actual,'before_all50':before,'after_all50':after,'only_edge_index25_version_changed':True,'all_other_current_objects_full_native_exact':True,'all_old_native_rows_and_array_order_exact':True,'canonical_unchanged':sha(MAIN)==bs['main']['sha256']});state=h.state(c);c.close();base.close()
 for label,args in [('verify',['verify']),('inventory',['inventory']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]:
  z=cli(args+['--db',str(db),'--journal',str(journal)],S/(label+'.json'))
  if label=='verify':assert z['ok']is True
 assert sha(MAIN)==bs['main']['sha256'];save(S/'result.json',{'passed':True,'state':state,'stage_db':pin(db),'literal_repair_equal':True,'all_old_rows_and_order_preserved':True,'canonical_unchanged':True,'source_media_assets_checks_reuse':{'proof':'All source/record/asset/media tables exactly unchanged from stage465 accepted source checks, with fullstage466 and467 table equality proofs.','first_stage_result':pin(D/'stage465-v1/result.json')},'source_final_approval':False,'elapsed_seconds':time.monotonic()-start})
except BaseException as e:save(S/'failure-preserved.json',{'error':str(e),'elapsed_seconds':time.monotonic()-start,'no_auto_retry':True});raise
