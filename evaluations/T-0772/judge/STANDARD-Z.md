# Bedömningsstandard Z (fastställd i T-0769, tillämpas oförändrad)

Destillerad ur T-0769:s blinda Z-granskning och rootens prövning före
avblindning. AI-härledd, inte mänskligt facit.

## Grind
`passed` kräver automatisk 15/15 (verklig införsel i engångsdatabas,
se respektive `Cnnn.auto.json`) och manuellt godkännande. `score` och
`maxScore` är den automatiska poängen oförändrad. Manuellt prövas
operationens reason, varje ändrings rationale och varje resolve.

## Redan prövade gränsfall
- Varje resolve ska ange ett individuellt sakskäl för just det objekt som
  den väntande prövningen gäller (se `input.pendingReviews`). En resolve för
  F-B som bara beskriver R-B:s rättelse och O-B:s underlag, utan F-B:s egen
  omprövning eller datumrättelse, underkänns. Samma text i båda resolve
  underkänns om den inte täcker F-B:s egen rättelse; det avgörande är fel
  objekt eller uteblivet individuellt skäl, inte textlikheten i sig.
- Korta motiveringar godtas när de pekar ut rätt objekt och den faktiska
  datumrättelsen eller evidensföljden. En resolve behöver inte upprepa det
  nya datumets siffror om objekt, rättelse och underlag anges.
- R-B som underlag för F-B läses som den indirekta kedjan R-B → O-B → F-B, i
  linje med prövningens ändrade revision och korrekt bundna evidensfält.
- ”Avläst datum” eller ”efter postgranskning” är beskrivningar av den
  stipulerade rättelsen, inte anspråk på ny arkivundersökning.
- `Provförsamlingen.` med extra slutpunkt i S-A.title: strikt underkänt
  (automatiskt 13/15), `formatting_only_failure: true`; `material_pass`
  bortser enbart från denna punkt och kräver allt annat, inklusive
  individuella resolve-skäl.
