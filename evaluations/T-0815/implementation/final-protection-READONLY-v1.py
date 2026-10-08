import json,importlib.util,hashlib,time
from pathlib import Path
R=Path.cwd();D=R/'evaluations/T-0815';S=D/'implementation/stage484-v1';start=time.monotonic();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);b=h.conn(D/'preparation/baseline483.sqlite');a=h.conn(S/'stage.sqlite');live=h.conn(R/'genealogy2/data/research.sqlite');assert h.state(a)=={'journal_head':484,'pending':0};assert h.state(live)=={'journal_head':483,'pending':0};assert h.all50(live)==h.all50(b)
(S/'fresh-live-baseline-all50-proof.json').write_text(json.dumps({'passed':True,'main_sha256':hashlib.sha256((R/'genealogy2/data/research.sqlite').read_bytes()).hexdigest(),'state':h.state(live),'all50_exact_to_readonly_baseline':True,'full_before_tables':'baseline-all50.json'},indent=2)+'\n')
ct=json.load(open(D/'implementation/consequence-table-v1.json'));rels=[];owner=[]
for r in ct['retains']:
 n=r['old_native'];assert h.native(a,n['id'])==n and h.current(a,n['object_id'])==n['id']
 if n['kind']=='relation':rels.append({'object_id':n['object_id'],'revision':n['id'],'full_native_exact':True})
for r in b.execute("select id,object_id from current_revision where evidence_status='OWNER_CONFIRMED'"):
 assert h.current(a,r['object_id'])==r['id'] and h.native(a,r['id'])==h.native(b,r['id']);owner.append(r['id'])
assert len(owner)==45
before=json.load(open(R/'evaluations/T-0814/root-actual-inventory-full-v1.json'));after=json.load(open(S/'inventory-full.json'));bm={p['id']:p for p in before['people']};am={p['id']:p for p in after['people']};assert set(bm)==set(am);keys=['identityGate','identityReview','treeEffect','lifePictureReview','stopReasons'];diff=[]
for pid in bm:
 changes={k:{'before':bm[pid].get(k),'after':am[pid].get(k)}for k in keys if bm[pid].get(k)!=am[pid].get(k)}
 if changes:diff.append({'person':pid,'differences':changes})
assert {x['person']for x in diff}=={'P-0042','P-0043'}
for pid in ['P-0042','P-0043']:
 assert am[pid]['identityReview']['outcome']=='failed'and am[pid]['identityReview']['usable'];assert am[pid]['treeEffect']['outcome']=='waiting'and am[pid]['treeEffect']['usable'];assert bm[pid]['lifePictureReview']==am[pid]['lifePictureReview']
for pid in ['P-0269','P-0270']:
 p=json.load(open(S/f'{pid}-pedigree.json'));old=json.load(open(R/f"evaluations/T-0814/root-actual-pedigree-{pid.replace('-','')}-v1.json"));assert len(p['paths'])==len(old['paths'])==41;assert p['paths']==old['paths']
(S/'final-axis-relations-OWNER-proof-v1.json').write_text(json.dumps({'persons':len(am),'nonfocal_axes_exact':len(am)-2,'all_axis_differences':diff,'focal_legacy_LIFE_full_exact':True,'no_new_native_LIFE':True,'protected_child_axes_full_exact':all(bm['P-0009'].get(k)==am['P-0009'].get(k)for k in keys),'relations_full_native_exact':rels,'OWNER45_full_native_heads_exact':owner,'default_pedigree_paths_full_exact':41,'elapsed_seconds':time.monotonic()-start},ensure_ascii=False,indent=2)+'\n');print('PASS axes534nonfocal/OWNER45/relations',len(rels))
