# North star

## Deklarativt mål

Projektets mål är att skapa och underhålla en så fullständig, balanserad och
källförankrad släkthistoria som det bevarade och lagligen åtkomliga
arkivmaterialet på internet medger för Adam Jan Gunnar och Axel Ivar Malte,
på både Sverker Adam Jansons och Kristina Elisabeth Petronella Hööks sida.

Samtliga direkta anlinjer ska föras bakåt generation för generation,
breddförst och balanserat mellan föräldrarnas släkter, till varje linjes
dokumenterade arkivfront. Arkivfronten är den tidigaste generation där
föräldrarelationen antingen kan beläggas eller där källornas bevarande,
digitalisering, åtkomst eller innehåll sätter en exakt redovisad gräns. Målet
har inget fast maximalt antal generationer. Generationerna räknas från Adam
och Axel; projektets gemensamma djup är den djupaste generation vars då
nåbara kohort har behandlats i sin helhet, medan varje grens individuella
arkivfront redovisas separat.

För varje identifierad person ska arkivet innehålla en så rik och
sammanhängande livsbild som källorna medger. Den omfattar, när det är sakligt
relevant, identitet och namnformer, ursprung och relationer, födelse och död,
boställen och flyttningar, äktenskap och barn, arbete och samhällsställning,
egendom och ekonomi, militär-, sjömans-, rättslig, social och annan erfarenhet
samt bevarade bilder, texter, underskrifter, vittnen och sociala nätverk.

## Tolkning och kvalitetskrav

Fullständighet betyder att en seriös och källkritisk ansträngning har gjorts i
de källfamiljer som är tillämpliga på personens liv. Det betyder inte att alla
personer ska ha lika många uppgifter eller källor, att varje obetydligt
omnämnande måste återfinnas eller att frånvaro får göras till fakta.

Varje relation och biografisk uppgift ska kunna spåras till exakt källa,
källställe och evidensbedömning. Relevanta originalbilder, avskrifter,
konflikter, nollresultat och kontrollsummor ska bevaras reproducerbart. En gren
får kallas online-utredd först när de relevanta källtyperna, katalogerna och
identifierade nätleverantörerna har prövats — inte bara när den första
arkivtjänsten tar slut.

Projektet ska bevara en oföränderlig, append-only evidenshistorik. Varje
observation lagras med exakt provenans och får inte skrivas över eller raderas
av senare tolkningar. Rättelser, omläsningar och motsägande belägg tillförs som
nya, länkade poster så att forskningshistoriken förblir reproducerbar och
granskningsbar. Ovanpå denna historik underhålls en konsoliderad och reviderbar
kunskapsbild som skiljer källornas observationer från projektets slutsatser.

Varje personakt ska representera en och samma verkliga person. Uppgifter från
olika källor får sammanföras först när identiteten bärs av uttrycklig evidens
och en rimligt sammanhängande kronologi, geografi, familjestruktur och
livshistoria. Namnlikhet, ungefärlig ålder eller gemensam socken räcker inte.
När identiteten inte kan avgöras ska kandidater och alternativa tolkningar
hållas åtskilda och osäkerheten redovisas.

Ingen direkt anlinje får föras vidare som etablerad genom en personidentitet
eller föräldrarelation som fortfarande är materiellt osäker. Kandidater får
undersökas, men deras vidare anor ska förbli hypotetiska tills den bärande
identiteten och relationen är tillräckligt belagda. Om senare evidens försvagar
en tidigare identifikation eller relation ska alla beroende personer,
relationer och slutsatser identifieras och återprövas, medan den underliggande
evidenshistoriken lämnas intakt.

När projektägaren uttryckligen anger att en familjeuppgift är säker ska den
godtas som sann projektinformation, märkas `OWNER_CONFIRMED` och bevaras som ett
Project Control Decision. Avsaknad av arkivhandling får inte i sig nedgradera
sådan kunskap. Senare motstridigt material ska bevaras och lyftas till ägaren
för nytt beslut, inte tyst skriva över eller ogiltigförklara uppgiften.

Varje arkivfront ska skilja mellan förstört eller saknat material,
odigitaliserat material, åtkomsthinder, uttömda relevanta källor och olöst
identitet samt ange vad som krävs för att grenen ska kunna återupptas. Arkivet
ska därför aldrig betraktas som slutgiltigt avslutat, utan som en verifierad
forskningsfront som kan flyttas när nya källor digitaliseras eller blir
åtkomliga.

Alla namngivna släktingar och relationsbärande personer i relevanta poster och
hushåll ska bevaras opportunistiskt när de bidrar till identifikation,
sammanhang eller en sannare livsbild. Sidogrenar får inte tränga undan den
balanserade framdriften i de direkta anlinjerna, och orelaterade personer på
samma sida ska inte dras in. Uppgifter om levande personer minimeras.

Ackumulation av observationer är inte i sig framsteg. En person eller position
får betraktas som behandlad först när identiteten och de bärande relationerna
har prövats, relevanta observationer har konsoliderats till en sammanhängande
personbild och materiella motsägelser eller osäkerheter har lösts eller tydligt
dokumenterats. En exakt klassificerad arkivfront kan avsluta en position men
får inte göras till en påhittad person eller relation.

## Mått

Läget mot målet beräknas, inte berättas. Generationerna räknas från Adam
och Axel: djup 1 är föräldrarna Sverker och Kristina, och djup d har 2^d
anpositioner. `node scripts/goal-state.mjs` räknar läget ur personakterna,
slutstatusarna och källtäckningsmatrisen och skriver ut det gemensamma
djupet, balansen mellan sidorna och nästa skiva. Måttet har fem delar per
anposition:

- **Person.** Positionen är känd när en personakt bär den genom en
  propagerande föräldrarelation. En relation märkt `LEAD`, `CONFLICT`,
  `REJECTED` eller `UNKNOWN` bär ingen position. En position är stängd när
  närmaste kända ana är en anspets med giltig arkivfront. Övriga positioner
  är öppna.
- **Konsolidering.** Varje personakt anger i avsnittet `## Arbetsläge` om
  akten är `GRANSKAD`, med datum och hänvisning till granskningen, eller
  `EJ GRANSKAD`. Saknat avsnitt betyder `EJ GRANSKAD`. Granskad betyder att
  identitets- och konsolideringspasset i forskningsprogrammet har gjorts
  och att akten bedöms avse en enda verklig person.
- **Arkivfront.** Varje anspets utan kända föräldrar bär i `## Slutstatus`
  exakt en av `VERIFIERAD`, `IDENTITET OLÖST`, `ÅTKOMSTSPÄRR`,
  `EJ DIGITALISERAD`, `ARKIVLUCKA` eller `KÄLLOR SLUT`, med förväntad
  källa, genomsökt omfång, bevarad negativ kontroll och återaktiveringsvillkor.
  En anspets utan giltig slutstatus är osökt, inte stängd.
- **Källbredd.** Personens rad i källtäckningsmatrisen. Positionen är
  källbredd-klar när ingen relevant källfamilj längre står som oprövad
  högprioriterad (`1`); varje övrig cell är använd, negativt avgränsad,
  åtkomstspärrad, villkorlig eller sakligt irrelevant.
- **Sida.** Om positionen nås genom Sverker eller Kristina, så att
  balansen mellan föräldrarnas släkter kan mätas.

En generation är **behandlad** när varje känd person i den är granskad och
källbredd-klar och varje anspets på samma eller närmare djup bär en giltig
arkivfront. Projektets **gemensamma djup** är det största d där varje
generation till och med d är behandlad. Varje grens **individuella
arkivfront** är dess anspets med giltig slutstatus. Antalet personer, källor
eller observationer ingår inte i måttet.

## Styrregel

Nästa skiva är alltid det arbete som gör den närmaste obehandlade
generationen behandlad, fördelat så att ingen sida ligger mer än en skiva
före den andra. Inom generationen prioriteras i ordning: anspetsar utan
giltig arkivfront, personer som inte är granskade, personer som inte är
källbredd-klara. Det har företräde framför att driva enstaka grenar längre
bakåt eller samla mer material om redan väl dokumenterade personer.

Wotan-uppgifter skärs ur måttets nästa skiva enligt konventionen i
`wotan/README.md` och avslutas när skivans mått har ändrats som utlovat.
North star auktoriserar inte arbete utanför en sådan aktiv och godkänd
uppgift; ägarbeslut, metodundantag och utgåvegrindar hör till Project
Control respektive styrdokumenten.
