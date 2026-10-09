import json,copy,sqlite3,hashlib
from pathlib import Path
D=Path('evaluations/T-0830/implementation');P=Path('evaluations/T-0830/primary');c=sqlite3.connect('file:genealogy2/data/research.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row;groups=json.load(open('evaluations/T-0830/independent/consolidated-consequence-requirements-v2.json'))['groups'];old={t['revision'].rsplit('@',1)[0]:t['full_current_native']for g in groups for t in g['targets']};changes={};retains=[];actions=[]
ex=json.load(open(P/'full-relevant-extraction-v2.json'))['units'];plan=json.load(open(P/'locked-source-plan-v2.json'));blind=json.load(open(P/'source-only-blind-manifest-v3.json'))['units'];dec=json.load(open(P/'source-decisions-v3.json'));search=json.load(open(P/'search-memory-C4-1853-v1.json'))
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def native(oid):
 if oid in old:
  o=old[oid];r=o['revision']
  if r['kind']=='record':
   o['assets']=[dict(e)for e in c.execute('select * from record_asset where revision_id=? order by rowid',(r['id'],))];o['media']=[dict(e)for e in c.execute('select * from record_media where revision_id=? order by rowid',(r['id'],))]
  return o
 r=dict(c.execute('select *from current_revision where object_id=?',(oid,)).fetchone());o={'revision':r,'data':dict(c.execute('select *from '+r['kind']+' where revision_id=?',(r['id'],)).fetchone()),'origins':[dict(e)for e in c.execute('select *from origin where revision_id=? order by rowid',(r['id'],))],'evidence':[dict(e)for e in c.execute('select *from dependency where revision_id=? order by rowid',(r['id'],))]}
 if r['kind']=='record':o.update(assets=[dict(e)for e in c.execute('select *from record_asset where revision_id=? order by rowid',(r['id'],))],media=[dict(e)for e in c.execute('select *from record_media where revision_id=? order by rowid',(r['id'],))])
 old[oid]=o;return o
def amend(oid):
 if oid in changes:return changes[oid]
 o=native(oid);r=o['revision'];data={k:json.loads(v)if k.endswith('_json')and isinstance(v,str)else v for k,v in o['data'].items()if k!='revision_id'};a={'id':oid,'kind':r['kind'],'expectedVersion':r['version'],'disposition':r['disposition'],'evidenceStatus':r['evidence_status'],'rationale':r['rationale'],'caveat':r['caveat'],'data':data,'origins':[{'unit':e['unit_id'],'coverage':e['coverage'],'note':e['note']}for e in o['origins']],'evidence':[{'object':e['basis_revision_id'].rsplit('@',1)[0],'version':int(e['basis_revision_id'].rsplit('@',1)[1]),'role':e['role'],'note':e['note']}for e in o['evidence']]}
 if r['kind']=='record':a.update(assets=[{'path':e['asset_path'],'region':e['region']}for e in o.get('assets',[])],media=[{'id':e['asset_id'],'region':e['region']}for e in o.get('media',[])])
 changes[oid]=a;return a
def setf(oid,key,value,reason):
 a=amend(oid);t=a['data']if key.startswith('data.')else a;k=key.split('.',1)[-1];before=copy.deepcopy(t[k]);t[k]=value
 if before!=value:actions.append({'object':oid,'field':key,'old':before,'new':copy.deepcopy(value),'exact_disposition':reason})
qualifications={}
def qualify(oid,key,clause,reason):
 a=amend(oid);t=a['data']if key.startswith('data.')else a;k=key.split('.',1)[-1];q=qualifications.setdefault((oid,key),{'old':t[k]or'','clauses':[]})
 if clause in q['clauses']:return
 q['clauses'].append(clause)
 setf(oid,key,'\n\n'.join(q['clauses'])+'\n\nHistorisk tidigare ordalydelse/läsomfång (ovan angivna följder ersätter endast exakt angivna frågor):\n'+q['old'],reason)
def support(oid,bid,v,note,role='supports'):
 a=amend(oid)
 if any(e['object']==bid and e['version']==v and e['role']==role for e in a['evidence']):return
 a['evidence'].append({'object':bid,'version':v,'role':role,'note':note})
def new(oid,kind,data,ev,caveat='',status=None,disposition='recorded'):
 assert oid not in changes and not c.execute('select 1 from object where id=?',(oid,)).fetchone();changes[oid]={'id':oid,'kind':kind,'expectedVersion':None,'disposition':disposition,'evidenceStatus':status,'rationale':'T-0830 bounded sexkällescope: fem egna original faktiskt lästa/oberoendeprövade; sjätte endast åtkomsthinder. Source-decisions-v3/extraction-v2, exakt accepterat återbruk och individuella konsekvenser; ingen ny oberoende röst antas.','caveat':caveat,'data':data,'origins':[],'evidence':ev}
def edge(oid,v,note,role='supports'):return {'object':oid,'version':v,'role':role,'note':note}
# Exact two media recipes; no stage or live registration here.
receipts=json.load(open(P/'exact-two-fetch-receipts-v1.json'));media=[]
for b in blind[:2]:
 r=next(z for z in receipts if z['image_id']==b['image_id']);assert H(b['path'])==b['sha256'];m={'id':'M-'+b['sha256'],'storagePath':'genealogy2/media/objects/'+b['sha256'],'sha256':b['sha256'],'bytes':b['bytes'],'originalName':Path(b['path']).name,'provenance':'T0830 Riksarkivet full original image; actualretrieval '+r['requested_at']+'; provider_version unknown; source '+b['source_id']};media.append({'input':str(Path(b['path']).resolve()),'planned':m})
(D/'media-stage-plan-v1.json').write_text(json.dumps(media,ensure_ascii=False,indent=2)+'\n')
copy134='T-0830, 2026-10-09: Anna Christina P-0134:s exakta två kopior C0005634_00013 (C/5 egen1852post) och C0005633_00014 (C/4 kontroller) är nu fullbevarade och relevanta egna fält prövade. Den tidigare tvåkopieskulden är sluten genom exakt kontrollerad mediaregistrering. Parallella C/4 och C/5 är samma registreringskedja, inte två oberoende händelsebelägg. Övriga äldre råreservationer och PK/LIFE-omfång består.'
boundary='T-0830 aktuell C/4-bild14-kontroll: 1853 års högersida har exakt21 visade poster från född17januari/döpt23januari till född12november/döpt20november. Ingen målpost för Lars Eric/Erik Jansson och Brita Christina Ersdotter där; ingen helårsnoll/hela församlingens frånvaro följer. Annan Anna Christina9/15maj med Johanna Jonsdotter vid Stäringe är skild från P0134; Kallviksposten Augusta Mathilda9/16oktober/JohanErsson/EvaLottaAndersdotter är endast ortkontroll. Gamla negativa kvitton förblir oförändrade; SEARCH-T0830-P0134-C0005633-00014-1853-parentpair@1 anger denna nya exakta passage.'
own316='T-0830, 2026-10-09: Cajsa Märta P-0316:s egna C0436/C0437/C0512-rader är fullfältsprövade med rubriker, ditton, blanker, marginaler och årsfält. Prövade svårtydda tecken behåller råreservationer, inga moderniserade förmågegrader eller obrutna vistelser härleds. T0812:s redan accepterade C0274-fullpost och T0136/T0110:s accepterade C0510-rad återbrukas. Andra personers egna olästa fält/fullT0420scope består.'
marriage='Aktuell källprecision: C0511 anger lysning1858-02-21. C0512 har eget gift-ditto under rå58 21/2; C0510:s accepterade aktuella råfält är58/59[?]26/3 (registered_marriage:null). Det är olika registerfält, inte två oberoende samstämmiga vigseldatum. Faktisk vigseldag är okänd; accepterad make-/vuxen-/nedåtkedja består.'
copy316='P-0316:s PK11 är EJ STYRKT på faktisk egen C0984/IndalF2(1895–1920)/1901post10/00199095_00032-kopieskuld. Auktoriserat sjätteoriginalförsök gav HTTP401 och exakt root-bildvisare gick till login; ingen originalbild läst, ingen söknoll. death_source_copy_missing:true består och native identity failed/tree waiting. Bara samma egenbild får återupptas efter åtkomst; makens1904bild50 ingår inte. Ingen LIFE/fullkontraktsPASS.'
witness='Aktuellt egenC5-fält: modern33; rå18/4 bevaras med äldre accepterad kyrktagningsfunktion skild från tryckt rubrik (ingen separat kyrktagningsrubrik). Vittnen Arrendat.And.Nilson/Nilsson, hu.A.[S/L?]G[ill/uit?]man, dr.A.[J/F?].Nilson/Nilsson, Pig.[A/C?].Br.Jonsdotter, alla iMåna[d?]. Inga initialer/orter/personidentiteter expanderas. Egen post/folio29 finns inte; tidigare terminal29 är avskriftsfel.'
for g in groups:
 gid=g['group']
 for t in g['targets']:
  oid=t['revision'].rsplit('@',1)[0]
  if gid.startswith('G12'):
   retains.append({'object':oid,'group':gid,'disposition':g['decision'],'full_old_native':t['full_current_native']});continue
  a=amend(oid)
  if gid.startswith('G01'):qualify(oid,'caveat',copy134,g['decision'])
  elif gid.startswith('G02'):
   qualify(oid,'caveat',own316,g['decision'])
   k='body'if'body'in a['data']else'markdown'if'markdown'in a['data']else None
   if k:qualify(oid,'data.'+k,own316,g['decision'])
  elif gid.startswith('G03'):
   qualify(oid,'caveat',copy134+' '+boundary,g['decision'])
   k='body'if'body'in a['data']else'markdown'if'markdown'in a['data']else None
   if k:qualify(oid,'data.'+k,copy134+' '+boundary,g['decision'])
  elif gid.startswith('G04'):
   qualify(oid,'caveat',own316+' '+copy316,g['decision'])
   k='body'if'body'in a['data']else'markdown'if'markdown'in a['data']else None
   if k:qualify(oid,'data.'+k,own316+' '+copy316,g['decision'])
  elif gid.startswith('G05'):qualify(oid,'caveat',own316+' '+copy316,g['decision'])
  elif gid.startswith('G06'):qualify(oid,'caveat',own316+' Råroll från just denna rad hålls skild från släktskapsinferens; egen identity accepted består.',g['decision'])
  elif gid.startswith('G07'):
   for k in ['caveat','data.body']:qualify(oid,k,marriage,g['decision'])
  elif gid.startswith('G08'):
   rid=a['data'].get('record_id',oid if a['kind']=='record'else a['data'].get('subject_id'));u=next((u for u in ex if rid in [s.rsplit('@',1)[0]for s in ([u['record']]if'record'in u else u.get('records',[]))]),None);assert u,oid
   clause=copy134+' '+boundary+' '+witness if u['unit']==1 else boundary if u['unit']==2 else own316+' Egen fullfältkarta/årskarta finns i TR-T0830-unit-'+str(u['unit'])+'@1.'
   if u['unit']==4:clause+=' Accepterat T0134/C1012 reserverar yngre Anders Olofs hushållsmånad; äldre säker april/augusti-konflikt är supersederad, ingen ny augustinormalisering.'
   if u['unit']==5:clause+=' '+marriage+' Endast Cajsa Märta-raden har fullprövats; NilsPetter65 28/11 och Katarina25/8[?] är separat kontext, ingen full sidopersonsprövning.'
   qualify(oid,'caveat',clause,g['decision'])
   if a['kind']=='transcription':
    qualify(oid,'data.reading_note',clause,g['decision']);qualify(oid,'data.text','Aktuell källbunden rättelse (äldre avskrift följer som historik): '+clause,g['decision'])
   elif a['kind']=='assessment':qualify(oid,'data.body',clause,g['decision'])
  elif gid.startswith('G09'):
   # R93d is unrelated correctedhousehold without currentcopy claim; retain its exact stronger metadata.
   if oid=='R-93d05ed3817c5615beff49df':retains.append({'object':oid,'group':gid,'disposition':'Current fullcaveat contains noC1041copydebt/whole1853claim; retain source-specific family/dräng corrections.', 'full_old_native':t['full_current_native']});changes.pop(oid,None);continue
   clause=copy134+' '+boundary
   if oid=='RESEARCH-P-0214-9d76f0343410':clause='P-0214:s dotter Anna Christina P-0134:s C/5-bild13 och C/4-bild14 är nu bevarade/prövade. '+boundary+' P0214:s egen kandidat-/ursprungsfråga och granskningsutfall ändras inte.'
   qualify(oid,'caveat',clause,g['decision'])
   for k in ['body','description','reading_note']:
    if k in a['data']:qualify(oid,'data.'+k,clause,g['decision'])
  elif gid.startswith('G10'):qualify(oid,'caveat',boundary if'1853'in oid or'Kallvik'in oid else witness if'C5-birth'in oid else copy134+' C5bild12egenavgränsning19mars återbrukad; denna föregående bild är inte nyöppnad.',g['decision'])
  elif gid.startswith('G11'):qualify(oid,'caveat',witness,g['decision'])
  elif gid.startswith('G13'):qualify(oid,'caveat',copy134 if'C5'in oid else boundary+' Bild14 nu bevarad, egen kontrollpost prövad; separat råroll tom bevaras.',g['decision'])
# Record preservation and full six record representations; onlytwo newmedia, archivedlocal3 retained.
for u,b in zip(ex,blind[:5]):
 recs=[u['record']]if'record'in u else u['records'];ev=[]
 for rv in recs:
  oid=rv.rsplit('@',1)[0];a=amend(oid)
  if u['unit']<=2:
   mid=media[u['unit']-1]['planned']['id'];a['media'].append({'id':mid,'region':None})
  ev.append(edge(oid,2,'Exakt eget record/fullkopia enligt sourceplan, samma registreringskedja; inga oberoende extra röster.'))
 audit='AUDIT-T0830-unit-'+str(u['unit']);body={'source_unit':u,'source_copy':{'path':b['path'],'sha256':b['sha256'],'bytes':b['bytes'],'image_id':b['image_id'],'source_revision_at_read':b['source_id'],'provider_version':'unknown'},'limits':'Endast exakt målrad/relevant kontroll; prövade reservationer, andra personers fullrest oförändrad.'}
 new(audit,'assessment',{'subject_id':recs[0].split('@')[0],'criteria':'source_extraction/1','outcome':'TESTED_SOURCE_BOUND','body':json.dumps(body,ensure_ascii=False,indent=2)},ev,'Full relevant extraction afterprimary+independentoriginal-first; source-unread unit6 excluded.')
 for j,rv in enumerate(recs):
  tr='TR-T0830-unit-'+str(u['unit'])+('-Kallvik'if j else'');new(tr,'transcription',{'record_id':rv.split('@')[0],'text':json.dumps(u,ensure_ascii=False,indent=2),'reading_note':'Primär full relevant extraktionv2 och separat original-först jämförelse; exakt målrad/kontroll, inga utvidgade namn eller egenfält för oöppnade sidopersoner.'},[edge(rv.split('@')[0],2,'Versionsbunden exakt recordrepresentation, samma underliggandeoriginal.')],witness if u['unit']==1 else boundary if u['unit']==2 else own316,status='TRANSCRIBED')
# Exact typed fields, retained all other keys.
for oid,u in [('O-P-0316-C0436-childhood',ex[2]),('O-P-0316-C0437-childhood',ex[3]),('O-P-0316-C0512-household',ex[4])]:
 a=amend(oid);v=copy.deepcopy(a['data']['value_json']);flag='own_remaining_columns_extracted'if u['unit']==5 else'own_knowledge_communion_notes_extracted';assert v[flag]is False;v[flag]=True;v['own_full_fields']=u['own_fields'];v['own_headers']=u['headers'];v['own_annual_fields']=u['annual_fields'];v['own_read_limits']=u.get('annual_limit',u.get('right_annotation','Prövade reservationer, ingen moderniserad förmågegrad.'));setf(oid,'data.value_json',v,'G05 exactownsourcefieldmap');setf(oid,'data.value_literal',json.dumps(v,ensure_ascii=False),'G05 structured currentownfullfields; olderliteral originalrevision retained');support(oid,'AUDIT-T0830-unit-'+str(u['unit']),1,'Exaktfullprövad egenrad, andra personers fält inte härledda.')
f='F-P-0316-source_assessment-own-fields-and-limits';v=copy.deepcopy(amend(f)['data']['value_json']);assert v['own_AI12_columns']=='outvunna'and v['own_childhood_columns']=='outvunna';v['own_AI12_columns']='fullfältprövade T0830 med TESTED_RESERVED år/tecken';v['own_childhood_columns']='fullfältprövade T0830 C0436/C0437, råkartor bevarade';v['own_AI8_columns']='accepterad full relevant egenfamiljerad T0136/C0510, med T0110:s senare58/59[?]26/3-rättelse och råreservation';v['own_C0436_full_fields']=ex[2];v['own_C0437_full_fields']=ex[3];v['own_C0512_full_fields']=ex[4];setf(f,'data.value_json',v,'ExactG05 only settledownflags; deathcopy/fullcontract/others retained')
for u in [3,4,5]:support(f,'AUDIT-T0830-unit-'+str(u),1,'Egenfält/fullkartor, inga fullfamiljgrindar.')
support(f,'R-b4d2026f0cdd001da7dfedde',2,'AccepteratT0136/T0110 aktuellt C0510fullrow; no neworiginalread.')
for cid in ['C0436-childhood','C0437-childhood','C0512-household']:
 oid='M-P-0316-'+cid;setf(oid,'data.role_literal','Hu.'if cid.startswith('C0512')else'D:r','ExactG06rawroleonly')
 if cid.startswith('C0512'):setf(oid,'data.name_literal','Dalsten, Kajsa Märta','Source-specificrawDalsten; no global spellingharmonization')
# TypedC5 terminal and twocontrolrows.
o='O-P-0134-C1041-C5-birth';v=copy.deepcopy(amend(o)['data']['value_json']);assert v['reference']=='29';v['reference']=None;v['mother_churching_raw']='18/4';v['mother_churching_function']='Äldre accepterad kyrktagningstolkning; ingen separat tryckt rubrik';v['own_full_fields']=ex[0]['own_fields'];v['own_headers']=ex[0]['headers'];setf(o,'data.value_json',v,'G10 exactterminal29withdrawn,33/raw18/4 reservedfunction');support(o,'AUDIT-T0830-unit-1',1,'Egenfullpost och terminal29rättelse.')
o='O-P-0134-C1041-Anna-Christina1853';v=copy.deepcopy(amend(o)['data']['value_json']);v['baptized']='1853-05-15';v['father_named']=False;v['own_control_record']=ex[1]['own_control_records'][0];setf(o,'data.value_json',v,'Owncontrol nottarget/no newperson');support(o,'AUDIT-T0830-unit-2',1,'Exakt skild AnnaChristina1853egenkontroll.')
o='O-P-0134-C1041-Kallvik-control';v=copy.deepcopy(amend(o)['data']['value_json']);v['born']='1853-10-09';v['baptized']='1853-10-16';v['own_control_record']=ex[1]['own_control_records'][1];setf(o,'data.value_json',v,'Exact positiveplacecontrol/no relationship');support(o,'AUDIT-T0830-unit-2',1,'Exakt Kallvikskontrollpost.')
# Sourcewitnessliteral/rawonly; no witnessendpoint.
for suffix,name in [('ABr-Jonsdotter','[A/C?]. Br. Jonsdotter'),('AJ-Nilsson','A. [J/F?]. Nilson/Nilsson'),('AS-Gillman','A. [S/L?] G[ill/uit?]man'),('And-Nilsson','And. Nilson/Nilsson')]:
 setf('M-C1041-witness-'+suffix,'data.name_literal',name,'G11 exactsharedreservation not expandedperson');o='O-P-0134-C1041-witness-'+suffix+'-home';setf(o,'data.value_literal','alla i Måna[d?]','G11 rawplace endingqualified');setf(o,'data.value_json','Måna[d?]','G11 no normalizedplace');support(o,'AUDIT-T0830-unit-1',1,'Exactcurrent witness/source role reservation, no person-ID.')
# Current person and applicable exact outcomes.
setf('P-0316','data.display_name','Cajsa Märta Dahlsten/Dalsten','Sharedsourceauthorization removes rejectedAndersdottertranscription')
for pid,pk,result,clause in [('0134','11','STYRKT',copy134),('0134','12','STYRKT','Daterad T0830 native identitetsgranskning passerar de sju kriterierna; fullkontrakt/LIFE fortfarande separat underkänt på tidigarePK03/08, T0270 och analogt ekonomimaterial kvar.'),('0316','04','STYRKT','Endaaktuella C0274vittnesskulden är redan fullt sluten av accepteratT0812fullpost: sju namngivna och tre onamngivna hustrur, moder28/kyrktagning27/7. Ingen LIFEpass.'),('0316','05','STYRKT',own316),('0316','11','EJ STYRKT',copy316),('0316','12','STYRKT',own316+' '+copy316)]:
 oid='CONTRACT-P-'+pid+'-PK-'+pk;setf(oid,'data.outcome',result,'Exactsourcev3 individual criteriondisposition');qualify(oid,'data.body',clause,'Exactcriterionclosure/residualsourcebounds')
 if pid=='0134':
  for u in [1,2]:support(oid,'AUDIT-T0830-unit-'+str(u),1,'Exact2copierestore/fullread, full LIFE unaffected.')
 elif pk=='04':support(oid,'TR-T0812-C0274-full-own-post',1,'Acceptedexactownsonpost24/witnessclosure; no newreading.')
 elif pk=='05':
  for u in [3,4,5]:support(oid,'AUDIT-T0830-unit-'+str(u),1,'Exact remainingthreeownrowclosure.')
  support(oid,'TR-T0812-C0274-full-own-post',1,'Acceptedearlierownsonpostfullread reused.')
 else:support(oid,'R-a4ae494d9c4204cc992500c0',1,'Knownpositiveownrecordrepresentation withoutrequiredlocalcopy; actualmissingcopy retained.',role='context')
setf('PATH-P-0134-KP-02','data.outcome','UTFÖRD OCH POSITIV; exaktaC5bild13/C4bild14kopior bevarade/fullprövade;1853kontroll gäller endast21visadeposter17Jan–12Nov/dop20Nov, ingenhelårsnoll.','Exactsourcev3/pathcurrentoutcome')
setf('PATH-P-0316-KP-05','data.outcome','UTFÖRD: exaktC0436/C0437/C0512egenfullfältprövning samtaccepteratT0812C0274; råreservationer består, annanperson/LIFE/copieskuld ejstängd.','Exactownextractionpathclosure')
setf('P-0316/Q-03','data.outcome','FASTSTÄLLD INOM EXAKT UTDRAGSFRÅGA; tre egna rader och tidigareC0274slutna, PK11C0984kopieskuld består.','Originalquestionactualownextractionclosureonly')
# One new immutable exactcurrentnegative; historicalreceipt notchanged.
new(search['search_id'],'search',{'question_id':'P-0134/Q-01','source_id':'S-0121','scope_json':search,'outcome':'negative','body':boundary+'\n\n'+json.dumps(search,ensure_ascii=False,indent=2)},[edge('S-0121',2,'Actualread source@1 preserved in memory; exact same correctedsourcehead@2 currentscope amendment, provider_version unknown.',role='derived_from'),edge('R-ab67d38b58e92a0c9b0329d2',2,'PositiveotherAnna control scope; nottargetidentity.'),edge('R-f9c30454d2afaad13941d205',2,'ExactKallvikpositiveplacecontrol scope; no genealogicaledge.')],boundary,status='TRANSCRIBED',disposition='accepted')
# Newnative reviews; noneexisted in currentgates. Underlyingacceptedsource+childchain, no person→reviewedge.
for ind in dec['individuals']:
 pid=ind['person'];suffix=pid.replace('P-','');identity='IDENTITY-REVIEW-T0830-'+suffix;tree='TREE-EFFECT-T0830-'+suffix
 if pid=='P-0134':basis=[('R-2c30f50bb85f191a282e6867',2),('R-d6ef52c986e2385ad3234a8b',2),('R-f13f82e65ef02371b3f59ceb',1),('R-8f2cc100133f10fe29bd5472',1),('R-1373b148c368836c5dbb5db3',1),('R-93d05ed3817c5615beff49df',1),('REL-parent-P-0134-P-0015',1),('AUDIT-T0830-unit-1',1),('AUDIT-T0830-unit-2',1)]
 else:basis=[('R-c77371fa1e3e588edfc2a685',1),('R-70588c1ff1abe62626d3ecb1',1),('R-b4d2026f0cdd001da7dfedde',2),('R-6f3dead04f730b5ad91e48bb',2),('TR-T0812-C0274-full-own-post',1),('REL-parent-P-0316-P-0254',1),('AUDIT-T0830-unit-3',1),('AUDIT-T0830-unit-4',1),('AUDIT-T0830-unit-5',1)]
 b=json.dumps({'dated_review':'2026-10-09','source_dispositions':ind,'source_authorities':{'primary':'source-decisions-v3','independent':'source-concurrence-and-waiting-candidate-v1/consolidated-v2'},'life_scope':'Identitylevelonly; legacyfullcontract andLIFE remainindependent, oldoutcomes preserved.'},ensure_ascii=False,indent=2)
 new(identity,'assessment',{'subject_id':pid,'criteria':'identity_review/1','outcome':ind['proposed_identity_review'],'body':b},[edge(oid,v,'Exactacceptedown/adult/descendantchain or individuallytestedsource; no extraindependentvote.')for oid,v in basis],copy134 if pid=='P-0134'else copy316)
 new(tree,'assessment',{'subject_id':pid,'criteria':'tree_effect/1','outcome':ind['proposed_tree_effect'],'body':('P0134 identitylevelpassed/supporting; acceptedP0134→P0015recorded_parent unchanged; life separate.'if pid=='P-0134'else'P0316 identifiedadult/mother andacceptedP0316→P0254recorded_parent unchanged; nativefailed/waiting solelyactualmandatoryownC0984copydebt, not unidentifiedperson or LIFEwaiver.')},[edge(identity,1,'Exactresultingdatedindividual nativeidentityreview, scope asstated; no rivalcurrent review.')])
 for oid in [pid,'ASSESSMENT-'+pid,'RESEARCH-'+pid+'-9d76f0343410']:
  clause=('Aktuell T0830 identitetsnivå GODKÄND/BÄRANDE enligt '+identity+'@1/'+tree+'@1; de sju kriterierna prövade med exaktpositiv1852-/vuxen-/sonkedja och sluten tvåkopieskuld. FulllegacykontraktsUNDERKÄND och LIFE/PK03/08 består.'if pid=='P-0134'else'Aktuell T0830 identitetsnivå UNDERKÄND/AVVAKTAR enligt '+identity+'@1/'+tree+'@1 endastpåfaktiskPK11C0984egenkopieskuld. PK04/PK05slutna; Cajsa MärtaDahlsten/Dalsten är identifierad mor, Andersdotter äldreavvisadtranscription; fullLIFE/rest kvar.')
  qualify(oid,'caveat',clause,'Exactcurrentreadview identityvslegacyfulllevel')
  if'body'in amend(oid)['data']:qualify(oid,'data.body',clause,'Exactcurrentown identitysection adoption')
# Actualchangedmethods only, preserve full oldmethod history; audit added only non-source/record endpoints toavoidcycle.
for oid,a in list(changes.items()):
 if a['expectedVersion']is not None:qualify(oid,'rationale','T-0830 aktuell metod: ny full egen källprövning eller dess exakt nödvändiga metadata-/råfältsföljd enligt sourcev3/independent13grupper; accepteratT0812/T0136/T0110 återbrukas utan omläsning. Äldre metod/provenans bevaras nedan.','Currentmethodsactualfiveoriginalwork, olderorigins retained')
# Complete126targetmapping includingretains and zero/multimatch discoveredexplicitly.
op={'id':'T-0830/five-read-blocked-sixth-source-consequences-v1','actor':'Codex mechanical / primary+independent Astra settled sourcev3','reason':'T0830AC1–5partial exact6union: fiveoriginals read/twoimmutablecopies/threearchivedreuse, P0134identityonlypassed, P0316failedPK11unit6HTTP401; append-onlyhistory/45OWNER/oldfullscope andindividualsourceconsequences.','dependencyReviewVersion':2,'media':[m['planned']for m in media],'changes':list(changes.values())}
p=D/'operation-candidate-v2-unbound.json';p.write_text(json.dumps(op,ensure_ascii=False,indent=2)+'\n');(D/'individual-transform-consequences-v2.json').write_text(json.dumps(actions,ensure_ascii=False,indent=2)+'\n');(D/'individual-retains-v2.json').write_text(json.dumps(retains,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'changes':len(changes),'retains':len(retains),'sha256':H(p)}))
