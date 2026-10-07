import json,sqlite3,pathlib,hashlib,copy,time,datetime
start=time.time();b=pathlib.Path('evaluations/T-0780');w=b/'implementation/C0685-v1';w.mkdir(exist_ok=True);p=b/'source-review/consequences-two/C-0685-source-consequence-handoff-v6.json';sha='2a537c682e635cb71af270118b3780759bbe3b2c88ba5c3ce3443166be33e579';assert hashlib.sha256(p.read_bytes()).hexdigest()==sha;d=json.load(open(p));c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
edges={i['current']['object_id']:i['edges'] for i in d['individual_dependency_decisions']};changes=[];table=[];full=[];prior=[];target={i['current']['object_id'] for i in d['objects'] if i['disposition'].startswith('revise')};over=[]
for f in (b/'implementation').rglob('*operation-v*.json'):
 z=json.load(open(f));prior.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 for ch in z.get('changes',[]):
  if ch['id'] in target:over.append({'object_id':ch['id'],'path':str(f)})
assert not over,over
for i in d['objects']:
 o=i['current'];rid=o['id'];h=dict(c.execute('select r.*,ob.kind from revision r join object ob on ob.id=r.object_id where r.id=?',(rid,)).fetchone());assert all(h[k]==o[k] for k in h);assert not c.execute('select 1 from revision where object_id=? and version>?',(h['object_id'],h['version'])).fetchone();data=dict(c.execute('select * from '+h['kind']+' where revision_id=?',(rid,)).fetchone());assert data==o['data'];orig=[dict(z) for z in c.execute('select * from origin where revision_id=?',(rid,))];assert len(orig)==len(o['origins']) and all(all(z[k]==q[k] for k in z) for z,q in zip(orig,o['origins']));ev=[dict(z) for z in c.execute('select * from dependency where revision_id=?',(rid,))];assert sorted(ev,key=lambda z:json.dumps(z,sort_keys=True))==sorted(o['evidence'],key=lambda z:json.dumps(z,sort_keys=True));ev=copy.deepcopy(o['evidence']);pro=copy.deepcopy(o)
 for e in i.get('edits',[]):
  obj=pro['data'] if e['field'].startswith('data.') else pro;k=e['field'].removeprefix('data.');assert isinstance(obj[k],str) and obj[k].count(e['old'])==e['expected_old_matches']==1,(rid,e['field']);obj[k]=obj[k].replace(e['old'],e['new'],1)
 for field,val in [('data.'+k,v) for k,v in data.items() if k!='revision_id']+[(k,h[k]) for k in ['disposition','evidence_status','rationale','caveat']]:
  newval=pro['data'][field[5:]] if field.startswith('data.') else pro[field];table.append({'object_id':h['object_id'],'revision':rid,'field':field,'old':val,'new':newval,'disposition':i['disposition'],'rationale':i['rationale'],'source_sha256':sha})
 if not i['disposition'].startswith('revise'):continue
 # Preview is not a new revision; independently reconstructed exact field edits must equal it before authorized edge changes.
 preview=i['prospective_full'];assert pro['data']==preview['data'] and all(pro[k]==preview[k] for k in ['caveat','rationale','disposition','evidence_status'])
 for e in edges.get(h['object_id'],[]):
  oldedge=e['old_edge'];matches=[j for j,z in enumerate(ev) if z==oldedge];assert len(matches)==1,(rid,e)
  if e['decision'].startswith('rebind'):ev[matches[0]]['basis_revision_id']=e['new_basis_revision_id']
  else:assert e['decision'].startswith('retain')
 if i.get('evidence_addition'):a=i['evidence_addition'];ev.append({'revision_id':rid,**a})
 ch={'id':h['object_id'],'kind':h['kind'],'expectedVersion':h['version'],'data':{k:v for k,v in pro['data'].items() if k!='revision_id'},'origins':[{'unit':z['unit_id'],'coverage':z['coverage'],'note':z['note']} for z in orig],'evidence':[{'basis':z['basis_revision_id'],'role':z['role'],'note':z['note']} for z in ev],'disposition':h['disposition'],'evidenceStatus':h['evidence_status'],'rationale':pro['rationale'],'caveat':pro['caveat']}
 for k,v in ch['data'].items():
  if k.endswith('_json') and isinstance(v,str):ch['data'][k]=json.loads(v)
 if h['kind']=='record':
  ch['assets']=[{'path':z['asset_path'],'region':z['region']} for z in c.execute('select * from record_asset where revision_id=?',(rid,))];ch['media']=[{'id':z['asset_id'],'region':z['region']} for z in c.execute('select * from record_media where revision_id=?',(rid,))]
 changes.append(ch);full.append({'current':o,'field_corrected':pro,'exact_authorized_evidence':ev,'incoming_edges':[dict(z) for z in c.execute('select * from dependency where basis_revision_id=?',(rid,))]})
assert len(changes)==76
new=[]
for n in d['new_native_specifications']:
 assert not c.execute('select 1 from object where id=?',(n['object_id'],)).fetchone()
 if n['kind']=='transcription':data={'record_id':n['record_id'],'text':n['text'],'reading_note':n['reading_note']};ev=[{'basis':n['basis_revision_id'],'role':'derived_from','note':'Explicit retained original image record@1; source-approved acyclic sequence.'}]
 else:data={k:n[k] for k in ['subject_id','criteria','outcome','body']};ev=[{'basis':z['basis_revision_id'],'role':z['role'],'note':z['note']} for z in n['evidence']]
 new.append({'id':n['object_id'],'kind':n['kind'],'expectedVersion':None,'data':data,'origins':[],'evidence':ev,'disposition':'recorded','evidenceStatus':None,'rationale':'T-0780: explicit settled C0685 source-bound consequence decision; no new independent historical evidence.','caveat':n.get('reading_note',n.get('body'))})
assert len(new)==8
# Explicit approved semantic ordering, never filename sorting: old image TR, audit, source metadata, source records, row mentions/observations, dependent conclusions, adoptions.
source=[ch for ch in changes if ch['kind']=='source'];records=[ch for ch in changes if ch['kind']=='record'];mentions=[ch for ch in changes if ch['kind']=='mention'];observations=[ch for ch in changes if ch['kind']=='observation'];rest=[ch for ch in changes if ch['kind'] not in ['source','record','mention','observation']]
groups=[('original-transcription',[new[0]]),('source-audit',[new[1]]),('source-metadata',source),('records',records),('mentions',mentions),('observations',observations),('consequences',rest),('bounded-adoptions',new[2:])];pins=[];available={r['id'] for r in c.execute('select id from revision')}
for name,chs in groups:
 if not chs:continue
 produced={ch['id']+'@'+str((ch['expectedVersion'] or 0)+1) for ch in chs}
 for ch in chs:
  for e in ch['evidence']:assert e['basis'] in available|produced,(name,ch['id'],e)
  # Reject within-operation stale bases explicitly.
  for e in ch['evidence']:
   bid,ver=e['basis'].rsplit('@',1)
   assert not any(t['id']==bid and int(ver)!=(t['expectedVersion'] or 0)+1 for t in chs),(name,ch['id'],e)
 op={'id':'T-0780/C0685-'+name+'-v1','actor':'Codex Sol mechanical implementation of settled Astra handoff v6','reason':'T-0780 C0685 bounded '+name+'; source approval '+sha+'; independent approval and total package gate pending.','dependencyReviewVersion':2,'changes':chs};f=w/(name+'-operation-v1.json');assert not f.exists();f.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');pins.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'changes':len(chs)});available|=produced
for name,obj in [('individual-field-table-v1.json',{'entries':table,'full_objects':177,'explicit_primary_overlap_reuse':d['overlap_exact_referrals'],'routing_only_not_certified':d['expanded_routing_dispositions']}),('complete-native-and-individual-dependency-binding-v1.json',{'revised_full_payloads':full,'individual_edges':d['individual_dependency_decisions'],'annotation_dependencies':d['additional_C0562_annotation_dependency_decisions'],'actual_fanout_dispositions':d['actual_individual_dependency_scope_dispositions'],'registry_record_retain':d['additional_source_registry_record_retain'],'no_blanket_resolution':True})]:
 f=w/name;f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');pins.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
r={'task':'T-0780','source_sha256':sha,'sequence':pins,'existing_revisions':76,'new_objects':8,'source_fields':84,'full_object_checks':177,'retains_and_primaryreuse':101,'prior_overlaps':over,'prior_pins':prior,'baseline_journal':281,'failed_attempts':0,'elapsed_seconds':time.time()-start,'stage_or_canonical_applies':0,'resolution_status':'Individual source-bound dispositions bound; exact stage request IDs pending authorized stage. No blanket resolves.'};(w/'canonical-ready-sequence-and-receipt-v1.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'sequence':pins[:8],'fields':len(table),'seconds':time.time()-start}))
