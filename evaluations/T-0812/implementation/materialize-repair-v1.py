import json,copy,hashlib,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0812';I=D/'implementation';start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(I/'stage478-v1/stage.sqlite');assert h.state(c)=={'journal_head':478,'pending':134};sf=D/'primary-actual134-repair-and-resolution-spec-v1.json';assert sha(sf)=='02b84b4385e1b9b1da53136ddcccd220cc52fe7149e26a53fc3a9d95d4a53b21';spec=json.load(open(sf));pending=[dict(x)for x in c.execute('select q.*from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null order by q.rowid')];assert [x['id']for x in pending]==[x['request']for x in spec['resolve']];apis={};olds={};rebinds=[];checks=[]
for x in spec['changes']:
 oid=x['id'];assert oid not in apis;n=h.native(c,h.current(c,oid));assert n['version']==x['expectedVersion'];a=h.api(n);a['expectedVersion']=n['version'];olds[oid]=n
 for f in x['fields']:
  path=f['field'].split('.');parent=a
  if len(path)==1 and path[0]not in a:parent=a['data']
  else:
   for k in path[:-1]:parent=parent[k]
  key=path[-1];old=json.loads(f['old'])if key.endswith('_json')and isinstance(f['old'],str)else f['old'];new=json.loads(f['new'])if key.endswith('_json')and isinstance(f['new'],str)else f['new'];assert parent[key]==old,('oldfield',oid,f['field']);parent[key]=copy.deepcopy(new)
 for rr in x['support_rebinds']:
  j=rr['index'];edge=a['evidence'][j];assert edge['object']+'@'+str(edge['version'])==rr['old'];assert edge['role']==rr['role']and edge['note']==rr['note'];obj,v=rr['new'].rsplit('@',1);edge['object']=obj;edge['version']=int(v);rebinds.append({'target':oid,**rr})
 for e in x['appendEvidence']:assert e not in a['evidence'];a['evidence'].append(copy.deepcopy(e))
 tuples=[(e['object'],e['version'],e['role'])for e in a['evidence']];assert len(tuples)==len(set(tuples)),('duplicate native tuple',oid)
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
decisions=spec['resolve'];assert [x['request']for x in decisions]==[x['id']for x in pending];contexts=json.load(open(I/'stage478-v1/actual-pending-contexts-initial.json'));requesttable=[]
for q,decision,resolution,context in zip(pending,decisions,spec['resolve'],contexts):
 assert q['affected_revision_id']==decision['affected_revision']and q['changed_revision_id']==decision['changed_revision'];assert context['request']==q;requesttable.append({'actual_full_context':context,'source_disposition':decision,'exact_native_resolution':resolution})
retains=[]
for x in spec['retains']:
 n=h.native(c,x['revision']);assert n['object_id']not in apis and h.current(c,n['object_id'])==n['id'];retains.append({'revision_id':n['id'],'old_native':n,'source_disposition':x})
for x in spec['resolve']:
 if x['source_disposition']=='REVISE_REQUIRED':assert 'rättelse görs före resolution'in x['rationale']
op={'id':'T-0812/31-current-copy-repairs-and-134-individual-decisions-v1','actor':'Codex / settled Astra decisions','reason':'T-0812 AC1–4: 31 exact current-copy corrections and 134 individualized actual dependency dispositions after accepted source adoption. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':[apis[o]for o in ordered],'resolve':[{'request':x['request'],'rationale':x['rationale']}for x in spec['resolve']]};p=I/'repair-operation-v1.json';assert not p.exists();p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');table={'operation_sha256':sha(p),'source_spec':{'path':str(sf.relative_to(R)),'sha256':sha(sf)},'changes':[{'object_id':o,'old_native':olds[o],'new_api':apis[o],'literal_fields':next(x['fields']for x in spec['changes']if x['id']==o),'source_disposition':'REVISE_EXACT'}for o in ordered],'individual_request_consequences':requesttable,'retains':retains,'explicit_rebinds':rebinds};q=I/'repair-consequence-table-v1.json';assert not q.exists();q.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');pf={'operation_sha256':sha(p),'table_sha256':sha(q),'changes':len(apis),'individual_resolutions':len(requesttable),'individual_retains':len(retains),'schema_checks':checks,'issues':issues,'old_fields_exact':True,'elapsed_seconds':time.monotonic()-start};f=I/'repair-preflight-v1.json';assert not f.exists();f.write_text(json.dumps(pf,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in pf.items()if k!='schema_checks'}))
