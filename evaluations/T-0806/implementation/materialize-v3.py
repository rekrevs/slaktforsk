import json,copy,hashlib,importlib.util
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0806';s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(D/'implementation/baseline467.sqlite');p=json.loads((D/'primary-source-candidate-v3.json').read_text());assert h.state(c)=={'journal_head':467,'pending':0};changes=[];table=[];issues=[];heads=dict(c.execute('select object_id,max(version) from revision group by object_id'));projected={**heads,**{x['object_id']:x['expected_version']+1 for x in p['changes']},**{x['id']:1 for x in p['new_reviews']}}
for x in p['changes']:
 old=h.native(c,h.current(c,x['object_id']));assert old==x['old_native'];assert old['version']==x['expected_version'];a=h.api(old);a['expectedVersion']=old['version']
 for f in x['fields']:
  target=a if f['field']=='caveat' else a['data'];assert target[f['field']]==f['old'],(x['object_id'],f['field']);target[f['field']]=f['new']
 for e in x['append_evidence']:a['evidence'].append({'object':e['object_id'],'version':e['version'],'role':e['role'],'note':e['note']})
 for i,e in enumerate(a['evidence']):
  if e['version']!=projected.get(e['object']):issues.append({'target':a['id'],'index':i,'edge':e,'baseline_head':heads.get(e['object']),'projected_head':projected.get(e['object']),'inherited':i<len(old['evidence'])})
 changes.append(a);table.append({'object_id':a['id'],'old_native':old,'new_api':a,'literal_fields':x['fields'],'source_disposition':'change','rationale':'Exact primary literal field decisions; no implicit rebind.'})
for x in p['new_reviews']:
 a={'id':x['id'],'kind':x['kind'],'expectedVersion':None,'data':{k:x[k] for k in ['subject_id','criteria','outcome','body']},'disposition':x['disposition'],'evidenceStatus':x['evidence_status'],'rationale':x['rationale'],'caveat':x['caveat'],'origins':x['origins'],'evidence':[{'object':e['object_id'],'version':e['version'],'role':e['role'],'note':e['note']}for e in x['evidence']]};assert a['id']not in heads
 for i,e in enumerate(a['evidence']):
  if e['version']!=projected.get(e['object']):issues.append({'target':a['id'],'index':i,'edge':e,'baseline_head':heads.get(e['object']),'projected_head':projected.get(e['object']),'inherited':False})
 changes.append(a);table.append({'object_id':a['id'],'old_native':None,'new_api':a,'source_disposition':'new_review','rationale':x['rationale']})
retains=[]
for x in p['retains']:
 n=h.native(c,h.current(c,x['object_id']));assert n['version']==x['version'];retains.append({'revision_id':n['id'],'old_native':n,'source_disposition':'retain','rationale':x['reason']})
op={'id':'T-0806/accepted-identity-two-person-v1','actor':'Codex / settled Astra decisions','reason':'T-0806 AC1–4: individual accepted-material identity assessment and bounded historical-copy qualification; no originals. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':changes}
sha=lambda b:hashlib.sha256(b).hexdigest()
for name,v in [('operation-v3.json',op),('consequence-table-v3.json',{'operation_sha256':sha((json.dumps(op,ensure_ascii=False,indent=2)+'\n').encode()),'changes':table,'retains':retains,'identity_criteria':p['identity_criteria'],'relation_dispositions':p['relation_dispositions']}),('support-version-preflight-v3.json',{'issues':issues,'count':len(issues),'no_implicit_rebind':True})]:
 f=D/'implementation'/name;f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(name,sha(f.read_bytes()))
print('issues',len(issues))
