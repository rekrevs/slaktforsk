# C-0570: Barbros bouppteckningsväg 1913 identifierad via API men endast analog

## Källa

[S-0448](../sources/S-0448-riksarkivet-nysatra-bouppteckning-1913-api-atkomst.md)

## Kontrollerat omfång

Fondens OAI-EAD anger att Bygdeå och Lövångers tingslag 1902 slogs samman
med Nysätra tingslag och att Bygdeå socken därefter ingick där. Riksarkivets
sök-API identifierar den exakta bouppteckningsvolymen för Barbros dödsår:

- Nysätra tingslags häradsrätts arkiv;
- `SE/HLA/1040118/F/F II/23`;
- Bouppteckningar och arvskiften;
- år 1913;
- Riksarkivet-id `k6CqF3Xtrn61t03Gjpu0Y3`.

API-posten har ingen `_links.image`. JSON-LD beskriver endast en analog
instans, och OAI-EAD bekräftar volym 23/1913 utan reproduktionskod. Ingen
bouppteckningstext har därför lästs.

## Register och rättat nollresultat

API-posten `uamwPFisWKkWqpnjo8xka2` identifierar den analoga
registervolymen `SE/HLA/1040129/C/C II/C II b/13`. Den omfattar enligt
källnoten `Nysätra tingslag: M - Ö` och registerkort utan adresser A–Ö
1903–1932. Olofsdotter hör till M–Ö, men ingen registerbild är exponerad.

Riksarkivets publika bouppteckningsregister anger samtidigt Nysätra
tingslags häradsrätt 1834–1910. Det tidigare sökfrågenollet för Barbro
1910–1937 kan alltså inte pröva en bouppteckning från 1913 och får inte
tolkas som frånvaro av akt.

## Klassificering och återaktivering

Detta är ett exakt käll- och åtkomstfynd, inte en personträff och inte ett
bouppteckningsnoll. Återaktivera API → JSON-LD → eventuell IIIF. Om
materialet fortfarande bara är analogt: beställ först C II b/13 hos
Riksarkivet i Härnösand och använd registerkortet för att läsa F II/23.

## Lokalt originalmaterial

De nio API-, JSON-LD-, OAI-EAD- och HTML-originalen med individuella
SHA-256-värden redovisas i [S-0448](../sources/S-0448-riksarkivet-nysatra-bouppteckning-1913-api-atkomst.md):

- [F II/23 API](../media/S-0448-riksarkivet-nysatra-FII23-api-records.json),
  [JSON-LD](../media/S-0448-riksarkivet-nysatra-FII23-archive.jsonld) och
  [OAI-EAD](../media/S-0448-riksarkivet-nysatra-FII23-oai-ead.xml);
- [fondens JSON-LD](../media/S-0448-riksarkivet-nysatra-fonds-archive.jsonld)
  och [OAI-EAD](../media/S-0448-riksarkivet-nysatra-fonds-oai-ead.xml);
- [C II b/13 API](../media/S-0448-riksarkivet-vasterbotten-CIIb13-api-records.json),
  [JSON-LD](../media/S-0448-riksarkivet-vasterbotten-CIIb13-archive.jsonld)
  och [OAI-EAD](../media/S-0448-riksarkivet-vasterbotten-CIIb13-oai-ead.xml);
- [registrets täckningssida](../media/S-0448-riksarkivet-bouppteckningsregister-vasterbotten.html).

## Stödda påståenden

A-2285 och A-2481–A-2482.
