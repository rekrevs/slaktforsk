# Repository instructions

Work directly on `main`; do not create work branches unless the owner
explicitly requests one. Owner instruction, 2026-09-18. Commit and push
still require authorization as stated below.

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

Follow the repository's provenance rules and the Riksarkivet access order in
`docs/research/riksarkivet-access.md`. Run the
relevant validators and regression tests after changes. Preserve unrelated user
changes. Do not order archival material, publish or deploy, create a PDF, or
commit and push unless the user has authorized that action.
