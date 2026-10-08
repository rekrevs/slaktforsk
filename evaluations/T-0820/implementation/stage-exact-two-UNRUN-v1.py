import pathlib,json,hashlib,shutil,subprocess,importlib.util,time
R=pathlib.Path.cwd();I=R/'evaluations/T-0820/implementation';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();MAIN=R/'genealogy2/data/research.sqlite';BASESHA='c0bfefbfe1a734cf216514d478c1f74c77a4f05237ae78a04e00b45517295c76';assert sha(MAIN)==BASESHA
hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';assert sha(hp)=='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2';sp=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
def save(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
S=I/'stage490-sequence-v1';assert not S.exists();S.mkdir();db=S/'stage.sqlite';shutil.copyfile(MAIN,db);journal=S/'journal';journal.mkdir();base=h.conn(MAIN);assert h.state(base)=={'journal_head':488,'pending':0};save(S/'baseline-all50.json',h.all50(base));start=time.monotonic()
try:
 for step,(name,pin)in enumerate([('operation-v1.json', '2f43fb2d179d855f8e239098eb19231f791e6ec0b43930ccf8b1edf045d88870'), ('repair20-operation-v1.json', '1f3f8fb5f15017e8debf325d418fd2b3e94d4a6921eb2ba9ffbd7d0cadc1a66a')],1):
  p=I/name;assert sha(p)==pin;op=json.load(open(p));r=subprocess.run(['node','genealogy2/cli.mjs','apply',str(p),'--db',str(db),'--journal',str(journal)],capture_output=True,text=True);(S/f'step{step}-apply.json').write_text(r.stdout);save(S/f'step{step}-process.json',{'exit':r.returncode,'stderr':r.stderr});assert r.returncode==0,r.stderr;c=h.conn(db);pending=[dict(x)for x in c.execute('select q.*from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];save(S/f'step{step}-pending.json',pending);contexts=[]
  for q in pending:
   n=h.native(c,q['affected_revision_id']);contexts.append({'request':q,'old_target_native':n,'current_target_native':h.native(c,h.current(c,n['object_id'])),'changed_basis_native':h.native(c,q['changed_revision_id']),'all_old_basis_current_stronger':[{'edge':e,'old_basis':h.native(c,e['basis_revision_id']),'current_stronger':h.native(c,h.current(c,h.native(c,e['basis_revision_id'])['object_id']))}for e in n['evidence']]})
  save(S/f'step{step}-pending-contexts.json',contexts);accepted=json.loads(c.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone()[0]);assert accepted=={**op,'dependencyReviewVersion':2,'searchMemoryVersion':1};save(S/f'step{step}-request-normalization.json',{'accepted_request':accepted,'only_supported_marker_defaults':True})
  for a in op['changes']:
   actual=h.api(h.native(c,h.current(c,a['id'])));assert actual==h.expected_defaults(a,actual),a['id']
  if step==1:
   expected=json.load(open(I/'repair20-operation-v1.json'));assert [q['id']for q in pending]==[x['request']for x in expected['resolve']]
  c.close()
 c=h.conn(db);save(S/'actual-all50.json',h.all50(c));save(S/'sequence-result.json',{'state':h.state(c),'MAIN_unchanged':sha(MAIN)==BASESHA,'elapsed_seconds':time.monotonic()-start,'unexpected_final_pending_requires_SOURCE':h.state(c)['pending']!=0});assert sha(MAIN)==BASESHA;print(json.dumps(h.state(c)))
except Exception as e:
 save(S/'failure-preserved.json',{'error':str(e),'elapsed_seconds':time.monotonic()-start});raise
