import json,copy,hashlib,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0810';I=D/'implementation';start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(I/'stage474-v1/stage.sqlite');assert h.state(c)=={'journal_head':474,'pending':59};sf=D/'primary-seven-repairs-and59-resolution-spec-v1.json';assert sha(sf)=='87617c661dc546e7987c142dc60d3907bd734437a710f840e9e9d1cbf614ffff';spec=json.load(open(sf));pending=[dict(x)for x in c.execute('select q.*from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];assert [x['id']for x in pending]==[x['request']for x in spec['resolve']];apis={};olds={};rebinds=[];checks=[]
for x in spec['changes']:
 oid=x['id'];assert oid not in apis;n=h.native(c,h.current(c,oid));assert n['version']==x['expectedVersion'];a=h.api(n);a['expectedVersion']=n['version'];olds[oid]=n
 for f in x['fields']:
  path=f['field'].split('.');parent=a
  if len(path)==1 and path[0]not in a:parent=a['data']
  else:
   for k in path[:-1]:parent=parent[k]
  key=path[-1];old=json.loads(f['old'])if key.endswith('_json')and isinstance(f['old'],str)else f['old'];new=json.loads(f['new'])if key.endswith('_json')and isinstance(f['new'],str)else f['new'];assert parent[key]==old,('oldfield',oid,f['field']);parent[key]=copy.deepcopy(new)
 for rr in x.get('rebindEvidence',[]):
  j=rr['index'];assert n['evidence'][j]==rr['old'];a['evidence'][j]['object']=rr['newObject'];a['evidence'][j]['version']=rr['newVersion'];rebinds.append({'target':oid,**rr})
 for e in x['appendEvidence']:assert e not in a['evidence'];a['evidence'].append(copy.deepcopy(e))
 cols=[dict(z)for z in c.execute('pragma table_info('+a['kind']+')')];allowed=[z['name']for z in cols if z['name']!='revision_id'];required=[z['name']for z in cols if z['name']!='revision_id'and z['notnull']and z['dflt_value']is None];assert all(a['data'].get(k)is not None for k in required);assert set(a['data'])<=set(allowed);checks.append({'id':oid,'required':required,'allowed':allowed,'PASS':True});apis[oid]=a
heads=dict(c.execute('select object_id,max(version)from revision group by object_id'));projected={**heads,**{o:a['expectedVersion']+1 for o,a in apis.items()}};issues=[]
for oid,a in apis.items():
 for j,e in enumerate(a['evidence']):
  assert e['object']in projected
  if e['version']!=projected[e['object']]:issues.append({'target':oid,'index':j,'edge':e,'projected':projected[e['object']]})
left=list(apis);ordered=[]
while left:
 ready=[o for o in left if not any(e['object']in left and e['version']==projected[e['object']]for e in apis[o]['evidence'])];assert ready,('cycle',left)
 for o in ready:ordered.append(o);left.remove(o)
decisions=spec['individualDispositions'];assert [x['request']for x in decisions]==[x['id']for x in pending];contexts=json.load(open(I/'stage474-v1/actual-pending-contexts-initial.json'));requesttable=[]
for q,decision,resolution,context in zip(pending,decisions,spec['resolve'],contexts):
 assert q['affected_revision_id']==decision['affected_revision']and q['changed_revision_id']==decision['changed_revision'];assert context['request']==q;requesttable.append({'actual_full_context':context,'source_disposition':decision,'exact_native_resolution':resolution})
retains=[]
for x in spec['retains']:
 assert x['id']not in apis;n=h.native(c,h.current(c,x['id']));assert n['version']==x['version'];retains.append({'revision_id':n['id'],'old_native':n,'source_disposition':x})
op={'id':'T-0810/seven-current-copy-repairs-and-59-individual-decisions-v1','actor':'Codex / settled Astra decisions','reason':'T-0810 AC1–4: seven exact current-copy corrections and 59 individualized actual dependency dispositions after accepted source adoption. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':[apis[o]for o in ordered],'resolve':spec['resolve']};p=I/'repair-operation-v1.json';assert not p.exists();p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');table={'operation_sha256':sha(p),'source_spec':{'path':str(sf.relative_to(R)),'sha256':sha(sf)},'changes':[{'object_id':o,'old_native':olds[o],'new_api':apis[o],'literal_fields':next(x['fields']for x in spec['changes']if x['id']==o),'source_disposition':'REVISE_EXACT'}for o in ordered],'individual_request_consequences':requesttable,'retains':retains,'explicit_rebinds':rebinds};q=I/'repair-consequence-table-v1.json';assert not q.exists();q.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');pf={'operation_sha256':sha(p),'table_sha256':sha(q),'changes':len(apis),'individual_resolutions':len(requesttable),'individual_retains':len(retains),'schema_checks':checks,'issues':issues,'old_fields_exact':True,'elapsed_seconds':time.monotonic()-start};f=I/'repair-preflight-v1.json';assert not f.exists();f.write_text(json.dumps(pf,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in pf.items()if k!='schema_checks'}))
