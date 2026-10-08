import json,copy,hashlib,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0814';I=D/'implementation';start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(Path(p).read_text());save=lambda n,v:(I/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(D/'preparation/baseline481.sqlite');assert h.state(c)=={'journal_head':481,'pending':0};assert sha(R/'genealogy2/data/research.sqlite')=='35d15336c750f760780af64e6e5b41a1a0a19f07a9c0451c52cff355ae928602';designp=D/'primary-complete-source-spec-v2.json';assert sha(designp)=='457318d174d7ceff44b31cfaa963dcce010dcc3d50f2d5f66ac8e97ec096ef9c';design=load(designp);specs=[]
for pin in design['components']:assert sha(R/pin['path'])==pin['sha256'];specs.append(load(R/pin['path']))
changes,reviews,task=specs;apis={};olds={};fields={};appends={};issues=[];rebinds=[];note=changes['support_rule'].split('note: ',1)[1].split(' Preserve existing',1)[0]
for x in changes['changes']:
 oid=x['object_id'];n=h.native(c,h.current(c,oid));assert n['version']==x['expected_version'],('version',oid);api=h.api(n);api['expectedVersion']=n['version'];apis[oid]=api;olds[oid]=n;fields[oid]=[];appends[oid]=[]
 for f in x['fields']:
  parts=f['field'].split('.');parent=api
  for key in parts[:-1]:parent=parent[key]
  key=parts[-1];old,new=f['old'],f['new']
  if key.endswith('_json'):
   if isinstance(old,str):old=json.loads(old)
   if isinstance(new,str):new=json.loads(new)
  assert parent[key]==old,('literal oldfield mismatch',oid,f['field']);parent[key]=copy.deepcopy(new);fields[oid].append(f)
 for rid in x['supports']:
  obj,v=rid.rsplit('@',1);edge={'object':obj,'version':int(v),'role':'supports','note':note};tu=(obj,int(v),'supports')
  if any((e['object'],e['version'],e['role'])==tu for e in api['evidence']):issues.append({'type':'explicit_support_existing_tuple','target':oid,'new_edge':edge,'old_evidence':n['evidence'],'requires_individual_source_disposition':True})
  else:api['evidence'].append(edge);appends[oid].append(edge)
for rr in changes['explicit_rebinds']:
 a=apis[rr['object_id']];j=rr['index'];e=a['evidence'][j];assert e['object']+'@'+str(e['version'])==rr['old_basis'] and e['role']==rr['role'];obj,v=rr['new_basis'].rsplit('@',1);a['evidence'][j]={**e,'object':obj,'version':int(v)};rebinds.append({'source_decision':rr,'old_edge':e,'new_edge':a['evidence'][j]})
amendp=D/'primary-two-READ-rebind-amendment-v1.json';assert sha(amendp)=='f23745247c00266401068c979468409ba59cd1e3868d2f7aade9e972cf0636a0';gatep=D/'independent-two-READ-rebind-source-gate-v1.json';assert sha(gatep)=='1b9387604dc69074d79b58546f93d4ca2a14f134d30b6eda126ecac46fb28826';amend=load(amendp)
for rr in amend['individual_decisions']:
 a=apis[rr['object_id']];j=rr['index'];assert a['expectedVersion']==rr['expected_version'];assert a['evidence'][j]==rr['old_edge'];a['evidence'][j]=copy.deepcopy(rr['new_edge']);rebinds.append({'source_amendment':{'path':str(amendp.relative_to(R)),'sha256':sha(amendp)},**rr})
for x in reviews['new_reviews']:
 oid=x['id'];assert not c.execute('SELECT 1 FROM object WHERE id=?',(oid,)).fetchone();apis[oid]=copy.deepcopy(x);assert x['expectedVersion'] is None;olds[oid]=None;fields[oid]=[];appends[oid]=[]
heads=dict(c.execute('SELECT object_id,max(version) FROM revision GROUP BY object_id'));proj={**heads,**{oid:(a['expectedVersion'] or 0)+1 for oid,a in apis.items()}};checks=[]
for oid,a in apis.items():
 tuples=[(e['object'],e['version'],e['role'])for e in a['evidence']];assert len(tuples)==len(set(tuples)),('evidence tuple',oid)
 cols=[dict(r)for r in c.execute('PRAGMA table_info('+a['kind']+')')];required=[r['name']for r in cols if r['name']!='revision_id' and r['notnull'] and r['dflt_value']is None];allowed=[r['name']for r in cols if r['name']!='revision_id'];missing=[k for k in required if a['data'].get(k)is None];extra=[k for k in a['data'] if k not in allowed];checks.append({'object':oid,'required':required,'allowed':allowed,'missing':missing,'unexpected':extra});assert not missing and not extra,('schema',oid,missing,extra)
 for j,e in enumerate(a['evidence']):
  assert e['object'] in heads or e['object'] in apis,('missing reference',oid,e)
  if e['version']!=proj[e['object']]:issues.append({'type':'stale_or_projected_basis','target':oid,'index':j,'edge':e,'current_version':heads.get(e['object']),'projected_version':proj[e['object']],'origin':'preserved old edge' if olds[oid]and j<len(olds[oid]['evidence']) else'new edge','requires_individual_source_disposition':True})
left=list(apis);ordered=[]
while left:
 ready=[oid for oid in left if not any(e['object']in left and e['version']==proj[e['object']]for e in apis[oid]['evidence'])];assert ready,('cycle',left)
 for oid in ready:ordered.append(oid);left.remove(oid)
allretains={}
for person in ['P-0336','P-0337']:
 for n in load(D/'preparation/native'/ (person+'.json'))['current']:
  if n['object_id']not in apis:allretains[n['object_id']]=h.native(c,n['id'])
parentreasons={x['id']:x for x in reviews['individual_parent_retains']};retains=[{'revision_id':n['id'],'old_native':n,'disposition':'RETAIN_EXACT','reason':parentreasons.get(n['id'],{}).get('reason',reviews['metadata_rule'])}for n in allretains.values()]
pf={'source_design':{'path':str(designp.relative_to(R)),'sha256':sha(designp)},'native_changes':len(apis),'current_corrections':16,'new_reviews':4,'fullnative_retains':len(retains),'explicit_rebinds':rebinds,'schema_checks':checks,'unique_evidence_tuples_pass':True,'issues':issues,'ordered_object_ids':ordered,'no_native_write':True,'elapsed_seconds':time.monotonic()-start};save('preflight-v2.json',pf)
if issues:
 save('provisional-exact-APIs-for-source-questions-v1.json',{'apis':[apis[o]for o in ordered],'issues':issues,'qualification':'No canonical-ready operation sealed; exact individual source decisions required.'});print(json.dumps({'preflight_issues':len(issues),'types':{t:sum(i['type']==t for i in issues)for t in {i['type']for i in issues}}}));raise SystemExit(0)
op={'id':'T-0814/accepted-material-identity-and-current-copy-v1','actor':'Codex / settled Astra decisions','reason':'T-0814 AC1–6: bounded accepted-material identity assessment and exact current-copy qualifications; no original access or LIFE assessment. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':[apis[o]for o in ordered]};save('operation-v1.json',op);save('consequence-table-v1.json',{'operation_sha256':sha(I/'operation-v1.json'),'source_design':pf['source_design'],'source_components':design['components'],'explicit_source_amendment':{'path':str(amendp.relative_to(R)),'sha256':sha(amendp)},'changes':[{'object_id':o,'old_native':olds[o],'new_api':apis[o],'literal_fields':fields[o],'explicit_support_appends':appends[o],'disposition':'REVISE_LITERAL'if olds[o]else'NEW_NATIVE_REVIEW'}for o in ordered],'retains':retains,'explicit_rebinds':rebinds,'individual_parent_retains':reviews['individual_parent_retains'],'remaining_owner_proposal':task});print(json.dumps({'operation':sha(I/'operation-v1.json'),'table':sha(I/'consequence-table-v1.json'),'retains':len(retains)}))
