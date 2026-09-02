# C-0582: Batch 92 — API-, IIIF- och åtkomstprovenans

## Källor

- [S-0079](../sources/S-0079-flen-AIIa1-forsamlingsbok-1900-1905.md)
- [S-0453](../sources/S-0453-riksarkivet-scb-bjorkvik-fodda-1860.md)
- [S-0454](../sources/S-0454-riksarkivet-scb-sodermanland-vigslar-1895.md)
- [S-0455](../sources/S-0455-riksarkivet-flen-AI26-husforhorslangd-1896-1900.md)
- [S-0456](../sources/S-0456-riksarkivet-bjorkvik-C9-fodelsebok-1872-1881.md)
- [S-0457](../sources/S-0457-riksarkivet-register-api-och-atkomst-flen-bjorkvik.md)

## Provenans och avgränsning

Riksarkivets API användes före alla andra Riksarkivet-vägar. Sök-API och
publik IIIF räckte för SCB-volymerna, Flen A I/26, Flen A II a/1 och
Björkvik C/9. Inget Chrome-anrop gjordes i batchen.

Födelse- och vigselregistrens noll är täckningsnoll eftersom registren inte
täcker de aktuella Södermanlandsposterna. De är inte personnoll. För Björkvik
C/7 och A I/17 a–b saknades bildlänkar i sök-API:et; exakta JSON-LD-omprov
gav `403`, liksom två endast sekvensmässigt härledda A I/17-manifest. Dessa
manifest-id:n accepteras därför inte som säkra. Flen A I/25 gav
API/JSON-LD/OAI-metadata men ingen bild-URI; katalogen stannade på orörd
CAPTCHA. Alla hinder är återaktiverbara enligt S-0457.

## Bevarade metadata-, routing- och hinderoriginal

- `S-0079-riksarkivet-flen-AIIa1-IIIF-manifest.json`
- `S-0453-riksarkivet-scb-sodermanland-1860-api-records.json`
- `S-0453-riksarkivet-scb-sodermanland-1860-IIIF-manifest-A0037175.json`
- `S-0453-riksarkivet-scb-sodermanland-1860-IIIF-manifest-A0035503.json`
- `S-0453-riksarkivet-scb-bjorkvik-fodda-1860-start-A0037175_00031.jpg`
- `S-0454-riksarkivet-scb-sodermanland-1895-api-records.json`
- `S-0454-riksarkivet-scb-sodermanland-1895-IIIF-manifest-A0037332.json`
- `S-0454-riksarkivet-scb-sodermanland-1895-IIIF-manifest-A0036622.json`
- `S-0455-riksarkivet-flen-AI-api-records.json`
- `S-0455-riksarkivet-flen-AI26-IIIF-manifest.json`
- `S-0456-riksarkivet-bjorkvik-C-api-records.json`
- `S-0456-riksarkivet-bjorkvik-C9-IIIF-manifest.json`
- `S-0457-riksarkivet-search-API-openapi.json`
- `S-0457-riksarkivet-fodelseregister-matilda-exakt-null.json`
- `S-0457-riksarkivet-fodelseregister-matilda-brett-null.json`
- `S-0457-riksarkivet-vigselregister-erik-matilda-null.json`
- `S-0457-riksarkivet-bjorkvik-AI-api-records.json`
- `S-0457-riksarkivet-bjorkvik-AI17a-jsonld-403.html`
- `S-0457-riksarkivet-bjorkvik-AI17b-jsonld-403.html`
- `S-0457-riksarkivet-bjorkvik-C7-jsonld-403.html`
- `S-0457-riksarkivet-bjorkvik-AI17a-IIIF-403.html`
- `S-0457-riksarkivet-bjorkvik-AI17b-IIIF-403.html`
- `S-0457-riksarkivet-flen-AI25-archive.jsonld`
- `S-0457-riksarkivet-flen-AI25-oai-ead.xml`
- `S-0457-riksarkivet-flen-AI25-katalog-captcha.html`

Exakta SHA-256 och byteantal finns i `genealogy/media-manifest.json`.

## Stött påstående

A-2517.
