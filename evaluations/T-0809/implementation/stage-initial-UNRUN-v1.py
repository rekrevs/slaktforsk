import json,hashlib,shutil,subprocess,importlib.util,time,traceback
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0809';I=D/'implementation';MAIN=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 start=time.monotonic();b=json.load(open(D/'preparation/baseline-state-v1.json'));assert sha(MAIN)==b['main']['sha256'];basepath=R/b['backup']['path'];assert sha(basepath)==b['backup']['sha256'];base=h.conn(basepath);assert h.state(base)=={'journal_head':471,'pending':0};opfile=I/'operation-v1.json';ctfile=I/'consequence-table-v1.json';assert sha(opfile)=='4fd117ec3cafd9651ce27acb3c53d3df7c2eee32e189046a2e40a16ac5505f7a';assert sha(ctfile)=='235928c258b46332f07a2da1c31bf4f49cf3b864eba427fc5ea46e7bf98ab69c';op=json.load(open(opfile));ct=json.load(open(ctfile));assert ct['operation_sha256']==sha(opfile)
 for t in ct['changes']:
  if t['old_native']:assert h.native(base,h.current(base,t['object_id']))==t['old_native']
 S=I/'stage472-v1';assert not S.exists();S.mkdir();db=S/'stage.sqlite';shutil.copyfile(basepath,db);journal=S/'journal';journal.mkdir();save(S/'baseline-all50.json',h.all50(base))
 try:
  args=['node','genealogy2/cli.mjs','apply',str(opfile),'--db',str(db),'--journal',str(journal)];r=subprocess.run(args,cwd=R,capture_output=True,text=True);(S/'apply.json').write_text(r.stdout);save(S/'apply-process.json',{'args':args,'exit':r.returncode,'stderr':r.stderr});assert r.returncode==0,r.stderr;c=h.conn(db);state=h.state(c);assert state['journal_head']==472
  accepted=dict(c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone());expected={**op,'dependencyReviewVersion':2,'searchMemoryVersion':1};assert json.loads(accepted['request_json'])==expected;save(S/'accepted-request-normalization-proof.json',{'raw_operation':op,'accepted_request':json.loads(accepted['request_json']),'only_added_metadata':{'dependencyReviewVersion':2,'searchMemoryVersion':1},'all_other_fields_exact':True})
  pending=[dict(x)for x in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];save(S/'actual-pending-full.json',pending);contexts=[]
  for q in pending:
   rid=q.get('target_revision_id') or q.get('target_revision');contexts.append({'request':q,'all_row_fields_preserved':True,'target_native':h.native(c,rid) if rid else None})
  save(S/'actual-pending-contexts-initial.json',contexts);proof=[]
  for x in op['changes']:
   n=h.native(c,h.current(c,x['id']));actual=h.api(n);assert actual==h.expected_defaults(x,actual),x['id'];proof.append({'object_id':x['id'],'actual_native':n,'literal_api_exact':True})
  for t in ct['retains']:assert h.native(c,t['revision_id'])==t['old_native'];assert h.current(c,t['old_native']['object_id'])==t['revision_id']
  save(S/'literal-native-and-retains-proof.json',{'changes':proof,'retains_exact':len(ct['retains'])});save(S/'actual-all50.json',h.all50(c));assert sha(MAIN)==b['main']['sha256'];save(S/'initial-result.json',{'state':state,'literal83_exact':True,'retains200_exact':True,'main_unchanged':True,'elapsed_seconds':time.monotonic()-start});print(json.dumps(state))
 except Exception as e:save(S/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.monotonic()-start});raise
if __name__=='__main__':main()
