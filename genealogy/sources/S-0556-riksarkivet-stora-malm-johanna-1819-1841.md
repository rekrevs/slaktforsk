# S-0556: Riksarkivet — Johanna Jansdotter i Stora Malm 1819–1841

## Källbeskrivning

Tre volymer i Stora Malms kyrkoarkiv bildar en sammanhängande källkedja:

| Volym | Referenskod | Permanent id | Arkis-UUID | Reproduktion |
|---|---|---|---|---|
| In- och utflyttningslängd B/1, 1838–1852 | `SE/ULA/11457/B/1` | `agAerDX9rH6cxG02H087k3` | `d4a8a292-49d8-11d5-a6ed-0002440207bb` | `C0007583` |
| Födelse- och dopbok C/6, 1818–1835 | `SE/ULA/11457/C/6` | `fQAerDX9rH6cxG02H087k3` | `d4a8a2a5-49d8-11d5-a6ed-0002440207bb` | `C0007590` |
| Husförhörslängd A I/13 a, 1819–1821 | `SE/ULA/11457/A I/13 a` | `AQAerDX9rH6cxG02H087k3` | `d4a8a229-49d8-11d5-a6ed-0002440207bb` | `C0007542` |

- Kontrollerat och hämtat: 2026-08-31.
- [B/1 JSON-LD](https://data.riksarkivet.se/archive/agAerDX9rH6cxG02H087k3.jsonld)
- [C/6 JSON-LD](https://data.riksarkivet.se/archive/fQAerDX9rH6cxG02H087k3.jsonld)
- [A I/13 a JSON-LD](https://data.riksarkivet.se/archive/AQAerDX9rH6cxG02H087k3.jsonld)
- IIIF-manifest: [B/1](https://lbiiif.riksarkivet.se/arkis!C0007583/manifest),
  [C/6](https://lbiiif.riksarkivet.se/arkis!C0007590/manifest) och
  [A I/13 a](https://lbiiif.riksarkivet.se/arkis!C0007542/manifest).

## API- och bildväg

Records-API:t identifierade alla tre volymerna som digitaliserade, men
JSON-LD-posterna exponerade ingen bild-URI. Den inloggade externa
Chrome-sessionen användes därför endast för att diagnostisera de äldre
Arkis-id:na i omdirigeringsadresserna. Både den exakta B/1-routen och en
vanlig sökning efter `Stora Malm B/1` visade ALTCHA även utanför sandboxen.
Ingen ruta aktiverades, ingen kontroll löstes och inga sessionsdata lästes
eller sparades.

Riksarkivets publika batch-endpoint band därefter respektive Arkis-UUID och
referenskod till reproduktionerna ovan utan sessionskaka. De tre officiella
IIIF-manifesten och maximala originalbilderna gick att hämta med
Riksarkivets bildvisare som `Referer`.

## Utflyttning till Bettna 1841

Stora Malm B/1 bild `C0007583_00018` har 1841 års in- och utflyttade på
samma uppslag. Utflyttningspost 27 anger `Pigan Johanna Jansd:r`, från
källformen `Backstugan`, till **Bettna**. Dagfältet är tomt och får inte
fyllas från närliggande rader.

Posten är den reciproka originalkontrollen till Bettna A I/11 a sida 33,
som anger Johanna Jonsdotter inflyttad `41 St. Malm`. Namnformen, året och
destinationen sammanfaller; B/1 lägger inte till födelsedatum eller
äktenskapsuppgift.

## Födelse och Walla-hushåll

Stora Malm C/6 bild `C0007590_00021`, post 39, anger **Johanna**, född
1819-05-30 och döpt 31 maj. Föräldrarna skrivs hemmansbrukaren **Jan
Ericson** och hans hustru **Lena Jonsdotter** i Walla.

A I/13 a sida 80, bild `C0007542_00090`, bekräftar samma hushåll i Walla:

- brukaren Jan Ericson, född 1791-05-09 i Björkvik;
- hustrun Lena Jonsdotter, född 1785-10-31 i Stora Malm;
- dottern Johanna Jansdotter, född 1819-05-30 i Stora Malm.

Födelseboken och husförhörslängden sammanfaller alltså i namn, exakt datum,
föräldrapar och plats. Tillsammans med Bettna-längdens exakta datum och B/1:s
reciproka destination identifierar detta starkt Johanna i
Grill-kandidathushållet. Det löser däremot inte identitetsluckan mellan
kandidatfamiljens strykning 1852 och den vuxne Erik Karlsson 1875–1876.
Jan Ericson och Lena Jonsdotter förs därför inte in som P-0133:s morföräldrar
och ingen ny föräldrarelation skapas.

## Lokalt bevarad metadata

| Fil | SHA-256 |
|---|---|
| [B/1 records-API](../media/S-0556-riksarkivet-stora-malm-B1-records-api.json) | `4bf76c38e074eb41c6add62a4e0426ab55efd398561aa2fe407b538d45c6a53f` |
| [B/1 JSON-LD](../media/S-0556-riksarkivet-stora-malm-B1-jsonld.json) | `3cfeeb18f41431f3d0feee1590cd3b89ea29165fcd76ee826d27a73730850f11` |
| [B/1 batchsida](../media/S-0556-riksarkivet-stora-malm-B1-batch.html) | `5ecaa50bce23aeeadb50b1efb8ac2ed5b2b7bb63f5d3d656300a7e449a7db1eb` |
| [B/1 IIIF-manifest](../media/S-0556-riksarkivet-stora-malm-B1-C0007583-IIIF-manifest.json) | `899a094e25ddb0c0b41ca62bb3b264dfc7da912820e70c75bb4316462370fcbd` |
| [C/6 records-API](../media/S-0556-riksarkivet-stora-malm-C6-records-api.json) | `9be97971d7ad9890f9a5cb539692ad975b84ce0fe75bcf280af8928e89cbcdbc` |
| [C/6 JSON-LD](../media/S-0556-riksarkivet-stora-malm-C6-jsonld.json) | `b59682cae074095d1be2c21b0064d0740f9cd88855105d4e4d8198f801e51f18` |
| [C/6 batchsida](../media/S-0556-riksarkivet-stora-malm-C6-batch.html) | `a205447a17fa4160259bfa9974cfbc0b419be8fd9cb11d3d317f03082372b3b9` |
| [C/6 IIIF-manifest](../media/S-0556-riksarkivet-stora-malm-C6-C0007590-IIIF-manifest.json) | `5629407efe3c9d7d418967573965e4492fc2e85f1c9f11dd660eae73a26ffb64` |
| [A I/13 a records-API](../media/S-0556-riksarkivet-stora-malm-AI13a-records-api.json) | `4be7843aaa74e930c978839c8bf787dc6f526a9179c1ea30539555cea511242b` |
| [A I/13 a JSON-LD](../media/S-0556-riksarkivet-stora-malm-AI13a-jsonld.json) | `57828e25153997d3bd8e21b247a50a71547c5b59c8c7360dc1cbaa3a23dd8f50` |
| [A I/13 a batchsida](../media/S-0556-riksarkivet-stora-malm-AI13a-batch.html) | `0a0fcc2dd403bb81447e1b3f7ab58be551172ac6d5d6b4fb90196152c7ab8236` |
| [A I/13 a IIIF-manifest](../media/S-0556-riksarkivet-stora-malm-AI13a-C0007542-IIIF-manifest.json) | `b209a8545632bfad11fa80b3a005d05079a7a41fef10d1f0270d5afe688a26cb` |

Fulloriginalen och den sammansatta identitetsbedömningen redovisas i
[C-0721](../citations/C-0721-stora-malm-johanna-jansdotter-1819-1841.md).

