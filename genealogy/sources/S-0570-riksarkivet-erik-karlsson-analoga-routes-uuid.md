# S-0570: Riksarkivet — Erik Karlssons analoga källvägar, UUID-omprov

## Källbeskrivning

Källpaketet omprövar fem redan identifierade analoga eller läsesalsbundna
vägar för P-0133 Erik Karlsson och den ännu olösta vistelsen 1867–1875.
Grundmetadata och källrelevans finns i [S-0247](S-0247-riksarkivet-vingakers-fogderi-katalog-1875.md),
[S-0248](S-0248-riksarkivet-sodermanlands-regemente-D14-10.md),
[S-0527](S-0527-riksarkivet-ardala-forssa-HII-flyttningsbilagor.md),
[S-0531](S-0531-riksarkivet-villattinge-bouppteckningar-1935.md) och
[S-0535](S-0535-riksarkivet-flen-lysningskallor-1895.md). Endast
Riksarkivet användes. Omprovet gjordes 2026-09-01.

## Exakta äldre katalog-id:n

De beständiga katalogposterna exponerade följande äldre Arkis-UUID:er:

| Route | Permanent id | Referenskod | Arkis-UUID |
|---|---|---|---|
| Forssa H II/1, flyttningsbilagor 1851–1890 | `iDJysMmaweZJTe018W43t3` | `SE/ULA/10279/H II/1` | `b2fdd4b0-49d8-11d5-a6ed-0002440207bb` |
| Villåttinge C II b/5, bouppteckningsregister 1933–1938 | `1ne7pFLAjaAWr0Z0SLNN70` | `SE/ULA/11693/C II b/5` | `cc071a07-4af5-42b6-a0d4-08c07155d71c` |
| Villåttinge F II/59, bouppteckningar 1935–1936 | `K6LKgLnlhaQoLa0flJzzL5` | `SE/ULA/11693/F II/59` | `a9546550-6f5c-46ae-b256-4029bd3ffd55` |
| Flen P I/1, pålysningsböcker 1849–1926 | `HTliVxXUWKwLP15z2zAhMF` | `SE/ULA/10257/P I/1` | `7fecdb45-5eb8-4e81-9564-117e17caad6f` |
| Södermanlands regemente D14/10, beväringsmönsterrullor 1871–1875 | `bVWWVwd2Lqz8tdLeklSj21` | `SE/KrA/0108/A/001:Ö/D14/10` | `7f20f895-c2a9-4f57-91bc-ead175ee5a11` |

Häradsskrivaren i Vingåkers fögderi, `SE/ULA/10459`, har permanent id
`uRn6bDX9rH6cxG02H087k3` och äldre Arkis-UUID
`9446bce1-49d8-11d5-a6ed-0002440207bb`.

UUID:erna lästes ur Riksarkivets egna omdirigeringsadresser i en ansluten
Chrome-session. Katalogvyerna stannade på ALTCHA även utanför sandboxen;
kontrollrutan berördes inte. Inga kakor, token, lagringsvärden eller andra
sessionsdata lästes eller bevarades.

## Publikt arkivträd och batchroute

Riksarkivets publika `Tree/SubTree` öppnades direkt i Chrome för C II b/5,
F II/59, P I/1 och D14/10. Varje svar hade tom synlig kropp och saknade
bildbarn eller reproduktionskod. Forssa H II/1:s motsvarande tomma trädsvar
var redan bevarat i S-0527. Den exakta publika batchrouten prövades för
samtliga fem volymer med UUID och referenskod; varje väg visade
Riksarkivets sida `Ett fel har inträffat` och exponerade inget bild-id.

Vingåkers fögderis fondträd visade fortfarande endast barnet `K Kartor`,
UUID `11803c49-9f2a-4e83-b420-679c2562c3a9`. Ingen mantalsserie eller
itemiserad Forssa-volym för 1875 visades. Tre snäva omprov mot records-API:t
för Vingåker, Oppunda/Villåttinge och Forssa 1875 stoppades av Riksarkivets
WAF före ett API-svar. De är därför åtkomstincidenter, inte söknoll.

Direkta HTTP-anrop till `sok.riksarkivet.se` stoppades på samma sätt med
HTTP 403 innan målsvaren kunde läsas. De faktiska träd- och batchvyerna ovan
lästes därför genom Chrome, i linje med användarens åtkomstinstruktion.

## Slutsats och återaktivering

Omprovet gav exakta, framtida digitaliseringsnycklar men ingen ny
originalbild eller persontext. Forssa H II/1 kvarstår som första källa för
attesten bakom B/3 post 14, Erik Carlsson mottagen 1876-04-30 från Årdala
till Stafsjön, folio 87. Mantalsvägen kräver den äldre gemensamma
förteckningsvolymen; D14/10 kräver beställning eller läsesal. För den sena
berikningen läses C II b/5 före F II/59, och P I/1 beställs med Flens
vigselpost 5 den 1895-12-28 som ankare.

Tomma träd och felsidor visar endast aktuellt exponeringsläge. De visar inte
att handlingarna saknas, att de aldrig har reproducerats eller att Erik
saknas i dem. Ompröva digital väg först när JSON-LD får en bild-URI,
fondträdet får nya serier eller Riksarkivets träd-/batchslutpunkt ändras.

Den rensade browserobservationen och slutsatsgränsen redovisas i
[C-0737](../citations/C-0737-erik-karlsson-analoga-routes-atkomstomprov.md).

