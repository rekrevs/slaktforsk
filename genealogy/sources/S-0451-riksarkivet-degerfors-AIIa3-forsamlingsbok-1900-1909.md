# S-0451: Riksarkivet — Degerfors A II a/3, församlingsbok 1900–1909

## Källbeskrivning

- Arkiv: Vindelns kyrkoarkiv (Degerfors kyrkoarkiv), `SE/HLA/1010028`
- Serie och volym: A II a/3, församlingsbok 1900–1909
- Omfång: folio 786–1165
- Referenskod: `SE/HLA/1010028/A II a/3`
- Riksarkivet-id: `t1PSkddOX4IDrn1D8bGdV3`
- Sök-API:
  <https://data.riksarkivet.se/api/records?text=SE%2FHLA%2F1010028%2FA%20II%20a&limit=100>
- JSON-LD:
  <https://data.riksarkivet.se/archive/t1PSkddOX4IDrn1D8bGdV3.jsonld>
- IIIF-manifest:
  <https://lbiiif.riksarkivet.se/arkis!F0013102/manifest> och
  <https://lbiiif.riksarkivet.se/arkis!00206816/manifest>
- Katalogpost:
  <https://sok.riksarkivet.se/arkiv/t1PSkddOX4IDrn1D8bGdV3>
- Läst och hämtad: 2026-08-29

## API-först och routing

Ett första sök-API- och OAI-försök stoppades av Riksarkivets WAF. Samma
anrop med URL-kodade parametrar, uttrycklig `Accept` och vanlig
`User-Agent` svarade därefter `200`; hindret är löst och dess original
bevaras separat i S-0452. Sök-API:et listade hela A II a-serien och visade
att folio 963 ligger i A II a/3. JSON-LD och båda manifesten svarade `200`,
och fulloriginalen hämtades via publik IIIF utan Chrome.

Manifestet binder folio 963 till `F0013102_00192`. B/3:s svårlästa hänvisning
för Nikanor prövades först som folio 1043 (`F0013102_00274`), men sidan är
Lavlund och saknar Zingmark. Detta bevaras som korrigerad routing, inte som
ett person- eller ortsnoll. Den positiva sidan 963 är rubricerad Rosinedahl
och innehåller Johan Oskar, Nikanor och Konrad Zingmark.

## Källkritik

Församlingsboken sammanför hushåll, födelsedata, civilstånd och
flytthänvisningar över flera år. Exakta födelser och vigsel bör fortfarande
kontrolleras i ministerialböcker när en sådan kontroll är avgörande. Överförda
och överstrukna rader har lästs försiktigt; svårlästa flytt- och
värnpliktsanteckningar normaliseras inte.

Originalfiler och SHA-256 är bundna i C-0574 och mediamanifestet.
