import pathlib,json,hashlib,importlib.util,sqlite3,time,subprocess
R=pathlib.Path.cwd();D=R/'evaluations/T-0818';P=D/'preparation';start=time.monotonic();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.load(open(p))
def save(n,v):
 p=P/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');return p
hp=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';s=importlib.util.spec_from_file_location('h',hp);h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(R/'genealogy2/data/research.sqlite');assert h.state(c)=={'journal_head':486,'pending':0};assert sha(P/'baseline486.sqlite')==sha(R/'genealogy2/data/research.sqlite')
# Accepted prefix is already independently verified through484; only actual accepted delta is reconciled here.
delta=[]
for seq in [485,486]:
 row=dict(c.execute('select *from operation_payload where sequence=?',(seq,)).fetchone());files=list((R/'genealogy2/journal').glob(f'{seq:09d}-*.json'));assert len(files)==1;f=files[0];receipt=load(f);assert receipt['sequence']==seq and receipt['policy']==row['policy'];assert receipt['request']==json.loads(row['request_json']);assert receipt['request']['id']==row['operation_id'];delta.append({'sequence':seq,'database_operation_payload':row,'accepted_receipt':receipt,'receipt_pin':{'path':str(f.relative_to(R)),'sha256':sha(f)},'exact_request_policy_sequence_id':True})
save('accepted-delta485-486-reconciliation-v1.json',{'state':h.state(c),'all_delta_exact':True,'prior484_reconciliation_reuse':'evaluations/T-0817/preparation/accepted484-receipt-journal-reuse-v1.json','actual486_all50_comparison':'evaluations/T-0817/actual-main-stage-comparison-v1.json','delta':delta})
snapshot=load(R/'evaluations/T-0817/preparation/protected-native-review-snapshot-v1.json');owners=snapshot['current_OWNER45_fullnative'];b=h.conn(R/'evaluations/T-0817/preparation/baseline484.sqlite')
for n in owners:assert h.native(c,h.current(c,n['object_id']))==h.native(b,h.current(b,n['object_id']))
save('OWNER45-current-reuse-proof-v1.json',{'all45_raw_fullnative_current_exact':True,'current_revision_ids':[n['id']for n in owners],'fullnative_and_exact_owner_decisions_reused_from':'evaluations/T-0817/preparation/locked-input-manifest-v2.json','no_scope_extension':True})
records=[h.native(c,h.current(c,oid))for oid in ['R-723ad8b54b5bb2c19909f059','R-6afb03ed14fc4c22984d0cac']];source=h.native(c,'S-0781@1');assets=[]
for n in records:
 for a in n.get('assets',[]):assets.append({'binding':a,'asset':dict(c.execute('select *from asset where path=?',(a['asset_path'],)).fetchone())})
 for a in n.get('media',[]):assets.append({'binding':a,'asset':dict(c.execute('select *from native_asset where id=?',(a['asset_id'],)).fetchone())})
matching=[]
for t in ['asset','native_asset']:
 for row in c.execute('select *from '+t):
  if any(k in str(dict(row))for k in ['C0006950_00205','C-1062','C0006950']):matching.append({'table':t,'row':dict(row)})
# Names only, no image decoding or opening.
filematches=[str(p.relative_to(R))for p in R.rglob('*')if p.is_file()and '.git'not in p.parts and any(k in p.name for k in ['C0006950_00205','C-1062'])]
meta=save('single-C1062-copy-metadata-v1.json',{'image_key':'C0006950_00205','material':'Lerbo A I/23 1886–1890, Spånga sida243','own_rows':{'P-0042':16,'P-0043':24},'exact_current_records':records,'source_fullnative':source,'record_asset_or_media_bindings':assets,'matching_asset_locator_rows':matching,'filename_matches':filematches,'controlled_copy_result':'Ingen namngiven lokal bildkopia återfunnen i canonical asset/native_asset locatorfält och repositoryfilnamn inom exakt C1062/C0006950-kontroll. Textcitation är positiv lokator, inte bildkopia; ingen generell frånvaro slutsats.','provider_version':'unknown','historical_dimensions_not_fresh_copy_measurement':{'width':7568,'height':6288,'source':'genealogy/citations/C-1062-lerbo-AI23-sida-243-spanga-oakta-son.md'},'known_IIIF_image_identifier':'C0006950_00205','no_image_opened_or_network_acquisition':True})
# Exact seven PK input and bounded fullnative field-routing; matches are candidates only.
criterion=[];routing=[]
for pid in ['P-0042','P-0043']:
 pack=load(P/'native'/f'{pid}.json');objects=pack['current'];pk=[]
 for n in objects:
  if n['object_id'] in [f'CONTRACT-{pid}-PK-{x:02d}'for x in [1,2,5,7,9,11,12]]:pk.append(n)
 criterion.append({'person':pid,'full_seven_criteria':pk,'relation_revision_ids':[n['id']for n in objects if n['kind']=='relation'],'research_revision_ids':[n['id']for n in objects if n['object_id'].startswith('RESEARCH-')],'current_full_file':f'current-full/{pid}.json'})
 for n in objects:
  matches=[]
  def walk(v,path):
   if isinstance(v,str)and any(k.casefold()in v.casefold()for k in ['C1062','C-1062','C0006950','PK-05','PK05','kunskaps','fullutvin','outvunn','saknad','UNDERKÄND','AVVAKTAR']):matches.append({'field':path,'exact_old_value':v})
   elif isinstance(v,dict):
    for k,a in v.items():walk(a,path+'.'+k)
   elif isinstance(v,list):
    for j,a in enumerate(v):walk(a,f'{path}[{j}]')
  walk(n,'native')
  if matches:routing.append({'person_route':pid,'revision_id':n['id'],'full_native':n,'literal_candidate_fields':matches})
save('fourteen-criterion-input-index-v1.json',criterion);save('current-semantic-copy-routing-v1.json',{'routing_only_not_source_dispositions':True,'objects':routing})
# Norm text snapshots include fresh owner mandate, while old OWNER exact scope remains bounded.
N=P/'normative-snapshots';N.mkdir();norms=['AGENTS.md','wotan/README.md','genealogy2/README.md','genealogy2/docs/working.md','docs/research/person-contract.md','docs/research/source-strategy.md','docs/research/research-program.md','PROJECT-CONTROL.md','wotan/dev-log/T-0818.md']
for name in norms:
 f=N/name.replace('/','__');f.write_bytes((R/name).read_bytes())
reuse=[R/'evaluations/T-0817/preparation/locked-input-manifest-v2.json',R/'evaluations/T-0817/preparation/protected-native-review-snapshot-v1.json',R/'evaluations/T-0817/preparation/accepted484-receipt-journal-reuse-v1.json',R/'evaluations/T-0817/actual-main-stage-comparison-v1.json',R/'evaluations/T-0817/root-actual-final-verification-v1.json',R/'evaluations/T-0817/implementation/stage486-v1/inventory-full.json',R/'evaluations/T-0817/implementation/stage486-v1/P-0269-pedigree.json',R/'evaluations/T-0817/implementation/stage486-v1/P-0270-pedigree.json',R/'evaluations/T-0815/primary-final-source-gate-v1.json',R/'genealogy/citations/C-1062-lerbo-AI23-sida-243-spanga-oakta-son.md',hp,D/'root-start-baseline-v1.json',D/'collect_usage.py']
paths=[f for f in P.rglob('*')if f.is_file()and '__pycache__'not in str(f)];paths+=reuse;paths+=[R/x['receipt_pin']['path']for x in delta]
result=save('preparation-result-v1.json',{'state':h.state(c),'main_sha256':sha(R/'genealogy2/data/research.sqlite'),'baseline_copy_exact':True,'focal_persons':2,'protected_child':'P-0009','OWNER45_current_exact_reuse':True,'delta485_486_exact':True,'scope_original_ceiling':1,'original_opening_or_acquisition':False,'elapsed_seconds':time.monotonic()-start,'usage_collector':'UNRUN; exact new T0818 root floor','failures':['Initial fulltask display truncated due embedded historical logs; full current task snapshot locked without claiming source interpretation'],'current_lock_complete_for_accepted_material_assessment':True,'image_access_still_root_decision':True});paths.append(result)
for f in paths:assert f.exists(),f
pins=[{'path':str(f.relative_to(R)),'sha256':sha(f),'bytes':f.stat().st_size}for f in sorted(set(paths))]
m={'task':'T-0818','state':h.state(c),'main_sha256':sha(R/'genealogy2/data/research.sqlite'),'scope':'P0042 ownrow16 and P0043 ownrow24, only shared C1062; child Ada protected; source ceiling1 not automatic access','readable_index':'preparation/fourteen-criterion-input-index-v1.json','current_persons':['P-0042','P-0043','P-0009'],'files':pins,'no_source_judgment_or_native_write':True};f=P/'locked-input-manifest-v1.json';f.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'manifest_sha256':sha(f),'pins':len(pins),'media_metadata_sha256':sha(meta),'state':h.state(c),'elapsed':time.monotonic()-start}))
