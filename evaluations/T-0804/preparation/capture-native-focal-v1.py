import json,hashlib,importlib.util,sqlite3,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'evaluations/T-0804/preparation';H=R/'evaluations/T-0781/implementation/stage_exact_two_settled_package_v2.py';sp=importlib.util.spec_from_file_location('h',H);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);c=h.conn(R/'genealogy2/data/research.sqlite');people=['P-0003','P-0007','P-0004','P-0005'];focal=set(people)
for kind in ['assessment','fact','identity','identity_resolution','narrative','participation','question','relation']:
 cols=[r['name'] for r in c.execute('pragma table_info('+kind+')')];keys=[k for k in ['subject_id','person_id','person_a','person_b','from_person','to_person'] if k in cols]
 if not keys:continue
 query='select r.object_id from current_revision r join '+kind+' x on x.revision_id=r.id where '+' or '.join('x.'+k+' in (?,?,?,?)' for k in keys)
 focal.update(r[0] for r in c.execute(query,people*len(keys)))
def native(rid):
 n=h.native(c,rid)
 for key,t in [('origins','origin'),('evidence','dependency')]:n[key]=[dict(z)for z in c.execute('select * from '+t+' where revision_id=? order by rowid',(rid,))]
 return n
objects={oid:native(h.current(c,oid)) for oid in sorted(focal)};supports={}
for n in objects.values():
 for e in n['evidence']:
  rid=e['basis_revision_id'];supports[rid]=native(rid)
  oid=supports[rid]['object_id'];current=h.current(c,oid)
  if current!=rid:supports[current]=native(current)
history={oid:[native(r[0])for r in c.execute('select id from revision where object_id=? order by version',(oid,))]for oid in sorted(focal) if objects[oid]['kind']=='assessment'}
owner={r['object_id']:native(r['id'])for r in c.execute("select * from current_revision where evidence_status='OWNER_CONFIRMED' order by object_id")}
operationids={n['operation_id'] for n in [*objects.values(),*supports.values(),*[z for rows in history.values() for z in rows]]};payloads=[dict(r)for r in c.execute('select * from operation_payload order by sequence') if r['operation_id'] in operationids]
p=D/'full-native-focal-and-direct-support-v1.json';p.write_text(json.dumps({'baseline':464,'pending':0,'focalPeople':people,'focal':objects,'directSupportReferenceOnly':supports,'assessmentHistory':history,'allCurrentOwnerConfirmedReferenceOnly':owner,'relevantAcceptedRequestsReferenceOnly':payloads,'scopeNote':'Complete native rowid-order arrays. Mechanical focal structured person fields only, direct basis and current supersession; no recursive support expansion, original reading or source judgement.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'focal':len(objects),'directSupport':len(supports),'ownerConfirmed':len(owner),'acceptedRequests':len(payloads),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
