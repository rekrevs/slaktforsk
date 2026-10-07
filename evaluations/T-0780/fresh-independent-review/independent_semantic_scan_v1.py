import sqlite3,json,re,hashlib,datetime
from pathlib import Path
base=Path(__file__).parent
c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
patterns={
'C-0043':r'C-?0043|Ebba\s*Alfrida|J\s*\.?\s*A\s*\.?\s*\[efternamn|Burman|arb\.\s*hem\.äg',
'C-0044':r'C-?0044|Anna\s*Albertina|Anders\s*Alfred|Jomark|1904[- /]0[35][- /]0[35]',
'C-0563':r'C-?0563|Zingmark|Sara\s*Sophi|Ester\s*Amali|186[458][- /](?:0[1238])',
'C-0561':r'C-?0561|Caj?sa\s*Greta|Jonas\s*Eugen|Olof\s*Konrad|Nica[nr]or|Nikanor',
'C-0685':r'C-?0685|Botsmark|Johan\s*Pet(?:er)?\.?\s*Zingmark|Johanna\s*Beata',
'C-0069':r'C-?0069|Ultervattnet|Anders\s*Olofsson|Magdalena\s*Christina|Brita\s*Stina\s*Hans',
'C-0425':r'C-?0425|Carl\s*Eric\s*Jakob|Nils\s*Leonard|Anna\s*Teresia\s*Bäckman|Eronberg|Seadström|Ruth\s*Maria\s*Mathilda',
'C-0062':r'C-?0062|Dop-vittnen|Forsberg|B:m|Maria\s*Olofsd|Maria\s*J[öo]nsd|Risliden',
'C-0106':r'C-?0106|Lotta\s*Sophi|giftoman|1867[- /]01[- /](?:20|22)',
'C-0060':r'C-?0060|Buberget|Hilda\s*Charlotta|Irena\s*Sofia|Astrid\s*Maria|Oskar\s*Rudolf',}
compiled={k:re.compile(v,re.I)for k,v in patterns.items()}
kinds=[r[0]for r in c.execute('select distinct kind from object')]
data={}
for kind in kinds:
 try:
  for row in c.execute('select * from "'+kind+'"'):data[row['revision_id']]=dict(row)
 except sqlite3.OperationalError:pass
hits=[];counts={k:0 for k in patterns}
for row in c.execute('select * from current_revision order by object_id'):
 obj=dict(row); obj['data']=data.get(obj['id'],{})
 fields={**{k:v for k,v in obj.items()if k!='data'},**{'data.'+k:v for k,v in obj['data'].items()}}
 matched={}
 for source,pat in compiled.items():
  fs={k:sorted(set(m.group(0)for m in pat.finditer(str(v))))for k,v in fields.items()if v is not None and pat.search(str(v))}
  if fs:matched[source]=fs;counts[source]+=1
 if matched:
  obj['evidence']=[dict(r)for r in c.execute('select * from dependency where revision_id=?',(obj['id'],))]
  obj['origins']=[dict(r)for r in c.execute('select * from origin where revision_id=?',(obj['id'],))]
  hits.append({'matches':matched,'object':obj,'review_disposition':None})
output={'task':'T-0780','created':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Independent direct readonly live current_revision scan over every metadata and subtype field incl structured JSON, status, caveat, outcome/body. Patterns selected from reviewer originals; not imported from Sol candidate list. Whole matched objects retained. Matches are routing, not errors.','patterns':patterns,'counts':counts,'items':hits}
p=base/'independent-semantic-scan-v1.json';p.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'counts':counts,'union':len(hits)},indent=2))
