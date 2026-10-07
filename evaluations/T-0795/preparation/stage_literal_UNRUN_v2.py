"""Root-gated clone-only stage, never main. Stop after actual dependency requests."""
from pathlib import Path
import argparse,json,copy,sqlite3,subprocess,importlib.util,datetime,time,traceback
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0795/preparation';P=O/'literal-package-v1';MAIN=R/'genealogy2/data/research.sqlite'
s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
assert h.sha(R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py')=='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2'
def native(c,rid):
 n=h.native(c,rid)
 for k,t in [('origins','origin'),('evidence','dependency')]:n[k]=[dict(x) for x in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
def run(args,p):
 r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);p.write_text(r.stdout);p.with_suffix('.stderr').write_text(r.stderr);h.write(p.with_suffix('.process.json'),{'args':args,'returncode':r.returncode});assert r.returncode==0,('STOP preserve failure',p,r.stderr);return json.loads(r.stdout)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--authorization',type=Path,required=True);ap.add_argument('--authorization-sha256',required=True);a=ap.parse_args();assert h.sha(a.authorization)==a.authorization_sha256;auth=json.loads(a.authorization.read_text());assert auth['clone_stage_authorized'] is True and auth['stage_helper_sha256']==h.sha(__file__)
 pins={'draft':'0107f182747a0416abf7cace9b09e24b712f7d848e13ee81364608861f06731e','media':'486102da3cc2fbfce5e98deb59e3f8b0cf2481dc7af7ed95e252c2818f6a2d34','table':'667882aac820fd0264101b2d1cfd80c4e14de9062adef6a7e75432660e568112'}
 for role,name in [('draft','operation-DRAFT-no-media.json'),('media','six-media-stage-plan.json'),('table','individual-consequence-table.json')]:assert h.sha(P/name)==pins[role] and auth['package'][role]==pins[role]
 for role in ['primary_gate','independent_gate']:
  g=auth[role];path=R/g['path'];assert h.sha(path)==g['sha256'];gate=json.loads(path.read_text());assert h.pointer(gate,g['pass_pointer']) is True
  for role,ptr in g['package_bindings'].items():assert h.pointer(gate,ptr)==pins[role]
  assert set(g['package_bindings'])==set(pins)
 base=h.conn(O/'baseline-j457.sqlite');live=h.conn(MAIN);bs=json.loads((O/'baseline-state.json').read_text());assert h.sha(MAIN)==bs['main']['sha256'];assert h.state(live)==h.state(base)=={'journal_head':457,'pending':0};assert h.all50(live)==h.all50(base)
 stage=O/'reviewed-stage-v1';assert not stage.exists();stage.mkdir();db=stage/'stage.sqlite';w=sqlite3.connect(db);base.backup(w);w.close();journal=stage/'journal';journal.mkdir();op=json.loads((P/'operation-DRAFT-no-media.json').read_text());media=json.loads((P/'six-media-stage-plan.json').read_text());assert len(op['changes'])==35 and len(media)==6;assert len(json.loads((P/'individual-consequence-table.json').read_text())['rows'])==48
 op['media']=[]
 for i,m in enumerate(media,1):
  assert h.sha(R/m['path'])==m['sha256'];result=run(['stage-media',str(R/m['path']),'--provenance',m['provenance']],stage/f'media-{i}.json');assert result['sha256']==m['sha256'];op['media'].append(result);record=next(x for x in op['changes'] if x['id']==m['record_id']);record['media']=[{'id':result['id'],'region':m['region']}]
 operation=stage/'operation-media-bound.json';h.write(operation,op);h.write(stage/'final-media-bound-consequence-table.json',{'operation_sha256':h.sha(operation),'draft_table':h.pin(P/'individual-consequence-table.json'),'rows':json.loads((P/'individual-consequence-table.json').read_text())['rows'],'media':op['media'],'source_semantics_unchanged':True});before=h.all50(base);run(['apply',str(operation),'--db',str(db),'--journal',str(journal)],stage/'apply.json');actual=h.conn(db);assert h.state(actual)['journal_head']==458
 proof=[]
 for x in op['changes']:
  n=native(actual,h.current(actual,x['id']));api=h.api(n);assert api==h.expected_defaults(x,api),(x['id'],'literal differs');proof.append({'approved_api':x,'actual_native':n})
 # Every old immutable revision and ordered native edge prefix preserved.
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
 pending=[dict(x) for x in actual.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];h.write(stage/'actual-pending-full.json',pending);h.write(stage/'literal-and-preservation-proof.json',{'changes':proof,'protected_unchanged':True,'outcomes_unchanged':True,'old_rows_unchanged':True,'all50_after':h.all50(actual),'state':h.state(actual)})
 for name,args in [('P0212-person',['person','P-0212','--format','json']),('P0212-inspect',['inspect','P-0212']),('inventory',['inventory','--full']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270']),('verify',['verify']),('verify-assets',['verify-assets']),('verify-source',['verify-source'])]:run(args+['--db',str(db)],stage/(name+'.json'))
 h.write(stage/'stage-result.json',{'operation':h.pin(operation),'database':h.pin(db),'state':h.state(actual),'pending':len(pending),'source_review':'STOP individual dual Astra dispositions required for actual pending before final ready','main_unchanged':h.sha(MAIN)==bs['main']['sha256'],'authorization':h.pin(a.authorization),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});assert h.sha(MAIN)==bs['main']['sha256'];print({'stage':str(stage),'state':h.state(actual),'pending':len(pending)})
if __name__=='__main__':
 started=time.monotonic()
 try:main()
 except BaseException as e:
  path=O/'stage-v2-failure-preserved.json'
  if not path.exists():h.write(path,{'error':str(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.monotonic()-started,'retry_authorized':False})
  raise
