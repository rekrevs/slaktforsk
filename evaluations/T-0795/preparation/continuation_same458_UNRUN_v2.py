"""Existing458 clone-only continuation. No first-op reapply or new clone."""
from pathlib import Path
import argparse,json,copy,importlib.util,time,traceback,datetime
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0795/preparation';S=O/'reviewed-stage-v1';D=O/'continuation-v1'
sp=importlib.util.spec_from_file_location('m',O/'stage_literal_UNRUN_v2.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);h=m.h;native=m.native;MAIN=m.MAIN
PRIMARY=R/'evaluations/T-0795/source-review/primary-stage-continuation-readiness-v1.json';INDEPENDENT=R/'evaluations/T-0795/independent-review/actual458-projection-seven-source-decisions-v1.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--authorization',type=Path,required=True);ap.add_argument('--sha256',required=True);a=ap.parse_args();assert h.sha(a.authorization)==a.sha256;auth=json.loads(a.authorization.read_text());assert auth['continuation_authorized'] is True and auth['helper_sha256']==h.sha(__file__)
 assert h.sha(PRIMARY)==auth['primary_sha256']=='1da27f8d292d9ae14c3c71017a344f76bcbe0e81fd0c1b60ccb03124c133069b';assert h.sha(INDEPENDENT)==auth['independent_sha256']=='75807dd0d8e1aa108cbb02878fba6f145c430586f8e3eb856b9fc6e9b3e77b48';assert json.loads(PRIMARY.read_text())['stage_continuation_ready'] is True and json.loads(INDEPENDENT.read_text())['PASS'] is True
 db=S/'stage.sqlite';assert h.sha(db)==auth['stage458_sha256']=='038545bf11bdab6f693d0e7067a0689a50b20d3e950ba625f36aa985297760d5';resolution=D/'resolution-operation.json';assert h.sha(resolution)==auth['resolution_sha256']=='e4a8247bcea7121e509ae1302a053dbc40f67184c97e2a155ca68d95245dbd73';op=json.loads((S/'operation-media-bound.json').read_text());assert h.sha(S/'operation-media-bound.json')=='df696be18e30db8e45bb5aa7be9d3ec508cd92698ff3c34ae9b94e6c3ec7d28c'
 base=h.conn(O/'baseline-j457.sqlite');actual=h.conn(db);live=h.conn(MAIN);bs=json.loads((O/'baseline-state.json').read_text());assert h.sha(MAIN)==bs['main']['sha256'] and h.state(live)=={'journal_head':457,'pending':0} and h.state(actual)=={'journal_head':458,'pending':7}
 stage=D/'actual459';assert not stage.exists();stage.mkdir();proof=[]
 for x in op['changes']:
  n=native(actual,h.current(actual,x['id']));api=h.api(n);expected=h.expected_defaults(x,api)
  if 'bindings' in expected:
   assert x['id'] in ['R-T0795-U'+str(i)+'-metadata' for i in range(1,7)]
   for oid,version in expected['bindings'].items():assert n['data']['source_id']==oid and version==1 and any(e['basis_revision_id']==oid+'@1' and e['role']=='supports' for e in n['evidence'])
   del expected['bindings']
  assert api==expected;proof.append({'approved_request':x,'actual_native':n,'actual_API':api,'approved_projection':'six request-only bindings omitted only after typed source_id and exact S@1 supports check'})
 before=h.all50(base)
 after=h.all50(actual)
 for t in before['tables']:
  if t not in h.DERIVED:
   schema=base.execute('select sql from sqlite_master where name=?',(t,)).fetchone()[0]
   if 'WITHOUT ROWID' in schema.upper():
    assert before['tables'][t]==after['tables'][t],('WITHOUT ROWID changed; return for specific review',t)
    continue
   count=base.execute('select max(rowid) from "'+t+'"').fetchone()[0] or 0
   if t in ['revision','origin','dependency','record_asset','record_media','operation_payload','operation','review_request','review_resolution','asset','native_asset'] or t in {x['kind'] for x in op['changes']} or t=='object':
    assert h.rows(base,t)==h.rows(actual,t,maximum=count),('old table changed',t)
   else:assert before['tables'][t]==after['tables'][t],t
 for t in ['origin','dependency','record_asset','record_media','review_resolution']:
  limit=base.execute('select max(rowid) from '+t).fetchone()[0] or 0
  assert h.rows(base,t,True)==h.rows(actual,t,True,maximum=limit),('ordered prefix changed',t)
 protected=json.loads((O/'protected-P0212-identity-tree-relation-OWNER.json').read_text())
 for rid,n in protected.items():assert h.current(actual,n['object_id'])==rid and native(actual,rid)==n
 for row in base.execute("select id from current_revision where id like 'ASSESSMENT%' or id like 'CONTRACT%' or id like 'THEME%'"):
  old=native(base,row[0]);now=native(actual,h.current(actual,old['object_id']));assert old['data'].get('outcome')==now['data'].get('outcome'),old['object_id']
 pending=[dict(x) for x in actual.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];h.write(stage/'literal-and-preservation-proof.json',{'changes':proof,'protected_unchanged':True,'outcomes_unchanged':True,'old_rows_unchanged':True,'all50_after':h.all50(actual),'state':h.state(actual)})

 h.write(stage/'projection-all35-proof.json',proof)
 actualpending=[dict(x) for x in actual.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];assert actualpending==json.loads((S/'actual-pending-full-after-stopped-stage.json').read_text());assert {q['id'] for q in actualpending}=={r['request'] for r in json.loads(resolution.read_text())['resolve']}
 m.run(['apply',str(resolution),'--db',str(db),'--journal',str(S/'journal')],stage/'apply-seven.json');assert h.state(actual)=={'journal_head':459,'pending':0}
 h.write(stage/'final459-all50.json',h.all50(actual))
 for item in proof:assert native(actual,item['actual_native']['id'])==item['actual_native'] and h.current(actual,item['actual_native']['object_id'])==item['actual_native']['id']
 h.write(stage/'final459-all35-full-native-proof.json',proof)
 # Historical full life review and all original native revisions stay byte-for-byte equal.
 rid='ASSESSMENT-T0790-P0212-life@1';assert native(actual,rid)==native(base,rid) and h.current(actual,'ASSESSMENT-T0790-P0212-life')==rid
 h.write(stage/'actual-seven-resolutions.json',[dict(x) for x in actual.execute('select * from review_resolution order by rowid') if x['request_id'] in {q['id'] for q in actualpending}])
 for name,args in [('P0212-person',['person','P-0212','--format','json']),('P0212-inspect',['inspect','P-0212']),('inventory',['inventory','--full']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270']),('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source'])]:
  got=m.run(args+['--db',str(db)],stage/(name+'.json'))
  if name.startswith('verify'):assert got['ok'] is True
 derived={k:h.pin(stage/(k+'.json')) for k in ['inventory','Adam-verified','Axel-verified','verify','verify-assets','verify-source']}
 h.write(stage/'final-stage-manifest.json',{'reviewed_stage_DB_pin':h.pin(db),'ordered_operations':[h.pin(S/'operation-media-bound.json'),h.pin(resolution)],'consequence_table_pin':h.pin(S/'final-media-bound-consequence-table.json'),'person_views':{'P-0212':{'baseline':h.pin(O/'P-0212-person.json'),'stage':h.pin(stage/'P0212-person.json')}},'final_derived_pins':derived,'final_state':h.state(actual),'actual_resolution_count':7,'main_unchanged':h.sha(MAIN)==bs['main']['sha256'],'source_final_gates':'pending dual exact finalstage SOURCE review','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});assert h.sha(MAIN)==bs['main']['sha256'];print({'state':h.state(actual),'manifest':h.pin(stage/'final-stage-manifest.json')})
if __name__=='__main__':
 started=time.monotonic()
 try:main()
 except BaseException as e:
  p=D/'continuation-failure-preserved.json'
  if not p.exists():h.write(p,{'error':str(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.monotonic()-started,'retry_authorized':False})
  raise
