import sqlite3,json,re,pathlib,datetime
c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
kinds=['person','source','record','transcription','mention','observation','identity','place','event','participation','relation','fact','question','search','assessment','narrative']
allrows=[]
for k in kinds:
 cols=[r['name'] for r in c.execute('pragma table_info("'+k+'")')]
 if 'revision_id' not in cols:continue
 for r in c.execute('select c.*,k.* from current_revision c join "'+k+'" k on k.revision_id=c.id'):
  allrows.append(dict(r))
terms=['P-0044', 'C-1060', 'C1060', 'Sven Edvin Severus', 'Ericslund', 'Erikslund', 'Ericsland', 'Tyrestorp', 'Igelstorp', 'Joh. Pet. Carlsson', 'Hilda Lovisa', 'Nilsson Valla', 'F0003287_00058']
hits=[]
for r in allrows:
 fields={k:v for k,v in r.items() if isinstance(v,str) and k not in ['id','object_id','revision_id','operation_id','previous_id']}
 found={k:[t for t in terms if t.casefold() in v.casefold()] for k,v in fields.items()};found={k:v for k,v in found.items() if v}
 if found:hits.append({'id':r['object_id'],'version':r['version'],'kind':r['kind'],'matches':found,'current':r})
p=pathlib.Path('evaluations/T-0778/independent-review')
(p/'C1060-independent-global-search-v1.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'all current_revision domain data and revision caveat/rationale/disposition/evidence_status; no use of Sol hit list','terms':terms,'objects_scanned':len(allrows),'hits':hits},ensure_ascii=False,indent=2)+'\n')
print('scanned',len(allrows),'hits',len(hits));print('counts', {k:sum(x['kind']==k for x in hits) for k in kinds})
