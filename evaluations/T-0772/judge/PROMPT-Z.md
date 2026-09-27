## Uppgift Z – blind sakgranskning av ändringspaket

Läs:
- `{OLD}/z/public/TASK.md` och `{OLD}/z/public/input.json` (särskilt
  `pendingReviews`),
- `{OLD}/z/private/RUBRIC.md` (fryst rubrik; kör inte evaluatorn själv,
  resultatet finns i auto-filerna),
- `{NEW}/judge/STANDARD-Z.md` (fastställd bedömningsstandard),
- varje `{NEW}/blind/z/Cnnn.json` i sin helhet och motsvarande
  `{NEW}/scores/Cnnn.auto.json` (verklig införsel i engångsdatabas).

Skriv för varje svar `out/Cnnn.final.json`:

```json
{"task":"z","passed":true,"score":15,"maxScore":15,"critical_errors":[],
 "manual_pass":true,
 "manual_checks":[{"object":"operation.reason","accepted":true,"reason":"..."}],
 "notes":["..."],"material_pass":true,"formatting_only_failure":false}
```

`manual_checks` omfattar operation.reason, rationale för S-A, R-B, O-B, F-B,
varje resolve (`resolve:<objekt>:<request>`) och `package.semantics`.
`score`/`maxScore` kopieras från auto-filen. `passed` = automatisk 15/15 och
manual_pass. `material_pass` och `formatting_only_failure` enligt standarden.

Skriv sist `out/judge-report.md`: vad du läste, sakfel som automatiken inte
fångade, gränsfall och en tabell Cnnn | auto/15 | manuellt | godkänd |
materiellt.
