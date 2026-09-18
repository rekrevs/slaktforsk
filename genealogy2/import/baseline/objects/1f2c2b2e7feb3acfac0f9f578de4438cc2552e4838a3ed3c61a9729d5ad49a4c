#!/usr/bin/env node
// Släktledsraden under aktens namn (T-0635, PCD-2026-09-11-033).
//
// Raden räknas ur föräldrakartan i lib/genealogy-relations.mjs och skrivs
// aldrig för hand. `--write` för in den, `--check` rapporterar saknade eller
// inaktuella rader, och validate-genealogy.mjs kör kontrollen.
//
// Etiketten följer ägarens konvention: stegen från Adam och Axel paras två och
// två till farfar/farmor/morfar/mormor, och ett udda sista steg blir far/mor.
// Längre vägar upprepar parorden - `mormors mormors mor` - i stället för att
// bygga längre sammansättningar.

import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { buildParentMap } from "./lib/genealogy-relations.mjs";
import { loadRetired } from "./lib/retired.mjs";

const ROOT = resolve(import.meta.dirname, "..");
export const SONS = ["P-0269", "P-0270"];
const SON_NAMES = { "P-0269": "Adam", "P-0270": "Axel" };
const PAIR = { ff: "farfar", fm: "farmor", mf: "morfar", mm: "mormor" };
const ONE = { f: "far", m: "mor" };
const WIDTH = 78;

export function kinTerm(path) {
  const words = [];
  for (let i = 0; i < path.length; i += 2) {
    words.push(i + 1 < path.length ? PAIR[path.slice(i, i + 2)] : ONE[path[i]]);
  }
  return words.map((word, i) => (i < words.length - 1 ? `${word}s` : word)).join(" ");
}

export function loadPeople(root = ROOT) {
  const dir = join(root, "genealogy", "people");
  const people = new Map();
  for (const file of readdirSync(dir).sort()) {
    const match = file.match(/^(P-\d{4})-.*\.md$/);
    if (!match) continue;
    const text = readFileSync(join(dir, file), "utf8");
    people.set(match[1], { file, text, name: text.match(/^# P-\d{4}: (.+)$/m)?.[1] ?? match[1] });
  }
  return people;
}

// Kolumnen `Relation` anger den länkade personens roll mot aktens person, och
// rollen står i cellens huvudled. Könet läses därför ur huvudledet i alla rader
// som pekar på personen.
// `uppgiven far` anger källans fadersuppgift; könet är inte osäkert. Ett huvudled
// med `till` beskriver en roll mot en tredje person och räknas inte.
const MALE = /^(?:biologisk[ae]?\s+|uppgiven\s+)?(?:far|fader|son|bror|helbror|halvbror|make|man)\b/i;
const FEMALE = /^(?:biologisk[ae]?\s+|uppgiven\s+)?(?:mor|moder|dotter|syster|helsyster|halvsyster|hustru|maka)(?![a-zåäö])/i;
const head = (relation) => relation.replace(/[*`_]/g, "").trim().split(/\s*[—–;,(]\s*/)[0].trim();

export function inferSexes(people) {
  const votes = new Map();
  for (const person of people.values()) {
    const section = (person.text.split("## Relationer")[1] ?? "").split(/\n## /)[0];
    for (const row of section.matchAll(/^\|\s*\[[^\]]+\]\((P-\d{4})[^)]*\)\s*\|\s*([^|]+)\|/gm)) {
      const [, target, relation] = row;
      const h = head(relation);
      if (/\btill\b/i.test(h)) continue;
      const sex = MALE.test(h) ? "m" : FEMALE.test(h) ? "f" : null;
      if (!sex) continue;
      const v = votes.get(target) ?? { m: 0, f: 0 };
      v[sex] += 1;
      votes.set(target, v);
    }
  }
  const sexes = new Map();
  for (const [id, v] of votes) sexes.set(id, v.m && v.f ? "?" : v.m ? "m" : "f");
  return sexes;
}

// Alla vägar från Adam; Axel är hans helbror och delar varje ana.
export function ancestorPaths(parents, sexes, from = SONS[0]) {
  const paths = new Map();
  const walk = (id, steps, via) => {
    for (const parent of parents.get(id) ?? []) {
      const sex = sexes.get(parent);
      const step = sex === "m" ? "f" : sex === "f" ? "m" : "?";
      const entry = { steps: steps + step, via: [...via, parent] };
      paths.set(parent, [...(paths.get(parent) ?? []), entry]);
      walk(parent, entry.steps, entry.via);
    }
  };
  walk(from, "", []);
  return paths;
}

// Länkar bryts aldrig; en rad med en lång länk får bli längre än WIDTH.
function wrap(text) {
  const lines = [];
  let line = "";
  for (const word of text.match(/\[[^\]]*\]\([^)]*\)\S*|\S+/g)) {
    if (line && line.length + 1 + word.length > WIDTH) {
      lines.push(line);
      line = word;
    } else line = line ? `${line} ${word}` : word;
  }
  if (line) lines.push(line);
  return lines.join("\n");
}

const link = (people, id, label = people.get(id).name) => `[${label}](${people.get(id).file})`;
const sons = (people) => `${link(people, SONS[0], SON_NAMES[SONS[0]])} och ${link(people, SONS[1], SON_NAMES[SONS[1]])}`;

export function ancestorBlock(people, id, entries) {
  if (entries.some((e) => e.steps.includes("?"))) return { error: `${id}: kön saknas för ett led i vägen` };
  const terms = [...new Set(entries.map((e) => kinTerm(e.steps)))];
  const generations = [...new Set(entries.map((e) => e.steps.length))].sort((a, b) => a - b);
  let text = `**Släktled:** ${terms.join(" och ")} till ${sons(people)}, generation ${generations.join(" och ")}.`;
  const routes = entries
    .filter((e) => e.via.length > 1)
    .map((e) => {
      const pronoun = e.steps.at(-1) === "f" ? "han" : "hon";
      return [...e.via.slice(0, -1).map((v) => link(people, v)), pronoun].join(" → ");
    });
  if (routes.length === 1) text += ` Vägen: ${routes[0]}.`;
  else if (routes.length > 1) text += ` Vägarna: ${routes.join("; ")}.`;
  return { text: wrap(text) };
}

export function sonBlock(people, id) {
  const other = SONS.find((s) => s !== id);
  return { text: wrap(`**Släktled:** ${SON_NAMES[id]} själv, bror till ${link(people, other, SON_NAMES[other])}. Generationerna räknas från dem båda.`) };
}

export function computeBlocks(root = ROOT) {
  const people = loadPeople(root);
  const parents = buildParentMap(people);
  const sexes = inferSexes(people);
  const [adam, axel] = SONS;
  const same = (a, b) => JSON.stringify([...(parents.get(a) ?? [])].sort()) === JSON.stringify([...(parents.get(b) ?? [])].sort());
  const errors = same(adam, axel) ? [] : ["Adam och Axel har olika föräldrar i föräldrakartan"];
  const blocks = new Map();
  for (const id of SONS) blocks.set(id, sonBlock(people, id));
  const anchorPhrases = new Map();
  const paths = ancestorPaths(parents, sexes);
  for (const [id, entries] of paths) {
    const block = ancestorBlock(people, id, entries);
    if (block.error) errors.push(block.error);
    else {
      blocks.set(id, block);
      if (entries.length === 1) anchorPhrases.set(id, kinTerm(entries[0].steps));
    }
  }
  const overrides = loadOverrides(root);
  const retired = loadRetired(root);
  const side = sideBlocks(people, sexes, anchorPhrases, overrides, { paths, parents });
  for (const [id, block] of side.blocks) if (!blocks.has(id) && !SONS.includes(id)) blocks.set(id, block);
  for (const [id, entry] of retired) {
    if (!people.has(id)) { errors.push(`avvecklade-akter.json: okänd person ${id}`); continue; }
    if (anchorPhrases.has(id)) errors.push(`avvecklade-akter.json: ${id} är en ana och kan inte avvecklas`);
    for (const [, ref] of entry.text.matchAll(/\[\[(P-\d{4})/g)) if (!people.has(ref)) errors.push(`avvecklade-akter.json: ${id} hänvisar till okänd person ${ref}`);
    if (!people.has(entry.motsvarighet) || retired.has(entry.motsvarighet)) errors.push(`avvecklade-akter.json: ${id} saknar en aktiv motsvarighet`);
    blocks.set(id, retiredBlock(people, side.phrases, entry));
  }
  for (const [id, o] of Object.entries(overrides)) {
    if (!people.has(id)) errors.push(`kinship-roles.json: okänd person ${id}`);
    if (!people.has(o.ankare)) errors.push(`kinship-roles.json: ${id} har okänt ankare ${o.ankare}`);
    else if (o.slag === "roll" && !blocks.has(o.ankare)) errors.push(`kinship-roles.json: ${id} kräver ett ankare med släktled`);
  }
  return { people, blocks, errors, readings: side.readings };
}

// Lästa tolkningar för sidopersoner vars roll inte går att härleda ur raderna.
function loadOverrides(root) {
  try {
    return JSON.parse(readFileSync(join(root, "genealogy", "kinship-roles.json"), "utf8")).roles ?? {};
  } catch (error) {
    if (error.code === "ENOENT") return {};
    throw error;
  }
}

// --- Sidopersoner (T-0636) ---------------------------------------------------
//
// En sidoperson knyts till en ana genom en roll. Rollen hämtas i första hand ur
// anans egen relationsrad, som enligt kolumnkonventionen anger den länkade
// personens roll mot anan. Står relationen bara i sidopersonens egen rad vänds
// den. Vittnesrader är undantaget: där beskriver cellen vittnet självt.
// Blodsläkt får en kompakt etikett (`farfars farfars syster`); andra roller och
// osäkra relationer behåller rollordet (`hustru till …`, `obekräftad far till …`).

const KIN = new Set(["son", "dotter", "barn", "bror", "syster", "syskon", "helbror", "helsyster", "halvbror", "halvsyster", "halvsyskon", "tvillingbror", "tvillingsyster", "sonson", "sondotter", "dotterson", "dotterdotter", "sonbarn", "dotterbarn", "barnbarn", "brorson", "brorsdotter", "brorsbarn", "systerson", "systerdotter", "systerbarn", "kusin", "farbror", "faster", "morbror", "moster", "halvfaster"]);
const REL = new Set(["far", "mor", "förälder", "hustru", "make", "make eller hustru", "styvmor", "styvfar", "styvson", "styvdotter", "styvbarn", "fosterfar", "fostermor", "fosterförälder", "fosterson", "fosterdotter", "fosterbarn", "svåger", "svägerska", "svärmor", "svärfar", "svärson", "svärdotter", "svärbarn", "måg", "husbonde", "matmor", "tjänstehjon", "hushållsmedlem"]);
const NEUTER = new Set(["barn", "syskon", "halvsyskon", "sonbarn", "dotterbarn", "barnbarn", "brorsbarn", "systerbarn", "styvbarn", "fosterbarn", "svärbarn", "tjänstehjon"]);
const HOS = new Set(["tjänstehjon", "hushållsmedlem"]);
const CLOSE = new Set(["son", "dotter", "barn", "bror", "syster", "syskon", "helbror", "helsyster", "halvbror", "halvsyster", "halvsyskon", "tvillingbror", "tvillingsyster"]);
const ADJ = /^(?:(?:yngre|äldre|yngst[ae]?|äldst[ae]?|enda|ende|gemensamm?a?|förste|första|andre|andra|tredje|fjärde)\s+)+/;
const HEDGE = /^(?:sekundärt uppgivet|sekundärt uppgiven|tidigare antagen|möjlig[at]?|sannolik[at]?|uppgiven|uppgivet|trolig[at]?)\s+/;
const PREFIX = /^(?:tidigare|senare)\s+/;
const CERTAIN_QUAL = /^(?:enligt familjeuppgift|enligt familjen|på fädernet|på mödernet|genom modern|genom fadern|i första äktenskapet|i andra äktenskapet)$/;
const UNCERTAIN = new Set(["LEAD", "CONFLICT", "REJECTED", "UNKNOWN"]);
// Samma förbehåll som föräldrakartan respekterar, utom rolltyperna styv/husbonde.
const RESERVATION = /uppgiven|tidigare antagen|sannolik|möjlig|hypotes|ej belagt|(?:inte|ej)(?: separat)? (?:belag[dt]|originalbelagd|säkra[dt]|säker|avgjor[dt]|prövad|prövat)|obelag[dt]|(?<![a-zåäö])öppe[nt](?![a-zåäö])/i;
const NORMAL = { broder: "bror", fader: "far", moder: "mor", maka: "hustru", man: "make" };

export function parseRole(text) {
  let s = text.toLowerCase().replace(/[*`_]/g, "").replace(/\s+/g, " ").trim();
  if (/^person i (?:familjehushållet|föräldrahushållet|hushållet)$|^(?:dottermarkerad )?hushållsmedlem$/.test(s)) return { noun: "hushållsmedlem", kind: "R" };
  const hedgeMatch = s.match(HEDGE);
  const hedge = hedgeMatch?.[0].trim() ?? "";
  if (hedgeMatch) s = s.slice(hedgeMatch[0].length);
  const prefixMatch = s.match(PREFIX);
  const prefix = prefixMatch?.[0].trim() ?? "";
  if (prefixMatch) s = s.slice(prefixMatch[0].length);
  s = s.replace(ADJ, "").replace(/ till båda$/, "");
  if (s === "husbondens hustru") return { noun: "matmor", hedge, kind: "R" };
  const m = s.match(/^([a-zåäö]+)(?: (.*))?$/);
  if (!m) return null;
  const noun = NORMAL[m[1]] ?? m[1];
  const rest = (m[2] ?? "").trim();
  if (rest && /^i (?:hushållet|familjehushållet|föräldrahushållet|samma hushåll)$/.test(rest) && ["son", "dotter", "bror", "syster", "barn"].includes(noun)) return { noun: `${noun} i hushållet`, hedge, kind: "R", prep: "hos" };
  if (rest && !CERTAIN_QUAL.test(rest)) return null;
  const base = { noun, hedge, prefix, qual: rest };
  if (KIN.has(noun)) return { ...base, kind: hedge || prefix ? "R" : "K" };
  if (REL.has(noun)) return { ...base, kind: "R" };
  return null;
}

// Den länkade personens roll mot aktens person, vänd till aktens roll mot den
// länkade. Värdet är [man, kvinna, okänt kön].
const INVERSE = {
  far: ["son", "dotter", "barn"], mor: ["son", "dotter", "barn"],
  son: ["far", "mor", "förälder"], dotter: ["far", "mor", "förälder"], barn: ["far", "mor", "förälder"],
  bror: ["bror", "syster", "syskon"], syster: ["bror", "syster", "syskon"], syskon: ["bror", "syster", "syskon"],
  helbror: ["helbror", "helsyster", "syskon"], helsyster: ["helbror", "helsyster", "syskon"],
  halvbror: ["halvbror", "halvsyster", "halvsyskon"], halvsyster: ["halvbror", "halvsyster", "halvsyskon"], halvsyskon: ["halvbror", "halvsyster", "halvsyskon"],
  farbror: ["brorson", "brorsdotter", "brorsbarn"], faster: ["brorson", "brorsdotter", "brorsbarn"],
  morbror: ["systerson", "systerdotter", "systerbarn"], moster: ["systerson", "systerdotter", "systerbarn"],
  farfar: ["sonson", "sondotter", "sonbarn"], farmor: ["sonson", "sondotter", "sonbarn"],
  morfar: ["dotterson", "dotterdotter", "dotterbarn"], mormor: ["dotterson", "dotterdotter", "dotterbarn"],
  kusin: ["kusin", "kusin", "kusin"],
  make: ["make", "hustru", "make eller hustru"], hustru: ["make", "hustru", "make eller hustru"],
  svärfar: ["svärson", "svärdotter", "svärbarn"], svärmor: ["svärson", "svärdotter", "svärbarn"],
  husbonde: ["tjänstehjon", "tjänstehjon", "tjänstehjon"], matmor: ["tjänstehjon", "tjänstehjon", "tjänstehjon"],
  styvfar: ["styvson", "styvdotter", "styvbarn"], styvmor: ["styvson", "styvdotter", "styvbarn"],
  fosterfar: ["fosterson", "fosterdotter", "fosterbarn"], fostermor: ["fosterson", "fosterdotter", "fosterbarn"], fosterförälder: ["fosterson", "fosterdotter", "fosterbarn"],
};

function invert(role, sex) {
  const forms = INVERSE[role.noun];
  if (!forms) return null;
  const noun = forms[sex === "m" ? 0 : sex === "f" ? 1 : 2];
  const kind = KIN.has(noun) && !role.hedge && !role.prefix ? "K" : "R";
  return { ...role, noun, kind, prep: undefined };
}

// Vittne vid dopet av den länkade personen: `dopvittne`, `eget dopvittne`,
// `dopvittne vid hennes dop`, `dopvittne åt`. En rad som namnger ett annat
// dopbarn (`Dopvittne till Anna Fredrika`) räknas inte.
// Vittnesordet måste stå i huvudledet (eller som `eget dopvittne`); i en cell som
// `bror och dopvittne` gäller vittnesmålet ett annat dop än personens eget.
const isWitness = (cell) => {
  if (/[Dd]opvittne (?:till|åt|vid dopet av) \p{Lu}/u.test(cell)) return false;
  return /^dopvittne(?:$| vid (?:hennes|hans) dop| vid dopet| åt)/i.test(head(cell)) || /(?:^|[\s,])eget dopvittne\b/i.test(cell);
};

const rowsOf = (person) => {
  const section = (person.text.split("## Relationer")[1] ?? "").split(/\n## /)[0];
  return [...section.matchAll(/^\|\s*\[[^\]]+\]\((P-\d{4})[^)]*\)\s*\|\s*([^|]+)\|([^\n]*)$/gm)]
    .map(([, target, relation, rest]) => ({ target, relation: relation.trim(), status: (rest.split("|")[1] ?? "").trim().toUpperCase() }));
};

const doubt = (row) => (row ? (row.status === "CONFLICT" ? "omstridd" : row.status === "REJECTED" ? "avvisad" : UNCERTAIN.has(row.status) || RESERVATION.test(row.relation) ? "obekräftad" : "") : "");
const agree = (word, noun) => (word && NEUTER.has(noun.split(" ")[0]) ? word.replace(/d$/, "t").replace(/ttt$/, "tt") : word);

// Alla kända roller mellan en sidoperson och en annan person. Osäkerhet i
// endera aktens rad gäller relationen.
function facts(people, sexes, s, other) {
  const theirs = rowsOf(people.get(other)).find((r) => r.target === s);
  const mine = rowsOf(people.get(s)).find((r) => r.target === other);
  const worst = [doubt(theirs), doubt(mine)].find((d) => d === "avvisad") ?? [doubt(theirs), doubt(mine)].find((d) => d === "omstridd") ?? [doubt(theirs), doubt(mine)].find(Boolean) ?? "";
  const out = [];
  const add = (f) => out.push(worst && !f.witness ? { ...f, kind: "R", doubt: worst } : { ...f, doubt: f.witness ? "" : worst });
  if (theirs) {
    if (isWitness(theirs.relation)) add({ witness: true, source: "ankare" });
    else {
      const role = parseRole(head(theirs.relation));
      if (role) add({ ...role, source: "ankare" });
    }
  }
  if (mine) {
    if (isWitness(mine.relation)) add({ witness: true, source: "egen" });
    else {
      const role = parseRole(head(mine.relation));
      const inverted = role && invert(role, sexes.get(s));
      if (inverted) add({ ...inverted, source: "egen" });
    }
  }
  return out;
}

const distance = (f) => (f.witness ? 3 : CLOSE.has(f.noun) ? 0 : KIN.has(f.noun) ? 1 : f.noun === "hustru" || f.noun === "make" ? 1 : 2);
const rank = (f) => (f.kind === "K" ? 0 : 10) + (f.doubt ? 20 : 0) + distance(f) + (f.source === "egen" ? 0.1 : 0);
const isKin = (f) => f.kind === "K" && !f.witness;

function roleText(f) {
  if (f.witness) return "dopvittne vid dopet av";
  const hedge = f.hedge || agree(f.doubt, f.noun);
  const noun = [f.prefix, f.noun, f.qual].filter(Boolean).join(" ");
  return `${hedge ? `${hedge} ` : ""}${noun} ${f.prep ?? (HOS.has(f.noun) ? "hos" : "till")}`;
}

const genitive = (phrase) => (phrase.endsWith("s") ? phrase : `${phrase}s`);
const SIBLING_WORD = { far: { bror: "farbror", syster: "faster" }, mor: { bror: "morbror", syster: "moster" } };
const kinPhrase = (anchorPhrase, noun) => SIBLING_WORD[anchorPhrase]?.[noun] ?? `${genitive(anchorPhrase)} ${noun}`;

// Syskon till en ana. Slutar etiketten på ett ensamt `far`/`mor` har svenskan
// ett eget ord för helsyskon: farfars mors syster är farfars moster. Halvsyskon
// skrivs ut - farfars mors halvsyster - enligt ägarens anvisning. Efter ett
// parord står syskonet i genitiv: farfars farfars syster.
const CONTRACT = {
  far: { bror: "farbror", helbror: "farbror", syster: "faster", helsyster: "faster" },
  mor: { bror: "morbror", helbror: "morbror", syster: "moster", helsyster: "moster" },
};
const SIBLING_NOUNS = new Set(["bror", "syster", "syskon", "helbror", "helsyster", "halvbror", "halvsyster", "halvsyskon"]);
const CHILD_NOUNS = new Set(["son", "dotter", "barn"]);

export function siblingPhrase(steps, noun) {
  if (!steps.length) return noun;
  const words = kinTerm(steps).split(" ");
  if (steps.length % 2 === 1) {
    const last = words.pop();
    const word = CONTRACT[last]?.[noun];
    if (word) return [...words, word].join(" ");
    words.push(last);
  }
  return `${genitive(words.join(" "))} ${noun}`;
}

// Hel- eller halvsyskon avgörs av föräldrakartan: två kända föräldrar var, och
// en av dem skiljer, ger halvsyskon. Annars skrivs det vanliga ordet.
function siblingNoun(s, other, sexes, parents) {
  const base = { m: "bror", f: "syster" }[sexes.get(s)] ?? "syskon";
  const mine = parents?.get(s) ?? new Set(), theirs = parents?.get(other) ?? new Set();
  const shared = [...mine].filter((p) => theirs.has(p)).length;
  return mine.size === 2 && theirs.size === 2 && shared === 1 ? `halv${base}` : base;
}

// Etiketten för en blodsläkting till ett ankare. Ett barn till en ana som inte
// ligger i anlinjen är syskon till nästa led mot Adam och Axel.
function kinLabel(s, anchor, f, phrases, lineage, sexes) {
  const entry = lineage?.paths?.get(anchor)?.[0];
  if (entry && CHILD_NOUNS.has(f.noun) && entry.via.length > 1) {
    // Bara när båda föräldrarna är kända för båda går hel- och halvsyskon att
    // skilja; annars står den bokstavliga formen kvar.
    const next = entry.via.at(-2);
    if (lineage.parents?.get(s)?.size === 2 && lineage.parents?.get(next)?.size === 2) {
      return siblingPhrase(entry.steps.slice(0, -1), siblingNoun(s, next, sexes, lineage.parents));
    }
  }
  if (entry && SIBLING_NOUNS.has(f.noun)) return siblingPhrase(entry.steps, f.noun);
  return kinPhrase(phrases.get(anchor), f.noun);
}

function sideText(people, anchor, anchorPhrase, f, ownPhrase) {
  if (isKin(f)) {
    return `**Släktled:** ${ownPhrase} till ${sons(people)} — ${[f.noun, f.qual].filter(Boolean).join(" ")} till ${link(people, anchor)}.`;
  }
  return `**Släktled:** ${roleText(f)} ${link(people, anchor)}, ${anchorPhrase} till ${sons(people)}.`;
}

export function sideBlocks(people, sexes, anchorPhrases, overrides = {}, lineage = null) {
  const pending = [...people.keys()].filter((id) => !anchorPhrases.has(id) && !SONS.includes(id) && !overrides[id]);
  const chosen = new Map();
  const phrases = new Map(anchorPhrases);
  const best = (s, anchors) => {
    let choice = null;
    for (const anchor of anchors) {
      for (const f of facts(people, sexes, s, anchor)) {
        if (!choice || rank(f) < rank(choice.f) || (rank(f) === rank(choice.f) && anchor < choice.anchor)) choice = { anchor, f };
      }
    }
    return choice;
  };
  // Nivå för nivå: först mot anorna, sedan mot dem som just blivit blodsläkt.
  // En osäker eller icke-släkt etikett får ersättas av säker släkt på en senare
  // nivå; en säker etikett rörs aldrig.
  let frontier = [...anchorPhrases.keys()];
  for (let level = 1; frontier.length; level += 1) {
    const next = [];
    for (const s of pending) {
      const previous = chosen.get(s);
      if (previous && isKin(previous.f)) continue;
      let choice = best(s, frontier);
      // Ett halvsyskon till en sidoperson kan vara släkt genom den förälder som
      // inte är ana, så det ger ingen släktetikett - bara rollen.
      if (choice && level > 1 && isKin(choice.f) && /^halv/.test(choice.f.noun)) choice = { ...choice, f: { ...choice.f, kind: "R" } };
      if (!choice || (previous && !isKin(choice.f))) continue;
      chosen.set(s, { ...choice, level });
      if (isKin(choice.f)) { phrases.set(s, kinLabel(s, choice.anchor, choice.f, phrases, lineage, sexes)); next.push(s); }
    }
    frontier = next;
  }
  const blocks = new Map();
  const readings = [];
  for (const s of pending) {
    const c = chosen.get(s);
    if (c) {
      blocks.set(s, { text: wrap(sideText(people, c.anchor, phrases.get(c.anchor), c.f, phrases.get(s))) });
      readings.push({ id: s, via: c.level === 1 ? "ana" : "släkt", anchor: c.anchor, kind: isKin(c.f) ? "K" : "R", witness: !!c.f.witness, source: c.f.source });
      continue;
    }
    const others = [...people.keys()].filter((id) => id !== s).sort();
    const context = best(s, others.filter((id) => phrases.has(id) || chosen.has(id))) ?? best(s, others);
    let text = `**Släktled:** ingen känd släktskap med ${sons(people)}.`;
    if (context) text += ` ${roleText(context.f).replace(/^./, (ch) => ch.toUpperCase())} ${link(people, context.anchor)}.`;
    blocks.set(s, { text: wrap(text) });
    readings.push({ id: s, via: "ingen", anchor: context?.anchor ?? null });
  }
  // Lästa tolkningar: rollordet och noten är lästa, ankarets släktled räknas.
  for (const [s, o] of Object.entries(overrides)) {
    if (!people.has(s) || !people.has(o.ankare)) continue;
    const phrase = phrases.get(o.ankare);
    const note = o.not ? ` ${o.not}` : "";
    const text = o.slag === "ingen"
      ? `**Släktled:** ${o.inledning ?? `ingen känd släktskap med ${sons(people)}.`} ${o.roll} ${link(people, o.ankare)}${phrase ? `, som är ${phrase}` : ""}.${note}`
      : `**Släktled:** ${o.roll} ${link(people, o.ankare)}, ${phrase} till ${sons(people)}.${note}`;
    blocks.set(s, { text: wrap(text) });
    readings.push({ id: s, via: "läst", anchor: o.ankare });
  }
  return { blocks, readings, phrases };
}

// Avvecklade akter (PCD-2026-09-11-034): raden anger skälet och den korrekta
// motsvarigheten. [[P-NNNN]] blir en länk, [[P-NNNN|släktled]] en länk följd
// av personens släktled.
export function retiredBlock(people, phrases, entry) {
  const text = entry.text.replace(/\[\[(P-\d{4})(\|släktled)?\]\]/g, (match, id, withPhrase, offset, whole) => {
    const phrase = withPhrase ? phrases.get(id) : null;
    const inserted = phrase ? `, ${phrase}${whole[offset + match.length] === " " ? "," : ""}` : "";
    return `${link(people, id)}${inserted}`;
  });
  return { text: wrap(`**Släktled:** avvecklad akt, ingen släktskap med ${sons(people)}. ${text}`) };
}

// Regionen mellan H1 och första H2 ägs av generatorn.
const REGION = /^(# P-\d{4}: [^\n]*\n)([\s\S]*?)(\n## )/;

export function render(text, block) {
  return text.replace(REGION, (_, h1, __, h2) => (block ? `${h1}\n${block}\n${h2}` : `${h1}${h2}`));
}

export function checkKinship(root = ROOT) {
  const { people, blocks, errors } = computeBlocks(root);
  for (const [id, person] of people) {
    const region = person.text.match(REGION)?.[2].trim() ?? "";
    const expected = blocks.get(id)?.text;
    if (expected && region !== expected) errors.push(`${person.file}: släktledsraden saknas eller är inaktuell; kör node scripts/kinship.mjs --write`);
  }
  return errors;
}

function main() {
  const mode = process.argv[2];
  if (mode === "--check") {
    const errors = checkKinship();
    for (const e of errors) console.error(e);
    console.log(errors.length ? `släktled: ${errors.length} fel.` : "släktled: OK.");
    if (errors.length) process.exitCode = 1;
  } else if (mode === "--write") {
    const { people, blocks, errors } = computeBlocks();
    for (const e of errors) console.error(e);
    let changed = 0;
    for (const [id, block] of blocks) {
      const person = people.get(id);
      const next = render(person.text, block.text);
      if (next !== person.text) {
        writeFileSync(join(ROOT, "genealogy", "people", person.file), next);
        changed += 1;
      }
    }
    console.log(`släktled: ${blocks.size} rader beräknade, ${changed} akter ändrade, ${errors.length} fel.`);
    if (errors.length) process.exitCode = 1;
  } else {
    console.error("Usage: node scripts/kinship.mjs --check | --write");
    process.exitCode = 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) main();
