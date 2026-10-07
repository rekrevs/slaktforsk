"""Three exact source-approved finite drafts, no runtime/stage code path."""
import json,hashlib,ast
from pathlib import Path
parent=Path('evaluations/T-0781/build_settled_core_and_PATH98_drafts_v2.py')
source=parent.read_text();definitions=source[:source.index('assert W.exists();')]
tree=ast.parse(definitions);assert all(isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef,ast.Expr)) for n in tree.body)
exec(compile(definitions,str(parent),'exec'))
W=B/'implementation/C0049-small14-copy104-C0067-clause22-drafts-v1';assert not W.exists();W.mkdir()
configs=[
 ('C0049-fourteen-small-native-field-consequence-specifications-v1.json','4c6cdd79ce958f8cd8a8456ca5917410bce8c87e13f65a35962c963849804657','C0049-small14-and-C0067-P0098-exact-current-field-overlap-allhistory-incoming-guards-v1.json','C0049-small14',14),
 ('C0049-finite-current-narrative-contract-path-key-theme-caveat-specifications-v1.json','ed77f47a4a27190c8dd4abd052518656f078eca3573cc452b72874cc42a72df2','C0049-finite104-exact-current-oldfield-overlap-and-allhistory-incoming-guards-v1.json','C0049-current-copy104',104),
 ('C0067-twentytwo-finite-witness-current-clause-decisions-v1.json','4a91e5bae6c126feb85c337306618dad4492dd922bd764a5c95f2b75dc4e4888','C0067-finite22-exact-current-oldfield-overlap-and-allhistory-incoming-guards-v1.json','C0067-current-witness-clause22',22)]
incoming=B/'source-review/C0049-seven-mention-and-one-event-incoming-exact-source-dispositions-v1.json';assert pin(incoming)['sha256']=='06c66681211d3c5c9b445b81eac769fbec14a3278f3992cfbc7c7e7a5ebe9b80';assert load(incoming)['dependent_small14_draft_production_permitted'] is True
operations=[];tables=[];allids=set();protected=load(B/'mechanical-current425-preparation-v1/complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json')['objects'];protected_oids={x['object_id'] for x in protected.values()}
for no,(name,expected,guardname,label,count) in enumerate(configs,1):
 sp=B/'source-review'/name;assert pin(sp)['sha256']==expected;s=load(sp);gp=B/'bounded-consequence-inputs-v1'/guardname;g=load(gp);gr={x['object_id']:x for x in g.get('rows',[])};changes=[];rows=[]
 assert len(s['objects'])==count
 for i,x in enumerate(s['objects']):
  oid=x['object_id'];assert oid not in allids and oid not in protected_oids;allids.add(oid);guard=gr[oid]
  assert not guard.get('existing_draft_overlap',[]) and not guard.get('fourteen_small_spec_overlap',False) and not guard.get('other_source_or_draft_target_overlap',False)
  edges=guard.get('allhistory_incoming',[])
  if label!='C0049-small14':assert edges==[]
  else:
   approved=load(incoming)['rows']
   for edge in edges:
    assert any(a.get('edge')==edge['edge'] for a in approved),('Unapproved incoming edge',oid,edge['edge'])
  old,new=revise(x,x['current']);changes.append(new)
  rows.append({'object_id':oid,'source_row_pointer':'/objects/'+str(i),'baseline_revision_ID':x['current']['id'],'old_API':old,'new_API':new,'source_exact_edits':x['edits'],'source_explicit_rebinds':x.get('evidence_rebinds',[]),'source_same_register_support_addition':x.get('evidence_addition'),'retains':x.get('preserve',x.get('retain')),'exact_current_oldfield_guards':True,'incoming_guard_pointer':'/rows/'+str(g.get('rows',[]).index(guard)),'incoming_source_closure_pin':pin(incoming) if edges else None,'source_reasons':x.get('source_scope_reasons',x.get('reason'))})
 assert len(changes)==count
 operations.append(operation(no,label,changes,pin(sp)))
 tables.append(save(label+'-full-individual-consequence-and-preservation-table-v1.json',{'source_spec_pin':pin(sp),'guard_pin':pin(gp),'operation_pin':operations[-1],'rows':rows,'ordered_changes_equal_source_rows':True,'source_declared_execution_order':s.get('execution_order'),'array_order_and_all_unamended_fields_preserved':True,'scope_grade_not_inferred':True,'stage':'UNRUN'}))
result=save('three-exact-settled-module-draft-operation-consequence-index-v1.json',{'task':'T-0781','operation_pins':operations,'individual_consequence_tables':tables,'counts':[14,104,22],'unique_targets':len(allids),'protected42_targets_intersection':[],'incoming_small14_exact_closure_pin':pin(incoming),'mechanical_builder_function_definition_pin':pin(parent),'stage':'UNRUN','canonical_apply':'UNRUN','global_source_and_independent_pre_stage_gates':'PENDING'})
print(json.dumps({'index_pin':result,'operation_pins':operations},indent=2))
