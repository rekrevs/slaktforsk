// Avvecklade personakter (PCD-2026-09-11-034). Registret är den enda källan;
// markeringen i akt och profil kontrolleras mot det.

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

export const RETIRED_MARKER = "AVVECKLAD AKT";

export function loadRetired(root) {
  const file = join(root, "genealogy", "avvecklade-akter.json");
  if (!existsSync(file)) return new Map();
  return new Map(Object.entries(JSON.parse(readFileSync(file, "utf8")).akter ?? {}));
}
