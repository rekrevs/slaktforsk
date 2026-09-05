import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { assessProfile, dependencyCycles, validateWotan, checkLocalLink, THEMES, REQUIREMENTS } from "./research-inventory.mjs";

const template = readFileSync(new URL("../genealogy/templates/research-profile.md", import.meta.url), "utf8");
function partial() {
  return template.replaceAll("P-NNNN", "P-0001")
    .replace("- Källklass: K-id från källstrategin.", "- Källklass: K-10")
    .replace("- Wotan: länk till beslutat utförande eller EJ BESLUTAT UTFÖRANDE med skäl.", "- Wotan: T-0001");
}
function closed() {
  let text = partial().split("### Q-01:")[0] + "\n## Källvägar\n\nIntegritetsminimerad; inga ytterligare källpassager är motiverade.\n\n## Kontraktsgranskning\n";
  text = text.replace("- Identitetsläge: `EJ BEDÖMT`", "- Identitetsläge: `PRÖVAT`")
    .replace("- Livsbildsläge: `EJ BEDÖMT`", "- Livsbildsläge: `INTEGRITETSMINIMERAD`")
    .replace("- Källstrategiläge: `EJ BEDÖMT`", "- Källstrategiläge: `GENOMGÅNGEN`")
    .replace("- Kontraktsgranskning: `EJ GRANSKAD`", "- Kontraktsgranskning: `GODKÄND`")
    .replace("- Granskningsdatum: ej granskat", "- Granskningsdatum: 2026-09-05")
    .replace("- Granskningsbelägg: saknas", "- Granskningsbelägg: [granskning](review.md)")
    .replace(/^- Tidslinje: .+$/m, "- Tidslinje: [nödvändig livslinje](person.md#tidslinje)")
    .replace(/^- Livsberättelse: .+$/m, "- Livsberättelse: [minimerad berättelse](person.md#livsberättelse)");
  for (const id of THEMES) text = text.replace(`| ${id} | EJ BEDÖMT | Individuell genomgång återstår. | — |`, `| ${id} | INTEGRITETSMINIMERAT | Endast nödvändig relationsinformation för levande person. | [bedömning](review.md) |`);
  return text + REQUIREMENTS.map((id) => `| ${id} | STYRKT | Individuellt bedömt: [belägg](review.md). |`).join("\n");
}
const assess = (text, extra = {}) => assessProfile({ personId: "P-0001", text, ...extra });

test("legacy KLAR without a profile remains unassessed, never a new approval", () => {
  const result = assess(null);
  assert.equal(result.review, "EJ INFÖRT");
  assert.equal(result.recordedApproval, false);
  assert.equal(result.biography, "EJ BEDÖMT");
});

test("partial adoption can preserve uncertainty without declaring all research complete", () => {
  const result = assess(partial());
  assert.deepEqual(result.errors, []);
  assert.equal(result.recordedApproval, false);
  assert.equal(result.themes.SYN, "EJ BEDÖMT");
});

test("copying GODKÄND onto unassessed themes or a live question is rejected", () => {
  const result = assess(partial().replace("- Kontraktsgranskning: `EJ GRANSKAD`", "- Kontraktsgranskning: `GODKÄND`"));
  assert.equal(result.recordedApproval, false);
  assert.ok(result.errors.some((e) => e.includes("teman")));
  assert.ok(result.errors.some((e) => e.includes("öppen materiell fråga")));
});

test("privacy minimization can be structurally reviewed but needs every outcome and evidence link", () => {
  const valid = assess(closed());
  assert.deepEqual(valid.errors, []);
  assert.equal(valid.recordedApproval, true);
  const missing = assess(closed().replace(/^\| PK-09.+\n?/m, ""));
  assert.equal(missing.recordedApproval, false);
  assert.ok(missing.errors.some((e) => e.includes("PK-09")));
});

test("a terminal source constraint cannot erase an open biography theme", () => {
  const result = assess(closed().replace("| BO | INTEGRITETSMINIMERAT |", "| BO | ÖPPET |"));
  assert.equal(result.recordedApproval, false);
  assert.ok(result.errors.some((e) => e.includes("teman")));
});

test("duplicate current status and a nonexistent review date cannot approve a profile", () => {
  const duplicate = assess(closed() + "\n- Identitetsläge: `OMSTRITT`\n");
  assert.equal(duplicate.recordedApproval, false);
  assert.ok(duplicate.errors.some((e) => e.includes("Identitetsläge")));
  assert.ok(assess(closed().replace("2026-09-05", "2026-02-30")).errors.some((e) => e.includes("granskningsdatum")));
});

test("prose saying another path is not required must not create that dependency", () => {
  const result = assess(partial().replace("- Beroenden: saknad", "- Beroenden: kräver inte KP-01; saknad"));
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.dependencies["P-0001/KP-01"], []);
});

test("explicit missing or cyclic source keys fail, including cycles across people", () => {
  assert.ok(assess(partial().replace("Föregående källvägar: INGA", "Föregående källvägar: KP-99")).errors.some((e) => e.includes("okänt beroende")));
  assert.ok(assess(partial().replace("Föregående källvägar: INGA", "Föregående källvägar: KP-01")).errors.some((e) => e.includes("cirkulärt")));
  const cross = assess(partial().replace("Föregående källvägar: INGA", "Föregående källvägar: P-0002/KP-03"), { pathExists: (id) => id === "P-0002/KP-03" });
  assert.deepEqual(cross.errors, []);
  assert.deepEqual(cross.dependencies["P-0001/KP-01"], ["P-0002/KP-03"]);
  assert.equal(dependencyCycles({ "P-0001/KP-01": ["P-0002/KP-03"], "P-0002/KP-03": [] }).length, 0);
  assert.ok(dependencyCycles({ "P-0001/KP-01": ["P-0002/KP-03"], "P-0002/KP-03": ["P-0001/KP-01"] }).length > 0);
});

test("unknown question, source class or executable task reference is rejected", () => {
  assert.ok(assess(partial().replace("- Frågor/teman: Q-01", "- Frågor/teman: Q-99")).errors.some((e) => e.includes("okänd fråga")));
  assert.ok(assess(partial().replace("- Källklass: K-10", "- Källklass: K-99")).errors.some((e) => e.includes("källklass")));
  assert.ok(assess(partial(), { taskIds: new Set() }).errors.some((e) => e.includes("okänd Wotan")));
});

test("local evidence links check actual files and Swedish heading anchors", () => {
  const root = mkdtempSync(join(tmpdir(), "genealogy-contract-"));
  try {
    mkdirSync(join(root, "profiles"));
    const profile = join(root, "profiles/P-0001.md");
    writeFileSync(profile, "# Profil\n");
    writeFileSync(join(root, "person.md"), "## Livsberättelse\n\nBelagd text.\n");
    assert.equal(checkLocalLink(root, profile, "../person.md#livsberättelse"), null);
    assert.match(checkLocalLink(root, profile, "../person.md#tidslinje"), /saknat ankare/);
    assert.match(checkLocalLink(root, profile, "../saknas.md"), /bruten länk/);
  } finally { rmSync(root, { recursive: true }); }
});

test("an archive-blocked task does not block an independent ready task", () => {
  const backlog = { next_id: 3, tasks: [
    { id: "T-0001", status: "BLOCKED", blocker: "Inloggning; exakt sida sparad." },
    { id: "T-0002", status: "READY" },
  ] };
  assert.deepEqual(validateWotan(backlog), []);
  backlog.tasks[1].after = ["T-0001"];
  assert.ok(validateWotan(backlog).some((e) => e.includes("körbar trots ofärdigt")));
});

test("Wotan rejects lost dev-logs, duplicate active work and circular predecessors", () => {
  const tasks = [{ id: "T-0001", status: "ONGOING", after: ["T-0002"] }, { id: "T-0002", status: "ONGOING", after: ["T-0001"] }];
  const errors = validateWotan({ next_id: 2, tasks }, () => false);
  for (const expected of ["dev-log", "next_id", "cyklisk", "flera ONGOING"]) assert.ok(errors.some((e) => e.includes(expected)), expected);
});
