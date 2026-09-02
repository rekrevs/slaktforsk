# C-0714: Svea A I b/8 och livgardesrullor för Olaus

## Källor

- [S-0383](../sources/S-0383-riksarkivet-svea-livgarde-AIa1-63-1868-1877.md)
- [S-0550](../sources/S-0550-riksarkivet-svea-aib8-livgardesrullor.md)

## Ny församlingskontroll

Den äldre kontrollen C-0480 gällde Svea livgardes aktiva
husförhörslängd A I a 1/63. Riksarkivets OAI identifierar därutöver den
särskilda A I b/8 för `änkor och avskedade`, 1847–1876. Volymen har ett
publikt 55-bildersmanifest.

Det första registerblocket är uttryckligen avgränsat till 1857–1860.
Volymens andra, odaterade register börjar på bild 48; dess fulla F-avsnitt
på bild 49 saknar både Fredberg och Fredriksson. Detta är ett nytt exakt
registerbladnoll, men inte ett fullständigt A I b/8-, församlings- eller
Svea-livgarde-noll.

## Bild-API-diagnos

Records-API:t gav WAF-HTML när anropet saknade vanlig webbläsar-
`User-Agent`, men gav korrekt JSON med `Mozilla/5.0`. Samma maximala
IIIF-bild gav däremot `200 image/jpeg` i samtliga tre testvarianter utan
sessionskaka, även med vanlig curl och utan `Referer`. Den observerade
spärren låg därför i records-API-anropets headers, inte i IIIF-bild-API:t.
Chrome och den inloggade sessionen behövdes inte.

## Militär återstart

Svea livgardes OAI-EAD och JSON-LD identifierar nu tio prioriterade
kompanirullor kring målintervallet, men de är analogt representerade och
flera samlingsvolymer har luckor inom sina vida datumspann. De ger därför
en beställningslista, inte ett nytt negativt resultat.

För Göta livgarde är vägen mer koncentrerad. Volym 194 är digital med 436
bilder och en kompanivis rekryt-/stamrulla, men manifestet saknar
namnregister. Det separata namnregistret i volym 198, den periodnära
rekryteringsjournalen 240 och avskedsjournalerna i 241 är analoga. Ingen av
de 436 rullbilderna har tolkats som ett Olaus-noll.

Återstartsordningen är därför:

1. volym 198: Fredberg/Fredriksson och båda källburna födelsedatumen;
2. vid träff, den digitala volym 194;
3. vid noll, volym 240 för 1874–1876 och volym 241:s avskedade;
4. därefter de kompanivisa Svea- och Göta-rullorna.

## Slutsatsens gräns

A I b/8 stärker bara det tidigare avgränsade Svea-registernollet. Den nya
militärinventeringen visar att den äldre församlingskontrollen inte tömde de
arkivmässiga stam-, rekryterings- och avskedsrullorna. Kungsholms uppgift `f.d. gardist`
står kvar, medan förband, tjänstetid, födelsedatumskonflikt och föräldrar är
olösta. Ingen relation skapas.

## Fulloriginal

| Bild | Storlek |
|---|---:|
| [A I b/8, volymomslag](../media/C-0714-riksarkivet-svea-AIb8-cover-00025805_00001.jpg) | 4 898 × 3 448 px |
| [A I b/8, register 1857–1860](../media/C-0714-riksarkivet-svea-AIb8-register-1857-1860-00025805_00043.jpg) | 5 427 × 4 216 px |
| [A I b/8, andra registrets början](../media/C-0714-riksarkivet-svea-AIb8-generalregister-00025805_00048.jpg) | 5 431 × 4 205 px |
| [A I b/8, andra registrets F-avsnitt](../media/C-0714-riksarkivet-svea-AIb8-generalregister-F-00025805_00049.jpg) | 5 431 × 4 213 px |
| [Göta 194, originalpärm](../media/C-0714-riksarkivet-gota-194-cover-K0000725_00002.jpg) | 4 912 × 5 296 px |
| [Göta 194, första kompanisidan](../media/C-0714-riksarkivet-gota-194-first-page-K0000725_00004.jpg) | 4 727 × 5 315 px |

### Exakt bildproveniens

- Fil: [A I b/8, volymomslag](../media/C-0714-riksarkivet-svea-AIb8-cover-00025805_00001.jpg)
- SHA-256: `71e49e02dcb92b37fc7ff644612238121e6e42a654561db58a6d427f8b11aad8`
- Fil: [A I b/8, register 1857–1860](../media/C-0714-riksarkivet-svea-AIb8-register-1857-1860-00025805_00043.jpg)
- SHA-256: `aef3eeb9526ba103a2dd9d2be7fb724c70947a1b917ca6a93bd3ad24b3044921`
- Fil: [A I b/8, andra registrets början](../media/C-0714-riksarkivet-svea-AIb8-generalregister-00025805_00048.jpg)
- SHA-256: `27c60575a693fa32104ec2ae81dd7afabf7798f92a34971d6bd793d933ac27f6`
- Fil: [A I b/8, andra registrets F-avsnitt](../media/C-0714-riksarkivet-svea-AIb8-generalregister-F-00025805_00049.jpg)
- SHA-256: `ff4c1de22477a5e8d88d14e3fd2bee30f44adf8d70e0f3a82c1068becfe9f3a5`
- Fil: [Göta 194, originalpärm](../media/C-0714-riksarkivet-gota-194-cover-K0000725_00002.jpg)
- SHA-256: `1458a90a82eff7d607fcd24c8884306ba9b94754d53e86b4f7c232cefa456777`
- Fil: [Göta 194, första kompanisidan](../media/C-0714-riksarkivet-gota-194-first-page-K0000725_00004.jpg)
- SHA-256: `8b41c7662a45c1a08bec51dd95747d2af354da925e64d130706b335112830f02`

### Metadata- och diagnosoriginal

- Svea församling: [fond-OAI](../media/S-0550-riksarkivet-svea-parish-fonds-oai-ead.xml), [A I b/8 JSON-LD](../media/S-0550-riksarkivet-svea-aib8-jsonld.json), [volym-OAI](../media/S-0550-riksarkivet-svea-aib8-oai-ead.xml) och [IIIF-manifest](../media/S-0550-riksarkivet-svea-aib8-00025805-IIIF-manifest.json).
- Åtkomstdiagnos: [WAF-svar](../media/S-0550-riksarkivet-records-api-no-user-agent-waf.html), [curl-huvuden](../media/S-0550-riksarkivet-iiif-default-no-referer-headers.txt), [Mozilla-huvuden](../media/S-0550-riksarkivet-iiif-mozilla-no-referer-headers.txt) och [Mozilla-/Referer-huvuden](../media/S-0550-riksarkivet-iiif-mozilla-referer-headers.txt).
- Svea livgarde: [fond-OAI](../media/S-0550-riksarkivet-svea-livgarde-fonds-oai-ead.xml), [Livkompaniets stamrulla](../media/S-0550-riksarkivet-svea-liv-stam-jsonld.json), [Livkompaniets rekryteringsrulla](../media/S-0550-riksarkivet-svea-livkompaniet-rekryteringsrulla-jsonld.json), [2. kompaniet](../media/S-0550-riksarkivet-svea-second-annotation-jsonld.json), [3. kompaniet](../media/S-0550-riksarkivet-svea-third-kapitulation-jsonld.json), [5. kompaniet](../media/S-0550-riksarkivet-svea-fifth-stam-jsonld.json), [6. kompaniets stamrulla](../media/S-0550-riksarkivet-svea-sixth-stam-jsonld.json), [6. kompaniets rekryteringsrulla](../media/S-0550-riksarkivet-svea-sjatte-kompaniet-rekryteringsrulla-jsonld.json), [7. kompaniet](../media/S-0550-riksarkivet-svea-seventh-stam-jsonld.json), [8. kompaniet](../media/S-0550-riksarkivet-svea-eighth-stam-jsonld.json) och [musikkompaniet](../media/S-0550-riksarkivet-svea-music-stam-jsonld.json).
- Göta livgarde: [fond-OAI](../media/S-0550-riksarkivet-gota-livgarde-fonds-oai-ead.xml), volym 194:s [JSON-LD](../media/S-0550-riksarkivet-gota-194-jsonld.json), [OAI](../media/S-0550-riksarkivet-gota-194-oai-ead.xml) och [IIIF-manifest](../media/S-0550-riksarkivet-gota-194-K0000725-IIIF-manifest.json) samt JSON-LD för [namnregister 198](../media/S-0550-riksarkivet-gota-198-namnregister-jsonld.json), [rekryteringsjournal 240](../media/S-0550-riksarkivet-gota-240-rekrytering-jsonld.json) och [avskedsjournal 241](../media/S-0550-riksarkivet-gota-241-avsked-jsonld.json).

Samtliga filer redovisas även med individuella SHA-256 i
`genealogy/media-manifest.json`.

## Stödda påståenden

A-2784–A-2788.
