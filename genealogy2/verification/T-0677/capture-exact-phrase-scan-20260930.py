"""Mechanical current typed-data phrase scan with capture-based deduplication."""
import ast,json,sqlite3,subprocess,sys,datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
p=Path(__file__).resolve().parent;post,seq,outname,*phrases=sys.argv[1:];phrases=[x.casefold() for x in phrases]
ns={'json':json};t=ast.parse((p/'build-c0001-temp-20260930.py').read_text());exec(compile(ast.Module(body=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in ['rows','full']],type_ignores=[]),'helpers','exec'),ns)
seen=set()
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ('id','object_id','object','revision_id') and isinstance(v,str):seen.add(v.split('@')[0])
   walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
inputs=list(p.glob(f'{post}-prestart-person-*-j{seq}-20260930.json'))+[p/f'{post}-impact-current-j{seq}-20260930.json']
for f in inputs:walk(json.loads(f.read_text()))
db=sqlite3.connect(f'file:{p.parents[2]}/genealogy2/data/research.sqlite?mode=ro',uri=True);db.row_factory=sqlite3.Row;matches=[];extra=[]
for r in db.execute('select id from object'):
 o=ns['full'](db,r['id']);s=json.dumps(o['data'],ensure_ascii=False).casefold();hits=[t for t in phrases if t in s]
 if hits:
  matches.append({'id':r['id'],'version':o['revision']['version'],'phrases':hits,'already_captured':r['id'] in seen})
  if r['id'] not in seen:extra.append(r['id'])
def inspect(oid):
 r=subprocess.run(['node','genealogy2/cli.mjs','inspect',oid,'--format','json'],cwd=p.parents[2],capture_output=True,text=True);assert r.returncode==0;return json.loads(r.stdout)
with ThreadPoolExecutor(max_workers=4) as pool:ins=dict(zip(extra,pool.map(inspect,extra)))
f=p/outname;assert not f.exists();f.write_text(json.dumps({'task':'T-0677','journal':int(max((p.parents[2]/'genealogy2/journal').glob('*.json')).name[:9]),'snapshot_journal':int(seq),'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Latest typed data only, exact case-insensitive phrases; mechanical matches, not substantive dispositions.','phrases':phrases,'matches':matches,'new_outside_existing_captures':ins},ensure_ascii=False,indent=2)+'\n');print({'matches':matches,'extra_ids':extra,'artifact':f.name})
