import json,pathlib,hashlib,sqlite3,datetime
B=pathlib.Path('evaluations/T-0784'); S=B/'root-authorized-exact-nine-stage-v1'; O=B/'independent-review'
def read(p):return json.loads(pathlib.Path(p).read_text())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def check(p):assert sha(p['path'])==p['sha256'];return p
def db(p):c=sqlite3.connect('file:'+str(pathlib.Path(p).resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
H=S/'complete-stage-result-and-Astra-handoff.json';h=read(H);prepath=O/'exact-nine-built-package-independent-pre-stage-source-consequence-gate-v1.json';pre=read(prepath)
assert sha(prepath)=='bb91b1700bf49d85b3f4572c2db8dd2ac9723c8ef663b16d11093f26fdeb6d03'
for k,v in h.items():
 if isinstance(v,dict) and 'path'in v and 'sha256'in v:check(v)
for v in h['validators']:check(v)
check(pre['operation_pin']);check(pre['own_complete_source_meaning_pin']);check(pre['source_spec_pin']);check(pre['baseline_pin'])
assert h['proposal_pin']==pre['proposal_pin'] and h['membership_pin']==pre['membership_pin']
stage=h['stage_DB_pin'];before=pin(stage['path']);c=db(stage['path']);basepath=B/'root-baseline-and-current-input-v1/baseline-j442.sqlite';b=db(basepath)
assert sha(basepath)=='2736bba18cfd3c2e9c160cd719e268b646667cdc8b9e3a55e55fb86db73e8148'
op=read(pre['operation_pin']['path']);oid=op['id'];stored=c.execute('select sequence,request_json from operation_payload where operation_id=?',(oid,)).fetchone();assert stored['sequence']==443 and json.loads(stored['request_json'])==op
assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==443
assert not c.execute('select 1 from review_request where operation_id=?',(oid,)).fetchone()
assert c.execute('select count(*) from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null').fetchone()[0]==0
assert read(h['actual_individual_request_pin']['path'])['requests']==[]
natives=read(h['all9_native_API_binding_pin']['path']);apirows=[]
for i,a in enumerate(op['changes']):
 rid=a['id']+'@'+str((a['expectedVersion'] or 0)+1);n=natives['objects'][rid]
 r=dict(c.execute('select * from revision where id=?',(rid,)).fetchone());actual={**r,'kind':c.execute('select kind from object where id=?',(a['id'],)).fetchone()[0]}
 actual['data']=dict(c.execute('select * from '+a['kind']+' where revision_id=?',(rid,)).fetchone())
 actual['origins']=[dict(x) for x in c.execute('select * from origin where revision_id=? order by rowid',(rid,))]
 actual['evidence']=[dict(x) for x in c.execute('select * from dependency where revision_id=? order by rowid',(rid,))]
 assert actual==n,(rid,'actual native mismatch')
 data={k:v for k,v in actual['data'].items() if k!='revision_id'}
 reconstructed={'id':a['id'],'kind':a['kind'],'expectedVersion':a['expectedVersion'],'data':data,'disposition':r['disposition'],'evidenceStatus':r['evidence_status'],'rationale':r['rationale'],'caveat':r['caveat'],'origins':[{'unit':e['unit_id'],'coverage':e['coverage'],'note':e['note']} for e in actual['origins']],'evidence':[{'object':e['basis_revision_id'].rsplit('@',1)[0],'version':int(e['basis_revision_id'].rsplit('@',1)[1]),'role':e['role'],'note':e['note']} for e in actual['evidence']]}
 assert reconstructed==a,(rid,'API mismatch')
 assert c.execute('select id from current_revision where object_id=?',(a['id'],)).fetchone()[0]==rid
 apirows.append({'revision_id':rid,'operation_pointer':f'/changes/{i}','direct_SQL_complete_native_equals_handoff':True,'whole_API_reconstructed_exact':True,'ordered_origins_and_evidence_exact':True,'current_head_exact':True})
# Whole schema and exact old-row order/values, excluding only recomputed object_search virtual/internal tables.
schema=lambda z:[tuple(x) for x in z.execute('select type,name,tbl_name,sql from sqlite_master order by type,name')]
assert schema(c)==schema(b)
names=[x[0] for x in b.execute("select name from sqlite_master where type='table' order by name")];tables=[]
allowed_append={'operation','operation_payload','object','revision','assessment','narrative','origin','dependency'}
for name in names:
 if name.startswith('object_search'):continue
 cols=[x[1] for x in b.execute('pragma table_info("'+name+'")')]
 try:
  old=[tuple(x) for x in b.execute('select rowid,* from "'+name+'" order by rowid')];new=[tuple(x) for x in c.execute('select rowid,* from "'+name+'" order by rowid')]
  assert new[:len(old)]==old,(name,'old row/order difference')
 except sqlite3.OperationalError:
  old=[tuple(x) for x in b.execute('select * from "'+name+'" order by '+','.join('"'+v+'"' for v in cols))];new=[tuple(x) for x in c.execute('select * from "'+name+'" order by '+','.join('"'+v+'"' for v in cols))];assert new==old
 if name not in allowed_append:assert new==old,(name,'unauthorized addition')
 tables.append({'table':name,'old_count':len(old),'actual_count':len(new),'all_existing_values_and_order_exact':True,'new_rows':len(new)-len(old)})
assert len(names)==50 and len(tables)==44
assert len(c.execute('select id from revision where operation_id=?',(oid,)).fetchall())==9
protected0=read(S/'protected42-before.json');protected1=read(S/'protected42-after.json');assert len(protected0)==42 and protected0==protected1
fullgates=read(O/'actual-stage-three-full-identity-gates-readonly-v1.json');targets={a['id'] for a in op['changes']}
def strip(v):
 if isinstance(v,list):return [strip(x) for x in v if not(isinstance(x,dict) and (x.get('object_id')in targets or x.get('id')in targets))]
 if isinstance(v,dict):return {k:strip(x) for k,x in v.items()}
 return v
gaterows=[]
for g in fullgates:
 p=g['person_id'];old=read(B/f'root-baseline-and-current-input-v1/{p}-whole-person-and-identity-gate-v1.json');view=read(S/f'{p}-full-person-current-review.json')
 assert strip(old['wholePerson'])==strip(view)
 assert g['life_picture_review']==old['identityGate']['life_picture_review']
 expected=('passed','supporting',True) if p=='P-0211' else ('failed','waiting',False)
 assert (g['identity_review']['outcome'],g['tree_effect']['outcome'],g['passed'])==expected
 for axis in ['identity_review','tree_effect']:assert g[axis]['source']=='native' and g[axis]['usable'] and not g[axis]['issues'] and len(g[axis]['ignored_assessments'])==1
 gaterows.append({'person_id':p,'actual_identity':expected[0],'actual_tree':expected[1],'actual_gate_passed':expected[2],'native_axes_usable_no_issues':True,'ignored_legacy':[x['revision_id'] for x in g['identity_review']['ignored_assessments']],'life_axis_entire_equal_baseline':True,'all_other_whole_person_view_content_exact_baseline_after_removing_only_nine_target_rows':True})
for f in ['verify.json','verify-assets.json','verify-source.json']:assert read(S/f)['ok'] is True
proof=read(S/'existing-native-history-order-and-narrow-derived-search-proof.json');assert proof['untouched_search_rows_exact'] and all(r['exact_current_domain_index_text'] for r in proof['touched_current_search_rows'])
assert set(x['object_id'] for x in proof['touched_current_search_rows'])==targets
c.close();b.close();assert pin(stage['path'])==before;check(pre['baseline_pin'])
result={'task':'T-0784','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'PASS_FINAL_EXACT_ACTUAL_STAGE_SOURCE_AND_CONSEQUENCE','finalreadyforcanonical':True,'operation_pin':pre['operation_pin'],'proposal_pin':pre['proposal_pin'],'membership_pin':pre['membership_pin'],'stage_DB_pin':stage,'handoff_pin':pin(H),'prior_own_complete_source_meaning_pin':pre['own_complete_source_meaning_pin'],'prior_own_exact_built_package_gate_pin':pin(prepath),'actual_three_full_gate_reading_pin':pin(O/'actual-stage-three-full-identity-gates-readonly-v1.json'),'baseline_physical_pin':pin(basepath),'live_MAIN_unchanged_pin':pre['baseline_pin'],'actual_journal':443,'actual_pending':0,'actual_requests':[],'individual_request_disposition':'No new requests exist in actual SQL or complete handoff; no individual resolution operation is necessary or approved.','actual_native_API_rows':apirows,'actual_semantic_axis_consequences':gaterows,'old_native_and_metadata_SQL_checks':tables,'schema_exact':True,'protected42_pin_before':pin(S/'protected42-before.json'),'protected42_pin_after':pin(S/'protected42-after.json'),'protected42_exact':True,'actual_context_pin':h['actual_request_context_native_pin'],'old_context_equality_pin':h['old_context_baseline_equality_pin'],'derived_search_proof_pin':pin(S/'existing-native-history-order-and-narrow-derived-search-proof.json'),'validators':h['validators'],'source_consequence_judgment':pre['source_consequence_conclusion'],'method_and_exposure':'Reuse own whole current21/three-person, stronger-source and three-copy readings through verified complete actual API equality. Native current views retain all other semantics exactly. Initial Arne judgement and its reasoned PK05 amendment remain preserved; unsolicited prefreeze metadata exposure limits remain explicit. No new original or independent evidence voice, no whole1214 reading claim.','scope_boundaries':['Evy identity/tree approval permits her gate only, no relation or other-person upgrade.','Arne PK05 precise already-used own C0882 continuation15 remains; sufficient completed own sources/graves credited and Bernhard OWNER_CONFIRMED untouched.','Maj PK05 own15/1945-46 and used744 field extraction plus PK11 used744r9-10 preservation remain exact; wider parent-task four images are not automatically her gate.','Native axes leave historical failed full-contract/life scope and exact old PK payloads intact. Maj copy remedies do not assert continuous residence or guaranteed access.','Existing task owners retained; no new scheduling mandate.'],'open_findings':[],'runtime_or_canonical_apply_authorized_by_this_agent':False,'canonical_actual_acceptance':False,'next':'Root fresh main baseline and controlled apply of this exact one-operation/nine-target package, then actual canonical result comparison and task acceptance.','usage':'UNKNOWN; root collects actual new-turn worker usage after final.'}
out=O/'exact-nine-actual-stage-final-independent-source-consequence-gate-v1.json';assert not out.exists();out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(pin(out)));print('PASS: direct SQL9 fullnative/API, 44 old tables ordered intact (six search tables separately verified), current3 gates+wholeview retains, actual443/0 no requests.')
