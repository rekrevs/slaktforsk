import json,sqlite3,hashlib,datetime,time
from pathlib import Path
b=Path('evaluations/T-0780');prep=b/'preparation';out=b/'implementation'/'dependency-preparation-v1';assert not out.exists();out.mkdir();start=time.time();c=sqlite3.connect('file:'+str(prep/'baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==281
selected=['C-0043','C-0044','C-0563','C-0561','C-0685','C-0069','C-0425','C-0062','C-0106','C-0060'];cur={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')};revs={r['id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id')};incoming={};deps={}
for r in c.execute('select * from dependency'):
 r=dict(r);incoming.setdefault(r['basis_revision_id'],[]).append(r);deps.setdefault(r['revision_id'],[]).append(r)
def full(oid):
 r=cur[oid].copy();rid=r['id'];r['data']=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(rid,)).fetchone());r['evidence']=deps.get(rid,[]);r['origins']=[dict(x) for x in c.execute('select * from origin where revision_id=?',(rid,))]
 if r['kind']=='record':
  r['assets']=[dict(x) for x in c.execute('select ra.*,a.sha256,a.bytes from record_asset ra join asset a on a.path=ra.asset_path where ra.revision_id=?',(rid,))];r['media']=[dict(x) for x in c.execute('select rm.*,a.storage_path,a.sha256,a.bytes,a.original_name,a.provenance from record_media rm join native_asset a on a.id=rm.asset_id where rm.revision_id=?',(rid,))]
 return r
index=[];objects={};contextowners={};graphowners={}
for cid in selected:
 card=json.load(open(prep/(cid+'-routing-v2.json')));scope=[]
 for row in card['current_records']:
  oid=row['object_id'];source=cur[oid];assert source['id']==row['id'];seed=source['id'];todo=[seed];paths={seed:[]};allreach=set()
  while todo:
   basis=todo.pop(0)
   for e in incoming.get(basis,[]):
    target=e['revision_id']
    if target not in paths:paths[target]=paths[basis]+[e];todo.append(target)
    allreach.add(target)
  currentitems=[];historical=[]
  for target in sorted(allreach):
   r=revs[target];iscurrent=cur[r['object_id']]['id']==target;entry={'object_id':r['object_id'],'revision_id':target,'distance':len(paths[target]),'path':paths[target],'all_reached_direct_dependency_edges':[e for e in deps.get(target,[]) if e['basis_revision_id']==seed or e['basis_revision_id'] in allreach]}
   if iscurrent:
    objects[r['object_id']]=full(r['object_id']);entry.update({'current_full_native_ref':r['object_id'],'Astra_disposition':None,'Astra_rationale':None,'authorized_basis_replacements':None});currentitems.append(entry);graphowners.setdefault(r['object_id'],set()).add(cid)
   else:historical.append(entry)
  objects[oid]=full(oid);p=out/(cid+'-'+oid+'-fanout-v1.json');p.write_text(json.dumps({'task':'T-0780','metadata_only_no_rebind_adjudication':True,'source_record_revision':seed,'source_current_full_native_ref':oid,'allroles_including_context_preserved':True,'current_dependency_objects':currentitems,'historical_dependency_objects':historical,'current_count':len(currentitems),'full_native_objects_dictionary':'current-full-native-objects-v1.json'},ensure_ascii=False,indent=2)+'\n');scope.append({'source_record_revision':seed,'path':str(p),'current_count':len(currentitems),'historical_count':len(historical)})
 index.append({'scope':cid,'records':scope,'union_current_dependents':len(set(y['object_id'] for rr in scope for y in json.load(open(rr['path']))['current_dependency_objects']))})
 cp=prep/'selected'/(cid+'-source-relevant-current-context-v1.json');context=json.load(open(cp));
 for r in context['objects']:
  assert cur[r['object_id']]['id']==r['revision_id'];contextowners.setdefault(r['object_id'],set()).add(cid)
# Full payload objects exist only once, referenced by exact object/revision in per-record files.
(out/'current-full-native-objects-v1.json').write_text(json.dumps({'baseline_journal':281,'objects':objects,'scope':'Onlyselectedrecordincominggraphconsumers; full metadata/data/evidence/origins/assets once, no personview expansion.'},ensure_ascii=False,indent=2)+'\n')
overlap=[]
for oid,owners in sorted(contextowners.items()):
 if len(owners)>1:overlap.append({'object_id':oid,'baseline_revision':cur[oid]['id'],'kind':cur[oid]['kind'],'context_scopes':sorted(owners),'dependency_scopes':sorted(graphowners.get(oid,set())),'potential_revisions_only_no_change_decision':True,'Astra_sequence_disposition':None})
# Already drafted changes are factual file membership only, not source adjudication.
drafted={}
for name in ['C-0043-candidate-operation-v2.json','C-0044-context-candidate-operation-v1.json','C-0062-Forsberg-candidate-operation-v1.json']:
 p=b/'implementation'/name;x=json.load(open(p))
 for ch in x['changes']:drafted.setdefault(ch['id'],[]).append({'path':str(p),'operation_id':x['id'],'expectedVersion':ch['expectedVersion'],'is_new':ch['expectedVersion'] is None})
for x in overlap:x['already_drafted_memberships']=drafted.get(x['object_id'],[])
(out/'potential-current-context-overlap-v1.json').write_text(json.dumps({'baseline_journal':281,'basis':'Deduplicated source-relevant currentcontext perselectedscope; overlap is candidate membership, never authorization to revise or substitute expectedVersion.','overlaps':overlap,'already_drafted_existing_overlap':[{'object_id':oid,'memberships':vs} for oid,vs in drafted.items() if len(vs)>1 and any(z['expectedVersion'] is not None for z in vs)]},ensure_ascii=False,indent=2)+'\n')
(out/'dependency-index-v1.json').write_text(json.dumps({'task':'T-0780','baseline_journal':281,'scope_index':index,'single_full_native_dictionary_objects':len(objects),'overlap_objects':len(overlap),'no_dispositions_or_applies':True},ensure_ascii=False,indent=2)+'\n')
files=sorted(out.glob('*.json'));pins=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files];measurement={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.time()-start,'stage':'metadata_dependency_and_sequence_preparation_only','selected_scopes':10,'selected_records':sum(len(x['records']) for x in index),'unique_full_native_objects':len(objects),'overlap_objects':len(overlap),'source_reads':0,'stage_or_canonical_applies':0,'failures':[],'pins':pins};(out/'mechanical-production-and-freeze-v1.json').write_text(json.dumps(measurement,ensure_ascii=False,indent=2)+'\n');print({'scopes':[(x['scope'],x['union_current_dependents']) for x in index],'objects':len(objects),'overlap':len(overlap),'seconds':measurement['elapsed_seconds']})
