from pathlib import Path
import sqlite3,json,hashlib,subprocess,importlib.util,datetime
R=Path(__file__).resolve().parents[3]; O=R/'evaluations/T-0795/preparation'; M=R/'genealogy2/data/research.sqlite'
spec=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
people=['P-0212']; before=h.sha(M);c=h.conn(M);assert h.state(c)=={'journal_head':457,'pending':0}
b=O/'baseline-j457.sqlite';assert not b.exists();t=sqlite3.connect(b);c.backup(t);t.close();d=h.conn(b);assert h.all50(c)==h.all50(d);h.write(O/'baseline-state.json',{'main':h.pin(M),'backup':h.pin(b),'state':h.state(c),'all50':h.all50(c)})
views={};seeds=set()
def ids(v):
 if isinstance(v,dict):
  rid=v.get('revision_id')
  if isinstance(rid,str) and '@' in rid:seeds.add(rid)
  for x in v.values():ids(x)
 elif isinstance(v,list):
  for x in v:ids(x)
def cli(args,p):
 r=subprocess.run(['node','genealogy2/cli.mjs',*args,'--db',str(b)],cwd=R,capture_output=True,text=True);assert r.returncode==0,r.stderr;p.write_text(r.stdout);return json.loads(r.stdout)
for p in people:
 v=cli(['person',p,'--format','json'],O/(p+'-person.json'));views[p]=v;ids(v)
 z=cli(['inspect',p],O/(p+'-inspect.json'));ids(z)
 h.write(O/(p+'-research.json'),v['research']);print('captured',p,flush=True)
for label,args in [('inventory',['inventory','--full']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]:cli(args,O/(label+'.json'));print(label,flush=True)
pool={};units={};docs={};media={}
def add(rid):
 if rid in pool:return
 n=h.native(d,rid)
 for k,table in [('origins','origin'),('evidence','dependency')]:n[k]=[dict(x) for x in d.execute('select * from '+table+' where revision_id=? order by rowid',(rid,))]
 pool[rid]=n
 for e in n['origins']:
  u=dict(d.execute('select * from unit where id=?',(e['unit_id'],)).fetchone());units[u['id']]=u
  if u['document_path'] not in docs:docs[u['document_path']]=dict(d.execute('select * from document where path=?',(u['document_path'],)).fetchone())
 for e in n['evidence']:
  add(e['basis_revision_id']);add(h.current(d,e['basis_revision_id'].rsplit('@',1)[0]))
 for e in n.get('assets',[]):media['asset:'+e['asset_path']]=dict(d.execute('select * from asset where path=?',(e['asset_path'],)).fetchone())
 for e in n.get('media',[]):media['native:'+e['asset_id']]=dict(d.execute('select * from native_asset where id=?',(e['asset_id'],)).fetchone())
for rid in sorted(seeds):add(rid)
# P0212 owner knowledge already covered by complete person view and protected snapshot below
for n in list(pool.values()):
 if n['kind']=='record':
  for table,f in [('transcription','record_id'),('assessment','subject_id')]:
   for row in d.execute('select r.id from current_revision r join '+table+' x on x.revision_id=r.id where x.'+f+'=?',(n['object_id'],)):add(row[0])
hist={}
# No unrelated full histories; complete current inputs and recursively bound support retained.
native=h.write(O/'complete-current-history-support-native.json',{'objects':pool,'origin_units':units,'documents':docs,'media_metadata':media,'histories':hist,'array_order':'native rowid; embedded raw JSON preserved','reading':'mechanical availability only; no new source reading or source judgment'})
# Exact database receipts for operations that produced bounded current/support revisions.
ops={n['operation_id'] for n in pool.values() if 'operation_id' in n}
receipts=[dict(x) for x in d.execute('select * from operation_payload order by sequence') if x['operation_id'] in ops]
h.write(O/'accepted-operation-receipts.json',receipts)
per={}
for p,v in views.items():
 req=v['research']['requirements'];themes=v['research']['themes'];pk={k:[x for x in req if x['criteria']=='legacy_person_contract/PK-'+k] for k in ['03','04','06','08','10']}
 per[p]={'name':v['person']['display_name'],'person_revision':v['person']['revision_id'],'view':h.pin(O/(p+'-person.json')),'research':h.pin(O/(p+'-research.json')),'PK':pk,'theme_count':len(themes),'themes':themes,'review_fields':{k:x for k,x in v['research'].items() if 'review' in k},'assessments':v.get('assessments',[]),'gate':v.get('review'),'privacy_candidates':[n for n in pool.values() if n['data'].get('subject_id')==p and any(s in json.dumps(n,ensure_ascii=False).lower() for s in ['integritet','levande','privat'])]}
manifest={'scope':people,'PK_scope':['03','04','06','08','10'],'theme_expected':10,'PK_expected':5,'baseline':h.pin(O/'baseline-state.json'),'native_dictionary':native,'people':per,'availability_only':True,'source_judgment':'pending Astra','current_research_complete':True,'current_heads':[rid for rid in sorted(pool) if h.current(d,pool[rid]['object_id'])==rid],'capture_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'counts':{'objects':len(pool),'units':len(units),'documents':len(docs),'receipts':len(receipts),'PK_available':sum(len(a) for p in per.values() for a in p['PK'].values()),'themes_available':sum(p['theme_count'] for p in per.values())}}
h.write(O/'current-input-manifest-v1.json',manifest);assert h.sha(M)==before and h.state(c)=={'journal_head':457,'pending':0};print(json.dumps(manifest['counts']),flush=True)
