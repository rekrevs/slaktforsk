import pathlib,json,hashlib,importlib.util,time
R=pathlib.Path.cwd();D=R/'evaluations/T-0818';S=D/'implementation/stage488-sequence-v1';start=time.monotonic();sp=importlib.util.spec_from_file_location('h',R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py');h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);a=h.conn(S/'stage.sqlite');b=h.conn(D/'preparation/baseline486.sqlite');snap=json.load(open(D/'preparation/protected-native-review-snapshot-v1.json'));op=json.load(open(D/'implementation/operation-v1.json'));changed={x['id']:x for x in op['changes']};after=json.load(open(S/'inventory-full.json'));am={p['id']:p for p in after['people']};keys=['identityGate','identityReview','treeEffect','lifePictureReview','stopReasons'];diff=[]
for old in snap['all536_review_axes']:
 pid=old['person'];delta={k:{'before':old[k],'after':am[pid].get(k)}for k in keys if old[k]!=am[pid].get(k)}
 if delta:diff.append({'person':pid,'exact_full_axis_differences':delta})
assert len(am)==536;assert {x['person']for x in diff}<={'P-0042','P-0043'}
for pid in ['P-0042','P-0043']:
 old=next(x for x in snap['all536_review_axes']if x['person']==pid);assert old['lifePictureReview']==am[pid]['lifePictureReview'];assert old['identityGate']==am[pid]['identityGate']
proof={}
for label,objects in [('OWNER45',snap['current_OWNER45_fullnative']),('relations26',snap['relations_fullnative'])]:
 for n in objects:assert h.native(a,h.current(a,n['object_id']))==h.native(b,h.current(b,n['object_id'])),(label,n['object_id'])
 proof[label]={'full_current_native_exact':True,'objects':len(objects)}
child=snap['protected_child_fullnative']['current'];shared=[];untouched=[]
for n in child:
 oid=n['object_id'];old=h.native(b,h.current(b,oid));now=h.native(a,h.current(a,oid))
 if oid in changed:
  assert oid in ['R-723ad8b54b5bb2c19909f059','R-6afb03ed14fc4c22984d0cac'];actual=h.api(now);assert actual==h.expected_defaults(changed[oid],actual);shared.append({'object':oid,'baseline_revision':old['id'],'final_revision':now['id'],'old_native':old,'final_native':now,'exact_approved_api':changed[oid],'approved_delta':'Only SOURCE-approved caveat prefix and exact one fullimage media binding; old record data/evidence/origin order retained.'})
 else:assert now==old,oid;untouched.append(n['id'])
assert len(child)==252 and len(untouched)==250 and len(shared)==2
ped=[]
for pid in ['P-0269','P-0270']:
 old=json.load(open(R/f'evaluations/T-0817/implementation/stage486-v1/{pid}-pedigree.json'));now=json.load(open(S/f'{pid}-pedigree.json'));assert old['paths']==now['paths']and old['edges']==now['edges'];assert len(now['paths'])==43 and not now['truncated'];ped.append({'root':pid,'paths':43,'full_paths_and_edges_exact':True,'truncated':False,'backing_gate_view_may_change_only_at_source_approved_focal_reviews':True})
result={'state':h.state(a),'persons':536,'nonfocal534_full_axes_exact':True,'focal_exact_full_axis_differences':diff,'focal_identityGate_full_exact':True,'focal_legacy_LIFE_full_exact':True,'Ada_identity_tree_LIFE_full_axes_exact':not any(x['person']=='P-0009'for x in diff),'protected_current_native':proof,'Ada252_intersection_qualification':{'untouched250_revision_ids':untouched,'approved_shared_source_records2':shared,'source_design':'source-design/primary-complete-source-design-v1.json','literal_operation_sha256':'2fca0ae8c038944f92bac4ba459de131a317eeb247ae3a2c2f8c5feceb17d3b5','not_all252_current_heads_byteidentical':True},'pedigrees':ped,'elapsed_seconds':time.monotonic()-start};p=S/'final-axis-native-protection-proof-v1.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS536/534, OWNER45/relations26, Ada250+2qualified, focalLIFE exact, paths43 unchanged')
