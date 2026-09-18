import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
import {DatabaseSync} from 'node:sqlite';
import {readCurrent,head} from '../lib/domain.mjs';
import {canonical,sha} from '../lib/archive.mjs';

// Explicit, bounded review builder. It never applies an operation or writes SQL.
export function buildObservationA(db) {
  const changes=[],cases=[],documents=new Map(),addedTargets=new Map(),dependencyReviews=[];
  const get=id=>{const x=readCurrent(db,id);if(!x)throw Error(`Saknat återbruk: ${id}`);return x;};
  const payload=x=>{const d={...db.prepare(`SELECT * FROM ${x.kind} WHERE revision_id=?`).get(x.revision_id)};delete d.revision_id;for(const k of Object.keys(d))if(k.endsWith('_json')&&d[k]!=null)d[k]=JSON.parse(d[k]);return d;};
  const proposed=id=>changes.find(x=>x.id===id);
  const version=id=>{const p=proposed(id);return p?(p.expectedVersion??0)+1:get(id).version;};
  const evidence=(id,role='supports',note='Samma bevarade underlag; inget nytt oberoende vittnesmål.')=>({object:id,version:version(id),role,note});
  const oldOrigins=x=>x.origins.map(o=>({unit:o.unit_id,coverage:o.coverage,note:o.note}));
  const mergeOrigins=(...groups)=>[...new Map(groups.flat().map(o=>[o.unit,o])).values()];
  const citation=(cid,start=1,end=null)=>{
    const d=db.prepare('SELECT d.* FROM document d JOIN legacy_entity e ON e.document_path=d.path WHERE e.id=? AND e.kind=?').get(cid,'citation');
    if(!d)throw Error(`Saknad citation ${cid}`);
    const last=d.text.replace(/\n$/,'').split('\n').length;
    const u=db.prepare('SELECT * FROM unit WHERE document_path=? AND start_line<=? AND end_line>=? ORDER BY end_byte-start_byte,id LIMIT 1').get(d.path,start,end??last);
    if(!u)throw Error(`Saknat befintligt ursprungsspann ${cid}:${start}–${end??last}`);
    documents.set(d.path,{path:d.path,sha256:d.sha256});
    return {unit:u.id,coverage:'partial',note:`Hela ${cid} inklusive senare tillägg är läst; detta ursprung bevarar befintlig text, ingen ny bildläsning.`};
  };
  const add=x=>{if(proposed(x.id))throw Error(`Dubbelt ändrings-id ${x.id}`);if((head(db,x.id)?.version??null)!==x.expectedVersion)throw Error(`Versionskonflikt ${x.id}`);changes.push(x);return x.id;};
  const reviseO=(id,value,{rationale,caveat,literal,origins=[],ownEvidence=null,record=null})=>{
    const x=get(id);if(x.version!==1||x.kind!=='observation')throw Error(`O-baslinje ändrad ${id}@${x.version}`);
    if(record&&x.record_id!==record)throw Error(`Postgräns ändrad ${id}`);
    const data={...payload(x),value_json:value,value_literal:literal??JSON.stringify(value)};
    const ev=ownEvidence??[x.record_id,...(x.mention_id?[x.mention_id]:[])];
    add({id,kind:'observation',expectedVersion:1,data,disposition:x.disposition,evidenceStatus:x.evidence_status,rationale,caveat,origins:mergeOrigins(oldOrigins(x),origins),evidence:ev.map(r=>evidence(r,r===x.mention_id?'derived_from':'supports'))});
    return id;
  };
  const newO=(id,record,property,value,origins,rationale,caveat,literal)=>add({id,kind:'observation',expectedVersion:null,data:{record_id:record,mention_id:null,property,value_json:value,value_literal:literal??JSON.stringify(value)},disposition:'recorded',evidenceStatus:'TRANSCRIBED',rationale,caveat,origins,evidence:[evidence(record)]});
  const fact=(id,subject,property,value,origins,bases,rationale,caveat,status='TRANSCRIBED')=>add({id,kind:'fact',expectedVersion:null,data:{subject_id:subject,property,value_type:'structured',value_json:value},disposition:'accepted',evidenceStatus:status,rationale,caveat,origins,evidence:bases.map(r=>evidence(r))});
  const addCase=(id,old,targets,rationale,citations)=>{
    const x=get(old),m=proposed(old);
    const units=db.prepare('SELECT t.unit_id FROM current_unit_target t WHERE t.target_id=? ORDER BY t.unit_id').all(old);
    for(const {unit_id} of units){if(!addedTargets.has(unit_id))addedTargets.set(unit_id,new Set());for(const t of targets)addedTargets.get(unit_id).add(t);}
    cases.push({id,observation:old,expectedVersion:x.version,record:x.record_id,before:payload(x),after:m.data,rationale,citations,comparisonTargets:targets,unitTargets:units.map(({unit_id})=>{
      const u=db.prepare('SELECT id,owner_id,kind,legacy_id,document_path,start_line,end_line FROM unit WHERE id=?').get(unit_id);return u;
    })});
  };
  const R={children15:'R-54b9a43526242cc9adee6c31',children86:'R-83ce4c405b6733bac7afd35c',bjerg4:'R-8a83ee945b26cabe321fb1ab',bjerg5:'R-fbd26dd590e542972a5cabbb',census1900:'R-12cfa4b0cfebd9409730fcb8',census1910:'R-9fcd6c77fb3fbdc8a110e24b',arne1915:'R-70eeff109bc651dce649a0ee',adaOriginal:'R-dc7d8a2eba63d983a98e6aa5',adaSCB:'R-0d1c75412788b5465ccb5bd3',death:'R-3f36aa1ea9e58476d9dd64da',census1930:'R-d2dae342a01c14af474e5fbf',stina6:'R-7d99e8402017d41b9b04f1e7',carolina:'R-827a4773eba203536d07a963',nils:'R-0910fc8b720c8388a94edf9f'};

  // 1. Three children in the earlier household, four in the later household.
  const children='O-P-0027-children-book-sequence',childrenF='F-P-0027-household_comparison-children-book-sequence';
  const childrenOrigins=mergeOrigins(oldOrigins(get(children)),[citation('C-0868'),citation('C-0871')]);
  const childrenWhy='A II a/15 s.15 och nästa bok s.86 är två avgränsade poster. Gunilla Birgitta står på s.86; s.15-observationen begränsas till de tre barn som A5222 lokaliserar där.';
  reviseO(children,{s15:['Lars Olof','Barbro Margareta','Björn Flemming']},{record:R.children15,rationale:childrenWhy,caveat:'Namn i det äldre hushållet enligt A5222. Barnens egna datum och senare fält är minimerade eller outvunna; inga sådana kolumner förklaras tomma.',origins:childrenOrigins,literal:'Lars Olof, Barbro Margareta och Björn Flemming i hushållet på sida15.'});
  for(const id of ['O-P-0296-C0871-child','O-P-0297-C0871-child','O-P-0373-C0871-head'])if(get(id).record_id!==R.children86)throw Error(`Fel s86-återbruk ${id}`);
  fact(childrenF,'P-0027','household_comparison',{earlier_record:R.children15,earlier_children:['Lars Olof','Barbro Margareta','Björn Flemming'],later_record:R.children86,later_children:['Lars Olof','Barbro Margareta','Björn Flemming','Gunilla Birgitta'],later_addition:'Gunilla Birgitta',known_children:4,exhaustive_lifetime_child_list:false,exact_child_dates_minimized:true,independent_information_paths:false},childrenOrigins,[children,'O-P-0296-C0871-child','O-P-0297-C0871-child','O-P-0373-C0871-head'],childrenWhy,'Samma administrativa kedja. Bokperioder daterar inte varje barn eller bevisar överlevnad till bokslut. En folkräkningsfrånvaro ger inte ensam säker födelsegräns.');
  addCase('a01',children,[childrenF],childrenWhy,['C-0868','C-0871','P-0027/A-5222']);

  // 2–4. Bjerg: each book retains its own children and dates; one synthesis owns comparisons.
  const grouping='O-P-0021-bjerg-first-marriage',dates='O-P-0021-household-date-variants',thilda='O-P-0021-Thilda-household-row';
  const bjergF='F-P-0021-household_comparison-Bjerg-AI4-AI5',dates4='O-P-0021-C0999-child-date-reports';
  const bjergOrigins=mergeOrigins(...[grouping,dates,thilda].map(id=>oldOrigins(get(id))),[citation('C-0991'),citation('C-0999')]);
  const groupValue=JSON.parse(get(grouping).value_json);if(!groupValue.group.includes('Thilda Augusta'))throw Error('Thildabaslinje ändrad');groupValue.group=groupValue.group.filter(n=>n!=='Thilda Augusta');
  const groupWhy='C0991:s AI/5-rader3–6 har fyra barn i förstaäktenskapsgruppen. Thilda är endast belagd i föregående AI/4 och flyttas ur AI/5-råvärdet till jämförelsen.';
  reviseO(grouping,groupValue,{record:R.bjerg5,rationale:groupWhy,caveat:get(grouping).caveat,origins:[citation('C-0991')],literal:'Mannens barn i 1sta äktenskapet: Carl Johan, Emma Charlotta, Anna Sofia, Augusta Victoria.'});
  const values4={CarlJohan:'1850-07-19',AnnaSofia:'1857-06-02',VictorAlbin:'1874-11-13'},values5={CarlJohan:'1850-04-24',AnnaSofia:'1857-06-24',VictorAlbin:'1874-11-03'};
  const datesWhy='De tre alternativparen var jämförelser mellan C0999/AI4 och C0991/AI5. Varje råobservation återger nu endast sin egen bok; ingen faktisk födelsedag avgörs.';
  reviseO(dates,values5,{record:R.bjerg5,rationale:datesWhy,caveat:'AI/5:s rapporterade dagar för tre olika barn. Personernas faktiska födelsedagar avgörs inte av denna postgränsrättelse.',origins:[citation('C-0991')]});
  newO(dates4,R.bjerg4,'reported_child_birth_dates',values4,[citation('C-0999')],datesWhy,'Tre namngivna rader inom samma hushåll. Ingen ny person eller accepterad födelsehändelse skapas.');
  const thildaValue=JSON.parse(get(thilda).value_json);delete thildaValue.nextBookAbsent;
  const thildaWhy='Thildas rad och strykning finns i AI/4, medan frånvaron gäller nästa boks namngivna hushåll. Den senare frånvaron hör till en jämförelse med båda posterna.';
  reviseO(thilda,thildaValue,{record:R.bjerg4,rationale:thildaWhy,caveat:'Familjeroll i förstaäktenskapsgruppen; egen födelsepost oläst. Strykningen är ingen egen dödsuppgift. Ingen ny person eller biologisk syskonrelation.',origins:[citation('C-0999')],literal:'Thilda Augusta 12/10 1861, överstruken.'});
  fact(bjergF,'P-0021','household_comparison',{AI4:{record:R.bjerg4,first_marriage_group:['Carl Johan','Emma Charlotta','Anna Sofia','Thilda Augusta','Augusta Victoria'],dates:values4},AI5:{record:R.bjerg5,first_marriage_group:groupValue.group,later_children:groupValue.laterChildren,dates:values5},Thilda_absent_from_AI5:true,Thilda_death_inferred:false,biological_parentage_resolved:false,biological_full_siblings_proven:false,selected_birth_dates:null,Augusta_date_repetition_hypothesis:'withdrawn; Anna Sofia differs between books and Augusta has her own birth record'},bjergOrigins,[grouping,dates,dates4,thilda,'O-P-0021-mother-marriage-household'],datesWhy+' '+groupWhy+' '+thildaWhy,'Klamrarna är bokförda familjegrupper, inte biologisk fullsyskonlista. Frånvaro/strykning ger ingen dödsdag. Den avvisade avskriftsupprepningen återaktiveras inte.');
  addCase('a02',grouping,[bjergF],groupWhy,['C-0991','C-0999']);
  addCase('a03',dates,[dates4,bjergF],datesWhy,['C-0991','C-0999']);
  addCase('a04',thilda,[bjergF],thildaWhy,['C-0991','C-0999']);

  // 5. The census reports remain distinct, with their shared provenance preserved.
  const year='O-P-0020-C0025-birth1858',year1910='O-P-0020-C0026-birth1850',yearF='F-P-0020-source_conflict-census1900-1910-birth-years';
  const yearOrigins=mergeOrigins(oldOrigins(get(year)),[citation('C-0025'),citation('C-0026')]);
  const yearWhy='1900-bladets egen födelseårscell är58;50 står på1910-bladet. Båda avvikande bladläsningarna bevaras utan att1910-värdet tillskrivs1900-posten.';
  reviseO(year,{year:1858},{record:R.census1900,rationale:yearWhy,caveat:'Rå58 är läst i1900-bilden, inte enbart registeruppgift. Ingen fastställd personfödelse ändras.',origins:[citation('C-0025')],literal:'58'});
  newO(year1910,R.census1910,'birth_year',{year:1850},[citation('C-0026')],yearWhy,'1910-bladets rapporterade fadersår. Utdrag ur samma församlingsbokskedja som1900; ingen extra oberoende röst.','50');
  fact(yearF,'P-0020','source_conflict',{father:{census1900:{raw:'58',year:1858},census1910:{raw:'50',year:1850}},mother:{census1900:{raw:'67',year:1867},census1910:{raw:'63',year:1863}},same_parish_book_extract_chain:true,independent_votes:false,systematic_transfer_error:'possible hypothesis; not established',accepted_birth_date_revised:false},yearOrigins,[year,year1910,R.census1900,R.census1910],yearWhy,'Båda föräldrarnas parallella avvikelse bevaras. Samma administrativa kedja avgör inte felorsaken. P0020:s belagda1850-03-18 omprövas inte här.','CONFLICT');
  addCase('a05',year,[year1910,yearF],yearWhy,['C-0025','C-0026']);

  // 6. The mother's 1886 birth is not raw text in her child's 1915 record.
  const ada='O-P-0003-C0008-mother-birth-corrected',adaF='F-P-0009-source_comparison-C0008-birth-reading';
  const adaOrigins=mergeOrigins(oldOrigins(get(ada)),[citation('C-0008'),citation('C-0014'),citation('C-0016')]);
  const adaWhy='1915-postens moderfält läses86 19/8[?]; Lerbo och det säkra1886-datumet kommer från moderns egen originalpost/beroende SCB-utdrag. Personsyntesen flyttas tillF.';
  reviseO(ada,{date_literal:'86 19/8[?]',date_selected:null,rejected_reading_literal:'86 8/8'},{record:R.arne1915,rationale:adaWhy,caveat:'Samma cells läshistorik:19/8 är förenligt med den täta handen. Ingen födelseort för modern är utvunnen ur denna post. Hennes etablerade födelse avgörs separat.',origins:[citation('C-0008')],literal:'86 19/8[?]; äldre läsning86 8/8 återtagen.'});
  fact(adaF,'P-0009','source_comparison',{child_birth_record:R.arne1915,mother_birth_reading_in1915:'86 19/8[?]',rejected_initial_reading:'86 8/8',own_birth_event:'E-birth-P-0009',own_birth_date:'1886-08-19',own_birth_parish:'Lerbo',own_original_record:R.adaOriginal,dependent_SCB_record:R.adaSCB,SCB_independent_of_original:false,Lerbo_written_in_child1915_record:false},adaOrigins,[ada,'E-birth-P-0009',R.adaOriginal,R.adaSCB],adaWhy,'Original och SCB är beroende återgivningar. Befintlig1886-födelsehändelse återbrukas; ingen ny person eller födelse skapas. Spånga/Gånga är föräldrahemvistens separata källskillnad.');
  addCase('a06',ada,[adaF,'E-birth-P-0009'],adaWhy,['C-0008','C-0014','C-0016','P-0003/A-0045']);

  // 7. Page comparisons explain a reading but are not raw fields of death post3.
  const death='O-P-0368-C0559-death',deathF='F-P-0368-source_assessment-C0559-control-rows';
  const deathValue=JSON.parse(get(death).value_json);delete deathValue.comparison_row10_field_filled;delete deathValue.initial_N_comparisons;
  const deathWhy='R avgränsar HögbyF/2 post3. Kontrollrader2/6/10 är läsargument på andra rader; de bevaras iF medan post3:s egna döds-/begravnings- och anteckningsfält består.';
  reviseO(death,deathValue,{record:R.death,rationale:deathWhy,caveat:get(death).caveat,origins:[citation('C-0559')]});
  fact(deathF,'P-0368','source_assessment',{target_record:R.death,target_post:3,comparison_row10_field_filled:true,comparison_field:'Dödsattest af läkare/barnmorska',initial_N_comparisons:['rad2 Nils Peter Olsson','rad6 Nils Peter Simonsson'],initial_N_compatible:true,remaining_place_letters_unresolved:true,sanatorium_place_selected:null,control_people_created:false},mergeOrigins(oldOrigins(get(death)),[citation('C-0559',70,90)]),[death,R.death],deathWhy,'Kontrollpersonerna namnges endast som handstilsjämförelse i den bevarade källtexten; inga nyaR/personer skapas. InledandeN avgör inte Nässjö. Tomt eget attestfält bevisar inte att läkare eller intyg aldrig funnits.');
  addCase('a07',death,[deathF],deathWhy,['C-0559','P-0368/A-7913']);

  // 8. A later reservation in the same cell must survive the migration.
  const code='O-P-0021-census-1930',codeValue=JSON.parse(get(code).value_json);
  if(codeValue.occupationCode!=='3-103-21')throw Error('Kodbaslinje ändrad');
  codeValue.occupationCode=null;codeValue.occupationCodeReadings=['3-103-21','2-102-21'];codeValue.occupationCodeChosen=null;
  const codeWhy='C0417/T0151 reserverar samma huvudyrkescell mellan3-103-21 och2-102-21. Det äldre ensamma råvärdet var för säkert; ingen ny post eller yrkestolkning tillkommer.';
  reviseO(code,codeValue,{record:R.census1930,rationale:codeWhy,caveat:get(code).caveat+' Huvudyrkeskoden är olöst mellan de två bevarade läsningarna; ingen av dem väljs.',origins:[citation('C-0417')],literal:'änkan Eliasson Johansson; Kyrkefalla1863; Värsås1930; huvudyrkeskod3-103-21 eller2-102-21, ej avgjord; skolbildning3; inkomst/förmögenhet5 —'});
  addCase('a08',code,[],codeWhy,['C-0417/T-0151']);

  // 9. Sättna was transferred from AI7 into an AI6 observation without own extraction.
  const stina='O-P-0344-C0836-s92',stinaF='F-P-0344-source_scope-AI6-birthplace-transfer';
  const stinaValue=JSON.parse(get(stina).value_json);if(stinaValue.birthplace!=='Sättna')throw Error('Sättnabaslinje ändrad');delete stinaValue.birthplace;
  const stinaWhy='C0831 lokaliserar Sättna tillAI/7 s.94. C0836 och A6465 ger namn/datum påAI/6 s.92 men ingen egen ortutvinning. Den överförda orten tas bort frånAI6-råvärdet.';
  reviseO(stina,stinaValue,{record:R.stina6,rationale:stinaWhy,caveat:'Ingen egen födelseort är utvunnen förAI/6 s.92 i detta underlag. Sättna finns iAI/7 och hennes födelseunderlag. Ingen s.92-cell har nygranskats eller bevisats tom. Bokperioden daterar ingen inflyttning.',origins:[citation('C-0836')]});
  fact(stinaF,'P-0344','source_scope',{AI6_record:R.stina6,AI6_birthplace_not_extracted:true,AI7_record:'R-e8a90d1636c6a21bedbb8072',AI7_reported_birthplace:'Sättna',removed_AI6_imported_value:'Sättna',person_birthplace_redecided:false,additional_independent_source_created:false},mergeOrigins(oldOrigins(get(stina)),[citation('C-0831'),citation('C-0836')]),[stina,'O-P-0344-C0346-s94','O-P-0344-C0830-birth'],stinaWhy,'C1012:s kolumnredovisning gäller s.185 i samma volym, inte en ny kontroll av s.92. Den etablerade personfödelsen ändras inte.');
  addCase('a09',stina,[stinaF],stinaWhy,['C-0831','C-0836','P-0344/A-3192','P-0344/A-6465']);

  // 10. The husband's separate row is context for Carolina's H.-row.
  const carolina='O-P-0362-C1013-rejected-Carolina',carolinaF='F-M-C1013-Carolina-household-context';
  const carolinaWhy='CarolinasR avgränsar endast hennes egen rad. Nils Danielssons namn finns på ett separat redan avgränsatR. Makens namn och identitetsavvisningen bevaras som bedömning utanför råvärdet.';
  reviseO(carolina,{birth_literal:'29 17/12',birth_parish:'Rönö',household:3},{record:R.carolina,rationale:carolinaWhy,caveat:'EgenH.-rad i tredje hushållet. Familjejämförelsen och avvisadP0313-identitet återges i egna bedömningar; inget nytt målpersonshushåll.',origins:[citation('C-1013',58,60)]});
  fact(carolinaF,'M-P-0362-C1013-rejected-Carolina','source_assessment',{household:3,page:55,reported_spouse_name:'Nils Danielsson',spouse_name_record:R.nils,own_role_literal:'H.',rejected_identity_target:'P-0313',rejection_object:'ID-P-0313-not-C1013-Carolina',new_person_created:false,new_pedigree_relation_created:false},mergeOrigins(oldOrigins(get(carolina)),[citation('C-1013',58,60)]),[carolina,R.nils,R.carolina],carolinaWhy,'Samma sida men separata personrader. Uppgiften ger ingen ny personkärna, släktkant eller utvidgning av CarolinasR.');
  addCase('a10',carolina,[carolinaF,'ID-P-0313-not-C1013-Carolina'],carolinaWhy,['C-0846','C-1013']);

  // Individually reviewed downstream conclusions. Payload/status/disposition are unchanged.
  const followups=[
    ['F-P-0373-source_correction-wife-fields-already-known',[childrenF],'Barnföljden tre/fyra är oförändrad och får nu korrekt stöd genom separata poster och jämförelseF. Vigsel, lysning, rubrik och yrkes-/inkomstfält är opåverkade.'],
    ['F-P-0373-source_scope-screenshots-and-unread-columns',[childrenF],'Samma bevarade skärmbilder och outvunna egna kolumner. Flyttad barnjämförelse ändrar varken kopiekvalitet, dataminimering eller förbudet att härleda födelsetid ur hushållsfrånvaro.'],
    ['F-P-0373-life_scope-occupation-and-book-period',[],'Transitiv följd: fyra kända barn består genom korrekt jämförelse; bokslut ger fortsatt ingen livsgräns och yrkes-/ursprungsluckorna ändras inte.'],
    ['E-death-P-0368',[],'Post3 har fortsatt uttrycklig dödsdag1895-01-14. KontrollradersN/attesttecken behövs inte för datumet; eventets datum, platsroll, status och personkoppling består.'],
    ['E-burial-P-0368',[],'Post3 har fortsatt uttrycklig begravningsdag1895-01-25. Ingen fysisk gravplats var utvunnen; kontrollradernas flytt tillF ändrar inget händelsefält.'],
    ['EP-E-death-P-0368-P-0368-principal',[],'SammaO/M identifierar den avlidne och sammaE bär oförändrat datum. Deltagarens person, omnämnande och roll består.'],
    ['EP-E-burial-P-0368-P-0368-principal',[],'Samma person och egenpost bär begravningsdeltagandet; inga kontrollpersoner ingår. E/M/person/roll består.'],
    ['F-P-0368-life_scope-raw-death-note-and-open-middle',[deathF],'Egen rättad transportnot, elva dagars intervall och samtliga livsluckor består. Kontrollargument finns iF; inget säkert sanatorium, namngiven hämtare eller läkarnärvaro härleds.'],
    ['F-P-0368-name_scope-Adelbert-Adalbert',[],'Namnformerna hör till oförändrade egnaM/postuppgifter. De flyttadeNils-jämförelserna gäller ortens begynnelsebokstav och ändrar inte Carlmans namnvarianter.'],
    ['ID-P-0313-not-C1013-Carolina',[carolinaF],'CarolinaCarlsdotter1829/Rönö/H. är fortsatt en annan än dotternCarolinaLarsdotter1849. Makens namn behövs inte för avvisningen; rejected/REJECTED består.'],
    ['SEARCH-P-0362-C1013-page55',[carolinaF],'Den lästa sidan55 har samma tre hushåll/fjorton rader och saknar målparets namn. Flyttat makenamn ändrar inte sidnollan eller dessS0661-scope.'],
    ['F-P-0362-life_scope-secure-father-open-origin',[],'Transitiv följd: sid55-identiteten förblir avvisad. Positiv fadersroll1849 och samtliga öppna egna födelse-/döds-/ursprungsfält är opåverkade.'],
    ['F-P-0362-source_scope-corrected-searches-and-copy-debt',[],'Transitiv följd: sidnollans gräns består. Övriga födelsebildfönster, vigselomfång och saknade kopior är oförändrade; ingen ny sökning är gjord.'],
    ['F-P-0363-life_scope-mother-widow-and-unread-consent',[],'Transitiv följd: MajaLenas avvisade1814-kandidat återaktiveras inte. Namngiven mor1849, änka/tillstånd1870 och dokumentets olästa karaktär är opåverkade.']
  ];
  for(const [id,extra,why] of followups){
    const x=get(id);if(x.version!==1)throw Error(`Beroende kräver ny individuell prövning: ${id}@${x.version}`);
    const ev=x.evidence.map(e=>{const b=db.prepare('SELECT object_id,version FROM revision WHERE id=?').get(e.basis_revision_id);if(!proposed(b.object_id)&&head(db,b.object_id).version!==b.version)throw Error(`Äldre sidobelägg kräver prövning: ${id}→${e.basis_revision_id}`);return evidence(b.object_id,e.role,e.note);});
    for(const e of extra)if(!ev.some(v=>v.object===e))ev.push(evidence(e));
    const p=payload(x);
    add({id,kind:x.kind,expectedVersion:1,data:p,disposition:x.disposition,evidenceStatus:x.evidence_status,rationale:'T-0663, individuell beroendegranskning: '+why,caveat:x.caveat,origins:oldOrigins(x),evidence:ev});
    dependencyReviews.push({object:id,expectedVersion:1,outcome:'rebind_unchanged_payload',rationale:why,payloadHash:sha(canonical(p)),disposition:x.disposition,evidenceStatus:x.evidence_status,evidence:ev});
  }
  // Resolve intra-operation bindings to final versions, then order dependencies before users.
  for(const x of changes)for(const e of x.evidence)e.version=version(e.object);
  for(const r of dependencyReviews)r.evidence=proposed(r.object).evidence;
  const pending=[...changes],ordered=[];
  while(pending.length){const i=pending.findIndex(x=>x.evidence.every(e=>!pending.some(y=>y.id===e.object)));if(i<0)throw Error('Cykel i ändringsbelägg');ordered.push(...pending.splice(i,1));}
  const unitDecisions=[];
  for(const [unit,extra] of addedTargets){if(!extra.size)continue;const before=db.prepare('SELECT * FROM current_unit_decision WHERE unit_id=?').get(unit);if(!before)throw Error(`Beslut saknas ${unit}`);
    const old=db.prepare('SELECT target_id FROM current_unit_target WHERE unit_id=? ORDER BY target_id').all(unit).map(x=>x.target_id);
    const targets=[...new Set([...old,...extra])].sort();if(targets.length===old.length)continue;
    unitDecisions.push({unit,expectedVersion:before.version,state:before.state,target:before.target_id,targets,question:before.question,rationale:before.rationale+'\nT-0663: råposterna avgränsas; samtliga äldre mål bevaras och jämförelse-/återbruksmål tillförs så hela sakinnebörden fortfarande kan nås.'});
  }
  // Any new unreviewed downstream object blocks delivery rather than being silently approved.
  const reviewed=new Set(followups.map(x=>x[0]));
  for(const c of cases){const deps=db.prepare(`WITH RECURSIVE ds(id) AS (SELECT revision_id FROM dependency WHERE basis_revision_id=? UNION SELECT d.revision_id FROM dependency d JOIN ds ON d.basis_revision_id=ds.id) SELECT DISTINCT cr.object_id FROM ds JOIN revision r ON r.id=ds.id JOIN current_revision cr ON cr.object_id=r.object_id`).all(c.observation+'@1').map(x=>x.object_id);
    c.dependents=deps;for(const id of deps)if(!reviewed.has(id)&&!proposed(id))throw Error(`Ogranskat beroende efter ny införsel: ${c.observation}→${id}`);
  }
  const review={schema:'T-0663-observation-a-review/1',preparedOnly:true,scope:'10 individuella observationsrättelser; gamla revisioner och alla beslutade personfakta bevaras.',sourceDocuments:[...documents.values()].sort((a,b)=>a.path.localeCompare(b.path)),cases,dependencyReviews,changeCount:ordered.length,unitDecisionCount:unitDecisions.length};
  return {changes:ordered,unitDecisions,dependencyReviews,review};
}

if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  const db=new DatabaseSync(process.argv[2]??'genealogy2/data/research.sqlite',{readOnly:true});
  try {const result=buildObservationA(db);fs.writeFileSync('genealogy2/migration/T-0663-observation-a-review.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({preparedOnly:true,cases:result.review.cases.length,changes:result.changes.length,unitDecisions:result.unitDecisions.length,dependencyReviews:result.dependencyReviews.length}));}finally{db.close();}
}
