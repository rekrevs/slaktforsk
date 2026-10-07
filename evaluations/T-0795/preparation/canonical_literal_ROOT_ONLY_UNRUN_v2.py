"""UNRUN root-only native CLI apply. Same pinned reviewed operation sequence.
No cloning/replacing live DB, retry, source grading or implicit resolve.
"""
import argparse,datetime,importlib.util,json,sqlite3,time,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[3];STAGE=R/'evaluations/T-0795/preparation/stage_literal_UNRUN_v2.py'
PEOPLE=['P-0212']
def main():
 assert __debug__
 p=argparse.ArgumentParser();p.add_argument('--authorization',required=True,type=Path);p.add_argument('--sha256',required=True);a=p.parse_args();start=time.monotonic()
 s=importlib.util.spec_from_file_location('stage_ro',STAGE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 h=m.h
 assert h.sha(a.authorization)==a.sha256;auth=json.loads(a.authorization.read_text());assert auth['task']=='T-0795' and auth['mode']=='ROOT_CANONICAL_EXACT_ONCE' and auth['root_authorized'] is True and auth['code_sha256']==h.sha(__file__)
 assert h.sha(STAGE)==auth['stage_helper_sha256']
 _,bs=h.readpin(auth['baseline_state_pin']);assert h.sha(R/bs['backup']['path'])==bs['backup']['sha256'];base=h.conn(R/bs['backup']['path']);live=h.conn(m.MAIN);assert h.sha(m.MAIN)==bs['main']['sha256'] and h.state(live)=={'journal_head':457,'pending':0} and h.all50(base)==h.all50(live)==bs['all50']
 stagepath=R/auth['reviewed_stage_DB_pin']['path']
 assert stagepath.resolve().is_relative_to(R/'evaluations/T-0795') and h.sha(stagepath)==auth['reviewed_stage_DB_pin']['sha256'];stage=h.conn(stagepath)
 ops=[]
 for pin in auth['ordered_operations']:
  path,op=h.readpin(pin);ops.append((path,op));stored=stage.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone();assert stored and json.loads(stored[0])==op
  assert not live.execute('select 1 from operation where id=?',(op['id'],)).fetchone()
 assert auth['final_state']==h.state(stage) and auth['final_state']['pending']==0
 for role in ['source_final_gate','independent_final_gate']:
  gspec=auth[role];_,g=h.readpin(gspec['pin']);assert h.pointer(g,gspec['ready_pointer']) is True
  for item in gspec['exact_bindings']:assert h.pointer(g,item['pointer'])==item['expected_value']
  assert set(gspec['bound_inputs'])=={'reviewed_stage_DB_pin','ordered_operations','consequence_table_pin'}
  for key in gspec['bound_inputs']:assert h.pointer(g,gspec['bound_inputs'][key])==auth[key]
 _,table=h.readpin(auth['consequence_table_pin']);assert table['operation_sha256']==auth['ordered_operations'][0]['sha256']
 out=(R/auth['output_path']).resolve();assert out.is_relative_to(R/'evaluations/T-0795') and not out.exists();out.mkdir();h.write(out/'authorization.json',auth)
 before=h.all50(live);h.write(out/'fresh-live457-all50.json',before)
 # Root supplies exact baseline and staged person JSON views; legacy gate/privacy
 # state must be approved as retained or explicitly changed by both source gates.
 for person in PEOPLE:
  for which,db in [('baseline',m.MAIN),('stage',stagepath)]:
   _,expected=h.readpin(auth['person_views'][person][which]);got=m.run(['person',person,'--format','json','--db',str(db)],out/(person+'-'+which+'.json'));assert got==expected
 attempted=[]
 try:
  for i,(path,op) in enumerate(ops):
   assert h.sha(a.authorization)==a.sha256 and h.sha(stagepath)==auth['reviewed_stage_DB_pin']['sha256']
   for pin in auth['ordered_operations']:h.readpin(pin)
   h.write(out/f'before-step-{i+1}.json',{'state':h.state(live),'operation':op['id']});attempted.append(op['id'])
   m.run(['apply',str(path),'--db',str(m.MAIN),'--journal',str(R/'genealogy2/journal')],out/f'apply-{i+1}.json')
  assert h.state(live)==auth['final_state'];newids={op['id'] for _,op in ops};checks=[];clocks=[]
  schema=[tuple(x) for x in stage.execute("select name,sql from sqlite_master where type='table' order by name")];assert len(schema)==50 and schema==[tuple(x) for x in live.execute("select name,sql from sqlite_master where type='table' order by name")]
  def key(row):return json.dumps(row,ensure_ascii=False,sort_keys=True,default=lambda b:{'bytes_hex':b.hex()})
  for name,_ in schema:
   left=[dict(x) for x in stage.execute('select * from "'+name+'"')];right=[dict(x) for x in live.execute('select * from "'+name+'"')]
   if name=='operation':
    rd={x['id']:x for x in right};assert len(left)==len(right)
    for row in left:
     other=rd[row['id']];lc=row.pop('recorded_at');rc=other.pop('recorded_at');assert row==other
     if lc!=rc:assert row['id'] in newids;clocks.append({'operation':row['id'],'stage':lc,'live':rc})
   else:assert sorted(left,key=key)==sorted(right,key=key),name
   checks.append(name)
  for name in ['dependency','origin','record_asset','record_media','review_resolution']:
   assert [tuple(x) for x in stage.execute('select rowid,* from '+name+' order by rowid')]==[tuple(x) for x in live.execute('select rowid,* from '+name+' order by rowid')],name
  for person in PEOPLE:
   _,expected=h.readpin(auth['person_views'][person]['stage']);got=m.run(['person',person,'--format','json','--db',str(m.MAIN)],out/(person+'-actual.json'));assert got==expected
  validations=[]
  for label,args in [('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source']),('inventory',['inventory','--full']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]:
   got=m.run(args+['--db',str(m.MAIN)],out/(label+'.json'))
   if label.startswith('verify'):assert got['ok'] is True
   _,expected=h.readpin(auth['final_derived_pins'][label]);assert got==expected
   validations.append(label)
  h.write(out/'actual-result.json',{'actual_state':h.state(live),'raw_all50_exact_stage':checks,'new_operation_clock_differences_only':clocks,'P0212_full_person_JSON_exact_stage':True,'validator_checks':validations,'elapsed_monotonic_seconds':time.monotonic()-start,'no_DB_replacement':True,'no_retry':True})
 except BaseException as e:
  h.write(out/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'actual_state':h.state(live),'attempted_operations':attempted,'elapsed_monotonic_seconds':time.monotonic()-start,'retry_authorized':False});raise
 finally:base.close();live.close();stage.close()
if __name__=='__main__':main()
