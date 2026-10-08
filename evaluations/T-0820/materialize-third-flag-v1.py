import pathlib,json,copy,hashlib,importlib.util
R=pathlib.Path.cwd();I=R/'evaluations/T-0820/implementation';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):p=I/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
f=R/'evaluations/T-0820/final-missed-preservation-flag-source-amendment-v1.json';assert sha(f)=='29cc45e97d969b448cdd5743d53f7ee6f14bb560988cb823e99573a262764dc1';s=json.load(open(f));hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';sp=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);stage=I/'stage490-sequence-v1/stage.sqlite';assert sha(stage)=='e313bd94ea6a45931705bd2790f70ba05870593c3ce061c4a4989f7fbbbe32f7';c=h.conn(stage);n=h.native(c,h.current(c,s['target']));assert n==s['full_old_native']and n['version']==2;a=h.api(n);a['expectedVersion']=2
for f in s['field_changes']:
 pp=f['field'].split('.');par=a
 for k in pp[:-1]:par=par[k]
 old=f['old'];new=f['new']
 if pp[-1].endswith('_json'):
  if isinstance(old,str):old=json.loads(old)
  if isinstance(new,str):new=json.loads(new)
 assert par[pp[-1]]==old;par[pp[-1]]=copy.deepcopy(new)
for e in s['evidence_appends']:
 ob,v=e['basis_revision_id'].rsplit('@',1);a['evidence'].append({'object':ob,'version':int(v),'role':e['role'],'note':e['note']})
tup=[(e['object'],e['version'],e['role'])for e in a['evidence']];assert len(tup)==len(set(tup));cols=[dict(r)for r in c.execute('pragma table_info(fact)')];allowed=[r['name']for r in cols if r['name']!='revision_id'];required=[r['name']for r in cols if r['name']!='revision_id'and r['notnull']and r['dflt_value']is None];assert set(a['data'])<=set(allowed)and all(a['data'].get(k)is not None for k in required)
for e in a['evidence']:assert h.native(c,h.current(c,e['object']))['version']==e['version']
op={'id':'T-0820/exact-final-preservation-flag-qualification-v1','actor':'Codex / settled Astra decisions','reason':'T-0820 AC3: exact SOURCE-approved final preservation flag qualification; no new source or other gap removal. Root alone applies canonical after hash-bound approval.','dependencyReviewVersion':2,'changes':[a]};save('third-flag-operation-v1.json',op)
prev=json.load(open(I/'repair20-consequence-table-v1.json'))['final_retains_amendment']['final560_full_retains'];removed=[x for x in prev if x['object_id']==s['target']];assert len(removed)==1;ret=[x for x in prev if x['object_id']!=s['target']];assert len(ret)==559;save('third-flag-consequence-table-v1.json',{'operation_sha256':sha(I/'third-flag-operation-v1.json'),'old_native':n,'new_api':a,'source_disposition':s,'prior560_step_retains_preserved':True,'removed_exact1':removed,'final559_full_retains':ret,'final37_native_changes':True});save('third-flag-preflight-v1.json',{'exact_old_native_fields':True,'required_allowed_schema':{'required':required,'allowed':allowed},'unique_evidence_tuples':True,'current_bindings_exact':True});print(json.dumps({'op':sha(I/'third-flag-operation-v1.json'),'table':sha(I/'third-flag-consequence-table-v1.json')}))
