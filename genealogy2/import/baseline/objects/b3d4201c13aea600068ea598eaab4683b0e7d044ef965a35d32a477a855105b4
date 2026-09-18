// Relationsparser shared by the ancestry audit and its regression tests.

const GRANDPARENT_WORD = /\b(morfar|mormor|farfar|farmor)\b/i;
// Relationskolumnen anger den länkade personens roll mot aktens person, och
// rollen står i cellens huvudled - före första tankstreck, semikolon, komma
// eller parentes. Släktord längre in beskriver någon annan: `Arnes far`,
// `sonens mor`, `halvbror - moderns son`, `svägerska; mor till dopbarnen`.
const PARENT_HEAD = /^(?:biologisk[ae]?\s+)?(?:far|fader|mor|moder)\b/i;
const CHILD_HEAD = /^(?:(?:gemensamm?a?|äldst[ae]?|yngst[ae]?|äldre|yngre|enda|ende|förste|första|andre|andra|tredje|oäkta|egen|eget|egna)\s+)*(?:son|dotter|barn)\b/i;
const relationHead = (relation) => relation.replace(/[*`_]/g, "").trim().split(/\s*[—–;,(]\s*/)[0].trim();
const EXCLUDE = /styv|husbonde|uppgiven|tidigare antagen|sannolik|möjlig|ej belagt|(?:inte|ej)(?: separat)? (?:belag[dt]|originalbelagd|säkra[dt]|säker|avgjor[dt]|prövad|prövat)|obelag[dt]|(?<![a-zåäö])öppe[nt](?![a-zåäö])/i;
const NON_PROPAGATING_STATUS = new Set(["LEAD", "CONFLICT", "REJECTED", "UNKNOWN"]);

// A prose label ends the preceding relationship block. JavaScript's `\w`
// does not include Swedish letters, so keep the supported alphabet explicit.
const LABEL = String.raw`[A-Za-zÅÄÖåäö][A-Za-zÅÄÖåäö0-9]*(?:\s+[A-Za-zÅÄÖåäö0-9]+)*\s*:`;
const proseBlock = (labels) =>
  new RegExp(String.raw`(${labels})\s*:\s*([^\n]*(?:\n(?!${LABEL})[^\n]*)*)`, "g");

export function buildParentMap(people) {
  const parents = new Map([...people.keys()].map((id) => [id, new Set()]));
  const link = (child, parent) => {
    if (people.has(child) && people.has(parent) && child !== parent) {
      parents.get(child).add(parent);
    }
  };

  for (const [id, person] of people) {
    const section = person.text.split("## Relationer")[1];
    if (!section) continue;
    const body = section.split(/\n## /)[0];

    for (const row of body.matchAll(/^\|\s*\[[^\]]+\]\((P-\d{4})[^)]*\)\s*\|\s*([^|]+)\|([^\n]*)$/gm)) {
      const [, target, rawRelation, remainingCells] = row;
      const relation = rawRelation.trim();
      const status = remainingCells
        .split("|")
        .map((cell) => cell.trim().toUpperCase())
        .find((cell) => NON_PROPAGATING_STATUS.has(cell));
      if (status) continue;
      if (EXCLUDE.test(relation) || GRANDPARENT_WORD.test(relation)) continue;
      const head = relationHead(relation);
      if (PARENT_HEAD.test(head)) link(id, target);
      else if (CHILD_HEAD.test(head)) link(target, id);
    }

    // Prosablock läses bara utanför tabeller. Ett kolon inne i en cell, som
    // `Barn:` i en syskonrad, får annars mönstret att starta mitt i tabellen
    // och svälja nästa rad som om den vore en uppräkning av barn.
    const prose = body.split("\n").filter((line) => !line.trimStart().startsWith("|")).join("\n");
    for (const block of prose.matchAll(proseBlock("Föräldrar|Fader|Moder|Far|Mor"))) {
      for (const [, target] of block[2].matchAll(/\((P-\d{4})/g)) link(id, target);
    }
    for (const block of prose.matchAll(proseBlock("Barn|Söner|Döttrar|Son|Dotter"))) {
      for (const [, target] of block[2].matchAll(/\((P-\d{4})/g)) link(target, id);
    }
  }

  return parents;
}

export function deriveDepths(parents, proband) {
  const depth = new Map([[proband, 0]]);
  const queue = [proband];
  while (queue.length) {
    const current = queue.shift();
    for (const parent of parents.get(current) ?? []) {
      if (!depth.has(parent)) {
        depth.set(parent, depth.get(current) + 1);
        queue.push(parent);
      }
    }
  }
  return depth;
}
