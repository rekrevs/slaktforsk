-- Native media do not belong to the frozen legacy import batch.
CREATE TABLE native_asset (
  id TEXT PRIMARY KEY, storage_path TEXT NOT NULL, sha256 TEXT NOT NULL,
  bytes INTEGER NOT NULL CHECK(bytes>=0), original_name TEXT NOT NULL,
  provenance TEXT NOT NULL, operation_id TEXT NOT NULL REFERENCES operation(id)
) STRICT;
CREATE TABLE record_media (
  revision_id TEXT NOT NULL REFERENCES record(revision_id),
  asset_id TEXT NOT NULL REFERENCES native_asset(id), region TEXT NOT NULL,
  PRIMARY KEY(revision_id,asset_id)
) STRICT;
-- Exact accepted requests support a durable, reproducible recovery journal.
CREATE TABLE operation_payload (
  sequence INTEGER PRIMARY KEY, operation_id TEXT NOT NULL UNIQUE REFERENCES operation(id),
  policy TEXT NOT NULL CHECK(policy IN ('legacy/1','native/2')),
  request_json TEXT NOT NULL CHECK(json_valid(request_json))
) STRICT;
CREATE VIRTUAL TABLE object_search USING fts5(object_id UNINDEXED,kind UNINDEXED,text);
