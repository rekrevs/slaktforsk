import assert from "node:assert/strict";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");

test("dashboardkontroller tillåter att kanonisk forskning går vidare utan uppdatering", () => {
  const fixture = mkdtempSync(join(tmpdir(), "slaktforsk-dashboard-"));
  try {
    for (const dir of ["scripts", "dashboard/public/data", "genealogy/people"]) {
      mkdirSync(join(fixture, dir), { recursive: true });
    }
    const script = join(fixture, "scripts/dashboard-data.test.mjs");
    const snapshot = join(fixture, "dashboard/public/data/project.json");
    copyFileSync(join(root, "scripts/dashboard-data.test.mjs"), script);
    copyFileSync(join(root, "dashboard/public/data/project.json"), snapshot);
    const before = readFileSync(snapshot);
    // Den kanoniska personmängden avviker avsiktligt från ögonblicksbilden.
    const check = (current) => spawnSync(process.execPath, [script], {
      encoding: "utf8",
      env: { ...process.env, GENEALOGY_DASHBOARD_CHECK_CURRENT: current },
    });
    const saved = check("0");
    assert.equal(saved.status, 0, saved.stderr || saved.stdout);
    const current = check("1");
    assert.notEqual(current.status, 0, "uttrycklig aktualitetskontroll ska upptäcka avvikelsen");
    assert.match(current.stderr, /personantalet ska följa personakterna/);
    assert.deepEqual(readFileSync(snapshot), before, "ingen kontroll får skriva om snapshoten");
  } finally {
    rmSync(fixture, { recursive: true, force: true });
  }
});

test("dashboardens vanliga npm-kommandon har ingen automatisk datauppdatering", () => {
  const { scripts } = JSON.parse(readFileSync(join(root, "dashboard/package.json"), "utf8"));
  assert.equal(scripts.data, "node scripts/refresh-data.mjs");
  for (const phase of ["dev", "build", "start", "test"]) {
    for (const name of [`pre${phase}`, phase, `post${phase}`]) {
      assert.doesNotMatch(scripts[name] ?? "", /npm\s+run\s+data|refresh-data|build-dashboard-data/);
    }
  }
  assert.equal(scripts.test, "node ../scripts/dashboard-data.test.mjs");
  assert.match(scripts["test:current"], /GENEALOGY_DASHBOARD_CHECK_CURRENT=1/);
});
