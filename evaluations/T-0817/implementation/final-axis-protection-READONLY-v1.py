import json,pathlib,hashlib,importlib.util,time
R=pathlib.Path.cwd();D=R/'evaluations/T-0817';S=D/'implementation/stage486-v1';t=time.monotonic();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(S/'stage.sqlite');x=json.load(open(D/'preparation/protected-native-review-snapshot-v1.json'));after=json.load(open(S/'inventory-full.json'));am={p['id']:p for p in after['people']};keys=['identityGate','identityReview','treeEffect','lifePictureReview','stopReasons'];diff=[]
for p in x['all536_review_axes']:
 pid=p['person'];changes={k:{'before':p[k],'after':am[pid].get(k)}for k in keys if p[k]!=am[pid].get(k)}
 if changes:diff.append({'person':pid,'differences':changes})
assert len(am)==536;assert [p['person']for p in diff]==['P-0337'],[p['person']for p in diff]
for label,rows in [('OWNER45',x['current_OWNER45_fullnative']),('child185',x['protected_child_fullnative']['current']),('relations22',x['relations_fullnative'])]:
 for n in rows:assert h.native(c,h.current(c,n['object_id']))==n,(label,n['id'])
p=S/'final-axis-OWNER-child-relation-proof-v1.json';p.write_text(json.dumps({'persons':536,'nonfocal_axes_full_exact':535,'focal_full_axis_differences':diff,'OWNER45_fullnative_exact':True,'Johannes185_fullnative_exact':True,'relations22_fullnative_exact':True,'elapsed_seconds':time.monotonic()-t},ensure_ascii=False,indent=2)+'\n');print('536 axes; only Brita differs; OWNER45/child185/relations22 PASS')
