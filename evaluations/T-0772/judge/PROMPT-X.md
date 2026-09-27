## Uppgift X – blind bildgranskning

Läs:
- `{OLD}/x/public/TASK.md` och de fem bilderna `{OLD}/x/public/*.jpg`
  (öppna dem med bildverktyg; egna förstoringar får skrivas i `out/tmp/`),
- `{OLD}/x/private/rubric.json` (fryst rubrik),
- `{NEW}/judge/STANDARD-X.md` (fastställd bedömningsstandard),
- varje `{NEW}/blind/x/Cnnn.json` och motsvarande `{NEW}/scores/Cnnn.auto.json`.

Skriv för varje svar `out/Cnnn.final.json`:

```json
{"task":"x","passed":true,"score":75,"maxScore":75,"critical_errors":[],
 "field_scores":[{"id":"A.r2.name","content":2,"state":1,"reason":"..."}],
 "crossouts_observed":5,"notes":["..."]}
```

`field_scores` har exakt de 25 cell-ID:na. `score` är summan av content+state.
`passed` = score ≥ 68 och inga bekräftade kritiska fel. `crossouts_observed`
är antalet av de fem överstrukna namncellerna B r8–r12 där svaret noterar
överstrykningen (0–5), utan poängpåverkan.

Skriv sist `out/judge-report.md`: vad du läste, visuella gränsfall du själv
prövat, poängprinciper du tillämpat och en tabell Cnnn | poäng/75 | godkänd |
överstrykningar/5.
