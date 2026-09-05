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

Efter en uttrycklig beställning om att uppdatera dashboarden, kör från denna
katalog i huvudprojektet:

```bash
npm run data
npm run test:current
```

Det första kommandot bygger om `public/data/project.json` från `genealogy/`
och `wotan/backlog.json`. Det andra jämför ögonblicksbilden med aktuella filer,
utan att skriva något. Vanliga tester kräver bara intern konsistens och tillåter
att projektet har gått vidare. Ett fristående bygge använder versionssparad data.
