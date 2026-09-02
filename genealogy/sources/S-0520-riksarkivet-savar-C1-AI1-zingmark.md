# S-0520: Riksarkivet — Sävar C/1 och A I/1, Johan Petter Zingmark

## Källbeskrivning

- Arkiv: Sävar kyrkoarkiv, `SE/HLA/1010199`
- Födelsebok: C/1, 1823–1837, referenskod `SE/HLA/1010199/C/1`,
  Riksarkivet-id `jhPzyZGRDb8aSLomDTa2u0`
- Husförhörslängd: A I/1, 1823–1830, referenskod
  `SE/HLA/1010199/A I/1`, Riksarkivet-id `VlZ2CY6ExKwQR8iB3SyoC6`
- Kontrollerad och bevarad: 2026-08-30
- [C/1 JSON-LD](https://data.riksarkivet.se/archive/jhPzyZGRDb8aSLomDTa2u0.jsonld)
- [A I/1 JSON-LD](https://data.riksarkivet.se/archive/VlZ2CY6ExKwQR8iB3SyoC6.jsonld)

## API-först och reproduktionskoppling

Båda exakta JSON-LD-posterna svarade `200` och angav en
bildrepresentation, men representationerna saknade bild-URI och
reproduktionskod. Den inloggade Riksarkivet-katalogens omdirigeringsadress
exponerade därefter de äldre Arkis-UUID:erna utan att ALTCHA-kontrollen
aktiverades:

| Volym | Arkis-UUID | Publikt `Tree/SubTree`-resultat | Reproduktion |
|---|---|---|---|
| C/1 | `e87fb6b6-6cd0-48d9-91c5-72c0d7640b80` | bildfilsnod | `C0034441` |
| A I/1 | `32c2f87e-8e21-4eed-9a6c-8b0b0dcf6466` | bildfilsnod | `C0034426` |

De officiella, läsbara trädsvaren hämtades från Riksarkivets publika
`/Tree/SubTree/`-slutpunkt. Nakna manifest- och Image API-anrop mot de två
reproduktionerna gav `403`. Som dokumenterad reserv efter API-försöken
användes därför en ny styrd flik i användarens redan inloggade
Riksarkivet-session. Exakta bilder hämtades genom Riksarkivets egen
bildvisare; inga kakor, tokens eller andra sessionsdata lästes eller
bevarades och ingen CAPTCHA aktiverades.

## Födelsenotisen

Sävar C/1, bild `C0034441_00056`, sidan 91, innehåller raden för Botsmark:

- född 1825-02-01;
- döpt 1825-02-15;
- `Johan Petter`;
- far `Bonden Carl Jonas Zingmark`;
- mor `Anna Sophia Holmström`.

Föregående bild `C0034441_00055` omfattar januari 1825 och bevaras som
kronologisk gränskontroll.

## Barndomshushållet

Sävar A I/1, Botsmark, sidan 157, bild `C0034426_00186`, visar i samma
hushåll:

- `Bonde Carl Jon. Zingmark`, född 1785;
- `Hust. Anna Sophia Holmström`, född 1792;
- sonen `Johan Petter`, född `1825 1/2`.

Husförhörslängden är ett oberoende sammanhållet hushållsbelägg som
bekräftar födelsenotisens föräldrapar. Övriga synliga barn förs inte vidare
här utan egen kontrollerad transkription.

## Lokalt bevarat material

| Fil | SHA-256 |
|---|---|
| [C/1 JSON-LD](../media/S-0520-riksarkivet-savar-C1-jsonld.json) | `3e79d7a4816eb0f2fb0be3aea493dd8439c09ff0a03e93d9ee13cef9c85a16fc` |
| [C/1 trädsvar](../media/S-0520-riksarkivet-savar-C1-tree.html) | `10184768b6568948dc3d114a33e43c39fc04b2214367aea1a5f5344ba6ed09a7` |
| [A I/1 JSON-LD](../media/S-0520-riksarkivet-savar-AI1-jsonld.json) | `48122760683f644bf0cc9819f3ae783e9b9b834442123cfcb3812553b3bbaf13` |
| [A I/1 trädsvar](../media/S-0520-riksarkivet-savar-AI1-tree.html) | `74f969f00133151c17a2f411fd02fadd497dd905cdd08afaa2318e210005616a` |

Fulloriginalen och deras dimensioner redovisas i [C-0681](../citations/C-0681-savar-C1-AI1-johan-petter-zingmark-foraldrar.md).

