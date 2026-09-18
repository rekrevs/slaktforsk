# Genealogy2

Auktoritativ kunskapsmodell efter T-0643:s verifierade skifte 2026-09-17,
enligt PCD-2026-09-16-001 och PCD-2026-09-17-001. All ny forskning och alla
rättelser skrivs här genom kontrollerade operationer. `genealogy/` är ett
bevarat, skrivskyddat forskningsarkiv. Wotan äger fortsatt utförandet.
Läs [arbetsvägen](docs/working.md) och [slutverifieringen](verification/T-0643-report.md).

SQLite är huvudlagring för strukturerad kunskap. Ursprungliga
dokument och versioner bevaras. Personakten blir en läsvy över personer,
källor, observationer, slutsatser och forskningsfrågor. Import är aldrig
i sig en genealogisk granskning eller ett nytt oberoende belägg.

## Körning

Kräver Node 26 med `node:sqlite`; inga npm-beroenden. Kör från repo-roten:

```sh
node genealogy2/cli.mjs status
node genealogy2/cli.mjs search "Hulda Amalia"
node genealogy2/cli.mjs show P-0016
node genealogy2/cli.mjs person P-0016
node genealogy2/cli.mjs person P-0016 --full --format markdown
node genealogy2/cli.mjs person P-0016 --format json
node genealogy2/cli.mjs inventory
node genealogy2/cli.mjs pedigree P-0269
node genealogy2/cli.mjs participations --role witness --event baptism
node genealogy2/cli.mjs context --group research-context
node genealogy2/cli.mjs inspect E-P0016-baptism
node genealogy2/cli.mjs inspect A-3652
node genealogy2/cli.mjs coverage
node genealogy2/cli.mjs verify
node genealogy2/cli.mjs verify-source
node --test genealogy2/test/*.test.mjs
```

`show` visar det bevarade äldre underlaget, med personakt
och profil åtskilda. Läs senare tillägg och historik tillsammans med
tidigare avskrifter. `person` visar en kort översikt med aktuella
uppgifter, granskningsgrind, konflikter, förbehåll och åtkomst till kvarvarande
underlag. `--full --format markdown` visar alla detaljer; `--format json`
ger hela den strukturerade personvyn. `inspect` visar objektets alla
versioner, argument, förbehåll, belägg och exakta ursprungsspann.
Personvyn har dessutom separata källobservationer, omnämnanden, sökningar
och kvarvarande tolkningsfrågor. Profilens frågor, teman, krav, söknycklar
och källvägsbedömningar återfinns i `research`; de behåller råa utfall och
kriterier. För enkla välkända frågeutfall finns även en normaliserad kod
(till exempel `ÖPPEN.` → `open`), utan att den äldre texten skrivs om.
Avvecklade profilfrågor behåller sin text och får `active: false`; ett
äldre öppet utfall återaktiverar inte forskningen. `active` anger att
frågan fortfarande ingår i forskningsmodellen, medan `outcome_code` anger
dess slutsatsläge. Uppgifter som preciserar en relation visas från båda
personerna under relationens `qualifications`, med samma revision och
egna förbehåll.

`search` söker både i aktuella domänobjekt och i det bevarade arkivet.
Träffarna anger vilket lager de tillhör. Personvyn och dess Markdownform
använder samma objektsläsare: händelse och deltagande har var sin bedömning,
motivering, förbehåll, provenans och omprövning. En ny objektrevision
stänger inte en väntande omprövning utan ett uttryckligt beslut.

## Typad modell och skrivväg

Schemat skiljer källbeskrivning, avgränsad källpost, avskrift, omnämnande
och observation från person, identitetsbeslut, händelse, deltagarroll,
relation och annan slutsats. Forskningsfråga, sökning, bedömning och
berättelse har egna tabeller. Ett person-id representerar en verklig person;
P-0295 finns som äldre alias till P-0027, medan P-0424 och P-0028 är skilda
personer. En avvecklad akt är inte automatiskt en avvisad personidentitet.

Varje objekt har oföränderliga revisioner. Nuvarande version är en SQL-vy,
inte en konkurrerande kopia. Datum skiljer exakta datum, år, ungefärliga
datum, intervall, alternativ och okänt; råform och förbehåll bevaras.
Kön härleds inte ur namn eller roller. Släktled/djup lagras inte i kärnan.
`pedigree` använder som standard `--mode verified`: roten och varje
passerad person måste ha uttryckligt godkänd identitetsgranskning och
bärande trädverkan. Livsbilden är en separat axel. Bara accepterade
föräldralänkar av tillåten art följs. Osäkra, avvisade eller ersatta
identiteter i beläggskedjan, väntande omprövningar och cykler stoppar
genomgången. Regler, bedömningsrevisioner och stopp är synliga.
`--mode typed` visar den bredare accepterade, typade delmängden utan
kontraktsgrinden; den får inte kallas verifierad antavla. Ingen av vyerna
intygar fullständig forskning. Vittnen och makar blir aldrig föräldrar
via rollord. Se [granskning av relationsarter](docs/relation-nature-review.md).

`inventory` skiljer identitetsnivå, trädverkan och livsbild. Äldre godkänd
helkontraktsgranskning behåller sitt ursprungliga omfång. `participations`
använder ett [uttryckligt frågeordförråd](docs/vocabulary.md): dopvittnen
med äldre `baptism_witness` hittas tillsammans med `witness`, medan råroll,
person-/omnämnandekoppling och egen evidensbedömning står kvar.

`apply` är den kontrollerade skrivvägen. En operation anger stabilt id,
aktör, skäl och ändringar med förväntad version. Hela operationen genomförs
eller rullas tillbaka. Samma operations-id och innehåll kan upprepas utan
dubbletter. Tidigare observationer ändras aldrig: rättelse ger ny revision.
Belägg pekar på en bestämd revision; rättelser skapar omprövningsmarkeringar
för berörda slutsatser, också genom flera led. Dessa stängs med en uttrycklig
motivering. Ägarkunskap får inte tyst nedgraderas eller ändras.

Nya källposter binder källbeskrivningen; avskrifter, omnämnanden och
observationer binder källposten; observationer och identitetsbeslut binder
omnämnandet; deltaganden binder händelsen och eventuellt omnämnande.
Ange revisionen i `evidence` eller `bindings: { "R-id": 1 }`. Referenser till
objekt som skapats eller reviderats tidigare i samma operation binds till
den uttryckligen skapade revisionen. Saknad eller inaktuell bindning stoppas.
Dessa beroenden följs vid rättelser även när en separat beläggslänk utelämnats.
Vanliga personreferenser, till exempel frågans subjekt, är inte i sig belägg
och skapar inte denna typ av beroende. Slutsatser anger sina övriga belägg
uttryckligen. Belägg som blir inaktuella inom samma operation stoppas.

```sh
node genealogy2/cli.mjs migrate
node genealogy2/cli.mjs apply-legacy genealogy2/operations/T-0641-pilot-v1.json
```

Pilotoperationen är spårbar, avgränsad överföring, inte ett nytt
forskningsresultat. JSON-filen är ett historiskt importpaket som kan spelas
upp; efterföljande ändringar görs som nya operationer. Den är inte en andra
redigerbar personmodell. Schema 001 bevarar underlaget, 002 inför domänen
och 003 inför den särskilda alias-/importmappningen. Schema 004 inför nya
medier, återställningsjournal och domänsökning. Schema 005 inför versionerade
beslut om importenheternas representation: mappad, bevarad text, historik
eller en konkret återstående tolkningsfråga. Schema 006 ger ett sådant
beslut flera uttryckliga mål, också när äldre objekt återbrukas. Detta är kunskapsläge, ingen
ny arbetskö vid sidan av Wotan. Okänd version stoppas;
endast `migrate` uppgraderar en befintlig databas.

`apply-legacy` är endast till för historiska importpaket med den äldre
beläggspolicyn. Det bevarar pilotens redan fattade beslut och implicerar
ingen efterhandskomplettering av dess beroenden. Nya forskningsoperationer
använder alltid `apply`. En operation är ett granskningsbart JSON-dokument
med `id`, `actor`, `reason` och `changes`; se
[arbetscykeltestet](test/workflow.test.mjs) för ett komplett syntetiskt exempel.

Nya mediefiler förbereds med `stage-media <fil> --provenance <text>`.
Resultatet läggs i operationens `media`-lista, och källpostens ändring anger
`media: [{ "id": "M-…", "region": "rad 1" }]`. Filen lagras under sin SHA-256
i `genealogy2/media/objects/`. Hash och verkligt innehåll kontrolleras före
skrivningen. Nya medier har egen provenans och tilldelas aldrig den gamla
importbasen. Redan infört medium kan återanvändas genom sitt id.

Piloten prövar 12 personidentiteter samt P-0295 som alias. Alla deras
forskningsfrågor, profilhuvuden och biografier följer med som versionerad
äldre kunskap. Ett utvalt sakligt tvärsnitt är typat: Huldas födelse/dop,
föräldrar, vittnen, ortstolkning, flytt, vigsel, Maj Amalias föräldrar,
ett bevarat noll, en avvisad hypotes, olika identitetsfall och ägarkunskap.
Detta är inte full konvertering av dessa personers samtliga uppgifter.

T-0645 har därefter fört över hela person- och källregistren:
538 äldre P-id motsvaras av 536 personkärnor, ett alias (P-0295 → P-0027)
och ett avvisat läsningsförslag utan egen person (P-0412, arkivreferens
till P-0453). Av 27 avvecklade akter gäller 25 verkliga separata personer;
avvecklad släktgren är alltså inte detsamma som felaktig personidentitet.
Vid registerinförandet fick de 524 tillkommande kärnorna `recorded`, med
uttryckliga förbehåll och utan gissat kön eller nya släktlänkar. Senare
personkohorter prövar och versionsuppdaterar kärnorna individuellt.
P-0060:s visningsnamn använder den tidigare uttryckliga rättelsen
Jonas Petter Johansson, medan den äldre rubriken finns kvar i underlaget.

Alla 805 källbeskrivningar är bevarade ordagrant inklusive metadata och
tillägg. Separata normaliserade arkivfält/källklasser är ännu inte
tilldelade. [Registerrapporten](migration/registry-report.json) redovisar
täckningen; [avvecklingsprövningen](migration/retirement-decisions.json)
bevarar migrationsbeslutens motiveringar och exakta stödspann. Dessa
historiska importunderlag redigeras inte för senare sakrättelser; nya
bedömningar införs som databasoperationer. De efterföljande kohorterna
för över detaljerade källposter och personkunskap enligt nedan.

T-0646–T-0651 har granskat samtliga 1111 citationer (de exakta listorna finns i
`migration/cohorts.json`). 1928 nya källposter och 845 ordagrant bevarade
avskrifter har införts; pilotposter och återkommande hänvisningar återbrukas.
2118 bedömningar knyter varje citations läshistorik till rätt post, även när
en senare citation inte har någon ny avskrift. `inspect C-0094` visar till
exempel Adelas post 84 skild från Fredrik Wilhelms 85–86; datumet från den
senare posten överförs inte till hennes rad. `inspect R-id` visar också
postens samlade läshistorik under `current.readings`.
Nya bildlänkar till en tidigare införd post kräver en vanlig postrevision;
importören stoppar annars återbruket. Tretton sådana poster har fått fjorton
kompletterande bildlänkar med bevarade äldre versioner och uttrycklig
omprövning av berörda avskrifter/läsningar.
Familjefotografiernas bildtexter hålls skilda från slutsatser om bosättning
och personernas positioner på bilderna. En senare rättelse i en annan
citation, som Charlottas Skön i C-0218 jämfört med äldre Alnö i C-0378,
följer den gemensamma källposten.

T-0650 har dessutom beskrivit åtta volymer som de äldre citationerna
identifierade exakt men saknade egna S-id för. S-0810–0817 har ordagrann
metadata och exakta ursprungsspann; okänd källklass är inte gissad. Detta
återbrukar befintlig forskning och innebär ingen ny arkivläsning.

T-0651 kompletterar med tretton källbeskrivningar ur uttrycklig äldre
metadata (S-0818–0829 och S-0831). Stora Malm B/1 återbrukar S-0556;
ett nytt id för samma volym skapades inte. Den sista gruppen bevarar
bland annat Urboms belagda vuxenkedja och dödspost samtidigt som länken
till ett visst födelsebarn är återöppnad. Katalogposter om läsesalsåtkomst
hålls skilda från lästa personposter och negativa personsökningar.

Alla gruppernas textenheter har ett uttryckligt representationsbeslut.
Det innebär inte att allt blivit typade fakta: blandade sökkontroller,
osäkra postgränser och ännu otolkade uppgifter bevaras som text eller med
en konkret tolkningsfråga. Ett söknoll blir ingen positiv träff för målpersonen. Namngivna eller
numrerade kontrollposter inom sökningen bevaras däremot som egna poster. Personkohorterna ska föra vidare befintlig saklig kunskap
med dessa förbehåll, utan ny arkivforskning eller automatisk statusuppgradering.

T-0652 har överfört den första hela personkohorten, P-0001–P-0050:
100 akter/profiler, 1052 aktuella påståenderader och 592 relationsrader.
Paketet inför 4365 objektrevisioner, däribland 248 händelser, 284 relationer,
687 källobservationer och 129 ytterligare forskningsfrågor. Gemensamma
uppgifter och pilotobjekt återbrukas. S-0832 avgränsar den redan citerade
Luleåseminarievolymen D I a/3; två nya källposter skiljer en indexrad från
en bevarad bild respektive sidkontext från en persons egen rad.

Varje textenhet har ett utfall: 3550 fullständigt representerade,
3955 bevarade som text, 105 historiska och 158 med konkreta kvarstående
tolkningsfrågor. Dessa antal gäller migrationsenheter, som kan överlappa;
de mäter inte forskningsgrad. Avvisat moderskap, avvecklad forskning,
beroende källuppgifter och motstridiga datum har sina egna gränser kvar.
Återspelning av journalen på den tidigare fullständigt återställda
säkerhetskopian gav identisk kanonisk export. 28 tester passerar.
Se [uppgiftens resultat och verifiering](../wotan/dev-log/T-0652.md).

T-0653 har också överfört P-0051–P-0100: 100 akter/profiler, 529 aktuella
påståenderader och 427 relationsrader. De 3225 revisionerna återbrukar
gemensamma familjehändelser och håller kandidatföräldrar, registreringsdagar
och avvecklad forskning åtskilda. Händelsers kvalificerande sakuppgifter
visas nu från samtliga deltagares personvyer. Två rättade källroller och
en observation som blandade två källposter har prövats genom nya revisioner
och uttryckliga omprövningsbeslut; äldre evidens har bevarats.

Gruppen har 96 uttryckliga tolkningsfrågor kvar. 30 tester passerar;
verklig journalreplay ger identisk kanonisk export och verifierade medier.
Se [resultat och verifiering](../wotan/dev-log/T-0653.md).
T-0654 har överfört P-0101–P-0150: 100 akter/profiler, 729 aktuella
påståenderader och 476 relationsrader. De 4039 revisionerna skiljer bland
annat lysningar från vigseldag, kandidatbarn från vuxenidentitet och
personliga utflyttningar från familjens fortsatta flyttar. Flerpostsjämförelser
ligger som slutsatser med sina skilda underlag. Återbrukade kontextfakta
visas nu även hos andra berörda personer, med sitt verkliga subjekt och
sina förbehåll. 18 utlösta beroendeomprövningar har dokumenterats.

Gruppen behåller 131 konkreta migrationsfrågor; detta är inte olösta
tekniska beroendeomprövningar. 38 nya modelltester och 67 äldre regressioner
passerar. Journalreplay på den återställda säkerhetskopian ger identisk
kanonisk export och verifierade medier. Se [resultat och verifiering](../wotan/dev-log/T-0654.md).
T-0655 har överfört P-0151–P-0200 med 2214 revisioner och 4679
spårbara enhetsbeslut. Gruppen bevarar 56 uttryckliga tolkningsfrågor.
Senare vittnesrättelser, namnlösa källpersoner och osäkra orters räckvidd
följer med utan nya säkra släktskaps- eller födelseortsslutsatser.
47 modelltester och 67 äldre regressioner passerar; återspelning av
26 journaloperationer ger identisk kanonisk export och verifierade medier.
Se [resultat och verifiering](../wotan/dev-log/T-0655.md).

T-0656 har överfört P-0201–P-0250 med 3529 revisioner och 6082
enhetsbeslut. Familjeuppgifter, postbundna råvärden och äldre rättelser
är åtskilda; 127 tolkningsfrågor är uttryckligt bevarade. Båda databaserna
har identisk kanonisk export och inga väntande beroendeomprövningar.
Se [resultat och verifiering](../wotan/dev-log/T-0656.md).

T-0657 har överfört P-0251–P-0300 med 3815 revisioner och 6056
spårbara enhetsbeslut; 122 konkreta tolkningsfrågor bevaras. En avvecklad
dubblettakts gamla profil får importbeslutet som ämne och kan läsas utan
att skriva över den verkliga personens aktuella profil. 72 modelltester
passerar; journalåterspelning ger identisk export och verifierade medier.
Se [resultat och verifiering](../wotan/dev-log/T-0657.md).

T-0658 har överfört P-0301–P-0350:699 aktuella påståenderader och446
relationsrader i100 akter/profiler. 3944 revisioner och6027 enhetsbeslut
bevarar även omfattande sökhistorik, avvisade identiteter och sena rättelser.
20 semantiska riskgrupper, fullt kohort-/återställningsprov samt tidigare
77 modelltester och67 äldre regressioner passerar. Verklig journalåterspelning
ger identisk export och inga väntande beroendeomprövningar.
Se [resultat och verifiering](../wotan/dev-log/T-0658.md).

T-0659 har överfört P-0351–P-0400: 308 aktuella påståenderader och 426
relationsrader i 100 akter/profiler. 3438 revisioner och 5364 enhetsbeslut
bevarar sena källrättelser, skilda granskningsnivåer och 80 uttryckliga
tolkningsfrågor. Avvecklade forskningsfrågor förblir inaktiva. 41 semantiska
riskgrupper, fullt kohort-/återställningsprov, 78 tidigare modelltester
och 67 äldre regressioner passerar. Huvuddatabasen och journalåterspelad
säkerhetskopia har identisk export; alla 414777 tidigare rader är bevarade.
Inga väntande beroendeomprövningar. Se
[resultat och verifiering](../wotan/dev-log/T-0659.md).

T-0660 har överfört P-0401–P-0450:332aktuella påståenderader och467
relationsrader, med3382revisioner. Den avvisade läsningen P0412 kvarstår
som arkivreferens; P0424 är en verklig person vars forskning är avvecklad.
59semantiska riskgrupper,80modelltester och67legacytester passerade.
Huvuddatabas och återställningskopia har samma hash och inga väntande
tekniska beroendeomprövningar. Se [resultat och verifiering](../wotan/dev-log/T-0660.md).

T-0661 har överfört P-0451–P-0500:234aktuella påståenderader och397
relationsrader med5501spårbara enhetsbeslut.83sakgrupper och det nya
fullprovet passerade, inklusive deterministisk personvy efter återställning.
81modelltester finns nu;80tidigare tester och67legacytester passerade,
samt4domänregressioner efter sorteringsrättelsen. Huvuddatabas och
återställningskopia har500akter,36journalposter,0teknisktpending och
sammahash99834877e6db1a01954cd55df05ba9b399dfa91a653c70873533a3f3503e853f.
Se [resultat och verifiering](../wotan/dev-log/T-0661.md).

T-0662 har överfört sista38akter, P-0501–P-0538, med2509revisioner och
3737enhetsbeslut.82sakgrupper samt hela kohort-/återställningsprovetPASS;
alla500basrader bevarade. Huvud och restored har538akter,37journalposter,
0teknisktpending och sammahash
631caa2f11ca8749f776c5ad382bb36664b07fc3eeea4e3101ca6e7288a1dca0.
Se [resultat och verifiering](../wotan/dev-log/T-0662.md).

Alla 538 äldre personakter är överförda: 536 verkliga personkärnor,
P0295 som alias till P0027 och P0412 som arkivreferens till en avvisad
läsning. T0663:s [restavstämning](verification/T-0663-report.md) redovisar
samtliga 97854 importenheter, med synlig text, historik och öppna
tolkningsfrågor. T0643:s läsvyer, fulla medieåterställning och samlade
regression är verifierade; skrivansvaret är nu flyttat hit.
`context --group research-context` förtecknar äldre forskningssammanhang;
`context genealogy/access-register.md --format markdown` visar exakt
bevarad text med datum-/historikgränser och navigationsanknytningar.

## Bevarande och import

`import/baseline/manifest.json` anger exakta filversioner. `objects/`
innehåller forskningsdokumentens ursprungliga byte, adresserade med SHA-256.
Allt källmaterial under `genealogy/media/`, inklusive sparade API-svar,
refereras på befintlig plats och verifieras mot filernas verkliga innehåll.
Det kopieras inte till databasen. En LFS-pekare accepteras inte som media.
Även övriga binära artefakter refereras med hash. `.DS_Store` och
Python-cachefiler undantas; inga forskningsdokument undantas.

Styrfiler, äldre Wotan-loggar (till och med T-0639) och befintliga skript
följer med som daterat sammanhang. Deras senare utveckling är tillåten;
`verify-source` kontrollerar den frysta `genealogy/`-mängden, också
tillkomna eller borttagna filer. De nya utvecklingsloggarna arkiveras inte
rekursivt i sin egen importbas.

```sh
# Redan gjort: snapshot skapas bara i en ny katalog.
node genealogy2/cli.mjs snapshot
# Kan upprepas mot samma bas utan nya poster.
node genealogy2/cli.mjs import
```

En A-rad kan innehålla flera uppgifter. C-id kan omfatta flera källposter.
Q-/KP-id är lokala till personen, exempelvis `P-0016/Q-01`.
Importören bevarar text, råa tabellceller, rubriker, filhash och exakta
UTF-8-byte-/radspann. De utvunna raderna är inte färdigt tolkade domänobjekt.
Senare semantiska mappningar länkas till dessa enheter. Citerad historik
räknas inte som nya aktuella assertioner.

## Backup och återställning

### Bevarat underlag i Git

PCD-2026-09-18-001 prioriterar Git-säkring av kod, schema, exakt importbas,
kuraterade migrationsbeslut, operationspaket och beständig journal.
Befintliga källmedier bevaras fortsatt enligt `../MEDIA-PRESERVATION.md`.
SQLite-filen och disponibla verifieringskopior hålls utanför Git.

Den tidigare dumpimplementationen i T-0665 är parkerad. Lokala filer under
`backups/` och `backup.sh` är experiment, ignoreras i Git och ska inte köras
som ordinarie rutin. Ingen uppdelad SQL-dump eller resticinstallation är
beslutad backupstrategi. Historiska provresultat bevaras som historik.

T-0666 har säkrat filunderlaget i en lokal Git-commit. T-0667 har prövat
startkedjan och ett avgränsat urval ur senare operationer; se
[återuppbyggnad, provresultat och kostnadsanalys](docs/reconstruction.md).
En fullständig
nybyggnad av slutläget från en ren Git-klon är ännu inte verifierad.
Git-säkringen gör inte journalen till en alternativ redigeringsyta och
innebär inte att varje historiskt använd originalkälla har sparats.
En lokal commit skyddar inte mot diskförlust; extern Git/LFS-status ska
redovisas separat. Den tidigare verifierade fullbackupvägen finns nedan.

### Journal och fullständig mediebackup

Runtimefilen `data/research.sqlite` ignoreras i git. En export är en
återställnings- och granskningsartefakt, inte en parallell redigeringsyta.
`apply` sparar begäran och dess ordningsnummer i samma transaktion som
ändringen, och skriver därefter en beständig kvittens till `genealogy2/journal/`.
Kommandot rapporterar framgång först när båda är sparade. Vid avbrott efter
databasens commit men före kvittensen: upprepa exakt samma operation eller
kör `journal`. Databasen avgör vilka operationer som verkligen genomförts.
Journalen får inte redigeras eller användas som en parallell personmodell.
En äldre operation före schema 004 kan sakna kvittens och måste då finnas i
återställningens basbackup. Historiska importpaket bevaras också separat.

```sh
node genealogy2/cli.mjs backup /tmp/research-backup.sqlite
node genealogy2/cli.mjs export /tmp/research-export.json
node genealogy2/cli.mjs restore /tmp/research-export.json --db /tmp/restored.sqlite
node genealogy2/cli.mjs verify --db /tmp/restored.sqlite
# Full backup, inklusive importbas och samtliga gamla och nya medier:
node genealogy2/cli.mjs backup-bundle /tmp/research-full-backup
node genealogy2/cli.mjs restore-bundle /tmp/research-full-backup /tmp/recovered-root
node genealogy2/cli.mjs verify-assets --db /tmp/recovered-root/genealogy2/data/research.sqlite --source /tmp/recovered-root
# Återspela eventuella senare kvittenser i ordning, på återställd databas:
node genealogy2/cli.mjs replay genealogy2/journal --db /tmp/recovered-root/genealogy2/data/research.sqlite --source /tmp/recovered-root
```

Kommandona vägrar skriva över befintliga mål. Exporten bevarar alla
forsknings- och provenanstabeller; fulltextindex byggs upp vid återställning.
`backup-bundle` tar en sammanhängande SQLite-backup och kopierar dess
refererade filer med kontroll av verkliga hashvärden. `restore-bundle`
återställer till en ny rot, kontrollerar alla filer och databasens integritet
och återskapar det frysta textmaterialet. En avbruten `.building`-katalog
räknas aldrig som färdig backup. Exportversioner från schema 001–006 kan
återställas; äldre schemafiler ändras inte.
Återställning av en stödd äldre full backup migrerar endast den nya kopian.

SQLite-backup och journal innehåller inte bilder. Vid återspelning behövs
även alla medier som tillkommit efter basbackupen. Kopiera dem till samma
relativa sökvägar i den nya roten; saknade eller ändrade filer stoppar
återspelningen. En full backup, senare journal och senare medier behöver
säkerhetskopieras till annan enhet för skydd mot diskförlust. Lokal
`verification/` är en verifieringskopia, inte detta externa skydd. Bevara
också programkoden i git. Äldre medier omfattas fortsatt av
`MEDIA-PRESERVATION.md` och Git LFS. Endast en databas ska användas för
ordinarie skrivning; återställda kopior är test-/återställningskopior tills
skrivansvaret uttryckligen flyttas. Optimistiska versionskontroller stoppar
konkurrerande ändringar mot en föråldrad objektrevision.

Status och tester redovisar teknisk överföring separat från återstående
semantisk konvertering. [Täckningsredovisningen](migration/README.md)
och dess exakta omfångsgrupper stödjer de avgränsade Wotan-uppgifterna.
Övergångskriterierna i T-0643 är uppfyllda. Fortsatt forskning kräver en
aktiv, godkänd, avgränsad Wotan-uppgift enligt den nya arbetsvägen.
