// Read-only builder. This module never opens a database or applies an operation.
import assert from 'node:assert/strict';
import {sha, canonical} from '../lib/archive.mjs';
import {head, readCurrent} from '../lib/domain.mjs';

export const OBSERVATION_C_REVISIONS = [
  'O-P-0003-C0266-cabins', 'O-P-0003-C0266-photo-childhood',
  'O-P-0019-mother-not-named', 'O-P-0043-related125-household_role_report',
  'O-P-0315-C0510-household', 'O-P-0043-related122-household_role_report',
  'O-P-0043-related123-household_role_report',
  ...['Britta-Anders','Britta-Erics','Kjerstin','Namndeman','Olof'].map(s=>`O-C0848-witness-${s}`),
];

const R = {
  story:'R-31ddf6090af32ffa30920ac9', photo7:'R-ebc1b097fdf641489b43ca8c',
  photo5:'R-e287bc29e8195678601ee5e6', letter:'R-2989c302482c679b7fa007d7',
  gunborg1918:'R-e15535f496176e63f9c9b415', gunborg1930:'R-4b47425bfe4a1bdc3e0449ab',
  ljungbacka402:'R-c2061a9ef8456576c3564fbf', ture402:'R-836c129ec57720e26352a023',
  ljungbacka914:'R-e67bb6868b81121b2d3f0732', hogsjo:'R-b4d2026f0cdd001da7dfedde',
  svenBirth:'R-b1609ddef74d345e7968a88a',
};

export function buildObservationCorrectionsC(db) {
  const changes=[], spans=new Map(), additions=new Map(), cases=[], before=new Map();
  const newVersions=new Map(), originNotes='T-0663 del c: exakt bevarat textursprung; ingen ny källäsning.';
  const current=id=>{const x=readCurrent(db,id);assert(x,`Saknat återbruk ${id}`);return x;};
  const payload=x=>{
    const row=db.prepare(`SELECT * FROM ${x.kind} WHERE revision_id=?`).get(x.revision_id);
    delete row.revision_id;
    for(const key of Object.keys(row))if(key.endsWith('_json')&&row[key]!==null)row[key]=JSON.parse(row[key]);
    return {...row};
  };
  const oldOrigins=x=>x.origins.map(o=>({unit:o.unit_id,coverage:o.coverage,note:o.note}));
  const uniqOrigins=list=>[...new Map(list.map(o=>[o.unit,o])).values()];
  function at(entity,kind,startLine,endLine=startLine) {
    const entities=db.prepare('SELECT document_path FROM legacy_entity WHERE id=? AND kind=?').all(entity,kind);
    assert.equal(entities.length,1,`Entydigt dokument krävs ${entity}/${kind}`);
    const path=entities[0].document_path, doc=db.prepare('SELECT * FROM document WHERE path=?').get(path);
    const lines=doc.text.split('\n');assert(startLine>=1&&endLine>=startLine&&endLine<=lines.length);
    assert(lines.slice(startLine-1,endLine).join('\n').trim(),`Tomt ursprung ${entity}:${startLine}-${endLine}`);
    const start=Buffer.byteLength(lines.slice(0,startLine-1).join('\n'))+(startLine>1?1:0);
    const end=start+Buffer.byteLength(lines.slice(startLine-1,endLine).join('\n'))+(endLine<lines.length?1:0);
    assert(end>start&&end<=doc.bytes);
    const id=sha(`${path}\0${doc.sha256}\0curated_span\0${start}\0${end}`);
    if(!db.prepare('SELECT id FROM unit WHERE id=?').get(id))spans.set(id,{id,path,sha256:doc.sha256,start,end,owner:entity,section:'T-0663/observation-boundary-c'});
    return {unit:id,coverage:'partial',note:originNotes};
  }
  function evidence(ids,role='supports') {
    return [...new Set(ids)].map(object=>({object,version:newVersions.get(object)??head(db,object)?.version,
      role,note:'Avgränsat bevarat underlag; samma familje-/bokföringskedja räknas inte som nya oberoende röster.'}));
  }
  function add(change) {
    assert(!changes.some(x=>x.id===change.id),`Dubblerad ändring ${change.id}`);
    assert(change.evidence.every(e=>Number.isInteger(e.version)),`Obundet belägg ${change.id}`);
    changes.push(change);newVersions.set(change.id,(change.expectedVersion??0)+1);return change;
  }
  function revise(id,recordId,mutate,rationale,extraOrigins=[],caveat=null) {
    const x=current(id);assert.equal(x.kind,'observation');assert.equal(x.version,1,`Ompröva ändrad bas ${id}`);
    assert.equal(x.record_id,recordId,`Ändrad postgräns ${id}`);before.set(id,x);
    const data=payload(x);mutate(data);
    return add({id,kind:'observation',expectedVersion:x.version,disposition:x.disposition,
      evidenceStatus:x.evidence_status,rationale,caveat:caveat??x.caveat,data,
      origins:uniqOrigins([...oldOrigins(x),...extraOrigins]),
      evidence:evidence([data.record_id,...(data.mention_id?[data.mention_id]:[])]),
      bindings:{[data.record_id]:head(db,data.record_id).version,...(data.mention_id?{[data.mention_id]:head(db,data.mention_id).version}:{})}});
  }
  function observation(id,recordId,property,value,literal,origins,caveat) {
    assert(!head(db,id),`Nytt id finns redan ${id}`);
    return add({id,kind:'observation',expectedVersion:null,disposition:'recorded',evidenceStatus:'TRANSCRIBED',
      rationale:`Återger endast den uttryckligt utvunna egna posten för ${property}; skiljs från den tidigare flerpostssyntesen.`,
      caveat,data:{record_id:recordId,mention_id:null,property,value_json:value,value_literal:literal},
      origins:uniqOrigins(origins),evidence:evidence([recordId]),bindings:{[recordId]:head(db,recordId).version}});
  }
  function fact(id,subject,property,value,origins,support,rationale,caveat) {
    assert(!head(db,id),`Nytt id finns redan ${id}`);
    return add({id,kind:'fact',expectedVersion:null,disposition:'accepted',evidenceStatus:'TRANSCRIBED',rationale,caveat,
      data:{subject_id:subject,property,value_type:'structured',value_json:value},
      origins:uniqOrigins(origins),evidence:evidence(support)});
  }
  function preserveTargets(observationId,targets) {
    const units=db.prepare(`SELECT DISTINCT d.* FROM current_unit_decision d
      JOIN unit_decision_target t ON t.decision_id=d.id WHERE t.target_id=?`).all(observationId);
    assert(units.length,`Inget aktuellt representationsmål ${observationId}`);
    for(const u of units) {
      const a=additions.get(u.unit_id)??{before:u,targets:new Set()};
      for(const t of targets)a.targets.add(t);additions.set(u.unit_id,a);
    }
  }
  const A=id=>{
    const units=db.prepare("SELECT id FROM unit WHERE kind='assertion' AND legacy_id=?").all(id);
    assert.equal(units.length,1,`Entydig A-enhet krävs ${id}`);
    return {unit:units[0].id,coverage:'partial',note:originNotes};
  };

  // B1: familyPhotoYear belongs to a separately delimited caption, not the prose R.
  const cabins='O-P-0003-C0266-cabins', cabinF='F-P-0003-family_account-cabins-and-photo1941';
  revise(cabins,R.story,data=>{
    assert.equal(data.value_json.buildings[0].familyPhotoYear,'1941');
    delete data.value_json.buildings[0].familyPhotoYear;delete data.value_json.ownershipProved;
  },'A1684:s byggberättelse hör till krönikans berättande text. Fotoåret1941 hör till separat bildtext7 och flyttas till en belagd F-syntes; inget ägarbevis tillförs.',
  [A('A-1684'),at('C-0266','citation',21,25)],
  'Sonens byggberättelse med dess ungefärliga tidsuppgifter; foto7 och frågan om lagfart redovisas i separat F.');
  fact(cabinF,'P-0003','family_account',{
    reported_buildings:changes.at(-1).data.value_json.buildings,
    photograph:{record:R.photo7,year:'1941',place:'Orrestaö',caption_context:'vid den nybyggda stugan',named:['Arne','May','Jan-Christer','Anita']},
    ownership_proven:false,independent_confirmation:false,
  },[A('A-1684'),at('C-0266','citation',21,25),at('C-0266','citation',45,46)],
  [cabins,'O-P-0303-C0266-photo-orrestao',R.photo7],
  'Bevarar A1684:s bygguppgift och foto7:s1941hållpunkt som två avgränsade delar i samma familjematerial.',
  'Byggande enligt sonen är inte fastställd lagfart, markägande eller kostnad. Bildtext och berättelse är inte oberoende källor.');
  preserveTargets(cabins,[cabinF,'O-P-0303-C0266-photo-orrestao']);
  cases.push({case:'B1',observation:cabins,reuse:['O-P-0303-C0266-photo-orrestao'],synthesis:cabinF});

  // B2: the age is in the later letter, while the caption carries its own positions.
  const photo='O-P-0003-C0266-photo-childhood', letterO='O-P-0003-C0267-photo-childhood-explanation', photoF='F-P-0003-photograph_identification-childhood';
  revise(photo,R.photo5,data=>{
    assert.equal(data.value_json.approximateAge,'fyra år');
    data.value_json={caption:'Arne mellan Vilhelmina och Fredrik; Ada sittande till höger om Fredrik.',
      named:['Arne','Vilhelmina','Fredrik','Ada']};data.value_literal=data.value_json.caption;
  },'Foto5:s bildtext har namn och positioner men ingen fyraårsålder. Åldern och senare positionsförklaringen förs på brevets egen R och sammanförs som F.',
  [at('C-0266','citation',43)],'Familjens egen bildtext; ingen ny bild- eller ansiktsanalys.');
  observation(letterO,R.letter,'photograph_explanation',{
    reported_age:'fyra år',Arne_position:'stående i bakre raden',Ada_position:'sittande med händerna i knäet',
    named_grandparents:['Vilhelmina (Mormor Mina)','Fredrik Jansson'],narrator:'Jan-Christer Janson',
  },'Jan-Christer: Arne fyra år, stående i bakre raden; Ada sitter med händerna i knäet; Vilhelmina (Mormor Mina) och Fredrik Jansson ingår.',
  [A('A-1680'),at('C-0267','citation',14,16)],'En senare familjeuppgift, inte en ålder avläst ur foto5:s bildtext.');
  fact(photoF,'P-0003','photograph_identification',{
    photograph_record:R.photo5,explanation_record:R.letter,identified_persons:['P-0003','P-0009','P-0043','P-0042'],
    age_from_letter:'fyra år',letter_author:'Jan-Christer Janson',mediator:'Sverker Adam Janson',
    historical_attribution:'C0266/A1680 kallar den senare förklaringen Sverkers.',
    independent_face_analysis:false,independent_informants_proven:false,
  },[A('A-1680'),at('C-0266','citation',43),at('C-0266','citation',52,55),at('C-0267','citation',14,16),at('S-0212','source',5,11)],
  [photo,letterO],
  'Skiljer bildtextens identifieringar från brevets ålder/positioner. C0267 och S0212 anger upphov och förmedlare, medan den äldre tillskrivningen bevaras som historik.',
  'Samma familjeuppgiftskedja; ingen ny självständig personidentifikation eller exakt fotodag fastställs.');
  preserveTargets(photo,[letterO,photoF]);cases.push({case:'B2',observation:photo,newOwn:letterO,synthesis:photoF});

  // B3: two bounded absences are retained as two observations and one synthesis.
  const mother='O-P-0019-mother-not-named', motherO='O-P-0019-C0019-mother-not-named', motherF='F-P-0019-source_scope-mother-two-records';
  revise(mother,R.gunborg1918,data=>{
    assert.deepEqual(data.value_json.scope,['C-0919 rad 10','C-0019 egen rad i familj 1']);
    data.value_json={named_mother:null,scope:'C-0919, Hyltinge A II a/5 uppslag13 rad10'};
    data.value_literal='Ingen mor namnges på Gunborg Elisabets egen rad10 i Hyltinge A II a/5 uppslag13.';
  },'Nollan på rad10 skiljs från folkräkningsbladets1930nolla. Båda äldre positiva personankarna och den olösta modersfrågan bevaras.',
  [A('A-5407'),at('C-0919','citation',37)],'Endast den egna1918–1920postens avgränsade tystnad; ingen negativ biologisk slutsats.');
  observation(motherO,R.gunborg1930,'mother_not_named',{
    named_mother:null,scope:'C-0019, SCB1930 Hyltinge s6 familj1, Gunborg Elisabets egen rad',
  },'Ingen mor namnges på Gunborg Elisabets egen rad i familj1 på1930bladet.',
  [A('A-5407'),at('C-0019','citation',26,30)],'Gäller denna rad, inte vad samtiden visste eller alla källor om modern.');
  fact(motherF,'P-0019','source_scope',{
    bounded_absences:[{record:R.gunborg1918,row:10},{record:R.gunborg1930,family:1}],
    mother_identified_in_these_records:false,candidate:'P-0117',candidate_accepted_as_mother:false,
    mother_unknown_to_contemporaries_proven:false,
  },[A('A-0116'),A('A-5407'),at('P-0019','person',54)], [mother,motherO],
  'Bevarar A5407:s tvåpostssyntes och relationsradens kandidatförbehåll separat från varje postegen nolla.',
  'Charlotta Cecilia Elisabet Gustafsson är kandidat via faderns äktenskap; ingen ny modersrelation accepteras.');
  preserveTargets(mother,[motherO,motherF]);cases.push({case:'B3',observation:mother,newOwn:motherO,synthesis:motherF});

  // B4: the seamstress and the married couple have separate row boundaries.
  const elin='O-P-0043-related125-household_role_report',elinF='F-P-0043-family_context-Elin-household-sequence';
  revise(elin,R.ljungbacka402,data=>{
    assert(data.value_literal.includes('1914-12-31'));
    data.value_json={row:9,name_literal:'Elin Augusta Larsson',occupation_literal:'sömmerska',
      reported_birth:'1882-09-27',birth_place:'Gåsinge',arrival_from:'Engelbrekts förs. Stockholm',registered_arrival:'1914-10-15'};
    data.value_literal='Elin Augusta Larsson | sömmerska | 82 27/9 | Gåsinge | Engelbrekts förs. Stockholm | 14 15/10';
  },'C0911/r9:s sömmerska hålls skild från makarnas r16–17. Vigsel1914-12-31 och sonhustruföljden återbrukas i F med rätt R.',
  [at('C-0911','citation',24,25)],'Egen rad9. Ingen senare vigsel eller fysisk flytt läses in i denna rad.');
  fact(elinF,'P-0043','family_context',{
    person_name:'Elin Augusta Larsson',earlier_record:R.ljungbacka402,earlier_row:9,
    earlier_role:'sömmerska',registered_arrival:'1914-10-15',arrival_from:'Engelbrekts församling',
    later_record:R.ture402,later_rows:[16,17],reported_spouse:'P-0046',registered_marriage:'1914-12-31',
    relation_to_subject:'sonhustru genom Ture',internal_reference:'Se här ofvan',
    physical_move_proven:false,wedding_place:null,
  },[at('P-0043','person',125),at('C-0911','citation',24,25),at('C-0911','citation',66,67),at('C-0911','citation',78,83)],
  [elin,'O-P-0046-A-4239-marriage_household'],
  'De interna hänvisningarna förbinder Elins r9 med makarnas egna r16–17. Sonhustrurelationen återger den befintliga familjesyntesen, inte ett ord i r9.',
  'Bokfört vigseldatum, inte ny läsning av en vigselpost. Elins moderskap ger inget biologiskt faderskap till Ture.');
  preserveTargets(elin,[elinF,'O-P-0046-A-4239-marriage_household']);cases.push({case:'B4',observation:elin,reuse:['O-P-0046-A-4239-marriage_household'],synthesis:elinF});

  // B5: the step-parent conclusion already exists at the conclusion layer.
  const hogsjo='O-P-0315-C0510-household', familyF='F-P-0315-family_context-six-known-children', step='REL-step-P-0405-P-0315';
  assert.equal(JSON.parse(current(familyF).value_json).stepmother,'P-0405');
  assert.equal(current(step).nature,'recorded_step_parent');
  revise(hogsjo,R.hogsjo,data=>{
    assert.equal(data.value_json.stepmother,'P-0405');delete data.value_json.stepmother;delete data.value_json.father;
    data.value_json.own_role_literal='son';data.value_json.household_head_literal='Nils Pehrsson';
    data.value_json.head_spouse_name_literal='Lisa Stina Jonsd:r';data.value_json.head_spouse_role_literal='h/2';
    data.value_literal=JSON.stringify(data.value_json);
  },'Hushållspostens son och h/2 bevaras som råroller. Styvmodersslutsatsen kräver korrelation med1836postens namngivna mor och återbrukas därför endast som befintlig F/relation.',
  [at('C-0510','citation',18,24),at('C-0510','citation',76)],
  'Egen familjegrupp lämnar sidan1858; de äldre makarna har egna1861noter. Sättna är senare prövningskandidat, ingen läst destination. Styvmodersrelationen återbrukas separat.');
  preserveTargets(hogsjo,[familyF,step,'O-P-0405-C0510-own','O-P-0315-C0509-birth']);
  cases.push({case:'B5',observation:hogsjo,reuse:[familyF,step,'O-P-0405-C0510-own','O-P-0315-C0509-birth']});

  // B6/B7: explicitly authorized two-row extension; no further discovery loop.
  for(const spec of [
    {case:'B6',n:122,oldRow:6,newRow:5,name:'Karl Harry',role:'fosterson',birth:'1906-09-07',place:'Nyköpings Östra',
      laterName:'Karl Harry Jansson',newO:'O-C0910-Karl-Harry-row5',F:'F-P-0043-family_context-Karl-Harry-sequence',cLines:[30,31]},
    {case:'B7',n:123,oldRow:7,newRow:6,name:'Karin Elisabet',role:'fosterdotter',birth:'1910-10-02',place:'Kila',
      laterName:'Karin Elisabet',newO:'O-C0910-Karin-Elisabet-row6',F:'F-P-0043-family_context-Karin-Elisabet-sequence',cLines:[32,32]},
  ]) {
    const id=`O-P-0043-related${spec.n}-household_role_report`;
    revise(id,R.ljungbacka402,data=>{
      assert(data.value_literal.includes('1914–1918'));
      data.value_json={row:spec.oldRow,name_literal:spec.name,role_literal:spec.role,reported_birth:spec.birth,
        birth_place:spec.place,registered_transfer:'1914-10-30',from_folio:420};
      data.value_literal=`${spec.role} ${spec.name}; ${spec.birth}, ${spec.place}; överförd med familjen från420 den1914-10-30.`;
    },`${spec.name}s tidigare fosterbarnsrad bevaras. Den senare1918hållpunkten${spec.n===122?' och modersanteckningen':''} hör till nästa bok och hålls skilda i egna O och F.`,
    [at('C-0911','citation',17,23)],'Egen rad på uppslag402, inte en sammanfattning av två böcker.');
    const later={row:spec.newRow,name_literal:spec.laterName,role_literal:'fb.',reported_birth:spec.birth,birth_place:spec.place};
    if(spec.n===122)later.mother_note_literal='Son till Elin Augusta Larsson-Jansson';
    observation(spec.newO,R.ljungbacka914,'household_fields',later,
      `fb. ${spec.laterName}; ${spec.birth}, ${spec.place}${spec.n===122?'; Son till Elin Augusta Larsson-Jansson':''}.`,
      [at('P-0043','person',spec.n),at('C-0910','citation',...spec.cLines)],
      'Egen rad på s914. Ingen ny P-identitet, ingen oavbruten faktisk omsorg och inget faderskap till Ture härleds.');
    fact(spec.F,'P-0043','family_context',{
      name:spec.name,relationship:'fosterbarn i hushållet',reported_summary_period:'1914–1918',
      registered_anchors:[{record:R.ljungbacka402,row:spec.oldRow,transfer:'1914-10-30'},
        {record:R.ljungbacka914,row:spec.newRow,book_period:'1916–1923',own_arrival_date:null}],
      ...(spec.n===122?{reported_mother:'Elin Augusta Larsson-Jansson',mother_basis_record:R.ljungbacka914}:{}),
      continuous_physical_care_proven:false,biological_parenthood_of_foster_household_proven:false,
    },[at('P-0043','person',spec.n),at('C-0911','citation',17,23),at('C-0910','citation',...spec.cLines)],
    [id,spec.newO],
    `${spec.name}s två bokföringshållpunkter hålls isär och den äldre relationsradens tidsföljd bevaras som kvalificerad syntes.`,
    '1914–1918 är aktens sammanfattning av källhållpunkter. Den senare raden har här ingen egen ankomstdag; ingen obruten fysisk vistelse påstås.');
    preserveTargets(id,[spec.newO,spec.F]);cases.push({case:spec.case,observation:id,newOwn:spec.newO,synthesis:spec.F});
  }

  // L1–L5: retain each witness's own locality, move only project epistemic metadata.
  const witnessF='F-P-0383-identity_boundary-own-baptism-witnesses';
  assert.equal(JSON.parse(current(witnessF).value_json).maternal_siblings_not_proven,true);
  for(const [suffix,place] of [['Britta-Anders','Mjöstan[?]'],['Britta-Erics','Kjerrbogärda'],['Kjerstin','Kåsegl[?]'],['Namndeman','Hattholt[?]'],['Olof','Wässenbo']]) {
    const id=`O-C0848-witness-${suffix}`;
    revise(id,R.svenBirth,data=>{
      assert.equal(data.value_json.home_literal,place);assert.equal(data.value_json.kinship_proven,false);
      delete data.value_json.kinship_proven;
    },`${suffix}: ${place} är postens egen ortuppgift. kinship_proven beskriver projektets släktskapsbedömning och återbrukas via befintlig F, inte som dopbokens råfält.`);
    preserveTargets(id,[witnessF]);cases.push({case:'L',observation:id,reuse:[witnessF]});
  }
  assert.deepEqual([...before.keys()].sort(),[...OBSERVATION_C_REVISIONS].sort());

  const alreadyMappedUnits=[];
  const unitDecisions=[...additions].map(([unit,{before:u,targets:extra}])=>{
    const old=db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=? ORDER BY target_id').all(unit).map(x=>x.target_id);
    if(u.target_id&&!old.includes(u.target_id))old.push(u.target_id);
    const targets=[...new Set([...old,...extra])].sort();
    if(targets.length===old.length){alreadyMappedUnits.push({unit,version:u.version,state:u.state,question:u.question,targets});return null;}
    return {unit,expectedVersion:u.version,state:u.state,target:u.target_id,targets,question:u.question,
      rationale:`${u.rationale}\nT-0663: bevarar alla tidigare mål och samma state/question; tillagda egna O/F håller den fulla innebörden nåbar efter postgränsrättelsen.`};
  }).filter(Boolean).sort((a,b)=>a.unit.localeCompare(b.unit));

  const dependencyReviews=[];
  for(const [id,old] of before) {
    const deps=db.prepare(`WITH RECURSIVE dependents(id) AS (
      SELECT revision_id FROM dependency WHERE basis_revision_id=?
      UNION SELECT d.revision_id FROM dependency d JOIN dependents p ON d.basis_revision_id=p.id
    ) SELECT DISTINCT c.object_id,c.id AS revision FROM dependents d JOIN revision r ON r.id=d.id
      JOIN current_revision c ON c.object_id=r.object_id ORDER BY c.object_id`).all(old.revision_id);
    for(const dep of deps) {
      assert.equal(dep.revision,`${dep.object_id}@1`,`Ändrat beroende kräver individuell prövning: ${dep.object_id}`);
      let rationale;
      if(dep.object_id===id.replace('O-C0848-witness-','EP-E-baptism-P-0383-'))rationale='Samma namngivna/anonyma vittne kvarstår på Svens egen doppost16/19feb1815 enligt C0848/C1016. Bara projektflaggan kinship_proven tas bort från O; ort, namn, post och witness-deltagande består.';
      else if(dep.object_id===witnessF)rationale='C0848/C1016 ger vittnesnamn/orter men bevisar inte släktskap. F:s kandidat- och släktskapsgränser kvarstår och är nu den rätta platsen för bedömningen; inget nytt samband accepteras.';
      else if(dep.object_id==='F-P-0383-source_scope-readings-and-life-limits')rationale='Denna F återbrukar vittnesbedömningen och anger fortsatt olösta egna livs-/släktfrågor. Att flytta kinship_proven ur rå-O ändrar ingen av dessa gränser eller källvägar.';
      else if(dep.object_id==='F-P-0513-source_assessment-witness-count-and-limits')rationale='P0513/A7500–7501 och C0848/C1016 är prövade: den skrivna listan saknar Hansson men stänger inte faderns släktvägar. De tre namngivna Anders-bärarna och den villkorliga Johannes-kandidaten är oförändrade; nämndemannens titel ger inte Olof en egen rättslig roll. F återbrukar P0383:s oförändrade vittnesbedömning samt O-C0848-father@1. Flytten av kinship_proven ur vittnenas råfält påverkar ingen av dessa avgränsningar.';
      else if(dep.object_id==='F-P-0514-source_assessment-witness-count-and-limits')rationale='P0514/A7591–7592 och C0848/C1016 är prövade: Britta Erics Dotr är inte en Anders-bärare. Två namngivna Anders-döttrar plus Olof Anderss. ger tre; Johannes blir bara en villkorlig fjärde, aldrig en femte säker bärare. Namnmönstret bevisar varken syskonrelationer eller statistiskt överskott. F återbrukar P0383:s oförändrade vittnesbedömning samt O-C0848-mother@1. Ingen av slutsatserna beror på att kinship_proven stod i rå-O.';
      else throw Error(`Ny oberoende beroendeprövning krävs: ${id} → ${dep.object_id}`);
      const retained=current(dep.object_id);
      dependencyReviews.push({changedObject:id,beforeRevision:old.revision_id,afterRevision:`${id}@2`,affectedObject:dep.object_id,
        affectedRevision:dep.revision,affected_revision_id:dep.revision,changed_revision_id:`${id}@2`,
        outcome:'retain_existing_revision',rationale:`${rationale} Den befintliga slutsatsrevisionen och dess uttryckliga äldre beläggsbindningar behålls efter denna individuella prövning; detta är ingen ombindning till O@2.`,
        retainedPayloadHash:sha(canonical(payload(retained))),
        retainedEvidenceBindings:db.prepare('SELECT basis_revision_id,role,note FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role').all(dep.revision)});
    }
  }
  assert.equal(dependencyReviews.length,25,'Ändrad beroendemängd kräver individuell prövning');
  const preservedRevisions=[...new Set([...before.values()].map(x=>x.revision_id).concat(dependencyReviews.map(x=>x.affectedRevision)))].sort().map(id=>{
    const revision=db.prepare('SELECT r.*,o.kind FROM revision r JOIN object o ON o.id=r.object_id WHERE r.id=?').get(id);
    const row=db.prepare(`SELECT * FROM ${revision.kind} WHERE revision_id=?`).get(id);
    const origins=db.prepare('SELECT * FROM origin WHERE revision_id=? ORDER BY unit_id').all(id);
    const dependencies=db.prepare('SELECT * FROM dependency WHERE revision_id=? ORDER BY basis_revision_id,role').all(id);
    return {id,sha256:sha(canonical({revision,payload:row,origins,dependencies}))};
  });
  return {changes,spans:[...spans.values()],unitDecisions,dependencyReviews,review:{
    task:'T-0663',part:'c',mode:'read-only-proposal',audit:'genealogy2/verification/T-0663-observation-boundary-audit-c.md',
    originalSignals:33,authorizedExtraSignals:2,boundaryCorrections:7,assessmentFieldCorrections:5,
    unchangedClearedSignals:23,cases,proposedRevisions:OBSERVATION_C_REVISIONS,
    noApply:true,noNewPersonOrRelationship:true,unitStateAndQuestionPreserved:true,preservedRevisions,alreadyMappedUnits,
    baseline:before.size,proposalHash:sha(canonical({changes,spans:[...spans.values()],unitDecisions,dependencyReviews})),
  }};
}
