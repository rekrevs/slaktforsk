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

## Var informationen hör hemma

| Ansvar | Auktoritativ plats | Ändringsregel |
|---|---|---|
| Mål och kvalitetskontrakt | [NORTH-STAR.md](NORTH-STAR.md) | Ändras genom uttryckliga projektbeslut |
| Mandat, vägval och undantag | [PROJECT-CONTROL.md](PROJECT-CONTROL.md) | Daterade beslut; tidigare beslut bevaras |
| Agenternas startväg | [AGENTS.md](AGENTS.md) | Gemensam ingång; CLAUDE hänvisar hit |
| Aktuella forskningsnormer | [Personkontrakt](docs/research/person-contract.md), [program](docs/research/research-program.md), [källstrategi](docs/research/source-strategy.md), [åtkomstmetod](docs/research/riksarkivet-access.md) | Sakkrav underhålls här; frysta original ändras inte |
| Aktuell kunskap och evidenshistorik | Genealogy2:s huvuddatabas och versionsbundna objekt | Skriv genom `apply` enligt [arbetsvägen](genealogy2/docs/working.md); läsvyer redigeras inte |
| Uppgifter och återupptagning | [Wotan](wotan/README.md), backlog och aktuell dev-log | Enda utförandekön; återuppta ONGOING före READY |
| Källunderlag och gamla forskningsdokument | `genealogy/`, exakt importbas | Fryst och fortsatt nödvändigt; gamla README, mallar och instruktioner är historik |
| Nya källmedier | `genealogy2/media/objects/` | Registrera med `stage-media`, provenans och Git LFS |
| Återställningsunderlag | Kod/schema, importbas, migrationsbeslut, operationer, journal och verkliga medier | Bevara enligt [återställningsbeskrivningen](genealogy2/docs/reconstruction.md) och [mediereglerna](MEDIA-PRESERVATION.md) |
| Presentationer och idéunderlag | Dashboard, utgåvor, IDEAS och RELATED-WORK | Daterade vyer/förslag; äger varken personfakta eller utförande |

**Vid motstridiga besked:** utgå från gällande ägarbeslut och deras uttryckliga
omfång, NORTH-STAR:s sakkrav och dessa aktuella normer. En äldre instruktion i
det frysta arkivet eller en avslutad task återaktiverar aldrig gammal skrivning.
Genealogy2:s aktuella revisioner gäller framför ersatta slutsatser; ursprungliga
observationer finns kvar. Skilj verkliga beläggskonflikter från inaktuella texter.
En verklig normkonflikt ska preciseras i aktuell Wotan-uppgift och lyftas för
styrbeslut om den inte redan avgjorts; skapa inte en lokal specialregel.

Nya metodlärdomar förs in i ansvarig aktiv norm. Nya sakfynd och
åtkomstkontroller hör i Genealogy2. Arbetsläge hör i Wotan. Vägval och ändrat
mandat hör i Project Control. Historiska beslut och underlag skrivs inte om.
Arbeta direkt på main enligt ägarens instruktion.

[T-0668:s organisationsanalys](genealogy2/docs/project-organization.md) är daterat
beslutsunderlag. T-0670 inför denna ansvarskarta och aktuella normer med
befintliga källsökvägar. Ingen fysisk omorganisation behövs för arbetsvägen.

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
[Personkontraktet](docs/research/person-contract.md),
[forskningsprogrammet](docs/research/research-program.md) och
[källstrategin](docs/research/source-strategy.md) anger de aktuella sakkraven.
Aktuella frågor, teman, söknycklar och
källvägar finns i genealogy2:s versionerade forskningsobjekt; äldre front,
täckning och loggar kan läsas med `context` som historiskt underlag.

[PROJECT-CONTROL.md](PROJECT-CONTROL.md) bevarar ägarbeslut och styrbedömningar.
[Riksarkivets åtkomstordning](docs/research/riksarkivet-access.md) gäller fortsatt.
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
[MEDIA-PRESERVATION.md](MEDIA-PRESERVATION.md) beskriver gamla och nya källmediers
bevarande med Git LFS och SHA-256-inventering. Genealogy2 återbrukar dessa
medier och kontrollerar deras faktiska innehåll.

## Dashboard

Den lokala [forskningsdashboarden](dashboard/README.md) visar en sparad
äldre ögonblicksbild. Den uppdateras endast när ägaren uttryckligen ber om
det. Forskning, tester, byggen och commit/push uppdaterar den inte.
Aktuellt kunskapsläge läses i genealogy2 och utförandestatus i Wotan.
