from pathlib import Path
import json,copy,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('h',R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);c=h.conn(R/'genealogy2/data/research.sqlite');m=h.pin(R/'genealogy2/data/research.sqlite');assert h.state(c)=={'journal_head':444,'pending':0}
p=R/'evaluations/T-0787/source-review/fifteen-core-source-and-current-identity-copy-exact-fields-spec-v2.json';assert h.sha(p)=='5a5e53d5603a315aa5668a9216280054496b199ae84ad69bf815e6ccfe3e817f';spec=json.loads(p.read_text());assert [r['object_id'] for r in spec['rows']]==spec['source_core_order'];assert len(set(spec['source_core_order']))==15
rows=[];incoming=[];caller_objects={};headmap={};issues=[]
for i,row in enumerate(spec['rows']):
 oid=row['object_id'];rid=oid+'@'+str(row['expected_version']);assert h.current(c,oid)==rid;old=h.native(c,rid);assert old==row['whole_old_native'];a=h.api(old);a['expectedVersion']=row['expected_version'];original=copy.deepcopy(a)
 for e in row['field_edits']:
  target=a;keys=e['field'].split('.')
  for k in keys[:-1]:target=target[k]
  assert target[keys[-1]]==e['old'],(oid,e['field']);target[keys[-1]]=copy.deepcopy(e['new'])
 for reb in row['evidence_rebinds']:
  matches=[(j,x) for j,x in enumerate(a['evidence']) if x['object']==reb['basis_object_id'] and x['version']==reb['old_version'] and x['role']==reb['role']];assert len(matches)==1,(oid,'zero/multiple specified rebind',reb);matches[0][1]['version']=reb['new_version']
 for e in row.get('evidence_additions',[]):
  assert not any((x['object'],x['version'],x['role'])==(e['object'],e['version'],e['role']) for x in a['evidence']);a['evidence'].append(copy.deepcopy(e))
 for e in a['evidence']:
  actualhead=headmap.get(e['object'],int(h.current(c,e['object']).rsplit('@',1)[1]));
  if actualhead!=e['version']:issues.append({'object_id':oid,'edge':e,'expected_current_head_at_step':actualhead,'source_question':'Existing unchanged basis would be stale at this producer order; no automatic rebind'})
 headmap[oid]=row['expected_version']+1
 edges=[]
 for r in c.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(rid,)):
  e=dict(r);caller=h.native(c,e['revision_id']);curr=h.current(c,caller['object_id']);e['caller_current_revision_id']=curr;e['caller_is_current']=curr==e['revision_id'];edges.append(e);incoming.append(e);caller_objects[e['revision_id']]=caller;caller_objects[curr]=h.native(c,curr)
 rows.append({'source_spec_row_pointer':'/rows/'+str(i),'object_id':oid,'expected_version':row['expected_version'],'full_old_native':old,'full_old_API_current_version':original,'exact_NEW_field_evidence_reconstruction_NOT_operation':a,'literal_full_old_fields_exact':True,'only_explicit_field_edits_and_ordered_rebind_additions':True,'source_disposition':row['source_disposition'],'incoming_disposition_from_spec':row['incoming_disposition'],'all_history_incoming_edges':edges,'all_nonzero_incoming_requires_source_individual_disposition_before_dependent_build':bool(edges)})
for r in spec['retains']:assert h.current(c,r['object_id'])==r['object_id']+'@'+str(r['version'])
extra={}
for oid in ['KEY-P-0253-d7a22d09fff5','BIO-P-0258','RESEARCH-P-0258-9d76f0343410','F-P-0241-children_source_context-six']:
 rid=h.current(c,oid);extra[rid]=h.native(c,rid)
assert h.pin(R/'genealogy2/data/research.sqlite')==m
out=h.write(O/'exact-fifteen-whole-old-field-head-order-evidence-and-incoming-guard-table-v1.json',{'task':'T-0787','source_spec_pin':h.pin(p),'actual_main_pin':m,'actual_state':h.state(c),'rows':rows,'retains':spec['retains'],'all_history_incoming':incoming,'full_incoming_caller_native_payloads':caller_objects,'four_additional_explicit_current_copy_inputs':extra,'sequential_current_basis_head_issues':issues,'status':'GUARDS_PASS_PENDING_INDIVIDUAL_INCOMING_SOURCE_GRADES' if not issues else 'STOP_SOURCE_BASIS_QUESTION','no_operation_stage_canonical_or_Wotan_write':True});print(json.dumps({'guard_table_pin':out,'targets':len(rows),'incoming_edges':len(incoming),'head_issues':issues}));c.close()
