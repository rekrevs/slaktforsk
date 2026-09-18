# S-0531: Riksarkivet — Villåttinge bouppteckningsregister och bouppteckningar 1935

## Källbeskrivning

Detta källpaket består uteslutande av Riksarkivets records-API, JSON-LD och
OAI-EAD för Villåttinge häradsrätt:

- arkivfond `SE/ULA/11693`, Riksarkivet-id `Py4ZIcmaweZJTe018W43t3`;
- serie `C II b Kortregister över bouppteckningar`;
- registervolym `SE/ULA/11693/C II b/5`, 1933–1938, Riksarkivet-id
  `1ne7pFLAjaAWr0Z0SLNN70`;
- serie `F II Bouppteckningar`;
- bouppteckningsvolym `SE/ULA/11693/F II/59`, 1935–1936, Riksarkivet-id
  `K6LKgLnlhaQoLa0flJzzL5`.

Kontrollerat och bevarat 2026-08-30.

## Behörig häradsrätt

Fondens OAI-EAD säger uttryckligen att Villåttinge härad omfattade Dunker,
Lilla Malma, Hyltinge, **Helgesta**, Årdala, Forssa, Flen och Mellösa samt
Malmköpings köping. Erik Karlsson var kyrkobokförd i Helgesta och dog
1935-03-20. Villåttinge häradsrätt är därför den källstyrda domstolsvägen
för en möjlig bouppteckning efter honom.

En inledande records-API-fråga på `Helgesta bouppteckningar` återförde
Villåttinges F II-serie bland träffarna. Arkivfondens OAI-EAD verifierar
jurisdiktionen direkt och används därför som det starkare routingbelägget.

## Exakt läsordning

OAI-förteckningen har ett särskilt `C II b Kortregister över
bouppteckningar`. Volym 5 omfattar 1933–1938 och täcker därmed målåret 1935.
Samma förteckning placerar bouppteckningarna i F II och anger volym 59 för
1935–1936. Den säkra arbetsordningen är därför:

1. sök Erik Karlsson i `C II b/5` och notera akt-/nummerhänvisningen;
2. använd hänvisningen i `F II/59`;
3. skapa först efter läsning av akten påståenden om arvingar, släktskap,
   egendom eller skulder.

Records-API:t ger permanenta id:n och fullsignum för båda volymerna.
JSON-LD-posterna innehåller endast fysisk instansiering med
representationstypen `Analog`. Ingen `_links.image`, digital instansiering
eller IIIF-länk finns. Registerkortet och bouppteckningen är därför exakta
beställningsvägar hos Riksarkivet i Uppsala, inte distanslästa personkällor.

## Slutsatsgräns

Ingen registerpost eller bouppteckningsakt för Erik har lästs. Metadata visar
att materialet och rätt tidsintervall finns samt i vilken ordning det bör
beställas. Den visar inte att en akt upprättades, att Erik finns i registret
eller vilka arvingar han i så fall hade. Resultatet är varken personträff
eller personnoll.

En separat exakt HTTP-fråga i Riksarkivets folkräkning 1870 omdirigerades
till ALTCHA innan något resultat kunde läsas. Ingen CAPTCHA interagerades
med och inget nollresultat registreras. Bouppteckningsroutingen ovan är
hämtad genom de öppna maskinläsbara gränssnitten och beror inte på den
åtkomstincidenten.

## Lokalt bevarat metadataunderlag

| Fil | SHA-256 |
|---|---|
| [API-fråga Helgesta/bouppteckningar](../media/S-0531-riksarkivet-helgesta-bouppteckningar-api.json) | `234d15702bf559106f7676274572a2c813fee6b44f490e5647160f0237c118dd` |
| [Arkivfondens JSON-LD](../media/S-0531-riksarkivet-villattinge-arkiv-jsonld.json) | `2987dc2608cf7cd1a8a69d9fbf8677d597adf4af2f9015799b28fe900e66433c` |
| [Arkivfondens OAI-EAD](../media/S-0531-riksarkivet-villattinge-arkiv-oai.xml) | `886de616c1529a7cb2510cb0d1c97d0bec00dfb7a571fbf15e027d291296c652` |
| [F II-seriens JSON-LD](../media/S-0531-riksarkivet-villattinge-FII-serie-jsonld.json) | `343e151266afe9c28d702b0a0dd3f0e367710e9e824fb082262941c09f9cb7dd` |
| [F II/59 records-API](../media/S-0531-riksarkivet-villattinge-FII59-api.json) | `b532ca7cedaba8109d6e9f4c71d92805c74be1732116121b4673e740acc8f268` |
| [F II/59 JSON-LD](../media/S-0531-riksarkivet-villattinge-FII59-jsonld.json) | `a09badb8aa9470be8a7066b203fd60693cbb45dfe5ce2054d00f494e83bead88` |
| [F II/59 OAI-EAD](../media/S-0531-riksarkivet-villattinge-FII59-oai.xml) | `3a759a869c9bd6dbdc5ccdd1d8dd5de40efe0fcd083cd960c0a00420999a043d` |
| [C II b/5 records-API](../media/S-0531-riksarkivet-villattinge-CIIb5-api.json) | `dafd2621b7ecde874a9536fba150bd44a9f4ccb00393b22edf3625ad1c014f8b` |
| [C II b/5 JSON-LD](../media/S-0531-riksarkivet-villattinge-CIIb5-jsonld.json) | `f3d92807cc2dacfc4c7440cb9d45419e1aaf00670a5bfe2c3c4b361b0b0dbcbb` |
| [C II b/5 OAI-EAD](../media/S-0531-riksarkivet-villattinge-CIIb5-oai.xml) | `346042fc4816720bd6f51b2738d2f3ed4545ec4955f9e2e11e3086050c6130fe` |

Tolkningen och återaktiveringsordningen redovisas i
[C-0694](../citations/C-0694-erik-karlsson-villattinge-bouppteckning-1935.md).
