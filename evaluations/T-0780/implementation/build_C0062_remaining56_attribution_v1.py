import json,sqlite3,hashlib,time,datetime
from pathlib import Path
b=Path('evaluations/T-0780');w=b/'implementation';start=time.time();p=b/'source-review/C-0062-remaining56-source-attribution-decisions-v1.json';sha='241e535e9d913ba282abe3d75cc2a4c2174aef6e981e1911a0af71655a334577';assert hashlib.sha256(p.read_bytes()).hexdigest()==sha;d=json.load(open(p));c=sqlite3.connect('file:'+str(b/'preparation/baseline-j281.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
cur={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')};targets={i['current']['object_id'] for i in d['objects'] if i['edits']};prior=[];over=[]
for f in sorted(w.glob('*operation-v*.json')):
 a=json.load(open(f));prior.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 for ch in a.get('changes',[]):
  if ch['id'] in targets:over.append({'id':ch['id'],'path':str(f)})
assert not over,over
changes=[];entries=[];fan=[]
for i in d['objects']:
 old=i['current'];h=cur[old['object_id']];rid=h['id'];assert all(h[k]==old[k] for k in h);data=dict(c.execute('select * from '+h['kind']+' where revision_id=?',(rid,)).fetchone());assert data==old['data'];orig=[dict(z) for z in c.execute('select * from origin where revision_id=?',(rid,))];assert all(all(z[k]==o[k] for k in z) for z,o in zip(orig,old['origins'])) and len(orig)==len(old['origins']);ev=[dict(z) for z in c.execute('select * from dependency where revision_id=?',(rid,))];assert sorted(ev,key=lambda z:json.dumps(z,sort_keys=True))==sorted(old['evidence'],key=lambda z:json.dumps(z,sort_keys=True));ev=old['evidence'];ed={e['field']:e for e in i['edits']}
 ch={'id':h['object_id'],'kind':h['kind'],'expectedVersion':h['version'],'data':{k:v for k,v in data.items() if k!='revision_id'},'origins':[{'unit':z['unit_id'],'coverage':z['coverage'],'note':z['note']} for z in orig],'evidence':[{'basis':z['basis_revision_id'],'role':z['role'],'note':z['note']} for z in ev],'disposition':h['disposition'],'evidenceStatus':h['evidence_status'],'rationale':h['rationale'],'caveat':h['caveat']}
 for field,val in [('data.'+k,v) for k,v in data.items() if k!='revision_id']+[(k,h[k]) for k in ['disposition','evidence_status','rationale','caveat']]:
  e=ed.get(field)
  if e:
   assert e['old']==val
   if field.startswith('data.'):ch['data'][field[5:]]=e['new']
   else:ch[{'evidence_status':'evidenceStatus'}.get(field,field)]=e['new']
  entries.append({'object_id':h['object_id'],'revision':rid,'field':field,'old':val,'new':e['new'] if e else val,'disposition':'revise_exact_field' if e else 'retain_exact_field','rationale':i['rationale'],'registered_evidence':ev,'source_decision_sha256':sha})
 if not ed:continue
 assert len(ed)==1
 if 'evidence' in ed:
  e=ed['evidence'];assert e['old']==ev;ch['evidence']=[{'basis':z['basis_revision_id'],'role':z['role'],'note':z['note']} for z in e['new']];entries.append({'object_id':h['object_id'],'revision':rid,'field':'evidence','old':ev,'new':e['new'],'disposition':'revise_exact_field','source_decision_sha256':sha})
 e=i['evidence_addition'];assert e['basis_revision_id']=='AUDIT-T0110-C-0062@1';assert c.execute('select 1 from revision where id=?',(e['basis_revision_id'],)).fetchone();ch['evidence'].append({'basis':e['basis_revision_id'],'role':e['role'],'note':e['note']})
 for k,v in ch['data'].items():
  if k.endswith('_json') and isinstance(v,str):ch['data'][k]=json.loads(v)
 changes.append(ch);incoming=[dict(z) for z in c.execute('select d.*,r.object_id,r.version,o.kind from dependency d join revision r on r.id=d.revision_id join object o on o.id=r.object_id where basis_revision_id=?',(rid,))]
 for z in incoming:z['dependent_is_current']=cur[z['object_id']]['id']==z['revision_id'];z['Astra_disposition']=None
 fan.append({'source_revision':rid,'incoming_edges':incoming})
assert len(d['objects'])==56 and len(changes)==7
op={'id':'T-0780/C0062-remaining56-attribution-v1','actor':'Codex Sol mechanical implementation of settled Astra decisions','reason':'Seven exact C0062 source-attribution qualifications; accepted identity and administrative split preserved. Prior full audit reused. Adoption and broader consequences pending.','dependencyReviewVersion':2,'changes':changes}
files=[]
for name,obj in [('C-0062-remaining56-attribution-operation-v1.json',op),('C-0062-remaining56-attribution-consequence-table-v1.json',{'entries':entries,'individual_objects':56,'revisions':7,'retains':49}),('C-0062-remaining56-attribution-dependency-input-v1.json',{'objects':fan,'no_automatic_rebind':True})]:
 f=w/name;assert not f.exists();f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');files.append(f)
for x in prior:assert hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256']
r={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'builder_elapsed_seconds':time.time()-start,'exact_fullcurrent_metadata_data_origins_evidence_oldmatches':'PASS','revision_count':7,'retains':49,'new_objects':0,'field_count':len(entries),'prior_overlap':over,'incoming_edges':sum(len(x['incoming_edges']) for x in fan),'source_decision_sha256':sha,'stage_or_canonical_applies':0,'failed_attempts':0,'pending':'Astra adoption target and broader semantic/independent review','prior_pins':prior,'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]};(w/'C-0062-remaining56-attribution-receipt-v1.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['revision_count','field_count','incoming_edges','pins']}))
