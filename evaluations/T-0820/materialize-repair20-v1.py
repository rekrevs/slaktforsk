import pathlib,json,copy,hashlib,importlib.util
R=pathlib.Path.cwd();I=R/'evaluations/T-0820/implementation';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):
 p=I/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
spec=R/'evaluations/T-0820/settled-actual20-repair-and-resolution-source-design-v1.json';assert sha(spec)=='65ce9e26bd4d9c61971766abbd57354abb0c0d9eb58d224c216b6efd1cf405df';s=json.loads(spec.read_text());hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';sp=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(I/'stage489-v1/stage.sqlite');assert h.state(c)=={'journal_head':489,'pending':20};pending=[dict(r)for r in c.execute('select q.*from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];assert pending==[x['request']for x in s['individual_requests']];apis=[];schema=[]
for x in s['changes_in_required_order']:
 n=h.native(c,h.current(c,x['object_id']));assert n==x['full_old_native']and n['version']==x['expected_version'];a=h.api(n);a['expectedVersion']=n['version']
 for f in x['field_changes']:
  pp=f['field'].split('.');par=a
  for k in pp[:-1]:par=par[k]
  old=f['old'];new=f['new']
  if pp[-1].endswith('_json'):
   if isinstance(old,str):old=json.loads(old)
   if isinstance(new,str):new=json.loads(new)
  assert par[pp[-1]]==old;par[pp[-1]]=copy.deepcopy(new)
 for rr in x['evidence_rebinds']:
  j=rr['index'];assert n['evidence'][j]==rr['old_edge'];ob,v=rr['new_basis_revision_id'].rsplit('@',1);a['evidence'][j]['object']=ob;a['evidence'][j]['version']=int(v)
 e=x['evidence_append'];ob,v=e['basis_revision_id'].rsplit('@',1);a['evidence'].append({'object':ob,'version':int(v),'role':e['role'],'note':e['note']});tuples=[(e['object'],e['version'],e['role'])for e in a['evidence']];assert len(tuples)==len(set(tuples));cols=[dict(r)for r in c.execute('pragma table_info('+a['kind']+')')];allowed=[r['name']for r in cols if r['name']!='revision_id'];required=[r['name']for r in cols if r['name']!='revision_id'and r['notnull']and r['dflt_value']is None];assert set(a['data'])<=set(allowed)and all(a['data'].get(k)is not None for k in required);schema.append({'object':a['id'],'required':required,'allowed':allowed,'tuple_uniqueness':True});apis.append(a)
for n in s['full_native_retains']:assert h.native(c,h.current(c,n['object_id']))==n
proj=dict(c.execute('select object_id,max(version)from revision group by object_id'));proj.update({a['id']:a['expectedVersion']+1 for a in apis});assert all(e['version']==proj[e['object']]for a in apis for e in a['evidence'])
op={'id':'T-0820/two-exact-scope-repairs-and20-individual-resolutions-v1','actor':'Codex / settled Astra decisions','reason':s['reason_for_second_operation'],'dependencyReviewVersion':2,'changes':apis,'resolve':[x['native_resolution']for x in s['individual_requests']]};save('repair20-operation-v1.json',op)
initial=json.load(open(I/'consequence-table-v1.json'));removed=[x for x in initial['retains']if x['object_id']in {a['id']for a in apis}];assert len(removed)==2;remaining=[x for x in initial['retains']if x not in removed];assert len(remaining)==560
save('repair20-consequence-table-v1.json',{'operation_sha256':sha(I/'repair20-operation-v1.json'),'source_spec':{'path':str(spec.relative_to(R)),'sha256':sha(spec)},'changes':[{'old_native':x['full_old_native'],'new_api':a,'source_disposition':x}for x,a in zip(s['changes_in_required_order'],apis)],'individual_request_consequences':[{'source_disposition':x,'exact_native_resolution':r}for x,r in zip(s['individual_requests'],op['resolve'])],'full_native_dependency_retains':s['full_native_retains'],'initial_step_retains':562,'final_retains_amendment':{'removed_exact2':removed,'final560_full_retains':remaining}});save('repair20-preflight-v1.json',{'actual_pending_bijection20':True,'schemas':schema,'exact_old_fields':True,'projected_bindings_exact':True,'native_resolutions_only_request_rationale':all(set(x)=={'request','rationale'}for x in op['resolve'])});print(json.dumps({'operation':sha(I/'repair20-operation-v1.json'),'table':sha(I/'repair20-consequence-table-v1.json')}))
