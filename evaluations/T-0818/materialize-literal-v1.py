import json,copy,hashlib,importlib.util,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0818';I=D/'implementation';I.mkdir(exist_ok=True);start=time.monotonic()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,v):
 assert not (I/n).exists();(I/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(D/'preparation/baseline486.sqlite');assert h.state(c)=={'journal_head':486,'pending':0};assert sha(R/'genealogy2/data/research.sqlite')==json.load(open(D/'preparation/baseline-v1.json'))['main']['sha256']
p=D/'source-design/primary-complete-source-design-v1.json';assert sha(p)=='023823a2c1065618b5d3ce6029cb607129707f0ba16d808d9c20c18dce05b585';s=json.load(open(p));apis={};old={};fields={};appends={};issues=[]
def decoded(n):
 n=copy.deepcopy(n)
 for k,v in n['data'].items():
  if k.endswith('_json')and isinstance(v,str):n['data'][k]=json.loads(v)
 return n
for x in s['existing_changes']:
 oid=x['object'];n=h.native(c,h.current(c,oid));assert n['version']==x['expectedVersion'];assert n==x['full_old_native'] or decoded(n)==x['full_old_native'],('full old mismatch',oid)
 a=h.api(n);a['expectedVersion']=n['version'];old[oid]=n;apis[oid]=a;fields[oid]=x['fields'];appends[oid]=x['evidence_append']
 for f in x['fields']:
  pp=f['path'].split('.');parent=a
  for k in pp[:-1]:parent=parent[k]
  assert parent[pp[-1]]==f['old'],('oldfield',oid,f['path']);parent[pp[-1]]=copy.deepcopy(f['new'])
 a['evidence'].extend(copy.deepcopy(x['evidence_append']))
 if x.get('media_append'):a.setdefault('media',[]).extend(copy.deepcopy(x['media_append']))
 for rr in x['evidence_rebind']:
  j=rr['index'];assert n['evidence'][j]==rr['old'],('exact oldedge',oid,j);e=rr['new'];ob,v=e['basis_revision_id'].rsplit('@',1);a['evidence'][j]={'object':ob,'version':int(v),'role':e['role'],'note':e['note']}
for x in s['new_objects']:
 assert not c.execute('select 1 from object where id=?',(x['id'],)).fetchone();assert x['expectedVersion']is None
 apis[x['id']]=copy.deepcopy(x);old[x['id']]=None;fields[x['id']]=[];appends[x['id']]=[]
heads=dict(c.execute('select object_id,max(version) from revision group by object_id'));proj={**heads,**{oid:(a['expectedVersion']or 0)+1 for oid,a in apis.items()}};schema=[]
for oid,a in apis.items():
 tuples=[(e['object'],e['version'],e['role'])for e in a['evidence']]
 if len(tuples)!=len(set(tuples)):issues.append({'type':'duplicate_tuple','object':oid,'tuples':tuples})
 cols=[dict(r)for r in c.execute('pragma table_info('+a['kind']+')')];allowed=[r['name']for r in cols if r['name']!='revision_id'];required=[r['name']for r in cols if r['name']!='revision_id'and r['notnull']and r['dflt_value']is None];missing=[k for k in required if a['data'].get(k)is None];extra=[k for k in a['data']if k not in allowed];schema.append({'object':oid,'required':required,'allowed':allowed,'missing':missing,'extra':extra})
 if missing or extra:issues.append({'type':'schema','object':oid,'missing':missing,'extra':extra})
 for j,e in enumerate(a['evidence']):
  if e['object']not in proj or e['version']!=proj[e['object']]:issues.append({'type':'unresolved_current_projected_binding','object':oid,'index':j,'edge':e,'current':heads.get(e['object']),'projected':proj.get(e['object'])})
left=list(apis);order=[]
while left:
 ready=[o for o in left if not any(e['object']in left and e['version']==proj[e['object']]for e in apis[o]['evidence'])];assert ready,('cycle',left)
 for o in ready:order.append(o);left.remove(o)
retains=[]
for x in s['retains']:
 n=h.native(c,h.current(c,x['object']));assert n['version']==x['version'] and (n==x['full_old_native']or decoded(n)==x['full_old_native']);assert x['object']not in apis
 retains.append({'object_id':x['object'],'revision_id':n['id'],'old_native':n,'disposition':x['decision'],'reason':x['reason']})
assert len(retains)==652 and len({r['object_id']for r in retains})==652
pf={'source_design':{'path':str(p.relative_to(R)),'sha256':sha(p)},'native_changes':32,'existing_changes':26,'new_objects':6,'retains':652,'schema_checks':schema,'issues':issues,'unique_evidence_tuple_preflight':not any(x['type']=='duplicate_tuple'for x in issues),'ordered_object_ids':order,'explicit_new_projected_bindings':[{'object':x['object'],**rr}for x in s['existing_changes']for rr in x['evidence_rebind']],'elapsed_seconds':time.monotonic()-start};save('preflight-v1.json',pf)
if issues:
 save('provisional-APIs-for-source-questions-v1.json',{'apis':[apis[o]for o in order],'issues':issues});print(json.dumps({'issues':issues},ensure_ascii=False));raise SystemExit(0)
op={'id':'T-0818/C1062-two-ownrows-and-current-consequences-v1','actor':'Codex / settled Astra decisions','reason':'T-0818 AC1–6: bounded single-source two full own-row adoption and exact current consequences; no extra original or LIFE assessment. Controlled apply requires hash-bound source approval and verified baseline; root alone applies canonical.','dependencyReviewVersion':2,'changes':[apis[o]for o in order],'media':copy.deepcopy(s['media'])};save('operation-v1.json',op)
save('consequence-table-v1.json',{'operation_sha256':sha(I/'operation-v1.json'),'source_design':pf['source_design'],'changes':[{'object_id':o,'old_native':old[o],'new_api':apis[o],'literal_fields':fields[o],'explicit_support_appends':appends[o],'disposition':'REVISE_LITERAL'if old[o]else'NEW_FULL_SOURCE_OBJECT'}for o in order],'retains':retains,'exact_relation_retains':s['exact_relation_retains'],'explicit_indexed_evidence_rebinds':pf['explicit_new_projected_bindings'],'rest_ownership':s['rest_ownership'],'protected':s['protected']});print(json.dumps({'operation':sha(I/'operation-v1.json'),'table':sha(I/'consequence-table-v1.json'),'issues':0,'changes':32,'retains':652}))
