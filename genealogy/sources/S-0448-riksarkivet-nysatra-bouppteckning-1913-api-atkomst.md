# S-0448: Riksarkivet — Nysätra tingslags bouppteckningar 1913, API och analog åtkomst

## Källbeskrivning

- Arkivfond: Nysätra tingslags häradsrätts arkiv, `SE/HLA/1040118`
- Arkivinstitution: Riksarkivet i Härnösand
- Fond-id: `3yCM633czrFaYNNCIgPkl3`
- Serie: F II, Bouppteckningar och arvskiften
- Målvolym: F II/23, 1913
- Referenskod: `SE/HLA/1040118/F/F II/23`
- Riksarkivet-id: `k6CqF3Xtrn61t03Gjpu0Y3`
- JSON-LD:
  <https://data.riksarkivet.se/archive/k6CqF3Xtrn61t03Gjpu0Y3.jsonld>
- OAI-PMH/EAD:
  <https://oai-pmh.riksarkivet.se/OAI/?verb=GetRecord&identifier=SE%2FHLA%2F1040118%2FF%2FF%20II%2F23&metadataPrefix=oai_ra_ead>
- Katalogpost:
  <https://sok.riksarkivet.se/arkiv/k6CqF3Xtrn61t03Gjpu0Y3>
- Kontrollerad: 2026-08-29

## Behörig arkivbildare

Fondens OAI-EAD beskriver den organisatoriska förändringen uttryckligen:
Bygdeå och Lövångers tingslag slogs 1902 samman med Nysätra tingslag utan
avbrott i arkivbildningen. Därefter ingick socknarna Bygdeå, Nysätra och
Lövånger i Nysätra tingslag. Barbro Kristina Olofsdotters död i Jomark,
Bygdeå, 1913 ska därför sökas i denna fond.

## API-först-resultat

Riksarkivets sök-API genomsöktes med en exakt `PartOfArchive`-fasett för
Nysätra tingslags häradsrätts arkiv. Fasetten gav 408 volymposter. Den
exakta 1913-posten är F II/23 och ligger i hierarkin
`Nysätra tingslags häradsrätts arkiv` → `HANDLINGAR TILL DOMBÖCKER OCH
PROTOKOLL M M` → `Bouppteckningar och arvskiften`.

API-posten saknar `_links.image` och anger `onlyDigitisedMaterials: false`.
JSON-LD innehåller endast en fysisk instans med representationstyp `Analog`;
OAI-EAD bekräftar volymnummer 23 och år 1913. Det finns alltså ingen
API-exponerad IIIF-länk att pröva och ingen grund för Chrome. Ingen akttext
eller personpost har lästs.

Ett första långt, färdigkodat API-anrop gav tillfälligt `403`. Samma data
kunde därefter hämtas med `curl --get --data-urlencode`, och ett senare
kontrollanrop på den långa URL:en svarade `200`. Händelsen klassas därför
som ett löst parameter-/WAF-hinder, inte som spärr för målvolymen.

## Registerväg

Riksarkivets API identifierar dessutom det analoga bouppteckningsregistret
`SE/HLA/1040129/C/C II/C II b/13`, id
`uamwPFisWKkWqpnjo8xka2`, i Västerbottens mellersta domsagas
häradsrätts arkiv. Volymens not lyder:

> Nysätra tingslag: M - Ö  
> Registerkort utan adresser: A - Ö (1903-1932)

Barbros efternamn Olofsdotter ligger i intervallet M–Ö. Även denna post
saknar `_links.image`; dess JSON-LD visar endast analog representation.
Registerkortet är därför den första fysiska läsordningen för att få
akt-/protokollhänvisning, följt av F II/23.

Riksarkivets publika specialsökningsregister är inte en ersättning. Dess
officiella täckningssida anger Bygdeå tingslags häradsrätt 1737–1901 och
Nysätra tingslags häradsrätt 1834–1910. Barbros 1913-akt ligger utanför den
publicerade registertäckningen.

## Återaktivering

1. Pröva sök-API → JSON-LD → eventuell IIIF på båda id:na igen för att fånga
   framtida digitalisering.
2. Om bildlänk fortfarande saknas: beställ eller läs hos Riksarkivet i
   Härnösand först `SE/HLA/1040129/C/C II/C II b/13`, namnintervallet
   Olofsdotter, år 1913.
3. Använd registerkortets akt-/protokollnummer för att beställa eller läsa
   `SE/HLA/1040118/F/F II/23`.
4. Skapa först därefter personpåståenden om arvingar, egendom, skulder eller
   familjerelationer. Nuvarande metadata belägger bara källvägen och
   åtkomstläget.

## Lokalt originalmaterial

- [`API-svar med F II/23`](../media/S-0448-riksarkivet-nysatra-FII23-api-records.json),
  SHA-256
  `224829231c1555b0dfff17732f0b234d5b417da0d4437008533c8390322fcecb`;
- [`F II/23 JSON-LD`](../media/S-0448-riksarkivet-nysatra-FII23-archive.jsonld),
  SHA-256
  `8ed1ba5c76f212ae82a023fd93b5d356694d32d2348ecf7217865d1519a9f8b6`;
- [`F II/23 OAI-PMH/EAD`](../media/S-0448-riksarkivet-nysatra-FII23-oai-ead.xml),
  SHA-256
  `a18ab4146a3cdad2deacbb071720a3ec3fe428082710e7ab985153c8308ad3b1`;
- [`fondens JSON-LD`](../media/S-0448-riksarkivet-nysatra-fonds-archive.jsonld),
  SHA-256
  `741e3e8cba9c7ec56b8c362a4f9639d54c6e2bab24aeaa7185fc8f7b3c3bb79c`;
- [`fondens OAI-PMH/EAD`](../media/S-0448-riksarkivet-nysatra-fonds-oai-ead.xml),
  SHA-256
  `5ef86e87a12b5acd999086e03f9240d13733cd91eb8bd631c2c94f62bc36c3b9`;
- [`API-svar med C II b/13`](../media/S-0448-riksarkivet-vasterbotten-CIIb13-api-records.json),
  SHA-256
  `efa82457620c6bfc091929228c360e60c4cddb94cdba62d58731b56833ea8170`;
- [`C II b/13 JSON-LD`](../media/S-0448-riksarkivet-vasterbotten-CIIb13-archive.jsonld),
  SHA-256
  `505f0dac9293f8f95f1ea6838cc812b61a51b8a91d66554ecd3a87b13b2b27a3`;
- [`C II b/13 OAI-PMH/EAD`](../media/S-0448-riksarkivet-vasterbotten-CIIb13-oai-ead.xml),
  SHA-256
  `33a31f567f52fd738708f3fbb440e5d29894b87e5fd3c62b48f7fa020ad40f4a`;
- [`Västerbottens län — registertäckning`](../media/S-0448-riksarkivet-bouppteckningsregister-vasterbotten.html),
  SHA-256
  `161a55c9db9645fa1812a78d20f5d38f4823f24805b2252da5c6855f7569b0d3`.
