# S-0551: Riksarkivet — SCB Västerbotten 1868, länets dödsranger

## Källbeskrivning

- Arkivbildare: Statistiska centralbyrån (SCB)
- Arkiv: `SE/RA/420401/01`, *Avdelningen för befolkningsstatistik,
  1:a avdelningen*
- Serie: `H 1 AA`, *Utdrag ur födelse-, vigsel- och dödböcker 1860–1949*
- Volym: `SE/RA/420401/01/H 1 AA/304`, 1868, `Västerbottens län`
- Permanent Riksarkivet-id: `qnJL2ugRrH6d0G02H087k3`
- Reproduktion: `A0035803`, 338 bildytor
- [Katalogpost](https://sok.riksarkivet.se/arkiv/qnJL2ugRrH6d0G02H087k3)
- [IIIF-manifest](https://lbiiif.riksarkivet.se/arkis!A0035803/manifest)
- Läst och hämtat: 2026-08-31

Detta är samma Riksarkivet-volym som den kompletta Sävarläsningen i
[S-0541](S-0541-riksarkivet-scb-savar-doda-1868.md) och den tidigare
fyrförsamlingskontrollen i
[S-0547](S-0547-riksarkivet-scb-vasterbotten-1868-alternativa-dodsforsamlingar.md).
Den nya kontrollen använder manifestets fulla församlingsstruktur för att
routa de 22 dödsranger som ännu saknade ett avgränsat bildfönster kring den
konfliktsatta dagen 1868-08-14.

## Manifestets fulla dödsstruktur

IIIF Presentation 3-manifestet namnger 27 församlingsranger med underliggande
`Död` → `1868`. Rangen anger första canvas för respektive dödsutdrag, men inte
alltid sista canvas eller ett eget blad för varje datum. Kronologin lästes
därför fram inom varje range; tabellens evidensbild innehåller eller synligt
omsluter den 14 augusti.

| Församling | Dödsrangens början | Evidensbild/intervall | Kontroll |
|---|---|---|---|
| Bjurholm | `_00175` | `_00178` | ny |
| Burträsk | `_00254` | `_00266` | ny |
| Bygdeå | `_00222` | `_00232` | C-0711 |
| Dorotea | `_00330` | `_00331` | ny |
| Fredrika | `_00324` | `_00325` | ny |
| Holmsund | `_00199` | `_00199` | ny |
| Holmön | `_00215` | `_00215` | ny |
| Jörn | `_00308` | `_00309` | ny |
| Lycksele | `_00311` | `_00314` | C-0711 |
| Lövånger | `_00249` | `_00252` | ny |
| Nordmaling | `_00167` | `_00171` | ny |
| Norsjö | `_00304` | `_00306` | ny |
| Nysätra | `_00241` | `_00246` | ny |
| Robertsfors | `_00237` | `_00239` | ny |
| Skellefteå landsförsamling | `_00274` | `_00287` | ny |
| Skellefteå stadsförsamling | `_00336` | `_00336` | ny |
| Sorsele | `_00321` | `_00322` | ny |
| Stensele | `_00318` | `_00319` | ny |
| Sävar | `_00206` | `_00206`–`_00214` | C-0705 |
| Tärna | `_00320` | `_00320` | ny |
| Umeå landsförsamling | `_00180` | `_00193` | C-0711 |
| Umeå stadsförsamling | `_00332` | `_00335` | ny |
| Vilhelmina | `_00326` | `_00329` | ny |
| Vindeln, tidigare Degerfors | `_00216` | `_00219` | C-0711 |
| Vännäs | `_00200` | `_00203` | ny |
| Åsele | `_00322` | `_00323` | ny |
| Örträsk | `_00316` | `_00317` | ny |

## Läsresultat för de 22 återstående rangerna

Ingen av de 22 nya fullbilderna namnger Sara Sophia
Pehrsdotter/Persdotter eller Zingmark. Bjurholm, Holmsund, Vännäs, Holmön,
Robertsfors, Nysätra, Norsjö, Örträsk, Tärna, Sorsele, Åsele, Fredrika,
Vilhelmina, Dorotea, Umeå stadsförsamling och Skellefteå stadsförsamling har
synliga datumföljder som omsluter eller passerar måldagen utan en målpost.

Nordmaling, Lövånger, Burträsk, Skellefteå landsförsamling, Jörn och Stensele
har en eller flera synliga poster exakt den 14 augusti, men de avser andra
personer. Bland de tydligaste avgränsningarna är Nordmalings pojke på 7 år
4 månader 21 dagar, Lövångers pojke på 1 år 9 månader 3 dagar, Jörns Nils
Johan Hans Gustaf på 28 år 5 månader 29 dagar och Stenseles dotter Sophia
Charlotta på 4 år 4 månader 16 dagar. Burträsks två poster den dagen är barn,
och Skellefteå landsförsamlings post har annan identitet än målpersonen.

Tillsammans med C-0705 och C-0711 har därmed varje manifestdefinierad
församlingsrange i Västerbottens SCB-volym 1868 ett avgränsat bild- och
datumfönster kring den 14 augusti. Det är inte en helårsläsning av de stora
församlingarna, ett Sverigeomfattande sökresultat eller ett bevis för att en
sent eller oordnat införd rad saknas utanför fönstren. SCB-utdragen är
dessutom samtida parallella avskrifter från kyrkoböckerna, inte oberoende
original. Resultatet identifierar ingen annan dödsort och verifierar inte
heller att 1868-08-14 är rätt dag.

## Digital åtkomst och bevarad proveniens

Det tidigare bevarade records-API-svaret, volymens JSON-LD och OAI-EAD samt
IIIF-manifestet i S-0541 återanvändes. Ranges och Image API gav de exakta
bildrutterna. De 22 maximala originalbilderna hämtades från Riksarkivets
Image API utan sessionskaka. Chrome och den inloggade sessionen användes
inte, och ingen CAPTCHA eller ALTCHA interagerades med.

- [Records-API-svar](../media/S-0541-riksarkivet-scb-vasterbotten-1868-records-api.json)
- [volymens JSON-LD](../media/S-0541-riksarkivet-scb-vasterbotten-1868-jsonld.json)
- [volymens OAI-EAD](../media/S-0541-riksarkivet-scb-vasterbotten-1868-oai-ead.xml)
- [IIIF-manifest](../media/S-0541-riksarkivet-scb-vasterbotten-1868-A0035803-IIIF-manifest.json)

De 22 nya fulloriginalen och deras individuella checksummor redovisas i
C-0715. S-0541 och C-0705 redovisar Sävars nio fullbilder; S-0547 och C-0711
redovisar de fyra tidigare alternativa församlingsfönstren.
