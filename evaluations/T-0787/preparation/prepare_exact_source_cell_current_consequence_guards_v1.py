from pathlib import Path
import json,hashlib,importlib.util
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent;hpath=R/'evaluations/T-0784/implementation/stage_root_authorized_exact_nine_v2.py';s=importlib.util.spec_from_file_location('h',hpath);h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
source=R/'evaluations/T-0787/source-review/three-local-originals-comparative-settled-source-fields-v1.json';assert h.sha(source)=='2f3ecd7cf6a92eda162f4516c0ddff2885456496086fc58af2ee14d3af2a4e0d';spec=json.loads(source.read_text());oldpath=O/'complete-bounded-current-history-upstream-source-native-inputs-v1.json';old=json.loads(oldpath.read_text());c=h.conn(R/'genealogy2/data/research.sqlite');m=h.pin(R/'genealogy2/data/research.sqlite');assert h.state(c)=={'journal_head':444,'pending':0}
ids={x['record'].rsplit('@',1)[0] for x in spec['settled_source']};selected={};clauses=[];allPK={};incoming=[]
terms=['28/2','28/1','60','388','394','Dop','dop','föräldrar','J. A.','J.A.','Vidusina','3011','kolumn','Kolumn','13','Villy','1922','1927','17/1','19/1','17/11','19/11','28/2','Storg','blyerts','oläst','utvunnen']
for rid,n in old['objects'].items():
 if h.current(c,n['object_id'])!=rid:continue
 pk=n['kind']=='assessment' and n['data']['subject_id'] in ['P-0241','P-0246'] and n['data']['criteria'].startswith('legacy_person_contract/')
 research=n['object_id'].startswith(('BIO-P-0241','BIO-P-0246','RESEARCH-P-0241','RESEARCH-P-0246','ASSESSMENT-P-0241','ASSESSMENT-P-0246'))
 family=n['object_id'] in ids or n['data'].get('record_id') in ids or n['data'].get('subject_id') in ids
 text=json.dumps({'data':n['data'],'caveat':n['caveat'],'rationale':n['rationale']},ensure_ascii=False);literal=any(ref in text for ref in ['C-0244','C-0246','C-0933'])
 if not (pk or research or family or literal):continue
 fresh=h.native(c,rid);assert fresh==n,('Exact old/native mismatch',rid);selected[rid]=fresh
 if pk:allPK[rid]=fresh
 fields=[]
 for k,v in {**{'caveat':n['caveat'],'rationale':n['rationale']},**{'data.'+k:v for k,v in n['data'].items() if k!='revision_id'}}.items():
  if isinstance(v,str):
   hits=[x for x in terms if x in v]
   if hits or family or pk or research:fields.append({'field':k,'whole_exact_old':v,'matched_literal_terms':hits,'new_native_field':'NOT_SUPPLIED_IN_SOURCE_CELL_SPEC; exact perobject API/old/new required before draft'})
 clauses.append({'object_id':n['object_id'],'version':n['version'],'revision_id':rid,'kind':n['kind'],'full_old_native_pointer':'/objects/'+rid,'source_family':family,'literal_citation_copy':literal,'current14PK_or_research':pk or research,'fields':fields,'source_disposition_pin':h.pin(source),'source_bound_cells_and_retains_pointer':'/settled_source and /comparative_retains','native_amendment_state':'PENDING_EXPLICIT_NATIVE_FIELD_SPEC_NO_INFERENCE'})
 for e in c.execute('select rowid as native_rowid,* from dependency where basis_revision_id=? order by rowid',(rid,)):
  edge=dict(e);oid=edge['revision_id'].rsplit('@',1)[0];edge['caller_current_revision_id']=h.current(c,oid);edge['caller_is_current']=edge['revision_id']==edge['caller_current_revision_id'];incoming.append(edge)
assert h.sha(R/'genealogy2/data/research.sqlite')==m['sha256']
out=h.write(O/'exact-current-source-family-copy-field-consequence-and-incoming-guards-v1.json',{'task':'T-0787','source_disposition_pin':h.pin(source),'previous_full_native_dictionary_pin':h.pin(oldpath),'actual_main_pin':m,'actual_state':h.state(c),'objects':selected,'individual_field_table':clauses,'settled_source_cells_and_retains':spec['settled_source'],'comparative_retains':spec['comparative_retains'],'source_scope_limits':spec['source_scope_limits'],'all_selected_whole_native_current_equal_previous443':True,'immediate_all_history_incoming':incoming,'zero_or_multiple_replacement_guards':'UNRUN; exact native replacements have not been specified','no_operations_stage_or_grade_constructed':True});print(json.dumps({'pin':out,'selected_current_objects':len(selected),'incoming':len(incoming)}));c.close()
