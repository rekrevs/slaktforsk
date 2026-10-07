"""T0788 exact two-person/current744 preparation. No image/source interpretation."""
from pathlib import Path
import json,hashlib,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;M=R/'genealogy2/data/research.sqlite';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
helper=R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py';sp=importlib.util.spec_from_file_location('mechanical',helper);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
acceptp=R/'evaluations/T-0786/root-canonical444-access-note-acceptance-v1.json';accept=json.loads(acceptp.read_text());mainpin=h.pin(M);c=h.conn(M);before=h.all50(c);assert h.state(c)=={'journal_head':444,'pending':0}
roots={'P-0007','P-0017','R-ab847c1960d02f28801419b3','S-0758'};views={}
def seed(v):
 if isinstance(v,dict):
  if isinstance(v.get('revision_id'),str) and '@' in v['revision_id']:roots.add(v['revision_id'].rsplit('@',1)[0])
  for w in v.values():seed(w)
 elif isinstance(v,list):
  for w in v:seed(w)
for person in ['P-0007','P-0017']:
 p=O/(person+'-whole-current444-person.json');v=h.run_cli(['person',person,'--full','--format','json'],p);seed(v);views[person]=h.pin(p)
oldp=R/'evaluations/T-0784/root-controlled-exact-nine-canonical-v1/P-0007-whole-person.json';old=json.loads(oldp.read_text());new=json.loads((O/'P-0007-whole-current444-person.json').read_text());assert old==new
pool={};units={};docs={};media={}
def add(rid):
 if rid in pool:return
 n=h.native(c,rid);pool[rid]=n
 for e in n['origins']:
  u=dict(c.execute('select * from unit where id=?',(e['unit_id'],)).fetchone());units[u['id']]=u;d=dict(c.execute('select * from document where path=?',(u['document_path'],)).fetchone());docs[d['path']]=d
 for e in n.get('assets',[]):
  a=dict(c.execute('select * from asset where path=?',(e['asset_path'],)).fetchone());media['asset:'+a['path']]=a
 for e in n.get('media',[]):
  a=dict(c.execute('select * from native_asset where id=?',(e['asset_id'],)).fetchone());media['native:'+a['id']]=a
 for e in n['evidence']:add(e['basis_revision_id']);add(h.current(c,e['basis_revision_id'].rsplit('@',1)[0]))
for oid in sorted(roots):add(h.current(c,oid))
# Own frozen relevant citations, exact accepted stronger sources; no source-content judgement.
refs=['C-0973','C-0972','C-0033','C-0894','C-0895'];routes=[]
for ref in refs:
 for r in c.execute('select distinct object_id from object_search where text like ? order by object_id',('%'+ref+'%',)):
  oid=r[0]
  if ref!='C-0973' and oid not in roots and not oid.startswith(('R-','TR-','READ-','AUDIT-')):continue
  rid=h.current(c,oid);add(rid);routes.append({'citation_literal':ref,'object_id':oid,'revision_id':rid,'full_native_pointer':'/objects/'+rid,'routing_only_not_source_grade':True})
histories={}
for oid in sorted(roots):
 hs=[r[0] for r in c.execute('select id from revision where object_id=? order by version',(oid,))];histories[oid]=hs
 for rid in hs:add(rid)
protectedp=R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json';protected=json.loads(protectedp.read_text())['objects'];assert len(protected)==42
for rid,n in protected.items():assert h.current(c,n['object_id'])==rid and h.native(c,rid)==n
np=h.write(O/'complete-bounded-current744-two-person-and-accepted-support-native-inputs-v1.json',{'objects':pool,'origin_units':units,'documents':docs,'assets_media_metadata':media,'root_object_histories':histories,'native_order':'All origins/evidence/assets/media native rowid order; sourceJSON arrays unchanged','no_source_grade':True})
current744='R-ab847c1960d02f28801419b3@1';assert h.current(c,current744.rsplit('@',1)[0])==current744 and pool[current744]['data']['source_id']=='S-0758'
sourcepath='genealogy/citations/C-0973-hulda-amalia-flen-1940-1955.md';doc=docs[sourcepath];assert 'F0015634_00156' in doc['text'];historicalsha='464e9a5b04fecc67bb8bc7ad36c32b7c94c159b37d93bfd09e21ffea83cb9efd';assert historicalsha in doc['text']
a=[dict(r) for r in c.execute('select * from asset where sha256=? or path like ?',(historicalsha,'%F0015634_00156%'))];na=[dict(r) for r in c.execute('select * from native_asset where sha256=? or original_name like ?',(historicalsha,'%F0015634_00156%'))];candidates=[]
for p in (R/'genealogy/media').rglob('*'):
 if p.is_file() and ('F0015634_00156' in p.name or p.stat().st_size==2101840):candidates.append(h.pin(p))
assert a==na==candidates==[] and not (R/'genealogy2/media/objects'/historicalsha).exists()
mp=h.write(O/'exact744-historical-full-image-route-and-current-local-absence-proof-v1.json',{'current_record':current744,'current_source_id':'S-0758','known_exact_viewer_URL':'https://sok.riksarkivet.se/bildvisning/F0015634_00156','historical_image_ID':'F0015634_00156','historical_dimensions':[7464,5272],'historical_bytes':2101840,'historical_sha256':historicalsha,'frozen_citation_sha256':doc['sha256'],'full_frozen_citation_pointer':'/documents/'+sourcepath.replace('/','~1'),'native_asset_exact_hash_or_ID_rows':na,'archive_asset_exact_hash_or_ID_rows':a,'read_only_archive_exact_ID_filename_or_exact_bytes_candidates':candidates,'native_hashblob_exists':False,'no_remote_fetch_or_image_opening':True,'scope':'Only whole744image ownr10cols9–13 and r9context. Other3folios/sisterbirth/lifereview excluded','current_access_or_returned_bytes':'NOT_VERIFIED_BY_SOL; root must release/fetch and pin actual returned original before Astra reading'})
locp=R/'evaluations/T-0784/mechanical-current442-preparation-v2/bounded-prior-accepted-source-receipt-and-current-native-locator-index-v1.json';loc=json.loads(locp.read_text());rp=[]
for p in loc['groups']['T-0675']:
 assert sha(R/p['path'])==p['sha256'];rp.append(p)
currentPK={}
for person in ['P-0007','P-0017']:
 currentPK[person]=[rid for rid,n in pool.items() if n['kind']=='assessment' and n['data']['subject_id']==person and n['data']['criteria'] in ['legacy_person_contract/'+k for k in ['PK-01','PK-02','PK-05','PK-07','PK-09','PK-11','PK-12']] and h.current(c,n['object_id'])==rid];assert len(currentPK[person])==7
incoming=[dict(r) for r in c.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(current744,))]
reuse=h.write(O/'current-review-and-exact-accepted932r3-860-720-reuse-locators-v1.json',{'native_input_pin':np,'current14identityPK':currentPK,'Maj_acceptedT0784_fullcurrent443_view_pin':h.pin(oldp),'fresh444_fullMaj_view_pin':views['P-0007'],'wholeJSON_and_filebytes_equal':sha(oldp)==views['P-0007']['sha256'],'T0675_existing_receipt_pins':rp,'relevant_exact_citations':['C-0033','C-0972','C-0894','C-0895'],'finite_current_literal_routing':routes,'current744_all_history_incoming':incoming,'no_automatic_grade_or_rebind':True})
assert sha(M)==mainpin['sha256'] and h.all50(c)==before and h.state(c)=={'journal_head':444,'pending':0}
index=h.write(O/'complete-exact744-current444-media-and-accepted-reuse-lock-v1.json',{'task':'T-0788','scope':['P-0007','P-0017','Flen744r9–10'],'actual_main_pin':mainpin,'actual_state':h.state(c),'root_actual444_acceptance_pin':h.pin(acceptp),'shared443_initial_baseline_proof_pin':h.pin(R/'evaluations/T-0786/preparation/fresh443-physical-baseline-logical-all50-and-live-unchanged-v1.json'),'all50_current444_before_and_after_equal':True,'protected42_full_current_exact':True,'whole_person_pins':views,'current_native_input_pin':np,'exact_original_route_and_absence_proof_pin':mp,'accepted_reuse_and_currentPK_incoming_pin':reuse,'root_existing_C0973_inspect_pin':h.pin(R/'evaluations/T-0786/C-0973-scope-routing-current444-inspect.json'),'counts':{'full_native_revisions':len(pool),'frozen_documents':len(docs),'current_identity_PK':14},'no_source_interpretation_remote_original_or_canonical_Wotan_write':True,'next_unperformed':'Root actual original fetch/hash release, then separate Astra own source interpretation','usage':'UNKNOWN pending root collector'});print(json.dumps({'index_pin':index,'counts':json.loads((R/index['path']).read_text())['counts']}));c.close()
