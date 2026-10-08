# Genealogy2: auktoritativ kunskapsmodell

- T-0643:s verifierade skifte 2026-09-17 är genomfört enligt
  PCD-2026-09-16-001 och PCD-2026-09-17-001. Läs README här,
  [arbetsvägen](docs/working.md) och aktuell Wotan-uppgift.
- All ny forskning och alla rättelser skrivs genom `apply`. Direkt
  SQL-redigering, ändrad journal eller handredigerad export är ingen
  godkänd forskningsväg. Bara huvuddatabasen används för ordinarie skrivning.
- Gamla `genealogy/` är ett bevarat, skrivskyddat forskningsarkiv. Skapa
  inga nya personakter, profiler, loggbatcher eller inventeringar där.
  Dashboarden uppdateras endast på ägarens uttryckliga begäran.
- Läs aktuella personvyer, forskningsobjekt och deras underlag. `person`
  ger översikten; `--full --format markdown` och `--format json` ger hela
  underlaget. `show` och `context` visar det frysta äldre materialet.
- Importbas, äldre objektrevisioner och evidenshistorik får aldrig skrivas
  om. Rättelser ger nya versioner och individuell beroendegranskning.
  Mekanisk extraktion är ingen ny slutsats eller oberoende källa.
- En observation och ett omnämnande hör till sin egen avgränsade källpost.
  Jämförelser mellan poster är slutsatser med alla underlag. Rådatum,
  källberoenden, konflikter, begränsade noll och förbehåll ska bevaras.
- En personkärna ska avse en verklig person. Håll konkurrerande identiteter
  åtskilda. Bevara OWNER_CONFIRMED utan tyst nedgradering. Härled inte kön
  ur namn eller deltagarroll och gör inte vittnen till föräldrar.
- Läs de aktuella normerna i `../docs/research/`: person-contract.md,
  research-program.md, source-strategy.md och riksarkivet-access.md.
  Rootens README äger ansvarskartan; NORTH-STAR äger sakmålet.
  De gamla dokumentformaten är inte krav på nya forskningsobjekt.
  Identitetsnivå och livsbild granskas separat. `pedigree` använder den
  verifierade identitetsgrinden som standard; `--mode typed` gör inte det.
  Accepterad person, färdig task och äldre KLAR är inga granskningsgodkännanden.
- Forskningsfrågor, teman, källvägar och söknycklar är kunskapsobjekt.
  Wotan är enda utförandekön. Batchen bevaras en gång i operation/journal
  med uppgift och acceptanskriterium; Wotan länkar till operations-id.
- Kör databas-, käll-/medie- och relevanta sak-/regressionskontroller.
  Vid breda modelländringar kör hela testsviten. Bevara testlogg och resultat
  i aktuell Wotan-uppgift; en grön strukturkontroll ersätter inte sakgranskning.
- Nya medier registreras med `stage-media` och provenans. Följ repositoryts
  Riksarkivsordning och åtkomstförbud. Beställ, publicera, skapa PDF eller
  committa/pusha endast med ägarens mandat för åtgärden.
- Säkerhetskopiera databas, importbas och verkliga medier med `backup-bundle`.
  Bevara kod, schema, importbas, operationspaket och journal i Git enligt
  PCD-2026-09-18-001 och T-0666/T-0667; bilder bevaras separat med Git LFS.
  T-0665:s dumpförsök och restic är parkerade. Kör inte backup.sh som rutin.
  Beskriv inte återuppbyggnad från Git som fullständigt verifierad innan
  provens dokumenterade omfång faktiskt stöder det.
  Återställ till en ny rot och verifiera även senare journal och medier.
  En äldre snapshot räcker inte efter nya skrivningar.
- Fortsätt från Wotans senaste Återupptagning. En ny session ska inte
  återskapa importbasen eller repetera redan verifierade migrationer.
