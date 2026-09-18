CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL) STRICT;
CREATE TABLE import_batch (
  id TEXT PRIMARY KEY, manifest_json TEXT NOT NULL CHECK(json_valid(manifest_json)),
  extractor TEXT NOT NULL
) STRICT;
CREATE TABLE document (
  path TEXT PRIMARY KEY, batch_id TEXT NOT NULL REFERENCES import_batch(id),
  sha256 TEXT NOT NULL, bytes INTEGER NOT NULL, text TEXT NOT NULL,
  frozen INTEGER NOT NULL CHECK(frozen IN (0,1))
) STRICT;
CREATE TABLE asset (
  path TEXT PRIMARY KEY, batch_id TEXT NOT NULL REFERENCES import_batch(id),
  sha256 TEXT NOT NULL, bytes INTEGER NOT NULL, frozen INTEGER NOT NULL CHECK(frozen IN (0,1))
) STRICT;
CREATE TABLE legacy_entity (
  id TEXT NOT NULL, kind TEXT NOT NULL CHECK(kind IN ('person','source','citation','profile')),
  document_path TEXT NOT NULL UNIQUE REFERENCES document(path), title TEXT NOT NULL,
  PRIMARY KEY(kind,id)
) STRICT;
CREATE TABLE unit (
  id TEXT PRIMARY KEY, document_path TEXT NOT NULL REFERENCES document(path),
  kind TEXT NOT NULL, legacy_id TEXT, owner_id TEXT, section TEXT NOT NULL,
  start_byte INTEGER NOT NULL, end_byte INTEGER NOT NULL,
  start_line INTEGER NOT NULL, end_line INTEGER NOT NULL,
  raw TEXT NOT NULL, parsed_json TEXT NOT NULL CHECK(json_valid(parsed_json)),
  historical INTEGER NOT NULL CHECK(historical IN (0,1)),
  CHECK(start_byte >= 0 AND end_byte > start_byte)
) STRICT;
CREATE INDEX unit_owner ON unit(owner_id,kind);
CREATE INDEX unit_document ON unit(document_path);
CREATE INDEX unit_legacy ON unit(legacy_id);
CREATE TABLE legacy_assertion (
  id TEXT PRIMARY KEY, unit_id TEXT NOT NULL UNIQUE REFERENCES unit(id),
  owner_id TEXT NOT NULL, status_raw TEXT, reliability_raw TEXT
) STRICT;
CREATE VIRTUAL TABLE document_search USING fts5(path UNINDEXED,text, tokenize='unicode61 remove_diacritics 2');
