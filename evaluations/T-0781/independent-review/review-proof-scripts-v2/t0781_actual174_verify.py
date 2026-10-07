import json,pathlib,hashlib,sqlite3,copy
B=pathlib.Path('evaluations/T-0781');S=B/'exact16-fresh-stage-v1';O=B/'independent-review'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
def con(p):c=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
def native(c,rid):
 x=dict(c.execute('select r.*,o.kind from revision r join object o on r.object_id=o.id where r.id=?',(rid,)).fetchone());x['data']=dict(c.execute('select * from '+x['kind']+' where revision_id=?',(rid,)).fetchone())
 for k,t in [('origins','origin'),('evidence','dependency')]+([('assets','record_asset'),('media','record_media')] if x['kind']=='record' else []):x[k]=[dict(r) for r in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return x
def api(n):
 d={k:(json.loads(v) if k.endswith('_json') and isinstance(v,str) else v) for k,v in n['data'].items() if k!='revision_id'}
 a={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version']-1 or None,'data':d,'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat'],'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in n['origins']],'evidence':[{'object':r['basis_revision_id'].rsplit('@',1)[0],'version':int(r['basis_revision_id'].rsplit('@',1)[1]),'role':r['role'],'note':r['note']} for r in n['evidence']]}
 if n['kind']=='record':a['assets']=[{'path':r['asset_path'],'region':r['region']} for r in n['assets']];a['media']=[{'id':r['asset_id'],'region':r['region']} for r in n['media']]
 return a
h=rd(S/'complete-stage-result-and-Astra-handoff.json');assert pin(S/'stage.sqlite')==h['stage_DB_pin'];g=rd(O/'two-source-complete-exact174-pre-stage-source-consequence-gate-v1.json');p=rd(g['proposal_pin']['path']);ctx=rd(h['actual_request_context_native_pin']['path']);b=con(p['baseline_pin']['path']);s=con(S/'stage.sqlite');rows=[];defaults=[];old=[]
for i,r in enumerate(g['individual_actual_approvals']):
 rid=r['resulting_revision_id'];x=native(s,rid);assert x==ctx['objects'][rid];a=api(x);e=copy.deepcopy(r['entire_actual_API']);ds=[]
 for k,v in [('origins',[]),('evidence',[]),('evidenceStatus',None),('caveat','')]:
  if k not in e:e[k]=v;ds.append({'path':'/'+k,'value':v})
 for k in a['data']:
  if k not in e['data']:e['data'][k]=None;ds.append({'path':'/data/'+k,'value':None})
 if e['kind']=='record':
  for k in ['assets','media']:
   if k not in e:e[k]=[];ds.append({'path':'/'+k,'value':[]})
 assert e==a,(rid,e,a)
 assert x['previous_id']==(r['object_id']+'@'+str(r['expected_version']) if r['expected_version'] else None)
 assert s.execute('select max(version) from revision where object_id=?',(r['object_id'],)).fetchone()[0]==x['version']
 rows.append({'revision_id':rid,'own_approved_API_pointer':'/individual_actual_approvals/'+str(i)+'/entire_actual_API','actual_native_pointer':'/objects/'+rid,'exact_API_field_and_ordered_array_equality':True,'default_representation_expansions':ds,'source_consequence_judgment_reused_from_own_pre_stage':True});defaults.extend([{'revision_id':rid,**z} for z in ds])
for rid,x in ctx['objects'].items():
 if rid in {r['revision_id'] for r in rows}:continue
 bn=native(b,rid);sn=native(s,rid);assert bn==sn==x;old.append(rid)
assert len(rows)==174 and len(old)==224
prot=rd(p['protected42_pin']['path'])['objects'];pa=rd(S/'protected42-after.json');pb=rd(S/'protected42-before.json');assert prot==pa==pb
for rid,x in prot.items():assert native(s,rid)==native(b,rid)==x
actualops=[dict(x) for x in s.execute('select * from operation_payload order by sequence')][-16:]
normal=[]
for op,r in zip(actualops,g['ordered_operations']):
 original=rd(r['path']);stored=json.loads(op['request_json']);exp=copy.deepcopy(original)
 if 'dependencyReviewVersion' not in exp:exp['dependencyReviewVersion']=2;normal.append({'operation_id':r['operation_id'],'only_added_control_default':'dependencyReviewVersion','value':2})
 assert stored==exp,(r['operation_id'],'journal mismatch');assert op['operation_id']==r['operation_id']
assert [r['sequence'] for r in actualops]==list(range(426,442))
vp=[]
for name in ['verify','verify-assets','verify-source','inventory','pedigree-verified-P0269']:
 v=rd(S/(name+'.json'));pr=rd(S/(name+'.process.json'));vp.append({'result':pin(S/(name+'.json')),'process':pin(S/(name+'.process.json')),'exact_saved_result':v if name.startswith('verify') else {'format':v.get('format'),'mode':v.get('mode'),'note':v.get('note')}})
 if name.startswith('verify'):assert v['ok'] is True
s.close();b.close();assert pin(S/'stage.sqlite')==h['stage_DB_pin']
out={'task':'T-0781','status':'ACTUAL174_COMPLETE_SOURCE_CONSEQUENCE_RESULT_BINDING_PASS_PENDING17_RESOLUTIONS','stage_handoff':pin(S/'complete-stage-result-and-Astra-handoff.json'),'stage_DB_pin':h['stage_DB_pin'],'own_pre_stage_gate':pin(O/'two-source-complete-exact174-pre-stage-source-consequence-gate-v1.json'),'actual_context_pin':h['actual_request_context_native_pin'],'actual174_rows':rows,'existing224_entire_native_payloads_exact_baseline_current_order':old,'protected42_exact':True,'protected42_before':pin(S/'protected42-before.json'),'protected42_after':pin(S/'protected42-after.json'),'entire_ordered_operation_request_normalizations':normal,'representation_limits':'Native *_json storage decoded only to the declared API structured value. Body/source JSON strings untouched; evidence/origins/assets/media read ORDER BY rowid without sorting. Explicit nullable/empty domain defaults enumerated per target; no field silently omitted. Default dependencyReviewVersion2 is native control semantics only, exact changes/resolve source content retained.','explicit_default_fields':defaults,'all16_ordered_journal_rows_exact_after_declared_default':True,'validator_bindings':vp,'all_existing_table_order_preservation_proof':pin(S/'existing-native-history-order-and-narrow-derived-search-proof.json'),'source_and_review_effect':'Actual fields exactly realize individual own approved source judgments, including legacy outcome preservation and13boundedadoptions. Stronger older evidence224 unchanged,42protected unchanged; no full-person/tree/life upgrade. Existing old revisions immutable.','actual_pending':17,'own17_before_primary_freeze':pin(O/'actual17-independent-own-source-consequence-freeze-v1.json'),'remaining':'Exact primary17 comparison, concrete resolution operation approval, root-only apply to sameclone, pending0/fullvalidators/finalhashbinding.','runtime_authorized':False,'canonical_or_final_global_PASS':False}
q=O/'actual174-native-protected-history-and-complete-result-binding-v1.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(pin(q));print('Default fields',len(defaults),'operation defaults',len(normal))
