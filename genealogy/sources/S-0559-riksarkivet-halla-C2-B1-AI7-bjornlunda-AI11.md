# S-0559: Riksarkivet — Halla C/2, B/1, A I/7 och Björnlunda A I/11

## Källbeskrivning

- Institution: Riksarkivet i Uppsala
- Halla kyrkoarkiv: `SE/ULA/10364`, permanent id
  `TRn6bDX9rH6cxG02H087k3`
- Halla C/2, 1793–1835: permanent id `ki59jjX9rH6cxG02H087k3`,
  Arkis-UUID `b649c1ba-49d8-11d5-a6ed-0002440207bb`, reproduktion
  `C0006543`
- Halla B/1, 1806–1860: permanent id `iS59jjX9rH6cxG02H087k3`,
  Arkis-UUID `b649c1b1-49d8-11d5-a6ed-0002440207bb`, reproduktion
  `C0006540`
- Halla A I/7, 1836–1840: permanent id `dC59jjX9rH6cxG02H087k3`,
  Arkis-UUID `b649c19c-49d8-11d5-a6ed-0002440207bb`, reproduktion
  `C0006530`
- Björnlunda kyrkoarkiv: `SE/ULA/10120`, permanent id
  `Whj6bDX9rH6cxG02H087k3`
- Björnlunda A I/11, 1836–1840: permanent id
  `ULj7hjX9rH6cxG02H087k3`, Arkis-UUID
  `ae475b79-49d8-11d5-a6ed-0002440207bb`, reproduktion `C0005953`
- Kontrollerat och hämtat: 2026-08-31

## Omfattning och routing

Records-API och OAI-EAD skilde Halla kyrkoarkiv i Uppsala från den
liknamniga församlingen på Gotland. Riksarkivets publika
`/Tree/SubTree/`-slutpunkt band de fyra exakta Arkis-posterna till
reproduktionerna ovan; IIIF-manifesten och fullbilderna fungerade med
Riksarkivets bildvisarsida som `Referer`.

Halla C/2:s manifest har 185 bilder. Födelseåret 1822 börjar på bild 81
och 1823 på bild 83, så hela 1822-följden är bilderna 81–82. Halla B/1:s
utflyttningsföljd 1836–1842 ligger på bilderna 56–61. Halla A I/7:s
ortregister hänvisar Ellesta Södergård till sida 37 och Norrgård till sida
40; hela Ellestaföljden, sidorna 37–40, ligger på bilderna 43–46.

Björnlunda A I/11:s manifest har 382 bilder men saknar sidstrukturer. Alla
bilder screenades i låg upplösning med lokal Apple Vision-OCR endast för
att nominera namnträffar. Den observerade beräkningsenheten var Apple M4
Max GPU. De 37 nominerade namnträffarna kontrollerades visuellt; OCR bär
inte ett negativt helvolymsresultat.

## Resultat och källkritik

Den ursprungliga slutsatsen att Halla C/2:s kompletta födelseföljd 1822
saknade Carl Eric/Fredric var en felläsning. Vid omläsning 2026-09-02
identifierades på bild 82 post 3 Carl Fredrik, född 1822-04-09 och döpt
12 april, som pigan Ella Ersdotters utomäktenskaplige son i Lilla
Wättstugan. Resultatet och den närmaste husförhörsroutingen bevaras i
S-0614/C-0798. Ingen Carl Fredrik-post finns på exakt 1822-07-09, men
detta är nu endast ett exaktdatumnoll; det får inte beskrivas som ett
års-, församlings- eller personnoll. Det öppna födelseregistrets nollträff
för hela Halla 1822 är en täckningslucka i registret och får ingen
sakpåståendestatus.

Halla B/1:s utflyttningssidor 1836–1842 saknar namnet Grill. Bild 59 har
däremot år 1839 raden `Drängen Carl Eric Carlsson`, från `Ellesta` till
`Björnlunda`. Det är en namnnära och ortsburen ledtråd, inte identifikation
med Carl Eric/Fredric Grill. Hela Ellesta sidorna 37–40 i Halla A I/7
saknar en motsvarande Carl Eric Carlsson; en flytt inom samma år kan ha
passerat utan en bestående hushållsrad.

Björnlunda A I/11 gav ingen säker match bland OCR-nominerade sidor.
Fulloriginalet på bild 189 har en `Dräng Eric Carlsson`, men födelsedatumet
är 1820-08-10 och avvisar honom som den datumangivna kandidaten. Eftersom
OCR kan missa handskrift är detta en kandidatavvisning, inte ett verifierat
helvolyms-, person- eller vistelsenoll.

Den externa, inloggade Chrome-sessionen nådde den äldre katalogposten för
Björnlunda A I/11 utanför sandboxen men sidan visade ändå ALTCHA. Ingen
checkbox aktiverades och ingen CAPTCHA/ALTCHA löstes. Den publika
`Tree/SubTree`- och IIIF-routen gav samma volym utan interaktion.

Halla-födelseposten är nu omprövad och binder genom exakt namn,
1822-04-09 och Halla till den senare Carl Fredrik Grill-kedjan; modern
Ella Ersdotter skapas därför i S-0614/C-0798. De separata
Carl Eric Carlsson-/Björnlunda-observationerna binder fortfarande inte
kandidatfamiljens strykning 1852 till den vuxne Erik 1875–1876.

## Lokalt bevarade metadataoriginal

| Original | SHA-256 |
|---|---|
| [Halla C/2 IIIF-manifest](../media/S-0559-riksarkivet-halla-C2-manifest.json) | `5b2c2991e10c974170a205b2aa9c2f9be3cdcdb2693af06964a47d1154ef1e2f` |
| [Halla C/2 OAI-EAD](../media/S-0559-riksarkivet-halla-C2-oai-ead.xml) | `362547ca2a4b2a0bb59e44f2552ea71562897333326e6629018be7ab9df01336` |
| [Halla C/2 Tree/SubTree-svar](../media/S-0559-riksarkivet-halla-C2-tree.html) | `46f10b0af2c305fb898bf12eb432ce816f02c5b980a81b11c1e934cc61980248` |
| [Halla B/1 IIIF-manifest](../media/S-0559-riksarkivet-halla-B1-manifest.json) | `b3d1b93ed8c0e8caa562352b1c8e577c7b791961feef9412892087c2e912f319` |
| [Halla B/1 OAI-EAD](../media/S-0559-riksarkivet-halla-B1-oai-ead.xml) | `ffc8d6e3450d174b2b11eac495645b7fe2615b6d07289047d1cccf653d9e8ae4` |
| [Halla B/1 Tree/SubTree-svar](../media/S-0559-riksarkivet-halla-B1-tree.html) | `b4aadccc19c1ebb37ee43d841d259b5ca217c08e552fd56bb06c740e603f4219` |
| [Halla A I/7 IIIF-manifest](../media/S-0559-riksarkivet-halla-AI7-manifest.json) | `214dc199c9ca2994071b33a8ac3447f9671ff2c64b451f429a69617d37fd49e4` |
| [Halla A I/7 OAI-EAD](../media/S-0559-riksarkivet-halla-AI7-oai-ead.xml) | `e9253f81d00d0ffb2d6eb4c5e7bec2d32a73f077996703b8564cb763c9075327` |
| [Halla A I/7 Tree/SubTree-svar](../media/S-0559-riksarkivet-halla-AI7-tree.html) | `26c2934054e9c09c9d78d613786217f7df9efc241acd43a0ffda23b3551a2049` |
| [Björnlunda A I/11 IIIF-manifest](../media/S-0559-riksarkivet-bjornlunda-AI11-manifest.json) | `b3cf0d41b86952db557a706ff361e96ca13cdc4c07ccdc0da4a86576c27efa6a` |
| [Björnlunda A I/11 OAI-EAD](../media/S-0559-riksarkivet-bjornlunda-AI11-oai-ead.xml) | `645cb4b2de98ad783755aa4b1444c4a5c3d140f940efe1b96d1a22a3c8942bea` |
| [Björnlunda A I/11 Tree/SubTree-svar](../media/S-0559-riksarkivet-bjornlunda-AI11-tree.html) | `53bf68ee0a710c59ae9da386a04a90ecddc0dda0c5567ba97fc37d4139c4098a` |
| [Födelseregister Halla 1822, täckningsnoll](../media/S-0559-riksarkivet-birthregister-halla-1822-coverage.json) | `d29e77681758a6ea95e71cb11e7fcebe57b582bfa8260533814a8b6adc49074d` |

Fulloriginal och individuella checksummor redovisas i
[C-0725](../citations/C-0725-halla-C2-B1-AI7-bjornlunda-AI11-carl-eric.md).
