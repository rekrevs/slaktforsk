# S-0534: Riksarkivet — Hemsjö H V, bilagor till lysnings- och vigselboken

## Källbeskrivning

Källpaketet avgränsar den möjliga bilagevägen till Olaus Fredberg
Fredrikssons och Britta Stina Svensdotters vigsel i Hemsjö 1877-09-20.
Hemsjö E/1 sida 33, post 6, har en samtida notering om ett prästbetyg från
Kungsholm för Olaus.

Riksarkivets JSON-LD för Hemsjö kyrkoarkiv, `SE/GLA/13204`, listar den
särskilda serien `SE/GLA/13204/H V`, **Bilagor till lysnings- och
vigselboken**. Serieposten har permanent id `ytVyx6VTyg8qta00I810yx`, men
saknar underliggande `schema:hasPart`, datering och bildrepresentation. Den
har endast en fysisk, analog instansiering. Records-API:ets första träff på
referenskoden återger samma serie utan volym- eller årsinnehåll.

Kontrollerat och bevarat 2026-08-30. Endast Riksarkivet användes.

## Digital åtkomstdiagnos

E/1 och H V har olika digitalt läge:

- E/1:s JSON-LD har en uttrycklig IIIF-länk till reproduktionen
  `00099267`;
- IIIF-manifestet svarar publikt och omfattar 52 bildytor, där
  `00099267_00035` identifieras som **Bild 35 / Sida 33**;
- H V:s JSON-LD saknar både bildinstansiering, `schema:image` och
  katalogiserad volym.

Den saknade vigselbilagan kan därför inte behandlas som ett trasigt
bildanrop till E/1. Riksarkivets maskinläsbara katalog tillhandahåller ingen
H V-volym eller reproduktionskod att anropa. Detta bevisar inte att
prästbetyget aldrig fanns eller att ingen analog handling kan finnas utanför
den exponerade förteckningen.

Ett försök att läsa OAI-EAD gav HTTP 403, men JSON-LD, records-API och E/1:s
IIIF-manifest gav den nödvändiga avgränsningen. Chrome användes inte för
denna kontroll och ingen CAPTCHA interagerades med.

## Lokalt bevarat metadataunderlag

| Fil | SHA-256 |
|---|---|
| [Hemsjöfondens JSON-LD](../media/S-0534-riksarkivet-hemsjo-fond-jsonld.json) | `ba1b788d23b433953d41219b652ed96b751192b670c5b614b538f3c725874965` |
| [H V-seriens JSON-LD](../media/S-0534-riksarkivet-hemsjo-HV-jsonld.json) | `0380ab68750e44dffefc4335cc4af63bb30fa91cf39009a8155ec8bf8b98aaa6` |
| [records-API, första träffen](../media/S-0534-riksarkivet-hemsjo-HV-api.json) | `64386750aefac03537cb49c299cc2359fc50ffedfe986ed83a50eea952adea06` |
| [E/1-volymens JSON-LD](../media/S-0534-riksarkivet-hemsjo-E1-jsonld.json) | `a752ae96c686438ef4afc863deb5e97dbdbe92cbad79913f29a7ecc0a51f3242` |
| [E/1:s IIIF-manifest](../media/S-0534-riksarkivet-hemsjo-E1-IIIF-manifest.json) | `6012749b8d0df7f56cc86632211273779a5b453588e367fc5522d8a0481b4860` |

Originalradens läsning, slutsatsgräns och återaktivering redovisas i
[C-0697](../citations/C-0697-hemsjo-HV-prastbetyg-olaus-fredberg.md).

