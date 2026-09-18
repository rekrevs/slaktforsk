# S-0707: Riksarkivets söktjänst Folkräkningar (Sveriges befolkning) 1930, personindex

- Leverantör: Riksarkivet, `https://sok.riksarkivet.se/folkrakningar/`
  (specialsök; indexet bygger på SCB:s församlingsbokutdrag 1930, jfr S-0700)
- Åtkomst: sökformuläret är captcha-skyddat (ALTCHA). Ägaren löste captchan
  själv 2026-09-05 och meddelade det i chatten; agenten använde därefter den
  öppna sessionen i Claude-in-Chrome. Ingen captcha löstes av agenten.
- Parametrar (GET): `Fornamn`, `Efternamn` (trunkering med `*`), `DatumFran`/
  `DatumTill` (födelseår), `Fodelseforsamling`, `Hemforsamling`, `Hemort`,
  `Lan`, `Folk1930=true` (övriga `FolkNNNN=false`), `AvanceradSok`.
  Träfflistan visar namn, födelseår, län, år; postvisningen nås via
  länken i namnet (`postid=Folk_NNNN`) och ger hemförsamling, hemort, sida
  i församlingsboken, civilstånd/vigselår, familjeställning, yrke,
  skolbildning, inkomst samt `Personer i hushållet`.
- Personer utan efternamn i utdraget indexeras utan efternamn (t.ex.
  `Anders Ivar`, 1903, Hudiksvall = P-0239), så efternamnssökning kan missa dem.
- Bevarat: sökningarnas parametrar och utfall i C-0898; inga bilder.
