from pathlib import Path
import json,importlib.util,datetime
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
M=R/'genealogy2/data/research.sqlite';main=h.pin(M);c=h.conn(M);assert h.state(c)=={'journal_head':446,'pending':0}
bp=R/'evaluations/T-0786/preparation/baseline-j443.sqlite';b=h.conn(bp)
receiptpaths=['evaluations/T-0786/root-canonical444-access-note-acceptance-v1.json','evaluations/T-0788/root-canonical446-two-access-notes-acceptance-v1.json'];receipts=[]
for path in receiptpaths:
 p=R/path;d=json.loads(p.read_text());receipts.append(h.pin(p))
 for key in ['all50_reviewed_stage_comparison']:
  if key in d:
   q=d[key];assert h.sha(R/q['path'])==q['sha256'];proof=json.loads((R/q['path']).read_text());assert proof['pass'] is True;receipts.append(q)
poolpaths=['evaluations/T-0786/preparation/complete-two-current-history-upstream-OWNER-native-inputs-v1.json','evaluations/T-0787/preparation/complete-bounded-current-history-upstream-source-native-inputs-v1.json','evaluations/T-0788/preparation/complete-bounded-current744-two-person-and-accepted-support-native-inputs-v1.json','evaluations/T-0789/preparation/Maj-current-native-PK-review-register-source-and-accepted-grave-inputs-v1.json'];taskproof=[];headproof={}
for path in poolpaths:
 p=R/path;d=json.loads(p.read_text());ids=sorted({n['object_id'] for n in d['objects'].values()});count=0
 for oid in ids:
  # All input objects existed before the three access-only additions.
  prior=h.current(b,oid);actual=h.current(c,oid);assert actual==prior,(oid,prior,actual);n=h.native(c,actual);old=h.native(b,prior);assert n==old,(oid,'oldfullnative/order difference');count+=1;headproof[oid]={'current_revision_id':actual,'full_native_and_arrays_equal_accepted443':True}
 taskproof.append({'saved_full_native_input_pin':h.pin(p),'existing_current_object_count':count,'all_current_heads_and_whole_native_equal':True})
new=[]
for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.operation_id in (?,?,?) order by r.rowid',('T-0786/shared-Sodertalje-uppslag15-access-note-v1','T-0788/dated-bounded-access-search-note-v1','T-0789/dated-bounded-access-search-note-v1')):
 n=h.native(c,r['id']);assert n['kind']=='search' and n['version']==1 and n['previous_id'] is None and n['origins']==[] and n['data']['question_id'] is None;new.append(n)
assert len(new)==3
# PersonView's actual linked/search SQL excludes these originless/null-question additions.
# Existing selection tables/current values were proven unchanged by exact accepted all50 chain.
viewproof=[]
viewpaths={'P-0003':'evaluations/T-0786/preparation/P-0003-whole-current-person.json','P-0007':'evaluations/T-0788/preparation/P-0007-whole-current444-person.json','P-0241':'evaluations/T-0787/preparation/P-0241-current-j443.json','P-0246':'evaluations/T-0787/preparation/P-0246-current-j443.json','P-0017':'evaluations/T-0788/preparation/P-0017-whole-current444-person.json'}
for person,path in viewpaths.items():
 v=json.loads((R/path).read_text());assert v['id']==person
 for n in new:
  rid=n['id'];linked=c.execute('select count(*) from origin o join unit u on u.id=o.unit_id where o.revision_id=? and u.owner_id=?',(rid,person)).fetchone()[0];targets=c.execute('select count(*) from current_unit_target t join unit u on u.id=t.unit_id where t.target_id=? and u.owner_id=?',(n['object_id'],person)).fetchone()[0];assert linked==targets==0
 viewproof.append({'person':person,'accepted_full_view_pin':h.pin(R/path),'all_existing_selected_head_native_values_exact':True,'new_search_notes_do_not_satisfy_personView_search_link_predicates':True,'whole_current_view_reuse':'Exact original query dependencies unchanged; no duplicate fullCLIcapture or new semanticread','domain_query_code_pin':h.pin(R/'genealogy2/lib/domain.mjs'),'domain_query_location':'personView lines252–288'})
pp=R/'evaluations/T-0781/mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json';protected=json.loads(pp.read_text())['objects'];assert len(protected)==42
for rid,n in protected.items():assert h.current(c,n['object_id'])==rid and h.native(c,rid)==n
media=json.loads((R/'evaluations/T-0787/preparation/root-local-media-hashes-v1.json').read_text())['media'];assert len(media)==3
for p in media:assert h.sha(R/p['path'])==p['sha256'] and (R/p['path']).stat().st_size==p['bytes']
freezepins=[]
for path in ['evaluations/T-0787/source-review/own-three-local-originals-full-relevant-reading-freeze-v1.json','evaluations/T-0787/independent-review/own-three-full-relevant-original-reading-freeze-v1.json','evaluations/T-0787/source-review/three-local-originals-comparative-settled-source-fields-v1.json','evaluations/T-0787/root-required3011-hold-and-exact-source-quality-resumption-pins-v1.json']:freezepins.append(h.pin(R/path))
logs=[]
for t in ['T-0786','T-0787','T-0788','T-0789']:
 p=R/('wotan/dev-log/'+t+'.md');text=p.read_text();i=text.rfind('## Återupptagning');logs.append({'task':t,'tasklog_pin':h.pin(p),'latest_checkpoint_full':text[i:]})
backlogp=R/'wotan/backlog.json';bk=json.loads(backlogp.read_text());entries=[t for t in bk['tasks'] if t['id'] in ['T-0786','T-0787','T-0788','T-0789']]
assert h.pin(M)==main and h.state(c)=={'journal_head':446,'pending':0}
out=h.write(O/'bounded-current446-existing-heads-fullnative-view-reuse-and-three-access-notes-reconciliation-v1.json',{'tasks':['T-0786','T-0787','T-0788','T-0789'],'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main_pin':main,'actual_state':h.state(c),'accepted444_446_all50_proof_pins':receipts,'original_443_physical_baseline_pin':h.pin(bp),'per_saved_input_head_reconciliation':taskproof,'unique_existing_current_head_proofs':headproof,'current_view_reuse_bindings':viewproof,'changed_only_native_objects_three_access_notes':new,'protected42_fullcurrent_native_unchanged':True,'three_original_media_pins_unchanged':media,'existing_three_original_reading_and_comparative_freeze_pins':freezepins,'tasklog_latest_checkpoints':logs,'actual_backlog_pin':h.pin(backlogp),'actual_four_task_entries':entries,'no_source_interpretation_new_original_build_apply_or_Wotan_write':True,'next_unperformed':'Root exact authenticated original3011 retrieval/release and Astra ownreading; existing3source readings remain reusable','usage':'UNKNOWN pending root collector'});print(json.dumps({'pin':out,'unique_existing_current_heads':len(headproof),'actual_state':h.state(c)}));c.close();b.close()
