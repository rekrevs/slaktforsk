# Slutresultatskontrakt för personforskning

Version: `person-research/v1`. Beslutat i PCD-2026-09-05-013.

Detta är normativa krav på resultatet för **varje identifierad person**,
oberoende av aktens ålder, storlek, tidigare KLAR, antavlestatus eller
ingångsskälet till forskningen. [North star](../NORTH-STAR.md) äger målet,
[forskningsprogrammet](research-plan.md) arbetsordningen och
[källstrategin](source-strategy.md) källvalen. Ett ordnat dokument utan
sakligt tillräcklig forskning uppfyller inte kontraktet.

## Ansvar och beständig representation

- Personakten äger personmodell, aktuell identitetsbedömning, livslinje,
  berättelse och temabedömningar.
- `research-profiles/P-NNNN.md` äger personens frågor, söknycklar, källvägar,
  källtäckning per omfång och kontraktsgranskning. Filen är ett kunskaps- och
  granskningsunderlag, **inte en andra arbetskö**: inga READY/ONGOING,
  arbetsordningar eller sessionscheckpoints där. Beslutat utförande länkas
  till Wotan. Saknade profiler är synliga bedömningsluckor.
- Källakter, citationer och forskningsbatchar bevarar observationer och
  utförda sökningar append-only. Profilen länkar, den duplicerar inte loggen.
- `source-coverage.md` och `frontier.md` är översikter. En cell eller etikett
  kan aldrig åsidosätta en olöst materiell fråga i akt/profil.
- `research-inventory.json` är en ombyggbar strukturell inventering av alla
  aktuella P-id:n. Den tilldelar inte saklig fullständighet. Wotan äger
  vilka inventeringsluckor som faktiskt ska behandlas och när.

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

Varje tema får en av följande bedömningar i profilens tabell:

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

En profil har en rad per tema med kolumnerna `Tema`, `Bedömning`,
`Omfång och slutsats/lucka`, `Belägg och källvägar`. Ingen generell
standardmotivering kopieras över 528 personer som ersättning för bedömning.

## Frågor, observationer och slutsatser

Projektets bevisprövning kräver fem led: rimligt uttömmande relevant
forskning, fullständiga källhänvisningar, analys och korrelation, behandling
av motstridiga belägg samt en skriftligt motiverad slutsats. Hur omfattande
prövningen behöver vara beror på frågan och vilka källor som kan förändra
svaret. En enkel samtida händelseuppgift och ett svårt identitetsproblem
behöver olika mycket argumentation, men båda måste vara spårbara.

Varje materiell fråga får ett stabilt lokalt id, exempelvis `Q-01` i
P-0003:s profil; global hänvisning är `P-0003/Q-01`. Den ska ange:

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

Varje vald konkret källväg får lokalt id `KP-01` och följande fält, i
punktform enligt [profilmallen](templates/research-profile.md):

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
- **Föregående källvägar:** enbart `INGA` eller explicita KP-id:n
  separerade med kommatecken; annan persons väg skrivs `P-NNNN/KP-01`.
  Prosan i Beroenden kan förklara alternativen men tolkas inte som en graf.
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

Profilen har exakt ett fält av varje sort:

```text
- Kontrakt: `person-research/v1`
- Person: P-NNNN
- Identitetsläge: `EJ BEDÖMT`
- Livsbildsläge: `EJ BEDÖMT`
- Källstrategiläge: `EJ BEDÖMT`
- Kontraktsgranskning: `EJ GRANSKAD`
```

Identitetsläge: `EJ BEDÖMT`, `PÅGÅR`, `PRÖVAT`, `OMSTRITT` eller `OLÖST`.
`PRÖVAT` betyder en dokumenterad identitetsbedömning, inte att varje uppgift
är säker. Livsbildsläge: `EJ BEDÖMT`, `PÅGÅR`, `GENOMGÅNGEN`, `AVGRÄNSAD`
eller `INTEGRITETSMINIMERAD`. Källstrategiläge: `EJ BEDÖMT`, `PÅGÅR` eller
`GENOMGÅNGEN`. Kontraktsgranskning: `EJ GRANSKAD`, `UNDERKÄND` eller
`GODKÄND`. Dessa fält beskriver granskningen och ändrar inte äldre parserns
relationer eller A-poststatusar.

`GODKÄND` kräver en daterad, beläggslänkad bedömning av **varje PK-01–12**,
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

Använd [personmallen](templates/person.md) och
[profilmallen](templates/research-profile.md). Vid forskning på en befintlig
akt ska profilen finnas eller skapas som första lokal inventering inom
uppgiften. Ange vilka PK-krav uppgiften behandlar och vilka som återstår.
Ett begränsat källprov får avslutas utan personens GODKÄND, men dess olösta
krav ska vara synliga och beslutat följdarbete ligga i Wotan.
