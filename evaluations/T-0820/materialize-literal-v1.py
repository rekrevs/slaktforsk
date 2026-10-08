import json,copy,hashlib,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0820';I=D/'implementation';I.mkdir(exist_ok=True);start=time.monotonic()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,v):
 assert not (I/n).exists();(I/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
helper=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';sp=importlib.util.spec_from_file_location('h',helper);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
MAIN=R/'genealogy2/data/research.sqlite';baseline='c0bfefbfe1a734cf216514d478c1f74c77a4f05237ae78a04e00b45517295c76';assert sha(MAIN)==baseline;c=h.conn(MAIN);assert h.state(c)=={'journal_head':488,'pending':0}
p=D/'complete-source-design-v3.json';assert sha(p)=='0be0a21330ec3a8b93cc683adb9f9b4caa98547aef2e940ca26010323398feb4';s=json.load(open(p));apis={};old={};issues=[]
def edge(e):
 ob,v=e['basis_revision_id'].rsplit('@',1);return {'object':ob,'version':int(v),'role':e['role'],'note':e['note']}
for x in s['changes']:
 oid=x['object_id'];n=h.native(c,h.current(c,oid));assert n==x['old_native'] and n['version']==x['expected_version'],oid;a=h.api(n);a['expectedVersion']=n['version'];old[oid]=n
 for f in x['field_changes']:
  pp=f['field'].split('.');par=a
  for k in pp[:-1]:par=par[k]
  ov=par[pp[-1]];fv=f['old'];nv=f['new']
  if pp[-1].endswith('_json'):
   if isinstance(fv,str):fv=json.loads(fv)
   if isinstance(nv,str):nv=json.loads(nv)
  assert ov==fv,('oldfield',oid,f['field']);par[pp[-1]]=copy.deepcopy(nv)
 for rr in x['evidence_rebinds']:
  j=rr['index'];assert n['evidence'][j]==rr['old_edge'];ob,v=rr['new_basis_revision_id'].rsplit('@',1);a['evidence'][j]['object']=ob;a['evidence'][j]['version']=int(v)
 a['evidence'].extend(edge(e)for e in x['evidence_appends'])
 if x.get('media_append'):a.setdefault('media',[]).append(copy.deepcopy(x['media_append']))
 apis[oid]=a
for x in s['new_objects']:
 assert not c.execute('select 1 from object where id=?',(x['id'],)).fetchone();assert x['expected_version']is None;a=copy.deepcopy(x);a['expectedVersion']=a.pop('expected_version');a['evidenceStatus']=a.pop('evidence_status');a['evidence']=[edge(e)for e in a['evidence']]
 for k,v in a['data'].items():
  if k.endswith('_json')and isinstance(v,str):a['data'][k]=json.loads(v)
 apis[a['id']]=a;old[a['id']]=None
heads=dict(c.execute('select object_id,max(version)from revision group by object_id'));proj={**heads,**{o:(a['expectedVersion']or 0)+1 for o,a in apis.items()}};schema=[]
for oid,a in apis.items():
 tuples=[(e['object'],e['version'],e['role'])for e in a['evidence']]
 if len(tuples)!=len(set(tuples)):issues.append({'type':'duplicate_tuple','object':oid})
 cols=[dict(r)for r in c.execute('pragma table_info('+a['kind']+')')];allowed=[r['name']for r in cols if r['name']!='revision_id'];required=[r['name']for r in cols if r['name']!='revision_id'and r['notnull']and r['dflt_value']is None];missing=[k for k in required if a['data'].get(k)is None];extra=[k for k in a['data']if k not in allowed];schema.append({'object':oid,'required':required,'allowed':allowed,'missing':missing,'extra':extra})
 if missing or extra:issues.append({'type':'schema','object':oid,'missing':missing,'extra':extra})
 for j,e in enumerate(a['evidence']):
  if not c.execute('select 1 from revision where object_id=?and version=?',(e['object'],e['version'])).fetchone() and not(e['object']in apis and e['version']==proj[e['object']]):issues.append({'type':'unresolved_binding','object':oid,'index':j,'edge':e})
left=list(apis);order=[]
while left:
 ready=[o for o in left if not any(e['object']in left and e['version']==proj[e['object']]for e in apis[o]['evidence'])];assert ready,('cycle',left)
 for o in ready:order.append(o);left.remove(o)
retains=[]
for x in s['retains']:
 n=h.native(c,h.current(c,x['object_id']));assert n==x['full_native']and n['version']==x['version'];assert x['object_id']not in apis;retains.append({'object_id':x['object_id'],'revision_id':n['id'],'old_native':n,'disposition':x['disposition'],'reason':x['reason']})
assert len(apis)==34 and len(retains)==562
save('preflight-v1.json',{'issues':issues,'schema':schema,'tuple_uniqueness':not any(x['type']=='duplicate_tuple'for x in issues),'order':order,'baseline_sha256':baseline,'elapsed_seconds':time.monotonic()-start})
if issues:save('provisional-APIs-v1.json',list(apis.values()));raise SystemExit(json.dumps(issues))
op={'id':'T-0820/C0800-exact-continuation-and-current-consequences-v1','actor':'Codex / settled Astra decisions','reason':'T-0820: exact bounded C0800 continuation adoption and SOURCE-approved current consequences under task acceptance criteria. Controlled apply requires hash-bound SOURCE approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':[apis[o]for o in order],'media':s['media']};save('operation-v1.json',op)
by={x['object_id']:x for x in s['changes']};save('consequence-table-v1.json',{'operation_sha256':sha(I/'operation-v1.json'),'source_design':{'path':str(p.relative_to(R)),'sha256':sha(p)},'changes':[{'object_id':o,'old_native':old[o],'new_api':apis[o],'source_disposition':by.get(o,{'disposition':'NEW_SOURCE_OBJECT'}),'disposition':'REVISE_LITERAL'if old[o]else'NEW_SOURCE_OBJECT'}for o in order],'retains':retains,'protected':s['protected'],'remaining_owners':s['remaining_owners']});assert sha(MAIN)==baseline;print(json.dumps({'changes':len(apis),'retains':len(retains),'op':sha(I/'operation-v1.json'),'table':sha(I/'consequence-table-v1.json')}))
