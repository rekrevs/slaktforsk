import pathlib,json,hashlib,shutil,subprocess,importlib.util,time,traceback
R=pathlib.Path.cwd();D=R/'evaluations/T-0818';I=D/'implementation';MAIN=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';assert sha(hp)=='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2';sp=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def save(p,v):assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def contexts(c,qs):
 out=[]
 for q in qs:
  old=h.native(c,q['affected_revision_id']);basis=[]
  for e in old['evidence']:
   n=h.native(c,e['basis_revision_id']);basis.append({'old_edge':e,'old_basis':n,'current_stronger_basis':h.native(c,h.current(c,n['object_id']))})
  out.append({'request':q,'old_target_native':old,'current_target_native':h.native(c,h.current(c,old['object_id'])),'changed_basis_native':h.native(c,q['changed_revision_id']),'all_old_target_basis_and_current_stronger':basis})
 return out
def pending(c):return [dict(r)for r in c.execute('select q.*from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')]
def main():
 start=time.monotonic();b=json.load(open(D/'preparation/baseline-v1.json'));basepath=D/'preparation/baseline486.sqlite';assert sha(MAIN)==sha(basepath)==b['main']['sha256'];base=h.conn(basepath);assert h.state(base)=={'journal_head':486,'pending':0};files=[I/'operation-v1.json',I/'57-resolution-operation-v1.json'];hashes=['2fca0ae8c038944f92bac4ba459de131a317eeb247ae3a2c2f8c5feceb17d3b5','f01a3837c064851c4d5155d31a6e51bb0164f2ef5ade0e634a86a36af04bb1ca'];tables=[I/'consequence-table-v1.json',I/'57-resolution-consequence-table-v1.json'];thashes=['2f714368b2ced59cf6d5f7880b5ec21bdfac9278229d4ca08b716a89aee4fe12','ad8b97fd3ecefc5a4292b9acb37a9e2e9f3d91d0d657020f0e99d5fca439ed3b']
 for p,v in zip(files,hashes):assert sha(p)==v
 for p,v in zip(tables,thashes):assert sha(p)==v
 ops=[json.load(open(p))for p in files];ct,rt=[json.load(open(p))for p in tables];assert ops[1]['changes']==[];assert ops[0]['media']==[json.load(open(D/'originals/staged-media-v1.json'))]
 for m in ops[0]['media']:assert sha(R/m['storagePath'])==m['sha256']
 S=I/'stage488-sequence-v1';assert not S.exists();S.mkdir();db=S/'stage.sqlite';shutil.copyfile(basepath,db);journal=S/'journal';journal.mkdir();save(S/'baseline-all50.json',h.all50(base))
 try:
  for j,(file,op)in enumerate(zip(files,ops),1):
   args=['node','genealogy2/cli.mjs','apply',str(file),'--db',str(db),'--journal',str(journal)];r=subprocess.run(args,cwd=R,capture_output=True,text=True);(S/f'apply-{j}.json').write_text(r.stdout);save(S/f'apply-{j}.process.json',{'args':args,'exit':r.returncode,'stderr':r.stderr});assert r.returncode==0,r.stderr;c=h.conn(db);assert h.state(c)['journal_head']==486+j;qs=pending(c);save(S/f'actual-pending-step-{j}.json',qs);save(S/f'actual-pending-contexts-step-{j}.json',contexts(c,qs));row=dict(c.execute('select *from operation_payload where operation_id=?',(op['id'],)).fetchone());assert json.loads(row['request_json'])=={**op,'dependencyReviewVersion':2,'searchMemoryVersion':1};save(S/f'accepted-request-normalization-step-{j}.json',{'raw_operation':op,'actual_operation_payload':row,'only_supported_policy_defaults':True})
   if j==1:
    assert [q['id']for q in qs]==[x['request']for x in ops[1]['resolve']]
    for a in ops[0]['changes']:
     n=h.native(c,h.current(c,a['id']));actual=h.api(n);assert actual==h.expected_defaults(a,actual),a['id']
    for t in ct['retains']:assert h.native(c,h.current(c,t['old_native']['object_id']))==t['old_native']
    for t in rt['retains']:assert h.native(c,h.current(c,t['old_native']['object_id']))==t['old_native']
  # No synthetic resolution or pendingzero assumption; return actual newly emitted requests.
  rows=[dict(r)for r in c.execute('select *from review_resolution where operation_id=? order by rowid',(ops[1]['id'],))];assert [{'request':x['request_id'],'rationale':x['rationale']}for x in rows]==ops[1]['resolve'];proof=[]
  for a in ops[0]['changes']:
   n=h.native(c,h.current(c,a['id']));actual=h.api(n);assert actual==h.expected_defaults(a,actual),a['id'];proof.append({'object':a['id'],'full_native':n,'API_exact':True})
  for t in ct['retains']+rt['retains']:assert h.native(c,h.current(c,t['old_native']['object_id']))==t['old_native']
  save(S/'literal-native-and-resolution-retains-proof.json',{'native32':proof,'retains652_exact':True,'resolution41_unique_targets_exact':True,'ordered57_resolutions':rows});save(S/'actual-all50.json',h.all50(c));assert sha(MAIN)==sha(basepath)==b['main']['sha256'];save(S/'result.json',{'state':h.state(c),'actual_new_pending':len(pending(c)),'native32_exact':True,'retains652_plus41_step_retains_exact':True,'resolution57_order_exact':True,'main486_unchanged':True,'baseline486_unchanged':True,'elapsed_seconds':time.monotonic()-start});print(json.dumps(h.state(c)))
 except Exception as e:save(S/'failure-preserved.json',{'error':str(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.monotonic()-start});raise
if __name__=='__main__':main()
