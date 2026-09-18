import {sha} from '../lib/archive.mjs';

export const PILOT_PEOPLE=['P-0016','P-0110','P-0111','P-0113','P-0114','P-0532','P-0007','P-0015','P-0027','P-0424','P-0028','P-0004'];
export function buildPilot(db) {
  const request={id:'T-0641/pilot-v1',actor:'Codex/T-0641',reason:'Avgränsad konvertering av redan utförd forskning. Ingen ny arkivläsning eller uppgradering av säkerhet.',spans:[],changes:[],mappings:[]};
  const entity=(id,kind)=> {
    const e=db.prepare('SELECT e.*,d.text,d.sha256,d.bytes FROM legacy_entity e JOIN document d ON d.path=e.document_path WHERE e.id=? AND e.kind=?').get(id,kind);
    if(!e)throw Error(`Saknat pilotunderlag: ${id}/${kind}`);return e;
  };
  const section=(id,title,kind=id.startsWith('C-')?'citation':'person')=> {
    const e=entity(id,kind);
    const matches=db.prepare("SELECT * FROM unit WHERE document_path=? AND kind='section' AND section LIKE ?").all(e.document_path,title);
    if(matches.length!==1)throw Error(`Avsnitt måste vara entydigt: ${id}/${title}: ${matches.length}`);return matches[0];
  };
  const assertion=id=> {
    const row=db.prepare('SELECT u.* FROM legacy_assertion a JOIN unit u ON u.id=a.unit_id WHERE a.id=?').get(id);
    if(!row)throw Error(`Saknad A-rad: ${id}`);return row;
  };
  function span(e,start=0,end=e.bytes,label='hela dokumentet') {
    const id=sha(`${e.document_path}\0${e.sha256}\0curated_span\0${start}\0${end}`);
    if(!request.spans.some(s=>s.id===id))request.spans.push({id,path:e.document_path,sha256:e.sha256,start,end,owner:e.id??null,section:label});
    return {id};
  }
  const origins=(units,coverage='partial')=>units.map(u=>({unit:u.id,coverage,note:'Återanvänt underlag, inte ett nytt oberoende vittnesmål.'}));
  const evidence=(ids,role='supports')=>ids.map(object=>({object,version:1,role,note:'Explicit beroende; ingen automatisk oberoenderäkning.'}));
  function add(id,kind,data,units,rationale,extra={}) {
    request.changes.push({id,kind,expectedVersion:null,disposition:'accepted',rationale,caveat:'',data,origins:origins(units),...extra});
    return id;
  }
  const exact=(value,literal=value)=>({precision:'exact',value,literal});
  const unknown=()=>({precision:'unknown',literal:'Ingen säker datering angiven för relationens början/slut.'});

  for(const id of PILOT_PEOPLE) {
    const e=entity(id,'person'),identity=section(id,'Identitet');
    add(id,'person',{display_name:e.title.replace(/^P-\d{4}:\s*/,''),sex:null,legacy_state:id==='P-0424'?'retired':'active'},[identity],
      id==='P-0424'?'Verklig separat person; den gamla aktens avveckling gäller den felaktiga ankopplingen.':'Återanvänder etablerad personidentitet; inget kön gissas ur namn eller rollord.');
  }
  for(const id of ['S-0061','S-0062','S-0343','S-0760','S-0024','S-0199']) {
    const e=entity(id,'source');
    add(id,'source',{title:e.title,archive_reference:null,source_class:null,description:e.text},[span(e)],'Befintlig källbeskrivning återanvänds ordagrant; arkivfält som ännu inte konverterats står kvar i beskrivningen.',{disposition:'recorded'});
  }
  const raw75=section('C-0075','Diplomatisk arbetsavskrift'),fix75=section('C-0075','Tillägg T-0125%'),place75=section('C-0075','Tillägg T-0182%');
  const raw94=section('C-0094','Diplomatisk arbetsavskrift'),fix94=section('C-0094','Tillägg T-0143%');
  const raw79=section('C-0979','Diplomatisk avskrift'),fix79=section('C-0979','Tillägg T-0125%');
  const raw76=section('C-0976','Diplomatisk avskrift'),fix76=section('C-0976','Tillägg T-0125%');
  const raw28=section('C-0028','Diplomatisk arbetsavskrift');
  const raw252=section('C-0252','Avskrift');
  const records=[
    ['R-C0075-29','S-0061','birth_baptism','Gryt C/6, 1877 nr 29, bild A0015920_00015',[raw75,fix75]],
    ['R-C0094-85-86','S-0062','arrival','Gryt B/2, 1874 nr 85–86, bild A0016344_00037; inte Adelas nr 84',[raw94,fix94]],
    ['R-C0979-46','S-0343','departure','Hyltinge B/4, utflyttade 1902 nr 46, s.32, bild 00154512_00036',[raw79,fix79]],
    ['R-C0976-banns86','S-0760','banns','Adolf Fredrik E I/17, 1903 nr 86, bild 00028353_00045',[raw76,fix76]],
    ['R-C0976-marriage96','S-0760','marriage','Adolf Fredrik E II/6, 1903 nr 96, s.196, bild 00028401_00199',[raw76,fix76]],
    ['R-C0028-15','S-0024','birth_baptism','Hyltinge C/8, 1920 nr 15, s.34, bild 00154522_00037',[raw28]],
    ['R-C0252-family','S-0199','owner_statement','Projektkonversation 2026-08-22 enligt C-0252',[raw252]]
  ];
  for(const [id,source,kind,locator,units] of records) {
    const assets=[];
    if(id==='R-C0075-29')assets.push({path:'genealogy/media/C-0075-riksarkivet-SE-ULA-10335-C6-bild-15-hulda-amalia-1877.jpg',region:'post 29 på helbild'});
    if(id==='R-C0094-85-86')assets.push({path:'genealogy/media/C-0094-riksarkivet-SE-ULA-10335-B2-bild-37-inflyttning-1874.jpg',region:'poster 85–86 på helbild'});
    if(id==='R-C0028-15')assets.push({path:'genealogy/media/C-0028-riksarkivet-SE-ULA-10422-C8-bild-37-sida-34.jpg',region:'post 15 på helbild'});
    add(id,'record',{source_id:source,record_type:kind,locator,dependence_note:id.startsWith('R-C0976')?'Lysningsbok och vigselbok tillhör samma registreringskedja, inte två oberoende händelsevittnen.':'Äldre citation och denna representation är samma forskningsunderlag.'},units,'Källpost avgränsad inom den äldre citationen.',{disposition:'recorded',assets});
  }
  add('TR-C0075','transcription',{record_id:'R-C0075-29',text:raw75.raw,reading_note:fix75.raw},[raw75,fix75],'Bevarar ursprunglig avskrift och läsgränser; ersätter inte Hogtorp[?] med slutsatsen Högtorp.',{disposition:'recorded',evidenceStatus:'TRANSCRIBED'});
  const mentions=[
    ['M-C0075-child','Hulda Amalia','dopbarn','P-0016'],
    ['M-C0075-father','Ålund, Per Albert','far; dräng','P-0110'],
    ['M-C0075-mother','Adela Amalia Urbom/Ulbom','mor; hustru','P-0111'],
    ['M-C0075-witness1','Fredr. Wilhelm Ålund','dopvittne; dräng','P-0113'],
    ['M-C0075-witness2','Anna Fredrica Blom','dopvittne; hans hustru','P-0114']
  ];
  for(const [id,name,role,p] of mentions) {
    add(id,'mention',{record_id:'R-C0075-29',name_literal:name,role_literal:role},[raw75,fix75],'Personomnämnande i den avgränsade posten, före identitetsbedömningen.',{disposition:'recorded',evidenceStatus:'TRANSCRIBED'});
    add('ID-'+id,'identity',{mention_id:id,person_id:p,decision:'accepted'},[section(p,'Identitet'),raw75],'Återanvänder aktens prövade sammanföring; detta är inte ett godkännande av samtliga gamla kontraktskrav.',{evidenceStatus:'CORROBORATED',evidence:evidence([id])});
  }
  function obs(id,record,mention,property,literal,value,units) {
    return add(id,'observation',{record_id:record,mention_id:mention,property,value_literal:literal,value_json:value},units,'Uppgift såsom källan har lästs, med råform och uttrycklig tolkningsgräns.',{disposition:'recorded',evidenceStatus:'TRANSCRIBED'});
  }
  obs('O-C0075-birth','R-C0075-29','M-C0075-child','birth_date','„ 25; september 1877',exact('1877-09-25'),[raw75,fix75]);
  obs('O-C0075-baptism','R-C0075-29','M-C0075-child','baptism_date','„ 30; september 1877',exact('1877-09-30'),[raw75,fix75]);
  obs('O-C0075-age','R-C0075-29','M-C0075-mother','age','27 / 28',{reading:'unresolved',alternatives:[27,28],selected:null,field:'dess sist fyllda ålders-år'},[raw75,fix75]);
  obs('O-C0075-residence','R-C0075-29','M-C0075-father','residence','dräng i Djupnäs',{name:'Djupnäs',role:'parents_residence',physical_birthplace_established:false},[raw75,fix75]);
  obs('O-C0075-witness-place','R-C0075-29','M-C0075-witness1','residence','Hogtorp[?]',{reading:'uncertain',literal:'Hogtorp[?]'},[raw75,fix75]);
  obs('O-C0075-churching','R-C0075-29','M-C0075-mother','churching_date','4/11[?]',{reading:'uncertain',literal:'4/11[?]'},[fix75]);
  obs('O-C0075-midwife','R-C0075-29','M-C0075-mother','birth_attendant','streck[?]',{reading:'uncertain',named_person:null},[fix75]);
  obs('O-C0094-place','R-C0094-85-86',null,'arrival_place','D:o [Högtorp]',{name:'Högtorp',folio:'170',persons_literal:'Fredr. Wilh. Ålund med hu',wife_named:false},[raw94,fix94]);
  obs('O-C0094-date','R-C0094-85-86',null,'arrival_date','ditto till 9/11 i post 80',exact('1874-11-09'),[fix94]);
  for(const [id,name] of [['PL-Gryt','Gryt'],['PL-Djupnas','Djupnäs'],['PL-Hogtorp','Högtorp']]) {
    add(id,'place',{name,jurisdiction:'Gryts församling, Södermanlands län',parent_id:id==='PL-Gryt'?null:'PL-Gryt'},id==='PL-Hogtorp'?[raw94,place75]:[raw75,fix75],'Ortsbegrepp, utan antagna koordinater eller byggnad.');
  }
  add('F-C0075-witness-place','fact',{subject_id:'M-C0075-witness1',property:'resolved_residence',value_type:'entity',value_json:'PL-Hogtorp'},[place75,assertion('A-7795')],
    'Samma man med hustru och församling i C-0094 1874 och C-0075 1877 ger Högtorp; slutsats från två källposter, inte en förbättrad råavskrift.',{evidenceStatus:'CORROBORATED',evidence:evidence(['O-C0075-witness-place','O-C0094-place']),caveat:'Avskriftens Hogtorp[?] står kvar oförändrad.'});
  add('F-P0016-parents-residence','fact',{subject_id:'P-0016',property:'parents_residence_at_birth',value_type:'entity',value_json:'PL-Djupnas'},[assertion('A-0391'),fix75],
    'A-0391 delas: föräldrarnas hemvist hålls skild från födelsehändelsens plats.',{evidenceStatus:'CORROBORATED',evidence:evidence(['O-C0075-residence']),caveat:'Fysisk förlossningsplats inte fastställd.'});
  add('E-P0016-birth','event',{event_type:'birth',date_json:exact('1877-09-25'),place_id:'PL-Gryt',place_role:'registered_parish'},[assertion('A-0391'),fix75],'Födelsedatumet bevaras; Gryt är församling, inte en belagd byggnad.',{evidenceStatus:'CORROBORATED',evidence:evidence(['O-C0075-birth']),caveat:'Djupnäs är föräldrahemvist; fysisk förlossningsplats inte säkert utskriven.'});
  add('E-P0016-baptism','event',{event_type:'baptism',date_json:exact('1877-09-30'),place_id:'PL-Gryt',place_role:'registered_parish'},[raw75,fix75],'Dopdatumet skiljs från moderns kyrkotagning.',{evidenceStatus:'TRANSCRIBED',evidence:evidence(['O-C0075-baptism'])});
  for(const [m,,,p] of mentions) {
    const role=m.endsWith('child')?'child':m.endsWith('father')?'father':m.endsWith('mother')?'mother':'witness';
    add('EP-baptism-'+p,'participation',{event_id:'E-P0016-baptism',person_id:p,mention_id:m,role},[raw75],
      'En gemensam doppost, med roll knuten till händelsen.',{evidenceStatus:'TRANSCRIBED',evidence:evidence(['E-P0016-baptism','ID-'+m])});
  }
  add('EP-birth-P0016','participation',{event_id:'E-P0016-birth',person_id:'P-0016',mention_id:'M-C0075-child',role:'child'},[assertion('A-0391')],'Huvudperson i födelsehändelsen.',{evidenceStatus:'CORROBORATED',evidence:evidence(['E-P0016-birth','ID-M-C0075-child'])});
  for(const [parent,mention] of [['P-0110','M-C0075-father'],['P-0111','M-C0075-mother']]) {
    add('REL-'+parent+'-P0016','relation',{from_person:parent,to_person:'P-0016',relation_type:'parent',nature:'recorded_parent',date_json:unknown()},[raw75,section('P-0016','Relationer')],'Riktningen är förälder till barn. Källans föräldrabeteckning görs inte till ett genetiskt test.',{evidenceStatus:'CORROBORATED',evidence:evidence(['ID-'+mention,'ID-M-C0075-child'])});
  }
  const moveDate={precision:'alternatives',literal:'ditto: 22/10, reservation för 23:e',values:['1902-10-22','1902-10-23'],preferred:'1902-10-22'};
  obs('O-C0979-departure','R-C0979-46',null,'departure_date','ditto från nr 42: ²²/₁₀; nr 47: ²³/₁₀',moveDate,[raw79,fix79]);
  obs('O-C0976-arrival','R-C0976-banns86',null,'registered_arrival_date','³⁰/₁₀ 02',exact('1902-10-30'),[raw76,fix76]);
  add('SEARCH-C0978-51-96','search',{question_id:null,source_id:'S-0343',scope_json:{description:'Hyltinge utflyttade 1902, endast poster 51–96',query:'Ålund / Hulda Amalia',bounds:{record_from:51,record_to:96,date_from:'1902-10-24',date_to:'1902-12-30',images:['00154512_00037','00154512_00038']}},outcome:'negative',body:assertion('A-3652').raw},[assertion('A-3652'),section('C-0978','Läst omfång och utfall')],
    'Nollet för det lästa intervallet är korrekt. En positiv post utanför intervallet upphäver inte observationen.',{disposition:'recorded',evidenceStatus:'NEGATIVE'});
  add('F-P0016-rejected-arrival-hypothesis','fact',{subject_id:'P-0016',property:'arrival_from_another_stockholm_parish_1902',value_type:'boolean',value_json:true},[assertion('A-3652'),assertion('A-3654'),section('C-0979','Rättelse')],
    'Den tidigare hypotesen är avvisad genom Hyltinge nr 46; själva söknollet är fortfarande giltigt.',{disposition:'rejected',evidenceStatus:'REJECTED',evidence:[...evidence(['SEARCH-C0978-51-96'],'context'),...evidence(['O-C0979-departure'],'contradicts')]});
  add('E-P0016-departure1902','event',{event_type:'registered_departure',date_json:moveDate,place_id:null,place_role:'Hyltinge till Stockholm, Adolf Fredrik'},[assertion('A-3654'),fix79],
    'Bokförd flytt med reserverad dag, skild från fysiskt resförlopp.',{evidenceStatus:'CORROBORATED',evidence:evidence(['O-C0979-departure']),caveat:'Rudstugan 41 är inte en säkert fastställd gatuadress; åtta dagar bevisar inte reslängd.'});
  add('EP-departure-P0016','participation',{event_id:'E-P0016-departure1902',person_id:'P-0016',mention_id:null,role:'migrant'},[assertion('A-3654')],'Återanvänder aktens identifikation av den egna flyttposten.',{evidenceStatus:'CORROBORATED',evidence:evidence(['E-P0016-departure1902'])});
  add('E-P0016-marriage1903','event',{event_type:'marriage',date_json:exact('1903-05-01'),place_id:null,place_role:'Adolf Fredriks kyrkobokföring; faktisk vigsellokal inte angiven'},[assertion('A-3646'),raw76,fix76],
    'Direkt vigselpost nr 96, med lysningsbokens korshänvisning. Samma registreringskedja.',{evidenceStatus:'CORROBORATED',evidence:evidence(['R-C0976-marriage96','R-C0976-banns86']),caveat:'Västmannagatan 72 är bostad, inte belagd vigsellokal.'});
  for(const p of ['P-0016','P-0532'])add('EP-marriage-'+p,'participation',{event_id:'E-P0016-marriage1903',person_id:p,mention_id:null,role:'spouse'},[raw76,fix76],'Namngiven part i vigseln.',{evidenceStatus:'CORROBORATED',evidence:evidence(['E-P0016-marriage1903'])});
  add('REL-P0016-P0532','relation',{from_person:'P-0016',to_person:'P-0532',relation_type:'spouse',nature:'marriage',date_json:exact('1903-05-01')},[assertion('A-3646')],'Äktenskapet är direkt belagt. Startdatum bevaras utan påhittat slutdatum.',{evidenceStatus:'CORROBORATED',evidence:evidence(['E-P0016-marriage1903'])});
  for(const parent of ['P-0016','P-0015'])add('REL-'+parent+'-P0007','relation',{from_person:parent,to_person:'P-0007',relation_type:'parent',nature:'recorded_parent',date_json:unknown()},[raw28,section('P-0007','Relationer')],
    'Förälder till Maj Amalia; varken förälder till den andra föräldern eller ett äktenskap mellan dem.',{evidenceStatus:'CORROBORATED',evidence:evidence(['R-C0028-15']),caveat:'Inget äktenskap mellan Hulda och Axel Edvard följer av barnets föräldrafält.'});

  const dup=section('P-0295','Identitet');
  request.mappings.push({id:'MAP-P0295-P0027',legacyId:'P-0295',target:'P-0027',type:'same_identity',unit:dup.id,rationale:dup.raw});
  add('IDENTITY-P0424-P0028','identity_resolution',{person_a:'P-0424',person_b:'P-0028',decision:'different_people'},[assertion('A-2423'),section('P-0424','Identitet')],
    'Skilda födelseposter, föräldrar, orter och personkedjor; avvisad sammanföring, inte avvisad verklig person.',{evidenceStatus:'CORROBORATED'});
  request.mappings.push({id:'MAP-P0424-not-P0028',legacyId:'P-0424',target:'P-0028',type:'rejected_identity',unit:assertion('A-2423').id,rationale:'Avvecklingsregistrets motsvarighet är här inte ett dubblettalias.'});
  const pcd=db.prepare("SELECT * FROM unit WHERE document_path='PROJECT-CONTROL.md' AND kind='section' AND section='PCD-2026-09-09-028'").get();
  if(!pcd)throw Error('Ägarbeslut saknas i den fasta basen');
  add('F-P0004-birth-owner','fact',{subject_id:'P-0004',property:'birth_date',value_type:'date',value_json:exact('1963-11-27')},[assertion('A-1553'),raw252,pcd],
    'Direkt självidentifikation och uttryckligt ägarbeslut; ingen ytterligare arkivkontroll krävs.',{evidenceStatus:'OWNER_CONFIRMED',evidence:evidence(['R-C0252-family']),caveat:'Privat familjeuppgift; ingen utökad information om nu levande hämtad.'});

  for(const p of PILOT_PEOPLE) {
    const profile=entity(p,'profile'), preface=profile.text.split(/(?=^## )/m)[0];
    const prefix=span(profile,0,Buffer.byteLength(preface),'profilens bevarade bedömningshuvud');
    add('ASSESSMENT-'+p,'assessment',{subject_id:p,criteria:'Befintlig person-research/v1; ursprungliga datum och kriterier i body',outcome:preface.match(/- Identitetsgranskning:\s*(.*)/)?.[1]??'Ej utskrivet',body:preface},[prefix],
      'Äldre registrerad bedömning återanvänds ordagrant, inte omprövad eller uppgraderad av importen.',{disposition:'recorded',origins:origins([prefix],'complete')});
    const questions=db.prepare("SELECT * FROM unit WHERE document_path=? AND kind='question' AND historical=0").all(profile.document_path);
    for(const q of questions) {
      const parsed=JSON.parse(q.parsed_json);
      add(q.legacy_id,'question',{subject_id:p,title:parsed.heading,outcome:parsed.fields['Slutsatsläge']??'Ej utskrivet',body:q.raw},[q],
        'Frågan och dess befintliga utfall återanvänds. Ingen ny körplan skapas i datamodellen.',{disposition:'recorded',origins:origins([q],'complete')});
    }
    const biography=section(p,'Biografisk sammanfattning');
    add('BIO-'+p,'narrative',{subject_id:p,title:'Biografisk sammanfattning',markdown:biography.raw},[biography],
      'Versionsbevarad tidigare biografi; ännu inte fullständigt styckekopplad till typade slutsatser.',{disposition:'recorded',origins:origins([biography],'complete')});
  }
  return request;
}
