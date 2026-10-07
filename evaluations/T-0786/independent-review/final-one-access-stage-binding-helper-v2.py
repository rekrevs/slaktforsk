import json,pathlib,hashlib,sqlite3,datetime
B=pathlib.Path('evaluations/T-0786');S=B/'one-search-stage-v1';O=B/'independent-review'
def read(p):return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
def chk(p):assert pin(p['path'])==p
hp=S/'complete-one-search-stage-result-and-Astra-handoff-v1.json';h=read(hp)
for v in h.values():
 if isinstance(v,dict) and 'path'in v:chk(v)
for v in h['validators']:chk(v)
reviewp=O/'exact-one-shared-access-search-source-specification-review-v1.json';review=read(reviewp);assert pin(reviewp)['sha256']=='123a93a5d39e9fb88f22eed319a9b7baba702dd2a7c5edc98635552a48671666'
spec=read(h['source_spec_pin']['path']);op=read(h['operation_pin']['path']);package=read(h['package_pin']['path']);a=spec['full_new_API']
assert op['changes']==[a] and len(package['operations'])==1 and package['operations'][0]['operation_pin']==h['operation_pin'];assert op['dependencyReviewVersion']==2 and set(op)=={'id','actor','reason','dependencyReviewVersion','changes'}
assert hashlib.sha256(json.dumps(a,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==review['full_API_sha256']
bp=read(B/'preparation/fresh443-physical-baseline-logical-all50-and-live-unchanged-v1.json');chk(bp['MAIN_pin']);chk(bp['baseline_pin'])
def connect(p):c=sqlite3.connect('file:'+str(pathlib.Path(p).resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
c=connect(h['stage_DB_pin']['path']);b=connect(bp['baseline_pin']['path'])
assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==444
assert json.loads(c.execute('select request_json from operation_payload where operation_id=?',(op['id'],)).fetchone()[0])==op
assert c.execute('select count(*) from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null').fetchone()[0]==0
assert not c.execute('select id from review_request where operation_id=?',(op['id'],)).fetchone()
assert read(h['actual_request_pin']['path'])['requests']==[]
rid=a['id']+'@1';r=dict(c.execute('select * from revision where id=?',(rid,)).fetchone());data=dict(c.execute('select * from search where revision_id=?',(rid,)).fetchone());origins=[dict(x) for x in c.execute('select * from origin where revision_id=? order by rowid',(rid,))];evidence=[dict(x) for x in c.execute('select * from dependency where revision_id=? order by rowid',(rid,))]
native={**r,'kind':'search','data':data,'origins':origins,'evidence':evidence};assert native==read(h['native_target_and_support_pin']['path'])['target']
d={k:v for k,v in data.items() if k!='revision_id'};d['scope_json']=json.loads(d['scope_json']);assert d==a['data'];assert origins==a['origins']==[]
assert [{ 'object':x['basis_revision_id'].rsplit('@',1)[0],'version':int(x['basis_revision_id'].rsplit('@',1)[1]),'role':x['role'],'note':x['note']} for x in evidence]==a['evidence']
for k,ak in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')]:assert r[k]==a[ak]
assert a['bindings']=={'S-0689':1};assert c.execute('select id from current_revision where object_id="S-0689"').fetchone()[0]=='S-0689@1';assert c.execute('select id from current_revision where object_id="R-18122baf2db2f6c17eda5082"').fetchone()[0]=='R-18122baf2db2f6c17eda5082@2'
assert not b.execute('select id from object where id=?',(a['id'],)).fetchone()
expected={'operation':1,'operation_payload':1,'object':1,'revision':1,'search':1,'dependency':2};checks=[]
for row in b.execute("select name from sqlite_master where type='table' order by name"):
 name=row[0]
 if name.startswith('object_search'):continue
 try:
  old=[tuple(x) for x in b.execute('select rowid,* from "'+name+'" order by rowid')];new=[tuple(x) for x in c.execute('select rowid,* from "'+name+'" order by rowid')];assert new[:len(old)]==old
 except sqlite3.OperationalError:
  cols=[x[1] for x in b.execute('pragma table_info("'+name+'")')];q='select * from "'+name+'" order by '+','.join('"'+x+'"' for x in cols);old=[tuple(x) for x in b.execute(q)];new=[tuple(x) for x in c.execute(q)];assert new==old
 assert len(new)-len(old)==expected.get(name,0),(name,len(new)-len(old));checks.append({'table':name,'old_rows_order_exact':True,'added':len(new)-len(old)})
assert len(checks)==44
schema=lambda z:[tuple(x) for x in z.execute('select type,name,tbl_name,sql from sqlite_master order by type,name')];assert schema(c)==schema(b)
proof=read(h['full_all50_diff_pin']['path']);assert proof['protected42_exact'] and proof['all_old_current_heads_metadata_history_retained'] and proof['derived_search_only_authorized_new_object']
for name in ['verify','verify-assets','verify-source']:assert read(S/(name+'.json'))['ok']
for current,previous in [('P-0269-verified-pedigree.json','Adam-verified-current443.json'),('P-0270-verified-pedigree.json','Axel-verified-current443.json')]:assert read(S/current)==read(B/'preparation'/previous)
assert all(read(S/'inventory.json')[k]==read(B/'preparation/inventory-current443.json')[k] for k in ['format','note','active','all'])
c.close();b.close();chk(h['stage_DB_pin']);chk(bp['MAIN_pin'])
result={'task':'T-0786','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'PASS_FINAL_EXACT_ACCESS_NOTE_SOURCE_AND_CONSEQUENCE','finalreadyforcanonical':True,'operation_pin':h['operation_pin'],'package_pin':h['package_pin'],'stage_DB_pin':h['stage_DB_pin'],'handoff_pin':pin(hp),'own_before_primary_freeze':pin(O/'own-bounded-access-classification-and-current-consequence-freeze-v1.json'),'own_exact_source_spec_review':pin(reviewp),'source_spec_pin':h['source_spec_pin'],'actual_state':{'journal_head':444,'pending':0},'actual_requests':[],'complete_actual_API_equals_personally_reviewed_source_API':True,'whole_stored_request_json_exact':True,'direct_SQL_old_tables':checks,'schema_exact':True,'source_and_record_heads_exact':True,'source_binding_and_two_ordered_evidence_edges_exact':True,'old_person_relations_OWNER_PK_reviews_paths_metadata_history_unchanged':True,'protected42_exact':True,'all50_and_derived_search_proof':h['full_all50_diff_pin'],'actual_target_support_pin':h['native_target_and_support_pin'],'validators':h['validators'],'both_verified_pedigrees_exact_443':True,'inventory_comparison':'All four shared fields format/note/active/all exact; preparation --full also carries persondetails and historicalmapping arrays while default stage carries detailhint. No wholeinventoryequality claim.','preserved_helper_failure':'v1 strict full inventory equality rejected different full/default output shape after all SQL validations; repaired v2 compares explicit same semantic aggregatefields. Prior script preserved; no DB writes or source amendment.','live_MAIN_unchanged_pin':bp['MAIN_pin'],'independent_source_consequence_judgment':'This exact one new search records dated limited access observations only, with unconfirmed candidateAIIa90, root-observed CAPTCHA/TLS403/robots and actual MCPquery scope. It adds no ownfamily/sourcecontent extraction and no person/sourceabsence, nondigitization or exhaustiveness finding. Exact prior source specification and own rawfreeze remain substantively correct; allcurrentgrades and strongerOWNER/sourceacceptedcredits retain. P0003failedPK05/waiting and P0007failedPK05/11/waiting remain. No individual runtime requests were generated, so no resolution needed.','outstanding_research':'Own Södertälje15 actualvolume/familyrow still unlocated/unread; T0786 promisedreading remains blockedpendingallowedaccess, not sourcecompleted by this approval. Maj1945–46 andFlen744 remainseparateT0789/T0788. No latestownerCAPTCHAanswer was supplied; anylateraccess requires additive reevaluation.','exposure_limits':'Ownaccessfreeze beforeprimary; newexternalHTTP/browserresults assessedfromrootpreservedobservations, not ownbrowser/imageinspection. PriorT0784wholecurrentreading reusedexactly; no repeated21PKreview or blanket858credit.','open_findings':[],'canonical_apply_authorized_by_this_agent':False,'actual_task_completion_approved':False,'usage':'UNKNOWN pending rootactualnewturncollector'}
out=O/'one-access-search-actual444-final-independent-source-consequence-gate-v1.json';assert not out.exists();out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(pin(out)))
