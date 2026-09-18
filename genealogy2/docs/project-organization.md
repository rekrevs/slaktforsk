# Projektets organisation efter Genealogy2

Analys 2026-09-18, T-0668. Detta dokument beskriver nuläge och ett förslag.
Ingen fysisk omorganisation eller ändring av skrivansvar har genomförts.

## Bedömning

Problemet är främst att olika informationsroller ligger blandade och ibland
beskrivs med äldre instruktioner. Katalogen genealogy är inte överflödig:
den innehåller både arkiverade arbetsdokument, centralt källmaterial och
metodtexter vars sakkrav fortfarande gäller. Genealogy2 innehåller i sin tur
både aktuell kunskapsmodell, körbar kod och historisk migrationsdokumentation.

Rekommendationen är att först göra de aktuella rollerna och arbetsvägarna
entydiga, med oförändrade källsökvägar. En senare flytt av medier eller
namnändring kräver en särskild prövning av lagrade referenser och återställning.

## Ansvarskarta för dagens filer

| Roll | Plats | Aktuell användning och ändringsregel |
|---|---|---|
| Mål, mandat och projektbeslut | `NORTH-STAR.md`, `PROJECT-CONTROL.md`, `AGENTS.md` | Gällande styrning; ändras genom projektets beslut |
| Utförande och återupptagning | `wotan/backlog.json`, `wotan/dev-log/` | Enda aktuella uppgiftskön; äldre kopior i importbasen är historik |
| Aktuell genealogisk kunskap | `genealogy2/data/research.sqlite` | Personer, relationer, observationer, slutsatser och forskningsfrågor; skrivs genom `apply` |
| Nya skrivningar och återspelning | `genealogy2/operations/`, `genealogy2/journal/` | Operationspaket respektive accepterade ordnade kvittenser; journalen redigeras inte manuellt |
| Bevarade källbeskrivningar och avskrifter | `genealogy/sources/`, `genealogy/citations/` | 805 respektive 1 111 dokument; ursprungligt underlag, med aktuell vidareutveckling i Genealogy2 |
| Faktiska äldre originalfiler | `genealogy/media/` och två andra artefakter under genealogy | 5 065 mediefiler, cirka 6,26 GB, samt två övriga DB-refererade artefakter; används fortfarande direkt |
| Nytt originalmaterial | `genealogy2/media/objects/` | Hashadresserat innehåll från `stage-media`; noll registrerade nya medier vid analysen |
| Äldre person-/forskningsarbete | `genealogy/people/`, `research-profiles/`, `research-log/`, front och täckning | Fryst underlag och argumentationshistorik; inte aktuella skrivytor eller uppgiftsköer |
| Gällande metodkrav i äldre representation | `genealogy/person-contract.md`, `research-plan.md`, `source-strategy.md`, `method-riksarkivet.md` | Sakkrav antagna av aktuella rootinstruktioner; gamla fil-/skrivregler ersatta av native arbetsväg |
| Exakt migrationsbas | `genealogy2/import/baseline/` | 3 717 dokumentversioner och manifest med externa filer; oföränderliga byte för provenans och återuppbyggnad |
| Migrationsbeslut och verifieringsbevis | `genealogy2/migration/`, valda filer i `verification/`, Wotan T-0640–T-0663 | Spårbara engångsbeslut, generatorunderlag, riskprov och resultat; inte en andra aktuell personmodell |
| Aktiv kod | `genealogy2/cli.mjs`, `lib/`, `schema/`, `test/` | Läsning, kontrollerad skrivning, datamodell och verifiering |
| Äldre verktyg | `scripts/` | Blandning av arkivkontroller, medieinventering, gamla indikatorer och utgåve-/dashboardverktyg; måste klassificeras per funktion |
| Presentation och leveranser | `dashboard/`, `genealogy/editions/`, `output/pdf/` | Härledda eller daterade utgåvor; dashboarddata ändras bara på uttrycklig beställning |
| Lokala kör- och försöksfiler | ignorerade databaser, återställningskopior, `genealogy2/backups/`, `tmp/` | Inte Git-säkrat kunskapsunderlag; gamla dumpförsök är parkerade, inte ordinarie rutin |

Gamla citationsakter är fortfarande källdokument även när deras strukturerade
innehåll har överförts. De är samtidigt daterade: en senare rättelse hör i
Genealogy2 och får inte skrivas tillbaka som om den alltid funnits i originalet.
Att läsa en historisk akt får alltså inte övertrumfa en senare dokumenterad
rättelse i den aktuella modellen.

## Faktiska glapp och beroenden

**Fryst katalog med ännu gällande normer.** De fyra metodfilerna ovan och
genealogy/README.md ingår med `frozen: true` i importbasen; deras nuvarande
hashar matchar basen. Genealogy/README beskriver fortfarande att skapa
akter och köra gamla inventeringens `--write`. Rootens aktuella instruktioner
upphäver detta, men en läsare som börjar i den gamla filen får fel arbetsväg.
Samma blandning av sakkrav och äldre representationsregler finns i programmet.
Att lägga en ny varningsrad i de frysta originalen skulle bryta bytebevarandet.

**Sökvägar är del av provenansen.** Schema 001 använder dokument- och
artefaktsökvägar som nycklar. `extract.mjs` använder dessutom filvägen när
enhets-id:n beräknas. `verify-source` förutsätter den frysta genealogy-mängden;
backup/restore återskapar samma relativa vägar. Mediemanifest, gamla länkar,
Git LFS-regler, tester och `context` använder dem också. En flytt kräver
därför mer än att rätta några Markdownlänkar. Historisk källidentitet måste
hållas skild från eventuell framtida fysisk lagringsplats.

**Medier har två lagringsvägar.** Gamla filer finns i genealogy/media och
nya registreras under genealogy2/media/objects. Git-attributen anger LFS för
de äldre binära filtyperna men ingen motsvarande regel för de nya
hashadresserade filerna. Det finns inga registrerade nya medier ännu, så
analysen har inte funnit en befintlig osäkrad native mediemängd. Bevarande-
och LFS-regeln för nytillkommet material bör ändå definieras före nästa
sådan införsel. Befintliga mediemanifestet inventerar bara den gamla vägen;
Genealogy2:s `verify-assets` omfattar däremot båda.

**Gamla verktyg har olika giltighet.** `goal-state` och `research-inventory`
beskriver det frysta arkivet. Medieinventering och strukturkontroll har
fortfarande värde för det arkivet, men är inte fullständiga kontroller av
den nya modellen. Dashboardens dokumenterade databyggare läser fortfarande
genealogy. Nästa beställning av aktuell dashboard behöver därför hantera
datakällan, inte bara köra den gamla byggkommandokedjan. Ingen sådan
uppdatering eller anpassning görs i denna uppgift.

**Dubblering har flera olika syften.** Hashkopiorna i importbasen bevarar
exakta äldre texter. Databasens representation gör dem sökbara och knyter
dem till versionerade slutsatser. Operationspaket och journal överlappar:
med projektets kanoniska hash matchar 41 av 42 operationsfiler någon av
de 39 journalbegärandena; piloten är det separata undantaget. Vissa paket
förekommer alltså i mer än en fil. Generatorproven och migrationsmanifesten
använder dessa filer som jämförelseunderlag. Det motiverar en senare
bevarandeprövning, inte omedelbar radering eller automatisk deduplicering.

## Alternativ

| Alternativ | Nytta | Kostnad och begränsning |
|---|---|---|
| Behåll sökvägar, förtydliga roller och aktuella ingångar | Snabbare orientering, minskad risk för gamla skrivvägar, bibehållen återställning | Namnen genealogy/genealogy2 kvarstår; en ansvarskarta behövs |
| Flytta aktuella metodtexter till ett tydligt docs-område och behåll fryst arkiv | Gällande normer kan vidareutvecklas utan att ändra importbasen | Kräver uttrycklig adoption, avstämning av sakkrav och uppdaterade aktiva hänvisningar |
| Dela fysiskt i exempelvis kod, källarkiv, data och historik | Enhetligare långsiktig katalogstruktur | Kräver spårbar sökvägsmappning, ändrad mediehantering, LFS, verktyg och återställningsprov; störst ingrepp |

De två första kan kombineras. Det tredje ger inte i sig bättre uppslagningar
eller säkrare kunskap och bör ha ett konkret användningsskäl innan det görs.

## Konkret rekommenderat första införande

Detta är ett förslag för ett senare genomförandebeslut:

1. Låt rootens README vara den korta ingången med vägar till aktuell
   forskning, källarkiv, metoder, återställning och Wotan. Behåll denna
   ansvarskarta som förklarande stöd; skapa ingen parallell uppgiftslista.
2. Adoptera de fyra gällande metodområdena till exempelvis
   `docs/research/person-contract.md`, `research-program.md`,
   `source-strategy.md` och `riksarkivet-access.md`. Bevara sakkrav och
   ägarbeslut, översätt enbart de pensionerade skriv-/filinstruktionerna,
   dokumentera ursprungsfil/hash och låt aktiva instruktioner peka dit.
   De frysta originalen ligger kvar oförändrade. Endast den adopterade
   versionen blir plats för framtida metodändringar efter beslutad övergång.
3. Beskriv de äldre skripten som arkiv-/utgåveverktyg och de nya som
   verktyg för aktuell forskning. Lägg aktiva hänvisningar utanför det
   frysta arkivet; ändra inte gamla forskningsloggar eller deras instruktioner.
4. Komplettera bevaranderegeln för nya native medier på deras befintliga
   plats och pröva Git/LFS-checkout med ett litet syntetiskt medium.
   Flytta inte de äldre 6,26 GB medierna för att få en enhetlig katalogbild.
5. Avsluta med länk-/rollkontroll, oförändrade frysta hashar och ett
   avgränsat återställningsprov. Ändra inte dashboardens data som bieffekt.

Genealogy2 behåller sitt namn tills en namnändring löser ett konkret problem.
Fysisk konsolidering, borttagning av dubblettpaket, gallring av verifieringsbevis
och dashboardbyte får egna avgränsningar om de senare beställs. Resticfrågan
påverkas inte och är fortsatt parkerad.

## Belägg och kontrollens gränser

Inventeringen avsåg Git-spårade filer på main efter `7426c674`; storlekar
avser materialiserade lokala byte, inte Git-packets komprimerade storlek.
Databasen öppnades enbart läsande för filreferenser och antalet native medier.
Ingen full referensgraf över alla historiska Markdownlänkar har byggts.

Kontrollerade ingångar: [rootinstruktioner](../../AGENTS.md),
[aktuellt arbetsflöde](working.md), [återuppbyggnad](reconstruction.md),
[äldre struktur](../../genealogy/README.md),
[dashboardens arbetsväg](../../dashboard/README.md),
[mediebevarande](../../MEDIA-PRESERVATION.md),
[import och fryst mängd](../lib/archive.mjs),
[enhets-id:n](../lib/extract.mjs), [ursprungsschema](../schema/001.sql),
[medier och restore](../lib/recovery.mjs),
[kontextklassificering](../lib/context.mjs),
[äldre medieinventering](../../scripts/media-manifest.mjs),
[dashboardbygge](../../scripts/build-dashboard-data.mjs) och
[Git-attribut](../../.gitattributes).
