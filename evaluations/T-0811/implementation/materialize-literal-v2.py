import pathlib,json,hashlib,copy,time,importlib.util
R=pathlib.Path.cwd();D=R/'evaluations/T-0811';I=D/'implementation';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();start=time.monotonic();s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(D/'preparation/baseline476.sqlite');assert h.state(c)=={'journal_head':476,'pending':0};sf=D/'primary-source-design-v3.json';assert sha(sf)=='545e9776d53164d9228f8fc62402bcc515592d23be79db3240fea4649e457f16';spec=json.load(open(sf));apis={};olds={};fields={};rebinds=[];checks=[]
for x in spec['changes']:
 oid=x['object_id'];assert oid not in apis;n=h.native(c,h.current(c,oid));assert n['version']==x['expectedVersion'];a=h.api(n);a['expectedVersion']=n['version'];olds[oid]=n;fields[oid]=x['fields']
 for f in x['fields']:
  path=f['field'].split('.');path=[{'evidence_status':'evidenceStatus'}.get(z,z)for z in path];parent=a
  for key in path[:-1]:parent=parent[key]
  key=path[-1];old=json.loads(f['old'])if key.endswith('_json')and isinstance(f['old'],str)else f['old'];new=json.loads(f['new'])if key.endswith('_json')and isinstance(f['new'],str)else f['new'];assert parent[key]==old,('zero/fullmatch',oid,f['field']);parent[key]=copy.deepcopy(new)
 for e in x['append_evidence']:assert e not in a['evidence'],('duplicate',oid,e);a['evidence'].append(copy.deepcopy(e))
 for rr in x['indexed_rebinds']:
  j=rr['index'];assert n['evidence'][j]==rr['old'];obj,v=rr['new_basis_revision_id'].rsplit('@',1);a['evidence'][j]['object']=obj;a['evidence'][j]['version']=int(v);rebinds.append({'target':oid,**rr})
 apis[oid]=a
for x in spec['new_objects']:
 oid=x['id'];assert oid not in apis and not c.execute('select 1 from object where id=?',(oid,)).fetchone();a=copy.deepcopy(x);assert a['expectedVersion']==0;a['expectedVersion']=None;apis[oid]=a;olds[oid]=None;fields[oid]=[]
for oid,a in apis.items():
 tuples=[(e['object'],e['version'],e['role'])for e in a['evidence']];assert len(tuples)==len(set(tuples)),('native unique evidence key',oid)
heads=dict(c.execute('select object_id,max(version)from revision group by object_id'));projected={**heads,**{o:(a['expectedVersion']or 0)+1 for o,a in apis.items()}};issues=[]
for oid,a in apis.items():
 cols=[dict(x)for x in c.execute('pragma table_info('+a['kind']+')')];allowed=[x['name']for x in cols if x['name']!='revision_id'];required=[x['name']for x in cols if x['name']!='revision_id'and x['notnull']and x['dflt_value']is None];assert set(a['data'])<=set(allowed)and all(a['data'].get(k)is not None for k in required);checks.append({'id':oid,'allowed':allowed,'required':required,'PASS':True})
 for j,e in enumerate(a['evidence']):
  assert e['object']in projected
  if e['version']!=projected[e['object']]:issues.append({'target':oid,'index':j,'edge':e,'current':heads.get(e['object']),'projected':projected[e['object']]})
left=list(apis);ordered=[]
while left:
 ready=[o for o in left if not any(e['object']in left and e['version']==projected[e['object']]for e in apis[o]['evidence'])];assert ready,('cycle',left)
 for o in ready:ordered.append(o);left.remove(o)
retains=[]
for x in spec['retains']:
 n=h.native(c,x['id']);assert h.current(c,n['object_id'])==n['id']and n['object_id']not in apis;retains.append({'revision_id':n['id'],'old_native':n,'source_disposition':'RETAIN_EXACT','rationale':x['reason']})
relations=[]
for x in spec['relations']:
 n=h.native(c,x['id']);assert h.current(c,n['object_id'])==n['id']and n['evidence']==x['exact_evidence'];relations.append({'full_native':n,'source_disposition':x})
op={'id':'T-0811/accepted-material-identity-current-copy-v1','actor':'Codex / settled Astra decisions','reason':'T-0811 AC1–4: individual accepted-material identity assessment and exact bounded current-copy qualifications. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':[apis[o]for o in ordered]};p=I/'operation-v2.json';assert not p.exists();p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');table={'operation_sha256':sha(p),'source_spec':{'path':str(sf.relative_to(R)),'sha256':sha(sf)},'changes':[{'object_id':o,'old_native':olds[o],'new_api':apis[o],'literal_fields':fields[o],'source_disposition':'NEW_EXACT'if olds[o]is None else'REVISE_EXACT'}for o in ordered],'retains':retains,'relation_retains':relations,'specific_retains':spec['specific_retains'],'explicit_rebinds':rebinds,'historical_Ingrid_scope':spec['historical_Ingrid_scope']};t=I/'consequence-table-v2.json';assert not t.exists();t.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');pf={'operation_sha256':sha(p),'table_sha256':sha(t),'changes':len(apis),'retains':len(retains),'relations':len(relations),'schema_checks':checks,'issues':issues,'old_fields_exact':True,'native_writes':0,'elapsed_seconds':time.monotonic()-start};f=I/'preflight-v2.json';assert not f.exists();f.write_text(json.dumps(pf,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in pf.items()if k!='schema_checks'}))
