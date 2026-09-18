# S-0462: Riksarkivet — födelseregistrets täckning för Olaus och Lundby 1852

## Källbeskrivning

- Tjänst: Riksarkivets öppna `birthrecords`-API
- Målperson: P-0336 Olaus Fredriksson Fredberg
- Mål: pröva den vuxennära uppgiften född 1852-05-24 i Lundby utan att
  ersätta originalkyrkböckerna
- Hämtad: 2026-08-29

## API-resultat

Sex första anrop utan vanlig webbläsar-`User-Agent` gav `403` och en
WAF-sida. Svarskropparna bevaras oförändrade trots filändelsen `.json`.
Exakt samma parameterkodade frågor med dokumenterad `User-Agent` gav `200`.

En rikstäckande namnfråga på `Olaus` och år 1852 gav sju poster: två i
Fjärestad och en vardera i Listerby, Raus, Hyby, Norra Åkarp och Falsterbo.
Ingen är född den 24 maj och ingen ligger i Lundby. De exakta frågorna
`Olaus` + Lundby respektive Stora Lundby gav noll.

Kontrollfrågorna visar emellertid att registret saknar den redan
originalbelagda Johan August, född 1849-07-05 i Stora Lundby, och dessutom
ger noll även för alla födslar i Stora Lundby 1849 och 1852 utan namnfilter.
Stora Lundby saknar alltså dokumenterad registertäckning för målåren.
Resultatet är täckningsnoll, inte ett nytt person- eller födelsenoll för
Olaus. De tidigare bildlästa resultaten i Stora Lundby, Lundby och Norra
Lundby påverkas inte.

## Bevarade API-original

WAF-svar utan `User-Agent`:

- `S-0462-riksarkivet-birthregister-olaus-lundby-1852.json`
- `S-0462-riksarkivet-birthregister-olaus-stora-lundby-1852.json`
- `S-0462-riksarkivet-birthregister-olaus-all-1852.json`
- `S-0462-riksarkivet-birthregister-johan-august-stora-lundby-1849-control.json`
- `S-0462-riksarkivet-birthregister-stora-lundby-1849-control.json`
- `S-0462-riksarkivet-birthregister-stora-lundby-1852-coverage.json`

Lyckade `200`-svar:

- `S-0462-riksarkivet-birthregister-olaus-lundby-1852-ua.json`
- `S-0462-riksarkivet-birthregister-olaus-stora-lundby-1852-ua.json`
- `S-0462-riksarkivet-birthregister-olaus-all-1852-ua.json`
- `S-0462-riksarkivet-birthregister-johan-august-stora-lundby-1849-control-ua.json`
- `S-0462-riksarkivet-birthregister-stora-lundby-1849-control-ua.json`
- `S-0462-riksarkivet-birthregister-stora-lundby-1852-coverage-ua.json`

Exakta byteantal och SHA-256 förs in i `genealogy/media-manifest.json`.

## Återaktivering

Kör inte om samma API-frågor utan ändrad dokumenterad registertäckning.
Återuppta Olaus genom Södra Lundby i Larv E/3, en egen föräldrapost, ett
gemensamt hushåll med Johan August eller en positiv militär-/flyttlänk.

