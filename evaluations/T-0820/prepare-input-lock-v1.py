import pathlib,json,hashlib,importlib.util,time,subprocess,re
R=pathlib.Path.cwd();D=R/'evaluations/T-0820';P=D/'preparation';P.mkdir(exist_ok=True);start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.load(open(p))
def save(n,v):
 p=P/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');return p
hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';sp=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);main=R/'genealogy2/data/research.sqlite';root=load(D/'root-start-baseline-v1.json');assert sha(main)==root['main_sha256'];c=h.conn(main);assert h.state(c)=={'journal_head':488,'pending':0};old=load(R/'evaluations/T-0819/preparation/baseline-v1.json');assert sha(main)==old['main']['sha256']
# Exact accepted same488 state permits reuse, no journal replay or repeated source reading.
recon=save('accepted488-current-reuse-proof-v1.json',{'state':h.state(c),'main_same_as_accepted_T0819_input':True,'main_sha256':sha(main),'accepted_T0818_all50_actual_comparison':'evaluations/T-0818/actual-main-stage-comparison-v1.json','full485_488_envelopes_reused':'evaluations/T-0819/preparation/accepted-T0817-T0818-envelope-reconciliation-v1.json','no_replay_or_repeated_negative_search':True})
source=h.native(c,'S-0616@1');record=h.native(c,'R-f350624d174adb78e71026fe@1');observation=h.native(c,'O-P-0336-C0800-census@1');assert h.current(c,record['object_id'])==record['id']and h.current(c,observation['object_id'])==observation['id'];sourcefile=save('exact-current-C0800-source-record-observation-v1.json',{'source':source,'record':record,'observation':observation})
oldfront=load(R/'evaluations/T-0819/preparation/four-current-front-full-native-and-criterion-index-v1.json');focal=next(x for x in oldfront['front']if x['person']=='P-0336');assert all(h.native(c,h.current(c,n['object_id']))==n for n in focal['full_current_raw_native']);save('current-Olaus-full-native-reuse-proof-v1.json',{'current_main_hash_same':True,'all478_current_native_objects_exact':len(focal['full_current_raw_native'])==478,'full_raw_front_index_reuse':'evaluations/T-0819/preparation/four-current-front-full-native-and-criterion-index-v1.json','full_person_reuse':'evaluations/T-0819/preparation/current-full/P-0336.json','native_direct_bound_current_stronger_reuse':'evaluations/T-0819/preparation/native-support-versions-v1.json','no_new_identity_source_grade':True})
# Exact field locators for this family source; current fullnative and all direct current/bound stronger supplied.
pat=re.compile(r'C-?0800|Folk_901017-090|Folk_111631011|R-f350624d174adb78e71026fe|O-P-0336-C0800-census',re.I);routes=[]
for r in c.execute('select *from current_revision'):
 n=h.native(c,r['id']);matches=[]
 def walk(v,p):
  if isinstance(v,str)and pat.search(v):matches.append({'field':p,'exact_old_value':v})
  elif isinstance(v,dict):
   for k,w in v.items():walk(w,p+'.'+k)
  elif isinstance(v,list):
   for j,w in enumerate(v):walk(w,f'{p}[{j}]')
 walk(n,'native')
 for k,v in n['data'].items():
  if k.endswith('_json')and isinstance(v,str):walk(json.loads(v),'native.data.'+k+'(decoded)')
 if matches:
  bases=[]
  for e in n['evidence']:
   raw=h.native(c,e['basis_revision_id']);bases.append({'edge':e,'bound_native':raw,'current_stronger_native':h.native(c,h.current(c,raw['object_id']))})
  routes.append({'object':n['object_id'],'current_revision':n['id'],'full_native':n,'exact_literal_fields':matches,'bound_and_current_stronger':bases})
routing=save('C0800-family-current-semantic-routing-v1.json',{'routing_only_not_certified_people_or_corrections':True,'exact_pattern':pat.pattern,'current_candidates':routes,'no_other_household_or_Rotman_research':True})
# Original metadata only. No image contents opened; dimensions from system metadata command.
assets=[]
for a in record['assets']:
 f=R/a['asset_path'];row=dict(c.execute('select *from asset where path=?',(a['asset_path'],)).fetchone());assert sha(f)==row['sha256']and f.stat().st_size==row['bytes'];entry={'exact_binding':a,'canonical_asset':row,'local_path':a['asset_path'],'actual_sha256':sha(f),'bytes':f.stat().st_size}
 if f.suffix.lower()in ['.jpg','.jpeg','.png']:
  result=subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight','-g','format',str(f)],capture_output=True,text=True);assert result.returncode==0;entry['actual_dimension_metadata_stdout']=result.stdout;entry['not_interpreted_or_classified_as_complete_original']=True
 assets.append(entry)
# Registered aliases/provenance plus exact filename check; bounded locator result never source absence.
alias=[]
for t in ['asset','native_asset']:
 for row in c.execute('select *from '+t):
  if any(k in str(dict(row))for k in ['Folk_901017','Folk_111631011','C-0800']):alias.append({'table':t,'row':dict(row)})
found=subprocess.run(['rg','--files','--hidden','-g','!.git','-g','*Folk_901017*','-g','*Folk_111631011*','-g','*C-0800*'],capture_output=True,text=True);assert found.returncode in [0,1];names=found.stdout.splitlines();save('C0800-local-copy-and-manifest-locators-v1.json',{'anchor_image':'Folk_901017-090','family_post':'Folk_111631011','registered_record_assets':assets,'registered_record_media':record['media'],'named_alias_metadata':alias,'exact_matching_filenames':names,'known_exact_anchor_viewer_pattern':'https://sok.riksarkivet.se/bildvisning/Folk_901017-090','viewer_pattern_not_new_HTTP_verified':True,'adjacent_continuation_image_id':None,'manifest_locator':'No local manifest matching exact family/anchor locators found in this controlled pass; exact provider/manifest resolution is still a root-controlled metadata step. No nextimage ID inferred.','provider_version':'unknown','historical_source_context_not_new_search':'S0616 metadata includes accepted2026-09-02 Olaus post observation; unrelated Grill/Bygdeå old searches not repeated or promoted','no_network_or_image_interpretation':True})
# OWNER scope preserved; exact current full45/direct25 bases reusable since sameMAIN.
owner=load(R/'evaluations/T-0819/preparation/current-OWNER45-and-direct-bases-v1.json');assert len(owner['OWNER45_full_raw_native'])==45
for n in owner['OWNER45_full_raw_native']:assert h.native(c,h.current(c,n['object_id']))==n
save('OWNER45-current-scope-reuse-proof-v1.json',{'all45_current_raw_native_exact':True,'direct25_bound_basis_fullnative_reuse':'evaluations/T-0819/preparation/current-OWNER45-and-direct-bases-v1.json','owner_decisions_exact_previous_snapshot_reused':True,'freshPCD004_task_mandate_snapshot_included':True,'scope_extension':False})
N=P/'norm-and-task-snapshots';N.mkdir();snaps=[]
for n in ['AGENTS.md','wotan/README.md','PROJECT-CONTROL.md','wotan/dev-log/T-0820.md','wotan/dev-log/T-0255.md','docs/research/person-contract.md','genealogy2/docs/working.md','docs/research/riksarkivet-access.md']:
 p=N/n.replace('/','__');p.write_bytes((R/n).read_bytes());snaps.append(p)
u=(R/'evaluations/T-0819/collect_usage.py').read_text().replace('T-0819','T-0820');(D/'collect_usage.py').write_text(u)
result=save('preparation-result-v1.json',{'state':h.state(c),'main_unchanged_sha256':sha(main),'focal_current_objects':478,'OWNER45':45,'owner_bases':25,'semantic_route_objects':len(routes),'originals_opened_or_acquired':0,'native_writes':0,'source_judgments':0,'continuation_id_unknown':True,'elapsed_seconds':time.monotonic()-start,'usage_collector':'UNRUN newT0820floor only','scope_maximum':'One manifest/one direct adjacent continuation only after exact ID/hash/SOURCE/rootrelease; no7Rotman/otherfamily research'})
reuse=[R/'evaluations/T-0819/preparation/locked-input-manifest-v1.json',R/'evaluations/T-0819/preparation/four-current-front-full-native-and-criterion-index-v1.json',R/'evaluations/T-0819/preparation/current-full/P-0336.json',R/'evaluations/T-0819/preparation/native-support-versions-v1.json',R/'evaluations/T-0819/preparation/current-OWNER45-and-direct-bases-v1.json',R/'evaluations/T-0819/preparation/accepted-T0817-T0818-envelope-reconciliation-v1.json',R/'evaluations/T-0819/settled-source-planning-design-v2.json',R/'evaluations/T-0819/root-actual-allocation-v1.json',R/'evaluations/T-0818/actual-main-stage-comparison-v1.json',R/'genealogy/citations/C-0800-riksarkivet-inloggat-omprov-grill-bygdea-fredberg.md',R/'genealogy/sources/S-0616-riksarkivet-inloggat-omprov-grill-bygdea-fredberg.md',hp,D/'root-start-baseline-v1.json',D/'collect_usage.py']
reuse += [R/x['local_path']for x in assets];reuse += list(D.glob('root-start-pedigree-*.json'))+[D/'root-start-inventory.json'];paths=list(P.rglob('*'));paths=[p for p in paths if p.is_file()and '__pycache__'not in str(p)]+reuse;assert sha(main)==root['main_sha256'];pins=[{'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted(set(paths))];m={'task':'T-0820','state':h.state(c),'main_sha256':sha(main),'focal':'P-0336 accepted identity/currentC0800 family boundaries; no guaranteedPASS','scope':'Only existing C0800 direct family continuation after Folk_901017-090; exact nextimage ID unassigned until permitted metadata resolution','current_full_input_reuse_complete':True,'new_sources_or_network':0,'native_or_queue_changes':0,'files':pins};p=P/'locked-input-manifest-v1.json';p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'manifest_sha256':sha(p),'pins':len(pins),'route_objects':len(routes),'elapsed':time.monotonic()-start}))
