# S-0544: Riksarkivet — Södermanlands regemente 1851 och Grills indelningsverksregister

## Källbeskrivning

- Institution: Riksarkivet, Krigsarkivet
- Arkiv: Generalmönsterrullor, arkiv med löpande volymnumrering,
  `SE/KrA/0023`
- Volym: `SE/KrA/0023/0/162`, 1851
- Reproduktion: `A0028136`, 394 bildytor
- IIIF-manifest:
  <https://lbiiif.riksarkivet.se/arkis!A0028136/manifest>
- Kompletterande register: [Indelningsverket (Grill)](https://sok.riksarkivet.se/grill)
- Forskningsguide:
  [Generalmönsterrullor och rullor](https://riksarkivet.se/Media/pdf-filer/sth/1-1.pdf)
- Kontrollerat: 2026-08-31; korrigerande maxoriginal och registerrouting
  2026-09-01

## API- och bildrouting

Det publika IIIF-manifestets struktur delar 1851 års volym i åtta
kompanier och ger följande startbilder:

| Kompani | Startbild |
|---|---|
| Livkompaniet | `A0028136_00044` |
| Vingåkers kompani | `A0028136_00087` |
| Nyköpings kompani | `A0028136_00126` |
| Oppunda kompani | `A0028136_00167` |
| Strängnäs kompani | `A0028136_00213` |
| Österrekarne kompani | `A0028136_00261` |
| Västerrekarne kompani | `A0028136_00301` |
| Gripsholms kompani | `A0028136_00348` |

Manifestet användes för att gå direkt till den sida där nummer 36 står i
respektive kompani. Bilderna hämtades via Riksarkivets IIIF-server med den
egna bildvisarsidan som `Referer`. Den första läsningen gjordes utan Chrome.
Efter den inloggade återaktiveringen 2026-09-01 kunde Grills register binda
Glippsta nummer 36 till Livkompaniet. Livkompaniets maxoriginal visar
`Glippsta` och `Carl Fredric Drill`; den äldre reducerade läsningen som en
annan man är fel och dokumenteras som avvisad i C-0708/C-0752.

Riksarkivets forskningsguide förklarar att rullorna har både ett nummer
inom hela regementet och ett kompaninummer. Kyrkoböcker kan i stället
hänvisa till rote- eller rusthållsnumret, medan Grills register använder
kompaninumret. Den synliga siffran `36` i Bettna A I/13 a kan därför inte
utan ytterligare routing behandlas som ett entydigt kompaninummer.

## Grills register och åtkomstgräns

Riksarkivets sida beskriver Grills register som ett sätt att söka fram
boställe, rusthåll och rote samt tillhörande kompani och regemente. Källan
är Claes Lorentz Grills *Statistiskt sammandrag af Svenska
indelningsverket*, utgivet 1855–1858.

Den generiska söksidan kunde hämtas och innehåller Bettna som valbar
socken. Den exakt avgränsade GET-frågan returnerade i den historiska
körningen `403 Web Application Firewall`. Efter att användaren själv hade
loggat in och redan besvarat CAPTCHA-utmaningen öppnade den användarägda
Chrome-sessionen Bettna-frågan. Bland 30 träffar anger post `Grill_21584`
Glippsta nummer 36 som rust-/rotehåll i Livkompaniet vid Södermanlands
regemente. Agenten löste ingen ny CAPTCHA och läste inga sessionsdata.

## Källkritik

1851 års generalmönsterrulla är en samtida militär originalkälla. Den
tidigare åttakompanislutsatsen var fel därför att Livkompaniets rad 36
felläses i den reducerade bilden. Sju andra kompanirader avser andra män;
Livkompaniets rad är den positiva Glippsta-raden. Grills register är en
senare tryckt sammanställning och används som routing, medan personen
identifieras i rullans original tillsammans med husförhörskedjan.

## Lokalt bevarat material

| Fil | SHA-256 |
|---|---|
| [IIIF-manifest](../media/S-0544-riksarkivet-gmr-1851-A0028136-IIIF-manifest.json) | `0db4122d5943f200f3e43e67b298e1e17c758e2a8d77d3c968d504c023ce23ff` |
| [Grills generiska söksida](../media/S-0544-riksarkivet-grill-search.html) | `ecf4b6a8aacd3b4011e8c9f2f685a156640fb0e6586526ffe11d598a2caa152c` |
| [Bettna-frågans WAF-svar](../media/S-0544-riksarkivet-grill-bettna-WAF.html) | `0ea48bade5f509f395f3bd0d154509dd25e2caabbebccf35e2d73346b8766e8b` |

De åtta lästa rullbilderna, med bild-id, dimensioner och checksummor,
redovisas i [C-0708](../citations/C-0708-sodermanlands-regemente-nr36-grill-atkomst.md).
Den korrigerande maxbilden och jämförelserna 1848/1855 redovisas i
[C-0752](../citations/C-0752-glippsta-nr36-carl-fredric-grill-1848-1855.md).
