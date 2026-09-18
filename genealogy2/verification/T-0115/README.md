# Verifieringsunderlag för T-0115

Slutrapporten finns i `../T-0115-report.md`. `check.py` verifierar individuell
täckning, bevarade dokumenthashar och utvalda konsolideringsgränser mot den
angivna databasen, normalt huvuddatabasen. `validation-result.json` redovisar
slutlägets kontroller; `focused-tests.log` bevarar de 40 riktade kodproven.

`pending-title-review.json` innehåller den individuella prövningen av 195
följder från S-0711:s titeländring. Dess scratch- och jämförelsefält beskriver
förberedelsens baslinje, inte en separat aktuell databas. Besluten är införda
och finns i versionsjournalen. `T-0115-evidence-links-review-draft.json`
bevarar de fyra beläggs-/routingrättelsernas läsunderlag; filnamnet är historiskt.

`coverage-candidates.json` är den fasta, ännu ej sakdispositionerade mängden
för T-0671. Den innehåller kandidatpar, inte fastställda fel. Wotan äger
utförandet. Ingen av filerna i denna katalog utgör en alternativ uppgiftskö.
