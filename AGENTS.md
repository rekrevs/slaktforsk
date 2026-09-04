# Repository instructions

Read the project's durable context before doing work:

1. `README.md` and `HANDOVER.md` for orientation and current state.
2. `NORTH-STAR.md` for the permanent objective and quality contract.
3. `genealogy/README.md` for the evidence and knowledge model.
4. `genealogy/research-plan.md`, `genealogy/frontier.md` and
   `genealogy/source-coverage.md` for workflow and current research gates.
5. `PROJECT-CONTROL.md` for approved owner decisions and exceptions.
6. `wotan/README.md` for the repository's Wotan convention, then
   `wotan/backlog.json` and the active `wotan/dev-log/` record for task work.

Run `node scripts/goal-state.mjs` to see the project's state against the
north star; do not reconstruct it from handover prose or chat history.

Use Wotan for task or backlog work and Project Control for strategic steering.
Do not start research outside the active, approved Wotan task. Tasks are cut
from the goal-state next slice as described in `wotan/README.md`: the nearest
untreated generation, balanced between both sides, before deeper or already
well-documented branches. Log each research batch once, in
`genealogy/research-log/`.

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
