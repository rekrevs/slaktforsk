"""Build exact source-owned nine-target draft only; never apply."""
import json,hashlib,copy
from pathlib import Path
R=Path(__file__).resolve().parents[3]; B=R/'evaluations/T-0784';O=B/'implementation/exact-nine-settled-draft-v1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(Path(p).relative_to(R)),'sha256':sha(p)}
def write(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
specpath=B/'source-review/six-native-review-and-three-Maj-copy-exact-source-specification-v3.json';assert sha(specpath)=='4e894f94981d72c7b3460aaf12399a81ad9323e3bd9a43a3946d32f7f9c165c1';s=json.loads(specpath.read_text())
gpath=B/'exact-nine-source-spec-mechanical-guards-v1/exact-nine-individual-full-consequence-and-mechanical-guards-v1.json';assert sha(gpath)=='6be138123ec789632be7efed9b5a98a56d4b1400f803b9eb84d49fb51b15abe3';g=json.loads(gpath.read_text());assert not g['issues'] and g['counts']['incoming_all_history']==0
main=R/'genealogy2/data/research.sqlite';assert sha(main)=='42321e363573c243597aded458e6a10d2d6cd8e4be47da02a227b149bbaed45f'
byid={x['object_id']:x for x in s['specifications']};assert not O.exists();O.mkdir()
changes=[];preservation=[]
for oid in s['required_order']:
 x=byid[oid];new=x['full_new_API'];changes.append(copy.deepcopy(new))
 if x['action']=='revise':
  old=x['full_old_API'];rebuild=copy.deepcopy(old)
  for e in x['exact_changes']:
   k=e['field'].split('.');assert len(k)==2 and k[0]=='data' and rebuild['data'][k[1]]==e['old'];rebuild['data'][k[1]]=e['new']
  assert new['evidence'][:len(old['evidence'])]==old['evidence'];rebuild['evidence']=copy.deepcopy(new['evidence']);assert rebuild==new
  clauseproof=[]
  if 'exact_clause_replacements' in x:
   body=old['data']['markdown']
   for e in x['exact_clause_replacements']:
    count=body.count(e['old']);assert count==1;body=body.replace(e['old'],e['new']);clauseproof.append({'old_literal':e['old'],'new_literal':e['new'],'exact_old_count':count})
   assert body==new['data']['markdown']
  preservation.append({'object_id':oid,'whole_API_reconstruction_equal':True,'existing_evidence_ordered_prefix_exact':True,'appended_exact_source_edges':new['evidence'][len(old['evidence']):],'literal_clause_guards':clauseproof,'every_other_metadata_field_array_exact':True})
operation={'id':'T-0784/three-native-identity-tree-and-Maj-current-copy-v1','actor':'Codex bounded settled implementation','reason':'T-0784: exact source-owned nine-target package; six separate native identity/tree axes and three explicitly settled Maj current-copy revisions. Historical reviews, OWNER, relations and life scope preserved.','dependencyReviewVersion':2,'changes':changes}
op=write(O/'01-exact-nine-source-settled-operation-v1.json',operation)
member={**op,'operation_id':operation['id'],'changes':9}
m=write(O/'exact-nine-ordered-operation-membership-v1.json',{'task':'T-0784','operations':[member],'targets':s['required_order'],'target_count':9,'source_spec_pin':pin(specpath),'mechanical_guard_pin':pin(gpath)})
p=write(O/'exact-nine-stage-ready-proposal-v1.json',{'task':'T-0784','status':'DRAFT_ONLY_REQUIRES_SEPARATE_PRIMARY_INDEPENDENT_AND_ROOT_STAGE_AUTHORIZATION','membership_pin':m,'operations':[member],'source_spec_pin':pin(specpath),'mechanical_guard_pin':pin(gpath),'target_count':9,'operation_count':1,'stage_runtime':'UNRUN','canonical_runtime':'UNRUN','individual_actual_request_grades_required':True})
proof=write(O/'exact-three-copy-literals-full-API-and-metadata-preservation-proof-v1.json',{'rows':preservation,'source_spec_pin':pin(specpath),'operation_pin':op,'full_approved_API_equal_all9':operation['changes']==[byid[t]['full_new_API'] for t in s['required_order']],'main_unchanged':sha(main)==g['MAIN_pin']['sha256']})
print(json.dumps({'proposal':p,'membership':m,'operation':op,'preservation_proof':proof}))
