// Relationsparser shared by the ancestry audit and its regression tests.

const GRANDPARENT_WORD = /\b(morfar|mormor|farfar|farmor)\b/i;
const PARENT_WORD = /\b(far|fader|mor|moder)\b/i;
const CHILD_WORD = /\b(son|dotter|barn)\b/i;
const EXCLUDE = /styv|husbonde|uppgiven|tidigare antagen|sannolik|möjlig|ej belagt/i;

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

    for (const row of body.matchAll(/^\|\s*\[[^\]]+\]\((P-\d{4})[^)]*\)\s*\|\s*([^|]+)\|/gm)) {
      const [, target, rawRelation] = row;
      const relation = rawRelation.trim();
      if (EXCLUDE.test(relation) || GRANDPARENT_WORD.test(relation)) continue;
      if (PARENT_WORD.test(relation)) link(id, target);
      else if (CHILD_WORD.test(relation)) link(target, id);
    }

    for (const prose of body.matchAll(proseBlock("Föräldrar|Fader|Moder|Far|Mor"))) {
      for (const [, target] of prose[2].matchAll(/\((P-\d{4})/g)) link(id, target);
    }
    for (const prose of body.matchAll(proseBlock("Barn|Söner|Döttrar|Son|Dotter"))) {
      for (const [, target] of prose[2].matchAll(/\((P-\d{4})/g)) link(target, id);
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
