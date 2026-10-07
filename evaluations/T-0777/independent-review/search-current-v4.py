import sqlite3,json,re,pathlib,datetime
c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
kinds=['person','source','record','transcription','mention','observation','identity','place','event','participation','relation','fact','question','search','assessment','narrative']
allrows=[]
for k in kinds:
 cols=[r['name'] for r in c.execute('pragma table_info("'+k+'")')]
 if 'revision_id' not in cols:continue
 for r in c.execute('select c.*,k.* from current_revision c join "'+k+'" k on k.revision_id=c.id'):
  allrows.append(dict(r))
terms=['P-0042', 'P-0043', 'P-0045', 'P-0046', 'P-0047', 'P-0065', 'P-0066', 'P-0068', 'P-0069', 'P-0070', 'P-0071', 'P-0072', 'P-0073', 'P-0430', 'P-0433', 'P-0117', 'P-0118', 'P-0133', 'P-0135','tjugosju','tvåårig','27 år','änkeskap','C-0084','C0084','Erik Axel','Charlotta Cecilia','oäkta gossebarn','levande gossebarn','C-0402','C0402','Buberget','Jonas Edvard','Hanna Matilda','Hanna Mathilda','Oskar Rudolf','C-0573','C0573','Zingmark','C-0896','C0896','638','inkomstenhet','hundratal','400 kronor','4 kronor','Astrid Charlotta','C-0911','C0911','Ljungbacka','Maud Karola','Emma Wilhelmina','Ture Alexius','Karl Harry','Karin Elisabet','Elin Augusta','Rhodin','1915-07-03','1906-09-07','1914-10-15','polererska','4–','4 –','4—']
hits=[]
for r in allrows:
 fields={k:v for k,v in r.items() if isinstance(v,str) and k not in ['id','object_id','revision_id','operation_id','previous_id']}
 found={k:[t for t in terms if t.casefold() in v.casefold()] for k,v in fields.items()};found={k:v for k,v in found.items() if v}
 if found:hits.append({'id':r['object_id'],'version':r['version'],'kind':r['kind'],'matches':found,'current':r})
p=pathlib.Path('evaluations/T-0777/independent-review')
(p/'independent-global-search-v4.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'all current_revision domain data and revision caveat/rationale/disposition/evidence_status; no use of Sol hit list','terms':terms,'objects_scanned':len(allrows),'hits':hits},ensure_ascii=False,indent=2)+'\n')
print('scanned',len(allrows),'hits',len(hits));print('counts', {k:sum(x['kind']==k for x in hits) for k in kinds})
