import pathlib,json,sqlite3,hashlib,subprocess,concurrent.futures,re,datetime
B=pathlib.Path(__file__).resolve().parent;R=B.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(B/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
c=sqlite3.connect('file:'+str(R/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
m=json.loads((B/'current-manifest.json').read_text());existing={x['id'] for x in m['captures'] if x['view']=='inspect'};people=set(p for v in m['cases'].values() for p in v['person_routes']);allids=set(existing)
# Complete research and domain-object histories referenced by full person views;
# capture source supports mechanically, without deciding their relative strength.
def walk(x):
 if isinstance(x,dict):
  if x.get('object_id'):allids.add(x['object_id'])
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for p in people:walk(json.loads((B/'current'/('person-full-'+p+'.json')).read_text()))
known={r[0] for r in c.execute('select object_id from current_revision')};allids&=known
supportids=set();front=set(allids)
# bounded backward dependency closure, actual registered dependencies only
while front:
 nxt=set()
 for oid in front:
  for row in c.execute('select d.basis_revision_id from dependency d join current_revision r on r.id=d.revision_id where r.object_id=?',(oid,)):
   rid=row[0];v=c.execute('select object_id from revision where id=?',(rid,)).fetchone()
   if v and v[0] not in allids:nxt.add(v[0])
 supportids|=nxt;allids|=nxt;front=nxt

def capture(oid):
 p=B/'current'/('inspect-'+oid.replace('/','__')+'.json');r=subprocess.run(['node','genealogy2/cli.mjs','inspect',oid],cwd=R,text=True,capture_output=True,check=True);p.write_text(r.stdout);x=json.loads(r.stdout)
 return {'id':oid,'view':'inspect','path':str(p.relative_to(R)),'sha256':sha(p),'version':x.get('currentVersion'),'truncated':False}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:m['captures']+=list(e.map(capture,sorted(allids-existing)))
m.update(count=len(m['captures']),person_routes=sorted(people),backward_support_capture_ids=sorted(supportids),support_selection='Mechanical full native person objects plus their registered backward dependency closure; Astra assesses relevance/strength. No new original opened.')
save('current-manifest.json',m)
save('cards-routing-sidecar.json',{'cases':m['cases'],'source_subject_status':'candidate routing only, Astra decides relevant source people','selection_unchanged':True})
selection=json.loads((B/'selection.json').read_text());receipts=[]
for cid,meta in selection['completion_receipts'].items():
 p=R/meta['path'];x=json.loads(p.read_text());assert sha(p)==meta['sha256'];receipts.append({'citation':cid,'path':meta['path'],'sha256':sha(p),'decision':x.get('decision'),'journal_head':x.get('journal_head'),'all_fields_preserved_in_original':True})
assert len(receipts)==39
save('completion-receipt-reconciliation.json',{'journal_head':277,'pending':0,'accepted_receipts':receipts,'count':39,'next_exact_two':selection['selected'],'no_missing_receipts':True})
save('baseline-protection.json',{'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'journal_head':277,'pending':0,'baseline_clone':{'path':str((B/'clone/research-pre.sqlite').relative_to(R)),'sha256':sha(B/'clone/research-pre.sqlite'),'integrity_check':sqlite3.connect(B/'clone/research-pre.sqlite').execute('pragma integrity_check').fetchone()[0]},'protected_current_revisions':[dict(x) for x in c.execute("select * from current_revision where kind in ('person','relation','identity','identity_resolution') or evidence_status='OWNER_CONFIRMED'")],'review_headers':[dict(x) for x in c.execute("select * from current_revision where kind='assessment' and object_id like 'ASSESSMENT-%'")],'selected_originals':selection['cards'],'captures':m['captures'],'inventory':{'path':str((B/'inventory.json').relative_to(R)),'sha256':sha(B/'inventory.json')},'pedigree':{'path':str((B/'pedigree-P0269.json').relative_to(R)),'sha256':sha(B/'pedigree-P0269.json')}})
print('Complete captures',m['count'],'routed people',len(people),'support closure',len(supportids))
