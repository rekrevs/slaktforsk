#!/usr/bin/env node

import { existsSync } from "node:fs";
import { resolve } from "node:path";

const projectGenerator = resolve(import.meta.dirname, "..", "..", "scripts", "build-dashboard-data.mjs");
const snapshot = resolve(import.meta.dirname, "..", "public", "data", "project.json");

if (existsSync(projectGenerator)) {
  await import(projectGenerator);
} else if (existsSync(snapshot)) {
  console.log("Använder den versionssparade dashboarddatan");
} else {
  throw new Error("Dashboarddata saknas och projektets datagenerator är inte tillgänglig");
}
