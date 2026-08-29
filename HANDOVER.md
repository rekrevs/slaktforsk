# Handover 2026-08-29

Detta är den korta ingången för en ny Codex-session. Chattens historik är
inte källa för projektläget. Läs filerna och kontrollera arbetsytan innan
någon åtgärd görs.

## Startordning i en ny session

1. Läs `README.md`, `wotan/backlog.json` och `wotan/dev-log/T-0012.md`.
2. Läs slutet av `genealogy/research-log/2026-08-29.md` samt de fyra öppna
   personraderna i `genealogy/frontier.md`.
3. Kör `git status --short`. Arbetsytan är avsiktligt mycket smutsig; rensa,
   återställ eller skriv inte över ändringar.
4. Återuppta bara den aktuella användarinstruktionen. Äldre chattpromptar är
   historik och får inte behandlas som nya uppdrag efter context compaction.
5. Om forskning ska fortsätta: återuppta Wotan T-0012 breddförst. Skapa inte
   en ny dashboard, starta inte T-0013 och påbörja ingen ny utgåve-PDF.

## Aktuellt projektläge

- Aktiv Wotan-uppgift: **T-0012**, `ONGOING` / `DOING`, storlek L.
- Senast färdiga forskningssteg är **batch 78**. Batch 76 fann
  Carlman–Ringberg-vigseln 1862-09-26 i Källa E I/1 (C-0533) och batch 77
  Jansson–Larsson-vigseln 1886-04-26 i Lerbo E I/4 (C-0535), båda via
  publik IIIF utan Chrome; Högby/Bäckebo respektive Lerbo 1883–1885 är
  negativt avgränsade (C-0534, C-0536). Batch 78 avgränsade P-0312/P-0313:s
  vigsel negativt i Jonsberg och Östra Husby 1869–1872 (C-0537). Batch 75:s
  original C-0529–C-0532 är sedan tidigare integrerade.
- Dashboarddatan innehåller 421 personer, 1 863 påståenden och 399
  föräldralänkar. Genealogin har 423 källposter, 535 citationsposter och 1 291
  sakmedier. Mediamanifestet har exakt samma 1 291 filer: 855 exakt bundna,
  408 källavgränsade och 28 citationsavgränsade, utan olänkade filer eller
  identiska hashdubbletter.
- P-0004-baslinjen är 66 kända anor. P-0210 har 56 kända anor och exakt fyra
  öppna djup-4-spetsar: P-0250, P-0336, P-0338 och P-0339. P-0251 Stina Kajsa
  Nordlund är vidareförd till föräldrarna P-0415 och P-0416.
- P-0415 Jonas Nordlund har giltig terminalstatus `IDENTITET OLÖST` på djup 5.
  Hans födelsenotis 1816 matchar namn, datum och ort, men fadersnamnet ser ut
  som Pehr Simonsson medan den senare CEDAR-biografin anger Jonas Stefansson.
  Ingen far har därför skapats för Jonas.
- P-0416 Gertrud Olofsdotters föräldrar P-0417 Olof Stefansson och P-0418
  Sigrid Jonsdotter är säkrade i Stöde C/2.
- T-0013 är `BLOCKED` efter T-0012 och ägarens obligatoriska
  redaktionella/designmässiga kontrollpunkt. T-0009 och T-0010 är parkerade
  `IDEA`, inte körbara nästa steg.

Detaljer finns i:

- `genealogy/research-log/2026-08-29.md` — batch 66–75 och reparationen.
- `wotan/dev-log/T-0012.md` — krav, beslut och hela körhistoriken.
- `genealogy/frontier.md` — personvis aktuell forskningsfront.
- `genealogy/source-coverage.md` — prövade och kvarvarande källfamiljer.
- `genealogy/method-riksarkivet.md` — reproducerbar Chrome- och källmetod.

## Återställd batch 75

De fyra original som först upptäcktes som avbrutet arbete har integrerats:

| Citat | Bild / huvudresultat |
|---|---|
| C-0529 | Stöde SCB 1872: Jöns Peter, son till Abraham Jönsson och Stina Cajsa Nordlund i Hullsjö |
| C-0530 | Sättna A I/8 s. 255: Stina Cajsa i föräldrahushållet Jonas Nordlund och Gertrud Olofsdotter, med fyra syskon |
| C-0531 | Holm C/1 1816: Jonas född 9 oktober; konflikt i fadersnamnet, ingen far skapad |
| C-0532 | Stöde C/2 1812: Gertrud, dotter till Olof Stefansson och Sigrid Jonsdotter i Hullsjö |

S-0266, S-0264 och S-0261 breddades och S-0419 skapades. P-0415–P-0421 och
A-2353–A-2365 bevarar personer och slutsatser. Bilddimensioner, SHA-256 och
proveniens finns i citationsposterna och `genealogy/media-manifest.json`.

## Reparation efter compaction-audit

Följande är reparerat och ska inte göras om:

- Relationsparsern misstolkade flerordsrubriker som `Historisk kandidatpost:`
  och `Make 1930:` och skapade fem falska föräldralänkar till P-0027 samt tre
  cykler. Parsern och regressionstesterna är rättade; inga självkanter,
  dubblettkanter, reciproka eller längre cykler, eller personer med fler än
  två föräldrar återstår.
- Dashboardens påståendecitat räknades dubbelt när samma C-ID förekom både i
  Markdown-länkens etikett och href. Bygget deduplicerar nu varje påståendes
  C-ID:n, och testet bevakar detta.
- De dubbla källposterna S-0068, S-0123 och S-0198 har slagits ihop med S-0008,
  S-0081 respektive S-0116. Levande citat pekar på de kvarvarande posterna.
- Två bitidentiska JPEG-kopior under C-0372 och C-0434 har tagits bort efter
  att citaten pekats om till de bevarade originalen för C-0273 och C-0342.
  Citationsposterna C-0372 och C-0434 finns kvar som separata evidensposter.
- Mediamanifestet är regenererat och rent: noll orphan-filer och noll
  identiska hashgrupper.

## Nästa forskningsåtgärd

Fortsätt breddrotationen från batch 78; följ inte den nyöppnade Nordlundgrenen
förbi väntande djup-4-arbete. Publik IIIF (`curl` med webbläsar-`User-Agent`)
räcker för volymer som svarar `200`; Chrome behövs bara för inloggade
volymer. Säkra återstarter är:

- **P-0310 Karl August Carlman:** andra vigseln med P-0357 i Högby E I/2
  1864–1894 (batch `A0008454`, bild 7 och framåt) och egen död i Högby F/2
  1895–1925 (batch `80003338`); båda svarar `200`.
- **P-0125 Lars Andersson:** död före april 1886 enligt C-0535; sök egen
  dödpost i Lerbo F 1867–1886. Ompröva samtidigt C-0016:s `Gånga` mot
  vigselns `Spånga`.
- **P-0312/P-0313:** vigselförsamlingen är okänd efter C-0537; läs Carolinas
  utflyttning i Jonsberg B och inflyttningsattesten i Östra Husby A I
  1866–1875 (Gäddestad) innan någon ny vigselbok öppnas.

- **P-0250 Abraham Jönsson:** läs Medelpads västra domsagas tingslag
  `SE/HLA/1040237`, `F II a/9` (ArkivDigital AID `v510406`) först efter
  manuell ALTCHA eller behörig ArkivDigital-inloggning. Inferera inget innan
  själva akten är läst.
- **P-0336 Olaus Fredberg:** egen föräldrapost eller gemensamt hushåll
  återstår. För inte automatiskt över brodern Johan Augusts föräldrar.
- **P-0338 Henrik Henriksson:** A I/4 Lagfors s. 23–33 och A I/5 s. 27–41 är
  redan radlästa. Återstart kräver familjeregister, bruksarkiv eller en ny
  positiv hushållsnyckel.
- **P-0339 Margareta Charlotta Sjödin/Sjölin:** 22 Stockholmsregister och
  Ljustorp B I/2:s förda inflyttningsföljd är redan kontrollerade. Återstart
  kräver ny församling, destination, döds- eller bouppteckningsnyckel.

När arbetet senare når djup 5 är P-0415 en exakt återstart för att lösa
fadersnamnskonflikten genom äldre Holm-hushåll och flyttkedjan. Upprepa inte
bara samma födelsenotis eller CEDAR-biografi.

## Riksarkivet och Chrome

Den fungerande metoden är verifierad med pluginversion **26.820.60940**. En ny
session får inte anta att den gamla browser-bindningen lever kvar:

1. ladda pluginens absoluta `browser-client.mjs`;
2. anslut med `agent.browsers.get("chrome")`;
3. namnge sessionen;
4. skapa alltid en ny styrd flik med `chrome.tabs.new()`;
5. kontrollera `Inloggad som:`/`Logga ut` i DOM;
6. navigera direkt och använd semantiska bildvisarkontroller;
7. hämta `Hela bilden …px (jpg)` och bevara dimensioner samt SHA-256.

Använd ingen AppleScript-styrning, kakextraktion, profilläsning, sandboxflykt
eller övertagning av gamla flikar. ALTCHA/CAPTCHA och `401` är åtkomstbesked,
inte nollresultat. Full metod finns i `genealogy/method-riksarkivet.md`.

## Dashboard — skapa inte en tredje

Det finns två skilda dashboardartefakter:

1. Ett tidigt, tillfälligt lokalt koncept, **Slakt Dashboard Concept**, som
   kördes på `http://127.0.0.1:56542/` och kan vara avstängt.
2. Projektets beständiga implementation i `dashboard/`, **Släktarkivet**, på
   <https://slaktarkivet.rekrevs.chatgpt.site/>. Hostingprojekt:
   `appgprj_6a91bf98d5788191bbd3f09db81e4541`.

Den andra är implementationen som ska utvecklas vidare. Den är skrivskyddad
och bygger `dashboard/public/data/project.json` direkt från projektfilerna;
den har ingen separat faktadatabas. Kör `npm test` och `npm run build` i
`dashboard/`. Publicerad data kan ligga efter arbetsytan. Publicera inte utan
en aktuell användarinstruktion om deployment.

Tidslinjen visar att prototypens artefakt- och uppgiftsstate inte bars fram
över context compaction, vilket ledde till en parallell implementation och en
felaktig efterhandsbeskrivning. Den visar däremot inte att den äldre
byggprompten i just detta fall spelades upp ordagrant: användaren skrev en ny
`ok bygg detta` efter kompakteringen. Den offentliga kommentaren har rättats
så att den gör denna skillnad.

## Context-compaction-buggen

- Korrigerad offentlig reproduktionskommentar:
  <https://github.com/openai/codex/issues/31659#issuecomment-5460997128>
- Relaterade ärenden: `openai/codex#31659`, `#35226`, `#35935`.
- `/feedback`-texten skrevs i chatten, men någon separat kvittens eller
  feedback-session-ID observerades inte.

Det säkert belagda mönstret här är förlust av artefakt-/uppgiftsstate över
compaction, parallellt arbete och därefter felaktig statusbeskrivning. Äldre
promptåterspelning förekommer enligt användarens återkommande erfarenhet, men
dashboardtidslinjen ensam bevisar inte ordagrann återspelning.

## Arbetsyta och bevarande

- Gren: `main`; privat remote: `https://github.com/rekrevs/slaktforsk.git`.
- Arbetsytan är avsiktligt mycket smutsig. `HANDOVER.md`, `dashboard/`, nya
  käll-/citat-/personposter och många originalmedia är pågående projektarbete.
- Gör inte `git clean`, reset, checkout eller annan bred återställning. Gör
  ingen commit, push eller deployment utan en aktuell användarinstruktion.

## Senast verifierat

Efter batch 78 passerade:

- `node --test scripts/ancestor-audit.test.mjs` — 4/4 tester.
- `node scripts/validate-genealogy.mjs` — 1 863 påståenden, 1 397
  Markdownposter och 1 292 filer i mediakatalogen inklusive `.gitkeep`.
- dashboardens `npm test` — 421 personer, 1 863 påståenden och 399
  föräldralänkar. `npm run build` föll efter batch 76 på ett miljöfel i
  `dashboard/node_modules/vinext` (`cli.js` importerar
  `build/preview-credentials.js` som saknas i installerad `1.0.0-beta.3`);
  det är oberoende av projektdatan och `node_modules` lämnades orört.
- `node scripts/verify-pedigree.mjs` — P-0004-baslinjen 66.
- `node scripts/verify-depth5-wave.mjs` — pass.
- `node scripts/media-manifest.mjs --check` — 1 291 sakmedier, 0 olänkade.
- mediamanifest-, Wotan- och dashboard-JSON — giltiga.
- `git diff --check` — pass; inga levande länkar pekar på de tre borttagna
  dubblettkällorna.

P-0210-auditen till och med djup 4 ger avsiktligt icke-noll och räknar exakt
de fyra öppna spetsarna P-0250, P-0336, P-0338 och P-0339. Till och med djup
5 har den 27 spetsar, varav P-0415 har giltig terminalstatus och 26 ännu saknar
giltig slutstatus. Detta är väntat forskningsläge, inte ett regressionsfel.

Kör en proportionerlig verifiering efter nästa ändring och skriv resultatet i
T-0012-loggen och dagsloggen.
