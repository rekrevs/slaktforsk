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
premise='1910 års egen yrkescell har ett dittotecken under Johans utskrivna Jordbruksarbetare och återger därmed samma yrkesuppgift för Ragnar. Ordet är inte utskrivet på hans rad; arbetsgivare, anställningsförhållande och yrkets varaktighet fastställs inte.'
ids={'BIO-P-0024':2,'RESEARCH-P-0024-9d76f0343410':3,'CONTRACT-P-0024-PK-06':2,'CONTRACT-P-0024-PK-07':2,'CONTRACT-P-0024-PK-09':2,'KEY-P-0024-a8ace2e6328f':2,'THEME-P-0024-ARB':2,'KEY-P-0011-5a3111f7ed7b':1};changes=[]
def replace(obj,f,old,new):
 assert obj['data'][f].count(old)==1,(obj['id'],old);obj['data'][f]=obj['data'][f].replace(old,new,1)
for oid,v in ids.items():
 obj=existing(oid,v);f='markdown' if 'markdown'in obj['data'] else'body'
 if oid.startswith('BIO-') or oid.startswith('RESEARCH-'):
  old=[p for p in obj['data'][f].split('\n\n') if 'gruppuppgift' in p and 'jordbruksarbetare'in p.lower()];assert len(old)==1
  replace(obj,f,old[0],'Den äldre granskningen 2026-09-09 nedgraderade yrkesuppgiften (A-0142/A-7697); detta granskningsförlopp bevaras som historik. '+premise)
 elif oid=='CONTRACT-P-0024-PK-06':replace(obj,f,'han har ingen egen yrkesanteckning','egen 1910-yrkesuppgift är dittoburen, medan arbetsgivare och varaktighet är öppna');obj['data'][f]+='\n'+premise
 elif oid=='CONTRACT-P-0024-PK-07':replace(obj,f,'Två poster är uttryckligen spärrade: de två bladen som självständiga röster, och `Jordbruksarbetare` som hans egen yrkesuppgift','En post är fortsatt spärrad: de två bladen som självständiga röster. Jordbruksarbetare är en egen dittoburen källuppgift1910');obj['data'][f]+='\n'+premise
 elif oid=='CONTRACT-P-0024-PK-09':replace(obj,f,'dittotecknet görs inte till en egen uppgift, och tillförlitligheten nedgraderas i stället för att lydelsen skrivs om','dittotecknet är en egen upprepning av Johans yrkesuppgift; den äldre nedgraderingen bevaras som granskningshistorik');obj['data'][f]+='\n'+premise
 elif oid=='KEY-P-0024-a8ace2e6328f':replace(obj,f,'~~`Jordbruksarbetare` som hans egen yrkesuppgift~~','`Jordbruksarbetare` som hans egen dittoburna yrkesuppgift');replace(obj,f,'**Spärrad som individuellt belägg.** Cellen är ett dittotecken under broderns rad.',premise)
 elif oid=='THEME-P-0024-ARB':replace(obj,f,'Dittot behåller sin tidigare personbundna begränsning.',premise)
 elif oid=='KEY-P-0011-5a3111f7ed7b':replace(obj,f,'Originalbelagd i vigselboken; födelseförsamlingen är inte läst.','Originalbelagd i vigselboken; Oskarshamn är uppgiven födelseort i egen SCB-rad 1930 (C-0027). Egen födelsepost och säker församlingstillhörighet vid födelsen är fortfarande oprövade.')
 else:raise Exception(oid)
 basis='AUDIT-T0775-C0027' if oid.startswith('KEY-P-0011') else 'AUDIT-T0775-C0026'
 assert not any(e['object']==basis for e in obj['evidence']);obj['evidence'].append({'object':basis,'version':1,'role':'supports','note':'T-0775 oberoende Astra-källkontroll och exact-copyrättelse; samma original, ingen ny historisk röst.'})
 obj['rationale']+=' T-0775 AC3–4: självständig slutAstra-prövning av egen råkolumn och aktuell textkopia; övriga fakta, utfall och ägarkunskap bevaras.'
 changes.append(obj)
op={'id':'T-0775/independent-copy-amendment-v1','actor':'Codex Sol implementation of explicit independent Astra decisions','reason':'T-0775 AC3–4: sju Ragnar1910dittokopior och en Katyfödelseortsnyckel preciserade efter självständig source/currentcopyprövning.','dependencyReviewVersion':2,'changes':changes};save('independent-copy-amendment-operation-v1.json',op);print(len(changes),'independently approved copy amendments')
