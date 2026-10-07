import json,sqlite3,hashlib,time,datetime
from pathlib import Path
b=Path('evaluations/T-0780');work=b/'implementation';start=time.time();dp=b/'source-review/C-0043-C-0044-semantic-amendment-v1.json';expected='021ca5e85eac9453ef77d2ef456151cd93d84428d7fc360fc848f1fab5c6664f';assert hashlib.sha256(dp.read_bytes()).hexdigest()==expected;d=json.load(open(dp));c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row;assert c.execute('select max(sequence) from operation_payload').fetchone()[0]==281;target={x['current']['object_id'] for x in d['objects']};previous=[];overlap=[]
for p in sorted(work.glob('*operation-v*.json')):
 x=json.load(open(p));previous.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 for ch in x.get('changes',[]):
  if ch['id'] in target:overlap.append({'object_id':ch['id'],'path':str(p),'expectedVersion':ch['expectedVersion']})
assert not overlap,'Unexpected candidate overlap: return to Astra before merge'
cur={r['object_id']:dict(r) for r in c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version)')};changes=[];entries=[];fan=[]
for item in d['objects']:
 old=item['current'];oid=old['object_id'];rid=old['id'];head=cur[oid];assert all(head[k]==old[k] for k in head);data=dict(c.execute('select * from '+head['kind']+' where revision_id=?',(rid,)).fetchone());assert data==old['data'];orig=[dict(x) for x in c.execute('select * from origin where revision_id=?',(rid,))];evidence=[dict(x) for x in c.execute('select * from dependency where revision_id=?',(rid,))];assert orig==old['origins'];assert evidence==old['evidence']==[];assert head['version']==1
 ch={'id':oid,'kind':head['kind'],'expectedVersion':1,'data':{k:v for k,v in data.items() if k!='revision_id'},'origins':[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in orig],'evidence':[],'disposition':head['disposition'],'evidenceStatus':head['evidence_status'],'rationale':head['rationale'],'caveat':head['caveat']};edits={x['field']:x for x in item['edits']};assert len(edits)==1
 for field,val in [('data.'+k,v) for k,v in data.items() if k!='revision_id']+[(k,head[k]) for k in ['caveat','rationale','disposition','evidence_status']]:
  e=edits.get(field)
  if e:assert e['old']==val
  entries.append({'object_id':oid,'revision_id':rid,'field':field,'old_wording':val,'new_wording':e['new'] if e else val,'disposition':'revise_exact_field' if e else 'retain_exact_field','Astra_rationale':e['reason'] if e else item['rationale'],'registered_evidence':evidence,'source_approval_sha256':expected,'source_basis':d['source_basis'],'no_new_evidence_attachment_authorized':True})
 for e in item['edits']:
  assert e['field'].startswith('data.');field=e['field'].removeprefix('data.');assert ch['data'][field]==e['old'];ch['data'][field]=e['new']
 for field,val in ch['data'].items():
  if field.endswith('_json') and isinstance(val,str):ch['data'][field]=json.loads(val)
 changes.append(ch)
 # Preserve all incoming exact edges. Transitive fanout exists only if a direct edge exists.
 incoming=[dict(z) for z in c.execute('select d.*,r.object_id,r.version,r.disposition,r.evidence_status,r.caveat,r.rationale,o.kind from dependency d join revision r on r.id=d.revision_id join object o on o.id=r.object_id where d.basis_revision_id=?',(rid,))]
 for z in incoming:
  z['dependent_is_current']=cur[z['object_id']]['id']==z['revision_id'];z['Astra_disposition']=None;z['Astra_rationale']=None
 fan.append({'source_revision':rid,'incoming_exact_edges':incoming,'dispositions_required_if_any':True})
assert len(changes)==3
op={'id':'T-0780/C0043-C0044-semantic-addendum-v1','actor':'Codex Sol mechanical implementation of exact Astra semantic addendum','reason':'T-0780 AC3: three exact additional current data-field qualifications, stronger C0049/C0891 support retained; initial source/semantic candidates preserved; independent hash-bound review pending.','dependencyReviewVersion':2,'changes':changes};p=work/'C-0043-C-0044-semantic-addendum-operation-v1.json';assert not p.exists();p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');tp=work/'C-0043-C-0044-semantic-addendum-consequence-table-v1.json';tp.write_text(json.dumps({'objects':3,'data_field_changes':3,'new_objects':0,'entries':entries,'scope':d['scope'],'status':d['status']},ensure_ascii=False,indent=2)+'\n');fp=work/'C-0043-C-0044-semantic-addendum-dependency-input-v1.json';fp.write_text(json.dumps({'journal':281,'objects':fan,'incoming_edge_count':sum(len(x['incoming_exact_edges']) for x in fan),'no_automatic_rebind_or_resolve':True},ensure_ascii=False,indent=2)+'\n')
for pin in previous:assert hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()==pin['sha256']
rp=work/'C-0043-C-0044-semantic-addendum-receipt-v1.json';rp.write_text(json.dumps({'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'builder_elapsed_seconds':time.time()-start,'canonical_and_stage_applies':0,'original_reads':0,'exactoldfield_currentmetadata_evidence_origins_checks':'PASS','candidate_overlap_count':0,'individual_fields':len(entries),'data_field_changes':3,'new_objects':0,'incoming_dependencies':sum(len(x['incoming_exact_edges']) for x in fan),'previous_candidate_pins_unchanged':previous,'pins':[{'path':str(z),'sha256':hashlib.sha256(z.read_bytes()).hexdigest()} for z in [dp,p,tp,fp]],'scope_remaining':'Expanded semantic completeness and independent exactpackage approval pending','failed_attempts':0},ensure_ascii=False,indent=2)+'\n');print({'operation_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fields':len(entries),'incoming_edges':sum(len(x['incoming_exact_edges']) for x in fan)})
