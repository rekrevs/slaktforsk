# T-0110: originalgranskning av ett låst stickprov

Urvalet låstes före bildläsningen: 30 citationer dragna utan återläggning ur
456 ramträffar, med bevarad seed, ramhash och deterministisk dragning i
[plan.md](plan.md), [frame.json](frame.json) och [sample.json](sample.json).
Ramen bygger på aktuella bärande slutsatser och uttryckliga beläggskopplingar;
den kan missa oregistrerade sakberoenden och innehåller viss övertäckning.
Ingen citation har ersatts efter att åtkomst eller innehåll blev känt.

## Mätresultat

| Utfall | Antal |
|---|---:|
| Bekräftade inom redovisat läsomfång | 18 |
| Minst ett aktuellt sakfel, rättat | 7 |
| Ej fullt prövbara | 2 |
| Utanför avsedd population: ägaruppgifter/åtkomstmetadata | 3 |
| Totalt dragna | 30 |

**7/25 = 28 procent** av de bedömbara citationerna innehöll minst ett fel.
Tvåsidigt **95-procentigt Wilsonintervall: 14,28–47,58 procent**, med binomial
approximation utan ändlighetskorrektion. Varje citation räknas en gång,
oberoende av antalet fel eller rättade objekt. Metod:
[NIST, Wilsonintervallet](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).

Bland samtliga 27 kvalificerade dragna citationer är den möjliga felandelen
**7/27–9/27 = 25,9–33,3 procent**, beroende på de två oklassificerade fallen.
Detta är en bortfallsgräns, inte ett konfidensintervall. C-0127:s högra
bildhalva saknas och känd originalväg gav HTTP403. C-0352:s uppgift om
barnets födelsesocken kan inte avgöras mot den bevarade bildens tomma fält;
indexråsvaret är inte bevarat. Ingendera räknas som bekräftad.
C-0047/C-0086 är ägaruppgifter och C-0671 åtkomstmetadata; de ligger kvar i
redovisningen som ramövertäckning utan att räknas som fel.

Intervallet gäller det villkorliga måttet bland bedömbara enheter i denna
ram. Det täcker inte systematiska ramfel eller selektivt bortfall och är
**inte hela projektets felfrekvens eller ett godkännande av north star**.
Ett fastställt fel räknas även om någon annan detalj i citationen fortfarande
är reserverad. Bekräftad betyder att den redovisade återgivningen prövats,
inte att personens identitet, livsbild eller alla sökvägar är färdiga.

## De sju rättade citationerna

| Citation | Sakligt resultat |
|---|---|
| C-0721 | Lenas hushållsdatum är 1785 31/10, inte 1783 21/10. Johannas hushållsmånad reserveras mot egna födelsebokens 30 maj. Kandidaten Helena är fortsatt LEAD; datumlikhet skapar ingen identitetsbrygga. Moderns råålder 34 bevaras separat. |
| C-0457 | Anna Stinas dag är 4 december och Jonas Alfreds 12 november i denna hushållsbok. Felaktiga konflikter från just denna läsning tas bort; andra böckers rådatum skrivs inte om utan läsning. |
| C-0925 | Ture 17 september 1912, Villy 19 januari 1922 och Ingrid 11 december 1921. Villys andra rapporterade dag 17 kvarstår som alternativ. En felläsning av Ingrid blir inte en verklig källkonflikt. |
| C-0048 | Dahlbergvittnena hör till Maria Magdalenas post 79, inte Anders Alfreds post 78. Fel deltaganden avvisas och rätt post/dop kopplas till vittnena. Anders Alfreds födelse 24 juli, dop 25 juli och föräldrar består. Jomarkjämförelsen avser post 84, inte 83. |
| C-0510 | Lisa Cajsa 8 mars 1858. Lars Petters giftcell 58/59[?] 26/3 hålls skild från lysning 21 februari i C-0511. Nils rådatum 02[?] 7/6[?] medger inte säkert 19 juli 1802. Härledda exakta intervall dras tillbaka. |
| C-0277 | Adela 4 augusti i hushållsrad mot egen födelsebok 3 augusti; båda källuppgifterna hålls isär. Edlas utflyttning 10 oktober 1861, inte 19. Frans född 1862 med reserverad dag/månad, inte säker dag 6. |
| C-0235 | LIBRIS har exakta sekundära datum 19020409 och 19910918 och anger Sveriges dödbok samt en bok från 2017 som underlag. Påståendet om saknade datum/oberoende rättas. Äldre bibliografiska länkar som inte återfinns i authoritysvaret är inte nyverifierade. |

Felen visar särskild utsatthet hos små dag-/månadsfält, radkopplingar,
kopierade familjesammanfattningar och påståenden om källors oberoende.
Urvalet är för litet för separata, tillförlitliga felandelar per feltyp.

## Bevarande och rättelseväg

Alla 30 utfall och full relevant utvinning finns som
`AUDIT-T0110-C-NNNN` i databasen, med versionsbundna underlag. Där redovisas
även tryckta kolumner, tomma fält och osäker läsning. Operationspaketen i
`genealogy2/operations/T-0110-*.json` och journalen bevarar rättelserna.
Tidigare revisioner och det frysta genealogyarkivet ändras inte.

C-0954:s Ingridrad på sida 166 och kvartersrubrik på 162 med kontinuitet 163–165
bekräftar den redan kända familjen. Fyra nya originalbilder och LIBRIS rå-JSON
är registrerade med provenans och innehållshash. Äldre avskrifters
historiska omfång hålls skilt från den nya fulla utvinningen.

Individuella omprövningar omfattar både utlösta dependency-begäranden och
innehållssökning efter kopierade uppgifter. Den senare behövs eftersom vissa
migrerade fakta, frågor och berättelser saknar explicita sakberoenden.
Fria textträffar behandlas inte automatiskt som stöd. T-0115 tar vidare
kontrollmekanismen och dispositionen av återstående forskningsluckor.

[results.json](results.json) är den maskinläsbara resultatlistan.
[check.py](check.py) kontrollerar fryst dragning, mediehashar, utfall,
utvalda rättelser och skyddade identitets-/ägaruppgifter. Slutlig verifiering
och faktiskt applicerade operationer dokumenteras i Wotans T-0110-logg.
