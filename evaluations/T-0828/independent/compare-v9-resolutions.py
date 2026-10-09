import json,hashlib,pathlib,copy
b=pathlib.Path('evaluations/T-0828');p=b/'implementation';approved=json.load(open(b/'independent/actual-pending-v6-dispositions-v1.json'))
old={(r['request']['affected_revision_id'],r['request']['changed_revision_id']):r for r in approved['rows'] if r['decision']=='retain'}
actual=json.load(open(p/'stage-v9/actual-pending-full-native-v1.json'))['rows'];op=json.load(open(p/'operation-resolutions-v9.json'));tab=json.load(open(p/'individual-resolution-table-v9.json'));res={r['request']:r for r in op['resolve']};table={r['actual_request']['id']:r for r in tab['rows']}
assert len(old)==len(actual)==len(res)==len(table)==35;assert op['changes']==[]
checks=[]
for r in actual:
 req=r['request'];key=(req['affected_revision_id'],req['changed_revision_id']);prev=old[key];assert r['affected_full_native']==prev['affected_full_native'];cb=copy.deepcopy(r['changed_full_native']);ob=copy.deepcopy(prev['changed_full_native']);cb['revision'].pop('operation_id');ob['revision'].pop('operation_id');assert cb==ob
 rr=res[req['id']];assert prev['reason'] in rr['rationale'];assert all(k in rr['rationale'] for k in key);assert table[req['id']]['actual_request']==req
 checks.append({'request':req,'affected_full_native_exact':True,'changed_basis_exact_except_operation_id':True,'individual_previously_reviewed_reason_preserved':True,'resolution':rr})
x={'task':'T-0828','decision':'APPROVE exact35 resolution payloads after reviewed source v9; final package/stage verification still pending','operation_sha256':hashlib.sha256((p/'operation-resolutions-v9.json').read_bytes()).hexdigest(),'table_sha256':hashlib.sha256((p/'individual-resolution-table-v9.json').read_bytes()).hexdigest(),'source_operation_sha256':hashlib.sha256((p/'operation-ordered-v9.json').read_bytes()).hexdigest(),'checks':checks,'source_delta_concurrence':'Complete v6→v9 delta inspected: five exact historical caveat supersessions, unchanged source literal/data/status/origin fields, specific support additions/rebindings and three direct period arrays concur. No new source semantics or gate changes.'}
out=b/'independent/exact-v9-resolution-review-v1.json';out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(out,hashlib.sha256(out.read_bytes()).hexdigest())
