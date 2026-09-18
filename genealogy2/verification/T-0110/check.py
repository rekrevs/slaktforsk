"""Read-only regression check for the locked T-0110 source audit."""
import hashlib,json,sqlite3,sys
from pathlib import Path
base=Path(__file__).resolve().parent
repo=base.parents[2]
db=Path(sys.argv[1] if len(sys.argv)>1 else repo/'genealogy2/data/research.sqlite').resolve()
c=sqlite3.connect(f'file:{db}?mode=ro',uri=True);c.row_factory=sqlite3.Row
sample=json.loads((base/'sample.json').read_text());frame=json.loads((base/'frame.json').read_text())
assert hashlib.sha256((base/'frame.json').read_bytes()).hexdigest()==sample['frame_sha256']
assert (base/'seed.txt').read_text().strip()==sample['seed']
ids=[r['citation'] for r in frame['rows']]
assert len(ids)==456,(len(ids),list(frame)[:5])
assert sorted(ids,key=lambda cid:hashlib.sha256((sample['seed']+cid).encode()).hexdigest())[:30]==sample['citations']
def read(oid):
 r=c.execute('select * from current_revision where object_id=?',(oid,)).fetchone();assert r,oid
 d=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone());d.pop('revision_id');return dict(r),d
def date(oid):return json.loads(read(oid)[1]['date_json'])
counts={}
for cid in sample['citations']:
 r,d=read('AUDIT-T0110-'+cid);body=json.loads(d['body']);out=d['outcome'];assert body['outcome']==out
 counts[out]=counts.get(out,0)+1
 for a in body['verified_media']+([body['additional_original']] if 'additional_original' in body else []):
  assert hashlib.sha256((repo/a['path']).read_bytes()).hexdigest()==a['sha256'],a['path']
assert counts=={'corrected':7,'confirmed':18,'not_fully_testable':2,'ineligible':3},counts
assert date('E-birth-P-0111')['value']=='1849-08-03'
assert json.loads(read('O-P-0477-C0721-Walla')[1]['value_json'])['birth_literal']=='1785 31/10 Malm'
assert json.loads(read('O-P-0272-C0457-own')[1]['value_json'])['birth_raw']=='1844-12-04'
assert json.loads(read('O-P-0258-C0925-own')[1]['value_json'])['birth']=='1922-01-19'
assert date('E-birth-P-0406')['value']=='1858-03-08'
assert date('E-birth-P-0403')['precision']=='unknown'
assert date('E-birth-P-0321')['precision']=='year'
assert date('E-registered_departure-P-0317-Lerbo1861')['value']=='1861-10-10'
assert date('E-birth-P-0258')['values']==['1922-01-17','1922-01-19']
assert date('E-birth-M-C0925-Ture-Attilio')['value']=='1912-09-17'
assert date('E-birth-P-0048')['value']=='1869-07-24'
assert date('E-baptism-P-0048')['value']=='1869-07-25'
r,d=read('ID-P-0477-Helena1785-candidate');assert r['disposition']=='candidate' and r['evidence_status']=='LEAD'
assert not c.execute("select 1 from current_revision r join participation p on p.revision_id=r.id where p.person_id in ('P-0054','P-0055','P-0056') and p.event_id='E-baptism-P-0048' and r.disposition='accepted'").fetchone()
protected=[]
for r in c.execute("select * from current_revision where evidence_status='OWNER_CONFIRMED' order by object_id"):
 d=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone());d.pop('revision_id');protected.append([r['object_id'],r['kind'],r['disposition'],d])
baseline=json.loads((base/'baseline-checks.json').read_text())
assert len(protected)==baseline['owner_object_count']
assert hashlib.sha256(json.dumps(protected,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==baseline['owner_payload_sha256']
assert c.execute("select count(*) from current_revision where kind='person'").fetchone()[0]==baseline['native_person_count']
assert c.execute('select count(*) from pending_review').fetchone()[0]==0
print(json.dumps(dict(ok=True,draw=30,outcomes=counts,owner_objects_unchanged=len(protected),persons=536,pending_reviews=0),ensure_ascii=False))
