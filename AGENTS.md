# Repository instructions

Read the project's durable context before doing work:

1. `README.md` for orientation.
2. `NORTH-STAR.md` for the permanent objective and quality contract.
3. `genealogy/README.md` for the evidence and knowledge model.
4. `genealogy/research-plan.md`, `genealogy/person-contract.md` and
   `genealogy/source-strategy.md` for the binding program, PK-01–12 outcome
   requirements and source selection. Then `genealogy/frontier.md` and
   `genealogy/source-coverage.md` for current research gates; read the selected
   persons' dossiers and `genealogy/research-profiles/P-NNNN.md` when working them.
5. `PROJECT-CONTROL.md` for approved owner decisions and exceptions.
6. For task work, always read `wotan/README.md` before selecting, creating
   or resuming a task. Then read `wotan/backlog.json` and the selected
   `wotan/dev-log/T-NNNN.md`, including its latest `Återupptagning` section.
   Reading the skill alone does not replace this repository-local convention.

Run `node scripts/goal-state.mjs` and `node scripts/research-inventory.mjs`
for the separate pedigree and all-dossier review indicators.
These do not prove the substantive fulfillment requirements in NORTH-STAR.md.
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
split new work instead of growing an unlimited task. Log each research batch
once, in `genealogy/research-log/`.

Apply the person contract to new, partial, disordered, disputed, previously
closed and side-person dossiers. Reuse sufficient existing research; never
auto-convert legacy GRANSKAD/KLAR to a passed contract review. Every touched
research dossier gets a profile or an explicit bounded adoption step in the
current task. Assess all ten life themes, preserve full relevant extraction,
track source paths by time/place/coverage, and use new search keys to reassess
dependencies across affected people. Profiles and the derived inventory hold
knowledge/review state only; Wotan alone schedules and resumes execution.
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
`genealogy/method-riksarkivet.md`. Run the
relevant validators and regression tests after changes. Preserve unrelated user
changes. Do not order archival material, publish or deploy, create a PDF, or
commit and push unless the user has authorized that action.
