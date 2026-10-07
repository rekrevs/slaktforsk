"""Mechanical implementation of settled Astra decisions in an isolated clone only."""
import pathlib,json,copy,sqlite3,hashlib,subprocess
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
def save(name,value):
 p=B/name;p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');return p
DB=sqlite3.connect('file:'+str(B/'clone/research-candidate-v2.sqlite')+'?mode=ro',uri=True);DB.row_factory=sqlite3.Row
def rows(q,args=()):return [dict(r) for r in DB.execute(q,args)]
def existing(oid,version):
 rev=rows('select * from revision where object_id=? order by version desc limit 1',(oid,))[0];assert rev['version']==version
 kind=rows('select kind from object where id=?',(oid,))[0]['kind'];data=rows(f'select * from {kind} where revision_id=?',(rev['id'],))[0];data.pop('revision_id')
 for k,v in data.items():
  if k.endswith('_json') and v is not None:data[k]=json.loads(v)
 origins=[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in rows('select * from origin where revision_id=?',(rev['id'],))]
 ev=[{'object':r['basis_revision_id'].rsplit('@',1)[0],'version':int(r['basis_revision_id'].rsplit('@',1)[1]),'role':r['role'],'note':r['note']} for r in rows('select * from dependency where revision_id=?',(rev['id'],))]
 return {'id':oid,'kind':kind,'expectedVersion':version,'data':data,'origins':origins,'evidence':ev,'disposition':rev['disposition'],'evidenceStatus':rev['evidence_status'],'rationale':rev['rationale'],'caveat':rev['caveat']}
def new(oid,kind,data,ev,caveat=''):
 assert not rows('select id from object where id=?',(oid,));return {'id':oid,'kind':kind,'expectedVersion':None,'data':data,'origins':[],'evidence':ev,'disposition':'recorded','evidenceStatus':None,'rationale':'T-0775 AC2–3: exakt genomförd Astra-beslutad fullpostutvinning och avgränsad adoption.','caveat':caveat}
clarification='T-0775, C-0035: Charlottas egen rad 2 följer med dittotecken hushållets bokförda överföring från p.335 till Mineberg p.420 den 1908-10-16 och vidare till p.402 den 1914-10-30. Hela 1900–1914 är därför inte en lucka utan egna ankare. Mellanleden 1900–1908 återstår; uppgifterna visar bokföring och inte obruten fysisk vistelse. Övriga luckor, frågor och granskningsutfall kvarstår.'
changes=[]
for oid,v in {'BIO-P-0043':4,'THEME-P-0043-BO':1,'CONTRACT-P-0043-PK-03':1,'P-0043/Q-01':1}.items():
 obj=existing(oid,v);field='markdown' if oid.startswith('BIO-') else 'body'
 if oid=='BIO-P-0043':
  old='åren 1900–1914 mellan folkräkningarna\noch Ljungbacka';assert obj['data'][field].count(old)==1;obj['data'][field]=obj['data'][field].replace(old,'åren 1900–1908 före Minebergankaret',1)
 obj['data'][field]+='\n\n'+clarification
 obj['rationale']+=' T-0775 AC3–4: exakt självständigt Astra-beslutad Charolttas egen rad2-kopieföljd; övriga luckor och utfall bevaras.'
 obj['evidence'].append({'object':'AUDIT-T0775-C0035','version':1,'role':'supports','note':'Egen rad2 med dittoburna källbundna överföringsankare; inget obrutet vistelseanspråk.'});changes.append(obj)
op={'id':'T-0775/independent-copy-amendment-v3','actor':'Codex Sol implementation of explicit independent Astra decision','reason':'T-0775 AC3–4: fyra aktuella Charlottakopior preciserade med egna bokföringsankare i sammaC0035scope.','dependencyReviewVersion':2,'changes':changes};save('independent-copy-amendment-operation-v3.json',op)
