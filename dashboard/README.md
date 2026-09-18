# Släktforskningsdashboard

Dashboarden är en skrivskyddad, mänskligt orienterad vy över projektets
personakter, relationer, forskningslogg och Wotan-status vid senaste beställda
uppdateringen. Den har ingen egen faktadatabas och är ingen källa till aktuellt
utförandestatus; det finns i Wotan och de kanoniska projektfilerna.

Dashboarden, inklusive dess data, uppdateras **bara när ägaren uttryckligen ber
om det** (PCD-2026-09-05-014). Forskning, tester, utvecklingsserver, byggen,
sessionsbevarande och commit/push använder den sparade ögonblicksbilden.

```bash
npm install
npm run dev
```

Verifiera den sparade ögonblicksbilden utan att uppdatera den:

```bash
npm test
npm run build
```

## Nästa uttryckligen beställda uppdatering

Nuvarande databygge läser den frysta genealogy-modellen. Det kan därför inte
återge Genealogy2:s aktuella forskningsläge. Innan en beställd uppdatering
av aktuell forskning levereras måste byggaren anpassas och verifieras mot
Genealogy2:s läsvyer, med korrekta separata granskningsnivåer. Avgränsa det
arbetet i Wotan då; denna instruktion startar ingen uppdatering.

Följande kommandon hör till den äldre byggaren och är endast relevanta om
beställningen uttryckligen gäller att återskapa en historisk genealogy-vy:

```bash
npm run data
npm run test:current
```

Det första äldre kommandot bygger om `public/data/project.json` från `genealogy/`
och `wotan/backlog.json`. Det andra jämför ögonblicksbilden med den
äldre byggarens indata,
utan att skriva något. Vanliga tester kräver bara intern konsistens och tillåter
att projektet har gått vidare. Ett fristående bygge använder versionssparad data.
