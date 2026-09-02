# S-0549: Riksarkivet — TORA för Bettna och alternativa militära förband

## Källbeskrivning

- Institution: Riksarkivet
- Topografipost: Glippsta, TORA-id `2443`
- Topografipost: Bettna församling, TORA-id `048208000`
- Arkiv: Generalmönsterrullor, `SE/KrA/0023`
- Volym: `SE/KrA/0023/0/226`, 1848–1851
- Permanent Riksarkivet-id: `BhJCd0B8wKUT8IPJ5O9AT3`
- Reproduktion: `A0028201`, 458 bildytor
- [IIIF-manifest](https://lbiiif.riksarkivet.se/arkis!A0028201/manifest)
- Volym: `SE/KrA/0023/0/832`, 1851
- Permanent Riksarkivet-id: `AeGlGBvofaUznP9yH8MzQ8`
- Reproduktion: `A0028846`, 359 bildytor
- [IIIF-manifest](https://lbiiif.riksarkivet.se/arkis!A0028846/manifest)
- Kontrollerat: 2026-08-31

## Topografisk routing

Riksarkivets records-API återger Glippsta som en bebyggelseenhet under
Bettna församling. Bettna-postens TORA-relationer namnger samtidigt tre
militära indelningar:

- Södermanlands regemente 04, TORA-id `4040000001002`
- Livregementets husarer 04, TORA-id `4040000001003`
- Livregementets grenadjärer 04, TORA-id `4040000001004`

Relationerna ligger på församlingsnivå och är daterade `0–9999`. De visar
därför att den tidigare kontrollen av Södermanlands regemente inte tömde
alla förbandsmöjligheter, men de binder inte Glippsta, året 1851 eller Carl
Erik Grill till något av de tre förbanden.

## API- och IIIF-routing till rullorna

Records-API och OAI-EAD identifierar volym 226 som Livregementets
grenadjärkårs rulla med delar för 1848 och 1851. IIIF-manifestet ger fyra
kompanier i båda årgångarna:

| Kompani | Start 1848 | Start 1851 |
|---|---|---|
| Livkompaniet | `A0028201_00044` | `A0028201_00271` |
| Östra Västmanlands kompani | `A0028201_00086` | `A0028201_00307` |
| Södermanlands kompani | `A0028201_00135` | `A0028201_00349` |
| Kungsörs kompani | `A0028201_00180` | `A0028201_00392` |

Volym 832 är Livregementets husarers rulla 1851. Manifestet ger fem
skvadroner:

| Skvadron | Start 1851 |
|---|---|
| Örebro skvadron | `A0028846_00053` |
| Livskvadronen | `A0028846_00074` |
| Östra Närkes skvadron | `A0028846_00123` |
| Västra Närkes skvadron | `A0028846_00164` |
| Vadsbo skvadron | `A0028846_00210` |

Manifestens ranges användes för att gå direkt till nummer 36 i varje
avgränsad kompani-/skvadronårgång. Records-API, JSON-LD, OAI-EAD, IIIF-
manifest och fullbilder lästes direkt; Chrome och en inloggad session
behövdes inte. Ingen CAPTCHA eller ALTCHA interagerades med.

## Källkritik

TORA är en orts- och indelningsroute, inte en personkälla. De odaterade
församlingsrelationerna kan inte ensamma avgöra vilket förband Glippsta
soldattorp tillhörde vid mitten av 1800-talet. Generalmönsterrullorna är
samtida militära originalkällor, men kontrollen av nummer 36 svarar bara på
den uttryckligen prövade nummerhypotesen. Den utesluter inte rote- eller
rusthållsnummer, andra nummersystem, ett annat år eller ett annat förband.
Ingen identitet eller föräldrarelation skapas.

## Lokalt bevarad metadata

| Fil | SHA-256 |
|---|---|
| [TORA records-API](../media/S-0549-riksarkivet-tora-bettna-glippsta-records-api.json) | `8868448dd81884a4ed216f51bd67d295a1df0f754c88c6dc0726245d343655b4` |
| [Bettna JSON-LD](../media/S-0549-riksarkivet-tora-bettna-jsonld.json) | `ce9d370dd4e5379de3698912cb945255f7bdf87d6e5b31100c8daa295c3ee3f7` |
| [Glippsta JSON-LD](../media/S-0549-riksarkivet-tora-glippsta-jsonld.json) | `28ddb8617daa9691d372a9029249a34259712e8248dc7c9a90d8e2e8cbc9e896` |
| [Generalmönsterrullornas fond-OAI-EAD](../media/S-0549-riksarkivet-gmr-fonds-oai-ead.xml) | `004543fe0239b742febac0a893b302d1828b93ab43d893a6081ab8d221428c25` |
| [Volym 226 records-API](../media/S-0549-riksarkivet-gmr-226-records-api.json) | `37f27e26bc88b5d8d311d8ff1e9e7baf1fc39ac5fb11acbda937e70a378f57d9` |
| [Volym 226 OAI-EAD](../media/S-0549-riksarkivet-gmr-226-oai-ead.xml) | `5be2d25647ad3ca402495b9e0b6f2344d076a6131b77f9e87743e4ba51334b8a` |
| [Volym 226 IIIF-manifest](../media/S-0549-riksarkivet-gmr-226-A0028201-IIIF-manifest.json) | `a9e3ed3fe23a7e9841c18215745a4dd8db220ff3c13b8b34ab20bd66e8a41371` |
| [Volym 832 records-API](../media/S-0549-riksarkivet-gmr-832-records-api.json) | `a17aa0e90191e0bec832316347f730f69ff4ebb9c949a9f5bb1ed1eac73b116b` |
| [Volym 832 OAI-EAD](../media/S-0549-riksarkivet-gmr-832-oai-ead.xml) | `c5fe37b5c766df2e5db6163a821b7654c0d59725718f396cdb8b891ed4b8343e` |
| [Volym 832 IIIF-manifest](../media/S-0549-riksarkivet-gmr-832-A0028846-IIIF-manifest.json) | `ff21adbb4d5bb93b376a177e35915d848ab45e945f8a786240b8e6a404d2eb59` |

De tretton lästa rullbilderna redovisas i
[C-0713](../citations/C-0713-bettna-tora-grenadjar-husar-nr36.md).
