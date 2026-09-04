# Repository instructions

Read the project's durable context before doing work:

1. `README.md` and `HANDOVER.md` for orientation and current state.
2. `NORTH-STAR.md` for the permanent objective and quality contract.
3. `genealogy/README.md` for the evidence and knowledge model.
4. `genealogy/research-plan.md`, `genealogy/frontier.md` and
   `genealogy/source-coverage.md` for workflow and current research gates.
5. `PROJECT-CONTROL.md` for approved owner decisions and exceptions.
6. `wotan/backlog.json` and the active `wotan/dev-log/` record for task work.

Use Wotan for task or backlog work and Project Control for strategic steering.
Do not start research outside the active, approved Wotan task. Within that
scope, prefer the nearest incompletely quality-reviewed generation or cohort
before deeper or already well-documented branches.

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

Follow the repository's provenance and Riksarkivet access rules. Run the
relevant validators and regression tests after changes. Preserve unrelated user
changes. Do not order archival material, publish or deploy, create a PDF, or
commit and push unless the user has authorized that action.
