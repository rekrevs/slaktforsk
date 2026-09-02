# S-0521: Riksarkivet — Lycksele C/3, födda 1829

## Källbeskrivning

- Arkiv: Lycksele kyrkoarkiv, `SE/HLA/1010118`
- Volym: C/3, födelse- och dopbok 1813–1831
- Referenskod: `SE/HLA/1010118/C/3`
- Riksarkivet-id: `Fc6S2139wKE35deSh844x0`
- Arkis-UUID: `089c613e-c910-43e9-8316-7a1cac8104ec`
- Reproduktion: `C0034151`
- Kontrollerad och bevarad: 2026-08-30
- [JSON-LD](https://data.riksarkivet.se/archive/Fc6S2139wKE35deSh844x0.jsonld)

## API-först och reproduktionskoppling

Den exakta JSON-LD-posten svarade `200` och visade en bildrepresentation
utan bild-URI. Den inloggade Riksarkivet-katalogens omdirigeringsadress
exponerade den äldre Arkis-UUID:n ovan utan att ALTCHA aktiverades. UUID:n
gav i Riksarkivets publika `Tree/SubTree`-slutpunkt en bildfilsnod med
reproduktion `C0034151`.

Nakna manifest- och Image API-anrop gav `403`. Efter dessa API-försök
användes därför Riksarkivets egen bildvisare i en ny styrd flik i
användarens redan inloggade session. Inga sessionsdata lästes eller
bevarades och ingen CAPTCHA aktiverades.

## Exakt negativ födelsekontroll

Lycksele C/3, sidan 126, bild `C0034151_00136`, innehåller den fortlöpande
födelse- och dopföljden för april–juni 1829. Följden omfattar målområdet
kring 1829-05-21, med bland annat poster daterade 9, 16 och 22 maj. Ingen
rad gäller Sara Sophia Pehrsdotter eller en säker motsvarande namnform.

Resultatet motsäger den senare Sävar A I/6b-uppgiften att Sara Sophia
föddes 1829-05-21 i Lycksele. Det är ett exakt datum- och bildfönsternoll,
inte ett bevis för att hon aldrig föddes i Lycksele eller att hennes
föräldrar kan uteslutas ur andra delar av volymen.

## Födelseregistrets täckning

Riksarkivets födelseregister-API gav:

- `place=Sävar`, år 1825: 0 poster;
- `place=Lycksele`, år 1829: 0 poster;
- `first_name=Johan Peter`, hela landet, år 1825: tre poster, samtliga i
  andra församlingar;
- `first_name=Sara Sophia`, hela landet, år 1829: 0 poster.

Att även den nu positivt lästa Sävar-posten saknas visar direkt att
registret inte täcker dessa mål på ett sätt som tillåter personnoll. Svaren
bevaras därför som täckningskontroll och får inte ersätta kyrkoboksbilden.

## Lokalt bevarat material

| Fil | SHA-256 |
|---|---|
| [JSON-LD](../media/S-0521-riksarkivet-lycksele-C3-jsonld.json) | `dba9f96a8cdde6b87869231c2cdda826456fae17e6624bb541be5bb72b854749` |
| [trädsvar](../media/S-0521-riksarkivet-lycksele-C3-tree.html) | `60da68b336884b1c9393e99a6cc6f3a67ff144a2b1f900db8242695d59df9ed2` |
| [Sävar 1825, täckning](../media/S-0521-riksarkivet-birthregister-savar-1825-coverage.json) | `30dd7bb280db045b590a0138cbbb20db8c74fd699a5338578da118318993a773` |
| [Lycksele 1829, täckning](../media/S-0521-riksarkivet-birthregister-lycksele-1829-coverage.json) | `1c114e5b353f6e4d344b0dc523461b9f700417754b6bd28811d9e68b34c81dc0` |
| [Johan Peter 1825, hela landet](../media/S-0521-riksarkivet-birthregister-johan-peter-all-1825.json) | `0e7c7718bc111d563ff490b186b6e4717e972bcdcd6879bf5328a6fee34c08e7` |
| [Sara Sophia 1829, hela landet](../media/S-0521-riksarkivet-birthregister-sara-sophia-all-1829.json) | `281747f97186de6e17bf5c86969d7632458f0f7966fa5a19251b9d1e6d87f5a1` |

Fulloriginalet och den strikta negativa slutsatsen redovisas i
[C-0682](../citations/C-0682-lycksele-C3-sara-sophia-1829-negativ.md).

En senare samma-dagskontroll fick det publika IIIF-manifestet och hela
födelseåret 1829 direkt från Riksarkivet utan Chrome. S-0532/C-0695
supersederar därför den snäva bildåtkomsten men inte C-0682:s korrekta noll
kring 1829-05-21.
