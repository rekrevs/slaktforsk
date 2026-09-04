# Wotan-konvention för detta projekt

Wotan är projektets enda exekveringskö. Den här filen beskriver den
repo-lokala konventionen som gör att ett kontinuerligt forskningsmål kan
drivas med ändliga uppgifter. Datamodell, statusar och storlekar följer
wotan-skillen; det som står här kompletterar den.

## Målet styr, kön verkställer

- Målet och måttet finns i `NORTH-STAR.md`. Läget mot målet räknas ut med
  `node scripts/goal-state.mjs`, aldrig ur handover-prosa eller chatthistorik.
- En uppgift skärs ur måttets **nästa skiva**: den närmaste obehandlade
  generationen, balanserad mellan Sverkers och Kristinas sida.
- Acceptanskriterier uttrycks som **måttdeltan**: vilka anspetsar som får
  giltig arkivfront, vilka personer som blir `GRANSKAD`, vilka
  källtäckningsceller som lämnar `1`.
- En uppgift är storlek `M` och ska kunna nå `DONE` inom ungefär fem till
  femton batchar. Ett program, en våg eller en kohort är inte en uppgift;
  det är en följd av uppgifter. Ingen uppgift får bli en öppen behållare.
- Vågskiften, utgåvegrinden före ny PDF och ägarfastställda familjefakta är
  Project Control-händelser, inte Wotan-uppgifter.

## En batch skrivs en gång

- **Forskningsloggen** `genealogy/research-log/YYYY-MM-DD.md` är den enda
  batchloggen: vad söktes, var, med vilket resultat, med S-, C-, A- och
  P-referenser. Append-only.
- **Dev-loggen** `wotan/dev-log/T-NNNN.md` bär uppgiftens kontext,
  acceptanskriterier, beslut, hinder och verifieringsbevis. Den upprepar
  inte batchinnehållet; den hänvisar till forskningsloggens datum och batch.
- **HANDOVER.md** är en kort lägessida som **skrivs om**, inte byggs på:
  startordning, aktiv uppgift och skiva, måttkommandot, arbetsyteregler.
  Historik hör inte hemma där.
- Personakter, frontier och källtäckningsmatris uppdateras i samma batch
  som fyndet. Forskningsprogrammet `genealogy/research-plan.md` innehåller
  metod, inte läge.

## Färdig betyder verifierad

- `DONE` sätts först när måttdeltan syns i `goal-state`-utdata och
  validatorer, anspetsrevision och tester har körts och lästs.
- Verifieringskommandon som alltid gäller:

```sh
node scripts/goal-state.mjs
node scripts/validate-genealogy.mjs
node --test scripts/
node scripts/media-manifest.mjs --check
```

- Beställ inte arkivmaterial, publicera, rendera PDF eller committa utan
  ägarens uttryckliga tillstånd. Rapportera vad som kördes och vad som återstår.

## Start av en session

1. Läs `AGENTS.md` och de filer den pekar på.
2. Kör `node scripts/goal-state.mjs` och `git status --short`.
3. Öppna första `ONGOING`, annars första `READY` med uppfyllda beroenden.
   Om kön är tom eller nästa skiva inte har någon uppgift: skär en ny
   uppgift ur måttet, eller stanna om skivan kräver ett ägarbeslut.
4. Arbeta batchvis, logga en gång, verifiera, avsluta uppgiften när dess
   måttdelta är uppnått.
