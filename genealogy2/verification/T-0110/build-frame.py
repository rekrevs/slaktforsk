from pathlib import Path
import sqlite3,json,re,collections,hashlib,sys
if len(sys.argv)!=3: raise SystemExit("Usage: build-frame.py inventory.json new-frame.json (from repository root)")
if Path(sys.argv[2]).exists(): raise SystemExit("Output already exists")
c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
rows=lambda q:[dict(r) for r in c.execute(q)]
current={r['id']:r for r in rows('select * from current_revision')}
allrev={r['id']:r for r in rows('select * from revision')}
data={k:{r['revision_id']:r for r in rows('select * from '+k)} for k in ['fact','person','identity','relation','event','participation','question','search','record']}
byobj={r['object_id']:r for r in current.values()}
inv=json.loads(Path(sys.argv[1]).read_text())
bearing={p['id'] for p in inv['people'] if p['treeEffect']['usable'] and p['treeEffect']['outcome']=='supporting'}
links=collections.defaultdict(set)
for d in rows("select * from dependency where role in ('supports','derived_from')"):links[d['revision_id']].add(d['basis_revision_id'])
cits={r['document_path']:r['id'] for r in rows("select * from legacy_entity where kind='citation'")}
orig=collections.defaultdict(set)
for r in rows('select o.revision_id,u.document_path,u.kind,u.parsed_json from origin o join unit u on u.id=o.unit_id'):
 if r['document_path'] in cits:orig[r['revision_id']].add(cits[r['document_path']])
 elif r['kind'] in ('assertion','relation'):
  # Only explicit legacy citation hyperlinks, not loose historical mentions.
  orig[r['revision_id']].update(re.findall(r'\[(C-\d{4})\]\(',r['parsed_json']))
def citations(rev):
 out=set();seen=set();stack=[rev]
 while stack:
  r=stack.pop()
  if r in seen:continue
  seen.add(r);out.update(orig[r]);stack.extend(links[r]-seen)
 return out
frame=collections.defaultdict(list)
def add(r,why,subject=None,sole=False):
 cs=citations(r['id'])
 if sole and len(cs)!=1:return
 for cid in cs:frame[cid].append(dict(object=r['object_id'],revision=r['id'],reason=why,subject=subject))
def eligible(r):return r['disposition'] in ('accepted','recorded') and r['evidence_status'] not in ('LEAD','CONFLICT','REJECTED','UNKNOWN')
events=set()
for r in current.values():
 if r['kind']=='participation':
  v=data['participation'][r['id']]
  if v['person_id'] in bearing and eligible(r):events.add(v['event_id']);add(r,'bearing_participation',v['person_id'])
for r in current.values():
 if not eligible(r):continue
 k=r['kind'];v=data.get(k,{}).get(r['id'],{})
 if k=='fact' and v['subject_id'] in bearing:add(r,'bearing_fact',v['subject_id'])
 elif k=='event' and r['object_id'] in events:add(r,'bearing_event')
 elif k=='relation':
  if v['from_person'] in bearing or v['to_person'] in bearing:add(r,'bearing_relation',v['from_person']+' / '+v['to_person'])
  if r['disposition']=='accepted' and v['relation_type']=='parent':add(r,'sole_parent_citation',sole=True)
 elif k=='identity' and r['disposition']=='accepted' and v['decision']=='accepted':add(r,'sole_identity_citation',v['person_id'],sole=True)
 elif k=='question' and v['outcome'].strip('.').upper() in ['FASTSTÄLLD','AVVISAD','OLÖST INOM PRÖVAT OMFÅNG','NEGATIVE']:
  # A closure can rely on a negative search via a dependency chain.
  seen=set();stack=list(links[r['id']]);neg=[]
  while stack:
   d=stack.pop()
   if d in seen:continue
   seen.add(d);stack.extend(links[d]-seen)
   if d in data['search'] and data['search'][d]['outcome']=='negative':neg.append(d)
  cs=citations(r['id'])
  if len(cs)==1 and neg:add(r,'sole_negative_closure',v['subject_id'],sole=True)
# Native imported question bodies still contain explicit textual citations
# without dependency rows. These four bounded-negative clauses were checked
# before the draw; the other three single-citation candidates describe positive
# records, not closures by negative evidence.
for oid,cid in [('P-0082/Q-02','C-1071'),('P-0344/Q-01','C-0858'),('P-0416/Q-01','C-1031'),('P-0452/Q-01','C-0854')]:
 r=byobj[oid];v=data['question'][r['id']]
 assert cid in v['body']
 frame[cid].append(dict(object=oid,revision=r['id'],reason='sole_negative_closure_text',subject=v['subject_id']))
result={'schema':'T-0110-frame/1','date':'2026-09-18','bearing_persons':sorted(bearing),'operation_count':c.execute('select count(*) from operation').fetchone()[0],'rows':[{'citation':cid,'supports':frame[cid]} for cid in sorted(frame)]}
p=Path(sys.argv[2]);p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'bearing_persons':len(bearing),'citations':len(frame),'reasons':dict(collections.Counter(x['reason'] for v in frame.values() for x in v)),'frame_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},ensure_ascii=False))
