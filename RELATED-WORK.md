# Relaterade arbeten

Aktualitetsnot 2026-09-18 (T-0670): datamodellens pilot, migration och
skifte är genomförda enligt [T-0643](wotan/dev-log/T-0643.md).
Diskussionerna och bedömningarna nedan är daterat beslutsunderlag, inte
aktuellt migrationsläge eller nya startorder. Se [ansvarskartan](README.md#var-informationen-hör-hemma)
och Wotan för dagens styrning och utförande. Tidigare osäkerheter är
bevarade med dåtidens omfång; slutverifieringen anger vad som faktiskt prövats.

- Protocol: `project-control-related-work/v0.1`
- Storage mode: `lightweight`
- Last synthesized: `2026-09-16`
- Scope: modeller och arbetssätt för datamodellfrågan i
  [IDEA-0001](ideas/IDEA-0001.md), på ägarens begäran.

## Daterad syntes, 2026-09-16

De granskade arbetena ger användbara förebilder för källbundna
personbeskrivningar, gemensamma händelser, provenans och kontrollerade
ändringar. De avgör inte om just detta projekt bör ha textfiler eller
SQLite som auktoritativ lagring.

**Projektets tolkning:** börja med informationsansvar och pröva verkliga
ändringsfall. GEDCOM X och Gramps bidrar med genealogiska begrepp
(RA-001/002 nedan), PROV med spårbarhet (RA-003), och de två
arkitekturråden med både en övergångsmetod och invändningar mot fler lager
(RA-004/005). SQLite-dokumentationen avgränsar vilka garantier motorn
faktiskt kan ge (RA-006/007). GEDCOM 7 är relevant för utbyte (RA-008).
GENTECH är identifierat men inte färdigbedömt (RA-009).
De fullständiga bedömnings-id:na har prefix `RA-2026-09-14-`.
Förkortningarna SR-001/002 nedan avser sökningarna
SR-2026-09-14-001/002.

**2026-09-16, ny frågeram:** ägaren frågar hur ett nybygge borde
utformas och undantar dagens kontrakt och standarder från bedömningen.
Codex rekommenderar då relationsdatabas som huvudlagring, med SQLite
för lokal användning med måttlig skrivsamtidighet. Detta är en egen
syntes, inte en standardföreskrift eller ett beslut om det befintliga systemet.
GENTECHs två diagram har nu lästs; den fullständiga modelltexten
är fortfarande inte granskad. Se RA-2026-09-16-001–005 nedan.

En följdfråga samma dag gäller återanvändning av det befintliga materialet.
Den föreslagna övergången i IDEA-0001 kombinerar en bevarad importbas,
spårbar konvertering och tydligt skrivansvar. RA-2026-09-16-006/007
ger begränsat metodstöd; de lokala importreglerna och deras kvalitet
är inte verifierade av de externa källorna.

Den viktigaste kvarvarande osäkerheten är om en mindre ändring inom
Markdown ger samma förbättring som en separat strukturerad kärna.
Inget jämförande arbetsflödestest har utförts. En testad förenkling,
tydligt bättre ändringsflöde med SQLite eller informationsförlust i en
föreslagen textmodell skulle ändra rekommendationen.

Filen infördes 2026-09-14. Äldre genealogiska metodkällor i
[källstrategin](docs/research/source-strategy.md), dess pilotunderlag och
`genealogy/citations/` ligger kvar; detta register ersätter inte
projektets S-/C-register eller dess källvärdering.

Styrbedömning: [PCR-2026-09-14-001](PROJECT-CONTROL.md#pcr-2026-09-14-001).
Inga externa arbeten har i sig skapat en Wotan-uppgift eller ett ägarbeslut.

## Sökning SR-2026-09-14-001

- Datum/aktör: 2026-09-14, Codex med webbsökning och läsning av primärkällor.
- Fråga: håller den första SQLite-/textmodellskissens påståenden om
  integritet, lagring och källbundna personer?
- Läge: focused-scan; retrospektivt bevarande av sökningen i den första,
  skrivskyddade granskningen.
- Källfamiljer: SQLite-dokumentation och GEDCOM X-specifikationen.
- Sökfrågor:
  - `site.sqlite.org foreign key support enabled separately each database connection STRICT tables`
  - `site.sqlite.org whentouse SQLite database file git transactions`
  - `site.gedcomx.org conceptual model persona evidence conclusion extracted person`
- Omfång: engelska, primära tekniska dokument; ingen undre datumgräns,
  tillgängligt material vid läsningen 2026-09-14. Ingen geografisk begränsning.
- Stoppregel: de aktuella påståendena om databasgarantier och persona
  kunde bedömas direkt i respektive ansvarig organisations dokumentation.
- Bevarat underlag: RA-2026-09-14-001, -006 och -007.
  SQLite-sidorna [STRICT Tables](https://www.sqlite.org/stricttables.html)
  och [Appropriate Uses](https://www.sqlite.org/whentouse.html) lästes också
  som bakgrund; ingen separat slutsats om versionskrav eller prestanda
  vilar på dem här.
- Täckningsluckor: ingen benchmark, testad migration, produktutvärdering
  eller systematisk genomgång av genealogiska datamodeller.

## Sökning SR-2026-09-14-002

- Datum/aktör: 2026-09-14, Codex med webbsökning och direktöppnade
  officiella dokument; förlänger SR-2026-09-14-001.
- Fråga: vilka etablerade modeller och arkitekturmönster hjälper oss
  skilja evidens, slutsats och granskning samt minska dubbelt underhåll?
- Läge: focused-scan, orienterande jämförelse inför styrbedömning.
- Källfamiljer: FamilySearch/GEDCOM, Gramps officiella wiki och kodförråd,
  NGS/GENTECH, W3C och Martin Fowlers egna arkitekturtexter.
- Sökfrågor:
  - `site.gramps-project.org data model event reference citation source person research notes`
  - `site.ngsgenealogy.org GENTECH genealogical data model evidence conclusion persona`
  - `site.w3.org TR prov-dm entity activity derivation revision`
  - `site.martinfowler.com CQRS event sourcing complexity same database`
  - `site.github.com/gramps-project/gramps EventRef CitationBase role _eventref.py`
  - `site.gedcom.io GEDCOM specification 7 exchange genealogical data`
  - `site.martinfowler.com bliki BoundedContext shared model`
- Kompletterande läsning: officiella sidor och avsnitt som preciserade
  persona, händelsereferenser, transaktioner, provenans och stegvis byte.
- Omfång: engelska, originalspecifikationer, officiell implementation och
  upphovsmannens metodbeskrivning. Ingen undre datumgräns; cutoff
  2026-09-14. Äldre etablerade modeller inkluderades avsiktligt.
- Stoppregel: genealogisk modell, implementerat händelsemönster,
  provenansmodell, stegvis övergång och ett relevant motargument mot
  ökad arkitekturkomplexitet var täckta.
- Exkluderat i denna fråga: forumdiskussioner och inofficiella kopior när
  originalet var tillgängligt. Bredare företagsarkitektur och distribuerade
  system fördjupades inte eftersom det aktuella arbetsflödet är lokalt.
- Bevarat: nio kontextuella bedömningar totalt från de båda sökningarna;
  åtta inkluderade, en uppskjuten. Antal sökträffar används inte som
  täckningsmått.
- Täckningsluckor: inget program installerat eller provkört; ingen
  heltäckande jämförelse med kommersiella släktforskningsprogram;
  GENTECHs fullständiga modell inte granskad; inget bevis för lägre
  arbetstid eller felfrekvens i detta projekt.

## Källor och bedömningar

Bedömningarna under RW-0001–0009 är gjorda av **Codex 2026-09-14**, mot frågan i
IDEA-0001/PCR-2026-09-14-001. `Revises: none` gäller samtliga; detta är den
första registreringen. Historiska bedömningar ska bevaras om senare
läsning ändrar slutsatsen.

Ingen extern fulltext eller binär källartefakt har sparats lokalt.
Länkar, läspunkt och egna läsanteckningar bevaras här. Där en levande
webbsida saknar identifierad revision anges hämtpunkt, inte ett påhittat
versionsnummer eller hash. Vid en senare beslutskritisk implementation
behöver använd specifikationsversion låsas mer exakt.

### RW-0001 — The GEDCOM X Conceptual Model

- Kanoniskt id: `http://gedcomx.org/conceptual-model/v1`.
- Upphov/typ: FamilySearch, Intellectual Reserve; modellspecifikation.
- Version/läspunkt: Conceptual Model 1.0, stable draft, `master` läst
  2026-09-14; dokumentets publiceringsdatum och commit-id inte fastställda.
- Källa: [officiell specifikation](https://github.com/FamilySearch/gedcomx/blob/master/specifications/conceptual-model-specification.md).

**RA-2026-09-14-001 — include; definition, method.** Avsnitt 1.3.5,
2.5.2 och 4–4.1 skiljer bland annat ursprungliga/normaliserade värden
och källutvunna personbeskrivningar. Persona avser en beskrivning från
en källa. Det ger begreppsligt stöd åt separationen i vår modellskiss,
men specifikationen är avsedd för informationsutbyte och specificerar
inte projektets arbetsflöde. Projektpåverkan: använd begreppen som
referens, inte som beslut att implementera hela standarden.
Sökningar: SR-001/002. Ompröva vid konkret schema- eller exportutformning.

### RW-0002 — Gramps datamodell och dataåtkomst

- Kanoniskt id: `repo:https://github.com/gramps-project/addons-source`.
- Upphov/typ: Gramps-projektet; officiell utvecklardokumentation.
- Version/läspunkt: `maintenance/gramps61`,
  `docs/addon-development/05-data-access.md`, läst 2026-09-14,
  commit-id inte fastställt.
- Källor: [dataåtkomst](https://github.com/gramps-project/addons-source/blob/maintenance/gramps61/docs/addon-development/05-data-access.md),
  [Using database API](https://gramps-project.org/wiki/index.php/Using_database_API)
  som kompletterande modellöversikt, levande wikisida läst samma datum.

**RA-2026-09-14-002 — include; comparator, implementation pattern.**
Avsnitten om händelser, referenser och `DbTxn` visar gemensamma
händelseobjekt, personbundna roller och grupperade ändringar.
Projektpåverkan: jämför både objektmodellen och hur en ändring utförs.
Dokumenterade API-mönster är starkare förebilder än enbart en tabellskiss,
men bevisar inte passningen för våra identitetskonflikter och granskningskrav.
Wikin har äldre backendexempel; inga slutsatser om versionshistorik dras.
Sökning: SR-002. Ompröva vid en faktisk Gramps-jämförelse.

### RW-0003 — PROV-DM: The PROV Data Model

- Kanoniskt id/version: `https://www.w3.org/TR/2013/REC-prov-dm-20130430/`.
- Upphov/typ: W3C; Recommendation, 2013-04-30.
- Läspunkt: [PROV-DM](https://www.w3.org/TR/prov-dm/), 2026-09-14.

**RA-2026-09-14-003 — include; definition, method.** Modellen beskriver
entiteter, aktiviteter, ansvariga aktörer, härledning och revision.
Projektpåverkan: låt nya tolkningar länka sitt underlag och sin föregångare;
pröva spårbara beroenden för omgranskning. Standarden gäller provenans,
inte genealogisk sanningshalt. Dess invalidation ska inte förväxlas med
att en historisk observation blir falsk. Full RDF-/PROV-implementation
är inte motiverad av denna läsning. Sökning: SR-002.
Ompröva om vi behöver utbyta provenans med externa system.

### RW-0004 — CQRS

- Kanoniskt id: `https://martinfowler.com/bliki/CQRS.html`.
- Upphov/typ: Martin Fowler; ursprunglig arkitekturartikel, 2011-07-14.
- Läspunkt: [CQRS](https://martinfowler.com/bliki/CQRS.html), 2026-09-14.

**RA-2026-09-14-004 — include; challenge, implementation pattern.**
Skilda modeller för ändring och läsning behöver inte skilda databaser.
Fowler framhåller också mönstrets komplexitet och risker.
Projektpåverkan: håll förslaget enkelt och kräv visad nytta av varje
nytt lager. Detta är erfarenhetsbaserat arkitekturråd, inget jämförande
försök på vårt arbetsflöde. Att generera en akt kräver inte att vi bygger
ett fullständigt CQRS-system. Sökning: SR-002.
Ompröva om skilda läsbehov eller samtidiga skrivare ändrar förutsättningarna.

### RW-0005 — Strangler Fig

- Kanoniskt id: `https://martinfowler.com/bliki/StranglerFigApplication.html`.
- Upphov/typ: Martin Fowler; ursprunglig beskrivning av arkitekturmönster.
- Version: levande artikel; publicerings-/revisionsdatum inte fastställt här.
- Läspunkt: [Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html), 2026-09-14.

**RA-2026-09-14-005 — include; method.** Beskriver stegvis ersättning
av delar i ett befintligt system. Projektpåverkan: föreslå ett avgränsat
byte med tydlig gräns för vilken representation som äger en uppgift.
Artikeln bevisar inte att en viss migrering är förlustfri; våra
evidens- och rättelsefall behöver prövas separat. Sökning: SR-002.
Ompröva när en faktisk pilot har visat övergångens kostnad.

### RW-0006 — SQLite Foreign Key Support

- Kanoniskt id: `https://www.sqlite.org/foreignkeys.html`.
- Upphov/typ: SQLite-projektet; officiell motordokumentation.
- Version/läspunkt: [Foreign Key Support](https://www.sqlite.org/foreignkeys.html),
  levande dokument läst 2026-09-14; ingen enskild motorversion utvärderad.

**RA-2026-09-14-006 — include; definition, challenge.** Främmande
nycklar kontrollerar deklarerade referenser och behöver aktiveras för
anslutningen. Projektpåverkan: skilj motorns referensgarantier från
identitetsprövning och semantisk dubblettkontroll. Källan beskriver
SQLite, inte integriteten i en filbaserad huvudmodell med ett senare
byggt index. Sökning: SR-001. Ompröva vid vald skrivväg och schema.

### RW-0007 — Atomic Commit In SQLite

- Kanoniskt id: `https://www.sqlite.org/atomiccommit.html`.
- Upphov/typ: SQLite-projektet; officiell motordokumentation.
- Version/läspunkt: [Atomic Commit](https://www.sqlite.org/atomiccommit.html),
  levande dokument läst 2026-09-14; ingen motor-/hårdvarukombination testad.

**RA-2026-09-14-007 — include; support, comparator.** Transaktionen
ger ett sammanhängande allt-eller-inget-utfall under dokumenterade
förutsättningar. Projektpåverkan: SQLite som huvudlagring har en verklig
fördel när en ändring berör flera poster. Det ersätter inte granskning,
export, backup eller ett korrekt domänbeslut. Sökning: SR-001.
Ompröva vid test av avbrott och återställning i den föreslagna arbetsformen.

### RW-0008 — FamilySearch GEDCOM 7

- Kanoniskt id: `https://gedcom.io/specifications/FamilySearchGEDCOMv7.html`.
- Upphov/typ: FamilySearch; specifikation för genealogiskt informationsutbyte.
- Version/läspunkt: [FamilySearch GEDCOM 7](https://gedcom.io/specifications/FamilySearchGEDCOMv7.html),
  versionsfamilj 7, levande publicerad specifikation läst 2026-09-14;
  ingen exportimplementation eller enskild underversion validerad.

**RA-2026-09-14-008 — include; comparator, definition.** Relevant
referens för utbyte av genealogiska uppgifter. Projektpåverkan:
bevara export som ett eget användningsfall, skilt från hela den interna
forskningsprocessen. Dokumentet är inte samma specifikation som GEDCOM X.
Varken fullständigt stöd eller förlustfri export av vårt granskningsläge
har fastställts. Sökning: SR-002. Ompröva när T-0009 eller annat
avgränsat exportarbete blir aktuellt.

### RW-0009 — GENTECH Genealogical Data Model 1.0

- Kanoniskt id: `https://www.ngsgenealogy.org/wp-content/uploads/NGS-History/Diagram_GENTECH_Data_Model_1.0.pdf`.
- Upphov/typ: GENTECH, bevarat hos National Genealogical Society;
  historisk modelldokumentation.
- Version/läspunkt: version 1.0 identifierad i officiell sökträff
  2026-09-14; full modell och exakt dokumentdatering inte verifierade.
- Källa: [diagram hos NGS](https://www.ngsgenealogy.org/wp-content/uploads/NGS-History/Diagram_GENTECH_Data_Model_1.0.pdf).

**RA-2026-09-14-009 — defer; background, comparator.** Potentiellt
relevant historisk modell för samma problemfamilj. Fulltexten har inte
granskats; posten stöder därför inga specifika modellkrav i rekommendationen.
Projektpåverkan: undvik att beskriva vår skiss som en ny uppfinning eller
att senare återupptäcka kandidaten utan minne av avgränsningen.
Sökning: SR-002. Ompröva inför en djupare begreppsmodelljämförelse,
särskilt om identitet och slutsats fortfarande är otillräckligt lösta.

## Sökning SR-2026-09-16-001

- Datum/aktör: 2026-09-16, Codex; webbsökning och primärkällor.
- Fråga: hur bör ett genealogiskt forskningssystem utformas från grunden,
  när befintliga kontrakt, standarder och övergångskostnad lämnas åt sidan?
- Läge: focused-scan; fördjupar SR-2026-09-14-001/002.
- Sökfrågor:
  - `site.ngsgenealogy.org GENTECH genealogical data model assertion persona evidence conclusion model pdf`
  - `site.sqlite.org whentouse many concurrent writers client server application`
  - `site.gramps-project.org wiki Gramps Data Model events event reference citations`
- Direktläsning: tidigare GEDCOM X- och PROV-specifikationer;
  NGS historiksida och de två GENTECH-diagrammen; Gramps officiella
  XML-DTD; SQLite Appropriate Uses, Foreign Key Support och Atomic Commit.
- Omfång: engelska primärkällor, ingen undre datumgräns; cutoff
  2026-09-16. Forum och inofficiella sammanfattningar användes inte
  som tekniskt belägg. Historiska modeller användes som begreppsligt stöd.
- Stoppregel: åtskillnaden källinnehåll/slutsats, delade händelser,
  forskningsfrågor/aktiviteter, provenans och lokal databasdrift hade
  kontrollerbara primära förebilder.
- Täckningsluckor: ingen systematisk marknadsstudie, ingen prototyp,
  inget belastningstest och ingen fullständig standardimplementation.
  GENTECH 1.1:s modelltext har inte lästs; ingen rekommendation att
  kopiera dess fullständiga schema görs.
- Artefakter: länkar och egna anteckningar; inga nya lokala fulltexter.

## Kompletterande bedömningar 2026-09-16

Alla fem bedömningar nedan är gjorda av Codex mot nybyggesfrågan i
IDEA-0001 och hör till SR-2026-09-16-001. De innebär inget ägarbeslut.
Äldre bedömningar ovan kvarstår som daterad historik.

### RA-2026-09-16-001 — GEDCOM X

- Work/version: RW-0001, Conceptual Model 1.0 stable draft, `master`
  läst 2026-09-16. Revises: none; ny frågekontext.
- Disposition/roll: include; definition, method.
- Utdrag i sak: avsnitt 4 skiljer en källas beskrivning från forskarens
  uppfattning; 4.1 definierar persona. Avsnitt 2.6 medger textuell analys.
- Påverkan: föreslå separata observationer, identitetskopplingar och
  slutsatser med bevarat argument. Modellens specifika SQL-utformning
  och granskningsflöde är vår design, inte GEDCOM X-krav.
- Begränsning/omprövning: utbytesspecifikation, ingen jämförande
  studie av arbetsflöden; precisera vid faktisk schemautformning.

### RA-2026-09-16-002 — Gramps XML-modell

- Work id: `repo:https://github.com/gramps-project/gramps`.
- Källa/version: [data/grampsxml.dtd](https://github.com/gramps-project/gramps/blob/master/data/grampsxml.dtd),
  `master`, läst 2026-09-16; commit-id inte fastställt.
  Officiell implementation/exportdefinition. Revises: none.
- Disposition/roll: include; implementation pattern, comparator.
- Utdrag i sak: `eventref` har händelsereferens, roll och egna
  citationsreferenser; händelse och källa är självständiga objekt.
- Påverkan: belägg bör kunna knytas till en enskild personroll.
  XML-definitionen är ett förebildsexempel, inte ett beslut om intern
  XML-lagring eller att alla Gramps familjeantaganden ska användas.
- Begränsning/omprövning: inget produktprov; kompletterar RW-0002 från
  samma projekt och räknas inte som oberoende effektbevis.

### RA-2026-09-16-003 — GENTECH, diagrammen

- Work/version: RW-0009, Diagram 1.0, augusti 1998, samt
  [Process 1.0](https://www.ngsgenealogy.org/wp-content/uploads/NGS-History/Process_GENTECH_Data_Model_1.0.pdf),
  lästa 2026-09-16. [NGS historik](https://www.ngsgenealogy.org/history/)
  anger att modelltext 1.1 kom maj 2000 och att diagrammen var oförändrade.
- Revises: RA-2026-09-14-009 endast för de nu lästa diagrammen;
  fulltextgranskning kvarstår uppskjuten.
- Disposition/roll: include; historical comparator, definition.
- Utdrag i sak: diagrammen skiljer evidens, slutsatser och administration
  samt innehåller forskningsmål, aktiviteter, sökningar och argument.
- Påverkan: forskningsfrågor och sökutfall har historiska förebilder som
  självständiga data. Vår persona-/personmodell likställs inte med
  GENTECHs detaljerade semantik.
- Begränsning/omprövning: diagramnivå, ingen full modellgranskning
  eller empirisk användbarhetsbedömning. Fördjupa om dess struktur ska återbrukas.

### RA-2026-09-16-004 — SQLite för lokal huvudlagring

- Work id: `url:https://www.sqlite.org/whentouse.html`.
- Källa/version: [Appropriate Uses For SQLite](https://www.sqlite.org/whentouse.html),
  officiell dokumentation, levande sida läst 2026-09-16.
  Publiceringsdatum och motorversion för ett tänkt system inte fastställda.
- Disposition/roll: include; support, boundary condition. Revises: none.
- Utdrag i sak: lokal lagring och måttlig skrivsamtidighet passar SQLite;
  motorn har en skrivare åt gången. Hög samtidig skrivbelastning kan
  motivera en klient/server-motor.
- Påverkan: välj SQLite i nybyggesförslaget under uttalade antaganden.
  Transaktioner och aktiverade främmande nycklar stöds separat av
  RW-0006/0007, vars dokument också kontrollerades igen 2026-09-16.
- Begränsning/omprövning: ingen uppmätt belastning eller färdig
  applikation. Ompröva motorvalet vid många samtidiga skrivare;
  begreppsmodellens värde beror inte på just SQLite.

### RA-2026-09-16-005 — PROV och versionshistorik

- Work/version: RW-0003, W3C Recommendation 2013-04-30,
  läst igen 2026-09-16. Revises: none; ny frågekontext.
- Disposition/roll: include; method.
- Utdrag i sak: avsnitt 5.2 länkar härledningar och revisioner till
  tidigare entiteter och aktiviteter.
- Påverkan: bevara versionsberoenden så att ändrat underlag kan
  identifiera berörd analys. Automatisk markering för omprövning är
  vårt designförslag, ingen sanningsprövning som PROV tillhandahåller.
- Begränsning/omprövning: ingen full PROV/RDF-implementation föreslås;
  ompröva vid krav på externt provenansutbyte.

## Sökning SR-2026-09-16-002

- Datum/aktör: 2026-09-16, Codex; riktad direktläsning.
- Fråga/läge: focused-scan av metodstöd för övergång till ett hypotetiskt
  genealogy2, inklusive parallell prövning och återställning.
- Källor/söklogik: återöppna RW-0005, Strangler Fig, samt SQLite Backup API
  på den officiella dokumentationsadressen. Inga nya sökmotorfrågor.
- Omfång: två engelska primärtexter; cutoff 2026-09-16; ingen undre
  datumgräns. Stopp när stegvis övergång och konsistent databasbackup
  hade direkt stöd. Ingen uttömmande migrationsstudie.
- Täckningsluckor: inga importförsök, tidmätningar eller tester av backup;
  ingen extern källa avgör de lokala A-/C-posternas betydelse.
- Artefakter: länkar och egna anteckningar, inga lokala fulltexter.

### RA-2026-09-16-006 — Stegvis övergång

- Aktör/kontext: Codex 2026-09-16, genealogy2-övergången i IDEA-0001.
- Work/version: RW-0005, [Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html),
  sidan daterad 2024-08-22, läst 2026-09-16.
- Disposition/roll: include; method. Revises: none; fördjupad frågekontext.
- Utdrag i sak: avgränsade delar kan ersättas stegvis, med en tillfällig
  övergångsarkitektur och lärande från de tidiga delarna.
- Påverkan: separera nybygge/provimport från skiftet av ordinarie
  skrivansvar. För ett litet lokalt projekt föreslår vi ett tydligt
  slutligt skifte; just denna avgränsning är vårt eget omdöme.
- Begränsning/omprövning: mönstret garanterar inte förlustfri dataimport.
  Ompröva omfattning och övergång när en pilot visar faktiska beroenden.
- Sökning: SR-2026-09-16-002.

### RA-2026-09-16-007 — Backup av SQLite

- Aktör/kontext: Codex 2026-09-16, bevarande och återställning i genealogy2.
- Work id: `url:https://www.sqlite.org/backup.html`.
- Källa/version: [SQLite Backup API](https://www.sqlite.org/backup.html),
  officiell levande dokumentation läst 2026-09-16; ingen motorversion testad.
- Disposition/roll: include; method. Revises: none.
- Utdrag i sak: Backup API kan skapa en konsistent databaskopia;
  dokumentationen beskriver också VACUUM INTO som ett alternativ.
- Påverkan: pröva verklig återställning av databas tillsammans med
  refererade media. Databasbackup bevarar inte automatiskt externa filer
  och återför inte nya databasändringar till äldre Markdown.
- Begränsning/omprövning: inget backupverktyg eller återgångsflöde har
  implementerats; kontrollera hela flödet innan ordinarie användning flyttas.
- Sökning: SR-2026-09-16-002.
