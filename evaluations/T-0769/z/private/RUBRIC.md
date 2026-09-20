# Frozen Z rubric — T-0769

Defined before scored model trials. Fifteen binary checks, equal weights, maximum 15. Strict acceptance requires 15/15. Partial score is diagnostic only; a rejected operation is never an acceptable production result.

1. Parseable JSON.
2. Exactly the four authorized changed IDs.
3. Native dependency policy 2, task reference and actor.
4. Actual applyOperation succeeds on isolated fixture.
5. Exact simple title correction.
6. Exact record locator correction.
7. Correct observation date and raw date.
8. Correct fact date, raw date and retained caveat.
9. P-A, S-B and OWNER_CONFIRMED F-OWNER current views unchanged.
10. O-B@2→R-B@3 and F-B@2→O-B@2 bindings exist.
11. Two unique individual review resolutions and zero pending; meaningful-length rationale (15+ characters).
12. Exact preserved/added media links; actual verifyAssets succeeds.
13. Expected versions, object kinds, dispositions, origin/evidence arrays, status, caveats and all final data fields match stipulated semantics.
14. Actual verifyDB succeeds.
15. Every preexisting revision and observation remains unchanged.

Motivation length is only a mechanical minimum, not proof of reasoning quality. Parent should inspect the two resolution rationales blind to model and flag irrelevant or interchangeable boilerplate. No hidden factual inference is required. Array order follows the public input; evidence and origins contain one element each.

Fixture is synthetic and tiny, patterned on real project pitfalls. It includes a prior R-B correction generating two pending reviews; the submitted operation updates all affected objects together, so no unpredictable newly generated review IDs need to be guessed. Tests exercise the real domain API, not a JSON-only imitation. No live project DB is opened. Metadata-only source typo is independent of the complex case. Media are tiny synthetic text files, not actual archival originals; file and provenance preservation semantics are real. CLI journaling/recovery and full production scale performance are outside this task.

Commands from repository root:

- `node evaluations/T-0769/z/private/evaluate.mjs /absolute/path/answer.json`
- `node evaluations/T-0769/z/private/self-test.mjs`

`prepare.mjs` is provenance for initial fixture generation; do not regenerate after freeze because fixture timestamps would change. `reference.json` passes all 15 checks; eight injected defects are rejected by self-test. All private files must remain undisclosed to scored agents.
