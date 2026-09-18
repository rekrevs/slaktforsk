"""Read-only coverage and consolidation checks, no full database rebuild."""
import hashlib,json,sqlite3,sys
from pathlib import Path
base=Path(__file__).resolve().parent;repo=base.parents[2]
c=sqlite3.connect(f'file:{Path(sys.argv[1] if len(sys.argv)>1 else repo/"genealogy2/data/research.sqlite").resolve()}?mode=ro',uri=True);c.row_factory=sqlite3.Row
packages=sorted((repo/'genealogy2/migration').glob('persons-??-?.json'));reviews={};ndocs=0;nassertions=0;nrelations=0
for file in packages:
 for row in json.loads(file.read_text()):
  pid=row['person'];assert pid not in reviews,pid
  assert row['readingNote'].strip() and row['documents'],pid
  for doc in row['documents']:
   assert hashlib.sha256((repo/doc['path']).read_bytes()).hexdigest()==doc['sha256'],doc['path'];ndocs+=1
  reviews[pid]=row;nassertions+=len(row['assertions']);nrelations+=len(row['relations'])
people={r[0] for r in c.execute("select object_id from current_revision where kind='person'")}
assert len(reviews)==538 and len(people)==536 and people<=reviews.keys()
assert set(reviews)-people=={'P-0295','P-0412'}
for p in people:
 assert c.execute("select 1 from current_revision r join assessment a on a.revision_id=r.id where a.subject_id=?",(p,)).fetchone(),p
def read(oid):
 r=c.execute('select * from current_revision where object_id=?',(oid,)).fetchone();assert r,oid
 d=dict(c.execute('select * from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone());return dict(r),d
for p in ['0004','0005','0006','0041','0210','0269','0270']:
 r,d=read('ASSESSMENT-P-'+p)
 assert 'Kontraktsgranskning: `UNDERKÄND`' in d['body'],p
for p in ['0005','0006','0041','0269','0270']:
 r,d=read('CONTRACT-P-'+p+'-PK-08');assert d['outcome']=='EJ STYRKT',p
assert 'flera kyrkogårdsförvaltningar' in read('S-0711')[1]['title']
for p,name in [('0187','Anders Ersson'),('0189','Per Eric Ersson'),('0190','Stina Cajsa Ersdotter'),('0518','Gustava Maria Rybergsdotter')]:
 assert read('P-'+p)[1]['display_name'].startswith(name),(p,read('P-'+p)[1])
# Known C1055 conflict may not silently regain support for eight sibling links.
for n in range(520,528):
 oid=f'REL-sibling-P-0065-P-{n:04d}';r,d=read(oid)
 bases={x[0].rsplit('@',1)[0] for x in c.execute('select basis_revision_id from dependency where revision_id=?',(r['id'],))}
 assert bases=={'R-ee9afd95459534c05d5e3e8d','R-efca6e283ff6a0bd4048e02e'},(oid,bases)
# Repaired links must cite the actual parents/child, not the unrelated C0467 record.
for parent in ['P-0517','P-0518']:
 r,d=read(f'REL-parent-{parent}-P-0389')
 assert d['from_person']==parent and d['to_person']=='P-0389' and d['relation_type']=='parent'
 bases={x[0] for x in c.execute('select basis_revision_id from dependency where revision_id=?',(r['id'],))}
 assert f'O-{parent}-C0851-parent@1' in bases and 'O-P-0389-C0851-child@1' in bases
r,d=read('REL-spouse-P-0517-P-0518')
assert d['relation_type']=='spouse'
bases={x[0] for x in c.execute('select basis_revision_id from dependency where revision_id=?',(r['id'],))}
assert {'O-P-0517-C0851-parent@1','O-P-0518-C0851-parent@1'}<=bases
assert json.loads(d['date_json'])['precision']=='unknown'
r,d=read('PATH-P-0275-KP-05')
assert '1911-01-16' in d['body']
bases={x[0] for x in c.execute('select basis_revision_id from dependency where revision_id=?',(r['id'],))}
assert {'E-death-P-0276@1','O-P-0276-C0460-own@1'}<=bases
assert c.execute('select count(*) from pending_review').fetchone()[0]==0
print(json.dumps(dict(ok=True,packages=len(packages),individual_reviews=len(reviews),current_persons=len(people),document_hash_checks=ndocs,assertion_dispositions=nassertions,relation_dispositions=nrelations,separate_retired_ids=sorted(set(reviews)-people),pending_reviews=0),ensure_ascii=False))
