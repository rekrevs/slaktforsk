"""Read-only root baseline comparison of every database table."""
import argparse,sqlite3,json,hashlib,pathlib,datetime
p=argparse.ArgumentParser();p.add_argument('baseline');p.add_argument('--output',required=True);a=p.parse_args()
def connect(path):return sqlite3.connect('file:'+str(pathlib.Path(path).resolve())+'?mode=ro',uri=True)
r=pathlib.Path(__file__).resolve().parents[2];live=connect(r/'genealogy2/data/research.sqlite');base=connect(a.baseline)
def schema(c):return c.execute("select name,sql from sqlite_master where type='table' and name not like 'sqlite_%' order by name").fetchall()
assert schema(live)==schema(base),'Table schema differs from baseline'
def digest(c,t):
 rows=[]
 for row in c.execute('select * from "'+t.replace('"','""')+'"'):
  rows.append(json.dumps(row,ensure_ascii=False,separators=(',',':'),default=lambda x:{'blob':x.hex()}))
 h=hashlib.sha256()
 for s in sorted(rows):h.update(s.encode());h.update(b'\n')
 return {'rows':len(rows),'sha256':h.hexdigest()}
checks=[]
for t,_ in schema(live):
 l=digest(live,t);b=digest(base,t);checks.append({'table':t,'live':l,'baseline':b,'pass':l==b})
o={'task':'T-0780','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_baseline_tables_equal':all(x['pass'] for x in checks),'checks':checks,'array_order':'Preserved in exact JSON column strings; SQL row order normalized.'}
pathlib.Path(a.output).write_text(json.dumps(o,indent=2)+'\n');print(json.dumps({k:v for k,v in o.items() if k!='checks'}));assert o['all_baseline_tables_equal']
