# T-0115: historisk förberedelse till slutrevisionen

Denna daterade arbetsavstämning bevarar vad som kontrollerades före införandet.
Slutresultat och aktuella dispositioner redovisas i [T-0115-report.md](T-0115-report.md).

Kontrollerad 2026-09-18 mot 40 operationer och 43 366 aktuella objekt i
`genealogy2/data/research.sqlite`, före applicering av T-0110:s rättelser.
Detta är förberedelse under pågående T-0110, inte start, slutrapport eller
DONE för T-0115. Huvuddatabasen, Wotan och det frysta arkivet har inte ändrats.
T-0110:s slutliga operationsnummer och mätresultat måste tillföras senare.

## Underlag och avgränsning

Samtliga inkommande punkter i `wotan/dev-log/T-0115.md` har jämförts med
aktuella objekt, gällande beslut, kod och befintliga migrationskontroller.
Granskningen använder avslutade individuella genomgångar; den gör inte en ny
manuell genomgång av 536 personer eller en fullständig databasombyggnad.

- De 45 `migration/persons-??-?.json` innehåller 538 olika person-id, utan
  dubbletter. Alla har läsanteckning och dokumentunderlag. Dokumentens lagrade
  SHA-256 stämmer med de frysta filerna. Paketen har sammanlagt 5 130
  påståendedispositioner och 4 366 relationsdispositioner. Alla 536 aktuella
  nativepersoner täcks. Detta belägger individuell granskning och spårbarhet,
  inte att varje forskningskrav är uppfyllt.
- P-0295 är identitetsalias till P-0027. P-0412 är avvecklad arkivreferens till
  P-0453 efter förkastad namnläsning, **inte** ytterligare ett identitetsalias.
  Ingen av dem är en egen aktuell person. Därav 538 granskningar/536 personer.
- Inga importenheter saknar dispositionsbeslut. 87 018 aktuella enhet–mål-länkar
  finns. [T-0663-report.md](T-0663-report.md) skiljer 35 109 strukturellt
  konverterade, 47 734 textbevarade, 6 797 historikbevarade och 8 214
  tolkningsväntande enheter. Textbevarande är inte semantisk slutgranskning;
  de 8 214 är inte lika många nya Wotan-uppgifter.
- `node genealogy2/cli.mjs inventory` gav 536 personer, 511 aktiva,
  199 godkända identitetsbedömningar, 51 som passerar identitets-/trädgrinden,
  0 uttryckligt godkända nya livsbildsbedömningar och 5 äldre godkända
  kontraktsbedömningar. De fem sistnämnda omfattas av styrningsmotsägelsen nedan.
- `node --test genealogy2/test/review.test.mjs genealogy2/test/inventory.test.mjs genealogy2/test/pedigree.test.mjs genealogy2/test/overview.test.mjs`:
  **26 godkända, 0 underkända**. Proven täcker positiva/negativa grindfall,
  motsägande och inaktuella bedömningar, oavgjorda beroenden, separata
  identitets-/livsbildsaxlar, typade släktkanter, kandidater och bevarade förbehåll.
- `node scripts/verify-pedigree.mjs`: **PASS, 90 härledda anor** i den historiska
  baslinjekontrollen. Det är inte den aktuella verifierade antavlans mått.
  Skriptet avslutar numera med felkod vid avvikelse; den gamla felkodsbristen
  i T-0115-loggen är inte längre aktuell.
- Fulla kohort-/återställningsprov återanvänds från
  [T-0643-report.md](T-0643-report.md), [T-0663-report.md](T-0663-report.md),
  respektive `test/person-cohort*.test.mjs` och `verification/persons-*-risk*.mjs`.
  De har inte körts om i denna förberedelse. Exempelvis prövar sista
  kohorttestet individuell disposition, bevarade tidigare rader och återspelning.

## Samtliga inkommande observationer

**Belagt hanterat** gäller det uttryckligen angivna fallet, inte hela korpusen.
**Representation ersatt** betyder att den gamla felmekanismen inte används av
den auktoritativa modellen. **Kontroll återstår** kräver avgränsad verifiering
eller disposition. **Sakligt följdarbete** får inte räknas som löst av migrering.

| Inkommen fråga | Disposition och konkret belägg i dagens modell | Återstår i T-0115 eller beslutat följdarbete |
|---|---|---|
| Sjufältslistan i `Arbetsläge`, tidiga akters avvikande rubriker | **Representation ersatt.** Bedömningar läses som versionerade nativeobjekt; `lib/review.mjs` skiljer identitet, trädverkan och äldre helkontrakt. De positiva/negativa review-proven passerar. `docs/research/person-contract.md` anger uttryckligen att den frysta rubrikformen inte är det nya skrivformatet. | Dispositionera det äldre formatkravet mot nuvarande fält-/grindkontrakt. Skriv inte om historiska akter för att skapa skenbar enhetlighet. Kontrollera att obligatoriska nativefält har relevanta negativa validatorprov. |
| Levande personers PK-08 och helnivå; både ursprungsfrågan och loggens `AVGJORD` | **Saklig styrningsmotsägelse.** PCD-2026-09-09-029 säger att samtliga sju förlorar helnivåsignalen till T-0034. T-0115-loggen och aktuella äldre bedömningar behåller däremot GODKÄND för P-0005, P-0006, P-0041, P-0269 och P-0270. P-0269/P-0270:s bedömningsförbehåll erkänner uttryckligen motsägelsen. Inventory räknar fortfarande fem äldre godkännanden. | Stäm av och rätta aktuell helnivå centralt mot ägarbeslutet; dokumentera motsägelsen och bevara historiken. Identitet och ägarbekräftade fakta ska inte sänkas. T-0034 är READY och äger den separata nätforskningen; utför den inte inom slutrevisionen. |
| OWNER_CONFIRMED; A-1553–1560 och undantaget A-0020 | **Belagt hanterat.** De åtta gamla påståendenas aktuella sakmål — födelsehändelser, namn-/identitetsuppgifter och föräldrarelationer — har OWNER_CONFIRMED enligt PCD-2026-09-09-028. A-0020 motsvaras av `F-P-0004-name_form-self` CORROBORATED. Källavskrifter behöver inte själva byta till ägarstatus. | Bevara detta vid helnivårättelsen. `domain.test.mjs` har skydd mot otillåten nedgradering; `person-cohort-05.test.mjs` prövar familjeuppgifterna. |
| Sex tillkomna och två bortfallna anor; P-0088:s spökkant | **Belagt hanterat, med olika sakutfall.** P-0082/P-0519 → P-0065 är accepterade typade föräldrar. P-0326 har inga föräldrarelationer; barnkorrelationen ger inte biologiska föräldrar. P-0536 → P-0021 och P-0537/P-0538 → P-0536 är accepterade relationer, men deras individuella identitetsgrindar är underkända. P-0264/P-0265 → P-0123 är candidate/LEAD. Historisk baslinje har daterade rättelser och PASS. Nativeantavlan följer typade kanter och personens grind, inte den gamla felaktiga P-0088-härledningen. | Redovisa de åtta olika dispositionerna; generera inte om en baslinje för att dölja dem. Återanvänd `persons-07-risk-checks.mjs`, `persons-11-part-d-risk.mjs` och kohort-06-testet. Ny verifierad antavla efter T-0110 ska kontrolleras separat. |
| Definitionen av EJ BÄRANDE och sidopersoners status | **Avgjort av senare ägarbeslut.** PCD-2026-09-11-035 och nuvarande personkontrakt anger BÄRANDE för faktisk anlinje till Adam/Axel; säker sidoperson är EJ BÄRANDE. Den äldre föreslagna tolkningen i T-0115 är därmed ersatt. | Bekräfta senare beslutets företräde i slutrapporten; återställ inte de 73 omklassificerade profilerna enligt den gamla förslagsformuleringen. |
| Kvalificerande prosa med `far`/`mor`; 24 celler/15 akter | **Representation ersatt.** `lib/pedigree.mjs` läser `relation_type='parent'`, riktning, disposition och natur; den tolkar inte släktord i rationale/caveat. Kandidat, konflikt och personens identitetsgrind prövas separat. | Lägg vid behov till ett uttryckligt litet regressionstest med släktord i fri prosa för att direkt motsvara den inkomna felklassen; de körda proven täcker typade roller men inte exakt denna formulering. |
| `far till`/`mor till` gäller tredje person; P-0016 och P-0287 | **Belagt hanterat i aktuell relationsmängd.** P-0016:s föräldrar är P-0110/P-0111; inga falska P-0015 → P-0016. P-0287:s föräldrar är P-0336/P-0337; barnet P-0239 är separat. Nativeföräldraskap härleds inte ur en text om tredje person. | Samma fokuserade prosa-/rollregression som föregående rad; ändra inte äldre arkivprosa enbart för parserns skull. |
| Namn efter personlänk: först 42 rader/10 akter, senare 245/64 i T-0173; mallkrav | **Representation ersatt och äldre rättelse dokumenterad.** Nativekanter refererar objekt-id och överlever namnets visningsform; personöversikt och typad antavla har passerande tester. Migrationspaketen innehåller individuella dispositionsbeslut för relationsenheterna. | Ange uttryckligen att nytt obligatoriskt format är typad relation, inte Markdownlänkens placering. Ingen ändring av fryst personmall behövs. |
| `CONFLICT` i fri Tid/plats-text stoppar giltig kant | **Representation ersatt.** Nativegrinden prövar explicit disposition/bedömning och beroendeversion, inte substrängar i fri text. Den äldre parsern har fortfarande fritextmönster och ska inte användas som aktuell kunskapsgrind. | Lägg det exakta negativa störningsfallet i samma avgränsade regression som släktprosan om det inte redan täcks när slutrevisionen görs. |
| Täckningsöversiktens korsprodukt: historiskt 404/138 och 396/136 | **Kontroll återstår.** Ommätning av 554 tabellrader ger 512 radvisa kandidater, 494 unika person–citation-par över 154 personer. Algoritm: varje rads P-id × C-id, kandidat när C-id saknas i personens frysta fil. Detta är varken 494 sakfel eller ett mått direkt jämförbart med de daterade äldre utfallen. Importerad täckningstext är uttryckligen inte semantiskt granskad. | Pröva kandidatlistan mot dagens nativebelägg, negativa kontroller och radens verkliga omfattning; korsprodukten kan skapa irrelevanta par. Prioritera P-0411 (21 radpar), P-0337 (19), P-0315 (18), P-0239 (17), P-0287 (16), P-0316 (15). Besluta ändligt följdarbete för rester som inte kan dispositioneras inom revisionen. Även motsatt riktning, utelämnade berörda personer, ingår. |
| Ofullständiga `Stödda påståenden`; 552/870 citationer och 2 633 saknade bakåtlänkar i äldre mätning | **Faktisk kvarstående mekanism.** Nativeberoenden har versionsstyrning och omprövning, men äldre ursprungslänkar är inte fullständiga sakberoenden. `inspect` för C-id använder importenheter, mål och origins; det expanderar inte alla aktuella prosaomnämnanden till slutsatser. C-0721 visar att rättade födelseobservationer har noll aktuella nedströmsberoenden trots saklig användning i andra objekt. | T-0110 måste göra manuell, objektvis effektanalys. T-0115 behöver besluta ett begränsat förbättringsarbete: komplett synlig rättelsepåverkan, skillnad mellan omnämnande/proveniens/belägg samt test av en faktisk kopierad slutsats. Skapa inte automatiskt stödrelation från varje C-id i en text. |
| Uppgift utan spår: P-0082:s `1796 3/9` | **Det konkreta ursprunget återfunnet.** C-0064:s övre Jon/Ulrika-post finns som `R-6be04582ec19e700c612f06c`, åtskild från nedre hushållsposten; egen rad har datumet. Därmed är detta inte längre en uppgift utan tillgängligt källinnehåll. | Slutkontrollera den aktuella datumslutsatsens exakta beroende vid rättelsepåverkanskontrollen. Korrekt datum i detta fall bevisar inte att övriga uppgifter utan spår saknas; börja sådan kandidatsökning i prioriterade täckningsgrupper. |
| Obevarade batch-84-läsningar: Anna Karolina Stenberg, Anders Edvard Åberg; S-0440 läst intervall | **Belagt kvalificerat, sakfrågor öppna.** `F-P-0426-source_history-unpreserved-adult-claims` anger evidence_preserved=false, marriage_created=false och spouse_created=false. `F-P-0429-partner_hypothesis-aberg` anger verified=false, archival_mention_created=false och krav på bevarad sida759. S-0440 skiljer äldre orientering725–760 från enda bevarade756 och öppna andra sidor. | Behåll hypoteserna som hypoteser. Avgränsa kartläggning av ytterligare påståenden från samma obevarade intervall; eventuell ny originalforskning ska få eget utförbart uppdrag. Att historiken nämner ett namn räknas inte som accepterad make. |
| A-2438/C-0552 hänvisar till759 men källan täcker756 | **Sakstödet har dragits tillbaka i aktuell hypotesrepresentation.** Åberg-objektet kräver just759 och skapar varken arkivomnämnande eller relation. Den gamla felaktiga länken bevaras som historia. | Ett lokaliseringstest kan flagga motsägande sida/post för nya stöd, men bevisar inte ensamt att ett dokument stöder en relation. Kombinera med ovanstående batch-84-disposition. |
| SCB/utdrag C-0257 Hudiksvall1900, C-0353 Helsingtuna1890 | **Belagt hanterat på postnivå.** `R-d203b0c2be21bd912c05f0cc` respektive `R-bfb57a8a02ff68548f60867c` anger uttryckligen utdrag ur församlingsbok/husförhörsbok och återkallar oberoende röst. Källstrategins K-08 säger att utdrag inte är oberoende av originalet. | Kontrollera kvarvarande synteser i de konkret berörda personerna, inte bara källpostens dependence_note. Nya bestämda påståenden om oberoende kräver verklig produktionskedja. |
| Hela Indals församlingsblad1880; C-0348/C-0832/S-0275 och fem personer | **Belagt hanterat i granskade aktuella synteser.** R-b94f43d83f34c17c9559c91c och R-8c140bc6859ebcb89d15668b avser olika poster på samma blad18; de är inte två oberoende röster. S-0275 rättar församlingsomfånget. P-0315/P-0316:s aktuella RESEARCH/PK-09 och P-0254:s RESEARCH anger samma bokföringskedja; P-0271:s familjesyntes varnar för tre skenoberoende röster. Ingen motsatt oberoendeformulering hittades i den riktade genomsökningen av dessa fem personers aktuella objekt. | Återanvänd `evidence-cohort.test.mjs` för C-0348. Generalisera inte resultatet till alla SCB-församlingar: den generella regeln är beroende tills annat belagts, inte ett nytt antagande om oberoende. |
| C-0839: noll på fel by och fel sida | **Kvalificerat men sakligt följdarbete.** `R-e6e4a5e1f810f0bb6f527a25` anger387[?], Utan G[å]rstads Rote/G[å]rstad[?], äldre397/Orrevalla/Gäddestad felaktigt. Detta får inte bli ett säkert Orrevalla-noll. | T-0286 äger prövning mot ortregistret. Kravet att läsa den egna sidans rubriker finns i nuvarande fullutvinningsnorm; inget nytt globalt ursprungsantagande behövs. |
| C-1055 som stöd för P-0065:s syskon | **Kvarstående evidenskonflikt synlig.** R-b0e359298b9139018c7eff63 bevarar motsägelsen mellan äldre avskrift med sex barn och senare T-0163-text att syskon saknas. Den saknade reproduktionen A0001440_00141 gör att enbart den senare texten inte avgör saken. `evidence-cohort.test.mjs` prövar att konflikten bevaras. | Kontrollera att varje aktuell syskonrelation stöds av sin verkliga egen källa och inte av ett generellt C-1055-noll. T-0464 äger återanskaffning/bevarandeskuld. Redovisa inte alla tre gamla felcitationsfall som sakligt slutna enbart för att gamla loggen säger rättade. |
| C-0467 som stöd för P-0517/P-0518:s föräldrapar | **Källomfång återgivet korrekt.** C-0467/R-a6968f39ef7aed43c5dbfbcc har dottern Fru Joh. Chr. Bökelund i annat hushåll. Egen födelsepost C-0851/R-f70518686d7a7c98d9d5bb80 anger Samuel Bökelund och Gustava Maria Rybergsd:r; den andra C-0851-posten hålls separat. P-0518:s aktuella namn är Rybergsdotter. | Kontrollera aktuell relation/identitetsbedömning mot just födelsepostens version; enbart C-id:s förekomst i täckningsöversikten är inte belägg. Äldre filnamnet Kylenstjerna är historik, inte aktuell namnform. |
| PK-11: ska saknad reproduktion fälla identitetsnivån? | **Gällande regel behålls.** Nuvarande personkontrakt placerar PK-11 på identitetsnivån. Inget senare beslut om flytt till livsbild har påträffats. Migrations-DONE eller bevarad text upphäver inte den materiella spärren. | Dispositionera förslaget som ingen regeländring inom T-0115. T-0393, T-0432, T-0444 och T-0464 är befintliga avgränsade följduppgifter; deras sakutfall får inte räknas som genomförda här. |
| Fulla tryckta kolumner: Wigd, Död., tom cell kontra oläst, Oförm./Förm. | **Norm införd; aktuell verifiering kvarstår.** PCD-2026-09-09-027 och nuvarande personkontrakt kräver fulla relevanta kolumner vid nya/omarbetade poster, inklusive tomt/oläst. Kravet är inte retroaktiv omskrivning av allt material. T-0110:s visuella granskning ger det avgränsade bakåtprovet och visar nya brister i C-0721. | Redovisa T-0110:s kolumnutfall separat från felaktiga huvuduppgifter. Maskinvalidering kan kräva att fält redovisas men kan inte intyga att ett original lästs fullständigt. Besluta eventuell liten schema-/valideringsförbättring med denna begränsning. |
| S-0711:s titel bara Floby trots Kalmar, Norra Öland och Malmö | **Faktisk aktuell rättelse återstår.** S-0711@1 heter fortfarande `SvenskaGravar.se, gravsatta i Floby pastorat`; beskrivningen omfattar fler områden och C-0960. | Rätta nativekällans aktuella titel/omfång genom versionerad operation, med äldre titel bevarad. Uppdelning behövs bara om faktisk källidentitet motiverar det. Ingen ny webbgranskning krävs för denna redaktionella rättelse. |
| C-0884/C-0889: egna hushållsrader nådde inte P-0005/P-0006 | **Belagt återfört med förbehåll.** C-0884 har separata aktuella poster för Tranbäret1, Mejseln3 och Gondolen2; Hertig Karls väg40 skiljs från minnesuppgift42. C-0889 har separata egna hushållsposter för Oskar, Birger och Ebba; barnens födelseort är blank på1006 men Burträsk på275. Aktuella persontexter tar upp raderna och rättelserna. | Detta löser exemplen, inte felklassen. Korsprodukt och C-0721:s påverkansanalys visar varför allmänna propageringskontroller fortfarande behövs. |
| Blankrad bryter påståendetabell; äldre fyrkolumnstabeller | **Representation ersatt.** Aktuella påståenden och relationer är typade objekt och personvyn renderas från dem. Nativeöversiktens tester prövar att förbehåll/konflikter inte försvinner. Individuella migrationsdispositioner inkluderar de äldre tabellraderna. | Mappa acceptanskriteriet till maskinvaliderade nativefält och renderingsprov. Börja inte retroaktivt putsa det frysta arkivets tabeller för att få T-0115 DONE. |
| Sammantryckt språk i C-0871/C-0899/C-0944 och andra ledgertillägg | **Kontroll/disposition återstår.** Råcitat och daterade äldre anteckningar ska bevaras; nya aktuella tolkningar ska vara läsbara. T-0110-utkasten skiljer ny aktuell rättelse från ordagrant bevarad äldre lydelse. | Skriv ett uttryckligt utfall: språkkravet gäller nya aktuella projekttexter, råcitat/historik ändras inte globalt. Granska nya rättelsetexter; eventuell större historisk språkputs ska inte smygas in i slutrevisionen. |
| C-0128: fel namn kvar i titlar/filnamn | **Konkreta nativepersoner rättade.** P-0187@2 Anders Ersson, P-0189@2 Per Eric Ersson, P-0190@2 Stina Cajsa Ersdotter. Vittnesroll och identitetsbegränsning bevaras; kohort-03-testet prövar korrigerade läsningar. Frysta filnamn är inte aktuella modellnamn. | Gör en begränsad avstämning av de registrerade namnfallen, inklusive P-0518. Skapa inte namnbytesarbete i frysta arkivet/dashboard. En framtida titelrättning behöver korrigera aktuella namn-/identitets-/berättelseobjekt, inte historiska råcitat. |
| Avvecklade akter och personer tillkomna efter ursprungsinventering | **Täckning belagd för dagens mängd.** Alla 536 nativepersoner finns i individuell granskning; P-0295/P-0412 har explicita olika avvecklingsutfall. Sista kohorterna täcker de senare personerna och tillförda riskgrupperna. | Kör mängdavstämningen igen efter T-0110 ifall personmängden ändrats. Migreringsstatus får inte ersätta aktuellt identitetsutfall. |

## Nytt från T-0110 som måste ingå i slutrevisionen

1. **C-0721 är en ny sakrättelse med bred textpåverkan.** Walla uppger Lena
   `1785 31/10`, inte `1783 21/10`. Johanna har hushållsdatum `1819 30/4[?]`,
   skilt från egna födelsebokens 30 maj. Kandidaten Helena1785-10-31 är fortfarande
   inte identifierad med Lena; moderns ålder34 bevaras utan automatisk utjämning.
   [T-0110/c0721-impact-draft.json](T-0110/c0721-impact-draft.json) identifierar
   40 direkt berörda aktuella objekt/48 fält samt 12 följdobjekt för full utvinning.
   [T-0110/c0721-correction-draft.json](T-0110/c0721-correction-draft.json) är
   ett **oapplicerat** förslag med 56 ändringar. Versionsberoenden och kvarvarande
   omprövningar måste stämmas av individuellt efter faktisk applicering.
2. **Beroendegrafen saknar verkliga kunskapskopplingar.** De två berörda
   observationerna `O-P-0477-C0721-Walla@1` och `O-P-0475-Walla-child@1` har
   noll aktuella nedströmsberoenden. Kopierade fakta, frågor, söknycklar och
   profilsammanfattningar måste därför hittas genom innehållssökning. Som
   omfattningssignal saknar 1 350/3 424 facts, 1 302/1 306 questions och
   538/538 narratives explicita beroenden. Detta är **inte lika många fel**:
   migrationsformatet tillåter ursprungsbunden text. Men C-0721 bevisar att
   automatisk omprövning inte ensam kan uppfylla T-0115:s propagationskrav.
3. **C-0235 LIBRIS innehåller faktiskt exakta sekundäruppgifter.** Bevarad
   authority-JSON har födelse19020409 och död19910918 och anger Sveriges dödbok
   samt *Kvinnan som red över Himalaya* som konsulterade källor. Den gamla
   formuleringen om inga exakta datum och ospecificerat institutionellt oberoende
   kan inte stå kvar. [T-0110/c0235-correction-draft.json](T-0110/c0235-correction-draft.json)
   är ett **oapplicerat** 18-ändringsförslag som bevarar råsvaret och preciserar
   beroendet. Sekundäruppgifterna är inte nya accepterade livshändelser.
   Authority-svaret avgör inte de äldre bibliografiska länkar som saknas där.
4. **Även övriga T-0110-rättelser måste ingå i den slutliga påverkan.**
   Vid denna förberedelse finns ytterligare oapplicerade utkast:
   [C-0048](T-0110/c0048-correction-draft.json) (post78 sammanblandad med
   post79:s Dahlbergvittnen, inklusive felaktiga deltaganden och identiteter),
   [C-0277](T-0110/c0277-correction-draft.json) (Adelas födelsedag, Edlas
   utflyttning och återtagen säker dag för Frans),
   [C-0510](T-0110/c0510-correction-draft.json) (Lisa Cajsas och Lars Petters
   giftceller samt osäkert rådatum för Nils, med C-0511 åtskild), och
   [huvudagentens övriga datumrättelser](T-0110/root-corrections-draft.json)
   (C-0457, C-0925 och avgränsning C-0352). Här är endast deras registrerade
   operationsomfång kontrollerat; huvudagenten ansvarar för bildgranskning,
   slutlig sakbedömning, applicering och full påverkan. Ingen av dem får
   försvinna ur T-0115:s efterkontroll bara för att tidigare migrationsprov
   passerade.
5. **Slutligt stickprovsutfall saknas ännu.** T-0110:s urval, analyserade enhet,
   nämnare, feldefinition, faktiska fel, fullutvinningsluckor och osäkerheter
   måste redovisas separat. Ingen felfrekvens eller konfidensslutsats bör
   uppfinnas från antalet rättade nativeobjekt. Korrigerade textkopior är inte
   lika många oberoende originalfel.

## Återstående, avgränsad körordning för huvudagenten

1. Avsluta T-0110: granska/applicera dess slutliga operationer, pröva varje
   berörd aktuell slutsats och kvarvarande omprövning, redovisa mätutfallet.
   Ovanstående utkast är underlag, inte facit om slutliga versionsnummer.
2. När T-0115:s beroenden är klara: verifiera personmängd/granskningscoverage
   igen och återanvänd kohorternas individuella utfall. Full ombyggnad och ny
   full manuell personläsning krävs inte av de nu identifierade problemen.
3. Genomför de två konkreta aktuella rättelserna: levande personers motsägande
   helnivåsignal enligt gällande PCD och S-0711:s källtitel. Behåll identitet,
   ägaruppgifter, historik och separata livsbildsnivåer.
4. Dispositionera täckningskandidaterna och de riktade sak-/beroendekontrollerna
   ovan. Varje materiell rest måste ha motivering och beslutat, ändligt Wotan-
   följdarbete före T-0115 DONE. Föreslagna teknikförbättringar är ännu inte
   beslutade uppgifter. Befintliga T-0286/T-0393/T-0432/T-0444/T-0464 ska
   återanvändas där de faktiskt täcker frågan.
5. Kontrollera att framtida fyndpass kräver avstämning före DONE enligt
   `wotan/README.md` och `genealogy2/docs/working.md`. Komplettera riktade
   nativeprover för fri prosa/statusord och rättelsepåverkan om de exakta
   felmekanismerna saknar regression. En fryst Markdownvalidator är inte
   tillräckligt skydd för nya nativeoperationer.
6. Kör relevanta slutkontroller på aktuell modell och sammanställ rapporten
   med separata utfall för **format**, **konsolidering**, **identitet** och
   **livsbild**. T-0115 DONE får varken betyda att alla personer är godkända
   eller att framtida bevarandeforskning redan är gjord.

## Förberett statusutkast och föreslaget ändligt följdarbete

[T-0115-status-correction-draft.json](T-0115-status-correction-draft.json)
innehåller **15 oapplicerade revisioner**: fem äldre bedömningshuvuden, fem
PK-08, två explicita premissbedömningar, två PCD-gränsbedömningar och S-0711.
Alla förväntade versioner stämde vid kontroll mot 40-operationersdatabasen.
Ingen ändring träffar ett OWNER_CONFIRMED-objekt. Alla identitets-/trädhuvudrader
är jämförda ordagrant och oförändrade; inga person-, relations-, observations-
eller händelseobjekt ändras. Ingen ny native livsbildsgranskning skapas.

Det finns inget separat lagrat `research_state`-objekt för dessa personer:
aktuella signaler hämtas ur bedömningsobjekten. Utkastet rättar just dessa
signaler och deras explicita motsägande premisser. Äldre granskningsdatum står
kvar som datum för den individuella granskningen; den avgränsade statusrättelsen
har ett eget daterat avsnitt. Det exakta PCD-avsnittet är redan bevarat som
importenhet `31f992ab15d556279b8751035297d8c219338869e9b3ef114e04c8d7b488c95e`
(PROJECT-CONTROL.md:4755–4788) och läggs till som styrningsproveniens.

**Aktuella anspråk som ändras:** de fem `ASSESSMENT-P-NNNN`-huvudenas
Kontraktsgranskning/outcome; de fem `CONTRACT-P-NNNN-PK-08`-utfallen/raderna;
`ASSESSMENT-P-0005-path-premise`, `ASSESSMENT-P-0006-path-premise` och
`AS-P-0269-profile-PCD029-boundary`, `AS-P-0270-profile-PCD029-boundary`.
**Daterad överföringshistorik som lämnas:** identiska kopior av migrations-
läsanteckningen i 80 övriga assessment-caveats, listade nedan. De redovisar
vilken äldre profiltext som överfördes och har inget eget helnivåkriterium.
Den centrala rättelsen säger uttryckligen att de inte är konkurrerande aktuella
helkontraktsbeslut. De skulle vara missvisande om en vy presenterade dem som
aktuella statusbeslut; därför ska huvudagentens slutliga personvyprov också
kontrollera denna skillnad. De får inte räknas som 80 nya statusprövningar.

S-0711 har 24 direkta, oförändrade beroendeobjekt (23 record, 1 search).
Versionsoperationen kan därför kräva omprövningsbeslut även om sakuppgifterna
är oförändrade. Efter applicering ska huvudagenten pröva hela den faktiska
beroendekön; detta utkast gissar inga omprövnings-id eller masskvitterar dem.
Källändringen ändrar titel, första rubrik och tillför ett daterat omfångsförtydligande;
övrig äldre beskrivning bevaras ordagrant.

Förslag till **en ändlig följduppgift efter T-0115**, ännu inte skapad eller
beslutad i Wotan: *Dispositionera täckningsöversiktens fasta 494 kandidatpar
mot aktuell native evidens*, storlek L med fyra faser om högst125 par. Frys
mängden i [T-0115-coverage-candidates-draft.json](T-0115-coverage-candidates-draft.json)
(512 ursprungsrader, 494 unika par, 154 personer); nytillkomna kandidater ingår
inte automatiskt. Arbeta med redan bevarade källtexter och aktuell databas.
Ingen ny bildhämtning, bred personläsning, full ombyggnad, ny generation eller
allmän bakåtkomplettering ingår.

Varje par ska få exakt nativeobjekt/version och ett motiverat utfall:
redan korrekt representerat; negativ kontroll; irrelevant korsprodukt;
historisk/förkastad kandidat; verklig sakuppgift saknas; spårbarhetslänk saknas;
eller olöst på grund av bristande underlag. Klassificera citationens verkliga
post/personomfång före eventuell ny stödrelation. En textträff eller gemensam
rad räcker inte för att skapa stöd. Enkla entydiga representation-/länkfel kan
rättas versionerat inom uppgiften med individuell påverkan; tvetydig identitet
eller nytt originalbehov får en exakt separat ägare. ACCEPTANS: alla494 par
har disposition, alla512 ursprungsrader kan spåras, inga kandidater räknas
slentrianmässigt som fel, varje verklig rest har en ändlig ägare och varje
applicerad rättelse har avstämd påverkan. Delmängder kan återanvända samma
redan granskade post men måste motivera varje person–citation-par.

Befintliga uppgifter som redan äger konkreta luckor ska återanvändas:

| Ägare | Exakt befintligt omfång som inte ska dubbleras |
|---|---|
| T-0034, READY | Öppen nätinformation för de levande; villkoret bakom de fem helnivårättelserna. |
| T-0286, BLOCKED efter T-0115 | Inga Nilsdotters Oklundanyckel/Orrevallakandidat; C-0839:s ort- och sidprövning. |
| T-0393, BLOCKED efter T-0115 | P-0015: C-0923 gravpost och C-0973 bilden F0015634_00156; T-0237 äger övriga C-0973-bilder. |
| T-0432, BLOCKED efter T-0115 | Fullbilder C-0985, C-0986/A0012148_00132, C-0074; avgränsat från T-0237/T-0240. |
| T-0444, BLOCKED efter T-0115 | C-0384, C-0385 och16 Hemsjökopior; C-0945 hänvisas redan till T-0232. |
| T-0448, BLOCKED efter T-0115 | Sävar A I/8 b714,738,759 för P-0426/P-0428/P-0429 samt kartläggning av andra påståenden från batch84:s obevarade sidor. Detta täcker uttryckligen Stenberg/Åberg-frågan. |
| T-0464, BLOCKED efter T-0115 | Degerfors A I/3 sida262 och A I/7b sida400, inklusive barnrader/C-1055 och bevarandeskulden. |

En **separat teknikuppgift**, om huvudagenten beslutar den, bör begränsas till
rättelsepåverkansvyn: visa versionsberoenden, importursprung och textomnämnanden
som skilda signaler, med regression för C-0721:s faktiskt missade slutsatser.
Den får inte automatiskt konvertera textträffar till stödrelationer eller kräva
omläsning av alla personer. Den löser navigationsmekanismen, medan
494-parsuppgiften avgör de fasta sakliga kandidaterna.

Exakt oförändrad mängd kopierade migrationsanteckningar:

- P-0006: `RESEARCH-P-0006-9d76f0343410@1`, `KEY-P-0006-3a90881c940b@1`, `KEY-P-0006-720d19a54885@1`, `KEY-P-0006-aa60b392fb9f@1`, `KEY-P-0006-e60e57df3b5f@1`, `KEY-P-0006-e9fd104d8626@1`, `THEME-P-0006-ID@1`, `THEME-P-0006-REL@1`, `THEME-P-0006-BO@1`, `THEME-P-0006-ARB@1`, `THEME-P-0006-EKO@1`, `THEME-P-0006-MIL@1`, `THEME-P-0006-SAM@1`, `THEME-P-0006-HAL@1`, `THEME-P-0006-PER@1`, `THEME-P-0006-SYN@1`, `PATH-P-0006-KP-01@1`, `PATH-P-0006-KP-02@1`, `CONTRACT-P-0006-PK-01@1`, `CONTRACT-P-0006-PK-02@1`, `CONTRACT-P-0006-PK-03@1`, `CONTRACT-P-0006-PK-04@1`, `CONTRACT-P-0006-PK-05@1`, `CONTRACT-P-0006-PK-06@1`, `CONTRACT-P-0006-PK-07@1`, `CONTRACT-P-0006-PK-09@1`, `CONTRACT-P-0006-PK-10@1`, `CONTRACT-P-0006-PK-11@1`, `CONTRACT-P-0006-PK-12@1`.

- P-0269: `RESEARCH-P-0269-9d76f0343410@1`, `KEY-P-0269-cbd294238233@1`, `KEY-P-0269-9a1b3f686531@1`, `THEME-P-0269-ID@1`, `THEME-P-0269-REL@1`, `THEME-P-0269-BO@1`, `THEME-P-0269-ARB@1`, `THEME-P-0269-EKO@1`, `THEME-P-0269-MIL@1`, `THEME-P-0269-SAM@1`, `THEME-P-0269-HAL@1`, `THEME-P-0269-PER@1`, `THEME-P-0269-SYN@1`, `RESEARCH-P-0269-8073a2e38d0e@1`, `RESEARCH-P-0269-dc9e05f77b98@1`, `CONTRACT-P-0269-PK-01@1`, `CONTRACT-P-0269-PK-02@1`, `CONTRACT-P-0269-PK-03@1`, `CONTRACT-P-0269-PK-04@1`, `CONTRACT-P-0269-PK-05@1`, `CONTRACT-P-0269-PK-06@1`, `CONTRACT-P-0269-PK-07@1`, `CONTRACT-P-0269-PK-09@1`, `CONTRACT-P-0269-PK-10@1`, `CONTRACT-P-0269-PK-11@1`, `CONTRACT-P-0269-PK-12@1`.

- P-0270: `RESEARCH-P-0270-9d76f0343410@1`, `KEY-P-0270-378fe3faa502@1`, `KEY-P-0270-3e3c005f2ab9@1`, `THEME-P-0270-ID@1`, `THEME-P-0270-REL@1`, `THEME-P-0270-BO@1`, `THEME-P-0270-ARB@1`, `THEME-P-0270-EKO@1`, `THEME-P-0270-MIL@1`, `THEME-P-0270-SAM@1`, `THEME-P-0270-HAL@1`, `THEME-P-0270-PER@1`, `THEME-P-0270-SYN@1`, `RESEARCH-P-0270-dc9e05f77b98@1`, `CONTRACT-P-0270-PK-01@1`, `CONTRACT-P-0270-PK-02@1`, `CONTRACT-P-0270-PK-03@1`, `CONTRACT-P-0270-PK-04@1`, `CONTRACT-P-0270-PK-05@1`, `CONTRACT-P-0270-PK-06@1`, `CONTRACT-P-0270-PK-07@1`, `CONTRACT-P-0270-PK-09@1`, `CONTRACT-P-0270-PK-10@1`, `CONTRACT-P-0270-PK-11@1`, `CONTRACT-P-0270-PK-12@1`.
