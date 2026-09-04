# Släktforskning

Detta är ett källstyrt släktforskningsprojekt. Wotan håller reda på arbetet;
forskningsresultaten ligger under `genealogy/`.

Varje agent läser först projektets [AGENTS.md](AGENTS.md), som routar vidare
till de kanoniska styrdokumenten. En ny arbetssession fortsätter sedan med
[HANDOVER.md](HANDOVER.md), som är en kort lägessida, och kör
`node scripts/goal-state.mjs` för läget mot målet.

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

Repository and source-artifact preservation are documented in
[`MEDIA-PRESERVATION.md`](MEDIA-PRESERVATION.md). The private GitHub repository
uses Git LFS for retained source media and keeps an exact, generated SHA-256
inventory in `genealogy/media-manifest.json`.

## Dashboard

Den lokala, skrivskyddade [forskningsdashboarden](dashboard/README.md) visar
progress, släktträd, personberättelser och senaste fynd direkt från projektets
befintliga filer.
