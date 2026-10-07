"""Read-only class capture from the fixed citation crosswalk, not a source decision."""
import json,sqlite3,subprocess,sys,datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
p=Path(__file__).resolve().parent;root=p.parents[2];post,seq=sys.argv[1:];citation=post.upper().replace('C','C-',1)
head=max((root/'genealogy2/journal').glob('*.json'));assert int(head.name[:9])==int(seq)
x=json.loads((p/'citation-crosswalk-prestart-review-20260924.json').read_text());entry=next(e for e in x['entries'] if e['citation']==citation)
ids=[r['id'] for r in entry['native_records']]+[s['source_id'] for s in entry['source_description_owners']]+[o['object_id'] for o in entry['other_current_targets']]
db=sqlite3.connect(f'file:{root}/genealogy2/data/research.sqlite?mode=ro',uri=True)
for r in entry['native_records']:
 ids += [x[0] for x in db.execute('select c.object_id from current_revision c join transcription t on t.revision_id=c.id where t.record_id=?',(r['id'],))]
ids=list(dict.fromkeys(ids))
def run(a):
 cmd=['node','genealogy2/cli.mjs']+a+['--format','json'];r=subprocess.run(cmd,cwd=root,capture_output=True,text=True);assert r.returncode==0,(cmd,r.stderr);return {'command':a,'exit':0,'payload':json.loads(r.stdout)}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,[['inspect',i] for i in ids]+[['impact',citation]]))
f=p/f'{post}-source-class-current-j{seq}-20260930.json';assert not f.exists();f.write_text(json.dumps({'task':'T-0677','journal_sequence':int(seq),'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixed_crosswalk_entry':entry,'results':results},ensure_ascii=False,indent=2)+'\n');assert max((root/'genealogy2/journal').glob('*.json'))==head;print({'file':str(f),'ids':ids})
