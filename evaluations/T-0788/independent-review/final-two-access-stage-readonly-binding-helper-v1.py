import json,pathlib,hashlib,sqlite3,datetime
B=pathlib.Path('evaluations/T-0788');S=B/'two-access-notes-stage-v1';O=B/'independent-review'
def read(p):return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
def chk(p):assert pin(p['path'])['sha256']==p['sha256'],p
hp=S/'complete-two-access-search-stage-result-and-Astra-handoff-v1.json';h=read(hp)
def pins(x):
 if isinstance(x,dict):
  if 'path'in x and 'sha256'in x:chk(x)
  for v in x.values():pins(v)
 elif isinstance(x,list):
  for v in x:pins(v)
pins(h)
reviewp=O/'exact-two-access-source-specification-meaning-review-v1.json';assert pin(reviewp)['sha256']=='45498a4f65bcb0d006518d96a05a49135538435828368b44409cabc5a417360e'
pkg=read(h['ordered_package_pin']['path']);assert [x['operation_pin']for x in pkg['operations']]==h['operation_pins']
def conn(p):c=sqlite3.connect('file:'+str(pathlib.Path(p).resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
b=conn(h['fresh_baseline_pin']['path']);c=conn(h['stage_DB_pin']['path']);main=conn(h['live_main_pin']['path'])
assert b.execute('select max(sequence)from operation_payload').fetchone()[0]==444
assert c.execute('select max(sequence)from operation_payload').fetchone()[0]==446
assert main.execute('select max(sequence)from operation_payload').fetchone()[0]==444
for db in [b,c,main]:assert db.execute('select count(*)from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null').fetchone()[0]==0
actual=read(h['actual_native_target_API_pin']['path']);targetchecks=[]
for i,(opp,spp) in enumerate(zip(h['operation_pins'],h['source_spec_pins'])):
 op=read(opp['path']);spec=read(spp['path']);a=spec['full_new_API'];assert op['changes']==[a]
 assert set(op)=={'id','actor','reason','dependencyReviewVersion','changes'} and op['dependencyReviewVersion']==2
 stored=c.execute('select sequence,request_json from operation_payload where operation_id=?',(op['id'],)).fetchone();assert stored[0]==445+i and json.loads(stored[1])==op
 assert not b.execute('select id from object where id=?',(a['id'],)).fetchone()
 assert not c.execute('select id from review_request where operation_id=?',(op['id'],)).fetchone()
 rid=a['id']+'@1';r=dict(c.execute('select *from revision where id=?',(rid,)).fetchone());data=dict(c.execute('select *from search where revision_id=?',(rid,)).fetchone());origins=[dict(x)for x in c.execute('select *from origin where revision_id=? order by rowid',(rid,))];ev=[dict(x)for x in c.execute('select *from dependency where revision_id=? order by rowid',(rid,))]
 d={k:v for k,v in data.items()if k!='revision_id'};d['scope_json']=json.loads(d['scope_json']);assert d==a['data'];assert origins==a['origins']==[]
 assert [{'object':x['basis_revision_id'].rsplit('@',1)[0],'version':int(x['basis_revision_id'].rsplit('@',1)[1]),'role':x['role'],'note':x['note']}for x in ev]==a['evidence']
 for k,ak in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')]:assert r[k]==a[ak]
 for edge in a['evidence']:assert c.execute('select id from current_revision where object_id=?',(edge['object'],)).fetchone()[0]==edge['object']+'@'+str(edge['version'])
 assert a['bindings']=={a['data']['source_id']:1}
 targetchecks.append({'object':rid,'entire_stored_API_exact':True,'entire_actual_data_and_metadata_ordered_edges_equals_own_reviewed_source_API':True,'context_only_current_support_heads_exact':True,'new_requests':[]})
expected={'operation':2,'operation_payload':2,'object':2,'revision':2,'search':2,'dependency':3};checks=[]
for (name,) in b.execute("select name from sqlite_master where type='table' order by name"):
 if name.startswith('object_search'):continue
 try:
  old=[tuple(x)for x in b.execute('select rowid,*from "'+name+'" order by rowid')];new=[tuple(x)for x in c.execute('select rowid,*from "'+name+'" order by rowid')];live=[tuple(x)for x in main.execute('select rowid,*from "'+name+'" order by rowid')];assert new[:len(old)]==old and live==old,name
 except sqlite3.OperationalError:
  cols=[x[1]for x in b.execute('pragma table_info("'+name+'")')];q='select *from "'+name+'" order by '+','.join('"'+x+'"'for x in cols);old=[tuple(x)for x in b.execute(q)];new=[tuple(x)for x in c.execute(q)];live=[tuple(x)for x in main.execute(q)];assert old==new==live
 assert len(new)-len(old)==expected.get(name,0),(name,len(new)-len(old));checks.append({'table':name,'complete_old_rows_and_rowid_order_retained':True,'new_rows':len(new)-len(old),'live_baseline_exact':True})
assert len(checks)==44
schema=lambda z:[tuple(x)for x in z.execute('select type,name,tbl_name,sql from sqlite_master order by type,name')];assert schema(b)==schema(c)==schema(main)
proof=read(h['full_all50_diff_pin']['path']);assert proof['protected42_exact'] and proof['all_old_current_heads_and_review_state_retained'] and proof['derived_current_search_only_two_exact_new_rows']
for n in ['verify','verify-assets','verify-source']:assert read(S/(n+'.json'))['ok']
for who in ['P-0269','P-0270']:assert read(S/(who+'-default-verified-pedigree.json'))==read(pathlib.Path('evaluations/T-0786/one-search-stage-v1')/(who+'-verified-pedigree.json'))
priorinv=read('evaluations/T-0786/one-search-stage-v1/inventory.json');inv=read(S/'inventory.json');assert all(inv[k]==priorinv[k]for k in ['format','note','active','all'])
requests=read(h['actual_individual_request_pin']['path']);assert requests['requests']==[]
for x in [b,c,main]:x.close()
chk(h['stage_DB_pin']);chk(h['fresh_baseline_pin']);chk(h['live_main_pin'])
result={'tasks':['T-0788','T-0789'],'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'PASS_FINAL_EXACT_TWO_ACCESS_NOTES_SOURCE_AND_CONSEQUENCE','finalreadyforcanonical':True,'handoff_pin':pin(hp),'ordered_package_pin':h['ordered_package_pin'],'operation_pins':h['operation_pins'],'stage_DB_pin':h['stage_DB_pin'],'fresh_baseline_pin':h['fresh_baseline_pin'],'live_MAIN_unchanged_pin':h['live_main_pin'],'source_spec_pins':h['source_spec_pins'],'own_exact_source_specification_review':pin(reviewp),'own_prior_freezes':[pin(O/'own-access-only-current-and-stronger-reuse-freeze-v1.json'),pin('evaluations/T-0789/independent-review/own-access-only-current-and-stronger-reuse-freeze-v1.json')],'actual_state':{'journal_head':446,'pending':0},'actual_sequential_steps':h['actual_sequential_steps'],'actual_requests':[],'individual_actual_target_checks':targetchecks,'direct_readonly_SQL_old_table_checks':checks,'schema_and_live_baseline_exact':True,'all50_derivedsearch_and_protected42_proof':h['full_all50_diff_pin'],'actual_fullnative_support_proof':h['actual_native_target_API_pin'],'validators':h['validators'],'both_default_verified_pedigrees_exact_accepted444':True,'inventory_shared_aggregate_fields_unchanged':True,'source_consequence_judgment':'Both actual full native search payloads exactly implement the personally reviewed source APIs. Root-observed dated publicfullmax401 and exactChromeLOGIN are limited access outcomes only. No originals or register content were received/read, no Maj/sister absence or source-exhaustion conclusion. Historical744hash and1945/46Jstarts remain routing; Arnepages remain notMajhits. Current strongest acceptedT0784 Maj/source/OWNER/relations and T0676grave credits remain unchanged; grave does not substitute for yearwiseownrows. Every existing native/person/PK/PATH/legacy/identity/tree/life/body/caveat and metadata/evidence/origin/history row is preserved. No requests generated, hence no individual resolution needed.','research_remaining':'T0788 exact744fullimage/ownr10cols9–13 and necessaryr9 unread; T0789 own1945/46registerlocating/personrows unread; both await actual permitted access and remain BLOCKED. No task DONE approval. T0787 required3011 hold remains, no partialthree-original package staged or approved by this gate.','method_limits':'Own freezes precede primary comparisons; observed external access is assessed from root logs, not claimed as independent browser/sourceimage inspection. Accepted prior wholecurrent/source work reused at exactdeclaredscope; no blanket468/79 wholehistory reading and no repeated21personreview. Direct SQL44 tables plus pinned all50 derivedsearch proof distinguished.','open_findings':[],'canonical_apply_authorized_by_this_agent':False,'actual_task_completion_approved':False,'usage':'UNKNOWN pending root actualnewturn collector'}
out=O/'two-access-notes-actual446-final-independent-source-consequence-gate-v1.json';assert not out.exists();out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(pin(out)))
