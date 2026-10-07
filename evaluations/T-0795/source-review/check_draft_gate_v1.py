import json,pathlib,hashlib,sqlite3,datetime
r=pathlib.Path('evaluations/T-0795');d=r/'preparation/literal-package-v1';s=r/'source-review'
def read(p):return json.loads(p.read_text())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
op=read(d/'operation-DRAFT-no-media.json');spec=read(s/'native-six-spec-v2.json');plan=read(s/'primary-literal-field-plan-v2.json');table=read(d/'individual-consequence-table.json');db=sqlite3.connect('file:evaluations/T-0795/preparation/baseline-j457.sqlite?mode=ro',uri=True);db.row_factory=sqlite3.Row
new=op['changes'][:24];assert new==spec['changes'];checks=[]
for a in op['changes'][24:]:
 rid=a['id']+'@'+str(a['expectedVersion']);n=dict(db.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.id=?',(rid,)).fetchone());data=dict(db.execute('select * from '+n['kind']+' where revision_id=?',(rid,)).fetchone());data.pop('revision_id');data={k:json.loads(v) if k.endswith('_json') and isinstance(v,str) else v for k,v in data.items()};cav=n['caveat']
 for row in plan['rows']:
  if row['revision']!=rid or row['disposition']!='revise':continue
  if row['field'].startswith('data.'):data[row['field'][5:]]=row['new']
  elif row['field']=='caveat':cav=row['new']
 origins=[{'unit':x['unit_id'],'coverage':x['coverage'],'note':x['note']} for x in db.execute('select * from origin where revision_id=? order by rowid',(rid,))]
 ev=[{'object':x['basis_revision_id'].rsplit('@',1)[0],'version':int(x['basis_revision_id'].rsplit('@',1)[1]),'role':x['role'],'note':x['note']} for x in db.execute('select * from dependency where revision_id=? order by rowid',(rid,))]
 chk={'id':a['id'],'data':data==a['data'],'caveat':cav==a['caveat'],'origins_full_order':origins==a['origins'],'evidence_full_prefix':ev==a['evidence'][:len(ev)],'metadata':a['disposition']==n['disposition'] and a['evidenceStatus']==n['evidence_status'] and a['rationale']==n['rationale']};assert all(v for k,v in chk.items() if k!='id'),chk;checks.append(chk)
assert read(d/'six-media-stage-plan.json')==spec['media_to_stage']
for x in spec['media_to_stage']:assert hashlib.sha256(pathlib.Path(x['path']).read_bytes()).hexdigest()==x['sha256']
x={'task':'T-0795','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'gate':'PRIMARY SOURCE PASS FOR SIX MEDIA STAGE AND EXACT BASELINE-CLONE TEST ONLY','PASS':True,'new24_match_exact':True,'revision11_sql_independent_checks':checks,'media6_exact':True,'pins':[pin(d/p) for p in ['operation-DRAFT-no-media.json','six-media-stage-plan.json','individual-consequence-table.json']],'source_assessment':'All six source meanings and literal48dispositions preserved. OldC0906 remains dated unchanged. Historical T0790life retained; no personalfact or gradechange. U4/U6 unopenedleads explicit.','helper_provenance_condition':'Existing draft checked directly against SQL without using h.native. materialize_literal_v1.py references helper with conditional-precedence issue for non-record origins/evidence. Actual executable wrapper/runtime patch explanation and reproducible lossless helper required before further stage; this does not invalidate independently checked exact draft bytes.','remaining':'No canonical approval. After helper provenance repair, actual media bindings, sequential staged dependency requests, per-request source dispositions, protected state checks and final exact hashes require final source gate.'};p=s/'primary-literal-draft-stage-gate-v1.json';p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(pin(p))
