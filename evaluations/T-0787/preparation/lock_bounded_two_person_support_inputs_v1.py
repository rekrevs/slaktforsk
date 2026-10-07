"""Finite T0787 current/source/media/accepted-reuse preparation; no interpretation."""
from pathlib import Path
import json,hashlib,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;M=R/'genealogy2/data/research.sqlite'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
helper=R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py';sp=importlib.util.spec_from_file_location('readonly',helper);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
pre=R/'evaluations/T-0786/preparation';proof=json.loads((pre/'fresh443-physical-baseline-logical-all50-and-live-unchanged-v1.json').read_text());assert sha(M)==proof['MAIN_pin']['sha256'];c=h.conn(M);b=h.conn(R/proof['baseline_pin']['path']);assert h.state(c)=={'journal_head':443,'pending':0} and h.all50(c)==h.all50(b)==proof['all50_before']
views={};roots=set();people=['P-0241','P-0246']
def ids(v):
 if isinstance(v,dict):
  if isinstance(v.get('revision_id'),str) and '@' in v['revision_id']:roots.add(v['revision_id'].rsplit('@',1)[0])
  for w in v.values():ids(w)
 elif isinstance(v,list):
  for w in v:ids(w)
for person in people:
 p=O/(person+'-current-j443.json');v=json.loads(p.read_text());assert v['id']==person;ids(v);views[person]=h.pin(p)
explicit=['R-bed92fa4152f5dd32d822b7e','R-9c672efe54c8704ede86a593','R-9e4b38c1a17678952adff8e8','S-0194','S-0731'];roots.update(explicit)
# Exactly named old accepted sources only, current matching support rows and their own audits.
selected_refs=['C-0240','C-0242','C-0243','C-0935','C-0244','C-0246','C-0933']
routeids=set()
for term in selected_refs:
 for r in c.execute('select distinct object_id from object_search where text like ? order by object_id',('%'+term+'%',)):routeids.add(r[0])
roots.update(routeids)
pool={};units={};docs={};assets={};hist={}
def add(rid):
 if rid in pool:return
 n=h.native(c,rid);pool[rid]=n
 for e in n['origins']:
  u=dict(c.execute('select * from unit where id=?',(e['unit_id'],)).fetchone());units[u['id']]=u;d=dict(c.execute('select * from document where path=?',(u['document_path'],)).fetchone());docs[d['path']]=d
 for e in n.get('assets',[]):
  d=dict(c.execute('select * from asset where path=?',(e['asset_path'],)).fetchone());assets['asset:'+d['path']]=d
 for e in n.get('media',[]):
  d=dict(c.execute('select * from native_asset where id=?',(e['asset_id'],)).fetchone());assets['native:'+d['id']]=d
 for e in n['evidence']:add(e['basis_revision_id']);add(h.current(c,e['basis_revision_id'].rsplit('@',1)[0]))
for oid in sorted(roots):add(h.current(c,oid))
for oid in sorted(roots):
 history=[r[0] for r in c.execute('select id from revision where object_id=? order by version',(oid,))];hist[oid]=history
 for rid in history:add(rid)
for oid in explicit[:3]:assert h.current(c,oid)==oid+'@1'
requirements={};axes={}
for person in people:
 rs=[];ax=[]
 for rid,n in pool.items():
  if n['kind']=='assessment' and n['data']['subject_id']==person and h.current(c,n['object_id'])==rid:
   criterion=n['data']['criteria']
   if criterion in ['legacy_person_contract/'+x for x in ['PK-01','PK-02','PK-05','PK-07','PK-09','PK-11','PK-12']]:rs.append(rid)
   if criterion in ['identity_review/1','tree_effect/1','life_picture_review/1','legacy_review_header']:ax.append(rid)
 assert len(rs)==7,(person,rs);requirements[person]=sorted(rs);axes[person]=sorted(ax)
dictpin=h.write(O/'complete-bounded-current-history-upstream-source-native-inputs-v1.json',{'objects':pool,'origin_units':units,'documents':docs,'assets_media_metadata':assets,'full_root_histories':hist,'data_arrays_and_evidence_origins_media_order':'Native rowid order; embedded JSONtext unchanged','no_source_grade':True})
incoming=[]
for oid in explicit[:3]:
 for r in c.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(oid+'@1',)):
  e=dict(r);n=h.native(c,e['revision_id']);e['caller_current_revision_id']=h.current(c,n['object_id']);e['caller_is_current']=e['caller_current_revision_id']==e['revision_id'];incoming.append(e)
routepin=h.write(O/'finite-current-consequence-object-and-exact-incoming-locators-v1.json',{'dictionary_pin':dictpin,'citation_literal_matched_current_ids':sorted(routeids),'explicit_target_current_ids':{oid:h.current(c,oid) for oid in explicit},'current_seven_PK':requirements,'current_native_and_legacy_review_ids':axes,'target_current_basis_all_history_incoming':incoming,'routing_is_not_source_person_or_amendment_grade':True})
media=json.loads((O/'root-local-media-hashes-v1.json').read_text());assert len(media['media'])==3
for p in media['media']:assert sha(R/p['path'])==p['sha256'] and (R/p['path']).stat().st_size==p['bytes']
loc=R/'evaluations/T-0784/mechanical-current442-preparation-v2/bounded-prior-accepted-source-receipt-and-current-native-locator-index-v1.json';prior=json.loads(loc.read_text());receiptpins=[]
for task in ['T-0674','T-0675']:
 for p in prior['groups'][task]:assert sha(R/p['path'])==p['sha256'];receiptpins.append(p)
ops=[]
for row in c.execute('select sequence,operation_id,request_json from operation_payload where sequence in (138,141,143) order by sequence'):
 d=dict(row);d['exact_request_JSON_retained']=True;ops.append(d)
reusepin=h.write(O/'exact-accepted-T0674-T0675-receipt-and-operation-scope-lock-v1.json',{'prior_locator_pin':h.pin(loc),'existing_receipt_pins':receiptpins,'accepted_operation_payloads':ops,'explicit_reuse_citation_scope':{'T-0674':['C-0240','C-0242','C-0243'],'T-0675':['C-0935']},'current_full_TR_audit_and_stronger_support_present_in_dictionary':dictpin,'limits':'Actual individual receipt/source scope remains authoritative; no blanket coverage grade or repeated original interpretation'})
assert sha(M)==proof['MAIN_pin']['sha256'] and h.state(c)=={'journal_head':443,'pending':0} and h.all50(c)==proof['all50_before']
index=h.write(O/'complete-bounded-current443-source-media-and-accepted-reuse-lock-v1.json',{'task':'T-0787','main_pin':h.pin(M),'actual_state':h.state(c),'shared443_all50_baseline_proof_pin':h.pin(pre/'fresh443-physical-baseline-logical-all50-and-live-unchanged-v1.json'),'shared_protected42_exact':True,'whole_person_input_pins':views,'root_inspect_pins':[h.pin(O/(ref+'-current-j443.json')) for ref in ['C-0244','C-0246','C-0933']],'native_input_pin':dictpin,'consequence_and_incoming_pin':routepin,'accepted_reuse_pin':reusepin,'three_original_media_pins':media['media'],'counts':{'full_native_revisions':len(pool),'documents':len(docs),'literal_current_route_ids':len(routeids),'identity_PK':14},'C0933_fol2995_original':'C-0934-riksarkivet-00205124_00243.jpg, SHA46c9adde…; no BI5 substitution','folio3011':'Explicit existing manifest Image00259 routing only until own2995 source reading; Sol has not opened either','no_original_or_remote_access':True,'source_or_native_grades':'NONE','Wotan_or_canonical_mutations':False,'future_T0786_search_apply_requires_fresh_live_journal_baseline_check_before_T0787_apply':True,'usage':'UNKNOWN pending root collector'})
print(json.dumps({'index_pin':index,'counts':json.loads((R/index['path']).read_text())['counts']}));c.close();b.close()
