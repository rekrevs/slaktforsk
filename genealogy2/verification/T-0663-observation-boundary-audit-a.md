# T-0663: individuell prövning av observationssignaler, del a

Datum: 2026-09-17. Avgränsad delegerad förberedelse: **de sista 32 av de 65 återstående signalerna**, i [huvudrapportens](T-0663-observation-boundary-audit.md) tabellordning. Första objekt är `O-P-0343-C0346-s94`, sista `O-P-0422-C0685-own`. Del c slutar med `O-P-0316-C0437-childhood`; delarna överlappar inte.

**Resultat: två bekräftade överförings-/postgränsfel och 30 avförda signaler.** Alla 32 O är aktuella **@1**. Ingen databas, fryst personleverans, gammal forskning eller originalbild har ändrats eller öppnats för ny läsning. Endast denna rapport är skriven. Avförande gäller den konkreta signalen och är ingen ny full person-, kontrakts- eller bildgranskning.

## Underlag och metod

Läst hela T-0663-loggen och huvudrapporten, aktuella O:s JSON, råvärde, förbehåll, direkta belägg och ursprung; respektive R:s lokalisering och samtliga aktuella avgränsningsbedömningar; samt berörda A-/relations-/textenheter. `value_literal` och `value_json` har samma sakinnehåll i alla 32. Där uppgiften endast finns i personakten, exempelvis egna kunskapsmärken och vaccinationstecken, har det konkreta textursprunget prövats och inte ersatts av en allmän hänvisning till citationen.

Hela följande citationer inklusive sena tillägg är lästa:

- C-0346, C-0831, C-0836: Strandlundhushållet och läsrättelser.
- C-0846, C-1013: de felidentifierade Jonsberghushållen.
- C-0380, C-1014: Hällefors post 67 och jämförelseposternas gränser.
- C-0436, C-0437, C-1012: Dahlstenhushållets två böcker och rättelser.
- C-0848, C-1016: Svens födelsepost och andra poster på uppslaget.
- C-0852, C-1022, C-1029: Målillas olika hushåll och senare återtagna slutsatser.
- C-0509, C-1017: Lars Petters födelsepost.
- C-0522, C-0672, C-0688: Stora Lundbys två positiva delkedjor och omtagning av samma hushåll.
- C-0685, C-0983: Zingmarks hushåll och egna titelgräns.

R/O lästes först i huvuddatabasen. Under T-0661:s tillfälliga skrivlås användes den färdigbyggda läsande 500-aktskopian `genealogy2-T0661-preflight-osygZz/db.sqlite`; huvuddatabasen kontrollerades åter efter införseln. T-0661 ändrar inte dessa O/R. De två bekräftade felens payloads, beroenden, representationsmål och föreslaget återbruk nedan är kontrollerade i huvuddatabasen efter införseln.

Flera C-id betyder ofta senare läsning av samma fysiska post. Det är inte självständiga röster och inte i sig ett postgränsfel. På motsvarande sätt är en familjemedlems uppgift tillåten inom ett R som uttryckligen omfattar hushållet; ett R som uttryckligen avgränsar en enda personrad får inte tyst utvidgas till grannraden.

## Samtliga 32 beslut

| Nr | Aktuellt O | Beslut och konkret grund |
|---:|---|---|
| 1 | `O-P-0343-C0346-s94@1` | **Avförd.** R-e8a90d1636c6a21bedbb8072 är hela Strandlundhushållet s.94. C0346/C0831 är samma bild. Senaste rättelsen december 1815, tom dagruta och Stockholm finns på rätt post; ingen dag 12 påstås. Egen vaccination, blanka fält och årsmärken stöds av A6450, A6454–56, A6459. Hustru/dotter ryms i hushålls-R. |
| 2 | `O-P-0344-C0346-s94@1` | **Avförd.** Samma R. Födelsedatum och Sättna är uttryckliga i C0831 på s.94. A6469 skiljer makens år 39 från hennes egen rad; O gör detsamma. A6468–70, A6473 bär hennes egna tecken/fält. Ingen s.92-hänvisning 224 har lagts här. |
| 3 | `O-P-0344-C0836-s92@1` | **Bekräftat fel.** R-7d99e8402017d41b9b04f1e7 är AI/6 s.92, men `birthplace:"Sättna"` saknar egen postutvinning där. Den uttryckliga Sättna-läsningen i O:s C0831-ursprung gäller AI/7 s.94. A6465 anger på s.92 namn och datum, inte födelseort. Exakt rättelse nedan. |
| 4 | `O-P-0362-C1013-rejected-Anna@1` | **Avförd.** R-cefceacc0fa3c619b2921b59 omfattar de fyra överstrukna raderna Petter/Anna/barnen. Anna Månsdrs `14 28/5`, Jonsb. och Petter är egna hushållsuppgifter. `1814 28/3` är uttryckligen felaktig projektläsning av samma rad, inte aktuell alternativ födelse eller Maja Lenas data. |
| 5 | `O-P-0362-C1013-rejected-Carolina@1` | **Bekräftat fel.** R-827a4773eba203536d07a963 är endast Carolinas egen rad; R:s bedömningar utesluter uttryckligen övriga familjen från denna avgränsning. `spouse:"Nils Danielsson"` kommer från den separat avgränsade föregående raden. Födelse Rönö `29 17/12` och egen råroll H. är riktiga. Exakt rättelse nedan. |
| 6 | `O-P-0362-C1013-rejected-Petter@1` | **Avförd.** Det gemensamma R-cefceacc0fa3c619b2921b59 omfattar Petter, Anna, Johan Fredrik och Anna Maria. Barn och maka ligger därför inom postgränsen. Inget tidigare Lars-datum görs till Petters säkert lästa födelse. |
| 7 | `O-P-0371-C0380-father@1` | **Avförd.** R-ee0b865502220b123b3abf8a är hela födelsepost 67. Modern, barnet och datum ingår i samma post. S. Torpen ersätter samma cells S. Försam.; initialer lämnas oupplösta. Råtalet 31 förvaras utan säker attribution till fadern. Inga orter eller folio från post 80/84 har lånats. |
| 8 | `O-P-0372-C0380-mother@1` | **Avförd.** Samma post 67. 31 år står under Omständigheter, med attributionen till modern uttryckligen obevisad; inget säkert beräknat födelseår ligger i O. Magnusd:r och äldre Magnust:r är samma namnfälts läshistorik. Faderns Hök blir inte moderns eget efternamn. |
| 9 | `O-P-0375-C0436-head@1` | **Avförd.** R-45b297a69f523f7abcb7fdf5 är AI/6 Säter s.185. Datum 1800-10-22, egna blanka fält, v, kunskapsmärken och årsvärden 1836–45 följer C0436:s T0134-tillägg. Ingen födelseort läggs i denna bok. Sidhuvudets mantal är inte hans ägarandel; sista 7/6 lämnas utan valt år. |
| 10 | `O-P-0375-C0437-head@1` | **Avförd.** R-dd31c2714bc0d4606128259b är AI/7 s.193. Indahl står på hans egen rad. Årsvärdena 1847–54, särskilt hans 1847 25/7[?] och 1853 6/4[?], hålls isär från hustruns. Sista 2/7 1854 är positivt belägg, ingen allmän livstidsförlängning. |
| 11 | `O-P-0376-C0436-wife@1` | **Avförd.** AI/6-R som nr9. Januari 1807 bevarar senaste rättelsen från juli. De gemensamt lästa maketecknen i C0436 är uttryckligen belagda på bådas egna rader. Ingen ortkolumn eller AI/7-Frejd-kolumn konstrueras; fastighetsmantal är inte personlig ägarandel. |
| 12 | `O-P-0376-C0437-wife@1` | **Avförd.** AI/7-R som nr10. Hennes födelseort är ditto under Indahl, inte utskrivet ortnamn på egen rad. Hennes 1847 28/3[?] och 1853 6/11 skiljs från makens värden. Den aktuella januari-rättelsen och egna blanka fält är bevarade. |
| 13 | `O-P-0377-C0436-son@1` | **Avförd.** AI/6 s.185, egen Nils Petter-rad inom familje-R. A5852 anger uttryckligen hans tomma koppfält, trots andras v. O överför inte AI/7:s v eller årsmärken till AI/6. A5853:s missvisande allmänna Frejd-rubrik kvalificeras mot C1012:s riktiga AI/6-header. |
| 14 | `O-P-0378-C0436-son@1` | **Avförd.** AI/6 s.185, Lars Johan 1836-07-05. Carl Johan är projektets upphävda läsning av samma namn, inte en ny person. Egenpostens född 3 juli/döpt 5 juli har inte skrivits in som AI/6:s födelsevärde. O anger uttryckligen att övriga egna kolumner inte utvunnits. |
| 15 | `O-P-0378-C0437-son@1` | **Avförd.** AI/7 s.193, Lars Johan och senare datum 5 juli. Endast här finns födelseortens ditto. Varken föräldrarnas årsmärken eller syskonens detaljer tillskrivs honom. Frånvaro av dödnot används inte som belägg att han levde till 1854. |
| 16 | `O-P-0379-C0436-child@1` | **Avförd.** AI/6 s.185 innehåller både Anna Helena och föräldrarna. T0134:s `20/6[?]` och äldre 22 juni bevaras som läshistorik utan vald dag; död 1841-11-10 är redan antecknad här. Dödspostens åldersräkning och broderjämförelse har inte gjorts till råvärden i denna O. |
| 17 | `O-P-0381-C0437-child@1` | **Avförd.** AI/7 s.193. O bevarar konflikten mellan T0134:s reservation och T0194:s senare påstående om reservationslös april, utan att låtsas att T0194 innebar ny bildläsning. Egen födelseposts augusti ersätter inte hushållsradens läshistorik. Dittotecknet är riktigt; den felaktiga sena utsagan att bara detta barn har ortuppgift har uttryckligen avvisats. |
| 18 | `O-P-0382-C0437-child@1` | **Avförd.** AI/7 s.193 har Eric `47 11/12`, dittoort och sonroll. O skiljer Erik/Eric som återgivningar och tillskriver inte barnet eget efternamn eller föräldrarnas nattvard 1854. Egen födelseposts dop 14 december och moderns ålder 47 har inte lånats hit. |
| 19 | `O-P-0383-C0848-birth@1` | **Avförd.** R-b1609ddef74d345e7968a88a är Svens födelsepost 16/19 februari 1815. C0848/C1016 återläser samma post. 33 åhr gäller modern enligt det sena kolumnargumentet; inga andra raders åldersvärden ligger i O. Åboen i Bodarne är föräldraledets stånd/hemvist, inte Svens yrke eller säkert födelsehus. |
| 20 | `O-P-0386-C0852-Anna-Anders@1` | **Avförd.** R-faaf6843ffbb61fd5ab1b597 omfattar Eric Josephssons familj på s.158. Anna Andersdr, hustru och Eric finns inom denna familjegräns. Inga Forsberg- eller gästgiverifält lånats. |
| 21 | `O-P-0386-C0852-Anna-Cath@1` | **Avförd.** R-086a1851c3a3dffaff47de12 är gästgiverihushållet s.138. Målilja 95 hör till Anna Cath. i C1029. O:s förbehåll lämnar familjerelationerna oprövade; textens tolkning änka/ny make skapar inte automatisk relation. |
| 22 | `O-P-0386-C0852-Eric@1` | **Avförd.** Eric-familjens s.158-R som nr20. Hesselby 94 och `pag.139,27`, Anna Andersdr och omnämnda barn är samma familjepost i C1022. Ingen exakt dag eller namngivna outvunna barn tillförs. |
| 23 | `O-P-0386-C0852-Jonas-Hoglander@1` | **Avförd.** Gästgiveri-R s.138. Holtz 95 och ankomst Hogsjhult 25 är hans egna värden i C1029. Ingen färdig makesrelation till Anna Cath. har konstruerats av radföljden. |
| 24 | `O-P-0386-C0852-Jonas-Rahm@1` | **Avförd.** Gästgiveri-R s.138. Gårdveda `94 28/5`, Hesterhult 20 och död `27 Maij 1824` gäller samma Jonas Ra[h]m-rad. Ingen annan persons flytt eller död har tillskrivits honom. |
| 25 | `O-P-0386-C0852-Nytorp-maid@1` | **Avförd.** R-dcbda9cd9ce43d8cb44d16a0 är uttryckligen den överstrukna pigraden, avskild från båda s.158-familjerna. Målilla 05, `pag.114,26` och Nytorp under nr2 hör till den. Varken namn eller familjekoppling har uppfunnits. |
| 26 | `O-P-0386-C0852-PW-Forsberg@1` | **Avförd.** R-c080d99fb40a847b177023a5 omfattar Forsberg/Sara Lena s.158. 1781-08-22, Stockholm och pag.252 är hans rad i C1022. Inga fält från gästgiveriets s.138 ligger här. |
| 27 | `O-P-0386-C0852-Samuel@1` | **Avförd.** Gästgiveri-R s.138. Sonen Samuel Fredric `21 15/4` är positivt utvunnen i C1029. Rårollen son bevaras utan att viss far eller mor avgörs. |
| 28 | `O-P-0386-C0852-Sara-Lena@1` | **Avförd.** Forsberg/Sara Lena-R s.158. Hennes Östergötland 92 och `pag.252,Stockholm` kommer från C1022:s egen rad, inte makens Stockholmsfödelse. |
| 29 | `O-P-0403-C0509-father@1` | **Avförd.** R-dcd5dfcfa8ef935f690f7b7f är hela Lars Petters födelsepost 1836. Moderns namn/25 och båda barndatumen är tillåtna inom samma post. Arklo och frånvaron av h. följer senaste rättelsen; Rosenbergs kontrollposter och senare hushållsdata ingår inte som egna råvärden. |
| 30 | `O-P-0404-C0509-mother@1` | **Avförd.** Samma födelse-R. Hennes 25, Arklo, inget h. samt barnet född27/döpt28 är egna postuppgifter. Ingen exakt egen födelsetid, vigsel eller senare h/2-slutsats har tillförts. |
| 31 | `O-P-0413-C0688-p94@1` | **Avförd.** R-2577c3688450fad3b179ad27@2 omfattar Fredric/Anna-blocket på s.94. C0672 och C0688:s omtagning är samma post, inte två hushåll. Rånot `afl.53` står kvar med två olösta betydelser; sonen på s.115, födelsepostens Olo och vigselpostens åldrar har inte förts in som s.94-värden. |
| 32 | `O-P-0422-C0685-own@1` | **Avförd.** R-de3335bd77494c1e87651fe8 är hela s.470-hushållet. C0983 läser samma egna titelområde; soldat-/bondetitlar från andra barnposter och senare böcker har inte lånats in. Datum, vigseluppgift och familjens 455/Nya bok603[?] är egna hushållsvärden. Vaccintecknet har särskilt textstöd i P0422:s hälsotabell rad212 med C0685, inte enbart i hustruns C0685-rad. |

## Bekräftat fel 1: Sättna på fel bokpost

**Nuvarande objekt:** `O-P-0344-C0836-s92@1`, `property:person_fields`, `record_id:R-7d99e8402017d41b9b04f1e7`, `mention_id:M-P-0344-C0836-s92`. R och M är @1. Status `TRANSCRIBED`, disposition `recorded`.

Nuvarande värde, i både JSON och råvärde:

```json
{"birth":"1813-09-17","birthplace":"Sättna","home":"Högsjö","vaccination":"v.","knowledge_marks":"punkter och klamrar,otolkade","individual_days_assigned_to_years":false,"from_literal":"224","from_place":null,"annual_marks":"flera årgångar1836–1845","book_period":"1836–1846"}
```

**Varför detta är ett överföringsfel:** [C0831](../../genealogy/citations/C-0831-indal-AI7-strandlund-foraldradata-rattelse.md) lokaliserar den positiva Sättna-uppgiften till **AI/7 s.94**. [C0836](../../genealogy/citations/C-0836-indal-AI5-AI6-hogsjo-familjekontroll.md) och [A6465](../../genealogy/people/P-0344-stina-cajsa-larsdotter.md#påståenden) lokaliserar AI/6-hushållet och hennes datum på s.92, men ger ingen egen Sättna-avskrift där. A3192:s övergripande identitets-/kedjeformulering är inte en sådan postegen utvinning. C0831 har ändå lagts som direkt ursprung till AI/6-O, och dess ort återges som rått AI/6-värde.

[C1012](../../genealogy/citations/C-1012-indal-AI6-AI7-sater-narlasning-rattelse.md) redovisar dessutom att AI/6:s kolumnuppsättning på **s.185** saknar födelseortskolumn. Den kontrollen är en relevant invändning mot en automatisk överföring, **inte en i denna audit utförd kontroll av s.92**. Rättelsen ska därför inte påstå att en viss s.92-cell har nygranskats eller bevisats tom. Det som är belagt här är avsaknaden av utvunnet posteget stöd för det importerade värdet.

**Minimal O@2:** samma typ, R, M, status och disposition; ta bort enbart `birthplace` ur både JSON och råvärde. Övriga nio fält behålls exakt. Nytt förbehåll preciserar: ”Ingen egen födelseortsuppgift är utvunnen för AI/6 s.92 i detta underlag. Sättna återges i AI/7 s.94 och personens andra födelseunderlag; uppgiften får inte räknas som ett separat råvärde här.” Äldre proveniens bevaras med C0831 markerad som rättelse-/jämförelsekontext, inte stöd för egna AI/6-fält.

**F och återbruk:** skapa exempelvis `F-P-0344-source_scope-AI6-birthplace-transfer` på P0344, `property:source_scope`, `TRANSCRIBED/accepted`. Föreslaget sakinnehåll:

```json
{"AI6_record":"R-7d99e8402017d41b9b04f1e7","AI6_birthplace_not_extracted":true,"AI7_record":"R-e8a90d1636c6a21bedbb8072","AI7_reported_birthplace":"Sättna","removed_AI6_imported_value":"Sättna","person_birthplace_redecided":false,"additional_independent_source_created":false}
```

Bind den till nya AI/6-O@2 och befintliga `O-P-0344-C0346-s94@1`. Återbruka också `O-P-0344-C0830-birth@1` där den egna födelsepostens Sättna ska visas. `O-P-0344-C0832-census@1` är korrekt 1880-ort men inte en oberoende röst. Ingen ändring av personens födelsehändelse eller antagna födelsesocken motiveras av denna modellrättelse.

Exakta relevanta textursprung: P0344/A3192 rad46, A6465 rad49, A6466 rad50, A6467 rad51, A6468 rad52, A6470 rad54, A6473 rad57; C0831 hela50 rader och C0836 hela77. A1969 rad45 är också nuvarande O-ursprung och representationsmål. Den nya F ska särskilt bindas till A3192 så att kedjeuppgiften fortfarande är synlig som jämförelse.

**Beroenden:** inga direkta versionsbundna aktuella objekt bygger på O@1. Aktuella representationsmål är A1969, A3192, A6465, A6466, A6467, A6468, A6470 och A6473. Bevara deras mål och komplettera där det behövs med F; gör inte de rätta datum-, hänvisnings- eller teckenfälten ofullständiga genom ortsrättelsen. Befintliga `F-P-0344-source_assessment-identity-and-limits@1` och `F-P-0344-source_correction-witnesses-and-neighbour@1` behöver inte skrivas om: de bär andra korrekt avgränsade sakuppgifter.

## Bekräftat fel 2: makens namn utanför Carolinas egen R-rad

**Nuvarande objekt:** `O-P-0362-C1013-rejected-Carolina@1`, `property:person_fields`, `record_id:R-827a4773eba203536d07a963`, `mention_id:M-P-0362-C1013-rejected-Carolina`. R och M är @1. Status `TRANSCRIBED`, disposition `recorded`.

Nuvarande värde:

```json
{"birth_literal":"29 17/12","birth_parish":"Rönö","spouse":"Nils Danielsson","household":3,"not_Carolina_Larsdotter1849":true}
```

**Varför detta är ett postgränsfel:** [C1013](../../genealogy/citations/C-1013-jonsberg-AI7-sida-55-omlast-hushallet-stammer-inte.md), tredje hushållet rader58–60, placerar Nils Danielsson på föregående rad och Carolina på egen H.-rad. R:s locator säger uttryckligen ”hustrun Carolina Carlsdotters egen rad i annat hushåll”. `READ-120431b6ab255f33b8efc688@1` säger att de övriga två familjeraderna avgränsas separat så den gamla personraden inte byter postgräns. `READ-4ceb88a3ef6ab0452934a98d@1` säger att övriga familjens namn inte är avgränsade här. Nils-namnet kan därför inte bli ett råvärde från just detta R.

**Minimal O@2:** behåll samma R/M, status och disposition, samt:

```json
{"birth_literal":"29 17/12","birth_parish":"Rönö","household":3}
```

Makens namn flyttas till en hushållsjämförelse-F. Flaggan `not_Carolina_Larsdotter1849` bevaras som den redan införda, uttryckliga identitetsbedömningen, inte som ett råfält i Carolinas rad. M@1:s `name_literal:"Carolina Carlsdotter"` och `role_literal:"H."` är egna lästa värden och återbrukas oförändrade.

**F och återbruk:** skapa exempelvis `F-M-C1013-Carolina-household-context` med subjekt `M-P-0362-C1013-rejected-Carolina`, `property:source_assessment`, `TRANSCRIBED/accepted`. Föreslaget sakinnehåll:

```json
{"household":3,"page":55,"reported_spouse_name":"Nils Danielsson","spouse_name_record":"R-0910fc8b720c8388a94edf9f","own_role_literal":"H.","rejected_identity_target":"P-0313","rejection_object":"ID-P-0313-not-C1013-Carolina","new_person_created":false,"new_pedigree_relation_created":false}
```

Bind F till nya Carolina-O@2, befintligt `R-0910fc8b720c8388a94edf9f@1` (Nils Danielssons egen rad) och Carolinas M/R. Nils-R:s `READ-0d99e6e614bdfaad5b074f3c@1` binder redan de tre familjeradernas avgränsning till C1013 rader58–60. Inget M/O för Nils finns på detta R vid kontrollen; det behövs inte för att bevara den befintliga lokala hushållsjämförelsen. Skapa ingen ny personkärna, släktkant eller utvidgad Carolina-R av denna anledning. Makens födelsedata ska inte kopieras till F om rättelsen enbart behöver hans namn och hushållsplacering.

Bevara den redan införda `ID-P-0313-not-C1013-Carolina@1`, vars `decision`, disposition och evidensstatus är `rejected/rejected/REJECTED`. Riktigt namn, annat födelseår och hustruroll räcker fortfarande för den avvisade sammanblandningen. ID-objektet blir inte accepted för att själva källobservationen är positiv.

**Direkta versionsberoenden som måste prövas vid O@2:**

1. `ID-P-0313-not-C1013-Carolina@1`, stöd från O@1. Avvisningen består; bind om efter uttrycklig kontroll av att grunduppgifterna består.
2. `SEARCH-P-0362-C1013-page55@1`, stöd från O@1 tillsammans med Anna-/Petter-O. Sidnoll för Lars/Maja Lena och dottern Carolina1849 består. Scope är S0661, AI/7 s.55, tre hushåll, fjorton rader; ingen volym- eller församlingsnolla tillkommer.

Aktuella representationsmål: P0362/A3227 rad35 och A3773 rad36; P0363/A3228 rad36 och A3774 rad37; samt P0363:s textenhet rader108–114. Komplettera dessa med F/fortsatt identitetsutfall där sammanhanget behövs. Alla sex direkta ursprungsenheter från O@1 bevaras: C0846 hela58 rader, C1013 hela108, och de fyra A-raderna. C1013:s exakta familjespann58–60 binder jämförelse-F till båda separata R.

## Avgränsade kontroller vid genomförande

- Kontrollera aktuella versioner på nytt före operationen. Föreslagen revision är **@2** endast så länge @1 fortfarande är aktuell.
- AI/6-O ska sakna födelseorten Sättna medan AI/7-O och den egna födelseposten behåller den. Datumet1813-09-17, 224-hänvisningen och egna tecken ska vara oförändrade. Ingen ny utsaga om en tom s.92-cell får införas.
- Carolina-O ska sakna makens namn och projektets identitetsflagga; samma namn/roll/födelseuppgift finns kvar. F ska nå både hennes egen R och Nils egen R. Den avvisade P0313-identiteten och sidnollans exakta gräns ska bestå.
- Alla gamla @1-revisioner, råvärden och tidigare textursprung ska finnas kvar. De berörda A-/textmålen ska nå både postegna värden och de flyttade jämförelserna.
- Avförda objekt ska inte automatiskt revideras för att flera C-id finns: särskilt Dahlstens olika årskolumner och bokheaders, Hällefors villkorade31, Lars Petters rättade27/28 och Stora Lundbys olösta `afl.53` ska bestå.

Detta är beslutsunderlag, inte en applicerad operation. Beroendegranskning och ordinarie återställnings-/idempotensprov tillhör den kommande versionerade rättelsen inom T-0663.
