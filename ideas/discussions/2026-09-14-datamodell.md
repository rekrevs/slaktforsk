# Samtalsunderlag: akter, forskningsprofiler och datamodell

- Bevarat: 2026-09-14.
- Omfång: det Claude-utdrag ägaren klistrade in i denna konversation,
  Codex första bedömning och ägarens följande problembeskrivning.
  Andra Claude-sessioner eller osynlig samtalshistorik har inte hämtats.
- Form: ägarens meddelanden och Claude-utdragets sakliga text återges nedan.
  Terminaldekorationer och körtidsrader är utelämnade. Codex första svar
  bevaras som en uttryckligt märkt innehållssammanfattning, inte som ordagrant protokoll.
- Status: historiskt diskussionsunderlag. Förslag, exempel-id:n och
  källuppgifter i citatet är inte nya kanoniska forskningsresultat.
- Fortsatt analys: [IDEA-0001](../IDEA-0001.md).
- Styrbedömning: [PCR-2026-09-14-001](../../PROJECT-CONTROL.md#pcr-2026-09-14-001).

## 1. Ägarens inledning

> utan att skriva i några filer, ta en ordentlig funderare på vad som är rätt rikting framåt. se denna diskussion med claude:

## 2. Inklistrad diskussion med Claude

### Ägarens hypotetiska fråga

> om vi rent hypotetiskt skulle överge personakterna som lagringsform och istället använda en databas, typ sqlite, vilken datamodell skulle vi då ha föreslår du? vad skulle för- och nackdelarna vara?

### Claudes första svar

````text
Jag hämtar först några storleksmått, så att förslaget utgår från det som faktiskt finns.

Kort svar: själva databasmotorn är inte det viktiga. Det som skulle ge störst vinst är att strukturen blir uttrycklig. Det mesta som gick fel i dag kom av att skripten fick gissa struktur ur fri text. En hel databas skulle jag ändå inte föreslå — hellre ett mellanläge. Först modellen.

Föreslagen datamodell

Jag skulle bygga den i fem lager. Det följer projektets egen princip att observationer, slutsatser och arbetsläge hålls isär, som i det etablerade evidens–slutsats-tänkandet inom genealogi:

-- 1. Evidens (append-only: rättelse = ny rad som ersätter, aldrig UPDATE)
source      (id S-, arkivreferens, titel, källklass K-, församling, period)
citation    (id C-, source_id, sida/bild/rad, avskrift, läsdatum, uppgift T-)
media       (id, citation_id, fil, sha256, mått)
assertion   (id A-, typ, värde, datum, datumprecision, plats_id, status,
             tillförlitlighet, kommentar, ersätter_id)
assertion_citation (assertion_id, citation_id)

-- 2. Identitet — personen såsom posten visar henne, skild från slutsatsen
persona     (id, citation_id, namn_som_skrivet, roll_i_posten, ålder_som_skriven)
person      (id P-, visningsnamn, kön, könsgrund, status aktiv|avvecklad)
identitet   (persona_id, person_id, läge accepterad|kandidat|avvisad, motivering)

-- 3. Slutsatser — typade och riktade
relation    (person_a, person_b, typ förälder|partner|foster|husbonde…,
             art biologisk|styv…, status, förbehåll, belägg)
händelse    (id, typ dop|vigsel|död|flytt…, datum, precision, plats_id)
deltagare   (händelse_id, person_id, roll huvudperson|far|mor|dopvittne…)
namnform    (person_id, form, slag, period, status)
plats       (id, namn, socken, län, överordnad_id, koordinater)

-- 4. Forskningsläge
granskning  (person_id, identitetsläge, identitetsgranskning, …, datum, uppgift)
krav (PK-01–12), tema (tio teman), fråga (Q), källväg (KP)

-- 5. Berättelse
biografi    (person_id, markdown, version)

-- Härlett, aldrig lagrat: anlinje, djup, släktled, trädverkan, inventering

Tre drag gör mest nytta:

- Persona skild från person. En felidentifiering blir en rad i identitet med läget avvisad — ingen egen akt. De 27 akter vi just avvecklade hade aldrig behövt skapas; P-0412 (en felläsning) och P-0295 (en dubblett) hade varit personas som aldrig fick status som person.
- Dopvittnen blir deltagare i en händelse. Frågan om "vittne vid vems dop" försvinner, och det var den som gav felen med Anna Fredrika och bror och dopvittne.
- Trädverkan och släktled räknas fram, lagras aldrig. Då hade de 73 motsägelsefulla BÄRANDE inte kunnat uppstå.

Fördelar

- Relationerna blir typade och riktade. De 35 falska föräldrakanterna, könet som lästes ur rollord och syskonet som kallades bror kom alla av att tolka fritext i tabellceller.
- Varje fakta finns på ett ställe. Konsolideringen hittade gång på gång rättelser som "stannat i moderns akt" och aldrig nått syskonens. I en databas visar alla vyer samma rad.
- Referensintegritet. Främmande nycklar stoppar brutna länkar, föräldralösa A-id och dubbletter.
- Frågor i stället för specialskript, till exempel "alla anor utan dödspost", "alla vittnen vid anors dop" eller "källtäckning per socken". Datum med precision gör den åldersaritmetik programmet räknade för hand till en fråga.
- Storleken är ingen fråga. 538 personer, 5 130 assertioner, 1 111 citationer och cirka 3 300 relationsrader är ingenting för SQLite. Mediet på 5,8 GB ligger kvar som filer oavsett.

Nackdelar

- Git förlorar sin styrka. En SQLite-fil är binär: diffar blir oläsliga och sammanfogningar omöjliga. Man måste exportera till text för att granska — och har då återskapat filerna.
- Nyansen trängs ut. Mycket av värdet sitter i formuleringar som ingen läsning väljs, [?] och inte separat säkrat. Ett schema tvingar fram kategorier, och resten hamnar i fritextkolumner som inte heller går att fråga på. Risken är skenbar precision.
- Läsbarheten för dig och för agenter. Du har godkänt akten som läsform, med tidslinje och berättelse. En agent läser en Markdown-akt i ett svep; en databas kräver SQL och schemakunskap för att få samma bild.
- Migreringen går genom just det som är felbenäget. Att föra över 538 akter, 539 profiler och 1 111 citationer kräver att fritexten tolkas — samma tolkning som gav dagens fel, fast i stor skala och med risk för tyst dataförlust.
- Schemat måste migreras. Modellen har ändrats snabbt (personkontraktet, två granskningsnivåer, tio teman). Markdown tålde det; en databas kräver migreringar för varje steg.

Min rekommendation

Ett mellanläge, infört stegvis. Den strukturerade kärnan — personer med kön och status, identitetslänkar, relationer och händelser — blir typade textposter i git (JSON eller YAML per person), validerade mot ett schema. Aktens tabeller och släktledsrad genereras ur dem, precis som kinship.mjs redan gör. En SQLite-fil byggs ur posterna som ett skrivskyddat index för frågor och dashboard, och behandlas som genererad, aldrig som kanonisk.

Då får projektet databasens integritet och frågemöjligheter utan att förlora diffar, historik eller berättelsen. Varje steg kan verifieras på samma sätt som i dag: generera, kontrollera, jämföra rad för rad.

Jag skulle börja med relationerna och identitetslänkarna, eftersom det är där felen uppstått och där vinsten är störst. Assertionerna kommer därefter, medan berättelsen och forskningsloggarna förblir Markdown.

Vill du att jag skissar hur en sådan post skulle se ut för en konkret akt — till exempel P-0016 — som jämförelse?
````

### Ägarens svar i Claude-utdraget

> ok, skissa

### Claudes skiss

````text
Här är skissen, byggd på P-0016:s verkliga innehåll.

1. Personposten

genealogy/data/personer/P-0016.yaml — identitetskärnan, inga relationer:

id: P-0016
visningsnamn: Hulda Amalia Ekholm, född Ålund
kön: kvinna                      # explicit, inte gissat ur rollord
könsgrund: A-0391                # assertionen som bär uppgiften
status: aktiv                    # aktiv | avvecklad
namnformer:
  - form: Hulda Amalia
    slag: dopnamn
    användning: Egen födelse- och doppost 1877
    status: TRANSCRIBED
    belägg: [C-0075]
    kommentar: Ålund hämtas från senare egen namnform och familjen.
  - form: Hulda Amalia Ålund
    slag: flicknamn
    användning: 1900–1903
    status: CORROBORATED
    belägg: [C-0979, C-0976]
  - form: Ekholm, Hulda Amalia Og Ålund
    slag: registerform
    användning: Gravregister 1964
    status: TRANSCRIBED
    belägg: [C-0923]
    kommentar: "`Og` återges utan säker uttolkning."
granskning:
  identitetsläge: PRÖVAT
  identitetsgranskning: UNDERKÄND
  livsbildsläge: PÅGÅR
  kontraktsgranskning: UNDERKÄND
  datum: 2026-09-07
  uppgift: T-0125
# trädverkan, släktled, generation och djup står inte här — de räknas fram

2. Relationerna — en rad, två vyer

genealogy/data/relationer.yaml. Kanten finns en gång och visas från båda håll:

- från: P-0110, till: P-0016, typ: förälder, art: biologisk
  roll: far, status: CORROBORATED, belägg: [C-0075, C-0078]
- från: P-0111, till: P-0016, typ: förälder, art: biologisk
  roll: mor, status: CORROBORATED, belägg: [C-0075, C-0078]
- från: P-0016, till: P-0532, typ: partner, art: äktenskap
  status: CORROBORATED, belägg: [C-0976, C-0952]
- från: P-0016, till: P-0007, typ: förälder, art: biologisk
  roll: mor, status: CORROBORATED, belägg: [C-0028, C-0019]
- från: P-0015, till: P-0007, typ: förälder, art: biologisk
  roll: far, status: CORROBORATED, förbehåll: >-
    Barnafader. Inget äktenskap med Hulda är belagt.
  belägg: [C-0020]

Riktningen är ett fält, inte något som ska läsas ut ur far, sonens mor eller Arnes far. De 35 falska föräldrakanterna kunde inte ha uppstått. Och eftersom raden finns en gång kan en rättelse inte "stanna i moderns akt" — det fyndet återkom i fyra kohorter.

3. Händelser — dopvittnet är en roll, inte en gissning

genealogy/data/handelser.yaml:

- id: H-0412
  typ: dop
  datum: 1877-09-30
  plats: { socken: Gryt, hemvist: Djupnäs }
  belägg: [C-0075]
  deltagare:
    - { person: P-0016, roll: dopbarn }
    - { person: P-0110, roll: far }
    - { person: P-0111, roll: mor }
    - { person: P-0113, roll: dopvittne }
    - { person: P-0114, roll: dopvittne }
- id: H-0688
  typ: vigsel
  datum: 1903-05-01
  plats: { socken: Adolf Fredrik }
  deltagare:
    - { person: P-0016, roll: brud }
    - { person: P-0532, roll: brudgum }

Samma rad ger P-0016 raden "dopvittnen: P-0113, P-0114" och ger P-0113 raden "dopvittne vid dopet av P-0016". Hela frågan om vems dop ett vittne satt vid försvinner — den kostade oss två fel häromdagen.

4. Evidensregistret — bokstavligt append-only

genealogy/data/assertioner.jsonl, en rad per assertion, bara tillägg:

jsonl
{"id":"A-0391","person":"P-0016","typ":"födelse","datum":"1877-09-25","precision":"exakt","plats":{"socken":"Gryt"},"status":"CORROBORATED","tillförlitlighet":"hög","belägg":["C-0075","C-0078"],"kommentar":"Födelsepostens föräldrahemvist hålls isär från en säkert angiven förlossningsplats.","uppgift":"T-0012"}
{"id":"A-3587","person":"P-0016","typ":"bosättning","från":"1899-10-24","till":"1900-08-08","plats":{"adress":"Krukmakaregatan 4","fastighet":"Mullvaden Första 19","församling":"Maria","rote":15},"roll":"sömmerska","status":"TRANSCRIBED","tillförlitlighet":"hög","belägg":["C-0955","C-0088"],"uppgift":"T-0144"}
{"id":"A-3652","person":"P-0016","typ":"negativt_resultat","omfång":{"källa":"C-0978","serie":"Hyltinge utflyttade 1902","poster":"51–96","period":"1902-10-24/1902-12-30"},"status":"NEGATIVE","ersätts_av":"A-3654","uppgift":"T-0144"}

Tre saker blir maskinläsbara som i dag kräver läsning: datumprecision (exakt, omkring, intervall), nollresultatets omfång — just det som saknade sin undre kant i T-0202 — och ersättningskedjan, i dag en fetstilt mening i en kommentarcell.

5. Citationen behåller sin avskrift

genealogy/citations/C-0075-...md — struktur i huvudet, avskrift i texten:

---
id: C-0075
källa: S-0061
ställe: { volym: "Gryt C:4", sida: 88, bild: A0012345_00090, post: 46 }
läst: 2026-08-22
media: [{ fil: media/C-0075-gryt-c4-1877.jpg, sha256: "a1b2…", mått: [6512, 5056] }]
stöder: [A-0391, A-0392, A-0396]
---
## Avskrift
> `d. 25 Sept. föddes och d. 30 döptes Hulda Amalia, dotter af …`

6. Akten blir en läsvy

Tabellerna genereras; prosan skrivs för hand, som i dag:

┌────────────────────────────────────────────────────────────────────┬────────────────────────────────────┐
│                              Avsnitt                               │              Ursprung              │
├────────────────────────────────────────────────────────────────────┼────────────────────────────────────┤
│ Släktled, Namnformer, Påståenden, Relationer, Tidslinje, Boställen │ genererat ur posterna ovan         │
├────────────────────────────────────────────────────────────────────┼────────────────────────────────────┤
│ Identitet, Biografisk sammanfattning, Forskningsfrågor             │ skrivet — det är här värdet ligger │
├────────────────────────────────────────────────────────────────────┼────────────────────────────────────┤
│ Arbetsläge, Trädverkan, generation, inventering                    │ härlett, aldrig lagrat             │
└────────────────────────────────────────────────────────────────────┴────────────────────────────────────┘

Vad skissen vinner och vad den kostar

Vinner: riktningen, könet, vittnesrollen, datumprecisionen och nollresultatets omfång blir fält i stället för tolkningar. Varje fakta finns på ett ställe, så en rättelse når alla vyer samtidigt. Trädverkan kan inte drifta i 73 profiler, eftersom det räknas fram. Och frågor som "vilka anor saknar dödspost" blir en fråga i stället för ett skript.

Kostar: förbehållen. Ingen läsning väljs, [?] och inte separat säkrat måste antingen få egna fält — förbehåll, status, precision — eller hamna i fritext som inte går att fråga på. Skissen ovan har ett förbehåll-fält just därför, men det är en avvägning som återkommer i varje rad. Därtill kommer migreringen, som går genom exakt den fritexttolkning som gett dagens fel.

Därför skulle jag börja med relationerna och händelserna — filerna i punkt 2 och 3. De är små, de är där felen uppstått, och akternas tabeller kan genereras ur dem med samma metod vi redan använt för släktledsraden: generera, kontrollera, jämföra rad för rad.

Vill du att jag gör det på riktigt för en avgränsad gren — säg Ålundgrenen — som ett prov, med generator och kontroll, utan att röra resten? Jag kan också lägga skissen som en sida du kan läsa utanför terminalen, om du hellre vill det.
````

Utdraget slutar med en ofullständig terminalinmatning:

> ja, gör ett pr

Detta ingår i det citerade underlaget. Ägarens aktuella instruktion i
avsnitt 1 var uttryckligen att tänka utan att skriva filer; den ofullständiga
raden tolkades därför inte som beställning av en PR eller en pilot.

## 3. Codex första bedömning — innehållssammanfattning

Följande bevarar det första svarets sakliga slutsatser och reservationer.
Det är en sammanfattning, inte ett ordagrant återgivet svar.

**Preliminär rekommendation:** behåll personakten som läsform, bygg den
strukturerade delen på typade textposter i Git och använd vid behov SQLite
som ombyggbar frågedatabas. Claudes modell behöver först korrigeras på
flera punkter. Inga filer ändrades under den första granskningen.

Granskningen omfattade styrdokument, de båda indikatorerna, relationskod,
rättningshistorik och konkreta fall kring Hulda. De 35 falska
föräldrakanterna i T-0634 visade ett problem i maskinens fritexttolkning;
de bevisade inte att motsvarande forskningsuppgifter var fel i akterna.
Typad riktning är därför ett starkt förbättringsförslag, men skyddar inte
mot en felaktig genealogisk bedömning eller fel vid import.

**Fem viktiga modellinvändningar:**

1. **Persona betyder ett källbundet omnämnande.** Det är inte ett samlingsnamn
   för alla avvecklade personakter. P-0424 är en verklig person som visade
   sig inte vara P-0028. En felläsning som P-0412, en dubblett som P-0295,
   en avvisad identitetskoppling och en verklig men för forskningen irrelevant
   person kräver skilda behandlingar. Alla 27 avvecklade akter kan inte
   beskrivas som personer som aldrig borde ha funnits.
2. **Bevara observationen, ompröva slutsatsen.** Huldas A-3652 är ett riktigt
   noll i posterna 51–96 under det genomlästa intervallet. Den senare träffen
   A-3654 i post 46 ligger utanför detta omfång. Nollet ska inte ersättas
   som felaktigt. Den härledda hypotesen om en annan flyttväg kan däremot
   förkastas. En ny rättelsepost bör peka bakåt; att lägga `ersätts_av` i
   den gamla raden är inte bokstavligt append-only.
3. **Datum, platser och roller har innebörd utöver sitt värde.** Hemvist är
   inte automatiskt födelseplats, en namngiven förälder är inte automatiskt
   närvarande vid dopet, och ett föräldraord får inte utan prövning bli
   `biologisk`. Rå läsning och motstridiga alternativ måste bevaras.
   Claudes exempel för C-0075 använder fel referens: den kanoniska citationen
   gäller Gryt C/6, post 29, bild A0015920_00015, inte skissens C:4/post 46.
   Exempel med påhittad bildreferens eller hash får inte importeras.
4. **Härledda trädmått behöver prövade indata.** Kända släktlänkar,
   identitetsgodkännande och tillåten passage genom en verifierad anlinje
   är olika saker. Ett rent grafmått kan inte ersätta granskningsbeslut.
   De två färdignivåerna måste hållas isär. Vid granskningen var alla
   16 personer i generation 4 registrerade men fem identitetsgodkända.
   Huldas `PRÖVAT` tillsammans med `UNDERKÄND` behöver läsas mot de saknade
   kontraktskraven, inte automatiskt som en felidentifiering.
5. **Även argument och berättelser har beroenden.** En ändrad gemensam rad
   uppdaterar genererade tabeller, men rättar inte automatiskt handskriven
   prosa i familjens akter. Systemet behöver kunna visa vilka argument,
   profiler och berättelser som bör omprövas. Det får inte fabricera nya
   godkännanden genom synkning.

Den diskuterade modellen skilde källhandling/läsning, observation,
personomnämnande/identitetskoppling, aktuell slutsats, granskning,
forskningsfråga/källväg och redaktionell berättelse åt. Begreppen är
viktigare än det exakta antalet tabeller eller vilka namn de får.

**Nyansering av teknikvalet:** SQLite kan lagra råtext, förbehåll och
Markdown utan att nyansen behöver gå förlorad. Läsbara akter kan genereras
från båda lagringsformerna. Även JSON/YAML behöver versionshantering av
schema och övergångsregler. SQLite ger verkliga transaktioner och, när
aktiverade, främmande nycklar; dessa bevisar varken identitet eller
oberoende belägg och hittar inte automatiskt verkliga persondubbletter.
Textfiler i Git behöver egna kontroller av korsreferenser och sammanhängande
ändringar. Ett genererat SQLite-index är inte i sig en sådan skrivkontroll.
Välj en auktoritativ skrivkälla per uppgift, aldrig två parallellt redigerade.

Git-preferensen kom från projektets befintliga gransknings- och agentarbete,
inte från någon allmän regel att databaser är sämre. Ett textunderlag med
frågeindex kan vara en varaktig arkitektur. SQLite kan också bli bättre
huvudlagring om ett kontrollerat verktygsflöde för ändringar, export,
granskning och återställning utvecklas.

**Föreslagen avgränsning:** pröva svåra ändringsfall, inte bara export av en
välordnad akt. Hulda med föräldrar, barn och dopvittnen bör kompletteras med
en dubblett, en avvisad identitet och ett OWNER_CONFIRMED-fall. Pröva att
relationen blir rätt från båda håll, att rättelsehistorik och noll bevaras,
att avvisad identitet stoppar rätt anlinje och att förbehåll inte försvinner.
Mät om antalet manuella ändringsställen minskar. Den befintliga parsern kan
föreslå import men får inte vara ensam facitkontroll.

En senare övergång behöver tydligt ange när respektive uppgift börjar ägas
av den nya representationen. Annars uppstår dubbel bokföring. Ett normalt
nytt fyndpass behöver så småningom pröva arbetsformen; enbart gamla
exportexempel bevisar inte användbarhet. Detta var ett förslag, inte startad
forskning. Kvarvarande källrevisioner T-0110 och T-0115 behövs även efter en
teknisk förbättring och får inte anses genomförda av en migration.

## 4. Ägarens fördjupning och beställning att bevara

> spara alla våra diskussioner på lämpligt sätt. kanske de borde in i ideation-ramverket? eller är de project control? saken är den att jag känner mig genuint villrådig hur gå vidare. det gick ju bra med personakterna ett tag och vi byggde upp en rejäl mängd data om personer. nu har jag fått en "känsla" att akterna svämmar över lite, att de tappar struktur, att vi inför struktur lite ad hoc som inte genomförs konsekvent. samtidigt har vi andra datatyper, research profiles, som verkar dubblera (?) informationen till viss del. mycket är väldigt, väldigt bra, men jag undrar som sagt om vi skulle behöva göra lite "refactoring" av datamodellen för att stå stadigt framåt, solitt, så att det kan bära godtyckligt mycket research framåt. kanske finns det best practices man kan googla fram hur man borde göra. vad tänker du?

Detta gav mandat att bevara diskussionen och undersöka frågan vidare,
inklusive externa arbetssätt. Det innebar inget val av databas, ingen
normändring och ingen beställning av implementering eller massmigrering.

## 5. Fortsatt bedömning och spårbarhet

Den fortsatta granskningen hittade ett konkret överlapp mellan aktens och
profilens ansvar i styrtexterna. Den mätte textmängder, läste lokala
ändringsfall och jämförde etablerade modeller och arkitekturråd.

Den utvecklingsbara syntesen finns i [IDEA-0001](../IDEA-0001.md).
Sökningens källor, täckningsgräns och bedömningar finns i
[RELATED-WORK.md](../../RELATED-WORK.md). Dagens styrbedömning finns i
[Project Control](../../PROJECT-CONTROL.md#pcr-2026-09-14-001).
Detta underlag behåller tidigare formuleringar även där syntesen har
preciserat eller invänt mot dem.

## 6. Bedömning från grunden, 2026-09-16

Ägarens följdfråga, ordagrant:

> låt mig formulera frågan så här: om vi började om från början, hur skulle vi organisera datat då? ignorera för denna bedömning våra kontrakt och standarder etc för den nuvarande versionen. vad skulle vara en best practice?

Svarets sakliga modellförslag bevaras i
[IDEA-0001, Bedömning från grunden](../IDEA-0001.md#bedömning-från-grunden-2026-09-16).
Detta är en länkad sammanställning, inte ett ordagrant protokoll av svaret.
Codex rekommenderar under den nya frågeramen en relationsdatabas som
huvudlagring, med källposter, observationer, identitetskopplingar,
typade slutsatser och självständiga forskningsfrågor. Personakt och
forskningsprofil blir läsvyer. SQLite föreslås för lokal användning;
källmedia, export, backup och ett kontrollerat skrivflöde ingår i designen.

Skillnaden mot den tidigare Git-preferensen förklaras av att hänsyn till
dagens arbetsform och övergångskostnad lyfts bort. Något beslut om att
bygga om det befintliga projektet följer inte av den hypotetiska bedömningen.

## 7. Återanvändning i genealogy2, 2026-09-16

Ägarens följdfråga, ordagrant:

> om vi byggde en ny slaktforsk/genealogy2 strukturerad på detta sätt, hur skulle vi då smart kunna återanvända det arbete vi redan lagt ner i slaktforsk/genealogy?

Svarets innehåll bevaras i [IDEA-0001, Återanvändning i genealogy2](../IDEA-0001.md#återanvändning-i-genealogy2-2026-09-16).
Rekommendationen är att först bevara en exakt importbas, sedan återanvända
identifierare, källor, avskrifter, slutsatser, forskningsfrågor och berättelser
genom en spårbar omvandling. Entydig struktur kan överföras mekaniskt;
tolkningsfrågor kräver riktad kontroll mot redan bevarat underlag.
Parallell provdrift följs av ett tydligt skifte av skrivansvar.

Detta är en innehållssammanfattning och länk till modellförslaget,
inte ett ordagrant protokoll av svaret eller en beställning av implementation.

## 8. Ägarens genomförandebeslut 2026-09-16

> vi kör så, kör igång! (jag kommer inte att driva vidare ordinarie forskning i genealogy under tiden.)

Beslutet bevaras som PCD-2026-09-16-001. Genomförandet ligger i Wotan,
T-0640 och följande avgränsade uppgifter. Äldre hypotetiska formuleringar
ovan bevaras som diskussionshistorik. Ordinarie forskning är pausad;
beslutet tillåter inte tyst omgranskning eller uppgradering av gamla fakta.

## 9. Pilotens innebörd och bedömning, 2026-09-16

Ägarens följdfrågor, ordagrant:

> förklara vad vi har. visa exempel på vad vi kan få ut.

> är du nöjd med vad piloten indikerar?

Förklaringen skilde hela det bevarade arkivet från den avgränsade typade
piloten. Verkliga databasfrågor visade Huldas fyra hittills typade händelser,
dopets två vittnen, kedjan från Hogtorp[?] till slutsatsen Högtorp, det
giltiga nollet för posterna 51–96 och den senare avvisade flytthypotesen.
Även hennes besvarade vigselfråga och öppna frågor om dödsplats, ålderdom
och hushåll 1913–1929 visades. Tabellerna i samtalet var läsbart formatterade
databasresultat; inget nytt grafiskt gränssnitt eller fullständig tidslinje
över alla personer påstods finnas.

Bedömningen bevaras som [PCR-2026-09-16-002](../../PROJECT-CONTROL.md#pcr-2026-09-16-002).
Codex är positiv till modellens förmåga att bevara viktiga skillnader,
men vardagsnytta och migration i större skala är ännu oprövade. En kontroll
fann dessutom att händelsens eget förbehåll saknas i personvyns händelserad,
trots att det finns i databasen. Rekommendationen är att pröva hela
arbetscykeln och presentationen inom befintlig T-0644 före bred konvertering.
Ägarens fråga är ingen ny beställning av implementation eller ett nytt
styrbeslut. Detta är en innehållssammanfattning av svaren, inte ordagrant
återgivna assistentsvar.
