// Slutstatus-parser shared by the ancestry audit and the goal-state measure.
//
// Varje front-person (en ana med färre än två kända föräldrar) måste bära
// exakt en slutstatus i avsnittet `## Slutstatus`. Alla utom VERIFIERAD kräver
// dessutom förväntad källa, vad som genomsöktes och minst en bevarad negativ
// kontroll med giltig C-referens. Saknas någon del är statusen ogiltig och
// positionen räknas som osökt, inte stängd.

export const TERMINAL_STATUSES = new Set([
  "VERIFIERAD",
  "IDENTITET OLÖST",
  "ÅTKOMSTSPÄRR",
  "EJ DIGITALISERAD",
  "ARKIVLUCKA",
  "KÄLLOR SLUT",
]);

export function readTerminalStatus(text, citationExists) {
  const section = text.split("## Slutstatus")[1];
  if (!section) return { ok: false, why: "saknar avsnittet ## Slutstatus" };
  const body = section.split(/\n## /)[0];

  const status = body.match(/^-\s*Status:\s*`([^`]+)`/m)?.[1]?.trim();
  if (!status) return { ok: false, why: "ingen Status-rad" };
  if (!TERMINAL_STATUSES.has(status)) return { ok: false, why: `okänd status ${status}` };
  if (status === "VERIFIERAD") return { ok: true, status };

  const missing = [];
  if (!/^-\s*Förväntad källa:\s*\S/m.test(body)) missing.push("förväntad källa");
  if (!/^-\s*Genomsökt:\s*\S/m.test(body)) missing.push("genomsökt");

  const controls = [...body.matchAll(/^-\s*Negativ kontroll:.*$/gm)]
    .flatMap((line) => [...line[0].matchAll(/\((?:\.\.\/citations\/)?(C-\d{4})[^)]*\)/g)])
    .map((m) => m[1]);
  const resolved = controls.filter((cid) => citationExists(cid));
  if (!resolved.length) missing.push("negativ kontroll med giltig C-referens");

  return missing.length
    ? { ok: false, status, why: `saknar ${missing.join(", ")}` }
    : { ok: true, status };
}

// `## Arbetsläge` bär personaktens konsolideringsläge. Saknat avsnitt betyder
// EJ GRANSKAD. Ett valfritt Källbredd-fält kan ersätta matrisraden när
// personen är integritetsminimerad eller när matrisen saknar rad.
export function readWorkState(text) {
  const section = text.split("## Arbetsläge")[1];
  const result = { reviewed: false, reviewedOn: null, reviewRef: null, coverageOverride: null };
  if (!section) return result;
  const body = section.split(/\n## /)[0];
  const cons = body.match(/^-\s*Konsolidering:\s*`([^`]+)`\s*(\d{4}-\d{2}-\d{2})?\s*(?:\(([^)]*)\))?/m);
  if (cons && cons[1].trim() === "GRANSKAD") {
    result.reviewed = true;
    result.reviewedOn = cons[2] ?? null;
    result.reviewRef = cons[3] ?? null;
  }
  const cov = body.match(/^-\s*Källbredd:\s*`([^`]+)`/m);
  if (cov) result.coverageOverride = cov[1].trim();
  return result;
}
