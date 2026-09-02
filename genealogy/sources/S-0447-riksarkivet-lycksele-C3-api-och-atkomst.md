# S-0447: Riksarkivet — Lycksele C/3, API-metadata och bildåtkomst 2026-08-29

> Historisk åtkomstpost. Hindret supersederades 2026-08-30 av
> [S-0521](S-0521-riksarkivet-lycksele-C3-1829.md), där reproduktionen och
> den exakta målbilden är lösta och lästa.

## Källbeskrivning

- Arkiv: Lycksele kyrkoarkiv, `SE/HLA/1010118`
- Serie: Födelse- och dopböcker
- Volym: C/3, 1813–1831; börjar oktober 1813
- Referenskod: `SE/HLA/1010118/C/3`
- Riksarkivet-id: `Fc6S2139wKE35deSh844x0`
- Sök-API:
  <https://data.riksarkivet.se/api/records?text=SE%2FHLA%2F1010118%2FC%2F3&limit=20>
- JSON-LD:
  <https://data.riksarkivet.se/archive/Fc6S2139wKE35deSh844x0.jsonld>
- OAI-PMH/EAD:
  <https://oai-pmh.riksarkivet.se/OAI/?verb=GetRecord&identifier=SE%2FHLA%2F1010118%2FC%2F3&metadataPrefix=oai_ra_ead>
- Katalog: <https://sok.riksarkivet.se/arkiv/Fc6S2139wKE35deSh844x0>
- Kontrollerad: 2026-08-29

## API-först-resultat

Sök-API, JSON-LD och OAI-PMH/EAD svarade `200`. Den exakta API-posten anger
referenskoden, Lycksele kyrkoarkiv, serien Födelse- och dopböcker och tiden
1813–1831. JSON-LD innehåller en `rico:Instantiation` som digital
representation men ingen användbar `schema:image` eller annan bild-URL.
OAI-posten är beskrivande metadata och ger inte heller en reproduktionskod.

Den autentiserade katalogen prövades först därefter och visade ALTCHA.
Kontrollen lämnades orörd enligt ägarregeln. Ingen kyrkoboksbild eller
födelsenotis lästes. Detta är ett åtkomsthinder, inte ett negativt
födelsefynd.

## Lokalt originalmaterial

- [`Sök-API-svar`](../media/S-0447-riksarkivet-lycksele-C3-api-records.json),
  SHA-256
  `4c86e6e9f8b82219b0261044959cb4f74617ffc3003d5dc12ef2f1c3422bc52f`.
- [`JSON-LD`](../media/S-0447-riksarkivet-lycksele-C3-archive.jsonld),
  SHA-256
  `dba9f96a8cdde6b87869231c2cdda826456fae17e6624bb541be5bb72b854749`.
- [`OAI-PMH/EAD`](../media/S-0447-riksarkivet-lycksele-C3-oai-ead.xml),
  SHA-256
  `507ea7cc62862da9d37bca85eb11b78a641b9fccda3db5e97a30ae49dbb62fa9`.

## Historisk routingsledtråd, nu supersederad

Två externa sekundärindex gav i den historiska körningen Ånäset/Vindeln som
routingsledtråd men saknade exponerad källbild och användes aldrig som
genealogiskt belägg. Den ledtråden är nu helt supersederad av Riksarkivets
egna original: Degerfors A I/5a s. 335 och A I/6b s. 399 i
[C-0727](../citations/C-0727-degerfors-anaset-sara-sophia-foraldrahem.md).
Föräldrarna och orten förs enbart från dessa Riksarkivet-original, inte från
sekundärindexen. Lycksele C/3:s lästa nollresultat i C-0682 står kvar som
kontroll av den senare motstridiga ortuppgiften.
