## Uppgift Y – blind sakgranskning av följdprövning

Läs:
- `{OLD}/y/public/TASK.md` och `{OLD}/y/public/input.json`,
- `{OLD}/y/rubric.private.json` (fryst rubrik med manuella kontroller),
- `{NEW}/judge/STANDARD-Y.md` (fastställd bedömningsstandard),
- varje `{NEW}/blind/y/Cnnn.json` i sin helhet och motsvarande
  `{NEW}/scores/Cnnn.auto.json`.

Skriv för varje svar `out/Cnnn.final.json`:

```json
{"task":"y","passed":true,"score":16,"maxScore":16,"critical_errors":[],
 "object_reviews":[{"id":"O1","accepted":true,"reason":"..."}],
 "global_checks":{"all_16_objects":true,"all_9_requests_exact":true,
  "request_mismatches":[],"canonical_changes_empty":true,
  "canonical_substantively_protected":true,
  "automatic_canonical_schema_deviation":false,
  "owner_confirmed_preserved":true,"no_new_person_or_relation":true,
  "identity_gate_preserved_no_new_life_approval":true,
  "existing_ludvig_date_explicitly_retained":true,
  "f5_residence_preserved":true,"no_fabricated_archival_findings":true,
  "evidence_relevant":true,"bounded_followups":true,"full_answer_read":true,
  "automatic_failed_checks":[]},
 "notes":["..."],"sensitivity_pass_without_F5":true}
```

`object_reviews` har exakt de 16 objekten. `score` = antal godtagbara
objektbeslut. `passed` följer standardens grind.

Skriv sist `out/judge-report.md`: vad du läste, gemensamma mönster,
gränsfall och en tabell Cnnn | poäng/16 | godkänd | utan F5-krav.
