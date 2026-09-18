# Forska och rätta i genealogy2

Detta är den aktiva arbetsvägen efter T-0643:s verifierade skifte 2026-09-17.
SQLite och dess versionsjournal är kunskapsmodellens huvudlagring.
Wotan är fortfarande den enda utförandekön. En exporterad JSON-fil eller
personvy ska inte redigeras som en andra personmodell.

## Läs före en avgränsad forskningsuppgift

Läs aktuell Wotan-logg och återupptagningspunkt. Öppna personens korta vy,
fulla detaljer och de källposter som uppgiften faktiskt berör:

```sh
node genealogy2/cli.mjs person P-0016
node genealogy2/cli.mjs person P-0016 --full --format markdown
node genealogy2/cli.mjs inspect R-C0976-banns86
node genealogy2/cli.mjs inspect A-3646
node genealogy2/cli.mjs inventory
node genealogy2/cli.mjs pedigree P-0269
```

Forskningsfrågor, källvägar, söknycklar, krav och teman ligger i personvyns
`research` och dess underliggande versionerade objekt. Aktuellt kunskapsläge
hämtas därifrån. Gamla akter, profiler, loggar och källtäckningsöversikter
är läsbart underlag, inte en konkurrerande uppdateringsplats:

```sh
node genealogy2/cli.mjs show P-0016
node genealogy2/cli.mjs context --group research-context
node genealogy2/cli.mjs context genealogy/source-coverage.md --format markdown
```

NORTH-STAR och uttryckliga ägarbeslut fortsätter att gälla. De sakliga
kraven i det aktuella [personkontraktet](../../docs/research/person-contract.md),
[forskningsprogrammet](../../docs/research/research-program.md) och
[källstrategin](../../docs/research/source-strategy.md) gäller. De kräver inte nya
Markdownprofiler. Identitetsnivå och livsbild hålls separata; accepterad
person eller relation är inget nytt kontraktsgodkännande. Den verifierade
antavlan kräver godkänd identitetsgranskning och bärande trädverkan för
varje passerad person. Livsbildens återstående arbete blockerar inte den
grinden. `--mode typed` är en uttrycklig inspektion av accepterade typade
länkar och får inte kallas verifierad antavla.

## Skriv en genomtänkt operation

Förbered en JSON-operation med stabilt `id`, `actor`, `reason` och
`changes`. Varje ändring anger `expectedVersion`, typ, sakdata,
disposition, evidensstatus, motivering, förbehåll och exakta underlag.
Läs den aktuella versionen först. Vid konflikt ska den nya versionen
sakprövas; ändra inte bara det förväntade versionsnumret.

Källbeskrivning S, avgränsad källpost R, avskrift T, omnämnande M och
observation O hålls åtskilda från person P, identitetsbeslut, händelse,
deltagande, relation och slutsats F. En observation återger sin egen
källpost. Jämförelser mellan poster och bedömningar hör i slutsatser med
alla berörda underlag. Samma registreringskedja är inte flera oberoende
röster. Kön härleds inte ur namn eller rollord. Rådatum och osäker precision
bevaras; tomfält eller utebliven träff får aldrig bli en obegränsad nolla.

Nya mediefiler införs med `stage-media` och knyts till rätt post. Ange
proveniens och spara full relevant utvinning från varje post som faktiskt
öppnats. Versionsbind källposter, omnämnanden och händelser med `evidence`
eller `bindings`. Beställningar, publicering och annan extern åtgärd kräver
sitt vanliga mandat. Följ [Riksarkivets åtkomstordning](../../docs/research/riksarkivet-access.md)
och [mediebevarandet](../../MEDIA-PRESERVATION.md).

```sh
node genealogy2/cli.mjs stage-media /sökväg/till/fil --provenance "Källa, åtkomst och läsning"
node genealogy2/cli.mjs apply genealogy2/operations/uppgift-batch.json
node genealogy2/cli.mjs verify
node genealogy2/cli.mjs verify-assets
```

Registrera en forskningsbatch en gång genom dess operation och journal.
Knyt skäl och forskningsanteckning till den aktiva Wotan-uppgiften och det
acceptanskriterium som förs framåt. Wotan hänvisar till operations-id och
resultat; skriv inte en parallell batch i det gamla forskningsarkivet.

## Rätta utan att skriva om historien

En rättelse skapar en ny revision av samma objekt. Tidigare innehåll,
ursprung och belägg står kvar. Behåll skilda verkliga personer och
konkurrerande identiteter; ett ersatt läsningsförslag är inte automatiskt
en person eller ett alias. Ägarkunskap får inte tyst ändras eller sänkas.
Registrera senare konflikt separat och för tillbaka den till ägaren.

Granska varje utlöst beroende. En slutsats kan versionsuppdateras och
bindas till det nya underlaget, eller stå kvar efter en uttrycklig
individuell motivering. `resolve` anger det exakta gransknings-id:t och
skälet; en ny revision stänger inte automatiskt en väntande omprövning.
Om källposten ändras behövs även prövning av dess avskrifter och omnämnanden.

Nya bedömningar använder det dokumenterade ordförrådet för identitetsnivå,
trädverkan och livsbild. Varje utfall behöver sakliga skäl och belägg;
konvertering, antal observationer eller en färdig Wotan-uppgift är inga
godkännandekriterier. Aktuella frågor och återaktiveringsvillkor bevaras
som kunskapsobjekt; de schemalägger inte arbete utanför Wotan.

| Bedömningens `criteria` | Tillåtna `outcome` | Betydelse |
|---|---|---|
| `identity_review/1` | `passed`, `failed` | Identitetsnivåns uttryckliga granskning |
| `tree_effect/1` | `supporting`, `waiting`, `non_supporting` | Om anlinjen får passera personen |
| `life_picture_review/1` | `passed`, `failed` | Separat granskning av livsbilden |

Använd en aktuell bedömning per kriterium och person; ny bedömning är en
revision med egna argument. Konkurrerande bedömningsobjekt eller väntande
omprövning stoppar grinden. Utan native bedömning återger läsaren den äldre
profilens uttryckliga rubrikutfall. Äldre helkontraktsgranskning märks som
just helkontrakt och omdöps inte till en oberoende ny livsbildsgranskning.

## Bevara och återställ

`apply` skriver databas och beständig journal. Samma operations-id och
innehåll kan köras igen utan dubblering. `journal` reparerar journalens
filkopior efter ett avbrott när databasskrivningen redan lyckats.
`apply-legacy` är endast historisk återspelning, aldrig vanlig skrivväg.

Använd `backup-bundle` och `restore-bundle` enligt README för databas,
importbas och verkliga medier. Kontrollera återställd export och mediehashar.
En gammal snapshot ensam räcker inte efter nya skrivningar: återspela även
senare journaloperationer och bevara deras nya media. Forskningsvyer och
JSON-exporter är läsbara, men enbart en rapport är ingen full säkerhetskopia.

Dashboarden behåller sin äldre ögonblicksbild tills ägaren ber om en
uppdatering. Byggen, validering och avslut av forskning uppdaterar den inte.
