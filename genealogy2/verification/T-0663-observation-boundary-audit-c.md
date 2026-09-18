# T-0663: slutprövning av observationssignaler, del c

Datum: 2026-09-17. Avgränsad, läsande förberedelse enligt delegeringen i den pågående Genealogy2-migrationen. Ingen DB, fryst leverans, äldre forskning eller originalbild har ändrats eller öppnats för ny läsning.

**Samtliga 33 tilldelade signalobjekt är sakprövade.** Resultat: **fem bekräftade post-/syntesfel, fem andra bekräftade lagerfel och 23 avförda postgränsmisstankar**. Därefter gav root uttryckligt tilläggsmandat för **två konkret upptäckta grannobjekt**, P0043/related122 och related123; båda har post-/syntesfel. Totalt behandlas alltså **35 objekt: sju post-/syntesfel, fem lagerfel, 23 avförda misstankar**. Inga objekt lämnas som oprövade i denna del.

Urvalet är de första 33 raderna i [grundrapportens](T-0663-observation-boundary-audit.md) tabell över 65 återstående signaler: `O-C0395-Sigfrid-Konstantin-row-marking` till `O-P-0316-C0437-childhood`. Agent a har bekräftat att dess 32 börjar vid `O-P-0343-C0346-s94`. De två senare sidofynden räknas separat och ändrar inte denna gräns.

Aktuella O-revisioner var **@1** för alla 35. R/O, ursprung, R:s avgränsningsbedömningar, direkta versionsberoenden och aktuella representationsmål kontrollerades läsande. Huvuddatabasen användes först och efter T0661:s införsel; under dess korta låsning användes roots verifierade 500-akters förprovsdatabas `genealogy2-T0661-preflight-osygZz/db.sqlite`. Ingen av kandidaternas äldre O/R ändrades av persons10. Inför ett framtida revisionspaket måste aktuella versioner och beroenden läsas på nytt, också efter persons11.

## Beslut för de ursprungliga 33

**B** = bekräftat post-/syntesfel; **L** = rätt källpost, men projektbedömning i råvärdet; **A** = den konkreta postgränsmisstanken avförd. A betyder inte att personens forskning eller varje metadatafält har nygodkänts.

| Nr | Objekt, samtliga @1 | Beslut | Konkret prövning |
|---|---|---|---|
| 1 | O-C0395-Sigfrid-Konstantin-row-marking | A | R-91fb1395f3794cdf22a51dc8 är hushållet på s161. Namn/födelseår överstrukna, dödskolumn inte överstruken står uttryckligen på rad9 i C0395/T0156. Inget dödboksfält har lagts in i värdet. |
| 2 | O-C0396-Sigfrid-Konstantin | A | R-53fd72e667a21401a1f02a0a är F/1 post12. Döds-/begravningsdag, 27 dagar, föräldrar, Gaxa, orsak och tomma fält finns i C0396:s eget tillägg. Den beräknade födelsedagen från jämförelsen har inte införts i O. |
| 3 | O-C0509-witness-Dahlquists-hustru | A | Namnlös hustru till uttryckligt Erik Gustaf Dahlquist i samma födelsepost; egen ort är null. C1017 fullständigar samma R-dcd5dfcfa8ef935f690f7b7f. |
| 4 | O-C0509-witness-Erik-Gustaf | A | Mellansätter[?] hör till detta vittne i samma doppost. Reservation kvar. |
| 5 | O-C0509-witness-Erik-Pehr | A | Arklo hör till drängen Erik Pehr[?] Pehrsson enligt senaste C1017. Ingen brodersrelation eller äldre säker Petter-form i O-värdet. |
| 6 | O-C0509-witness-Jakob | A | Östanskär hör till Jakob Jakobsson i samma vittneslista. |
| 7 | O-C0509-witness-Jakobs-hustru | A | Samma posts uttryckliga namnlösa hustru; referens till Jakob, ingen egen påhittad ort. |
| 8 | O-C0509-witness-Johan | A | Arklo hör till Johan Ersson i samma post. |
| 9 | O-C0509-witness-Johans-hustru | A | Samma posts uttryckliga namnlösa hustru; referens till Johan, egen ort null. |
| 10 | O-C0509-witness-Sophia | A | Sophia Jonsdotter i Östanskär finns i det sena fullständiga vittnesledet C1017/T0136, inte i någon annan doppost. |
| 11 | O-C0848-witness-Britta-Anders | L | Mjöstan[?] hör till samma Svenspost, R-b1609ddef74d345e7968a88a. `kinship_proven:false` är däremot projektets bedömning. |
| 12 | O-C0848-witness-Britta-Erics | L | Kjerrbogärda hör till samma post. Ortreservationen finns i förbehållet. `kinship_proven:false` är projektbedömning. |
| 13 | O-C0848-witness-Kjerstin | L | Kåsegl[?] hör till samma post; samma felplacerade släktskapsbedömning. |
| 14 | O-C0848-witness-Namndeman | L | Hattholt[?] hör till det anonyma vittnet i samma post; Johannes-kandidaten från novemberposten har inte lagts in i rånamnet. Samma felplacerade släktskapsbedömning. |
| 15 | O-C0848-witness-Olof | L | Wässenbo hör till Olof Anderss. i samma post; samma felplacerade släktskapsbedömning. |
| 16 | O-P-0002-C0889-military-empty | A | R-f42593630a33262d1bd6854d omfattar fol275 r1–6. Makens positiva militärfält och hennes tomma rad ligger båda inom R. Värdet drar ingen slutsats om andra böcker eller organisationer. |
| 17 | O-P-0003-C0266-cabins | B | Berättelsens R-31ddf6090af32ffa30920ac9 innehåller byggberättelsen; `familyPhotoYear:1941` kommer från separat foto/bildtext7, R-ebc1b097fdf641489b43ca8c. Se fall B1. |
| 18 | O-P-0003-C0266-photo-childhood | B | R-e287bc29e8195678601ee5e6 är foto/bildtext5; fyraårsåldern och den senare positionsförklaringen kommer från brevets R-2989c302482c679b7fa007d7. Se B2. |
| 19 | O-P-0019-mother-not-named | B | O är knuten till C0919/r10 men JSON:s scope omfattar dessutom C0019:s familj1, en annan R. Se B3. |
| 20 | O-P-0029-own_row1704 | A | `G.B. 1839` är en avläst hänvisning på Ida Sofias egen rad24, inte innehåll hämtat ur den förra boken. A5473 kompletterar uttryckligen C0951:s kortare avskrift. Änkefältet 35 9/4 är också eget. |
| 21 | O-P-0040-BT0813-absence | A | Jan Oskar saknas bland de fyra namngivna gravsatta på läsdagen. Både C0878 och C0879 innehåller samma kompletta fyrlista; O behöver inte slå ihop disjunkta listor. Begränsningen till gravplats/läsdag kvarstår. |
| 22 | O-P-0043-related125-household_role_report | B | R-c2061a9ef8456576c3564fbf omfattar C0911 r1–9. Vigseln1914-12-31 kommer från separat r16–17; sonhustruföljden är en syntes. Se B4. |
| 23 | O-P-0123-C0277-own-row | A | R-9b65e989ea7512c17bdf70ad är hela hushållssidan101. Jämförelsen med hustruns datum och det gemensamma nattvardsdatumet ligger inom R. Senare födelseoriginalets datum/identitet har inte skrivits in som egna råfält. |
| 24 | O-P-0205-C0134-child | A | C0134 säger att samma elva barn visas och tillämpar uttryckligen C0133/T0139:s ortsrättelser på sin egen kontrollerade helbild. Maria Christinas Åkullsjön/Bygdeå är därför inte bara lånat från faderns ansedel. Två visningar är fortsatt ett sekundärt informationsursprung. |
| 25 | O-P-0239-C0255-own | A | R-df14606f839d5a800592eab8 avgränsar uttryckligen samma census-hushålls index/bildrepresentation. Nio namn, familj2 och Anders Ivars egna1903/Hudiksvallfält ryms där; den vuxne missionärens andra poster ligger inte i värdet. |
| 26 | O-P-0247-C0926-384 | A | C0675 och C0926 gäller identisk fysisk post s384 r1–7, R-edf25c5213fddb6fe0a5fcde. Gertruds egna fält inklusive1914 och lysningsreferenser ryms där. Sen kronologi/erkännandeteori har inte smugit in i O. |
| 27 | O-P-0255-C0253-own | A | C1046 är fullare läsning av samma födelsepost10, R-25417249fc98dced0150d888. Datum, Widusina-insättning, föräldrar, T., Högsjö,119 och oläsliga ord ligger i egen post. |
| 28 | O-P-0271-C0253-father | A | Samma post; torpare är markerad tolkning av T., medan överstruket ord fortfarande är oläsligt. Inget senare Höglund-led eller hushållsboksdatum införs. |
| 29 | O-P-0272-C0253-mother | A | Samma post; make, barnets födelse/dop, Högsjö och119 är postegna. Dopvittnets släktskap har inte gjorts till råuppgift. |
| 30 | O-P-0310-C0465-birth | A | C0465/C1015/C1028 gäller samma födelsepost R-fc8bb67308b9870bf697457b. O bevarar råtalet28 och avsaknad av synlig rubrik; andra posters talmängd/modersåldersslutsats ligger inte i värdet. |
| 31 | O-P-0315-C0510-household | B | Själva s108 är rätt. `stepmother:P-0405` förutsätter korrelation med1836postens annan namngiven mor, inte bara s108:s h/2. Se B5. |
| 32 | O-P-0316-C0436-childhood | A | R-45b297a69f523f7abcb7fdf5 är s185. O har födelse1834-03-21 och uttryckligen ingen ortkolumn; s193:s Indahl har inte förts bakåt. |
| 33 | O-P-0316-C0437-childhood | A | R-dd31c2714bc0d4606128259b är s193. Ditto under föreståndarens Indahl återger denna boks egen kolumn. Föräldrarnas nattvard blir inte dotterns. |

## Bekräftade fel och precis revisionsgräns

Alla förslag nedan gäller framtida **nya revisioner**, med gamla @1 bevarade. Ett O-id byter inte typ till F. Föreslagna nya id:n är beskrivande förslag, inte införda objekt.

### B1. Stugberättelsen och foto7

`O-P-0003-C0266-cabins@1`: [C0266](../../genealogy/citations/C-0266-jan-christer-slaktkronika-arne-2011.md), berättelsen och fotografiernas punkt7, håller isär berättande text och bildtext. R:s avgränsningsbedömning delar uttryckligen dokumentet i en berättelse och elva bild–text-par. JSON:s `familyPhotoYear:"1941"` överskrider berättelse-R även om fotografiet är korrekt bundet som context. `ownershipProved:false` är dessutom en forskningsbegränsning, inte sonens råutsaga.

**O@2:** behåll bara den rapporterade byggberättelsen för Orrestaö/1940-talet och Båvens strand nära Årdala/början av1960-talet, med personursprung A1684 som uttryckligen bevarar de utförligare tidsuppgifterna. Ta bort fotoåret och ägarbevisbedömningen ur råvärdet. De senare skall fortfarande framgå som avgränsning/syntes.

**Återbruk/F:** `O-P-0303-C0266-photo-orrestao@1` är kontrollerat på exakt foto7-R och återger1941, Orrestaö och ”vid nybyggda stugan”. Återbruka detta och foto-R som stöd för föreslagen `F-P-0003-family_account-cabins-and-photo1941`, jämte berättelsens O@2. F får beskriva två familjeuppgifter i samma material, utan oberoende korroboration, lagfart eller kostnad. Ingen ny person eller bostadshändelse behövs.

**Beroenden:** inga direkta versionsberoenden funna. Aktuellt representationsmål är P0003/A1684, aktrad61. Det skall nå både den smalare O och fotosyntesen efter rättelsen.

### B2. Foto5 och den senare brevuppgiften

`O-P-0003-C0266-photo-childhood@1`: foto5:s egen bildtext namnger och placerar Arne, Ada, Vilhelmina och Fredrik. [C0266](../../genealogy/citations/C-0266-jan-christer-slaktkronika-arne-2011.md) skiljer sedan uttryckligen ut ett separat meddelande med fyraårsåldern. [Hela C0267](../../genealogy/citations/C-0267-jan-christer-minnen-flen-sodertalje.md) tillskriver meddelandet Jan-Christer. [S0212](../../genealogy/sources/S-0212-jan-christer-janson-minnen-flen-sodertalje.md) anger Jan-Christer som upphovsperson och Sverker som förmedlare. Nuvarande råvärde kombinerar dessa och kallar den senare förklaringen Sverkers.

**O@2:** endast foto5:s egen bildtext: Arne mellan Vilhelmina och Fredrik, Ada sittande till höger om Fredrik. Inget eget fyraårsfält eller senare brevursprung i dess råvärde. Befintliga personkopplingar behöver inte omprövas.

**Egen brev-O/F:** föreslagen `O-P-0003-C0267-photo-childhood-explanation` på R-2989c302482c679b7fa007d7 återger Jan-Christers uppgift om fyra år och positionerna; ingen motsvarande egen brev-O hittades vid återbrukskontrollen. Föreslagen `F-P-0003-photograph_identification-childhood` sammanför foto/bildtext och brevet med korrekt förmedlingskedja. Bevara att C0266/A1680 historiskt säger Sverker; gör inte två uppgiftslämnare eller oberoende ansiktsverifikation av formuleringen.

**Beroenden:** inga direkta versionsberoenden. Aktuella mål P0003/A1680 på rad57 och P0009:s bevarade text på rad178. Båda behöver den kompletta F efter att foto-O smalnats av.

### B3. Gunborgs modersnolla i två skilda poster

`O-P-0019-mother-not-named@1` har `scope:["C-0919 rad 10","C-0019 egen rad i familj 1"]`, trots att `record_id` är R-e15535f496176e63f9c9b415. [C0919](../../genealogy/citations/C-0919-axel-edvard-banvaktstugan-70-hyltinge-1918-1920.md) r10 och [C0019](../../genealogy/citations/C-0019-maj-amalia-folkrakning-1930.md) familj1 är olika poster/böcker. A5407 i akten är uttryckligen en sammanfattning av båda. Att båda R finns i beläggen bevarar ursprunget men gör inte sammanfattningen postegen.

**O@2:** ”Ingen mor namnges på Gunborg Elisabets rad10 i A II a/5 uppslag13”, med bara den egna postens scope. Föreslagen `O-P-0019-C0019-mother-not-named` på R-4b47425bfe4a1bdc3e0449ab håller den separata1930nollan. De befintliga egna1930-O för koder/nattvard/inkomst innehåller inte denna sak och skall inte byggas ut till obestämda samlingsobjekt.

**F:** föreslagen `F-P-0019-source_scope-mother-two-records` sammanför de två avgränsade frånvarona. Behåll Charlotta Cecilia Elisabet som kandidat, utan accepterad moderslänk, och skilj ”inte namngiven här” från ”okänd för samtiden”.

**Beroenden:** inga direkta versionsberoenden. Mål P0019/A0116 rad38, A5407 rad46 och relationsrad54. Deras befintliga faderskap respektive kandidatförbehåll skall förbli nåbara; inget nytt moderskap eller nytt tvillingskap följer av modellrättelsen.

### B4. Elin: r9 är inte r16–17

`O-P-0043-related125-household_role_report@1` ligger på C0911/R-c2061a9ef8456576c3564fbf r1–9. [C0911:s sena fullständiga tillägg](../../genealogy/citations/C-0911-jansson-ljungbacka-flen-1914-1915.md) avgränsar Ture/Elin som ett separat hushåll r16–17, R-836c129ec57720e26352a023. O:s förbehåll erkänner redan att vigseldatumet kommer från de senare raderna, men råvärdet har ändå hela relationssyntesen inklusive vigsel1914-12-31 och ”därefter sonhustru”.

**O@2:** behåll endast Elin Augusta Larssons r9: sömmerska, Gåsinge1882-09-27, från Engelbrekts församling1914-10-15, samt det som faktiskt behövs ur denna avgränsade rad. Ingen senare vigsel/sonhustru i dess råvärde.

**Återbruk/F:** `O-P-0046-A-4239-marriage_household@1` på R-836c129ec57720e26352a023 återger redan det egna hushållets bokförda vigseldatum och båda namnen korrekt. Återbruka den för föreslagen `F-P-0043-family_context-Elin-household-sequence`, med ursprung i relationsrad125 och de interna hänvisningarna mellan r3/r9 och r16–17. [C0910](../../genealogy/citations/C-0910-arne-hos-morforaldrarna-ljungbacka-flen-1918.md) får tillföra sin senare familj endast genom dess egen R om den behövs. Ingen ny P, biologiskt faderskap, exakt fysisk flytt eller geografisk vigselort behövs.

**Beroenden:** inga direkta versionsberoenden. P0043:s relationsrad125 är aktuellt `pending_interpretation`-mål. Bevara dess frågeställning där den går utöver den faktiskt representerade syntesen; pending är ingen ersättning för korrekt R-gräns.

### B5. Lars Petters styvmor är en korrelation

`O-P-0315-C0510-household@1`, R-b4d2026f0cdd001da7dfedde, innehåller `stepmother:"P-0405"` i både JSON och råtext. [C0510:s tolkning](../../genealogy/citations/C-0510-indal-AI8-hogsjo-sida-108-nilsson-dahlsten.md) säger uttryckligen varför: h/2 jämförs med Lars Petters **egen födelsenotis**, vars mor är Lisa Stina Larsdotter. Hushållsboken namnger Lisa Stina Jonsd:r som andra hustru; den säger inte ensam vem som födde sonen. [C0509/C1017](../../genealogy/citations/C-1017-indal-C4-1836-arklo-och-radens-lydelse.md) är alltså en nödvändig annan post för styvmodersslutsatsen.

**O@2:** behåll datum, ort, egen nattvard, kunskaps-/kopptecken,1858 års reserverade utflyttningsnot och korrekt225-klamring. Ersätt den syntetiska styvmodersuppgiften med postens egna namn-/rollformer där den äldre gruppen behöver anges: Nils Pehrsson och `h/2 Lisa Stina Jonsd:r`; sonrollen kan stå som källa. Inga sena ortskandidater eller härledd modersidentitet i råvärdet.

**Återbruk:** `F-P-0315-family_context-six-known-children@1` har redan modernP0404, styvmodernP0405 och den rättade namnformen; `REL-step-P-0405-P-0315@1` har redan kvalificerad styvföräldrarrelation, inte genealogisk föräldrakant. Återbruka dem, plus egna `O-P-0405-C0510-own` och den kontrollerade födelseposten `O-P-0315-C0509-birth`. Ingen ny familjeslutsats behövs. Om beläggsbindningen kompletteras skall den få egen version, inte ändra gamla ursprung.

**Beroenden:** inga direkta versionsberoenden till just detta O. Aktuella mål P0315/A2311 rad48, A2312 rad49, A5840 rad70 och A5841 rad71 (`pending_interpretation`). A2312 måste behålla tillgång till F:s styvmoderssyntes.1858 års hänvisningar och föräldrarnas1861fält ryms i R och är inte i sig fel.

### L1–L5. Fem vittnen har en projektbedömning i rå-JSON

De fem `O-C0848-witness-{Britta-Anders,Britta-Erics,Kjerstin,Namndeman,Olof}` har **rätt postgräns**. [C0848](../../genealogy/citations/C-0848-hemsjo-C4-sven-catharina-kontroll.md) och [C1016](../../genealogy/citations/C-1016-hemsjo-C4-1815-tomrummet-provat.md) återger exakt samma Svenspost16/19feb1815. Ortvärdena hör till respektive vittne. Däremot är `kinship_proven:false` inte något som står i dopboken: det beskriver projektets bedömning av vad namnlikheten kan belägga.

**Precist förslag:** O@2 för var och en tar bort endast `kinship_proven` ur rå-JSON och behåller den individuella orten och läsreservationen. Ingen omidentifiering eller ändrad ort följer. Avför inte den anonyme nämndemannen och ersätt inte hans rånamn med Johannes Andersson.

**Återbruk:** `F-P-0383-identity_boundary-own-baptism-witnesses@1` bär redan de nödvändiga kvalificeringarna: moderns syskon inte bevisade, Johannes-kandidaten inte fastställd och frånvaro av Hansson inte uttömd faderssläkt. Den redovisar också att den sena räkningen av Andersdotterformer inte stämmer med den explicita listan. Ingen ny F eller ny släktrelation behövs.

**Direkta beroenden:** för varje O finns motsvarande `EP-E-baptism-P-0383-<suffix>` och den gemensamma F ovan. De fem EP samt F skall versionsgranskas vid rättelsen; dopvittnesdeltagandet skall bestå. Gemensamt representationsmål är P0383/A3783, aktrad40. Denna andra feltyp skall inte räknas som fem bevis för blandade R-poster.

## Två uttryckligen tillagda sidofynd

Root utvidgade efter konkret rapport delegeringen från33 till33+2. Båda följande objekt ligger på R-c2061a9ef8456576c3564fbf, C0911 r1–9, har endast detta direkta R-belägg och saknar direkta versionsberoenden. Därför fångades de inte av grundrapportens flerkällesignaler. Hela C0910 och C0911 samt deras sena tillägg har lästs ovan.

| Extra | Objekt @1 | Beslut | Exakt fel |
|---|---|---|---|
| 34 | O-P-0043-related122-household_role_report | B | Rårelationsraden förenar Karl Harry på C0911/r6 med C0910/r5:s namngivna mor Elin Augusta Larsson-Jansson och perioden1914–1918. Modersanteckningen och den senare hållpunkten står inte på den bundna1914posten. |
| 35 | O-P-0043-related123-household_role_report | B | Karin Elisabets födelsedatum/ort och fosterbarnsroll finns i C0911/r7, men intervallet1914–1918 sammanfattar också hennes senare C0910/r6. Den förra boken slutar1915;1918 är ingen egen råuppgift där. |

**B6 Karl Harry, egen O@2:** behåll den tidigare postens `Karl Harry`, fosterson,1906-09-07, Nyköpings Östra och den egna familjens registrerade överföring. Stryk inte fosterbarnsrollen. Modersnamnet, den senare Janssonformen och den samlade tidsföljden skall inte tillskrivas denna R. Befintligt omnämnande `M-P-0043-related122` har redan namnformen Karl Harry.

**B7 Karin Elisabet, egen O@2:** behåll den tidigare postens `Karin Elisabet`, fosterdotter,1910-10-02,Kila och egen överföringskontext. Ta bort den syntetiska slutpunkten1918. Befintligt `M-P-0043-related123` tillhör rätt tidigare R.

**Senare egna O och F:** R-e67bb6868b81121b2d3f0732 är redan korrekt avgränsad till C0910/s914 r1–8. Ingen egen O för Karl Harrys r5 eller Karins r6 hittades i återbrukskontrollen. Föreslå `O-C0910-Karl-Harry-row5` med `fb. Karl Harry Jansson` och den uttryckliga modersnoteringen, samt `O-C0910-Karin-Elisabet-row6` med hennes egen `fb.`-rad. Använd vid behov nya radbundna M med just dessa utvunna namn/roller, utan nya P. Föreslagna `F-P-0043-family_context-Karl-Harry-sequence` respektive `F-P-0043-family_context-Karin-Elisabet-sequence` sammanför de registrerade hållpunkterna från båda böckerna.1914–1918 är en dokumenterad följd, inte bevisad oavbruten faktisk omsorg eller uttömmande vistelse. Karl Harrys angivna moderskap till Elin bevaras; Tures biologiska faderskap följer inte.

**Representationsberoenden:** P0043:s relationsrader122 och123 är båda `pending_interpretation`. De behöver sina egna O och F-mål så att datum/roller/modern fortfarande går att följa. Raderna får inte förbli påstått postegna bara för att en tolkning fortfarande är pending. Samordna dessa två revisioner med B4, så att samma Elin och samma senare hushåll inte dupliceras.

## Underlag och avslutningskontroll

Följande **hela citationstexter inklusive sena tillägg** lästes för denna del; referenser till andra källor inom deras analys öppnades bara när de faktiskt behövdes för de35 objektens gränser:

- [C0395](../../genealogy/citations/C-0395-hogby-AI10-gasa-sida-161-carlman.md), [C0396](../../genealogy/citations/C-0396-hogby-F1-kristina-ringberg-dod-1874.md).
- [C0435](../../genealogy/citations/C-0435-indal-C4-lars-petter-1836-negativ-arskontroll.md), [C0509](../../genealogy/citations/C-0509-indal-C4-lars-petter-fodd-1836.md), [C1017](../../genealogy/citations/C-1017-indal-C4-1836-arklo-och-radens-lydelse.md).
- [C0848](../../genealogy/citations/C-0848-hemsjo-C4-sven-catharina-kontroll.md), [C1016](../../genealogy/citations/C-1016-hemsjo-C4-1815-tomrummet-provat.md).
- [C0889](../../genealogy/citations/C-0889-zingmark-burtrask-gammelbyn-1930-1950.md), [C0266](../../genealogy/citations/C-0266-jan-christer-slaktkronika-arne-2011.md), [C0267](../../genealogy/citations/C-0267-jan-christer-minnen-flen-sodertalje.md).
- [C0919](../../genealogy/citations/C-0919-axel-edvard-banvaktstugan-70-hyltinge-1918-1920.md), [C0019](../../genealogy/citations/C-0019-maj-amalia-folkrakning-1930.md), [C0951](../../genealogy/citations/C-0951-ida-sofia-zingmark-dod-1944.md).
- [C0878](../../genealogy/citations/C-0878-oskar-alfred-zingmark-grav-burtrask-1963.md), [C0879](../../genealogy/citations/C-0879-ebba-alfrida-zingmark-grav-burtrask-1997.md), [C0911](../../genealogy/citations/C-0911-jansson-ljungbacka-flen-1914-1915.md), [C0910](../../genealogy/citations/C-0910-arne-hos-morforaldrarna-ljungbacka-flen-1918.md), [C0277](../../genealogy/citations/C-0277-urbom-ajax-hjulfabriken-1861-1865.md).
- [C0133](../../genealogy/citations/C-0133-hans-nilsson-sekundarpost.md), [C0134](../../genealogy/citations/C-0134-anna-christina-jonsdotter-sekundarpost.md), [C0255](../../genealogy/citations/C-0255-anders-ivar-hudiksvall-1910-index.md), [C0256](../../genealogy/citations/C-0256-hook-hushall-hudiksvall-1910.md).
- [C0675](../../genealogy/citations/C-0675-sattna-AIIa4-gertrud-nils-august-hallin.md), [C0926](../../genealogy/citations/C-0926-hallen-henriksson-storbranna-fol-384.md), [C0253](../../genealogy/citations/C-0253-ingrid-christina-vidusina-fodd-1866.md), [C1046](../../genealogy/citations/C-1046-indal-C5-ingrid-vittneskolumn-och-namnnotering.md).
- [C0465](../../genealogy/citations/C-0465-malilla-C4-carl-august-fodd-1825.md), [C1015](../../genealogy/citations/C-1015-malilla-C4-1825-vittnena-utvunna.md), [C1028](../../genealogy/citations/C-1028-malilla-C4-1825-moderns-alder.md).
- [C0510](../../genealogy/citations/C-0510-indal-AI8-hogsjo-sida-108-nilsson-dahlsten.md), [C1018](../../genealogy/citations/C-1018-indal-AI8-sida-108-flyttkolumnerna.md), [C0436](../../genealogy/citations/C-0436-indal-AI6-sater-dahlsten-familj-sida-185.md), [C0437](../../genealogy/citations/C-0437-indal-AI7-sater-dahlsten-familj-sida-193.md), [C1012](../../genealogy/citations/C-1012-indal-AI6-AI7-sater-narlasning-rattelse.md).

De aktuella A-/relationsursprungen kontrollerades särskilt där C är kortare än akten: P0003/A1680,A1684, P0019/A0116,A5407, P0029/A5473, P0043/r122–125 och P0002:s avgränsade militärnolla. Det är återbruk av bevarad forskning, inte ny originalutvinning.

En framtida rättelse behöver sju avgränsade O@2 för B-fallen och fem O@2 som flyttar släktskapsbedömningen till befintlig F. Alla positiva uppgifter och deras källstatus skall bestå. Pröva särskilt att fotoåret/fyraårsåldern ligger på rätt R, att Gunborgs två nollor förblir två avgränsade observationer, att C0911/r1–9 inte bär r16–17:s vigsel eller C0910:s modersnot och1918hållpunkt, och att styvmodersslutsatsen är nåbar via F/relation. Kontrollera därefter aktuella representationsmål, de fem vittnes-EP:s versionsberoenden och den gemensamma F. Detta är ett ändligt förslag, ingen implementerad operation och ingen generell automatisk omskrivning av alla signaler.

## Förberett native-förslag och beroendeprövning efter persons11

Efter uttryckligt uppdrag finns nu [den läsande byggaren](../migration/T-0663-observation-c.mjs), [det fullständiga granskningsförslaget](../migration/T-0663-observation-c-review.json) och [riskkontrollen](T-0663-observation-c-risk.mjs). Byggaren returnerar ändringar, exakta ursprungsspann, representationsbeslut och beroendegranskningar men utför aldrig `apply`.

Förslaget omfattar **22 ändringar: 12 O@2, fyra nya postegna O och sex nya F**. De befintliga styvföräldra- och vittnesbedömningarna återbrukas. **13 enhetsbeslut** får kompletterande mål; befintliga mål, state och question bevaras. Ytterligare fem berörda enheter har redan vittnesbedömningen som mål och behöver ingen ny beslutversion. **15 extra ursprungsspann** redovisas för inläggning av den samordnande operationen. Inga personkärnor, släktrelationer, omnämnanden eller händelser ändras.

Ombyggnad mot den införda 538-aktersbasen stoppade först på två nya transitiva beroenden från persons11. De prövades därefter individuellt mot hela [P0513:s akt](../../genealogy/people/P-0513-olof-hansson-bodarne.md), hela [P0514:s akt](../../genealogy/people/P-0514-britta-andersdotter-bodarne.md), deras aktuella F/ursprung/bindningar samt hela C0848/C1016 inklusive senare tillägg:

- `F-P-0513-source_assessment-witness-count-and-limits@1`: frånvaro av Hansson i listan stänger inte faderns släktvägar. F:s tre namngivna Anders-bärare, villkorliga Johannes-kandidat och gräns mellan vittnets ämbete och Olofs egen roll är fortsatt korrekta.
- `F-P-0514-source_assessment-witness-count-and-limits@1`: Erics är inte Anders. Två Anders-döttrar plus Olof Anderss. ger tre; Johannes är en villkorlig fjärde. A7591/A7592:s räknefel, obestyrkt statistiskt överskott och avsaknad av bevisade syskonlänkar är redan korrekt kvalificerade i F.

Det ger **25 exakta beroendepar och nio unika berörda slutsatsobjekt**: fem vittnesdeltaganden, P0383:s två F och föräldrarnas två F. Alla nio behåller sina befintliga @1 och sina uttryckliga historiska beläggsbindningar efter individuell prövning. Gamla O@1 innehåller samma vittnesuppgifter som O@2 plus den felplacerade bedömningsflaggan; säkra sakuppgifter och slutsatser ändras därför inte. Varje par redovisar exakt `affected_revision_id`, `changed_revision_id`, sakmotivering, bevarad sakdatahash och befintliga beläggsbindningar. Integrationen måste lösa just dessa utlösta requests med respektive motivering; ingen allmän auto-clear föreslås.

Det begränsade bygg- och sakförprovet på 538-basen passerar **12 riskgrupper**. Förslaget kontrollerar gamla revisioner, ursprung, separata postgränser, alla 25 aktuella beroendepar och bevarade enhetsfrågor. Nytt eller ändrat beroende stoppar byggaren för separat prövning. Ingen databasinförsel är utförd av denna del; samlat native-apply-, återställnings- och idempotensprov återstår hos den samordnande agenten.
