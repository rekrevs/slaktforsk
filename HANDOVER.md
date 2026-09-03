# Handover 2026-09-03 (batch 228, verifierad)

Detta är den korta ingången för en ny Codex-session. Chattens historik är
inte källa för projektläget. Läs filerna och kontrollera arbetsytan innan
någon åtgärd görs.

Sedan ägarbeslutet 2026-09-03 finns projektets deklarativa mål i
`NORTH-STAR.md`. En ny session ska använda Riksarkivets globalt konfigurerade
MCP först för lämplig upptäckt, sökning och registerrouting och därefter följa
lager- och bevismodellen i `genealogy/method-riksarkivet.md`. API, JSON-LD,
OAI och IIIF-manifest avgränsar källan; originalbilden bär normalt sidbundna
personpåståenden. När bild-id redan är känt föredras direkt IIIF för
systematiska svep och lokalt bevarande. MCP-viewern är en orienteringsväg och
Chrome en snäv sista åtkomstreserv, inte obligatoriska mellanled. Om
MCP-verktygen inte syns är det ett åtkomst- eller sessionsläge, inte ett
källnoll.

Detta är aktuell handover efter batch 228 och ersätter den förbrukade
batch-227-ingången.

## Startordning i en ny session

1. Läs `README.md`, `NORTH-STAR.md`, `genealogy/method-riksarkivet.md`,
   `wotan/backlog.json` och `wotan/dev-log/T-0012.md`.
2. Läs `genealogy/research-log/2026-09-03.md`, därefter S-0633, C-0817 och
   P-0133. Batch 228 ger TORA-koordinater och kartrouting för Glippsta och
   Malstanäs, visar att socken-/länsfiltren missar kända positiva kontroller
   och bevarar ett verkligt IIIF/Chrome-åtkomstfall. Glippstas kartbild och
   båda `info.json` finns lokalt; Malstanäsbilden gav publik `401` och kunde
   ses men inte reproducerbart bevaras via inloggad Chrome. Inga sessionsdata
   lästes. Läs därefter S-0632, C-0816 och P-0051. Batch 227 ger Rosenberg-baserad miljökontext åt Jomark nära
   Robertsfors bruk och åt den avgränsade Öfverklinten-ledtråden. Lexikonet
   belägger inget bruksarbete, ingen ny vistelse och inget föräldraskap;
   moderna `Överklinten` och Lugnet gav endast stavnings-/lexikonbundna
   noll. Läs därefter S-0631, C-0815 och P-0336. Batch 226 ger
   Rosenberg-baserad miljökontext åt Rökland/Rockland
   och Tureberg samt en Lundby→Stora Lundby-hänvisning utan att lösa
   födelseidentiteten eller föräldrarna. Läs därefter S-0630, C-0814 och
   P-0133. Batch 225 ger Rosenberg-baserad ortskontext åt Glippsta,
   Malstanäs och Väsby utan att göra lexikonet till person- eller yrkeskälla.
   Läs därefter S-0629, C-0813 och P-0051. Batch 224 avgränsar sjömanshusens Matrikel/Liggare som en ny
   Piteå-källfamilj utan exakt Olaus/Olof Pehrsson/Persson-träff; två
   Olof/Ol. Jung-närträffar 1843 förblir orelaterade och originalen i
   Härnösands D I a/1 samt D I b/1 är analoga/mikrokort. Läs därefter
   S-0628, C-0812 och P-0336. Batch 223 visar att DDS mål-, lokal- och länstäckning inte ger en
   kompatibel Olaus-kandidat, medan nationella tjänstekontroller fungerar.
   Metadatanoll på fullnamn och fem redan katalogbelagda referenskoder är
   frågesynlighet, inte katalog- eller volymnoll. Läs därefter S-0627,
   C-0811 och P-0133. Batch 222 visar genom sex kända positiva målhändelser, tre
   länskontroller och positiva nationella tjänstekontroller att DDS saknar
   användbar synlig täckning för Södermanlands målområde; resultatet är
   inte ett person-, händelse-, vistelse-, relations- eller levnadsbanenoll.
   Läs därefter S-0626, C-0810 och P-0051. Batch 221 visar genom målfrågor, kända positiva lokala
   kontroller, länskontroller och positiva nationella tjänstekontroller att
   DDS saknar användbar synlig täckning för målområdet; resultatet är inte
   ett person-, födelse-, vigsel-, vistelse- eller föräldranoll. Läs därefter
   `genealogy/research-log/2026-09-02.md`, S-0625, C-0809 och
   P-0336. Batch 220 avgränsar SCB:s hela Sollentunautdrag 1920 till
   `A0056304_00294`–`_00339`, bevarar alla 46 fulloriginal och avvisar fem
   OCR-nomineringar i original; resultatet är endast en maskinassisterad
   kandidatscreening. Läs därefter S-0624, C-0808 och P-0133. Batch 219
   avgränsar SCB:s 31 Helgestasidor 1920 och avvisar fem
   OCR-nomineringar i fulloriginal; resultatet är endast en
   maskinassisterad kandidatscreening. Läs därefter S-0623, C-0807 och
   P-0051. Batch 218 läser nio fattigbarnslistor i Bygdeå K I/2 för
   1838–1843 och 1845–1847 samt avvisar fyra OCR-nomineringar i original;
   resultatet är strikt list-/namn-/profilbundet. Läs därefter S-0622,
   C-0806 och P-0336. Batch 217 fyller folkräkningsluckan 1900 med sju
   personposter och original `Folk_001017-164`; Edit står född 1894 mot
   1910 års 1895 och kräver egen födelsenotis. Läs därefter S-0621, C-0805
   och P-0133. Batch
   216 routar Forssa kommunalnämnds G 4/1–2 samt Helgesta
   kommunalnämnds D 2:1 och G 4 B/2–11 som exakta analoga mantals-/
   uppbördsvägar över Eriks kända Forssa- och Helgestaperioder. Läs därefter
   S-0620, C-0804 och P-0051. Batch 215 routar Bygdeå häradsrätts direkta domboks- och
   småprotokollsvolymer samt Svea hovrätts renoverade kopior för 1830; alla
   är analoga och endast läsesalsbundna. Läs därefter S-0619, C-0803 och
   P-0336. Batch 214 avvisar Karlskrona sjömanshus Olaus Fredriksson nr 272
   genom Torhamnuppgifterna, målpersonens samtidiga positiva kedja och hela
   Torhamn C I/5:s två exakt-datumnoll. Läs därefter S-0618, C-0802 och
   P-0133. Batch 213 identifierar Helgesta fattigvårdsnämnds periodtäckande
   analoga vägar D 2:1, A 1:1 och G 5:1 och avgränsar D 3:1 till 1950–1952.
   Läs därefter S-0617, C-0801 och P-0051. Batch 212 identifierar de
   analoga Bygdeå-mantalsvolymerna
   1830–1850 och avgränsar den digitala mantalsdatabasen till 1642–1820.
   Läs därefter S-0614–S-0616, C-0798–C-0800, P-0474, P-0500, P-0133 och
   P-0336. Batch 211 rättar Halla-födelsen och Flen–Helgesta-datumen samt
   bevarar de tre inloggade omproven. Läs därefter S-0613, C-0797 och
   P-0336. Batch 210 bevarar H II/1:s fullreproduktionsomfattande
   maskinassisterade namnformsscreening och sex fulloriginalavvisade
   kandidater. Läs därefter S-0612, C-0796 och P-0133 samt P-0135–P-0137
   för batch 209:s positiva Flen–Helgesta-kedja 1907–1909.
3. Kör `git status --short`. Rensa, återställ eller skriv inte över
   ändringar som finns där.
4. Återuppta bara den aktuella användarinstruktionen. Äldre chattpromptar är
   historik och får inte behandlas som nya uppdrag efter context compaction.
5. Om forskning ska fortsätta: rotera breddförst inom Wotan T-0012 från
   batch 228:s beständiga läge till P-0336. Upprepa inte C-0817:s exakta
   TORA-frågor utan ny stavnings-, kart-, jordregister- eller arkivnyckel.
   Kör ofiltrerad kontroll när TORA-filter ger noll; förena inte homonymer
   med avvikande socken/kommun. Kartorna från 1634/1685 belägger inte Erik.
   Malstanäsbildens publika `401` är ett åtkomstresultat; Chrome-reserven
   löste visning men inte beständig binär. Upprepa inte C-0816:s exakta
   Rosenbergfrågor utan ny stavnings-, kart-, jordregister-, arkiv- eller
   täckningsnyckel. Jomarks närhet till Robertsfors belägger inte arbete
   eller egendomsförhållande, och Öfverklintenposten belägger inte Barbros
   vistelse eller Olaus som far. Upprepa inte C-0815:s exakta
   Rosenbergfrågor utan ny stavnings-, kart-, jordregister-, arkiv- eller
   täckningsnyckel. Ortsmaterialet belägger inte personen, yrket,
   födelseidentiteten eller föräldrarna. Upprepa inte C-0814:s exakta
   Rosenbergfrågor eller namn-/ortmetadata utan ny stavnings-, kart-,
   jordregister-, arkiv- eller täckningsnyckel. Ortsposterna belägger inte
   personen och deras verksamhetsflaggor är inte Eriks yrken. Upprepa inte C-0813:s
   Piteåfiltrerade sjömanshusfrågor utan ändrad täckning eller en ny namn-,
   nummer-, fartygs-, original- eller hushållsnyckel; fulltextträffarna är
   inte personnoll. Upprepa inte DDS-frågorna för
   Stora Lundby/Hemsjö/Sollentuna eller Älvsborg/Stockholm och upprepa inte
   C-0812:s metadatanoll utan en dokumenterad täcknings- eller sökförändring;
   resultaten är inte person-, födelse-, föräldra-, katalog- eller
   volymnoll. Upprepa inte DDS-frågorna för
   Bettna/Årdala/Forssa/Flen/Helgesta eller Södermanland utan en
   dokumenterad täckningsförändring; C-0811 är ett registertäckningsresultat
   och får inte bli personnoll. Upprepa inte heller DDS-frågorna för
   Bygdeå/Lövånger/Västerbotten utan en dokumenterad täckningsförändring;
   C-0810 är ett registertäckningsresultat och får inte bli personnoll.
   Upprepa inte blind OCR av
   SCB:s Sollentunautdrag 1920 `A0056304_00294`–`_00339` utan en ny
   adress-, gårds-, sido-, familjemedlems- eller yrkesnyckel. Alla 46
   fulloriginal finns beständigt i `genealogy/media/` med C-0809-prefix;
   C-0809 är inte ett person-, vistelse-, församlings-, årgångs- eller
   helreproduktionsnoll. Upprepa inte heller blind OCR av SCB:s
   Helgestautdrag 1920 `A0056311_00782`–`_00812` utan en ny gårds-,
   hushålls-, sido- eller yrkesnyckel. C-0808 är inte ett person-,
   vistelse-, församlings-, årgångs- eller helreproduktionsnoll. Upprepa
   inte heller blind OCR av
   Bygdeå K I/2 `A0017300`; återta endast med ny person-, hushålls-, ärende-,
   datum- eller sidnyckel. Någon 1844-lista identifierades inte, och C-0807
   är inte ett person-, understöds-, föräldra- eller helvolymsnoll. J/4
   följs först från en faktisk bilagehänvisning. Upprepa inte folkräkningen
   1900 eller familjeposterna `Folk_117700509`–`Folk_117700515`; C-0806 har
   fyllt denna ryggrad. Om Edit senare återtas ska hennes egen födelsenotis
   lösa konflikten 1894/1895. Återta inte Forssa G 4/1–2,
   Helgesta D 2:1 eller G 4 B/2–11 utan analog originalläsning eller en ny
   gårds-, årgångs- eller bokföringsnyckel; ingen personrad har lästs och
   posterna saknar nätbild. Återta inte Bygdeå
   A I a/41, A I b/5, A II/10, Svea hovrätt E XI e/4118–4119 eller E XII
   b/384–390 utan ändrad digital åtkomst eller en ny akt-, tings- eller
   ärendenyckel; de är analoga och endast läsesalsbundna. Återta inte Karlskrona
   sjömanshus Olaus Fredriksson nr 272 som P-0336; C-0803 avvisar den exakta
   kandidaten men utesluter inte sjöarbete för målpersonen. Återta inte
   Helgesta D 2:1,
   A 1:1 eller G 5:1 utan analog originalläsning eller en faktisk folio-,
   datum- eller protokollhänvisning. Återta inte Vol/38–39 utan analog
   originalläsning eller en ny gårds-/hushållsnyckel. Upprepa inte blind OCR
   av Stora Lundby H II/1 `A0062259` utan en ny dokument-, datum-, gårds-
   eller flyttnyckel; Östra Fågelvik H II/5 post 4 den 1873-04-25 är
   fortsatt direkt Olaus-återstart. Om en ny CAPTCHA visas: rör inte
   kontrollen. Gör ingen läsesals- eller
   kopiebeställning. Använd endast Riksarkivet; använd MCP först där den
   täcker behovet och API/JSON-LD/IIIF som komplettering eller reserv.
   Skapa inte en ny dashboard, starta inte T-0013 och påbörja ingen ny
   utgåve-PDF.

## Sessionscheckpoint 2026-09-03 — batch 228

- TORA via MCP gav beständiga koordinat- och kartrutter för Glippsta och
  Malstanäs samt en källspecifik Väsby-kandidat. Filtren missade kända
  positiva kontroller; Bergatorp/Brosätter-homonymer förenades inte.
- Direkt IIIF bevarade två `info.json` och Glippstas karta. Malstanäs
  bildderivat gav `401`; inloggad Chrome visade rätt volym/bild 37 men
  kunde inte ge en reproducerbar lokal binär. Inga sessionsdata lästes.
- S-0633, C-0817, A-3114–A-3117 och fyra mediaartefakter bevarar hela
  utfallet. T-0012 är fortsatt `ONGOING`/`DOING`; nästa rotation är P-0336.
- Verifiering: 500 personer, 2 598 påståenden, 525 föräldralänkar, 1 968
  Markdownposter och 4 332 mediafiler inklusive `.gitkeep`; manifest 4 331
  (2 528 exakt, 1 775 käll-, 28 citationsavgränsade, 0 olänkade).

## Sessionscheckpoint 2026-09-03 — batch 227

- Rosenbergs geografiska lexikon prövades via Riksarkivets MCP för
  P-0051:s redan personbelagda Jomarkliv och den avgränsade
  Lundberg/Olaus-ledtråden.
- Jomark beskrivs som en by i Bygdeå nära Robertsfors bruk. Robertsfors
  egen post konkretiserar en järn-, verkstads-, kvarn-, såg-, varvs- och
  lastplatsmiljö vid Rickleån, men belägger inte att Barbro eller hennes
  familj arbetade där eller tillhörde egendomen.
- Historiska `Öfverklinten` beskrivs som en by vid Rickleån med kvarn.
  Moderna `Överklinten` och Lugnet gav noll. Det är stavnings- och
  lexikonkänslighet, inte vistelse- eller släktskapsnoll; Olaus förblir en
  obevisad faderskandidat.
- S-0632, C-0816, A-3110–A-3113 och en checksummad observation bevarar
  poster och inferensgränser. T-0012 förblir `ONGOING`/`DOING`; nästa
  breddrotation är P-0133. Ingen person, relation, födelseidentitet,
  förälder, ny bostads- eller yrkeshändelse, beställning, webbläsarsession,
  PDF, deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 594 påståenden, 525 föräldralänkar, 1 966
  Markdownposter och 4 328 mediafiler inklusive `.gitkeep`. Manifestet har
  4 327 poster: 2 528 exakt, 1 771 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, observationens SHA-256, oförändrad
  PDF-yta och `git diff --check` passerade. De väntat icke-nollande
  auditerna visar tio ogiltiga slutstatusar genom P-0004:s djup 5 med
  P-0051 som nästa tillåtna arbetsdjup och exakt P-0336 öppen genom
  P-0210:s djup 4.

## Sessionscheckpoint 2026-09-03 — batch 226

- Rosenbergs geografiska lexikon prövades via Riksarkivets MCP för
  P-0336:s redan personbelagda livskedja.
- Rökland/Rockland beskrivs som by-, ångsågs- och lastplatsmiljö på västra
  Alnön och Tureberg som hållplats på Norra stambanan mellan Järva och
  Rotebro. Lundby i Älvsborg/Vättle hänvisas till Stora Lundby.
- Personens vistelser, järnvägsyrken och död bärs av separata källor.
  Lexikonet belägger inget såg-/lastplats- eller Turebergsarbete och löser
  inte födelseidentiteten eller föräldrarna. Björknäs-/Kungsholmsnollen är
  endast lexikonbundna.
- S-0631, C-0815, A-3106–A-3109 och en checksummad observation bevarar
  poster och inferensgränser. T-0012 förblir `ONGOING`/`DOING`; nästa
  breddrotation är P-0051. Ingen person, relation, födelseidentitet,
  förälder, ny bostadshändelse, beställning, webbläsarsession, PDF,
  deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 590 påståenden, 525 föräldralänkar, 1 964
  Markdownposter och 4 327 mediafiler inklusive `.gitkeep`. Manifestet har
  4 326 poster: 2 527 exakt, 1 771 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, observationens SHA-256, oförändrad
  PDF-yta och `git diff --check` passerade. De väntat icke-nollande
  auditerna visar tio ogiltiga slutstatusar genom P-0004:s djup 5 med
  P-0051 som nästa tillåtna arbetsdjup och exakt P-0336 öppen genom
  P-0210:s djup 4.

## Sessionscheckpoint 2026-09-03 — batch 225

- Rosenbergs geografiska lexikon prövades via Riksarkivets MCP som ny
  berikningskälla för P-0133:s redan källbundna livslopp.
- Rosenberg 16202 beskriver Glippsta som en by nära Oxelösunds järnväg,
  36781 Malstanäs som en herrgård vid Uren med kvarn och såg och 63857
  Väsby i Flen som en gård vid Båven nära Västra stambanan, under Mälby i
  Helgesta.
- Personkopplingen bärs fortsatt av kyrkoböcker och folkräkningar.
  Lexikonet namnger inte Erik och verksamhetsflaggorna blir inte yrken.
  Mindre orters och namn-/ortmetadatans noll är endast stavnings-,
  lexikon- och frågefältsbundna.
- S-0630, C-0814, A-3102–A-3105 och en checksummad observation bevarar
  posterna och inferensgränserna. T-0012 förblir `ONGOING`/`DOING`;
  nästa breddrotation är P-0336. Ingen person, relation, ny bostadshändelse,
  beställning, webbläsarsession, PDF, deployment, commit eller push
  skapades.
- Verifiering: 500 personer, 2 586 påståenden, 525 föräldralänkar, 1 962
  Markdownposter och 4 326 mediafiler inklusive `.gitkeep`. Manifestet har
  4 325 poster: 2 526 exakt, 1 771 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, observationens SHA-256, oförändrad
  PDF-yta och `git diff --check` passerade. De väntat icke-nollande
  auditerna visar tio ogiltiga slutstatusar genom P-0004:s djup 5 med
  P-0051 som nästa tillåtna arbetsdjup och exakt P-0336 öppen genom
  P-0210:s djup 4.

## Sessionscheckpoint 2026-09-03 — batch 224

- Riksarkivets MCP prövade sjömanshusens Matrikel och Liggare som ny
  källfamilj för Olaus/Olof Pehrsson född 1784-02-07 i Överklinten, med
  `Piteå` som positiv flyttnyckel.
- Piteåfiltrerad Matrikel visade ingen användbar täckning. Liggare gav
  regionala kontrollposter men ingen huvudperson med någon av de fyra
  Olaus/Olof Pehrsson/Persson-formerna i de kompletta målfrågorna.
- `Olof Jung` och `Ol. Jung` 1843 anges födda och hemma i Piteå och är bara
  närträffar. Härnösands sjömanshus D I a/1 och D I b/1 är enligt MCP
  odigitaliserade/otranskriberade och tillgängliga på mikrokort; ingen sida
  lästes och ingen person eller relation skapades.
- S-0629, C-0813, A-3099–A-3101 och en checksummad observation bevarar
  frågor, söksemantik, närträffar, originalrutter och tolkningsgräns. Olaus
  förblir obevisad faderskandidat. T-0012 förblir `ONGOING`/`DOING`; nästa
  breddrotation är P-0133. Ingen beställning, webbläsarsession, PDF,
  deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 582 påståenden, 525 föräldralänkar, 1 960
  Markdownposter och 4 325 mediafiler inklusive `.gitkeep`. Manifestet har
  4 324 poster: 2 525 exakt, 1 771 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 77,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-/observations-/
  dashboard-JSON, dashboardtest, produktionsbygge, observationens SHA-256,
  oförändrad PDF-yta och `git diff --check` passerade. De väntat
  icke-nollande auditerna visar tio ogiltiga slutstatusar genom P-0004:s
  djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt P-0336 öppen
  genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-03 — batch 223

- Riksarkivets MCP användes först på P-0336:s olösta födelse- och
  föräldrafråga. DDS missade Olaus/Olof i Stora Lundby 1852, den
  originallästa brodern Johan August 1849 och Olaus säkra vigsel/död samt
  tre länskontroller.
- Nationella tjänstekontroller gav 25 födelse-, 238 vigsel- och fyra
  dödposter. Exakt-datumfrågorna gav ingen kandidat förenlig med den säkra
  Älvsborg–Fågelvik–Alnö-kedjan.
- Metadatasökningen missade fullnamn och fem redan katalogbelagda
  referenskoder trots positiva breda kontroller. Det upphäver inte tidigare
  katalogbelägg. S-0628, C-0812, A-3098 och en checksummad strukturerad
  observation bevarar frågor och tolkningsgräns.
- Olaus födelsedatum och föräldrar förblir olösta. T-0012 förblir
  `ONGOING`/`DOING`; nästa breddrotation är P-0051. Ingen person, relation,
  beställning, webbläsarsession, PDF, deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 579 påståenden, 525 föräldralänkar, 1 958
  Markdownposter och 4 324 mediafiler inklusive `.gitkeep`. Manifestet har
  4 323 poster: 2 524 exakt, 1 771 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 77,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-/observations-/
  dashboard-JSON, dashboardtest, produktionsbygge, observationens SHA-256,
  oförändrad PDF-yta och `git diff --check` passerade. De väntat
  icke-nollande auditerna visar tio ogiltiga slutstatusar genom P-0004:s
  djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt P-0336 öppen
  genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-03 — batch 222

- Riksarkivets MCP användes först för sex exakta, originallästa händelser i
  P-0133:s familj: födelsen i Bettna 1851, vigslarna i Årdala 1876 och Flen
  1895, dödsfallen i Forssa 1887, Flen 1920 och Helgesta 1935. Alla sex
  gav noll i DDS Födelse/Döda/Vigsel.
- Tre länsvida Södermanlandskontroller gav också noll, medan nationella
  tjänstekontroller gav 156 födelseposter, 32 vigselposter och en
  dödfulltextträff. Utfallet är ett DDS-täckningshinder och ändrar inte
  originalbeläggen.
- S-0627, C-0811, A-3097 och en checksummad strukturerad MCP-observation
  bevarar frågor, kontrollresultat och tolkningsgräns.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0336. Ingen
  person, relation, läsesals-/kopiebeställning, webbläsarsession, PDF,
  deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 578 påståenden, 525 föräldralänkar, 1 956
  Markdownposter och 4 323 mediafiler inklusive `.gitkeep`. Manifestet har
  4 322 poster: 2 523 exakt, 1 771 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 77,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-/observations-/
  dashboard-JSON, dashboardtest, produktionsbygge, ny hel- och
  detaljrendering av den oförändrade 20-sidiga A4-utgåvan, metadata-, text-
  och teckengränskontroller, observationens SHA-256 och `git diff --check`
  passerade. De väntat icke-nollande auditerna visar tio ogiltiga
  slutstatusar genom P-0004:s djup 5 med P-0051 som nästa tillåtna
  arbetsdjup och exakt P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-03 — batch 221

- Riksarkivets globalt konfigurerade MCP användes först för P-0051:s
  olösta födelse- och föräldrafråga. DDS Födelse gav noll för Barbro/Cajsa
  i Bygdeå och Lövånger 1830; DDS Vigsel gav noll för Olof Pehrsson och
  Maja Stina Pehrsdotter i Bygdeå 1810.
- Kända positiva lokala kontroller, vanliga namn och länsvida
  Västerbottenkontroller gav också noll, medan samtidiga nationella
  tjänstekontroller gav 1 151 födelseposter och 130 vigselposter. Utfallet
  är därför ett DDS-täckningshinder, inte ett nytt person-, födelse-,
  vigsel-, vistelse- eller föräldranoll.
- S-0626, C-0810, A-3096 och en checksummad strukturerad MCP-observation
  bevarar frågor, kontrollresultat och tolkningsgräns. Tidigare
  originallästa belägg och konflikter står oförändrade.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0133. Ingen
  person, relation, läsesals-/kopiebeställning, webbläsarsession, PDF,
  deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 577 påståenden, 525 föräldralänkar, 1 954
  Markdownposter och 4 322 mediafiler inklusive `.gitkeep`. Manifestet har
  4 321 poster: 2 522 exakt, 1 771 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 77,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-/observations-/
  dashboard-JSON, dashboardtest, produktionsbygge, oförändrad 20-sidig
  utgåva, observationens SHA-256 och `git diff --check` passerade. De
  väntat icke-nollande auditerna visar tio ogiltiga slutstatusar genom
  P-0004:s djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt
  P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 220

- Den tidigare oprövade Sollentuna-källan 1920 öppnade i ägarens inloggade
  Riksarkivet-Chrome utan ny CAPTCHA/ALTCHA. Records gav WAF-HTML och
  JSON-LD gav HTTP 403, men två officiella IIIF-manifest identifierar
  `SE/RA/420401/10/H 1 AA/13`, permanent id
  `oteW3OgRrH6d0G02H087k3`, och reproduktionerna `A0056304`/`C0301345`.
- I `A0056304` är hela Sollentunaföljden de 46 källbilderna
  `_00294`–`_00339`, sida 1–90; `_00340` börjar Lovö sida 1. Den alternativa
  reproduktionen börjar Sollentuna på `C0301345_00589` och Lovö på
  `_00681`.
- Alla 46 fulloriginal hämtades genom den signerade visaren. Två Apple
  Vision-OCR-pass på observerad M4 Max/arm64, varav ett över 276 separata
  namn-/yrkesfält, nominerade fem fulloriginal som avvisades visuellt som
  andra namn, födelseprofiler eller yrken. Ingen säker Olaus Fredberg-rad
  återfanns.
- S-0625, C-0809 och A-3094–A-3095 samt båda manifesten, OCR-kandidatfil,
  observation, fem kandidatkopior, tre gränskopior och samtliga 46
  screenade fulloriginal finns i projektet. Nästa session behöver inte
  Chrome, `Downloads` eller chattens historik för batchen. Screeningen är
  inte en visuell namn-för-namn-läsning och inte ett person-, vistelse-,
  församlings-, årgångs- eller helreproduktionsnoll. Upprepa bara med ny
  adress-, gårds-, sida-, familjemedlems- eller yrkesnyckel.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0051. Ingen
  läsesals-/kopiebeställning, PDF, deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 576 påståenden, 525 föräldralänkar, 1 951
  Markdownposter och 4 321 mediafiler inklusive `.gitkeep`. Manifestet har
  4 320 poster: 2 521 exakt, 1 771 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 77,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-/observations-/
  dashboard-JSON, dashboardtest, produktionsbygge, oförändrad 20-sidig
  utgåva och `git diff --check` passerade. De förväntat icke-nollande
  auditerna visar tio ogiltiga slutstatusar genom P-0004:s djup 5 med
  P-0051 som nästa tillåtna arbetsdjup och exakt P-0336 öppen genom
  P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 219

- SCB:s tidigare oprövade församlingsboksutdrag för Helgesta 1920 öppnade i
  inloggad Riksarkivet-Chrome utan ny CAPTCHA/ALTCHA. IIIF-manifestets range
  och fulloriginalen avgränsar Helgesta sida 1–31 till
  `A0056311_00782`–`_00812`; bild 813 börjar Hyltinge. Ingen sessionsdata
  eller beställning rördes.
- Tre Apple Vision-OCR-pass över de 31 navigationsbilderna nominerade tre
  namnformer och två `51`-liknande former. Fem fulloriginal visar andra
  hushåll eller bokförings-/anmärkningsformer, inte en säker Erik
  Karlsson/Carlsson eller Grill född 1851.
- S-0624, C-0808 och A-3092–A-3093 samt tio sakmedier bevarar utfallet.
  Screenen är inte en visuell namn-för-namn-läsning och inte ett person-,
  vistelse-, församlings-, årgångs- eller helreproduktionsnoll. Ingen person
  eller relation skapades. Upprepa endast med ny gårds-, hushålls-, sido-
  eller yrkesnyckel. T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation
  är P-0336. Ingen PDF, deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 574 påståenden, 525 föräldralänkar, 1 949
  Markdownposter och 4 263 mediafiler inklusive `.gitkeep`. Manifestet har
  4 262 poster: 2 508 exakt, 1 726 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, oförändrad 20-sidig utgåva, tio nya
  mediekontrollsummor och `git diff --check` passerade. De förväntat
  icke-nollande auditerna visar tio ogiltiga slutstatusar genom P-0004:s
  djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt P-0336 öppen
  genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 218

- P-0051:s tidigare oprövade sociala route Bygdeå K I/2 öppnade i den
  inloggade katalogen utan ny CAPTCHA/ALTCHA efter att records-API och OAI
  gett WAF/403. Publik IIIF gav reproduktion `A0017300` med 393 bildytor
  utan interna strukturer. Ingen kontroll, sessionsdata eller beställning
  rördes.
- Nio fattigbarnslistor för 1838–1843 och 1845–1847 lästes visuellt i
  maximaloriginal. Ingen uttrycklig Barbro/Barbru Cajsa Olofsdotter eller
  entydig 1830-02-24-profil finns i namnkolumnerna; någon exponerad
  1844-lista identifierades inte.
- Apple Vision-OCR över alla 393 navigationsbilder nominerade fyra övriga
  sidor som avvisades visuellt i maximaloriginal. OCR är endast navigation
  och kan missa handskrift; resultatet är inte ett person-, vistelse-,
  understöds-, föräldra- eller helvolymsnoll.
- S-0623, C-0807 och A-3089–A-3091 samt sexton sakmedier bevarar utfallet.
  Ingen person eller relation skapades. Återta K I/2 endast med ny riktad
  nyckel; H III/1, H I/1 och L III/1 förblir direkta analoga vägar och J/4
  kräver en faktisk bilagehänvisning. T-0012 förblir `ONGOING`/`DOING`;
  nästa breddrotation är P-0133. Ingen PDF, deployment, commit eller push
  skapades.
- Verifiering: 500 personer, 2 572 påståenden, 525 föräldralänkar, 1 947
  Markdownposter och 4 253 mediafiler inklusive `.gitkeep`. Manifestet har
  4 252 poster: 2 498 exakt, 1 726 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, oförändrad 20-sidig utgåva, sexton nya
  mediekontrollsummor och `git diff --check` passerade. De förväntat
  icke-nollande auditerna visar tio ogiltiga slutstatusar genom P-0004:s
  djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt P-0336 öppen
  genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 217

- P-0336:s förbisedda folkräkningslucka 1900 är fylld mellan de redan lästa
  åren 1890 och 1910. `Folk_117700509`–`Folk_117700515` och originalbild
  `Folk_001017-164` placerar den gifte stationskarlsförmannen Olaus med
  Johanna och barnen Frida, Augusta, Ester, Edit och Oskar i Jordgubben
  N:o 11, Kungsholm rote 17.
- Originalets födelseår är i radordning 1852, 1866, 1883, 1890, 1891, 1894
  och 1895. Edit står alltså född 1894 år 1900 men 1895 år 1910; Oskar står
  1895 redan 1900. Bevara konflikten och skapa inget tvillingpåstående.
- Barnens efternamn står inte i blocket och konstrueras inte. Frida är Olaus
  dotter, men denna källa ensam gör inte Johanna till hennes biologiska mor.
- Fyra records-API-frågor gav WAF/403. Inloggad katalog samt publikt
  IIIF-manifest, `info.json` och original fungerade utan ny CAPTCHA. Ingen
  kontroll, sessionsdata eller läsesals-/kopiebeställning rördes.
- S-0622, C-0806, A-2999–A-3002 och A-3085–A-3088 bevarar resultatet. Ingen
  person eller relation skapades. Olaus föräldrar och hans två konkurrerande
  födelsedatum förblir öppna. T-0012 är fortsatt `ONGOING`/`DOING`; nästa
  breddrotation är P-0051. Ingen PDF, deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 569 påståenden, 525 föräldralänkar, 1 945
  Markdownposter och 4 237 mediafiler inklusive `.gitkeep`. Manifestet har
  4 236 poster: 2 482 exakt, 1 726 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, fyra kontrollsummor och `git diff --check`
  passerade. De förväntat icke-nollande auditerna visar tio ogiltiga
  slutstatusar genom P-0004:s djup 5 med P-0051 som nästa tillåtna
  arbetsdjup och exakt P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 216

- P-0133:s återstående källfamiljer auditerades utan omläsning av de slutna
  kyrkoboks-, folkräknings-, flytt-, vigsel-, döds-, boupptecknings- eller
  fattigvårdsvägarna. Den nya familjen är kommunala mantals-, debiterings-
  och uppbördslängder.
- Forssa kommunalnämnds G 4/1, 1863–1893, och G 4/2, 1894–1909, är två
  exakt itemiserade volymer som katalogmässigt täcker Eriks kända
  Forssaperiod 1876–1895.
- Helgesta kommunalnämnds D 2:1 har uttryckliga mantalshäften för 1910 och
  1916–1917. G 4 B/2–3 samt årshäftena G 4 B/4–11 bildar en exakt
  uppbördsroute 1910–1935.
- Flen-kontrollen gav endast allmänna räkenskaper 1894–1912 och separat
  avgränsade municipalsamhällesserier som inte är bundna till Eriks gårdar.
  Detta är inget person-, vistelse- eller Flen-noll.
- Sex records-API-frågor och fyra OAI- plus fyra JSON-LD-omprov gav 403.
  Den inloggade katalogen öppnade alla tretton exakta Forssa-/
  Helgestavolymerna utan ny CAPTCHA, men ingen hade synlig `Bild`- eller
  `Läsesal`-länk. Ingen kontroll, sessionsdata eller beställning rördes.
- S-0621, C-0805, A-3082–A-3084 och en strukturerad observation bevarar
  resultatet. Ingen person eller relation skapades. T-0012 förblir
  `ONGOING`/`DOING`; nästa breddrotation är P-0336. Ingen PDF, deployment,
  commit eller push skapades.
- Verifiering: 500 personer, 2 565 påståenden, 525 föräldralänkar, 1 943
  Markdownposter och 4 233 mediafiler inklusive `.gitkeep`. Manifestet har
  4 232 poster: 2 478 exakt, 1 726 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, kontrollsumma och `git diff --check`
  passerade. De förväntat icke-nollande auditerna visar tio ogiltiga
  slutstatusar genom P-0004:s djup 5 med P-0051 som nästa tillåtna
  arbetsdjup och exakt P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 215

- P-0051:s återstående källfamiljer auditerades utan omläsning av de slutna
  kyrkoboks-, flytt-, fattigvårds-, mantals- eller Piteåintervallen. Den
  starkaste oprövade vägen var domstolshandlingar kring en utomäktenskaplig
  börd 1830.
- Bygdeå tingslags häradsrätt A I a/41 är ordinarie dombok 1830, A I b/5
  urtima domböcker och protokoll 1819–1830 och A II/10 småprotokoll
  1830–1834. Alla tre exakta JSON-LD-poster anger analog representation.
- Svea hovrätts renoverade kopior ger E XI e/4118–4119, de två
  Västerbottenvolymerna 1830, och E XII b/384–390, sju registerlösa
  småprotokollsdelar för samma år. Alla nio är analoga; katalogen mappar inte
  Bygdeå till en bestämd volym eller del.
- Bygdeå C II:s särskilda förmynderskapsböcker börjar först 1867. Det är ett
  serie-/tidsomfångsresultat och utesluter inte äldre förmynderskaps-,
  faderskaps- eller underhållsärenden i dombok eller småprotokoll.
- Den inloggade Chrome-sessionen visade ingen ny CAPTCHA/ALTCHA, men de
  exakta lokala och renoverade provposterna visade bara `Läsesal` utan
  bildlänk. Ingen kontroll, sessionsdata eller beställning rördes. Ingen
  rättshandling eller personrad lästes och inget mål- eller personnoll
  skapades.
- S-0620, C-0804, A-3079–A-3081 och nio metadata-/observationsfiler bevarar
  resultatet. Ingen person eller relation skapades. T-0012 förblir
  `ONGOING`/`DOING`; nästa breddrotation är P-0133. Ingen PDF, deployment,
  commit eller push skapades.
- Verifiering: 500 personer, 2 562 påståenden, 525 föräldralänkar, 1 941
  Markdownposter och 4 232 mediafiler inklusive `.gitkeep`. Manifestet har
  4 231 poster: 2 477 exakt, 1 726 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, kontrollsummor och `git diff --check`
  passerade. De förväntat icke-nollande auditerna visar tio ogiltiga
  slutstatusar genom P-0004:s djup 5 med P-0051 som nästa tillåtna
  arbetsdjup och exakt P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 214

- Riksarkivets inloggade rikssökning `Olaus Fredriksson` gav 153 synliga
  träffar. De två träffarna under företag och arbetsliv gäller samme ogifte
  jungman, född 1852, med födelse- och hemförsamling Torhamn i Blekinge,
  inskrivningsnummer 272 vid Karlskrona sjömanshus.
- De officiella sjömanshusraderna beskriver påmönstringar på *Gustaf Wasa*
  1874-07-20 och *Frithiof* 1875-04-16. Karlskrona D I a/1 och det
  inskrivningsnummerordnade D I d/14 visar endast `Läsesal`; E VI:s
  inskrivningshandlingar och E VII:s prästbetyg är enligt katalogen gallrade
  i sin helhet. Ingen analog personrad beställdes eller lästes.
- Torhamn C I/5:s kompletta födelseår 1852 är IIIF-bilderna
  `C0058822_00325`–`_00331`, med föregående årsgräns på bild 324 och nästa
  år på bild 331. Alla sju bildytor lästes visuellt. Året saknar Olaus på
  både 24 maj och 4 september; andra Olaus-poster på andra datum hindrar ett
  allmänt namn- eller personnoll.
- Sjömannen nr 272 avvisas som P-0336 genom de två Torhamnfälten,
  målpersonens positiva Lundby–Fågelvik–Alnö-kedja och de två exakta
  datumnollen. Avvisningen betyder inte att P-0336 aldrig arbetade till sjöss.
- S-0619, C-0803, A-3075–A-3078, två filtrerade registerrader, ett
  IIIF-manifest, åtta originalbilder och en strukturerad observation bevarar
  resultatet. Ingen person eller relation skapades. Föräldrarna och
  födelsedatumskonflikten förblir öppna. T-0012 är fortsatt
  `ONGOING`/`DOING`; nästa breddrotation är P-0051. Ingen PDF, deployment,
  commit eller push skapades.
- Verifiering: 500 personer, 2 559 påståenden, 525 föräldralänkar, 1 939
  Markdownposter och 4 223 mediafiler inklusive `.gitkeep`. Manifestet har
  4 222 poster: 2 468 exakt, 1 726 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, kontrollsummor och `git diff --check`
  passerade. De förväntat icke-nollande auditerna visar tio ogiltiga
  slutstatusar genom P-0004:s djup 5 med P-0051 som nästa tillåtna
  arbetsdjup och exakt P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 213

- P-0133:s återstående biografiska källfamiljer auditerades utan omläsning av
  slutna kyrkoboks-, folkräknings-, flytt-, vigsel-, död- eller
  bouppteckningsvägar. Riksarkivets inloggade katalog identifierar
  *HELGESTA KOMMUN (1863–1951). FATTIGVÅRDSNÄMNDEN*,
  `SE/D002/FKG_162-1`, 1808–1951, 38 volymer hos Flens kommunarkiv.
- D 2:1, understödsförteckning 1923–1936, är första personförda originalroute
  över Eriks sena understöds-/institutionsperiod. A 1:1, protokoll 1909–1936,
  och G 5:1, understödsjournal 1929, är hänvisningsstyrda komplement.
- D 3:1:s intagningsförteckning omfattar endast 1950–1952, D 1:1 börjar 1937
  och F 1:1:s katalogiserade personförda fattigliggare slutar 1916. Dessa är
  serie-/tidsomfångsresultat, inte person-, intagnings-, understöds- eller
  anhörignoll.
- Records-API och OAI gav HTTP 403; katalogposterna exponerar ingen digital
  bild eller reproduktion. Ingen Erik-post kunde fjärrläsas och ingen ny
  CAPTCHA, sessionsdata eller beställning rördes. S-0618, C-0802,
  A-3073–A-3074 och en strukturerad observation bevarar resultatet. T-0012
  förblir `ONGOING`/`DOING`; nästa breddrotation är P-0336. Ingen PDF,
  deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 555 påståenden, 525 föräldralänkar, 1 937
  Markdownposter och 4 212 mediafiler inklusive `.gitkeep`. Manifestet har
  4 211 poster: 2 457 exakt, 1 726 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, kontrollsumma och `git diff --check`
  passerade. De förväntat icke-nollande auditerna visar tio ogiltiga
  slutstatusar genom P-0004:s djup 5 med P-0051 som nästa tillåtna
  arbetsdjup och exakt P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 212

- P-0051:s öppna källfamiljer auditerades utan att de slutna kyrkoboks-,
  flytt-, fattigvårds- eller Piteåintervallen lästes om. Fondens OAI-EAD och
  den inloggade katalogen identifierar Umeå fögderi Vol/38, 1830–1842, och
  Vol/39, 1843–1850, som de exakta mantalsvolymerna `för Bygdeå socken.`
- Båda volymerna visar endast `Läsesal`, ingen bildlänk; deras exakta
  `Tree/SubTree`-vägar är tomma. Publika records-/OAI-omprov gav 403, men
  katalogen öppnade utan ny CAPTCHA. Ingen kontroll, sessionsdata eller
  beställning rördes.
- En fokuserad digital sökning visar att de 195 digitala registerträffarna
  tillhör *Mantalslängder 1642–1820*. Målperioden 1830–1850 täcks inte där.
  Ingen mantalsrad eller person lästes och inget närvaro-, frånvaro-,
  vistelse-, födelse- eller föräldranoll skapades. H III/1 förblir första
  födelsenära analoga väg; Vol/38–39 är kompletterande hushålls-/skattevägar.
- S-0617, C-0801, A-3072 och en strukturerad observation bevarar resultatet.
  T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0133. Ingen
  PDF, deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 553 påståenden, 525 föräldralänkar, 1 935
  Markdownposter och 4 211 mediafiler inklusive `.gitkeep`. Manifestet har
  4 210 poster: 2 456 exakt, 1 726 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardtest, produktionsbygge, kontrollsumma och `git diff --check`
  passerade. De förväntat icke-nollande auditerna visar tio ogiltiga
  slutstatusar genom P-0004:s djup 5 med P-0051 som nästa tillåtna
  arbetsdjup och exakt P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 211

- Efter ägarens besked om aktiv inloggning och besvarad kontroll kördes tre
  tidigare spärrade Riksarkivet-vägar om utan ny CAPTCHA och utan läsning av
  sessionsdata. Indelningsverkets exakta Hagby/Bettna-formfråga gav 0
  träffar endast inom frågefältsomfånget; globalsökningen `Olof Pehrsson
  Bygdeå` gav 22 huvudsakligen sena träffar och inget personnoll.
- Folkräkningen 1890, `Folk_111631011`, återfinner Olaus Fredberg som
  stationskarlsförman i Jordgubben 1–5 på Kungsholm med Johanna Charlotta
  Janson och sex namngivna barn. Originalbilden är bevarad i C-0800.
- Helgesta B/4:s originalreproduktion `00154377` öppnades. Post 1 på bild
  62 visar Erik Karlsson med hustru och ett barn från Flen, registrerade
  1909-01-22 till sida 313. Flen A II a/3 c:s utflyttning är 1909-01-18;
  den tidigare november-/samma-dagstolkningen är rättad till fyra dagar.
- Halla C/2:s tidigare helårsnoll var fel. Bild 82 visar Carl Fredrik född
  1822-04-09 och döpt 12/4 i Lilla Wättstugan som pigan Ella Ersdotters
  utomäktenskaplige son. P-0500 skapas som säker mor; ingen far skapas ur
  patronymikonet Pehrsson. Jernbol-attesterna 1840 och A I/13 b sida 121
  fyller samtidigt den tidiga tjänstekedjan.
- S-0614–S-0616, C-0798–C-0800 och A-3061–A-3071 bevarar batchen. Ingen
  beställning, PDF, deployment, commit eller push skapades.
- Verifiering: 500 personer, 2 552 påståenden, 525 föräldralänkar, 1 933
  Markdownposter och 4 210 mediafiler inklusive `.gitkeep`. Manifestet har
  4 209 poster: 2 454 exakt, 1 727 källavgränsade, 28 citationsavgränsade
  och 0 olänkade. Parser-/datatester 5/5, pedigree 77, djup-5-paket,
  utgåvemanifest, projekt-/Wotan-/manifest-/observations-/dashboard-JSON,
  dashboardens produktionsbygge och `git diff --check` passerade. De
  förväntat icke-nollande auditerna visar tio ogiltiga slutstatusar genom
  P-0004:s djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt P-0336
  öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 210

- Batch 210 är bevarad i repositoryt: S-0613, C-0797, A-3060, P-0336,
  forskningsfront, källtäckning, forskningsplan, forskningslogg,
  Wotan-logg, sex fulloriginal och en härledd 908-radig OCR-fil.
- Stora Lundby H II/1:s reproduktion `A0062259` har 908 bildytor. Samtliga
  screenades som 1 600-pixlars IIIF-navigationskopior; OCR användes endast
  för kandidatnavigation och är inte original eller transkription.
- Sex relevanta namnkandidater lästes i fulloriginal och avvisades genom
  andra patronymikon och/eller födelsedatum 1820–1843. Ingen person eller
  relation skapades.
- Utfallet är en fullreproduktionsomfattande maskinassisterad
  namnformsscreening, inte en visuell fullvolymsläsning eller ett person-,
  familje-, årgångs-, vistelse- eller församlingsnoll. Upprepa inte blind
  OCR utan ny dokument-, datum-, gårds- eller flyttnyckel.
- Den verkliga Chrome-sessionen var inloggad men fick efter omladdning en
  ny ALTCHA. Agenten rörde inte kontrollen eller sessionsdata; publik IIIF
  bar originalarbetet och ingen beställning gjordes.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0474–P-0475.
  Ingen beställning, PDF, deployment, commit eller push skapades.
- Verifiering: 499 personer, 2 541 påståenden, 524 föräldralänkar, 1 926
  Markdownposter och 4 190 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 4 189 poster: 2 449 exakt, 1 712 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 76,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-JSON,
  dashboard-build och `git diff --check` passerade. Ingen PDF skapades
  eller verifierades. Auditerna visar fortsatt elva ogiltiga slutstatusar
  genom P-0004:s djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt
  P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 209

- Batch 209 är bevarad i repositoryt: S-0612, C-0796, A-3053–A-3059,
  P-0133, P-0135–P-0137, forskningsfront, källtäckning, forskningsplan,
  forskningslogg, Wotan-logg, tio maximaloriginal, åtta metadataoriginal
  och ett strukturerat observationsoriginal.
- Flen A II a/2 a följer Erik, Matilda, Sven Arvid och Karl Oskar från
  Brosätter sida 216 till Segerslund sida 185 år 1907. A II a/3 c följer
  Erik, Matilda och Sven Arvid sida 224 → Wäsby sida 255 år 1908 och anger
  Helgesta 1909-01-18. Karl Oskars frånvaro är bara sid- och
  hushållsbunden.
- Helgesta A II a/2 sida 313 ger samma hushåll från Flen 1909-01-22
  och hänvisar till Vilhelmsro sida 315. Det är en fyra dagar senare
  registrerad ankomst, inte ett reciprokpar samma dag. Detta fyller luckan till 1910 och
  gör A II a/3 sida 346 till ett senare sidnoll, inte en motsägelse.
- Helgesta B/4:s originalreproduktion `00154377` är nu öppnad och post 1
  på bild 62 bekräftar Erik Karlsson med hustru och ett barn från Flen,
  ankomna 1909-01-22 till sida 313. Den äldre mikrofilmsreproduktionen
  `F0003391` bevaras som separat representation. Ingen beställning gjordes.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0336. Ingen
  person, biologisk relation, beställning, PDF, deployment, commit eller
  push skapades.
- Verifiering: 499 personer, 2 540 påståenden, 524 föräldralänkar, 1 924
  Markdownposter och 4 183 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 4 182 poster: 2 442 exakt, 1 712 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 76,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-/observations-JSON,
  dashboard-build och `git diff --check` passerade. Ingen PDF skapades
  eller verifierades. Auditerna visar fortsatt elva ogiltiga slutstatusar
  genom P-0004:s djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt
  P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 208

- Batch 208 är bevarad i repositoryt: S-0611, C-0795, A-3050–A-3052,
  P-0051, forskningsfront, källtäckning, forskningsplan, forskningslogg,
  Wotan-logg, 65 maximaloriginal och ett strukturerat observationsoriginal.
- Bygdeå C/3:s fulla exponerade födelseföljd 1811–1820, bilderna
  `C0034039_00166`–`_00214`, saknar en säker barnpost med Olof Pehrsson och
  Maja Stina Pehrsdotter som föräldrar. Bilderna 212 och 213 visar samma
  sidetikett 384 men är separata originalexponeringar med olika checksummor
  och bevaras båda.
- Den fulla exponerade död- och begravningsföljden 1811–1829, bilderna
  `_00345`–`_00360`, saknar en säker dödsrad för paret. En nybyggare Olof
  Pehrsson, 76 år, i december 1820 avvisas som Olaus född 1784-02-07; det
  svårlästa ortnamnet transkriberas inte.
- Båda nollen är strikt volym-/serie-/tids-/bild-/namn-/profilbundna med
  C/3:s `Defekt`-reservation. De bevisar inte barnlöshet, vistelse,
  överlevnad, identitet, föräldraskap eller frånvaro i annan församling.
- Efter ägarens besked om inloggning och egen CAPTCHA-lösning bekräftade den
  synliga Chrome-vyn aktiv inloggning, men en snäv Olof Pehrsson-/Bygdeå-
  fråga gav omedelbart en ny ALTCHA före resultat. Agenten rörde inte
  kontrollen eller sessionsdata; publik IIIF gav originalen. Ingen
  beställning gjordes.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0133. Ingen
  person, sammanslagning, relation, beställning, PDF, deployment, commit
  eller push skapades.
- Verifiering: 499 personer, 2 533 påståenden, 524 föräldralänkar, 1 922
  Markdownposter och 4 164 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 4 163 poster: 2 423 exakt, 1 712 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 76,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-/observations-JSON,
  dashboard-build och `git diff --check` passerade. Ingen PDF skapades
  eller verifierades. Auditerna visar fortsatt elva ogiltiga slutstatusar
  genom P-0004:s djup 5 med P-0051 som nästa tillåtna arbetsdjup och exakt
  P-0336 öppen genom P-0210:s djup 4.

## Sessionscheckpoint 2026-09-02 — batch 207

- Batch 207 är bevarad i repositoryt: uppdaterade S-0116 och S-0565,
  C-0794, A-3041–A-3049, P-0494–P-0499, relationerna i P-0133 och
  P-0474–P-0475, forskningsfront, källtäckning, forskningsplan,
  forskningslogg, Wotan-logg, sex fulloriginal och ett IIIF-manifest.
- Bettna C/5 bild 35 visar Anna Lotta född 1846-01-14 och döpt 18/1 i
  Glippsta soldattorp med soldaten Carl Eric Grill och Johanna Jonsdotter.
  Bettna C/6 bild 9 visar Maria Sofia född 1863-03-27 med soldaten Carl
  Fredric Drill och Johanna Jonsdotter. Båda positiva posterna
  sammanfaller med hushållskedjan.
- C/5:s exakta följder över Lovisas 1849-02-27 och den SCB-ledda
  alternativdagen 1848-02-27, Johanna Mathildas 1854-04-21 samt Heddas
  1858-11-22 saknar säker målpost eller familjeprofil. De är strikt
  bild-/datumfönster-/namn-/profilbundna konflikter och upphäver inte de
  uttryckliga hushållsrelationerna.
- Carl Johan P-0494 har Johanna som originalbelagd mor och tomt
  fadersfält. Carl Fredrik är endast styv-/hushållsfar; ingen biologisk
  relation skapades. P-0495–P-0499 bevarar de fem döttrarna med
  positiva relationer och oförändrade källkonflikter.
- Publik IIIF fungerade med Riksarkivets bildvisare som `Referer`; den
  inloggade Chrome-sessionen behövde inte användas. Ingen CAPTCHA/ALTCHA
  eller sessionsdata rördes och ingen beställning skapades.
- Verifiering: 499 personer, 2 530 påståenden, 524 föräldralänkar, 1 920
  Markdownposter och 4 098 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 4 097 poster: 2 415 exakt, 1 654 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree
  76, djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-JSON,
  dashboard-build och `git diff --check` passerade. Ingen PDF skapades
  eller verifierades. Auditerna visar fortsatt elva ogiltiga slutstatusar
  genom P-0004:s djup 5 och exakt P-0336 öppen genom P-0210:s djup 4.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0051. Ingen
  beställning, PDF, deployment, commit eller push skapades.

## Sessionscheckpoint 2026-09-02 — batch 206

- Batch 206 är bevarad i repositoryt: S-0610, C-0793,
  A-3037–A-3040, P-0474, forskningsfront, källtäckning, forskningsplan,
  forskningslogg, Wotan-logg, sex maximaloriginal, fjorton
  metadataoriginal och en strukturerad observation.
- Livkompaniets rekryteringsrulla 1840-12-31 visar nr 36/36 Glippsta,
  `Carl Fredrik Drill`, lejd av rote 142 Bokulla, Sörmland, det
  rättade/överskrivna årsfältet 1822, 5 fot 10 tum och ogift.
  Anmärkningen börjar `Approberas` och har säker datering 1841-02-15;
  GMR 1842:s 1841-02-18 bevaras separat.
- En tillhörande lapp 1840-12-22 skriver `Drängen Carl Drill` och är
  undertecknad Anders Andersson. Den delvis oläsliga fortsättningen bär
  inga påståenden. Bokulla sida 90 i Björkvik A I/13 b och A I/14 b
  saknar säker målrad: två strikta volym-/period-/plats-/sidnoll, inte
  person- eller vistelsenoll. Bokulla görs inte till bostadsort.
- Hagby/Bettna-frågan kördes om efter ägarens besked men fick en ny
  synlig verifiering före resultat. Ingen CAPTCHA/ALTCHA eller sessionsdata
  rördes. Publika Riksarkivet-API-/JSON-LD-/träd-/IIIF-vägar gav
  originalen; ingen beställning skapades.
- Verifiering: 493 personer, 2 521 påståenden, 513 föräldralänkar, 1 913
  Markdownposter och 4 091 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 4 090 poster: 2 409 exakt, 1 653 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree
  76, djup-5-paket, utgåvemanifest, projekt-/Wotan-/manifest-JSON,
  dashboard-build och `git diff --check` passerade. Ingen PDF skapades
  eller verifierades. Auditerna visar fortsatt elva ogiltiga slutstatusar
  genom P-0004:s djup 5 och exakt P-0336 öppen genom P-0210:s djup 4.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0475. Ingen
  person, relation, beställning, PDF, deployment, commit eller push
  skapades.

## Sessionscheckpoint 2026-09-02 — batch 205

- Batch 205 är bevarad i repositoryt: S-0609, C-0792, A-3036, P-0336,
  forskningsfront, källtäckning, forskningsplan, forskningslogg,
  Wotan-logg, fyra läskopior, två IIIF-manifest, ett records-API-resultat
  och en strukturerad observation.
- A II a/8:s ortregister routar Tureberg till A II a/9 bilderna 157–189,
  uppslag 406–423 och 425–439. Samtliga 33 exponerade bilder saknar en
  säker Olaus/Olof Fredberg/Fredriksson-, Johanna Charlotta Jansson- eller
  målprofilsrad. Resultatet är ett exakt käll-/volym-/tids-/ortregister-/
  bildintervall-/namn-/profilnoll, inte ett person-, vistelse- eller
  dödsortsnoll.
- Dödbokens `1338` ligger i de statistiska räknekolumnernas slutsummering
  och är inte en sida i A II a/12. Bilderna lästes i ägarens redan
  inloggade Chrome utan att någon CAPTCHA visades eller hanterades och
  utan läsning av sessionsdata. Ingen beställning gjordes.
- Verifiering: 493 personer, 2 517 påståenden, 513 föräldralänkar, 1 911
  Markdownposter och 4 070 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 4 069 poster: 2 403 exakt, 1 638 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree
  76, djup-5-paket, utgåvemanifest, projekt-/Wotan-JSON,
  manifest/checksummor, dashboard-build, oförändrad 20-sidors-PDF och
  `git diff --check` passerade. De avsiktligt icke-nollande auditerna visar
  elva ogiltiga slutstatusar genom P-0004:s djup 5 och exakt P-0336 öppen
  genom P-0210:s djup 4.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0474. Ingen
  person, relation, beställning, PDF, deployment, commit eller push
  skapades.

## Sessionscheckpoint 2026-09-02 — batch 204

- Batch 204 är bevarad i repositoryt: S-0608, C-0788–C-0791,
  A-3030–A-3035, omläsningen av C-0579, P-0213, forskningsfront,
  källtäckning, forskningsplan, forskningslogg, Wotan-logg, 76 lästa
  originalbilder och tio metadata-/observationsfiler.
- Flen B/4 utflyttade post 115 visar dottern Maria Sofia Eriksson från
  Bergatorp, folio 281, till endast `Mellösa` 1899-11-10. Posten tillför
  efternamnsformen `Eriksson` men avgör inte om Lilla eller Stora Mellösa
  var faktisk destination.
- Lilla Mellösa B/3 inflyttade 1899 poster 1–150 och utflyttade 1900
  poster 1–149, hela folkräkningen 1900 med 55 bilder samt Stora Mellösa
  B/6 inflyttade 1899 poster 1–126 följda av tom sida saknar målprofilen.
  Detta är fyra separata volym-/registerår-/post- eller
  bildföljd-/namn-/profilnoll, inte person-, vistelse-, destinations- eller
  generella församlingsnoll.
- De tidigare missade rutterna kördes om efter ägarens besked i inloggad
  extern Chrome. Tre nya ALTCHA visades och lämnades orörda; inga
  sessionsdata lästes. Publik JSON-LD/IIIF gav originalen, medan nya
  data-API-anrop mötte WAF. Ingen beställning gjordes.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0336 Olaus
  Fredberg. Ingen person, relation, PDF, deployment, commit eller push
  skapades.
- Verifiering: 493 personer, 2 516 påståenden, 513 föräldralänkar, 1 909
  Markdownposter och 4 062 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 4 061 poster: 2 399 exakt, 1 634 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 76,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-JSON,
  manifest/checksummor, dashboard-build och oförändrad 20-sidors-PDF
  passerade. De två avsiktligt icke-nollande auditerna visar fortsatt elva
  ogiltiga slutstatusar genom P-0004:s djup 5 och exakt P-0336 öppen genom
  P-0210:s djup 4. `git diff --check` passerade.

## Sessionscheckpoint 2026-09-02 — batch 203

- Batch 203 är bevarad i repositoryt: S-0607, C-0785–C-0787,
  A-3027–A-3029, rättelsen av C-0579/A-2513, P-0015, forskningsfront,
  källtäckning, forskningsplan, forskningslogg, Wotan-logg, nio nya
  Sköldinge-maxoriginal med nio Image API-infofiler, nio autentiserat
  hämtade Hyltinge-fulloriginal, ett Flen-maxoriginal med Image API-info,
  tre källmetadatafiler och en strukturerad observation.
- Sköldinge B/6 inflyttade 1897 är komplett genom posterna 1–175 utan
  målprofil. Hyltinge B/4 inflyttade 1897 poster 1–81 och utflyttade 1898
  poster 1–75 saknar den också. Detta är tre separata
  volym-/år-/postföljd-/namn-/profilnoll och inte person- eller
  vistelsenoll.
- Flen B/4 inflyttade post 85 visar sonen Axel Edvard Eriksson från
  Hyltinge till Bergatorp, folio 281, 1898-11-09. Den samtidiga posten
  rättar Flen A I/26:s fält till `Hyltinge 98 9/11 85`, inte det tidigare
  `21/11`. Hyltinges saknade motsvarighet bevaras som källucka utan att
  underkänna Flens positiva post.
- Hyltinge lästes och hämtades i ägarens inloggade externa Chrome;
  Sköldinge nåddes genom publik JSON-LD/IIIF. Direkt NAD/global sökning
  gav nya orörda ALTCHA. Ingen sessionsdata lästes och ingen beställning
  gjordes.
- Verifiering: 493 personer, 2 510 påståenden, 513 föräldralänkar, 1 904
  Markdownposter och 3 976 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 3 975 poster: 2 377 exakt, 1 570 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 76,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-JSON,
  manifest/checksummor, dashboard-build, oförändrad 20-sidors-PDF och
  `git diff --check` passerade. De två avsiktligt icke-nollande auditerna
  visar fortsatt elva ogiltiga slutstatusar genom P-0004:s djup 5 och
  exakt P-0336 öppen genom P-0210:s djup 4.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0213 Elli
  Maria Sofia. Ingen person, relation, beställning, PDF, deployment,
  commit eller push skapades.

## Sessionscheckpoint 2026-09-02 — batch 202

- Batch 202 är bevarad i repositoryt: S-0606, C-0783–C-0784,
  A-3024–A-3026, P-0143, P-0015, forskningsfront, källtäckning,
  forskningsplan, forskningslogg, Wotan-logg, 23 nya fulloriginal, 23
  Image API-infofiler och 18 metadata-/observationsfiler. Flen B/4 post 38
  visar Erik Arvid från Bergatorp, folio 281, till Stockholm
  1897-10-20; post 39 visar Axel Edvard till Sköldinge samma dag.
- Avgränsade E/Eriksson-sekvenser kring datumet i Hedvig Eleonora, Klara,
  Storkyrko-, Adolf Fredriks, Maria Magdalena, Kungsholms, Katarina,
  Johannes och Jakobs församlingar saknar Erik Arvids målprofil. Detta är
  nio separata volym-/namnsekvens-/datum-/profilnoll, inte ett Stockholm-,
  person-, vistelse- eller folkräkningsnoll. Finska, hov/garnison,
  odigitaliserade serier och senare vidareflyttning ingår inte.
- Records-API och officiella IIIF-manifest gav metadata och maxoriginal.
  Den exakta globala sökningen i inloggad extern Chrome gav en ny orörd
  ALTCHA. Ingen sessionsdata lästes och ingen beställning gjordes.
- Verifiering: 493 personer, 2 507 påståenden, 513 föräldralänkar, 1 900
  Markdownposter och 3 943 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 3 942 poster: 2 348 exakt, 1 566 källavgränsade, 28
  citationsavgränsade och 0 olänkade. Parser-/datatester 5/5, pedigree 76,
  djup-5-paket, utgåvemanifest, projekt-/Wotan-JSON,
  manifest/checksummor, dashboard-build, oförändrad 20-sidors-PDF och
  `git diff --check` passerade. De två avsiktligt icke-nollande auditerna
  visar fortsatt elva ogiltiga slutstatusar genom P-0004:s djup 5 och
  exakt P-0336 öppen genom P-0210:s djup 4.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0015 via
  Sköldinge 1897. Ingen person, beställning, PDF, deployment, commit eller
  push skapades.

## Äldre sessionscheckpoint 2026-09-02 — batch 201

- Batch 201 är bevarad i repositoryt: S-0605, C-0780–C-0782,
  A-3021–A-3023, P-0142, forskningsfront, källtäckning, forskningsplan,
  forskningslogg, Wotan-logg, åtta nya fulloriginal och åtta
  metadata-/observationsfiler. Forssa A I/18 sida 83 visar Anna Erika kvar
  under fadern, född 1877-01-23, med destination Sköldinge 1892.
- Forssa B/4 utflyttade post 26 säkrar `Eriksson, Anna Erika, dotter`,
  Svartgjötorp, folio 83, Sköldinge och datumet 1892-10-22. Sköldinge
  B/5:s fotograferade inflyttningsföljd 1892 börjar med post 6 och slutar
  med 243; målprofilen saknas där, men posterna 1–5 exponeras inte. Detta
  är endast ett exponerad postföljd-/namn-/ursprungsnoll och motsäger inte
  den positiva flytten.
- Direktbildvisarna fungerade i inloggad Chrome och publikt IIIF gav
  övriga original. Exakta Sköldinge-NAD-, kyrkoarkiv- och
  folkräkningsrutter gav nya orörda ALTCHA. Ingen sessionsdata lästes och
  ingen beställning gjordes.
- Verifiering: 493 personer, 2 504 påståenden, 513 föräldralänkar, 1 897
  Markdownposter och 3 879 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 3 878 poster: 2 325 exakt, 1 525
  källavgränsade, 28 citationsavgränsade och 0 olänkade. Parser-/datatester
  5/5, pedigree 76, djup-5-paket, utgåvemanifest, projekt-/Wotan-JSON,
  manifest/checksummor, dashboard-build, oförändrad 20-sidors-PDF och
  `git diff --check` passerade. De två avsiktligt icke-nollande auditerna
  visar fortsatt elva ogiltiga slutstatusar genom P-0004:s djup 5 och
  exakt P-0336 öppen genom P-0210:s djup 4.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0143. Ingen
  beställning, PDF, deployment, commit eller push skapades.

## Äldre sessionscheckpoint 2026-09-02 — batch 200

- Batch 200 är bevarad i repositoryt: S-0603–S-0604, C-0777–C-0779,
  A-3017–A-3020, P-0136, forskningsfront, källtäckning, forskningsplan,
  forskningslogg, Wotan-logg, fem nya fulloriginal, en härledd beskärning
  och elva metadata-/observationsfiler. Flen A II a/1 sida 349 anger
  `Kungl. Lifgard. t. häst` / Stockholm 1903-10-22.
- Flen B/4:s exakta 22-oktoberblock och följande 23-oktobergräns saknar
  målprofilen. Livgardets `C0055484` sidor 198–201 och 206–207 saknar den
  också i Eriksson-/Ersson- och Karl/Carl-avsnitten. Båda resultaten är
  strikt serie-/register-/avsnitts-/profilbundna och motsäger inte den
  positiva flyttnotisen.
- Riksarkivets metadata identifierar församling `018001984`, regementsarkiv
  `SE/KrA/0161` samt personalvolymerna `/019:Ö/D I/5` och
  `/020:Ö/D IV/4`. De saknar publik bildlänk; ingen beställning gjordes.
  Direktbildvisaren `C0055484` fungerade i inloggad Chrome. Topografi,
  folkräkning och den omkörda Grill-frågan gav nya orörda ALTCHA-rutor.
- Verifiering: 493 personer, 2 501 påståenden, 513 föräldralänkar, 1 893
  Markdownposter och 3 863 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 3 862 poster: 2 317 exakt, 1 517
  källavgränsade, 28 citationsavgränsade och 0 olänkade. Parser-/datatester
  5/5, pedigree 76, djup-5-paket, utgåvemanifest, projekt-/Wotan-JSON,
  manifest/checksummor, dashboard-build, oförändrad 20-sidors-PDF och
  `git diff --check` passerade. De två avsiktligt icke-nollande auditerna
  visar fortsatt elva ogiltiga slutstatusar genom P-0004:s djup 5 och
  exakt P-0336 öppen genom P-0210:s djup 4.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0142. Ingen
  beställning, PDF, deployment, commit eller push skapades.

## Äldre sessionscheckpoint 2026-09-02 — batch 199

- Batch 199 är bevarad i repositoryt: S-0602, C-0776, A-3009–A-3016,
  P-0051, forskningsfront, källtäckning, forskningsplan, forskningslogg,
  Wotan-logg, 112 lästa originalbilder och sex metadata-/observationsfiler.
  Bygdeå A I/6 sida 80 visar Nils Jonsson född 1775, hustrun Maja Stina
  född 1779 och döttrarna Anna Cajsa 1800/Maja Stina 1802. Hushållet är
  direkt transkriberat, men identiteten med 1799 års vigselpar är endast
  `LEAD`: patronymikon, säker marginalnot och fortsatt hushållsbrygga
  saknas. Ingen person, sammanslagning eller relation skapades.
- Hela A I/7a Överklinten sidorna 114–131, Bygdeå C/3:s födelseföljder
  1800/1802 och dödföljd 1799–1810 samt Umeå landsförsamling C/5:s alla
  38 födelsebilder 1800/1802 är lästa. Utfallet är endast strikt orts-,
  serie-, års- och bildintervallbundet, med C/3:s uttryckliga
  `Defekt`-/gleshetsreservation. Upprepa inte intervallen utan ny positiv
  nyckel.
- Den exakta Umeå-NAD-sidan visade en ny CAPTCHA trots aktiv inloggning och
  ägarens tidigare lösning; rutan lämnades orörd. Riksarkivets publika OAI-,
  arkivträds- och IIIF-route gav `C0034535` och originalen. Grill-fliken har
  fortsatt den förberedda frågan ort `Hagby`, socken `Bettna` och en synlig
  ALTCHA. Inget av åtkomstlägena är ett käll- eller registernoll.
- Verifiering: 493 personer, 2 497 påståenden, 513 föräldralänkar, 1 888
  Markdownposter och 3 846 mediafiler inklusive `.gitkeep`.
  Mediamanifestet har 3 845 poster: 2 300 exakt, 1 517
  källavgränsade, 28 citationsavgränsade och 0 olänkade. Parser-/datatester
  5/5, pedigree 76, djup-5-paket, utgåvemanifest, projekt-/Wotan-JSON,
  manifest/checksummor, dashboard-build, oförändrad 20-sidors-PDF och
  `git diff --check` passerade. De två avsiktligt icke-nollande auditerna
  visar fortsatt elva ogiltiga slutstatusar genom P-0004:s djup 5 och
  exakt P-0336 öppen genom P-0210:s djup 4.
- T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0133. Ingen
  beställning, PDF, deployment, commit eller push skapades.

## Äldre sessionscheckpoint 2026-09-01 — batch 198

- Batch 198 är bevarad i repositoryt: S-0601, C-0775, A-3004–A-3008,
  P-0133/P-0474–P-0475, forskningsfront, källtäckning, forskningsplan,
  forskningslogg, Wotan-logg, två maxoriginal, två Image API-infofiler och
  en strukturerad observation. A I/14 b:s register routar `Hagby` →
  `D:o Soldattorp` till sida 184; hela sidan saknar Grillfamiljens namn och
  profil, men är endast ett exakt sida-/platsrubriknoll. Den breda
  A I/14 a–b-screeningen bär fortsatt inget noll. Inloggat
  `Indelningsverket (Grill)` stoppade Hagby/Bettna-frågan med en ny ALTCHA
  före resultat; agenten rörde den inte och fliken är bevarad för ägarens
  lösning. Kontroll: 2 489 påståenden, 1 885 Markdownposter, 3 728
  mediafiler inklusive `.gitkeep`, manifest 3 727 (2 281 exakt/1 418
  käll-/28 citationsavgränsade, 0 olänkade) och dashboard 493/2 489/513.
  T-0012 förblir aktiv; nästa breddrotation är P-0051. Ingen beställning,
  PDF, deployment, commit eller push skapades. Den oförändrade
  20-sidors-PDF:en verifierades.
- Batch 197 är bevarad i repositoryt: S-0600, C-0774, A-2996–A-3003,
  P-0336/P-0397, de nya barnakterna P-0489–P-0493, trädtext,
  forskningsfront, källtäckning, forskningsplan, forskningslogg, Wotan-logg
  och ett checksummat original. Folkräkningens registerposter och
  mantalsutdrag `Folk_101003-031` placerar den gifte bangårdsmästaren Olaus
  och Johanna Charlotta i Gösen nr 4, 15 i Klara rote 3 och gör Augusta,
  Ester, Edit, Oskar och Elvira till uttryckligen barnkodade barn. Inga
  efternamn konstruerades och gemensamt födelseår 1895 gjordes inte till
  tvillingpåstående. Larv E/3 öppnades efter ägarens egen CAPTCHA-lösning
  utan ny utmaning men stod fortsatt endast som `Läsesal`; ingen
  beställning lades. Kontroll: 2 484 påståenden, 1 883 Markdownposter,
  3 723 mediafiler inklusive `.gitkeep`, manifest 3 722 (2 275
  exakt/1 419 käll-/28 citationsavgränsade, 0 olänkade) och dashboard
  493/2 484/513. T-0012 förblir aktiv; Olaus föräldrar är öppna och nästa
  breddrotation är P-0474–P-0475. Ingen läsesalsbeställning, PDF,
  deployment, commit eller push skapades. Den oförändrade 20-sidors-PDF:en
  verifierades.
- Batch 196 är bevarad i repositoryt: S-0599, C-0773, A-2995,
  konflikträttelserna A-2292/A-2294–A-2295, P-0133/P-0135,
  forskningsfront, källtäckning, forskningsplan, trädtext, forskningslogg,
  Wotan-logg, ett maxoriginal och ett IIIF-manifest. Flens länslasaretts
  separata SCB-post säkrar Matilda Charlotta Karlsson f. Sjöberg död
  1920-01-31, född 1860-08-08, hustru till torparen Erik Karlsson i Flen
  och med dödsorsaken `Bronchopneumonia`. Makens senare 1920-04-03 står
  kvar som källkonflikt. Manifestet var publikt; maximalbilden hämtades i
  ägarens redan inloggade Chrome efter ägarens egen CAPTCHA-hantering utan
  ny kontroll eller sessionsdataläsning. Kontroll: 2 476 påståenden, 1 876
  Markdownposter, 3 722 mediafiler inklusive `.gitkeep`, manifest 3 721
  (2 274 exakt/1 419 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 488/2 476/503. T-0012 förblir aktiv; nästa breddrotation är
  P-0336. Ingen person, relation, beställning, PDF, deployment, commit eller
  push skapades. Den oförändrade 20-sidors-PDF:en verifierades.
- Batch 195 är bevarad i repositoryt: S-0598, C-0772, A-2991–A-2994,
  P-0051, forskningsfront, källtäckning, forskningsplan, forskningslogg,
  Wotan-logg, fyra nya maxoriginal och en strukturerad läsobservation.
  Vigseln 1810-11-14 namnger Olof Pehrsson i Överklinten och änkan Maja
  Stina Pehrsdotter i Brattliden. A I/7a markerar Olaus född 1784 som
  `gift`; kandidatidén är stark men saknar exakt födelsedatumbrygga och
  fortsatt hushållskedja. Brattliden s. 159 och s. 19 är endast två
  ortsavsnittsnoll. Vigseln 1799 kan förklara Maja Stinas änkestatus men
  kvinnans identitet är öppen. H I/1, H III/1 och L III/1 omprövades efter
  ägarens inloggning och egen CAPTCHA-hantering men stod kvar som
  `Läsesal` utan bild/order. Kontroll: 2 475 påståenden, 1 874
  Markdownposter, 3 720 mediafiler inklusive `.gitkeep`, manifest 3 719
  (2 272 exakt/1 419 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 488/2 475/503. T-0012 förblir aktiv; nästa breddrotation är
  P-0133. Ingen person, relation, beställning, PDF, deployment, commit eller
  push skapades. Den oförändrade PDF-kontrollen saknar `pdfplumber`.
- Batch 194 är bevarad i repositoryt: S-0597, C-0771, A-2987–A-2990,
  rättelserna av S-0538/C-0702 och P-0133/P-0474–P-0475,
  forskningsfront, källtäckning, forskningsplan, forskningslogg, Wotan-logg,
  tre fulloriginal och nio metadata-/observationsoriginal. GMR 1859 visar
  Landin antagen på Glippsta nr 36 den 1854-08-26; detta är en senast-gräns
  för Carl, inte en avgångsorsak. 1852-notisen är `52 Östra R.`, inte
  `52 W:a V.`; exakt intern plats förblir öppen. Västra Vingåkers kompletta
  inflyttningsår 1852 är ett strikt avgränsat noll och A I/13 a:s
  OCR-screen har inget negativt bevisvärde. Kontroll: 2 471 påståenden,
  1 872 Markdownposter, 3 715 mediafiler inklusive `.gitkeep`, manifest
  3 714 (2 267 exakt/1 419 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 488/2 471/503. T-0012 förblir aktiv; nästa breddrotation är
  P-0051. Ingen person, relation, beställning, PDF, deployment, commit eller
  push skapades. Den oförändrade PDF-kontrollen saknar `pdfplumber`.
- Batch 193 är bevarad i repositoryt: S-0596, C-0770, A-2985–A-2986,
  P-0336, forskningsfront, källtäckning, forskningsplan, forskningslogg,
  Wotan-logg, tre fulloriginal och en strukturerad läsobservation. F II a/9
  år 1853 är exakt bilderna 209–325, 117 visuellt granskade bildytor, utan
  säker Fredric/Anna- eller målortsakt. Resultatet är källavgränsat och
  `afl.53` betyder fortsatt avflyttad. Kontroll: 2 467 påståenden, 1 870
  Markdownposter, 3 703 mediafiler inklusive `.gitkeep`, manifest 3 702
  (2 255 exakt/1 419 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 488/2 467/503. T-0012 förblir aktiv; nästa breddrotation är
  P-0474–P-0475. Ingen person, relation, beställning, PDF, deployment,
  commit eller push skapades.
- Batch 192 är bevarad i repositoryt: den berikade S-0081, C-0767–C-0769,
  A-2980–A-2984, P-0133–P-0134, P-0136, P-0143, P-0213, forskningsfront,
  källtäckning, forskningsplan, forskningslogg, Wotan-logg och fem nya
  sakmedier. Records-API och det publika IIIF-manifestet `F0002785` gav
  originalen utan Chrome. Erik Arvids 13 februari står i konflikt med
  husförhörens 13 mars; Maria Sofias original saknar `Elli`; Carl/Karl
  Oskar hålls som stavningsformer. Kontroll: 2 465 påståenden, 1 868
  Markdownposter, 3 699 mediafiler inklusive `.gitkeep`, manifest 3 698
  (2 252 exakt/1 418 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 488/2 465/503. T-0012 förblir aktiv; nästa breddrotation är
  P-0336. Ingen person, relation, beställning, PDF, deployment, commit
  eller push skapades.
- Batch 191 är bevarad i repositoryt: S-0593–S-0595, C-0764–C-0766,
  A-2973–A-2979, P-0051, forskningsfront, källtäckning, forskningsplan,
  forskningslogg, Wotan-logg och 52 nya sakmedier. A I/5a–e och A I/6a–b
  omfattar 2 134 bildytor; två OCR-pass gav endast avvisade kandidater och
  inget helvolymsnoll. Alla 26 vigseloriginal 1850–1855 saknar det exakta
  paret Olof Pehrsson/Persson och Anna Lovisa Brännberg. Födelseregistrets
  namnfrågor faller på dokumenterad Piteå-täckningslucka; C I/12 öppnades
  inloggat utan ny CAPTCHA och två exakta barnnamnslikheter har andra
  föräldrar. Porsnäsmannen förblir olöst. Kontroll: 2 460 påståenden,
  1 865 Markdownposter, 3 694 mediafiler inklusive `.gitkeep`, manifest
  3 693 (2 249 exakt/1 416 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 488/2 460/503. T-0012 förblir aktiv; nästa breddrotation är
  P-0133. Ingen person, relation, beställning, PDF, deployment, commit eller
  push skapades.
- Batch 190 är bevarad i repositoryt: S-0592, C-0763, A-2966–A-2972,
  rättelserna av S-0553/C-0718/S-0116/A-2799/A-2804, P-0474–P-0475,
  forskningsfront, källtäckning, forskningsplan, forskningslogg, Wotan-logg,
  33 fulloriginal och sex metadata-/observationsoriginal. Livkompaniets
  Glippsta nr 36 är Carl Fredric Drill, antagen 1841-02-18; Bettna B/1
  för honom från Björkvik till Glippsta 1841-11-11 och GMR 1845 visar
  honom gift. Carl Johan är född 1843-01-04 och `oäkta`, med Johanna som
  mor och tomt fadersfält. Vigseln avgränsas efter 1843-01-04 och senast
  1845-07-07 men saknas i de kompletta relevanta följderna i Bettna, Stora
  Malm och Björkvik. Kontroll: 2 453 påståenden, 1 859 Markdownposter,
  3 642 mediafiler inklusive `.gitkeep`, manifest 3 641 (2 215 exakt/
  1 398 käll-/28 citationsavgränsade, 0 olänkade) och dashboard
  488/2 453/503. T-0012 förblir aktiv; nästa breddrotation är P-0051.
  Ingen person, relation, beställning, PDF, deployment, commit eller push
  skapades.
- Batch 189 är bevarad i repositoryt: S-0591, C-0762, A-2963–A-2965,
  P-0336, forskningsfront, källtäckning, forskningsplan, forskningslogg,
  Wotan-logg och en ny sakobservation. Samtliga elva exakta katalogposter
  öppnades i den inloggade sessionen utan CAPTCHA men stod kvar som
  `Läsesal`; ingen order eller kopiebeställning skickades. De breda och
  snäva bouppteckningsfrågorna gav ingen Fredric-nyckel, och den namnblanka
  Stora Lundby-kontrollen gav också noll. Kontroll: 2 446 påståenden, 1 857
  Markdownposter, 3 603 mediafiler inklusive `.gitkeep`, manifest 3 602
  (2 176 exakt/1 398 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 488/2 446/503. T-0012 förblir aktiv; nästa breddrotation är
  P-0474–P-0475. Ingen person, relation, beställning, PDF, deployment,
  commit eller push skapades.
- Batch 188 är bevarad i repositoryt: S-0589–S-0590, C-0757–C-0761,
  A-2954–A-2962, personakterna P-0133–P-0135 och P-0474–P-0475,
  forskningsfront, källtäckning, forskningsplan, trädtext, forskningslogg,
  Wotan-logg och fyra nya sakmedier.
  Verifieringsresultatet redovisas under `Senast verifierat`.
- Ingen nödvändig forskningsuppgift, källidentifierare eller återstartspunkt
  finns endast i `/tmp`, Chrome eller en autentiserad webbläsarsession.
- Arbetsytan innehåller omfattande avsiktliga, ännu ocommittade och delvis
  ospårade projektfiler från det löpande målet. De är beständigt skrivna på
  disk och är auktoritativt arbetsläge; kör inte clean/reset/checkout och
  försök inte rekonstruera dem från chattminne.
- Återstart efter Batch 196: T-0012 fortsätter `ONGOING`/`DOING` med
  breddrotation P-0336. För P-0133/P-0135 ska `A0031515_00557`, de
  ordinarie Helgesta/Flen-dödböckerna och 1920-04-03-inferensen inte läsas
  om utan en ny institutions-, journal-, begravnings- eller
  bouppteckningsnyckel. Matildas dödsdag är 1920-01-31 och 3 april är en
  bevarad konflikt. GMR 1859 och Västra Vingåker B I/3 1852 ska inte
  läsas om utan ny saklig nyckel; `52 Östra R.` följs först från ett nytt
  internt gårds-, sido- eller hushållsankare. För P-0336 ska F II a/9
  bilderna 209–325
  inte läsas om utan en ny person-, akt-, gårds-, arvinge- eller
  jurisdiktionsnyckel. För P-0051 ska A I/5a–e/A I/6a–b:s blinda
  kandidatscreening, E I/4–5:s kompletta vigselår 1850–1855,
  födelseregistrets Piteåfrågor och C I/12 bilderna 26–124 inte upprepas
  utan en ny positiv by-, sida-, familje-, flytt-, vigsel- eller
  födelsenyckel. Den nya makanyckeln Maja Stina Pehrsdotter får bara bära
  riktad direkt originalnominering, inte en ny blind helvolymsskärm. Läs
  inte om C/3:s vigselrader 1799/1810, A I/7a Brattliden s. 159 eller
  A I/8 Brattliden s. 19 utan en ny hushålls-, barn-, flytt- eller
  dödsnyckel. Porsnäsmannen 1858 är olöst, inte avvisad. H III/1, H I/1
  och L III/1 förblir analoga läsesalsvägar; ingen beställning är skickad.
- Beständigt bakgrundsläge från batch 186: den användarägda Chrome-sessionen återaktiverade de
  tidigare spärrade Riksarkivet-frågorna efter att ägaren själv besvarat
  CAPTCHA:n; ingen ny kontroll hanterades av agenten. SCB 1880 placerar
  Carl Fredrik, Johanna och Hedda i Gatstugan Backstuga; SCB 1890 och
  A I/20 a sida 47 placerar Carl i Hagbystugan, medan ett separat register
  fortsatt säger Götstugan. Indelningsverket routar Glippsta nr 36 till
  Livkompaniet och maxoriginalen 1848/1851/1855 visar Carl Fredric
  Drill/Grill före Lars Petter Landin; C-0708:s gamla åttakompaninoll är
  rättat. Folkräkning 1900 visar Johan Petter Zingmark som svärfar i Maria
  Elinas hushåll med Erik August Lindberg och åtta barn. Övriga omkörda
  frågor är strikt täckningsuteslutna eller frågebundna noll, inte person-
  eller aktsnoll.
- Beständigt bakgrundsläge från batch 183: SCB-intervallen Lundby i Göteborgs och Bohus län
  `A0056067_00120`–`_00135` och Norra Lundby i Skaraborgs län
  `A0056082_00246`–`_00253` är komplett visuellt lästa. Den enda Olaus
  född 1852 står på A0056067 bild 125 och är avvisad genom fel län och
  hushållets Johan August född 1858, mot målpersonens Älvsborg och
  säkrade bror född 1849. Kandidatens `ibm` efter `Förf.` står som en
  separat källkonflikt mot C-0387:s kompletta C/6-årgång utan Olaus.
  Upprepa inte de 24 bildytorna utan ny identitetsnyckel. För P-0336 är
  Östra Fågelvik H II/5 och de prioriterade analoga militär-/SJ-rutterna
  fortsatt första återstarter.
- Beständigt bakgrundsläge från batch 181: Piteå stadsförsamlings A I/1a–2a är routade till
  `C0035078` och `C0035079`. Deras inbundna P–R-register visar ingen
  Olaus/Olof Pehrsson/Persson i A I/1a, men det separata registret är
  uttryckligen ofullständigt och resultatet är bara ett registerbladsnoll.
  A I/2a hänvisar `Persson, Olof` till sida 192; där står drängen Olof
  Pehrsson född 1804-04-21, inte Överklintenkandidaten född 1784-02-07.
  Kandidaten är avvisad. Upprepa inte P–R-bladen eller sida 192 utan en ny
  namn-, sida-, hushålls- eller flyttnyckel. De separata A I/1b–2b-posterna
  har tomma publika träd. Olaus förblir endast faderskandidat; H III/1 är
  fortsatt första analoga födelseväg för Barbro och H II/1 återtas endast
  genom personregistret eller ny dokumentnyckel. Katalogvägarna visade
  CAPTCHA även i ansluten Chrome, men ingen kontroll berördes och publika
  arkivträd/IIIF gav originalen utan CAPTCHA.
- Beständigt bakgrundsläge från batch 177: P-0133:s Bettna A I/16 b s. 201 hänvisar internt
  till s. 185 år 1867; sida 185 för Erik Grill till Forssa 1868-10-06.
  Forssa B/3 tar emot honom 1868-11-01 till Sjöstugan, och A I/13 s. 100
  samt A I/14 s. 99 fortsätter samma namn, exakta födelsedatum och
  inflyttningspost. C-0318:s Karlsson/Carlsson-scope missade Grill-raden;
  A-1919 är `REJECTED`. Årdalas `från Forssa 75` ansluter vistelsen men
  den samtidiga flyttposten 1875 saknas. Bettna B/3 a:s hela utflyttningsår
  1867 är läst som bokföringsnoll och ska inte upprepas utan ny nyckel.
  Forssa H II/1, mantal och beväring är nu kompletterande berikningsvägar.
  P-0051:s Lövånger A I/9a–b 1842–1846 är exakt
  routade till `C0034167`–`C0034168` med sammanlagt 564 bildytor utan
  bystrukturer. Två OCR-pass användes bara för navigation; alla 30
  bildytor med en nominerad `1830`-token lästes i maximala original.
  Närmast var Clara Olofsdotter född 1830-03-22 i Kräkånger, inte
  Barbro/Barbru Cajsa född 24/2. Resultatet är inte ett person-,
  vistelse-, by-, församlings- eller helvolymsnoll och ska inte upprepas
  utan ny positiv by-, sida-, hushålls- eller flyttnyckel. P-0051:s Piteå
  A I/3b–e och A I/4a–e är exakt
  routade till `C0035001`–`C0035009`. Två OCR-pass över 1 867 bildytor var
  endast kandidatnavigation; nio Olaus-rader och en Olof född 1784 avvisades
  i fulloriginal. Det är inte ett person-, vistelse-, by- eller helvolymsnoll
  och ska inte upprepas utan ny by-/sidnyckel. H I/1, H III/1, L III/1,
  C II b/13 och F II/23 har exakta äldre Arkis-UUID:er men tomma publika
  arkivträd och HTTP 500 på batchrouten. Beställningsordningen kvarstår.
  P-0472 står som separat dräng i Ånäset A I/2 s. 179 med
  Lyckseleanteckning. Publika arkivträd löser nu A I/6, A I/7 och C/2;
  A I/7 s. 126 återfinner honom i Åskilje och C/2:s hela 1798-år saknar
  en förenlig födelsepost. Upprepa inte A I/7-screeningen, Degerfors C/1
  år 1798, Lycksele C/2 år 1798, Degerfors C/2 år 1809 eller B/1
  1822–1826 utan ny positiv nyckel. A I/6 är inte personscreenad.
  P-0473:s föräldrar P-0478 Jan Larsson och P-0479 Sara Lisa
  Jonsdotter är säkrade i A I/2 och två följande Ånäset-led; följ dem inte
  djupare före en balanserad djup-6-våg. Beatas dödsår 1852 ligger i ett
  katalogiserat gap mellan C/3:s döddel och F/2 och får inget konstruerat
  datum. P-0474 följs från Götstugan till Stora Hesselstugan. Bettna F/4
  sida 1 post 1 och A I/21 a sida 27 korsbelägger död 1895-01-04; F/4
  anger begravning 13/1. A I/20 a:s registerrad får fortfarande inte göras
  till ett exakt levnads- eller bostadsår och Carlsson-kandidaten 1885 är
  avvisad. Hela Bettna F/3:s dödföljd 1883–1894 är namnformsbundet
  negativ, liksom B/5:s sakliga flyttföljd 1891–1894; A I/21 a s. 337
  saknar honom men är bara ett sidnoll. Upprepa inte dessa följder. F/4:s
  1822-04-09 och husförhörens 1822-07-09 är en olöst konflikt. P-0475 dog
  1883-02-24 och hennes föräldrar
  P-0476–P-0477 är säkrade. Jans 1791-05-09 Björkvik är konfliktsatt av
  hela C/4-årgången; Lenas Helena-kandidat 1785-10-31 i Walla är inte en
  säker föräldrabrygga. Följ dem inte djupare före nästa balanserade våg.
  P-0133:s föräldrar P-0474–P-0475 och vistelse 1867–1875 är lösta;
  Forssa H II/1 är fortsatt en exakt analog attestväg för 1868 och 1876
  men inte ett villkor för relationerna eller vistelsekedjan. Forssa
  H II/1, D14/10, Flen P I/1 och Villåttinge C II b/5 → F II/59 har exakta
  äldre UUID:er men publika träd/batchvyer exponerar inga bilder; Vingåkers
  fondträd visar fortfarande bara K Kartor. De är analoga återstarter och
  inget person- eller materialnoll. Forssa-SCB har efter nyckeln
  `Sjöstugan`/`Grill` återlästs positivt på bild 42; A-2836 är avvisad.
  Upprepa inte A I/17:s OCR-screen eller övriga SCB-skärmar utan ny nyckel. Carls
  Halla–Björnlunda-spår kräver en ny positiv identitetsnyckel; upprepa inte
  C/2 år 1822, B/1 åren 1836–1842, Ellesta s. 37–40 eller blind OCR av
  Björnlunda A I/11. För P-0051 är
  hela E I/3:s vigselföljd 1806–1830 nu läst negativt; posterna
  1819–1826-10-07 hålls uttryckligen som pastorsämbetsrekonstruktion och
  inte som obruten samtida följd. H II/1 återtas bara
  genom personregistret eller en ny dokumentnyckel; H III/1 är fortsatt
  första analoga originalroute för Barbros födelsefråga. P-0423:s ursprung
  och föräldrar är nu lösta; P-0051:s stadsregister är färdigroterade i
  batch 181 och nästa breddrotation är P-0133.
  Sävar mantal `SE/HLA/1100016/Vol/150` är bara analog
  berikningsroute för parets tidiga hushåll. För P-0336
  förblir Göta livgardes analoga namnregister 198 förstahandsroute;
  journalerna 240/241 följs av Svea `D III/2`, Livgardet till häst
  `D VI/6` och Göta GMR 237. Östra Fågelvik H II/5:s läsesalsattest 1873 är
  en direkt äldre reserv. Upprepa inte B II/1:s kompletta inflyttningsår
  1876 eller GMR 1553:s blinda OCR-screening utan ny nyckel. Bjärke
  personregister är nu reproduktion `C0104265`; hela rubrikavsnittet
  `Jakobsson (Jackobsson, Jacobsson, Jacopsson)` på bilderna 94–95 saknar
  Fredric/Fredrik. Upprepa inte avsnittet utan en ny namnform. Detta är bara
  ett registernoll. F II a/9 är reproduktion `C0100962` med 524 bilder men
  utan manifeststrukturer; 1853-delen återtas bara med ny datum-, akt-,
  gårds- eller sidnyckel och är inget boupptecknings-/personnoll. H V/1–2,
  H II/5, SJ F 1 A/4 och D 4 A/1 samt de tre prioriterade gardesrullorna
  har exakta äldre UUID:er men tomma publika träd.

## Aktuellt projektläge

- Aktiv Wotan-uppgift: **T-0012**, `ONGOING` / `DOING`, storlek L.
- **Batch 191 har kört om P-0051:s återstående digitala Piteårutter efter
  användarens inloggning och besvarade CAPTCHA.** A I/5a–e och A I/6a–b
  omfattar 2 134 bildytor; två OCR-pass användes endast för navigation och
  gav inget säkert namn-/årssamband med Olaus 1784. Alla 26 maxoriginal i
  vigselföljden 1850–1855 saknar det exakta paret Olof Pehrsson/Persson och
  Anna Lovisa Brännberg. Födelseregistrets noll är täckningsbundet eftersom
  även namnblank Piteå 1853–1858 ger noll. Den inloggade katalogen öppnade
  däremot C I/12 som `C0035059` utan ny CAPTCHA; två barnnamnslikheter har
  andra föräldrar. S-0593–S-0595, C-0764–C-0766, A-2973–A-2979 och 52 nya
  sakmedier bevarar resultatet. Porsnäsmannen är olöst och ingen relation
  skapades. Kontroll: 2 460 påståenden, 1 865 Markdownposter, 3 694
  mediafiler inklusive `.gitkeep`, manifest 3 693 (2 249 exakt/1 416
  käll-/28 citationsavgränsade, 0 olänkade) och dashboard 488/2 460/503.
  T-0012 förblir aktiv; nästa breddrotation är P-0133. Ingen beställning,
  PDF, deployment, commit eller push skapades.
- **Batch 190 har rättat och förlängt P-0474–P-0475:s tidiga kedja.**
  GMR 1842 visar Livkompaniets Glippsta nr 36 med Carl Fredric Drill,
  antagen 1841-02-18; A-2804:s äldre åttakompaninoll är avvisat. Bettna
  B/1 för soldaten från Björkvik till Glippsta 1841-11-11 och GMR 1845
  visar honom gift. C/5 rättar Carl Johan till 1843-01-04, `oäkta`, med
  Johanna som mor och tomt fadersfält. Vigseln avgränsas efter den dagen
  och senast 1845-07-07 men saknas i de tre kompletta relevanta
  församlingsföljderna. S-0592, C-0763, A-2966–A-2972 och 39 nya sakmedier
  bevarar resultatet. Kontroll: 2 453 påståenden, 1 859 Markdownposter,
  3 642 mediafiler inklusive `.gitkeep`, manifest 3 641 (2 215 exakt/
  1 398 käll-/28 citationsavgränsade, 0 olänkade) och dashboard
  488/2 453/503. T-0012 förblir aktiv; nästa breddrotation är P-0051.
  Ingen person, relation, beställning, PDF, deployment, commit eller push
  skapades.
- **Batch 189 har fullföljt P-0336:s inloggade omkörning.** Alla elva
  tidigare spärrade katalogposter öppnas utan CAPTCHA men är fortsatt
  `Läsesal`; Riksarkivets ordergränssnitt är för läsning på plats och ingen
  beställning skickades. Bouppteckningsregistrets Fredric-frågor gav ingen
  aktnyckel. Den namnblanka Stora Lundby-kontrollen är också tom, så
  utfallet är ett täckningsbundet registernoll och inte person- eller
  aktsnoll. S-0591, C-0762, A-2963–A-2965 och en ny sakobservation bevarar
  resultatet. Kontroll: 2 446 påståenden, 1 857 Markdownposter, 3 603
  mediafiler inklusive `.gitkeep`, manifest 3 602 (2 176 exakt/1 398
  käll-/28 citationsavgränsade, 0 olänkade) och dashboard 488/2 446/503.
  T-0012 förblir aktiv; nästa breddrotation är P-0474–P-0475. Ingen person,
  relation, beställning, PDF, deployment, commit eller push skapades.
- **Batch 188 har fullföljt P-0133:s inloggade omkörning.** De fem tidigare
  CAPTCHA-spärrade volymerna öppnas nu men är fortsatt läsesalsmaterial.
  Eriks bouppteckningsregisterutfall är täckningsbundet, medan Anna
  Christina, Johanna och Carl Fredrik fått tre exakta analoga aktvägar.
  S-0589–S-0590, C-0757–C-0761, A-2954–A-2962 och fyra nya sakmedier
  bevarar resultatet. Kontroll: 2 443 påståenden, 1 855 Markdownposter,
  3 602 mediafiler inklusive `.gitkeep`, manifest 3 601 (2 175 exakt/1 398
  käll-/28 citationsavgränsade, 0 olänkade) och dashboard 488/2 443/503.
  T-0012 förblir aktiv; nästa breddrotation är P-0336. Ingen person,
  föräldralänk, PDF, deployment, commit eller push skapades.
- **Batch 186 har återaktiverat Riksarkivets tidigare spärrade frågor och
  rättat ett falskt militärt noll.** Carl Fredrik Grill återfinns i
  Gatstugan Backstuga 1880 och Hagbystugan 1890; A I/20 a sida 47 bekräftar
  den senare orten men lämnar Götstugan som registerkonflikt. Glippsta
  nummer 36 är Livkompaniet och visar Carl Fredric Drill/Grill 1848 och
  1851 före soldatbytet som syns 1855. Johan Petter Zingmark återfinns 1900
  som svärfar i dotterns hushåll med åtta barn. Nio sidolinjepersoner,
  S-0584–S-0586, C-0750–C-0753, A-2922–A-2946 och 32 nya sakmedier bevarar
  resultatet. Kontroll: 2 427 påståenden, 1 843 Markdownposter, 3 553
  mediafiler inklusive `.gitkeep`, manifest 3 552 (2 159 exakt/1 365
  käll-/28 citationsavgränsade, 0 olänkade) och dashboard 488/2 427/503.
  T-0012 förblir aktiv; nästa breddrotation är P-0051. Ingen PDF,
  deployment, commit eller push skapades.
- **Batch 185 har återfunnit Erik Grill i föräldrahushållet 1860.** SCB
  bild `A0056037_00317` visar Carl Fredrik Grill, Johanna Jansdotter och
  sonen E. född 1851 i den redan säkra familjeprofilen. Det fyller
  samtidsglappet 1852–1866 utan att skapa exakt datum från en årsuppgift.
  Två syskonrader är konfliktsatta och A I/15 b:s Wernerhushåll är endast
  ett sida-/platsnoll. S-0583, C-0749, A-2916–A-2921 och 46 nya sakmedier
  bevarar resultatet. Kontroll: 2 402 påståenden, 1 827 Markdownposter,
  3 521 mediafiler inklusive `.gitkeep`, manifest 3 520 (2 146 exakt/
  1 346 käll-/28 citationsavgränsade, 0 olänkade) och dashboard
  479/2 402/487. T-0012 förblir aktiv; nästa breddrotation är P-0474–P-0475.
  Ingen PDF, deployment, commit eller push skapades.
- **Batch 184 har avvisat Olof Pehrsson i Hortlax som Överklintenmannen.**
  Piteå tingslags A II/34:s register och bouppteckning nummer 8 identifierar
  den avlidne förre skattebonden Olof Pehrsson i Hortlax 1829. Piteå land
  A I/6a sida 526 anger honom född 1760, inte 1784-02-07. Ingen person eller
  relation skapades; resultatet är inget person-, vistelse- eller
  föräldranoll. S-0581–S-0582, C-0748, A-2912–A-2915 och elva nya
  sakmedier bevarar resultatet. Kontroll: 2 396 påståenden, 1 825
  Markdownposter, 3 475 mediafiler inklusive `.gitkeep`, manifest 3 474
  (2 126 exakt/1 320 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 479/2 396/487. T-0012 förblir aktiv; nästa breddrotation är
  P-0133. Ingen PDF, deployment, commit eller push skapades.
- **Batch 183 har slutläst SCB 1860:s andra Lundby-ranger och avvisat den
  enda Olaus 1852-kandidaten.** Records-API och IIIF avgränsar 24 bilder i
  Lundby/Göteborgs och Bohus län samt Norra Lundby/Skaraborg. Bild
  `A0056067_00125` har Olaus 1852 och Johan August 1858 i samma hushåll;
  länet och syskonåret utesluter P-0336, vars positiva kedja anger Älvsborg
  och vars bror föddes 1849. `ibm`/`Förf.` står kvar som konflikt mot
  Lundby C/6:s årgångsnoll. Ingen person eller relation skapades. S-0580,
  C-0747 och A-2907–A-2911 samt 52 nya sakmedier bevarar resultatet.
  Kontroll: 2 392 påståenden, 1 822 Markdownposter, 3 464 mediafiler
  inklusive `.gitkeep`, manifest 3 463 (2 123 exakt/1 312 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 479/2 392/487. T-0012
  förblir aktiv; nästa breddrotation är P-0051. Ingen PDF, deployment,
  commit eller push skapades.
- **Batch 182 har återfunnit Erik Grill i SCB:s Forssa-utdrag 1870 och
  rättat ett falskt screeningutfall.** Manifestet avgränsar Forssa till
  `A0056581_00037`–`_00044`; maxoriginalet för bild 42 visar `Grill,
  Erik, Dräng`, född 1851 i Bettna och ogift. Radordningen motsvarar
  Sjöstugan sida 100, utan att skapa en relation till det föregående
  hushållet. A-2836 är nu `REJECTED`; de kvarstående snäva skärmarna förs
  separat i A-2906. S-0579, C-0746 och A-2903–A-2906 samt två nya
  sakmedier bevarar resultatet. Kontroll: 2 387 påståenden,
  1 820 Markdownposter, 3 412 mediafiler inklusive `.gitkeep`, manifest
  3 411 (2 099 exakt/1 284 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 479/2 387/487. T-0012 förblir aktiv; nästa breddrotation är
  P-0336. Ingen PDF, deployment, commit eller push skapades.
- **Batch 181 har prövat Piteå stadsförsamlings inbundna personregister och
  avvisat den enda konkreta Olof-kandidaten.** Publika arkivträd och IIIF
  löste A I/1a–2a till `C0035078`–`C0035079`, trots att exakta
  kataloglänkar i ansluten Chrome fortsatt visade orörd CAPTCHA. P–R-bladet
  i A I/1a saknar målformen, men registret är uttryckligen ofullständigt och
  resultatet är bara ett registerbladsnoll. A I/2a hänvisar `Persson, Olof`
  till sida 192; där står drängen Olof Pehrsson född 1804-04-21, inte
  Olaus född 1784-02-07. De separata A I/1b–2b-posterna har tomma publika
  träd. Ingen relation eller personnoll skapades. S-0578, C-0745 och
  A-2899–A-2902 samt sex nya sakmedier bevarar resultatet. Kontroll:
  2 383 påståenden, 1 818 Markdownposter, 3 410 mediafiler inklusive
  `.gitkeep`, manifest 3 409 (2 098 exakt/1 283 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 479/2 383/487. T-0012
  förblir aktiv; nästa breddrotation är P-0133. Ingen PDF, deployment,
  commit eller push skapades.
- **Batch 180 har säkrat Petter Reinholds Lyckselevistelse i Åskilje och
  avgränsat födelseåret 1798.** Katalogernas `returnUrl` gav äldre
  Arkis-UUID:er och publika arkivträd löste A I/6, A I/7 och C/2 till
  `C0034136`, `C0034137` och `C0034150`. A I/7 sida 126 har en separat rad
  som försiktigt läses `Rein[hold] Pehrsson`, född 1798. Degerfors A I/2:s
  fulla namn, samma år och uttryckliga Lyckseleflytt korroborerar
  identiteten. C/2:s hela födelseår 1798 saknar en förenlig post; Petrio
  till Olof Ersson och Elisabeth Abrahamsdotter avvisas. A I/6 är routad
  men inte personscreenad, B I/1 börjar 1834, och exakt födelsedag,
  födelseort samt föräldrar är öppna. Katalogvägarna visade CAPTCHA i
  ansluten Chrome, men ingen kontroll berördes; publika Tree/IIIF gav
  originalen utan CAPTCHA. S-0577, C-0744 och A-2896–A-2898 samt tolv nya
  sakmedier bevarar resultatet. Kontroll: 2 379 påståenden, 1 816
  Markdownposter, 3 404 mediafiler inklusive `.gitkeep`, manifest 3 403
  (2 095 exakt/1 280 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 479/2 379/487. T-0012 förblir aktiv; nästa breddrotation är
  P-0051. Ingen PDF, deployment, commit eller push skapades.
- **Batch 179 har löst Carl Fredrik Grills livsslut och slutläst B/5.**
  F/4 sida 1 post 1 registrerar den avskedade soldaten från Stora
  Hesselstugan som död 1895-01-04 och begravd 13/1; A I/21 a sida 27
  korsbelägger namn, titel, ort och dödsdag. F/4:s 1822-04-09 står kvar i
  konflikt med husförhörens 1822-07-09. Den senare omläsningen C-0798
  återfann födelsen 1822-04-09 och modern Ella Ersdotter. B/5:s
  samtliga sakliga in- och utflyttningsposter 1891–1894 är visuellt
  slutlästa utan Carl Fredrik/Carl Fredric/Carl Eric Grill. Chrome-
  bildvisarna fungerade utan CAPTCHA; exakt folkräkning 1890 visade fortsatt
  orörd ALTCHA. S-0576, C-0743 och A-2893–A-2895 samt 24 nya sakmedier
  bevarar resultatet. Kontroll: 2 376 påståenden, 1 814 Markdownposter,
  3 392 mediafiler inklusive `.gitkeep`, manifest 3 391 (2 091 exakt/
  1 272 käll-/28 citationsavgränsade, 0 olänkade) och dashboard
  479/2 376/487. T-0012 förblir aktiv; nästa breddrotation är
  P-0472–P-0473. Ingen PDF, deployment, commit eller push skapades.
- **Batch 178 har slutläst SCB:s hela Stora Lundby-utdrag 1870 utan att
  skapa ett falskt personnoll.** Records-API och IIIF avgränsar
  `SE/RA/420401/05/H 1 A/96`, `A0056624_00444`–`_00462`, före Skallsjö
  på `_00463`. Alla 19 maximala original lästes visuellt; ingen säker
  Olaus/Olof Fredriksson/Fredrikson/Fredberg-rad finns. Apple Vision-OCR
  användes endast för kandidatnavigation. S-0575, C-0742 och
  A-2891–A-2892 samt 19 fulloriginal och två metadataoriginal bevarar det
  strikt käll-, församlings-, årgångs- och namnformsbundna resultatet.
  Kontroll: 2 373 påståenden, 1 812 Markdownposter, 3 368 mediafiler
  inklusive `.gitkeep`, manifest 3 367 (2 067 exakt/1 272 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 479/2 373/487. T-0012
  förblir aktiv; nästa breddrotation är P-0474–P-0475. Ingen PDF,
  deployment, commit eller push skapades.
- **Batch 177 har löst P-0133:s vistelse 1867–1875 under namnet Grill och
  rättat ett falskt volymnoll.** Bettna A I/16 b s. 201→185 för Erik till
  Forssa 1868-10-06; Forssa B/3 post 25 tar emot honom 1/11 till
  Sjöstugan, där A I/13 s. 100 och A I/14 s. 99 fortsätter exakt namn,
  datum, ort och post. C-0318:s Karlsson/Carlsson-scope missade sida 99 och
  A-1919 är nu `REJECTED`. Bettna B/3 a:s hela utflyttningsår 1867 är ett
  komplett bokföringsnoll som stämmer med internflytten, inte ett personnoll.
  Årdalas `från Forssa 75` ansluter vistelsen; endast den samtidiga
  flyttposten 1875 saknas. Inloggad Chrome utanför sandboxen visade ändå
  orörd ALTCHA på Forssa H II/1 och A I/13; publik Tree/IIIF gav A I/13
  utan interaktion. S-0574, C-0741 och A-2885–A-2890 samt åtta
  fulloriginal och sju metadata-/processoriginal bevarar resultatet.
  Kontroll: 2 371 påståenden, 1 810 Markdownposter, 3 347 mediafiler
  inklusive `.gitkeep`, manifest 3 346 (2 048 exakt/1 270 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 479/2 371/487. T-0012
  förblir aktiv; nästa breddrotation är P-0336. Ingen PDF, deployment,
  commit eller push skapades.
- **Batch 176 har avgränsat Lövånger A I/9a–b utan att skapa ett falskt
  helvolymsnoll.** De två officiella manifesten omfattar 564 bildytor
  1842–1846 utan bystrukturer. Två lokala OCR-pass användes bara för
  kandidatnavigation; 30 nominerade `1830`-bilder lästes sedan visuellt i
  maximala original. Ingen motsvarar Barbro/Barbru Cajsa Olofsdotter född
  1830-02-24. Närmast är Clara Olofsdotter född 1830-03-22 i Kräkånger och
  hon avvisas genom både förnamn och datum. S-0573, C-0740 och
  A-2882–A-2884, 30 fulloriginal, två IIIF-manifest och en rensad
  screening-/åtkomstobservation bevarar resultatet. Kontroll: 2 365
  påståenden, 1 808 Markdownposter, 3 332 mediafiler inklusive `.gitkeep`,
  manifest 3 331 (2 040 exakt/1 263 käll-/28 citationsavgränsade,
  0 olänkade) och dashboard 479/2 365/487. T-0012 förblir aktiv; nästa
  breddrotation är P-0133. Ingen PDF, deployment, commit eller push
  skapades.
- **Batch 175 har avgränsat Carl Fredrik Grills sena Bettna-spår utan att
  konstruera ett dödsfall.** Hela F/3:s dödföljd 1883–1894 är slutläst utan
  namnformerna Carl Fredrik/Carl Fredric/Carl Eric Grill, och A I/21 a
  s. 337 saknar honom vid Fiskartorp/Götstugan. B/4, B/5 och F/4 är exakt
  routade; bara B/4 har OCR-screenats, enbart som kandidatnavigation, så
  dessa serier bär inget person- eller helvolymsnoll. Den anslutna,
  autentiserade Chrome-sessionen utanför sandboxen visade fortfarande
  orörd CAPTCHA/ALTCHA på både katalog- och folkräkningsrutten. S-0572,
  C-0739 och A-2878–A-2881, 40 fulloriginal, fyra IIIF-metadataoriginal
  och en rensad åtkomstobservation bevarar resultatet. Kontroll: 2 362
  påståenden, 1 806 Markdownposter, 3 299 mediafiler inklusive `.gitkeep`,
  manifest 3 298 (2 037 exakt/1 233 käll-/28 citationsavgränsade,
  0 olänkade) och dashboard 479/2 362/487. T-0012 förblir aktiv; nästa
  breddrotation är P-0051. Ingen PDF, deployment, commit eller push
  skapades.
- **Batch 174 har brutit Bjärke-bildhindret men hållit huvudserien öppen.**
  Publikt Tree/SubTree exponerar personregistret som `C0104265` och F II
  a/9 som `C0100962`. Bilderna 94–95 avgränsar hela
  Jakobsson/Jacobsson-avsnittet utan Fredric/Fredrik; det är ett exakt
  register- och namnformsnoll, inte boupptecknings- eller personnoll.
  Huvudseriens 524 bilder saknar strukturer och 1853-delen slutlästes inte.
  Åtta analoga Olaus-routes fick exakta äldre Arkis-UUID:er men deras
  publika träd är tomma. Katalogrutterna visade fortsatt orörd CAPTCHA/ALTCHA
  i ansluten Chrome utanför sandboxen. S-0571/C-0738/A-2873–A-2877, två
  fulloriginal, fyra IIIF-metadataoriginal och en rensad åtkomstobservation
  bevarar resultatet. Kontroll: 2 358 påståenden, 1 804 Markdownposter,
  3 254 mediafiler inklusive `.gitkeep`, manifest 3 253 (1 992 exakt/
  1 233 käll-/28 citationsavgränsade, 0 olänkade) och dashboard
  479/2 358/487. T-0012 förblir aktiv; nästa breddrotation är P-0474–P-0475.
  Ingen PDF, deployment, commit eller push skapades.
- **Batch 173 har gjort P-0133:s analoga återstarter exakt kontrollerbara.**
  Villåttinge C II b/5 och F II/59, Flen P I/1, Södermanlands regemente
  D14/10 samt Vingåkers fögderi har exakta äldre Arkis-UUID:er. De fyra
  volymträden är tomma och deras batchvyer samt Forssa H II/1:s batchvy visar
  Riksarkivets interna felsida utan bild-id. Vingåkers fondträd visar fortsatt
  endast K Kartor; tre records-API-omprov stoppades av WAF före resultat och
  är inga noll. Katalogposterna visade fortfarande orörd ALTCHA i Chrome
  utanför sandboxen; inga sessionsdata lästes. Ingen originalbild eller
  persontext exponerades. S-0570/C-0737/A-2870–A-2872 bevarar resultatet.
  Kontroll: 2 353 påståenden, 1 802 Markdownposter, 3 247 mediafiler inklusive
  `.gitkeep`, manifest 3 246 (1 985 exakt/1 233 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 479/2 353/487. T-0012
  förblir aktiv; nästa breddrotation är P-0336. Ingen PDF, deployment, commit
  eller push skapades.
- **Batch 172 har routat Piteå-husförhören och avgränsat Barbros återstarter.**
  A I/3b–e och A I/4a–e är reproduktionerna `C0035001`–`C0035009` med
  sammanlagt 1 867 bildytor. Två lokala OCR-pass användes bara för
  navigation; tio verkliga kandidater lästes i maximala original och
  avvisades genom annat födelseår eller patronymikon. Olof född 1784 står
  som son i Anders Pehrssons hushåll. Screeningen kan missa handskrift och
  skapar inget vistelse- eller faderskapsnoll. H I/1, H III/1, L III/1,
  C II b/13 och F II/23 har nu exakta Arkis-UUID:er, men publika träd saknar
  bildbarn och batchanropen ger HTTP 500. Extern inloggad Chrome utanför
  sandboxen visade fortfarande orörd ALTCHA på A I/3b. S-0568–S-0569,
  C-0735–C-0736 och A-2865–A-2869 bevarar resultatet. Kontroll: 2 350
  påståenden, 1 800 Markdownposter, 3 246 mediafiler inklusive `.gitkeep`,
  manifest 3 245 (1 984 exakt/1 233 käll-/28 citationsavgränsade,
  0 olänkade) och dashboard 479/2 350/487. T-0012 förblir aktiv; nästa
  breddrotation är P-0133. Ingen PDF, deployment, commit eller push skapades.
- **Batch 171 har säkrat Beatas föräldrar och avgränsat Petters ursprung.**
  Degerfors A I/2 s. 179 placerar Beata 1809 under P-0478 Jan Larsson och
  P-0479 Sara Lisa Jonsdotters `döttr. o. barn`; A I/3 s. 221 och A I/4
  s. 262 sluter kedjan till den gifta familjen. Petter Reinhold står
  separat som dräng med Lyckseleanteckning. C/1:s hela 1798-år saknar honom
  och C/2:s hela 1809-år saknar Beata. Lycksele A I/6, A I/7 och C/2 är
  exakta men bildmässigt olästa routes. Degerfors dödboksföljd har ett
  kataloggap kring Beatas uppgivna dödsår 1852. Verklig inloggad Chrome
  utanför sandboxen visade fortfarande orörd ALTCHA; API/JSON-LD/OAI/IIIF
  gav resten. S-0566–S-0567, C-0733–C-0734, A-2855–A-2864 och
  P-0478–P-0479 bevarar resultatet. Kontroll: 2 345 påståenden, 1 796
  Markdownposter, 3 199 mediafiler inklusive `.gitkeep`, manifest 3 198
  (1 937 exakt/1 233 käll-/28 citationsavgränsade, 0 olänkade) och dashboard
  479/2 345/487. P-0004 har 76 kända anor och elva öppna slutstatusar genom
  djup 5; P-0210 har exakt P-0336 öppen genom djup 4. T-0012 förblir aktiv;
  nästa breddrotation är P-0051. Ingen PDF, deployment, commit eller push
  skapades.
- **Batch 170 har säkrat Johannas livsslut och öppnat hennes föräldrar.**
  Bettna A I/18 a följer Carl Fredrik Grill och Johanna Jansdotter vid
  Östra Soldattorp nr 38 genom 1878; A I/19 a:s gratialistregister och
  sida 193 återfinner dem i Götstugan 1881–1885. F/3 säkrar Johanna död
  1883-02-24. A I/20 a listar Carl i gratialistregistret men den hänvisade
  hushållssidan saknar honom; hans död är öppen och Carlsson 1885 är
  avvisad. Bettna C/6 1870–1871 och Björkvik B/4 inflyttade 1878–1879 är
  kompletta, avgränsade noll. C/6 och A I/13 a säkrar P-0476 Jan Ericson
  och P-0477 Lena Jonsdotter som Johannas föräldrar. Jans uppgivna
  1791-05-09 Björkvik motsägs av hela C/4-årgången; Lenas Helena-kandidat
  1785-10-31 i Walla är stark men inte en sluten föräldrabrygga. Verklig
  inloggad Chrome utanför sandboxen visade fortfarande orörd ALTCHA;
  API/JSON-LD/OAI/IIIF gav originalen. S-0564–S-0565, C-0731–C-0732,
  A-2844–A-2854 och P-0476–P-0477 bevarar resultatet. T-0012 förblir
  aktiv; nästa breddrotation är P-0472–P-0473. Kontroll: 2 335 påståenden,
  1 790 Markdownposter, 3 165 mediafiler inklusive `.gitkeep`, manifest
  3 164 (1 903 exakt/1 233 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 477/2 335/485. P-0004 har 74 kända anor och tolv öppna
  slutstatusar genom djup 5; P-0210 har exakt P-0336 öppen genom djup 4.
  Ordinarie kontroller passerade; ingen PDF, deployment, commit eller push
  skapades.
- **Batch 169 har gjort den militära återstarten för P-0336 exakt utan att
  tillskriva honom ett förband.** Riksarkivets API/OAI/JSON-LD identifierar
  Göta GMR 237, Svea `D III/2`, `D VI/16` och två kompanirullor samt
  Livgardet till hästs `D VI/6` som sex analoga vägar över målperioden.
  Digitala GMR 1553 omfattar 1875; manifestet avgränsar bilderna 182–354.
  OCR användes bara för navigation. Bild 268:s Olaus Robert, född 1841 i
  Nyköping, avvisades i fulloriginal och screeningen görs inte till ett
  fullvolyms-/person-/förbandsnoll. Extern inloggad Chrome utanför sandboxen
  omdirigerade fortfarande katalogposten till orörd ALTCHA; publik
  batchsida och IIIF gav originalet utan interaktion. S-0563/C-0730/
  A-2839–A-2843 bevarar resultatet. T-0012 förblir aktiv och nästa
  breddrotation är P-0474–P-0475. Kontroll: 2 324 påståenden, 1 784
  Markdownposter, 3 112 mediafiler inklusive `.gitkeep`, manifest 3 111
  (1 850 exakt/1 233 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 475/2 324/483. P-0004 har fortsatt 72 kända anor och tretton
  öppna slutstatusar genom djup 5; P-0210 har exakt P-0336 öppen genom
  djup 4. Ordinarie kontroller passerade; ingen PDF, deployment, commit
  eller push skapades.
- **Batch 168 har löst Erik Karlssons föräldraidentitet.** Bettna A I/16 b
  sida 201 visar under Hagby och Östra Soldattorp nr 38 Carl Fredrik Grill,
  Johanna Jansdotter och sonen Erik med exakt 1851-01-30 Bettna. C/5,
  A I/13 a och A I/16 b ger tre ursprungliga Bettna-led; vuxenkedjans
  exakta datum, ort och patronymikon gör P-0474–P-0475 till korroborerade
  djup-5-föräldrar. SCB 1870 visar föräldraparet kvar utan Erik. A I/17 och
  avgränsade SCB-skärmar gav ingen säker målrad men inget helvolymsnoll.
  Vistelsen 1867–1875 är öppen och Carls egen Halla-födelse konfliktsatt.
  Extern Chrome utanför sandboxen visade fortfarande orörd ALTCHA;
  API/JSON-LD/OAI/Tree/IIIF gav originalen. S-0562/C-0729/A-2833–A-2838,
  två fulloriginal och tolv metadataoriginal bevarar resultatet; nästa
  breddrotation är P-0336. Kontroll: 2 319 påståenden, 1 782
  Markdownposter, 3 095 mediafiler inklusive `.gitkeep`, manifest 3 094
  (1 833 exakt/1 233 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 475/2 319/483. P-0004 har 72 kända anor och tretton öppna
  slutstatusar genom djup 5; P-0210 har exakt P-0336 öppen genom djup 4.
  Ordinarie kontroller passerade; ingen PDF, deployment, commit eller push
  skapades.
- **Batch 167 har slutläst Piteå landsförsamling E I/3:s återstående
  vigselföljd 1819–1830 utan att skapa en farrelation.** Alla 31
  fulloriginal, bilderna `71000569_00061`–`_00091`, lästes. Den
  rekonstruerade delen 1819–1826-10-07 saknar Olaus/Olof
  Pehrsson/Persson med kandidatens exakta födelsedatum 1784-02-07; den
  följande samtida delen genom 1830 saknar samma namnformer i motsvarande
  åldersläge. Slutsatserna är två proveniensmärkta, serie-, församlings-
  och tidsbundna vigselnoll, inte vistelse-, överlevnads-, civilstånds-
  eller faderskapsbelägg. Publik Riksarkivet-IIIF fungerade utanför
  nätverkssandboxen utan Chrome eller CAPTCHA/ALTCHA. S-0561/C-0728/
  A-2831–A-2832 och 31 checksummade fulloriginal bevarar resultatet;
  nästa breddrotation är P-0133. Kontroll: 2 313 påståenden, 1 778
  Markdownposter, 3 081 mediafiler inklusive `.gitkeep`, manifest 3 080
  (1 831 exakt/1 221 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 473/2 313/481. P-0004 har fortsatt 70 kända anor och tolv
  öppna slutstatusar genom djup 5; P-0210 har exakt P-0336 öppen genom
  djup 4. Ordinarie kontroller passerade; ingen PDF, deployment, commit
  eller push skapades.
- **Batch 166 har löst Sara Sophia Pehrsdotters ursprung och föräldrar i
  Riksarkivets original.** Degerfors A I/5a s. 335 och A I/6b s. 399
  placerar henne, född 1829-05-21, som dotter till P-0472 Petter Reinhold
  Pehrsson och P-0473 Beata Jonsdotter i Ånäset. Den senare sidan anger
  `Säfvar` och 1850-11-24, samma giftårsdag som två Sävarlängder. C/2:s
  vigselpost 1826 namnger föräldraparet. Den skannade födelseföljden i C/2
  slutar i augusti 1828 före döddelen, så Saras egen 1829-notis kan inte
  läsas. `Lycksele` är nu en senare ortkonflikt; vigselregisterpost och
  dödsdagen 1868-08-14 är fortsatt öppna. Inloggad Chrome utanför sandboxen
  visade ALTCHA och lämnades orörd; publik records-API/IIIF gav originalen.
  Vol/150:s exakta UUID gav ett tomt Tree-svar och är nu analog berikning.
  S-0084/S-0156/S-0171/C-0727/A-2826–A-2830 bevarar resultatet; nästa
  breddrotation är P-0051. Kontroll: 2 311 påståenden, 1 776 Markdownposter,
  3 050 mediafiler inklusive `.gitkeep`, manifest 3 049 (1 800 exakt/
  1 221 käll-/28 citationsavgränsade, 0 olänkade) och dashboard
  473/2 311/481. P-0004 har 70 kända anor och tolv öppna slutstatusar genom
  djup 5; P-0210 har fortsatt exakt P-0336 öppen genom djup 4. Ordinarie
  kontroller passerade; ingen PDF, deployment, commit eller push skapades.
- **Batch 165 har slutläst Göta livgardes församlings B II/1 år 1876 utan
  att skapa en person eller relation.** Alla sju fulloriginal, bilderna
  `00025680_00095`–`_00101`, visar att årets åtta förda inflyttningsposter
  står på bild 95 och att följande inflyttningssidor är tomma. Ingen säker
  Olaus/Olof Fredberg/Fredriksson finns. Katalogens reservation att längden
  bara omfattar personer som inte är upptagna i rekrytrullorna gör detta
  till ett komplett bok- och årsnoll, inte ett person-, Stockholms-,
  förbands- eller tjänstgöringsnoll. Tillsammans med B I/2 försvagas
  Göta-församlingshypotesen. Extern inloggad Chrome omdirigerade trots
  åtkomst utanför sandboxen volym 198:s permanenta länk till ALTCHA;
  kryssrutan lämnades orörd. Publik `Tree/SubTree` för 198/240/241 gav inga
  bildfilsbarn, medan API/JSON-LD/OAI/IIIF gav B II/1. S-0560/C-0726/
  A-2823–A-2825 bevarar resultatet; nästa breddrotation är P-0423.
  Kontroll: 2 306 påståenden, 1 773 Markdownposter, 3 040 mediafiler
  inklusive `.gitkeep`, manifest 3 039 (1 796 exakt/1 215 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 471/2 306/479. Ordinarie
  kontroller passerade; ingen PDF, deployment, commit eller push skapades.
- **Batch 164 har avgränsat Halla–Björnlunda-spåret utan att skapa en
  föräldrarelation.** Halla C/2:s 9-julifönster 1822, bilderna
  `C0006543_00081`–`_00082`, saknar Carl Eric/Fredric 1822-07-09 och
  står i konflikt med Bettna A I/11 a:s senare uppgift utan att bli
  personnoll. Halla B/1 har 1839 `Drängen Carl Eric Carlsson` från Ellesta
  till Björnlunda; Ellesta s. 37–40 saknar motsvarande hushållsrad.
  Björnlunda A I/11:s OCR-nominerade träffar kontrollerades visuellt;
  bild 189:s Eric Carlsson är född 1820-08-10 och avvisas, men inget
  helvolymsnoll skapas. Extern inloggad Chrome utanför sandboxen visade
  ändå ALTCHA på den äldre katalogposten; den lämnades orörd. Publik
  `Tree/SubTree` och IIIF gav volymen utan interaktion. S-0559/C-0725/
  A-2819–A-2822, 14 fulloriginal och 13 metadataoriginal bevarar
  resultatet. Den senare C-0798 rättar helårstolkningen genom den positiva
  födelsen 9 april och modern Ella Ersdotter. 1852–1875-glappet var då öppet.
  Kontroll: 2 303 påståenden, 1 770 Markdownposter, 3 027 mediafiler
  inklusive `.gitkeep`, manifest 3 026 (1 786 exakt/1 212 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 471/2 303/479. Ordinarie
  kontroller passerade; ingen PDF, deployment, commit eller push skapades.
- **Batch 163 har läst Piteå landsförsamling E I/3:s kompletta
  vigselföljd 1810–1818 utan att skapa en farrelation.** Manifestets
  årsgränser gör bilderna `71000569_00020`–`_00060` till det exakta
  41-bildersintervallet; samtliga fulloriginal hämtades och lästes.
  Extern Chrome öppnade och hämtade den exakta bildrouten utan CAPTCHA.
  Den publika IIIF-routen fungerade därefter utanför nätverkssandboxen med
  varje canvas faktiska manifestbredd och bildvisaren som `Referer`.
  Ingen säker Olaus/Olof Pehrsson eller Persson motsvarande mannen född
  1784-02-07 i Överklinten finns i intervallet. Bild 38:s närform är Eric
  Pehrsson yngre, och övriga Olof-rader har andra patronymikon eller
  släktnamn. Resultatet är ett strikt serie-, församlings- och tidsbundet
  vigselnoll, inte vistelse-, senare vigsel-, frånvaro- eller
  faderskapsbelägg. Volymanmärkningen säger att luckan 1819–1826-10-07 har
  rekonstruerats; den senare E I/3-routen måste behandlas därefter.
  S-0558/C-0724/A-2817–A-2818 och 41 fulloriginal bevarar resultatet.
  T-0012 förblir `ONGOING`/`DOING`; nästa breddrotation är P-0133.
  Kontroll: 2 299 påståenden, 1 768 Markdownposter, 3 000 mediafiler
  inklusive `.gitkeep`, manifest 2 999 (1 772 exakt/1 199 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 471/2 299/479. Ordinarie
  kontroller och originalens checksummor passerade; auditerna har fortsatt
  elva öppna slutstatusar genom P-0004:s djup 5 och exakt P-0336 öppen
  genom P-0210:s djup 4. Ingen PDF, deployment, commit eller push skapades.
- **Batch 162 har läst SCB:s kompletta Sävarutdrag 1860 utan att
  konstruera ett personnoll eller en flytt.** Records-API, JSON-LD, OAI-EAD
  och IIIF identifierade `SE/RA/420401/03/H 1 A/103`, permanent id
  `tNSW3OgRrH6d0G02H087k3`, reproduktion `A0056108`. Manifestets
  Sävarrange är bilderna `_00421`–`_00473`, före Holmön `_00474`; alla 53
  fulloriginal kontrollerades. Den visuellt lästa födelseårskolumnen saknar
  den förväntade sammanhängande profilen Johan Peter 1825, Sara Sophia 1829
  och barnen 1851/1853/1854/1856/1858. Lokal OCR bar endast
  kandidatnavigeringen. Resultatet är ett komplett utdrags- och
  kombinationsnoll, inte personnoll, flyttbelägg eller stöd för annan
  församling; A I/5b:s positiva hushåll står kvar. Publik API/IIIF fungerade
  utan sessionskaka med normal `User-Agent` och Riksarkivet-`Referer`;
  Chrome och CAPTCHA/ALTCHA behövdes inte. S-0557/C-0723/A-2815–A-2816,
  53 fulloriginal och fyra metadataoriginal bevarar resultatet. T-0012
  förblir `ONGOING`/`DOING`; nästa breddrotation är P-0051. Kontroll:
  2 297 påståenden, 1 766 Markdownposter, 2 959 mediafiler inklusive
  `.gitkeep`, manifest 2 958 (1 731 exakt/1 199 käll-/28
  citationsavgränsade, 0 olänkade) och dashboard 471/2 297/479. Ordinarie
  kontroller passerade; auditerna har fortsatt elva öppna slutstatusar genom
  P-0004:s djup 5 och exakt P-0336 öppen genom P-0210:s djup 4. Ingen PDF,
  deployment, commit eller push skapades.
- **Batch 161 har prövat den verkliga Chrome-vägen och avvisat tre
  Göta-kandidater utan att skapa ett personnoll.** Den exakta permanenta
  routen till analoga namnregister 198 visade ALTCHA även i inloggad Chrome
  utanför sandboxen; ingen kontroll aktiverades. Omdirigeringen gav
  Arkis-identifieraren `ee04c964-05da-4b86-8727-b5c0ccd5d2f7`, men ett
  publikt batchanrop gav bara felsida. Volym 194:s IIIF fungerade utan
  session. En maskinassisterad screen av rullbilderna 4–435 nominerade Per
  Alexander Svensson, Carl Olaus Carlsson och Johan Olsson Fredberg; alla
  tre avvisades i fulloriginal genom namn, födelsedatum och värvningsdatum.
  OCR kan missa handskrift, så inget fullvolyms-, person- eller förbandsnoll
  skapades. S-0550/C-0722/A-2813–A-2814 samt tre fulloriginal och ett
  åtkomstoriginal bevarar resultatet. T-0012 förblir `ONGOING`/`DOING` och
  nästa breddrotation är P-0423. Kontroll: 2 295 påståenden, 1 764
  Markdownposter, 2 902 mediafiler inklusive `.gitkeep`, manifest 2 901
  (1 678 exakt/1 195 käll-/28 citationsavgränsade, 0 olänkade) och
  dashboard 471/2 295/479. Ordinarie kontroller passerade; auditerna har
  fortsatt elva öppna slutstatusar genom P-0004:s djup 5 och exakt P-0336
  öppen genom P-0210:s djup 4. Ingen PDF, deployment, commit eller push
  skapades.
- **Batch 160 har följt Johanna Jansdotter från Bettna tillbaka till hennes
  födelsefamilj utan att överbrygga Erik Karlssons identitetsglapp.** Stora
  Malm B/1 bild `C0007583_00018` ger hennes reciproka utflyttning 1841 från
  Backstugan till Bettna; dagfältet är tomt. C/6 bild `C0007590_00021`
  anger födelsen 1819-05-30, dopet 31 maj och föräldrarna Jan Ericson och
  Lena Jonsdotter i Walla. A I/13 a sida 80 placerar samma dotter och
  föräldrapar i Walla. Den externa, inloggade Chrome-sessionen visade
  ALTCHA både på exakt post och vanlig sökning utanför sandboxen; ingen
  kontroll aktiverades. Publik Arkis-batch och IIIF fungerade utan
  sessionskaka. S-0556/C-0721/A-2810–A-2812 bevarar resultatet. Luckan
  1852–1875 återstår, så ingen person eller relation skapades. Kontroll:
  2 293 påståenden, 1 763 Markdownposter, 2 898 mediafiler inklusive
  `.gitkeep`, manifest 2 897 (1 674 exakt/1 195 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 471/2 293/479. T-0012
  förblir `ONGOING`/`DOING`; nästa breddrotation är P-0336.
- **Batch 159 har slutläst Olausspårets digitala dödbok utan att skapa
  Barbros far.** Piteå landsförsamling F/1:s hela manifestavgränsade
  död- och begravningsföljd 1808–1819-05-15, `C0035068_00010`–`_00071`,
  saknar en säker Olaus/Olof Pehrsson/Persson som motsvarar mannen född
  1784-02-07 i Överklinten. Alla 62 fulloriginal lästes sida för sida.
  Resultatet är endast serie-, församlings- och tidsbundet och säger inget
  säkert om vistelse, vigsel, senare liv eller Barbros faderskap. Extern
  Chrome gav fullstor bildnedladdning utan CAPTCHA; direkt IIIF-bildbegäran
  gav `403`. Den separata bouppteckningssökningen visade ändå ALTCHA utanför
  sandboxen och lämnades orörd. S-0555/C-0720/A-2809 bevarar resultatet.
  Kontroll: 2 290 påståenden, 1 761 Markdownposter, 2 883 mediafiler
  inklusive `.gitkeep`, manifest 2 882 (1 671 exakt/1 183 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 471/2 290/479. Ingen person
  eller relation skapades. T-0012 förblir `ONGOING`/`DOING`; nästa
  breddrotation är P-0133.
- **Batch 158 har gjort P-0336:s mantals- och bouppteckningsvägar exakta
  utan personläsning.** Älvsborgs landskontor 551–554 ger analoga
  mantalsrutter 1852–1853. Bjärke häradsrätt F II a/9 täcker
  bouppteckningar 1849–1855 och personregistret är exakt
  `SE/RA/870001/3/15/19`, men ingen reproduktionskod, IIIF-URL eller
  personrad kunde läsas. Extern Chrome visade ALTCHA även utanför sandboxen;
  den lämnades orörd. S-0554/C-0719/A-2805–A-2808 och fjorton
  metadataoriginal bevarar routingen utan frånvarobelägg.
- **Batch 157 förlängde Grillfamiljen bakåt och gav en ny lysningsroute;
  dess militära slutsats är rättad av batch 190.** Bettna A I/11 a sida 33
  placerar Carl Eric Grill, Johanna Jonsdotter och sonen Carl Johan vid
  Glippsta soldattorp 1841–1845. Stora Malm E I/2 har en överstruken
  1841-notis för `Carl Fredric Grill` och Johanna Jansdotter med
  Södermanlands regemente nummer 36 i Björkviks församling men utan
  vigseldag. Hela vigselföljden 1840–1843 i Bettna och vigselåret 1841 i
  Björkvik saknar paret. Den dåvarande slutsatsen att samtliga åtta
  kompaninummer 36 avsåg andra män är nu `REJECTED`: maxoriginalet visar
  Carl Fredric Drill på Livkompaniets Glippsta nr 36; sju rader gäller
  andra män. Extern Chrome prövades uttryckligen men Riksarkivet visade
  ALTCHA både på exakt katalogroute och Grill-formuläret; den lämnades
  orörd. Publika UUID-/batch-/IIIF-vägar fungerade utan sessionskaka.
  S-0553/C-0718/A-2799–A-2804, 24 fulloriginal och 26 metadataoriginal
  bevarar den historiska passagen; S-0592/C-0763 bär rättelsen. Kontroll
  efter batch 157 var 2 285 påståenden, 1 757 Markdownposter,
  2 807 mediafiler inklusive `.gitkeep`, manifest 2 806 (1 609 exakt/
  1 169 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  471/2 285/479. Ingen person eller relation skapades. T-0012 förblir
  `ONGOING`/`DOING`; nästa breddrotation är P-0336.
- **Batch 156 har identifierat Olaus exakt och öppnat Piteåspåret utan att
  konstruera Barbros far.** Bygdeå C/3 bild `C0034039_00023` anger Olaus
  född 1784-02-07 i Överklinten som son till Pehr Johansson och Anna Cajsa
  Olofsdotter. På hans rad i A I/6:s 1805-kolumner kan `Piteå` läsas; den
  föregående förkortningen lämnas oläst. Piteå landsförsamlings kompletta
  vigselår 1805–1809 och dödår 1805–1807 samt stadsförsamlingens separata
  ministerialföljd 1805 saknar en säker Olaus/Olof Pehrsson/Persson. Det är
  endast serie-, års- och församlingsbundna noll. H II/1:s 647 oregelbundet
  ordnade flyttningsbilagebilder kräver personregistret i arkivexpeditionen
  eller en ny dokumentnyckel; F/1:s strukturerade dödår 1808–1819 är nästa
  digitala route och är ännu olästa. Chrome/session användes inte. En
  katalog-CAPTCHA lämnades orörd och Riksarkivets publika arkivträd gav
  reproduktionskoderna. S-0552/C-0716–C-0717/A-2792–A-2798, 36
  fulloriginal och 20 metadataoriginal bevarar resultatet. Totalt: 2 279
  påståenden, 1 755 Markdownposter, 2 757 filer i mediakatalogen inklusive
  `.gitkeep`, manifest 2 756 (1 585 exakt/1 143 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 471/2 279/479. Alla ordinarie
  kontroller passerade; auditerna har fortsatt elva öppna slutstatusar genom
  djup 5 och exakt P-0336 öppen genom P-0210:s djup 4. T-0012 förblir
  aktiv, ingen PDF ändrades och nästa breddrotation är P-0133.
- **Batch 155 har avgränsat alla manifestdefinierade SCB-dödsranger i
  Västerbotten 1868 kring P-0423:s konfliktsatta dödsdag utan att konstruera
  dödsort eller säker dag.** Det bevarade records-API-svaret, JSON-LD,
  OAI-EAD och IIIF Presentation 3-manifestet för
  `SE/RA/420401/01/H 1 AA/304`, reproduktion `A0035803`, namnger 27
  församlingsranger. Sävar och fyra alternativa församlingar var tidigare
  lästa. De 22 återstående rangerna har nu var sin maximal originalbild som
  innehåller eller synligt omsluter 14 augusti. Ingen namnger Sara Sophia
  Pehrsdotter/Persdotter eller Zingmark; exakta 14/8-poster i sex
  församlingar avser andra personer. Resultatet är datumfönsterbundet, inte
  fulla församlingsår, Sverige-/läns-/personnoll eller ett oberoende original.
  Chrome/session behövdes inte. S-0551/C-0715/A-2789–A-2791 och 22
  fulloriginal. Totalt: 2 272 påståenden, 1 752 Markdownposter, 2 701 filer
  i mediakatalogen inklusive `.gitkeep`, manifest 2 700 (1 549 exakt/1 123
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 272/479. Alla
  ordinarie kontroller passerade; auditerna har fortsatt elva öppna
  slutstatusar genom djup 5 och exakt P-0336 öppen genom P-0210:s djup 4.
  T-0012 förblir aktiv, ingen PDF ändrades och nästa breddrotation är P-0051.
- **Batch 154 har gjort P-0336:s livgardesväg och bild-API-diagnos exakta
  utan att konstruera militärt förband eller identitet.** Records-API,
  JSON-LD, OAI-EAD och IIIF identifierade Svea livgardes församlings A I b/8,
  `SE/SSA/0005E/A I b/8`, 1847–1876, reproduktion `00025805`. Första
  registret gäller 1857–1860; det andra, odaterade registrets fulla
  F-avsnitt saknar Fredberg och Fredriksson. Detta är bara ett registerblads-
  och namnformsnoll. Records-API:t gav WAF utan normal User-Agent men korrekt
  JSON med `Mozilla/5.0`; samma maxbild gav `200 image/jpeg` i tre
  header-varianter utan sessionskaka. Bild-API:t var alltså inte blockerat
  för den prövade källan, och Chrome/session behövdes inte. Svea fond-OAI och
  tio JSON-LD-poster ger prioriterade analoga kompanirutter. Göta 194 är
  digital med 436 bilder; bara pärm, första uppslag och manifeststruktur är
  lästa. Namnregister 198, rekryteringsjournal 240 och avskedsjournalerna i
  241 är analoga, vilket ger återstarten 198 → 194 → 240/241 → kompanivisa
  rullor utan personnoll. S-0550/C-0714/A-2784–A-2788, sex fulloriginal och
  26 metadata-/diagnosoriginal. Totalt: 2 269 påståenden, 1 750
  Markdownposter, 2 679 filer i mediakatalogen inklusive `.gitkeep`, manifest
  2 678 (1 527 exakt/1 123 käll-/28 citationsavgränsade, 0 olänkade),
  dashboard 471/2 269/479. Alla ordinarie kontroller passerade; auditerna har
  fortsatt 11 öppna slutstatusar genom djup 5 och exakt P-0336 öppen genom
  djup 4. T-0012 förblir aktiv, ingen PDF ändrades och nästa breddrotation är
  P-0423.
- **Batch 153 har utvidgat P-0133:s nummer-36-kontroll till två alternativa
  militära indelningar utan att skapa identitet eller föräldrarelation.**
  TORA binder Glippsta till Bettna församling och namnger Södermanlands
  regemente 04, Livregementets grenadjärer 04 och Livregementets husarer 04
  som församlingsvisa relationer. De är daterade `0–9999` och binder inte
  Glippsta, 1851 eller Carl Erik Grill till ett förband. Records-API,
  OAI-EAD och IIIF identifierade generalmönsterrulla 226, reproduktion
  `A0028201`, för grenadjärkåren 1848/1851 och rulla 832, reproduktion
  `A0028846`, för husarerna 1851. Nummer 36 i grenadjärkårens fyra kompanier
  båda åren och husarernas fem skvadroner 1851 avser andra män eller en
  administrativt indragen rad. Resultatet avvisar bara de tretton prövade
  nummer-/förbands-/årshypoteserna; annat nummersystem, år eller förband,
  Grills WAF-spärrade ortsrouting och identitetsgapet 1852–1875 förblir
  öppna. Chrome/session behövdes inte och ingen CAPTCHA/ALTCHA interagerades
  med. S-0549/C-0713/A-2781–A-2783, tretton fulloriginal och tio
  metadataoriginal. Totalt: 2 264 påståenden, 1 748 Markdownposter, 2 647
  filer i mediakatalogen inklusive `.gitkeep`, manifest 2 646 (1 521
  exakt/1 097 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  471/2 264/479. Alla ordinarie kontroller passerade; auditerna har fortsatt
  11 öppna slutstatusar genom djup 5 och exakt P-0336 öppen genom djup 4.
  T-0012 förblir aktiv, ingen PDF ändrades och nästa breddrotation är P-0336.
- **Batch 152 har avgränsat Olausspåret på de registrerade
  Överklinten-sidorna utan att avvisa kandidaten eller konstruera en far.**
  A I-seriens JSON-LD, exakta OAI-poster, Riksarkivets publika arkivträd
  och IIIF identifierade A I/8, `SE/HLA/1010025/A I/8`, id
  `hsMd6Qtq9KUcg16xgv9pp3`, reproduktion `C0034017`, samt A I/9,
  `SE/HLA/1010025/A I/9`, id `EvNzXFMJu2H1XYnmmTeZ53`, reproduktion
  `C0034018`. Volymregistren routar Överklinten till sida 295 respektive
  sida 185. A I/8:s bild 300 är tom trots sidetiketten 295; bild 301 bär
  det faktiska ortsuppslaget. De två ortssidorna saknar Olaus född 1784 och
  Barbro/Barbru född 1830. A I/9:s `Son Olaus` är född 1819 och en annan
  generation. A I/7a saknar säkert läsbar destination och A I/9 är märkt
  defekt, så resultatet är bara ett ortssidesnoll, inte helvolyms-,
  destinations-, person- eller faderskapsnoll. Ingen person eller relation
  skapades. En bred records-fråga och ett första OAI-anrop gav WAF, men de
  exakta API/OAI/JSON-LD/IIIF-rutterna fungerade; Chrome/CAPTCHA användes
  inte. S-0548/C-0712/A-2778–A-2780, fem fulloriginal och nio
  metadataoriginal. Totalt: 2 261 påståenden, 1 746 Markdownposter, 2 624
  filer i mediakatalogen inklusive `.gitkeep`, manifest 2 623 (1 508
  exakt/1 087 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  471/2 261/479. Alla ordinarie kontroller passerade; auditerna har fortsatt
  11 öppna slutstatusar genom djup 5 och exakt P-0336 öppen genom djup 4.
  T-0012 förblir aktiv, ingen PDF ändrades och nästa breddrotation är P-0133.
- **Batch 151 har avgränsat fyra alternativa SCB-dödsfönster för P-0423
  utan att konstruera en dödsort.** Det bevarade IIIF-manifestet för
  SCB:s Västerbottensvolym 1868 routade fullbilder kring 14 augusti i Umeå
  landsförsamling, Vindeln/tidigare Degerfors, Bygdeå och Lycksele.
  Bilderna `_00193`, `_00219`, `_00232` och `_00314` saknar Sara Sophia
  Pehrsdotter/Persdotter/Zingmark. Enda lästa posten exakt 14 augusti är
  Degerfors nr 65, en flicka Sofia, 3 år 10 månader 25 dagar. Resultatet är
  bara ett fyrbilders- och namnformsbundet källnoll; fulla församlingsår,
  andra församlingar och sent införda rader är inte stängda, och
  SCB-utdragen är inte oberoende original. Ingen alternativ dödsort eller
  dödsdag identifierades. Chrome/CAPTCHA användes inte.
  S-0547/C-0711/A-2775–A-2777 och fyra fulloriginal. Totalt: 2 258
  påståenden, 1 744 Markdownposter, 2 610 filer i mediakatalogen inklusive
  `.gitkeep`, manifest 2 609 (1 494 exakt/1 087 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 471/2 258/479. Alla
  ordinarie kontroller passerade; auditerna har fortsatt 11 öppna
  slutstatusar genom djup 5 och exakt P-0336 öppen genom djup 4. T-0012
  förblir aktiv, ingen PDF ändrades och nästa breddrotation är P-0051.
- **Batch 150 har gjort C:394 till en exakt analog berikningsväg för
  P-0338 utan att påstå personinnehåll.** Riksarkivets fond
  `SE/HLA/3010533`, *By- och släkthandlingar, Ljustorps sn*, är ett
  selektivt Edén-arkiv som i första hand rör bland annat Lagfors. Volym 2:s
  mantals-/skatte- och taxeringslängder överlappar Henriks torparår. Volym
  3:s bouppteckningar slutar 1883, året före hans död, men
  auktionsprotokoll, arvskiften/testamenten och fyrktalslängder sträcker sig
  över 1884. Volym 4:s kommunalstämmomaterial når dödsåret. Allt är spridda
  år och ännu personoläst. Records-API/OAI/JSON-LD visar endast analog
  instansiering; Chrome/CAPTCHA användes inte. S-0546/C-0710/A-2771–A-2774
  och åtta metadataoriginal. Totalt: 2 255 påståenden, 1 742
  Markdownposter, 2 606 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 2 605 (1 490 exakt/1 087 käll-/28 citationsavgränsade,
  0 olänkade), dashboard 471/2 255/479. Alla ordinarie kontroller
  passerade; auditerna har fortsatt 11 öppna slutstatusar genom djup 5 och
  exakt P-0336 öppen genom djup 4. T-0012 förblir aktiv, ingen PDF ändrades
  och nästa breddrotation är P-0423.
- **Batch 149 har avgränsat P-0336:s digitala konfirmationskälla men funnit
  en kritisk Stora Lundby-lucka 1869.** Fond-OAI, records-API, volym-OAI,
  JSON-LD och IIIF identifierade D I/2, `SE/GLA/13505/D I/2`, 1839–1879,
  reproduktion `00079197`, samt D I/3, 1869–1878, reproduktion `00079430`.
  D I/2 bilder 66–80 och D I/3 bilder 9–10 täcker de manifestdefinierade
  listorna för Stora Lundby/Skallsjö/Lerum 1865–1868 och 1870–1873 samt
  Skallsjö/Lerum 1869. De 17 fulloriginalen saknar säker Olaus
  Fredriksson/Fredberg och båda källburna datumen, men Stora Lundby 1869
  saknas i båda manifesten och förblir en exakt digital källucka. Resultatet
  är bara ett avgränsat konfirmationskällnoll och löser varken födelse,
  datumkonflikt eller föräldrahypotes. Ingen person eller relation skapades.
  Chrome/CAPTCHA användes inte. S-0545/C-0709/A-2768–A-2770, 17
  fulloriginal och nio metadataoriginal. Totalt: 2 251 påståenden, 1 740
  Markdownposter, 2 598 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 2 597 (1 482 exakt/1 087 käll-/28 citationsavgränsade,
  0 olänkade), dashboard 471/2 251/479. Alla ordinarie kontroller
  passerade; auditerna har fortsatt 11 öppna slutstatusar genom djup 5 och
  exakt P-0336 öppen genom djup 4. T-0012 förblir aktiv, ingen PDF ändrades
  och nästa breddrotation är P-0338.
- **Batch 148 har avvisat exakt hypotesen att Glippsta-längdens `36` är
  Carl Erik Grills kompaninummer i Södermanlands regemente.** 1851 års
  generalmönsterrulla, `SE/KrA/0023/0/162`, delar sig via IIIF-manifestet i
  åtta kompanier. Nummer 36 lästes i samtliga och avser varje gång en annan
  man. Riksarkivets egen guide visar samtidigt att regements-, kompani- och
  rote-/rusthållsnummer måste hållas isär; fyndet är alltså inte ett
  soldat-, person-, familje- eller förbandsövergripande noll. Grills
  specialregister är den exakta ortsroutern, men Bettna-GET stoppades av
  `403 Web Application Firewall`. Ingen resultatlista lästes, Chrome
  användes inte och ingen ALTCHA/CAPTCHA interagerades med. S-0544/C-0708/
  A-2765–A-2767, åtta rullbilder och tre metadataoriginal. Totalt: 2 248
  påståenden, 1 738 Markdownposter, 2 572 filer i mediakatalogen inklusive
  `.gitkeep`, manifest 2 571 (1 456 exakt/1 087 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 471/2 248/479. Alla
  ordinarie kontroller passerade; auditerna har fortsatt 11 öppna
  slutstatusar genom djup 5 och exakt P-0336 öppen genom djup 4. Ingen
  person, relation eller PDF ändrades. T-0012 förblir aktiv; nästa
  breddrotation är P-0336.
- **Batch 147 har identifierat C. E. Lundberg från Lugnet tillbaka till
  födelsefamiljen i Överklinten utan att konstruera Barbros föräldrar.**
  A I/12b sida 330 och A I/13b sida 480 följer samma hushåll 1846–1862
  och rättar den tidigare A I/13a-felroutingen. C/3:s födelsenotis samt
  A I/6 sida 71 och A I/7a sida 116 binder Carl Eric, född 1806-10-14 i
  Överklinten, till Pehr Johansson och Anna Catharina/Anna Cajsa
  Olofsdotter. Lugnetlängderna anger 13 oktober och moderns födelseår står
  i spänning till födelsenotisens ålder; båda konflikterna lämnas öppna.
  De äldre längderna namnger brodern Olaus, född 1784, som konkret men
  obevisad kandidatväg bakom Barbros patronymikon. Eftersom maken Anders
  Anderssons far är Anders Nilsson pekar det bokstavliga
  `farbrodern`-ordet starkt mot Barbros sida, men ingen biologisk relation
  skapades. Records-API, JSON-LD, publikt arkivträd och IIIF användes;
  Chrome/CAPTCHA användes inte. S-0543/C-0707/A-2761–A-2764, fem
  fulloriginal och tio metadataoriginal. Totalt: 2 245 påståenden, 1 736
  Markdownposter, 2 561 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 2 560 (1 445 exakt/1 087 käll-/28 citationsavgränsade,
  0 olänkade), dashboard 471/2 245/479. Ordinarie data-, test-, pedigree-,
  djup-5-, utgåvemanifest-, dashboard-, produktionsbygg- och diffkontroller
  passerade. Auditerna har fortsatt 11 öppna slutstatusar genom djup 5
  respektive exakt P-0336 öppen genom djup 4. T-0012 förblir aktiv; nästa
  breddrotation är P-0133 och ingen PDF ändrades.
- **Batch 146 har slutläst SCB:s Sävarutdrag 1868 och rättat
  mantalsfronten för P-0423.** Records-API/OAI/JSON-LD identifierade
  `SE/RA/420401/01/H 1 AA/304`, id `qnJL2ugRrH6d0G02H087k3`, och IIIF
  `A0035803`. Sävar döda avgränsas av Presentation API 3-rangerna till
  bilder 206–214 före Holmön på 215. Alla nio blad, poster 1–158, saknar
  Sara Sophia; den numrerade följden går från 11 till 16 augusti utan post
  den 14:e. Eftersom SCB är en samtida parallell avskrift stärks men löses
  inte konflikten mot A I/6b:s 1868-08-14. Umeå fögderis kompletta OAI-EAD
  visar dessutom den tidigare förbisedda `SE/HLA/1100016/Vol/150`, Sävar
  1849–1858. Den är endast analog och oläst men nu första exakta
  beställningsroute före A I/5b. Sävars H V/H VI/K IV c saknar
  katalogiserade målårsbilagor; ingen händelsefrånvaro infereras.
  S-0541–S-0542/C-0705–C-0706/A-2758–A-2760, nio fulloriginal och nio
  metadataoriginal. Totalt: 2 241 påståenden, 1 734 Markdownposter,
  2 546 filer i mediakatalogen inklusive `.gitkeep`, manifest 2 545
  (1 430 exakt/1 087 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  471/2 241/479. Chrome användes inte och ingen CAPTCHA/ALTCHA
  interagerades med. Ingen person, relation eller PDF ändrades. T-0012
  förblir aktiv; nästa rotation är P-0051.
- **Batch 145 har avgränsat P-0338:s bouppteckningsväg och löst den
  saknade bild-URI:n.** Records-API hittade registervolymen
  `SE/RA/870001/3/22/34`, men JSON-LD:s två bildinstansieringar saknade
  URI. Inloggad Chrome användes endast för diagnos; den orörda
  ALTCHA-omdirigeringen exponerade Arkis-id
  `5da3f6bc-8ffb-4648-a910-07913f8c6360`, varefter Riksarkivets publika
  batchsida gav `A0043220` och `C0103777`. Ingen ALTCHA aktiverades och
  inga sessionsdata lästes. Alla fjorton personkort i den selektiva
  Ber–Per-volymen lästes utan Henrik Henriksson/Henriksson. Detta är ett
  komplett registernoll, inte ett generellt bouppteckningsnoll. F II-seriens
  första katalogiserade volym är F II/1, 1888–1892, så 1884 är en
  arkivstrukturell lucka. Bild 14 gav en separat `LEAD`: Jonas Höglin,
  torpare i Frötuna 1874, `Ljustorp P. 2 nr 7`, utan ny säker relation.
  S-0540/C-0704/A-2755–A-2757, 22 fulloriginal och sexton metadatafiler.
  Totalt: 2 238 påståenden, 1 730 Markdownposter, 2 528 filer i
  mediakatalogen inklusive `.gitkeep`, manifest 2 527 (1 421 exakt/1 078
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 238/479.
  P-0004-baslinjen är 68 och P-0210 61; auditerna har fortsatt 11 öppna
  slutstatusar genom djup 5 respektive exakt P-0336 öppen genom djup 4.
  Alla relevanta data-, käll-, dashboard- och byggkontroller passerade.
  Ingen PDF ändrades. T-0012 förblir aktiv; nästa rotation är P-0423.
- **Batch 144 har rättat 1860-personregistrets täckning och slutläst SCB:s
  Stora Lundby-utdrag för P-0336/P-0411.** Riksarkivets officiella
  registreringsbeskrivning anger att 1860-personregistret endast omfattar
  Jämtlands län; C-0523:s fråga på Johan August i Älvsborg är därför en
  historisk ALTCHA-incident men ska inte återaktiveras. Records-API,
  OAI-EAD och JSON-LD identifierar i stället SCB-volymen
  `SE/RA/420401/03/H 1 A/69`, permanent id
  `ktSW3OgRrH6d0G02H087k3`, med IIIF-manifest `A0056074`. Rangen `Stora
  Lundby 1860` börjar på bild 27 och nästa range, `Skallsjö 1860`, på bild
  45. Hela intervallet 27–44 har lästs utan kombinationen Fredric/Anna
  Britta 1824, Johan August 1849 och Olaus 1852. Detta är förenligt med
  A I/10:s `afl.53` men ger ingen destination, inget personnoll utanför
  församlingen och ingen föräldrarelation. S-0539/C-0703/A-2753–A-2754,
  18 fulloriginal och sju metadatafiler. Chrome användes inte och ingen
  CAPTCHA/ALTCHA interagerades med. Totalt: 2 235 påståenden, 1 728
  Markdownposter, 2 490 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 2 489 (1 399 exakt/1 062 käll-/28 citationsavgränsade,
  0 olänkade), dashboard 471/2 235/479. P-0004-baslinjen är 68 och P-0210
  61; auditerna har fortsatt 11 öppna slutstatusar genom djup 5 respektive
  exakt P-0336 öppen genom djup 4. Alla relevanta data-, käll-, dashboard-
  och byggkontroller passerade. Den oförändrade PDF-verifieraren kunde inte
  starta eftersom `pdfplumber` saknas; ingen PDF ändrades. T-0012 förblir
  aktiv; nästa rotation är P-0338.
- **Batch 143 rättade Bettna C/5 och öppnade en stark P-0133-kandidat utan
  föräldrakant.** Barnet fött 1851-01-30 i Glippsta soldattorp har `Gustaf
  Oscar` överstruket och `Erik` kvar. A I/12 a s. 33 och A I/13 a s. 37
  binder Grill–Jonsdotter-hushållet över volymgränsen; hela gruppen stryks
  1852. Batch 194/C-0771 har senare rättat den då preliminära läsningen
  `52 W:a V.` till `52 Östra R.`. S-0538/C-0702/A-2752, två
  fulloriginal och två IIIF-manifest. Ingen relation skapades; rotera vid
  behov tillbaka först med ny ort- eller flyttnyckel.
- **Batch 142 har avgränsat Stora Lundbys födelsebilagor och öppnat en
  ny lysningsroute för P-0336:s föräldrahypotes.** H III heter `Bilagor
  till födelseboken` men har endast H III/1 1898–1981, H III/2 1982–1988
  och H III/3 1989–1991; serien kan därför inte bära 1852-frågan. H V/2,
  `SE/GLA/13505/H V/2`, 1838–1870, är en förteckning över lysningssedlar,
  och H V/1, `SE/GLA/13505/H V/1`, 1777–1870, innehåller
  lysningshandlingar. Båda omfattar pastoratet och täcker Fredric–Anna
  Brittas säkra lysning 1849-01-28. H V/2 är endast en orienterande
  parallellkälla; ingen säker registerhänvisning till H V/1 förutsätts.
  Båda är analoga utan bildlänk och med tom OAI-`dsc`; ingen handling är
  läst och ingen föräldrarelation skapades. Den breda API-frågan mötte WAF,
  men fondfiltrerade records-API-, JSON-LD- och OAI-anrop fungerade.
  Hindret ligger före bild-API:t och Chrome/CAPTCHA användes inte.
  S-0537/C-0701/A-2749–A-2751 och tolv metadataoriginal. Totalt: 2 232
  påståenden, 1 723 Markdownposter, 2 461 filer i mediakatalogen inklusive
  `.gitkeep`, manifest 2 460 (1 377 exakt/1 055 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 471/2 232/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller inklusive PDF-kontrollen passerade. T-0012 förblir aktiv;
  nästa rotation är P-0133 och ingen PDF ändrades.
- **Batch 141 har gjort Bygdeå H III/1 till P-0051:s första
  beställningsroute för födelsekonflikten.** Records-API, JSON-LD och OAI
  identifierar `SE/HLA/1010025/H III/1`, permanent id
  `Tnml0Sz3pIV5fdMJMr9bM6`, med uttryckligt material 1829–1831 och bland
  annat rapporter från Robertsfors bruk om födda 1830–1832. Ingen handling
  eller personrad är läst och metadatan placerar inte Barbro i Robertsfors.
  API saknar bildlänk, JSON-LD visar endast analog instansiering och OAI
  saknar `dao`; hindret ligger före bild-API och Chrome/CAPTCHA användes
  inte. S-0536/C-0700/A-2746–A-2748 och fem metadataoriginal.
  Totalt: 2 229 påståenden, 1 721 Markdownposter, 2 449 filer i
  mediakatalogen inklusive `.gitkeep`, manifest 2 448 (1 365 exakt/1 055
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 229/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller inklusive PDF-kontrollen passerade. T-0012 förblir aktiv;
  nästa rotation är P-0336 och ingen PDF ändrades.
- **Batch 140 har systematiskt läst den relevanta följande
  bouppteckningssekvensen för P-0423.** Umeå F II a/13:s akt 76 är daterad
  1868-08-03, före den konfliktsatta dödsdagen. Efter rullskarven börjar
  akt `76 1/2` den 20 augusti. Varje högersidesrektum och därefter varje
  funnen aktinledning i den sammanhängande följden till sista akt 119 år
  1869 har lästs utan säker Sara Sophia Pehrsdotter/Persdotter/Zingmark som
  avliden. Resultatet är ett villkorligt sekvensnoll, inte ett helt
  volymnoll eller en verifiering av dödsdagen. IIIF-bilderna fungerade
  direkt med Riksarkivet-`Referer`; Chrome, inloggningssession och CAPTCHA
  användes inte. S-0528/C-0699/A-2744–A-2745 och nio nya kontrollbilder.
  Totalt: 2 226 påståenden, 1 719 Markdownposter, 2 444 filer i
  mediakatalogen inklusive `.gitkeep`, manifest 2 443 (1 360 exakt/1 055
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 226/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller inklusive PDF-kontrollen passerade. T-0012 förblir aktiv;
  nästa rotation är P-0051 och ingen PDF ändrades.
- **Batch 139 har avgränsat Flens lokala lysningskällor för Erik och
  Matilda 1895.** E I/1 slutar 1861 och E I/2 börjar 1905; H V/1 börjar
  1919. Ingen av dessa katalogiserade volymer täcker den säkra
  SCB-vigseln 1895-12-28. P I/1, Pålysningsböcker 1849–1926, permanent id
  `HTliVxXUWKwLP15z2zAhMF`, är den enda periodtäckande lokalvolymen i de
  prövade serierna. Den är analog utan bildlänk och OAI-`dsc` är tom;
  ingen målrad är läst. S-0535/C-0698/A-2741–A-2743 och nio nya
  metadatafiler. Chrome/CAPTCHA användes inte och ingen relation skapades.
  Totalt: 2 224 påståenden, 1 718 Markdownposter, 2 435 filer i
  mediakatalogen inklusive `.gitkeep`, manifest 2 434 (1 351 exakt/1 055
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 224/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller inklusive PDF-kontrollen passerade. T-0012 förblir aktiv;
  nästa rotation är P-0423 och ingen PDF ändrades.
- **Batch 138 har avgränsat Olaus prästbetyg och Hemsjö H V utan att
  skapa föräldrar.** Skön-vigseln 1874 rättades före forskning till brodern
  Johan August; Olaus egen Hemsjö E/1-post 1877 lästes i stället. Den anger
  `Prestbet. från Kungsholmen lämnades för mannen. Ingen attest` men
  återger inte dokumentets innehåll. JSON-LD och records-API identifierar
  `SE/GLA/13204/H V`, Bilagor till lysnings- och vigselboken, med endast
  analog instansiering och utan underliggande volym, datering eller
  bildlänk. E/1:s publika IIIF-manifest fungerar, har 52 bildytor och
  identifierar `00099267_00035` som sida 33. Hindret gäller därför en icke
  exponerad bilaga, inte ett bild-API-fel för vigselboken. OAI gav 403;
  Chrome/CAPTCHA användes inte. S-0534/C-0697/A-2738–A-2740 och fem nya
  metadatafiler. Totalt: 2 221 påståenden, 1 716 Markdownposter, 2 426 filer
  i mediakatalogen inklusive `.gitkeep`, manifest 2 425 (1 351 exakt/1 046
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 221/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller inklusive PDF-kontrollen passerade. T-0012 förblir aktiv;
  nästa rotation är P-0133 och ingen PDF ändrades.
- **Batch 137 har gjort H I/1 till exakt originalväg för C. E. Lundbergs
  skriftliga medgivande utan att skapa ett släktskap.** Bygdeå H V/1:s
  detaljerade spridda innehåll saknar 1860 och volymen avvisas. H V-serien
  hänvisar i stället enstaka 1800-talsvigselbilagor till H I/1, 1802–1891,
  som är en exakt men oläst beställningsroute. OAI saknar bildlänk och de
  närliggande reproduktionerna `C0034041`–`C0034043` är D II/1, H II/1
  och L I/1. Records-API gav WAF. Chrome användes endast för den av ägaren
  tillåtna bild-API-diagnosen och stannade på orörd ALTCHA; ingen CAPTCHA
  interagerades med. S-0533/C-0696/A-2735–A-2737 och fyra nya medier.
  Totalt: 2 218 påståenden, 1 714 Markdownposter, 2 421 filer i
  mediakatalogen inklusive `.gitkeep`, manifest 2 420 (1 351 exakt/1 041
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 218/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller inklusive PDF-kontrollen passerade. T-0012 förblir aktiv;
  nästa rotation är P-0336 och ingen PDF ändrades.
- **Batch 136 har läst hela Lyckseleåret 1829 och prövat den enda tydliga
  Sara Sophia-kandidaten utan att skapa en föräldralänk.** C/3-bilderna
  `C0034151_00132`–`_00141` omfattar hela 1829; bild 142 börjar 1830.
  Bild 137 har Sara Sophia född 1829-08-06, döpt 8 augusti, dotter till
  Mats Ersson i Rusele och Maja Greta Jonsdotter. Hon följs i A I/8a
  s. 67 och A I/9 s. 69 genom 1845 men saknas på A I/10a:s exakt
  avgränsade Ruselefolio s. 99. Sävar B/1:s hela inflyttning 1845–1849
  saknar en säker reciprok rad. Kandidatens datum och far/patronymikon
  avviker från Botsmarkuppgiftens 1829-05-21 och Pehrsdotter, så hon hålls
  separat. Publik IIIF fungerade; Chrome/CAPTCHA användes inte.
  S-0532/C-0695/A-2732–A-2734 och 25 nya medier. Totalt: 2 215
  påståenden, 1 712 Markdownposter, 2 417 filer i mediakatalogen inklusive
  `.gitkeep`, manifest 2 416 (1 347 exakt/1 041 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 471/2 215/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller inklusive PDF-kontrollen passerade. T-0012 förblir aktiv;
  nästa rotation är P-0051 och ingen PDF ändrades.
- **Batch 135 har gjort Erik Karlssons sena bouppteckningsväg exakt med
  endast Riksarkivet.** En folkräkningsfråga för 1870 stannade vid orörd
  ALTCHA och gav inget resultat; Chrome användes inte. Records-API,
  JSON-LD och OAI-EAD verifierar att Villåttinge häradsrätts fond
  `SE/ULA/11693` omfattar Helgesta. Den exakta analoga läsordningen är
  kortregistret `C II b/5`, 1933–1938, id
  `1ne7pFLAjaAWr0Z0SLNN70`, före bouppteckningsvolymen `F II/59`,
  1935–1936, id `K6LKgLnlhaQoLa0flJzzL5`. Ingen Erik-rad, akt, arvinge
  eller relation är läst eller skapad. S-0531/C-0694/A-2729–A-2731 och
  tio officiella metadatafiler. Totalt: 2 212 påståenden, 1 710
  Markdownposter, 2 392 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 2 391 (1 322 exakt/1 041 käll-/28 citationsavgränsade,
  0 olänkade), dashboard 471/2 212/479. P-0004-baslinjen är 68 med exakt
  P-0051/P-0133/P-0423 öppna på arbetsdjup 4; P-0210 har 61 anor och
  exakt P-0336 öppen. Alla ordinarie kontroller inklusive PDF-kontrollen
  passerade. T-0012 förblir aktiv; nästa rotation är P-0423 och ingen PDF
  ändrades.
- **Batch 134 har gjort Olaus Fredbergs centrala pensionsväg exakt med
  endast Riksarkivet.** Records-API, OAI-EAD och JSON-LD verifierar
  personalaktsboxen `SE/GLA/16066/F 1 A/4`, 1870–1944, `-1879: F-H`,
  direkt och utan extern inventariekälla. Pensionsarkivet
  `SE/RA/420334/057` har följts maskinellt via D, D 4 och D 4 A till den
  permanenta posten `lMLgUcG1LKcymCK2zmfly8`:
  `SE/RA/420334/057/D/D 4/D 4 A/1`, 1911–1915, `Liggare över
  pensionstagare`. Båda volymposterna har endast analog instansiering och
  ingen Olaus-post är läst eller bekräftad. D 1 A, D 3 och E 2 börjar
  senare och är inte första väg för målåret. Chrome användes endast för
  bild-API-diagnos; den inloggade katalogen stannade vid orörd ALTCHA.
  S-0530/C-0693/A-2726–A-2728 och åtta nya metadatafiler. Totalt:
  2 209 påståenden, 1 708 Markdownposter, 2 382 filer i mediakatalogen
  inklusive `.gitkeep`, manifest 2 381 (1 312 exakt/1 041 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 471/2 209/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller passerade; den oförändrade PDF:ens separata layouttest saknade
  `pdfplumber`. T-0012 förblir aktiv och ingen PDF skapades.
- **Batch 133 har säkrat giftomanstexten och Lugnet-routingen utan att
  konstruera en relation.** Bygdeå C/4 bild `C0034040_00333` läses nu
  `Farbrodern B:n C. E. Lundberg i Lugnet` med skriftligt medgivande.
  Texten står i Barbros vigselrad men identifierar inte självständigt vem
  som var brorsbarnet; ingen person eller biologisk relation skapades.
  Riksarkivets OAI-EAD placerar Lugnet i Bygdeå före överföringen till
  Burträsk 1870 och anger orten i Bygdeå A I:6 framåt. Den då gjorda
  A I/13a-registertolkningen är senare rättad i batch 147: exakt Lugnet
  ligger i A I/13b. Bygdeå E I/1:s fulla dödår 1865–1870 samt B/2:s fulla
  inflyttning 1860 och utflyttning 1870 saknar säker C. E. Lundberg men
  ger inget vistelse- eller släktskapsnoll. API/JSON-LD/OAI/IIIF
  fungerade. Den inloggade exakta by-/gårdsnamnsvägen stannade på orörd
  ALTCHA; ingen CAPTCHA interagerades med. S-0529/C-0692/A-2723–A-2725
  och 50 nya medier. Totalt: 2 206 påståenden, 1 706 Markdownposter,
  2 374 filer i mediakatalogen inklusive `.gitkeep`, manifest 2 373
  (1 311 exakt/1 034 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  471/2 206/479. P-0004-baslinjen är 68 med exakt
  P-0051/P-0133/P-0423 öppna på arbetsdjup 4; P-0210 har 61 anor och
  exakt P-0336 öppen. Alla ordinarie kontroller passerade; den
  oförändrade PDF:ens separata layouttest saknade `pdfplumber`. T-0012
  förblir aktiv och ingen PDF skapades.
- **Batch 132 har indexerat Sara Sophias dopvittnesnätverk och öppnat den
  exakta digitala bouppteckningsvolymen utan att överdriva stickprovet.**
  Omläsning av de åtta bevarade barnnotiserna gav en säkert läsbar delmängd
  1856–1864 med återkommande Botsmarkvittnen och Zingmark-/Lindgren-namn,
  men ingen uttrycklig Lycksele- eller ursprungsort. Inget släktskap
  infererades. Riksarkivets API/JSON-LD/OAI identifierar Umeå tingslags
  häradsrätt och F II a/13, 1865–1869, som exakt digital bouppteckningsroute
  med IIIF `A0071108` och 1 725 bilder. Ett heuristiskt stickprov av 21
  aktstarts-/kontrollbilder, bland annat registrerade nr 77–85, 87–90, 92
  och 107–108, saknade målet men är uttryckligen inte ett akt-, års- eller
  volymnoll. Registerfrågan returnerade orörd ALTCHA; ingen CAPTCHA
  interagerades med och Chrome behövdes inte. Sävars H II har ingen
  katalogiserad 1868-volym. S-0528/C-0690–C-0691/A-2720–A-2722 och 31 nya
  medier. Totalt: 2 203 påståenden, 1 704 Markdownposter, 2 324 filer i
  mediakatalogen inklusive `.gitkeep`, manifest 2 323 (1 306 exakt/989
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 203/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller passerade; den oförändrade PDF:ens separata layouttest saknade
  `pdfplumber`. T-0012 förblir aktiv och ingen PDF skapades.
- **Batch 131 har gjort Forssa H II/1 till P-0133:s exakta analoga
  attestväg.** Årdala H II:s exakta OAI-EAD-post har tom `dsc` och saknar
  katalogiserad volym; detta är ett beståndsgap, inte bevis att en attest
  aldrig funnits. Forssa H II/1, 1851–1890, finns hos Riksarkivet i
  Uppsala, saknar åtkomstbegränsning men har ingen digital instansiering
  eller bildlänk. Den inloggade katalogen användes bara för
  bild-API-diagnos, omdirigerade till ALTCHA och lämnades orörd; inga
  sessionsdata bevarades. Publika Tree/SubTree gav inget bildfilsbarn.
  Beställ volymen med Erik Carlsson, mottagen 1876-04-30 från Årdala till
  Stafsjön, Forssa B/3 post 14, folio 87. Volymen är oläst och inga
  föräldrar infereras. S-0527/C-0689/A-2717–A-2719 och fyra nya medier.
  Totalt: 2 200 påståenden, 1 701 Markdownposter, 2 293 filer i
  mediakatalogen inklusive `.gitkeep`, manifest 2 292 (1 302 exakt/962
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 471/2 200/479.
  P-0004-baslinjen är 68 med exakt P-0051/P-0133/P-0423 öppna på
  arbetsdjup 4; P-0210 har 61 anor och exakt P-0336 öppen. Alla ordinarie
  kontroller passerade; T-0012 förblir aktiv och ingen PDF skapades.
- **Batch 130 har gett Fredric–Anna ett positivt avflyttningsår men ingen
  mottagande ort.** A I/10:s alternativa omtagning av sida 94 visar
  `afl.53` intill det överstrukna Fredric Jacobson–Anna Britta
  Olsdotter-blocket. A I/11 sida 94–95 saknar dem och Johan/Olaus men ger
  ingen destination. Hela C/4:s födelseår 1853 saknar Olaus eller barn till
  paret; hela dödsåret saknar Fredric/Anna. Vigselregistret missar även
  parets säkra 1849-vigsel, så senare API-noll är bara täckningsbundna.
  H II/1:s andra reproduktion C0045766 avser uttryckligen 1770–1841 och är
  ingen post-1850-route. Ingen föräldrakant skapades. S-0526/C-0688/
  A-2711–A-2716 och tio nya medier. Totalt: 2 197 påståenden, 1 699
  Markdownposter, 2 289 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 2 288 (1 302 exakt/958 käll-/28 citationsavgränsade, 0
  olänkade), dashboard 471/2 197/479. P-0004-baslinjen är 68 med exakt
  P-0051/P-0133/P-0423 öppna på arbetsdjup 4; P-0210 har 61 anor och exakt
  P-0336 öppen. Alla ordinarie kontroller passerade; T-0012 förblir aktiv
  och ingen PDF skapades.
- **Batch 129 har rättat fattigvårdskatalogen och läst P-0051:s hela
  digitala fattigkassespår 1830–1853.** Riksarkivets records-API visar att
  Bygdeå L I/4 trots huvuddateringen 1805–1822 även innehåller
  `Fattigräkenskaper 1805-1853`; den tidigare antagna katalogkonflikten är
  upphävd. Alla 48 original från 1 maj 1830 till 1 maj 1853,
  `C0034046_00156`–`_00203`, är lästa och bevarade. Ingen uttrycklig
  Barbro Christina/Barbru Cajsa Olofsdotter eller säker Jomark-post finns.
  Detta är ett intervallnoll i räkenskaperna, inte bevis mot anonymt,
  kollektivt eller vårdnadshavarbokfört stöd. L III/1:s analoga strödda
  fattigvårdshandlingar 1832–1852 är en separat, oläst återstartsroute.
  Publik IIIF fungerade med Riksarkivets bildvisarsida som `Referer`; ingen
  Chrome, CAPTCHA eller sessionsdata behövdes. S-0525/C-0687/A-2710;
  A-1885 och S-0238/C-0310 är rättade. Totalt: 2 191 påståenden, 1 697
  Markdownposter, 2 279 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 2 278 (1 295 exakt/955 käll-/28 citationsavgränsade, 0
  olänkade), dashboard 471/2 191/479. P-0004-baslinjen är 68 med exakt
  P-0051/P-0133/P-0423 öppna på arbetsdjup 4; P-0210 har 61 anor och exakt
  P-0336 öppen. Alla ordinarie kontroller passerade; T-0012 förblir aktiv
  och ingen PDF skapades.
- **Batch 128 har hittat Sara Sophia Pehrsdotters tidigaste säkra
  Zingmark-hushåll och avgränsat vigsel-/flyttspåren utan att konstruera en
  vigselort.** Sävar A I/5b s. 470 ger Johan Peter och Sara Sophia med
  vigselåret 1850, datumet `24/11` och barnkedjan; den säger `Sophia
  Wilhelmina`, vilket bevaras som konflikt mot födelsebokens `Christina
  Wilhelmina`. Hela vigselföljden 1850 i både Sävar C/2 och Lycksele E I/1
  saknar paret och datumet 1850-11-24. Datumet står därför kvar som positiv
  men konfliktsatt hushållstext. Hela Sävar B/1:s inflyttning 1850–1851
  saknar säker Sara Sophia; en namnnära kvinna avvisas genom A I/4a s. 248
  som född 1830-05-07 och återflyttad till Bygdeå. Hela Botsmark s.
  340–356 i A I/4b saknar säkert målhushåll, med Bäcknäs nya s. 357 som
  bevarad gräns. Riksarkivets records-API, JSON-LD, OAI, Tree/SubTree och
  IIIF gav materialet. Chrome användes bara enligt ägarens tillåtelse för
  bild-API-diagnos; en CAPTCHA-omdirigering observerades utan interaktion,
  fliken stängdes och inga sessionsdata bevarades. S-0523–S-0524/
  C-0684–C-0686/A-2704–A-2709. Totalt: 2 190 påståenden, 1 695
  Markdownposter, 2 228 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 2 227 (1 293 exakt/906 käll-/28 citationsavgränsade, 0
  olänkade), dashboard 471/2 190/479. P-0004-baslinjen är 68 med exakt
  P-0051/P-0133/P-0423 öppna på arbetsdjup 4; P-0210 har 61 anor och exakt
  P-0336 öppen. Alla ordinarie kontroller passerade; T-0012 förblir aktiv
  och ingen PDF skapades.
- **Batch 127 har omläst och beständigt bevarat Erik Karlssons
  1875-källrygg utan att konstruera ett ursprung.** Årdala B/3:s hela
  inflyttning 1875, poster 1–53 på bilder 29–30, och Forssa B/3:s hela
  utflyttning 1875, poster 1–31 på bild 27, saknar en säker motsvarande
  Erik Karlsson/Carlsson. Årdala A I/13 s. 190 Långvik saknar honom också;
  Gustaf Albert Carlsson, född 1853-02-07 i Bettna, är en annan person.
  Flyttlängderna avgränsades och hämtades genom publika IIIF-manifest.
  A I/13:s direkta manifest/bild gav `403`, så den redan inloggade
  Riksarkivet-visaren användes som snäv reserv utan CAPTCHA eller läst
  sessionsdata. Den senare texten `från Forssa 75` står kvar som positiv
  källtext utan samtidig motsvarighet: detta är ett källryggsgap, inte ett
  vistelsenoll eller en ny födelseidentitet. S-0522/C-0683/A-2702–A-2703.
- **Batch 126 har löst Johan Peter Zingmarks födelse och föräldrar samt
  avgränsat Sara Sophias uppgivna Lycksele-födelse.** Riksarkivets äldre
  Arkis-UUID:er bands via den publika `Tree/SubTree`-slutpunkten till
  `C0034441`, `C0034426` och `C0034151` efter att JSON-LD saknat bild-URI.
  Sävar C/1 s. 91 och A I/1 s. 157 säkrar Johan Petter 1825-02-01 och
  föräldrarna P-0470 Carl Jonas Zingmark samt P-0471 Anna Sophia Holmström.
  Lycksele C/3 s. 126 saknar Sara Sophia kring uppgivna 1829-05-21; detta är
  datumfönsternoll, inte församlingsnoll. Nakna bilder gav 403 och den redan
  inloggade Riksarkivet-visaren användes som snäv reserv utan CAPTCHA eller
  sessionsdata. S-0520–S-0521/C-0681–C-0682.
- **Batch 125 har avgränsat Stora Lundby H II/1 och Lundby på Hisingens
  utflyttningsår 1873 utan att konstruera Olaus ursprung.** Endast
  Riksarkivets records-API, JSON-LD och IIIF användes; ingen Chrome
  behövdes. Stora Lundby H II/1 är digital men märkt `Kartong. Spridda
  år.`; A0062259 bilder 541–595 gav ingen säker Olaus/Fredberg eller
  Fredric–Anna Britta–Johan-grupp. Bild 555:s Olaus Olsson och bild 570:s
  Anders Bengtsson avvisas. Resultatet är ett exakt 55-bilders fönsternoll,
  inte en komplett årgång eller volym. C0045766 manifestbevarades då;
  batch 130 visar att reproduktionen uttryckligen avser 1770–1841 och
  därför inte kan bära 1853-frågan. Lundby
  på Hisingens B I/3:s hela utflyttningsföljd 1873, poster 1–116 på bilder
  90–95, saknar rätt Olaus; post 18 är Olof Fredr. Eriksson. Det är ett
  årgångsnoll för utflyttade, inte vistelsenoll. Östra Fågelviks positiva
  länsangivelse och Stora Lundbys historiska namn gör därmed Stora Lundby
  till starkare arkivrutt. S-0518–S-0519/C-0679–C-0680/A-2694–A-2695 och
  71 nya medier bevarar batchen. Totalt: 2 176 påståenden, 1 682
  Markdownposter, 2 161 mediafiler inklusive `.gitkeep`, manifest 2 160
  (1 274 exakt/858 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  469/2 176/477. P-0004-baslinjen är 66 och P-0210 har 61 kända anor med
  fortsatt exakt en öppen djup-4-spets, P-0336. T-0012 förblir aktiv;
  skapa ingen PDF.
- **Batch 124 har tagit Nybergs familj 98 ur den verifierade antavlan utan
  att radera registerspåret.** Endast Riksarkivet användes. Kompletta
  Ljustorp C/1-födelseföljder 1796, 1801 och 1804, C/2-vigslar 1819 och
  C/2-döda 1833 bär inte de uppgivna barnåren, vigseldatumet eller dödsåret.
  A I/1 och A I/3 saknar det äldre hushållet på bevarade Laxsjönssidor;
  A I/2:s förstörda sida 15 är en uttrycklig lucka, inte ett noll.
  P-0461–P-0462 finns kvar som `CONFLICT`-personer men deras relationer till
  P-0451 är märkta `uppgiven` och räknas inte längre som föräldrakantsbelägg.
  P-0451:s äldre föräldrar och födelseort är öppna tills en positiv
  originalrad hittas. Bild-API-problemet är samtidigt löst metodiskt:
  Riksarkivets äldre `C003…`-manifest ger 403 naket men 200 när den
  motsvarande `sok.riksarkivet.se/bildvisning/<bild-id>` skickas som
  `Referer`; inga kakor behöver exporteras. S-0517/C-0678/A-2688–A-2693
  och 41 nya medier bevarar batchen. Totalt: 2 174 påståenden, 1 678
  Markdownposter, 2 090 mediafiler inklusive `.gitkeep`, manifest 2 089
  (1 258 exakt/803 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  469/2 174/477. P-0004-baslinjen är 66 och P-0210 har 61 kända anor men
  fortsatt bara P-0336 som öppen djup-4-spets. Ordinarie kontroller
  passerade; PDF-layoutkontrollens Python-paket saknas lokalt och ingen PDF
  ändrades. T-0012 förblir aktiv; rotera breddfronten och skapa ingen PDF.
- **Batch 123 har bevarat P-0247 Gertrud Kristina
  Jönsson/Henriksson/Hallins födelsekonflikt, andra familj och livskedja
  till 1951 samt avgränsat det senare bildhindret.** Endast Riksarkivet
  användes. Hela Sättna C/5 och det beroende SCB-avsnittet 1874 saknar
  hennes egen födelsenotis trots fem senare samstämmiga original för
  1874-02-23 och Abraham Jönsson/Stina Kajsa Nordlund; konflikten får inte
  harmoniseras bort. A II a/4 säkrar omgifte 1918-03-09 med nya P-0467
  Nils August Hallin och tillför P-0468 Nils Eugen samt P-0469 Ivar
  Henning. A II b/1 och A II a/6 s. 389/392 leder vidare till A II a/8
  s. 388: Nils dödnoteras 1951-06-18 och Gertrud hänvisas till nya boken
  s. 304. API-metadata identifierar den som A II a/10, 1951–1971, men
  sidan är oläst. Sättna F/1–F/2 saknar säker Gertrud 1927–1943 och
  1952–1955; därefter visas restriktionsblad. F/2:s 1951-följd saknar
  säker Nils, så ingen dödsort sluts av marginalnoteringen. Bild-API-
  diagnosen är specifik: kända A II b/1/A II a/6/A II a/8-bilder är
  sessionsskyddade, medan A II a/10 redan saknar publikt reproduktions-id
  i sök-API/JSON-LD/OAI. Den inloggade katalogposten leder till orörd
  människoverifiering och en sekvenskandidat gav `Not Found`. Återstart:
  A II a/10 s. 304 när Riksarkivet exponerar ett giltigt bild-id utan att
  verifieringen behöver röras. S-0513–S-0516/C-0674–C-0677/P-0467–P-0469/
  A-2675–A-2687 och 25 nya sakmedier bevarar batchen. Totalt: 2 168
  påståenden, 1 676 Markdownposter, 2 049 mediafiler inklusive `.gitkeep`,
  manifest 2 048 (1 217 exakt/803 käll-/28 citationsavgränsade, 0
  olänkade), dashboard 469/2 168/479. Alla ordinarie tester, bygge,
  pedigree-, edition-, JSON- och manifestkontroller passerade; P-0210 har
  fortsatt exakt en öppen djup-4-spets, P-0336. T-0012 förblir aktiv och
  breddfronten ska rotera; skapa inte en ny PDF.
- **Batch 122 har bundit Johan August till Anna Brita och hennes make
  Fredric Jacobson utan att överskriva födelsepostens faderskonflikt.**
  Endast Riksarkivet användes, via API och IIIF; ingen Chrome-session
  behövdes. Stora Lundby C/4 ger Fredric Jacobson och Anna Britta Olsdotter
  vigda 1849-04-15 efter lysning 28 januari. A I/10 s. 115 visar Anna med
  den indragna raden Johan August, född 1849-07-05, och hänvisningen till
  s. 94, där Fredric står med hustrun Anna Britta. C-0521:s högupplösta
  födelsepost namnger samtidigt `Olo Andersson i Hjällsnäs Såg` som Johans
  far. Olo står därför kvar som uppgiven far och Fredric som moderns
  dokumenterade make; biologisk, legal och social fadersroll är olösta.
  Hela Stora Lundby B/2:s utflyttningsföljd 1853 och tre
  födelseregisterfrågor gav snävt avgränsade noll. C-0522/S-0414 är
  rättade så att hushållsnollet inte döljer de positiva delkedjorna.
  Anna/Fredric är endast en möjlig Olaus-föräldrahypotes på `LEAD`-nivå;
  ingen ny föräldrakant skapades. S-0512/C-0672–C-0673/P-0466/
  A-2669–A-2674 och tio nya sakmedier bevarar fyndet. Totalt: 2 155
  påståenden, 1 665 Markdownposter, 2 024 mediafiler inklusive `.gitkeep`,
  manifest 2 023 (1 192 exakt/803 käll-/28 citationsavgränsade, 0
  olänkade), dashboard 466/2 155/475. Alla ordinarie tester, bygge,
  pedigree-, edition-, JSON- och manifestkontroller passerade; P-0210 har
  fortsatt exakt en öppen djup-4-spets, P-0336. Nästa säkra källväg är att
  följa Fredric–Anna efter A I/10 med båda Olaus-datumen och en ny
  gårds-/sidnyckel; upprepa inte B/2 1853 utan ny uppgift.
- **Batch 121 har slutit P-0315 Lars Petter Nilssons och P-0316 Cajsa Märta
  Andersdotter/Dahlsten/Dalstens centrala livslinjer till deras egna
  dödsfall.** Endast Riksarkivet användes. Indal A II a/1 s. 130 anger
  Cajsa Märta död 1901-03-05 och Lars Petter död 1904-09-25. SCB Indal post
  10 år 1901 och post 36 år 1904 korsbekräftar fullständiga namn,
  födelsedatum och Högsjö; Cajsa är Lars Petters hustru och Lars står senare
  som före detta torpare och änkling. Dödsorsaks- och dödsortsfälten är
  tomma. Indal F/2 1895–1920 är API-identifierad, men JSON-LD:s två
  bildrepresentationer saknar `schema:image`, reproduktions-id och bild-id;
  OAI tillför ingen digital länk. Den inloggade katalogsidan omdirigerades
  till orörd människeverifiering på ägarens uttryckliga Chrome-tillåtelse.
  Inga sessionsdata sparades och detta är åtkomsthinder, inte dödboksnoll.
  S-0499–S-0500/S-0510–S-0511/C-0668–C-0671/A-2665–A-2668 bevarar
  resultaten. Totalt: 2 149 påståenden, 1 661 Markdownposter, 2 014
  mediafiler inklusive `.gitkeep`, manifest 2 013 (1 182 exakt/803
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 465/2 149/475.
  Ordinarie tester, bygge, pedigree-, edition-, JSON- och
  manifestkontroller passerade; P-0210 har fortsatt exakt en öppen
  djup-4-spets, P-0336. T-0012 förblir aktiv och breddfronten ska rotera;
  de äldre flytt-/hushållsgapen är sekundär berikning.
- **Batch 120 har slutit P-0312 Anders Magnus Carlssons centrala livslinje
  till egen död.** Endast Riksarkivet användes. Data-API och publika
  IIIF-manifest routade Östra Husby A II a/1–A II a/3 till Gäddestad s. 68,
  91 och 93. De följer Anders Magnus som hemmansägare och änkling
  1900–1920; sista sidan anger död 1920-09-10. SCB:s Östra Husby-post 26 i
  `SE/RA/420401/01/H 1 AA/2276` korsbekräftar namn, dag, födelse
  1844-08-28, civilstånd och Gäddestad 1 samt anger `Kräfta`. Dödsortsfältet
  är tomt; `Lasarettsläkaren i Norrköping` är läkar-/intygsnotis och inte
  belägg för dödsort. A II a/3 och SCB-bilden svarade 401 utan session och
  hämtades via ägarens uttryckligt tillåtna, inloggade Riksarkivet-visare;
  inga sessionsdata sparades. S-0506–S-0509/C-0664–C-0667/A-2660–A-2664
  och åtta lokala original/manifest bevarar kedjan. Totalt: 2 145
  påståenden, 1 655 Markdownposter, 2 010 mediafiler inklusive `.gitkeep`,
  manifest 2 009 (1 177 exakt/804 käll-/28 citationsavgränsade, 0 olänkade),
  dashboard 465/2 145/475. Ordinarie tester, bygge, pedigree-, edition-,
  JSON- och manifestkontroller passerade; P-0210 har fortsatt exakt en
  öppen djup-4-spets, P-0336. T-0012 förblir aktiv och breddfronten ska
  rotera; eventuell bouppteckning för P-0312 är sekundär berikning.
- **Batch 119 har slutit P-0277 Anna Greta Hillbergs centrala livslinje till
  egen död och förklarat bild-API-spärren.** Endast Riksarkivet användes.
  Katalog-API och publika IIIF-manifest routade Hudiksvall F I/4 och F I/5;
  den av ägaren tillåtna och inloggade Chrome-sessionen användes endast för
  att öppna originalbilder som svarar 401 utan session. Bildvisaren använder
  `/v2/arkis!<bild-id>/...`; korrekt men oautentiserat `/v2/`-anrop kräver
  fortfarande inloggning, så felet var sessionsbunden rättighet och inte
  felaktigt bild-id. Hela F I/4 1931–1932 och F I/5 1933–1936 lästes utan
  målpost. F I/5 `00198658_00057`, sida 51 post 65, namnger `Hök, Anna
  Greta, f. Hillberg`, död 1937-06-14, född `57 9/6`, änka efter
  gårdsägaren Anders Gustaf Hök och med dödsorsaken `Marasmus senilis +
  Bronchit. ac.`. Särskild dödsort och begravningsdag har inte gjorts till
  påståenden. S-0504–S-0505/C-0662–C-0663/A-2657–A-2659 och två lokala
  manifest bevarar träff, exakta nollintervall och åtkomstmodell. Totalt:
  2 140 påståenden, 1 647 Markdownposter, 2 002 mediafiler inklusive
  `.gitkeep`, manifest 2 001 (1 169 exakt/804 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 465/2 140/475. Ordinarie
  tester, bygge, pedigree-, edition-, JSON- och manifestkontroller
  passerade; P-0210 har fortsatt exakt en öppen djup-4-spets, P-0336.
  T-0012 förblir aktiv. En framtida session får inte anta att ägarens
  inloggning består; rotera breddförst till nästa kohortperson.
- **Batch 118 har slutit P-0271/P-0272:s centrala livslinjer och säkrat två
  söners relationer.** Endast Riksarkivet användes, via API/JSON-LD/IIIF
  där möjligt; ingen Chrome-session användes. Hela Indal A II a/1:s
  Högsjöavsnitt s. 126–140 lästes, med s. 141 som ortgräns. S. 129 ger
  Nils Petter Höglund död 1906-01-19, Anna Stina Strandlund död 1904-11-15,
  Erik Nikolaus vigd 1906-07-14 med nya P-0465 Anna Kristina Nyberg, Jonas
  flytt till s. 138 och Gustaf Julius Elof till Nordamerika 1906-08-24.
  Fulla SCB-dödavsnitt bekräftar datumen och ger kräfta för Nils; tomma
  dödsorts-/orsaksfält förblir tomma. Fullt vigselavsnitt och egna C/5-/
  SCB-födelseposter säkrar vigsel, bådas första gifte, Eriks och Jonas
  föräldrar, barnordning och `odöpt`; Jonas datum är 1880-11-12 och den
  senare 22-novemberuppgiften en traderad avvikelse. Indal B/2:s 1906-bilder
  är exakt routade men svarar 401 med inloggningskrav, alltså åtkomsthinder
  och inte flyttningsnoll. S-0499–S-0503/C-0654–C-0661/A-2639–A-2656 och
  24 nya sakmedier bevarar allt. Totalt: 2 137 påståenden, 1 643
  Markdownposter, 2 000 mediafiler inklusive `.gitkeep`, manifest 1 999
  (1 167 exakt/804 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  465/2 137/475. Ordinarie tester, bygge, pedigree-, edition-, JSON- och
  manifestkontroller passerade; P-0210 har fortsatt exakt en öppen
  djup-4-spets, P-0336. T-0012 och `/goal` förblir aktiva.
- **Batch 116 har gjort P-0339:s bouppteckningsspår exakt utan att göra ett
  personnoll.** Riksarkivets strukturerade Ljustorp-frågor för 1901 gav 0 på
  Margreta/Margareta Charlotta mot Henriksson/Sjölin/Sjödin, även med för-
  respektive efternamn ensamt. `Charlotta` gav kontrollpersonen Anna
  Charlotta Andersson; den namnfria frågan gav exakt tolv poster. Registret
  är uttryckligen ofullständigt. Märta Kristina Vigg i Lagfors routas
  positivt till F II/5 nr 53 och den exakta volymen är
  `SE/HLA/1040061/F/F II/5`, 1901–1905, hos Riksarkivet i Härnösand, endast
  `Läsesal`. Ingen målakt har lästs; oregistrerade akter är möjliga och
  A I/10:s 1901-04-19 står fortsatt i konflikt med F/2-nollet. Nästa steg är
  läsning av F II/5:s 1901-avsnitt kring akter efter 19 april, parallellt
  med E 5-intagningshandlingarna för modern. Upprepa inte registerfrågorna
  utan ny digitalisering eller ny namn-/ortsnyckel. S-0498/C-0652/
  A-2636–A-2638 och fem medier bevarar allt. Ingen person eller
  föräldrakant skapades. Verifiering: 2 119 påståenden, 1 628
  Markdownposter, 1 959 mediafiler inklusive `.gitkeep`, manifest 1 958
  (1 142 exakt/788 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  464/2 119/471 och ordinarie tester/bygge gröna. P-0210 har fortsatt exakt
  en öppen djup-4-spets, P-0336. T-0012 förblir aktiv.
- **Batch 115 har slutit Brita Stina Svensdotters centrala livslinje och
  rättat ett äldre falskt noll.** Kungsholm F I/9 `00026746_00180`, s. 179
  post 365, namnger `Hustrun Fredberg, Brit Stina`, död 1886-10-01, 35 år,
  dödsorsak lungsot och begravd 7/10. Hemvist står kort som `37 D` och
  dödsortsfältet är tomt. F III/1 har faktiskt `Fredberg, B. S. 179` under
  1886; C-0366:s äldre Fredberg-noll var en felläsning och är rättat utan
  att metodhistoriken raderats. Rotemanspost `434800120110` ger familj,
  Jordgubben 1–5/littera D 1 och bland annat Fleminggatan 35–37 som samtida
  kontext; parallella gatunamn är inte separata flyttar. S-0497/C-0651/
  A-2632–A-2635 och fyra medier bevarar allt. Ingen person eller
  föräldrakant skapades. Verifiering: 2 116 påståenden, 1 626
  Markdownposter, 1 954 mediafiler inklusive `.gitkeep`, manifest 1 953
  (1 137 exakt/788 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  464/2 116/471 och samtliga ordinarie tester/bygge gröna. P-0210 har
  fortsatt exakt en öppen djup-4-spets, P-0336. T-0012 förblir aktiv.
- **Batch 114 har gjort 1876 års adresskalender exakt återstartbar utan att
  överdriva OCR- eller åtkomstresultat.** Volymen är Riksarkivet CE7363,
  FamilySearch post 541311/identifierare 1771125 och Geneanet 10897871.
  Riksarkivet saknar bildlänk, Stadsarkivet har före-1882-årgångarna på
  mikrokort, FamilySearchs boksidor kräver inloggning och Geneanet kräver
  Premium. Den öppna titelbegränsade fulltexten gav 22 `Fredberg`-resultat
  och målvolymen först, men sex exakta Olaus/Olof–Fredberg/Fredriksson/
  Fredrikson-frågor gav ingen målvolym; det är OCR-/frågenoll, inte
  originalnoll. Stadsarkivets 1729/1810-tomtregister gav tolv
  Kungsholmsgatan-rader men ingen nr 15 och är avvisat som 1876-källa utan
  ny samtida fastighetsnyckel. Nästa exakta steg är inloggad visuell läsning
  av målvolymen eller läsesals-/mikrokortsexemplaret, med sökning på båda
  efternamnsfamiljerna och 15 Kungsholmsgatan. S-0496/C-0650/A-2627–A-2631
  och åtta medier bevarar allt. Ingen person eller föräldrakant skapades.
  Verifiering: 2 112 påståenden, 1 624 Markdownposter, 1 950 mediafiler
  inklusive `.gitkeep`, manifest 1 949 (1 133 exakt/788 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 464/2 112/471 och samtliga
  ordinarie tester/bygge gröna. P-0210 har fortsatt exakt en öppen
  djup-4-spets, P-0336. T-0012 förblir aktiv.
- **Batch 113 har rättat Olaus 1876-adress och gjort nästa Stockholmsoriginal
  exakt.** Kungsholm B I/16:s maximalbild läses 15 Kungsholmsgatan, inte den
  preliminära 15 Upplandsgatan; `M:a` förblir osäkert. Kungsholms A I a
  slutar 1870 och A I b täcker bara 1785–1787/1806, så vanlig
  husförhörsrouting 1876 saknas. Stadsarkivets officiella instruktion anger
  att mantalsregistret saknar kvinnor och att mantalsskrivningsnumret används
  för hushållssökning och beställning. Den namnfria 1877-frågan på
  Kungsholmen nr 1217 ger bara Olaus men är inte hushållsnoll. Beställ full
  mantalsuppgift 1877 nr 1217 i läsesalen och pröva fastighet/hushåll bakåt
  mot 15 Kungsholmsgatan. S-0495/C-0649/A-2624–A-2626 och fyra medier
  bevarar allt. Ingen person eller föräldrakant skapades. Verifiering:
  2 107 påståenden, 1 622 Markdownposter, 1 942 mediafiler inklusive
  `.gitkeep`, manifest 1 941 (1 125 exakt/788 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 464/2 107/471 och samtliga
  ordinarie tester/bygge gröna. P-0210 har fortsatt exakt en öppen
  djup-4-spets, P-0336. T-0012 förblir aktiv.
- **Batch 112 har avgränsat två nya Stockholmsregister och gett ett positivt
  1877-ankare utan att överdriva 1876-nollen.** Stockholms stadsarkivs K050
  för Hovförsamlingens församlingsböcker 1835–1890 och K194 för Sabbatsbergs
  husförhör 1789–1868 samt in-/utflyttning 1830–1927 hämtades som officiella
  helregister. OCR användes bara för lokalisering; Fredriksson-avsnitten och
  övergångarna lästes visuellt. Fredberg saknas och ingen Fredriksson-rad
  gäller Olaus. Mantalsregistret 1800–1884 gav noll 1876 för de fyra exakta
  namnparen Olaus/Olof × Fredberg/Fredriksson, men återfinner honom 1877 som
  stationskarl i Kungsholmen, mantalsskrivningsnummer 1217. Underliggande
  mantalslängd är inte läst; 1876-resultatet är därför inget närvaro- eller
  Stockholmsnoll. S-0493–S-0494/C-0647–C-0648/A-2621–A-2623, två PDF:er och
  fem skärmbilder bevarar provenans, SHA-256, noll, kontroll och återstart.
  Ingen person eller föräldrakant skapades. Verifiering: 2 104 påståenden,
  1 620 Markdownposter, 1 938 mediafiler inklusive `.gitkeep`, manifest
  1 937 (1 121 exakt/788 käll-/28 citationsavgränsade, 0 olänkade),
  dashboard 464/2 104/471 och samtliga ordinarie tester/bygge gröna.
  P-0210 har fortsatt exakt en öppen djup-4-spets, P-0336. T-0012 förblir
  aktiv.
- **Batch 111 har slutit P-0336:s Alnö–Stockholm-led och rättat två
  registerfelläsningar.** Alnö A I/8 `C0032576` s. 167 placerar Olaus
  Fredriksson i Rökland, född 1852-09-04 i Lundby i Älvsborgs län och
  inflyttad från Fågelvik med B/2:s ankomstdata. A I/9a `C0032577` s. 193
  upprepar datum/ort, hänvisar till s. 167 och anger frejdebetyg till
  Stockholm 1876-01-15, destination Stockholm, attest nr 31. Den centrala
  kedjan Lundby → Björknäs i Östra Fågelvik → Alnö → Stockholm är därmed
  sluten 1873–1876. Gardes-/församlingsgapet är nu exakt 15 januari–14 juni
  1876 före Kungsholms `f.d. gardist`-rad; inget förband eller föräldrapar
  namnges. Två Alnö-rader stärker 4 september mot fyra senare original med
  24 maj utan att avgöra konflikten. A I/9b läses `Fredberg, J. A. F. Arb.
  192` och `Fredriksson, Olaus, Arb. 193`: Johan Augusts sida 102 och Olaus
  mellanläsning 73 är fel. S. 192 korroborerar Johan August, Anna Lovisa,
  Augusta Fredrika och vigseln; s. 73/102 är bevarade avvisade rutter.
  Sidorna 192–193 är inte ett gemensamt hushåll. S-0492/C-0643–C-0646/
  A-2617–A-2620, två manifest och nio fulloriginal bevarar allt. Ingen
  person eller föräldrakant skapades. Verifiering: 2 101 påståenden, 1 616
  Markdownposter, 1 931 mediafiler inklusive `.gitkeep`, manifest 1 930
  (1 114 exakt/788 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  464/2 101/471 och samtliga ordinarie tester/bygge gröna. P-0210 har
  fortsatt exakt en öppen djup-4-spets, P-0336. T-0012 förblir aktiv.
- **Batch 110 har screenat hela Stora Lundby A I/13 utan att överdriva
  nollresultatet.** Reproduktionen `C0045755` har 151 förda sidbilder på
  bilderna 9–159, handnumrerade sidor 1–149. Alla screenades visuellt efter
  Olaus/Fredriksson/Fredberg utan säker målrad. Bild 78/sida 70 kontrollerades
  i maximal upplösning och gäller drängen Olaus Johansson, född 1849-04-02 i
  Lundby; han avvisas. Utfallet är ett volymomfattande
  namnformsscreeningsnoll, inte ett person-, vistelse- eller församlingsnoll,
  och OCR-utdata bär inget påstående. A I/14 bild 8 är ett ortregister utan
  personnamn och gav ingen oberoende nyckel. Upprepa inte en blind A I/13-
  helvolymsscreening. Förstahandsvägen är fortsatt Östra Fågelvik H II/5:s
  läsesalsbundna 1873-attest; använd därefter bara nya gårds-/sid-/
  familjehänvisningar. S-0491/C-0641–C-0642/A-2615–A-2616 och 153 nya
  sakmedier bevarar samtliga 151 sidbilder, maximal kandidatkontroll,
  ortregister, manifest, noll, metodgräns och återstart. Ingen person eller
  föräldrakant skapades. Verifiering: 2 097 påståenden, 1 611
  Markdownposter, 1 920 mediafiler inklusive `.gitkeep`, manifest 1 919
  (1 103 exakt/788 käll-/28 citationsavgränsade, 0 olänkade), dashboard
  464/2 097/471, P-0004-baslinje 66 och P-0210 exakt en väntad öppen
  djup-4-spets P-0336. Tester, produktionsbygge, djup-5-vågpaket, oberoende
  pedigree, JSON, mediamanifest och `git diff --check` är gröna. T-0012
  förblir aktiv.
- **Batch 109 har genomläst Stora Lundbys hela bevarade
  flyttningsbilageavsnitt för 1873 och gjort nästa originalväg exakt.**
  Stora Lundby H II/2, `SE/GLA/13505/H II/2`, är reproduktion `A0062260`.
  Årsavdelarna på bild 71 och 103 omsluter dokumentbilderna 72–102; alla
  lästes i fulloriginal utan Olaus Fredriksson/Fredberg. Bild 81 gäller
  namnaliken Olaus Andersson född 1846 och är uttryckligen avvisad.
  Resultatet är ett volym-/års-/namnformsnoll, inte ett person- eller
  Lundbynoll. Den mottagande församlingen bör ha behållit flyttattesten:
  Östra Fågelvik H II/5, `SE/VA/13687/H II/5`, omfattar attester 1866–1887
  men är endast läsesalsmaterial hos Värmlandsarkiv. Ingen Olaus-attest är
  bekräftad där. Beställ 1873 och matcha B/5 inflyttade nr 4, 1873-04-25,
  Olaus Fredriksson från Lundby i Älvsborgs län till Björknäs, folio 23;
  bevara fram-/baksida och följ alla äldre hänvisningar i Stora Lundby
  A I/13. S-0490/C-0639–C-0640/A-2613–A-2614 och 44 medier bevarar hela
  kedjan. Ingen person eller föräldrakant skapades. Verifiering: 2 095
  påståenden, 1 608 Markdownposter, 1 767 mediafiler inklusive `.gitkeep`,
  manifest 1 766 (1 097 exakt/641 käll-/28 citationsavgränsade,
  0 olänkade), dashboard 464/2 095/471, P-0004-baslinje 66 och P-0210
  exakt en väntad öppen djup-4-spets, P-0336. Tester, djup-5-vågpaket,
  oberoende pedigree, JSON, produktionsbygge och mediamanifest är gröna.
- **Batch 108 har rättat Fågelvik-routen och fört P-0336:s centralryggrad
  exakt bakåt till Lundby i Älvsborgs län.** Östra Fågelvik B/5 inflyttade
  nr 4 visar drängen Olaus Fredriksson från Lundby i Älvsborgs län till
  Björknäs 1873-04-25, folio 23. Utflyttade nr 65 visar honom från
  Björknäs till Norrland 1873-10-24, samma datum som den bevarade Alnö-
  attestens utfärdande. Västra Fågelvik A I/17:s nu öppnade originalregister
  saknar Björknäs; C-0604:s B/1-noll var alltså ett sant men felplacerat
  boknoll, inte en bokföringskonflikt. Östra A I/25 s. 23 och 30 saknar en
  säker Olaus-rad trots B/5:s foliohänvisning; mismatchen är bevarad utan
  person-/ortsnoll. A I/24 s. 57 och 89 är äldre avgränsade sidnoll. Stora
  Lundby B/3:s hela utflyttningsår 1873, nr 1–45, saknar Olaus; A I/13 är
  bildöppen men registerlös och inte genomläst. Riksarkivets 1870-index ger
  även kontrollnamnet Johan noll i Älvsborgs län och är därför klassat som
  täckningsnoll. S-0489/C-0627–C-0638/A-2604–A-2612 bevarar original,
  manifest, konflikter och återstart. Inga personer eller föräldrakantar
  skapades. Nästa steg är en oberoende sid-/namnnyckel till Stora Lundby
  A I/13 eller en ny primär flyttningslänk; upprepa inte de nu slutna
  källintervallen utan ändrad täckning. Verifiering: 2 093 påståenden,
  1 605 Markdownposter, 1 723 filer i mediakatalogen inklusive `.gitkeep`,
  manifest 1 722 (1 090 exakt/604 käll-/28 citationsavgränsade,
  0 olänkade), dashboard 464/2 093/471, P-0004-baslinje 66 och P-0210
  exakt en väntad öppen djup-4-spets, P-0336. Tester, djup-5-vågpaket,
  oberoende pedigree, JSON, produktionsbygge och `git diff --check` är gröna.
- **Batch 107 löste P-0338:s föräldrar och öppnade nästa generation med
  strikt lägre evidensstatus.** Efter ägarens manuella ALTCHA-verifiering
  öppnade Riksarkivets Nybergspost `SE/RA/870001/2/22/171` bildserien
  `A0059777`. Familj 99 namnger Henrik Henriksson d.y. och Brita Flinkberg
  med barnet Henrik 1829 samt Jonas 1835 och Cecilia 1836. De två senare
  är redan original-/Familiaidentifierade dopvittnen, så P-0451–P-0452 är
  korroborerade föräldrar och P-0463–P-0464 syskon. Familj 98 öppnar
  P-0461 Henrik Henriksson d.ä. och P-0462 Anna Greta endast som
  `TRANSCRIBED`. Ljustorp A I/3 s. 43 korroborerar paret och exponerar
  registerkonflikterna 1796/1797 och Anna Greta/Cajsa Brita 1824; B I/1
  s. 15 bekräftar flytten 1850; Lagfors A I/1 s. 34–36 ger ett strikt
  originalbaserat senare noll som inte motsäger relationen. S-0487–S-0488/
  C-0623–C-0626/A-2591–A-2603 och sex bilder bevarar allt. Verifiering:
  2 084 påståenden, 1 592 Markdownposter, manifest 1 703 (1 071 exakt/604
  käll-/28 citationsavgränsade, 0 olänkade), dashboard 464/2 084/471,
  P-0004-baslinje 66 och P-0210 exakt en öppen djup-4-spets. Nästa
  breddrotation är P-0336; följ inte P-0461–P-0462 djupare före den.
- **Batch 106 har gjort P-0336:s SJ-personalaktsväg exakt utan att påstå en
  personträff.** Trafikverket 2024:024 leder till Riksarkivets
  `SE/GLA/16066 Regionala personalkontoret Stockholm`. F 1 A:s
  seriebeskrivning säger att huvudserien för födda före 1910 gäller
  trafiksektioner; box 4 är `SE/GLA/16066/F 1 A/4`, märkt `-1879: F-H`.
  Olaus födelseår 1852, Fredberg-namn och arbete vid Centralstationens
  persontrafik ger exakt routing dit. Boxen är `Läsesal` utan bild och ingen
  akt är bekräftad eller läst. Beställ i Riksarkivet Göteborg med båda
  födelsedatumen och namnformerna; om boxen saknar honom, kontrollera F 1 B
  och `SE/RA/420334/057`. S-0485–S-0486/C-0622/A-2589–A-2590, hela
  rapport-PDF:n och tre bilder bevarar provenans och hinder. Inga personer
  eller föräldralänkar skapades. Verifiering: 2 071 påståenden, 1 582
  Markdownposter, manifest 1 697 (1 065 exakt/604 käll-/28
  citationsavgränsade, 0 olänkade), dashboard 460/2 071/463, baslinje 66,
  P-0210 väntat två öppna djup-4-spetsar, tester och bygge gröna. Nästa
  breddrotation är P-0338.
- **Batch 105 gav P-0338 en källutlöst sidogren och ett korrekt klassat
  bostadsregisternoll.** Ljustorps hembygdsförenings `Vem bodde var`
  dokumenterar selektivt torp och backstugor 1850–1950. Henriksson-sidan
  saknar mål-Henrik 1829, alltså täckningsnoll och inte personnoll. Sonen
  P-0456 Henrik Petter anges däremot som första redovisade boende på
  Hinkestorpet i Rundbacken. De redan bevarade A I/6- och A I/10-originalen
  säkrar honom som son till P-0338–P-0339 och öppnar P-0457 Ingrid Gustafva
  Byström samt sönerna P-0458–P-0460. S-0484/C-0621/A-2581–A-2588 och tre
  bilder bevarar fyndet. Inga föräldrar skapades för mål-Henrik. Nästa
  breddrotation är P-0336 via ny central- eller SJ-personalaktväg.
- **Batch 104 gav P-0336 en pressbelagd järnvägsbiografi utan att lösa
  föräldrarna.** KB:s exakta frassökning gav 14 tidningssidor 1886–1925;
  varje använd artikel är visuellt läst i originalvisaren. *Signalen* 1899
  namnger Olaus stationskarlförman och vald för andra filialen. Den långa
  pensionsartikeln 1915 anger 40 års järnvägsarbete, praktisk ledning av
  Centralstationens yttre persontrafik under omkring 20 år,
  organisationsmedlemskap och avtackning; DN korroborerar ceremonin.
  DN:s runa 1925 anger ordinarie SJ-tjänst 1876, befordran 1883 och senare
  bangårdsmästartjänst med ansvar för krävande växling. Tre barn uppges ha
  gått in i järnvägstjänst, men de namnges inte och ingen individuell
  slutsats har skapats. Familjens annons preciserar jordfästningen till
  Sollentuna kyrka 12 augusti klockan 15. `Spara sida` krävde inloggning;
  direkt IIIF gav bara en bevarad logotypreserv. S-0481–S-0483/C-0615–
  C-0620/A-2574–A-2580 och 14 bilder bevarar allt. Nästa biografiska kontroll
  är en SJ-personalakt; nästa breddrotation är P-0338.
- **Batch 103 gav P-0338 en aktuell Lagfors-registerväg utan att skapa
  föräldrar.** Medelpads Släktforskarförenings publika översikt listar
  `Lagfors – Ljustorp`; Ljustorps innehåll kräver medlemsinloggning. Den
  äldre publika Lagforssidan namnger Helge Nybergs familjeregister
  1742–1860 och Karl Ivar Lundqvists född-/vigsel-/dödregister, men gamla
  beställningslänkar används inte som aktuella villkor. C-0613 visar att
  Släktdatas L-lista saknar både Lagfors och Ljustorp och C-0614 att
  Geneanets exakta datum-/makakriterier inte tillämpades utan Premium;
  ingetdera är personnoll. C-0612–C-0614/S-0478–S-0480/A-2571–A-2573
  bevarar routingen och hindren. Ingen person eller föräldralänk skapades.
- **Batch 102 är historik och dess Västra Fågelvik-/registerslutsats är
  ersatt av batch 108.** Seriemetadatan tolkades då som att A I/17 saknade
  register, men originalets bild 7 visar ett register utan Björknäs och
  Östra Fågelvik B/5 ger de positiva raderna. Släktdata täcker Stora Lundby-födda endast
  1689–1762 och 1855–1992 och saknar Västra Fågelvik: C-0609 är ett
  täckningsgap, inte personnoll. FamilySearchs exakta Olaus/Björknäs-fråga
  och bildbläddring stoppades av inloggning före resultat (C-0610).
  Geneanets publika index visar en sekundär Stora Lundby-rad men maskerar
  personfälten bakom Premium (C-0611). S-0475–S-0477/A-2568–A-2570
  bevarar allt; ingen person, förälder eller datumkonflikt har lösts.
- **Batch 101 löste P-0339 Margreta Charlottas far och barnhusbakgrund.**
  Ljustorp A I/4 s. 86 skriver `Barnh. flickan Margreta Charl. Schölin`,
  född 1825-08-13. Allmänna barnhusets originalrulla 2532 namnger
  fabriksarbetaren P-0454 James Schölin som far och P-0455 Nils Larsson i
  Löfberg som fosterbonde; endast James får biologisk föräldrakant. Modern
  saknas. Rullans `N:o 90`, barnhusnr 2532 och inskrivningsår 1831 är exakt
  återstart till E 5-intagningshandlingar som måste beställas och läsas på
  plats i Stockholms stadsarkiv. Mantalsregistret 1830 har två J Schölin,
  varav en handskmakeriarbetare med hushåll i Maria norra nr 968, men ingen
  är identifierad som James. Ljustorp A I/10 s. 264 anger död 1901-04-19 i
  dödskolumnen; detta konfliktförs mot F/2:s fulla noll 1901–1902. C-0606–
  C-0608/S-0472–S-0474/A-2558–A-2567 bevarar fynd, kandidater, noll,
  konflikt och återstart. Nästa breddspetsar är P-0336 och P-0338; P-0339:s
  mor och dödskonflikt står kvar som källspecifika frågor utan att hålla
  henne som föräldralös djup-4-spets.
- **Batch 100 förde P-0338 Henrik Henrikssons centralryggrad till november
  1850.** Familias exakta sökning på namn och 1829-08-10 ger endast biografi
  `13659891`, utan föräldrar. Ljustorp B I/1 s. 15 rad 14 anger drängen
  Henrik från Lagfors bruksförsamling till Lagforsby. Alla tre
  Rundbackentranskriptionerna A I/1 s. 34–36 är lästa: kandidatmiljön finns
  på s. 34, men målpersonen och Brita saknas. Eftersom Henrik flyttade 1850
  och volymen börjar 1860 är detta inte ett originalnoll och avgör inte
  relationen. Exakta Riksarkiv-id:n är `PJasZaXJHaIUWYMdzp6Po1` för
  Lagfors A I/1 och `Df6Qh8JhtKET8DW3coryY5` för Ljustorp B I/1; båda har
  bildinstansiering utan bild-URI bakom orörd ALTCHA. C-0605/S-0471/
  A-2556–A-2557 och nio medier bevarar fynd och återstart. Inga föräldrar
  eller nya personer skapades.
- **Batch 99 är bevarad felroutningshistorik, rättad i batch 108.**
  Västra Fågelvik B/1:s hela utflyttningsföljd 1873, nr 1–35, saknar Olaus
  trots den positiva originalattesten utfärdad 1873-10-24. C-0604/S-0470/
  A-2555 bevarar ett bok- och årsbundet noll samt två fulloriginal; det är
  ett sant boknoll i fel Fågelviksförsamling, inte en bokföringsavvikelse
  eller ett Fågelvik-, Björknäs- eller personnoll.
  A I/17 1871–1880 är exakt identifierad som Riksarkiv-id
  `tuyZqkkL2wT7oNHt8OssK3`, men JSON-LD saknar bild-URI och den inloggade
  katalogreserven står bakom orörd ALTCHA. Återstart: ägarens manuella
  CAPTCHA-bekräftelse eller ny laglig bildväg, sedan A I/15:s ortregister →
  Björknäs → gårdskontinuitet genom A I/16–A I/17 → inflyttning bakåt.
  Den tidigare A I/17-registervägen är slutligt rättad i batch 108. **Batch 98 förde
  P-0336 Olaus Fredriksson
  från Fågelvik/Björknäs till
  Rökland i Alnö 1873.** B/2 nr 76 och originalattesten H II/1 bild
  `A0018657_00334` säkrar namn, yrke, födelseår 1852, Lundby i Älvsborgs
  län, Fågelvik/Björknäs och flytten 1873-12-02. Attestens datumfras slutar
  `eller den 4 September`; 1852-09-04 är därför en historisk konflikt mot
  fyra senare 1852-05-24-original, inte längre bara registeravvikelse.
  Skön E I/2 löser Johan August–Anna Lovisas vigsel 1874-12-12, båda i
  Rökland. Den dåvarande A I/9b-läsningen s. 102 och uppgiften att A I/9a
  saknade användbar bildväg är rättade i batch 111: Johan August står på
  s. 192 och volymen är läst i original. B/2:s hela inflyttning 1872–1874
  saknar fortsatt paret. Hudiksvall och
  Arboga vigslar 1874 är fulla noll; Arboga är avvisad felläsningsrutt.
  C-0521 är rättad från `Andris Jacobson` till `Ole`/`Olo Andersson`:
  P-0453 Olof Andersson ersätter faderskanten, P-0412 är `REJECTED`
  historik och Olaus har fortsatt inga föräldrar. C-0600–C-0603,
  S-0467–S-0469 och A-2548–A-2554 bevarar allt. Nästa exakta steg är
  den nya Östra Fågelvik B/5-raden bakåt från Lundby i Älvsborgs län.
  Batch 96: Ljustorp E I/1 sida 17 rad 8 primärbelägger Henrik–Margaretha
  Charlotta Sjölin vigda 1854-07-16; det äldre sida-18-nollet är
  `REJECTED`. Familia och sex A I/6-original identifierar dopvittnena Jonas
  Henriksson/Höglin och Cecilia Henriksdotter och följer dem mot Hindric
  Henriksson/Vinroth–Brita Flinkbergs Rundbackenhushåll. Familia skriver
  deras relation `ej bestämd` och länkar inte Henrik till föräldrar;
  P-0451–P-0452 är därför endast kandidater och antavlan står kvar på 58
  kända anor. Margaretha Charlottas datum är rättat från felläst 1825-05-12
  till konflikten 1825-08-12/13; C-0525:s gamla registerkontroll prövade fel
  datum och får inte ärvas som augustinoll. Henrik Petter är rättad till
  1857-04-20. Sockenkatalogen lokaliserar Rundbacken till Lagfors A I/1 s.
  34–36; Nybergs register och bruksarkiven är exakt routade men olästa bakom
  utebliven bildlänk, WAF och orörd ALTCHA. S-0464–S-0466/C-0592–C-0596
  bevarar 36 nya exakt checksummade sakmedier och återstart. Batch 97:
  P-0339:s tio Stockholmsregister har nu sökts om på rätt datum
  1825-08-12/13 utan målrad; två andra 13-augustibarn är avvisade och
  flera stadsförsamlingar saknar täckning. Hela Ljustorp F/2 år 1900 är
  radläst utan målpost och sluter dödboksintervallet 1900–1902. Den fullare
  1910-frågan stannar på orörd ALTCHA. C-0597–C-0599 bevarar elva nya
  exakt checksummade medier, korrekt noll och återstart. Den rutten är nu
  ersatt av batch 101:s barnhusoriginal och dödsanteckning; 1910-CAPTCHA:n
  är sekundär åtkomsthistorik.
  Återuppta P-0338 först via A I/1 s. 34–36 i original eller Nybergs
  register.
- Föregående färdiga forskningssteg är **batch 93**. Den löste P-0422 Johan Peter
  Zingmarks livsslut i Degerfors F/3 och A II a/2: död 1903-07-24 i
  Ekträsk, begravd 2 augusti, utan angiven dödsorsak. P-0051:s nya
  Lövånger-/Bygdeå-registerfrågor klassades som täckningsnoll. Sävar C/1 och
  A I/1 är API-/JSON-LD-identifierade men saknar bild-URI; två privata
  Zingmarksidor är endast routing-`LEAD` med en födelsemånadskonflikt.
  S-0458–S-0461/C-0583–C-0587/A-2518–A-2522.
- Föregående färdiga **batch 92**: P-0133 Erik Karlssons andra
  vigsel är säkrad i SCB:s Flenutdrag 1895-12-28, och Flen A I/26 s. 281 →
  A II a/1 s. 346 binder Bergatorpshushållet över bokskiftet 1900–1901.
  Björkvik C/9 öppnar P-0446 Karl August, född utom äktenskapet
  1880-11-11 med Matilda Sjöberg som enda namngivna förälder; Erik är
  styvfar och får inte infereras som biologisk far. SCB:s Björkvikutdrag
  1860 öppnar Matildas föräldrar P-0444 Gustaf Sjöberg, dräng i Bokulla,
  och P-0445 Stina Lotta utan angivet efternamn. A II a/1 s. 281 bevaras
  som korrigerad routing: hänvisningen avsåg föregående volym. Tre
  församling/år-noll och registertäckningsnoll är bevarade utan
  överinferens. Allt hämtades API-/IIIF-först utan Chrome.

  Björkvik C/7 och A I/17 a–b är API-identifierade som digitaliserade men
  saknar bildlänk; exakta JSON-LD-omprov och två osäkra sekvensmanifest gav
  `403`. Flen A I/25 har API/JSON-LD/OAI-metadata men ingen bild-URI och
  katalogen stannar på orörd CAPTCHA. Återstart: API → JSON-LD → IIIF på
  nytt, därefter inloggad katalog utan CAPTCHA eller annan laglig
  leverantör. S-0453–S-0457/C-0576–C-0582.

  Föregående **batch 91**: Degerfors B/3:s hela
  inflyttning 1898–1900 och F/3:s dödsrader 1898-11-28–1900 saknar säker
  P-0422 Johan Peter Zingmark; de är slutna volymnoll, inte livsslut.
  Nikanor och Olof Konrad återfinns positivt i Rosinedahl. A II a-seriens
  första WAF löstes med korrekt API-innehållsförhandling; API/JSON-LD/IIIF
  gav A II a/3 s. 963 utan Chrome. Sidan primärbelägger Johan Oskars tio
  barn 1888–1909 samt Nikanors nya hustru P-0441 och söner P-0442–P-0443.
  Folio 1043 är en bevarad korrigerad routing; den exakta folkräkningsfrågan
  för Johan Peter stannar på orörd ALTCHA. S-0449–S-0452/C-0571–C-0575.

  Föregående **batch 90**: Bygdeå F/2 s. 29 post 39
  säkrar P-0051 Barbro Kristina Olofsdotter död i Jomark 1913-05-23,
  begravd 8 juni och änka efter förre hemmansägaren Anders Andersson.
  Dödbokens `14/2 30` konfliktförs mot Jomarklängdernas `24/2 1830`; hela
  1912 är negativt läst före den positiva 1913-posten. Sök-API och JSON-LD
  gav två manifest; manifest/`info.json` svarade `200`, bilderna `401`, och
  först då användes bildvisaren utan CAPTCHA. C-0569/S-0332 bevarar 20
  bilder och åtta metadata-/hinderoriginal.

  Bouppteckningen drevs därefter helt utan Chrome. Fondens OAI-EAD belägger
  att Bygdeå ingick i Nysätra tingslag efter 1902. Det publika registret
  slutar 1910 och kunde inte pröva 1913. API/JSON-LD/OAI identifierar de
  analoga volymerna `SE/HLA/1040129/C/C II/C II b/13` (Nysätra M–Ö,
  registerkort 1903–1932) och `SE/HLA/1040118/F/F II/23` (1913). Ingen
  bildlänk finns; återstarten är API/JSON-LD/IIIF på nytt och annars fysisk
  läsning/beställning hos Riksarkivet i Härnösand i ordningen C II b/13 →
  F II/23. S-0448/C-0570 bevarar nio metadataoriginal och det rättade
  register­nollet.

  Batch 89: A I/7b:s positiva
  hänvisning är följd till Sävar A I/6b s. 603. API/JSON-LD prövades först;
  efter utebliven bildlänk och IIIF `403` användes autentiserad bildvisare
  utan CAPTCHA. Sidan säkrar Johan Peter–Sara Sophias första vigseldag
  1850-11-24, hennes födelsedatum 1829-05-21 med orten skriven Lycksele,
  tvillingarna Axel/Anders och dödsanteckningen 1868-08-14. C/3-originalen
  rättar tvillingarnas födelser till 1864-03-23/24 och säkrar Sara Rebecka–
  Ester Amalia 1868-02-12/13; E I/1 säkrar Axels död 1865-02-18. C/2 säkrar
  Sophia Beata 1851-08-01. P-0438–P-0440 är nya och P-0028 har nu nio
  belagda helsyskon; första barnkullen omfattar minst tio barn
  (C-0563–C-0567). Sara Sophias dödsdag är `CONFLICT`, eftersom hela
  E I/1–F/1-intervallet fortfarande saknar säker post (C-0555; nu 23
  fulloriginal). Lycksele C/3 identifierades via sök-API, JSON-LD och OAI
  (`200`) men saknar bildlänk; katalogens ALTCHA lämnades orörd. Tre
  metadataoriginal och exakt API-först-återstart finns i S-0447/C-0568.
  Batch 88: Riksarkivets sök-API och
  JSON-LD identifierade Sävar C/2 och A I/7b (`200`) men saknade bildfält;
  direkt-IIIF för batcherna `C0034442` och `C0034437` gav `403`. Först då
  användes den autentiserade bildvisaren, utan CAPTCHA. A I/7b s. 672
  visar sju då synliga barn i Johan Peter Zingmarks första gifte och pekar bakåt till
  gamla bokens sida 603. Fyra egna födelsenotiser 1853–1858 namnger Johan
  Peter/Peter Zingmark och Sara Sophia Pehrsdotter som föräldrar till Carl
  Reinhold, Christina Wilhelmina, Maria Elina och Pehr August. P-0435–P-0437
  är nya källbundna sidopersoner; den då kända bilden gav sex säkra helsyskon
  (C-0561–C-0562). Fyra nya fulloriginal; Maria Elinas befintliga
  C-0192-original återanvänds. Vigselbilderna 1848–1858 orienterades men gav
  varken säker träff eller tillräckligt avgränsat noll; nästa positiva
  återstarten var Sävar A I/6b s. 603 och är nu genomförd i batch 89.
  Batch 87: API-försöket för P-0422:s
  födelse i Sävar C/1 gav `403`/WAF och `ERR_BLOCKED_BY_CLIENT`; först
  därefter prövades inloggad katalog, som utlöste orörd ALTCHA. C-0558/S-0446
  bevarar åtkomsthindret utan källnoll och med API-först-återstart. Den redan
  API-/IIIF-avgränsade Högby F/2 (`info.json` `200`, bild-API `401`) öppnades
  därefter i inloggad reservvisare utan ny katalogsökning. C-0559 löser Oskar
  Mauritz Adelbert Carlmans död 1895-01-14 av lungsot och C-0560 Carl August
  Carlmans död 1901-11-21 av hjärtlidande, begravd 27/11. Två fulloriginal.
  Batch 86: Östra Husby A I/21:s
  flyttnotis ledde till Häradshammar C/7, som säkrar Anders Magnus Carlsson–
  Carolina Larsdotters lysning 1870-08-28 och vigsel 1870-10-14 med bådas
  exakta födelsedatum; modern Maja Lena Jonsdotter var änka och gav
  skriftligt samtycke (C-0557). Jonsberg B I/3 1868–1872 gav ett avgränsat
  noll med fyra fulloriginal (C-0556), utan inferens om tidigare avresa.
  Sök-API/JSON-LD användes före Chrome; katalogen behövdes bara för att lösa
  batch-id:n som API-lagret utelämnade och vars direkt-IIIF gav `403`.
  Batch 85: Sävar E I/1 verifierar
  Johan Peter Zingmark–Kajsa Greta Nilsdotters vigsel 1870-07-02; E I/1:s
  dödavsnitt och F/1 ger ett fullständigt, granskningsbart tvåvolymsnoll för
  Sara Sophia 1868-02-13–1870-07-02 (senare rättat till 23 fulloriginal,
  C-0555), och A I/9b
  s. 670 följer Johan Peter till änkestatus 1895-07-02 och flytt till
  Degerfors 1898-11-28 (C-0553–C-0554). Batch 84 identifierade via Sävar A I/8b s. 756
  P-0422 som bonden Johan Peter Zingmark (f. 1825-02-01,
  Botsmark nr 7) och skapade tio sidopersoner (C-0552). Batch 83 kedjebelade
  brygga 7
  (P-0251 Stina Kajsa Nordlund: kolardottern från Stormyran → Stöde 1871,
  C-0551). Batch 82 visade att P-0028 Johan
  Oskar Zingmark var felidentifierad: han är född 1861-05-28 i Botsmark som
  son till P-0422 J. P. Zingmark och P-0423 Sara Sophia Pehrsdotter
  (C-0546–C-0550), inte Lundström-sonen Johan August Johansson (nu P-0424).
  P-0058–P-0059 är avlänkade från antavlan och pedigree-baslinjen är
  uppdaterad. Familjeutgåvan v1 har därmed ett erratum som väntar på
  ägarbeslut. Batch 81 slöt identitetskedjan
  för P-0253 Erik Jonas Henriksson (Ljustorp A I/10 s. 265 → Holm 1894 →
  Sättna 1900; vigsel 1900-11-24, död 1910-03-02; C-0542–C-0544). Batch 80
  säkrade P-0125 Lars
  Anderssons död 1874-02-05 i Anderslund (Lerbo F/1, C-0541) med ålder som
  stöder 1820-08-21. Batch 79 säkrade P-0310 Karl
  August Carlmans andra vigsel 1882-03-28 i Kalmar E I/5 (C-0539) och
  församlingsboksburna död 1901-11-21 i Högby A II a/1 s. 140 (C-0538), med
  Högby E I/2 1879–1890 negativt avgränsat och Högby F/2 registrerad som
  `401`-spärr (C-0540, S-0429). Batch 76 fann
  Carlman–Ringberg-vigseln 1862-09-26 i Källa E I/1 (C-0533) och batch 77
  Jansson–Larsson-vigseln 1886-04-26 i Lerbo E I/4 (C-0535), båda via
  publik IIIF utan Chrome; Högby/Bäckebo respektive Lerbo 1883–1885 är
  negativt avgränsade (C-0534, C-0536). Batch 78 avgränsade P-0312/P-0313:s
  vigsel negativt i Jonsberg och Östra Husby 1869–1872 (C-0537). Batch 75:s
  original C-0529–C-0532 är sedan tidigare integrerade.
- Dashboarddatan innehåller 452 personer, 2 028 påståenden och 454
  föräldralänkar. Genealogin har 463 källposter, 597 citationsposter och 1 599
  sakmedier. Mediamanifestet har exakt samma 1 599 filer: 967 exakt bundna,
  604 källavgränsade och 28 citationsavgränsade, utan olänkade filer. De två
  bevarade `401`-svarskropparna i S-0332 är avsiktligt bitidentiska och
  dokumenterar var sitt IIIF-anrop.
- Granskning av identitetsbryggor 2026-08-29 (forskningsloggen): brygga 1
  (P-0239 → P-0287) är fastställd av ägaren (`PCD-2026-08-29-001`), brygga 6
  (P-0253) är kedjebelagd i batch 81; bryggorna 2–5 och 7–9 (P-0336, P-0134,
  P-0094, P-0050, P-0276, P-0312): omvärderade 2026-08-29 — 3, 4 och 5 är
  vid omläsning starka/kedjebelagda; 2, 8 och 9 får inte fördjupas förbi utan
  oberoende länk. Brygga 7 (P-0251) är kedjebelagd i batch 83;
  brygga 10 (P-0028) prövades i batch 82 och visade sig vara en
  felidentifiering som är rättad.
- P-0004-baslinjen är 68 kända anor och har tre öppna djup-4-spetsar:
  P-0051, P-0133 och P-0423. P-0210 har 61 kända anor och exakt en öppen
  djup-4-spets, P-0336. P-0339 är vidareförd till
  P-0454 James Schölin, medan modern är källspecifikt öppen. P-0250 Abraham Jönsson är
  vidareförd till P-0447–P-0448. P-0251 Stina Kajsa
  Nordlund är vidareförd till föräldrarna P-0415 och P-0416.
- P-0415 Jonas Nordlund har giltig terminalstatus `IDENTITET OLÖST` på djup 5.
  Hans födelsenotis 1816 matchar namn, datum och ort, men fadersnamnet ser ut
  som Pehr Simonsson medan den senare CEDAR-biografin anger Jonas Stefansson.
  Ingen far har därför skapats för Jonas.
- P-0416 Gertrud Olofsdotters föräldrar P-0417 Olof Stefansson och P-0418
  Sigrid Jonsdotter är säkrade i Stöde C/2.
- T-0013 är `BLOCKED` efter T-0012 och ägarens obligatoriska
  redaktionella/designmässiga kontrollpunkt. T-0009 och T-0010 är parkerade
  `IDEA`, inte körbara nästa steg.

Detaljer finns i:

- `genealogy/research-log/2026-08-29.md` — batch 66–93, pågående batch 94
  och reparationen.
- `wotan/dev-log/T-0012.md` — krav, beslut och hela körhistoriken.
- `genealogy/frontier.md` — personvis aktuell forskningsfront.
- `genealogy/source-coverage.md` — prövade och kvarvarande källfamiljer.
- `genealogy/method-riksarkivet.md` — reproducerbar API-först- och
  reservmetod för Chrome.

## Återställd batch 75

De fyra original som först upptäcktes som avbrutet arbete har integrerats:

| Citat | Bild / huvudresultat |
|---|---|
| C-0529 | Stöde SCB 1872: Jöns Peter, son till Abraham Jönsson och Stina Cajsa Nordlund i Hullsjö |
| C-0530 | Sättna A I/8 s. 255: Stina Cajsa i föräldrahushållet Jonas Nordlund och Gertrud Olofsdotter, med fyra syskon |
| C-0531 | Holm C/1 1816: Jonas född 9 oktober; konflikt i fadersnamnet, ingen far skapad |
| C-0532 | Stöde C/2 1812: Gertrud, dotter till Olof Stefansson och Sigrid Jonsdotter i Hullsjö |

S-0266, S-0264 och S-0261 breddades och S-0419 skapades. P-0415–P-0421 och
A-2353–A-2365 bevarar personer och slutsatser. Bilddimensioner, SHA-256 och
proveniens finns i citationsposterna och `genealogy/media-manifest.json`.

## Reparation efter compaction-audit

Följande är reparerat och ska inte göras om:

- Relationsparsern misstolkade flerordsrubriker som `Historisk kandidatpost:`
  och `Make 1930:` och skapade fem falska föräldralänkar till P-0027 samt tre
  cykler. Parsern och regressionstesterna är rättade; inga självkanter,
  dubblettkanter, reciproka eller längre cykler, eller personer med fler än
  två föräldrar återstår.
- Dashboardens påståendecitat räknades dubbelt när samma C-ID förekom både i
  Markdown-länkens etikett och href. Bygget deduplicerar nu varje påståendes
  C-ID:n, och testet bevakar detta.
- De dubbla källposterna S-0068, S-0123 och S-0198 har slagits ihop med S-0008,
  S-0081 respektive S-0116. Levande citat pekar på de kvarvarande posterna.
- Två bitidentiska JPEG-kopior under C-0372 och C-0434 har tagits bort efter
  att citaten pekats om till de bevarade originalen för C-0273 och C-0342.
  Citationsposterna C-0372 och C-0434 finns kvar som separata evidensposter.
- Mediamanifestet är regenererat och rent: noll orphan-filer. Batch 90
  tillförde därefter två avsiktligt bitidentiska `401`-svarskroppar för två
  skilda IIIF-anrop; de är båda provenansbundna i S-0332/C-0569.

## Nästa forskningsåtgärd

Fortsätt breddrotationen med P-0015 Axel Edvard. Flen B/4 post 39 ger en
säker positiv Flen→Sköldinge-flytt 1897-10-20; följ den mot Sköldinges
inflyttnings-/hushållslängder och den kända återkomsten från Hyltinge
1898. P-0143 Erik Arvid har samtidigt en säker Stockholmspost samma dag.
Återta honom endast genom den exakta globala sökningen efter ägarens egen
verifiering eller en ny församlings-, adress- eller registerbrygga.
Upprepa inte de redan lästa nio civila Stockholmsspannen och rör inte den
nya ALTCHA-rutan. T-0012 förblir `ONGOING`/`DOING`; använd endast
Riksarkivet.

### Historisk backlogkontext

Rotera breddförst mellan de kvarvarande frontpersonerna. Batch 168 löste
P-0133:s föräldrar, batch 169 gjorde P-0336:s militära återstart exakt,
batch 170 följde P-0474–P-0475 och batch 171 följde P-0472–P-0473.
Beatas föräldrar är nu P-0478–P-0479; Petters egna föräldrar är fortsatt
öppna bakom den exakt katalogiserade Lycksele-routen. Nästa breddrotation
återgår därför till P-0051 enligt den balanserade vågen. För P-0336 är första
militära prioritet Göta livgardes analoga namnregister 198 med
Fredberg/Fredriksson och båda födelsedatumen; därefter följer journalerna
240/241, Svea `D III/2`, Livgardet till häst `D VI/6` och Göta GMR 237.
GMR 1553:s 1875-block ska inte OCR-screenas igen utan en ny namn-, nummer-
eller skvadronsnyckel. Den direkta äldre vägen är fortsatt Östra Fågelvik H II/5:s
läsesalsattest 1873; matcha inflyttade nr 4 den 25 april och använd en
positiv gårds-/sidnyckel tillbaka mot Stora Lundby. För P-0423 krävs en ny
positiv ort-, datum-, dödserie- eller flyttnyckel; upprepa inte Lycksele
C/3 s. 126 eller F II a/13-bilderna 1163–1724.
Ägarens aktuella källregel pausar Stadsarkivets mantalsbeställning och alla
FamilySearch-/Geneanetvägar. För Stockholmsgapet får bara Riksarkivets egna
API-, katalog- och bildkällor användas; adresskalendern kan återtas inom
regeln via Riksarkivets `CE7363`. Kungsholms A I a slutar 1870; sök inte en
påhittad 1876-volym. Militär rulla kräver en ny förbandsnyckel. Upprepa inte
de redan avgränsade Stockholmsspåren utan ändrad Riksarkivstäckning eller ny
namnform; deras noll är inte närvaronoll. Fördjupa inte redan vidareförda
djup-5/6-grenar före denna spets. Publik IIIF (`curl` med
webbläsar-`User-Agent`)
räcker för volymer som svarar `200` på bildnivå; ett manifest kan svara `200`
medan bilderna ger `401` (Högby F/2), och omvänt är Högby A II a/1–6
1895–1943 publika. Ägarregel: använd alltid sök-API → JSON-LD → IIIF före
Chrome där så är möjligt; Chrome är reserv för saknad bildlänk/reproduktionskod
eller dokumenterad `401`/`403`. Säkra
återstarter är:

- **P-0051 Barbro Christina Olofsdotter:** döden är löst i C-0569. Upprepa
  inte Bygdeå F/2 1912–1913 eller det publika bouppteckningsregistret.
  C-0707/S-0543 identifierar farbrodern C. E. Lundberg starkt som Carl
  Eric, född 1806-10-14 i Överklinten, son till Pehr Johansson och Anna
  Catharina/Anna Cajsa Olofsdotter. A I/6 och A I/7a namnger hans bror
  Olaus, född 1784, som första digitala kandidatväg mot Barbros
  patronymikon. Följ Olaus och syskonen från A I/7a framåt endast för en
  uttrycklig Barbro-koppling eller ett säkert avvisande; skapa inte en
  farrelation från namnformen. Upprepa inte A I/13a-felroutingen: exakt
  Lugnet finns i A I/12b sida 330 och A I/13b sida 480.
  C-0716 säkrar Olaus född 1784-02-07 och läser `Piteå` i A I/6:s marginal.
  C-0717 avgränsar Piteå landsförsamlings vigselår 1805–1809 och dödår
  1805–1807 samt stadsförsamlingens ministerialföljd 1805. C-0720 har nu
  dessutom läst hela F/1:s död- och begravningsföljd 1808–1819-05-15 utan
  säker kandidat. C-0724 har läst hela E I/3:s vigselföljd 1810–1818 utan
  en säker Olaus/Olof Pehrsson eller Persson. C-0728 har också slutläst
  E I/3 1819–1830; delen 1819–1826-10-07 hålls som
  pastorsämbetsrekonstruktion. Upprepa inte dessa år. C-0735 routar
  A I/3b–e och A I/4a–e till nio officiella IIIF-manifest. Två OCR-pass
  användes bara för navigation, och tio verkliga kandidater avvisades i
  maxoriginal. Resultatet är inte ett helvolyms- eller vistelsenoll; återta
  endast via ny by-, sida-, familje- eller flyttnyckel. H II/1 återtas först
  genom personregistret i arkivexpeditionen eller en ny dokument-/ortnyckel.
  Första originalroute för ursprunget är nu Bygdeå H III/1:s analoga
  födelse- och dopbilagor: volymen har uttryckligt material 1829–1831 och
  bland annat Robertsforsrapporter om födda 1830–1832. Beställ med båda
  konfliktdagarna, alla namnformer och Jomark/Bygdeå/Lövånger; metadatan är
  inte personträff eller Robertsforsursprung, C-0700/S-0536.
  Bouppteckningen är en exakt analog återstart: C-0736 ger äldre
  Arkis-UUID:er för `uamwPFisWKkWqpnjo8xka2` och
  `k6CqF3Xtrn61t03Gjpu0Y3`, men de publika arkivträden är tomma och
  batchrouten ger HTTP 500. Beställ C II b/13 och därefter F II/23 hos
  Riksarkivet i Härnösand. Ursprung och
  föräldrar kan därefter också återtas via L III/1:s analoga strödda
  fattigvårdshandlingar. C-0696 avvisar H V/1 för 1860 och gör H I/1 till
  exakt oläst beställningsroute för C. E. Lundbergs skriftliga medgivande;
  C-0736 ger H I/1, H III/1 och L III/1 exakta Arkis-UUID:er men inga
  bildbarn. Inget släktskap får infereras.
  Därutöver kräver föräldrafrågan en ny positiv social-, flytt- eller
  förmynderskapsnyckel; välj inte en namnlik födelsepost för att fylla
  konflikten. C-0583 visar
  att Lövångers separata B-serie börjar 1861 och att födelseregistrets noll
  för 1830 är täckningsnoll; upprepa inte dessa API-frågor utan ändrad
  dokumenterad registertäckning.

- **P-0133/P-0135 Erik Karlsson–Matilda Sjöberg:** P-0133:s föräldrar är
  nu korroborerade som P-0474 Carl Fredrik Grill och P-0475 Johanna
  Jansdotter genom C-0729. Upprepa inte Bettna A I/17:s OCR-screen eller
  SCB 1870-skärmarna utan ny dokumentnyckel; de gav inget helvolymsnoll.
  Vistelsen 1867–1875 återstår via Forssa H II/1:s analoga attest samt de
  läsesalsbundna mantals-/beväringsvägarna i C-0319, men luckan blockerar
  inte längre föräldraidentiteten. Upprepa inte SCB 1860,
  SCB-vigslarna 1895, Flen A I/26 s. 281, A II a/1 s. 281/346 eller
  Björkvik C/9 post 112. Upprepa inte heller Årdala B/3 inflyttade 1875,
  Forssa B/3 utflyttade 1875 eller Årdala A I/13 s. 190: C-0683 bevarar
  deras fullständiga, avgränsade noll. C-0718/S-0553, rättade genom
  C-0763/S-0592, följer familjen vid Glippsta tillbaka till 1841 och bevarar den
  överstrukna Stora Malm-notisen för Carl Fredric Grill och Johanna
  Jansdotter utan vigseldag. Maxoriginalet visar Carl Fredric Drill på
  Livkompaniets Glippsta nr 36 år 1842, antagen 1841-02-18, och Bettna B/1
  för honom från Björkvik till Glippsta 1841-11-11. Upprepa inte den
  militära kedjan, Björkvik B/1 1841 eller de kompletta vigselföljderna i
  Bettna, Stora Malm och Björkvik utan ny positiv nyckel. C-0721/S-0556 har
  nu säkrat Johannas reciproka utflyttning från
  Backstugan i Stora Malm till Bettna 1841, hennes födelse 1819-05-30 i
  Walla och föräldraparet Jan Ericson–Lena Jonsdotter i A I/13 a. C-0729
  säkrar henne som Eriks mor. C-0732 följer paret genom 1878 och vidare i
  Götstugan 1881–1885 samt säkrar Johanna död 1883-02-24. Carls senare
  hushållssida och död är öppna; Carlsson 1885, Bettna C/6 1870–1871 och
  Björkvik B/4 1878–1879 ska inte upprepas. C-0731 skapar föräldrarna som
  P-0476–P-0477. Jans 1791-05-09 Björkvik är konfliktsatt och Lenas
  Helena-kandidat i Walla är inte en säker föräldrakant. Carls
  Halla/Björkvik-spår gäller hans egen konfliktsatta födelse och kräver en
  ny positiv identitetsnyckel. Matildas nästa
  generation ska bindas i Björkvik A I/17 a–b/C/7 när API-bildvägen öppnas;
  sonen Karl August följs reciprokt via Helgesta 1896-11-13. Börja alltid
  API → JSON-LD → IIIF; S-0457 bevarar `403` och orörd CAPTCHA.
  C-0698 visar att Flens E I har ett kataloggap 1862–1904 och att H V/1
  börjar 1919. Konstruera ingen lokal E I-bok för vigselåret 1895. P I/1,
  Pålysningsböcker 1849–1926, är en exakt analog beställningsroute men
  OAI-posten har tom innehållsförteckning; ingen målrad får förutsättas.

- **P-0310 Karl August Carlman:** egen dödpost är löst i Högby F/2:
  1901-11-21, hjärtlidande, begravd 27/11 (C-0560); sonen Oskar är löst i
  samma volym 1895-01-14, lungsot (C-0559). Upprepa inte målsidorna.
  Bouppteckning efter P-0311 (uppvisad 1882) är oläst.
- **P-0422/P-0423 Zingmark i Botsmark:** A I/6b s. 603, C/2 och C/3 säkrar
  första vigseldagen och minst tio barn i första giftet, däribland två
  tvillingpar; upprepa inte C-0561–C-0567:s sidor. Sara Sophias dödsdag
  1868-08-14 i hushållet står i konflikt med det fullständiga
  E I/1–F/1-nollet (C-0555/C-0563); återstarta via alternativ dödserie
  eller ny dokumentnyckel, inte samma dödbokssidor. C-0690
  indexerar den säkert läsbara dopvittnesdelen som lokalt Botsmarknätverk
  utan släktskapsinferens. Umeå F II a/13 1865–1869 är exakt digital
  bouppteckningsroute. C-0699 har nu systematiskt kontrollerat den kompletta
  följande protokollsekvensen från akt `76 1/2` den 20 augusti 1868 genom
  sista akt 119 år 1869 utan målträff. Det är inte ett helt volymnoll och
  verifierar inte dödsdagen; upprepa inte bilderna 1163–1724. Registret
  stannade historiskt på orörd ALTCHA. Sävars H II saknar katalogiserad
  1868-volym. Hela Lycksele
  C/3:s födelseår 1829 är nu läst. Årets enda tydliga Sara Sophia föddes
  1829-08-06 till Mats Ersson och Maja Greta Jonsdotter i Rusele och följs
  där till 1845; hon saknas på 1846 års Ruselefolio och i Sävar B/1
  inflyttade 1845–1849. Datum och far/patronymikon avviker från målpersonen,
  så kandidaten får inte kopplas utan ny oberoende brygga. Upprepa inte
  helåret, Ruselefolierna eller Sävar B/1 1845–1851 (C-0682/C-0695).
  Upprepa inte Degerfors B/3 eller F/3 1898–1900: intervallen är fullständigt
  lästa utan Johan Peter. Livsslutet är nu löst: Degerfors F/3 post 87 och
  A II a/2 s. 601 följer honom som före detta sågverksarbetare i Ekträsk,
  död 1903-07-24 och begravd 2 augusti (C-0584–C-0585). Upprepa inte
  målsidorna. Sävar C/1 s. 91 och A I/1 s. 157 säkrar nu födelsen
  1825-02-01 och föräldrarna P-0470 Carl Jonas Zingmark, född 1785, och
  P-0471 Anna Sophia Holmström, född 1792, i två original (C-0681). De är
  nya djup-5-spetsar; de äldre C-0558/C-0587-hindren är endast historik.
- **P-0125 Lars Andersson:** död 1874-02-05 är säkrad (C-0541); nästa
  nyckel är husförhörsbokens `p. 164` i Lerbo A I/20 1871–1875, som saknar
  bildlänk i sök-API:et (pröva inloggad katalog). Ompröva fortfarande
  C-0016:s `Gånga` mot vigselns `Spånga`.
- **P-0312/P-0313:** vigseln är löst i Häradshammar 1870-10-14 (C-0557);
  upprepa inte Jonsberg/Östra Husby-vigselsökningarna eller Jonsberg B I/3
  1868–1872. P-0312:s Gäddestadskedja är sluten genom A II a/1–A II a/3
  till död 1920-09-10 av `Kräfta` (C-0664–C-0667); Norrköping-notisen är
  inte dödsort. Eventuell bouppteckning och Carolinas äldre
  Jonsberg–Häradshammar-flytt före 1868 är sekundär berikning, inte nästa
  centralspinekrav.

- **P-0250 Abraham Jönsson:** föräldrarna är nu säkrade i C-0333/C-0590.
  Upprepa inte A I/8 s. 88–97 eller A I/9-Hullsjö s. 92–93. Efter nästa
  breddrotation följs P-0447/P-0448 bakåt via 1805-08-22 respektive
  1812-07-28 och föregående husförhör. Bouppteckningen i
  `SE/HLA/1040237`, `F II a/9` (AID `v510406`) är en separat senare väg
  bakom ALTCHA/inloggning.
- **P-0336 Olaus Fredberg:** födelseregistrets nya noll får inte sökas om
  eller göras till personnoll utan ändrad täckning. Lundby–Östra Fågelvik–
  Alnö–Stockholm-kedjan är sluten till frejdebetyget 1876-01-15; sök nu
  först Göta livgardes analoga namnregister 198; vid Fredberg/Fredriksson-
  träff använd digitala rekrytapprobationsjournalen 194, annars de analoga
  journalerna 240/241 och kompanivisa rullor. Stockholms flyttnings-/
  hushållsregister och generalmönster-/vakansrullor fram till Kungsholm
  1876-06-14 är parallella vägar. Maria F-sektionerna, Svea/Göta livgarde
  och Livgardet till häst är avgränsat negativa men inte förbandsnoll.
  Upprepa inte A I/9a s. 73/102, Västra Fågelvik B/1, Stora Lundby B/3,
  H II/2, H II/1 bilder 541–595, Lundby på Hisingens B I/3 år 1873,
  1870-indexet eller den blinda A I/13-screeningen utan ny nyckel.
  Den äldre positiva vägen är Östra Fågelvik H II/5:s läsesalsattest 1873.
  C0045766 är en andra H II/1-reproduktion som enligt manifestet avser
  1770–1841 och därför inte är en 1853-route. Hisingens kompletta
  utflyttningsnoll 1873 stärker Stora Lundby-
  routingen tillsammans med länsangivelsen och Lundby i Bjärke-historiken,
  men det är inget vistelsenoll.
  C-0697 har redan läst Hemsjö E/1:s prästbetygsnotering. H V-serien saknar
  katalogiserad volym, datering och bildlänk medan E/1:s IIIF fungerar;
  upprepa inte vigselbilden som bilagesökning och gör inte dokumentankaret
  till ett bild-API-fel eller föräldrabekräftelse. Återta H V först vid ny
  Riksarkivetmetadata/reproduktionskod eller analog beställningskontroll.
  Släktdatas täckningsgap och Geneanets Premiumrad får inte göras till
  personnoll respektive föräldrakälla. Egen föräldrapost eller gemensamt
  hushåll återstår; för inte automatiskt över brodern Johan Augusts
  föräldrar.
- **P-0338 Henrik Henriksson:** A I/4 Lagfors s. 23–33 och A I/5 s. 27–41 är
  redan radlästa. Familias A I/1 s. 34–36 är komplett lästa och ska inte
  upprepas. Återstarta originalen B I/1 s. 15 och A I/1 s. 34–36 via de
  exakta id:na ovan efter ägarens manuella CAPTCHA-bekräftelse eller ny
  laglig bild-URI. Alternativt använder ägaren Medelpads
  Släktforskarförenings medlemsväg till `Lagfors – Ljustorp` och följer en
  registerträff till original. Upprepa inte Släktdatas oförändrade
  täckningsnoll eller Geneanets oförfinade Premiumfråga.
- **P-0339 Margareta Charlotta Sjödin/Sjölin:** 22 Stockholmsregister och
  Ljustorp B I/2:s förda inflyttningsföljd är redan kontrollerade. Återstart
  kräver ny församling, destination, döds- eller bouppteckningsnyckel.

När arbetet senare når djup 5 är P-0415 en exakt återstart för att lösa
fadersnamnskonflikten genom äldre Holm-hushåll och flyttkedjan. Upprepa inte
bara samma födelsenotis eller CEDAR-biografi.

## Riksarkivet: MCP-upptäckt, direkt data/IIIF och Chrome-reserv

Den aktuella regeln är bindande: använd MCP först för lämplig upptäckt och
registerrouting, gå därefter direkt via API/JSON-LD/OAI/IIIF för avgränsning,
original och systematiska svep, och använd Chrome endast när åtkomst eller
interaktiv visning faktiskt kräver den inloggade ytan. Dokumentera exakt
varför övergången behövs. I
batch 86 saknade API/JSON-LD bildlänk för två digitaliserade volymer och
direkt-IIIF gav `403`; först då användes den inloggade katalogen/bildvisaren.
ALTCHA/CAPTCHA får inte lösas utan uttrycklig ägarbekräftelse.

Den fungerande metoden är verifierad med pluginversion **26.820.60940**. En ny
session får inte anta att den gamla browser-bindningen lever kvar:

1. ladda pluginens absoluta `browser-client.mjs`;
2. anslut med `agent.browsers.get("chrome")`;
3. namnge sessionen;
4. skapa alltid en ny styrd flik med `chrome.tabs.new()`;
5. kontrollera `Inloggad som:`/`Logga ut` i DOM;
6. navigera direkt och använd semantiska bildvisarkontroller;
7. hämta `Hela bilden …px (jpg)` och bevara dimensioner samt SHA-256.

Använd ingen AppleScript-styrning, kakextraktion, profilläsning, sandboxflykt
eller övertagning av gamla flikar. ALTCHA/CAPTCHA och `401` är åtkomstbesked,
inte nollresultat. Full metod finns i `genealogy/method-riksarkivet.md`.

## Dashboard — skapa inte en tredje

Det finns två skilda dashboardartefakter:

1. Ett tidigt, tillfälligt lokalt koncept, **Slakt Dashboard Concept**, som
   kördes på `http://127.0.0.1:56542/` och kan vara avstängt.
2. Projektets beständiga implementation i `dashboard/`, **Släktarkivet**, på
   <https://slaktarkivet.rekrevs.chatgpt.site/>. Hostingprojekt:
   `appgprj_6a91bf98d5788191bbd3f09db81e4541`.

Den andra är implementationen som ska utvecklas vidare. Den är skrivskyddad
och bygger `dashboard/public/data/project.json` direkt från projektfilerna;
den har ingen separat faktadatabas. Kör `npm test` och `npm run build` i
`dashboard/`. Publicerad data kan ligga efter arbetsytan. Publicera inte utan
en aktuell användarinstruktion om deployment.

Tidslinjen visar att prototypens artefakt- och uppgiftsstate inte bars fram
över context compaction, vilket ledde till en parallell implementation och en
felaktig efterhandsbeskrivning. Den visar däremot inte att den äldre
byggprompten i just detta fall spelades upp ordagrant: användaren skrev en ny
`ok bygg detta` efter kompakteringen. Den offentliga kommentaren har rättats
så att den gör denna skillnad.

## Context-compaction-buggen

- Korrigerad offentlig reproduktionskommentar:
  <https://github.com/openai/codex/issues/31659#issuecomment-5460997128>
- Relaterade ärenden: `openai/codex#31659`, `#35226`, `#35935`.
- `/feedback`-texten skrevs i chatten, men någon separat kvittens eller
  feedback-session-ID observerades inte.

Det säkert belagda mönstret här är förlust av artefakt-/uppgiftsstate över
compaction, parallellt arbete och därefter felaktig statusbeskrivning. Äldre
promptåterspelning förekommer enligt användarens återkommande erfarenhet, men
dashboardtidslinjen ensam bevisar inte ordagrann återspelning.

## Arbetsyta och bevarande

- Gren: `main`; privat remote: `https://github.com/rekrevs/slaktforsk.git`.
- Batch 66–78, reparationspasset, `dashboard/` och `HANDOVER.md` är
  committade och pushade i `8b55621` (2026-08-29) på ägarens uppdrag;
  arbetsytan var därefter ren.
- Gör inte `git clean`, reset, checkout eller annan bred återställning. Gör
  ingen commit, push eller deployment utan en aktuell användarinstruktion.

## Senast verifierat

Efter batch 228 passerade:

- `node --test scripts/*.test.mjs` — 5/5 tester.
- `node scripts/validate-genealogy.mjs` — 2 598 påståenden, 1 968
  Markdownposter och 4 332 filer i mediakatalogen inklusive `.gitkeep`;
  Wotan-JSON giltig.
- dashboardens datatest och `npm run build` — 500 personer, 2 598
  påståenden och 525 föräldralänkar.
- `node scripts/verify-pedigree.mjs` — P-0004-baslinjen 77.
- `node scripts/verify-depth5-wave.mjs` och
  `node scripts/validate-edition-manifest.mjs` — pass.
- `node scripts/media-manifest.mjs --check` — 4 331 sakmedier (2 528
  exakt, 1 775 käll- och 28 citationsavgränsade), 0 olänkade.
- projekt-, Wotan-, mediamanifest-, observations-, utgåve- och
  dashboard-JSON är giltiga; den nya observationskontrollsumman,
  den oförändrade utgåvan och `git diff --check` passerar.
- den befintliga utgåvan är oförändrad; ingen PDF skapades eller ändrades i
  batchen.

P-0210-auditen till och med djup 4 ger avsiktligt icke-noll och räknar
exakt P-0336 som öppen spets. P-0004 har 77 kända anor; auditen ger
avsiktligt status 1 med tio ogiltiga slutstatusar genom djup 5 och anger
P-0051 som fortsatt nästa tillåtna djup-4-front. Wotans källstyrda
breddrotation fortsätter från batch 228 till P-0336. Ingen PDF skapades
eller ändrades i batchen.

Kör en proportionerlig verifiering efter nästa ändring och skriv resultatet i
T-0012-loggen och dagsloggen.
