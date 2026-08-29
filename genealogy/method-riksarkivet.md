# Metod: att nå Riksarkivets material reproducerbart

Detta dokument beskriver hur projektets källbilder och volymuppgifter hämtas
utan manuellt bläddrande, så att varje citatpost går att kontrollera i
efterhand. Metoden verifierades 2026-08-20 genom att en tidigare sparad bild
(C-0067) laddades ned på nytt och gav identisk SHA-256-kontrollsumma.

## Verifierad Chrome-metod 2026-08-28

Den tidigare fungerande Chrome-metoden har nu reproducerats i en helt ny
browser-runtime med den installerade pluginversionen **26.820.60940**:

1. ladda pluginens `browser-client.mjs` och anslut med
   `agent.browsers.get("chrome")`;
2. namnge sessionen och skapa alltid en ny styrd flik med
   `chrome.tabs.new()`;
3. navigera direkt till en katalog- eller bildvisar-URL;
4. kontrollera DOM-texten `Inloggad som: ...` innan källarbete börjar;
5. om Riksarkivets ALTCHA-ruta visas, klicka den synliga
   `Jag är inte en robot`-kontrollen semantiskt och fortsätt först när sidan
   själv godkänt kontrollen;
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
- Det finns även indexerade personposter för en del församlingar:
  `/api/records/birthrecords` med `first_name`, `place`, `year_min`, `year_max`
  med flera. Täckningen är ojämn och tyngdpunkten ligger i södra Sverige, så
  noll träffar där säger ingenting om huruvida posten finns.

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
- Skicka en vanlig webbläsar-`User-Agent`; utan den svarar tjänsten `403`.
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
| `403` | volymen är digitaliserad men serveras inte publikt via IIIF |

`403` gäller det direkta IIIF-anropet. Det är **inte** längre tillräckligt för
slutsatsen att volymen inte kan nås på distans: den inloggade webbkatalogen och
bildvisaren kan fortfarande ge åtkomst.

Skillnaden mellan 401 och 403 följer batchprefixet. Prövat 2026-08-20:

| Batch | Volym | Svar |
|---|---|---|
| `A0027066` | Bygdeå C/5 | 200 |
| `A0001442` | Degerfors A I/8b | 200 |
| `F0003348` | Flen A I/26 | 200 |
| `C0042580` | Sävar A I/6b | **403** |
| `C0034028` | Bygdeå A I/14b | **403** |

Båda `C0…`-batcherna avser volymer som projektet redan har lokala bilder från,
hämtade i en tidigare session. De är alltså digitaliserade, men nås inte
publikt via IIIF nu.

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
