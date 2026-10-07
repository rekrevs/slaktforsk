"""T0786 mechanical current443 baseline/input capture; no source judgment or runtime writes."""
from pathlib import Path
import json,hashlib,sqlite3,importlib.util,subprocess,datetime,re
R=Path(__file__).resolve().parents[3]; O=Path(__file__).resolve().parent; MAIN=R/'genealogy2/data/research.sqlite';EXPECT='4dffaf975b66fc7fb70c0ebda39be93a52fd64d7add03100e54e6c47a4220fd0';PEOPLE=['P-0003','P-0007'];sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
helper=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';assert sha(helper)=='ce9c424a2f1f36748880e15c83b44e4aa8aa407ab627ee723bf7c90b6b709ce2';s=importlib.util.spec_from_file_location('readonly_helpers',helper);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
assert sha(MAIN)==EXPECT
backlog=R/'wotan/backlog.json';b=json.loads(backlog.read_text());entries={t['id']:t for t in b['tasks']};assert entries['T-0786']['status']=='ONGOING';assert [t['id'] for t in b['tasks'] if t['status']=='ONGOING']==['T-0786']
start=datetime.datetime.now(datetime.timezone.utc).isoformat();live=h.conn(MAIN);pre=h.all50(live);assert h.state(live)=={'journal_head':443,'pending':0}
baseline=O/'baseline-j443.sqlite';assert not baseline.exists();dest=sqlite3.connect(baseline);live.backup(dest);dest.close();base=h.conn(baseline);assert h.all50(base)==pre and h.state(base)==h.state(live)
wt=O/'working-tree-before.txt';assert not wt.exists();git=subprocess.run(['git','status','--short'],cwd=R,text=True,capture_output=True);assert git.returncode==0;wt.write_text(git.stdout)
branch=subprocess.run(['git','branch','--show-current'],cwd=R,text=True,capture_output=True);assert branch.returncode==0 and branch.stdout.strip()=='main'
seed=set();viewpins={};clis={}
def addids(v):
 if isinstance(v,dict):
  if isinstance(v.get('revision_id'),str) and '@' in v['revision_id']:seed.add(v['revision_id'].rsplit('@',1)[0])
  for x in v.values():addids(x)
 elif isinstance(v,list):
  for x in v:addids(x)
for person in PEOPLE:
 p=O/(person+'-whole-current-person.json');v=h.run_cli(['person',person,'--full','--format','json','--db',str(baseline)],p);addids(v);viewpins[person]=h.pin(p);h.write(O/(person+'-whole-current-research.json'),v['research'])
for id in ['C-0882','S-0689']:
 p=O/(id+'-complete-existing-inspect.json');v=h.run_cli(['inspect',id,'--db',str(baseline)],p);addids(v);clis[id]=h.pin(p)
seed.add('S-0689')
for label,args in [('inventory',['inventory','--full']),('Adam-verified',['pedigree','P-0269']),('Axel-verified',['pedigree','P-0270'])]:
 p=O/(label+'-current443.json');h.run_cli(args+['--db',str(baseline)],p);clis[label]=h.pin(p)
pool,units,docs,media,histories={},{},{},{},{}
def add(rid):
 if rid in pool:return
 n=h.native(base,rid);pool[rid]=n
 for origin in n['origins']:
  u=dict(base.execute('select * from unit where id=?',(origin['unit_id'],)).fetchone());units[u['id']]=u;d=dict(base.execute('select * from document where path=?',(u['document_path'],)).fetchone());docs[d['path']]=d
 for e in n['evidence']:
  add(e['basis_revision_id']);add(h.current(base,e['basis_revision_id'].rsplit('@',1)[0]))
 for e in n.get('assets',[]):
  m=dict(base.execute('select * from asset where path=?',(e['asset_path'],)).fetchone());media['asset:'+m['path']]=m
 for e in n.get('media',[]):
  m=dict(base.execute('select * from native_asset where id=?',(e['asset_id'],)).fetchone());media['native:'+m['id']]=m
for oid in sorted(seed):add(h.current(base,oid))
for rid,n in list(pool.items()):
 if n['kind']=='record':
  for table,field in [('transcription','record_id'),('assessment','subject_id')]:
   for r in base.execute('select c.id from current_revision c join '+table+' x on x.revision_id=c.id where x.'+field+'=? order by c.object_id',(n['object_id'],)):add(r[0])
for oid in sorted({n['object_id'] for n in pool.values()}):
 hist=[r[0] for r in base.execute('select id from revision where object_id=? order by version',(oid,))];histories[oid]=hist
 for rid in hist:add(rid)
protected_input=R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json';protected=json.loads(protected_input.read_text())['objects'];assert len(protected)==42
for rid,n in protected.items():assert h.current(base,n['object_id'])==rid and h.native(base,rid)==n;add(rid)
for r in base.execute("select id from current_revision where evidence_status='OWNER_CONFIRMED' order by object_id"):add(r[0])
nativepin=h.write(O/'complete-two-current-history-upstream-OWNER-native-inputs-v1.json',{'objects':pool,'origin_units':units,'documents':docs,'media_metadata':media,'full_histories':histories,'native_evidence_origins_assets_media_order':'Exact stored rowid order; embedded JSONsource arrays unchanged','source_reading_grade':'NONE_MECHANICAL_CAPTURE_ONLY'})
# Relevant routing beyond body: exact literals/source refs in whole native fields. Astra decides implications.
terms=['S-0689','C-0882','C0882','uppslag15','uppslag 15','1936–1961','1943-11-24','AIIa77','A II a/77'];routes=[]
for rid,n in pool.items():
 if h.current(base,n['object_id'])!=rid:continue
 hits=[]
 def walk(v,p=''):
  if isinstance(v,str):
   found=[t for t in terms if t in v]
   if found:hits.append({'field_pointer':p,'matched_literal_terms':found,'full_exact_field':v})
  elif isinstance(v,dict):
   for k,y in v.items():walk(y,p+'/'+k.replace('~','~0').replace('/','~1'))
  elif isinstance(v,list):
   for i,y in enumerate(v):walk(y,p+'/'+str(i))
 walk(n)
 if hits:routes.append({'object_id':n['object_id'],'revision_id':rid,'kind':n['kind'],'matches':hits,'full_native_pointer':'/objects/'+rid.replace('~','~0').replace('/','~1'),'candidate_source_disposition':'PENDING_ASTRA_NOT_MECHANICAL_RECOMMENDATION'})
routingpin=h.write(O/'finite-current-route-clause-and-structured-metadata-locator-v1.json',{'dictionary_pin':nativepin,'rows':routes,'meaning':'Exact literal routing only, not need-to-amend or source-grade certification'})
# Exact current native support head/API and all-history incoming for potential assessment/path changes.
selected={rid:n for rid,n in pool.items() if n['kind']=='assessment' and n['data']['subject_id'] in PEOPLE and (n['data']['criteria'] in ['identity_review/1','tree_effect/1','legacy_review_header'] or n['data']['criteria'].startswith('legacy_person_contract/'))}
callers=[]
for rid,n in selected.items():
 for e in base.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(rid,)):
  edge=dict(e);caller=h.native(base,edge['revision_id']);edge['caller_current_revision_id']=h.current(base,caller['object_id']);edge['caller_is_current']=edge['caller_current_revision_id']==edge['revision_id'];callers.append(edge)
currentpin=h.write(O/'exact-current-PK-native-review-full-body-caveat-and-incoming-v1.json',{'dictionary_pin':nativepin,'objects':selected,'all_history_incoming_edges':callers,'source_dispositions_required_before_rebind_or_build':True})
# Existing URLs are historical routing, never independently verified current access.
urlrows=[]
for path,d in docs.items():
 if path.startswith('genealogy/sources/S-0689') or path.startswith('genealogy/citations/C-0882'):
  for url in dict.fromkeys(re.findall(r'https?://[^\s<>\]\)]+',d['text'])):urlrows.append({'document_path':path,'frozen_document_sha256':d['sha256'],'known_url':url,'current_access_status':'NOT_RECHECKED_BY_SOL','full_document_dictionary_pointer':'/documents/'+path.replace('~','~0').replace('/','~1')})
urlpin=h.write(O/'existing-C0882-S0689-catalog-and-viewer-URL-routing-v1.json',{'rows':urlrows,'no_catalog_or_original_opened':True})
accept=R/'evaluations/T-0784/root-actual-three-person-canonical-acceptance-v1.json';assert sha(accept)=='85d1af907bc1e97d9a9e684a6a1f7ef6358e60be57dccd245ad7c481129eafa8';accepted=json.loads(accept.read_text());assert accepted['main_pin']['sha256']==EXPECT
acceptedpins=[h.pin(accept),accepted['canonical_handoff_pin'],*accepted['source_gates'],h.pin(R/'evaluations/T-0784/source-review/primary-current-21-comparative-exact-dispositions-v3.json'),h.pin(R/'evaluations/T-0784/implementation/previous-all-twelve-individual-G002-receipt-pins-unchanged-proof-v1.json')]
for p in acceptedpins:assert sha(R/p['path'])==p['sha256']
source_reuse=[]
for rid,n in selected.items():
 if n['operation_id'].startswith('T-0784/'):
  assert n==h.native(live,rid);source_reuse.append({'revision_id':rid,'person':n['data']['subject_id'],'criterion':n['data']['criteria'],'outcome':n['data']['outcome'],'full_native_input_pointer':'/objects/'+rid,'accepted_operation':n['operation_id'],'retained_scope':'Exact native axis/current clauses; not a new whole source read or automatic source exhaustion'})
reusepin=h.write(O/'accepted-T0784-exact-current-two-person-reuse-and-immutable-receipt-lock-v1.json',{'receipt_pins':acceptedpins,'individual_two_person_axis_inputs':source_reuse,'no_repeated_original_reading':True,'no_new_source_grade':True})
assert sha(MAIN)==EXPECT and h.state(live)=={'journal_head':443,'pending':0} and h.all50(live)==pre and h.all50(base)==pre
proofpin=h.write(O/'fresh443-physical-baseline-logical-all50-and-live-unchanged-v1.json',{'MAIN_pin':h.pin(MAIN),'baseline_pin':h.pin(baseline),'actual_state':h.state(live),'all50_schema_raw_rows_BLOB_embedded_JSON_and_native_order_equal':True,'all50_before':pre,'protected42_full_native_current_exact':True,'protected42_input_pin':h.pin(protected_input),'no_canonical_Wotan_or_source_mutations':True})
index=h.write(O/'complete-current443-two-person-route-preparation-index-v1.json',{'task':'T-0786','status':'MECHANICAL_INPUTS_LOCKED_SOURCE_DISPOSITIONS_PENDING','started_at_utc':start,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':PEOPLE,'active_task_entry':entries['T-0786'],'owner_run_limit':'ExactlyT0786–0789; currentpreparation T0786 only','proof_pin':proofpin,'whole_person_views':viewpins,'readonly_current_inventory_and_pedigree_inspect_pins':clis,'complete_native_input_pin':nativepin,'finite_current_route_clauses_pin':routingpin,'current_PK_review_and_incoming_pin':currentpin,'known_catalog_urls_pin':urlpin,'accepted_reuse_pin':reusepin,'working_tree_pin':h.pin(wt),'working_branch':'main','counts':{'full_native_revisions':len(pool),'frozen_documents':len(docs),'current_literal_route_rows':len(routes),'protected42':42,'current_and_historical_review_incoming_edges':len(callers)},'next_unperformed':'Astra exact bounded catalog/access dispositions and primary individual current-consequence spec; no operations or neworiginals authorized to Sol','usage':'UNKNOWN pending root collector'})
print(json.dumps({'index_pin':index,'counts':json.loads((R/index['path']).read_text())['counts'],'known_URL_rows':urlrows,'actual_state':h.state(live)},ensure_ascii=False));base.close();live.close()
