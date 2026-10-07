import json,sqlite3,subprocess,time,re,hashlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
b=Path('evaluations/T-0780/preparation');s=b/'selected';s.mkdir(exist_ok=True);start=time.time();c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
selected=['C-0043','C-0044','C-0563','C-0561','C-0685','C-0069','C-0425','C-0062','C-0106','C-0060'];ix=[];persons=set();objects=set();clean=[]
def cli(args,p):
 r=subprocess.run(['node','genealogy2/cli.mjs',*args],capture_output=True,text=True);p.write_text(r.stdout);assert r.returncode==0,r.stderr;return json.loads(r.stdout)
for cid in selected:
 card=json.load(open(b/(cid+'-routing-v1.json')));rs={x['object_id'] for x in card['current_records']};objects|=rs
 for cl in card['actual_j281_accepted_graph_claims']:
  persons.update(v for k,v in cl['data'].items() if k in ['person_id','from_person','to_person']);objects.add(cl['claim_revision']['object_id'])
 persons.update(card['metadata_person_routing']);impact=cli(['impact',cid],s/(cid+'-impact-v1.json'));ix.append({'citation':cid,'impact':str(s/(cid+'-impact-v1.json'))})
 for r in card['current_records']:
  objects.add(r['data']['source_id'])
  clean.append({'citation':cid,'record_id':r['object_id'],'locator':r['data']['locator'],'media':[{'path':m['path'],'sha256':m['actual_sha256'],'width':m.get('width'),'height':m.get('height')} for m in card['media']]})
# Full currently associated person context captures stronger sources/research, no adjudication.
def person(pid):
 cli(['person',pid,'--full','--format','json'],s/(pid+'-full-v1.json'))
 cli(['person',pid,'--format','json'],s/(pid+'-person-v1.json'))
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(person,sorted(persons)))
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(lambda oid: cli(['inspect',oid],s/(oid+'-inspect-v1.json')),sorted(objects)))
(s/'original-only-routing-v1.json').write_text(json.dumps({'task':'T-0780','warning':'Locator/routing only; no transcription or correction proposals. Locator text may include previously inferred row labels; original must establish actual full unit.','entries':clean},ensure_ascii=False,indent=2)+'\n')
(s/'selected-input-index-v1.json').write_text(json.dumps({'task':'T-0780','selected':selected,'persons':sorted(persons),'inspected_objects':sorted(objects),'impact':ix,'elapsed_seconds':time.time()-start,'read_only':True},ensure_ascii=False,indent=2)+'\n')
print({'persons':len(persons),'objects':len(objects),'seconds':time.time()-start})
