# C-0587: Sävar C/1 och A I/1 — API fungerar men bild-URI saknas

> Historisk åtkomstcitation. C-0681 supersederar hindret med lösta
> reproduktionskoder, födelsenotisen och barndomshushållet.

## Källor

- [S-0446](../sources/S-0446-riksarkivet-savar-C1-atkomst-2026-08-29.md)
- [S-0461](../sources/S-0461-riksarkivet-savar-AI1-atkomst-1823-1830.md)

## Resultat

Ett nytt URL-kodat API-försök löste den tidigare WAF-spärren för Sävar C/1
och identifierade volymen med Riksarkivet-id `jhPzyZGRDb8aSLomDTa2u0`.
JSON-LD svarade `200`, men bildrepresentationen saknar URI. Samma mönster
gäller A I/1, id `VlZ2CY6ExKwQR8iB3SyoC6`: sök-API och JSON-LD fungerar,
men inget manifest, batch-id eller bild-URI exponeras.

Ingen sida lästes. Johan Peters födelsenotis och det gemensamma hushåll som
skulle kunna pröva Carl Jonas Zingmark och Anna Sophia Holmström är därför
fortsatt åtkomstspärrade. Detta är inte källnoll eller föräldrabekräftelse.

## Bevarade API-original

- `S-0446-riksarkivet-savar-C1-api-retry.json`
- `S-0446-riksarkivet-savar-C1-archive-retry.jsonld`
- `S-0461-riksarkivet-savar-AI-series-api.json`
- `S-0461-riksarkivet-savar-AI1-archive.jsonld`

Exakta SHA-256 och byteantal finns i `genealogy/media-manifest.json`.

## Stött påstående

A-2522; C-0558/A-2454 uppdateras av den lösta API-fasen men deras
bildåtkomsthinder kvarstår.
