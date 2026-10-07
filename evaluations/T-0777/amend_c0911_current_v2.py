import json,pathlib,hashlib
B=pathlib.Path(__file__).resolve().parent
x=json.loads((B/'C-0911-consequence-candidate-operation-v1.json').read_text())
for fn in ['C-0911-HAL-age-copy-amendment-v5.json','C-0911-Q02-chronology-amendment-v6.json']:
 d=json.loads((B/'source-review'/fn).read_text()); a=[c for c in x['changes'] if c['id']==d['object']]; assert len(a)==1
 assert a[0]['expectedVersion']==d['version']; a[0]['data']['body']=d['new_full_field']
(B/'C-0911-consequence-candidate-operation-v2.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
edges={'F-P-0043-family_context-Elin-household-sequence':['O-P-0043-related125-household_role_report'],'F-P-0043-family_context-Karl-Harry-sequence':['O-C0910-Karl-Harry-row5','O-P-0043-related122-household_role_report']}
for fid,oids in edges.items():
 c=next(c for c in x['changes'] if c['id']==fid)
 for oid in oids:
  es=[e for e in c['evidence'] if e['object']==oid]; assert len(es)==1 and es[0]['version']==2; es[0]['version']=3
old=[c['id'] for c in x['changes']]; pending=x['changes'][:]; ordered=[]; done=set(); allids=set(old)
while pending:
 for c in pending:
  deps={e['object'] for e in c['evidence'] if e['object'] in allids and e['version']==next(z['expectedVersion']+1 for z in x['changes'] if z['id']==e['object'])}
  if deps<=done:
   ordered.append(c);done.add(c['id']);pending.remove(c);break
 else: raise AssertionError('cycle')
x['changes']=ordered
(B/'C-0911-consequence-candidate-operation-v2.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
(B/'C-0911-current-implementation-amendment-v2.json').write_text(json.dumps({'task':'T-0777','preserved':'C-0911-consequence-candidate-operation-v1.json','decisions':['C-0911-HAL-age-copy-amendment-v5.json','C-0911-Q02-chronology-amendment-v6.json','metadata-dependency-amendment-v3.json'],'exact_rebinds':edges,'old_change_order':old,'new_change_order':[c['id'] for c in ordered],'data_array_order_preserved':True},ensure_ascii=False,indent=2)+'\n')
