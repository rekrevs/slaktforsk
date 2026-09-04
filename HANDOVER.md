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

- Senaste ägarbeslut: `PCD-2026-09-04-001`. North star har fått ett
  beräkningsbart mått och en styrregel; Wotan används som ändlig kö skuren
  ur måttets nästa skiva; en batch loggas en gång i dagsloggen.
- T-0012 är stängd vid konsolideringsgrinden (T-0021). Den återstående
  kohorten är skuren i ändliga uppgifter T-0022–T-0029, två per steg och
  sida enligt styrregeln: djup 1–4 (T-0022 S, T-0023 K), arkivfronter på
  djup 5 (T-0024 S, T-0025 K), konsolidering djup 5 (T-0026, T-0027) och
  källbredd djup 5 (T-0028, T-0029). T-0013 väntar bakom dem och
  utgåvegrinden. Nästa `READY` är T-0022; ingen uppgift är `ONGOING`.
- Mätt läge: gemensamt djup 0 under det nya kontraktet. Djup 1–4 från Adam
  och Axel saknar konsolideringspass och källbreddsdisposition; djup 5
  (kohorten om 32) har tre anspetsar utan giltig arkivfront, P-0051, P-0336
  och P-0339, samt oprövade prioritet-1-källfamiljer på alla 32.
- Kvalitetsgrinden: inga `LEAD`-, `CONFLICT`-, `REJECTED`- eller
  `UNKNOWN`-relationer propagerar. Ägarfastställda relationer
  (`OWNER_CONFIRMED`, PCD-2026-08-20-001, -08-29-001, -09-03-003/-004/-005)
  kräver inga arkivbelägg. Utgåvegrinden i `PCD-2026-08-23-001` gäller:
  ingen ny PDF utan ägardiskussion.
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
- Gren `main`; privat remote `https://github.com/rekrevs/slaktforsk.git`
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
