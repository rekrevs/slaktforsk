# Handover

Kort lägessida för en ny agentsession. Den skrivs om vid varje uppgiftsskifte
och byggs inte på. Chattens historik är inte källa för projektläget; filerna
och `node scripts/goal-state.mjs` är det. Historiska handovers finns i
`genealogy/research-log/handover-archive-2026-09-04.md`.

## Startordning

1. Följ `AGENTS.md`: läs `README.md`, `NORTH-STAR.md`, `genealogy/README.md`,
   `genealogy/research-plan.md`, `genealogy/method-riksarkivet.md`,
   `PROJECT-CONTROL.md`, `wotan/README.md` och `wotan/backlog.json`.
2. Kör `node scripts/goal-state.mjs` och `git status --short`. Rensa,
   återställ eller skriv inte över ändringar som finns i arbetsytan.
3. Läs den aktiva uppgiftens dev-log och den senaste dagsloggen under
   `genealogy/research-log/`. Batchhistorik läses bara vid behov.
4. Återuppta bara den aktuella användarinstruktionen. Äldre chattpromptar är
   historik och får inte behandlas som nya uppdrag efter context compaction.

## Aktuellt läge 2026-09-04

- Senaste styrbeslut: `PCD-2026-09-04-006`. Efter att T-0013 verifierat den
  första djup-6-skivan ska T-0033 behandla den andra balanserade skivan:
  P-0145, P-0214, P-0289 och P-0290 på Sverkers sida samt P-0350, P-0351,
  P-0360 och P-0361 på Kristinas sida. Nya djup-7-föräldrar registreras men
  deras anor forskas inte vidare i uppgiften.
- T-0032 är `DONE`. Den visuellt och strukturellt verifierade version 4 finns
  i `output/pdf/adam-och-axel-janson-fem-generationer-v4.pdf`: 43 sidor,
  varav två sammanhängande 31-personers träd och 31 katalogsidor för 62 unika
  personer. Träden visar namn, kända levnadsår och ort utan interna koder;
  katalogen visar ID, namngivna familjerelationer, kända livsuppgifter och
  C-referenser. Version 1–3 är bytebevarade. V4:s SHA-256 är
  `5d9dfabda85c7c4c3e1c4171068961931a4f3caa9b8dfa6933f48faf75a47259`.
- T-0013 är `DONE`: alla åtta mål har giltig front eller verifierade
  föräldrar. P-0123 fick P-0264 Lorentz Urbom och P-0265 Anna Maja
  Eriksdotter som korroborerade föräldrar; P-0344 fick P-0502 Lars Larsson
  och P-0503 Anna Jonsdotter. Övriga sex fick reproducerbara terminala
  fronter. Batch 258 är uppgiftens enda forskningsloggpost.
- Mätt läge: gemensamt djup 5. Djup 6 har 55 kända och nio stängda
  positioner, åtta granskade och källbreddsklara personer samt 31 ogiltiga
  fronter till och med djupet. T-0033 är nästa `READY` M-uppgift.
- Kvalitetsgrinden: inga `LEAD`-, `CONFLICT`-, `REJECTED`- eller
  `UNKNOWN`-relationer propagerar. Ägarfastställda relationer
  (`OWNER_CONFIRMED`, PCD-2026-08-20-001, -08-29-001, -09-03-003/-004/-005)
  kräver inga arkivbelägg. Utgåvegrinden i `PCD-2026-08-23-001` är uppfylld
  genom `PCD-2026-09-04-002`; den aktuella bruksversionen styrs av
  `PCD-2026-09-04-005` och den verifierade version 4-utgåvan.
- Bevarade nollresultat och exakta återstartvillkor står i personakter,
  citationer och `genealogy/source-coverage.md`. Upprepa inte en dokumenterad
  sökning utan ny nyckel.

## Arbetsregler som alltid gäller

- Riksarkivets åtkomstordning: MCP först där den täcker behovet, därefter
  API/JSON-LD/OAI/IIIF, sist inloggad katalog eller Chrome. Full metod i
  `genealogy/method-riksarkivet.md`. ALTCHA/CAPTCHA löses inte utan ägarens
  uttryckliga bekräftelse; `401`/`403` är åtkomstbesked, inte källnoll.
- Beställ inte arkivmaterial, publicera eller deploya inte, skapa ingen PDF,
  committa eller pusha inte utan en aktuell användarinstruktion.
- Gör inte `git clean`, reset, checkout eller annan bred återställning.
- Dashboard: projektets implementation är `dashboard/` (Släktarkivet,
  <https://slaktarkivet.rekrevs.chatgpt.site/>, hostingprojekt
  `appgprj_6a91bf98d5788191bbd3f09db81e4541`). Skapa ingen ny dashboard. Den
  bygger `public/data/project.json` från projektfilerna; kör `npm test` och
  `npm run build` där. Publicerad data kan ligga efter arbetsytan.
- Gren `main`; publik remote `https://github.com/rekrevs/slaktforsk.git`
  med Git LFS för media, se `MEDIA-PRESERVATION.md`.

## Verifiering efter varje batch

```sh
node scripts/goal-state.mjs
node scripts/validate-genealogy.mjs
node --test scripts/
node scripts/media-manifest.mjs --check
PROBAND=P-0004 node scripts/ancestor-audit.mjs --through-depth=5
PROBAND=P-0210 node scripts/ancestor-audit.mjs --through-depth=4
cd dashboard && npm test && npm run build
```

Anspetsrevisionerna ger avsiktligt icke-noll så länge öppna spetsar finns;
läs listan, inte bara exitkoden. Skriv verifieringsresultatet i uppgiftens
dev-log och batchinnehållet i dagsloggen.
