import json,hashlib,pathlib
base=pathlib.Path('evaluations/T-0790'); prep=base/'preparation'; out=base/'independent-review'
people=['P-0004','P-0210','P-0005','P-0006','P-0211','P-0212']
# Independent notes composed before exposure to primary proposals.
notes={
'P-0004':{
'ID':'Behåll självidentifiering och OWNER-datum; ingen ny identitetsgrind. Fullständighet gäller minimal identifikation, inte alla livsfrågor.',
'ARB':'Behåll faderns krönika 2011 som daterad uppgift om SICS avdelningschef/Kista och doktorsexamen Uppsala; Kista är arbetsort, inte belagd bostad eller nutida titel.',
'BO':'Motiverad minimering av privat boende; inga kontinuerliga bostadsperioder kan härledas ur arbetsorten Kista.',
'EKO':'Inget individuellt ekonomiskt underlag krävs eller samlas inom den motiverade minimeringen; ingen frånvaro av egendom påstås.',
'MIL':'Inget militär-/sjöfartsunderlag återbrukas; personens privatliv minimeras, inte ett negativt tjänstgöringsfaktum.',
'REL':'Behåll föräldrar, syskon, maka och söner med respektive aktuell evidensstatus; ordet ägaruppgifter är källkategori och gör inte alla relationer OWNER_CONFIRMED.',
'SAM':'Privata kyrkliga/rättsliga/sociala detaljer minimeras; ingen negativ sakslutsats av utebliven insamling.',
'HAL':'Levande ägares hälsa minimeras; ingen dödsuppgift eller hälsoslutledning.',
'PER':'Återbruka redan accepterad bildtext Sverker med Arne 1975 och familjekrönika 2011, inte ny bildgranskning.',
'SYN':'Minimal berättelse kan konsolideras från befintliga födelse-, familje-, foto- och 2011ankare; kalla inte livsbilden färdig medan PK08/T0034 består.',
'03':'STYRKT inom motiverad minimering: daterade befintliga ankare, inga påhittade mellantider.',
'04':'STYRKT: aktuella relationer bevaras individuellt med befintliga statusar och inga nya privata nätverk.',
'06':'STYRKT efter aktuell personbunden motivering av alla tio teman, utan automatisk blankettdispens från PK08.',
'08':'EJ STYRKT: PCD20260909029 namnger personen; T0034 birthdaypassage återstår. Privat minimering släcker inte frågan.',
'10':'STYRKT efter konsekvent aktuell minimal berättelse; inga nya livsfakta eller blankettnätförbud.'},
'P-0210':{
'ID':'Behåll OWNER namn/födelsedatum och Höök/Janson utan uppfunnet namnbytesdatum; födelseort okänd.',
'ARB':'Yrke/utbildning saknas i befintligt individuellt material; privat minimering tillämpas, inte personnoll.',
'BO':'Föräldrarnas Sundsvall/Lidingö är inte hennes födelse-/bostadsorter. Ingen bostadsperiod kan återvinnas ur föräldrarnas sammanhang.',
'EKO':'Individuell privatekonomi minimeras; inget negativt sakfaktum.',
'MIL':'Ingen befintlig militär-/sjöfartsuppgift; privat minimering, inte visad frånvaro.',
'REL':'Bevara make/söner/föräldrar och tre i C0225 namngivna far-/morföräldrar; avsaknad av mormorsnamn i just meddelandet är inte okända anor.',
'SAM':'Privata rättsliga/kyrkliga/sociala uppgifter minimeras; födelsefamiljen kräver ingen allmän medlemskartläggning.',
'HAL':'Sannolikt levande; ingen fabricerad dödsuppgift, hälsa minimerad.',
'PER':'Inga särskilda bevarade bilder/brev om henne identifierade i nuvarande material; familjeuppgift från maken är ett informantled, inte tre oberoende röster.',
'SYN':'Minimal familjeberättelse kan bibehållas; saknad födelseort och namnbytesdatum ska vara öppet preciserade och T0034 skild från legitim privat minimering.',
'03':'STYRKT: födelsedatum och sönernas ankare med okända orter/mellantider synliga; formulera minimering som tillämpad avgränsning, inte allmän tillåtelseregel.',
'04':'STYRKT: bevarade åtta relationer och deras källgränser; inga nya privata relationer krävs.',
'06':'STYRKT efter explicit aktuell motivering av tio teman; privatstatus är personbunden.',
'08':'EJ STYRKT: exakt namngiven av PCD20260909029; T0034 passage inte utförd.',
'10':'STYRKT efter rättat nätförbuds-/fullständighetsspråk; minimal källbunden text, inte antavlegodkännandets automatkonvertering.'},
'P-0005':{
'ID':'Behåll1938/Flen och aktuell identifikation; privat dag återförs inte. Minnets juli och Tranbärets2/7råreserv är inte ny exakt födelseprövning.',
'ARB':'Återbruka självuppgifter1945skola, student1958, Falsterbo1959, Uppsala1960, docent1973/prof emeritus2006; inte oberoende universitetsbevis eller säkra dateringar av alla utbildningssteg.',
'BO':'Flen samt registerankare Södertälje1943–47; bevara40/42konflikt, läsreserver och senare1948–70hänvisning. Registrering ger inte kontinuerlig fysisk vistelse.',
'EKO':'Aktuell @2-reserv gäller: affär och dess radbindning olösta; inte verksamhet hos far eller son. Privat ekonomi minimeras.',
'MIL':'15mån I1Solna/T4Hässleholm enligt eget minne; inga rullor lästa och inte yrkesmilitär.',
'REL':'Behåll CORROBORATED moderrelation REL-parent-P0007-P0005@1 med senare Flen/T0150-stöd. Äldre h.f.-resonemang får inte nedgradera den till TRANSCRIBED.',
'SAM':'Komplettera befintlig sammanfattning med dop1941-11-16 från redan accepterat event/Flenbok; fysisk dopplats okänd. Uppsalanation1960 självuppgift.',
'HAL':'Privat hälsa minimeras; faderns tänkta dödsorsak1993 gäller inte honom och är inte säker medicinsk slutsats.',
'PER':'Egna minnen/krönika och accepterade bildtexter1941/1943 återbrukas. Ingen ny bildläsning; Flen1943besökets kalenderreservation består.',
'SYN':'Konsolidera redan belagt dop och starkare moderstöd. Mellanankare/efter2011 minimeras, men öppen T0034fråga får inte kallas avskriven.',
'03':'STYRKT efter tillägg av redan befintligt dop1941ankare och tydliga register-/minnesgränser; ingen ny privat dag.',
'04':'STYRKT med senaste moderrelationens CORROBORATED, bevarade familjerelationer och hushållsroll skild från släktskap.',
'06':'STYRKT efter individuell temakonsolidering inklusive SAM-dop och aktuella ekonomireserver.',
'08':'EJ STYRKT @2 gäller före gammal STYRKT/parkering. T0034 äger birthday; far P0003 äger1948–70hushållspassage, ej nystartad här.',
'10':'STYRKT efter befintliga stödtillägg och aktuell integritets-/källvägsskillnad; ingen säker harmonisering40/42.'},
'P-0006':{
'ID':'Behåll Anna Hillevi,1938 och Burträsk med f275 som ortstöd; f1006födelseruta är blank. Ingen privat födelsedag eller inferred native sex.',
'ARB':'Makens2011uppgift om fil kand och akademisk sekreterarexamen; examensår/yrkesutövning okända och föräldrarnas läraryrke ej hennes.',
'BO':'Registerankare Gammelbyn1938–43/f275från1943 och avgång1950-09-02 Umeå; attestAug30 separat, mottagarbok oläst.',
'EKO':'Ingen individuell ekonomi i barnraderna, privat ekonomi minimerad; föräldrarnas förhållanden överförs inte.',
'MIL':'EJ RELEVANT kan behållas som personbunden sökprioritering utifrån kohort och ingen trigger; ingen utsaga om att kvinnan saknade all militär/sjöfart. Faderns174 ej hennes.',
'REL':'OWNER föräldrar och tre bröder skyddas. Birger var fastighetsgranne, inte därför hushållsmedlem.',
'SAM':'Historiska kyrkobokföringsrader fram till1950 återbrukas; inget nutida medlems-/trosfaktum.',
'HAL':'Blank dödskolumn under bokperioden ger inget senare livs-/hälsobevis; privat hälsa minimeras.',
'PER':'Ingen accepterad bildtext bland krönikans11 namnger henne; kyrkoboksrad är inte privatfoto. Ingen ny bildkontroll gjord.',
'SYN':'Skilj1938–50registerankare från odaterade examina/marriage uppgivna2011.2011är inte examens-/vigselår; blankettnätförbud redan supersederat.',
'03':'STYRKT inom personbunden minimering med exakta tid-/ortgränser och oläst1950mottagarbok synlig.',
'04':'STYRKT med OWNER och samtida hushållsstöd; bevara granne/hushållsskillnad.',
'06':'STYRKT med individuella teman; MIL avgränsning inte negativt livsfaktum.',
'08':'EJ STYRKT @2/PCD20260909029. T0034 birthday och föräldrarnas Umeåfortsättning är separata; inget utfört här.',
'10':'STYRKT med full aktuell caveat: f1006blank/f275ort, separat avgång/attest, odaterade examina; ingen ny privat detalj.'},
'P-0211':{
'ID':'Behåll native T0784passed/supporting. C0240ochC0935 accepterade fullposter med raw teckenreserver; ingen ny originalgrind.',
'ARB':'Yrkesuppgift saknas; mötet IbraRadio är inte anställning. Personbunden privat minimering kan behållas.',
'BO':'SundsvallsBB nedkomst, Storbränna föräldraboställe och Sättna registrering hålls isär; ingen nuvarande bosättning samlas.',
'EKO':'Egendom/privatekonomi avgränsas för möjligt levande person; inget personnoll.',
'MIL':'Faderns nummer är P0241s, inga egna militära privata uppgifter.',
'REL':'Komplettera känd familjebrygga med redan befintlig make/vigsel1962/dotter1964/efterlevande2017; föräldrar+femsyskon bevarade utan ny dubbelkartläggning.',
'SAM':'Historiskt icke döpt ger inte senare tro/medlemskap;1962vigsel enligt minnesord, ingen läst vigselbok.',
'HAL':'Hon överlevde maken enligt2017minnesord; det bevisar inte levande2026. Ingen ny hälsa/dödskartläggning.',
'PER':'Familjeuppgifter och makens barnskrivna minnesord redan bevarade; ingen ny insamling av privatmaterial.',
'SYN':'Nuvarande födelsecentrerade BIO behöver få befintliga1962/1964/2017ankare och reserver för att motivera full minimal livsbedömning.',
'03':'STYRKT efter konsolidering av redan bevarade1938/1962/1964/2017ankare; mellanperioder/privat senare liv explicit minimerade.',
'04':'STYRKT efter att make och känd vigsel återbrukats jämte föräldrar/dotter/syskon; inget privat utvidgat nätverk nödvändigt.',
'06':'STYRKT efter ny individuell60radersprövningens Evydel; inte automatisk följd av T0784identity.',
'08':'STYRKT kan motiveras efter faktisk omprövning: T0674/T0675/T0784 löser historisk post/identityroute; T0214rester är inte hennes livsgrind. PCD029namnger inte Evy. Privat minimering med konkret scope; delad Gunnarvigselväg kvar på Gunnar utan påhittad stängning.',
'10':'STYRKT först när minimal berättelse konsoliderat befintliga senare familjeankare; full nuvarande text godkänns inte oförändrad.'},
'P-0212':{
'ID':'GENOMGÅNGET; OWNER Gunnar Ivar Emanuel skyddas. Dokumentens Ivar Gunnar Emanuel och registreringsberoende är dokumentär fråga, inte personosäkerhet.',
'ARB':'ÖPPET. Minnesordens lärarutbildning/Floby studierektor/Fredriksberg rektor, men okända utbildnings- och tjänsteår. C0906är daterat katalogprov, ej universellt arkivslut.',
'BO':'ÖPPET.1933registrering/föräldrakontext,1946registrering frånIndien,1951egen1719 och1967Floby; inga säkra sammanhängande vistelser. Stockholmstrakten vidKristinasfödelse obelagd inferens.',
'EKO':'OMPRÖVA AVGRÄNSAT till exakt daterad källgräns/öppet alternativbehov: C0906s1875–1933serie saknar1960tal, ingen personsökning eller bevis alla vägar förbjudna.',
'MIL':'AVGRÄNSAT endast daterat2026-09-06katalogprov; omkring1953 är kohortförväntan, inte genomförd inskrivning. Ingen personrulla läst; ingen sjöfartstrigger.',
'REL':'ÖPPET. Kända föräldrar/syskon/maka/barn återbrukas; två barns minimering är inte egen felgrund. Vigselbok1962oläst/ortokänd. Odöpt1933/ickeSwChurch1946 utesluter inte senare dop/vittnen.',
'SAM':'ÖPPET. Minnesordens Liberal/FN/kulturnämnd/medalj2008; inga mandatperioder eller medlemskap ur tidiga dopnoter. Föreningsarkiv oprövade.',
'HAL':'ÖPPET. Död2017-09-22 och gravsättning2018-05-11; Falköping hemort ej fysisk dödsplats. Ingen dödsorsak/ohälsa/släktmedlems hälsa infereras.',
'PER':'ÖPPET. Barnens minnesomdömen/amatörmåleri bevaras subjektivt. IFK1948namne kandidat; brev/foton/målningar otestade, T0362 begränsade ägarfrågor.',
'SYN':'ÖPPET. Korrigera Stockholmstrakten och universalåtkomst.1951–62 saknar säkra daterade ankare; undaterad utbildning/möte får inte automatiskt läggas efter1962. PK10kan passera efter korrekt text medan materiella luckor består.',
'03':'EJ STYRKT:1951–62och tunna1962–67passagen materiella. T0359äger1718/1719plusmaxettregister, egen1719; T0362äger korta nyckelfrågor.',
'04':'EJ STYRKT för öppna livsnätverks-/vigselfrågor, inte för minimerade privata barn. Full läst familjekontext bevarad.',
'06':'EJ STYRKT: teman redovisade men materiella vägar kvar; sexöppettal är föråldrat (sju nu ÖPPET), EKO/MIL inte universellt uttömda.',
'08':'EJ STYRKT: T0359/T0362 och daterat begränsade C0906alternativ; ingen åtkomstgaranti/avskrivning. Källvägsutfall skiljs från Wotanstatus.',
'10':'EJ STYRKT i oförändrad BIO@5 på grund av Stockholmstrakten och universellt katalogslut; STYRKT möjligt efter precisa korrigeringar utan att kräva ny källa.'}}
rows=[]
for p in people:
 d=json.load(open(prep/(p+'-person.json')))['research']
 for typ,vs in [('theme',d['themes']),('PK',d['requirements'])]:
  for v in vs:
   code=v['revision_id'].split('@')[0].split('-')[-1]
   if typ=='PK' and code not in ['03','04','06','08','10']:continue
   owner=('T-0034: personlig birthdaypassage; nuvarande minimal livstext T-0790' if p in people[:4] else 'T-0790: minimal befintlig livskonsolidering; T-0214 familjerester separat, Gunnarfrågor T-0359/T-0362' if p=='P-0211' else 'T-0359:1951hushåll; T-0362:1951–67nycklar; övriga KP05frågor kvar i P-0212 current research för framtida bounded kärnval, inget nytt uppdrag skapat')
   rows.append({'person':p,'kind':typ,'code':code,'current_revision':v['revision_id'],'current_outcome':v.get('outcome'),'current_body':v.get('body'),'current_caveat':v.get('caveat'),'independent_disposition':notes[p][code],'remaining_scope_and_owner':owner})
pins={}
for path in [base/'root-current454-six-person-input-and-own-review-release-v1.json',prep/'current-input-manifest-v1.json',prep/'complete-current-history-support-native.json',prep/'supplement-current-incoming-receipts-and-context-v2.json',prep/'context-pins.json',prep/'README.md']+[prep/(p+'-person.json') for p in people]:
 pins[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
result={'schema':'T0790-independent-own-existing-material-freeze/1','date':'2026-10-06','role':'independent Astra source/consequence','candidate_proposals_seen':False,'input_pins_sha256':pins,'baseline_journal':454,'baseline_main_sha256':'405a7330c23522ae3a08e2ad9ae4ac7b57bb4c194a8c8db01e596095f5bcbecf','scope':people,'coverage':{'themes':60,'life_PK':30,'new_original_reads':0,'new_images':0,'new_external_searches':0,'pool_revisions_available':809,'pool_revisions_claimed_read':False,'read_scope':'Six current person/research/body+caveat, targeted current native supports/accepted audit qualifications and owner contexts. Metadata availability and older accepted readings do not count as new original or whole-source rereview.'},'native_life_recommendations':[{'person':p,'outcome_after_required_consolidation':'passed' if p=='P-0211' else 'failed','reason':'Personbunden minimal livsbild kan passera efter konsoliderade befintliga familjeankare, aktuell källvägsprövning och exakt paketgranskning; ingen automatisk konvertering av identity/privatstatus.' if p=='P-0211' else 'PCD20260909029/T0034 materiell personlig passage kvar.' if p in people[:4] else 'Materiella1951–67livsfrågor/yrkes- och nätverksvägar kvar. PK10 kan rättas utan PK03/08pass.','final_package_source_approval':False} for p in people],'individual_rows':rows,'protected':'Native identity/tree, accepted ancestry and OWNER_CONFIRMED are preserved. No schema outcome inferred from old KLAR; no new canonical operations authored here.'}
assert len(rows)==90
(out/'own-freeze-v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(hashlib.sha256((out/'own-freeze-v1.json').read_bytes()).hexdigest())
