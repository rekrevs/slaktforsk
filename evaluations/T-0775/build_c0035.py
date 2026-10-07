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
source=json.loads((B/'source-decisions/C-0035-source.json').read_text());decision=json.loads((B/'source-decisions/C-0035-decisions.json').read_text());rid='R-f5f8416dc73115868c6b7c36';changes=[]
name_replacements={
'CONTRACT-P-0045-PK-01':('`Jansson` är hushållets visningsnamn, och den enda egna formen stavas `Jaensson`','`Jansson` finns också på egen vuxenrad i C-0035r10; senare egen form `Jaensson` bevaras'),
'CONTRACT-P-0045-PK-07':('Tre poster är uttryckligen spärrade: `Jansson` som hans egen skrivna form,','Två poster är fortsatt uttryckligen spärrade:'),
'CONTRACT-P-0045-PK-09':('`Jansson` skiljs från `Jaensson` och den förra kallas visningsnamn, inte belagd form','`Jansson` på egen C-0035r10 skiljs från senare egna `Jaensson`; barndomskällan saknar fortfarande eget efternamn'),
'THEME-P-0045-ID':('`Jaensson` som hans enda egna efternamnsform','`Jaensson` som senare egen efternamnsform, jämte egen `Jansson` i C-0035r10'),
'KEY-P-0045-319fcdd151f9':('`Jansson` som projektets visningsnamn','`Jansson` också som egen vuxenform i C-0035r10'),
'KEY-P-0045-37baef485027':('Får användas som visningsnamn men inte som belagd egen form.','Spärren gäller enbart barndomskällans1888–1891omfång. Egen vuxenform Jansson är belagd i C-0035r10.'),
'KEY-P-0045-723f55e38971':('den enda efternamnsform som är hans egen','en senare efternamnsform som är hans egen; C-0035r10 har även egen Jansson')}
def replace(obj,f,old,repl):
 assert obj['data'][f].count(old)==1,(obj['id'],old);obj['data'][f]=obj['data'][f].replace(old,repl,1)
for e in decision['native_changes']:
 obj=existing(e['id'],e['expectedVersion']);oid=e['id'];a=e['action'];f='markdown' if 'markdown' in obj['data'] else 'body'
 if a=='append_full_boundary_and_bind_audit':
  if obj['kind']=='record':obj['caveat']+=' '+e['text']
  else:obj['data'][f]+='\n\n'+e['text']
 elif a=='replace_affected_value_literal':obj['data']['value_literal']=e['text'];obj['caveat']+=' T-0775: fullfältstabellen ersätter äldre generell tomfältsbeskrivning; källbunden nattvardsdag bevaras.'
 elif a=='replace_name_paragraph_preserve_other_text':
  old=[p for p in obj['data'][f].split('\n\n') if p.startswith('**Den första är hans namn.**') or p.startswith('**Namnet kräver en åtskillnad')];assert len(old)==1;replace(obj,f,old[0],e['text'])
  for before,after in e.get('also_replace',{}).items():
   if before in obj['data'][f]:replace(obj,f,before,after)
  obj['data'][f]+='\n\n'+e['append']
 elif a=='replace_body_keep_title_and_open':obj['data'][f]=e['text']
 elif a=='replace_exact_span':replace(obj,f,e['before'],e.get('after',e.get('text')))
 elif a in ['append_context_and_keep_open','append_source_bounded_occupation','append_reserved_note_keep_outcome','append_controlled_scope_keep_outcome']:obj['data'][f]+='\n\n'+e['text']
 elif a=='replace_two_row_scope_and_append':replace(obj,f,e['before'],e['text'])
 elif a=='replace_exclusive_name_claim_keep_other_text':
  old,new_text=name_replacements[oid];replace(obj,f,old,new_text)
 elif a=='replace_flen_annual_only_claim_keep_other_text':
  old=e['remove_claim'] if oid!='THEME-P-0045-BO' else 'Skedevi- och Flenperioderna vilar på årsankare, inte på daterade flyttar';replace(obj,f,old,e['text'])
  for old,new_text in e.get('additional_exact_corrections',{}).items():replace(obj,f,old,new_text)
 else:raise Exception(a)
 for ev in obj['evidence']:
  if ev['object']==rid and ev['version']==1:ev['version']=2
 obj['rationale']+=' T-0775 AC3: exakt individuell Astra C0035 ändring; orelaterad evidens, äldre starkare stöd och grindutfall bevaras.'
 changes.append(obj)
ev=[{'object':rid,'version':2,'role':'supports','note':'T-0775 Astra fullpostmatris och reserverad attribution; samma original, ingen ny historisk röst.'}]
audit=new('AUDIT-T0775-C0035','assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_reservations','body':json.dumps({'source':source,'decisions':decision},ensure_ascii=False,indent=2)},ev,decision['gates']);changes.append(audit)
for pid in decision['impact_people']:
 own=[r for r in source['matrix'] if r.get('person')==pid];assert own
 changes.append(new('ADOPT-T0775-C0035-'+pid,'assessment',{'subject_id':pid,'criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':json.dumps({'person':pid,'own_rows':own,'coverage':decision['coverage'],'limitations':source['limitations'],'gates':decision['gates']},ensure_ascii=False,indent=2)},ev+[{'object':audit['id'],'version':1,'role':'supports','note':'Individuella egna rader inom samma avgränsade sourceaudit.'}],decision['gates']))
q=next(r for r in decision['new_objects'] if r['type']=='question');assert not rows('select id from object where id=?',(q['suggested_id'],));changes.append(new(q['suggested_id'],'question',{'subject_id':'P-0009','title':q['title'],'outcome':q['outcome'],'body':q['body']},ev,'Attribution och läsning öppna; ingen ny moder-/barnidentitet eller händelse.'))
for row in source['matrix']:
 num=row['row']
 if num not in [4,8,9,10,11,12]:continue
 if num in [8,9]:mid='M-P-0047-foster-'+str(81 if num==8 else 82)
 else:
  mid='M-T0775-C0035-row'+str(num);rawname=next(x['raw'] for x in row['cells'] if x['column']==1)
  changes.append(new(mid,'mention',{'record_id':rid,'name_literal':rawname,'role_literal':'källans namn-/familjeställningscell, rad'+str(num)},ev,'Råform inom denna källrad; ingen ny person eller säker global identifikation.'))
 obs_ev=ev+[{'object':mid,'version':1,'role':'supports','note':'Ordinarie källomnämnande; ingen ny personidentitet.'}]
 changes.append(new('O-T0775-C0035-row'+str(num),'observation',{'record_id':rid,'mention_id':mid,'property':'complete_source_row','value_literal':json.dumps(row,ensure_ascii=False),'value_json':row},obs_ev,'Hela raden med status/reservation. För r10 bevaras ofvanr3 och12 23/4 separat från gift12 23/6; ingen tyst normalisering.'))
entry=source['additional_interlinear_entry'];changes.append(new('O-T0775-C0035-unattributed-pencil','observation',{'record_id':rid,'mention_id':None,'property':'unattributed_interlinear_note','value_literal':json.dumps(entry,ensure_ascii=False),'value_json':entry},ev,'Svag läsning och attribution öppna; ingen säker moder, barnperson eller födelse-/dödhändelse.'))
op={'id':'T-0775/C0035-candidate-v1','actor':'Codex Sol mechanical implementation of settled Astra C0035 decisions','reason':'T-0775 AC2–4: full samepostutvinning, explicit begränsade följdrättelser och öppen blyertsfråga; endast isolerad klon.','dependencyReviewVersion':2,'changes':changes};save('C-0035-candidate-operation-v1.json',op);print('C35',len(changes),'changes; no apply')
