"""Mechanical implementation of settled Astra decisions in an isolated clone only."""
import pathlib,json,copy,sqlite3,hashlib,subprocess
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
def save(name,value):
 p=B/name;p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');return p
DB=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True);DB.row_factory=sqlite3.Row
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
source=json.loads((B/'source-decisions/C-0026-source.json').read_text());decision=json.loads((B/'source-decisions/C-0026-decisions.json').read_text());changes=[];rid=source['record_version'].rsplit('@',1)[0]
for edit in decision['native_changes']:
 obj=existing(edit['id'],edit['expectedVersion']);oid=edit['id']
 if oid==rid:obj['caveat']+=' '+edit['text']
 elif oid.startswith('READ-'):obj['data']['body']+='\n\nT-0775: '+edit['text']
 elif oid.startswith('O-'):
  obj['data']['value_literal']=edit['value_literal'];obj['data']['value_json'].update(edit['value_json']);obj['caveat']=edit['caveat']
 elif oid=='THEME-P-0022-SAM':
  old='Egna a/N och råmarkering l dokumenterade; inget namngivet samfund eller egen trosutsaga.';assert obj['data']['body'].count(old)==1;obj['data']['body']=obj['data']['body'].replace(old,edit['text'],1)
 else:raise Exception(oid)
 obj['rationale']+=' T-0775 AC3: individuell rättelse enligt Astra C0026 beslut; äldre orelaterat stöd och utfall bevaras.'
 # Settled R dependency keeps same source grounding and explicitly moves to completed current record.
 if oid!=rid:
  for e in obj['evidence']:
   if e['object']==rid and e['version']==1:e['version']=2
 changes.append(obj)
record_ev=[{'object':rid,'version':2,'role':'supports','note':'T-0775 Astra-källbeslut; samma originalpost, ingen ny historisk röst.'}]
audit=new('AUDIT-T0775-C0026','assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_reservations','body':json.dumps({'source':source,'decisions':decision},ensure_ascii=False,indent=2)},record_ev,'Svag råtext, källkonflikter och tidigare styrkta personuppgifter hålls skilda; ingen grindändring.')
changes.insert(2,audit)
for pid in decision['impact_people']:
 own=[x for x in source['matrix'] if x.get('person')==pid];assert len(own)==1
 body=json.dumps({'citation':'C-0026','person':pid,'own_row':own[0],'source_scope':source['scope'],'limitations':source['limitations'],'individual_decision':next((x for x in decision['native_changes'] if x['id']=='O-'+pid+'-census-1910-own-fields'),None),'gates':decision['gates']},ensure_ascii=False,indent=2)
 changes.append(new('ADOPT-T0775-C0026-'+pid,'assessment',{'subject_id':pid,'criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':body},record_ev+[{'object':audit['id'],'version':1,'role':'supports','note':'Egen rad och hela avgränsningen i Astra-beslutad matris.'}],'Övriga livsbilds- och källskulder samt identitets-/trädutfall bevaras.'))
op={'id':'T-0775/C0026-candidate-v1','actor':'Codex Sol mechanical implementation of settled Astra C0026 decisions','reason':'T-0775 AC2–4: full relevant postutvinning, individuell religionskolumnsrättelse och nio avgränsade personadoptioner; endast isolerat pilotklon.','dependencyReviewVersion':2,'changes':changes};save('C-0026-candidate-operation-v1.json',op)
print('Candidate',len(changes),'changes; no apply performed')
