import json,importlib.util,copy,hashlib
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0808';sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(D/'preparation/baseline469.sqlite');p=json.load(open(D/'primary-source-adoption-spec-v1.json'));apis={};olds={};heads=dict(c.execute('select object_id,max(version) from revision group by object_id'))
for f in p['field_changes']:
 oid=f['id']
 if oid not in apis:
  n=h.native(c,h.current(c,oid));assert n['version']==f['expectedVersion'];olds[oid]=n;apis[oid]=h.api(n);apis[oid]['expectedVersion']=n['version']
 a=apis[oid];v=a
 for key in f['field'][:-1]:v=v[key]
 assert v[f['field'][-1]]==f['old'],(oid,f['field']);v[f['field'][-1]]=f['new'];a['evidence'].extend(f['append_supports'])
for r in p['explicit_rebinds']:
 matches=[e for e in apis[r['id']]['evidence']if e['object']==r['basis']and e['version']==r['old_version']];assert len(matches)==1;matches[0]['version']=r['new_version']
projected={**heads,**{oid:apis[oid]['expectedVersion']+1 for oid in apis},**{a['id']:1 for a in p['new_source_objects']}};issues=[]
for a in [*p['new_source_objects'],*apis.values()]:
 for i,e in enumerate(a['evidence']):
  if e['version']!=projected.get(e['object']):issues.append({'target':a['id'],'index':i,'edge':e,'current':heads.get(e['object']),'projected':projected.get(e['object']),'needs_explicit_source_disposition':True})
out={'status':'partial sourceadoption only; no operation/apply','source_spec_sha256':hashlib.sha256((D/'primary-source-adoption-spec-v1.json').read_bytes()).hexdigest(),'new_source_apis':p['new_source_objects'],'existing_apis':list(apis.values()),'old_native':olds,'literal_field_matches_exact':True,'explicit_rebind_matches_exact':True,'version_questions':issues};f=D/'implementation/source-adoption-preflight-v1.json';f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(len(issues));print(json.dumps(issues,ensure_ascii=False))
