import json,pathlib,hashlib,copy
B=pathlib.Path('evaluations/T-0781');D=B/'mechanical-current425-preparation-v1/full-finite-current-history-and-complete-upstream-support-native-dictionary-v1.json';d=json.loads(D.read_text());rows=[]
def get(o):return d['objects'][d['current_object_revisions'][o]]
def add(oid,values,reason,rebind=[]):
 o=get(oid);es=[]
 for f,n in values.items():
  parts=f.split('.');v=o
  for p in parts:v=v[p]
  assert v!=n,(oid,f);es.append({'field':f,'old':v,'new':n})
 rows.append({'object_id':oid,'current':o,'decision':'exact_bounded_source_field_revision','edits':es,'evidence_rebinds':rebind,'evidence_addition':{'basis_revision_id':'TR-T0781-C0049-fullpost@1','role':'supports','note':'T-0781 hela egna C0049familjeraden; samma historiska registerkälla, ingen extra oberoende identifikation eller egen födelsenotis.'},'reason':reason,'preserve':'All other complete native/API fields, disposition/evidence_status, ordered origins and evidence retained. Only explicitly listed edge replacements, in their original positions; append the specified support after retained/rebound prefix.','incoming_requirement':'Full current and all-history incoming must be individually disposed before dependent build; no automatic rebind.'})
def edge(oid,old,new):
 es=[e for e in get(oid)['evidence'] if e['basis_revision_id']==old];assert len(es)==1
 return [{'old':es[0],'new_basis_revision_id':new,'preserve_role_note_and_position':True,'source_reason':'Same source/person/role; exact newly corrected own-row fields or birth date, no new independent identity or upgraded status.'}]
for pid in ['0052','0053','0057']:
 oid=f'M-P-{pid}-C0049';vals={'data.role_literal':'D:r','caveat':'Namn och den uttryckliga rollen D:r återges från den egna C0049raden. Patronymikon och kön härleds inte som utskrivna källfält.'}
 if pid=='0057':vals['data.name_literal']='Magdalena Euphrosyne'
 add(oid,vals,'Egen dotterroll är faktiskt läst; '+('Magdalena ersätter äldre feltolkning Margareta på samma rad.' if pid=='0057' else 'Befintlig egen namnform bevaras.')+' Gamla R49@1 kvar som historiskt stöd.')
 oid=f'O-P-{pid}-C0049';o=get(oid);j=json.loads(o['data']['value_json'])
 if pid=='0057':
  lit='Magdalena Euphrosyne; 1863-05-29; B:å';j['reported_birth']='1863-05-29';j['reported_birth_place']='Bygdeå, normaliserat från egen B:å-förkortning';c='Egen C0049rad läses Magdalena Euphrosyne,1863 29/5 och B:å; äldre Margareta24/5 och påstått ditto var avläsningsfel. Egen födelsenotis är ännu inte läst. Volymperioden är inte belagd sammanhängande boendetid.'
 else:
  name,date=('Catharina Johanna','1865-05-11') if pid=='0052' else ('Anna Albertina','1871-09-28');lit=f'{name}; {date}; [egen födelseortscell blank]';j['reported_birth_place']=None;c='Egen C0049födelseortscell är blank utan belagt eget ditto; äldre Bygdeånormalisering från ditto dras tillbaka för just denna rad. Egen födelsenotis är ännu inte läst. Volymperioden är inte belagd sammanhängande boendetid.'
 add(oid,{'data.value_literal':lit,'data.value_json':json.dumps(j,ensure_ascii=False,separators=(',',':')),'caveat':c},'Explicit egenradsavskrift och rättad ortsgrund. Familj, folio, hushållsort och dotterrelation bevaras; ingen ny födelsenotis.',edge(oid,f'M-P-{pid}-C0049@1',f'M-P-{pid}-C0049@2'))
oid='O-P-0048-A-0248-child_family';o=get(oid);add(oid,{'data.value_literal':o['data']['value_literal'].replace('Margareta Euphrosyne','Magdalena Euphrosyne')},'Samma syster i samma familjerad, endast förnamnsavläsningen rättas; gamla R49@1 behålls historiskt.')
oid='F-P-0048-relation_context-64';o=get(oid);add(oid,{'data.value_json':o['data']['value_json'].replace('P-0057 Margareta Euphrosyne','P-0057 Magdalena Euphrosyne')},'Endast synlig namnform korrigeras; arkivlänkens gamla filnamn, systerrelation och tidigare relationstabellstatus bevaras. Detta uppgraderar inte P0057:s aktuella TRANSCRIBED-identitet.')
oid='F-P-0057-name_form-given';o=get(oid);add(oid,{'data.value_json':o['data']['value_json'].replace('Margareta Euphrosyne','Magdalena Euphrosyne')},'Egen förnamnsform i samma avgränsade hushåll, TRANSCRIBED består.')
oid='P-0057';o=get(oid);add(oid,{'data.display_name':'Magdalena Euphrosyne Andersdotter','rationale':o['rationale'].replace('Margareta','Magdalena')},'Visningsnamn och motsvarande sakpremiss rättas. Samma person-ID, familjerad, accepted/TRANSCRIBED, sex=null och avgränsade identitetsbedömning; inget andra individuellt personbelägg.')
oid='ID-P-0057-C0049';o=get(oid);add(oid,{'rationale':o['rationale'].replace('Margareta','Magdalena')},'Samma direkta M→P-länk; rättat namn ändrar inte accepted/TRANSCRIBED eller avgränsad identitet. Explicit M@2-bindning till samma egenrad.',edge(oid,'M-P-0057-C0049@1','M-P-0057-C0049@2'))
oid='E-birth-P-0057';o=get(oid);add(oid,{'data.date_json':o['data']['date_json'].replace('1863-05-24','1863-05-29')},'Datum rättas från senare hushållsuppgift; samma Bygdeå från egenB:å, accepted/TRANSCRIBED och caveat egen födelsenotis oläst består.')
oid='EP-E-birth-P-0057-P-0057-principal';add(oid,{},'Uttrycklig följd av E@2:s datumrättelse; P0057, principal och hela övriga metadata kvar.',edge(oid,'E-birth-P-0057@1','E-birth-P-0057@2'))
oid='F-P-0050-relation_context-P-0057';o=get(oid);add(oid,{'data.value_json':o['data']['value_json'].replace('1863-05-24','1863-05-29')},'Relationkontextens hushållsuppgivna dotterdatum rättas; ingen ny separat födelsekälla eller ändrad relation.')
x={'task':'T-0781','scope':'Fourteen exact small C0049 source-field consequences, not new person/contract approval.','source_decision_pin':{'path':str(B/'source-review/C0049-primary-settled-source-extraction-v3.json'),'sha256':'239e80e48f8a40d73d252b4309d40cb8f5d9d32e46d02ab01ce0c8008903790e'},'input_pin':{'path':str(D),'sha256':hashlib.sha256(D.read_bytes()).hexdigest()},'objects':rows,'execution_order':'R49@2 then fullTR49@1; M52/53/57@2 and E57@2 before their new O/ID/EP consumers; all other rows after fullTR.','runtime_authorized':False}
p=B/'source-review/C0049-fourteen-small-native-field-consequence-specifications-v1.json';p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(len(rows),hashlib.sha256(p.read_bytes()).hexdigest())
