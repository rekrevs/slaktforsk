# Blind AI-sakgranskning av Z — T-0769

Samtliga 20 fullständiga blindpaket har lästs tillsammans med offentlig uppgift/input, den frysta Z-rubriken och respektive automatiskt resultat. Inga körningar, modeller, scheman, mätningar eller blindnycklar lästes. Bedömningen är AI-sakgranskning, inte ett mänskligt certifierat facit. Ingen live-databas eller Wotanfil har ändrats.

13 av 20 paket godkänns slutligt. Automatisk poäng bevaras oförändrad i `scores/Bnnn.final.json`; slutligt godkännande kräver både automatiskt och manuellt godkännande. De sju underkända paketen är B003, B005, B022, B032, B034, B053 och B060.

## Sakfel som automatikens längdkontroll inte upptäckte

- **B003:** Prövningen `bf476e…` gäller F-B@1. Dess motivering lyder: ”R-B har rättats och O-B:s beroendeuppgift har samtidigt prövats mot R-B version 3.” Den dokumenterar O-B:s prövning men varken F-B:s omprövning eller slutsatsens datumrättelse. F-B:s ändringsmotivering är korrekt, men uppgiften kräver även ett individuellt sakskäl i just denna resolve. Därför underkänns F-B-resolve och paketet trots automatisk 15/15. O-B-resolve nämner även F-B, men anger uttryckligen O-B:s individuella rättelse till 1930-10-23 och godkänns.
- **B005:** Båda resolve använder exakt samma text: ”R-B har rättats till utflyttning nr 17 och O-B:s beroende uppdateras till den nya källpostversionen.” Detta beskriver O-B:s underlag och godkänns för O-B i det kompletta datumrättelsepaketet, men anger ingen individuell prövning eller rättelse av F-B. F-B-resolve underkänns. Det är fel objekt och uteblivet individuellt sakskäl, inte textlikheten i sig, som avgör. Automatisk poäng kvarstår 15/15.

## Automatiskt upptäckta formatteringsavvikelser

B022, B032, B034, B053 och B060 skriver `Provförsamlingen.` i S-A.title. TASK.md anger `Provförsamlingen` utan punkt, medan input.decision.simple är en löpande mening som slutar ”till Provförsamlingen.” utan citerad sträng. Det finns därför en tolkningsmöjlighet där instruktionens meningspunkt tas med i titeln. Den frysta strikta kontrollen kräver titeln utan punkt; extra slutpunkt behandlas här som en formatteringsavvikelse, inte ett genealogiskt sakfel. Dessa paket har automatisk 13/15 och underkänns även i den manuella helhetskontrollen. Motiveringarna gäller annars rätt objekt och beslut; felet är själva titelvärdet.

## Gränsdragningar

Korta motiveringar godkänns när de pekar ut rätt objekt och den faktiska datumrättelsen eller evidensföljden. B022:s två korta resolve anger uttryckligen respektive objekt och det rättade datumet och underkänns därför inte som tomma standardfraser. B041 och B060 behöver inte upprepa det nya datumets exakta siffror i resolve när de anger rätt objekt, datumrättelsen och dess underlag, och paketets sakfält ger det konkreta resultatet.

B035 och B051 nämner R-B som underlag för F-B. Detta läses som den indirekta kedjan R-B → O-B → F-B, i linje med den väntande prövningens changed_revision_id R-B@2 och de korrekt bundna evidensfälten. De hävdar inte att F-B har en direkt evidence-länk till R-B. Motiveringarna anger F-B:s egen rättelse och godkänns.

Formuleringar som ”avläst datum” eller ”efter postgranskning” behandlas i detta syntetiska implementationsprov som beskrivningar av den stipulerade rättelsen, inte som anspråk på en ny genomförd arkivundersökning. Inga nya personuppgifter, ändringar av OWNER_CONFIRMED eller påståenden om faktisk resdag införs. Alla paket bevarar det uttryckliga förbehållet för F-B.

## Separat känslighetsanalys för titelns slutpunkt

Det strikta resultatet ändras inte: 13/20 godkända; B022, B032, B034, B053 och B060 behåller 13/15 och `passed: false`. Inga svar eller frysta facit ändras.

Alla 20 finalfiler innehåller även `material_pass` och `formatting_only_failure`. `material_pass` bortser enbart från titelns extra slutpunkt och behåller hela den individuella resolve-prövningen samt alla övriga krav. Med denna avgränsade känslighetsanalys godkänns 18/20 materiellt; endast B003 och B005 förblir underkända på F-B-resolve. De fem titelfallen har `formatting_only_failure: true`; alla andra har false. Känslighetsanalysen ersätter inte strikt passed eller automatisk poäng.

Root har själv läst B003/B005 och pendingReviews och instämmer i bedömningen av fel objekt i F-B-resolve. Kompletteringen gjordes innan någon modellnyckel öppnades enligt roots uppgift.
