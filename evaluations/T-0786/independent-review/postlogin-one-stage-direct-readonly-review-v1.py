from pathlib import Path
import sqlite3,json,hashlib,datetime
B=Path('evaluations/T-0786'); S=B/'postlogin-one-search-stage-v1'; O=B/'independent-review'
J=lambda p:json.loads(Path(p).read_text()); pin=lambda p:{'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
h=J(S/'complete-one-search-stage-result-and-Astra-handoff-v1.json')
def verify_pins(x):
 if isinstance(x,dict):
  if set(['path','sha256'])<=set(x): assert pin(x['path'])['sha256']==x['sha256'],x['path']
  for v in x.values():verify_pins(v)
 elif isinstance(x,list):
  for v in x:verify_pins(v)
verify_pins(h)
op=J(h['operation_pin']['path']);spec=J(h['source_spec_pin']['path']);assert op['changes']==[spec['full_new_API']];assert op['dependencyReviewVersion']==2;assert not op.get('resolve',[])
mp=Path('genealogy2/data/research.sqlite');sp=Path(h['stage_DB_pin']['path']);before=[pin(mp),pin(sp)]
a=sqlite3.connect('file:'+str(mp.resolve())+'?mode=ro',uri=True);b=sqlite3.connect('file:'+str(sp.resolve())+'?mode=ro',uri=True)
assert a.execute('select max(sequence) from operation_payload').fetchone()[0]==446
assert b.execute('select max(sequence) from operation_payload').fetchone()[0]==447
assert b.execute('select count(*) from review_request r left join review_resolution s on s.request_id=r.id where s.request_id is null').fetchone()[0]==0
assert json.loads(b.execute('select request_json from operation_payload where sequence=447').fetchone()[0])==op
schema='select type,name,tbl_name,sql from sqlite_master order by type,name';assert a.execute(schema).fetchall()==b.execute(schema).fetchall()
allowed={'operation':1,'operation_payload':1,'object':1,'revision':1,'search':1,'dependency':2};checks=[]
for (t,) in a.execute("select name from sqlite_master where type='table' order by name"):
 if t.startswith('object_search'): continue
 try:old=a.execute(f'SELECT rowid,* FROM "{t}" ORDER BY rowid').fetchall();new=b.execute(f'SELECT rowid,* FROM "{t}" ORDER BY rowid').fetchall()
 except sqlite3.OperationalError:old=a.execute(f'SELECT * FROM "{t}" ORDER BY 1,2').fetchall();new=b.execute(f'SELECT * FROM "{t}" ORDER BY 1,2').fetchall()
 assert new[:len(old)]==old,t;assert len(new)-len(old)==allowed.get(t,0),t
 checks.append({'table':t,'old_rows':len(old),'exact_old_row_order':True,'delta':len(new)-len(old)})
x=spec['full_new_API'];rid=x['id']+'@1';b.row_factory=sqlite3.Row
r=dict(b.execute('select * from revision where id=?',(rid,)).fetchone());d=dict(b.execute('select * from search where revision_id=?',(rid,)).fetchone());d.pop('revision_id');d['scope_json']=json.loads(d['scope_json']);assert d==x['data'];assert r['rationale']==x['rationale'] and r['caveat']==x['caveat'] and r['disposition']==x['disposition'] and r['evidence_status']==x['evidenceStatus'] and r['previous_id'] is None
edges=[dict(e) for e in b.execute('select * from dependency where revision_id=? order by rowid',(rid,))];expected=[{'revision_id':rid,'basis_revision_id':e['object']+'@'+str(e['version']),'role':e['role'],'note':e['note']} for e in x['evidence']];assert edges==expected
assert b.execute('select count(*) from origin where revision_id=?',(rid,)).fetchone()[0]==0
assert J(S/'actual-individual-requests-v1.json') in [[],{'requests':[]}]
proof=J(h['full_all50_diff_pin']['path']);assert proof['protected42_exact'] and proof['derived_search_only_authorized_new_object']
validators=[]
for pp in h['validators']:
 p=Path(pp['path']); proc=p.with_suffix('.process.json');v=J(proc);assert v['exit_code']==0;validators.append({'output':pp,'process':pin(proc),'exit_code':0})
a.close();b.close();assert before==[pin(mp),pin(sp)]
r={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'handoff':pin(S/'complete-one-search-stage-result-and-Astra-handoff-v1.json'),'DBs_unchanged_by_own_readonly_SQL':before,'state':{'main':446,'stage':447,'pending':0},'full_spec_API_and_whole_stored_operation_equal':True,'ordered_edges':edges,'scope_json_representation':'Parsed native JSON string compared to API object; no array sorting or source field changes.','direct_old_table_checks':checks,'remaining_derived_object_search_scope':'Pinned all50 proof, not direct prefix assertion on rebuilt FTS shadow rows.','protected42_and_all_old_source_review_knowledge_unchanged':True,'actual_requests':[],'validator_checks':validators}
p=O/'postlogin-one-stage-direct-readonly-review-proof-v1.json';assert not p.exists();p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(pin(p)))
