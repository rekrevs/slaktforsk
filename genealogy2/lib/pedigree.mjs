import {readCurrent} from './domain.mjs';
import {identityGate} from './review.mjs';

// A spelling used by the explicit owner-confirmed biological relation in the
// migrated material. This query alias never edits the stored nature or status.
export const canonicalParentNature=raw=>raw==='biological_parent'?'biological':raw;

export function pedigree(db,root,{mode='verified',maxDepth=20,maxPaths=10000}={}) {
  if(!['verified','typed'].includes(mode))throw Error('Ogiltigt antavleläge; välj verified eller typed');
  if(!Number.isInteger(maxDepth)||maxDepth<0||maxDepth>100||!Number.isInteger(maxPaths)||maxPaths<1)throw Error('Ogiltig gräns för antavlefråga');
  const start=readCurrent(db,root);if(start?.kind!=='person')throw Error('Antavlan kräver en personidentitet');
  const cache=new Map();
  const read=id=>{if(!cache.has(id))cache.set(id,readCurrent(db,id));return cache.get(id);};
  const gates=new Map();
  const gate=id=>{if(mode==='typed')return null;if(!gates.has(id))gates.set(id,identityGate(db,id));return gates.get(id);};
  const gateReasons=g=>g?.passed===false?g.reasons.map(r=>`Identitetsgrind: ${r.message}`):[];
  const reasons=o=>!o?['Objekt saknas']:[...(o.disposition!=='accepted'?[`Bedömning ${o.disposition}`]:[]),...(o.pending_reviews.length?['Omprövning väntar']:[])];
  const supportedIdentities=id=>db.prepare(`WITH RECURSIVE basis(id) AS (
    SELECT basis_revision_id FROM dependency WHERE revision_id=? AND role IN ('supports','derived_from')
    UNION SELECT d.basis_revision_id FROM dependency d JOIN basis b ON b.id=d.revision_id WHERE d.role IN ('supports','derived_from')
  ) SELECT r.object_id,r.disposition,r.id FROM basis b JOIN revision r ON r.id=b.id JOIN object o ON o.id=r.object_id WHERE o.kind='identity'`).all(id);
  const edges=[],excluded=[],paths=[{person:root,depth:0,via:[]}],queue=[{person:root,people:[root],via:[]}];
  const rootGate=gate(root),rootReasons=[...reasons(start),...gateReasons(rootGate)];
  let truncated=false;
  if(rootReasons.length) {excluded.push({person:root,reasons:rootReasons,gate:rootGate});queue.length=0;}
  for(let n=0;n<queue.length;n++) {
    const branch=queue[n];
    const parents=db.prepare("SELECT object_id FROM current_relation WHERE to_person=? AND relation_type='parent' ORDER BY object_id").all(branch.person);
    if(branch.via.length===maxDepth){if(parents.length)truncated=true;continue;}
    for(const row of parents) {
      const edge=read(row.object_id),parent=read(edge.from_person),parentGate=gate(edge.from_person);
      const why=[...reasons(edge),...reasons(parent).map(r=>`Förälder: ${r}`),...gateReasons(parentGate).map(r=>`Förälder: ${r}`)];
      if(!['recorded_parent','biological'].includes(canonicalParentNature(edge.nature)))why.push(`Föräldrarelationens art: ${edge.nature}`);
      for(const i of supportedIdentities(edge.revision_id)) {
        if(i.disposition!=='accepted')why.push(`Åberopad identitet ${i.id} är ${i.disposition}`);
        const current=read(i.object_id);
        if(current.revision_id!==i.id)why.push(`Åberopad identitet ${i.id} är ersatt`);
        if(current.pending_reviews.length)why.push(`Åberopad identitet ${i.id} väntar på omprövning`);
      }
      if(branch.people.includes(edge.from_person))why.push('Cykel i föräldralänkarna');
      if(why.length){excluded.push({relation:edge,via:branch.via,reasons:why,gate:parentGate});continue;}
      if(paths.length>=maxPaths){truncated=true;continue;}
      if(!edges.some(e=>e.object_id===edge.object_id))edges.push(edge);
      const via=[...branch.via,edge.object_id];
      paths.push({person:edge.from_person,depth:via.length,via});
      queue.push({person:edge.from_person,people:[...branch.people,edge.from_person],via});
    }
  }
  const common='Endast aktuella accepterade parent-länkar (recorded_parent eller biological, inklusive läsalias biological_parent) och accepterade personobjekt. correlated_parent ger ingen automatisk passage. Lagrade relationsord och bedömningar bevaras. Inga väntande omprövningar eller åberopade osäkra/avvisade/ersatta identiteter. Riktning: från förälder till barn. Vittnes- och partnerroller ger inga föräldrakanter.';
  const rules=mode==='verified'
    ?'Verifierad vy: roten och varje passerad förälder måste dessutom ha godkänd identitetsgranskning och bärande trädverkan enligt aktuell identityGate. Livsbildens granskningsutfall är separat. '
    :'Typad vy: identitetsgranskningens kontraktsgrind prövas inte. ';
  return {root,mode,rules:rules+common+' Roten visas som frågans utgångspunkt även om dess grind stoppar fortsatt passage. Vyn intygar inte att hela antavlan är fullständig.',maxDepth,maxPaths,truncated,paths,edges,excluded,root_gate:rootGate,gates:[...gates.values()]};
}
