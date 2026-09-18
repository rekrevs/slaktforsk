CREATE TABLE operation (
  id TEXT PRIMARY KEY, request_hash TEXT NOT NULL, actor TEXT NOT NULL,
  recorded_at TEXT NOT NULL, reason TEXT NOT NULL
) STRICT;
CREATE TABLE object (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL CHECK(kind IN ('person','source','record','transcription','mention','observation','identity','identity_resolution','place','event','participation','relation','fact','question','search','assessment','narrative'))
) STRICT;
CREATE TABLE revision (
  id TEXT PRIMARY KEY, object_id TEXT NOT NULL REFERENCES object(id),
  version INTEGER NOT NULL CHECK(version>0), operation_id TEXT NOT NULL REFERENCES operation(id),
  disposition TEXT NOT NULL CHECK(disposition IN ('recorded','accepted','candidate','rejected','retired')),
  evidence_status TEXT, rationale TEXT NOT NULL, caveat TEXT NOT NULL,
  previous_id TEXT REFERENCES revision(id), UNIQUE(object_id,version)
) STRICT;
CREATE TABLE origin (
  revision_id TEXT NOT NULL REFERENCES revision(id), unit_id TEXT NOT NULL REFERENCES unit(id),
  coverage TEXT NOT NULL CHECK(coverage IN ('partial','complete','context')),
  note TEXT NOT NULL, PRIMARY KEY(revision_id,unit_id)
) STRICT;
CREATE TABLE dependency (
  revision_id TEXT NOT NULL REFERENCES revision(id), basis_revision_id TEXT NOT NULL REFERENCES revision(id),
  role TEXT NOT NULL CHECK(role IN ('supports','contradicts','context','derived_from')),
  note TEXT NOT NULL, PRIMARY KEY(revision_id,basis_revision_id,role),
  CHECK(revision_id!=basis_revision_id)
) STRICT;
CREATE TABLE review_request (
  id TEXT PRIMARY KEY, operation_id TEXT NOT NULL REFERENCES operation(id),
  affected_revision_id TEXT NOT NULL REFERENCES revision(id),
  changed_revision_id TEXT NOT NULL REFERENCES revision(id), reason TEXT NOT NULL
) STRICT;
CREATE TABLE review_resolution (
  request_id TEXT PRIMARY KEY REFERENCES review_request(id),
  operation_id TEXT NOT NULL REFERENCES operation(id), rationale TEXT NOT NULL
) STRICT;
CREATE TABLE person (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), display_name TEXT NOT NULL,
  sex TEXT CHECK(sex IN ('female','male','unknown') OR sex IS NULL),
  legacy_state TEXT CHECK(legacy_state IN ('active','retired') OR legacy_state IS NULL)
) STRICT;
CREATE TABLE source (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), title TEXT NOT NULL,
  archive_reference TEXT, source_class TEXT, description TEXT NOT NULL
) STRICT;
CREATE TABLE record (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), source_id TEXT NOT NULL REFERENCES object(id),
  record_type TEXT NOT NULL, locator TEXT NOT NULL, dependence_note TEXT NOT NULL
) STRICT;
CREATE TABLE record_asset (
  revision_id TEXT NOT NULL REFERENCES record(revision_id), asset_path TEXT NOT NULL REFERENCES asset(path),
  region TEXT NOT NULL, PRIMARY KEY(revision_id,asset_path)
) STRICT;
CREATE TABLE transcription (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), record_id TEXT NOT NULL REFERENCES object(id),
  text TEXT NOT NULL, reading_note TEXT NOT NULL
) STRICT;
CREATE TABLE mention (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), record_id TEXT NOT NULL REFERENCES object(id),
  name_literal TEXT NOT NULL, role_literal TEXT NOT NULL
) STRICT;
CREATE TABLE observation (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), record_id TEXT NOT NULL REFERENCES object(id),
  mention_id TEXT REFERENCES object(id), property TEXT NOT NULL, value_literal TEXT NOT NULL,
  value_json TEXT CHECK(value_json IS NULL OR json_valid(value_json))
) STRICT;
CREATE TABLE identity (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), mention_id TEXT NOT NULL REFERENCES object(id),
  person_id TEXT NOT NULL REFERENCES object(id), decision TEXT NOT NULL CHECK(decision IN ('accepted','candidate','rejected'))
) STRICT;
CREATE TABLE identity_resolution (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), person_a TEXT NOT NULL REFERENCES object(id),
  person_b TEXT NOT NULL REFERENCES object(id), decision TEXT NOT NULL CHECK(decision IN ('same_person','different_people','unresolved')),
  CHECK(person_a!=person_b)
) STRICT;
CREATE TABLE place (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), name TEXT NOT NULL,
  jurisdiction TEXT NOT NULL, parent_id TEXT REFERENCES object(id)
) STRICT;
CREATE TABLE event (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), event_type TEXT NOT NULL,
  date_json TEXT NOT NULL CHECK(json_valid(date_json)), place_id TEXT REFERENCES object(id),
  place_role TEXT NOT NULL
) STRICT;
CREATE TABLE participation (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), event_id TEXT NOT NULL REFERENCES object(id),
  person_id TEXT REFERENCES object(id), mention_id TEXT REFERENCES object(id), role TEXT NOT NULL,
  CHECK(person_id IS NOT NULL OR mention_id IS NOT NULL)
) STRICT;
CREATE TABLE relation (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), from_person TEXT NOT NULL REFERENCES object(id),
  to_person TEXT NOT NULL REFERENCES object(id), relation_type TEXT NOT NULL,
  nature TEXT NOT NULL, date_json TEXT NOT NULL CHECK(json_valid(date_json)),
  CHECK(from_person!=to_person)
) STRICT;
CREATE TABLE fact (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), subject_id TEXT NOT NULL REFERENCES object(id),
  property TEXT NOT NULL, value_type TEXT NOT NULL CHECK(value_type IN ('text','number','date','entity','boolean','structured')),
  value_json TEXT NOT NULL CHECK(json_valid(value_json))
) STRICT;
CREATE TABLE question (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), subject_id TEXT NOT NULL REFERENCES object(id),
  title TEXT NOT NULL, outcome TEXT NOT NULL, body TEXT NOT NULL
) STRICT;
CREATE TABLE search (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), question_id TEXT REFERENCES object(id),
  source_id TEXT NOT NULL REFERENCES object(id), scope_json TEXT NOT NULL CHECK(json_valid(scope_json)),
  outcome TEXT NOT NULL CHECK(outcome IN ('negative','positive','access_problem','inconclusive')),
  body TEXT NOT NULL
) STRICT;
CREATE TABLE assessment (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), subject_id TEXT NOT NULL REFERENCES object(id),
  criteria TEXT NOT NULL, outcome TEXT NOT NULL, body TEXT NOT NULL
) STRICT;
CREATE TABLE narrative (
  revision_id TEXT PRIMARY KEY REFERENCES revision(id), subject_id TEXT NOT NULL REFERENCES object(id),
  title TEXT NOT NULL, markdown TEXT NOT NULL
) STRICT;
CREATE INDEX revision_object ON revision(object_id,version);
CREATE INDEX dependency_basis ON dependency(basis_revision_id);
CREATE INDEX origin_unit ON origin(unit_id);
CREATE VIEW current_revision AS
  SELECT r.*,o.kind FROM revision r JOIN object o ON o.id=r.object_id
  WHERE NOT EXISTS(SELECT 1 FROM revision newer WHERE newer.object_id=r.object_id AND newer.version>r.version);
CREATE VIEW pending_review AS
  SELECT q.* FROM review_request q WHERE NOT EXISTS(SELECT 1 FROM review_resolution s WHERE s.request_id=q.id);
CREATE VIEW current_relation AS
  SELECT r.object_id,r.version,r.disposition,r.evidence_status,r.caveat,p.*
  FROM current_revision r JOIN relation p ON p.revision_id=r.id;
CREATE VIEW current_participation AS
  SELECT r.object_id,r.version,r.disposition,r.evidence_status,r.caveat,p.*
  FROM current_revision r JOIN participation p ON p.revision_id=r.id;
