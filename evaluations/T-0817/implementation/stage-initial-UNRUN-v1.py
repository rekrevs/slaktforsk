import json,hashlib,shutil,subprocess,importlib.util,time,traceback
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0817';I=D/'implementation';MAIN=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 start=time.monotonic();b=json.load(open(D/'preparation/baseline-v1.json'));assert sha(MAIN)==b['main']['sha256'];basepath=D/'preparation/baseline484.sqlite';assert sha(basepath)=='f73c9599c70b2938b581593c1250995122d79bfa4451e72be1e040cc6c339d0e';base=h.conn(basepath);assert h.state(base)=={'journal_head':484,'pending':0};opfile=I/'operation-v1.json';ctfile=I/'consequence-table-v1.json';assert sha(opfile)=='c80ee20bb555cf145a94e9fa8266f68956913daf4f0a1fb1954dc68554307961';assert sha(ctfile)=='9322aef09ec9cea3f290802449df1652dd2b03749854ed28497efed05e6c7a80';op=json.load(open(opfile));ct=json.load(open(ctfile));assert ct['operation_sha256']==sha(opfile)
 for t in ct['changes']:
  if t['old_native']:assert h.native(base,h.current(base,t['object_id']))==t['old_native']
 S=I/'stage485-v1';assert not S.exists();S.mkdir();db=S/'stage.sqlite';shutil.copyfile(basepath,db);journal=S/'journal';journal.mkdir();save(S/'baseline-all50.json',h.all50(base))
 try:
  args=['node','genealogy2/cli.mjs','apply',str(opfile),'--db',str(db),'--journal',str(journal)];r=subprocess.run(args,cwd=R,capture_output=True,text=True);(S/'apply.json').write_text(r.stdout);save(S/'apply-process.json',{'args':args,'exit':r.returncode,'stderr':r.stderr});assert r.returncode==0,r.stderr;c=h.conn(db);state=h.state(c);assert state['journal_head']==485
  accepted=dict(c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone());expected={**op,'dependencyReviewVersion':2,'searchMemoryVersion':1};assert json.loads(accepted['request_json'])==expected;save(S/'accepted-request-normalization-proof.json',{'raw_operation':op,'accepted_request':json.loads(accepted['request_json']),'only_added_metadata':{'dependencyReviewVersion':2,'searchMemoryVersion':1},'all_other_fields_exact':True})
  pending=[dict(x)for x in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];save(S/'actual-pending-full.json',pending);contexts=[]
  for q in pending:
   rid=q['affected_revision_id'];old=h.native(c,rid);cur=h.native(c,h.current(c,old['object_id']));bases=[]
   for edge in old['evidence']:
    basis=h.native(c,edge['basis_revision_id']);strong=h.native(c,h.current(c,basis['object_id']));bases.append({'edge':edge,'old_basis':basis,'current_stronger_basis':strong})
   changed=h.native(c,q['changed_revision_id']);contexts.append({'request':q,'old_target_native':old,'current_target_native':cur,'changed_basis_native':changed,'all_old_target_basis_and_current_stronger':bases})
  save(S/'actual-pending-contexts-initial.json',contexts);proof=[]
  for x in op['changes']:
   n=h.native(c,h.current(c,x['id']));actual=h.api(n);assert actual==h.expected_defaults(x,actual),x['id'];proof.append({'object_id':x['id'],'actual_native':n,'literal_api_exact':True})
  for t in ct['retains']:assert h.native(c,t['revision_id'])==t['old_native'];assert h.current(c,t['old_native']['object_id'])==t['revision_id']
  save(S/'literal-native-and-retains-proof.json',{'changes':proof,'retains_exact':len(ct['retains'])});save(S/'actual-all50.json',h.all50(c));assert sha(MAIN)==b['main']['sha256'];save(S/'initial-result.json',{'state':state,'literal47_exact':True,'retains483_exact':True,'main_unchanged':True,'elapsed_seconds':time.monotonic()-start});print(json.dumps(state))
 except Exception as e:save(S/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.monotonic()-start});raise
if __name__=='__main__':main()
