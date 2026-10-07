import json,sqlite3,subprocess,time,hashlib,datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
b=Path('evaluations/T-0780');out=b/'preparation/C0060-additive-presentations-v1';start=time.time();persons=['P-0030','P-0031','P-0067','P-0068','P-0069','P-0070','P-0071','P-0072','P-0073'];db=b/'preparation/baseline-j281.sqlite';c=sqlite3.connect('file:'+str(db)+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==281
# CLI reads the frozen exact j281 clone, never live mutation.
def capture(pid):
 for kind,args in [('full',['person',pid,'--full','--format','json']),('overview',['person',pid,'--format','json'])]:
  p=out/(pid+'-'+kind+'-v1.json')
  if p.exists():json.load(open(p));continue # valid completed presentations preserved; do not repeat
  r=subprocess.run(['node','genealogy2/cli.mjs',*args,'--db',str(db)],capture_output=True,text=True);assert r.returncode==0,r.stderr;x=json.loads(r.stdout);p.write_text(r.stdout)
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(capture,persons))
cur={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')};revs={r['id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id')};domain={};evidence={}
for kind in set(x['kind'] for x in cur.values()):
 for r in c.execute('select * from '+kind):domain[r['revision_id']]=dict(r)
for r in c.execute('select * from dependency'):r=dict(r);evidence.setdefault(r['revision_id'],[]).append(r)
ids=set(persons)
for oid,r in cur.items():
 d=domain[r['id']]
 if any(d.get(f) in persons for f in ['subject_id','person_id','from_person','to_person','person_a','person_b']):ids.add(oid)
# Presentation object identifiers add any further objects exposed in CLI full details/research.
def visit(x):
 if isinstance(x,dict):
  if x.get('object_id') in cur:ids.add(x['object_id'])
  for v in x.values():visit(v)
 elif isinstance(x,list):
  for v in x:visit(v)
for pid in persons:visit(json.load(open(out/(pid+'-full-v1.json'))))
rids={cur[x]['id'] for x in ids};todo=list(rids)
while todo:
 rid=todo.pop()
 for e in evidence.get(rid,[]):
  if e['basis_revision_id'] not in rids:rids.add(e['basis_revision_id']);todo.append(e['basis_revision_id'])
known={}
query_order_amendments=[]
for o in json.load(open(b/'preparation/selected/complete-current-impact-and-support-package-v1.json'))['objects']:known[o['id']]=o
for p in [b/'implementation/dependency-preparation-v1/current-full-native-objects-v1.json',b/'implementation/dependency-preparation-v1/additional-context-full-native-objects-v2.json']:
 for o in json.load(open(p))['objects'].values():known[o['id']]=o
allobjects=[];outside=[];covered=[]
for rid in sorted(rids):
 r=revs[rid].copy();r['data']=domain[rid];r['evidence']=evidence.get(rid,[]);r['origins']=[dict(z) for z in c.execute('select * from origin where revision_id=?',(rid,))];r['current']=cur[r['object_id']]['id']==rid
 if r['kind']=='record':
  r['assets']=[dict(z) for z in c.execute('select ra.*,a.sha256,a.bytes from record_asset ra join asset a on a.path=ra.asset_path where ra.revision_id=?',(rid,))];r['media']=[dict(z) for z in c.execute('select rm.*,a.* from record_media rm join native_asset a on a.id=rm.asset_id where rm.revision_id=?',(rid,))]
 allobjects.append(r)
 if rid not in known:outside.append(r)
 else:
  k=known[rid];assert k['data']==r['data'];assert sorted(k['evidence'],key=lambda x:json.dumps(x,sort_keys=True))==sorted(r['evidence'],key=lambda x:json.dumps(x,sort_keys=True))
  if k['evidence']!=r['evidence']:
   query_order_amendments.append({'revision_id':rid,'fresh_whole_table_query_evidence':r['evidence'],'prior_frozen_evidence':k['evidence'],'same_exact_relational_rows':True,'disposition':'Preserve prior frozen evidence-array order; no dependency row or data-array order change.'});r['evidence']=k['evidence']
  assert all(k[f]==r[f] for f in ['kind','disposition','evidence_status','rationale','caveat','version']);covered.append(rid)
(out/'full-current-person-and-exact-support-dictionary-v1.json').write_text(json.dumps({'baseline_journal':281,'persons':persons,'read_only_presentation_scope':True,'objects':allobjects},ensure_ascii=False,indent=2)+'\n');(out/'objects-outside-prior-frozen-dictionaries-v1.json').write_text(json.dumps({'baseline_journal':281,'metadata_only_existing_native_objects_not_new_claims':True,'objects':outside,'count':len(outside),'exact_versions':[x['id'] for x in outside]},ensure_ascii=False,indent=2)+'\n')
(out/'prior-frozen-coverage-check-v1.json').write_text(json.dumps({'persons':persons,'current_and_exactolder_support_objects':len(allobjects),'alreadycovered_objects':len(covered),'alreadycovered_exactdata_evidence_meta_MATCH':True,'outside_prior_frozen_dictionaries':len(outside),'outside_current':sum(x['current'] for x in outside),'outside_older':sum(not x['current'] for x in outside),'record_priorcore_and_native_additionaldictionary_boundaries':'Compared prior3023core plus deduplicated4079context and460dependencydict union, exactrevisionID','source_decisions_gate':'Root must accept additive exact input freeze before dependent source decisions using outside objects.'},ensure_ascii=False,indent=2)+'\n')
(out/'query-order-comparison-amendment-v1.json').write_text(json.dumps({'metadata_only_comparison_amendment':True,'amendments':query_order_amendments,'failed_initial_attempt':'Exact array order differed for whole-table versus indexed per-revision query; each exact relational row set verified before preserving prior frozen order. Completed9CLIviews never repeated.'},ensure_ascii=False,indent=2)+'\n')
files=sorted(out.glob('*.json'));freeze={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_journal':281,'pending':0,'persons':persons,'fullviews':9,'overviewviews':9,'outside_count':len(outside),'capture_elapsed_seconds':time.time()-start,'original_reads':0,'stage_or_canonical_applies':0,'source_interpretations':0,'failed_attempts':1,'query_order_amendments':len(query_order_amendments),'pins':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files]};(out/'additive-presentation-and-native-input-freeze-v1.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n');print({'full':9,'overview':9,'objects':len(allobjects),'outside':len(outside),'seconds':time.time()-start})
