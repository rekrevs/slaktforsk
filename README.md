# Släktforskning

Detta är ett källstyrt släktforskningsprojekt. Wotan håller reda på arbetet;
forskningsresultaten ligger under `genealogy/`.

Varje agent läser först projektets [AGENTS.md](AGENTS.md), som routar vidare
till de kanoniska styrdokumenten. Före uppgiftsval och återupptagning ska
[wotan/README.md](wotan/README.md) läsas. Läs sedan
[backloggen](wotan/backlog.json) och den valda uppgiftens dev-log: pågående
arbete återupptas från sitt sparade delresultat, inte från början.
`node scripts/goal-state.mjs` visar registrerat framsteg, medan north stars
sakliga krav avgör måluppfyllelse. Ingen separat handover-fil används.

## Grundregel

En uppgift om en person blir inte ett fastställt faktum därför att den står i
ett släktträd. Varje påstående får en evidensstatus och en hänvisning till den
källa eller uppgiftslämnare som faktiskt stöder det.

Se projektets [north star](NORTH-STAR.md) för den långsiktiga riktningen,
[forskningsprogrammet](genealogy/research-plan.md) för generationsmetod och
[forskningsfronten](genealogy/frontier.md) för öppna
anlinjer, [källtäckningsmatrisen](genealogy/source-coverage.md) för prövade och
prioriterade källfamiljer och [genealogy/README.md](genealogy/README.md) för struktur,
källmodell och citeringsregler samt
[genealogy/method-riksarkivet.md](genealogy/method-riksarkivet.md) för
Riksarkivets åtkomstordning och hur källbilderna hämtas reproducerbart.
Det långsiktiga ägarbeslutet finns i
[PROJECT-CONTROL.md](PROJECT-CONTROL.md); all körbar forskning ligger i Wotan
enligt konventionen i [wotan/README.md](wotan/README.md).

Den bindande ansatsen är **balanserad anutvidgning och fullständiga
livsbilder i återkommande genomgångar**. [Personkontraktet](genealogy/person-contract.md)
anger tolv verifierbara resultatkrav för alla slags personakter;
[källstrategin](genealogy/source-strategy.md) beskriver fyrtio källklasser
och hur tidiga fynd öppnar fortsatt sökning. Personernas forskningsprofiler
bevarar frågor, teman, söknycklar och källvägar; utförandet ligger i Wotan.
`node scripts/research-inventory.mjs` inventerar samtliga P-id:n och visar
vad som ännu inte prövats enligt kontraktet. Äldre KLAR är inget nytt godkännande.

Repository and source-artifact preservation are documented in
[`MEDIA-PRESERVATION.md`](MEDIA-PRESERVATION.md). The public GitHub repository
uses Git LFS for retained source media and keeps an exact, generated SHA-256
inventory in `genealogy/media-manifest.json`.

## Dashboard

Den lokala, skrivskyddade [forskningsdashboarden](dashboard/README.md) visar
progress, släktträd, personberättelser och fynd från en sparad ögonblicksbild av
projektets filer. Dashboarden uppdateras endast när ägaren uttryckligen ber om
det. Forskning, tester, byggen och commit/push uppdaterar den inte; aktuellt
projekttillstånd läses ur de kanoniska filerna och Wotan.
