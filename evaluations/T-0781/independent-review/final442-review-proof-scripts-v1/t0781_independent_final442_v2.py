import json,pathlib,hashlib,sqlite3,datetime
B=pathlib.Path('evaluations/T-0781');S=B/'exact16-fresh-stage-v1';F=S/'actual17-resolution-apply-v1';O=B/'independent-review'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
def check(p):assert pin(p['path'])['sha256']==p['sha256'],p;return rd(p['path']) if p['path'].endswith('.json') else None
def con(p):c=sqlite3.connect(pathlib.Path(p).resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
def native(c,rid):
 x=dict(c.execute('select r.*,o.kind from revision r join object o on r.object_id=o.id where r.id=?',(rid,)).fetchone());x['data']=dict(c.execute('select * from '+x['kind']+' where revision_id=?',(rid,)).fetchone())
 for k,t in [('origins','origin'),('evidence','dependency')]+([('assets','record_asset'),('media','record_media')] if x['kind']=='record' else []):x[k]=[dict(r) for r in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return x
def api(n):
 d={k:(json.loads(v) if k.endswith('_json') and isinstance(v,str) else v) for k,v in n['data'].items() if k!='revision_id'}
 a={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version']-1 or None,'data':d,'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat'],'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in n['origins']],'evidence':[{'object':r['basis_revision_id'].rsplit('@',1)[0],'version':int(r['basis_revision_id'].rsplit('@',1)[1]),'role':r['role'],'note':r['note']} for r in n['evidence']]}
 if n['kind']=='record':a['assets']=[{'path':r['asset_path'],'region':r['region']} for r in n['assets']];a['media']=[{'id':r['asset_id'],'region':r['region']} for r in n['media']]
 return a
h=rd(F/'complete-final442-zero-pending-exact17-resolution-stage-handoff-v1.json')
for v in h.values():
 if isinstance(v,dict) and 'path' in v and 'sha256' in v:check(v)
for v in h['validator_pins']:check(v)
g=rd(O/'two-source-complete-exact174-pre-stage-source-consequence-gate-v1.json');own17=rd(O/'actual17-complete-independent-pre-resolution-meaning-and-instruction-gate-v1.json')
m=check(h['final17_membership_pin']);steps=check(h['actual_all17_step_state_index_pin']);ctx=check(h['all398_native_context_pin']);prot=check(h['protected42_pin'])['objects'];op=check(h['resolution_operation_pin'])
a=con(h['original_stage441_snapshot_pin']['path']);z=con(h['final_stage_DB_pin']['path']);main=con(h['main_pin']['path'])
schema=lambda c:[tuple(r) for r in c.execute('select type,name,tbl_name,sql from sqlite_master order by type,name')]
assert schema(a)==schema(z)
tables=[r[0] for r in z.execute("select name from sqlite_master where type='table' order by name")];assert len(tables)==50
ordering={}
def rows(c,t):
 schema_sql=c.execute("select sql from sqlite_master where type='table' and name=?",(t,)).fetchone()[0]
 if 'WITHOUT ROWID' in schema_sql.upper():
  cols=[r[1] for r in sorted(c.execute('pragma table_info("'+t+'")').fetchall(),key=lambda r:r[5]) if r[5]]
  ordering[t]={'physical_rowid':False,'declared_primary_key_order':cols}
  query='select * from "'+t+'" order by '+','.join('"'+v+'"' for v in cols)
 else:
  ordering[t]={'physical_rowid':True,'order':'rowid'};query='select rowid,* from "'+t+'" order by rowid'
 return [tuple(r) for r in c.execute(query)]
unchanged=[];appended=[]
for t in tables:
 ar=rows(a,t);zr=rows(z,t)
 if t in ['operation','operation_payload','review_resolution']:
  assert zr[:len(ar)]==ar,t
  expected=17 if t=='review_resolution' else 1;assert len(zr)-len(ar)==expected
  appended.append({'table':t,'old_rows':len(ar),'appended_rows':expected,'entire_old_rows_including_rowids_prefix_exact':True})
 else:assert ar==zr,t;unchanged.append({'table':t,'rows':len(ar),'entire_rows_and_declared_order_exact':True,'ordering':ordering[t]})
assert len(unchanged)==47
pending=lambda c:c.execute('select count(*) from review_request q left join review_resolution r on q.id=r.request_id where r.request_id is null').fetchone()[0]
head=lambda c:c.execute('select max(sequence) from operation_payload').fetchone()[0]
assert (head(a),pending(a))==(441,17);assert (head(z),pending(z))==(442,0);assert (head(main),pending(main))==(425,0)
assert len(ctx['objects'])==398
for rid,n in ctx['objects'].items():assert native(a,rid)==native(z,rid)==n,rid
actual174=[]
for i,r in enumerate(g['individual_actual_approvals']):
 n=native(z,r['resulting_revision_id']);assert api(n)==r['entire_actual_API'],r['object_id']
 assert z.execute('select max(version) from revision where object_id=?',(r['object_id'],)).fetchone()[0]==n['version']
 actual174.append({'revision_id':n['id'],'own_source_API_pointer':'/individual_actual_approvals/'+str(i),'entire_actual_API_equal':True,'current_version_equal':True})
assert len(actual174)==174
for rid,n in prot.items():assert native(z,rid)==native(a,rid)==native(main,rid)==n
assert len(prot)==42
assert len(m['operations'])==17;assert len(steps['steps'])==17
assert [{k:r[k] for k in ['path','sha256','operation_id']} for r in m['operations'][:16]]==[{k:r[k] for k in ['path','sha256','operation_id']} for r in g['ordered_operations']]
ops=[];prev={'journal_head':425,'pending':0}
for i,(r,st) in enumerate(zip(m['operations'],steps['steps'])):
 raw=check(r);stored=dict(z.execute('select * from operation_payload where sequence=?',(426+i,)).fetchone());assert json.loads(stored['request_json'])==raw;assert stored['operation_id']==r['operation_id']==st['operation_id']
 sr=check(st['actual_step_receipt_pin']);assert sr['before']==st['expected_before']==prev;assert sr['after']==st['expected_after'];assert sr['operation_pin']=={'path':r['path'],'sha256':r['sha256']};prev=sr['after']
 ops.append({'index':i+1,'path':r['path'],'sha256':r['sha256'],'operation_id':r['operation_id'],'actual_sequence':426+i,'entire_stored_request_JSON_exact':True,'actual_step_receipt_pin':st['actual_step_receipt_pin']})
assert prev=={'journal_head':442,'pending':0};assert op['changes']==[] and op['dependencyReviewVersion']==2
stored17=[dict(r) for r in z.execute('select rowid as native_rowid,* from review_resolution where operation_id=? order by rowid',(op['id'],))]
assert stored17==check(h['stored17_resolution_pin']);assert op['resolve']==[r['approved_resolution_instruction'] for r in own17['rows']];assert len(stored17)==17
resolution_rows=[]
for i,(r,n) in enumerate(zip(own17['rows'],stored17)):
 assert n['request_id']==r['request_id']==op['resolve'][i]['request'];assert n['rationale']==r['approved_resolution_instruction']['rationale'];assert n['operation_id']==op['id']
 assert dict(z.execute('select * from review_request where id=?',(r['request_id'],)).fetchone())==r['actual_request']
 rid=r['retained_current_revision_id'];o,v=rid.rsplit('@',1);assert z.execute('select max(version) from revision where object_id=?',(o,)).fetchone()[0]==int(v)
 resolution_rows.append({'request_id':r['request_id'],'retained_current_revision_id':rid,'native_rowid':n['native_rowid'],'approved_resolution_instruction':r['approved_resolution_instruction'],'own_frozen_decision':r['own_frozen_decision'],'own_source_scope':r['own_frozen_rationale'],'own_meaning_gate_pointer':'/rows/'+str(i),'entire_literal_and_order_exact':True,'actual_request_and_current_revision_exact':True})
val=[]
for v in h['validator_pins']:
 d=check(v);p=pathlib.Path(v['path']);pr=rd(p.with_name(p.stem+'.process.json'));assert pr['returncode']==0;check(pr['stdout_pin']);check(pr['stderr_pin'])
 if p.stem.startswith('verify'):assert d['ok'] is True
 assert pin(S/p.name)['sha256']==v['sha256']
 val.append({'result_pin':v,'process_pin':pin(p.with_name(p.stem+'.process.json')),'returncode':0,'entire_result_equal_pre_resolution441':True})
for c in [a,z,main]:c.close()
for k in ['final_stage_DB_pin','original_stage441_snapshot_pin','main_pin']:check(h[k])
primary=B/'source-review/two-source-complete-exact17-final-primary-source-consequence-gate-v1.json';pg=rd(primary);assert pg['stage_DB_pin']==h['final_stage_DB_pin'];assert pg['membership_pin']==h['final17_membership_pin']
proof={'task':'T-0781','status':'DIRECT_READONLY_FINAL442_ENTIRE_STATE_AND_APPROVED_PACKAGE_BINDING_PASS','final_stage_handoff_pin':pin(F/'complete-final442-zero-pending-exact17-resolution-stage-handoff-v1.json'),'stage_DB_pin':h['final_stage_DB_pin'],'historical441_snapshot_pin':h['original_stage441_snapshot_pin'],'actual_journal':442,'actual_pending':0,'main_pin_checked_unchanged':h['main_pin'],'main_journal':425,'main_pending':0,'method':'Own sqlite3 connections to absolute file URIs with mode=ro. All50 tables compared:46 tables preserve physical rowid and row order; four WITHOUT ROWID FTS index/config tables compare every row in declared primary-key order, explicitly listed. Schema exact. No evidence/origin/asset/media sorting. All398 complete native objects with original source strings and ordered arrays; actual174 entire API reconstructed exactly against own individual approvals with zero omitted fields or implicit defaults. Mechanical equality carries prior sufficient source judgments and does not claim new whole398 semantic reading.','schema_exact':True,'all47_entire_tables_including_rowids_exact':unchanged,'only_three_exact_prefix_appends':appended,'all398_entire_native_payloads_equal_own_earlier_context':True,'all174_individual_exact_API':actual174,'all42_protected_entire_native_current_equal':True,'ordered17_exact_stored_operation_APIs':ops,'all17_individual_actual_resolutions':resolution_rows,'validators':val,'control_representation':'Explicit dependencyReviewVersion numeric2 matches input and stored entire request JSON; no added defaults or altered resolution semantics.','own_SQL_open_failures':[],'preserved_helper_attempt':'Initial v1 comparison stopped before writes on four WITHOUT ROWID FTS index/config tables; v2 explicitly compares those by declared primary keys and preserves physical rowids for46 other tables. No source/API or runtime change.','writes_to_databases':False}
pp=O/'final442-direct-readonly-native-protected-literal17-and-package-proof-v1.json';assert not pp.exists();pp.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
receipts=['two-source-complete-exact174-pre-stage-source-consequence-gate-v1.json','actual174-native-protected-history-and-complete-result-binding-v1.json','actual17-independent-own-source-consequence-freeze-v1.json','actual17-complete-independent-pre-resolution-meaning-and-instruction-gate-v1.json','exact-built17-resolution-and-complete17-member-preapply-review-v1.json','two-source-finite320-individual-own-prior-reading-and-current-scope-closure-v1.json','direct55-and-independent-search-relevance-closure-v1.json','five-stronger-prior-own-reading-current425-reuse-dispositions-v1.json','ASSESSMENT-P0094-exact-prior-own-whole-reading-reuse-v1.json','six-future-owner-exact-append-source-and-preservation-review-v1.json','two-audit-final-rationale-whole-operation-equality-and-source-review-v1.json','ten-exact-support-version-actual-API-independent-review-v1.json','original-first-freeze-index-v1.json','C0049-original-first-whole-entry-reading-freeze-v1.json']
for name in receipts:assert (O/name).exists(),name
out={'task':'T-0781','status':'INDEPENDENT_COMPLETE_EXACT17_ACTUAL442_SOURCE_CONSEQUENCE_GLOBAL_PASS','final_complete_package_PASS':True,'source_consequence_global_PASS':True,'independent_final_ready':True,'scope':['C-0049','C-0067'],'stage_DB_pin':h['final_stage_DB_pin'],'actual_stage_journal':442,'actual_stage_pending':0,'proposal_pin':h['final17_proposal_pin'],'membership_pin':h['final17_membership_pin'],'ordered_operations':ops,'native_changes':174,'native_revisions':157,'new_native_objects':17,'resolution_count':17,'individual_actual_resolution_approvals':resolution_rows,'all174_individual_source_approval_pin':pin(O/receipts[0]),'own_final_direct_SQL_proof_pin':pin(pp),'prior_sufficient_own_review_chain':[pin(O/n) for n in receipts],'primary_final_source_gate_pin':pin(primary),'final_stage_handoff_pin':pin(F/'complete-final442-zero-pending-exact17-resolution-stage-handoff-v1.json'),'source_consequence_judgment':'PASS for the complete exact package: the actual174 source changes realize my individually reviewed source-bound corrections, current semantic retains and stronger-support dispositions; every actual17 request has the separately frozen and subsequently compared individual meaning and literal resolution. Ten historical consumers are already superseded; seven retain their justified current conclusions and explicit old bases. Zero pending is substantively justified by those17 decisions, not by validator success alone. Actual resolution application adds only the approved17 reasons plus journal metadata; all47 knowledge/search/history tables, all398 context payloads, all174 approved APIs and42 protected objects remain exact. No source interpretation, stronger support, uncertainty, outcome or adoption scope changes at resolution.','settled_source_boundaries':{'C0049':'Own original-first full sixfamily-row/header/column/ditto/blank/margin reading frozen before newprimary/current claims; historical repository exposure acknowledged, no retrospective blindness. Lower2 separated context rows add no people/source units. Magdalena Euphrosyne29May1863 with own B:å; three younger own birthplace cells blank. Annual F/N entries, reserved1867glyph and marriageglyph remain row/time bounded; stronger C0184 marriage5July1860 retained; no continuous physical residence/lifetime-childtotal inference.','birth_places':'P52 structured Bygdeå retained from explicit older C46 with its own caveat/support, not filled from C49blank. P53 false inherited ditto removed to null, not geographical counterproof. EP53 exact approved E53 rebind, EP52 individual old-basis retain.','C0067':'Sufficient T0131/T0182 wholepost prior research reused; no new image or invented independent reading. 8Feb birth/11Feb baptism1872, q./(4)/ages and witness/place/initial reservations preserved. Three Ultervattnet witnesses plus separately reserved fourth place; no proved childrank/familytotal, forced initial expansion, identity/kinship/age or guaranteed unread-route content/cost/access.','stronger_older_support':'C69 wholepost and C48 T0110/post78 source-specific own prior judgments remain applicable and exact; no import of wrong post79 or independent evidence voice. Earlier supported parent dates remain stronger than later age statements. All immutable older versions and support metadata preserved.','review_state':'42 protected OWNER/identity/tree/life objects exact. Legacy assessment criteria/data/outcomes retain historical full-contract meaning; caveat-only source completion is not a new identity/life approval. P57 accepted TRANSCRIBED identity retained, no restored historical CORROBORATED upgrade or duplicate person.','adoption':'13 source-bounded native adoptions (sixC49/sevenC67) are approved at task scope; no fullperson/identity/tree/life contract upgrade or source-exhaustion claim.','finite_coverage':'Own320 individual finite source-scoped dispositions, direct55 wholecurrent readings and independent390 routing/relevance closure with73 outside contexts remain bound. Primary897 exclusion/routing scope is consistent but neither whole897 nor whole398 semantic reading credit is claimed.'},'future_six':'Exact six existing-owner appendtexts remain independently approved by the pinned own receipt; preserve whole original log prefix/status/after/AC and exclusions, no new IDs/tasks or task-per-glyph. Execution only after actual two-source acceptance and root authorization; no Wotan changes made here.','derived_views':'All five final validator outputs equal pre-resolution441 outputs; default verified pedigree and inventory are bound without interpreting task/source completion or pending0 as new identity/life/person approval.','historical_pin_mapping':{'historical_stage_path':str(S/'stage.sqlite'),'historical_sha256':h['original_stage441_snapshot_pin']['sha256'],'immutable_original441_snapshot_pin':h['original_stage441_snapshot_pin'],'interpretation':'Earlier441/17 gate pins are historical preconditions whose exact bytes survive in this snapshot. They are not current stage hashes and no earlier gate is rewritten.'},'findings_open':[],'current_semantic_findings_open':[],'runtime_authorized':False,'canonical_apply_authorized':False,'canonical_already_applied':False,'task_or_program_accepted':False,'root_next_condition':'Root alone checks fresh main425/0 baseline and exact17 ordered files, authorizes controlled canonical CLI apply, compares actual main with this reviewed442/0 stage and records acceptance. No database replacement.','main_pin_observed_unchanged':h['main_pin'],'production_usage':{'new_turn_input_tokens':'UNKNOWN','new_turn_cached_input_tokens':'UNKNOWN','new_turn_output_tokens':'UNKNOWN','note':'No observable worker usage metadata in these tools. Root collects actual new-turn session records after final response; unknown is not zero.'},'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
q=O/'two-source-complete-exact17-final-independent-source-consequence-global-gate-v1.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'proof':pin(pp),'final_gate':pin(q),'actual_stage':[442,0],'unchanged_tables':len(unchanged),'individual_resolutions':len(resolution_rows)},indent=2))
