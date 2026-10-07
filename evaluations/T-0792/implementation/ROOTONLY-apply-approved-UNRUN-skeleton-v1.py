# GENERIC SKELETON ONLY: no final source pins or authorization supplied.
# Root must review final exact task-specific version after both final source gates.
"""ROOT ONLY UNRUN. Requires root-created true authorization plus both final source gates.
Canonical writes use exact approved controlled CLI operations; never database replacement.
"""
import argparse,hashlib,importlib.util,json,sqlite3,subprocess,time,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0792/implementation';MAIN=R/'genealogy2/data/research.sqlite';H=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def loadpin(pin):
 p=(R/pin['path']).resolve();assert p.is_relative_to(R) and sha(p)==pin['sha256'];return p,json.loads(p.read_text())
def ptr(x,p):
 for k in p.strip('/').split('/')if p else []:x=x[int(k)]if isinstance(x,list)else x[k]
 return x
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 pa=argparse.ArgumentParser();pa.add_argument('--authorization',required=True);pa.add_argument('--authorization-sha256',required=True);ar=pa.parse_args();ap=Path(ar.authorization).resolve();assert ap.is_relative_to(D) and sha(ap)==ar.authorization_sha256;a=json.loads(ap.read_text());assert a['task']=='T-0792' and a['mode']=='ROOT_ONLY_EXACT_APPROVED_CANONICAL_APPLIES' and a['rootAuthorized'] is True and a['code_sha256']==sha(Path(__file__))
 assert sha(H)==a['helper_pin']['sha256'];sp=importlib.util.spec_from_file_location('h',H);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
 mp,m=loadpin(a['final_manifest_pin']);assert m['state']==a['final_state']
 for f in m['files']:assert sha(R/f['path'])==f['sha256'],f
 _,ct=loadpin(a['consequence_table_pin']);assert ct['operation_sha256']==a['operation_pins'][0]['sha256']
 for f in a.get('extra_allocation_pins',[]):loadpin(f)
 _,bs=loadpin(a['baseline_state_pin']);base=h.conn(R/bs['backup']['path']);assert sha(R/bs['backup']['path'])==bs['backup']['sha256'];assert sha(MAIN)==bs['main']['sha256'];live=h.conn(MAIN);assert h.state(base)==h.state(live)==a['baseline_state'] and h.all50(base)==h.all50(live)
 finaldb,_=loadpin(a['final_result_pin']);fr=json.loads(finaldb.read_text());stagepath=R/fr['stage_db']['path'];assert sha(stagepath)==fr['stage_db']['sha256'];stage=h.conn(stagepath);assert h.state(stage)==a['final_state'];ops=[]
 for pin in a['operation_pins']:
  p,op=loadpin(pin);ops.append((p,op,pin))
 assert len(ops)==len(a['operation_expectations']) and len(ops)>0
 for (_,op,_),expected in zip(ops,a['operation_expectations']):
  assert op['id']==expected['id'] and len(op['changes'])==expected['change_count'] and len(op.get('resolve',[]))==expected['resolve_count']
 for role in ['primary_final_gate','independent_final_gate']:
  gspec=a[role];_,g=loadpin(gspec['pin']);assert ptr(g,gspec['ready_pointer']) is True;assert ptr(g,gspec['manifest_sha_pointer'])==a['final_manifest_pin']['sha256'];assert ptr(g,gspec['stage_db_sha_pointer'])==fr['stage_db']['sha256'];assert ptr(g,gspec['consequence_sha_pointer'])==a['consequence_table_pin']['sha256']
  assert [ptr(g,p)for p in gspec['operation_sha_pointers']]==[x[2]['sha256']for x in ops]
 out=(R/a['output_path']).resolve();assert out.is_relative_to(D) and not out.exists();out.mkdir();before=h.all50(live);start=time.monotonic();save(out/'preimage-and-root-authorization.json',{'authorization':a,'authorization_sha256':ar.authorization_sha256,'before_all50':before,'state':h.state(live),'main_preimage_sha256':sha(MAIN)})
 def cli(args,p):
  z=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);save(p.with_suffix('.process.json'),{'args':args,'returncode':z.returncode,'stderr':z.stderr});assert not p.exists();p.write_text(z.stdout);assert z.returncode==0,z.stderr;return json.loads(z.stdout)
 try:
  for i,(p,op,pin)in enumerate(ops,1):
   assert sha(p)==pin['sha256'];cli(['apply',str(p)],out/f'actual-apply-{i}.json');c=h.conn(MAIN);assert h.state(c)==a['operation_expectations'][i-1]['resulting_state'];accepted=dict(c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone());assert json.loads(accepted['request_json'])==op;save(out/f'actual-accepted-request-{i}.json',accepted);c.close()
  c=h.conn(MAIN);actual=h.all50(c);reviewed=h.all50(stage);assert actual['schema']==reviewed['schema']==before['schema'];assert actual['ordered_native_arrays']==reviewed['ordered_native_arrays'];assert all(h.rows(c,n,True)==h.rows(stage,n,True) for n in (*h.ORDER_TABLES,'review_resolution'));proof={}
  opids=[op['id']for _,op,_ in ops]
  for name in reviewed['tables']:
   if name!='operation':assert actual['tables'][name]==reviewed['tables'][name],name;proof[name]='full rows exact reviewed stage'
   else:
    sr=[dict(x)for x in stage.execute('select * from operation order by id')];lr=[dict(x)for x in c.execute('select * from operation order by id')];stamps={x['id']:x['recorded_at']for x in sr};dif=[]
    for x in lr:
     if x['id'] in opids:dif.append({'operation':x['id'],'canonical_recorded_at':x['recorded_at'],'stage_recorded_at':stamps[x['id']]});x['recorded_at']=stamps[x['id']]
    assert lr==sr;proof[name]={'full_rows_exact_except_exact_approved_operation_recorded_at_fields':dif}
  # Every old immutable row and native order matches the live preimage.
  for name in before['tables']:
   if name in h.DERIVED:continue
   sql=base.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
   if 'WITHOUT ROWID' in sql.upper():assert actual['tables'][name]==before['tables'][name];continue
   maximum=base.execute('select max(rowid) from "'+name+'"').fetchone()[0]
   if maximum is not None:assert h.rows(c,name,True,maximum)==h.rows(base,name,True),name
  save(out/'actual-vs-reviewed-all50-and-order-proof.json',{'passed':True,'state':h.state(c),'tables':proof,'before_all50':before,'actual_all50':actual,'reviewed_stage_all50':reviewed,'ordered_native_arrays_exact':True,'old_native_rows_order_exact':True,'no_database_replacement':True});c.close()
  for label,args in [('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source']),('inventory',['inventory']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]:
   v=cli(args,out/(label+'.json'))
   if label.startswith('verify'):assert v['ok'] is True
   if label in ['inventory','Adam-verified','Axel-verified']:assert v==json.loads((stagepath.parent/(label+'.json')).read_text()),label
  for pid in ['P-0241','P-0246','P-0239','P-0240']:
   reviewed_person=cli(['person',pid,'--full','--format','json','--db',str(stagepath)],out/(pid+'-reviewed-stage-full.json'))
   actual_person=cli(['person',pid,'--full','--format','json'],out/(pid+'-actual-full.json'));assert actual_person==reviewed_person,pid
  save(out/'actual-canonical-result.json',{'passed':True,'state':a['final_state'],'actual_main_sha256':sha(MAIN),'approved_stage_db_sha256':fr['stage_db']['sha256'],'all50_exact_except_approved_operation_timestamps':True,'all_five_ordered_native_arrays_exact':True,'four_full_person_views_exact_reviewed_stage':True,'default_pedigrees_and_inventory_exact_stage':True,'elapsed_seconds':time.monotonic()-start,'source_approval_pins':[a['primary_final_gate']['pin'],a['independent_final_gate']['pin']]})
 except BaseException as e:
  z=h.conn(MAIN);save(out/'failure-preserved-no-auto-retry.json',{'error':str(e),'traceback':traceback.format_exc(),'actual_state':h.state(z),'elapsed_seconds':time.monotonic()-start,'do_not_repeat_completed_operations':True});z.close();raise
 finally:base.close();live.close();stage.close()
if __name__=='__main__':main()
