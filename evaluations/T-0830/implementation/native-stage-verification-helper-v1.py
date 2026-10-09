import sqlite3,json,sys,hashlib
from pathlib import Path
stage=Path(sys.argv[1]);op=Path(sys.argv[2]);out=Path(sys.argv[3]);a=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);b=sqlite3.connect('file:'+str(stage.resolve())+'?mode=ro',uri=True);a.row_factory=b.row_factory=sqlite3.Row;o=json.load(open(op));errors=[];checks=[]
refs={'record':['source_id'],'transcription':['record_id'],'mention':['record_id'],'observation':['record_id','mention_id'],'identity':['mention_id'],'participation':['event_id','mention_id']}
for m in o['changes']:
 r=dict(b.execute('select *from current_revision where object_id=?',(m['id'],)).fetchone());rid=r['id'];expect=(m['expectedVersion']or 0)+1
 for k,v in {'version':expect,'kind':m['kind'],'disposition':m['disposition'],'evidence_status':m.get('evidenceStatus'),'rationale':m['rationale'],'caveat':m.get('caveat','')}.items():
  if r[k]!=v:errors.append([m['id'],k,r[k],v])
 data=dict(b.execute('select *from '+m['kind']+' where revision_id=?',(rid,)).fetchone());data.pop('revision_id')
 for k,v in m['data'].items():
  actual=json.loads(data[k])if k.endswith('_json')and data[k]is not None else data[k]
  if actual!=v:errors.append([m['id'],'data.'+k])
 orig=[{'unit':z['unit_id'],'coverage':z['coverage'],'note':z['note']}for z in b.execute('select *from origin where revision_id=?order by rowid',(rid,))]
 if orig!=m.get('origins',[]):errors.append([m['id'],'origins order'])
 evidence=[{'object':z['basis_revision_id'].rsplit('@',1)[0],'version':int(z['basis_revision_id'].rsplit('@',1)[1]),'role':z['role'],'note':z['note']}for z in b.execute('select *from dependency where revision_id=?order by rowid',(rid,))];expected=list(m.get('evidence',[]))
 for f in refs.get(m['kind'],[]):
  t=m['data'].get(f)
  if t and not any(e['object']==t for e in expected):expected.append({'object':t,'version':b.execute('select version from current_revision where object_id=?',(t,)).fetchone()[0],'role':'derived_from','note':'Versionsbunden strukturreferens: '+f})
 if evidence!=expected:errors.append([m['id'],'evidence order',evidence,expected])
 if m['kind']=='record':
  for table,key,col in [('record_asset','assets','asset_path'),('record_media','media','asset_id')]:
   got=[{('path'if key=='assets'else'id'):z[col],'region':z['region']}for z in b.execute('select *from '+table+' where revision_id=?order by rowid',(rid,))];want=[{('path'if key=='assets'else'id'):z['path'if key=='assets'else'id'],'region':z.get('region')or'helbild'}for z in m.get(key,[])]
   if got!=want:errors.append([m['id'],key,got,want])
 checks.append({'object':m['id'],'resulting_revision':rid,'all_native_fields_metadata_origins_evidence_asset_order_exact':not any(e[0]==m['id']for e in errors)})
baseheads={z['object_id']:z['id']for z in a.execute('select object_id,id from current_revision')};changed={m['id']for m in o['changes']};unrelated=[oid for oid in baseheads if oid not in changed];unrelated_bad=[oid for oid in unrelated if b.execute('select id from current_revision where object_id=?',(oid,)).fetchone()[0]!=baseheads[oid]]
owner=[dict(z)for z in a.execute("select *from current_revision where evidence_status='OWNER_CONFIRMED'")];owner_bad=[z['object_id']for z in owner if dict(b.execute('select *from current_revision where object_id=?',(z['object_id'],)).fetchone())!=z]
b.execute("attach database 'file:genealogy2/data/research.sqlite?mode=ro' as baseline")
tables=['object','revision','origin','dependency','record_asset','record_media','operation','operation_payload','review_resolution','legacy_mapping','unit_decision','unit_decision_target']+list(refs)+['person','source','identity_resolution','place','event','relation','fact','question','search','assessment','narrative']
history=[]
for t in dict.fromkeys(tables):
 n=b.execute('select count(*)from (select *from baseline.'+t+' except select *from main.'+t+')').fetchone()[0];history.append({'table':t,'missing_or_changed_prior_rows':n})
proof={'operation_sha256':hashlib.sha256(op.read_bytes()).hexdigest(),'changed_objects':len(checks),'exact_candidate_native_checks':checks,'errors':errors,'unrelated_current_heads_unchanged':len(unrelated)-len(unrelated_bad),'unrelated_head_errors':unrelated_bad,'owner_confirmed_count':len(owner),'owner_errors':owner_bad,'all_prior_rows_preserved':history,'baseline_journal':505,'stage_journal':b.execute('select max(sequence)from operation_payload').fetchone()[0],'pending':b.execute('select count(*)from pending_review').fetchone()[0]};out.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'errors':len(errors),'unrelated_errors':len(unrelated_bad),'owner_errors':len(owner_bad),'historical_errors':sum(z['missing_or_changed_prior_rows']for z in history),'proof_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}));assert not errors and not unrelated_bad and not owner_bad and not any(z['missing_or_changed_prior_rows']for z in history)
