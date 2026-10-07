"""Bounded readonly capture for root's C0049+C0067 lock; no source grades or originals."""
import datetime, hashlib, json, re, sqlite3, subprocess
from pathlib import Path

B=Path('evaluations/T-0781'); W=B/'mechanical-current425-preparation-v1'
MAIN=Path('genealogy2/data/research.sqlite')
def load(p): return json.loads(Path(p).read_text())
def pin(p): return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def checked(p):
 assert pin(p['path'])==p,p
 return load(p['path'])
def save(name,value):
 p=W/name; assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');return pin(p)
def conn(p):
 c=sqlite3.connect(p.resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
def state(c):
 return {'journal_head':c.execute('select max(sequence) from operation_payload').fetchone()[0], 'pending':c.execute('select count(*) from review_request r left join review_resolution s on r.id=s.request_id where s.request_id is null').fetchone()[0]}
def tables(c):
 out={}
 for t,sql in c.execute("select name,sql from sqlite_master where type='table' and name not like 'sqlite_%' order by name"):
  rows=[json.dumps(tuple(x),ensure_ascii=False,separators=(',',':'),default=lambda x:{'blob':x.hex()}) for x in c.execute('select * from "'+t.replace('"','""')+'"')]
  h=hashlib.sha256()
  for s in sorted(rows):h.update(s.encode());h.update(b'\n')
  out[t]={'schema':sql,'rows':len(rows),'sha256':h.hexdigest()}
 return out
def native(c,rid):
 row=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone();assert row is not None,rid
 n=dict(row);n['data']=dict(c.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone())
 for key,table in [('origins','origin'),('evidence','dependency')]+([('assets','record_asset'),('media','record_media')] if n['kind']=='record' else []):
  n[key]=[dict(x) for x in c.execute('select * from '+table+' where revision_id=? order by rowid',(rid,))]
 return n
def cli(args,name):
 p=W/name;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists()
 command=['node','genealogy2/cli.mjs',*args,'--db',str(W/'baseline-j425.sqlite')]
 result=subprocess.run(command,capture_output=True)
 p.write_bytes(result.stdout);e=p.with_suffix(p.suffix+'.stderr');e.write_bytes(result.stderr)
 assert result.returncode==0,(command,result.returncode,result.stderr.decode())
 commands.append({'command':command,'exit_code':result.returncode,'output_pin':pin(p),'stderr_pin':pin(e)})
 return load(p) if p.suffix=='.json' else None

assert not W.exists(); W.mkdir(parents=True)
backlog_before_pin=pin('wotan/backlog.json');tasklog_before_pin=pin('wotan/dev-log/T-0781.md')
recommendation_path=B/'primary-two-metadata-current-reuse-recommendation-v1.json'
recommendation=load(recommendation_path)
assert recommendation['recommended_exact_two']==['C-0049','C-0067']
snapshot=checked(recommendation['current250_snapshot'])
acceptance=checked(recommendation['actual_root_acceptance']); remaining=checked(recommendation['actual_remaining_reconciliation'])
assert acceptance['approved_for_program_acceptance'] and remaining['actual_accepted_count']==10 and remaining['remaining_count']==21
for a in remaining['actual_individually_accepted_receipts']: checked(a['receipt_pin'])
assert set(recommendation['recommended_exact_two']) <= set(remaining['remaining_citations_in_fixed_cohort_order'])
assert pin(MAIN)==recommendation['canonical_baseline']
media=[{**x['image_pin'],'citation':x['citation'],'actual_hash_matches':pin(x['image_pin']['path'])==x['image_pin'],'opened':False} for x in recommendation['source_units']]
assert all(x['actual_hash_matches'] for x in media)
live=conn(MAIN);assert state(live)=={'journal_head':425,'pending':0}
before=tables(live);assert len(before)==50
dest=sqlite3.connect(W/'baseline-j425.sqlite');live.backup(dest);dest.close(); c=conn(W/'baseline-j425.sqlite')
assert tables(c)==before
baseline_pin=save('fresh-all50-baseline-receipts-media-and-actual425-reconciliation-v1.json',{'task':'T-0781','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'live_DB_pin':pin(MAIN),'clone_pin':pin(W/'baseline-j425.sqlite'),'state':state(c),'all50_clone_tables_exact':True,'table_state':before,'recommendation_pin':pin(recommendation_path),'prior_current250_pin':recommendation['current250_snapshot'],'actual_acceptance_pin':recommendation['actual_root_acceptance'],'remaining_reconciliation_pin':recommendation['actual_remaining_reconciliation'],'accepted10_receipts':remaining['actual_individually_accepted_receipts'],'remaining21':remaining['remaining_citations_in_fixed_cohort_order'],'locked_media_actual_pins':media,'new_original_reads':0,'source_scope_approval':False})
protected_ids=[r[0] for r in c.execute("select r.id from revision r left join assessment a on a.revision_id=r.id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) and (r.evidence_status='OWNER_CONFIRMED' or a.criteria in ('identity_review/1','tree_effect/1','life_picture_review/1')) order by r.object_id")]
protected_pin=save('complete-current-OWNER-identity-tree-life-protected-native-payloads-v1.json',{'objects':{rid:native(c,rid) for rid in protected_ids},'count':len(protected_ids),'array_order':'ORDER BY rowid; native JSON text untouched','source_grade':False})
commands=[];persons=sorted({p for x in recommendation['source_units'] for p in x['metadata_person_links_not_certified_source_membership']});assert len(persons)==13
git=subprocess.run(['git','status','--short'],capture_output=True);assert git.returncode==0
(W/'git-status-before.txt').write_bytes(git.stdout)
cli(['inventory'],'current-inventory.json');cli(['pedigree','P-0269'],'current-default-verified-P0269-pedigree.json')
views=[]
for p in persons:
 cli(['person',p],'person-views/'+p+'-overview.md')
 v=cli(['person',p,'--full','--format','json'],'person-views/'+p+'-full.json')
 cli(['inspect',p],'person-views/'+p+'-inspect-history.json')
 research_pin=save('person-views/'+p+'-current-research.json',v.get('research'))
 views.append({'person_id':p,'full_person_pin':pin(W/'person-views'/f'{p}-full.json'),'inspect_history_pin':pin(W/'person-views'/f'{p}-inspect-history.json'),'research_pin':research_pin,'metadata_routed_not_certified_source_person':True})
impact={citation:cli(['impact',citation],'citation-routing/'+citation+'-complete-impact.json') for citation in recommendation['recommended_exact_two']}
current={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) order by r.object_id')}
pool={};selected={};routing=[]
person_pattern=re.compile(r'(?<![\w-])(?:'+ '|'.join(map(re.escape,persons))+r')(?![\w-])')
terms=['C-0049','C0049','C-0067','C0067','Anders Alfred','Barbro Catharina','Barbru Catharina','Barbro Christina','Margareta Euphrosyne','Anna Fredrika','Jacob Andersson','Maria C. Hans','A. Andersson','C. Jacobs','Anna Nilsd','Ytteråträsk','1860-07-05','60 5/7']
def matches(v,pointer=''):
 hits=[]
 if isinstance(v,dict):
  for k,x in v.items():hits+=matches(x,pointer+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(v,list):
  for i,x in enumerate(v):hits+=matches(x,pointer+'/'+str(i))
 elif isinstance(v,str):
  found=[term for term in terms if term.casefold() in v.casefold()]+sorted(set(person_pattern.findall(v)))
  if found:
   first=min(v.casefold().find(x.casefold()) for x in found)
   hits.append({'field_pointer':pointer,'matched_literal_terms':found,'bounded_context':v[max(0,first-160):first+420],'field_length':len(v),'routing_only_not_semantic_relevance_or_grade':True})
 return hits
for oid,row in current.items():
 n=native(c,row['id']);hits=matches({k:n[k] for k in ['data','caveat','rationale','disposition','evidence_status']})
 if hits or oid in snapshot['objects']:
  pool[n['id']]=n;selected[oid]=n['id'];routing.append({'object_id':oid,'revision_id':n['id'],'kind':n['kind'],'subject_id':n['data'].get('subject_id'),'matches':hits,'included_in_prior_current250':oid in snapshot['objects']})
# Exact impact revisions and their full native histories, with no judgment from graph routing.
all_revision_ids={r[0] for r in c.execute('select id from revision')}
def collect_ids(v):
 if isinstance(v,dict):
  for x in v.values():yield from collect_ids(x)
 elif isinstance(v,list):
  for x in v:yield from collect_ids(x)
 elif isinstance(v,str) and v in all_revision_ids:yield v
for x in impact.values():
 for rid in collect_ids(x):
  n=native(c,rid);pool[rid]=n
  oid=n['object_id'];cur=current[oid]['id'];selected[oid]=cur;pool[cur]=native(c,cur)
# Full native history for finite routed current objects; then complete upstream evidence closure.
history=[]
for oid in sorted(selected):
 ids=[r[0] for r in c.execute('select id from revision where object_id=? order by version',(oid,))]
 for rid in ids:pool[rid]=native(c,rid)
 history.append({'object_id':oid,'current_revision_id':selected[oid],'ordered_history_revision_ids':ids})
todo=list(pool)
while todo:
 n=pool[todo.pop()]
 for e in n['evidence']:
  rid=e['basis_revision_id']
  if rid not in pool:pool[rid]=native(c,rid);todo.append(rid)
snapshot_comparison=[]
for oid,prior in snapshot['objects'].items():
 actual=pool[selected[oid]];diffs=[]
 for k in sorted(set(prior)|set(actual)):
  if prior.get(k)!=actual.get(k):diffs.append({'field':k,'prior':prior.get(k),'actual_ORDER_BY_rowid':actual.get(k)})
 assert all(x['field'] in ['evidence','origins','assets','media'] and sorted(map(lambda y:json.dumps(y,sort_keys=True),x['prior']))==sorted(map(lambda y:json.dumps(y,sort_keys=True),x['actual_ORDER_BY_rowid'])) for x in diffs),(oid,diffs)
 snapshot_comparison.append({'object_id':oid,'prior_pointer':'/objects/'+oid.replace('~','~0').replace('/','~1'),'current_revision_id':actual['id'],'all_scalar_data_and_metadata_equal':True,'explicit_native_query_order_differences':diffs,'whole_ordered_equal':not diffs})
native_pin=save('full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json',{'objects':pool,'current_object_revisions':selected,'ordered_histories':history,'array_order':'ORDER BY rowid for dependencies/origins/assets/media; data JSON strings and contained array order unchanged','capture_not_source_reading_grade':True})
routing_pin=save('finite-current-semantic-copy-field-routing-and-prior250-equality-v1.json',{'terms':terms,'metadata_person_ids':persons,'current_field_routes':routing,'prior250_comparisons':snapshot_comparison,'full_native_pin':native_pin,'citation_impact_pins':{x:pin(W/'citation-routing'/(x+'-complete-impact.json')) for x in impact},'scope_and_grade': 'Astra must adjudicate every relevant route; unrelated names and provenance can match. No inferred source membership, approval, retain or rebind.'})
prior_logs=[]
for task in ['T-0131','T-0182','T-0110','T-0766']:
 p=Path('wotan/dev-log')/(task+'.md');target=W/'prior-reuse-full-inputs'/p.name;target.parent.mkdir(exist_ok=True);target.write_bytes(p.read_bytes());prior_logs.append({'original_pin':pin(p),'captured_complete_input_pin':pin(target),'reading_credit':'Prior documented field/source scope only, Astra assigns actual reuse; historical hypotheses not renewed.'})
assert tables(live)==before and pin(MAIN)==recommendation['canonical_baseline']
assert pin('wotan/backlog.json')==backlog_before_pin and pin('wotan/dev-log/T-0781.md')==tasklog_before_pin
command_pin=save('all-readonly-CLI-view-command-results-v1.json',commands)
result=save('complete-bounded-two-current-preparation-index-v1.json',{'task':'T-0781','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'MECHANICAL_PREPARATION_ONLY_AWAIT_ROOT_LOCK_AND_SOURCE_RELEASE','exact_two':recommendation['recommended_exact_two'],'baseline_reconciliation_pin':baseline_pin,'protected_full_native_pin':protected_pin,'protected_count':len(protected_ids),'full13_person_research_inspect_views':views,'full_native_dictionary_pin':native_pin,'current_field_routing_pin':routing_pin,'prior_full_reuse_input_pins':prior_logs,'explicit_stronger_older_support_refs':recommendation['current_stronger_prior_reuse_refs'],'recommendation_pin':pin(recommendation_path),'readonly_CLI_command_results_pin':command_pin,'counts':{'routed_persons':len(persons),'selected_current_object_routes':len(selected),'complete_native_current_history_support_revisions':len(pool),'lexical_field_routed_current_objects':len(routing),'prior_current_snapshot_objects':len(snapshot['objects'])},'live_all50_unchanged':True,'live_DB_pin':pin(MAIN),'actual_state':state(live),'canonical_writes':0,'Wotan_writes':0,'operations_constructed':0,'new_original_reads':0,'C0067_mode':'Exact sufficient T0131/T0182 fullpost reuse; no routine image reopen','source_or_independent_approval':False,'actual_model_usage':None})
c.close();live.close();print(json.dumps({'preparation_index':result,'counts':load(result['path'])['counts'],'state':{'journal_head':425,'pending':0}},ensure_ascii=False,indent=2))
