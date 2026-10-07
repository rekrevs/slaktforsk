import json,pathlib,hashlib
B=pathlib.Path('evaluations/T-0781'); O=B/'independent-review'
def read(p): return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
def save(n,d):p=O/n;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(pin(p))
files=['sixtytwo-current-consumer-whole-reading-and-source-scope-dispositions-v1.json','C0049-121-current-semantic-scope-and-legacy-outcome-dispositions-v1.json','C0067-131-current-semantic-dispositions-and-22-exact-copy-findings-v1.json','first-bounded-source-comparison-and-C0067-reuse-findings-v1.json','nine-other-sibling-route-source-scope-dispositions-and-IF002-v1.json','fifteen-direct-and-stronger-current-native-independent-reading-v1.json','outside73-independent-bounded-context-dispositions-v1.json','ASSESSMENT-P0094-exact-prior-own-whole-reading-reuse-v1.json']
m={}
for f in files:
 p=O/f;d=read(p)
 if 'actually_whole_current_native_read' in d: k='actually_whole_current_native_read/objects'; rows=d['actually_whole_current_native_read']['objects']
 elif 'revision_id' in d:k='';rows=[d]
 else:k='individual_rows' if 'individual_rows' in d else 'rows';rows=d[k]
 for i,r in enumerate(rows):m.setdefault(r['revision_id'],[]).append({'receipt':pin(p),'pointer':f'/{k}/{i}' if k else '', 'literal_own_predicate_and_disposition':r})
dictp=B/'mechanical-current425-preparation-v1/full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json';native=read(dictp)['objects'];out=[]
for f in ['C0049-finite-individual-semantic-amend-and-retain-index-v2.json','C0067-finite-individual-semantic-amend-and-retain-index-v1.json']:
 p=B/'source-review'/f;d=read(p);pr=read(d['projection_pin']['path']); assert pin(d['projection_pin']['path'])==d['projection_pin']
 for i,r in enumerate(d['rows']):
  rid=r['current_revision_id'];a=pr['rows'][r['projection_index']];n=native[rid]; data=a.get('whole_data',a.get('data'));c=pr['caveats'][a.get('whole_caveat_id',a.get('caveat_id'))] if isinstance(pr['caveats'],list) else pr['caveats'][str(a.get('whole_caveat_id',a.get('caveat_id')))];assert data==n['data'],rid;assert c==n['caveat'],(rid,c,n['caveat']);assert rid in m,rid
  out.append({'citation':d['citation'],'revision_id':rid,'primary_index':pin(p),'primary_row_pointer':f'/rows/{i}','current_native_pin':pin(dictp),'current_native_pointer':'/objects/'+rid,'primary_semantic_projection_exact_native_data_caveat':True,'own_prior_reading_or_bounded_relevance':m[rid],'own_source_scope_decision':'AGREE_WITH_EXACT_PRIMARY_SOURCE_DISPOSITION_AFTER_OWN_CONTEXT_REVIEW','approved_disposition':r['disposition'],'approved_scope_reason':r['scope_reason'],'actual_amendment_overlay_required':r['disposition']!='retain_current_in_this_source_scope','scope_limit':'Own literal predicate retained exactly; scoped relevance exclusions are not whole-object reading. Native metadata equality does not create source reading or person-contract approval.'})
save('two-source-finite320-individual-own-prior-reading-and-current-scope-closure-v1.json',{'task':'T-0781','status':'FINITE_SOURCE_SCOPE_PASS_WITH_ACTUAL_OVERLAYS_REQUIRED','rows':out,'count':len(out),'source_row98_correction':'Accepted v2: prior birth investigation is not identified own birth record; Jomark Barbru unresolved and Bodan separate. All other150 rows unchanged.','additional_E52_E53_questions':'Closed by separate exact three-API/one-retain receipt9ad9e16d; not inferred from finite index count.','scope':'These320 rows are finite source-specific dispositions, not320 new whole-native readings. Existing exact own readings and two bounded context exclusions reused.','global_package_PASS':False,'runtime_authorized':False})
