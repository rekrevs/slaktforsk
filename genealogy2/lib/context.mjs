import fs from 'node:fs';
import {sha} from './archive.mjs';

const cohorts = JSON.parse(fs.readFileSync(new URL('../migration/cohorts.json', import.meta.url), 'utf8'));
const documentGroups = new Map(cohorts.groups.flatMap(group => group.documents.map(path => [path, group.id])));
const contextGroups = new Set(['research-context', 'archive-context']);
const notice = 'Bevarat sammanhang från importbasen. Dokumentets egna statusord och nästa steg är historiska; de anger varken aktuellt personläge eller en utförandekö. Textomnämnanden nedan är navigationshjälp, inte nya personfakta eller identitetsbeslut.';

// These labels describe the purpose of the preserved documents, not the truth or
// current validity of their contents. No unit-conversion decision is inferred.
const purposes = {
  'genealogy/README.md': ['historical_governance', 'Äldre regler och orientering', 'Beskriver den äldre forskningsstrukturens lager, evidensstatus, provenans och utgåvegrind.'],
  'genealogy/access-register.md': ['access_history', 'Daterad åtkomsthistorik', 'Samlar daterade, ibland senare upphävda åtkomstbesked. Beskeden är inte beständiga egenskaper hos arkivvolymerna.'],
  'genealogy/avvecklade-akter.json': ['historical_register', 'Äldre register över avvecklade akter', 'Bevarar äldre beslut och visningstexter. Hänvisningar och motsvarigheter skapar inte nya sammanslagningar eller aktuell forskningsstatus.'],
  'genealogy/kinship-roles.json': ['historical_register', 'Äldre register över relationsformuleringar', 'Bevarar lästa rollord, kandidater och avvisade uppgifter för presentation; det är ingen ny föräldrakarta.'],
  'genealogy/frontier.md': ['historical_indicator', 'Äldre forskningsfront', 'Bevarar daterade översikter och rättelser om öppna fronter. Historiska nästa steg blir inte en aktuell arbetskö.'],
  'genealogy/tree.md': ['historical_indicator', 'Äldre antavleöversikt', 'Bevarar en härledd arbetsöversikt och ersätter inte personernas egna belägg eller den aktuella antavlan.'],
  'genealogy/research-inventory.json': ['historical_indicator', 'Äldre inventeringsögonblick', 'Härledd struktur- och granskningsinventering vid importen; den bevisar inte saklig forskning eller dagens personstatus.'],
  'genealogy/source-coverage.md': ['historical_coverage', 'Äldre källtäckningsmatris', 'Bevarar källvägar, sökomfång, reserverade celler och återaktiveringsvillkor. Visningen utför eller schemalägger ingen passage.'],
  'genealogy/media-manifest.json': ['material_metadata', 'Bevarad medieförteckning', 'Förtecknar medier och kontrollsummor. En länk eller matchande hash innebär ingen ny läsning av ett original.'],
  'genealogy/editions/assets/README.md': ['material_metadata', 'Utgåvans kartprovenans', 'Beskriver kartgeometri och moderna orienteringspunkter; punkterna är inte exakta historiska fastighetskoordinater.'],
  'genealogy/research-profiles/README.md': ['historical_governance', 'Äldre profilregler', 'Beskriver frågor, teman, källvägar och kontraktsbedömningar som kunskapsläge, åtskilt från Wotans utförandestatus.'],
  'genealogy/source-contexts/README.md': ['historical_governance', 'Äldre regler för källkontext', 'Beskriver återbrukbar ort-, tids- och arkivrouting. Sådan metadata belägger inte personförekomst, identitet eller personnoll.'],
  'genealogy/method-riksarkivet.md': ['historical_governance', 'Äldre åtkomstmetod', 'Bevarar metod och erfarenheter för arkivåtkomst vid importen; ingen ny åtkomstprövning har gjorts.'],
  'genealogy/person-contract.md': ['historical_governance', 'Äldre personkontrakt', 'Bevarar granskningskrav och skillnaden mellan identitetsnivå och livsbild; katalogen tilldelar inga personbetyg.'],
  'genealogy/person-standard.md': ['historical_governance', 'Äldre aktstandard', 'Bevarar skriv- och utvinningsregler för personakter; inga nya fakta skapas genom visningen.'],
  'genealogy/research-plan.md': ['historical_governance', 'Äldre forskningsprogram', 'Bevarar program, kvalitetskrav och historiska beslut. Utförande och återupptagning bestäms inte av denna arkivvy.'],
  'genealogy/source-strategy.md': ['historical_governance', 'Äldre källstrategi', 'Bevarar regler för val, täckning och återbruk av källvägar; visningen innebär ingen ny sökning.'],
  'genealogy/identity-review-2026-09-04.md': ['historical_review', 'Tidigare identitetsrevision', 'Daterad konsolideringsrevision med sin ursprungliga argumentation; inte ett automatiskt nytt godkännande av berörda personer.'],
  'genealogy/research-program-verification-2026-09-05.md': ['historical_review', 'Tidigare programverifiering', 'Bevarar utförda kontroller och deras dåvarande omfång; resultatet blir ingen aktuell projekt- eller personstatus.'],
  'genealogy/source-strategy-pilot-2026-09-05.md': ['historical_review', 'Tidigare källstrategipilot', 'Bevarar en daterad prövning av källstrategin och dess gränser; den ersätter ingen individuell aktuell sakbedömning.'],
  'genealogy/research-log/front-notes-archive-2026-09-04.md': ['historical_log', 'Arkiverade frontanteckningar', 'Äldre anteckningar och fortsättningsförslag, bevarade som historik utan återaktivering.'],
  'genealogy/research-log/handover-archive-2026-09-04.md': ['historical_log', 'Arkiverat överlämningsmaterial', 'Äldre sessions- och utförandeminne. Det får inte bli en parallell återupptagningskö.']
};

function classification(path, group) {
  let p = purposes[path];
  if (!p && /^genealogy\/research-log\/\d{4}-\d{2}-\d{2}\.md$/.test(path)) p = ['historical_log', 'Daterad forskningslogg', 'Kronologiskt bevarade sökningar, resultat och rättelser. Katalogisering innebär inte att varje stor logg har semantiskt omprövats.'];
  if (!p && /^genealogy\/editions\/[^/]+\.json$/.test(path)) p = ['edition_material', 'Tidigare utgåveunderlag', 'Bevarar en viss utgåvas urval, kartnycklar eller layout. Äldre utgåveuppgifter ersätter inte den aktuella personmodellen.'];
  if (!p && /^genealogy\/templates\/[^/]+\.md$/.test(path)) p = ['historical_template', 'Äldre dokumentmall', 'Bevarar en mall, dess exempel och fältnamn; exemplen är inte nya personuppgifter eller beställt arbete.'];
  if (!p && path.startsWith('wotan/')) p = ['historical_execution', 'Äldre Wotan-underlag', 'Bevarar utförandehistorik från importen. Aktuella uppgiftsstatusar och återupptagningspunkter hämtas inte från denna kopia.'];
  if (!p && /^(?:AGENTS|CLAUDE|README|NORTH-STAR|PROJECT-CONTROL)\.md$/.test(path)) p = ['historical_governance', 'Äldre projektstyrning', 'Bevarar projektets styrsammanhang vid importen; visningen återutfärdar inga instruktioner.'];
  if (!p) p = group && !contextGroups.has(group)
    ? ['legacy_entity', 'Bevarat registerdokument', 'Ursprungligt person-, profil- eller källdokument; aktuell native representation ska prövas separat.']
    : ['preserved_material', 'Övrigt bevarat material', 'Dokumentet bevaras med ursprung och innehåll. Ingen full semantisk omprövning eller aktuell status härleds av katalogiseringen.'];
  return {kind:p[0],label:p[1],purpose:p[2],authority:'historical_context',semantic_review:'not_asserted'};
}

function summary(row) {
  const group = documentGroups.get(row.path) ?? null;
  const title = row.title || row.text?.match(/^#\s+([^\r\n]+)$/m)?.[1] || row.path;
  return {path:row.path,title,sha256:row.sha256,bytes:row.bytes,import_batch:row.batch_id,
    import_group:group,cohort_baseline:cohorts.baseline,cohort_baseline_matches:row.batch_id===cohorts.baseline,
    frozen:Boolean(row.frozen),classification:classification(row.path,group),notice};
}

function filterValue(value, name) {
  if (value == null) return '';
  if (typeof value !== 'string') throw new TypeError(`${name} måste vara text`);
  return value.trim();
}

/** Lists preserved context by default; an explicit group selects its exact manifest documents. */
export function contextList(db, {group,query} = {}) {
  group = filterValue(group,'group'); query = filterValue(query,'query').toLocaleLowerCase('sv');
  const rows = db.prepare(`SELECT d.*,e.title FROM document d
    LEFT JOIN legacy_entity e ON e.document_path=d.path ORDER BY d.path`).all();
  return rows.filter(row => {
    const actual = documentGroups.get(row.path);
    if (group ? actual !== group : !contextGroups.has(actual)) return false;
    return !query || [row.path,row.title??'',row.text].some(s => s.toLocaleLowerCase('sv').includes(query));
  }).map(summary);
}

const linkPath = path => path.split('/').map(encodeURIComponent).join('/');

function references(db, text) {
  const entities = new Map();
  for (const e of db.prepare('SELECT id,kind,document_path,title FROM legacy_entity ORDER BY id,kind,document_path').all()) {
    if (!entities.has(e.id)) entities.set(e.id,[]);
    entities.get(e.id).push({kind:e.kind,path:e.document_path,title:e.title,href:linkPath(e.document_path)});
  }
  const tasks = new Set(db.prepare("SELECT path FROM document WHERE path GLOB 'wotan/dev-log/T-[0-9][0-9][0-9][0-9].md'").all().map(r=>r.path));
  const found = new Map();
  // Exact identifiers only. Do not expand ranges or turn partial numbers into IDs.
  const pattern = /(?<![\p{L}\p{N}_-])([PSCT]-\d{4})(?![\p{L}\p{N}_])/gu;
  let cursor=0,byte=0,line=1;
  for (const match of text.matchAll(pattern)) {
    const before=text.slice(cursor,match.index);
    byte+=Buffer.byteLength(before); line+=(before.match(/\n/g)??[]).length;
    const id=match[1],start=byte,end=start+Buffer.byteLength(id);
    if (!found.has(id)) {
      const path=`wotan/dev-log/${id}.md`;
      const targets=id.startsWith('T-') ? (tasks.has(path)?[{kind:'wotan',path,title:id,href:linkPath(path)}]:[]) : (entities.get(id)??[]);
      found.set(id,{id,kind:id.startsWith('T-')?'wotan':'legacy_entity',resolved:targets.length>0,
        relation:'text_mention_only',targets,occurrences:[]});
    }
    found.get(id).occurrences.push({start_byte:start,end_byte:end,line});
    byte=end;cursor=match.index+id.length;
  }
  return [...found.values()].sort((a,b)=>a.id.localeCompare(b.id));
}

/** Returns the immutable imported text, never a read of a possibly newer worktree file. */
export function contextDocument(db, path) {
  if (typeof path !== 'string' || !path) throw new TypeError('Dokumentets exakta importsökväg krävs');
  const row=db.prepare(`SELECT d.*,e.title FROM document d
    LEFT JOIN legacy_entity e ON e.document_path=d.path WHERE d.path=?`).get(path);
  if (!row) return null;
  if (Buffer.byteLength(row.text)!==row.bytes || sha(row.text)!==row.sha256) throw Error(`Importtextens byte/hash avviker: ${path}`);
  const units=db.prepare(`SELECT id,kind,legacy_id,owner_id,section,start_byte,end_byte,start_line,end_line,historical
    FROM unit WHERE document_path=? ORDER BY start_byte,end_byte,id`).all(path);
  return {...summary(row),text:row.text,integrity:{bytes_verified:true,sha256_verified:true},
    units:units.map(u=>({...u,historical:Boolean(u.historical)})),references:references(db,row.text)};
}

const escapeLabel = text => text.replace(/[\\\[\]`*_<>]/g,'\\$&').replace(/[\r\n]+/g,' ');

/** Markdown wrapper; the final original-text portion remains byte-for-byte unchanged. */
export function renderContextDocument(data) {
  if (!data) throw new TypeError('Dokument saknas');
  const lines=[`# ${escapeLabel(data.title)}`,'',data.notice,'',
    `Dokument: ${data.path}`,`SHA-256: ${data.sha256}`,`Byte: ${data.bytes}`,
    `Importbas: ${data.import_batch}`,`Importgrupp: ${data.import_group??'saknas i kohortmanifestet'}`,
    `Dokumenttyp: ${data.classification.label}`,'',data.classification.purpose,'',
    'Katalogen gör ingen full semantisk granskning av innehållet. Ursprungliga rubriker, instruktioner och statusord återges som arkivtext.',''];
  if (!data.cohort_baseline_matches) lines.push('Kohortmanifestets bas skiljer sig från dokumentets importbas; grupptillhörigheten är endast en sökvägsmatchning.','');
  const linked=data.references.filter(r=>r.resolved),unlinked=data.references.filter(r=>!r.resolved);
  if (linked.length) {
    lines.push('## Identifierare som nämns','',
      'Länkarna navigerar till dokumentvägar. De anger inga relationer, evidensgrader eller aktuella arbetsstatusar.','');
    for (const ref of linked) lines.push(`- ${ref.id}: ${ref.targets.map(t=>`[${escapeLabel(t.title)} (${t.kind})](<${t.href}>)`).join('; ')}. Första textställe: rad ${ref.occurrences[0].line}.`);
    lines.push('');
  }
  if (unlinked.length) lines.push('Ej återfunna som dokument i importbasen: '+unlinked.map(r=>r.id).join(', ')+'. Inga mål har gissats.','');
  lines.push('## Bevarad originaltext','');
  return lines.join('\n')+'\n'+data.text;
}
