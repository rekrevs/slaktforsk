import json,copy,importlib.util,hashlib
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0808';S=D/'implementation/stage470-v1';sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(S/'stage.sqlite');a=json.load(open(D/'primary-actual83-and-six-copy-amendment-v1.json'));b=json.load(open(D/'primary-seventh-title-copy-amendment-v1.json'));apis={};olds={};fields={}
for f in a['field_changes']:
 oid=f['id']
 if oid not in apis:n=h.native(c,h.current(c,oid));assert n['version']==f['expectedVersion'];olds[oid]=n;apis[oid]=h.api(n);apis[oid]['expectedVersion']=n['version'];fields[oid]=[]
 api=apis[oid];v=api
 for k in f['field'][:-1]:v=v[k]
 assert v[f['field'][-1]]==f['old'],(oid,f['field'],type(v[f['field'][-1]]).__name__,type(f['old']).__name__,v[f['field'][-1]],f['old']);v[f['field'][-1]]=f['new'];api['evidence'].extend(f['append_supports']);fields[oid].append(f)
for r in a['explicit_rebinds']:
 e=apis[r['id']]['evidence'][r['index']];assert e['object']==r['basis']and e['version']==r['old_version'];e['version']=r['new_version']
oid=b['object_id'];old=h.native(c,h.current(c,oid));assert old['version']==b['expected_version'];normalized=copy.deepcopy(old)
for k,v in normalized['data'].items():
 if k.endswith('_json')and isinstance(v,str):normalized['data'][k]=json.loads(v)
assert normalized==b['full_old_native'];api=h.api(old);api['expectedVersion']=old['version'];assert api['data']['value_json']['reports'][1]['title']==b['field_changes'][0]['old'];api['data']['value_json']['reports'][1]['title']=b['field_changes'][0]['new'];api['evidence'].extend(b['evidence_append']);apis[oid]=api;olds[oid]=old;fields[oid]=b['field_changes'];heads=dict(c.execute('select object_id,max(version)from revision group by object_id'));proj={**heads,**{oid:api['expectedVersion']+1 for oid,api in apis.items()}};issues=[]
for oid,api in apis.items():
 for i,e in enumerate(api['evidence']):
  if e['version']!=proj.get(e['object']):issues.append({'target':oid,'index':i,'edge':e,'current':heads.get(e['object']),'projected':proj.get(e['object'])})
left=list(apis);order=[]
while left:
 ready=[oid for oid in left if not any(e['object']in left and e['version']==proj[e['object']]for e in apis[oid]['evidence'])];assert ready
 for oid in ready:order.append(oid);left.remove(oid)
actual={r['id']:dict(r)for r in c.execute('select q.* from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null')};assert len(actual)==83;decisions=a['individual_dependency_decisions'];assert len(decisions)==83 and {d['request_id']for d in decisions}==set(actual)
for d in decisions:assert actual[d['request_id']]['affected_revision_id']==d['affected']and actual[d['request_id']]['changed_revision_id']==d['changed'];assert d['reason']
retains=[]
for r in a['retained_targets']:n=h.native(c,h.current(c,r['id']));assert n['version']==r['version'];assert r['id']not in apis;retains.append({'revision_id':n['id'],'old_native':n,'source_disposition':'retain','rationale':r['reason']})
op={'id':'T-0808/seven-copy-repair-and-83-individual-decisions-v1','actor':'Codex / settled Astra decisions','reason':'T-0808 AC2–4: seven exact necessary semantic consequences and all83 individually reviewed initial dependency requests. Newly emitted requests require separate source disposition. Root alone applies canonical after hash-bound final approval.','dependencyReviewVersion':2,'changes':[apis[id]for id in order],'resolve':[{'request':d['request_id'],'rationale':d['reason']}for d in decisions]};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();f=D/'implementation/repair-operation-v1.json';f.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');t=D/'implementation/repair-consequence-table-v1.json';t.write_text(json.dumps({'operation_sha256':sha(f),'changes':[{'object_id':id,'old_native':olds[id],'new_api':apis[id],'literal_fields':fields[id],'source_disposition':'change','rationale':'Exact individual source repair spec.'}for id in order],'retains':retains,'individual_dependency_dispositions':decisions,'explicit_rebinds':a['explicit_rebinds'],'version_questions':issues},ensure_ascii=False,indent=2)+'\n');print('APIs',len(order),'resolve',len(decisions),'retains',len(retains),'issues',len(issues));print(sha(f));print(sha(t));print(json.dumps(issues,ensure_ascii=False))
