-- A discarded candidate dossier is an import alias, not a second real person.
CREATE TABLE legacy_mapping (
  id TEXT PRIMARY KEY, legacy_kind TEXT NOT NULL, legacy_id TEXT NOT NULL,
  target_id TEXT NOT NULL REFERENCES object(id), operation_id TEXT NOT NULL REFERENCES operation(id),
  mapping_type TEXT NOT NULL CHECK(mapping_type IN ('same_identity','rejected_identity','archival_reference')),
  origin_unit_id TEXT NOT NULL REFERENCES unit(id), rationale TEXT NOT NULL,
  FOREIGN KEY(legacy_kind,legacy_id) REFERENCES legacy_entity(kind,id),
  UNIQUE(legacy_kind,legacy_id,target_id,mapping_type)
) STRICT;
