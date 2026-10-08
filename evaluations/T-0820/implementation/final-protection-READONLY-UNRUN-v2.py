import pathlib,json,hashlib,importlib.util
R=pathlib.Path.cwd();I=R/'evaluations/T-0820/implementation';S=I/'stage490-sequence-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';sp=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);MAIN=R/'genealogy2/data/research.sqlite';assert sha(MAIN)=='c0bfefbfe1a734cf216514d478c1f74c77a4f05237ae78a04e00b45517295c76';b=h.conn(MAIN);c=h.conn(S/'stage.sqlite');assert h.state(c)=={'journal_head':490,'pending':0},'Unexpected pending: return SOURCE before final approval'
def save(n,x):p=S/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
ops=[json.load(open(I/n))for n in ['operation-v1.json','repair20-operation-v1.json']];apis={a['id']:a for op in ops for a in op['changes']};assert len(apis)==36
for oid,a in apis.items():
 actual=h.api(h.native(c,h.current(c,oid)));assert actual==h.expected_defaults(a,actual),oid
ct=json.load(open(I/'repair20-consequence-table-v1.json'));ret=ct['final_retains_amendment']['final560_full_retains'];assert len(ret)==560
for n in ret:assert h.native(c,h.current(c,n['object_id']))==n['old_native']
for n in ct['full_native_dependency_retains']:assert h.native(c,h.current(c,n['object_id']))==n
res=ops[1]['resolve'];stored=[dict(x)for x in c.execute('select *from review_resolution where operation_id=? order by rowid',(ops[1]['id'],))];assert [(x['request_id'],x['rationale'])for x in stored]==[(x['request'],x['rationale'])for x in res]
protected=[]
for r in b.execute('select object_id,max(version)from revision group by object_id'):
 if r[0]not in apis:assert h.native(b,h.current(b,r[0]))==h.native(c,h.current(c,r[0])),r[0];protected.append(r[0])
owners=json.load(open(R/'evaluations/T-0819/preparation/current-OWNER45-and-direct-bases-v1.json'))['OWNER45_full_raw_native'];assert len(owners)==45
for n in owners:assert h.native(c,h.current(c,n['object_id']))==n
prefix={}
for name in h.all50(b)['tables']:
 if name in h.DERIVED:continue
 sql=b.execute('select sql from sqlite_master where name=?',(name,)).fetchone()[0]
 if 'WITHOUT ROWID'in sql.upper():assert h.rows(b,name)==h.rows(c,name)
 else:
  limit=b.execute('select max(rowid)from "'+name+'"').fetchone()[0];assert h.rows(b,name,True)==(h.rows(c,name,True,limit)if limit is not None else [])
 prefix[name]=True
assert len(prefix)==44
old=json.load(open(R/'evaluations/T-0818/implementation/stage488-sequence-v1/inventory-full.json'));new=json.load(open(S/'inventory-full.json'));keys=['identityGate','identityReview','treeEffect','lifePictureReview','stopReasons'];am={p['id']:p for p in new['people']};diff=[]
for p in old['people']:
 delta={k:{'before':p.get(k),'after':am[p['id']].get(k)}for k in keys if p.get(k)!=am[p['id']].get(k)}
 if delta:diff.append({'person':p['id'],'exact_differences':delta})
assert len(am)==536;assert {x['person']for x in diff}<={'P-0336'}
for k in ['identityGate','lifePictureReview']:assert next(p for p in old['people']if p['id']=='P-0336').get(k)==am['P-0336'].get(k)
pq=R/'evaluations/T-0820/primary-exact-focal-stopReasons-source-qualification-v1.json';iq=R/'evaluations/T-0820/independent-exact-focal-stopReasons-qualification-v1.json';assert sha(pq)=='8644e2fb3e6f6c13c5e4055050d7fd2936cb0176842e273304b834f85d15743f';assert sha(iq)=='522d37fecb86c7d773e388faaf48ec0c68d4c448c281970c7e842a7d2462d7a5';pd=json.load(open(pq))['approved_exact_focal_differences'];idd=json.load(open(iq))['exact_authorized_focal_before_after'];actual=diff[0]['exact_differences'];assert actual==pd and actual==idd

for pid in ['P-0269','P-0270']:
 oldped=json.load(open(R/f'evaluations/T-0820/root-start-pedigree-{pid.replace("P-","P")}.json'));newped=json.load(open(S/f'{pid}-pedigree.json'));assert oldped['paths']==newped['paths']and oldped['edges']==newped['edges'];assert len(newped['paths'])==43 and not newped['truncated']
for m in ops[0]['media']:
 n=dict(c.execute('select *from native_asset where id=?',(m['id'],)).fetchone());assert sha(R/m['storagePath'])==m['sha256'];save('actual-media-registration-final.json',n)
save('final-native-protection-proof-v2.json',{'state':h.state(c),'literal36_exact':True,'retains560_exact':True,'resolution20_order_rationales_exact':True,'dependency13_retains_exact':True,'all_other_current_native_exact':len(protected),'OWNER45_exact':True,'history44_prefixes_exact':prefix,'all50':h.all50(c),'all536_axes_nonfocal535_exact':True,'focal_exact_differences_for_SOURCE_qualification':diff,'pedigree43_paths_edges_exact':True,'MAIN_unchanged_sha256':sha(MAIN)})
