-- A compound legacy unit can represent several independently revisable objects.
-- Older single-target decisions remain unchanged and visible through the view.
CREATE TABLE unit_decision_target (
  decision_id TEXT NOT NULL REFERENCES unit_decision(id),
  target_id TEXT NOT NULL REFERENCES object(id),
  PRIMARY KEY(decision_id,target_id)
) STRICT;
CREATE VIEW current_unit_target AS
  SELECT d.unit_id,d.id AS decision_id,d.target_id FROM current_unit_decision d WHERE d.target_id IS NOT NULL
  UNION
  SELECT d.unit_id,d.id AS decision_id,t.target_id FROM current_unit_decision d
  JOIN unit_decision_target t ON t.decision_id=d.id;
