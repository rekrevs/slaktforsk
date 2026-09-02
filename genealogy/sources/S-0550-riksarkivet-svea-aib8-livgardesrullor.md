# S-0550: Riksarkivet — Svea A I b/8 och livgardesrullor 1874–1876

## Källbeskrivning

- Institution: Riksarkivet
- Arkiv: Svea livgardes församlings kyrkoarkiv, `SE/SSA/0005E`
- Volym: `SE/SSA/0005E/A I b/8`, *Husförhörslängder för änkor och
  avskedade*, 1847–1876
- Permanent Riksarkivet-id: `aMVKJbmdBaYCjAo6p5mEy7`
- Reproduktion: `00025805`, 55 bildytor
- [IIIF-manifest](https://lbiiif.riksarkivet.se/arkis!00025805/manifest)
- Arkiv: Svea livgarde, `SE/KrA/0101/A`
- Arkiv: Göta livgarde, `SE/KrA/0102/A`
- Kontrollerat: 2026-08-31

## A I b/8:s register

Records-API, JSON-LD, OAI-EAD och IIIF identifierar samma digitala volym.
Manifestet innehåller två registerblock efter den paginerade längden:

- bild 43 rubricerar det första `Register öfver privatförsamlingen ifrån
  och med 1857 till och med 1860`; dess C–H-sida ligger på bild 44;
- bild 48 rubricerar ett andra, odaterat `Register`; dess sammanhängande
  C–H-sida ligger på bild 49 och följs av I–M på bild 50.

Det andra registrets fulla F-avsnitt på `00025805_00049` innehåller bland
annat Friskopff, Forsman, Fagerberg, Forsslander, Fyhr, Froberg, Forssell och
Flemming, men ingen Fredberg eller Fredriksson. Resultatet är ett exakt
register- och namnformsnoll i just detta registerblad. Det är inte ett
fullständigt personnoll i volymen, ett tjänstgöringsnoll i Svea livgarde
eller bevis för att Olaus tillhörde ett annat förband.

## Åtkomstdiagnos

Ett första records-API-anrop utan vanlig webbläsar-`User-Agent` gav
Riksarkivets HTML-sida `Web Application Firewall`. Samma exakta fråga med
`Mozilla/5.0` gav JSON och den korrekta volymposten. Detta var alltså ett
headerkänsligt records-API-svar, inte ett fel i bild-API:t.

Den maximala IIIF-bilden `00025805_00049` prövades därefter utan
sessionskaka i tre varianter: vanlig curl utan `Referer`, webbläsar-
`User-Agent` utan `Referer` och samma `User-Agent` med Riksarkivet som
`Referer`. Alla tre svarade `200` och `image/jpeg`. Varken Chrome,
inloggningssession, CAPTCHA eller ALTCHA behövdes.

## Exakta Svea livgarde-rutter

Fondens OAI-EAD och de enskilda JSON-LD-posterna ger följande prioriterade
kompanivägar som överlappar eller omsluter 1874–1876:

| Kompani | Referenskod | Datering och innehåll | Åtkomst |
|---|---|---|---|
| Livkompaniet | `A/012:Ö/D II/1` | 1842–1880; stamrulla 1847–1880 | analog |
| Livkompaniet | `A/012:Ö/D V/1` | 1864–1901; rekryteringsrullor 1864–1889, 1894–1901 | analog |
| 2. kompaniet | `A/013:Ö/D III/1` | annotationsrulla 1865–1880 | analog |
| 3. kompaniet | `A/014:Ö/D II/1` | kapitulationsjournaler 1849–1880 | analog |
| 5. kompaniet | `A/016:Ö/D I/1` | kapitulations- och stamrullor 1836–1887 | analog |
| 6. kompaniet | `A/017:Ö/D II/2` | kapitulations- och stamrullor 1867–1885 | analog |
| 6. kompaniet | `A/017:Ö/D III/1` | rekryteringsrullor 1864–1894 i en volym 1809–1907 | analog |
| 7. kompaniet | `A/018:Ö/D II/2` | kapitulations- och stamrullor 1837–1891 | analog |
| 8. kompaniet | `A/019:Ö/D II/2` | kapitulations- och stamrullor 1865–1885 | analog |
| Musikkompaniet | `A/020:Ö/D I/1` | kapitulations- och stamrullor 1819–1887 | analog |

Datumspann betyder inte att varje år är representerat i varje samlingsvolym.
Fjärde kompaniets bevarade stamrulla slutar enligt förteckningen 1873 och
nästa börjar 1887. Tabellen är därför en beställningsroute, inte ett
förbandsomfattande noll eller påstående om komplett årstäckning.

## Göta livgardes centrala väg

Göta livgardes fulla OAI-EAD och exakta JSON-LD-poster gör den centrala
återstartsordningen ovanligt tydlig:

| Referenskod | Datering | Kataloginnehåll | Åtkomst |
|---|---:|---|---|
| `SE/KrA/0102/A/001:Ö/0/194` | 1874–1912 | stamrulla över manskap | digital, `K0000725`, 436 bildytor |
| `SE/KrA/0102/A/001:Ö/0/198` | 1874–1927 | namnregister till stamrullan | analog |
| `SE/KrA/0102/A/001:Ö/0/240` | 1857–1877 | rekryterings- och approbationsjournaler | analog |
| `SE/KrA/0102/A/001:Ö/0/241` | 1809–1907 | rekryterings- och approbationsjournaler; 1870–1907 även journaler över avskedade | analog |

Volym 194:s katalogpost kallar materialet stamrulla. Det fotograferade
originalets pärm lyder samtidigt `Kongl. Andra Lifgardet. Rekryt
Approbations Journal tillhörande Second Chefs Expeditionen`, och första
uppslaget är kompanivis med fält för namn, födelsedatum, värvningsdatum,
födelseort, yrke, föregående tjänst och anmärkningar. Den digitala volymen
är alltså personrelevant men registerlös i manifestet.

## Batch 161: extern Chrome och kandidatkontroll

Den exakta permanenta katalogrouten för volym 198 öppnades i en verklig,
inloggad Chrome-session utanför sandboxen. Riksarkivet visade ändå ALTCHA;
ingen checkbox aktiverades och ingen kontroll löstes. Omdirigeringens
`returnUrl` gav Arkis-identifieraren
`ee04c964-05da-4b86-8727-b5c0ccd5d2f7`. Ett publikt batchanrop med denna
identifierare gav bara Riksarkivets generiska felsida, utan batchmetadata,
reproduktionskod eller bildlänk. Namnregister 198 är alltså fortsatt analogt
och oläst.

Volym 194:s publika IIIF-bilder fungerade däremot utan session och CAPTCHA.
Rullbilderna 4–435 screenades maskinellt för namnformer och periodnära årtal;
OCR:n användes bara för att välja sidor för originalkontroll. Tre starkaste
kandidater lästes i fulloriginal och avvisades:

- Livkompaniet nr 93: Per Alexander Svensson, född 1852-03-07, värvad
  1876-06-03;
- 4. kompaniet nr 47: Carl Olaus Carlsson, född 1859-07-01, värvad
  1877-07-11;
- 7. kompaniet nr 85: Johan Olsson Fredberg, född 1877-09-26, värvad
  1895-03-19.

Maskinscreeningen kan missa handskrivna namn. Den är inte en verifierad
fullvolymsläsning och de 436 bilderna görs inte till ett Olaus-, förbands-
eller tjänstgöringsnoll. Namnregister 198 förblir den säkraste vägen.

## Batch 165: offentlig Tree/SubTree och förnyad Chrome-kontroll

De permanenta posterna exponerar Arkis-UUID:erna
`ee04c964-05da-4b86-8727-b5c0ccd5d2f7` för volym 198,
`bd466318-2dbd-4279-ba82-1a0f624895d6` för volym 240 och
`1fa79ae6-56e6-42fa-b14a-180bc1cb76e2` för volym 241. Riksarkivets
publika `/Tree/SubTree/`-slutpunkt gav för var och en bara samma tomma
ASP TreeView-kommentar, utan bildfilsbarn eller reproduktionskod.

På ägarens uttryckliga förslag prövades volym 198 samtidigt på nytt i den
verkliga, inloggade Chrome-sessionen utanför sandboxen. Den permanenta
länken omdirigerade åter till ALTCHA. Ingen checkbox aktiverades och ingen
CAPTCHA löstes. Resultaten bekräftar den nuvarande digitala åtkomstgränsen
men säger inget om innehållet i de tre analoga volymerna.

Den säkraste återstarten är att först beställa volym 198 och slå upp
Fredberg/Fredriksson samt båda födelsedatumen. En träff kan routas tillbaka
till digitala volym 194. Vid noll följer volym 240 för 1874–1876 och volym
241:s avskedsjournaler före Kungsholmsnotisen 1876-06-14. De kompanivisa
rekryterings- och stamrullorna i samma fond är reservvägar. Ingen Olaus-rad
är ännu bekräftad eller avvisad i dessa militära original.

## Källkritik

Kungsholm B I/16 säger bara `f.d. gardist`; den namnger inget förband. A I
b/8:s registerblad hör till Svea livgardes församling men behöver inte
omfatta varje tidigare gardist eller varje militär rulla. Arkivförteckningar
och analog/digital representation ger exakta sökvägar, inte personinnehåll.
Ingen identitet, militär tjänstgöring eller föräldrarelation skapas.

## Lokalt bevarad proveniens

Följande Riksarkivet-original är bevarade med individuella SHA-256 i
`genealogy/media-manifest.json`:

- församlingsfondens och de båda militärfondernas fulla OAI-EAD;
- A I b/8:s JSON-LD, volym-OAI och IIIF-manifest;
- tio exakta Svea-kompanivolymers JSON-LD;
- Göta 194:s JSON-LD, volym-OAI och IIIF-manifest samt JSON-LD för
  volymerna 198, 240 och 241;
- WAF-svaret, de tre IIIF-svarshuvudena och det publika batchfelsvaret för
  volym 198:s Arkis-identifierare;
- de tre tomma Tree/SubTree-svaren för volymerna 198, 240 och 241.

De sex tidigare lästa fulloriginalen redovisas i
[C-0714](../citations/C-0714-svea-aib8-och-livgardesrullor-olaus.md).
Tre nya, avvisade kandidatposter och batchfelsvaret redovisas i
[C-0722](../citations/C-0722-gota-livgarde-volym-194-198-olaus-kandidater.md).
Tree/SubTree-svaren och den förnyade åtkomstkontrollen redovisas i
[C-0726](../citations/C-0726-gota-livgarde-BII1-1876-och-analoga-journaler.md).
