import json,pathlib,hashlib,sqlite3,subprocess,datetime
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[1]
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,d):(BASE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cli(args):
 r=subprocess.run(['node','genealogy2/cli.mjs',*args],cwd=ROOT,text=True,capture_output=True,check=True)
 return json.loads(r.stdout)
c=sqlite3.connect('file:'+str(ROOT/'genealogy2/data/research.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
pre=ROOT/'genealogy2/verification/T-0677/pre-start-scope-review-proposed-20260924.json';d=json.loads(pre.read_text());vd=pre.parent
completed={}
for p in vd.glob('*astra-completion*.json'):
 x=json.loads(p.read_text());cid=x.get('citation');decision=x.get('decision','')
 if cid:completed[cid]={'path':str(p.relative_to(ROOT)),'sha256':sha(p),'decision':decision,'journal':x.get('journal_head')}
# Earlier root completion receipts are explicitly paired with durable checkpoint.
prior=['C-0002','C-0004','C-0751','C-0008','C-0028','C-0033','C-0034','C-0030','C-0031','C-0032']
for cid in prior:
 if cid not in completed:
  matches=sorted(vd.glob(cid.replace('C-','c')+'*completion*.json'))
  completed[cid]={'path':str(matches[-1].relative_to(ROOT)) if matches else None,'sha256':sha(matches[-1]) if matches else None,'checkpoint':'T-0677 latest checkpoint identifies initial ten as completed','receipt_detail_check_pending':not bool(matches)}
order=[cid for g in d['start_order_proposed'] for cid in g['citations']]
selected=[x for x in order if x not in completed][:3]
assert len(completed)==27,(len(completed),sorted(completed))
assert selected==['C-0026','C-0027','C-0035'],selected
cards=[]
for cid in selected:
 m=next(x['manifest'] for x in d['whole_citation_crosswalk'] if x['manifest']['id']==cid)
 records=[];pids=set()
 for rid in m['native_record_ids']:
  x=cli(['inspect',rid]);save(rid+'-inspect.json',x);cur=x['current'];sid=cur['source_id'];sx=cli(['inspect',sid]);save(sid+'-inspect.json',sx)
  ids=c.execute('''select distinct i.person_id from identity i join revision ir on ir.id=i.revision_id join mention m on m.record_id=? join revision mr on mr.id=m.revision_id where i.mention_id=mr.object_id and ir.version=(select max(version) from revision where object_id=ir.object_id) and mr.version=(select max(version) from revision where object_id=mr.object_id)''',(rid,)).fetchall()
  pids.update(r[0] for r in ids)
  assets=[]
  for p in m['legacy_media_paths']:
   row=c.execute('select * from asset where path=?',(p,)).fetchone();assets.append({'path':p,'registered':dict(row) if row else None,'actual_sha256':sha(ROOT/p),'actual_bytes':(ROOT/p).stat().st_size})
  records.append({'id':rid,'version':x['currentVersion'],'source_id':sid,'source_version':sx['currentVersion'],'locator':cur['locator'],'assets':assets})
 cards.append({'citation':cid,'metadata_only':True,'document':{'path':m['document_path'],'sha256':sha(ROOT/m['document_path'])},'records':records,'person_ids_from_current_identity_links':sorted(pids),'no_new_source_reading':True})
save('selection.json',{'task':'T-0775','state':'METADATA_PROPOSAL_REQUIRES_ROOT_LOCK','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'basis':{'path':str(pre.relative_to(ROOT)),'sha256':sha(pre),'ordering':'adopted original start_order_proposed, within group manifest order'},'canonical_journal':c.execute('select max(sequence) from operation_payload').fetchone()[0],'completed_count':len(completed),'completion_receipts':completed,'selected':selected,'cards':cards,'limitations':['Metadata selection is not a source judgement; images have not been opened.','Existing record caveats are preserved in full inspect captures, not reinterpreted.']})
print('Selected',selected,'persons',[(x['citation'],x['person_ids_from_current_identity_links']) for x in cards])
