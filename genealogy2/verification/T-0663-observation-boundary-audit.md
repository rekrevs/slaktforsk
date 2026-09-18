# T-0663: förberedande granskning av observationsgränser

Datum: 2026-09-17. Utförd som avgränsad delegerad förberedelse medan T-0663:s formella föregångare slutförs. **Ingen databas, fryst personleverans eller gammal forskning har ändrats av denna granskning.** Inga originalbilder, arkivtjänster eller nya personkällor har öppnats.

Resultat från **tolv sakprövade observationsobjekt**: **sju bekräftade postgränsfel**, **en missad senare läsreservation inom samma post**, och **fyra fall utan belagt postgränsfel**. En maskinell inventering redovisas nedan. Flera C-id eller flera belägg är signaler, inte felbevis. Gränsen bestäms av den faktiska R-postens lokalisering och den bevarade källtexten.

Underlag: hela T-0663-loggen och review-formatet, aktuella databasrevisioner, deras ursprung och versionsbundna belägg, R-posternas lokalisering/avgränsningsbedömningar samt **hela** C-0008, C-0014, C-0016, C-0025, C-0026, C-0417, C-0509, C-0559, C-0868, C-0871, C-0878, C-0879, C-0890, C-0962, C-0991, C-0999 och C-1017 inklusive sena tillägg. De berörda personernas A-/relationsursprung har kontrollerats; detta är ingen ny full kontraktsgranskning av dessa personer.

## Sju bekräftade postgränsfel

Samtliga nedanstående O är aktuella **@1** vid granskningen. Föreslagna ändringar är nya revisioner och kompletterande F/O, aldrig ändringar av @1 eller av frysta JSON-leveranser. Objekttypen för ett befintligt id får inte bytas från observation till fact.

### 1. O-P-0027-children-book-sequence

**Fel:** R-54b9a43526242cc9adee6c31 avgränsar Kyrkefalla A II a/15 s.15, Lundkvists hushåll rader1–5. `value_json.nextBook` och `value_literal` tillför Gunilla Birgitta från nästa bok, A II a/20 s.86, R-83ce4c405b6733bac7afd35c. Båda R finns faktiskt i O:s belägg, vilket visar jämförelsens ursprung men inte gör den till råuppgift i s.15-posten.

[C-0868](../../genealogy/citations/C-0868-augusta-smuleberg-1930-original.md), sista T-0151-tillägget, avgränsar raderna1–5 och kvarvarande utvinningsgräns. [C-0871](../../genealogy/citations/C-0871-augusta-smuleberg-1941-vamb.md), arbetsavskriften och T-0194-tillägget, namnger den senare barnlistan och dess integritetsgränser. Personursprung: P0027/A5222 och fyra relationsrader, s.98–101 i akten.

**Föreslagen gräns:** O@2 behåller endast s.15:s tre namngivna barn och dess egen utvinningsgräns. En F om barnföljden återger skillnaden mellan s.15 och s.86 med båda R/egna O som belägg. Återbruka redan införda s.86-observationer för P0296/P0297/P0374 och kommande P0528 där sak och rad verkligen stämmer; skapa inga nya personkärnor eller exakta integritetsminimerade barndatum.

**Beroenden:** två direkt versionsbundna F: `F-P-0373-source_correction-wife-fields-already-known` och `F-P-0373-source_scope-screenshots-and-unread-columns`. Aktuella representationsmål omfattar dessutom P0027/A5222 + fyra relationsrader samt P0373/A7916. Dessa måste få fortsatt åtkomst till hela syntesen när O smalnas av. T0662/P0528 ska inte återanvända den felaktiga O som egen s.86-rad.

### 2. O-P-0021-bjerg-first-marriage

**Fel:** R-fbd26dd590e542972a5cabbb är Mofalla A I/5 s.18, rader1–9. JSON:s `group` innehåller Thilda Augusta. [C-0991](../../genealogy/citations/C-0991-mofalla-AI5-sida18-bjerg-augusta-victoria.md), tabellen och T-0118-rättelsen, har fyra barn i förstaäktenskapsgruppen inklusive Augusta Victoria; Thilda finns **bara i föregående A I/4**, R-8a83ee945b26cabe321fb1ab. Det framgår positivt av [C-0999](../../genealogy/citations/C-0999-mofalla-AI4-sida18-bjerg-forsta-hustrun.md), rad6 och fynd4. O:s enda R-belägg är A I/5.

**Föreslagen gräns:** ta bort Thilda från A I/5-observationens grupp, bevara henne i egen A I/4-O. En F om familjegruppernas följd får bära sammanslagningen. Bevara första-/andraäktenskapsgrupperingen som källans uppgift, inte säker biologisk faderskap/fullsyskonskap. Inga nya personer behövs för denna gränsrättelse.

**Beroenden:** inga direkt versionsbundna objekt hittades. Aktuella textmål: P0021/A0672, A3683, A3684, A3688, A3710 och den samlade relationsprosans rad117. Särskilt rad117 behöver F-syntesen för att inte tappa Thilda när O korrigeras. Samordna med T0662/P0534–0537:s egna korrekt avgränsade poster.

### 3. O-P-0021-household-date-variants

**Fel:** samma A I/5-R som föregående fall, men både JSON och råtext jämför **två böcker**: Carl Johan 1850-07-19/04-24, Anna Sofia 1857-06-02/06-24, Victor Albin 1874-11-13/11-03. C0999:s A I/4 och C0991:s A I/5 ger respektive först/sist i paren. Inget av dessa alternativpar är avskrivet som ett par i A I/5.

**Föreslagen gräns:** egen O på A I/5 återger endast 24april,24juni,3november för respektive barn; egen A I/4-O återger19juli,2juni,13november. Jämförelsen och den tillbakadragna hypotesen om Augustas avskriftsupprepning flyttas till F med båda posterna. Inget av barnens födelsedatum avgörs av denna modellrättelse.

**Beroenden:** inga direkt versionsbundna objekt hittades; aktuella textmål P0021/A3712, A3721 och relationsprosans rad117. De nuvarande målen måste kompletteras med den nya F, särskilt där båda bokläsningarna är assertionens sakliga innehåll.

### 4. O-P-0021-Thilda-household-row

**Fel:** den positiva Thilda-raden är korrekt knuten till A I/4, R-8a83ee945b26cabe321fb1ab, men JSON-fältet `nextBookAbsent:true` är en jämförelse med **A I/5**. C0999/fynd4 säger uttryckligen att hon är överstruken i A I/4 och inte med i A I/5. Bara A I/4-R är versionsbundet i O.

**Föreslagen gräns:** O@2 behåller Thilda Augusta,12okt1861 och överstrykningen i A I/4. Frånvaron gäller det namngivna nästa hushållet och förs i F/avgränsad källbedömning med A I/5 som underlag. Överstrykning + frånvaro blir ingen dödsdag eller dödsslutsats.

**Beroenden:** inga direkt versionsbundna objekt; P0021/A3711 är aktuellt representationsmål. Dess fulla innebörd kräver båda delarna efter rättelsen.

### 5. O-P-0020-C0025-birth1858

**Fel:** R-12cfa4b0cfebd9409730fcb8 är 1900 års folkräkningsblad för Djursätra. Dess eget fadersår är `58`, men JSON har även `comparison_1910:1850`. [C-0025](../../genealogy/citations/C-0025-bernhard-folkrakning-1900.md), T-0176-tillägget, skiljer uttryckligen bladens `58`/`50`; [C-0026](../../genealogy/citations/C-0026-bernhard-folkrakning-1910.md) placerar `50` på 1910-bladet, R-9fcd6c77fb3fbdc8a110e24b. Nuvarande O har endast1900-R som belägg.

**Föreslagen gräns:**1900-O behåller `58`/1858 som källrapport. Jämförelsen mot1910 förs i F med båda R/O. Behåll båda föräldrarnas parallella avvikelse som möjlig överföringshypotes, inte fastställd orsak eller två oberoende originalröster.

**Beroenden:** inga direkt versionsbundna objekt; P0020/A0127 och bevarat textspann266–284 är aktuella mål. Återbruka egen1910-O om dess fält/rad är rätt.

### 6. O-P-0003-C0008-mother-birth-corrected

**Fel:** O är knuten till Arnes födelsepost1915 i Flen, R-70eeff109bc651dce649a0ee, men JSON/råvärde anger moderns födelseort **Lerbo**. [C-0008](../../genealogy/citations/C-0008-arne-godvig-fodelse-1915.md) återger hennes datum `86 19/8[?]` och hemvist Ökna i Floda; den återger ingen födelseort Lerbo i1915-raden. Lerbo och den säkrare1886dateringen kommer från hennes egen originalpost och SCB-utdrag, [C-0016](../../genealogy/citations/C-0016-ada-wilhelmina-originalfodelse-1886.md) och [C-0014](../../genealogy/citations/C-0014-ada-wilhelmina-fodelse-1886.md). Alla tre R är redan belägg till O, men detta är en personsyntes.

**Föreslagen gräns:**1915-O återger den där lästa reserverade födelsesiffran och rättelsens egen läshistorik; ingen Lerbo-ort förs in som råuppgift från1915. Återbruka modern P0009:s befintliga1886-O/event och för korrelationen/rättelsen i F. Original R-dc7d8a2eba63d983a98e6aa5 och SCB R-0d1c75412788b5465ccb5bd3 är beroende återgivningar; uppgradera inte antalet oberoende röster. Det är inte fel i sig att modern observeras i barnets födelsepost.

**Beroenden:** inga direkt versionsbundna objekt; P0003/A0045 är aktuellt mål och behöver F eller återbruk av P0009:s rätta objekt. Moderns personidentitet och etablerade födelse avgörs inte på nytt.

### 7. O-P-0368-C0559-death

**Fel:** R-3f36aa1ea9e58476d9dd64da avgränsar Högby F/2,1895s.1 **post3**. O:s JSON och råtext innehåller också `comparison_row10_field_filled:true` och `initial_N_comparisons` med Nils Peter på **rader2 och6**. [C-0559](../../genealogy/citations/C-0559-hogby-F2-oskar-mauritz-carlman-dod-1895.md), T-0194-tillägget, är entydig om dessa andra radnummer. Jämförelserna är relevanta läsargument men ligger utanför R:s post3.

**Föreslagen gräns:** O@2 behåller post3:s positiva död/burial/yrke/hemvist, reserverade sanatorieort, tomma egna attestfält och rättade anteckning `Liket hämtades till hemmet.` + `E116`. Kontrollradernas innehåll och handstilsargument förs i en F/assessment med exakta C0559-textursprung; skapa inte nya kontrollpersoner. Ingen ny bildläsning och ingen säker sanatorieort följer av rättelsen.

**Beroenden:** sex direkt versionsbundna objekt: `E-death-P-0368`, `EP-E-death-P-0368-P-0368-principal`, `E-burial-P-0368`, `EP-E-burial-P-0368-P-0368-principal`, `F-P-0368-life_scope-raw-death-note-and-open-middle`, `F-P-0368-name_scope-Adelbert-Adalbert`. A2456 och A7913 är textmål. Datumen behöver inte ändras när stödets postgräns rättas; beroendegranskningen måste uttryckligen bekräfta det och behålla läsargumentet.

## Ett bekräftat fel av annan art

### 8. O-P-0021-census-1930

R-d2dae342a01c14af474e5fbf avgränsar den rätta SCB1930-familjegruppen. JSON/råtext har enbart huvudyrkeskoden `3-103-21`. Hela [C-0417](../../genealogy/citations/C-0417-folkrakning-1930-augusta-alva-smuleberg.md), sista T-0151-tillägget, anger att samma cell senare ligger närmare `2-102-21`, utan avgörande läsning. **Missad senare reservation, inte blandning av två R.**

Föreslagen O@2 bevarar båda läsningarna, samma cell och olöst val; en kodbedömning ska inte välja yrke eller inkomsten500 utan belagd enhet. Inga direkt versionsbundna objekt hittades. Aktuella textmål: P0021/A2138,A2139,A2140,A3267. Samordna med den kvalificering som T0662 redan tillför utan att upphäva dess rätta Värsås-/Skövdegräns.

## Fyra kontroller där postgränsfel inte är belagt

### 9. O-P-0021-grave-birth-and-other-burials

**Den konkreta misstanken avförs som postgränsfel med nuvarande modell.** R-6927d7c76f11c87f82841eb4 är `burial_plot_register`, locator hela gravplatsen04A194,195,196; dess gränsbedömning READ-67373b07ab30e2fd13ee4468 säger uttryckligen **fyra namngivna gravsatta**. Hela [C-0962](../../genealogy/citations/C-0962-eliasson-familjegrav-varsas.md) återger Augusta, Per Vilhelm, Ragnar och Tekla från samma gravplatsvy. De tre personernas fält i O ryms inom den befintliga R-gränsen. Inga separata person-R har slagits ihop i detta O.

De faktiska gränserna består: ingen lokal svarskopia enligt senare avstämning, gravregistret visar inte biologiska relationer, och Ragnar/Tekla-identifikationerna var LEAD vid denna överföring. Dessa ger inget mandat att göra en automatisk R-split. Inga direkt versionsbundna objekt; A3612/A3613 är befintliga textmål.

### 10. O-P-0033-church_fields

`comparison:[B,ab,ab,b]` väckte signal, men R-67f44133b117de7897502fa2 omfattar uttryckligen **hela Rosinedahlshushållet rader1–13**, inte bara Johan Magnus egen rad6. [C-0890](../../genealogy/citations/C-0890-zingmark-rosinedahl-degerfors-1910-1920.md), sista tillägget, placerar samtliga jämförda råtecken på rader3–8 inom denna R. **Ingen visad övergång till annan R.**

Johan Magnus `A.N.` och skalans oklara innebörd är rätt åtskilda i O/förbehåll. Påståendet om högsta bokstav är en bedömning; gör det inte till prestations-/skolslutsats. Arrayen behöver inte läsas som komplett avskrift av alla syskons rader. Inga direkt versionsbundna objekt; A7721 och bevarat textutfall är mål.

### 11. O-P-0039-BT0813-absence

Två R-belägg väckte signal: Oskars R-e7d485f210b9d3a322c3b56f och Ebbas R-0d13f1e0e6bc75acbf8426e2. Hela [C-0878](../../genealogy/citations/C-0878-oskar-alfred-zingmark-grav-burtrask-1963.md) **och** [C-0879](../../genealogy/citations/C-0879-ebba-alfrida-zingmark-grav-burtrask-1997.md) återger samma fyra gravsatta inom BT0813. O:s utsaga om Alfred Torgnys frånvaro kräver därför inte att två disjunkta personlistor sammanfogas; båda bevarade beskrivningarna bär listan. **Inget bekräftat blandningsfel.**

De två R är personregistreringsposter med gemensam medgravsattelista. Om fortsatt modellering vill uttrycka hela gravplatsens undersökning mer direkt är en native search/F med S0691, BT0813, läsdag2026-09-05 och fyra uppräknade poster tydligare än en implicit personpostnolla. Det är ett modelleringsförslag, inte skäl att upphäva den giltiga begränsade nollan. Ingen slutsats om hans död eller annan grav. Inga direkt versionsbundna objekt; A4904 är mål. O-P-0040-BT0813-absence har inte räknats som ett trettonde sakprov och kvarstår i maskinlistan.

### 12. O-P-0315-C0509-birth

Två direkta C-ursprung, men **samma födelsepost**: R-dcd5dfcfa8ef935f690f7b7f, Indal C/4, bildC0033077_00137. Hela [C-0509](../../genealogy/citations/C-0509-indal-C4-lars-petter-fodd-1836.md) och [C-1017](../../genealogy/citations/C-1017-indal-C4-1836-arklo-och-radens-lydelse.md) beskriver samma bild/post och rättar avskriften, senast T-0136. O:s född27dec1836, döpt28dec, rättat27 ovan äldre29, Arklo som föräldrahemvist, modern25 och inget uttryckligt hustrutecken är **egna postuppgifter**. Rosenbergkontrollen och senare hushållsbokens datum har inte skrivits in som råa värden i O. **Inget postgränsfel.** Inga direkt versionsbundna objekt; A2171,A2309,A2310,A5839 är mål.

## Föreslagen ändlig rättelse och beroendekontroll

Ett kommande avgränsat revisionspaket kan omfatta **de sju namngivna O-gränserna plus kodreservationen**, deras nya/återbrukade postegna O och F-synteser samt exakt de berörda representations- och versionsberoendena ovan. Behåll alla gamla revisioner, alla positiva källuppgifter och alla olösta identitets-/datumkonflikter. Före applicering kontrolleras då aktuella versioner på nytt, särskilt efter T0662:s införsel. Inventeringens återstående signaler kräver senare individuell prövning; de är inte automatiskt fel eller automatiskt godkända. Ingen ny Wotan-kö skapas i denna rapport.

Testa mot fasta källfall att s.15-O saknar Gunilla, A I/5-O saknar Thilda, de separata böckernas datum stannar på rätt R,1915-O inte tillskrivs Lerbo från1886, post3 inte bär kontrollrader2/6/10, och att alla jämförelser fortfarande är nåbara som F via de ursprungliga A-/relationsraderna. Pröva kodens två läsningar och att kontrollfallen9–12 inte skrivs om enbart för antalet belägg. Kör därefter beroendegranskning, idempotens och ordinarie import-/återställningsprov enligt T0663:s plan.

## Kontroll av T0662 del c:s könsmetadata

Min sena ifyllnad av `sex` för P0519–0527 byggde på moder/hustru/son/dotter, **inte på ett separat utvunnet könsfält**. Namn/patronymikon användes inte, men detta uppfyllde ändå inte review-formatets uttryckliga regel: ”Kön kräver explicit uppgift, aldrig rollord/namn.” Jag rapporterade felet innan frysning.

Root delegerade därefter en uttrycklig rättelse av de **ännu ofrysta** egna11c-filerna: alla nio kärnor har nu `sex:null`, råroller och relationsuppgifter är oförändrade, och generatorer/refinement/riskförväntning är konsekventa. Begränsat läsande byggförprov passerade på nytt:9personer,583kuraterade ändringar,67A,79relationsrader,920byggda operationsändringar. Ingen DB-operation gjordes. Denna separat auktoriserade rättelse är ingen ändring av01–09 eller av denna audits read-only-underlag.

## Maskinell inventering

Populationen är observationsobjekt **skapade i persons01–09**, men inventeringen läser deras **aktuella revision**. Därmed ingår även tre O-P-0266-C300-* som senare fått @2 i T-0658/source-precision-v1. Att bara filtrera den aktuella operationens namn hade felaktigt tappat dem. En träfffri observation är inte sakgodkänd av denna maskinella kontroll.

Signaler: **B** = `nextBook|otherBook|laterBook|previousBook` i JSON/råvärde; **J** = uttrycklig jämförelse-/flerboksprosa i samma fält; **C** = fler än ett distinkt direkt citation-ursprung; **R** = fler än ett distinkt direkt R-belägg. Kända P0021-objekt från T0663-loggen läggs till som riktade frön även när orden inte matchar. Återgivna C-id i tabellen är R-postens maskinellt hämtade citationsursprung, inte påstående att alla dessa hela C har saklästs.

Detektorn är medvetet begränsad. Tidiga O har ofta bara A-id som direkt ursprung, och en akt kan sammanställa flera C utan signal i råvärdet. Tabellen är därför en **ändlig misstankelista**, inte ett bevis för att alla andra O har rätt postgräns. De tolv sakproven ovan är hela det manuellt prövade urvalet.

<!-- MACHINE_INVENTORY -->

Population: **2794 O**. Maskinella signaler: **73**. Med fyra riktade frön: **77**. Sakprövade: **12**. **65 återstående signalobjekt**, listade nedan utan felklassificering.

| Ursprunglig operation | Skapade O |
|---|---:|
| T-0652/persons-01-v1 | 687 |
| T-0653/persons-02-v1 | 196 |
| T-0654/persons-03-v1 | 357 |
| T-0655/persons-04-v1 | 46 |
| T-0656/persons-05-v1 | 265 |
| T-0657/persons-06-v1 | 332 |
| T-0658/persons-07-v1 | 369 |
| T-0659/persons-08-v1 | 305 |
| T-0660/persons-09-v1 | 237 |

| O-id och aktuell version | Signal | Egen R | R:s citationsursprung | O:s direkta C-ursprung |
|---|---|---|---|---|
| O-C0395-Sigfrid-Konstantin-row-marking@1 | C | R-91fb1395f3794cdf22a51dc8 | C-0395 | C-0395, C-0396 |
| O-C0396-Sigfrid-Konstantin@1 | C | R-53fd72e667a21401a1f02a0a | C-0396 | C-0395, C-0396 |
| O-C0509-witness-Dahlquists-hustru@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-C0509-witness-Erik-Gustaf@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-C0509-witness-Erik-Pehr@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-C0509-witness-Jakob@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-C0509-witness-Jakobs-hustru@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-C0509-witness-Johan@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-C0509-witness-Johans-hustru@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-C0509-witness-Sophia@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-C0848-witness-Britta-Anders@1 | C | R-b1609ddef74d345e7968a88a | C-0848 | C-0848, C-1016 |
| O-C0848-witness-Britta-Erics@1 | C | R-b1609ddef74d345e7968a88a | C-0848 | C-0848, C-1016 |
| O-C0848-witness-Kjerstin@1 | C | R-b1609ddef74d345e7968a88a | C-0848 | C-0848, C-1016 |
| O-C0848-witness-Namndeman@1 | C | R-b1609ddef74d345e7968a88a | C-0848 | C-0848, C-1016 |
| O-C0848-witness-Olof@1 | C | R-b1609ddef74d345e7968a88a | C-0848 | C-0848, C-1016 |
| O-P-0002-C0889-military-empty@1 | J | R-f42593630a33262d1bd6854d | C-0889 | — |
| O-P-0003-C0266-cabins@1 | R | R-31ddf6090af32ffa30920ac9 | C-0266 | — |
| O-P-0003-C0266-photo-childhood@1 | R | R-e287bc29e8195678601ee5e6 | C-0266 | — |
| O-P-0019-mother-not-named@1 | R | R-e15535f496176e63f9c9b415 | C-0919 | — |
| O-P-0029-own_row1704@1 | B | R-f97991f08c7b097bb3f3197e | C-0951 | — |
| O-P-0040-BT0813-absence@1 | R | R-e7d485f210b9d3a322c3b56f | C-0878 | — |
| O-P-0043-related125-household_role_report@1 | R | R-c2061a9ef8456576c3564fbf | C-0911 | — |
| O-P-0123-C0277-own-row@1 | J | R-9b65e989ea7512c17bdf70ad | C-0277 | C-0277 |
| O-P-0205-C0134-child@1 | C | R-b2ccf2e48852c1253d23158d | C-0134 | C-0133, C-0134 |
| O-P-0239-C0255-own@1 | C | R-df14606f839d5a800592eab8 | C-0255, C-0256 | C-0255, C-0256 |
| O-P-0247-C0926-384@1 | C | R-edf25c5213fddb6fe0a5fcde | C-0675, C-0926 | C-0675, C-0926 |
| O-P-0255-C0253-own@1 | C | R-25417249fc98dced0150d888 | C-0253 | C-0253, C-1046 |
| O-P-0271-C0253-father@1 | C | R-25417249fc98dced0150d888 | C-0253 | C-0253, C-1046 |
| O-P-0272-C0253-mother@1 | C | R-25417249fc98dced0150d888 | C-0253 | C-0253, C-1046 |
| O-P-0310-C0465-birth@1 | C | R-fc8bb67308b9870bf697457b | C-0465 | C-0465, C-1015, C-1028 |
| O-P-0315-C0510-household@1 | C | R-b4d2026f0cdd001da7dfedde | C-0510 | C-0510, C-1018 |
| O-P-0316-C0436-childhood@1 | C | R-45b297a69f523f7abcb7fdf5 | C-0436 | C-0436, C-1012 |
| O-P-0316-C0437-childhood@1 | C | R-dd31c2714bc0d4606128259b | C-0437 | C-0437, C-1012 |
| O-P-0343-C0346-s94@1 | C | R-e8a90d1636c6a21bedbb8072 | C-0346 | C-0346, C-0831 |
| O-P-0344-C0346-s94@1 | C | R-e8a90d1636c6a21bedbb8072 | C-0346 | C-0346, C-0831 |
| O-P-0344-C0836-s92@1 | C | R-7d99e8402017d41b9b04f1e7 | C-0836 | C-0831, C-0836 |
| O-P-0362-C1013-rejected-Anna@1 | C | R-cefceacc0fa3c619b2921b59 | C-0846 | C-0846, C-1013 |
| O-P-0362-C1013-rejected-Carolina@1 | C | R-827a4773eba203536d07a963 | C-0846 | C-0846, C-1013 |
| O-P-0362-C1013-rejected-Petter@1 | C | R-cefceacc0fa3c619b2921b59 | C-0846 | C-0846, C-1013 |
| O-P-0371-C0380-father@1 | C | R-ee0b865502220b123b3abf8a | C-0380 | C-0380, C-1014 |
| O-P-0372-C0380-mother@1 | C | R-ee0b865502220b123b3abf8a | C-0380 | C-0380, C-1014 |
| O-P-0375-C0436-head@1 | C | R-45b297a69f523f7abcb7fdf5 | C-0436 | C-0436, C-1012 |
| O-P-0375-C0437-head@1 | C | R-dd31c2714bc0d4606128259b | C-0437 | C-0437, C-1012 |
| O-P-0376-C0436-wife@1 | C | R-45b297a69f523f7abcb7fdf5 | C-0436 | C-0436, C-1012 |
| O-P-0376-C0437-wife@1 | C | R-dd31c2714bc0d4606128259b | C-0437 | C-0437, C-1012 |
| O-P-0377-C0436-son@1 | C | R-45b297a69f523f7abcb7fdf5 | C-0436 | C-0436, C-1012 |
| O-P-0378-C0436-son@1 | C | R-45b297a69f523f7abcb7fdf5 | C-0436 | C-0436, C-1012 |
| O-P-0378-C0437-son@1 | C | R-dd31c2714bc0d4606128259b | C-0437 | C-0437, C-1012 |
| O-P-0379-C0436-child@1 | C | R-45b297a69f523f7abcb7fdf5 | C-0436 | C-0436, C-1012 |
| O-P-0381-C0437-child@1 | C | R-dd31c2714bc0d4606128259b | C-0437 | C-0437, C-1012 |
| O-P-0382-C0437-child@1 | C | R-dd31c2714bc0d4606128259b | C-0437 | C-0437, C-1012 |
| O-P-0383-C0848-birth@1 | C | R-b1609ddef74d345e7968a88a | C-0848 | C-0848, C-1016 |
| O-P-0386-C0852-Anna-Anders@1 | C | R-faaf6843ffbb61fd5ab1b597 | C-0852 | C-0852, C-1022 |
| O-P-0386-C0852-Anna-Cath@1 | C | R-086a1851c3a3dffaff47de12 | C-0852 | C-0852, C-1029 |
| O-P-0386-C0852-Eric@1 | C | R-faaf6843ffbb61fd5ab1b597 | C-0852 | C-0852, C-1022 |
| O-P-0386-C0852-Jonas-Hoglander@1 | C | R-086a1851c3a3dffaff47de12 | C-0852 | C-0852, C-1029 |
| O-P-0386-C0852-Jonas-Rahm@1 | C | R-086a1851c3a3dffaff47de12 | C-0852 | C-0852, C-1029 |
| O-P-0386-C0852-Nytorp-maid@1 | C | R-dcbda9cd9ce43d8cb44d16a0 | C-0852 | C-0852, C-1022 |
| O-P-0386-C0852-PW-Forsberg@1 | C | R-c080d99fb40a847b177023a5 | C-0852 | C-0852, C-1022 |
| O-P-0386-C0852-Samuel@1 | C | R-086a1851c3a3dffaff47de12 | C-0852 | C-0852, C-1029 |
| O-P-0386-C0852-Sara-Lena@1 | C | R-c080d99fb40a847b177023a5 | C-0852 | C-0852, C-1022 |
| O-P-0403-C0509-father@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-P-0404-C0509-mother@1 | C | R-dcd5dfcfa8ef935f690f7b7f | C-0435, C-0509 | C-0509, C-1017 |
| O-P-0413-C0688-p94@1 | C | R-2577c3688450fad3b179ad27 | C-0522, C-0688 | C-0672, C-0688 |
| O-P-0422-C0685-own@1 | C | R-de3335bd77494c1e87651fe8 | C-0685 | C-0685, C-0983 |

### Reproducerbart urval

Populationens SQL (öppna databasen läsande):

```sql
SELECT c.object_id, c.version, c.operation_id, o.*
FROM current_revision c JOIN observation o ON o.revision_id = c.id
WHERE EXISTS (
  SELECT 1 FROM revision r
  WHERE r.object_id = c.object_id AND r.version = 1
    AND r.operation_id GLOB 'T-06*/persons-0[1-9]-v1'
);
```

För varje rad söks B/J-uttrycken ovan i `value_json + value_literal`. C räknas genom `origin → unit → legacy_entity(kind=citation)` för aktuell O-revision. R räknas genom `dependency → revision → object(kind=record)`. Distinkta id:n räknas; dubbla ursprungsspann i samma C blir inte flera citationer. Detta kompletteras med de fyra riktade P0021-fröna. Kända historiska rättelser identifieras via aktuell revision; de görs inte om på grund av gammal @1-text.
