# Slutresultatskontrakt för personforskning

Aktiv norm, adopterad i T-0670 (2026-09-18). Sakkraven består; skrivning
och representation följer [Genealogy2:s arbetsväg](../../genealogy2/docs/working.md).
Ord som akt och profil avser aktuella personvyer och forskningsobjekt, inte
nya Markdownfiler. [Fryst ursprung](../../genealogy/person-contract.md)
(SHA-256 `b36148a6d00d9fdaf8ed0dfa32df566d3a82084706886d4fabb3c80ddaf996f3`) bevaras som historik.

Version: `person-research/v1`. Beslutat i PCD-2026-09-05-013.

Detta är normativa krav på resultatet för **varje identifierad person**,
oberoende av aktens ålder, storlek, tidigare KLAR, antavlestatus eller
ingångsskälet till forskningen. [North star](../../NORTH-STAR.md) äger målet,
[forskningsprogrammet](research-program.md) arbetsordningen och
[källstrategin](source-strategy.md) källvalen. Ett ordnat dokument utan
sakligt tillräcklig forskning uppfyller inte kontraktet.

## Ansvar och beständig representation

- Genealogy2:s versionerade person-, relations-, händelse- och slutsatsobjekt
  äger aktuell personmodell, livslinje och berättelse. Personvyn visar dem.
- Personens forskningsobjekt äger frågor, söknycklar, teman, källvägar,
  täckning och granskning. En profil är deras samlade kunskapsbild,
  **inte en andra arbetskö**: inga READY/ONGOING eller sessionscheckpoints.
  Saknade individuella bedömningar ska vara synliga.
- Källposter, avskrifter, observationer och versionsbundna underlag bevarar
  evidenshistoriken. En rättelse tillför en revision; historiken skrivs inte om.
  En forskningsbatch bevaras en gång i operation/journal; Wotan länkar dit.
- `inventory`, verifierad `pedigree` och personvyer härleds från modellen.
  En indikator kan inte åsidosätta en olöst materiell fråga. Gamla frontier,
  source-coverage och research-inventory är frysta historiska översikter.
- Wotan äger beslutat utförande, ordning och återupptagning. Alla nya
  kunskapsändringar går genom `apply`, aldrig genom att redigera en läsvy.

## Gemensamma resultatkrav

| Krav | Resultat som ska finnas | Vad granskaren faktiskt ska kontrollera |
|---|---|---|
| PK-01 Identitet | En akt avser en person; namnformer, ankare och kopplingen framåt redovisas. Kandidater har skilda identiteter. | Tidsföljd, geografi, hushåll, närstående och relevanta alternativ bär sammanföringen. Namnlikhet räcker inte. |
| PK-02 Påståenden | Atomära påståenden med status, exakt belägg och aktuell bedömning. | Vad källan säger, normalisering och slutsats är åtskilda. Ingen avskriftstatus används som automatiskt identitetsbevis. |
| PK-03 Livslinje | Källstödd kronologi över hela den kända livstiden, inklusive bostads-/hushållsperioder och förändringar. | Materiella tidsluckor och motstridiga överlapp syns. Enstaka folkräkningsår har inte gjorts till oavbrutet boende. Okända start-/slutpunkter är öppna. |
| PK-04 Relationer och nätverk | Föräldrar, partner, barn och relevanta syskon, vittnen, grannar, förmyndare och medflyttare med tids- och källkontext. | Samtliga relevanta personer i läst målpost/hushåll är bevarade; social närhet har inte gjorts till släktskap. |
| PK-05 Full informationsutvinning | Relevanta uppgifter ur hela den undersökta posten/akten, bilagor och uttryckliga hänvisningar är hanterade. | Forskaren har inte slutat läsa vid den sökta födelsedagen eller första arvingen. Olästa fortsättningar och läsosäkerheter är preciserade. |
| PK-06 Tematäckning | Alla tio teman nedan har en uttrycklig individuell bedömning, relevant omfång och belägg/lucka. | Tomma rubriker, textmängd och många källor räknas inte som genomgång. Även möjliga ännu okända spår har bedömts. |
| PK-07 Söknycklar | Kända namn, familjekonstellationer, platser, tider, organisationer och arkivnycklar med provenans, osäkerhet och användningsområde. | Uppgiften gäller rätt tid/person. Adress är inte ägande; yrke är inte säker arbetsgivare; värnplikt är inte yrkessoldat. |
| PK-08 Källstrategi | Relevanta frågor har källvägar med ingång, omfattning, förväntat kunskapsvärde, beroenden, åtkomst och sökutfall. | Hinder hos en tjänst har inte blivit källslut. Saknad nyckel har en prövad eller konkret möjlig anskaffningsväg. |
| PK-09 Bevisföring | Bärande slutsatser förklarar stöd, källberoende, alternativ, motbevis och kvarstående osäkerhet. | Kopierade datum eller index över samma original har inte räknats som oberoende belägg. Konflikter är analyserade, inte nedröstade. |
| PK-10 Livsberättelse | En konsoliderad, källförankrad biografisk text med hänvisningar till belägg/påståenden. | Berättelsen återger aktuell bedömning och levnadsvillkor som källorna medger. Allmän ortshistoria är märkt som kontext och tillskrivs inte personen utan belägg. |
| PK-11 Provenans och rättelser | Exakta källställen, läsdatum, avskrift/tolkning, relevant original och SHA-256; länkade rättelser. | Gamla observationer finns kvar. Omfördelning mellan identiteter kan följas och beroende slutsatser har omprövats. |
| PK-12 Slutgranskning och återöppning | Daterad bedömning per krav, redovisade gränser och konkreta återaktiveringsvillkor. | Ingen materiell genomförbar åtgärd döljs som valfri berikning. Task-DONE, arkivfront, trädsäkerhet och personfullständighet hålls isär. |

Kraven beskriver innehåll, inte krav på identisk prosa i alla akter. Små akter
får vara korta och länka till gemensamma hushålls- eller källbedömningar.
Hänvisningen måste precisera vad som gäller just denna person. Samma arbete
behöver inte skrivas om i varje akt, men ingen person får försvinna ur täckningen.

## Två färdignivåer

Kraven ovan beskriver en fullständig personbehandling. De uppfylls inte alltid
samtidigt, och de har olika verkan på antavlan. Kontraktet skiljer därför på
två nivåer med **var sitt granskningsutlåtande**.

| Nivå | PK-krav | Verkan |
|---|---|---|
| **Identitetsnivå** | PK-01, PK-02, PK-05, PK-07, PK-09, PK-11, PK-12 | Grind för antavlan. Utan den får ingen anlinje passera personen. |
| **Livsbildsnivå** | PK-03, PK-04, PK-06, PK-08, PK-10 | Personens levnad. Får ligga efter, men skulden ska synas. |

Fördelningen följer var kunskapen kommer ifrån, inte hur intressant den är.

**PK-05 ligger i grinden med avsikt.** Full informationsutvinning gäller den
post som redan är uppslagen: moderns ålder i dopnotisens ytterkolumn,
`Hitkom. ifrån` i hushållsraden, en ståndsbeteckning som förklarar ett
efternamn. Sådana uppgifter kostar ingenting extra och är ofta just det som
bär linjen vidare. Att sluta läsa vid det sökta datumet är fel på
identitetsnivån, inte en uppskjuten berikning.

**PK-08 ligger i livsbilden med samma avsikt.** Det dyra är att öppna *nya*
källfamiljer — bouppteckningar, mantal, jord och lagfart, domböcker — för
frågor som inte flyttar fronten. Det arbetet skjuts upp, inte det som ligger
på en redan läst sida.

**PK-04 delas.** Personer i den lästa posten eller det lästa hushållet hör
till identitetsnivån; att söka upp nätverk därutöver hör till livsbilden.

De tio temana hör i sin helhet till livsbildsnivån. `Livsbildsläge:
EJ BEDÖMT` är därför ett giltigt läge för en identitetsgodkänd person, inte
en brist.

**Nivåerna får aldrig slås ihop till ett mått.** En person kan vara
identitetsgodkänd i åratal innan livsbilden görs; en generation kan vara
trädklar utan att vara livsbildsklar. Genealogy2:s inventering och verifierade antavla
håller de två åtskilda, så att den uppskjutna skulden är synlig i stället
för dold.

## Tio teman som alltid ska bedömas

| Tema-id | Område | Frågor som grundgenomgången ska upptäcka |
|---|---|---|
| ID | Identitet och ursprung | Namnformer, födelse/dop, identitetsankare, ursprung, konkurrerande personer. |
| REL | Familj och sociala nätverk | Föräldrar, partner, barn, syskon, fosterrelationer, faddrar, vittnen och övrigt relevant nätverk. |
| BO | Boende och migration | Boställen under livet, hushåll, flyttkedjor, resor, ut-/invandring och gränsändringar. |
| ARB | Arbete, utbildning och samhällsställning | Yrkesförlopp, försörjning, arbetsgivare, skolgång, lärlingstid, föreningar och offentliga uppdrag. |
| EKO | Egendom och ekonomi | Ägande/brukande, bostadsvillkor, arv, skulder, tillgångar, fattigdom och förändringar. |
| MIL | Militär och sjöfart | Värnplikt, soldat-/båtsmanstjänst, förband, sjömanshus, fartyg, resor och pension. |
| SAM | Rättsligt, kyrkligt och socialt liv | Mål, förmynderskap, medborgarskap, församling, fattigvård, kommun- och institutionskontakter. |
| HAL | Hälsa och livets slut | Dokumenterad ohälsa/funktionsnedsättning, död/begravning och källans grund för orsaksuppgifter. |
| PER | Personliga spår | Bilder, signaturer, brev, dagböcker, muntliga minnen, personarkiv, press och biografiskt tryck. |
| SYN | Sammanhängande livsbild | Tidsluckor, förändringar, källkritisk berättelse och tydlig gräns mellan personfakta och historisk kontext. |

Varje tema får en av följande sakliga bedömningar i personens forskningsobjekt:

- `EJ BEDÖMT`: ingen individuell bedömning genomförd.
- `ÖPPET`: relevant fråga, undersökningslucka eller möjlig upptäcktsväg återstår.
- `GENOMGÅNGET`: tillämpligt omfång är sakligt undersökt och konsoliderat;
  länka resultat och granskning. Det betyder inte att allt är känt.
- `AVGRÄNSAT`: en källgrundad gräns för dagens online-undersökning är prövad,
  med alternativ och återaktivering. Tillfällig utloggning kvalificerar inte.
- `EJ RELEVANT`: individuell motivering utifrån livstid/sammanhang och
  rimlig upptäcktskontroll; frånvaro i en kyrkobok räcker inte.
- `INTEGRITETSMINIMERAT`: saklig dataminimering för levande/privat person;
  nödvändiga identitets- och relationsuppgifter består.

Varje temabedömning anger tema, utfall, omfång, slutsats/lucka och belägg
samt källvägar. Ingen generell standardmotivering ersätter individuell
bedömning. Orden här anger saklig innebörd; operationens schema och tillåtna
fält följer arbetsvägen, inte den gamla profilens tabellkolumner.

## Frågor, observationer och slutsatser

Projektets bevisprövning kräver fem led: rimligt uttömmande relevant
forskning, fullständiga källhänvisningar, analys och korrelation, behandling
av motstridiga belägg samt en skriftligt motiverad slutsats. Hur omfattande
prövningen behöver vara beror på frågan och vilka källor som kan förändra
svaret. En enkel samtida händelseuppgift och ett svårt identitetsproblem
behöver olika mycket argumentation, men båda måste vara spårbara.

Varje materiell fråga får ett stabilt objekt-id. Äldre lokala id:n, exempelvis
`P-0003/Q-01`, bevaras som ursprungsreferenser till motsvarande objekt.
Revidera en befintlig fråga i stället för att skapa en dubblett. Den ska ange:

1. exakt fråga, person(er), tid/plats och varför svaret spelar roll;
2. känt underlag och vilka antaganden som ännu bara är hypoteser;
3. rimliga alternativa svar/identiteter och vilken observation som skulle
   skilja dem eller motsäga huvudförslaget;
4. källvägar och deras förväntade diskriminerande eller biografiska värde;
5. aktuell slutsats, belägg, källberoenden och olösta konflikter;
6. vilka andra påståenden/personer som påverkas om slutsatsen ändras.

Slutsatsläget anges som `ÖPPEN`, `STÖDD`, `FASTSTÄLLD`, `OMSTRIDD`,
`AVVISAD` eller `OLÖST INOM PRÖVAT OMFÅNG`. Detta är analytiska bedömningar,
inte nya A-poststatusar eller tillstånd i Wotan. `FASTSTÄLLD` kräver en
skriven argumentation med rimligt uttömmande prövning relativt frågan;
antal källor eller en automatisk poängsumma räcker inte. Tillräckligt
belagda enkla slutsatser behöver kort argumentation; svåra identiteter mer.

`OWNER_CONFIRMED` gäller enligt sitt beslut och får användas som fastställd
projektinformation. Saknat original ger inget nytt beviskrav för den
uppgiften. Ett påträffat faktiskt motbelägg bevaras och lyfts till ägaren.

Bedöm källa, information och evidens separat: original/avskrift/index;
vem som kan ha lämnat en viss uppgift och när; samt hur den stöder eller
motsäger just denna fråga. Samma handling kan ha både starka och svaga
informationsuppgifter. Ett index eller SCB-utdrag kan vara användbart utan
att vara ett nytt oberoende belägg för originalets födelsedatum.

## Källvägar och beroenden

Varje vald konkret källväg får ett stabilt objekt-id och ska bära följande
innehåll. Äldre `P-NNNN/KP-01` bevaras som ursprungsreferens; inga nya
profiler enligt den frysta Markdownmallen skapas:

- **Frågor/teman:** vilka Q-id:n och teman vägen kan bidra till.
- **Källklass:** K-id från källstrategin; eventuell motiverad ny klass.
- **Tid/plats och arkivbildare:** historisk jurisdiktion, serie, volym,
  källperiod och personperiod; det okända märks som okänt.
- **Förväntad information:** vilket utfall kan lösa en fråga, skilja
  kandidater eller öppna en ny sökning; vad vägen inte kan avgöra.
- **Ingång och söknycklar:** register/original/katalog, stabila referenser,
  kända namnformer, orter, familj, tidsintervall och deras provenans.
- **Beroenden:** specifik saknad uppgift eller åtkomst, varför den behövs,
  hur den kan erhållas, om det kan göras nu och eventuell föregående KP.
- **Föregående källvägar:** explicita referenser till föregående vägobjekt
  eller uttryckligen inga. Äldre lokala KP-id:n ska personkvalificeras.
  Prosan i Beroenden förklarar alternativen men ersätter inte referenserna.
- **Leverantörer och åtkomst:** relevant arkivinstitution och tillåtna
  nätvägar, faktisk kontrollerad åtkomst med datum eller `EJ KONTROLLERAD`.
- **Undersökt omfång och utfall:** länk till exakt batch/citation; serie,
  år, sidor, frågeparametrar, varianter, täckningskontroll, avbrott och luckor.
- **Bedömning och återaktivering:** saklig disposition och vad som ändrar den.
- **Wotan:** beslutad uppgift eller `EJ BESLUTAT UTFÖRANDE` med skäl;
  inget eget utförandestatusfält eller prioriterad kö i profilen.

Sökutfall skiljs mellan `EJ UNDERSÖKT`, `POSITIVT`, `LOKALT NOLL`,
`LÄSOSÄKERHET`, `ÅTKOMSTHINDER`, `EJ DIGITALISERAT`, `ARKIVLUCKA` och
`RELEVANTA VÄGAR PRÖVADE`. Flera utfall kan behövas för olika delar av
omfånget; dela då vägen. En katalogträff är positiv för existens/routing,
inte för en ännu oläst persons uppgifter.

Beroenden får inte vara cirkulära eller sluta i ett vagt ”kräver mer data”.
Sök andra ingångar, exempelvis anhörig + ort + tidsintervall. Ett nytt
namn, dödsdatum, fastighetsnamn eller förband ska omedelbart prövas mot
**samtliga berörda villkorliga vägar**, även i andra personprofiler.
Inaktuella beroenden tas bort med hänvisning till fyndet. Nytt utförande
sker inom aktuell uppgifts omfång eller i en avgränsad Wotan-efterföljare.

## Negativa resultat och oberoende

Ett söknoll dokumenterar en utförd sökning. Negativ evidens kräver dessutom
argument för varför personen/uppgiften borde ha funnits i ett tillräckligt
komplett och läst omfång. Dokumentera registreringsregler, luckor, tänkbara
namnformer och kontrollfall. Ett ofullständigt namnindex kan inte bära
slutsatsen att en bouppteckning saknas. Ett manifest bär sidföljd, inte
frånvaro av en person på sidor som aldrig lästes.

Vid varje källpassage följ hänvisningar och utvinn hela relevanta innehållet
inom omfånget. Bevara rå läsning, separera tolkning och återanvänd redan
hämtat original. Om en gammal citation endast täcker första sidan markeras
resten oläst; ”bouppteckning kontrollerad” kan inte avsluta hela handlingen.

## Återställning från olika utgångslägen

| Ingångsläge | Första nödvändiga åtgärd | Tillåtet resultat |
|---|---|---|
| Ny person/nytt namn | Skilj kandidat från etablerad identitet; bevara relevant målpost och relation; skapa profil med ärligt obesvarade teman. | Minimal spårbar akt och avgränsad identitetsfråga, aldrig automatisk säker ana. |
| Halvfärdig akt | Återanvänd belägg, extrahera befintlig tidslinje och söknycklar, markera olästa tidsavsnitt och teman. | Fortsättning från faktisk lucka; inget omtag av redan tillräckligt arbete. |
| Stor/rörig akt | Sortera observationer från aktuell bedömning, förena hänvisningar, inventera dubbletter och föråldrade öppna frågor. | En aktuell livsbild med synlig historik; mängd text ersätter inte prövning. |
| Sammanblandad eller motsägelsefull akt | Skydda kandidatgränser, stoppa osäker propagering och kartlägg beroende slutsatser före fortsatt utvidgning. | Separata identiteter, länkade rättelser och uttryckliga kvarstående alternativ. |
| Äldre GRANSKAD/KLAR | Pröva vilket omfång den äldre granskningen faktiskt täckte mot PK-01–12. | Återanvändbart arbete tillgodoräknas med belägg; ny kontraktsgranskning är inte automatiskt godkänd. |
| Externt blockerad passage | Bevara exakt passage och prövade alternativ i Wotan; skilj personens öppna krav från den hindrade källan. | Annat tillgängligt godkänt arbete fortsätter; inloggning återupptas från sparad punkt. |
| Sidoperson/FAN/kandidat | Bevara identifikations- och relationsvärde och bedöm teman proportionerligt. | Egen spårbar akt; dokumenterad lägre planeringsprioritet är inte en permanent dispens från målkraven. |
| Levande/privat person | Bedöm nödvändig identitets-/relationsinformation och integritetsgräns. | Minimal akt med motiverad temabedömning; ingen aktiv breddinsamling av privata detaljer. |
| Nya belägg efter avslut | Identifiera berörda frågor, teman, personer och avgränsningar. | Endast berörda delar återöppnas; tidigare evidens och giltiga relationer består. |

## Kontraktsgranskning och slutresultat

Aktuell granskning lagras som versionsbundna bedömningar, en per person
och kriterium, enligt [arbetsvägens ordförråd](../../genealogy2/docs/working.md):

| Kriterium | Utfall | Saklig innebörd |
|---|---|---|
| `identity_review/1` | `passed`, `failed` | Godkänd eller underkänd identitetsnivå |
| `tree_effect/1` | `supporting`, `waiting`, `non_supporting` | BÄRANDE, AVVAKTAR eller EJ BÄRANDE |
| `life_picture_review/1` | `passed`, `failed` | Separat granskning av livsbildsnivån |

Utebliven granskning är inte underkännande och får aldrig bli godkännande.
De svenska begreppen nedan anger sakkraven. Äldre uttryckliga profilutfall
läses fortfarande med sin ursprungliga innebörd när native bedömning saknas.
`Kontraktsgranskning` avsåg hela kontraktet och omdöps aldrig till en ny
oberoende livsbildsgranskning. Dokumentera även identitets-, livsbilds- och
källstrategiläge i de aktuella forskningsbedömningarna med sakliga skäl.
Äldre termer `EJ BEDÖMT`, `PÅGÅR`, `PRÖVAT`, `OMSTRITT`, `OLÖST`,
`GENOMGÅNGEN`, `AVGRÄNSAD` och `INTEGRITETSMINIMERAD` behåller sin innebörd;
de är inte nya Wotan-statusar eller automatiskt tillåtna schemafält.

`life_picture_review/1: passed` kräver en daterad, beläggslänkad prövning
av PK-03, 04, 06, 08 och 10, alla tio teman, konsoliderad livslinje och
berättelse samt motiverade källgränser och återaktivering. En uppskjuten
genomförbar livsbildsfråga får inte döljas av godkännandet. Identitetsnivån
ska redan vara godkänd, men dess bedömning lagras och redovisas separat.
Full personbehandling kräver båda nivåerna; inget nytt gemensamt mått införs.

`Identitetsgranskning`: `EJ GRANSKAD`, `UNDERKÄND` eller `GODKÄND`, och gäller
**endast identitetsnivåns krav** PK-01, 02, 05, 07, 09, 11 och 12. `GODKÄND`
där kräver en daterad, beläggslänkad bedömning av dessa sju, ett
`Identitetsläge` som är `PRÖVAT` eller sakligt avgränsat `OLÖST`, och säger
ingenting om livsbilden.

`Trädverkan`: `BÄRANDE`, `EJ BÄRANDE` eller `AVVAKTAR`. Fältet svarar på den
enda fråga identitetsnivån finns för: **får antavlan passera denna person?**
`BÄRANDE` kräver prövad identitet och bärande plats i den direkta antavlan
(PCD-2026-09-11-035); en säker sidoperson blir inte därför BÄRANDE.
En `OLÖST` identitet kan vara
korrekt avgränsad och identitetsgodkänd, men den får aldrig bära en anlinje
uppåt; den står då `AVVAKTAR`. Utan detta fält blir identitetsgodkännandet en
gummistämpel.

`Kontraktsgranskning: GODKÄND` kräver `Identitetsgranskning: GODKÄND` —
den fulla nivån kan inte hoppa över grinden. Därutöver kräver den en daterad,
beläggslänkad bedömning av **varje PK-01–12**,
alla tio teman, konsoliderad tidslinje och berättelse, redovisade alternativ,
källtäckning och beroenden. Inga materiella genomförbara frågor får återstå.
Godkännandet ska ange granskat källäge och vilka källgrundade gränser som
består; det innebär inte att alla datum eller föräldrar blivit kända.
Olöst identitet kan vara korrekt avgränsad men får aldrig öppna säker antavla.

En genomförbar men uppskjuten undersökning, tidsbudget eller tillfällig
inloggningsspärr ger inte godkännande. En fullständigt prövad online-gräns
eller integritetsminimering kan göra det med konkret motivering. Äldre
`KLAR`, `GRANSKAD` och slutstatusar behålls som historiska bedömningar och
registrerade indikatorer tills saklig omprövning gjorts. De konverteras inte.

Den maskinella inventeringen kontrollerar struktur, fält och referenser och
visar separat om profiler saknas eller är oprövade. Den kan inte läsa
originalen åt granskaren eller intyga genealogisk bevisning. Manuella
godkännanden måste därför alltid granskas sakligt före kohort-/projektavslut.

## Mallar och tillämpning

Använd [arbetsvägen](../../genealogy2/docs/working.md) och Wotans
[forskningsmall](../../wotan/templates/research-task.md). Vid forskning på
en befintlig person ska forskningsobjekten först läsas och vid behov
kompletteras genom en avgränsad adoption inom uppgiften. Ange vilka PK-krav
uppgiften behandlar och vilka som återstår.
Ett begränsat källprov får avslutas utan personens GODKÄND, men dess olösta
krav ska vara synliga och beslutat följdarbete ligga i Wotan.

Ange alltid vilken **nivå** uppgiften arbetar på. En frontuppgift som bygger
antavlan avslutas med `Identitetsgranskning` och `Trädverkan` satta; den
lämnar `Livsbildsläge` och `Kontraktsgranskning` orörda och det är ett
fullständigt resultat, inte ett halvfärdigt. En livsbildsuppgift förutsätter
att identitetsnivån redan är godkänd.

## Precision och full avskrift

Sakregler adopterade från [den frysta aktstandarden](../../genealogy/person-standard.md)
(PCD-2026-09-07-026 och PCD-2026-09-09-027). Dess rubrikordning och
Markdowntabeller styr inte Genealogy2:s representation.

- Använd ett motiverat visningsnamn; redovisa belagda stavningar,
  patronymikon och familjenamn med användningstid och belägg i Namnformer.
  Källcitat behåller sin stavning. Varken förälders namn eller makes namn
  bevisar automatiskt personens eget namn, namnbyte eller namnbytesdatum.
- Skriv säkra fullständiga datum `ÅÅÅÅ-MM-DD` i tabeller. År får stå ensamt
  när precisionen stannar där; skriv `omkring`, `före`, `efter` eller ett
  uttryckligt intervall vid osäkerhet. Fyll aldrig en saknad dag med 01.
  I löptext får datum skrivas naturligt på svenska.
- Ange plats så precist som belägget tillåter, med socken/församling när
  det behövs för att skilja likalydande orter. Bevara osäker ortläsning.
- Skriv aktuell kunskap i sammanfattningen. Ett senare fynd ska föras in
  även i tidslinje, relevant tematabell, relationer och profilens frågor.
  Orden ”obelagt”, ”oläst”, ”återstår” och ”okänt” ska alltid prövas mot
  sparade belägg. Oklart, inte undersökt och undersökt utan träff skiljs åt.
- Håll prosa proportionerlig mot materialet. Skilj personfaktum,
  källuppgift, inferens, familjeminne och allmän historisk kontext.
  Syntes får inte göra en osäker uppgift säker eller ge en nolla större
  räckvidd än den granskade källpassagen.

### Tabellförda källor

En citation som återger en post ur en tabellförd källa — husförhörslängd,
församlingsbok, ministerialbok, folkräkningsblad — ska lista uppslagets
**tryckta** kolumnrubriker och för varje kolumn ange om den är **avskriven**,
**tom** eller **oläst**.

Skälet är att en cell som inte nämns i dag inte går att skilja från en cell
som är läst och tom. Personaktsprogrammet har funnit fyra fall där en tryckt
kolumn aldrig lästs av någon avskrift: kolumnen `Wigd` bar en vigseldag som
söktes i sju vigselårgångar, kolumnen `Död.` bar en dödsdag på en rad vars
akt sade att personens senare öde inte var fastställt, en annan `Död.`-kolumn
påstods ligga utanför bilden fast den var synlig och tom, och två tryckta
smalkolumner lästes som ett marginaltal.

Läs rubrikraden i **samma utsnitt** som datacellen. En kolumns innebörd
avgörs av dess position, och positionen kan inte fastställas ur en cell
enbart. `—` i en avskrift betyder saknad uppgift, aldrig en oläst kolumn.

Kravet gäller nya och omarbetade citationer. Befintliga citationer skrivs
inte om retroaktivt; se PCD-2026-09-09-027.

Dokumenterat prövad oläslighet är en källgräns, inte automatiskt PK-05-brist.
En brist namnger den outvunna kolumnen eller fortsättningen. Bedöm varje
PK-krav för sig: en korrekt källkritisk berättelse kan uppfylla PK-10 medan
livsluckor i PK-03/08 består. Historiska upphävda slutsatser ska vara tydligt
ersatta i aktuell läsvy med spårbar rättelse; ursprunglig evidens bevaras.
Presentationskontroll, saklig konsolidering och kontraktsuppfyllelse är tre
skilda granskningsresultat. Tomt fält är aldrig ett genomfört negativt fynd.
