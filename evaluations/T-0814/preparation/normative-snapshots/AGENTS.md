# Repository instructions

Work directly on `main`; do not create work branches unless the owner
explicitly requests one. Owner instruction, 2026-09-18. Commit and push
still require authorization as stated below.

## Model allocation

Owner-approved working rule, 2026-09-19, based on the
[T-0769 evaluation](evaluations/T-0769/report.md):

- Use **Astra** for source interpretation, identity and evidence judgements,
  conflicts, and final assessment of how corrections affect existing knowledge.
- Use **Sol** for bounded implementation of already-settled decisions with
  explicit inputs, expected changes and verifiable acceptance criteria. Run
  the applicable validators; return unresolved interpretation or evidence
  questions to Astra before applying dependent changes.
- Do not use **Terra or Luna** for project work unless the owner changes this
  rule. When the boundary between Astra and Sol is unclear, choose Astra.

This is a practical allocation rule from a small benchmark, not a guarantee
of correctness. Existing source checks and review requirements still apply.

### Working procedure for bounded G001 research batches

Persisted for session continuity at the owner's request, 2026-10-02.
This clarifies the existing allocation; it does not establish a cost-saving
guarantee or expand an approved batch. The evidence is preserved in
[T-0776's review](evaluations/T-0776/independent-final-review-v1.md) and
[working rubric](evaluations/T-0776/rubric-v1.md).

- Root coordinates the bounded batch. Delegate mechanical preparation and
  settled implementation to **gpt-6.1-sol**, source/evidence decisions to
  **gpt-6-astra**, and final source/consequence review to a separate
  **gpt-6-astra** agent. These roles do not delegate further. Keep Astra's
  work focused on interpretation, evidence and consequences; Sol prepares
  complete current inputs and performs the mechanical checks.
- Before new source interpretation, reconcile actual accepted receipts and
  the canonical journal, then lock the exact scope, original hashes, current
  relevant objects, stronger older support and quality criteria. Metadata
  routing is not a certified list of source people. Reuse sufficient research.
- Astra reads the full relevant record, including headers, own-row dittos,
  blanks and margins, and gives explicit source-bound decisions. A repeated
  own-row attribute need not be written out. Different records in one
  registration chain do not automatically provide independent evidence.
- Sol builds an individual consequence table with object/version, exact
  field, old wording, support and Astra's disposition, including retains.
  Search beyond citation IDs and Markdown bodies: check caveats, outcomes,
  status fields and structured keys too. Dated anchors must reach applicable
  gap descriptions without implying continuous physical residence; unread
  or untested claims must identify their exact source/time/field scope.
  Read the whole current body and caveat before treating explicitly superseded
  historical wording as current ignorance. Clear stale template flags only
  from already-settled decisions, with an explicit metadata amendment.
- A requested correction with zero or unexpected multiple matches, an
  unresolved interpretation, or a required evidence-version rebind returns
  to Astra before dependent changes. Do not silently skip it or substitute
  wording. Preserve initial candidates, rejected attempts and later amendments.
- The independent Astra reviewer first records its own original reading
  before seeing candidate claims, then searches current semantic copies
  independently of Sol's list and checks stronger support. Final approval
  binds the exact corrected package by hash; technical PASS alone is not
  source approval. The complete independent review remains part of the method.
- Sol tests the exact canonical-ready operations sequentially on a baseline
  clone, preserving data-array order, full metadata/evidence/origins,
  individual dependency resolutions and protected knowledge/review state.
  Run applicable validators. Root checks the live baseline and approved
  package before controlled canonical apply, then verifies the actual result
  against the reviewed stage. Never promote by replacing the main database.
- Measure real work as well as source count: coverage, native changes,
  findings, correction burden and elapsed time. Count preparation, both Astra
  roles, failed attempts, repairs and finalization as production. Collect
  actual new-turn model usage after worker final responses; distinguish cache
  and output, and report unobservable root usage as unknown rather than zero.
  Record meter readings and concurrent consumption separately. Shared budget
  changes and unequal source scopes do not prove savings or superior quality.

Current progress, the next unperformed step and the owner's batch limit belong
in the active Wotan task's latest `Återupptagning`, not in this procedure or
a separate handover file. A session change does not repeat accepted work or
authorize a fourth source after a completed three-source batch.

## Research workflow

Genealogy2 is the authoritative knowledge model after T-0643's verified
cutover (PCD-2026-09-16-001 and PCD-2026-09-17-001). Read
`genealogy2/README.md`, its local instructions and `genealogy2/docs/working.md`.
Use the controlled versioned write path for all new research and corrections.
`genealogy/` is a preserved, read-only research archive; do not resume writing
its dossiers, profiles, logs or derived inventories. Current research and access
norms live in `docs/research/`; archived instructions in genealogy are historical,
including its README. The dashboard remains an
older snapshot until the owner explicitly requests an update.

Read the project's durable context before doing work:

1. `README.md` for orientation.
2. `NORTH-STAR.md` for the permanent objective and quality contract.
3. `genealogy2/README.md` and `genealogy2/docs/working.md` for the current
   evidence model, reading commands and controlled writing workflow.
4. Read `docs/research/research-program.md`, `docs/research/person-contract.md`
   and `docs/research/source-strategy.md` for balanced generations, PK-01–12,
   source selection and full extraction. These are the current normative texts;
   their frozen originals are provenance, not alternative instructions.
   Read the selected persons through `person`, `inspect` and their
   current `research` objects. Use `context` for archived front, coverage and
   source-path history; those frozen texts are not current execution state.
5. `PROJECT-CONTROL.md` for approved owner decisions and exceptions.
6. For task work, always read `wotan/README.md` before selecting, creating
   or resuming a task. Then read `wotan/backlog.json` and the selected
   `wotan/dev-log/T-NNNN.md`, including its latest `Återupptagning` section.
   Reading the skill alone does not replace this repository-local convention.

Run `node genealogy2/cli.mjs inventory` and the default verified
`node genealogy2/cli.mjs pedigree <P-id>` for current review and pedigree views.
Read full person details and source-path assessments for substantive coverage.
The old goal-state and research-inventory scripts describe only the frozen
archive; never run their write modes to refresh it. No indicator proves the
substantive fulfillment requirements in NORTH-STAR.md.
Use canonical evidence and decisions, not chat history, to resolve discrepancies.

Update the dashboard (including its data snapshot) only when the owner explicitly
requests it. Research, task completion, tests, builds, session preservation and
commit/push do not imply permission to refresh it. Routine checks must accept an
older, internally consistent dashboard snapshot; use canonical files for current
project state. See PCD-2026-09-05-014 and `dashboard/README.md`.

Wotan is the sole execution and resumption state. Do not introduce HANDOVER.md
or a separate session-start task/list. Save partial work, evidence, pending
verification and the next unperformed step in the current task before a planned
interruption. Resume ONGOING before READY and reconcile its checkpoint with the
working tree; rereading instructions does not authorize repeating completed work.

Use Wotan for task or backlog work and Project Control for strategic steering.
Do not start research outside an active, approved, bounded Wotan task. Research
tasks follow the nearest substantively untreated generation, balanced between
both sides, including disputed closures before deeper or already well-documented
branches. Give each task explicit scope, exclusions and verifiable outcomes;
split new work instead of growing an unlimited task. Record each research batch
once through its genealogy2 operation and durable journal; include the task id
and acceptance criterion, and link that operation from Wotan.

Apply the person contract to new, partial, disordered, disputed, previously
closed and side-person dossiers, **at the level the task works on**. The
contract has two completion levels (`docs/research/person-contract.md`, "Två färdignivåer"):
the identity level (PK-01, 02, 05, 07, 09, 11, 12) is the pedigree's gate and
uses `identity_review/1` and `tree_effect/1`; the life-picture level
(PK-03, 04, 06, 08, 10), including the ten themes, may lag and uses
`life_picture_review/1`. Older explicit Identitetsgranskning/Trädverkan
headers remain readable without new approval. Legacy Kontraktsgranskning
retains its original full-contract scope; it is not a new native life review.
A front task that ends with the identity level approved
and the life picture untouched is complete, not half-done. Never let a line of
descent pass a person whose `Trädverkan` is not `BÄRANDE`, and never merge the
two levels into one measure. Reuse sufficient existing research; never
auto-convert legacy GRANSKAD/KLAR to a passed contract review. Every touched
research dossier gets a profile or an explicit bounded adoption step in the
current task, represented in native research objects rather than new Markdown
files. Assess the ten life themes at the life-picture level, preserve
full relevant extraction from every record actually opened, track source paths
by time/place/coverage, and use new search keys to reassess dependencies across
affected people. Native research objects, their profile views and the derived
inventory hold knowledge/review state only; Wotan alone schedules and resumes execution.
Task DONE, accepted ancestry, rich biography and source exhaustion are distinct.

During an explicitly continuous north-star run, an empty or blocked queue calls
for Project Control to assess remaining requirements and create justified bounded
work within delegated authority, not automatic completion. Single-task requests
and session-preparation work remain bounded by the user's current request.

Treat the evidence ledger as append-only and the canonical person model as
revisable. One person record must represent one real person. Keep competing
identities separate, preserve conflicts, and never propagate an explicitly
uncertain identity or parent relation into the verified pedigree. Observations,
conclusions and work status are separate layers; accumulated observations alone
do not make a person or generation complete.

When the owner explicitly states that a family fact is certain, accept it as
true project information and record it as `OWNER_CONFIRMED` in the canonical
model and as a Project Control Decision. Do not demote owner-confirmed knowledge
merely because an archival original is absent; preserve any later conflict and
bring it back to the owner instead of silently overriding the decision.

Owner clarification, 2026-10-07: this applies to **all** owner-confirmed
information in subsequent work, not only the most recently discussed fact.
Before interpreting or revising a person's identity, relations, research gaps
or tree gate, retrieve and use the relevant current OWNER_CONFIRMED objects
and their exact owner decisions. Preserve their scope and provenance; a missing
archival original or unfinished extraction is not a new proof requirement for
an owner-confirmed fact. Keep archive/life-picture gaps visible separately.
An actual contradictory source is a conflict to preserve and bring to the
owner, never a reason to silently downgrade owner-confirmed knowledge.
Do not extend a confirmed fact to unconfirmed identities or ancestor relations.

Follow the repository's provenance rules and the Riksarkivet access order in
`docs/research/riksarkivet-access.md`. Run the
relevant validators and regression tests after changes. Preserve unrelated user
changes. Do not order archival material, publish or deploy, create a PDF, or
commit and push unless the user has authorized that action.


## Beständigt sökminne

Ägarbeslut2026-10-07: dokumentera samtliga resultatlösa sökningar per person/fråga med stabilt sök-ID/revision, exakt faktiskt material-ID/åberopad källversion, leverantörsversion eller uttryckligen okänd version, datum, söknycklar/metod, exakt läst omfång, kopiehash eller motiverad kopiebrist och återstartvillkor. Före ny sökning återbrukas tillräckliga tidigare pass enligt genealogy2/docs/working.md:s sökminnesstandard. Åtkomsthinder är inte söknoll; modellrevision är inte leverantörsversion. Historiska kvitton ändras inte och okända äldre metadata fabriceras inte.

## Hård kärnträdsprioritet — PCD-2026-10-05-001

Ägarens2026-10-05 beslut ersätter HELA originalrevisionens tidigare automatiska köföreträde. AdamP0269/AxelP0270:s närmaste sakligt otillräckliga direkta anled, identitetsgrindar och föräldrafrågor går först, balanserat mellan Sverkers och Kristinas sida. Använd current body/caveat/PK/stronger/OWNER och exakt accepted återbruk; äldre failed-grind är varken automatiskt personosäkerhet eller automatiskt PASS. Full livsbild är separat och planeras avgränsat i generationsvågen; nästa djup får inte bli skäl att uppskjuta den permanent.

Wotan är fortfarande den enda kön. CORE_IDENTITY och CORE_LIFE kräver exakt P-id/relation/fråga och bounded dev-log; CORE_SUPPORT kräver en konkret nödvändig kärnleverans. Relevanta sidopersoner/kandidater kan vara CORE_IDENTITY när anfrågan kräver dem. DEFERRED är bevarat lägre prioriterat arbete, inte orelaterat/avskrivet/avslutat. Oklassade gamla och nya uppdrag är inte automatiskt tillåtna kärnuppgifter. Främja endast sakligt prövade avgränsade delar. Dela blandade scopes förlustfritt före utförande, med exakt union, restägare, full äldre AC/checkpoint och återbruk. Alla nödvändiga följdrättelser även i sidoobjekt ingår fortsatt i sourcekvaliteten; ny fristående sidoforskning utvidgar aldrig kärnbatchen.

Läs wotan/README.md och kör `node scripts/wotan-priority.mjs` före nästa uppgiftsval. Återuppta behörig ONGOING först; en DEFERRED ONGOING kräver checkpoint/Project Control, aldrig tyst avbrott. Välj annars första behöriga kärn-READY i backlogordning inom faktiskt körmandat. Om sådan saknas: Project Control för verklig kärngrind och möjlig nästa boundedpassage; kör aldrig DEFERRED automatiskt och skapa inte obegränsat mandat. Explicit ägarbeställning av lägre uppgift är ett tillåtet avgränsat undantag, dokumenterat i dess checkpoint/PC, utan generell fallback. Priority eller READY ger inte i sig ett nytt utförandemandat.

Fullmaterialrevisionens fasta union, append-onlyevidens, aktuella person-/granskningsnivåer, egna originals läsomfång och slutgrind består. Håll alla uppskjutna frågor synliga med exactperson/source/time/field, tidigare accepterade steg, återstående steg, ägare och verkligt återstartvillkor; köprioritet får aldrig fabricera after/blocker/IDEA/DONE. Inga frysta arkiv-/dashboardwrites följer av detta beslut.


## Stående pushgodkännande —2026-10-08

Ägaren: ”stanna inte och fråga om sådant utan kör på. jag godkänner alla pushar i detta projekt.” Alla pushar till detta projekts befintliga origin/main är ägargodkända; begär inte nytt rutinmedgivande. Se PCD-2026-10-08-002. Detta utvidgar inte forskningsomfång eller övriga åtgärdsmandat; commit följer tillämpligt mandat.
