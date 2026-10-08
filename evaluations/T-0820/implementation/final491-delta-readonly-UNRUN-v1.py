import pathlib,json,hashlib,importlib.util,subprocess,time
R=pathlib.Path.cwd();I=R/'evaluations/T-0820/implementation';S=I/'stage491-continuation-v1';PREV=I/'stage490-sequence-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';sp=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);assert sha(PREV/'stage.sqlite')=='e313bd94ea6a45931705bd2790f70ba05870593c3ce061c4a4989f7fbbbe32f7';before=h.conn(PREV/'stage.sqlite');c=h.conn(S/'stage.sqlite');assert h.state(c)=={'journal_head':491,'pending':0},'Unexpected new pending: SOURCE own dispositions required; do not resolve'
def save(n,x):p=S/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
op=json.load(open(I/'third-flag-operation-v1.json'));a=op['changes'][0];actual=h.api(h.native(c,h.current(c,a['id'])));assert actual==h.expected_defaults(a,actual);exact=[]
for r in before.execute('select object_id,max(version)from revision group by object_id'):
 if r[0]!=a['id']:assert h.native(before,h.current(before,r[0]))==h.native(c,h.current(c,r[0])),r[0];exact.append(r[0])
ct=json.load(open(I/'third-flag-consequence-table-v1.json'));assert len(ct['final559_full_retains'])==559
for n in ct['final559_full_retains']:assert h.native(c,h.current(c,n['object_id']))==n['old_native']
ops=[json.load(open(I/n))for n in ['operation-v1.json','repair20-operation-v1.json','third-flag-operation-v1.json']];allapi={x['id']:x for o in ops for x in o['changes']};assert len(allapi)==37
for oid,x in allapi.items():
 actual=h.api(h.native(c,h.current(c,oid)));assert actual==h.expected_defaults(x,actual),oid
res=ops[1]['resolve'];stored=[dict(r)for r in c.execute('select *from review_resolution where operation_id=?order by rowid',(ops[1]['id'],))];assert [(r['request_id'],r['rationale'])for r in stored]==[(r['request'],r['rationale'])for r in res]
prefix={}
for name in h.all50(before)['tables']:
 if name in h.DERIVED:continue
 sql=before.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
 if 'WITHOUT ROWID'in sql.upper():assert h.rows(before,name)==h.rows(c,name)
 else:
  m=before.execute('select max(rowid)from "'+name+'"').fetchone()[0];assert h.rows(before,name,True)==(h.rows(c,name,True,m)if m is not None else [])
 prefix[name]=True
captures=[]
for name,args in [('P-0336-person.json',['person','P-0336','--full','--format','json']),('inventory-full.json',['inventory','--full']),('verify.json',['verify']),('verify-assets.json',['verify-assets']),('verify-source.json',['verify-source'])]:
 p=S/name;assert not p.exists();t=time.monotonic();r=subprocess.run(['node','genealogy2/cli.mjs',*args,'--db',str(S/'stage.sqlite')],capture_output=True,text=True);p.write_text(r.stdout);save(name+'.process.json',{'exit':r.returncode,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t});assert r.returncode==0,r.stderr;x=json.loads(r.stdout)
 if name.startswith('verify'):assert x['ok']and not x.get('errors',[])and not x.get('problems',[])
 captures.append({'path':str(p.relative_to(R)),'sha256':sha(p)})
old=json.load(open(PREV/'inventory-full.json'));new=json.load(open(S/'inventory-full.json'));keys=['identityGate','identityReview','treeEffect','lifePictureReview','stopReasons'];am={x['id']:x for x in new['people']};assert len(am)==536
for x in old['people']:
 for k in keys:assert x.get(k)==am[x['id']].get(k),(x['id'],k)
# Native current relations/OWNER/person/review objects all belong to unchanged IDs; sole changed fact is explicit API exact.
reused=[PREV/n for n in ['P-0287-person.json','P-0009-person.json','P-0269-pedigree.json','P-0270-pedigree.json','targeted-review-pedigree-tests.log','final-native-protection-proof-v2.json']]
save('final491-delta-protection-proof-v1.json',{'state':h.state(c),'37native_exact':True,'559retains_exact':True,'20ordered_resolution_rationales_exact':True,'sole_delta_object':a['id'],'all_other_current_fullnative_exact':len(exact),'all536_fullreview_axes_exact_vs490':True,'44native_history_prefixes_vs490_exact':prefix,'all50_final':h.all50(c),'fresh_captures':captures,'reused_readers_peds43_tests18_proofpins':[{'path':str(p.relative_to(R)),'sha256':sha(p)}for p in reused],'reuse_boundaries':'Exact full unchanged current native and all536axes proof preserves OWNER45/allrelations/Johannes/Ada own scopes and accepted path gates; sole changed preservation flag individually approved. No new SOURCE/gate interpretation.'})
