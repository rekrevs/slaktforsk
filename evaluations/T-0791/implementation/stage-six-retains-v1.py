"""Exact source/independent-approved resolve-only operation on new task-local clone."""
import datetime,hashlib,importlib.util,json,shutil,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0791/implementation';PRE=D/'stage461-v2';DEST=D/'stage462-v1';assert not DEST.exists();START=time.monotonic();H=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';s=importlib.util.spec_from_file_location('h',H);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pin=lambda p:{'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def cli(args,p):
 r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);save(p.with_suffix('.process.json'),{'args':args,'returncode':r.returncode,'stderr':r.stderr});assert not p.exists();p.write_text(r.stdout);assert r.returncode==0,r.stderr;return json.loads(r.stdout)
def native(c,rid):
 n=h.native(c,rid)
 for k,t in [('origins','origin'),('evidence','dependency')]:n[k]=[dict(r)for r in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
OP=D/'candidate-six-retains-operation-v1.json';assert sha(OP)=='bd4a9f79b5ae6043a4d176b367fdc0d021222103f0dcc6543ff0600bbbab81e1';op=json.loads(OP.read_text());assert op['changes']==[] and len(op['resolve'])==6
source=R/'evaluations/T-0791/primary/six-retains-clone-gate-v1.json';indep=R/'evaluations/T-0791/independent-six-retains-clone-gate-v1.json';assert sha(indep)=='0d87e066028709e4b941e7bd3858bebe105c0bd401a97a8ff779e1750dc2bfc0';sg=json.loads(source.read_text());ig=json.loads(indep.read_text());assert ig['ready_for_clone_stage'] is True and ig['operationSha256']==sha(OP);assert sg['operationSha256']==sha(OP)
bs=json.loads((D/'baseline-state-v1.json').read_text());MAIN=R/bs['main']['path'];assert sha(MAIN)==bs['main']['sha256'];pre=h.conn(PRE/'stage.sqlite');assert h.state(pre)=={'journal_head':461,'pending':6};before=h.all50(pre);requests=[dict(r)for r in pre.execute('select q.* from review_request q left join review_resolution s on s.request_id=q.id where s.request_id is null order by q.id')];assert [r['request']for r in op['resolve']]==[r['id']for r in requests]
objects={r['affected_revision_id']:native(pre,r['affected_revision_id'])for r in requests};DEST.mkdir();db=DEST/'stage.sqlite';shutil.copyfile(PRE/'stage.sqlite',db);journal=DEST/'journal';journal.mkdir();save(DEST/'preimage-and-gates.json',{'preimage':pin(PRE/'stage.sqlite'),'source_gate':pin(source),'independent_gate':pin(indep),'operation':pin(OP),'before_all50':before,'affected_full_native':objects,'canonicalApproval':False})
try:
 applied=cli(['apply',str(OP),'--db',str(db),'--journal',str(journal)],DEST/'apply.json');c=h.conn(db);assert h.state(c)=={'journal_head':462,'pending':0};req=json.loads(c.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone()[0]);assert req==op;after=h.all50(c);assert after['schema']==before['schema'];assert after['ordered_native_arrays']==before['ordered_native_arrays']
 for name in before['tables']:
  if name in ['operation','operation_payload','review_resolution']:
   limit=pre.execute('select max(rowid) from "'+name+'"').fetchone()[0];assert h.rows(c,name,True,limit)==h.rows(pre,name,True)
  else:assert after['tables'][name]==before['tables'][name],name
 assert all(native(c,rid)==old for rid,old in objects.items());actual=[dict(r)for r in c.execute('select * from review_resolution where operation_id=? order by rowid',(op['id'],))];assert [{'request':r['request_id'],'rationale':r['rationale']}for r in actual]==op['resolve']
 save(DEST/'six-exact-retains-full-native-and-order-proof.json',{'passed':True,'requests':requests,'approved_resolve':op['resolve'],'actual_resolution_rows':actual,'affected_native_unchanged':objects,'before_all50':before,'after_all50':after,'ordered_arrays_unchanged':True,'only_three_append_tables':True})
 c.close();pre.close()
 for name,args in [('verify',['verify']),('inventory',['inventory']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]:
  r=cli(args+['--db',str(db),'--journal',str(journal)],DEST/(name+'.json'))
  if name=='verify':assert r['ok'] is True
 r=subprocess.run(['node','evaluations/T-0791/implementation/capture-review-axes-v1.mjs',str(DEST.relative_to(R))],cwd=R,capture_output=True,text=True);save(DEST/'axis-proof.process.json',{'returncode':r.returncode,'stderr':r.stderr,'stdout':r.stdout});assert r.returncode==0,r.stderr
 assert sha(MAIN)==bs['main']['sha256'];save(DEST/'result.json',{'passed':True,'state':{'journal_head':462,'pending':0},'stage_db':pin(db),'literal_resolves_equal':True,'all_six_old_assessments_preserved':True,'full_native_arrays_order_preserved':True,'canonical_unchanged':True,'source_media_assets_checks_reuse':{'proof':'Only operation/operation_payload/review_resolution appended; source/media/assets schemas/table data exactly equal stage461 verified inputs.','first_stage_result':pin(PRE/'result.json')},'source_final_approval':False,'elapsed_seconds':time.monotonic()-START})
except BaseException as e:
 save(DEST/'failure-preserved.json',{'error':str(e),'elapsed_seconds':time.monotonic()-START,'no_auto_retry':True});raise
