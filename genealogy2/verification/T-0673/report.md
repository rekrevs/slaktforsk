# T-0673: inventering och pilot för fullständig originalrevision

2026-09-18. T-0673:s avgränsade leverans är färdig. **Hela materialets
sakgranskning är inte genomförd.** Programmet ägs av Wotan, med 91 ändliga
kohorter T-0674–T-0764 och separat slutrevision T-0765.

## Omfång och beständighet

Manifestet låstes före bildläsning, efter 53 journaloperationer: 1111 äldre
citationer, 1955 aktuella källposter, 805 äldre och 828 aktuella
källbeskrivningar, 452 sökobjekt, 5067 importerade tillgångar och fem nya
medier. Dessa mängder överlappar och ska inte summeras som antal källor.
`lock.json` binder manifest, metod och exakt tolvdelad pilot med SHA-256.

`ownership.json` antar `cohorts-draft.json` och mappar varje grupp till Wotan.
Filnamnet draft och dess interna förslagsstatus är historisk proveniens,
inte aktuell arbetsstatus. `priority.json` kompletterar den ursprungliga
fördelningen med faktisk stödgraf. Endast backlog och dev-log äger utförandet.

Oberoende `check-scope.py` kontrollerar exakt och unik fördelning av alla sju
huvudmängder, fyra stödmängder samt 5023 distinkta innehållshashar.
270 citationer saknar direkt postmappning, 630 poster direkt medielänk och
4078 tillgångar direkt postlänk. Det är kopplingsmått, inte konstaterade fel.
Även dessa enheter har ägare; metadata, historik och ägarutsagor får särskild
disposition utan att försvinna ur täckningen.

## Pilotutfall

Exakta objekt, kvarstående begränsningar och ansvarig följduppgift finns i
`pilot-results.json`. Blinda läsningar, kontrolläsningar och jämförelser
bevaras i respektive JSON, inklusive läsarnas egna preliminära fel.

| Enhet | Resultat |
|---|---|
| P01 födelse/dop | Dopdag 14 april, inte 12, för båda tvillingarna. Vittnes-/förrättarfält delvis osäkra. |
| P02 vigsel | Brudgumsåret är ofullständigt 184; posten belägger inte 1849. Ingen föräldrakolumn eller namngiven far. |
| P03 död | Fel kolumnbetydelse rättad till barnmorska; civilståndets kombinerade rubrik bevarad. Födelsedagen fortsatt osäker. |
| P04 husförhör | 30/1 bekräftat; födelse-/inflyttningsår och andra svåra fält reserverade. |
| P05 flyttning | Avgränsad hushållspost bekräftad; inga namngivna hustru/barn tillagda. |
| P06 folkräkning | Hildur Elisabetta i utdraget, inte avskriftens Charlotta. Personens andra källors namnform bevarad. |
| P07 militär | Titel/rubriker återfunna, ålder/tjänstetid/längd/civilstånd kontrollerade; namn fortsatt osäkert. |
| P08 söknoll | Ingen identifierad sökt parrelation på sida263; blek skrift begränsar nollresultatet. |
| P09 Familia | Hela relevanta sekundärvyn utvunnen; inga kyrkboksoriginal därigenom verifierade. |
| P10 katalog | Bevarad projektmetadatasammanfattning identifierad; ingen personuppgift verifierad. |
| P11 ägarutsaga | OWNER_CONFIRMED bevarad; originalarkiv krävs inte för sådan ägarkunskap. |
| P12 saknad bild | Exakt bild gav403; ingen bildläsning, fortsatt återanskaffning i T-0319. |

Fyra enheter har säkert konstaterade fel: P01, P02, P03, P06. Det är ett
ändamålsstyrt metodurval, **inte ett skattat felmått för databasen**. Osäkra
omläsningar räknas inte som säkra rättelser. Ingen identitets-/föräldrarelation
eller person får helgodkännande enbart genom dessa granskningar.

Sex apply-operationer gav 90 revisioner, två nya medier och 133 individuellt
avslutade följdprövningar. Datumfält, observationer, avskrifter, fakta,
persontexter, frågor, söknycklar och källvägar prövades efter respektive fynd.
Operationsförslagen granskades separat; saknade beläggslänkar och förlorad
textkontext rättades före apply. Exakta operationer finns i
`genealogy2/operations/T-0673-*.json`; journalen äger införandehistoriken.
Äldre förslagskopior i verifieringsmappen är granskningshistorik, inte nya
operationsbeställningar. Kör inte om dem som om de vore aktuell plan.

P07:s två tillkomna rubrik-/titelbilder är fördelade i `additions.json`.
P01:s tvillingpost var redan del av det låsta materialet och lästes på samma
bild. Nytillkomna avskrifter och auditobjekt dokumenterar granskningen;
de är inte nya oberoende historiska källor.

## Metod, arbetsåtgång och effektivisering

Två läsare kan göra samma fel. Enighet räcker därför inte: använd relevanta
rubriker, förstoringar och jämförelsebokstäver på originalet. Skilj råvärden
från normalisering och källtolkning från personidentitet. Full relevant
postutvinning betyder inte att oläsliga fält får låtsas vara lästa säkert.

Registrerade delintervall för förstläsningar var P01 63s, P02 34s, P07 32s,
P03 76s, P04 206,6s, P05 92,6s; separata kontrolläsningar P06 16s och P08 24s.
Dessa omfattar inte all öppning, förstoring, jämförelse, diskussion,
följdprövning och verifiering. P03 hade en inledande överblick före timern.
Rootaktivtid har inte mätts heltäckande och parallell tid får inte summeras
till väggtid. Underlaget medger ingen trovärdig total kostnadsprognos för
hela revisionen. Framtida kohorter bör mäta de separata arbetsmomenten.

1955 poster grupperas i1526 komponenter genom delad bild/exakt lokalisering;
största komponenten har50 poster. Återbruk av exakt utvunnet radomfång och
primärt läsansvar per innehållshash sparar hämtning och dubbelarbete utan
att kalla olika rader automatiskt granskade. Befintliga T-0110/T-0673-läsningar
får återbrukas efter omfångs-, versions- och osäkerhetskontroll.

Den stora följdkostnaden ligger även i fri text vars beroenden inte är
explicit länkade. T-0672 prioriteras därför som nästa verktygssteg.
T-0671:s fasta494par-lista behåller eget konsistensansvar. Stödgrafen omfattar
2192 aktuella accepterade föräldra-/identitetsbeslut; saknade postvägar och
äldre revisionsbindningar redovisas. En ensam grafväg är inte bevis på en
ensam oberoende historisk källa.

## Verifiering och slutgrind

`verification-results.json`: verify, verify-assets och verify-source godkända;
59 operationer totalt, noll öppna omprövningar. Samtliga41 OWNER_CONFIRMED-
revisioner och deras objekt är orörda. Native inventory och Adams pedigree
är identiska med pilotens startläge: identitetsgodkännande199, kombinerad
grind51 och explicit livsbildsgodkännande0. Detta är regressionskontroll,
inte bevis att alla kvarvarande belägg är felfria.

Äldre validator,67 regressionstester och media-manifestkontroll passerar.
Äldre goal-state/research-inventory körda; historiska indikatorer ersätter
inte Genealogy2:s sakgrind. Fryst genealogy och dashboard är orörda.
Fulla native121-testsviten från T-0115 upprepades inte: inga ändringar i
modell/runtime gjordes; aktuell data/källor/medier kontrollerades efter apply.
Kohortgeneratorn återgav det låsta fördelningsunderlaget byteidentiskt.

T-0765 kräver exakt täckningsavstämning och ett nytt oberoende slumpstickprov
om minst100 distinkta aktiva primära granskningsenheter (eller alla om färre),
med frö/urval låst före resultat-/bildläsning. Riskprov redovisas separat.
Osäkert, rättat, granskat och åtkomsthindrat hålls isär. Planering och gröna
tekniska tester öppnar inte programmets slutgrind.

Förstoringar som nämns med `/tmp/` i läsloggarna var arbetskopior.
De bevarade originalbilderna och angivet rad-/bildomfång är återläsningsunderlag;
ingen slutsats förutsätter att temporära beskärningar finns kvar.
