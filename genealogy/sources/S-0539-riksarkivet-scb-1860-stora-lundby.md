# S-0539: Riksarkivet — SCB:s församlingsutdrag för Stora Lundby 1860

## Källbeskrivning

- Arkivbildare: Statistiska centralbyrån (SCB)
- Arkiv: `SE/RA/420401/03`, *1860 års folkräkning*
- Serie: `H 1 A`, *Primärmaterial, utdrag ur husförhörslängderna*
- Volym: `SE/RA/420401/03/H 1 A/69`, 1860, med anmärkningen
  `Älvsborgs län: 25-61 Nödinge-Hällestad.`
- Permanent Riksarkivet-id: `ktSW3OgRrH6d0G02H087k3`
- Reproduktion: `A0056074`
- [Katalogpost](https://sok.riksarkivet.se/arkiv/ktSW3OgRrH6d0G02H087k3)
- [IIIF-manifest](https://lbiiif.riksarkivet.se/arkis!A0056074/manifest)
- Lästa och hämtade: 2026-08-31

## Registertäckning och vald källväg

Riksarkivets egen sida om registreringsläget säger att 1860 års
personregister bara omfattar Jämtlands län. En personfråga med Stora Lundby
kan därför inte bära vare sig träff eller noll för Johan August 1849. Den
äldre ALTCHA-incidenten i S-0415 bevaras som en faktisk åtkomsthändelse men
är inte längre en meningsfull återstartsväg.

Riksarkivets separata tjänst *Församlingsutdrag 1860–1940* anger däremot att
det skannade materialet består av underlagen till samtliga folkräkningar
1860–1940. Records-API:t återgav den exakta volymposten som första träff och
länkade till dess publika IIIF-manifest. OAI-EAD verifierade fond, serie och
volym; JSON-LD verifierade den digitala instansieringen.

## Exakt Stora Lundby-intervall

IIIF-manifestets range `Stora Lundby 1860` börjar på canvas
`A0056074_00027`. Nästa församlingsrange, `Skallsjö 1860`, börjar på
`A0056074_00045`. Det kompletta Stora Lundby-intervallet är därmed bilderna
`_00027`–`_00044`, 18 bilder.

Samtliga 18 bilder lästes visuellt rad för rad. Blanketten skriver bara
förnamnsinitialer, så kontrollen gjordes på efternamn, hushållsgruppering och
födelseår. Ingen hushållskombination motsvarar Fredric Jacobson/Jacobsson
född 1824, Anna Britta Olsdotter/Olofsdotter född 1824, Johan August född
1849 och Olaus född 1852. Resultatet är ett komplett utdrags- och
kombinationsnoll för Stora Lundby 1860, inte ett personnoll i annan
församling. A I/10:s tidigare `afl.53` gör dessutom frånvaron förenlig med
att Fredric–Anna-gruppen hade lämnat församlingen 1853; utdraget anger inte
vart.

## Digital åtkomst

Records-API, OAI-EAD, JSON-LD och IIIF användes direkt. Data-API:t och
IIIF-bilderna svarade när vanliga webbläsarhuvuden och Riksarkivets egen
bildvisarsida användes som `Referer`; ingen sessionskaka behövdes. Chrome
användes inte och ingen CAPTCHA eller ALTCHA interagerades med.

## Lokalt bevarad metadata

| Fil | SHA-256 |
|---|---|
| [Registreringsläget för folkräkningar](../media/S-0539-riksarkivet-folkrakningar-registrering.html) | `d046f656936281a324c0248f009af6ff560a4d27c058f0f41dd04a2ace68ebbb` |
| [Församlingsutdrag 1860–1940](../media/S-0539-riksarkivet-forsamlingsutdrag.html) | `b74c72746c1a60fc95218fb265edf342ae2ec4c119a6c609d7d7351ebdc164c9` |
| [Records-API-svar](../media/S-0539-riksarkivet-scb-1860-H1A69-records-api.json) | `e1465d2d4d8ec8acf9d4fea9c3502f3bff16d603c4c2154486e9c6ec81306638` |
| [Fondens OAI-EAD](../media/S-0539-riksarkivet-scb-1860-fonds-oai-ead.xml) | `dd1c2182659b516222815fd788f71477d4df0e54b01ad883e1c4f3ede1fc0943` |
| [Volymens OAI-EAD](../media/S-0539-riksarkivet-scb-1860-H1A69-oai-ead.xml) | `7047c09163882ee2e91e2684ca81ebd4cc110e381eb93bcfb4e518e23514d579` |
| [Volymens JSON-LD](../media/S-0539-riksarkivet-scb-1860-H1A69-jsonld.json) | `9b76d2601b5b9738062cd7b4c160cc74b3c18d8634ad28360c1358a10f4ccf4b` |
| [IIIF-manifest](../media/S-0539-riksarkivet-scb-1860-A0056074-IIIF-manifest.json) | `4250075b09c687602d9f89435bd9fc0b3f1b480e10171d027a958e8c96b4102c` |

De 18 fullupplösta originalbilderna och deras individuella checksummor
redovisas i C-0703.
