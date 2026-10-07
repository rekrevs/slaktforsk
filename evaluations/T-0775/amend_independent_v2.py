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

obj=existing('PATH-P-0045-KP-04',1);old='belagt i två av hans egna\n  rader';repl='belagt i flera egna rader, nu även C-0035 r4 och r10 med motsvarande 1908-form';assert obj['data']['body'].count(old)==1;obj['data']['body']=obj['data']['body'].replace(old,repl,1)
obj['rationale']+=' T-0775 AC3–4: exakt självständigt Astra-beslutad militärnyckelprecision; inskrivningslängd fortsatt EJ UNDERSÖKT och ingen tjänstgöringsslutsats.'
obj['evidence'].append({'object':'AUDIT-T0775-C0035','version':1,'role':'supports','note':'Eget rånummer på r4/r10; samma bokföringskedja, ingen extra oberoende historisk röst.'})
op={'id':'T-0775/independent-copy-amendment-v2','actor':'Codex Sol implementation of explicit independent Astra decision','reason':'T-0775 AC3–4: ytterligare individuell KP04kopias två-radsomfång preciserat efter oberoende källkontroll.','dependencyReviewVersion':2,'changes':[obj]};save('independent-copy-amendment-operation-v2.json',op)
