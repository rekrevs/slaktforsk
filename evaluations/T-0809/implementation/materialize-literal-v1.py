import json,copy,hashlib,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0809';I=D/'implementation';start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(D/'preparation/baseline471.sqlite');assert h.state(c)=={'journal_head':471,'pending':0};a=json.load(open(D/'primary-source-adoption-spec-v2.json'));b=json.load(open(D/'primary-current-consequence-spec-v2.json'));assert sha(D/'primary-source-adoption-spec-v2.json')=='5a86f0b4e804b0d50fad878ac47ea29a707763cb04e6e372efb9ad29780a31b4';assert sha(D/'primary-current-consequence-spec-v2.json')=='d0d9850cc1a6aee54d4624e22d99247a190866d329c8ceb088262446fff97baa';apis={};olds={};fields={};rebinds=[];media=[]
for spec in a['changes']+b['changes']:
 oid=spec['id'];assert oid not in apis,('duplicate target',oid);n=h.native(c,h.current(c,oid));assert n['version']==spec['expectedVersion'],('stale',oid);api=h.api(n);api['expectedVersion']=n['version'];olds[oid]=n;fields[oid]=[]
 for f in spec['fields']:
  parent=api if f['field']=='caveat' else api['data'];assert f['field'] in parent,('missingfield',oid,f['field']);assert parent[f['field']]==f['old'],('zero/fullfield mismatch',oid,f['field']);parent[f['field']]=f['new'];fields[oid].append(f)
 for e in spec.get('supportAppend',[]):
  assert e not in api['evidence'],('duplicateappend',oid,e);api['evidence'].append(copy.deepcopy(e))
 for rr in spec.get('evidenceRebinds',[]):
  index=rr['index'];assert n['evidence'][index]==rr['oldEdge'];edge=api['evidence'][index];assert edge['object']==rr['object'] and edge['version']==rr['oldVersion'];edge['version']=rr['newVersion'];rebinds.append({'target':oid,**rr})
 assert not spec.get('support_rebinds',[]),('unhandledrebind',oid)
 for m in spec.get('media_append_exact',[]):
  assert m not in media;media.append(m);api['media'].append({'id':m['id'],'region':'helbild'})
 apis[oid]=api
for spec in a['newObjects']+b['newObjects']:
 oid=spec['id'];assert oid not in apis and not c.execute('select 1 from object where id=?',(oid,)).fetchone();nativekeys=['disposition','evidenceStatus','rationale','caveat','origins','evidence'];data={k:v for k,v in spec.items() if k not in ['id','kind',*nativekeys]};api={'id':oid,'kind':spec['kind'],'expectedVersion':None,'data':data,**{k:spec[k] for k in nativekeys}};apis[oid]=api;olds[oid]=None;fields[oid]=[]
heads=dict(c.execute('select object_id,max(version) from revision group by object_id'));projected={**heads,**{oid:(api['expectedVersion']or 0)+1 for oid,api in apis.items()}};issues=[]
for oid,api in apis.items():
 for index,e in enumerate(api['evidence']):
  assert e['object'] in projected,('missingbasis',oid,e)
  if e['version']!=projected[e['object']]:issues.append({'target':oid,'index':index,'edge':e,'current':heads.get(e['object']),'projected':projected[e['object']],'origin':'preserved old edge' if olds[oid] and index<len(olds[oid]['evidence']) else 'new/appended edge','needs_individual_source_confirmation':True})
left=list(apis);ordered=[]
while left:
 ready=[oid for oid in left if not any(e['object'] in left and e['version']==projected[e['object']] for e in apis[oid]['evidence'])];assert ready,('cycle',left)
 for oid in ready:ordered.append(oid);left.remove(oid)
retainmap={}
for x in b['relationRetains']+b['explicitRetains']:
 assert x['id']not in apis;retainmap[x['id']]=x
for n in json.load(open(D/'preparation/current-native-v1.json'))['current']:
 if n['object_id'] not in apis and n['object_id']not in retainmap:retainmap[n['object_id']]={'id':n['object_id'],'version':n['version'],'decision':'RETAIN_UNLISTED_EXACT','reason':b['metadata_rule']}
retains=[]
for oid,x in retainmap.items():
 n=h.native(c,h.current(c,oid));assert n['version']==x['version'];retains.append({'revision_id':n['id'],'old_native':n,'source_disposition':x.get('disposition',x.get('decision')),'rationale':x['reason']})
op={'id':'T-0809/five-own-row-adoption-six-images-identity-v1','actor':'Codex / settled Astra decisions','reason':'T-0809 AC1–4: exact five own-row readings, six original copies, bounded current-copy corrections and individual identity assessment. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'media':media,'changes':[apis[oid]for oid in ordered]};p=I/'operation-v1.json';p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');table={'operation_sha256':sha(p),'source_specs':[{'path':str((D/f).relative_to(R)),'sha256':sha(D/f)}for f in ['primary-source-adoption-spec-v2.json','primary-current-consequence-spec-v2.json']],'changes':[{'object_id':oid,'old_native':olds[oid],'new_api':apis[oid],'literal_fields':fields[oid],'source_disposition':'new' if olds[oid]is None else 'revise','support_disposition':'Exact source-spec support appends/rebinds only; all other arrays retained.'}for oid in ordered],'retains':retains,'explicit_rebinds':rebinds,'seven_criteria':b['sevenCriteria'],'remaining_ownership':b['remainingOwnership']};t=I/'consequence-table-v1.json';t.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');pf={'operation_sha256':sha(p),'consequence_sha256':sha(t),'exact_full_field_matches':True,'issues':issues,'stable_topological_order':ordered,'changes':len(apis),'retains':len(retains),'media':len(media),'elapsed_seconds':time.monotonic()-start};q=I/'preflight-v1.json';q.write_text(json.dumps(pf,ensure_ascii=False,indent=2)+'\n');print('op',sha(p),'table',sha(t),'changes',len(apis),'retains',len(retains),'issues',len(issues));print(json.dumps(issues,ensure_ascii=False))
