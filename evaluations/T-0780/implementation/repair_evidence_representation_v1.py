import pathlib,json,re,hashlib,copy,time
start=time.time();w=pathlib.Path('evaluations/T-0780/implementation');out=w/'evidence-schema-repair-v1';out.mkdir(exist_ok=True);maps=[];unchanged=[];ambiguous=[]
for f in sorted(w.rglob('*operation-v*.json')):
 if out in f.parents:continue
 old=json.load(open(f));new=copy.deepcopy(old);edits=[]
 for ch in new.get('changes',[]):
  for index,e in enumerate(ch.get('evidence',[])):
   if 'basis' not in e:continue
   if set(e)!={'basis','role','note'} or not isinstance(e['basis'],str) or not re.fullmatch(r'.+@[1-9][0-9]*',e['basis']) or not isinstance(e['role'],str) or not isinstance(e['note'],str):ambiguous.append({'path':str(f),'id':ch['id'],'index':index,'evidence':e});continue
   basis=e.pop('basis');oid,ver=basis.rsplit('@',1);e['object']=oid;e['version']=int(ver);edits.append({'object_id':ch['id'],'index':index,'basis':basis,'canonical':copy.deepcopy(e)})
 if not edits:unchanged.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()});continue
 assert not any(x['path']==str(f) for x in ambiguous),'Ambiguous representation returns Astra'
 reverse=copy.deepcopy(new)
 for item in edits:
  ch=next(x for x in reverse['changes'] if x['id']==item['object_id']);e=ch['evidence'][item['index']];oid=e.pop('object');ver=e.pop('version');e['basis']=oid+'@'+str(ver)
 assert reverse==old,'Unexpected nonsupport/ordered evidence difference'
 new['id']=old['id']+'-evidence-schema-v1';new['reason']=old['reason']+' Mechanical evidence representation amendment only; same exact source-approved basis versions, role/note/order. Original invalid draft preserved.'
 rel=f.relative_to(w);target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();target.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n');maps.append({'old_path':str(f),'old_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'fixed_path':str(target),'fixed_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'individual_edges':edits,'all_non_evidence_payload_unchanged':True,'exact_ordered_semantic_edges_unchanged':True,'operation_id_unique_amendment':new['id']})
r={'task':'T-0780','authority':'Root explicit schema-only repair instruction 2026-10-03; no basis-version decisions','mapping':maps,'already_canonical':unchanged,'ambiguous':ambiguous,'failed_initial_schema_drafts':len(maps),'evidence_edges_represented':sum(len(x['individual_edges']) for x in maps),'elapsed_seconds':time.time()-start,'stage_or_canonical_applies':0,'status':'Exact representation repairs; independent hash-bind must be renewed; no previous technical PASS inherited'};(out/'all-draft-schema-inventory-and-mapping-v1.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['failed_initial_schema_drafts','evidence_edges_represented','ambiguous','elapsed_seconds']}))
