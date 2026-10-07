import json, hashlib, copy
from pathlib import Path
B=Path('evaluations/T-0784'); O=B/'source-review'; P=B/'mechanical-current442-preparation-v2'
def load(p): return json.loads(Path(p).read_text())
def pin(p): return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def save(name,data):
 p=O/name; assert not p.exists(); p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(pin(p))); return pin(p)
oldpath=O/'primary-current-21-individual-requirement-and-three-outcome-freeze-v1.json'
old=load(oldpath); new=copy.deepcopy(old)
D=load(P/'complete-three-current-history-upstream-native-dictionary-v1.json')['objects']
amendments=[]
for row in new['individual_21']:
 if row['person']=='P-0007' and row['requirement'] in ['PK-05','PK-11','PK-12']:
  before=row['source_bound_reason']
  if row['requirement']=='PK-11':
   row['source_bound_reason']=before.replace('Helgesta fol744 rad10','Flen A II a/7 c fol744 rad10')+' Den relevanta användningen är explicit i RESEARCH-P-0007-9d76f0343410@3: fol744:s utskrivna gemensamma föräldrar bär den aktuella helsysterslutsatsen, medan932 har en upprepningsbunden not. Det är proveniensen för detta redan åberopade familjebelägg som saknas, inte ett krav att först göra systerns fristående livs- eller födelseforskning.'
  elif row['requirement']=='PK-05':
   row['source_bound_reason']=before+' Därtill återstår egna kolumner9–13 på systerns redan åberopade Flen A II a/7 c fol744 rad10 enligt R-ab847c1960d02f28801419b3@1. Denna målrad används i Majs aktuella identitetsargument för gemensamma föräldrar; relevanta personer i redan använda målposter omfattas av PK05. T0377 äger fullradens kvarvarande utvinning efter T0237:s bevarande, samordnat till en passage. Detta utvidgas inte till andra folier, systerns olästa egen födelsepost eller hela hennes liv.'
  else:
   row['source_bound_reason']=before.replace('relevant C0973/744-proveniens hos T0237','relevant C0973/Flen744-proveniens hos T0237 och full relevant egen744rad10 hos T0377')
  amendments.append({'person':row['person'],'requirement':row['requirement'],'old_reason':before,'new_reason':row['source_bound_reason'],'grade_unchanged':True})
new['supersedes_only_named_reason_clauses']=pin(oldpath)
new['root_AC1_release_pin']=pin(B/'root-AC1-current-baseline-and-receipt-lock-release-v1.json')
new['amendment_basis']={'record':'R-ab847c1960d02f28801419b3@1','current_argument':'RESEARCH-P-0007-9d76f0343410@3','whole_existing_task_log_pin':pin('wotan/dev-log/T-0377.md'),'scope':'Exact place and already-used row/field scope only; all21 grades, everyold nativepayload and everyother reason unchanged.'}
amendpin=save('primary-exact-Flen744-place-and-used-row-scope-amendment-v1.json',{'initial_freeze_pin':pin(oldpath),'amendments':amendments,'basis':new['amendment_basis'],'new_original_read':False,'independent_T0784_exposure':False})
newpin=save('primary-current-21-individual-requirement-and-three-outcome-freeze-v2.json',new)

def edge(rev,role,note):
 object_id,version=rev.rsplit('@',1); return {'object':object_id,'version':int(version),'role':role,'note':note}
def APIfromNative(v):
 data=copy.deepcopy(v['data']); data.pop('revision_id',None)
 a={'id':v['object_id'],'kind':v['kind'],'expectedVersion':v['version'],'data':data,'origins':[{'unit':r['unit_id'],'coverage':r['coverage'],'note':r['note']} for r in v['origins']],'evidence':[edge(r['basis_revision_id'],r['role'],r['note']) for r in v['evidence']],'disposition':v['disposition'],'evidenceStatus':v['evidence_status'],'rationale':v['rationale'],'caveat':v['caveat']}
 return a
specs=[]
person_rows={p:[r for r in new['individual_21'] if r['person']==p] for p in new['scope_person_ids']}
for p,rows in person_rows.items():
 compact=p.replace('-',''); outcome=new['person_outcomes'][p]
 identity_id='ASSESSMENT-T0784-'+compact+'-identity'
 tree_id='ASSESSMENT-T0784-'+compact+'-tree'
 current_legacy='ASSESSMENT-'+p
 common_caveat='Ingen ny original- eller extern källäsning i T0784. Bedömningen gäller endast identitetsnivåns sju krav och bärande relationer; livsbilden, tidigare fullkontraktsgranskningar och alla historiska versioner bevaras. Tillräckligt tidigare arbete återbrukas med sina råreservationer och beroenden. Wotan ensam äger utförande och prioritet.'
 body='T-0784, individuell identitetsgranskning 2026-10-05.\n\nAktuellt utfall: '+outcome['identity_review']+'. Sakligt etablerad personidentitet skiljs från fullgjord identitetsgrind. Denna native identity_review/1 ersätter den äldre legacygranskningens verkan på aktuell identitetsaxel, utan att skriva om dess historiska utfall eller skapa en livsbildsgranskning. Den utgör också avgränsad native adoption av de nedan individuellt prövade aktuella forskningskraven.\n\n'
 body+='\n\n'.join(r['requirement']+' — '+r['grade']+'. '+r['source_bound_reason'] for r in rows)
 refs=[]
 for r in rows: refs.append(edge(r['current_revision_id'],'context','Hela aktuella legacykravet, inklusive historiskt utfall och förbehåll, individuellt läst. Det nya utfallet följer denna prövning; det är inte en automatisk konvertering.'))
 for rev in rows[0]['support_revision_ids']:
  refs.append(edge(rev,'supports','Versionsbundet befintligt underlag inom de namngivna person-/fältgränserna i denna bedömning. Samma historiska uppgiftskedja räknas inte som en ny oberoende röst.'))
 if p=='P-0007':
  refs += [edge('KEY-P-0007-bf37119ff18f@2','supports','Samma paket: exakt rättad datum-/årsräckvidd, ingen ny personuppgift.'),edge('PATH-P-0007-KP-05@2','supports','Samma paket: avgränsad oläst passage och åtkomst; inga källresultat eller åtkomstlöften.')]
 api={'id':identity_id,'kind':'assessment','expectedVersion':0,'data':{'subject_id':p,'criteria':'identity_review/1','outcome':outcome['identity_review'],'body':body},'origins':[],'evidence':refs,'disposition':'recorded','evidenceStatus':None,'rationale':'T-0784: individuell aktuell omprövning av PK01/02/05/07/09/11/12 mot hela aktuella krav, bärande relationer, accepterat tidigare källarbete och exakta kvarstående gränser. Ingen automatisk legacyuppgradering.','caveat':common_caveat}
 specs.append({'object_id':identity_id,'action':'new','expected_absent':True,'full_new_API':api,'source_row_pointers':[{'file':newpin,'pointer':'/individual_21/'+str(new['individual_21'].index(r))} for r in rows],'native_identity_or_relation_change':False})
 if outcome['tree_effect']=='supporting':
  treebody='T-0784, trädverkan 2026-10-05: BÄRANDE. Den nya individuella identity_review/1 är passed efter full prövning av alla sju identitetskrav. Befintliga accepterade person- och föräldrarelationer bär passage genom Evy; inga nya anor, familjekanter eller bevisstatusar skapas. C0935:s rånamn/dag normaliseras inte till C0240:s datum. Den gamla AVVAKTAR-bedömningen bevaras som historik; privat livsbild och andra familjepassager är inte här godkända.'
 else:
  treebody='T-0784, trädverkan 2026-10-05: AVVAKTAR. Personkorrelationen och befintliga accepterade relationer består, men identity_review/1 är failed på '+', '.join(outcome['failed_requirements'])+'. Antavlan får därför inte passera denna person som identitetsgodkänd. Det innebär ingen ny tvist eller demotion av de accepterade relationerna. De exakta kvarvarande passagerna, ägarna och återaktiveringsvillkoren finns i den samtidigt versionsbundna identitetsgranskningen. Äldre livsbilds- och fullkontraktsutfall bevaras.'
  if p=='P-0003': treebody+=' Bernhards OWNER_CONFIRMED faderskap kvarstår oförändrat; den aktuella väntan kräver inget nytt fadersbevis.'
 tree={'id':tree_id,'kind':'assessment','expectedVersion':0,'data':{'subject_id':p,'criteria':'tree_effect/1','outcome':outcome['tree_effect'],'body':treebody},'origins':[],'evidence':[edge(identity_id+'@1','supports','Samma pakets individuella aktuella identitetsprövning; trädverkan följer dess sakliga kravutfall, inte personens äldre arbetsstatus.')],'disposition':'recorded','evidenceStatus':None,'rationale':'T-0784: separat trädverkan härledd från den nya individuella identitetsgranskningen; inga nya person- eller relationsbeslut.','caveat':common_caveat}
 specs.append({'object_id':tree_id,'action':'new','expected_absent':True,'full_new_API':tree,'source_row_pointers':[{'file':newpin,'pointer':'/person_outcomes/'+p}],'native_identity_or_relation_change':False})

key=D['KEY-P-0007-bf37119ff18f@1']; ka=APIfromNative(key)
ka['data']['body']=key['data']['body'].replace('Säker; datumet upprepas i sju poster.','Säker personnyckel i den prövade kedjan av sju korrelerade poster. C-0019 anger endast födelseår; exakt datum och övriga personuppgifter stöds av de andra egna posterna. Antalet poster är inte antalet oberoende datumvittnen.')
assert ka['data']['body']!=key['data']['body']
ka['evidence'].append(edge('CONTRACT-P-0007-PK-01@2','supports','T0677:s redan accepterade C0019-räckvidd: endast födelseår i denna post, övriga egna poster bär exakt datum.'))
specs.append({'object_id':key['object_id'],'action':'revise','whole_old_native':key,'full_old_API':APIfromNative(key),'full_new_API':ka,'exact_changes':[{'field':'data.body','old':key['data']['body'],'new':ka['data']['body']}],'evidence_action':'Append the one specified current support edge; preserve existing order and all other fields.','source_disposition':'Nödvändig aktuell kopierättelse för PK07; ingen ny källa, datumändring eller identitetsändring.','incoming_disposition':'Requires exact all-history incoming inventory before build. No automatic dependent rebind.'})
path=D['PATH-P-0007-KP-05@1']; pa=APIfromNative(path)
pa['data']['body']='''### KP-05: Södertäljes församlingsbok uppslag 15 och hennes egna mantalsrader 1945–1946

- Frågor/teman: Q-02, Q-04, BO, REL, ARB.
- Källklass: K-01, K-10.
- Tid/plats och arkivbildare: Södertälje kyrkoarkiv SE/SSA/1572. Inflyttningsposten1943 hänvisar till församlingsbok uppslag15; exakt volym och egen familjerad är ännu inte fastställda genom läsning. S-0689:s tidigare katalogkontroll anger AIIa77–116(1936–1961) som inte digitaliserade; det är en annan åtkomstgren än mantalsregistren AIIc/33(1945) och AIIc/34(1946).
- Förväntad information: den hänvisade familjeraden kan ge egna person-/familjeställningsfält, in-/överföringar och fortsättning. Majs egna mantalsrader kan ge den egna namnformen och distrikt/fastighet. Innehåll, träff och personkorrelation är oprövade; tom yrkescell är ingen ny yrkesuppgift eller livslång negativ slutsats. Barnuppgifter minimeras till nödvändig relation.
- Ingång och söknycklar: uppslag15 i C0882, Södertälje BI/11 s279 nr132, Arne Godvig1943-11-24; postens hushållssummor namnger inte Maj eller barnen. Maj korreleras genom den redan prövade egna familjekedjan. Egna nycklar är Jansson May Amalia1920-05-11, Mejseln3 och Gondolen2. C0883 anger hennes egen1944rad, men1945s96 och1946s104 är Arnes sidor och får inte betecknas som lokaliserade egna Maj-rader.
- Beroenden och åtkomst: uppslag15 kräver först exakt volym-/åtkomstprövning inom den ovan angivna analoga källgrenen. För1945–1946 krävs lokalisering av hennes egna rader i de angivna AIIc-volymerna. Den historiska inloggade läsningen2026-09-05 av andra egna poster bevisar inte åtkomst eller innehåll i dessa återstående passager. En inloggning ensam löser inte uppslag15; ingen ny åtkomstkontroll har gjorts i T0784 och inga alternativ förklaras uttömda.
- Föregående källvägar: KP-01.
- Undersökt omfång och utfall: EJ UNDERSÖKT för uppslag15 och Majs egna1945–1946-rader. Arnes redan lästa årsregisterrader och Majs egen1944rad återbrukas med sina egna fältgränser; samma administrativa kedja är inte flera oberoende röster.
- Bedömning och återaktivering: den uttryckliga uppslagshänvisningen och kvarvarande egna registerrader hålls som precis utvinningsrest. T0379 är befintlig avgränsad ägare. Uppslag15 undersöks högst en gång för de gemensamt relevanta Arne-/Maj-följderna; Arnes T0227 behåller sitt övriga omfång. Nytt utförande, arkivkontakt eller beställning följer Wotans beslut och kräver eget mandat; T0784 gör endast aktuell käll-/kravbedömning.
'''
for rev,note in [('S-0689@1','Daterad katalog-/åtkomstskillnad AIIa och AIIc, inte läst personpost eller uttömda alternativ.'),('R-18122baf2db2f6c17eda5082@2','Exakt egen inflyttningspost132 och uppslag15; inga namn för hustru/barn i denna post.'),('R-51c053d56cc1a32d26231525@1','1945s96 är Arnes egen rad; Majs egna1945–1946-rader uttryckligen olästa.')]:
 pa['evidence'].append(edge(rev,'supports',note))
specs.append({'object_id':path['object_id'],'action':'revise','whole_old_native':path,'full_old_API':APIfromNative(path),'full_new_API':pa,'exact_changes':[{'field':'data.body','old':path['data']['body'],'new':pa['data']['body']}],'evidence_action':'Append exactly three ordered current support edges; preserve all other fields including original outcome/caveat/rationale/origins.','source_disposition':'Preciserar verklig egen oläst tids-/fält-/åtkomstrest för PK05/07/12; inga resultat eller fullständighetslöften.','incoming_disposition':'Requires exact all-history incoming inventory before build. No automatic dependent rebind.'})
save('six-native-review-and-two-Maj-copy-exact-source-specification-v1.json',{'task':'T-0784','status':'SOURCE_SETTLED_EXACT_SPEC_NOT_RUNTIME_AUTHORIZATION','source_freeze_pin':newpin,'initial_amendment_pin':amendpin,'root_AC1_release_pin':new['root_AC1_release_pin'],'expected_target_count':8,'new_assessments':6,'revisions':2,'specifications':specs,'required_order':['KEY-P-0007-bf37119ff18f','PATH-P-0007-KP-05','ASSESSMENT-T0784-P0211-identity','ASSESSMENT-T0784-P0211-tree','ASSESSMENT-T0784-P0003-identity','ASSESSMENT-T0784-P0003-tree','ASSESSMENT-T0784-P0007-identity','ASSESSMENT-T0784-P0007-tree'],'preserve':'All21 old PK native payloads and all3 legacy headers, all relation/person/OWNER acceptance, all life states and unrelated source/current objects retained exactly. New current native axes contain explicit21 judgments and supersede historical gate effect only.','pending':'Mechanical absence/head/incoming check; exact8 current/API consequence proof; independent source/copy judgment and fullpackage byte binding. No stage or canonical authority.'})
