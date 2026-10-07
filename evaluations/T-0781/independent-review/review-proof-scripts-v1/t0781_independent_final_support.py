import json,pathlib,hashlib,copy
B=pathlib.Path('evaluations/T-0781');O=B/'independent-review'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
def save(n,d):p=O/n;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(pin(p));return pin(p)
p=B/'implementation/complete-two-source-settled-draft-package-v2/complete-two-source-draft-package-proposal-v1.json';new=rd(p);old=rd(new['prior_package_preserved_pin']['path']);spec=rd(new['two_audit_exact_metadata_amendment_pin']['path']);by={r['object_id']:r for r in spec['objects']};renew=[];unchanged=[]
for a,b in zip(old['operations'],new['operations']):
 aa=rd(a['path']);bb=rd(b['path']);assert pin(a['path'])['sha256']==a['sha256'];assert pin(b['path'])['sha256']==b['sha256']
 if a['sha256']==b['sha256']:assert a['path']==b['path'];unchanged.append(pin(b['path']));continue
 c=aa['changes'][0];s=by[c['id']];assert c==s['entire_prior_candidate_API'];assert c['rationale']==s['old'];expected=copy.deepcopy(aa);expected['changes'][0]['rationale']=s['new'];assert bb==expected
 renew.append({'object_id':c['id'],'prior_operation':pin(a['path']),'actual_operation':pin(b['path']),'actual_pointer':'/changes/0','only_changed_field':'rationale','old':s['old'],'new':s['new'],'entire_operation_exact_prior_plus_only_explicit_rationale':True,'own_judgment':'Accept lasting source-review scope wording. Whole previously reviewed source extraction/body/ordered evidence unchanged. No claim of already completed canonical or person-review gate.'})
assert len(renew)==2 and len(unchanged)==14
save('two-audit-final-rationale-whole-operation-equality-and-source-review-v1.json',{'task':'T-0781','status':'EXACT_TWO_METADATA_AMENDMENTS_PASS','source_spec':new['two_audit_exact_metadata_amendment_pin'],'rows':renew,'fourteen_unchanged_ordered_members':unchanged,'old_full_source_reading_reused':True,'runtime_authorized':False})
# Explicit own prior row bindings, no primary-as-own credit.
m={}
for f in ['sixtytwo-current-consumer-whole-reading-and-source-scope-dispositions-v1.json','first-bounded-source-comparison-and-C0067-reuse-findings-v1.json','fifteen-direct-and-stronger-current-native-independent-reading-v1.json']:
 q=O/f;d=rd(q)
 if 'actually_whole_current_native_read' in d:k='actually_whole_current_native_read/objects';rows=d['actually_whole_current_native_read']['objects']
 else:k='individual_rows' if 'individual_rows' in d else 'rows';rows=d[k]
 for i,r in enumerate(rows):m.setdefault(r['revision_id'],[]).append({'receipt':pin(q),'pointer':f'/{k}/{i}','literal_own_scope':r})
q=B/'source-review/two-source-29-direct-and-26-profile-individual-current-disposition-index-v1.json';d=rd(q);rows=[]
for i,r in enumerate(d['rows']):
 rid=r['current_revision_id'];assert rid in m,rid
 rows.append({'revision_id':rid,'primary_pointer':f'/rows/{i}','own_prior_bindings':m[rid],'own_scope_decision':'AGREE_EXACT_SOURCE_SCOPE_RETAIN_OR_EXPLICIT_AMENDMENT','primary_disposition':r['disposition'],'primary_scope_or_exact_spec':r.get('scope_reason',r.get('source_spec'))})
q897=B/'source-review/two-source-finite897-routing-relevance-exclusion-and154-registry-dispositions-v2.json';d897=rd(q897)
save('direct55-and-independent-search-relevance-closure-v1.json',{'task':'T-0781','status':'BOUNDED_CURRENT_SOURCE_SCOPE_CLOSED','primary55':pin(q),'rows':rows,'primary897_index':pin(q897),'own_independent_search':pin(O/'independent-live425-semantic-field-search-v1.json'),'own_outside73_relevance':pin(O/'outside73-independent-bounded-context-dispositions-v1.json'),'scope_agreement':'Primary897 group predicates are consistent with own independent390 hit search, own73 outside-context dispositions, own finite320 and full55 current readings. This is changed-field relevance agreement, not a claim of 897 whole objects reread or blanket substantive endorsement. Other persons/year/source records and stable references stay outside these two corrections.','metadata233_routing_interpretation':'230 no source field effect plus3 explicitly amended; limits historical233 wording is routing count only.','own_primary_group_reasons_read':sorted(set(r['scope_reason'] for r in d897['rows'])),'stronger_prior_support':'Own C69/C48 exact-reuse receipt009cad and own C0184/C46/C72/family context findings govern. No identity/parent/review upgrades from grouping.','runtime_authorized':False,'global_package_PASS':False})
