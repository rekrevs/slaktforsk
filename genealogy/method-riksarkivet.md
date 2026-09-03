# Metod: att nå Riksarkivets material reproducerbart

Detta dokument beskriver hur projektets källbilder och volymuppgifter hämtas
utan manuellt bläddrande, så att varje citatpost går att kontrollera i
efterhand. Metoden verifierades 2026-08-20 genom att en tidigare sparad bild
(C-0067) laddades ned på nytt och gav identisk SHA-256-kontrollsumma.

## Ägarregel 2026-09-03: Riksarkivets MCP först där den täcker behovet

När en ny Codex-session har tillgång till den globalt konfigurerade
MCP-servern `riksarkivet` ska dess verktyg användas som första lämpliga ingång
för upptäckt, sökning, registerrouting och snabb interaktiv inspektion. Det
gäller bland annat strukturerad person- och registersökning, arkivmetadata,
transkriberat material, guider, manifest och dokumentvisning. När en exakt
reproduktions- eller bildnyckel väl är känd följer arbetet lagerreglerna nedan;
MCP-viewern är då inte ett obligatoriskt mellanled. Riksarkivet och dess
arkivposter, volymer och reproduktioner är fortfarande de källor som ska
citeras.

Ett MCP-svar ska därför så långt möjligt följas till och dokumenteras med
arkivbildare, referenskod, serie, volym, sida eller bild, beständigt id och
originalbild enligt projektets vanliga provenanskrav. Ett negativt MCP-resultat
är endast ett avgränsat sökresultat inom verktygets angivna täckning, inte ett
bevis för att personen eller handlingen saknas i arkivet.

Om MCP-servern inte är tillgänglig i sessionen, saknar ett relevant verktyg
eller inte exponerar tillräcklig metadata eller bildåtkomst, fortsätter arbetet
med den reproducerbara API-/JSON-LD-/IIIF-ordningen nedan. Chrome förblir den
snäva sista reserven. Ingen onödig information om levande personer ska skickas
till MCP-servern, och reglerna om inloggning och ALTCHA/CAPTCHA ändras inte.

### Operativ lager- och bevismodell

`MCP först` är en regel om första lämpliga ingång, inte ett krav att all senare
läsning eller bildhantering ska gå genom MCP. Arbetet skiljer på följande lager:

| Lager | Huvuduppgift | Vad lagret kan belägga | Normal övergång |
|---|---|---|---|
| MCP-sökning och specialverktyg | upptäckt, bred sökning, stavningsprövning, registerträffar och routing till ort, arkiv, serie eller volym | de fält som en namngiven register-, transkriptions- eller ortspost faktiskt återger; annars endast en kandidat eller sökobservation | följ positiva träffar till beständigt id, referenskod och när möjligt original |
| API, JSON-LD, OAI och IIIF-manifest | hierarki, metadata, reproduktions-id, canvasföljd samt avgränsning av år, församling eller handling | källans identitet och det dokumenterade undersökningsomfånget, men inte att en viss person står på en sida | gå till de exakta bildytorna och bevara avgränsningens start- och slutkontroller |
| Transkription eller originalbild | läsning och sakbelägg | en MCP-/registertranskription bär bara sina uttryckliga fält; för kyrkoboks- och andra sidbundna personpåståenden är den visuellt lästa originalbilden normal bevisgrund | skapa källpost, citat, påstående och uttrycklig evidensbedömning |
| Inloggad katalog eller Chrome-visare | snäv åtkomstreserv när publikt reproduktions-id saknas, direktbild ger `401`/`403` eller katalogen ensam exponerar nästa nyckel | endast det som faktiskt läses i katalogen eller originalbilden; åtkomstläget i sig är inget källnoll | återgå om möjligt till beständig metadata eller lokal, checksummad originalkopia |

MCP-burna Rosenberg-, TORA-, sjömanshus- och andra registerposter kan alltså
vara källor för avgränsade orts- eller registerpåståenden. De får inte utan egen
personbärande information omvandlas till bostad, arbete, identitet eller
släktskap. Ett IIIF-manifest belägger på motsvarande sätt volymens struktur och
ett sveps omfattning, medan den lästa bilden bär sidans personuppgifter.

### Negativa MCP-resultat och kontrollfrågor

Innan ett MCP-noll bevaras ska verktygets uppgivna täckning granskas och, när
det är möjligt, minst en känd positiv kontroll köras i samma dataset och nära
målfrågans geografi, tid och posttyp. Om även kontrollen ger noll klassificeras
utfallet som ett täcknings- eller frågesynlighetsresultat, inte som frånvaro av
personen eller handlingen. Ett filtrerat noll ska vid behov prövas mot en
ofilterad namnfråga och relevanta historiska stavningar; filterfälten kan vara
snävare eller ha annan normalisering än fritexten. Alla sådana omprov ska
redovisa exakt fråga och får inte sammanföra homonyma träffar.

### MCP-viewer eller direkt IIIF

MCP:s viewer får användas för snabb orientering, enstaka bildkontroll eller när
den exponerar en annars saknad länk. När reproduktions-, manifest- eller
bild-id redan är känt föredras den direkta IIIF-pipelinen för systematiska
svep, deterministisk år→bild-avgränsning, fullupplösta original, beskärningar,
rotationer, kompositer och lokal kontrollsummering. Detta är nästa lager efter
MCP-upptäckten och strider därför inte mot `MCP först`.

## Ägarregel 2026-08-29: API före Chrome

Riksarkivets API-lager ska alltid prövas före Chrome där det är möjligt:

1. sök-API för arkiv, serie och volym;
2. JSON-LD och `schema:hasPart` för hierarkin;
3. IIIF-manifest, `info.json` och Image API för innehåll och fulloriginal;
4. först därefter inloggad katalog/bildvisare om bildlänk saknas eller om
   IIIF ger ett dokumenterat `401`/`403`.

Chrome ska då användas så snävt som möjligt, exempelvis för att lösa ett
reproduktions-id som API/JSON-LD utelämnar eller för att hämta en bild som
direkt-IIIF spärrar. Varje övergång ska journalföra vad API-lagret gav, exakt
åtkomstfel och en återaktiveringsväg. ALTCHA/CAPTCHA löses inte utan ägarens
uttryckliga bekräftelse.

## Verifierad Chrome-reservmetod 2026-08-28

Den tidigare fungerande Chrome-metoden har nu reproducerats i en helt ny
browser-runtime med den installerade pluginversionen **26.820.60940**:

1. ladda pluginens `browser-client.mjs` och anslut med
   `agent.browsers.get("chrome")`;
2. namnge sessionen och skapa alltid en ny styrd flik med
   `chrome.tabs.new()`;
3. navigera direkt till en katalog- eller bildvisar-URL;
4. kontrollera DOM-texten `Inloggad som: ...` innan källarbete börjar;
5. om Riksarkivets ALTCHA-ruta visas, stanna och begär ägarens uttryckliga
   bekräftelse innan någon `Jag är inte en robot`-kontroll används;
6. använd bildvisarens semantiska kontroller, bland annat `Nästa bild`,
   sidväljaren och `Ladda ner`;
7. välj `Hela bilden …px (jpg)`, kontrollera filen i `~/Downloads`, kopiera
   den till `genealogy/media/` och registrera dimensioner och SHA-256.

Testet gav tre nya fulloriginal i 5 712–6 256 bildpunkters bredd och en
inloggad DOM-session. Ingen AppleScript-styrning, kakextraktion,
profilkopiering, sandboxflykt eller övertagning av en gammal flik användes.
När en browser-bindning väl finns ska den återanvändas; ett nytt
`get("chrome")` görs bara efter ett uttryckligt frånkopplingsfel.

## Åtkomstlägen

- **Fritt** utan inloggning: kyrkoböcker digitaliserade i Riksarkivets äldre
  batcher, i praktiken material fram till omkring sekelskiftet 1900, samt
  folkräkningarnas bildutdrag.
- **Inloggning krävs** för yngre volymer, exempelvis Hyltinges
  församlingsböcker 1918–1927 och de SCB-utdrag och folkräkningsbilder som
  använts i C-0015, C-0019, C-0020 och C-0028. Anrop mot dessa ger `401`.
  Sådana bilder måste hämtas i en inloggad webbläsarsession.

Ett `401` är alltså ett åtkomstbesked, inte ett tecken på att bilden saknas.
Notera det i forskningsloggen i stället för att tolka det som en arkivlucka.

## Sökning efter arkiv, serie och volym

Riksarkivets söktjänst `sok.riksarkivet.se/nad` skyddas av captcha och kan inte
skriptas. Använd i stället det öppna sök-API:et:

```
https://data.riksarkivet.se/api/records?text=<fritext>&limit=<n>
```

- Fritext på arkivnamn ger arkivbildarens referenskod, exempelvis
  `Björkviks kyrkoarkiv` → `SE/ULA/10119`.
- Fritext på referenskod plus serie listar volymerna med datering och, när de
  är digitaliserade, ett IIIF-manifest under `_links.image`.
- Teckenkodning: skicka söksträngen URL-kodad, exempelvis med
  `curl -G --data-urlencode`. Rå `ö` i en URL ger noll träffar.
- JSON-LD-slutpunkten kan ge ett missvisande `403` utan innehållsförhandling.
  Skicka både en vanlig webbläsar-`User-Agent` och
  `Accept: application/ld+json`; omprovet gav `200` för Sättna A II a/6,
  A II a/8 och A II a/10 den 2026-08-30.
- Det finns även indexerade personposter för en del församlingar:
  `/api/records/birthrecords` med `first_name`, `place`, `year_min`, `year_max`
  med flera. Täckningen är ojämn och tyngdpunkten ligger i södra Sverige, så
  noll träffar där säger ingenting om huruvida posten finns.

Ett katalogiserat `rico:hasRepresentationType` = `Image` i JSON-LD är inte
ensamt en bildpekare. Sättna A II a/10 visar ett viktigt mellanläge:
sök-API:t saknar `_links.image`, JSON-LD:s bildrepresentation saknar URI och
OAI-EAD anger sekretess utan digital länk. Den inloggade katalogposten kan då
fortfarande kräva människoverifiering. Klassificera detta som **saknat
publikt reproduktions-id före IIIF**, inte som `401` mot en känd bild och
inte som bevis för att volymen är odigitaliserad. Gissa inte att luckor i en
närliggande batchnummerserie är giltiga bild-id:n; de kan ge `Not Found`.

I IIIF Presentation API 3 ligger canvasföljden under manifestets `items`,
medan en församlings- eller handlingsrange kan ange endast sin första canvas
under `structures`. Avgränsa då ett intervall från den aktuella rangens start
till bilden omedelbart före nästa start av samma handlingstyp. Sävars
dödboksutdrag 1868 verifierades på detta sätt som `_00206`–`_00214`, eftersom
nästa dödrange, Holmön, börjar på `_00215`. Kontrollera alltid att nästa range
är semantiskt jämförbar; en annan handlingstyp får inte användas som gräns.

### Äldre Arkis-UUID och publikt trädsvar

Ett verifierat reservspår finns när en exakt JSON-LD-post anger
bildrepresentation men utelämnar reproduktions-id. Riksarkivets egen
katalog kan i sin omdirigeringsadress till människoverifieringen exponera
postens äldre Arkis-UUID. Läs endast adressen; aktivera inte ALTCHA utan
uttrycklig bekräftelse. Den exakta UUID:n kan prövas mot Riksarkivets
publika, läsande trädslutpunkt:

```
https://sok.riksarkivet.se/Tree/SubTree/?postid=Arkis+<uuid>&s=Balder&prependUrl=&id=<uuid>&vol=n
```

Ett bildfilsbarn i svaret kan bära den officiella reproduktionskoden. Denna
kedja verifierades 2026-08-30 för Sävar C/1 (`C0034441`), Sävar A I/1
(`C0034426`) och Lycksele C/3 (`C0034151`). Gissa aldrig UUID eller
reproduktionskod och behandla inte en CAPTCHA-omdirigering som tillstånd att
lösa kontrollen.

### Arkis-UUID till reproduktionsbatch

För en registerpost kan den äldre Arkis-UUID:n även användas mot
Riksarkivets publika, läsande batchsida:

```
https://sok.riksarkivet.se/bildvisning/batchar/<uuid>?referenskod=<referenskod>
```

Den kedjan verifierades 2026-08-31 för registerposten
`SE/RA/870001/3/22/34`. Records-API:t hittade posten och JSON-LD angav två
bildinstansieringar men saknade deras URI:er. Katalogens orörda
ALTCHA-omdirigering exponerade UUID:n
`5da3f6bc-8ffb-4648-a910-07913f8c6360`; batchsidan returnerade därefter de
officiella reproduktionerna `A0043220` och `C0103777`. IIIF-manifesten och
bilderna kunde sedan läsas utan sessionsdata. Chrome användes alltså bara
för att läsa omdirigeringsadressen och diagnostisera den saknade
API-kopplingen; ALTCHA aktiverades inte. Bevara batchsvaret och verifiera
referenskoden mot API-metadata i stället för att gissa någon identifierare.

För dessa äldre `C...`-batcher gav nakna manifest- och bildanrop `403`.
Omprovet 2026-08-31 visar att samma publika resurser kan svara `200` utan
sessionskaka när den egna sidan
`https://sok.riksarkivet.se/bildvisning/<bild-id>` skickas som `Referer`.
Pröva därför hänvisningshuvudet före inloggad bildvisare. En faktisk `401`
från `/v2/` är en annan åtkomstklass och kan fortfarande vara
sessionsbunden. Dokumentera alltid vilket anrop och vilket HTTP-svar som
observerades; läs eller bevara aldrig sessionsdata.

## Volymens innehåll

Manifestet beskriver volymen och ofta dess årsavdelningar:

```
https://lbiiif.riksarkivet.se/arkis!<batch>/manifest
```

- `metadata` ger arkiv, serie, referenskod, datering och källhänvisning.
- `structures` innehåller för kyrkoböcker ofta en avdelning per år med den
  bild där året börjar. Det ersätter blädrande efter rätt uppslag.
- Varje canvas har bild-id och länk till bildvisaren.

## Bildhämtning

Bilder hämtas via IIIF Image API:

```
https://lbiiif.riksarkivet.se/arkis!<bildid>/full/max/0/default.jpg      # full upplösning
https://lbiiif.riksarkivet.se/arkis!<bildid>/full/2000,/0/default.jpg    # översikt
https://lbiiif.riksarkivet.se/arkis!<bildid>/<x>,<y>,<w>,<h>/max/0/default.jpg  # detalj
https://lbiiif.riksarkivet.se/arkis!<bildid>/info.json                   # native bredd och höjd
```

- Regionen anges i bildpunkter; `pct:`-syntax stöds inte och ger `501`.
- Storleken får inte överstiga regionens bredd; annars svarar servern `400`.
  Använd `max` för detaljutsnitt.
- För en batch som ger `403`, skicka dess egen Riksarkivet-sida
  `https://sok.riksarkivet.se/bildvisning/<bild-id>` som `Referer`. Detta gav
  `200` utan sessionskaka för de prövade `C0…`-batcherna. En vanlig
  `User-Agent` ensam ska inte antas lösa felet.
- Spara alltid fullupplösningsbilden i `media/` och för in dimensioner och
  SHA-256 i citatposten.

Folkräkningarnas bilder ligger under ett eget prefix:

```
https://lbiiif.riksarkivet.se/folk!<volymkod>/manifest
https://lbiiif.riksarkivet.se/folk!<volymkod>-<sida>/full/max/0/default.jpg
```

Bild-id i bildvisaren skrivs `Folk_904045-012`, medan IIIF-identifieraren är
`folk!904045-012`. Folkräkningsbilderna är fotograferade utdrag i låg
upplösning, omkring 800 × 1380 bildpunkter, men är läsbara.

### Personregister och SCB:s församlingsutdrag är skilda lager

Riksarkivets officiella registreringsbeskrivning anger att
personregistret för 1860 bara omfattar Jämtlands län och att 1870 bara
omfattar Västerbottens och Norrbottens län. Ett sökformulär som erbjuder år
och ort är alltså inte i sig bevis för att kombinationen är registrerad. Läs
täckningsbeskrivningen före varje nollslutsats; en CAPTCHA före
resultatlistan ska varken lösas automatiskt eller behandlas som den verkliga
forskningsfronten när målområdet saknar täckning.

Det skannade primärmaterialet under *Församlingsutdrag 1860–1940* kan ha
betydligt bredare geografisk täckning. För Stora Lundby 1860 gav
records-API:t den exakta volymen `SE/RA/420401/03/H 1 A/69` och ett vanligt
`arkis!A0056074`-manifest, inte `folk!`-prefixet. Manifestets
församlingsranges anger bara startcanvas. Ett komplett intervall fås genom
att läsa från målrange-starten fram till canvasen omedelbart före nästa
församlingsrange; här `_00027`–`_00044`, eftersom Skallsjö börjar på
`_00045`. Dokumentera båda range-etiketterna och bevara hela intervallet
innan resultatet kallas ett komplett församlingsutdragsnoll.

## Textlager

Vissa volymer har HTR-text via `download/current/text/<batch>?format=text&imageid=<bildid>`.
För de volymer som hittills använts i projektet saknas textlager och svaret
blir `500` med inbäddat `404`. Läsningen sker då direkt i bilden.

## Tre svar, inte två: 200, 401 och 403

### Ingen tyst åtkomstförlust

Ett åtkomstfel mot material som rimligen borde vara öppet får aldrig behandlas
som en tyst nollträff eller ensam motivering för att avsluta en gren. När det
inträffar ska forskaren:

1. meddela ägaren medan arbetet pågår,
2. journalföra exakt tjänst, volym/bild-id, tidpunkt och svar (exempelvis
   HTTP-kod, captcha eller krav på inloggning),
3. skilja åtkomsthindret från en faktisk negativ kontroll i källan, och
4. ange en konkret återaktiveringsväg samt pröva andra lagliga leverantörer
   eller parallella källor innan en terminal status sätts.

Detta gör åtkomstproblem undersökningsbara och ger ägaren möjlighet att hjälpa
till med exempelvis en inloggad session eller en alternativ leverantör.

En rättelse av det som först dokumenterades här. IIIF svarar med **tre** olika
koder, och de betyder olika saker:

| Svar | Betydelse |
|---|---|
| `200` | volymen serveras publikt |
| `401` | volymen finns digitalt men kräver inloggning |
| `403` | det direkta anropet avvisas; pröva korrekt bildvisar-`Referer` innan åtkomsten klassas |

`403` gäller det prövade direkta IIIF-anropet. Det är **inte** tillräckligt för
slutsatsen att volymen inte kan nås publikt eller på distans. Samma URI kan
svara `200` med sin egen bildvisarsida som `Referer`; först därefter är
inloggad webbkatalog eller bildvisare en relevant reserv.

### Bildtjänstens `/v2/` och sessionsbunden 401

En styrd kontroll i en inloggad Riksarkivet-session 2026-08-30 visar den
aktuella bildkedjan mer exakt. Bildvisaren för reproduktion `00198658`
använder det publika manifestet
`https://lbiiif.riksarkivet.se/arkis!00198658/manifest`, men själva
bildtjänsten ligger under `/v2/`, exempelvis
`https://lbiiif.riksarkivet.se/v2/arkis!00198658_00057/info.json` och
`.../full/max/0/default.jpg`.

Oautentiserade anrop till den korrekta `/v2/`-bildvägen svarar `401` med
Riksarkivets besked att inloggning krävs. Samma bild öppnas i den inloggade
bildvisaren. Referer och vanlig webbläsaridentitet räcker inte; åtkomsten är
knuten till Riksarkivets autentiserade session. Katalog-API och publikt
manifest ska därför fortsatt användas för volym- och årsrouting, medan
inloggad bildvisare får användas för den visuella originalkontrollen när
bildsvaret är `401`. Sessionsuppgifter, kakor och kontodata får aldrig
kopieras till projektet.

### Reproduktionsmanifest som kräver bildvisaren som Referer

En ytterligare variant verifierades 2026-08-30 för Ljustorps äldre
reproduktioner `C0033121`, `C0033122`, `C0033123` och `C0033133`.
Bildvisarsidans HTML bäddar in manifestet
`https://lbiiif.riksarkivet.se/arkis!<reproduktion>/manifest`. Ett direkt
anrop till manifestet gav `403`, men exakt samma URI gav `200` när HTTP-
huvudet `Referer` sattes till en motsvarande sida på
`https://sok.riksarkivet.se/bildvisning/<bild-id>`. Manifestets
`full/max/0/default.jpg` fungerade därefter på samma sätt. Inga kakor eller
sessionsdata behövdes eller exporterades.

Detta är skilt från `/v2/`-bildens autentiseringsbundna `401` ovan. Vid ett
`C0…`-manifest-`403` ska ordningen därför vara:

1. läs bildvisarsidans HTML och verifiera den inbäddade manifest-URI:n,
2. upprepa manifestanropet med den egna Riksarkivet-bildvisarsidan som
   `Referer`,
3. använd inloggad Chrome endast om anropet fortfarande är spärrat eller om
   exakt bild-id måste återfinnas visuellt.

Det bevarade försöket och de framgångsrika manifesten finns i
[S-0517](sources/S-0517-riksarkivet-ljustorp-C1-C2-AI1-AI3-henrik-konflikt.md).

Skillnaden mellan `401`, naket `403` och publikt `200` följer inte
batchprefixet tillräckligt säkert för en åtkomstslutsats. Följande var de
nakna svar som observerades 2026-08-20:

| Batch | Volym | Svar |
|---|---|---|
| `A0027066` | Bygdeå C/5 | 200 |
| `A0001442` | Degerfors A I/8b | 200 |
| `F0003348` | Flen A I/26 | 200 |
| `C0042580` | Sävar A I/6b | **403** |
| `C0034028` | Bygdeå A I/14b | **403** |

Båda `C0…`-batcherna avser digitaliserade volymer. Tabellen bevarar det nakna
testets svar; den visar inte att rätt bildvisar-`Referer` har prövats och får
inte längre citeras som bevis för att bilderna är icke-publika.

## Viktig varning om sök-API:ets bildlänkar

Fältet `_links.image` i `data.riksarkivet.se/api/records` saknades för både
Sävars och Bygdeås husförhörslängder — samma volymer vars batcher ger 403.

**Slutsatsen "ingen bildlänk ⇒ volymen är inte digitaliserad" är därför
felaktig.** Avsaknad av bildlänk kan lika gärna betyda att volymen är
digitaliserad men inte publikt serverad.

Vad som faktiskt kan fastställas på distans är att volymen **inte går att nå**,
inte varför. Formulera slutsatser därefter: skriv "kan inte nås på distans" och
inte "är inte digitaliserad", om inte något oberoende belägg finns för det
senare.

### Inte heller RDF-posten hjälper

Varje volym har en RDF-representation på
`data.riksarkivet.se/archive/<id>.jsonld`, där ett fält `schema:image` pekar på
IIIF-manifestet. Det verkade vara en pålitligare väg än sök-API:ets
`_links.image`. Det är det inte.

Prövat 2026-08-20: Sävars husförhörslängd `A I/6b`, vars batch `C0042580`
bevisligen är digitaliserad eftersom projektet har lokala bilder från den,
saknar `schema:image` i sin RDF-post precis som i sök-API:et.

**Rättelse 2026-08-21.** Varken sök-API:et eller RDF-posten kan skilja
*odigitaliserad* från *digitaliserad men inte publikt serverad via direkt
IIIF*. Ett känt batch-id och dess `403` räcker inte heller för att avgöra
fjärråtkomst. Den inloggade vanliga webbkatalogen visade `Digitaliserat
material finns`, gav en `Bild`-länk och öppnade bildvisaren för elva prövade
`C0…`-batcher som samtidigt gav `403` på direktmanifestet. Positiv åtkomst ska
därför klassificeras i fyra separata lager:

1. katalogpost finns,
2. katalogposten visar digitalt material och `Bild`,
3. bildvisaren öppnar volymen i inloggad session,
4. direkt API/IIIF fungerar eller är spärrat.

Först när den inloggade katalogposten saknar bildlänk får projektet använda
`ÅTKOMSTSPÄRR`, och då endast med exakt återaktiveringsväg. Det tidigare
statusnamnet `EJ DIGITALISERAD` ska inte längre användas för nya bedömningar
utan oberoende belägg för själva digitaliseringsläget. Den fulla revisionen
finns i [`source-coverage.md`](source-coverage.md).

## Åtkomstregeln följer volymen, inte sidan

Detta prövades systematiskt 2026-08-20. Spärren avgörs av **volymens sluttid**,
inte av den enskilda sidans ålder. En volym som sträcker sig långt in på
1900-talet är stängd i sin helhet, även för uppslag som är mer än hundra år
gamla.

| Volym | Tidsomfång | Batch | Svar |
|---|---|---|---|
| Helgesta E I/1 | 1885–1894 | `F0003401` | 200 |
| Helgesta E I/2 | 1895–1948 | `F0003402` | 401 |
| Helgesta C/8 | 1916–1946 | `F0015641` | 401 |
| Flen E I/2 | 1905–1915 | `00154059` | 200 |
| Flen E I/3 | 1914–1935 | `00154060` | 401 |
| Hyltinge A II a/5 | 1918–1927 | `F0007058` | 401 |
| Hyltinge C/6 | 1879–1894 | `F0003419` | 200 |

Gränsen ligger alltså inte vid ett bestämt årtal i innehållet. Flens
vigselbok 1905–1915 är öppen medan Helgestas vigselbok är stängd trots att den
innehåller samma årgångar, eftersom den senare fortsätter till 1948. Slutsatsen
för planeringen: kontrollera alltid **volymens** datering i sök-API:et innan en
efterforskning läggs upp, och leta efter en parallell volym med tidigare
slutår som täcker samma år.

En andra spärr är att alla volymer inte är digitaliserade. Saknad `_links.image`
i sök-API:et betyder att volymen inte kan nås på distans alls; den kan ändå
finnas i läsesalen eller hos en kommersiell leverantör. Det är en
digitaliserings- och åtkomstlucka och ska inte skrivas som arkivlucka.

## Volymkoder för folkräkningen 1890, Södermanlands län

Volymkoden är `9` för 1890, `8` för 1880, följt av tvåsiffrigt länsnummer och
tresiffrigt församlingsnummer. Södermanland har länsnummer `04`, Västerbotten
`24`. Tabellen nedan togs fram genom att hämta manifestens etiketter för
`904001`–`904099`. Samma metod fungerar för andra län och år.

| Församling | Volymkod 1890 |
|---|---|
| Tuna | `904001` |
| Bergshammar | `904002` |
| Tunaberg | `904003` |
| Lunda | `904004` |
| Kila | `904005` |
| Björkvik | `904006` |
| Halla | `904007` |
| Stigtomta | `904008` |
| Nykyrka | `904009` |
| Bärbo | `904010` |
| Sankt Nikolai | `904011` |
| Ripsa | `904012` |
| Lid | `904013` |
| Runtuna | `904014` |
| Ludgo | `904015` |
| Spelvik | `904016` |
| Bälinge | `904017` |
| Tystberga | `904018` |
| Torsåker | `904019` |
| Lästringe | `904020` |
| Sättersta | `904021` |
| Bogsta | `904022` |
| Råby-Rönö | `904023` |
| Svärta | `904024` |
| Helgona | `904025` |
| Hölö | `904026` |
| Mörkö | `904027` |
| Västerljung | `904028` |
| Trosa landsförsamling | `904029` |
| Vagnhärad | `904030` |
| Västra Vingåker | `904031` |
| Östra Vingåker | `904032` |
| Julita | `904033` |
| Österåker | `904034` |
| Stora Malm | `904035` |
| Lerbo | `904036` |
| Floda | `904037` |
| Sköldinge | `904038` |
| Blacksta | `904039` |
| Vadsbro | `904040` |
| Husby-Oppunda | `904041` |
| Bettna | `904042` |
| Vrena | `904043` |
| Helgesta | `904044` |
| Hyltinge | `904045` |
| Dunker | `904046` |
| Lilla Malma | `904047` |
| Malmköping | `904048` |
| Årdala | `904049` |
| Forsa | `904050` |
| Lilla Mellösa | `904051` |
| Flen | `904052` |
| Fors | `904053` |
| Torshälla landsförsamling | `904054` |
| Gillberga | `904055` |
| Lista | `904056` |
| Tumbo | `904057` |
| Råby-Rekarne | `904058` |
| Öja | `904059` |
| Västermo | `904060` |
| Jäder | `904061` |
| Barva | `904062` |
| Kjula | `904063` |
| Sundby | `904064` |
| Vallby | `904065` |
| Hammarby | `904066` |
| Stenkvista | `904067` |
| Ärla | `904068` |
| Husby-Rekarne | `904070` |
| Näshulta | `904071` |
| Kloster | `904072` |
| Gåsinge | `904073` |
| Dillnäs | `904074` |
| Frustuna | `904075` |
| Kattnäs | `904076` |
| Björnlunda | `904077` |
| Gryt | `904078` |
| Åker | `904079` |
| Länna | `904080` |
| Vansö | `904081` |
| Härad | `904082` |
| Fogdö | `904083` |
| Helgarö | `904084` |
| Strängnäs landsförsamling | `904085` |
| Toresund | `904086` |
| Överselö | `904087` |
| Ytterselö | `904088` |
| Aspö | `904089` |
| Kärnbo | `904090` |
| Taxinge | `904091` |
| Överenhörna | `904092` |
| Ytterenhörna | `904093` |
| Nyköpings västra | `904094` |
| Nyköpings östra | `904095` |
| Eskilstuna | `904096` |
| Strängnäs stadsförsamling | `904097` |
| Torshälla stadsförsamling | `904098` |
| Mariefred | `904099` |

Numret `904069` saknar volym i serien.
