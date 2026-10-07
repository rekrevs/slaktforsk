import json,pathlib,hashlib,copy
b=pathlib.Path('evaluations/T-0790');p=b/'preparation/materialized-source-v3-literal-v1';op=json.loads((p/'operation-literal.json').read_text());tab=json.loads((p/'individual-consequence-table.json').read_text());s=json.load(open(b/'source-review/settled-90-dispositions-and-literal-field-decisions-v3.json'));n=json.load(open(b/'preparation/complete-current-history-support-native.json'));errors=[]
def check(ok,scope):
 if not ok:errors.append(scope)
def decode(k,v):
 return json.loads(v) if k.endswith('_json') and isinstance(v,str) else v
check(len(op['changes'])==40,'40changes')
for i,c in enumerate(s['exact_changes']):
 old=n['objects'][c['target_revision']];raw={k:decode(k,v) for k,v in old['data'].items() if k!='revision_id'}
 exp={'id':old['object_id'],'kind':old['kind'],'expectedVersion':old['version'],'data':raw,'origins':[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in old['origins']],'evidence':copy.deepcopy(c['literal_api_evidence']),'disposition':old['disposition'],'evidenceStatus':old['evidence_status'],'rationale':old['rationale'],'caveat':old['caveat']+ ('\n\n' if old['caveat'] else '')+c['amendment_caveat']}
 for f in c['field_changes']:exp['data'][f['field']]=decode(f['field'],f['new'])
 check(op['changes'][i]==exp,['completeAPI',i,c['target_revision']])
 t=tab['changes'][i];check(t['old_native']==old,['fulloldnative',i]);check(t['new_api']==exp,['tablenew',i]);check(t['individual_evidence_decisions']==c['individual_evidence_decisions'],['tableedges',i])
for i,r in enumerate(s['six_life_reviews'],34):
 check(op['changes'][i]==r,['newlifefull',i]);check(tab['changes'][i]['new_api']==r,['tablenewlife',i]);check(r['evidenceStatus'] is None,['nullnewlife',i])
check(tab['all90_individual_dispositions']==s['individual_table'],'table90exact');check(tab['followup']==s['bounded_followup'],'followupExact')
changed={r['object_id'] for r in [n['objects'][c['target_revision']] for c in s['exact_changes']]}
for r in tab['retains']:
 check(r['old_native']==n['objects'][r['revision_id']],['wholeoldretain',r['revision_id']]);check(r['revision_id'].rsplit('@',1)[0] not in changed,['retainchanged',r['revision_id']])
check(len({x['revision_id'] for x in tab['retains']})==len(tab['retains'])==72,'72uniqueRetains')
check(all(x['kind'] not in ['person','relation','event'] for x in op['changes']),'protectedKinds')
check({x['data'].get('criteria') for x in op['changes']}.isdisjoint({'identity_review/1','tree_effect/1'}),'protectedGrinds')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
result={'schema':'T0790-independent-prestage-source-gate/1','ready_for_stage':not errors,'operation_sha256':sha(p/'operation-literal.json'),'consequence_sha256':sha(p/'individual-consequence-table.json'),'source_spec_sha256':sha(b/'source-review/settled-90-dispositions-and-literal-field-decisions-v3.json'),'source_outcome':'PASS' if not errors else 'FAIL','checks':{'literal_complete_APIs':40,'existing_complete_preservation':34,'new_native_life_null_evidence_status':6,'whole_native_retains':72,'individual_theme_PK_dispositions':90,'field_order_evidence_order_origins_caveat':'Compared complete parsed values against independently reconstructed expected API from pinned native and approved sourcev3; array ordering retained. JSON object key order not semantically significant.'},'errors':errors,'source_judgment':'Prior own freeze/independent semantic search and corrected comparative v3 judgement reused. Materialized package reproduces source-settled revisions, individual preserves, stronger support, legacy metadata scope and actual T0795 bounds. Fivefailed/oneEvyminimalpassed remain justified with individual90coverage. No original/source access added.','approval_scope':'Ready for one baseline-clone stage only. Does not grade unseen runtime pending requests, authorize canonical apply or approve an unseen staged DB. Actual pending dependency requests and exact final stage must return to source review.','canonical_apply_approved':False,'final_stage_source_approved':False}
(b/'independent-review/prestage-source-gate-v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('errors',errors);print('gate_sha256',sha(b/'independent-review/prestage-source-gate-v1.json'))
