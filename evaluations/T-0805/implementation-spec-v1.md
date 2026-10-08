# T-0805 settled implementation specification v1

Owner-authorized bounded read-only node view and global future negative-search standard. No canonical research apply, no new archive/catalogue access, no dashboard, no migration or deletion of task history. Main467 must remain byte-identical.

## Node view

Add read-only CLI `work <P-id>`, JSON and Markdown (default Markdown), using current personView and identityGate and sole Wotan backlog. New pure module exports can support tests. A versioned `wotan/node-links.json` holds ONLY association/navigation metadata, not work status/priority/checkpoints or a second queue. Explicit pilot scope P-0240/P-0241/P-0246; outside pilot fail clearly or label unmapped (never claim no outstanding work).

Exactly six route links:
- T0803-R1 -> T-0803, P-0240, P-0240/Q-02 and PATH-P-0240-KP-02; childhood1902–1930 metadata.
- T0803-R2 -> T-0803, P-0240, same question/path; nurse-training metadata.
- T0803-R3 -> T-0803, P-0240, P-0240/Q-03 and PATH-P-0240-KP-04; death1991/probate custody metadata.
- T0217-Emma-probate -> T-0217, P-0246, PATH-P-0246-KP-03; probate1963 routing.
- T0217-Axel-probate -> T-0217, P-0241, P-0241/Q-02 and PATH-P-0241-KP-03; probate1983 routing.
- T0217-Axel-military -> T-0217, P-0241, PATH-P-0241-KP-03; registration28965/21 routing.

Full scopes/stops remain in original devlogs; association summaries are not expanded authority. Shared task T-0217 must have identical task ID/status/scope link and combined people anchor when displayed at both people, never duplicated execution owners. View derives task status/priority/after eligibility from live backlog each time; no auto-start or approval. Validate mapping format, duplicate routes, known task/person/question/path IDs and exact association references. Do not derive links by text regex. No route DONE just because task READY or question supported. Display actual current question/path outcomes separately from execution state, and legacy free-text states as exact/qualified values. Display source/model refs and existing search receipts (positive/negative/access/inconclusive) with scope. Existing searches without new standard labelled legacy/unqualified, never fabricated completion. Read-only whole-model export/hash tests and CLI tests.

## Global search memory contract

For ALL NEW native negative searches through writeOperation/CLI require operation searchMemoryVersion:1 and scope_json.search_memory format search-memory/1. Annotate new native requests in writeOperation, preserve previous operation exact hash/flags on idempotent retries. Old unmarked operations replay with old semantics; no rewritten journal/schema migration. New native callers may not force older policy. applyOperation supports absent marker as historical/library compatibility, explicit marker1 enforces contract; reject unknown markers. Existing source revision changes must not make an unchanged operation retry fail.

Existing scope_json.description/query/bounds remain required; negative bounds must be nonempty. Additional search_memory fields:
- subjects: nonempty list of existing object IDs; question_id must be present and its subject_id included. Person-related search thus reaches the correct person; a source/relation question can bind its actual subject. No false person association by name match.
- performed_at: valid ISO timestamp with timezone.
- method: nonempty actual method description (manual pages/index/database queries, etc.).
- material: identifier (nonempty stable archive/catalogue/edition/item ID), source_version positive integer matching current source_id's version at actual apply; source_id/version must be present in search evidence as supports or context (explicit dependency, not an invented independent source).
- material.provider_version: {value:string|null,unknown_reason:string if null}. This is supplier version, not our source revision.
- material.snapshot: either {sha256:64hex,reference:nonempty string} or {sha256:null,unavailable_reason:nonempty string}. Do not manufacture hashes or claim unavailable copy saved. Can be captured index response/full page, never partial crop substituted as full source.
- coverage: {completed:true,limitations:nonempty string}. Describes completion of exact declared search, not whole source exhaustion. Explicit bounds/query must remain separately visible. Access failures belong outcome access_problem, not completed negative.
- reactivation: nonempty list of nonempty condition strings (new key, newly digitized/versioned content, overlooked segment, etc.).

Validator must prove actual object/reference/source version matching; validate field types/date/hash and useful rejection paths. A legacy search lacking this contract remains available with missing metadata stated; historical negative is not auto-upgraded. If redoing a search due to changed keys/material, preserve previous receipt and record changed exact scope/why, not overwrite old history. No automatic 'same hash -> same genealogy answer' rule.

## Validation

Meaningful targeted tests: unbounded/incomplete negative rejected atomically; mismatched source version and question subject rejected; known supplier/hash and explicit unknown version/copy alternatives accepted; access_problem not mislabelled negative; old unmarked requests/replay and idempotent native retries preserve exact hashes; explicit downgrade rejected; shared task current status and blockers update via sole backlog; outside pilot and missing refs explicit; read-only work CLI does not mutate DB/journal. Relevant complete genealogy2 test suite for write/replay changes. Keep implementation limitations explicit.

Root handles current normative documentation, owner decision, Wotan status and actual endpoints. Sol handles code/fixtures and fixed route mapping only; independent Astra checks specification/data/semantics/actual view consequence. No further delegation.
