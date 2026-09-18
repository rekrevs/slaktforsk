-- Representation decisions for frozen import units are knowledge about the
-- conversion, never an execution queue. Wotan alone schedules the work.
CREATE TABLE unit_decision (
  id TEXT PRIMARY KEY, unit_id TEXT NOT NULL REFERENCES unit(id),
  version INTEGER NOT NULL CHECK(version>0), operation_id TEXT NOT NULL REFERENCES operation(id),
  state TEXT NOT NULL CHECK(state IN ('mapped_complete','preserved_text','pending_interpretation','preserved_history')),
  target_id TEXT REFERENCES object(id), rationale TEXT NOT NULL, question TEXT NOT NULL,
  previous_id TEXT REFERENCES unit_decision(id), UNIQUE(unit_id,version),
  CHECK(state!='mapped_complete' OR target_id IS NOT NULL),
  CHECK(state!='pending_interpretation' OR length(trim(question))>0)
) STRICT;
CREATE INDEX unit_decision_unit ON unit_decision(unit_id,version);
CREATE VIEW current_unit_decision AS SELECT d.* FROM unit_decision d
  WHERE NOT EXISTS(SELECT 1 FROM unit_decision newer WHERE newer.unit_id=d.unit_id AND newer.version>d.version);
