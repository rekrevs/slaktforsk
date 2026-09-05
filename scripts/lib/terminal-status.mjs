// Slutstatus-parser shared by the ancestry audit and the goal-state measure.
//
// Varje front-person (en ana med färre än två kända föräldrar) måste bära
// exakt en slutstatus i avsnittet `## Slutstatus`, förväntad källa,
// genomsökt omfång, återaktivering och en giltig C-referens. VERIFIERAD
// använder Belägg; övriga statusar använder Negativ kontroll. Detta är en
// strukturkontroll, inte ett bevis för beläggens sakliga tillräcklighet.

export const TERMINAL_STATUSES = new Set([
  "VERIFIERAD",
  "IDENTITET OLÖST",
  "ÅTKOMSTSPÄRR",
  "EJ DIGITALISERAD",
  "ARKIVLUCKA",
  "KÄLLOR SLUT",
]);

function sectionBody(text, heading) {
  return text.split(new RegExp(`^## ${heading}[ \\t]*$`, "m"))[1]?.split(/^## /m)[0];
}

// Only indented continuation lines belong to a field. In particular, an
// empty value must not consume the next bullet through a whitespace match.
function field(body, label) {
  return body.match(new RegExp(`^- ${label}:[ \\t]*(.*(?:\\n[ \\t]+[^\\n]*)*)`, "m"))?.[1]?.trim() ?? "";
}

export function readTerminalStatus(text, citationExists) {
  const section = sectionBody(text, "Slutstatus");
  if (!section) return { ok: false, why: "saknar avsnittet ## Slutstatus" };
  const body = section;

  const status = body.match(/^-\s*Status:\s*`([^`]+)`/m)?.[1]?.trim();
  if (!status) return { ok: false, why: "ingen Status-rad" };
  if (!TERMINAL_STATUSES.has(status)) return { ok: false, why: `okänd status ${status}` };
  if ([...body.matchAll(/^-\s*Status:/gm)].length !== 1) {
    return { ok: false, status, why: "kräver exakt en Status-rad" };
  }

  const missing = [];
  if (!field(body, "Förväntad källa")) missing.push("förväntad källa");
  if (!field(body, "Genomsökt")) missing.push("genomsökt");
  if (!field(body, "Återaktivera när")) missing.push("återaktiveringsvillkor");

  const evidenceField = status === "VERIFIERAD" ? "Belägg" : "Negativ kontroll";
  const controls = [...field(body, evidenceField).matchAll(/\((?:\.\.\/citations\/)?(C-\d{4})[^)]*\)/g)]
    .map((m) => m[1]);
  const resolved = controls.filter((cid) => citationExists(cid));
  if (!resolved.length) missing.push(`${evidenceField.toLowerCase()} med giltig C-referens`);

  return missing.length
    ? { ok: false, status, why: `saknar ${missing.join(", ")}` }
    : { ok: true, status };
}

// `## Arbetsläge` bär personaktens konsolideringsläge. Saknat avsnitt betyder
// EJ GRANSKAD. Källbredd-fältet används bara när matrisen saknar rad.
export function readWorkState(text) {
  const section = sectionBody(text, "Arbetsläge");
  const result = { reviewed: false, reviewedOn: null, reviewRef: null, coverageOverride: null, coverageJustification: null };
  if (!section) return result;
  const body = section.split(/\n## /)[0];
  const cons = body.match(/^-\s*Konsolidering:\s*`([^`]+)`\s*(\d{4}-\d{2}-\d{2})?\s*(?:\(([^)]*)\))?/m);
  if (cons && cons[1].trim() === "GRANSKAD") {
    result.reviewed = true;
    result.reviewedOn = cons[2] ?? null;
    result.reviewRef = cons[3] ?? null;
  }
  const cov = field(body, "Källbredd").match(/^`([^`]+)`([\s\S]*)$/);
  if (cov) {
    result.coverageOverride = cov[1].trim();
    result.coverageJustification = cov[2].replace(/^\s*\d{4}-\d{2}-\d{2}[.\s]*/, "").trim() || null;
  }
  return result;
}
