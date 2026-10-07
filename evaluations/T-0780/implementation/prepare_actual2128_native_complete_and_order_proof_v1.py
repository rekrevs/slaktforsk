"""Readonly completed clone payload/evidence insertion-order and baseline equality proof."""
import datetime,hashlib,importlib.util,json,sqlite3
from pathlib import Path
B=Path('evaluations/T-0780');S=B/'full10-stage-final143-v1';W=B/'implementation/actual2128-readonly-preparation-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
def save(n,x):
 p=W/n;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return pin(p)
def conn(p):
 c=sqlite3.connect(p.resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
c=conn(S/'stage.sqlite');baselinepath=B/'preparation/baseline-j281.sqlite';base=conn(baselinepath)
assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==424
assert c.execute('select count(*) from review_request r left join review_resolution s on r.id=s.request_id where s.request_id is null').fetchone()[0]==2128
assert not W.exists();W.mkdir()
helper=B/'implementation/stage_settled_package_v3.py';assert sha(helper)=='7a3d43742f4aa0b697afddd4b3e11e47bdf6c76f82c556106cbc786b7fa7016e'
spec=importlib.util.spec_from_file_location('readonly_stage_helper',helper);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
before=load(S/'baseline-all-table-state.json');actualbase=module.table_state(base);assert before==actualbase
baselinepin=save('immutable-j281-baseline-all50-equals-actual-stage-before-v1.json',{'baseline_file_pin':pin(baselinepath),'actual_stage_before_pin':pin(S/'baseline-all-table-state.json'),'all50_tables_exact_equal':True,'actual_baseline_all_table_state':actualbase})
def native(db,rid,ordered=True):
 row=db.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone()
 if row is None:return None
 n=dict(row);n['data']=dict(db.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone())
 for key,table in [('origins','origin'),('evidence','dependency')]+([('assets','record_asset'),('media','record_media')] if n['kind']=='record' else []):
  n[key]=[dict(x) for x in db.execute('select * from '+table+' where revision_id=?'+(' order by rowid' if ordered else ''),(rid,))]
 return n
def api(n):
 d={k:v for k,v in n['data'].items() if k!='revision_id'}
 for k,v in d.items():
  if k.endswith('_json') and isinstance(v,str):d[k]=json.loads(v)
 a={'id':n['object_id'],'kind':n['kind'],'expectedVersion':n['version']-1 or None,'data':d,'origins':[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in n['origins']],'evidence':[{'object':x['basis_revision_id'].rsplit('@',1)[0],'version':int(x['basis_revision_id'].rsplit('@',1)[1]),'role':x['role'],'note':x['note']} for x in n['evidence']],'disposition':n['disposition'],'evidenceStatus':n['evidence_status'],'rationale':n['rationale'],'caveat':n['caveat']}
 if n['kind']=='record':
  a['assets']=[{'path':x['asset_path'],'region':x['region']} for x in n['assets']];a['media']=[{'id':x['asset_id'],'region':x['region']} for x in n['media']]
 return a
def defaults(x,actual):
 y=json.loads(json.dumps(x));y.setdefault('origins',[]);y.setdefault('evidence',[]);y.setdefault('evidenceStatus',None);y.setdefault('caveat','')
 for k in actual['data']:y['data'].setdefault(k,None)
 for key in ['origins','evidence']:
  for a in y[key]:
   a.setdefault('note','')
   if key=='origins':a.setdefault('coverage','partial')
 if x['kind']=='record':
  for key in ['assets','media']:
   y.setdefault(key,[])
   for a in y[key]:a.setdefault('region','helbild')
 return y
def diff(a,b,path=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append({'field':path+'/'+k,'old_present':k in a,'new_present':k in b,'old':a.get(k),'new':b.get(k)})
   else:out.extend(diff(a[k],b[k],path+'/'+k))
  return out
 return [{'field':path,'old':a,'new':b,'arrays_compared_in_saved_order':True}]
gatepath=B/'source-review/all10-global-primary-source-ready-gate-v6.json';gate=load(gatepath);targets={};oldtargets={};comparisons=[];operationchecks=[]
for i,p in enumerate(gate['operations'],1):
 assert sha(Path(p['path']))==p['sha256'];op=load(p['path']);journal=c.execute('select * from operation_payload where operation_id=?',(op['id'],)).fetchone();assert journal is not None;assert json.loads(journal['request_json'])==op
 operationchecks.append({'index':i,'operation_pin':p,'stage_journal_sequence':journal['sequence'],'entire_ordered_journal_request_equals_approved_API':True})
 for j,x in enumerate(op['changes']):
  rid=x['id']+'@'+str((x['expectedVersion'] or 0)+1);n=native(c,rid);assert n is not None;targets[rid]=n;a=api(n);expected=defaults(x,a);d=diff(expected,a);assert not d,(rid,d)
  defaultnative=native(c,rid,False);presentation=diff(defaultnative,n)
  previous=n['previous_id'];old=native(c,previous) if previous else None
  if old:oldtargets[previous]=old;assert old==native(base,previous)
  comparisons.append({'actual_revision_id':rid,'object_id':x['id'],'operation_pin':p,'approved_API_pointer':'/changes/'+str(j),'actual_native_pointer':'/objects/'+rid.replace('~','~0').replace('/','~1'),'expectedVersion':x['expectedVersion'],'all_API_fields_and_metadata_and_ORDER_BY_rowid_arrays_exact':True,'explicit_domain_default_fields_added':[k for k in expected if k not in x],'actual_data_nullable_fields_absent_in_API':[k for k in a['data'] if k not in x['data']],'native_SQL_default_presentation_vs_rowid_differences':presentation,'previous_revision_id':previous,'full_previous_native_equals_immutable_stage_before':True if old else None,'all_native_previous_to_actual_field_differences':diff(old,n) if old else [{'field':'/','old':None,'new_pointer':'/objects/'+rid}],'no_source_grade':True})
assert len(targets)==893
tp=save('all893-full-actual-native-targets-in-journal-insertion-order-v1.json',{'objects':targets,'array_order':'Explicit ORDER BY rowid retains CLI sequential insertion; complete ordered request independently bound in operation_payload. Default SQL index presentation differences preserved in proof.'})
bp=save('all-previous-native-target-payloads-stage-before-equality-v1.json',{'objects':oldtargets,'baseline_all50_proof_pin':baselinepin,'all_equal_immutable_baseline':True})
pp=save('all893-target-full-API-equality-and-native-order-differences-v1.json',{'gate_pin':pin(gatepath),'actual_native_target_pin':tp,'previous_native_target_pin':bp,'objects':comparisons,'operations':operationchecks,'all143_ordered_API_journal_requests_exact':True,'all893_complete_API_reconstructions_exact':True,'representation_rules':'Only native data revision_id wrapper omitted and JSON text parsed to exact API value; documented domain defaults added. No sort/multiset replacement of ordered arrays.'})
handoff=S/'actual-handoff-v1/full-actual-request-current-and-direct-support-native-payloads-v1.json';prior=load(handoff)['objects'];support={};supportproof=[];new=[]
for rid,oldpresentation in prior.items():
 n=native(c,rid);before=native(base,rid)
 if before is None:new.append(rid);continue
 assert n==before,rid;support[rid]=n
 supportproof.append({'revision_id':rid,'all_fields_with_rowid_array_order_exact_stage_before':True,'previous_handoff_default_SQL_presentation_differences':diff(oldpresentation,n)})
sp=save('all-existing-actual-request-support-full-baseline-native-payloads-v1.json',{'objects':support,'baseline_all50_proof_pin':baselinepin,'all_complete_native_payloads_equal_before_clone':True})
rp=save('all-request-support-baseline-equality-and-query-order-representation-proof-v1.json',{'prior_actual_handoff_pin':pin(handoff),'complete_baseline_native_pin':sp,'objects':supportproof,'new_revision_ids_not_in_baseline':new,'no_sort_or_metadata_loss':True})
summary=save('native-complete-order-and-baseline-proof-index-v1.json',{'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all893_actual_native_pin':tp,'all893_API_and_order_proof_pin':pp,'all_previous_native_targets_pin':bp,'all_existing_request_support_native_pin':sp,'support_equality_order_proof_pin':rp,'baseline_all50_proof_pin':baselinepin,'counts':{'actual_targets':len(targets),'previous_targets':len(oldtargets),'existing_request_support_revisions':len(support),'new_handoff_revisions':len(new),'target_default_SQL_order_differences':sum(bool(x['native_SQL_default_presentation_vs_rowid_differences']) for x in comparisons)},'stage_database_unchanged_pin':pin(S/'stage.sqlite'),'readonly_no_resolution_apply':True})
c.close();base.close();print(json.dumps({'summary':summary,'all893_native':tp,'all893_API_proof':pp,'baseline_support_native':sp,'counts':load(summary['path'])['counts']},indent=2))
