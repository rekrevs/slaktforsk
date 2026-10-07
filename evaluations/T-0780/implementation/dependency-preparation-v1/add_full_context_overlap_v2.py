import json,sqlite3,hashlib,time,datetime
from pathlib import Path
b=Path('evaluations/T-0780');s=b/'preparation/selected';o=b/'implementation/dependency-preparation-v1';start=time.time();idx=json.load(open(o/'dependency-index-v1.json'));c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;cur={r['object_id']:dict(r) for r in c.execute('select r.*,x.kind from revision r join object x on x.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')};members={};full=json.load(open(o/'current-full-native-objects-v1.json'))['objects'];extra={}
for unit in idx['scope_index']:
 cid=unit['scope']
 for layer,suffix in [('source_relevant','source-relevant-current-context-v1.json'),('semantic_expanded','deduplicated-current-context-v1.json')]:
  p=s/(cid+'-'+suffix);x=json.load(open(p))
  for r in x['objects']:
   oid=r['object_id'];assert cur[oid]['id']==r['revision_id'];entry=members.setdefault(oid,{'object_id':oid,'baseline_revision':r['revision_id'],'kind':r['kind'],'source_relevant_scopes':set(),'semantic_expanded_scopes':set(),'primary_settled_context_scopes':set()});entry[layer+'_scopes'].add(cid)
# Include the full already-settled primary contexts, preserving their exact fieldscope and versions.
for name,key,cid in [('C-0043-primary-decisions-v1.json','items','C-0043'),('C-0044-primary-decisions-v1.json','objects','C-0044'),('C-0062-primary-Forsberg-decisions-v1.json','objects','C-0062')]:
 p=b/'source-review'/name;x=json.load(open(p))
 for row in x[key]:
  r=row.get('current',row);oid=r['object_id'];entry=members.setdefault(oid,{'object_id':oid,'baseline_revision':cur[oid]['id'],'kind':cur[oid]['kind'],'source_relevant_scopes':set(),'semantic_expanded_scopes':set(),'primary_settled_context_scopes':set()});entry['primary_settled_context_scopes'].add(cid)
for oid,r in members.items():
 for k in ['source_relevant_scopes','semantic_expanded_scopes','primary_settled_context_scopes']:r[k]=sorted(r[k])
 r['all_candidate_scopes']=sorted(set(r['source_relevant_scopes'])|set(r['semantic_expanded_scopes'])|set(r['primary_settled_context_scopes']));r['Astra_sequence_disposition']=None;r['warning']='Mechanical scoped candidate membership; no change/rebind/expectedVersion substitution authorized.'
 if oid not in full:
  native=cur[oid].copy();rid=native['id'];native['data']=dict(c.execute('select * from '+native['kind']+' where revision_id=?',(rid,)).fetchone());native['origins']=[dict(z) for z in c.execute('select * from origin where revision_id=?',(rid,))];native['evidence']=[dict(z) for z in c.execute('select * from dependency where revision_id=?',(rid,))]
  if native['kind']=='record':native['assets']=[dict(z) for z in c.execute('select * from record_asset where revision_id=?',(rid,))];native['media']=[dict(z) for z in c.execute('select * from record_media where revision_id=?',(rid,))]
  extra[oid]=native
for r in members.values():r['full_native_dictionary']='current-full-native-objects-v1.json' if r['object_id'] in full else 'additional-context-full-native-objects-v2.json'
p=o/'all-selected-current-context-overlap-v2.json';p.write_text(json.dumps({'baseline_journal':281,'layers':'All source-relevant and expanded semantic currentcontext files plus alreadysettled exactprimarycontexts; membership only.','candidate_union_objects':len(members),'overlap_objects':[r for oid,r in sorted(members.items()) if len(r['all_candidate_scopes'])>1],'single_scope_object_index':[r for oid,r in sorted(members.items()) if len(r['all_candidate_scopes'])==1]},ensure_ascii=False,indent=2)+'\n');q=o/'additional-context-full-native-objects-v2.json';q.write_text(json.dumps({'baseline_journal':281,'dictionary_excludes_alreadypreserved460graphobjects':True,'objects':extra},ensure_ascii=False,indent=2)+'\n');f=o/'context-overlap-additive-freeze-v2.json';f.write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.time()-start,'union_objects':len(members),'full_native_total':len(full)+len(extra),'overlap_objects':sum(len(r['all_candidate_scopes'])>1 for r in members.values()),'metadata_only_no_apply':True,'pins':[{'path':str(z),'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'bytes':z.stat().st_size} for z in [p,q]]},ensure_ascii=False,indent=2)+'\n');print({'allcontextunion':len(members),'additionalpayloads':len(extra),'overlap':sum(len(r['all_candidate_scopes'])>1 for r in members.values()),'seconds':time.time()-start})
