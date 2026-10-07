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
source=json.loads((B/'source-decisions/C-0027-source.json').read_text());decision=json.loads((B/'source-decisions/C-0027-decisions.json').read_text());dispositions=json.loads((B/'source-decisions/C-0027-dispositions.json').read_text());rid='R-18df18d44d81e11a21a93743';changes=[]
def replace(obj,old,repl):
 assert obj['data']['body'].count(old)==1,(obj['id'],old);obj['data']['body']=obj['data']['body'].replace(old,repl,1)
def settle(obj,reason):
 for e in obj['evidence']:
  if e['object']==rid and e['version']==1:e['version']=2
 obj['rationale']+=' T-0775 AC3: individuell Astra-disposition: '+reason
 return obj
for edit in decision['native_changes']:
 obj=existing(edit['id'],edit['expectedVersion']);a=edit['action']
 if a=='append_caveat_and_bind_full_extraction':obj['caveat']+=' '+edit['text']
 elif a=='patch_value_json':
  v=obj['data']['value_json']
  for key in edit.get('remove_keys',[]):assert key in v;del v[key]
  for key in edit.get('remove_from_empty',[]):assert key in v['empty'];v['empty'].remove(key)
  v.update(edit.get('set_keys',{}));obj['caveat']+=' '+edit['reason']
 elif a=='replace_exact_span':
  replace(obj,edit['before'],edit['after'])
  for old,repl in edit.get('also_replace',{}).items():replace(obj,old,repl)
 elif a=='replace_caveat':obj['caveat']=edit['text']
 else:raise Exception(a)
 changes.append(settle(obj,edit.get('reason','Exact source-decisions/C-0027-decisions.json change.')))
for e in dispositions['rows']:
 if e['action']!='revise':continue
 obj=existing(e['id'],e['version']);oid=e['id']
 if oid=='CONTRACT-P-0011-PK-05':replace(obj,'Den enda outvunna cellen','Det kontrollerade men oavgjorda råtecknet')
 elif oid=='CONTRACT-P-0012-PK-05':obj['data']['body']+='\nT-0775: äldre blankbeskrivning av m-kolumnen rättas till egen X−; skol-, barn- och ekonomifältens lokala blankhet bevaras. Inget grindutfall ändras.'
 elif oid=='CONTRACT-P-0014-PK-05':obj['data']['body']+='\nT-0775: lodrätt fortsättnings-/dittospår finns i tryckt m-kolumn, utan orttolkning. Övriga egna tomma fält har lokal räckvidd; daterat utfall bevaras.'
 elif oid=='PATH-P-0010-KP-07':
  replace(obj,'födelseortskoden `353`','råkoden `353` i den tryckta m-kolumnen (kodens typ/nyckel ej fastställd)');obj['data']['body']+='\nT-0775: kolumnrubrikerna är nu direkt kontrollerade och råmärkets position avgjord. Kodnyckel, enhet och barnkod är fortfarande EJ UNDERSÖKT; ingen ny arkivväg öppnad.'
 elif oid.startswith('READ-'):obj['data']['body']+='\nT-0775: hela målrad30–33 kontrollerad enligt fullfältstabell; m-kolumn353/572/X−/lodrättspår bevaras utan fastställd kodnyckel.'
 elif oid=='THEME-P-0012-EKO':replace(obj,'Faderns inkomst 6 900 tillhör honom','Faderns råcell 69— har oavgjord enhet; 6 900 är en upphävd normalisering. Råcellen tillhör honom')
 elif oid=='THEME-P-0012-SAM':replace(obj,'Egna kyrkliga och civila kolumner 1930 är tomma','Ogift kvinnokategori är markerad; nattvards- och anmärkningsfält saknar egen saktext. Tryckt m-cell innehåller rå X− utan avkodad innebörd')
 else:raise Exception(oid)
 changes.append(settle(obj,e['reason']))
ev=[{'object':rid,'version':2,'role':'supports','note':'T-0775 Astra fullpostprövning av samma original; ingen ny historisk röst.'}]
audit=new('AUDIT-T0775-C0027','assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_reservations','body':json.dumps({'source':source,'decisions':decision,'individual_dispositions':dispositions},ensure_ascii=False,indent=2)},ev,decision['gates']);changes.append(audit)
for pid in decision['impact_people']:
 own=[r for r in source['matrix'] if r.get('person')==pid];assert len(own)==1,(pid,source.keys())
 changes.append(new('ADOPT-T0775-C0027-'+pid,'assessment',{'subject_id':pid,'criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':json.dumps({'person':pid,'own_row':own[0],'coverage':decision['coverage'],'gates':decision['gates'],'limits':source.get('limitations')},ensure_ascii=False,indent=2)},ev+[{'object':audit['id'],'version':1,'role':'supports','note':'Egen rad i fullpostmatris och dess begränsningar.'}],decision['gates']))
op={'id':'T-0775/C0027-candidate-v1','actor':'Codex Sol mechanical implementation of settled Astra C0027 decisions','reason':'T-0775 AC2–4: exakt fullpostutvinning, individuella råfält-/prosekorrigeringar och fyra personadoptioner; isolerad pilotklon.','dependencyReviewVersion':2,'changes':changes};save('C-0027-candidate-operation-v1.json',op);print(len(changes),'C0027 changes; not applied')
