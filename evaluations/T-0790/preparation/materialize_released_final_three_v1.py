"""Root-released mechanical3 full APIs/table only; NO apply or source judgment."""
from pathlib import Path
import json,hashlib,importlib.util,time
R=Path(__file__).resolve().parents[3];O=R/'evaluations/T-0790/preparation';S=O/'reviewed-stage-v1';start=time.monotonic()
p=R/'evaluations/T-0790/source-review/final-semantic-three-amendments-and-two-retains-v1.json';assert hashlib.sha256(p.read_bytes()).hexdigest()=='5dc7ffd59432fecf655c68e2cad416a23ec794217402535a1abb198ebe6c27c1';source=json.loads(p.read_text())
sp=importlib.util.spec_from_file_location('m',O/'stage_literal_authorized_v1.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);assert m.sha(m.LIB)==m.LIB_SHA
hp=importlib.util.spec_from_file_location('h',m.LIB);h=importlib.util.module_from_spec(hp);hp.loader.exec_module(h)
db=S/'stage.sqlite';assert h.sha(db)==source['source_stage_sha256'];stage=h.conn(db);main=h.conn(m.MAIN);bs=json.loads((O/'baseline-state.json').read_text());assert h.sha(m.MAIN)==bs['main']['sha256'] and h.state(stage)=={'journal_head':456,'pending':0} and h.state(main)=={'journal_head':454,'pending':0}
pool={};units={};documents={};hist={}
def capture(rid):
 if rid in pool:return pool[rid]
 n=m.native(h,stage,rid);pool[rid]=n
 for e in n['origins']:
  u=dict(stage.execute('select * from unit where id=?',(e['unit_id'],)).fetchone());units[u['id']]=u
  documents[u['document_path']]=dict(stage.execute('select * from document where path=?',(u['document_path'],)).fetchone())
 for e in n['evidence']:capture(e['basis_revision_id'])
 return n
changes=[];rows=[];retains=[]
for x in source['changes']:
 rid=x['target_revision'];n=capture(rid);assert h.current(stage,n['object_id'])==rid==h.current(main,n['object_id']) and n==m.native(h,main,rid);assert n['version']==x['expectedVersion'] and n['kind']==x['kind'] and x['field']=='data.body' and n['data']['body']==x['old_body'] and x['outcome_change'] is False
 api=h.api(n);api['expectedVersion']=n['version'];old=json.loads(json.dumps(api));api['data']['body']=x['new_body'];api['caveat']=n['caveat']+'\n\n'+x['amendment_caveat'];edge_decisions=[]
 for edge in x['additional_evidence']:
  basis=h.current(stage,edge['object']);assert basis==edge['object']+'@'+str(edge['version']);capture(basis)
  same=[e for e in api['evidence'] if all(e[k]==edge[k] for k in ['object','version','role'])];assert len(same)<=1
  if same:edge_decisions.append({'source_literal':edge,'decision':'reuse existing exact edge and original note','actual_edge':same[0]})
  else:api['evidence'].append(edge);edge_decisions.append({'source_literal':edge,'decision':'append exact in source order','actual_edge':edge})
 assert api['origins']==old['origins'] and all(api[k]==old[k] for k in ['rationale','disposition','evidenceStatus','kind','id','expectedVersion']) and all(api['data'][k]==z for k,z in old['data'].items() if k!='body')
 changes.append(api);rows.append({'old_native':n,'old_full_api':old,'new_api':api,'source_disposition':'revise','rationale':x['reason'],'exact_old_new_fields':{'body':{'old':x['old_body'],'new':x['new_body']},'caveat':{'old':n['caveat'],'new':api['caveat']}},'literal_evidence_consequences':edge_decisions,'source_spec':x,'actual_MAIN454_equals_stage456_original_target':True})
for x in source['retains']:
 rid=x['target_revision'];n=capture(rid);assert h.current(stage,n['object_id'])==rid==h.current(main,n['object_id']) and n==m.native(h,main,rid);retains.append({'revision_id':rid,'old_native':n,'source_disposition':'retain','rationale':x['reason'],'exact_source_scope':x,'actual_MAIN454_equals_stage456':True})
for oid in sorted({n['object_id'] for n in pool.values()}):
 hist[oid]=[r[0] for r in stage.execute('select id from revision where object_id=? order by version',(oid,))]
 for rid in hist[oid]:capture(rid)
assert len(changes)==3 and len(retains)==2
out=O/'final-three-literal-draft-v1';assert not out.exists();out.mkdir()
op={'id':'T0790-final-three-semantic-consequence-amendments-v1','actor':'Codex/Sol-literal-final-three-source-decisions','reason':'T-0790 AC2/3/5: tre nödvändiga semantiska följdrättelser i befintliga native research/PK05, två exakta observationsbehållanden. Ingen syskonrelation, identitets-/trädgrind eller ny livs-/källforskning beslutas. Source spec SHA '+h.sha(p),'dependencyReviewVersion':2,'changes':changes}
op_pin=h.write(out/'operation-final-three-literal.json',op);membership=[h.pin(O/'materialized-source-v3-literal-v1/operation-literal.json'),h.pin(O/'exact-nine-request-only-resolution-draft-v1/resolve-literal.json'),op_pin]
inputpin=h.write(out/'full-five-actual-native-support-history-origins-MAIN454-stage456.json',{'objects':pool,'origin_units':units,'documents':documents,'histories':hist,'all5current_MAIN454_stage456_fullnative_equal':True,'reading':'mechanical availability only no new original/source interpretation'})
tablepin=h.write(out/'final-three-and-two-retains-consequence-table.json',{'operation_sha256':op_pin['sha256'],'source_spec_pin':h.pin(p),'baseline_input_pin':inputpin,'stage_before_pin':h.pin(db),'changes':rows,'retains':retains,'ordered_three_operation_membership':membership,'no_native_relation_identity_tree_change':True,'all90_and_six_life_outcomes':'UNCHANGED','new_pending_count':'UNTESTED_REQUIRE_ACTUAL_STAGE_CONTEXT_AND_ASTRA_DECISIONS'})
h.write(out/'mechanical-draft-result.json',{'operation_pin':op_pin,'table_pin':tablepin,'input_pin':inputpin,'ordered_three_operation_membership':membership,'actualbefore':h.state(stage),'fullfive_main_stage_equality':True,'runtime_apply':False,'final_literal_source_and_independent_hash_gates_required':True,'elapsed_monotonic_seconds':time.monotonic()-start});assert h.sha(db)==source['source_stage_sha256'] and h.sha(m.MAIN)==bs['main']['sha256'];print(json.dumps({'operation':op_pin,'table':tablepin,'inputs':inputpin,'elapsed':time.monotonic()-start}));stage.close();main.close()
