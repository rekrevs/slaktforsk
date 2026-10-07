import json,hashlib,pathlib,sqlite3,datetime
B=pathlib.Path('evaluations/T-0784'); D=B/'implementation/exact-nine-settled-draft-v1'; O=B/'independent-review'
def read(p):return json.loads(pathlib.Path(p).read_text())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def jsha(j):return hashlib.sha256(json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def checkpin(p):assert sha(p['path'])==p['sha256'];return p
opfile=D/'01-exact-nine-source-settled-operation-v1.json'; propfile=D/'exact-nine-stage-ready-proposal-v1.json'; memfile=D/'exact-nine-ordered-operation-membership-v1.json'; ownfile=O/'exact-nine-source-API-meaning-and-copy-consequence-review-v1.json'
op=read(opfile);prop=read(propfile);mem=read(memfile);own=read(ownfile)
assert sha(opfile)=='00841fa152f65e6f195725f17b66be60be270441f478147985543d8a7d30baff'
assert sha(propfile)=='fd438f10ba90901ab1171868c00e8acebb86de19979bcc1c64b3d0ac393b3ee9'
assert sha(memfile)=='33afa563644ee34c07147006cae92e4e7a54dfd92871611dac84dad94ff8c176'
assert sha(ownfile)=='1b8b49ebe3d06429f750bb239d079d6d0eb986608a25d5f6a0c56d8c32b54fe5'
for p in [prop['membership_pin'],prop['source_spec_pin'],prop['mechanical_guard_pin'],*prop['operations'],own['source_spec'],own['source_freeze'],own['dictionary'],*own['own_frozen_and_comparative']]:checkpin(p)
spec=read(own['source_spec']['path']); guard=read(prop['mechanical_guard_pin']['path']); dictionary=read(own['dictionary']['path'])['objects']
S={x['object_id']:x for x in spec['specifications']};R={x['object_id']:x for x in own['rows']}
assert [x['id'] for x in op['changes']]==mem['targets']==own['required_order']==guard['required_order']
assert len(op['changes'])==9 and len(prop['operations'])==1 and prop['operations']==mem['operations']
assert op['dependencyReviewVersion']==2 and op.get('resolves',[])==[]
assert set(op)=={'id','actor','reason','dependencyReviewVersion','changes'}
main=pathlib.Path('genealogy2/data/research.sqlite'); before=pin(main);assert before==guard['MAIN_pin']
c=sqlite3.connect('file:'+str(main.resolve())+'?mode=ro',uri=True)
assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==442
assert c.execute('select count(*) from review_request q left join review_resolution r on r.request_id=q.id where r.request_id is null').fetchone()[0]==0
heads=dict(c.execute('select object_id,max(version) from revision group by object_id'))
rows=[]
for i,api in enumerate(op['changes']):
 oid=api['id'];s=S[oid];r=R[oid];g=guard['rows'][i]
 assert api==s['full_new_API']==g['NEW_exact_source_API']
 assert jsha(api)==r['whole_spec_API_sha256'] and r['entire_API_semantics_reviewed']
 expected=api['expectedVersion'];assert heads.get(oid)==expected
 incoming=[]
 if expected is not None:
  assert g['OLD_native']==dictionary[oid+'@'+str(expected)]
  incoming=list(c.execute('select d.revision_id,d.basis_revision_id,d.role,d.note from dependency d join revision r on r.id=d.basis_revision_id where r.object_id=? order by d.rowid',(oid,)))
  assert incoming==g['incoming_all_history']==[]
 else:assert not c.execute('select 1 from object where id=?',(oid,)).fetchone()
 edges=[]
 for e in api.get('evidence',[]):
  assert heads[e['object']]==e['version'];edges.append({'object':e['object'],'version':e['version'],'sequential_current_head_exact':True})
 heads[oid]=(expected or 0)+1
 rows.append({'operation_pointer':f'/changes/{i}','object_id':oid,'expected_version':expected,'whole_API_sha256':jsha(api),'own_meaning_pointer':f"/rows/{r['index']}",'source_API_pointer':r['whole_API_pointer'],'whole_API_exact_own_approved':True,'incoming_all_history':incoming,'ordered_support_current_head_checks':edges})
c.close();assert pin(main)==before
result={'task':'T-0784','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'PASS_EXACT_BUILT_PACKAGE_PRE_STAGE_SOURCE_AND_CONSEQUENCE','ready_for_stage':True,'operation_pin':pin(opfile),'proposal_pin':pin(propfile),'membership_pin':pin(memfile),'own_complete_source_meaning_pin':pin(ownfile),'source_spec_pin':own['source_spec'],'mechanical_guard_pin':prop['mechanical_guard_pin'],'baseline_pin':before,'baseline_journal':442,'baseline_pending':0,'rows':rows,'source_consequence_conclusion':{'P-0211':'identity passed / tree supporting; all seven identity requirements individually satisfied by already accepted sources. No new source vote or relation upgrade.','P-0003':'identity failed / tree waiting; only PK05 direct already-used C0882 continuation to own parish-book15 remains. All old accepted full-source and grave credits retained; Bernhard OWNER_CONFIRMED unchanged.','P-0007':'identity failed / tree waiting; PK05 exact own passage15/1945-46 and used Flen744 columns, PK11 preservation of actually used744r9-10. No automatic requirement for every mother-task folio. All three current-copy findings precisely corrected.','historical_and_stronger':'Three copies retain all other fields, evidence order and historical limitations under own prior complete reconstruction. Six distinct identity/tree reviews supersede gate effect only; persons, relations, OWNER, 21 prior PK payloads, legacy and life reviews not mutated. Necessary later stronger support and accepted family correlations reused, not new evidence.','dependencies':'Direct read-only SQL confirms zero all-history incoming to three revised copies; every submitted ordered support matches actual baseline head or an earlier exact producer. No inferred resolutions or support rebinds.'},'method':'Complete prior own current21/three-person readings, stronger support and source-spec meaning reused through exact whole-API equality. Exposure limits and preserved initial/amended Arne judgments remain in pinned own receipts. No new original reading; no blanket1214 credit.','open_findings':[],'runtime_authorization':False,'actual_stage_review_complete':False,'final_global_or_canonical_approval':False,'next_required':'Root stage authorization and exact fresh-clone application, full current/protected/history/metadata/validator result assessment, any actual individual dependency requests, then separate final source/consequence gate.','production_usage':'UNKNOWN pending root actual usage collector','preserved_preparation_failure':'v1 mistakenly asserted operation table count442; actual443 includes historical pilot without operation_payload. No writes occurred. v2 explicitly checks native journal max(sequence)442; baseline hash identical throughout.'}
out=O/'exact-nine-built-package-independent-pre-stage-source-consequence-gate-v1.json';assert not out.exists();out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(pin(out)));print('All9 exact own/source APIs, all sequential support versions, zero history incoming and unchanged MAIN442/0 verified.')
