import pathlib,json,hashlib,shutil,subprocess,time,importlib.util,traceback
R=pathlib.Path.cwd();D=R/'evaluations/T-0814';I=D/'implementation';MAIN=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 start=time.monotonic();b=json.load(open(D/'preparation/baseline-v1.json'));assert sha(MAIN)==b['main']['sha256'];pin=json.load(open(I/'resolution-stage-preimage-pin-v1.json'));source=R/pin['path'];assert sha(source)==pin['sha256'];old=h.conn(source);assert h.state(old)=={'journal_head':482,'pending':42};opath=I/'42-resolution-operation-v1.json';tpath=I/'42-resolution-consequence-table-v1.json';assert sha(opath)=='5603a8fe7a99d2ada43e0bf77a9836e0d9cd3746cdd937ddd28b04b42f05b3e5';assert sha(tpath)=='bfd7e9fdcb9bf2f6b82356e05a0794062de04836bd71d4379639b8bba809ee09';op=json.load(open(opath));table=json.load(open(tpath));assert op['changes']==[]
 for t in table['retains']:assert h.native(old,h.current(old,t['old_native']['object_id']))==t['old_native']
 S=I/'stage483-v1';assert not S.exists();S.mkdir();db=S/'stage.sqlite';shutil.copyfile(source,db);journal=S/'journal';journal.mkdir()
 try:
  args=['node','genealogy2/cli.mjs','apply',str(opath),'--db',str(db),'--journal',str(journal)];r=subprocess.run(args,capture_output=True,text=True);(S/'apply.json').write_text(r.stdout);save(S/'apply.process.json',{'args':args,'exit':r.returncode,'stderr':r.stderr});assert r.returncode==0,r.stderr;c=h.conn(db);assert h.state(c)['journal_head']==483;accepted=dict(c.execute('select *from operation_payload where operation_id=?',(op['id'],)).fetchone());assert json.loads(accepted['request_json'])=={**op,'dependencyReviewVersion':2,'searchMemoryVersion':1};save(S/'accepted-request-normalization-proof.json',{'raw_operation':op,'actual_accepted':accepted,'only_supported_metadata_defaults':True});pending=[dict(x)for x in c.execute('select q.*from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];save(S/'actual-pending-full.json',pending)
  contexts=[]
  for q in pending:
   oldtarget=h.native(c,q['affected_revision_id']);cur=h.native(c,h.current(c,oldtarget['object_id']));bases=[]
   for e in oldtarget['evidence']:
    basis=h.native(c,e['basis_revision_id']);bases.append({'old_edge':e,'old_basis':basis,'current_stronger':h.native(c,h.current(c,basis['object_id']))})
   contexts.append({'request':q,'old_target':oldtarget,'current_target':cur,'changed_basis':h.native(c,q['changed_revision_id']),'all_basis_and_stronger':bases})
  save(S/'actual-pending-full-contexts.json',contexts)
  for t in table['retains']:assert h.native(c,h.current(c,t['old_native']['object_id']))==t['old_native']
  actual=[dict(x)for x in c.execute('select *from review_resolution where operation_id=? order by rowid',(op['id'],))];assert [{'request':x['request_id'],'rationale':x['rationale']}for x in actual]==op['resolve'];save(S/'42-native-resolution-and-retains-proof.json',{'ordered_resolutions':actual,'full_retains':table['retains'],'changes_empty':True});assert sha(source)==pin['sha256']and sha(MAIN)==b['main']['sha256'];save(S/'actual-all50.json',h.all50(c));save(S/'result.json',{'state':h.state(c),'source482_unchanged':True,'main481_unchanged':True,'all42retains_exact':True,'all42resolution_order_exact':True,'elapsed_seconds':time.monotonic()-start});print(json.dumps(h.state(c)))
 except Exception as e:save(S/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.monotonic()-start});raise
if __name__=='__main__':main()
