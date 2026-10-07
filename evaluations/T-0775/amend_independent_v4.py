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

obj=existing('O-P-0024-census-1910-fields',2)
old='Aktens senare bedömning begränsar yrket till gruppuppgift med medel tillförlitlighet; ingen egen utskriven yrkesanteckning.'
newtext='1910 års egen yrkescell har ett dittotecken under Johans utskrivna Jordbruksarbetare och återger därmed samma yrkesuppgift för Ragnar. Ordet är inte utskrivet på hans rad; arbetsgivare, anställningsförhållande och yrkets varaktighet fastställs inte.'
assert obj['caveat'].count(old)==1;obj['caveat']=obj['caveat'].replace(old,newtext,1)
obj['rationale']+=' T-0775 AC3–4: självständig Astra-rättelse av kvarvarande gruppuppgiftsreservation; råditto och övriga caveats bevaras.'
obj['evidence'].append({'object':'AUDIT-T0775-C0026','version':1,'role':'supports','note':'Egen råditto i1910kolumn; individuellt reserverad arbetsgivar-/varaktighetsgräns.'})
op={'id':'T-0775/independent-copy-amendment-v4','actor':'Codex Sol implementation of explicit independent Astra decision','reason':'T-0775 AC3–4: kvarvarande felaktig gruppuppgift i O24caveat rättad med egen råditto, inga övriga råfältändringar.','dependencyReviewVersion':2,'changes':[obj]};save('independent-copy-amendment-operation-v4.json',op)
