// Fixed read-only regression, not a new original-image audit.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {openDB} from '../../lib/store.mjs';
import {sha,canonical} from '../../lib/archive.mjs';
import {impact} from '../../lib/impact.mjs';
const root=fileURLToPath(new URL('../../../',import.meta.url));
const dbPath=process.argv[2]??path.join(root,'genealogy2/data/research.sqlite');
const db=openDB(dbPath,{readOnly:true});
const fileHashes=()=>Object.fromEntries([dbPath,...fs.readdirSync(path.join(root,'genealogy2/journal')).filter(n=>n.endsWith('.json')).sort().map(n=>path.join(root,'genealogy2/journal',n))].map(p=>[path.relative(root,p),sha(fs.readFileSync(p))]));
const before=fileHashes(),results=[],views=new Map();
try {
  for(const c of JSON.parse(fs.readFileSync(new URL('cases.json',import.meta.url),'utf8')).cases) {
    const start=performance.now(),r=impact(db,c.citation,{query:c.query});views.set(c.citation,r);
    for(const revision of c.records)assert(r.seeds.some(s=>s.revision_id===revision),revision);
    for(const revision of c.expected_current_dependents)assert(r.dependencies.current.some(s=>s.revision_id===revision),revision);
    results.push({citation:c.citation,query:c.query,elapsed_ms:Math.round(performance.now()-start),
      seeds:r.seeds.map(s=>s.revision_id),current_dependencies:r.dependencies.current.length,historical_dependencies:r.dependencies.historical.length,
      origin_links:r.provenance.origins.length,target_links:r.provenance.targets.length,
      current_text_candidates:r.text_candidates.current.length,historical_text_candidates:r.text_candidates.historical.length,
      expected_current_dependents_found:c.expected_current_dependents,
      result_sha256:sha(canonical(r)),result:'PASS'});
  }
  const date=views.get('C-0721'),raw=impact(db,'C-0721',{query:'1783 21/10'}),name=impact(db,'C-0721',{query:'Lena Jonsdotter'});
  const copy=raw.text_candidates.current.find(r=>r.revision_id==='S-0556@2');assert(copy&&!copy.registered_dependency);
  assert(copy.hits.some(h=>h.field==='description'&&h.term==='1783 21/10'));
  const full=db.prepare("SELECT description FROM source WHERE revision_id='S-0556@2'").get().description;
  assert(full.includes('Bevarad beskrivningshistorik'));assert(full.includes('felläsning'));
  const old=date.text_candidates.historical.find(r=>r.revision_id==='E-birth-P-0477@1');assert(old);
  const namesake=name.text_candidates.current.find(r=>r.revision_id==='BIO-P-0363@1');assert(namesake&&!namesake.registered_dependency);
  assert(!name.dependencies.current.some(r=>r.object_id==='BIO-P-0363'));
  const actual=name.dependencies.current.find(r=>r.revision_id==='BIO-P-0477@2');assert(actual);
  assert(actual.reached_dependencies.some(e=>e.basis_revision_id==='O-P-0477-C0721-Walla@2')); // one shortest path may instead use the other Walla observation
  const retained=views.get('C-0048').dependencies.current.find(r=>r.revision_id==='E-birth-P-0048@1');assert(retained);
  assert(retained.path.some(e=>e.basis_revision_id==='R-5bff8de790faa07588de3620@1'));
  assert.deepEqual(fileHashes(),before,'database and old journal bytes must remain unchanged');
  console.log(JSON.stringify({task:'T-0672',result:'PASS',database_state:date.database_state,cases:results,
    fixtures:{unlinked_copy:copy,historical_revision:old,namesake,current_supported:actual,retained_old_basis:retained},
    semantic_dispositions:{unlinked_copy:'S-0556 description carries the corrected copied date and preserved older wording, without dependency; candidate, not a newly discovered error.',
      current_text_history:'The same current description contains a retracted statement under Bevarad beskrivningshistorik; only manual field reading determines its meaning.',
      namesake:'BIO-P-0363 is Maja Lena Jonsdotter in Mönnerum/Jonsberg, spouse Lars Svensson, child Carolina1849; unrelated to Walla Lena/Jan Ericson. Do not link or correct by substring.'},
    unchanged_database_and_journal:true,before_hashes:before,
    limitations:'Fixed post-correction cases verify discovery and classification only, not original readings or completeness of semantic impact.'},null,2));
} finally {db.close();}
