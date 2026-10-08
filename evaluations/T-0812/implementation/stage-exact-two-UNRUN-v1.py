import json,hashlib,shutil,subprocess,importlib.util,time,traceback
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0812';I=D/'implementation';MAIN=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def cli(args,p):
 t=time.monotonic();r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=R,capture_output=True,text=True);p.write_text(r.stdout);save(p.with_suffix('.process.json'),{'args':args,'exit':r.returncode,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t});assert r.returncode==0,r.stderr;return json.loads(r.stdout)
def main():
 start=time.monotonic();b=json.load(open(D/'preparation/baseline-state-v1.json'));assert sha(MAIN)==b['main']['sha256'];basepath=R/b['backup']['path'];assert sha(basepath)==b['backup']['sha256'];base=h.conn(basepath);assert h.state(base)=={'journal_head':477,'pending':0};S=I/'stage479-sequence-v1';assert not S.exists();S.mkdir();db=S/'stage.sqlite';shutil.copyfile(basepath,db);journal=S/'journal';journal.mkdir();save(S/'baseline-all50.json',h.all50(base));proof=[]
 try:
  for index,(name,tablefile,opsha,ctsha)in enumerate([('operation-v1.json','consequence-table-v1.json','f4c93141988777743cd4dfc56ce26acd84cb8c14c98a52ae944197f602972914','65aab307977831cdac3d663ee4d081a740d349995fc40993f3007d305122fef2'),('repair-operation-v1.json','repair-consequence-table-v1.json','0821e87eb610b6e869b3cb820e1a9b9037fb6e57436f01e72c2cc72df0c2bd9f','f29573c78f9a208fc557a8fca4fdf458382a6981df5721ff2005ebb01854be83')],1):
   opath=I/name;assert sha(opath)==opsha and sha(I/tablefile)==ctsha;op=json.load(open(opath));table=json.load(open(I/tablefile));assert table['operation_sha256']==opsha;c=h.conn(db)
   for t in table['changes']:
    if t['old_native']is not None:assert h.native(c,h.current(c,t['object_id']))==t['old_native'],t['object_id']
   c.close();cli(['apply',str(opath),'--db',str(db),'--journal',str(journal)],S/f'apply-{index}.json');c=h.conn(db);state=h.state(c);assert state['journal_head']==477+index
   accepted=dict(c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone());expected_request={**op,'dependencyReviewVersion':2,'searchMemoryVersion':1};assert json.loads(accepted['request_json'])==expected_request;save(S/f'after-{index}-supported-cli-request-normalization-proof.json',{'raw_operation':op,'accepted_request':json.loads(accepted['request_json']),'only_supported_cli_metadata_added':{'dependencyReviewVersion':2,'searchMemoryVersion':1},'all_other_fields_literal_exact':True})
   literal=[]
   for x in op['changes']:
    n=h.native(c,h.current(c,x['id']));actual=h.api(n);assert actual==h.expected_defaults(x,actual),x['id'];literal.append({'object_id':x['id'],'actual_native':n,'literal_api_exact':True})
   for t in table['retains']:assert h.native(c,t['revision_id'])==t['old_native'];assert h.current(c,t['old_native']['object_id'])==t['revision_id']
   pending=[dict(x)for x in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];save(S/f'after-{index}-native-proof.json',{'state':state,'literal':literal,'retains_exact':len(table['retains']),'accepted':accepted});save(S/f'after-{index}-pending-full.json',pending);contexts=[]
   for q in pending:
    old=h.native(c,q['affected_revision_id']);cur=h.native(c,h.current(c,old['object_id']));bases=[]
    for e in old['evidence']:
     bn=h.native(c,e['basis_revision_id']);bases.append({'edge':e,'bound_native':bn,'current_stronger_native':h.native(c,h.current(c,bn['object_id']))})
    contexts.append({'request':q,'old_target_native':old,'current_target_native':cur,'changed_basis_native':h.native(c,q['changed_revision_id']),'all_old_basis_current_stronger':bases})
   save(S/f'after-{index}-pending-full-contexts.json',contexts);proof.append({'step':index,'state':state,'changes':len(literal),'retains':len(table['retains'])});c.close()
  c=h.conn(db);save(S/'actual-all50.json',h.all50(c));assert sha(MAIN)==b['main']['sha256'];save(S/'result.json',{'steps':proof,'state':h.state(c),'main_unchanged':True,'exact_sequence_tested':True,'elapsed_seconds':time.monotonic()-start});print(json.dumps({'state':h.state(c),'steps':proof}))
 except Exception as e:save(S/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.monotonic()-start});raise
if __name__=='__main__':main()
