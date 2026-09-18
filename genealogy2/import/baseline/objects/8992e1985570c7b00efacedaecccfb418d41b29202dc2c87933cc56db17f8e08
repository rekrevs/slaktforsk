# C-0977: ALTCHA hävd av ägaren, och vad bouppteckningsregistret faktiskt täcker

## Källa

[S-0409](../sources/S-0409-riksarkivet-bouppteckningsregister-abraham-jonsson.md)

## Vad som hände

**2026-09-06 löste ägaren själv ALTCHA-verifieringen** i sin inloggade
Chrome och öppnade därmed Riksarkivets katalog- och specialsökssidor för
sessionen. Agenten löste ingen captcha; det förbudet står fast.

Kontroll omedelbart efteråt, i samma flik:

| Adress | Status |
|---|---|
| `sok.riksarkivet.se/bouppteckningar` | **200** |
| `sok.riksarkivet.se/nad` | **200** |
| `sok.riksarkivet.se/dodregister` | **200** |
| `sok.riksarkivet.se/arkiv/<id>` | **200**, hela förteckningsträdet renderas |

Spärren hade sedan 2026-09-05 bokförts som hinder i fem profiler: P-0016,
P-0028, P-0029, P-0048 och P-0049.

## Den viktigaste konsekvensen: NAD-trädet

Katalogsidan visar **hela förteckningen med `Bild`-länk per volym**, vilket
metadatasökningen inte gör. Direkt vid första användningen gav den en serie
som varit osynlig: **Adolf Fredriks `E IV` Register till lysnings- och
vigselböcker**, vars volym `/4` täcker **1903–1943 i ett enda alfabetiskt
register** ([S-0760](../sources/S-0760-adolf-fredrik-lysning-vigsel-register.md)).
Den uppslagningen löste på minuter en fråga som annars hade krävt en
svepning av sex årgångars vigselbok
([C-0976](C-0976-ekholm-alund-vigsel-1903-adolf-fredrik.md)).

## Den näst viktigaste: bouppteckningsregistret täcker inte de begärda åren

Sökformuläret på `/bouppteckningar` är en GET-form med fälten `Fornamn`,
`Efternamn`, `Hemort`, `Hemforsamling`, `DatumFran`, `DatumTill`, `Yrke`,
`AnhorigFornamn`, `AnhorigEfternamn` och `Lan`. Träfflistan renderas med
javaskript och måste läsas i fliken.

Fyra kontroller 2026-09-06:

| Sökning | Utfall |
|---|---|
| `Efternamn=Andersson`, `Hemforsamling=Burträsk`, alla år | 102 rader, **högsta årtal 1910** |
| `Hemforsamling=Burträsk`, 1900–1929 | 102 rader, **högsta årtal 1910** |
| `Hemforsamling=Burträsk`, 1930–1960 | **0 träffar** |
| `Hemforsamling=Hyltinge`, alla år | 102 rader, år **1765–1908** |
| `Hemforsamling=Hyltinge`, 1909–1970 | **0 träffar** |
| `Efternamn=Ekholm`, 1905–1925, hela riket | 52 rader, ingen Axel Vilhelm |

**Registret slutar 1910 för Burträsk och 1908 för Hyltinge.** De
bouppteckningar som fem profiler pekat på — efter Anders Alfred Andersson
1949, efter Anna Fredrika 1947, efter Axel Vilhelm Ekholm 1913 och efter
Hulda Amalia Ekholm 1964 — ligger alltså **utanför registrets omfång**.

Det ändrar hur hindret ska beskrivas. Vägen var aldrig bara *spärrad*: den
**täckte inte de efterfrågade åren**. Bouppteckningarna finns i respektive
domsagas häradsrättsarkiv och måste sökas där, inte i registret. Att
formulera hindret som "bakom ALTCHA" var en felaktig, om än i god tro
gjord, beskrivning i P-0016, P-0028, P-0029, P-0048 och P-0049.

## Vad som fortfarande gäller

Ägarens captchalösning gäller **denna session**. Regeln står fast: agenten
löser aldrig en ALTCHA eller annan människoverifiering, och en spärr som
återkommer ska bokföras som hinder och lämnas till ägaren.

## Stödda påståenden

Rättelse av hinderbeskrivningen i KP-02 i [P-0048](../research-profiles/P-0048.md)
och [P-0049](../research-profiles/P-0049.md), KP-04 i [P-0016](../research-profiles/P-0016.md),
KP-02 i [P-0028](../research-profiles/P-0028.md) och KP-02 i
[P-0029](../research-profiles/P-0029.md).

## Tillägg T-0125, 2026-09-07: jurisdiktion och gammalt åtkomsthinder

Den redan dokumenterade hävningen av ALTCHA den 6 september 2026
ersätter det äldre hindret vid den passagen. Ett gammalt captcharesultat
är inte ett aktuellt bevis på källslut. Ingen ny åtkomst har prövats här.

En uppgift om att det särskilda registrets Hyltinge-täckning slutar 1908
avgör inte om Hulda Amalias bouppteckning efter döden 1964 finns: hennes
hemort är då Flen enligt C-0923. Den avgör inte heller makens
bouppteckningsväg 1913, eftersom C-0952 anger Katarina som hans
kyrkobokföringsort, medan dödsplatsen var Helgesta. Rätt domstolsområde
och katalog-/registertäckning måste prövas personbundet. S-0750/C-0961:s
redan dokumenterade domstolskatalogprov tillgodoräknas, men ett register-
eller bildlänksnoll är inte bevis för att bouppteckning aldrig upprättades.
