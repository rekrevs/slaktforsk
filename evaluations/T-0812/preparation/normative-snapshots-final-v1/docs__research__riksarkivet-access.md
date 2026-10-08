# Riksarkivet: aktuell åtkomst- och läsmetod

Aktiv norm, adopterad i T-0670 (2026-09-18) från den
[frysta metodhistoriken](../../genealogy/method-riksarkivet.md)
(SHA-256 `0bffd070d02fad00b1ec67850f155225564d7e7544a288a05edfe8628ee48c7b`). Ägarreglerna och läskraven gäller fortsatt.
Daterade tjänstesvar, versionsnummer, kodexempel och volymtabeller ligger kvar
som tekniskt erfarenhetsunderlag i originalet. De är inte garantier för
aktuell åtkomst eller instruktioner att använda gamla skrivplatser.
Kontrollera den konkreta tjänsten och dagens verktygsinstruktioner vid användning.

Alla nya källposter, avskrifter och åtkomstbedömningar skrivs genom
[Genealogy2:s arbetsväg](../../genealogy2/docs/working.md). Nya original
registreras med `stage-media` och provenans; inga nya filer skrivs i genealogy.
Fullupplösningsoriginal, dimensioner, SHA-256 och exakt källställe bevaras.

## Ägarregel 2026-09-03: Riksarkivets MCP först där den täcker behovet

När en ny agentsession har tillgång till den globalt konfigurerade
MCP-servern `riksarkivet` ska dess verktyg användas som första lämpliga ingång
för upptäckt, sökning, registerrouting och snabb interaktiv inspektion. Det
gäller bland annat strukturerad person- och registersökning, arkivmetadata,
transkriberat material, guider, manifest och dokumentvisning. När en exakt
reproduktions- eller bildnyckel väl är känd följer arbetet lagerreglerna nedan;
MCP-viewern är då inte ett obligatoriskt mellanled. Riksarkivet och dess
arkivposter, volymer och reproduktioner är fortfarande de källor som ska
citeras.

Ett MCP-svar ska därför så långt möjligt följas till och dokumenteras med
arkivbildare, referenskod, serie, volym, sida eller bild, beständigt id och
originalbild enligt projektets vanliga provenanskrav. Ett negativt MCP-resultat
är endast ett avgränsat sökresultat inom verktygets angivna täckning, inte ett
bevis för att personen eller handlingen saknas i arkivet.

Om MCP-servern inte är tillgänglig i sessionen, saknar ett relevant verktyg
eller inte exponerar tillräcklig metadata eller bildåtkomst, fortsätter arbetet
med den reproducerbara API-/JSON-LD-/IIIF-ordningen nedan. Chrome förblir den
snäva sista reserven. Ingen onödig information om levande personer ska skickas
till MCP-servern, och reglerna om inloggning och ALTCHA/CAPTCHA ändras inte.

### Operativ lager- och bevismodell

`MCP först` är en regel om första lämpliga ingång, inte ett krav att all senare
läsning eller bildhantering ska gå genom MCP. Arbetet skiljer på följande lager:

| Lager | Huvuduppgift | Vad lagret kan belägga | Normal övergång |
|---|---|---|---|
| MCP-sökning och specialverktyg | upptäckt, bred sökning, stavningsprövning, registerträffar och routing till ort, arkiv, serie eller volym | de fält som en namngiven register-, transkriptions- eller ortspost faktiskt återger; annars endast en kandidat eller sökobservation | följ positiva träffar till beständigt id, referenskod och när möjligt original |
| API, JSON-LD, OAI och IIIF-manifest | hierarki, metadata, reproduktions-id, canvasföljd samt avgränsning av år, församling eller handling | källans identitet och det dokumenterade undersökningsomfånget, men inte att en viss person står på en sida | gå till de exakta bildytorna och bevara avgränsningens start- och slutkontroller |
| Transkription eller originalbild | läsning och sakbelägg | en MCP-/registertranskription bär bara sina uttryckliga fält; för kyrkoboks- och andra sidbundna personpåståenden är den visuellt lästa originalbilden normal bevisgrund | skapa källpost, citat, påstående och uttrycklig evidensbedömning |
| Inloggad katalog eller Chrome-visare | snäv åtkomstreserv när publikt reproduktions-id saknas, direktbild ger `401`/`403` eller katalogen ensam exponerar nästa nyckel | endast det som faktiskt läses i katalogen eller originalbilden; åtkomstläget i sig är inget källnoll | återgå om möjligt till beständig metadata eller lokal, checksummad originalkopia |

MCP-burna Rosenberg-, TORA-, sjömanshus- och andra registerposter kan alltså
vara källor för avgränsade orts- eller registerpåståenden. De får inte utan egen
personbärande information omvandlas till bostad, arbete, identitet eller
släktskap. Ett IIIF-manifest belägger på motsvarande sätt volymens struktur och
ett sveps omfattning, medan den lästa bilden bär sidans personuppgifter.

### Negativa MCP-resultat och kontrollfrågor

Innan ett MCP-noll bevaras ska verktygets uppgivna täckning granskas och, när
det är möjligt, minst en känd positiv kontroll köras i samma dataset och nära
målfrågans geografi, tid och posttyp. Om även kontrollen ger noll klassificeras
utfallet som ett täcknings- eller frågesynlighetsresultat, inte som frånvaro av
personen eller handlingen. Ett filtrerat noll ska vid behov prövas mot en
ofilterad namnfråga och relevanta historiska stavningar; filterfälten kan vara
snävare eller ha annan normalisering än fritexten. Alla sådana omprov ska
redovisa exakt fråga och får inte sammanföra homonyma träffar.

### MCP-viewer eller direkt IIIF

MCP:s viewer får användas för snabb orientering, enstaka bildkontroll eller när
den exponerar en annars saknad länk. När reproduktions-, manifest- eller
bild-id redan är känt föredras den direkta IIIF-pipelinen för systematiska
svep, deterministisk år→bild-avgränsning, fullupplösta original, beskärningar,
rotationer, kompositer och lokal kontrollsummering. Detta är nästa lager efter
MCP-upptäckten och strider därför inte mot `MCP först`.

## Ägarregel 2026-08-29: API före Chrome

Riksarkivets API-lager ska alltid prövas före Chrome där det är möjligt:

1. sök-API för arkiv, serie och volym;
2. JSON-LD och `schema:hasPart` för hierarkin;
3. IIIF-manifest, `info.json` och Image API för innehåll och fulloriginal;
4. först därefter inloggad katalog/bildvisare om bildlänk saknas eller om
   IIIF ger ett dokumenterat `401`/`403`.

Chrome ska då användas så snävt som möjligt, exempelvis för att lösa ett
reproduktions-id som API/JSON-LD utelämnar eller för att hämta en bild som
direkt-IIIF spärrar. Varje övergång ska journalföra vad API-lagret gav, exakt
åtkomstfel och en återaktiveringsväg. ALTCHA/CAPTCHA löses inte utan ägarens
uttryckliga bekräftelse.

## Inloggning, åtkomstfel och återupptagning

Använd installerad browser-skill enligt dess aktuella instruktioner när
webbläsarreserven behövs. Läs inte ut kakor eller kopiera en användarprofil
för att återskapa en session. Historiska pluginrecept ersätter inte dagens
verktygsinstruktioner. Bevara inga autentiseringsuppgifter i forskningsmaterialet.

Vid utloggning eller captcha sparas exakt volym, bild/sida, URL, tidpunkt,
HTTP-svar, läsgräns, syfte och nästa ej utförda steg i uppgiftens Återupptagning.
Informera ägaren om behovet; ALTCHA/CAPTCHA kräver ägarens uttryckliga bekräftelse.
Fortsätt annat redan godkänt, avgränsat arbete under väntan. Återuppta den
sparade passagen när åtkomsten är åter, utan omstart eller nytt rutinmedgivande.

Ett oväntat åtkomstfel får inte tyst bli ett noll eller avsluta en gren:
meddela ägaren under arbetet, bevara det exakta felet och pröva tillåtna
alternativ. Skilj katalogpost, digital reproduktion, inloggad visare och
fungerande direktanrop. Historiska `401` har krävt inloggning; ett `403`
kan bero på anropsvillkor. Pröva bildens egen visarsida som `Referer` där den
vägen är tillämplig och dokumentera det faktiska svaret. Ingen svarskod ensam
bevisar frånvaro, odigitaliserat material eller arkivförlust.

En saknad bildlänk i MCP, sök-API, RDF eller IIIF-samling bevisar inte att
volymen saknar bilder. Kontrollera den fullständiga katalogen och vid behov
den inloggade visaren innan en terminal åtkomstbedömning görs. Om även denna
kontroll är blockerad ska just den oprövade kontrollen anges. `EJ DIGITALISERAD`
kräver oberoende belägg för digitaliseringsläget. Tillfällig spärr är ett
hinder, aldrig källslut. Kontrollera hela volymens tidsomfång, inte enbart
målsidans år; en parallell volym kan ha annan åtkomst.

ArkivDigital får inte besökas eller användas av agenten, heller inte för
katalogkontroll. Ägarens utdrag ger inget tillstånd till tjänsten.
Ingen beställning eller kontakt med arkiv följer utan separat mandat.

## Hitta rätt volym och uppslag

- Återanvänd känd referenskod, reproduktions-id, bevarat original och tidigare
  kontroller. Gå från MCP till metadata/hierarki/manifest och därifrån till
  exakt bild. IIIF-samlingar kan vara ofullständiga; korta svar är inget noll.
- Kontrollera volym, år och referenskod mot manifestets etikett eller fullständig
  katalog. Närliggande id:n har ibland gett rätt volym, men är gissningar tills
  detta verifierats. Föredra kända länkar framför obegränsade id-svep.
- Använd manifestets `structures`, canvasetiketter, ortregister och uttryckliga
  foliohänvisningar. Kontrollera parallella serier, delade band, inskjutna blad,
  dubblettbilder och sidluckor. Bildnummer och sidnummer är inte samma sak;
  ett beräknat offset ska alltid verifieras på måluppslaget.
- Ett årsindex eller ortregister lokaliserar, men garanterar inte full täckning.
  Läs fortsättningar och pröva båda banden när en församling är delad.
  Metadata bär omfång/routing, inte personfakta på olästa sidor.
- Rubrikmontage och små översikter får effektivisera lokaliseringen. Kontrollera
  utsnittet mot en känd sida; läs målposten i full upplösning innan avskrift.
  Anpassa region och storlek till bildens faktiska dimensioner.

## Läsning och negativa resultat

Läs hela bilden i översikt innan ett noll dokumenteras: räkna sidor och
kolumner och kontrollera att läsytan täcker hela det åberopade året eller
avsnittet. Båda sidor av uppslaget och alla relevanta hushåll ska omfattas.
Namnregister och deras uteslutningar får inte ensamma bära ett personnegativt
belägg; pröva relevant originalomfång. Skilj SCB:s avskrift från original och
registertranskription; de återger inte nödvändigtvis samma fält eller täckning.

Positivkontrollera en söktjänsts använda fältkombination mot en känd person,
ort eller titel i samma dataset innan den ska bära ett negativt belägg.
Om kontrollen fallerar är utfallet ett verktygs-/täckningsproblem. Lägg om
sökningen till fungerande fält; begränsa varje noll till faktiskt prövat
omfång och bevara frågeparametrarna. Ett indexnoll kan bevaras som just en
sökobservation utan att bli negativ evidens för personen.

Styrande fält — ort, församlingsförkortning, folio, datum eller annan nyckel
för nästa sökning — ska läsas i maximal upplösning och återges ordagrant
med läsosäkerhet, skilt från normalisering. Regeln gäller även ortregister.
Korsläs avsändande och mottagande församling när båda bokför samma händelse
innan uppgiften används som söknyckel. Om det inte går, bevara hindret och
behandla läsningen som en osäker ledtråd.

[Personkontraktet](person-contract.md#precision-och-full-avskrift) kräver
tryckta kolumnrubriker och skillnaden avskriven/tom/oläst för nya eller
omarbetade tabellavskrifter. Läs rubrik och datacell i samma utsnitt. Utvinn
hela relevanta posten med fortsättningar och hänvisningar; bevara rå läsning,
osäkerheter och original. En tekniskt lyckad hämtning är inte en läsning.

## Återanvänd daterad erfarenhet

Det [frysta åtkomstregistret](../../genealogy/access-register.md) innehåller
volymspecifika besked. Före ett nytt negativt åtkomstbesked kontrolleras:

1. Katalogpostens detaljvy och `Reproducerad på:`, inte bara sökträffen.
2. `Innehåller även:` och se-hänvisningar till andra handlingstyper/serier.
3. Serieförteckningens egna rader och fortsättningshänvisningar.
4. Myndighetens verksamhetstid och efterföljande arkivbildare.
5. Om handlingen kan ligga under en arkivbildare med ett annat slags namn.

Först när dessa har kontrollerats kan katalogläsningen bära ett negativt
åtkomstbesked. Det är fortfarande inget belägg för att en person saknas.
Läs relevanta tidigare kontroller, jämför datum och pröva vad som faktiskt
behöver kontrolleras igen. Ny åtkomstkunskap lagras i versionerade
källvägs-/forskningsobjekt i Genealogy2, med källa, datum och avgränsning.
Wotan sparar endast beslutat utförande och återupptagning.

Den [tekniska metodhistoriken](../../genealogy/method-riksarkivet.md) bevarar
API-/IIIF-adresser, bildprefix, routingexempel och tidigare webbläsarprov.
Senare rättelser där visar varför en äldre lyckad teknik eller generalisering
måste prövas på den konkreta volymen. Ingen gammal nedladdningssökväg eller
skrivinstruktion återaktiveras genom att exemplet återanvänds.
