import json,pathlib,sqlite3,hashlib
p=pathlib.Path('evaluations/T-0809');L=lambda n:json.loads((p/n).read_text());c=sqlite3.connect('file:'+str(p/'implementation/stage473-sequence-v1/stage.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
ops=[L('implementation/operation-v2.json'),L('implementation/repair-operation-v1.json')];proof=[]
for op in ops:
 for z in op['changes']:
  rev=dict(c.execute('select * from revision where object_id=? order by version desc limit 1',(z['id'],)).fetchone());assert rev['operation_id']==op['id'];assert rev['version']==(z['expectedVersion'] or 0)+1
  d=dict(c.execute('select * from '+z['kind']+' where revision_id=?',(rev['id'],)).fetchone());d.pop('revision_id')
  for k,v in list(d.items()):
   if k.endswith('_json') and v is not None:d[k]=json.loads(v)
  assert d==z['data'],z['id']
  for k,m in [('disposition','disposition'),('evidence_status','evidenceStatus'),('rationale','rationale'),('caveat','caveat')]:assert rev[k]==z.get(m), (z['id'],k)
  origins=[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in c.execute('select * from origin where revision_id=? order by rowid',(rev['id'],))];assert origins==z['origins']
  ev=[{'object':r['basis_revision_id'].rsplit('@',1)[0],'version':int(r['basis_revision_id'].rsplit('@',1)[1]),'role':r['role'],'note':r['note']} for r in c.execute('select * from dependency where revision_id=? order by rowid',(rev['id'],))];assert ev==z['evidence'],z['id']
  if z['kind']=='record':
   media=[{'id':r['asset_id'],'region':r['region']} for r in c.execute('select * from record_media where revision_id=? order by rowid',(rev['id'],))];assert media==z['media']
  proof.append({'id':z['id'],'revision':rev['id'],'all_literal_native_fields_metadata_and_order_equal':True})
actual=[{'request':r['request_id'],'rationale':r['rationale']} for r in c.execute('select * from review_resolution where operation_id=? order by rowid',(ops[1]['id'],))];assert actual==ops[1]['resolve'];assert len(actual)==96
for m in ops[0]['media']:
 r=dict(c.execute('select * from native_asset where id=?',(m['id'],)).fetchone());assert r['sha256']==m['sha256'];assert hashlib.sha256(pathlib.Path(m['storagePath']).read_bytes()).hexdigest()==m['sha256']
x={'task':'T-0809','actual_current_api_proofs':proof,'stored96_resolution_rows_order_rationales_exact':True,'six_actual_media_hashes_exact':True,'pending':L('implementation/stage473-sequence-v1/after-2-pending-full.json'),'own_source_decision_sha256':hashlib.sha256((p/'independent-actual96-dispositions-v2.json').read_bytes()).hexdigest()};f=p/'independent-final-actual-source-check-v1.json';f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print('PASS',len(proof),len(actual),hashlib.sha256(f.read_bytes()).hexdigest())
