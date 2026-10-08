import json,copy,hashlib,importlib.util
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0808';sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(D/'preparation/baseline469.sqlite');a=json.load(open(D/'primary-source-adoption-spec-v1.json'));b=json.load(open(D/'primary-current-consequence-spec-v1.json'));apis={};olds={};fields={};issues=[];dedup=[]
for f in a['field_changes']+b['field_changes']:
 oid=f['id']
 if oid not in apis:
  n=h.native(c,h.current(c,oid));assert n['version']==f['expectedVersion'];olds[oid]=n;apis[oid]=h.api(n);apis[oid]['expectedVersion']=n['version'];fields[oid]=[]
 api=apis[oid];v=api
 for k in f['field'][:-1]:v=v[k]
 assert v[f['field'][-1]]==f['old'],(oid,f['field'],'zero/mismatch');v[f['field'][-1]]=f['new'];fields[oid].append(f)
 for e in f['append_supports']:
  matches=[old for old in api['evidence']if all(old[k]==e[k]for k in ['object','version','role'])]
  if not matches:api['evidence'].append(e)
  elif e in matches:dedup.append({'target':oid,'exact_duplicate_append':e})
  else:issues.append({'target':oid,'conflicting_duplicate_append_notes':e,'existing':matches})
for r in a['explicit_rebinds']+b['explicit_rebinds']:
 matches=[e for e in apis[r['id']]['evidence']if e['object']==r['basis']and e['version']==r['old_version']];assert len(matches)==1,(r,'zero/multi');matches[0]['version']=r['new_version']
for n in a['new_source_objects']+b['new_reviews']:
 assert not c.execute('select 1 from object where id=?',(n['id'],)).fetchone();apis[n['id']]=n;olds[n['id']]=None;fields[n['id']]=[]
heads=dict(c.execute('select object_id,max(version) from revision group by object_id'));projected={**heads,**{id:(api['expectedVersion']or 0)+1 for id,api in apis.items()}}
for id,api in apis.items():
 for i,e in enumerate(api['evidence']):
  if e['version']!=projected.get(e['object']):issues.append({'target':id,'index':i,'edge':e,'current':heads.get(e['object']),'projected':projected.get(e['object']),'needs_source_disposition':True})
# Stable topological order only for exact resulting-version references.
left=list(apis);ordered=[]
while left:
 ready=[id for id in left if not any(e['object']in left and e['version']==projected[e['object']]for e in apis[id]['evidence'])]
 assert ready,('Source-dependent cycle',left)
 for id in ready:ordered.append(id);left.remove(id)
retains=[]
for x in b['retains']:
 assert x['id']not in apis,('retain/change overlap',x['id']);n=h.native(c,h.current(c,x['id']));assert n['version']==x['version'];retains.append({'revision_id':n['id'],'old_native':n,'source_disposition':x['disposition'],'rationale':x['reason']})
op={'id':'T-0808/four-unit-full-reading-identity-v1','actor':'Codex / settled Astra decisions','reason':'T-0808 AC1–4: exact four-unit full own-post reading, bounded source corrections and individual identity assessments. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':[apis[id]for id in ordered]};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();f=D/'implementation/operation-v1.json';f.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');table={'operation_sha256':sha(f),'source_specs':[{'path':str(D/'primary-source-adoption-spec-v1.json'),'sha256':sha(D/'primary-source-adoption-spec-v1.json')},{'path':str(D/'primary-current-consequence-spec-v1.json'),'sha256':sha(D/'primary-current-consequence-spec-v1.json')}],'changes':[{'object_id':id,'old_native':olds[id],'new_api':apis[id],'literal_fields':fields[id],'source_disposition':'new'if olds[id]is None else'change','rationale':'Exact settled source specification; explicit rebinds only.'}for id in ordered],'retains':retains,'explicit_rebinds':a['explicit_rebinds']+b['explicit_rebinds'],'exact_duplicate_appends_once':dedup};t=D/'implementation/consequence-table-v1.json';t.write_text(json.dumps(table,ensure_ascii=False,indent=2)+'\n');p=D/'implementation/preflight-v1.json';p.write_text(json.dumps({'literal_fields_exact':True,'issues':issues,'count':len(issues),'stable_topological_order':ordered,'exact_duplicate_appends_once':dedup},ensure_ascii=False,indent=2)+'\n');print('API',len(ordered),'retains',len(retains),'issues',len(issues));print(sha(f));print(sha(t));print(json.dumps(issues,ensure_ascii=False))
