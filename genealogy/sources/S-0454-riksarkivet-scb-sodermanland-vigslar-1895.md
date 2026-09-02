# S-0454: Riksarkivet — SCB-utdrag, Södermanlands vigslar 1895

## Källbeskrivning

- Arkivbildare: Statistiska Centralbyrån (SCB), samlingspost
- Samling: Utdrag ur födelse-, vigsel- och dödböcker 1860–1949
- Referenskod/volym: `SE/RA/420401/01/H 1 AA/1123` (1895), Södermanlands län
- Riksarkivet-id: `rLSW3OgRrH6d0G02H087k3`
- IIIF-manifest: <https://lbiiif.riksarkivet.se/arkis!A0037332/manifest> och
  <https://lbiiif.riksarkivet.se/arkis!A0036622/manifest>
- Läst och hämtad: 2026-08-29

## API-först och routing

Sök-API:et identifierade årsvolymen och båda manifesten. Manifest
`A0037332` routade direkt till vigselavsnitten för fyra källburna
kandidatförsamlingar:

| Församling | Bild-id | Resultat |
|---|---|---|
| Helgesta | `A0037332_00619` | ingen Erik Karlsson–Matilda Charlotta Sjöberg |
| Forssa | `A0037332_00627` | ingen träff |
| Flen | `A0037332_00631` | positiv post 5, 1895-12-28 |
| Björkvik | `A0037332_00550` | ingen träff |

Alla fyra årssidor hämtades som fulloriginal via publik IIIF. Ingen Chrome
användes.

## Källkritik

SCB-utdraget är en samtida officiell avskrift från vigselboken. Det positiva
Flen-resultatet säkrar församling, datum, par, födelsedata, yrke och boställen,
men är inte den bundna kyrkoboken. De tre negativa sidorna används endast som
avgränsade församling/år-noll; de behövs inte längre för att lokalisera den
nu funna vigseln.

API-svar, manifest och de fyra originalsidorna är bevarade lokalt. Målbildens
SHA-256 binds i C-0577 och nollresultaten i C-0578.
