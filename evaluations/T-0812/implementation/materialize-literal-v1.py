import json,copy,hashlib,importlib.util,time,traceback
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0812';I=D/'implementation';start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(D/'preparation/baseline477.sqlite');assert h.state(c)=={'journal_head':477,'pending':0};designpath=D/'primary-complete-source-design-v3.json';assert sha(designpath)=='e4024f5a59e8ae37a6ff58704a019bff933fe075f3f28c5a66a0bcf6b526c55c';design=json.load(open(designpath));specs=[]
for pin in design['components']:
 assert sha(R/pin['path'])==pin['sha256'];specs.append(json.load(open(R/pin['path'])))
apis={};olds={};fields={};rebinds=[];media=[];appendrecords={};issues=[]
def normal(v,key):
 return json.loads(v)if key.endswith('_json')and isinstance(v,str)else v
for component,spec in enumerate(specs):
 for x in spec.get('changes',[]):
  oid=x['id'];n=h.native(c,h.current(c,oid));assert n['version']==x['expectedVersion'],('stale',oid)
  if oid not in apis:apis[oid]=h.api(n);apis[oid]['expectedVersion']=n['version'];olds[oid]=n;fields[oid]=[];appendrecords[oid]=[]
  api=apis[oid]
  fs=x.get('fields',[{k:x[k]for k in ['field','old','new','reason']if k in x}])
  for f in fs:
   path=f['field'].split('.');path=[{'evidence_status':'evidenceStatus'}.get(k,k)for k in path];parent=api
   if len(path)==1 and path[0]not in api:parent=api['data']
   else:
    for k in path[:-1]:parent=parent[k]
   key=path[-1];old=normal(f['old'],key);new=normal(f['new'],key);assert key in parent and parent[key]==old,('zero/fullfield mismatch',oid,f['field']);parent[key]=copy.deepcopy(new);fields[oid].append({'source_component':design['components'][component],**f})
  for rr in x.get('support_rebinds',[]):
   index=[j for j,e in enumerate(api['evidence'])if e['object']+'@'+str(e['version'])==rr['old']];assert len(index)==1,('zero/multirebind',oid,rr,index);j=index[0];obj,v=rr['new'].rsplit('@',1);api['evidence'][j]['object']=obj;api['evidence'][j]['version']=int(v);rebinds.append({'target':oid,'index':j,**rr})
  for rr in x.get('rebindEvidence',[]):
   j=rr['index'];assert n['evidence'][j]==rr['old'],('oldedge mismatch',oid,j);api['evidence'][j]['object']=rr['newObject'];api['evidence'][j]['version']=rr['newVersion'];rebinds.append({'target':oid,**rr})
  for raw in x.get('appendEvidence',[]):
   e=copy.deepcopy(raw)
   if 'id'in e:e['object']=e.pop('id')
   assert e not in api['evidence'],('duplicateappend requires source',oid,e);api['evidence'].append(e);appendrecords[oid].append(e)
  for m in x.get('media_append_exact',[]):
   assert m not in media;media.append(m);assert {'id':m['id'],'region':'helbild'}not in api['media'];api['media'].append({'id':m['id'],'region':'helbild'})
 for x in spec.get('newObjects',[]):
  oid=x['id'];assert oid not in apis and not c.execute('select 1 from object where id=?',(oid,)).fetchone();meta={'id','kind','disposition','evidenceStatus','rationale','caveat','origins','evidence','expectedVersion'};api={k:copy.deepcopy(v)for k,v in x.items()if k in meta};api['expectedVersion']=None;api['data']=copy.deepcopy(x['data'])if 'data'in x else{k:copy.deepcopy(v)for k,v in x.items()if k not in meta};apis[oid]=api;olds[oid]=None;fields[oid]=[];appendrecords[oid]=[]
for oid,a in apis.items():
 tuples=[(e['object'],e['version'],e['role'])for e in a['evidence']];assert len(tuples)==len(set(tuples)),('unique evidence tuple requires source',oid)
checks=[]
for oid,a in apis.items():
 cols=[dict(x)for x in c.execute('pragma table_info('+a['kind']+')')];allowed=[x['name']for x in cols if x['name']!='revision_id'];required=[x['name']for x in cols if x['name']!='revision_id'and x['notnull']and x['dflt_value']is None];missing=[k for k in required if a['data'].get(k)is None];unexpected=[k for k in a['data']if k not in allowed];checks.append({'id':oid,'kind':a['kind'],'required':required,'allowed':allowed,'missing':missing,'unexpected':unexpected});assert not missing and not unexpected,('schema',oid,missing,unexpected)
heads=dict(c.execute('select object_id,max(version)from revision group by object_id'));projected={**heads,**{oid:(a['expectedVersion']or 0)+1 for oid,a in apis.items()}}
for oid,a in apis.items():
 for j,e in enumerate(a['evidence']):
  assert e['object']in projected,('missingbasis',oid,e)
  if e['version']!=projected[e['object']]:issues.append({'target':oid,'index':j,'edge':e,'current':heads.get(e['object']),'projected':projected[e['object']],'origin':'preserved old edge'if olds[oid]and j<len(olds[oid]['evidence'])else'new edge','requires_source_confirmation':True})
left=list(apis);ordered=[]
while left:
 ready=[oid for oid in left if not any(e['object']in left and e['version']==projected[e['object']]for e in apis[oid]['evidence'])];assert ready,('cycle',left)
 for oid in ready:ordered.append(oid);left.remove(oid)
retains={};fieldretains=design['field_retains']
for spec in specs:
 for x in spec.get('explicit_retains',[])+spec.get('relations',[]):
  rid=x['revision'];n=h.native(c,rid);assert h.current(c,n['object_id'])==rid;assert n['object_id']not in apis;retains[n['object_id']]={'id':n['object_id'],'version':n['version'],**x}
allretained={}
for person in ['P-0254','P-0255']:
 for n in json.load(open(D/'preparation'/f'{person}-current-native-v1.json'))['current']:allretained[n['object_id']]=n
for row in json.load(open(D/'preparation/two-unit-parent-date-copy-routing-and-schema-v1.json'))['routing']:
 n=row['full_current_native'];allretained[n['object_id']]=n
for oid,n in allretained.items():
 if oid not in apis and oid not in retains:retains[oid]={'id':oid,'version':n['version'],'disposition':'RETAIN_EXACT_UNMENTIONED','reason':design['retention_rule']}
retainrows=[]
for oid,x in retains.items():
 n=h.native(c,h.current(c,oid));assert n['version']==x['version'];retainrows.append({'revision_id':n['id'],'old_native':n,'source_disposition':x})
op={'id':'T-0812/two-own-unit-adoption-identity-v1','actor':'Codex / settled Astra decisions','reason':'T-0812 AC1–4: exact two own-unit readings, existing original copies, bounded current-copy corrections and individual identity assessment. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'media':media,'changes':[apis[o]for o in ordered]};p=I/'operation-v1.json';assert not p.exists();p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');table={'operation_sha256':sha(p),'source_design':{'path':str(designpath.relative_to(R)),'sha256':sha(designpath)},'source_specs':design['components'],'changes':[{'object_id':o,'old_native':olds[o],'new_api':apis[o],'literal_fields':fields[o],'explicit_support_appends':appendrecords[o],'disposition':'NEW_EXACT'if olds[o]is None else'REVISE_LITERAL','support_rule':'Only explicit appends/rebinds; remaining old arrays exact.'}for o in ordered],'retains':retainrows,'field_scope_retains':fieldretains,'explicit_rebinds':rebinds,'criteria':specs[-1]['criteria'],'remaining_owners':specs[-1]['remaining_owners']};t=I/'consequence-table-v1.json';assert not t.exists();t.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');pf={'operation_sha256':sha(p),'consequence_sha256':sha(t),'changes':len(apis),'retains':len(retainrows),'field_scope_retains':len(fieldretains),'media':len(media),'schema_checks':checks,'issues':issues,'stable_order':ordered,'elapsed_seconds':time.monotonic()-start,'native_write':False};f=I/'preflight-v1.json';assert not f.exists();f.write_text(json.dumps(pf,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:pf[k]for k in ['operation_sha256','consequence_sha256','changes','retains','field_scope_retains','media','elapsed_seconds']}));print('version issues',len(issues))
