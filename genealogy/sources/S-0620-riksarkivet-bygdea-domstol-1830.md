# S-0620: Riksarkivet — Bygdeå domstolskällor och renoverade kopior 1830

## Källbeskrivning

Denna kontroll använder endast Riksarkivet och prövar en tidigare oprövad
källfamilj för P-0051:s olösta ursprung: rättsliga handlingar som kan bära
faderskaps-, underhålls- eller förmynderskapsuppgifter kring ett barn antecknat
som `oäkta`. Kontrollen gäller katalog, hierarki, tidsomfång och fjärråtkomst;
ingen domstolshandling eller personpost har lästs.

- Lokalt arkiv: `SE/HLA/1040105`, *Bygdeå tingslags häradsrätts arkiv*
- Arkivbildare: Bygdeå tingslags häradsrätt
- Förvarande institution: Riksarkivet i Härnösand
- Hovrättskopior: `SE/RA/420422/02`, *Svea Hovrätt, Advokatfiskalens arkiv*
- Förvarande institution för hovrättskopiorna: Riksarkivet i
  Stockholm/Täby, depå Marieberg
- Kontrollerat: 2026-09-02

## Bygdeå tingslags häradsrätt

Riksarkivets records-API, JSON-LD och OAI-EAD identifierar följande exakta
målårsleder:

| Serie/volym | Datering | Records-id | Kataloganmärkning |
|---|---|---|---|
| `A I a/41`, domböcker vid ordinarie ting | 1830 | `97jjgVRzkI9Um25ZnKVPs0` | — |
| `A I b/5`, domböcker och protokoll vid urtima ting | 1819–1830 | `CpVQ8WfQpKIk9tuTgjynH2` | `Kapsel.` |
| `A II/10`, småprotokoll | 1830–1834 | `aE1A5xPFR4cG8dUnwDJM52` | — |
| `F I/1`, inneliggande handlingar | 1805–1865 | `cmzy2AdKzgdLIxt4Af5AyR` | spridda år |

JSON-LD anger `Analog` representation för samtliga fyra volymer. De exakta
posterna öppnades också i ägarens inloggade Chrome-session. Varje post visade
endast `Läsesal` och saknade bildlänk. Ingen ny CAPTCHA/ALTCHA visades, ingen
kontroll eller sessionsdata rördes och ingen läsesals- eller kopiebeställning
skapades.

F I/1:s detaljerade anmärkning namnger en Robertsforsförteckning från 1819,
memorialdomböcker 1837, ett saköreslängdskoncept 1845 samt stämnings- och
uppskovslistor 1855–1860. Den anger inget särskilt 1830-block. Volymen är
därför inte en avgränsad digital omväg till målåret.

Den särskilda serien `C II`, *Förmynderskapsböcker med register*, innehåller
endast volym 1, 1867–1888, och volym 2, 1888–1901. Det finns alltså ingen
katalogiserad särskild förmynderskapsbok för 1830 i denna serie. Det är ett
serie- och tidsomfångsresultat; det utesluter inte att förmynderskapsärenden
kan finnas i domböcker eller småprotokoll.

## Svea hovrätts renoverade kopior

JSON-LD-hierarkin ledde från Advokatfiskalens arkiv till `E XI`, *Renoverade
domböcker*, och dess underserie `E XI e`, *Häradsrätters renoverade
domböcker*. Serien är enligt katalogen länsvis ordnad till och med 1845.
Records-API:t gav två exakta Västerbottenvolymer för 1830:

| Referenskod | Anmärkning | Records-id | Representation/åtkomst |
|---|---|---|---|
| `SE/RA/420422/02/E/E XI/E XI e/4118` | Västerbottens län nr 154 | `7wFsAGzcEwHJAhAPYG0kr2` | `Analog`; `Läsesal` |
| `SE/RA/420422/02/E/E XI/E XI e/4119` | Västerbottens län nr 155 | `FYBnE2U0xq6hnTlr002wP1` | `Analog`; `Läsesal` |

Katalogen anger inte vilken av de två som innehåller Bygdeå. Båda exakta
poster öppnades inloggat och saknar bildlänk.

Under `E XII`, *Renoverade småprotokoll*, anger under Serien `E XII b` att
förkortningarna `T`, `TÄB` och `F` kan omfatta bland annat
förmynderskaps-, äktenskapsförords- och bouppteckningsprotokoll. För 1830
finns sju delar, volymerna `/384`–`/390`. Varje del anger `Register saknas`
och varje JSON-LD-post har endast analog representation. Del 1 kontrollerades
dessutom i den inloggade katalogen och visade bara `Läsesal`. Den publika
katalogen kan därför inte avgöra vilken del som omfattar Bygdeå utan att
originalen läses.

## Forskningsresultat och avgränsning

Den juridiska källfamiljen är nu exakt routad men inte fjärrläsbar. Först bör
`A I a/41` prövas för ordinarie mål 1830, därefter `A I b/5` för urtima mål
och `A II/10` för småprotokoll. Hovrättens två Västerbottenvolymer och sju
oindexerade småprotokollsdelar är alternativa analoga kopieleder, inte lästa
personkällor.

Ingen akt, dom, namnrad eller person har lästs. Metadatan belägger därför
varken att Barbro förekommer eller saknas, att ett faderskaps- eller
underhållsmål existerade, eller vem hennes föräldrar eller vårdnadshavare
var. Bygdeå H III/1 förblir den mest födelsenära förstahandsvägen; denna nya
domstolsroute återtas först vid ändrad digital åtkomst eller en ny akt-,
tings- eller ärendenyckel.

## Bevarat underlag

| Underlag | SHA-256 |
|---|---|
| [Strukturerad katalog- och åtkomstobservation](../media/S-0620-riksarkivet-bygdea-domstol-1830-observation.json) | `6d1b66044e6b581d04d67db78b9a7f69e33323b1266ecb45c4c5bd9a67f84d40` |
| [Filtrerade records-API-poster, Bygdeå häradsrätt](../media/S-0620-riksarkivet-bygdea-domstol-1830-records.json) | `661e82d9e3800081f8d2d84369e66b8a607b7672c56ebe06288d42f81eb89fdc` |
| [Samlade JSON-LD-original, Bygdeå häradsrätt](../media/S-0620-riksarkivet-bygdea-domstol-1830-jsonld.json) | `78f24263f969ad28b45fe0b4936ce808f43d50effbc97ee27e6f00b9ae999870` |
| [OAI-EAD, F I/1](../media/S-0620-riksarkivet-bygdea-FI1-oai-ead.xml) | `88896d5ca525d1c329e81907d9e5d8e3097d9940f8fcbcdb43d5b63ddae7ec6e` |
| [OAI-EAD, C II](../media/S-0620-riksarkivet-bygdea-CII-oai-ead.xml) | `9f680e951f54eec88f297b6e15b7391a0fb659aa5054b21523428d8d38e6b832` |
| [Filtrerade records-API-poster, renoverade kopior 1830](../media/S-0620-riksarkivet-svea-renoverade-1830-records.json) | `9bc258a9f2f768cf82a2989fa24b5ee397bbd461a1f6b9e60d010ebaf348582b` |
| [Samlade JSON-LD-original, nio renoverade målårsvolymer](../media/S-0620-riksarkivet-svea-renoverade-1830-jsonld.json) | `e55b811aa0e3e293b5689fe6772f23e83b6d0c2f234475dcba82763a9fe63731` |
| [JSON-LD, serien E XI e](../media/S-0620-riksarkivet-svea-E-XIe-series.jsonld) | `7735b229b998838f5a5316cdd606be002fd86d591b116e83c91eba15714d551e` |
| [JSON-LD, serien E XII b](../media/S-0620-riksarkivet-svea-E-XIIb-series.jsonld) | `c9def2dc20b63b8e917cee051054b011e21c6f5f24a3d86919c8173200321d80` |

## Stödda påståenden

A-3079–A-3081.
