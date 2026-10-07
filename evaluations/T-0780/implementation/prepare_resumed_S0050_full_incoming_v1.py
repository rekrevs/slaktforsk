import json,hashlib,sqlite3,datetime
from pathlib import Path
B=Path('evaluations/T-0780');W=B/'implementation/resumed-S0050-rejected-identity-full-incoming-v1'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
S=B/'source-review/resumed-S0050-rejected-identity-copy-decision-v1.json';assert sha(S)=='0eea957532c9fe51d3452ac67ed8bee6c1f0718d2c5a77a821f1390b57694f45';d=load(S);assert len(d['objects'])==1;cur=d['objects'][0]['current'];assert cur['object_id']=='S-0050'
P=B/'implementation/resumed-C0561-ten-bounded-context-queue-v1/concrete-current133-partial-sequence-and-constraint-proposal-v1.json';assert sha(P)=='d6e39bf88e2a3ed8d07ab1dcfb8ba986afc8622386a5e6c2fe3435f74535c44d';seq=load(P)['sequence'];candidates={x['id']:{'payload':x,'membership_pointer':p} for p in seq for x in load(p['path'])['changes']};assert 'S-0050' not in candidates
c=sqlite3.connect('file:'+str((B/'preparation/baseline-j281.sqlite').resolve())+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
def native(rid):
 row=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone();assert row;n=dict(row);n['data']=dict(c.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone());n['origins']=[dict(z) for z in c.execute('select * from origin where revision_id=?',(rid,))];n['evidence']=[dict(z) for z in c.execute('select * from dependency where revision_id=?',(rid,))]
 if n['kind']=='record':
  n['assets']=[dict(z) for z in c.execute('select * from record_asset where revision_id=?',(rid,))];n['media']=[dict(z) for z in c.execute('select * from record_media where revision_id=?',(rid,))]
 return n
assert native(cur['id'])==cur;assert not c.execute('select 1 from revision where object_id=? and version>?',('S-0050',cur['version'])).fetchone()
fan=[];full={}
for row in c.execute('select d.*,r.object_id,r.version,not exists(select 1 from revision n where n.object_id=r.object_id and n.version>r.version) is_current from dependency d join revision r on r.id=d.revision_id where d.basis_revision_id in(select id from revision where object_id=?)',('S-0050',)):
 e=dict(row);fan.append({'edge':e,'current_candidate_consumer':candidates.get(e['object_id']),'Astra_individual_disposition':None});full[e['revision_id']]=native(e['revision_id'])
strong={}
for oid in ['BIO-P-0424','RESEARCH-P-0424-9d76f0343410','IMPORT-P-0424']:
 row=c.execute('select id from revision where object_id=? order by version desc limit 1',(oid,)).fetchone()
 if row:strong[row['id']]=native(row['id'])
assert not W.exists();W.mkdir();p=W/'complete-S0050-current-history-incoming-and-current-candidates-v1.json';p.write_text(json.dumps({'task':'T-0780','saved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pin':{'path':str(S),'sha256':sha(S)},'current_proposal_pin':{'path':str(P),'sha256':sha(P)},'whole_current_source':cur,'all_history_incoming':fan,'whole_incoming_native':full,'exact_named_current_stronger_identity_inputs':strong,'current_incoming_count':sum(x['edge']['is_current'] for x in fan),'all_history_incoming_count':len(fan),'distinct_incoming_versions':len(full),'no_candidate_overlap':True,'build_stage_canonical':'UNRUN','individual_Astra_grading_required_before_dependent_action':True},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'path':str(p),'sha256':sha(p),'current_incoming':sum(x['edge']['is_current'] for x in fan),'history_incoming':len(fan),'versions':len(full)},indent=2))
