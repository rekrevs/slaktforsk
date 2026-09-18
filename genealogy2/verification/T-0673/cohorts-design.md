# T-0673: förslag till heltäckande kohorter

`cohorts-draft.json` fördelar det låsta manifestets mängder på **91 ändliga
kohorter**, plus en föreslagen separat slutrevision. G001–G091 är lokala
fördelningsnycklar, inte Wotan-id eller status. Fördelningen är nu antagen genom `ownership.json`: T-0674–T-0764
äger kohorterna och T-0765 slutrevisionen. Wotan äger genomförande,
omprioritering och återupptagning. Filnamnet med draft bevarar den
hash som prioriteringens revisionsbevis använder.

## Granskningsenheter och stöd

- **42 postkohorter:** 34 med sakposter, en blandad, sex katalog-/metadata-
  grupper och en ägargrupp. Högst 50 native poster per kohort. Kategorin är
  en arbetsväg härledd ur posttypen, aldrig ett godkännande eller undantag
  från läsning. Varje relevant post, kolumn och slutsats prövas.
- **Sex citationskohorter:** de 270 citationer som saknar direkt postmappning,
  högst 50 per grupp. Övriga citationers hela omfång ägs av en postkohort;
  andra berörda post-/mediekohorter korsrefereras. Saknad direkt mappning
  innebär inte saknad tidigare forskning. Även negativa och historiska
  citationer ska få uttryckligt utfall.
- **13 sökkohorter:** alla 452 aktuella sökningar, högst 40 per grupp,
  uppdelade i negativt, positivt, inkonklusivt och åtkomstproblem.
  Söknollens räckvidd prövas separat från eventuell läst personrad.
- **Nio källbeskrivningskohorter:** högst 100 native källbeskrivningar per
  grupp, med deras äldre källdokument. Källidentitet, täckning, ursprung och
  beroenden prövas; detta är inte ett andra uppdrag att läsa alla bilder.
- **21 medieomfångskohorter:** högst 200 distinkta innehållshashar per grupp
  för tillgångar utan direkt aktuell postkoppling. Varje tillgång får
  proveniens-/omfångsdisposition. Relevanta ursprungsuppgifter får ett exakt
  läsomfång; tekniska JSON-filer, kartunderlag, derivat, dubbletter och
  `.gitkeep` blir inte automatiskt varsitt manuellt originaluppdrag.

Storlekarna är fasta ingångsgränser, inte tidsgarantier. En citation eller
sökning kan omfatta många sidor. Vid faktisk överstorlek krävs en uttrycklig
uppdelning med bevarad union innan arbetet växer; inget oläst delomfång får
falla bort. Pilotens exakta läsningar kan återbrukas först efter avstämning
av omfång och revision, inte enbart eftersom objektet ingår i piloten.

## Delade bilder och ansvar

Posterna bildar **1 526 komponenter** via samma bildhash eller exakt
källa/lokator. Största komponenten har 50 poster och hålls därför samman.
Varje av de **5 023 distinkta tillgångshasharna** får exakt en primär
läsansvarig. Alla filalias till samma innehåll följer samma ägare.
Andra berörda uppgifter hänvisar dit och granskar sina egna påståenden
mot exakt läsomfång. En nödvändig oberoende kontrolläsning är fortfarande
obligatorisk för svåra/avgörande fält; den är ingen andra schemaläggning av
hela primärgranskningen.

Olika beskärningar, upplösningar eller komprimeringar kan ha olika hash.
De har **inte** automatiskt identifierats som samma bild. Exakt locator
sammanför vissa sådana fall; mänsklig avstämning kan kräva dokumenterade
ansvarsjusteringar före läsning. Provens länkar från citation/källbeskrivning
är proveniens, aldrig automatiskt stöd för varje personpost.

Historiska mediekopplingar och dokumentursprung fördelas till respektive
nuvarande post-/källägare som granskningsunderlag, utan att gamla revisioner
skrivs om eller blir godkända. Ägaruppgifter behåller sin särskilda
OWNER_CONFIRMED-verkan; kataloguppgifter räknas inte som personbelägg.
Alla dessa mängder finns kvar i fördelningen.

## Prioritet och samordning

Manifestet innehåller inte den fullständiga relation–identitet–beläggsgrafen
eller uppgift om ensamt bärande stöd. **Ingen kohort är därför märkt som
bevisat viktigast genom en gissning utifrån genre.** Före start ska de
aktuella beroendena och båda släktsidorna prövas och verkligt bärande
identitets-/relationsstöd ges företräde. G-numren är inte utförandeordning.

T-0671:s täckningskandidater ska korsrefereras till de ansvariga citationerna,
sökningarna och medieomfången. T-0672:s följdverktyg stödjer rättelserna men
ersätter inte läsningen. Kända återbevarandeuppgifter måste samordnas innan
ny anskaffning; åtkomstblockerade läsenheter behåller ägare och reservation.
Dessa beroenden beslutas i Wotan, inte genom en extra statuslista här.

## Exakt täckning

Varje identitet nedan har exakt en ägare; ingen extra identitet tillkommer:

| Manifestmängd | Antal |
| --- | ---: |
| Citationer | 1 111 |
| Äldre källbeskrivningar | 805 |
| Aktuella native källposter | 1 955 |
| Aktuella native källor | 828 |
| Aktuella sökningar | 452 |
| Importerade tillgångar | 5 067 |
| Native medier | 5 |

Dessutom har samtliga 12 166 dokument–objektassociationer, 1 464
post–medieassociationer, 30 tidigare T-0110-audits och 30 dubblettgrupper
exakt en ansvarig kohort via manifestindex och radens hash. De är stöd,
inte extra manuella primärenheter. Baslinjens 53 operationer och dess hash
är låst proveniens, inte nya forskningsuppgifter.

`union_checks` redovisar mängdlikhet och unik fördelning per mängd.
`content_reading_owners` ger den enda primärägaren per bild-/filhash.
`support_association_owners` täcker varje stödrad med dess exakta index/hash.
Inga innehåll har sakgranskats av fördelningen. Ett grönt unionstest bevisar
endast att ingenting faller ur planens mängder.

## Genomförd prioritering

`priority.json` spårar 610 aktiva accepterade föräldrarelationer och1582
identitetskopplingar på baslinjen genom exakta supports/derived_from-vägar.
15kohorter har verifierade släktbeslut med en nåbar post i den explicita
grafen;285beslut saknar postväg och räknas som kopplingsluckor. Inget av
dessa mått bevisar antal verkligt oberoende källor. Alla91kohorter har
ordnats efter denna konservativa riskbedömning; båda sidor ingår i högsta
riskbandet. Tidigare avsnitts krav på graftriage är alltså genomfört.

T-0672 ligger först som avgränsad verktygsförbättring efter T-0673; sedan
följer de prioriterade originalkohorterna. T-0671 behåller sitt separata
494par-omfång och ingår i slutrevisionens beroenden. Ingen av dessa två
stöduppgifter räknas som originalläsning.
