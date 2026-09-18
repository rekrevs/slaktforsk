# T-0672: läsande rättelsepåverkan

Leveransen är `node genealogy2/cli.mjs impact <objekt/C-id> [--query fras]`.
Den visar exakta versionskedjor, importerad proveniens och möjliga textkopior
som skilda lager. Historiska revisioner hålls isär från aktuella. Ingen
matchning tillför stöd, ändrar personidentitet eller avgör ett granskningsbeslut.
Arbetsvägen finns i `../../docs/working.md`, avsnittet Hitta följder av en rättelse.

## Verifiering mot verkligt material

`cases.json` låser de sju T-0110-fallen och kända direkta följdobjekt som en
separat läsande granskare identifierade innan resultatet kontrollerades.
`node genealogy2/verification/T-0672/check.mjs` kör dem mot skrivskyddad
huvuddatabas. Valfri första parameter är en annan redan befintlig DB-fil.
Testet ska vid framtida sakrevisioner prövas mot sina dokumenterade gamla
förväntningar, inte skriva tillbaka äldre versionsnummer.

`results.json` bevarar den faktiskt körda regressionen vid 59 operationer:
alla sju fall passerar, inklusive deras kända direkta följdobjekt.
Körningarna tog ungefär 2,2–2,4 sekunder per fall på aktuell datamängd.
Det mäter maskinell framtagning, inte individuell sakgranskning.

| Kontroll | Verifierat utfall |
|---|---|
| C-0721, S-0556@2 | Textkopian av rådatumet hittas utan att importursprung eller ordmatchning blir ett registrerat belägg. |
| S-0556@2.description | Aktuell rättelse och bevarad återtagen formulering finns i samma fält; träffen förblir kandidat tills fältet lästs. |
| E-birth-P-0477@1 | Gammalt kopierat datum visas bland historiska revisioner, inte som aktuell uppgift att skriva om. |
| BIO-P-0363@1 | Den orelaterade Maja Lena Jonsdotter hittas på frasen Lena Jonsdotter men får ingen identitets-/stödrelation. |
| BIO-P-0477@2 | Verkligt versionsstöd till O-P-0477-C0721-Walla@2 syns, även när en annan lika kort väg valts för path. |
| C-0048, E-birth-P-0048@1 | Den aktuella slutsatsens verkliga bindning till postens äldre @1 består trots att posten nu är @2. |

De granskade sakrättelserna var redan införda i T-0110/T-0115. Detta är ett
prov av upptäckt och klassificering, ingen ny bildläsning eller generell
sakcertifiering. Alla namn-/datumträffar är inte fel och deras antal ska inte
användas som felstatistik. Saknade semantiska länkar och andra stavningar
kan fortfarande undgå sökningen. Begär relevanta explicita sökfraser.

## Kodkontroller och bevarande

Fem nya positiva/negativa testfall prövar äldre transitiva kedjor,
frikopplade aktuella revisioner, ursprung/mål utan stöd, kopior, historik,
namnar, bokstavlig sökning, filnamnsreferenser och okända indata samt
oförändrad full export och väntande granskningar efter library/CLI-anrop.
20 riktade regressioner passerar (inklusive fem nya), liksom en separat
slutkörning av de fem efter sista resultatfältet införts.67 äldre tester
passerar. CLI verify, verify-source och verify-assets passerar.
Se `verification.json`, `focused-tests.log` och `impact-tests.log`.

Den oberoende kodgranskningen fann att C-id följt av ett filnamnsbindestreck
kunde missas. Det rättades och fick en regression utan separat C-id-länktext;
C-0001 matchar fortfarande inte C-00010. Det första verkliga provet antog
felaktigt en viss kortaste väg där flera vägar fanns. Vyn visar nu också
samtliga omedelbara länkar från den nådda grafen, med roller bevarade.

Huvuddatabasens och den befintliga journalens samtliga filhashar är identiska
före/efter de verkliga sökningarna. Ingen operation eller sakrevision infördes.
Schema, apply/resolve och gammal återspelningssemantik är oförändrade.
Fryst genealogy, dashboard och den orelaterade anträdstextfilen är orörda.

Wotan T-0672 äger avslutet. Rapporternas review.items är granskningsunderlag,
inte en utförandekö. Fortsatt originalrevision börjar enligt backlogordning
med T-0674; dess tidigare låsta mängd och pilotreservationer gäller fortsatt.
