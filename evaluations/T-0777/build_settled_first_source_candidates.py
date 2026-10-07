"""Mechanical new source objects from Astra's approved C0402/C0573 extraction.
Current consequences remain separate and require individual disposition.
"""
import pathlib,json,hashlib,sqlite3
B=pathlib.Path(__file__).resolve().parent;R=B.parents[1]
db=sqlite3.connect('file:'+str(B/'clone/research-pre.sqlite')+'?mode=ro',uri=True)
def ev(oid,v,note):return {'object':oid,'version':v,'role':'supports','note':note}
def save(name,x):(B/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for cid in ['C-0402','C-0573']:
 code=cid.replace('-','');text=(B/'source-review'/f'{cid}-source-v1.md').read_text();changes=[]
 def add(oid,kind,data,evidence,limits):
  assert not db.execute('select 1 from object where id=?',(oid,)).fetchone()
  changes.append({'id':oid,'kind':kind,'expectedVersion':None,'data':data,'origins':[],'evidence':evidence,'disposition':'recorded','evidenceStatus':None,'rationale':f'T-0777 AC2–4: Astras avgjorda fullfältsläsning och avgränsade adoption; samma registreringskedja, ingen ny oberoende historisk röst.','caveat':limits})
 if cid=='C-0402':
  rid='R-126171c8899cd464e47c503b';bases=[ev(rid,2,'Den befintliga fulla hushållsposten, s145.'),ev('S-0005',1,'Versionsbunden folkräkningsmetadata.')]
  raw=text.split('## Full fields\n\n',1)[1].split('## Settled decisions',1)[0].strip()
  decision=text.split('## Settled decisions and implementation\n\n',1)[1].split('Claims `six children`',1)[0].strip()
  limit='Församlingsboksutdrag per1900-12-31; födelseår utan dag/månad. Samma bokföringskedja är beroende. Tomma tros-/nationalitetsfält är endast lokala blankheter; inga identitets-/relations-/grindändringar.'
  tr='TR-T0777-C0402-fullfields';audit='AUDIT-T0777-C0402'
  add(tr,'transcription',{'record_id':rid,'text':raw,'reading_note':limit+' Äldre fem-uppgift ersätts för detta fulla hushåll: sju personer, sex barn.'},bases,limit)
  add(audit,'assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_limits','body':decision+'\nFullgruppen består av Anders och sex barn; fullfältsavskriften dokumenterar samtliga egna markeringar.'},bases+[ev(tr,1,'Samtliga sju personrader och tryckta rubriker.')],limit)
  own=[('P-0065','Anders Jonsson','Bonde |39|ortditto Degerfors|Enkling m','Änkling1900 ersätter inte tidigare starkare exakt dödsuppgift för hustrun; födelseåret39 ersätter inte prövningen av äldre dag.'),('P-0068','Jonas Edvard','s. |71|ortditto|Ogift m','Inget utskrivet eget patronymikon eller yrke.'),('P-0069','Anders','s. |76|ortditto|Ogift m','Inget utskrivet eget patronymikon eller yrke.'),('P-0070','Hildur Charlotta','d. |78|ortditto|Ogift q','Skild från Hanna Matilda1882; inget eget yrke eller patronymikon.'),('P-0071','Karl Magnus','s. |80|ortditto|Ogift m','Inget utskrivet eget patronymikon eller yrke.'),('P-0072','Hanna Matilda','d. |82|ortditto|Ogift q','Matilda är källans form; andra namnformer och exakta datum behåller sina äldre stöd.'),('P-0073','Oskar Rudolf','s. |85|ortditto|Ogift m','Inget utskrivet eget patronymikon eller yrke.')]
  for pid,name,fields,specific in own:
   add('ADOPT-T0777-C0402-'+pid,'assessment',{'subject_id':pid,'criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':json.dumps({'person':pid,'source_name':name,'own_fields':fields,'scope':'Buberget, s145, egen rad i sjupersonsfamilj per1900-12-31','all_other_status_cells':'blank','occupation_if_not_explicit':'blank','final_religion_nationality_absence_column':'blank','family_count':'left1 with bracket for Anders and six children','specific_limit':specific},ensure_ascii=False,indent=2)},bases+[ev(tr,1,'Fullfältsutvinning och egen rad.'),ev(audit,1,'Avgjord källräckvidd.')],limit+' '+specific)
 else:
  raw=text.split('Header ',1)[1].split('\nRetain P0433',1)[0].strip();decision='Retain P0433'+text.split('\nRetain P0433',1)[1].split('\nAdd current',1)[0]
  own=[('P-0433','R-00847ebce446544a7f868a05','Olof Konrad Zingmark','78 | Säfvar, Vbttn[abbreviation]'),('P-0430','R-5321c97f97c84d73381a6a62','Nikanor Zingmark','72 | own ditto to Säfvar,Vbttn')]
  for pid,rid,name,birth in own:
   bases=[ev(rid,1,'Egen avgränsad personrad, s128.'),ev('S-0005',1,'Versionsbunden folkräkningsmetadata.')];suffix=pid.replace('-','');tr=f'TR-T0777-C0573-{suffix}-fullfields';audit=f'AUDIT-T0777-C0573-{suffix}'
   limit='Församlingsboksutdrag per1900-12-31, beroende av hushållsbokskedjan. Egen1 utan gemensam parentes; grannraden bevisar inte gemensamt hushåll eller släktskap. Rosinedahl kommer från äldre fortsättnings-/ankomstrouting; ingen egen ortsrubrik i denna bild. Tomt tros-/nationalitetsfält är lokal blankhet.'
   add(tr,'transcription',{'record_id':rid,'text':'Own person: '+name+'\n'+raw,'reading_note':'Egen rad: Sågverksarbetare | '+birth+' | Ogift m. Övriga statusceller och slutkolumn tomma. '+limit},bases,limit)
   add(audit,'assessment',{'subject_id':rid,'criteria':'original_revision/1','outcome':'reviewed_with_limits','body':decision},bases+[ev(tr,1,'Egen fullfältstabell; båda rader beskrivs i avskriftens kontext med skilda gränser.')],limit)
   add('ADOPT-T0777-C0573-'+pid,'assessment',{'subject_id':pid,'criteria':'bounded_source_adoption/1','outcome':'reviewed_with_limits','body':json.dumps({'person':pid,'name_literal':name,'occupation_literal':'Sågverksarbetare','birth_literal':birth,'status_literal':'Ogift m','family_count':'own1; no shared bracket','remaining_status_cells':'blank','final_column':'blank','scope':'s128, egen personrad, per1900-12-31','stronger_knowledge_retained':'Äldre exakta födelsedatum, föräldrar och ankomstkedja från andra poster behåller sin källgrund.'},ensure_ascii=False,indent=2)},bases+[ev(tr,1,'Egen fullfältsutvinning.'),ev(audit,1,'Avgjord källräckvidd.')],limit)
 op={'id':f'T-0777/{code}-source-candidate-v1','actor':'Codex Sol mechanical implementation of settled Astra decisions','reason':f'T-0777 AC2–4: {cid} full relevant original and bounded own-row adoption; controlled canonical-ready operation subject to independent final review.','dependencyReviewVersion':2,'changes':changes}
 p=B/f'{cid}-source-candidate-operation-v1.json';save(p.name,op)
 save(f'{cid}-first-source-candidate-freeze-v1.json',{'task':'T-0777','scope':cid,'status':'first_source_candidate_before_testing_current_consequences_still_pending','baseline_head':255,'files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},{'path':str((B/'source-review'/f'{cid}-source-v1.md').relative_to(R)),'sha256':hashlib.sha256(text.encode()).hexdigest()}]})
 print(cid,len(changes),'new source objects; no current revisions')
