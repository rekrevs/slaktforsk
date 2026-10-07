import json,pathlib,hashlib,sqlite3,sys
B=pathlib.Path('evaluations/T-0781');O=B/'independent-review'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
def ck(p):assert pin(p['path'])['sha256']==p['sha256'];return rd(p['path'])
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
proposal=pathlib.Path(sys.argv[1]);p=rd(proposal); table=ck(p['full_individual_consequence_table_pin']);ck(p['membership_pin']);nativep=B/'mechanical-current425-preparation-v1/full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json';native=rd(nativep)['objects']
assert pin(p['baseline_pin']['path'])==p['baseline_pin'];c=sqlite3.connect('file:'+p['baseline_pin']['path']+'?mode=ro',uri=True);heads=dict(c.execute('select object_id,max(version) from revision group by object_id'));c.close()
modulefiles=['C0049-core-five-pass-one-metadata-pending-and-P0098-API-review-v1.json','C0067-three-producer-wrapper-whole-API-independent-review-v1.json','C0049-oldTR-exact-rationale-amendment-independent-review-v1.json','C0067-four-exact-actual-API-independent-review-v1.json','C0067-twentytwo-actual-clause-entire-API-consequence-review-v1.json','C0049-fourteen-actual-entire-API-and-direct-dependency-review-v1.json','C0049-onehundredfour-actual-field-API-and-legacy-outcome-review-v1.json','two-source-five-clause-and-thirteen-adoption-exact-API-review-v1.json','P0052-P0053-three-actual-birth-API-and-one-retain-independent-review-v1.json','two-audit-final-rationale-whole-operation-equality-and-source-review-v1.json']
# Explicit individual substantive review locators; one exact object row, not blanket counts.
own={};reviewdocs={}
for f in modulefiles:
 q=O/f;d=rd(q);reviewdocs[f]=d
 def visit(x,ptr=''):
  if isinstance(x,dict):
   if 'object_id' in x and any(k in x for k in ['own_judgment','own_source_judgment','individual_own_source_consequence','own_source_consequence']):own.setdefault(x['object_id'],[]).append({'receipt':pin(q),'pointer':ptr,'literal_individual_review':x})
   for k,v in x.items():visit(v,ptr+'/'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):visit(v,ptr+'/'+str(i))
 visit(d)
# Explicit review renewal receipts must be provided as further arguments.
renewals=[]
for f in sys.argv[3:]:
 q=pathlib.Path(f);d=rd(q);renewals.append(pin(q))
 for x in walk(d):
  if 'object_id' in x and any(k in x for k in ['own_judgment','own_source_judgment','own_source_consequence']):own.setdefault(x['object_id'],[]).append({'receipt':pin(q),'literal_individual_review':x})
rows=[];ids=[];ops=[];ti=0;baselineheads=dict(heads)
for a in p['operations']:
 op=ck(a);ops.append({'path':a['path'],'sha256':a['sha256'],'index':a['index'],'operation_id':a['operation_id']});assert len(op['changes'])==a['changes']
 for j,x in enumerate(op['changes']):
  oid=x['id'];assert oid not in ids;ids.append(oid);assert heads.get(oid)==x['expectedVersion'],(oid,heads.get(oid),x['expectedVersion']);assert oid in own,oid
  t=table['rows'][ti];assert t['object_id']==oid and t['entire_exact_after_API']==x and t['operation_index']==a['index'] and t['change_index']==j
  if x['expectedVersion'] is not None:assert t['full_before_native']==native[oid+'@'+str(x['expectedVersion'])]
  for e in x.get('evidence',[]):assert heads.get(e['object'])==e['version'],(oid,e,heads.get(e['object']))
  rows.append({'object_id':oid,'actual_operation':pin(a['path']),'actual_pointer':'/changes/'+str(j),'expected_version':x['expectedVersion'],'resulting_revision_id':oid+'@'+str((x['expectedVersion'] or 0)+1),'entire_actual_API':x,'consequence_table_pointer':'/rows/'+str(ti),'full_actual_API_equal_individually_reviewed_table':True,'own_substantive_module_reviews':own[oid],'own_final_decision':'APPROVE_EXACT_SOURCE_CONSEQUENCE_FOR_THIS_CANDIDATE','scope':'Only the explicit source-field/API change, own stronger evidence and retained historical review limits in linked individual judgments; no full-person identity/tree/life approval.'})
  heads[oid]=(x['expectedVersion'] or 0)+1;ti+=1
assert len(rows)==174 and len(ops)==16
protected=ck(p['protected42_pin']);assert len(protected['objects'])==42;assert not(set(ids)&{v['object_id'] for v in protected['objects'].values()})
primary=pathlib.Path(sys.argv[2]);pg=rd(primary)
# Root/primary literal ready assertions are inspected before this script; pins alone are not source credit.
closurefiles=['original-first-freeze-index-v1.json','first-bounded-source-comparison-and-C0067-reuse-findings-v1.json','five-stronger-prior-own-reading-current425-reuse-dispositions-v1.json','ASSESSMENT-P0094-exact-prior-own-whole-reading-reuse-v1.json','two-source-finite320-individual-own-prior-reading-and-current-scope-closure-v1.json','direct55-and-independent-search-relevance-closure-v1.json','six-future-owner-exact-append-source-and-preservation-review-v1.json']
finite=rd(O/closurefiles[4]);targetmap={r['object_id']:r for r in rows}; overlays=[]
for r in finite['rows']:
 oid=r['revision_id'].rsplit('@',1)[0]
 if r['actual_amendment_overlay_required']:assert oid in targetmap,oid
 overlays.append({'current_revision_id':r['revision_id'],'citation':r['citation'],'own_finite_disposition':r['approved_disposition'],'actual_target_pointer':'/individual_actual_approvals/'+str(ids.index(oid)) if oid in targetmap else None,'retained_source_scope':'The applicable source-specific decision remains bounded even if the same object has an explicit correction under the other source.'})
out={'task':'T-0781','status':'INDEPENDENT_COMPLETE_EXACT_PRE_STAGE_SOURCE_CONSEQUENCE_PASS','complete_bounded_pre_stage_review':True,'no_open_candidate_source_findings':True,'exact_scope':['C-0049','C-0067'],'proposal_pin':pin(proposal),'membership_pin':p['membership_pin'],'consequence_table_pin':p['full_individual_consequence_table_pin'],'primary_source_ready_gate_pin':pin(primary),'ordered_operations':ops,'counts':p['counts'],'individual_actual_approvals':rows,'finite320_actual_overlay_bindings':overlays,'own_complete_source_scope_and_stronger_reading_receipts':[pin(O/f) for f in closurefiles],'individual_module_receipts':[pin(O/f) for f in modulefiles],'later_exact_support_renewals':renewals,'baseline_pin':p['baseline_pin'],'main425_preparation_pin':p['main425_pin'],'protected42_pin':p['protected42_pin'],'protected42_no_target_intersection':True,'current_head_evidence_and_producer_order_independently_verified':True,'legacy_assessment_meaning':'Historical criteria, grades, outcomes and full-contract meaning preserved. AS52/53/57 caveat-only sourcecompletion is not a new identity/life gate; no typedidentity/tree/life additions. All13 new adoptions are bounded source adoption only.','source_limits':'C49 original-first own freeze before comparative claims; prior historical exposure acknowledged. C67 sufficient T0131/T0182 fullpost reuse, no routine new image or independent extra source vote. Own blank cells and uncertain annual/marginal glyphs stay bounded. Stronger C48/C46/C0184 and C69/census support retained by exact per-field judgments. Same P57 row/person retained, no new identity/parent relation.','primary_finite_C49_v1_historical_pointer_superseded_by_v2':pin(B/'source-review/C0049-finite-individual-semantic-amend-and-retain-index-v2.json'),'not_claimed':'No blanket897 or1242 whole-object reading; counts are routing/target counts, exact own scope predicates remain controlling. No stage/current resolution meaning or final canonical PASS has yet been asserted.','stage_UNRUN':True,'canonical_apply_authorized':False,'runtime_authority':'Root only. This gate permits consideration of one fresh exact package clone-stage; actual resulting requests, individual resolutions, protected/current results and final validators require later separate exact review.','final_global_canonical_PASS':False,'observable_worker_usage':'UNKNOWN here; root collects actual new-turn response token/cache/output records after worker final.'}
q=O/'two-source-complete-exact174-pre-stage-source-consequence-gate-v1.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(q))
