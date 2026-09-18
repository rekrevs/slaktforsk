# Återuppbyggnad från bevarade filer

Bedömning 2026-09-18, T-0667. Riktad kontroll PASS; full återuppbyggnad av
slutläget från en ren klon har inte körts. SQLite är fortsatt den ordinarie
kunskapsmodellen och `apply` den kontrollerade skrivvägen.

## Vad som behövs

| Underlag | Funktion |
|---|---|
| `schema/`, `lib/`, `cli.mjs` och Node 26 med SQLite/FTS5 | Samma schema, extraktion och operationsregler |
| `import/baseline/manifest.json` och samtliga hashadresserade `objects/` | Exakta ursprungstexter och provenansspann, inklusive äldre styrkontext |
| `operations/T-0641-pilot-v1.json` och historikmetadata i `lib/rebuild.mjs` | Den första operationen, som föregår journalformatet |
| `journal/000000001-…json` och alla senare poster i ordning | Redan fattade beslut, ändringar och deras historiska tider |
| Alla externa filer som importmanifestet och senare medieoperationer refererar | Originalbilder och övriga underlag, inklusive verkliga LFS-objekt |

Kuraterade paket och granskningar i `migration/`, historiska operationer och
Wotan-loggar bevarar dessutom varför konverteringen blev som den blev.
Återställning behöver inte på nytt generera dessa beslut med en agent.
Enbart det gamla genealogy-trädet är inte hela återställningsunderlaget.

T-0666:s commit `ba43433fee2666a35619ff8b4cc47d1570527e60` bevarar
4 327 nya/ändrade filer inklusive kod, bas och migration. Databas,
disponibla verifieringskopior och de parkerade SQL-dumparna är undantagna.
T-0667 tillför startfunktionen, provet, resultatet och denna instruktion.
GitHub main kontrollerades samma dag till `d1e4a8bc`; den nya grenen är
ännu lokal och extern LFS-hämtning är inte verifierad. En commit är inte
en extern säkerhetskopia.

## Reproducerbar start och föreslagen fortsättning vid förlust

Arbeta från den bevarade kodversionen, med verkligt LFS-innehåll enligt
projektets mediaanvisning. Välj en ny databasfil. Från repositoryts rot:

```sh
node genealogy2/cli.mjs bootstrap /tmp/rebuilt-genealogy.sqlite
node genealogy2/cli.mjs replay genealogy2/journal --db /tmp/rebuilt-genealogy.sqlite
node genealogy2/cli.mjs verify --db /tmp/rebuilt-genealogy.sqlite
node genealogy2/cli.mjs verify-assets --db /tmp/rebuilt-genealogy.sqlite
```

Starten och första journalposten är prövade tillsammans. Kommandoföljdens
hela replay till slutläget är en dokumenterad återställningsväg att pröva
vid behov, inte ett här genomfört fullprov. Jämför då även kanonisk export
med senast bevarad verifieringshash för motsvarande historiska slutläge.
T-0643:s slutläge hade hash
`1fc97543096073e048136e12bcb0d26cca357f60bb962a248b1cb0ca9366ecba`;
senare forskningsändringar ska naturligtvis ha en annan hash.

`bootstrap` kräver en ny fil och vägrar en befintlig databas eller avbruten
`.restoring`-fil. Det läser importbasen och det exakt identifierade
pilotpaketet, använder pilotens ursprungliga tid och återställer den
historiska basen utan journalkvittens. Därmed är nummer 1 ledigt för den
verkliga första journalposten. Anpassningen sker i en tillfällig export i
minnet och en ny återställningsdatabas; den skriver inte om huvuddatabas,
journal eller ursprungspaket. Den vanliga operationsmotorn är oförändrad.

Detta löser ett konkret övergångsproblem: vanlig `apply-legacy` på piloten
med dagens schema skulle lägga en ny kvittens på nummer 1, vilket kolliderar
med den bevarade journalen. Att ha rätt filer var därför inte ensamt nog
för en korrekt startinstruktion.

## Vad kontrollen faktiskt visar

Kör det begränsade provet med huvuddatabasen tillgänglig enbart för jämförelse:

```sh
node genealogy2/verification/T-0667-sample.mjs
node --test genealogy2/test/rebuild.test.mjs genealogy2/test/import.test.mjs genealogy2/test/workflow.test.mjs
```

[Maskinresultatet](../verification/T-0667-result.json) namnger urvalet,
kodhashar och indata-commit. Senaste provet tog 15,8 sekunder:

| Del | Resultat |
|---|---|
| Fullständig indataavstämning | 3 717 importdokument, 5 067 refererade artefakter, 40 operationsunderlag och 39 ordnade kvittenser |
| Importbasens integritet | Samtliga dokumentbyte och manifest kontrollerade med SHA-256; Git-spårning och artefaktstorlekar kontrollerade |
| Start från filer | Cirka 6,2 s; ny databas med korrekt pilotoperation/tid och utan felaktig journalkvittens |
| Exakt replay av prefix | Första journalposten införd, byteekvivalent lagrad begäran och sekvens; omkörning ändrar inget; 1 488 objekt |
| Senare sakligt urval | 198 objekt, samtliga deras 216 revisioner, 4 textenheters beslutshistorik och 1 460 jämförda rader identiska |
| Relevanta regressioner | 7 tester PASS, cirka 38,4 s; även avbrott, skydd mot överskrivning, ändrad pilot, medier, journal och rollback |

Urvalet omfattar pilotens familj och dopvittnen, alias/avvisade identiteter,
sen rättelse av en observation/slutsats, rättad dödshändelse samt beslut
från operationerna 38 och 39. Referenser och alla tidigare versioner sluts
deterministiskt från filpaketen. Även operationsberoenden för särskilt
kuraterade provenansspann följer med. Första urvalsförsöket missade sådana
spann och stoppades av en främmande nyckel; urvalsberäkningen rättades,
utan ändring av data eller operationsmotorn.

Den sena delen använder **projektioner** av originaloperationerna. Deras
begäranshashar och kompakta sekvens är inte originaljournalen, och fulla
personvyer ingår inte. Objektens faktiska revisioner, sakfält, belägg,
ursprung, medielänkar och aktuella revision jämförs däremot exakt med
huvuddatabasen. Inga huvuddatabasrader används för att bygga provdatabasen.
Reproducerbarheten för hela journalen kan inte bevisas genom att sätta ihop
dessa stickprov. Detta är ingen statistiskt slumpmässig undersökning.

Den tidigare skrivskyddade `verify-assets`-kontrollen samma dag verifierade
innehållshasharna för alla 5 067 artefakter. Dessa oförändrade medier
hashades inte om enbart för detta prov. Extern LFS-tillgänglighet, total
diskförlust och samtliga kombinationer i slutläget är inte prövade här.
Tidigare historiska underlagsluckor, exempelvis det saknade lexikonsvaret
i C-1017, finns kvar; återställning kan bara återskapa bevarat material.

## Varför migrationen var dyr och vad som kan förenklas

Det finns ingen komplett tids-/tokenbokföring per moment. Vi kan därför
inte ange hur stor andel av totalarbetet som var nödvändig eller undvikbar.
Följande åtskillnad stöds av kod, paket och Wotan-loggar:

1. **Semantisk konvertering.** Gamla A-rader och citationer hade blandat
   omfång, motstridiga läsningar och person-/källgränser som behövde bedömas.
   Textbevarande, typning och säkerhetsbedömning var olika resultat. Dessa
   beslut är nu sparade; en återställning ska återanvända dem utan ny
   källtolkning. Att automatisera all denna första bedömning i efterhand
   kan inte antas ge samma kvalitet eller samma resultat.
2. **Utveckling under pågående migration.** Modell, importer, läsvyer och
   testförväntningar utvecklades samtidigt. T-0661 fann exempelvis ett
   verkligt sorteringsfel först i den sista personvyjämförelsen efter
   export/restore. T-0659 hade sena fel i testförväntningar för både öppna
   tolkningsfrågor och skilda granskningsnivåer. Dessa omstarter behövs inte
   för återspelning med sparade, färdigprövade paket.
3. **Upprepad full uppbyggnad i tester.** Personkohortstester importerar
   basen och återspelar allt större prefix före nästa kohort. T-0662:s
   prov tog 1 030,5 s, medan T-0643:s samlade 119 modelltester tog
   1 942,1 s. Båda tiderna inkluderar betydligt mer än införsel. Det nya
   15,8-sekundersprovet omfattar mindre data och får inte användas som en
   uppmätt hastighetsökning för samma arbetsmängd eller prognos för full replay.
4. **Maskinell införsel.** Operationsmotorn preparerar flera SQL-satser
   per objekt, uppdaterar fulltext och följer beroenden. Det är kandidater
   för profilering vid ett faktiskt hastighetsproblem. Ingen isolerad
   mätning visar nu att någon av dem dominerar hela migrationen.

Prioriterad förbättring är därför att återanvända de redan fattade besluten
och den nu prövade startvägen. Vid framtida större konverteringar kan
små kontrakts-/riskprov köras före dyra slutprov, och en fryst, kontrollerad
testbas delas mellan tester där det är säkert. Ett separat från-noll-prov
behövs då för att inte dölja fel i basbygget. Eventuell cache måste knytas
till kod-, schema- och indatahashar; den får aldrig bli enda återställningsbas.

Breda databasoptimeringar och en omorganisation av överlappande filer är
inte genomförda här. Journal och operationspaket innehåller delvis samma
beslut, och stora historiska radhashlistor är verifieringsbevis snarare än
replayindata. Deras framtida placering/bevarande kan bedömas i T-0668 utan
att ta bort något nu. Restic kvarstår som parkerad möjlighet i T-0669.

Belägg: [T-0659](../../wotan/dev-log/T-0659.md),
[T-0661](../../wotan/dev-log/T-0661.md),
[T-0662](../../wotan/dev-log/T-0662.md),
[T-0643:s verifieringsmanifest](../migration/T-0643-support/verification-manifest.json)
och [T-0667](../../wotan/dev-log/T-0667.md).
