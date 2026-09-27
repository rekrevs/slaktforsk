# Blind sakgranskning X, T-0772

Detta är AI-granskning, inte mänskligt certifierat facit. Ingen modellidentitet har undersökts. Inget nätverk eller några subagenter har använts. Inga forskningsdata, körningsloggar eller git-historik har lästs.

## Lästa underlag

- `evaluations/T-0769/x/public/TASK.md`.
- De fem bilderna `A-full.jpg`, `A-detail.jpg`, `B-full.jpg`, `B-left-detail.jpg` och `B-right-detail.jpg` i samma public-katalog, samtliga öppnade med bildverktyg.
- `evaluations/T-0769/x/private/rubric.json`.
- `evaluations/T-0772/judge/STANDARD-X.md`.
- Samtliga 14 svar i `evaluations/T-0772/blind/x/` och motsvarande `evaluations/T-0772/scores/Cnnn.auto.json`, med ID enligt tabellen nedan. Förkontrollerna användes som avvikelselistor, inte facit.

Endast kataloglistning gjordes för att finna bild- och svarsnamnen; inga andra uppgifters svar eller förkontrollers innehåll lästes. Ett försök att skapa extra förstoringar av två B-celler avbröts eftersom Pillow saknades. Bedömningen bygger på de fem direkt öppnade bilderna, inklusive de befintliga detaljbilderna.

## Visuell prövning och poängprinciper

Alla 25 efterfrågade celler har jämförts med varje svar i sin helhet. A:s namn, yrkesförkortning och datum stöds av bilden. De fyra efterfrågade tomma A-cellerna saknar ditto; vaccinmarkeringarna tillhör en annan kolumn. Giftcellen i r2 har 3 över 5 och r3:s giftcell är tom. B:s namn och datum har prövats inklusive s./d. och korsets slut framför Gerda.

B r8:s andranamn har svåra streck vid diagonalkrysset. Nikolaus och Nickolaus godtas; C016:s specifika c/k-reservation är rimlig. Michaelson i C004 stöds inte. B r8:s två blyertstal kan läsas 12,14 eller 13,14; båda får full innehållspoäng. C016 och C021 reserverar konkret den sista siffran och får även statuspoäng.

B r9:s dagtal visar en 3-liknande form följd av ett smalt stigande streck; 31/3 föredras. 5/3 är endast godtagbart som uttryckligt reserverad läsning enligt standarden. C003 beskriver ett extra dragstreck men fastslår 5; C006 beskriver en 4-liknande flagga men anger ändå 5/3 som read utan att reservera den valda dagsläsningen. C017 och C019 beskriver bråkets lutning/punkt, inte osäkerhet i dagen. Dessa noter uppfyller inte reservationskravet. Övriga säkra 5/3-svar saknar sådan reservation helt. Innehåll 0, status 0 och kritiskt fel tillämpas på dessa svar. Detta är en bedömning av avskriftens säkerhetsanspråk, inget påstående om personens verkliga födelsedatum.

Radlinjerna i B-right-detail och fullbilden placerar 16 i r10 och r11, medan r9 och r12 är tomma. Infört 16 i r9 är kritiskt radfel i C004 och C013. I C011, C014, C026, C029 och C038 återges talen däremot i rätt råfält. Deras osäkerhet gäller om en notering kan vara avsedd för föregående rad trots dess tydliga placering i det egna radbandet. Uppgiften gäller den egna cellen; denna avsiktsreservation motiverar inte uncertain och ger statusavdrag, men inget innehållsavdrag eller kritiskt radfel. Det skiljs från verklig glyfosäkerhet i svag blyerts.

C006:s Charlotta/Charlatta-reservation är konkret och bildmässigt rimlig: vokalen efter l är öppen och nära diagonalen. Rätt huvudläsning med denna osäkerhet får full poäng. B r12:s 17/9 stöds av dagtalets 1 och 7 samt månadens ögla och nedstapel.

Content 2 ges för rätt diplomatisk läsning, 1 för liten diplomatisk förlust och 0 för fel eller utelämnad cell. C004:s d. för s. i två annars rätt lästa namn får 1. Read behåller normalt statuspoäng i textbärande cell även vid fel namn; undantaget för oreserverat 5/3 följer standarden. Blank i textcell eller read i tom cell ger 0 statuspoäng. Interpunktion och mellanrum normaliseras. Överstrykningar räknas separat utan poängavdrag. Inga ytterligare globala kritiska fel är belagda i svaren; frånvaro av otillåtna arbetsåtgärder kan inte verifieras ur enbart svarsobjekten.

## Resultat

| Cnnn | poäng/75 | godkänd | överstrykningar/5 |
|---|---:|:---:|---:|
| C003 | 72/75 | nej | 5/5 |
| C004 | 59/75 | nej | 0/5 |
| C006 | 72/75 | nej | 5/5 |
| C011 | 69/75 | nej | 5/5 |
| C013 | 66/75 | nej | 5/5 |
| C014 | 69/75 | nej | 5/5 |
| C016 | 75/75 | ja | 5/5 |
| C017 | 72/75 | nej | 5/5 |
| C019 | 72/75 | nej | 5/5 |
| C020 | 72/75 | nej | 5/5 |
| C021 | 75/75 | ja | 5/5 |
| C026 | 69/75 | nej | 5/5 |
| C029 | 69/75 | nej | 5/5 |
| C038 | 70/75 | nej | 5/5 |

Varje finalfil innehåller en konkret motivering för samtliga 25 fält. Godkänt kräver minst 68 poäng och inga bekräftade kritiska fel.

Programmatisk slutkontroll godkänd: exakt alla 14 svars-ID, giltig JSON i samtliga finalfiler, exakt de 25 unika cell-ID:na per svar (350 fältposter totalt), tillåtna poängvärden, korrekta summor och konsekvent pass-regel. Överstrykningsantal och samtliga 14 tabellrader stämmer med finalfilerna.
