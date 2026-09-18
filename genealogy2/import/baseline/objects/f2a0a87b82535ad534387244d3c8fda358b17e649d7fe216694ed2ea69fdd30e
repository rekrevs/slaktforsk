# S-0777: Varola kyrkoarkiv C/4, födelse- och dopbok 1781–1823

## Källbeskrivning

- Institution: Riksarkivet i Göteborg
- Arkivbildare: **Varola kyrkoarkiv**, `SE/GLA/13615` (1527–2001)
- Referenskod: `SE/GLA/13615/C/4`
- Serie/volym: Födelse- och dopböcker `C/4`
- Tidsomfång: 1781–1823
- Reproduktion: **`C0053282`**, 163 bilder, **skannad från mikrofilm**
- Bildvisare: <https://sok.riksarkivet.se/bildvisning/C0053282_00001>
- Arkis-UUID för volymen: `14e483cb-77a1-11d5-a6f2-0002440207bb`
- Läst: 2026-09-07 (T-0097)

## Hur arkivet lokaliserades

Varolas kyrkoarkiv var **inte lokaliserat i projektet** före 2026-09-07.
Riksarkivets MCP `search_metadata` gav arkivbildaren direkt —
`SE/GLA/13615`, Riksarkivet i Göteborg — och serien `C` med volymerna
`C/1`–`C/9`.

**MCP:t exponerade dock ingen bildlänk för `C/4`**, till skillnad från
`C/6`, `C/7` och `C/8`. Ett rimligt men felaktigt intryck vore att volymen
saknar digital reproduktion.

Vägen som gav svaret är den som står i
[method-riksarkivet.md](../method-riksarkivet.md): katalogpostens
omdirigering exponerar volymens **Arkis-UUID**, och den publika, läsande
batchsidan

```
https://sok.riksarkivet.se/bildvisning/batchar/<uuid>
```

svarar med reproduktionslistan. För `C/4` gav den `C0053282`, 163 bilder,
mikrofilm. **ALTCHA aktiverades inte.**

## Källkritik: detta är en pastoratsbok

Volymen är **inte** en bok för Varola socken ensam. Varje år förs som fyra
skilda avsnitt med egna rubriker:

> `Födde och Döpte 1799 uti Walora Församling och Sochen`
> `Födde och Döpte 1799 uti Wärsås Sochen`
> `Födde och Döpte 1799 uti Ljunghems Sochen`
> `Födde och Döpte 1799 uti Edåsa Sochen`

Ordningen är genomgående Varola → Värsås → Ljunghem → Edåsa, och avsnitten
löper över uppslagsgränserna.

**Två konsekvenser för läsning:**

1. **IIIF-manifestets `structures` duger inte ensamt.** Indexet ger en enda
   startbild per år — för 1799 bild 56 — men det är Ljunghems avsnitt.
   Varolas 1799 börjar på **bild 54**. Årsindexet måste alltid kontrolleras
   mot rubriken innan ett avsnitt läses.
2. **Ett negativt resultat i Varola är inte ett negativt resultat i
   pastoratet.** De tre grannsocknarnas avsnitt ligger på samma uppslag och
   kostar nästan ingenting att läsa i samma svep.

## Årsindex ur manifestet, med rubrikkontroll

| Årgång | Manifestets startbild | Varolaavsnittets faktiska start |
|---|---|---|
| 1798 | 53 | tidigare än 53 (avsnittet löper in på 53) |
| **1799** | 56 | **54** (rubriken `1799 uti Walora Församling och Sochen`) |
| 1800 | 58 | **56**, högersidan |

## Läsmetod

IIIF `full/4000,`-hämtning i den anslutna Chrome-fliken, ritad på en duk och
läst kolumn för kolumn med datum- och namnkolumnerna förstorade till bildens
egen upplösning. Uppslagen mäter omkring 7 150 × 6 300 px.
