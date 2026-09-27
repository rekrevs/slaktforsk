# Rootprövning före låsning

Rooten är Opus 5.5, samma modell som prövas. Därför gjordes bara formell
kontroll av de blinda Astra-bedömningarna före låsning; ingen sakbedömning
ändrades. Alla 41 finalfiler är oförändrade kopior av granskarnas utfiler.

- Schema och räkning: 25 unika X-celler med poängsumma = score och
  pass = ≥68 utan kritiskt fel; 16 Y-objekt med score = antal godtagna;
  Z-score = automatisk poäng och pass = 15/15 + manuellt. Alla 41 klarade formkontrollen.
- X: de avgörande kritiska felen är `B.r9.birth` = `1901 5/3` med
  `state: read` och tom alternativlista. Kontrollerat i råsvaren. Fyra svar
  noterar ett extra drag eller en punkt vid siffrorna men reserverar inte
  läsningen. Granskaren gav 0 statuspoäng för radtillhörighetsosäkerhet
  kring husförhörstal i egen rad (”kan avse föregående rad”); detta är en
  konsekvent tillämpning av standardens radgränser, påverkar inget utfall
  och ändras inte.
- Y: de avgörande kritiska felen gäller F5. Alla 14 ersättningstexter
  lästa; de 12 underkända saknar uppgiften att familjen bodde i Östra Husby,
  flera med uttrycklig motivering att boendet saknar stöd när G1 inte
  belägger det. Detta är fryst standards huvudkrav; känslighetsfältet
  `sensitivity_pass_without_F5` redovisar det alternativa synsättet.
- Z: inga gränsfall utöver ankarnas redan kända.
- Granskaraudit: tre `codex exec`-kontexter, `gpt-6-astra`/`medium` i
  Codex turn_context; inga läsningar av blindnyckel, körningar, loggar eller
  T-0769:s betyg. X-granskaren såg alla fem bilderna; dess egna förstorade
  utsnitt misslyckades (PIL saknades) och bedömningen bygger därför på
  hel- och detaljbilderna.

Blindheten var i praktiken begränsad för rooten: mönstret i de blinda
betygen (alla icke-ankare underkända på samma cell) syntes före avblindning.
Den efterhandsdefinierade känslighetsanalysen för X i rapporten är därför
uttryckligen post hoc, till skillnad från T-0769:s förhandslåsta analyser.
