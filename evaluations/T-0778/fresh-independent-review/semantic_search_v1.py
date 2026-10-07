import sqlite3,json,re
from pathlib import Path
c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
terms=re.compile(r'C[- ]?1047|Eriksro|Drottninggatan.?3|638|Sandberg|elvaår|hitkomst|1923.{0,5}1930|1919.{0,5}1930',re.I)
heads=c.execute('select r.*,o.kind from revision r join object o on o.id=r.object_id where r.version=(select max(rr.version) from revision rr where rr.object_id=r.object_id)').fetchall();out=[]
for row in heads:
 r=dict(row);k=r['kind'];d=dict(c.execute(f'SELECT * FROM "{k}" WHERE revision_id=?',(r['id'],)).fetchone()); fields={**r,**d};hits={f:v for f,v in fields.items() if isinstance(v,str) and terms.search(v)}
 if hits:out.append({'object':r['object_id'],'version':r['version'],'kind':k,'hits':hits,'full':fields})
p=Path('evaluations/T-0778/fresh-independent-review/semantic-current-hits-v1.json');p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(len(out),'current objects matched')
for x in out:
 if any(s in json.dumps(x,ensure_ascii=False) for s in ['P-0003','P-0042','P-0043','P-0047','C1047','C-1047']):print(x['object'],x['version'],','.join(x['hits']))
