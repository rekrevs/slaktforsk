# T-0643: verifierat skifte till genealogy2

Överföringen är slutförd 2026-09-17 enligt PCD-2026-09-16-001 och ägarens
uppdrag att arbeta kontinuerligt tills den är klar. Genealogy2 är nu den
auktoritativa kunskapsmodellen. `genealogy/` är bevarat forskningsarkiv;
all ny forskning och alla rättelser går genom den kontrollerade skrivvägen.
Dashboarden behåller sin tidigare ögonblicksbild. Ingen ny arkivforskning,
publicering, PDF, commit eller push ingick.

## Omfång och redovisning

Samtliga 538 äldre personakter är överförda med sina identitetsgränser:
536 verkliga personkärnor, P0295 som alias till P0027 och P0412 som
arkivreferens till en avvisad läsning. Avvecklad forskning är inte samma
sak som en avvisad verklig person. Aktuell kärna omfattar 43 366 objekt.

3 717 dokument, 5 067 medie-/artefaktfiler och samtliga 97 854 importenheter
är redovisade. [T-0663:s sakrapport](T-0663-report.md) beskriver exakt vad
som är typat, textbevarat, historik respektive fortsatt tolkningsfråga.
47 734 textbevarade enheter räknas inte som full semantisk konvertering.
8 214 överlappande frågebärande enheter behåller sina tidigare frågor och
tillstånd; de är inte nya uppdrag eller tekniskt väntande omprövningar.

De 51 dokumenten i forskningssammanhanget är tillgängliga genom `context`
med full text, hash och historiskt syfte. Gamla nästa-steg-notiser blir
ingen ny utförandekö. Forskningsfrågor, sökningar, teman, källvägar och
bedömningar kan läsas i den aktuella personvyn och uppdateras som egna
versionerade objekt. Äldre program och kontrakt behåller sina sakkrav;
deras Markdownformat kräver ingen dubbelskrivning.

## Ordinarie läsning och granskning

`person` visar nu en kort översikt. Hela Markdownvyn finns med `--full
--format markdown` och hela strukturerade vyn med `--format json`.
Unika fullständiga förbehåll, konflikter, kandidater och väntande
omprövningar bevaras i översikten. Händelsens bedömning är skild från
deltagandets; alias, avvisad läsning och avvecklad forskning är synliga.

| Provakt | Översikt, rader | Full vy, rader |
|---|---:|---:|
| P-0059 | 144 | 3 081 |
| P-0412, arkivreferens | 52 | 875 |
| P-0424, avvecklad forskning | 129 | 2 408 |
| P-0434 | 76 | 1 517 |

Alla fyra översikter är mindre än en sjättedel av fullvyns textlängd.
De faktiska CLI-resultaten har jämförts med hela personobjektet och med
resultaten efter återställning. Detta visar minskad presentationsmängd;
forskarens tidsbesparing vid framtida arbete är ännu inte uppmätt.

`pedigree` har som standard en verifierad identitetsgrind. Roten och varje
passerad person måste ha uttryckligt godkänd identitetsgranskning och
bärande trädverkan. Nya kriterier går före gamla profilhuvuden per axel.
Konkurrerande bedömningar, väntande omprövning, ogiltigt eller ersatt
underlag ger synliga stopp. Livsbilden är en separat axel: P0004 passerar
identitetsgrinden trots underkänd livsbild. P0453 och P0481–0488 passerar
inte bara för att deras personkärnor är accepterade.

För P0269 ger den verifierade vyn 20 positioner och 19 kanter samt
14 synliga stopp. `--mode typed` ger 161 positioner och 160 accepterade
typade kanter utan kontraktsgrinden. Skillnaden ändrar inga lagrade
släktrelationer och är inget nytt godkännande. Det ägarbekräftade
`biological_parent` har ett prövat läsalias; två `correlated_parent` med
senare gradinvändning normaliseras inte blint. Den fulla
[sakgranskningen](../docs/relation-nature-review.md) bevarar dessa gränser.

Inventeringen har 511 aktiva av 536 personkärnor, 199 användbara
identitetsgodkännanden och 51 bärande identitetsgrindar. Fem godkända äldre
helkontrakt behåller sitt ursprungliga omfång. Inget nytt fristående
livsbildsgodkännande har uppfunnits av migrationen. Dessa är registrerade
bedömningar och inget bevis att projektets north star är uppfylld.

Det [gemensamma frågeordförrådet](../docs/vocabulary.md) hittar samtliga
479 dopvittnen, inklusive åtta med äldre `baptism_witness`. Råroller och
omnämnandekopplingar är oförändrade. Samtliga 2 501 deltaganden och
1 306 forskningsfrågor är inventerade; 76 avvecklade frågor förblir
inaktiva. Okända utfallskoder visas med råtext och får inget gissat utfall.

## Skrivning, korrigering och återställning

Arbetscykelproven registrerar nya uppgifter, frågor och verkliga mediebyte
i isolerade testdatabaser; rättar observationer och identiteter; följer
beroenden; prövar konkurrerande versionsskrivning och transaktionsfel;
simulerar avbrott mellan databascommit och journalkvittens; och återställer
basbackup plus senare journal och medier. Syntetiska fakta har inte skrivits
i huvuddatabasen. Ofullständiga eller skadade medier stoppar återställning.

Den slutliga fullbackupen ligger i `verification/T-0643-backup`: 8 786 filer
och 6 935 580 706 byte, inklusive databas, importbas och verkliga refererade
medier. Den har återställts till `verification/T-0643-restored-root`.
Båda databasernas kanoniska export har hash:

`1fc97543096073e048136e12bcb0d26cca357f60bb962a248b1cb0ca9366ecba`.

Databasintegritet, alla mediehashar, oförändrat forskningsarkiv och
funktionella person-/forsknings-/antavlevyer passerar på båda kopiorna.
Återspelning av samtliga 39 journalposter på den nya kopian ger 0 ändringar.
T0663:s separata prov visar dessutom att samtliga 532 332 tidigare rader
och äldre tolkningsfrågor är bevarade efter de motiverade rättelserna.

Backupen är en lokal verifieringskopia. Rutinen för kopia till annan enhet,
senare journal och nytillkomna medier beskrivs i [README](../README.md#backup-och-återställning).
Runtimefilen är ignorerad i git; programkod, bas, operationspaket, journal,
granskningsunderlag och verifieringsloggar är beständiga lokala filer.
Inget commit-/pushmandat har antagits.

## Verifiering och instruktioner

- Hela modellsviten, 28 testfiler: 119 tester PASS.
- Äldre regressioner: 67 tester PASS.
- 35 semantiska T0663-riskgrupper före/efter införsel och efter återställning: PASS.
- Verkliga CLI-bruksprov, full backup/restore, journal, databasintegritet
  och käll-/mediekontroller: PASS.
- Slutlig struktur-/Wotanvalidering, länkkontroll och oförändrat
  genealogy/dashboard: PASS.

[T-0643-result.json](T-0643-result.json) innehåller huvud-/återställningsjämförelsen.
Exakta loggar, provvyer och filhashar finns i
[verifieringsmanifestet](../migration/T-0643-support/verification-manifest.json).
Rootens README/AGENTS, genealogy2:s README/AGENTS/arbetsväg, Wotans
konvention/mallar och north stars hänvisning till aktuella indikatorer är
samordnade. De anger samma skrivplats och bevarar ursprungliga sakkrav.
PCD-2026-09-17-001 dokumenterar ägarens fortsättningsmandat och dess
verkställda övergång; inget nytt forskningsmål eller ägarfaktum har införts.

Alla sex skifteskriterier i T-0643 är uppfyllda. Ingen migrationsuppgift
återstår. Fortsatt ordinarie forskning väljs i Wotan inom sitt befintliga
mandat och följer den aktuella [arbetsvägen](../docs/working.md).
