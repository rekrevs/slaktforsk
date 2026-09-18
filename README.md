# Släktforskning

Detta är ett källstyrt släktforskningsprojekt. [Genealogy2](genealogy2/README.md)
är den auktoritativa kunskapsmodellen efter det verifierade skiftet i
[T-0643](wotan/dev-log/T-0643.md). All ny forskning och alla rättelser skrivs
där genom versionerade operationer. `genealogy/` är det bevarade äldre
forskningsarkivet. Wotan håller reda på utförandet.

Varje agent läser först [AGENTS.md](AGENTS.md), projektets styrdokument och
[arbetsvägen i genealogy2](genealogy2/docs/working.md). Före uppgiftsval och
återupptagning ska [wotan/README.md](wotan/README.md) läsas. Läs sedan
[backloggen](wotan/backlog.json) och den valda uppgiftens senaste
återupptagningspunkt. Ingen separat handover-fil används.

## Läs aktuell forskning

Kräver Node 26 med `node:sqlite`, utan npm-beroenden:

```sh
node genealogy2/cli.mjs person P-0016
node genealogy2/cli.mjs person P-0016 --full --format markdown
node genealogy2/cli.mjs inventory
node genealogy2/cli.mjs pedigree P-0269
node genealogy2/cli.mjs participations --role witness --event baptism
```

Personvyn visar aktuella uppgifter, konflikter, förbehåll, frågor och
granskningsläge med vägar till fulla detaljer och provenans. `inventory`
skiljer identitetsnivå och livsbild. `pedigree` tillämpar den uttryckliga
identitetsgrinden; stopp och deras skäl är synliga. Inget mått intygar
saklig måluppfyllelse. Gamla `scripts/goal-state.mjs` och
`scripts/research-inventory.mjs` beskriver endast det frysta arkivet.

## Kvalitetskrav och styrning

En uppgift blir inte fastställd därför att den står i ett släktträd. Varje
påstående ska ha en egen evidensbedömning och hänvisning till det underlag
som faktiskt stöder det. Källuppgifter, identitetsbeslut och slutsatser
hålls isär. Historik och ägarbekräftad kunskap bevaras.

[NORTH-STAR.md](NORTH-STAR.md) anger det långsiktiga målet: balanserad
anutvidgning och fullständiga livsbilder i återkommande genomgångar.
De sakliga kraven i det bevarade [personkontraktet](genealogy/person-contract.md),
[forskningsprogrammet](genealogy/research-plan.md) och
[källstrategin](genealogy/source-strategy.md) består. Deras äldre filformat
ersätts av den nya arbetsvägen. Aktuella frågor, teman, söknycklar och
källvägar finns i genealogy2:s versionerade forskningsobjekt; äldre front,
täckning och loggar kan läsas med `context` som historiskt underlag.

[PROJECT-CONTROL.md](PROJECT-CONTROL.md) bevarar ägarbeslut och styrbedömningar.
[Riksarkivets åtkomstordning](genealogy/method-riksarkivet.md) gäller fortsatt.
Öppna idéer finns i [IDEAS.md](IDEAS.md) och bedömt externt underlag i
[RELATED-WORK.md](RELATED-WORK.md). Dessa är ingen parallell utförandekö.

## Bevarande och överföring

Alla 538 äldre personakter är överförda med bevarade identitetsgränser:
536 verkliga personkärnor, ett alias och en avvisad läsning som arkivreferens.
Samtliga importenheter är redovisade; text, historik och olösta tolkningsfrågor
är synliga utan att räknas som full semantisk konvertering.
[Slutverifieringen](genealogy2/verification/T-0643-report.md) redovisar
sakgranskning, tester, journal och full återställning med verkliga medier.
Migrationens avslut betyder inte att släktforskningen är färdig.

Säkerhetskopiering och återställning beskrivs i
[genealogy2/README.md](genealogy2/README.md#backup-och-återställning).
[MEDIA-PRESERVATION.md](MEDIA-PRESERVATION.md) beskriver äldre källmediers
bevarande med Git LFS och SHA-256-inventering. Genealogy2 återbrukar dessa
medier och kontrollerar deras faktiska innehåll.

## Dashboard

Den lokala [forskningsdashboarden](dashboard/README.md) visar en sparad
äldre ögonblicksbild. Den uppdateras endast när ägaren uttryckligen ber om
det. Forskning, tester, byggen och commit/push uppdaterar den inte.
Aktuellt kunskapsläge läses i genealogy2 och utförandestatus i Wotan.
