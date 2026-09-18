# Importens täckning

Slutavstämningen 2026-09-17 finns i [T-0663:s rapport](../verification/T-0663-report.md)
och [T-0643:s skiftesverifiering](../verification/T-0643-report.md). Alla
97 854 importenheter har ett uttryckligt utfall. Det inkluderar synlig
text, historik och olösta tolkningsfrågor; inte allt är fullständigt
semantiskt typat. Kör `coverage` för aktuell, härledd redovisning.

## Bevarad pilotavstämning

Avstämt 2026-09-16 i T-0642. Bas:
`a97081f666ca46e2b692ebdb2fcb98cf0a57d5412e1a35007af8fb18046a04c0`.

| Bevarande | Antal |
|---|---:|
| Exakta dokument i importbas och databas | 3 717 |
| Externa, hashkontrollerade artefakter | 5 067 |
| Personakter / profiler | 538 / 538 |
| Källakter / citationer | 805 / 1 111 |
| Aktuella A-rader | 5 130 |
| Typade objekt i pilotens kunskapsmodell | 138 |

Alla 8 784 filer i manifestet är redovisade. Media omfattar 5 064 filer
enligt det gamla mediamanifestet; andra externa artefakter och mediekatalogens
README gör att importens kategorier inte har identiska antal.

Den fullständiga rapporten anger ett utfall, en orsak och en omfångsgrupp
för var och en av 84 182 utvunna textenheter. Enheterna innehåller både
hela avsnitt och deras tabellrader; de överlappar och är inte antal fakta.
Ingen fullbordandeprocent räknas från dem.

| Textenheternas utfall | Antal |
|---|---:|
| Fullständigt mappade representationsenheter | 64 |
| Delvis mappade | 41 |
| Bevarad historik | 737 |
| Bevarat styr-/kod-/genomförandesammanhang | 6 021 |
| Bevarade, återstående betydelsetolkning | 77 319 |

De 64 fullständiga mappningarna avser pilotens frågeavsnitt, biografier
och profilhuvuden. Det betyder att deras innehåll är överfört till sin
representation, inte att forskningens slutsatser har nygodkänts. Sakliga
pilotmappningar är märkta partiella där ursprungsraden eller avsnittet
innehåller mer än det aktuella målobjektet.

[cohorts.json](cohorts.json) namnger varje omfångsgrupp med de exakta P-,
C- och S-id:n och dokument som hör dit. Grupperna äger ingen körstatus;
den finns enbart i Wotan. Fortsättningen omfattar:

- T-0644: skrivflöden, nya media, sökning och drift/återställning.
- T-0645: fullständigt person-/källregister och prövning av 27 avvecklingar.
- T-0646–T-0651: sex grupper med källposter, avskrifter och evidensgränser.
- T-0652–T-0662: elva personkohorter om högst 50 befintliga P-id:n.
- T-0663: forskningssammanhang och motiverad hantering av kvarvarande text.
- T-0643: slutlig avstämning och skifte, beroende av leveranserna ovan.

Samma källpost och relation ska återanvändas över gruppgränserna. En
osäker uppgift får fortsätta vara osäker. Ingen ny arkivforskning krävs
bara därför att representationen ändras. Arbetets omfattning ska prövas
mot utfallet i de första konverteringsgrupperna; ingen tid eller automatisk
mappningsandel är utlovad.

Den fulla rapporten är härledd och ignoreras i git. Återskapa den till
ett nytt filnamn med:

```sh
node genealogy2/cli.mjs coverage /tmp/genealogy2-coverage.json
```

Pilotrapportens hash:
`80504d572d9b7f192a92efd4c2f6506313052c7db6350be8c55c704a0e2e6803`.
Efter ytterligare databasändringar får den aktuella rapporten en annan
hash; detta dokument bevarar pilotens avstämning.
