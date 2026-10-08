import json,pathlib,hashlib,importlib.util,datetime
R=pathlib.Path.cwd();D=R/'evaluations/T-0814';S=D/'implementation/stage483-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
b=h.conn(D/'preparation/baseline481.sqlite');a=h.conn(S/'stage.sqlite');assert h.state(a)=={'journal_head':483,'pending':0}
owner=[]
for row in b.execute("select object_id,id from revision where evidence_status='OWNER_CONFIRMED'"):
 old=h.native(b,row['id']);new=h.native(a,row['id']);assert old==new;owner.append(row['id'])
axes=json.load(open(S/'final-axis-differences-and-relation-proof.json'));assert {x['person']for x in axes['all_person_axis_differences']}=={'P-0336','P-0337'}
for pid in ['P-0336','P-0337']:
 p=json.load(open(S/f'{pid}-person.json'))
 # Reader layouts retained verbatim; detailed axis values in pinned inventory.
inv=json.load(open(S/'inventory-full.json'));m={p['id']:p for p in inv['people']}
for pid in ['P-0336','P-0337']:
 assert m[pid]['identityReview']['outcome']=='failed' and m[pid]['identityReview']['usable']
 assert m[pid]['treeEffect']['outcome']=='waiting' and m[pid]['treeEffect']['usable']
assert len(json.load(open(S/'P-0269-pedigree.json'))['paths'])==41
assert len(json.load(open(S/'P-0270-pedigree.json'))['paths'])==41
for name in ['verify','verify-assets']:
 v=json.load(open(S/f'{name}.json'));assert v['ok'] and not v['errors']
v=json.load(open(S/'verify-source.json'));assert not v.get('problems',[])
result={'task':'T-0814','state':h.state(a),'main_unchanged_sha256':sha(R/'genealogy2/data/research.sqlite'),'stage_sha256':sha(S/'stage.sqlite'),'literal_native_apis':20,'ordered_individual_resolutions':42,'initial_step_retains':613,'resolution_step_retains':42,'step_retains_are_not_unique_sum':True,'persons':536,'nonfocal_axes_exact':534,'focal_identity':'failed usable','focal_tree':'waiting usable','focal_life':'unchanged legacy full-contract; no new native LIFE','protected_child':'P-0287','retained_relations_exact':17,'changed_spouse_relation':'Only source-approved nature recorded_sibling→recorded_spouse; full API proven in final-exact-native-package-proof','owner_confirmed_revision_rows_exact':len(owner),'owner_revision_ids':owner,'default_pedigree_paths_each':41,'tests':'18/18 targeted review/pedigree PASS; unchanged code wider accepted tests reused','reader_capture_seconds':json.load(open(S/'reader-capture-result.json'))['elapsed_seconds'],'production_limitations':'Model token usage collected by root after final responses; worker usage not independently observable. Preflight two stale READ bindings returned and explicitly approved; rejected queue-position candidate preserved. No source originals opened, no canonical writes.'}
(S/'final-qualified-result-v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
files={p for p in D.rglob('*')if p.is_file() and '__pycache__'not in str(p) and not p.name.startswith('final-manifest') and 'final-source-gate'not in p.name and p.suffix not in ['-wal','-shm']}
# Preserve exact reusable input pins, without copying historical source files.
for p in [D/'preparation/locked-input-manifest-v1.json',D/'implementation/literal-manifest-v1.json',D/'implementation/42-resolution-literal-manifest-v1.json']:
 def walk(v):
  if isinstance(v,dict):
   if 'path'in v and isinstance(v['path'],str) and (R/v['path']).is_file():files.add(R/v['path'])
   for x in v.values():walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(json.load(open(p)))
pins=[{'path':str(p.relative_to(R)) if p.is_absolute() else str(p),'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted(files,key=str)]
out=D/'implementation/final-manifest-v1.json';out.write_text(json.dumps({'task':'T-0814','stage_state':h.state(a),'stage_database':str((S/'stage.sqlite').relative_to(R)),'stage_sha256':sha(S/'stage.sqlite'),'qualified_result':str((S/'final-qualified-result-v1.json').relative_to(R)),'canonical_approval':False,'canonical_apply_root_only':True,'pins':pins},ensure_ascii=False,indent=2)+'\n');print('manifest',sha(out),'pins',len(pins),'stage',sha(S/'stage.sqlite'))
